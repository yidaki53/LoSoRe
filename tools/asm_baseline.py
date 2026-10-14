"""ASM->C baseline experiment: does a purpose-trained decompilation LLM beat
general-purpose qwen2.5-coder on OUR 16-bit real-mode DOS target?

Tests the two SoK (arXiv 2610.11556) claims empirically on liero-dos:

  A: llm4decompile-6.7b (End model, purpose-trained)    asm -> C
  B: qwen2.5-coder:14b (general-purpose)                asm -> C
  C: qwen2.5-coder:14b                                  Ghidra decomp-C -> C
  D: qwen2.5-coder:14b, draft.py's EXACT current prompt asm + decomp-C -> Pascal

  A vs B  -> purpose-built vs general model at same input/output language
  B vs C  -> SoK headline: pseudo-C-in beats assembly-in (same model both sides)
  D       -> current pipeline (Pascal; judged by draft._sanitize_pascal only --
             FPC is Docker-only and `make build` mutates targets/, so the
             Pascal arm is NOT compile-tested here)

All C arms compile with a Ghidra-typedef preamble (undefined1..8,
__cdecl16near, true/false) so the harness measures the MODEL's C, not
decompiler output-format noise. Two compile modes: strict (gnu99) then
lenient (gnu89, implicit decls allowed) -> "compile rate" counts strict+lenient;
failures are bucketed (nndecomp-style failure taxonomy).

Deterministic: temperature=0, stratified sample of --n functions across the
size distribution. Outputs + JSON + markdown -> reports/asm_baseline/.

Transport: ollama /api/generate (raw completion; llm4decompile is a BASE
model, not instruct, so no chat template). engine/draft.py's run_llm speaks
llama.cpp '/completion' and is left untouched.

Usage:  python3 tools/asm_baseline.py --target liero-dos [--n 12]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import statistics
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
import draft  # noqa: E402  (reuse _sanitize_pascal — the pipeline's own gate)

OLLAMA = "http://localhost:11434"
LLM4_MODEL_PREFIX = "llm4decompile"
QWEN_MODEL = "qwen2.5-coder:14b"
NUM_CTX = 8192
NUM_PREDICT = 1024
ASM_CAP = 6000  # chars of asm fed to A/B (D uses draft.py's 3000)

# Ghidra decompiler output-format preamble: PARSING artifacts of the
# decompiler's C dialect, not something the model should have to reproduce.
GHIDRA_PREAMBLE = """\
#include <stdint.h>
#include <stddef.h>
typedef unsigned char undefined1, byte, uchar;
typedef unsigned short undefined2, ushort, word;
typedef unsigned int undefined4;
typedef unsigned long undefined8;
typedef long long longlong;
typedef unsigned long long ulonglong;
typedef unsigned int uint;
typedef short int16;
#define __cdecl16near
#define __cdecl16far
#define __stdcall16near
#define __stdcall16far
#define __cdecl
#define __stdcall
#define __fastcall
#define __pascal
#define __near
#define __far
#define __interrupt
#define __declspec(x)
/* BSD/kernel types some models assume (not Ghidra, but harmless to accept) */
typedef unsigned char u_char;
typedef unsigned short u_short, u_int16;
typedef unsigned int u_int, u32, uint32;
typedef unsigned short uint16, ushort_t;
typedef unsigned char uint8;
#ifndef true
#define true 1
#define false 0
#endif
"""

# LLM4Decompile End prompt, verbatim from albertan017/LLM4Decompile README.
LLM4_PROMPT = "# This is the assembly code: \n {asm}\n # What is the source code? \n"

ASM_TO_C_PROMPT = (
    "Decompile this x86 16-bit real-mode DOS function (Ghidra instruction "
    "listing; segment:offset addresses) into one C function.\n"
    "RULES:\n"
    "- Output ONLY compilable C (C99): exactly one function definition, named "
    "exactly as the assembly label (e.g. FUN_1000_01a1).\n"
    "- Declare every local; calls to routines not shown may be used but must "
    "not be declared (implicit declaration is fine); preserve control flow "
    "and arithmetic exactly.\n"
    "- No markdown, no prose, no #include (use stdint types if needed), no "
    "Ghidra artifacts (unaff_*, DAT_* as code).\n\nASSEMBLY:\n{asm}\n"
)

DECOMP_REFINE_PROMPT = (
    "This is noisy Ghidra decompiler pseudocode of a 16-bit DOS function: it "
    "uses fake types (undefined1/undefined2), fake register-parameters "
    "(unaff_DS, in_*, out_*) and placeholder names (FUN_*, DAT_*, uVarN).\n"
    "Produce a single clean, COMPILABLE C function with the SAME semantics "
    "and the SAME FUN_* call names (external symbols keep their names). "
    "Remove Ghidra scaffolding: fold unaff_*/in_*/out_* away, declare every "
    "local, keep addresses as pointer casts. Output ONLY C, no markdown or "
    "prose.\n\nGhidra pseudocode:\n{decomp}\n"
)

# verbatim from engine/draft.py pascal branch (kept in sync manually)
DRAFT_PAS_PROMPT_HEAD = (
    "You are reconstructing the ORIGINAL Turbo Pascal 7 (16-bit real-mode DOS) "
    "source of a function. Given the disassembly and a C reference, output the "
    "Pascal it most likely came from.\nRULES:\n"
    "- Output ONLY Turbo Pascal 7 source: a single `procedure Name;` (or "
    "`function`) with a `begin ... end;` body. No markdown, no prose, no "
    "comments except brief ones.\n"
    "- It must compile standalone under {$MODE TP} with no undeclared "
    "identifiers. Use only standard TP7 types (Byte, Word, Integer, Boolean, "
    "Char, Pointer, String).\n"
    "- The C uses fake identifiers (FUN_xxxx, DAT_xxxx, uVarN) — replace them "
    "with plain Pascal locals/params; do not invent globals.\n"
    "- Preserve control flow and arithmetic exactly. If a construct has no "
    "clean Pascal form (e.g. a far call to another routine), call that "
    "routine by name; every sibling routine is ALREADY forward-declared, so "
    "DO NOT declare or define any other procedure/function.\n"
)


def ollama_generate(model: str, prompt: str, timeout: int = 900) -> str:
    """Raw completion via ollama /api/generate (no chat template)."""
    data = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": 0, "num_ctx": NUM_CTX,
                    "num_predict": NUM_PREDICT},
    }).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read()).get("response", "")


def ollama_unload(model: str) -> None:
    data = json.dumps({"model": model, "keep_alive": 0}).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=data,
                                 headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=60).read()
    except Exception:
        pass


def find_llm4_model() -> str:
    r = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if LLM4_MODEL_PREFIX in line.lower():
            return line.split()[0]
    sys.exit(f"FAIL: no '{LLM4_MODEL_PREFIX}' model in ollama (still pulling?)")


def asm_to_ops(asm_text: str) -> str:
    """Ghidra .s -> LLM4Decompile's <func>:\\nOPERATIONS format: drop the header
    comment and the segment:offset address column (their corpus has none)."""
    out = []
    for ln in asm_text.splitlines():
        if ln.lstrip().startswith(";"):
            continue
        ln = re.sub(r"^\s*[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}\s+", "", ln)
        if ln.strip():
            out.append(ln.rstrip())
    return "\n".join(out)


def compile_c(code: str, workdir: pathlib.Path, stem: str) -> tuple[str, str]:
    """(status, first_error); status in {strict, lenient, fail}."""
    f = workdir / f"{stem}.c"
    f.write_text(GHIDRA_PREAMBLE + "\n" + code)
    modes = [
        ("strict", ["-std=gnu99", "-Wno-error=implicit-function-declaration"]),
        # gnu89 + downgrades: GCC14+ made implicit decls errors by default
        ("lenient", ["-std=gnu89", "-Wno-implicit-function-declaration",
                     "-Wno-implicit-int"]),
    ]
    first_err = ""
    for status, flags in modes:
        r = subprocess.run(["gcc", *flags, "-fsyntax-only", "-w", str(f)],
                           capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            return status, ""
        if not first_err:
            errs = [l for l in r.stderr.splitlines() if "error" in l]
            first_err = errs[0] if errs else (r.stderr.strip().splitlines() or [""])[-1]
    return "fail", first_err


def bucket(err: str) -> str:
    for pat, name in [
        (r"implicit declaration", "implicit-func-decl"),
        (r"undeclared|unknown type name", "undeclared-ident"),
        (r"expected", "syntax"),
        (r"conflicting types|previous (?:declaration|implicit)", "type-conflict"),
        (r"void value not ignored", "void-value"),
        (r"incompatible|initialization", "incompatible-type"),
        (r"too many arguments", "arg-count"),
        (r"storage size|incomplete", "incomplete-type"),
    ]:
        if re.search(pat, err, re.I):
            return name
    return "other"


def extract_c(text: str) -> str:
    """Pull C out of markdown fences / prose the model may have added."""
    t = text.strip()
    if "```" in t:
        chunks = [c for c in t.split("```") if c.strip()]
        code = max(chunks, key=len)
        code = "\n".join(l for l in code.splitlines()
                         if l.strip().lower() not in ("c", "cpp", "c++"))
        t = code.strip()
    lines = t.splitlines()
    start = 0
    for i, ln in enumerate(lines):
        if re.match(r"\s*(#|typedef|void|int|char|short|long|unsigned|static|const|"
                    r"uint\d*|int\d*|bool\b|size_t|struct\s+\w+\s*\{|\w+\s*\()", ln):
            start = i
            break
    return "\n".join(lines[start:]).strip()


def stratified_pick(root: pathlib.Path, n: int) -> list[str]:
    sizes = sorted(
        ((p.stem, len(p.read_text().splitlines()))
         for p in (root / "asm").glob("FUN_*.s")
         if (root / "decomp" / f"{p.stem}.c").exists()),
        key=lambda x: x[1])
    if n >= len(sizes):
        return [s[0] for s in sizes]
    idx = sorted({round(i * (len(sizes) - 1) / (n - 1)) for i in range(n)})
    return [sizes[i][0] for i in idx]


def run_arm(arm: str, model: str, fns: list[str], root: pathlib.Path,
            outdir: pathlib.Path) -> list[dict]:
    asm_dir, dec_dir = root / "asm", root / "decomp"
    rows: list[dict] = []
    for f in fns:
        t0 = time.time()
        if arm == "A":
            prompt = LLM4_PROMPT.format(asm=asm_to_ops((asm_dir / f"{f}.s").read_text()))
        elif arm == "B":
            prompt = ASM_TO_C_PROMPT.format(asm=(asm_dir / f"{f}.s").read_text()[:ASM_CAP])
        elif arm == "C":
            prompt = DECOMP_REFINE_PROMPT.format(decomp=(dec_dir / f"{f}.c").read_text())
        else:  # D — draft.py's exact current pascal prompt
            prompt = (DRAFT_PAS_PROMPT_HEAD
                      + f"- The routine is named `{f}`; keep that exact name.\n\n"
                      f"ASSEMBLY:\n{(asm_dir / f'{f}.s').read_text()[:3000]}\n\n"
                      f"REFERENCE C (Ghidra, for meaning only):\n"
                      f"{(dec_dir / f'{f}.c').read_text()}")
        try:
            raw = ollama_generate(model, prompt)
        except Exception as e:  # load-timeout etc — record, don't crash the run
            rows.append({"fn": f, "arm": arm, "seconds": round(time.time()-t0, 1),
                         "compile": "fail", "error": f"transport: {e}",
                         "bucket": "transport", "has_func_def": False,
                         "has_ctrlflow": False, "chars": 0})
            print(f"  [arm {arm}] {f} TRANSPORT-FAIL {e}")
            continue
        dt = time.time() - t0
        adir = outdir / arm
        adir.mkdir(parents=True, exist_ok=True)
        if arm == "D":
            clean = draft._sanitize_pascal(raw)
            (adir / f"{f}.pas").write_text(clean or raw)
            rows.append({
                "fn": f, "arm": arm, "seconds": round(dt, 1),
                "sanitize_pass": bool(clean),
                "has_begin_end": bool(clean and "begin" in clean.lower()
                                      and "end;" in clean.lower()),
                "chars": len(clean or raw), "raw": raw,
            })
        else:
            (adir / f"{f}.raw.c").write_text(raw)
            code = extract_c(raw)
            status, err = compile_c(code, adir, f)
            rows.append({
                "fn": f, "arm": arm, "seconds": round(dt, 1),
                "compile": status, "error": err[:200], "bucket": bucket(err),
                "has_func_def": bool(re.search(r"\w+\s+\w+\s*\([^;]*\)\s*\{", code)),
                "has_ctrlflow": bool(re.search(r"\b(if|for|while|switch)\b", code)),
                "chars": len(code), "raw": raw,
            })
        print(f"  [arm {arm}] {f} {rows[-1].get('compile', rows[-1].get('sanitize_pass'))} {dt:.0f}s")
    return rows


def summarize(rows: list[dict]) -> str:
    md = ["| arm | model | input | out | n | strict | any-compile/sanitize | struct |",
          "|---|---|---|---|---|---|---|---|"]
    meta = {"A": ("llm4decompile-6.7b", "asm", "C"),
            "B": ("qwen2.5-coder:14b", "asm", "C"),
            "C": ("qwen2.5-coder:14b", "decomp-C", "C"),
            "D": ("qwen2.5-coder:14b", "asm+decomp-C", "Pascal")}
    for arm in "ABCD":
        rs = [r for r in rows if r["arm"] == arm]
        if not rs:
            continue
        model, inp, out = meta[arm]
        n = len(rs)
        if arm == "D":
            ok = sum(r.get("sanitize_pass", False) for r in rs)
            st = sum(r.get("has_begin_end", False) for r in rs)
            md.append(f"| {arm} | {model} | {inp} | {out} | {n} | — | "
                      f"{ok}/{n} ({100*ok//n}%) | {st}/{n} |")
        else:
            strict = sum(r.get("compile") == "strict" for r in rs)
            anyok = sum(r.get("compile") != "fail" for r in rs)
            st = sum(r.get("has_func_def") and r.get("has_ctrlflow") for r in rs)
            md.append(f"| {arm} | {model} | {inp} | {out} | {n} | {strict}/{n} | "
                      f"{anyok}/{n} ({100*anyok//n}%) | {st}/{n} |")
    md.append("\n**failure buckets (C arms)**\n")
    bk: dict[str, int] = {}
    for r in rows:
        if r["arm"] in "ABC" and r.get("compile") == "fail":
            bk[r["bucket"]] = bk.get(r["bucket"], 0) + 1
    md.append(", ".join(f"{k}={v}" for k, v in sorted(bk.items(), key=lambda x: -x[1]))
              or "none")
    t: dict[str, list] = {}
    for r in rows:
        t.setdefault(r["arm"], []).append(r["seconds"])
    md.append("\n**median seconds/call**\n")
    md.append(", ".join(f"{a}={statistics.median(v):.0f}" for a, v in sorted(t.items())))
    return "\n".join(md)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="liero-dos")
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--arms", default="ABCD")
    a = ap.parse_args()
    root = pathlib.Path("targets") / a.target
    outdir = pathlib.Path("reports") / "asm_baseline"
    for sub in "ABCD":
        (outdir / sub).mkdir(parents=True, exist_ok=True)
    llm4 = find_llm4_model()
    fns = stratified_pick(root, a.n)
    print(f"[asm_baseline] target={a.target} llm4={llm4} qwen={QWEN_MODEL}")
    print(f"[asm_baseline] {len(fns)} fns: {', '.join(fns)}")
    rows: list[dict] = []
    for arm in a.arms:
        model = llm4 if arm == "A" else QWEN_MODEL
        print(f"\n=== arm {arm} ({model}) ===")
        rows += run_arm(arm, model, fns, root, outdir)
        if arm == "A":
            ollama_unload(llm4)
    (outdir / "results.json").write_text(json.dumps(rows, indent=2))
    (outdir / "summary.md").write_text(summarize(rows) + "\n")
    print("\n" + summarize(rows))
    print(f"\n[asm_baseline] -> {outdir}/results.json, {outdir}/summary.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
