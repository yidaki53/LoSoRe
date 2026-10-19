"""e6_match.py — E6 matching-decomp pilot (Pascal-first, TP7). Part 1/2."""
from __future__ import annotations
import argparse, json, pathlib, re, subprocess, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
TARGET = ROOT / "targets" / "liero-dos"
OUT = ROOT / "reports" / "overnight6"
OLLAMA = "http://localhost:11434"
QWEN = "qwen2.5-coder:14b"
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

def ollama_gen(model: str, prompt: str, npx: int = NUM_PREDICT, timeout: int = 300) -> str:
    data = json.dumps({"model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": 0.0, "num_ctx": NUM_CTX, "num_predict": npx}}).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=data,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()).get("response", "")

def sanitize_pas(text: str, fn: str, decl: str) -> str:
    lines = text.splitlines()
    start = 0
    for i, l in enumerate(lines):
        if re.match(r"\s*(procedure|function)\s+" + re.escape(fn) + r"\b", l, re.I):
            start = i; break
    else:
        for i, l in enumerate(lines):
            if re.match(r"\s*(procedure|function)\b", l, re.I):
                start = i; break
    body = "\n".join(lines[start:])
    idxs = [m.start() for m in re.finditer(r"(?im)^\s*end\s*;\s*$", body)]
    if idxs:
        body = body[:idxs[-1]] + "end;\n"
    return body.strip() + "\n"

def build_and_diff(fn: str, body: str, decl: str) -> dict:
    wdir = OUT / fn
    wdir.mkdir(parents=True, exist_ok=True)
    # Compile as a PROGRAM with sibling stubs + MemW declared (else every
    # lone unit fails on unknown identifiers — that measures the harness).
    fwd = TARGET / "src" / "_forward.inc"
    stubs = fwd.read_text(errors="replace") if fwd.exists() else ""
    # Drop ONLY the candidate's own forward decl (its body re-declares it).
    # Earlier substring matching dropped unrelated stubs (FUN_202c_0b*
    # prefixes) -> 'Forward declaration not solved' fatals. Exact match.
    stubs = "\n".join(l for l in stubs.splitlines()
                       if fn not in re.findall(r"FUN_\w+", l))
    # Promote procedure stubs the model ASSIGNS from (Ghidra mislabels some
    # AL-returning routines as void; the asm 'OR AL,AL after CALL' proves a
    # value is returned). Infer the return type from the assigned variable.
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
    # Empty bodies for every forward stub (else 'Forward declaration not
    # solved' fatals — the candidate only implements ONE routine).
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
    memdecl = "var MemW: array[Word] of Word;\n"
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
    orig = (TARGET / "asm" / f"{fn}.s").read_text(errors="replace")
    def hist(t):
        from collections import Counter
        m = re.findall(r"\b(MOV|ADD|SUB|CMP|JMP|JZ|JNZ|CALL|CALLF|PUSH|POP|LEA|LES|SHL|SHR|XOR|OR|AND|RET|NOP|CWD|INT)\b", t)
        return Counter(m)
    h1, h2 = hist(orig), hist(body.upper())
    keys = set(h1) | set(h2)
    import math
    dot = sum(h1[k]*h2[k] for k in keys)
    n1 = math.sqrt(sum(v*v for v in h1.values())) or 1
    n2 = math.sqrt(sum(v*v for v in h2.values())) or 1
    overlap = dot / (n1*n2)
    match_pct = round(100*(0.5*overlap + 0.5*(1.0 if ok else 0.0)), 1)
    return {"compile_ok": ok, "error": err, "asm_overlap": round(overlap,3),
            "match_pct": match_pct}

def pilot(fn: str, attempts: int = 3, model: str = QWEN) -> dict:
    ctx = fn_context(fn)
    fdir = OUT / fn
    fdir.mkdir(parents=True, exist_ok=True)
    rows = []
    prev_err = ""
    for n in range(attempts):
        sibs = "\n".join(ctx["sibsig"].get(c, c) for c in ctx["callees"]
                         if c.startswith("FUN_")) or "none"
        prompt = PROMPT.format(fn=fn, decl=ctx["decl"] or f"procedure {fn};",
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
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.score_all:
        rows = score_all()
        (OUT / "scores.json").write_text(json.dumps(rows, indent=2))
        return 0
    r = pilot(a.fn, a.attempts, a.model)
    print(json.dumps(r, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())

