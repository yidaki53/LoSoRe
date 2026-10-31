"""e6_match.py — E6 matching-decomp pilot (Pascal-first, TP7). Part 1/2."""
from __future__ import annotations
import argparse, json, math, os, pathlib, re, subprocess, sys, time, urllib.request

# Ensure tools package is importable
_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from tools.pascal.tp7_fix import fix_pascal_tp7, auto_tp7_fix

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
TARGET = ROOT / "targets" / "liero-dos"
OUT = ROOT / "reports" / "overnight6"
OLLAMA = "http://localhost:11434"
QWEN = "hf.co/mradermacher/llm4decompile-9b-v2-GGUF:Q4_K_M"
NUM_CTX = 8192
NUM_PREDICT = 2048

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
Rules: output ONLY the routine ending with 'end;'. Types Byte/Char/Word/Integer/Longint/Boolean/Pointer only.
NO C-style 'void' keyword – use Pascal 'procedure FUN_name;' declaration.
NO 'function ... : Word' return types – use 'procedure' for void-returning routines.
NO C-style '//' comments – use block comments only.
NO type casts like 'Word(x)', 'Byte(x)' – declare variables in var section instead.
NO undeclared variables – ALL variables must be declared in the var section.
NO duplicate procedure/function identifiers – each FUN_ must have unique declaration.
NO missing begin/end; – output must have matching begin...end;.
NO C-style parameter lists – absolutely no (Byte b, Word w, ...) syntax. First line MUST be exactly 'procedure FUN_name;'. All parameters go in var section.
Mem[]/MemW[] for absolute memory."""


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

def _branch_target(inst: str) -> int | None:
    m = re.search(r"(?:0x)?([0-9a-fA-F]{4,})", inst)
    if m:
        try:
            return int(m.group(1), 16)
        except ValueError:
            return None
    return None


def normalize_inst(inst: str) -> str:
    """Normalize x86 instruction mnemonic for CFG comparison.

    Strips operand-size suffixes from mnemonics (MOVW->MOV, ADDL->ADD),
    normalizes register operands to REG, normalizes $immediate values to
    $IMM, and collapses conditional jumps (JZ/JE/JNZ/...) to JCC.
    Hex addresses are preserved so _branch_target() still works.
    """
    inst = inst.upper().strip()
    # Strip size suffix from mnemonic (first token)
    parts = inst.split(None, 1)
    if parts:
        mnemonic = parts[0]
        if len(mnemonic) > 2 and mnemonic[-1] in "WLQBD":
            mnemonic = mnemonic[:-1]
        if len(parts) > 1:
            inst = mnemonic + " " + parts[1]
        else:
            inst = mnemonic
    # Normalize register operands (%eax, AX, AL, SI, etc.)
    inst = re.sub(r"%\w+", "REG", inst)
    inst = re.sub(r"\b[A-D][BXCL]\b", "REG", inst)
    inst = re.sub(r"\b[SB][DP]\b", "REG", inst)
    # Normalize $immediate values (preserve bare hex addresses for branch targets)
    inst = re.sub(r"\$0[xX][0-9A-Fa-f]+", "$IMM", inst)
    inst = re.sub(r"\$\d+", "$IMM", inst)
    # Collapse conditional jumps to JCC
    inst = re.sub(r"\bJ(Z|E|NZ|NE|L|LE|G|GE|B|BE|A|AE|S|NS|P|NP|C|NC)\b",
                  "JCC", inst)
    return inst


def cfg_from_ghidra_asm(text: str, normalized: bool = False) -> dict:
    addrs: list[int] = []
    insts: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        m = re.match(r"^([0-9a-fA-F]{4}):([0-9a-fA-F]{4})\s+(.+)$", line)
        if not m:
            continue
        seg = int(m.group(1), 16)
        off = int(m.group(2), 16)
        addr = seg * 16 + off
        inst = m.group(3).upper()
        if normalized:
            inst = normalize_inst(inst)
        addrs.append(addr)
        insts.append(inst)
    return _cfg_from_lists(addrs, insts)

def cfg_from_objdump(text: str, normalized: bool = False) -> dict:
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
        if normalized:
            inst = normalize_inst(inst)
        addrs.append(addr)
        insts.append(inst)
    return _cfg_from_lists(addrs, insts)

def _cfg_from_lists(addrs: list[int], insts: list[str]) -> dict:
    n = len(addrs)
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
            t = _branch_target(inst)
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
            t = _branch_target(inst)
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
    # Aggressively remove any C-style 'void' keyword and convert to Pascal procedure
    text = re.sub(r'\bvoid\b', '', text, flags=re.I)
    # Convert C-style variable declarations to Pascal format
    # Comma-separated vars: Word var1, var2; -> var1, var2: Word;
    text = re.sub(r'Word\s+(\w+),\s*(\w+)\s*;', r'\1, \2: Word;', text)
    # Single variable: Word x; -> x: Word;
    text = re.sub(r'Word\s+(\w+)\s*;', r'\1: Word;', text)
    # Uppercased types case-insensitive: WORD x; / Word x; -> x: Word;
    text = re.sub(r'(?i)WORD\\s+(\\w+)\\s*;', r'\\1: Word;', text)
    # Strip markdown fences and backticks from LLM output
    text = re.sub(r'^\s*```', '', text, flags=re.M)
    text = re.sub(r'^\s*`', '', text, flags=re.M)
    text = re.sub(r'```$', '', text, flags=re.M)
    text = re.sub(r"'`", '', text)
    # Strip markdown fences and backticks
    text = re.sub(r'^\s*```', '', text, flags=re.M)
    text = re.sub(r'^\s*`', '', text, flags=re.M)
    text = re.sub(r'```$', '', text, flags=re.M)
    def _declare_undeclared(text: str) -> str:
        \"\"\"Add missing local variable declarations.\"\"\"
        var_refs = re.findall(r'\b(\w+)\s*:\s*(\w+);', text)
        declared = set(re.findall(r'(\w+):\s*(Word|Integer|Byte|Char|Boolean|Longint|Pointer);', text))
        for ref in var_refs:
            if ref not in declared:
                text += f'  {ref[0]}: Integer;'
        return text
    def _normalize_c_early(text: str) -> str:
        \"\"\"Normalize C constructs to Pascal types early.\"\"\"
        text = re.sub(r'\bint\s+(\w+)\b', r'\1: Integer;', text, flags=re.I)
        text = re.sub(r'\bchar\s+(\w+)\b', r'\1: Byte;', text, flags=re.I)
        text = re.sub(r'\blong\s+(\w+)\b', r'\1: Longint;', text, flags=re.I)
        text = re.sub(r'\bdouble\s+(\w+)\b', r'\1: Longint;', text, flags=re.I)
        text = re.sub(r'\bfloat\s+(\w+)\b', r'\1: Real;', text, flags=re.I)
        # Convert C style variable declarations to Pascal
        text = re.sub(r'(\w+)\s*,\s*(\w+)\s*;', r'\1, \2:', text)
        return text
    def _strip_stmt_decls(text: str) -> str:
        \"\"\"Remove C type leak declarations from statements.\"\"\"
        # Remove C-style type declarations that leak into statements
        # e.g., "int x;" or "char c;" should be removed or converted
        text = re.sub(r'\b(int|char|float|double|long)\s+\w+\s*;', '', text, flags=re.I)
        # Remove standalone type keywords that aren't Pascal declarations
        text = re.sub(r'^\s*(int|char|float|double|long)\s*$', '', text, flags=re.MULTILINE)
        return text
        \"\"\"Normalize C constructs to Pascal types early.\"\"\"
        # Convert C type declarations to Pascal equivalents
        text = re.sub(r'\bint\s+(\w+)\b', r'\\1: Integer;', text, flags=re.I)
        text = re.sub(r'\bchar\s+(\w+)\b', r'\\1: Byte;', text, flags=re.I)
        text = re.sub(r'\blong\s+(\w+)\b', r'\\1: Longint;', text, flags=re.I)
        text = re.sub(r'\bdouble\s+(\w+)\b', r'\\1: Longint;', text, flags=re.I)
        text = re.sub(r'\bfloat\s+(\w+)\b', r'\\1: Real;', text, flags=re.I)
        # Convert C style variable declarations to Pascal
        text = re.sub(r'(\w+)\s*,\s*(\w+)\s*;', r'\1, \2:', text)
        return text
        \"\"\"Add missing local variable declarations.\"\"\"
        var_refs = re.findall(r'\b(\w+)\s*:\s*(\w+);', text)
        declared = set(re.findall(r'(\w+):\s*(Word|Integer|Byte|Char|Boolean|Longint|Pointer);', text))
        for ref in var_refs:
            if ref not in declared:
                text += f'  {ref[0]}: Integer;'
        return text
        \"\"\"Truncate function arguments to first 3 parameters.\"\"\"
        # Find the function/declaration line and truncate args
        # Pattern: procedure/FunctionName(arg1, arg2, arg3, arg4, ...)
        # Keep only first 3 args
        m = re.match(r'\s*(procedure|function)\s+(\w+)\s*\(([^)]*)\)\s*;?\s*$', text, re.I)
        if m:\n        args = m.group(3)\n        arg_list = [a.strip() for a in args.split(',')]\n        # Keep only first 3 arguments\n        if len(arg_list) > 3:\n            arg_list = arg_list[:3]\n            new_args = ', '.join(arg_list)\n            text = text[:m.end(3)] + new_args + text[m.end(3):]\n        return text\s+(\w+)\s*;', r'\1: Word;', text)
    text = re.sub(r'\n\s*\n\s*end;\s*$', '\nend;', text, flags=re.I)
    # Balance begin/end: count begin vs end; and add missing end; if needed
    # Strip { } comments for counting
    text_no_comments = re.sub(r'\{[^}]*\}', '', text)
    begin_count = len(re.findall(r'\bbegin\b', text_no_comments))
    end_count = len(re.findall(r'\bend\b', text_no_comments))
    if begin_count > end_count:
        text = text.rstrip() + '\n' + 'end;' * (begin_count - end_count)
    # If no begin at all, add minimal begin...end;
    if begin_count == 0 and 'end;' not in text_no_comments:
        text = text.rstrip() + '\nbegin\nend;'
    # Ensure first line is proper Pascal declaration
    first = text.strip().split('\n')[0]
    if re.match(r'\s*(?:void|function)\s+', first, re.I):
        # Remove 'void' or 'function Type Name(' and replace with 'procedure Name;'
        first = re.sub(r'\bvoid\b', '', first, flags=re.I).strip()
        m = re.match(r'\s*function\s+\w+\s*\([^)]*\)\s*$', first, re.I)
        if m:
            first = re.sub(r'\s*function\s+\w+\s*\([^)]*\)\s*$', f'procedure {fn};', first, flags=re.I)
        m = re.match(r'\s*function\s+\w+\s*:\s*\w+\s*;?\s*$', first, re.I)
        if m:
            first = re.sub(r'\s*function\s+\w+\s*:\s*\w+\s*;?\s*$', f'procedure {fn};', first, flags=re.I)
    if not re.match(r'\s*procedure\s+\w+\s*;?\s*$', first, re.I):
        # Prepend procedure declaration if missing
        first = f'procedure {fn};'
    # Reconstruct text with fixed first line
    lines = text.strip().split('\n')
    lines[0] = first
    text = '\n'.join(lines)
    # Fix structural issue: end; must come AFTER begin;, not before
    # Detect and fix cases where end; appears before begin;
    lines = text.split('\n')
    # Find positions of end; and begin;
    end_positions = [i for i, line in enumerate(lines) if line.strip() == 'end;']
    begin_positions = [i for i, line in enumerate(lines) if line.strip() == 'begin']
    # If end; comes before begin;, swap them or reposition
    if end_positions and begin_positions and end_positions[0] < begin_positions[0]:
        # Move the first end; to after the first begin;
        new_lines = lines.copy()
        end_line = new_lines.pop(end_positions[0])
        # Insert end; after the first begin;
        insert_pos = begin_positions[0] + 1
        new_lines.insert(insert_pos, end_line)
        text = '\n'.join(new_lines)
    # Convert C-style var declarations "Type var1, var2;" to Pascal "var1, var2: Type;"
    # Handle multiple patterns: comma-separated vars, single var, uppercased types
    def _cstyle_to_pascal(m):
        vtypes = m.group(1).lower()
        vars_ = m.group(2).strip()
        # Handle comma-separated variables: "Word var1, var2;"
        if ',' in vars_:
            vars_list = [v.strip() for v in vars_.split(',')]
            result = [f'{v}: {vtypes};' for v in vars_list]
            return ' '.join(result)
        # Single variable: "Word x;"
        return f'  {vars_}: {vtypes};'
    # Pattern 1: Type var1, var2; (comma-separated)
    text = re.sub(r'^\s*(Byte|Char|Word|Integer|Longint|Boolean|Pointer)\s+([\w,\s]+?);\s*$',
                  _cstyle_to_pascal, text, flags=re.MULTILINE | re.IGNORECASE)
    # Pattern 2: Type single_var; (single variable, may be uppercased by LLM)
    text = re.sub(r'^\s*(Byte|Char|Word|Integer|Longint|Boolean|Pointer)\s+(\w+);\s*$',
                  lambda m: f'  {m.group(2).strip()}: {m.group(1).lower()};',
                  text, flags=re.MULTILINE | re.IGNORECASE)
    # Remove unmatched block comment braces: standalone { or } without a pair
    # Strip complete { ... } comments first
    text = re.sub(r'\{[^}]*\}', '', text)
    # Remove any remaining standalone { or }
    text = re.sub(r'\{', '', text)
    text = re.sub(r'\}', '', text)
    # Ensure var keyword precedes variable declarations after procedure header
    lines = text.split('\n')
    new_lines = []
    in_var_section = False
    prev_non_empty = ''
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Detect var declaration pattern: "name: Type;"
        if (stripped and ':' in stripped and stripped.endswith(';')
            and not stripped.startswith(('procedure', 'function', 'begin', 'end',
                                          'if', 'for', 'while', 'repeat', 'case',
                                          'var', 'const', 'type', 'label', 'else',
                                          'then', 'do', 'until', 'of', 'downto', 'to'))
            and not stripped.startswith('{')
            and not in_var_section
            and prev_non_empty != 'var'):
            # Check if this looks like a var declaration (x: Word; or x, y: Word;)
            if re.match(r'^[\w,\s]+:\s+(Byte|Char|Word|Integer|Longint|Boolean|Pointer);', stripped):
                new_lines.append('var')
                in_var_section = True
        # Track when we leave var section
        if stripped == 'begin':
            in_var_section = False
        if stripped:
            prev_non_empty = stripped
        new_lines.append(line)
    text = '\n'.join(new_lines)
    return text
def build_and_diff(fn: str, body: str, decl: str, normalized: bool = False) -> dict:
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
    # Add forward declarations for ALL callees called in the body (not just := assigned ones)
    all_callees = set(re.findall(r"\b(FUN_\w+)\s*\(", body))
    for callee in all_callees:
        already_declared = any(
            re.match(r"\s*(?:procedure|function)\s+" + re.escape(callee) + r"\b", l)
            for l in stubs.splitlines()
        )
        if not already_declared:
            stubs += "\nprocedure " + callee + "; forward;"
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
        cfg_cand = cfg_from_objdump(od_text, normalized=normalized)
        cfg_orig = cfg_from_ghidra_asm(
            (TARGET / "asm" / f"{fn}.s").read_text(errors="replace"),
            normalized=normalized)
        cfg_sim = cfg_similarity(cfg_cand, cfg_orig)
        # Mnemonic histogram: original asm vs compiled objdump asm
        from collections import Counter
        def hist(t):
            m = re.findall(r"\b(MOV|ADD|SUB|CMP|JMP|JZ|JNZ|CALL|CALLF|PUSH|POP|LEA|LES|SHL|SHR|XOR|OR|AND|RET|NOP|CWD|INT)\b", t)
            if normalized:
                m = [normalize_inst(x) for x in m]
            return Counter(m)
        h1_text = cfg_orig["insts"] and " ".join(cfg_orig["insts"]) or ""
        h2_text = od_text.upper()
        h1, h2 = hist(h1_text), hist(h2_text)
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
          hand_pas: str | None = None, few_shot: bool = False,
          auto_tp7: bool = False, normalized: bool = False) -> dict:
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
        if auto_tp7:
            say(f"{fn} running auto_tp7_fix() ...", )
            fix_result = auto_tp7_fix(body, fn)
            body = fix_result["fixed"]
            say(f"{fn} auto_tp7: compile={fix_result['compile_ok']} iterations={fix_result['iterations']}")
            if fix_result["error"]:
                say(f"{fn} auto_tp7 error: {fix_result['error'][:200]}")
            (fdir / "hand_tp7.pas").write_text(body)
        res = build_and_diff(fn, body, ctx["decl"], normalized=normalized)
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
        res = build_and_diff(fn, body, ctx["decl"], normalized=normalized)
        res.update({"attempt": n, "seconds": round(time.time()-t0,1)})
        rows.append(res)
        say(f"{fn} attempt {n}: compile={res['compile_ok']} match={res['match_pct']}%")
        prev_err = "" if res["compile_ok"] else res["error"]
        if res["match_pct"] >= 95.0:
            break
    (fdir / "results.json").write_text(json.dumps(rows, indent=2))
    return {"fn": fn, "rows": rows,
            "best": max((r.get("match_pct",0) for r in rows), default=0.0)}

def load_target_functions(target_slug: str) -> list:
    """Load function names from a target's functions.json."""
    fj = ROOT / "targets" / target_slug / "functions.json"
    if fj.exists():
        with open(fj) as f:
            data = json.load(f)
        return [fn["name"] for fn in data.get("functions", [])]
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fn", default="FUN_24dd_0548")
    ap.add_argument("--target", default="liero-dos", help="Target slug (e.g. liero-dos, stickman)")
    ap.add_argument("--attempts", type=int, default=3)
    ap.add_argument("--model", default=QWEN)
    ap.add_argument("--score-all", action="store_true")
    ap.add_argument("--panel", action="store_true", help="Run all EVAL_FNS for the target")
    ap.add_argument("--hand", action="store_true", help="Use hand-written Pascal from targets/<target>/pascal/FUN_xxxx.pas")
    ap.add_argument("--few-shot", action="store_true", help="Include hand-decompiled gold standards as few-shot examples in LLM prompt")
    ap.add_argument("--auto-tp7", action="store_true", help="Run auto_tp7_fix() (LLM + fpc -Mtp feedback loop) on hand-written .pas before build_and_diff")
    ap.add_argument("--normalized", action="store_true", help="Use normalized CFG scoring (normalize mnemonics before CFG comparison)")
    a = ap.parse_args()

    global TARGET, OUT, EVAL_FNS
    TARGET = ROOT / "targets" / a.target
    OUT = ROOT / "reports" / f"overnight_{a.target}"
    EVAL_FNS = load_target_functions(a.target) or ["FUN_24dd_0548"]

    OUT.mkdir(parents=True, exist_ok=True)
    if a.score_all:
        rows = score_all()
        (OUT / "scores.json").write_text(json.dumps(rows, indent=2))
        return 0
    if a.panel:
        results = []
        for fn in EVAL_FNS:
            say(f"PANEL: {fn}")
            hp = f"targets/{a.target}/pascal/{fn}.pas" if a.hand else None
            r = pilot(fn, a.attempts, a.model, hand_pas=hp, few_shot=a.few_shot,
                      auto_tp7=a.auto_tp7, normalized=a.normalized)
            results.append(r)
            say(f"PANEL: {fn} best={r['best']}%")
        (OUT / "panel_results.json").write_text(json.dumps(results, indent=2))
        bests = [r["best"] for r in results]
        say(f"PANEL DONE: mean={sum(bests)/len(bests):.1f}% max={max(bests):.1f}% min={min(bests):.1f}%")
        return 0
    hp = f"targets/{a.target}/pascal/{a.fn}.pas" if a.hand else None
    r = pilot(a.fn, a.attempts, a.model, hand_pas=hp, few_shot=a.few_shot,
              auto_tp7=a.auto_tp7, normalized=a.normalized)
    print(json.dumps(r, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())