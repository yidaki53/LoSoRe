"""e6_match.py — E6 matching-decomp pilot (Pascal-first, TP7). Part 1/2."""
from __future__ import annotations
import argparse, json, math, pathlib, re, subprocess, sys, time, urllib.request

from tools.asmcfg import parse_ghidra_asm, resolve_branch_target

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "targets" / "liero-dos"
OUT = ROOT / "reports" / "overnight6"
OLLAMA = "http://localhost:11434"
QWEN = "hf.co/mradermacher/llm4decompile-9b-v2-GGUF:Q4_K_M"
NUM_CTX = 8192
NUM_PREDICT = 1024

EVAL_FNS = ["FUN_1000_5e66","FUN_1e7d_018a","FUN_1ec2_00d0","FUN_1ec2_0d5d",
  "FUN_249c_0180","FUN_24dd_0548","FUN_24dd_2e94","FUN_24dd_3360",
  "FUN_24dd_3711","FUN_24dd_3ed3","FUN_24dd_4905","FUN_2971_65df"]

def say(m):
    print(f"[e6 {time.strftime('%H:%M:%S')}] {m}", flush=True)

def score_fn(fn: str) -> dict:
    txt = (TARGET / "asm" / f"{fn}.s").read_text(errors="replace").splitlines()
    body = [l for l in txt if not l.strip().startswith(";")]
    instrs = len(body)
    branches = sum(1 for l in body if re.search(r"JZ|JNZ|JCXZ|LOOP", l))
    jumps = sum(1 for l in body if re.search(r"JMP|CALLF?|RET", l))
    score = instrs + 3*branches + 2*jumps
    return {"fn": fn, "instrs": instrs, "branches": branches,
            "jumps": jumps, "score": score}

def score_all():
    rows = sorted([score_fn(f) for f in EVAL_FNS], key=lambda r: r["score"])
    for r in rows:
        print(f"{r['fn']:15s} score={r['score']:4d} instr={r['instrs']:4d}")
    return rows

def fn_context(fn: str) -> dict:
    asm = (TARGET / "asm" / f"{fn}.s").read_text(errors="replace")
    gp = TARGET / "decomp" / f"{fn}.c"
    ghidra = gp.read_text(errors="replace") if gp.exists() else ""
    decl = ""
    fwd = TARGET / "src" / "_forward.inc"
    if fwd.exists():
        for line in fwd.read_text(errors="replace").splitlines():
            if fn in line:
                decl = line.strip(); break
    callees = sorted(set(re.findall(r"CALLF?\s+(0x[0-9a-f:]+|FUN_\w+)", asm)))
    # Sibling signatures for every FUN_ callee (model must match arity exactly).
    sibsig = {}
    fwd = TARGET / "src" / "_forward.inc"
    if fwd.exists():
        for line in fwd.read_text(errors="replace").splitlines():
            m = re.match(r"\s*(procedure|function)\s+(FUN_\w+)(.*forward;)", line)
            if m:
                sibsig[m.group(2)] = line.strip()
    callers = []
    for s in (TARGET/"asm").glob("FUN_*.s"):
        if s.stem == fn: continue
        try: t = s.read_text(errors="replace")
        except OSError: continue
        if fn in t:
            callers.append(s.stem)
            if len(callers) >= 10: break
    globs = sorted(set(re.findall(r"\[0x[0-9a-fA-F]+\]", asm)))[:20]
    return {"asm": asm, "ghidra": ghidra, "decl": decl, "callees": callees,
            "callers": callers, "globals": globs, "sibsig": sibsig}

PROMPT = """You are reverse-engineering a Turbo Pascal 7 DOS program (Liero v1.33).
Write ONE Turbo Pascal 7 routine for {fn}.
First line EXACTLY: {decl}
Original assembly: {asm}
Ghidra C hint (do NOT copy C idioms): {ghidra}
Called by: {callers} / Calls: {callees} / Addrs: {globals}
Sibling signatures (call EXACTLY as declared, no invented return values):
{sibsig}
Rules: output ONLY the routine ending with 'end;'. Types Byte/Char/Word/Integer/Longint/Boolean/Pointer only. No Result var, no goto, no Exit(v). A procedure call is a STATEMENT (never ':='). A function call returns a value. Mem[]/MemW[] for absolute memory."""


# Few-shot examples from hand-decompiled gold standards
FEWSHOT_DIR = TARGET / "pascal"

