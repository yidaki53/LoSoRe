"""diagnose silent drops: why functions end up as skeletons in src/.\n\nTwo modes, both offline by default:\n  1. batch analyzer (default)\n       python3 tools/diag_drop.py --target liero-dos --batch 60\n     Reads the *current* src/FUN_*.inc files and classifies each function into\n     SKELETON | NO_DECL | TRUNCATED | TOXIC | CLEAN, then prints a tally and\n     the top offenders with samples. No LLM calls.\n\n  2. online census (--online)\n       python3 tools/diag_drop.py --target liero-dos --batch 30 --online\n     Re-runs the LLM path for a small new batch and re-classifies the *raw*\n     LLM output, to confirm the offline on-disk distribution matches real\n     LLM behaviour (and pins down whether the root cause is prompt-,\n     sanitizer-, or gate-level).\n\nUsage:\n  python3 tools/diag_drop.py [--target SLUG] [--batch N] [--online] [--only-reason REASON]\n"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

repo_root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "engine"))

import draft  # noqa: E402

INC_RE = re.compile(r"^FUN_[0-9A-Fa-f]{4}(?:_[0-9A-Fa-f]{4})*$")
SKELETON_RE = re.compile(r"TODO: translate from asm", re.I)
DECL_RE = re.compile(r"^\s*(procedure|function)\s+[A-Za-z_]\w*", re.I)
END_RE = re.compile(r"end\s*;", re.I)
NO_END_RE = re.compile(r"end\s*\.", re.I)


def classify(content: str) -> str:
    """Classify one on-disk .inc into a silent-drop reason.

    Only the actual routine body (from the first `procedure|function`
    declaration line to EOF) is examined; the template header and the
    Ghidra-reference comment block are skipped so they never flag false
    positives.
    """
    if not content.strip():
        return "EMPTY"
    lines = content.splitlines()
    body_start = 0
    for i, ln in enumerate(lines):
        if re.match(r"^\s*(procedure|function)\s+[A-Za-z_]\w*", ln, re.I):
            body_start = i
            break
    body = "\n".join(lines[body_start:])
    if SKELETON_RE.search(body):
        return "SKELETON"
    if not body.strip():
        return "NO_DECL"
    # a routine declaration always preceded the body above, by construction
    if any(NO_END_RE.match(ln.strip()) for ln in reversed(body.splitlines()[:80])):
        return "TRUNCATED"
    if not END_RE.search(body):
        return "TRUNCATED"
    # residue in the body only (not in the reference comment block)
    if any(k in body for k in ("DAT_", "PCode", "unaff_", "->", "0x")):
        return "TOXIC"
    return "CLEAN"


def analyze(target: str, limit: int | None):
    """Return (tally, samples, files) for the current src/*.inc of a target."""
    root = pathlib.Path(f"targets/{target}")
    src = root / "src"
    files = sorted(src.glob("FUN_*.inc"))
    if limit is not None:
        files = files[:limit]
    tally: dict[str, int] = {}
    samples: dict[str, list[str]] = {}
    for f in files:
        content = f.read_text(errors="replace")
        reason = classify(content)
        tally[reason] = tally.get(reason, 0) + 1
        samples.setdefault(reason, []).append(f.name)
    return tally, samples, files


def _print(tally: dict[str, int], samples: dict[str, list[str]], total: int, target: str) -> None:
    print(f"[diag] classified {total} .inc files")
    for reason in sorted(tally, key=lambda k: -tally[k]):
        print(f"  {reason:12s} {tally[reason]:4d}  ({tally[reason]/total:.1%})")
    for reason, names in samples.items():
        if reason == "SKELETON":
            continue
        print(f"--- {reason} sample ({len(names)}) ---")
        for n in names[:3]:
            p = pathlib.Path(f"targets/{target}/src/{n}")
            try:
                txt = p.read_text(errors="replace")
            except Exception:
                continue
            print(f"    {n}: {txt[:80].replace(chr(10), ' | ')}")


def online_census(target: str, end: int, endpoint: str = "http://localhost:8080") -> None:
    """Re-run the LLM path on a small batch; classify raw LLM output."""
    from engine import draft as d
    root = pathlib.Path(f"targets/{target}")
    asm = root / "asm"
    fns = [p.stem for p in sorted(asm.glob("FUN_*.s"))]
    print(f"[diag:online] re-running LLM on fns[0:{end}] = {fns[:end]}")
    counts: dict[str, int] = {}
    lang, conf, compiler = d.detect_language(target)
    kind = d._yaml_kv(root / "config" / "target.yaml", "kind", "game")
    platform = d._yaml_kv(root / "config" / "target.yaml", "platform", "unknown")
    fs_prefix = d.fewshot_context(target, compiler, platform)
    for f in fns[:end]:
        decl = d._decl_for(root, f)
        seed_c = d.read_decomp_seed(root, f)
        asm_text = (asm / f"{f}.s").read_text(errors="replace")[:3000]
        refs = sorted({s for s in re.findall(r"\bFUN_[0-9A-Fa-f]{4}\w*\b", seed_c)
                       if s != f})[:12]
        sib_txt = ""
        if refs:
            rows = "\n".join(f"  {s}: {d._decl_for(root, s)}" for s in refs)
            sib_txt = ("Called routines are forward-declared with EXACTLY these "
                       "signatures - match arity and argument types when calling:\n"
                       + rows + "\n")
        prompt = (
            "You are reconstructing the ORIGINAL Turbo Pascal 7 (16-bit real-mode "
            "DOS) source of a function. Given the disassembly and a C reference, "
            "output the Pascal it most likely came from.\n"
            "- Output ONLY Turbo Pascal 7 source: a single `procedure Name;` (or "
            "`function`) with a `begin ... end;` body. No markdown, no prose, no "
            "comments except brief ones.\n"
            "- It must compile standalone under {$MODE TP} with no undeclared "
            "identifiers. Use only standard TP7 types (Byte, Word, Integer, "
            "Boolean, Char, Pointer, String).\n"
            "- The C uses fake identifiers (FUN_xxxx, DAT_xxxx, uVarN) - replace "
            "them with plain Pascal locals/params; do not invent globals.\n"
            "- Preserve control flow and arithmetic exactly. If a construct has no "
            "clean Pascal form (e.g. a far call to another routine), call "
            "that routine by name; every sibling routine is ALREADY forward-"
            "declared, so DO NOT declare or define any other procedure/function.\n"
            "- Raw/absolute memory: declare typed pointer variables (`p: ^Byte;`) "
            "and use `p^`, Inc(p, n); do not use Seg()/Ofs() and do not cast "
            "comparisons (Byte(x = 0) is invalid Pascal - write an `if`).\n"
            "- You may NOT dereference an expression: (p + n)^ and p^[i] on a "
            "non-array are ILLEGAL. Do q := p; Inc(q, n); first, then q^.\n"
            "- Keep value types exact: never assign Word/Integer to Char or vice "
            "versa - convert with Chr(n)/Ord(c)/Byte(x)/Word(x). The sibling "
            "signature table is authoritative for return types.\n"
            f"- The routine is named `{f}`. Its first line MUST be exactly:\n"
            f"    {decl}\n"
            "  Do not add, drop or rename parameters; read argument values only "
            "through these parameter names.\n"
            f"{sib_txt}"
            f"ASSEMBLY:\n{asm_text}\n\nREFERENCE C (Ghidra, for meaning only):\n{seed_c}\n"
        )
        llm_out = d.run_llm(prompt, None, endpoint)
        clean = d._sanitize_pascal(llm_out) if llm_out else ""
        if not clean:
            counts["NO_DECL/EMPTY"] = counts.get("NO_DECL/EMPTY", 0) + 1
            if not llm_out:
                counts["NO_OUTPUT"] = counts.get("NO_OUTPUT", 0) + 1
            else:
                counts["SANITIZE_STRIPPED"] = counts.get("SANITIZE_STRIPPED", 0) + 1
        else:
            counts["CLEAN"] = counts.get("CLEAN", 0) + 1
        print(f"  {f:16s} clean={len(clean):4d} chars  llm_len={len(llm_out or '')}")
    print("[diag:online] counts:", counts)


def _print_gate(tally: dict[str, int], total: int) -> None:
    print(f"[diag:gate-sim] simulated compile-gate revert on {total} .inc files")
    for reason in sorted(tally, key=lambda k: -tally[k]):
        print(f"  {reason:28s} {tally[reason]:4d}  ({tally[reason]/total:.1%})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="liero-dos")
    ap.add_argument("--batch", type=int, default=60)
    ap.add_argument("--online", action="store_true")
    ap.add_argument("--endpoint", default="http://localhost:8080")
    ap.add_argument("--gate-sim", action="store_true",
                    help="simulate the compile-gate's revert logic (no FPC run)")
    ap.add_argument("--only-reason", default=None)
    a = ap.parse_args()

    if a.online:
        online_census(a.target, a.batch, a.endpoint)
        return 0
    if a.gate_sim:
        tally = gate_sim(a.target, a.batch if a.batch else None)
        total = sum(tally.values())
        _print_gate(tally, total)
        return 0
    tally, samples, files = analyze(a.target, a.batch if a.batch else None)
    total = sum(tally.values())
    if a.only_reason:
        print(f"[diag] files matching {a.only_reason}:")
        for f in sorted(pathlib.Path(f"targets/{a.target}/src").glob("FUN_*.inc")):
            if classify(f.read_text(errors="replace")) == a.only_reason:
                print("  ", f.name)
        return 0
    _print(tally, samples, total, a.target)
    return 0


def gate_sim(target: str, limit: int | None) -> dict[str, int]:
    """Simulate the compile-gate's own revert logic on the *current* .inc files.

    This is the offline equivalent of `_compile_gate` (the only thing that
    actually turns an LLM draft into a skeleton), so it tells you what the gate
    would drop right now without re-running FPC.
    """
    root = pathlib.Path(f"targets/{target}")
    src = root / "src"
    files = sorted(src.glob("FUN_*.inc"))
    if limit is not None:
        files = files[:limit]
    tally: dict[str, int] = {}
    for f in files:
        content = f.read_text(errors="replace")
        lines = content.splitlines()
        # body = from the first routine declaration line to EOF
        body_lines = []
        for ln in lines:
            if re.match(r"^\s*(procedure|function)\s+[A-Za-z_]\w*", ln, re.I):
                body_lines = lines[lines.index(ln):]
                break
        body = "\n".join(body_lines)
        stripped = [ln for ln in body.splitlines() if ln.strip()]
        if not stripped:
            tally["EMPTY"] = tally.get("EMPTY", 0) + 1
            continue
        # 1) truncated: no closing end;
        if not stripped[-1].rstrip().endswith("end;"):
            tally["TRUNCATED(NOT END;)"] = tally.get("TRUNCATED(NOT END;)", 0) + 1
            continue
        # 2) TOXIC residue in the body only (skip the reference C comment block)
        if any(k in body for k in ("DAT_", "PCode", "unaff_", "->", "0x")):
            tally["TOXIC"] = tally.get("TOXIC", 0) + 1
            continue
        # 3) no routine declaration
        if not any(re.match(r"^\s*(procedure|function)\s+[A-Za-z_]\w*", ln, re.I)
                   for ln in body.splitlines()):
            tally["NO_DECL"] = tally.get("NO_DECL", 0) + 1
            continue
        tally["CLEAN"] = tally.get("CLEAN", 0) + 1
    return tally


if __name__ == "__main__":
    sys.exit(main())