def load_fewshot_examples(exclude_fn: str | None = None, max_examples: int = 5) -> str:
    """Load hand-decompiled Pascal files as few-shot examples for the LLM."""
    if not FEWSHOT_DIR.exists():
        return ""
    examples = []
    for pas_file in sorted(FEWSHOT_DIR.glob("FUN_*.pas")):
        fn = pas_file.stem
        if exclude_fn and fn == exclude_fn:
            continue
        if len(examples) >= max_examples:
            break
        asm_file = TARGET / "asm" / f"{fn}.s"
        asm_text = asm_file.read_text(errors="replace") if asm_file.exists() else "(no asm available)"
        pas_text = pas_file.read_text(errors="replace")
        examples.append(
            f"EXAMPLE — {fn}:\n"
            f"asm: {asm_text[:800]}\n"
            f"pascal:\n{pas_text}\n"
        )
    if not examples:
        return ""
    return "FEW-SHOT EXAMPLES (hand-decompiled gold standards — match this style):\n" + "\n".join(examples) + "\n---\n"

# CFG extraction (hardened referee)

def _is_branch(inst: str) -> bool:
    return bool(re.match(r"^(JMP|J[ACEGLOSPZB]|LOOP[ECZ]?|JCXZ|JECXZ|CALL|CALLF|RET|IRET|INT)", inst))

def _is_cond_branch(inst: str) -> bool:
    return bool(re.match(r"^(J[ACEGLOSPZB]|LOOP[ECZ]?|JCXZ|JECXZ)", inst))

def _is_call(inst: str) -> bool:
    return bool(re.match(r"^(CALL|CALLF)", inst))

def _is_ret(inst: str) -> bool:
    return bool(re.match(r"^(RET|IRET)", inst))

def cfg_from_ghidra_asm(text: str) -> dict:
    parsed = parse_ghidra_asm(text)
    return _cfg_from_lists(parsed["addrs"], parsed["insts"], parsed["segments"])

def cfg_from_objdump(text: str) -> dict:
    addrs: list[int] = []
    insts: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^\s*([0-9a-fA-F]+):\s+[0-9a-fA-F ]+\s+(\S+)", line)
        if not m:
            continue
        addr = int(m.group(1), 16)
        inst = m.group(2).upper()
        inst = re.sub(r"%[REGX]\d*$", "", inst)
        inst = re.sub(r"[QBLW]$", "", inst)
        addrs.append(addr)
        insts.append(inst)
    return _cfg_from_lists(addrs, insts)

def _cfg_from_lists(
    addrs: list[int],
    insts: list[str],
    source_segments: list[int | None] | None = None,
) -> dict:
    n = len(addrs)
    if source_segments is None:
        source_segments = [None] * n
    elif len(source_segments) != n:
        raise ValueError("source_segments must match the instruction count")
    if n == 0:
        return {"blocks": 0, "edges": 0, "cond": 0, "call": 0, "ret": 0,
                "sizes": [], "addrs": [], "insts": []}
    leader = set()
    leader.add(0)
    for i in range(n):
        inst = insts[i]
        if _is_branch(inst) or _is_call(inst) or _is_ret(inst):
            if i + 1 < n:
                leader.add(i + 1)
            t = resolve_branch_target(inst, source_segments[i])
            if t is not None:
                try:
                    j = addrs.index(t)
                    leader.add(j)
                except ValueError:
                    pass
    leaders = sorted(leader)
    block_id = [0] * n
    bid = 0
    li = 0
    for i in range(n):
        if li + 1 < len(leaders) and i == leaders[li + 1]:
            bid += 1
            li += 1
        block_id[i] = bid
    nblocks = bid + 1
    edges: set[tuple[int, int]] = set()
    cond_edges = 0
    calls = 0
    rets = 0
    sizes = [0] * nblocks
    for i in range(n):
        sizes[block_id[i]] += 1
        inst = insts[i]
        cur = block_id[i]
        if _is_branch(inst) or _is_call(inst) or _is_ret(inst):
            if i + 1 < n:
                edges.add((cur, block_id[i + 1]))
            t = resolve_branch_target(inst, source_segments[i])
            if t is not None:
                try:
                    j = addrs.index(t)
                    edges.add((cur, block_id[j]))
                    if _is_cond_branch(inst):
                        cond_edges += 1
                except ValueError:
                    pass
            if _is_call(inst):
                calls += 1
            if _is_ret(inst):
                rets += 1
    return {
        "blocks": nblocks,
        "edges": len(edges),
        "cond": cond_edges,
        "call": calls,
        "ret": rets,
        "sizes": sizes,
        "addrs": addrs,
        "insts": insts,
    }

def cfg_similarity(a: dict, b: dict) -> float:
    if a["blocks"] == 0 or b["blocks"] == 0:
        return 0.0
    bsim = min(a["blocks"], b["blocks"]) / max(a["blocks"], b["blocks"])
    esim = min(a["edges"], b["edges"]) / max(a["edges"], b["edges"]) if max(a["edges"], b["edges"]) > 0 else 1.0
    ac = a["cond"] / max(a["blocks"], 1)
    bc = b["cond"] / max(b["blocks"], 1)
    csim = 1.0 - abs(ac - bc)
    asig = (a["call"], a["ret"])
    bsig = (b["call"], b["ret"])
    ksim = 1.0 if asig == bsig else 0.5
    sa = sorted(a["sizes"])
    sb = sorted(b["sizes"])
    if len(sa) == 0 or len(sb) == 0:
        ssim = 0.0
    else:
        bins = [1, 2, 3, 5, 10, 20]
        def hist(sizes):
            h = [0] * (len(bins) + 1)
            for s in sizes:
                placed = False
                for i, b in enumerate(bins):
                    if s <= b:
                        h[i] += 1
                        placed = True
                        break
                if not placed:
                    h[-1] += 1
            tot = sum(h) or 1
            return [x / tot for x in h]
        ha, hb = hist(sa), hist(sb)
        dot = sum(x * y for x, y in zip(ha, hb))
        na = math.sqrt(sum(x * x for x in ha)) or 1
        nb = math.sqrt(sum(x * x for x in hb)) or 1
        ssim = dot / (na * nb)
    return round(0.3 * bsim + 0.25 * esim + 0.25 * csim + 0.1 * ksim + 0.1 * ssim, 3)

def ollama_gen(model: str, prompt: str, npx: int = NUM_PREDICT, timeout: int = 300) -> str:
    data = json.dumps({"model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": 0.0, "num_ctx": NUM_CTX, "num_predict": npx}}).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=data,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()).get("response", "")

def _c_to_pascal(text: str, fn: str) -> str:
    """Mechanical C -> Turbo Pascal 7 conversion for LLM4Decompile output."""
    t = text
    # Strip comments
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"//.*$", "", t, flags=re.M)
    lines = t.splitlines()
    # Header: void FUN_xxx() or type FUN_xxx(params)
    first = lines[0].strip() if lines else ""
    m = re.match(r"\s*(?:void|(\w+))\s+(\w+)\s*\(([^)]*)\)\s*$", first, re.I)
    if m:
        nm = m.group(2)
        is_void = re.match(r"\s*void\s+", first, re.I) is not None
        header = f"procedure {nm};" if is_void else f"function {nm}: Word;"
        body_lines = lines[1:]
    else:
        header = decl or f"procedure {fn};"
        body_lines = lines
    # Separate var declarations from statements
    var_decls = []
    stmts = []
    for line in body_lines:
        s = line.strip()
        if not s or s in ("{", "}"):
            continue
        # Match: type varname;  (C declaration)
        dm = re.match(r"\b(Byte|Char|Word|Integer|Longint|Boolean|int|char|void|unsigned|long)\s+(\w+)\s*;?", s, re.I)
        if dm:
            vtype = dm.group(1)
            vname = dm.group(2)
            vtype_map = {"char": "Byte", "int": "Integer", "void": "", "unsigned": "", "long": "Longint"}
            pt = vtype_map.get(vtype.lower(), vtype)
            if pt:
                var_decls.append(f"  {vname}: {pt};")
            continue
        stmts.append(s)
    # Build output
    out = [header]
    if var_decls:
        out.append("var")
        out.extend(var_decls)
    out.append("begin")
    brace_depth = 0
    for s in stmts:
        if s == "{":
            brace_depth += 1
            continue
        if s == "}":
            brace_depth -= 1
            if brace_depth <= 0:
                break
            continue
        # Type conversions in expressions
        s = re.sub(r"\bchar\b", "Byte", s, flags=re.I)
        s = re.sub(r"\bint\b", "Integer", s, flags=re.I)
        s = re.sub(r"\bvoid\b", "", s, flags=re.I)
        s = re.sub(r"\bunsigned\b", "", s, flags=re.I)
        s = re.sub(r"\blong\b", "Longint", s, flags=re.I)
        s = re.sub(r"\bbool\b", "Boolean", s, flags=re.I)
        # Pointer dereference
        s = re.sub(r"\*\(\s*wordptr\s*\)\s*\(\s*(0x[0-9a-fA-F]+)\s*\)", r"MemW[\1]", s, flags=re.I)
        s = re.sub(r"\*\(\s*byteptr\s*\)\s*\(\s*(0x[0-9a-fA-F]+)\s*\)", r"Mem[\1]", s, flags=re.I)
        # Turbo Pascal uses $hex not 0xhex
        s = re.sub(r"0x([0-9a-fA-F]+)", lambda m: "$" + m.group(1).upper(), s)
        # Logical operators
        s = s.replace("==", "=").replace("!=", "<>")
        s = s.replace("&&", " and ").replace("||", " or ")
        s = re.sub(r"!(\w)", r"not \1", s)
        # if (cond) -> if cond then ; also handle if cond then (no parens)
        s = re.sub(r"^if\s*\((.+)\)\s*$", r"if \1 then", s)
        s = re.sub(r"^if\s+(.+)\s+then\s*;?\s*$", r"if \1 then", s)
        # Assignment: var = expr -> var := expr
        s = re.sub(r"^(\w+)\s*=\s*(.+)$", r"\1 := \2", s)
        # MemW[addr] = val -> MemW[addr] := val
        s = re.sub(r"(MemW\[[^\]]+\])\s*=\s*(.+)$", r"\1 := \2", s)
        # Mem[addr] = val -> Mem[addr] := val
        s = re.sub(r"(Mem\[[^\]]+\])\s*=\s*(.+)$", r"\1 := \2", s)
        # Remove return;
        s = re.sub(r"\breturn\s*;?", "", s)
        # Skip printf
        if re.match(r"\s*printf", s, re.I):
            continue
        # Strip trailing semicolons and spaces
        s = s.rstrip(";").strip()
        if s:
            out.append(s + ";")
    # Close with end;
    out.append("end;")
    return "\n".join(out) + "\n"


def sanitize_pas(text: str, fn: str, decl: str) -> str:
    # Detect C-style output (LLM4Decompile model)
    first = text.strip().splitlines()[0] if text.strip() else ""
    if re.match(r"\s*(?:void|\w+)\s+\w+\s*\(\),?\s*$", first, re.I):
        return _c_to_pascal(text, fn)
    # Native Pascal output
    lines = text.splitlines()
    start = 0
    for i, l in enumerate(lines):
        if re.match(r"\s*(procedure|function)\s+" + re.escape(fn) + r"\b", l, re.I):
            start = i
            break
    else:
        for i, l in enumerate(lines):
            if re.match(r"\s*(procedure|function)\b", l, re.I):
                start = i
                break
    body = "\n".join(lines[start:])
    idxs = [m.start() for m in re.finditer(r"(?im)^\s*end\s*;\s*$", body)]
    if idxs:
        body = body[:idxs[-1]] + "end;\n"
    # Convert C type declarations to Pascal types in var block
    body = re.sub(r"\bint\b", "Integer", body)
    body = re.sub(r"\buint\b", "Word", body)
    body = re.sub(r"\bundefined4\b", "Longint", body)
    body = re.sub(r"\bqword\b", "Longint", body)
    body = re.sub(r"\bQWord\b", "Longint", body)
    body = re.sub(r"\bbyte_t\b", "Byte", body)
    body = re.sub(r"\bword_t\b", "Word", body)
    body = re.sub(r"\buint32_t\b", "Longint", body)
    return body.strip() + "\n"


def build_and_diff(fn: str, body: str, decl: str) -> dict:
    wdir = OUT / fn
    wdir.mkdir(parents=True, exist_ok=True)
    # Compile as a PROGRAM with sibling stubs + MemW declared.
    fwd = TARGET / "src" / "_forward.inc"
    stubs = fwd.read_text(errors="replace") if fwd.exists() else ""
    stubs = "\n".join(l for l in stubs.splitlines()
                       if fn not in re.findall(r"FUN_\w+", l))
    assigned = set(re.findall(r":=\s*(FUN_\w+)\s*[;(]", body))
    var_types = dict(re.findall(r"(?im)^\s*(\w+)\s*:\s*(Char|Byte|Word|Integer|Longint|Boolean)\s*;",
                                body))
    for callee in assigned:
        for i, l in enumerate(stubs.splitlines()):
            if re.match(r"\s*procedure\s+" + re.escape(callee) + r"\b", l):
                lhs = re.search(r"(\w+)\s*:=\s*" + re.escape(callee), body)
                t = var_types.get(lhs.group(1), "Word") if lhs else "Word"
                stubs_list = stubs.splitlines()
                stubs_list[i] = f"function {callee}: {t}; forward;"
                stubs = "\n".join(stubs_list)
                break
    impls = []
    for l in stubs.splitlines():
        m = re.match(r"\s*(procedure|function)\s+(\w+)(\(.*\))?(?::\s*(\w+))?; forward;", l)
        if m:
            kind, nm, params, rt = m.group(1), m.group(2), m.group(3) or "", m.group(4)
            if kind == "procedure":
                impls.append(f"procedure {nm}{params};\nbegin\nend;")
            else:
                zero = {"Boolean": "False", "Char": "#0", "Pointer": "nil"}.get(rt or "Word", "0")
                impls.append(f"function {nm}{params}: {rt or 'Word'};\nbegin\n{nm} := {zero};\nend;")
    impls = "\n".join(impls)
    memdecl = "var MemW: array[Word] of Word;\nvar Mem: array[0..65535] of Byte;\n"
    prog = ("{$MODE TP}\nprogram cand;\n" + memdecl + stubs + "\n" + impls
            + "\n" + body + "\nbegin\nend.\n")
    (wdir / f"{fn}_cand.pas").write_text(prog)
    try:
        r = subprocess.run(["docker", "run", "--rm", "-v", f"{wdir}:/src",
            "-w", "/src", "rev:dos-tp7", "fpc", "-Mtp", f"/src/{fn}_cand.pas"],
            capture_output=True, text=True, timeout=180)
        ok = (r.returncode == 0)
        err = (r.stderr + r.stdout)[-500:]
    except Exception as e:
        ok, err = False, f"docker-fail: {e}"
    
    # Hardened referee: objdump the binary, diff CFG + mnemonic histogram
    cfg_sim = 0.0
    hist_overlap = 0.0
    if ok:
        binpath = wdir / f"{fn}_cand"
        od = subprocess.run(["objdump", "-d", str(binpath)],
            capture_output=True, text=True, timeout=60)
        od_text = od.stdout
        cfg_cand = cfg_from_objdump(od_text)
        cfg_orig = cfg_from_ghidra_asm(
            (TARGET / "asm" / f"{fn}.s").read_text(errors="replace"))
        cfg_sim = cfg_similarity(cfg_cand, cfg_orig)
        # Mnemonic histogram: original asm vs compiled objdump asm
        from collections import Counter
        def hist(t):
            m = re.findall(r"\b(MOV|ADD|SUB|CMP|JMP|JZ|JNZ|CALL|CALLF|PUSH|POP|LEA|LES|SHL|SHR|XOR|OR|AND|RET|NOP|CWD|INT)\b", t)
            return Counter(m)
        h1, h2 = hist(cfg_orig["insts"] and " ".join(cfg_orig["insts"]) or ""), hist(od_text.upper())
        keys = set(h1) | set(h2)
        dot = sum(h1[k]*h2[k] for k in keys)
        n1 = math.sqrt(sum(v*v for v in h1.values())) or 1
        n2 = math.sqrt(sum(v*v for v in h2.values())) or 1
        hist_overlap = dot / (n1*n2)
    else:
        cfg_orig = cfg_from_ghidra_asm(
            (TARGET / "asm" / f"{fn}.s").read_text(errors="replace"))
    
    match_pct = round(100*(0.30*(1.0 if ok else 0.0) + 0.40*cfg_sim + 0.30*hist_overlap), 1)
    return {"compile_ok": ok, "error": err, "cfg_sim": cfg_sim,
            "hist_overlap": round(hist_overlap,3),
            "match_pct": match_pct}

def pilot(fn: str, attempts: int = 3, model: str = QWEN,
          hand_pas: str | None = None, few_shot: bool = False) -> dict:
    ctx = fn_context(fn)
    fdir = OUT / fn
    fdir.mkdir(parents=True, exist_ok=True)
    rows = []
    prev_err = ""
    # Few-shot preamble (gold-standard hand-decompiled examples)
    fewshot = load_fewshot_examples(exclude_fn=fn) if few_shot else ""
    # Hand-written Pascal mode: skip LLM, use provided file directly.
    if hand_pas:
        hp = pathlib.Path(hand_pas)
        if not hp.exists():
            say(f"{fn}: hand file {hand_pas} not found")
            return {"fn": fn, "rows": [], "best": 0.0}
        text = hp.read_text(errors="replace")
        body = sanitize_pas(text, fn, ctx["decl"])
        (fdir / "hand.pas").write_text(body)
        res = build_and_diff(fn, body, ctx["decl"])
        res.update({"attempt": 0, "seconds": 0.0, "hand": True})
        rows.append(res)
        say(f"{fn} hand: compile={res['compile_ok']} match={res['match_pct']}%")
        (fdir / "results.json").write_text(json.dumps(rows, indent=2))
        return {"fn": fn, "rows": rows,
                "best": max((r.get("match_pct",0) for r in rows), default=0.0)}
    for n in range(attempts):
        sibs = "\n".join(ctx["sibsig"].get(c, c) for c in ctx["callees"]
                         if c.startswith("FUN_")) or "none"
        prompt = fewshot + PROMPT.format(fn=fn, decl=ctx["decl"] or f"procedure {fn};",
            asm=ctx["asm"][:4000], ghidra=ctx["ghidra"][:3000],
            callers=", ".join(ctx["callers"]) or "none",
            callees=", ".join(ctx["callees"]) or "none",
            globals=", ".join(ctx["globals"]) or "none", sibsig=sibs)
        if prev_err:
            prompt += f"\nPrev attempt failed: {prev_err[:800]}\nFix ONLY that error.\n"
        say(f"{fn} attempt {n}: generating...")
        t0 = time.time()
        try:
            raw = ollama_gen(model, prompt)
        except Exception as e:
            rows.append({"attempt": n, "match_pct": 0.0, "compile_ok": False,
                         "error": f"gen-fail: {e}"}); continue
        body = sanitize_pas(raw, fn, ctx["decl"])
        (fdir / f"base_{n}.pas").write_text(body)
        res = build_and_diff(fn, body, ctx["decl"])
        res.update({"attempt": n, "seconds": round(time.time()-t0,1)})
        rows.append(res)
        say(f"{fn} attempt {n}: compile={res['compile_ok']} match={res['match_pct']}%")
        prev_err = "" if res["compile_ok"] else res["error"]
        if res["match_pct"] >= 95.0:
            break
    (fdir / "results.json").write_text(json.dumps(rows, indent=2))
    return {"fn": fn, "rows": rows,
            "best": max((r.get("match_pct",0) for r in rows), default=0.0)}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fn", default="FUN_24dd_0548")
    ap.add_argument("--attempts", type=int, default=3)
    ap.add_argument("--model", default=QWEN)
    ap.add_argument("--score-all", action="store_true")
    ap.add_argument("--panel", action="store_true", help="Run all EVAL_FNS")
    ap.add_argument("--hand", action="store_true", help="Use hand-written Pascal from targets/liero-dos/pascal/FUN_xxxx.pas")
    ap.add_argument("--few-shot", action="store_true", help="Include hand-decompiled gold standards as few-shot examples in LLM prompt")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.score_all:
        rows = score_all()
        (OUT / "scores.json").write_text(json.dumps(rows, indent=2))
        return 0
    if a.panel:
        results = []
        for fn in EVAL_FNS:
            say(f"PANEL: {fn}")
            hp = f"targets/liero-dos/pascal/{fn}.pas" if a.hand else None
            r = pilot(fn, a.attempts, a.model, hand_pas=hp, few_shot=a.few_shot)
            results.append(r)
            say(f"PANEL: {fn} best={r['best']}%")
        (OUT / "panel_results.json").write_text(json.dumps(results, indent=2))
        bests = [r["best"] for r in results]
        say(f"PANEL DONE: mean={sum(bests)/len(bests):.1f}% max={max(bests):.1f}% min={min(bests):.1f}%")
        return 0
    hp = f"targets/liero-dos/pascal/{a.fn}.pas" if a.hand else None
    r = pilot(a.fn, a.attempts, a.model, hand_pas=hp, few_shot=a.few_shot)
    print(json.dumps(r, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())


def _fix_types(src: str) -> str:
    """Convert C type names to Pascal types."""
    import re
    src = re.sub(r"\bregister\b", "", src)
    type_patterns = [
        (r"\b(uint)\b", " Word"),
        (r"\b(int)\b", " Integer"),
        (r"\b(undefined4)\b", " Longint"),
        (r"\b(qword|QWord)\b", " Longint"),
        (r"\b(byte_t)\b", " Byte"),
        (r"\b(word_t)\b", " Word"),
        (r"\b(uint32_t)\b", " Longint"),
    ]
    for pattern, replacement in type_patterns:
        src = re.sub(pattern, replacement, src)
    # Remove "var" keyword from var declarations, keep the variable name and type
    src = re.sub(r"^var\s+", "", src, flags=re.MULTILINE)
    # Clean up leading/trailing spaces on each line (preserve newlines)
    parts = src.split("\n")
    cleaned = []
    for part in parts:
        part = re.sub(r"^[ \t]+", "", part)
        part = re.sub(r"[ \t]+$", "", part)
        cleaned.append(part)
    src = "\n".join(cleaned)
    # Remove any standalone "var " left without declaration
    src = re.sub(r"^var\s*$", "", src, flags=re.MULTILINE)
    # Clean up multiple consecutive spaces within lines
    src = re.sub(r"[ \t]{2,}", " ", src)
    return src

def _fix_arity(src: str) -> str:
    """
Fix procedure/function arity - truncate surplus args and remove args from zero-param functions."""
    import re
    import pathlib
    # Try to find _forward.inc in various locations
    fwd_paths = [
        pathlib.Path(__file__).resolve().parent.parent / "reports" / "overnight6" / "src" / "_forward.inc",
        pathlib.Path(__file__).resolve().parent.parent / "src" / "_forward.inc",
        pathlib.Path(__file__).resolve().parent.parent / "targets" / "liero-dos" / "src" / "_forward.inc",
    ]
    funcs = {}
    for fwd in fwd_paths:
        if fwd.exists():
            for line in fwd.read_text(errors="replace").splitlines():
                m = re.match(r"function\s+(FUN_\w+)\(([^)]*)\);", line)
                if m:
                    fname = m.group(1)
                    params_str = m.group(2)
                    nparams = len([p for p in params_str.split(",") if p.strip()])
                    funcs[fname] = nparams
            break  # Use first found _forward.inc

    # Process function/procedure calls to fix arity
    # Find all FUN_* calls in source
    calls = re.findall(r"(FUN_\w+)\s*\(([^)]*)\),?\s*", src)
    for call_name, args_str in calls:
        if call_name in funcs:
            ndeclared = funcs[call_name]
            # Parse actual args
            if args_str.strip():
                arg_list = [a.strip() for a in args_str.split(",") if a.strip()]
            else:
                arg_list = []

            if ndeclared == 0:
                # Zero-param function: remove all args
                src = re.sub(
                    r"\b" + re.escape(call_name) + r"\([^)]*\)",
                    call_name + ";",
                    src,
                )
            elif len(arg_list) > ndeclared:
                # Truncate surplus args
                new_args = ", ".join(arg_list[:ndeclared])
                src = re.sub(
                    r"\b" + re.escape(call_name) + r"\([^)]*\)",
                    call_name + "(" + new_args + ")",
                    src,
                )
    return src


def _normalize_c_early(src: str) -> str:
    """Normalize C idioms early before Pascal matching."""
    import re
    # GCC inline-asm crumbs collapse away
    if re.match(r"^\s*__asm__", src):
        return ""
    if re.match(r'^"[^"]*\\n[^"]*"\s*;?\s*$', src):
        return ""
    # Strip storage-class keywords
    src = re.sub(r"\bregister\b\s*", "", src)
    # Scalar casts vanish: x = (int)y; -> x = y;
    src = re.sub(r"\(\s*(?:int|unsigned\s+short|unsigned|char|long|void)\s*\)", "", src)
    # for countdown sentinel: for (i = param_2; i; i--); -> for__countdown__i__param_2
    m = re.match(r"for\s*\(\s*(\w+)\s*=\s*(\w+)\s*;\s*\1\s*;\s*\1--\s*\)\s*;?\s*$", src)
    if m:
        return f"for__countdown__{m.group(1)}__{m.group(2)}"
    # Cast-pointer store with post-increment: *(Byte*)param_4++ = wDestLen;
    m = re.match(r"\*\(\s*Byte\s*\*\s*\)\s*(\w+)\s*\+\+\s*=\s*(.+);?\s*$", src)
    if m:
        return f"MemW[Word({m.group(1)})] := {m.group(2)}\nInc({m.group(1)})"
    # Deref load: wSrcLen = *(Byte*)param_3;
    m = re.match(r"(\w+)\s*=\s*\*\(\s*Byte\s*\*\s*\)\s*(\w+);?\s*$", src)
    if m:
        return f"{m.group(1)} = MemW[Word({m.group(2)})]"
    # Pointer bump compound assignment: param_4 += line_rem; -> Inc(param_4, line_rem)
    m = re.match(r"(\w+)\s*\+\=\s*(.+?);?\s*$", src)
    if m:
        return f"Inc({m.group(1)}, {m.group(2)})"
    # Standalone ++ / --
    m = re.match(r"^(\w+)\+\+\s*;?\s*$", src)
    if m:
        return f"Inc({m.group(1)})"
    m = re.match(r"^(\w+)--\s*;?\s*$", src)
    if m:
        return f"Dec({m.group(1)})"
    # Multiplication survives unchanged
    return src


def _strip_stmt_decls(src: str) -> str:
    """Remove C-style declarations leaked into the statement section."""
    import re
    lines = src.splitlines(keepends=True)
    out = []
    for line in lines:
        stripped = line.strip()
        # Match C-type declarations like "Word param_1;" or "Byte y2 = 3;"
        if re.match(r"^(?:Byte|Char|Word|Integer|Longint|Boolean)\s+\w+(?:\s*=\s*\d+)?\s*;\s*$", stripped):
            continue  # Skip this declaration line
        out.append(line)
    return "".join(out)


def region_outline(asm: str) -> str:
    """Outline natural loops in assembly code."""
    import re
    lines = asm.splitlines()
    if not lines or all(not l.strip() or l.strip().startswith(";") for l in lines):
        return "no loops available"
    # Parse instructions: seg:off  INSTR ...
    addrs = []
    insts = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        m = re.match(r"^([0-9a-fA-F]{4}):([0-9a-fA-F]{4})\s+(.+)$", line)
        if m:
            seg = int(m.group(1), 16)
            off = int(m.group(2), 16)
            addr = seg * 16 + off
            inst = m.group(3).upper()
            addrs.append(addr)
            insts.append(inst)
    if not addrs:
        return "no loops available"
    # Find back-edges: branch to an earlier address = loop header
    loop_headers = set()
    for i, inst in enumerate(insts):
        # Match all x86 branch instructions (JMP, Jcc, LOOP, JCXZ, JECXZ)
        if re.match(r"^(JMP|J[A-Z][A-Z0-9]|LOOP[ECZ]?|JCXZ|JECXZ)", inst):
            # Match segment:offset targets like 0x1000:5e9a (case-insensitive 0x prefix)
            t = re.search(r"0[xX]([0-9a-fA-F]+):([0-9a-fA-F]+)", inst)
            if t:
                try:
                    seg = int(t.group(1), 16)
                    off = int(t.group(2), 16)
                    target = seg * 16 + off
                    if target in addrs:
                        j = addrs.index(target)
                        if j <= i:
                            loop_headers.add(target)
                except ValueError:
                    pass
    # Cap at 40 loops
    headers = sorted(loop_headers)[:40]
    if not headers:
        return "no loops available"
    out = [f"loop@0x{h:04x}" for h in headers]
    out.insert(0, f"instrs={len(insts)}")
    return "\n".join(out)


def _declare_undeclared(body: str) -> str:
    """Add declarations for undeclared variables in a Pascal procedure body."""
    import re
    # Find var block
    var_block_match = re.search(r"(\nvar\s*)(.+?)(^\nbegin|\nbegin)", body, re.DOTALL | re.MULTILINE)

    # Collect already-declared variables in var block
    declared = set()
    if var_block_match:
        var_block = var_block_match.group(2)
        for m in re.finditer(r"^\s*(\w+)\s*:\s*(Char|Byte|Word|Integer|Longint|Boolean)\s*;", var_block, re.MULTILINE):
            declared.add(m.group(1).lower())

    # Variables to declare (known TP7 types only, skip known names)
    # Exclude names that are already params/procedure declarations
    names_to_declare = []
    skip_names = {"procedure", "function", "begin", "end", "var", "Word", "Byte", "Integer",
                  "Longint", "Char", "Boolean", "Mem", "MemW", "param"}
    for name in re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b", body):
        if name in skip_names:
            continue
        # Skip names that appear in procedure declarations like "proc Name(Param: Word);"
        # These are parameter declarations, not var declarations
        if name.lower() in declared:
            continue
        if name.startswith("FUN_") or name.startswith("Mem") or name == "Param":
            continue
        if name[0].isupper() and len(name) <= 4:
            continue
        # Skip if this is a param declaration pattern (Name: Type in procedure heading)
        # Check if this name appears as a parameter in a procedure/function declaration
        if re.search(r"\bprocedure\s+\w+\s*\([^)]*" + "(?<![a-zA-Z])" + re.escape(name) + "(?![a-zA-Z])" + r"[^)]*\)", body, re.I):
            continue
        if re.search(r"\bfunction\s+\w+\s*\([^)]*" + "(?<![a-zA-Z])" + re.escape(name) + "(?![a-zA-Z])" + r"[^)]*\)", body, re.I):
            continue
        names_to_declare.append(name)

    # Add declarations after var block header, without duplicating existing vars
    if names_to_declare:
        # Check if there's already a var block
        if var_block_match:
            # Add new declarations after the existing var block variables
            # but before "begin"
            new_decls = [name for name in names_to_declare if name.lower() not in declared]
            if new_decls:
                decl_line = "  " + "\n  ".join(f"{name}: Word;" for name in new_decls)
                # Insert after the var block, before "begin"
                body = re.sub(
                    r"(\nvar\s*)(.+?)(^\nbegin|\nbegin)",
                    rf"\1\2\n  {decl_line}\n\3",
                    body,
                    flags=re.DOTALL | re.MULTILINE
                )
        else:
            # No var block exists, add one with the new declarations
            decl_line = "  " + "\n  ".join(f"{name}: Word;" for name in names_to_declare)
            body = re.sub(
                r"(\nbegin)",
                rf"\2  {decl_line}\n",
                body,
                flags=re.DOTALL | re.MULTILINE
            )
    return body