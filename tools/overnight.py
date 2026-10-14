"""Overnight experiment suite: 6h unattended, inspired by the 2026 AI-RE wave.

Prior art distilled (why each phase exists):
  - momo5502's MW2 decomp (500B+ tokens, ~90% byte-matched): a machine-checkable
    PASS/FAIL harness is the best feedback for agents; instructions decay over
    long generations so RESTATE the rules every iteration; throw bad code away
    (verifier-selected best-of-N) instead of salvaging it; a good harness makes
    cheaper models viable.
  - AutoDecompiler (arXiv 2606.16162): RL-trained multi-turn refinement with
    T_max=3 turns of compiler-error feedback beats single-shot (+15% behavioral
    executability). We test the *inference-time* part of this (no RL).
  - SM64DS 99.9% matching / DecLLM (ISSTA'25): compile-and-compare iteration.

Phases (each writes incremental JSON, crash-safe, self time-capped):
  E4  LoRA-finetune Qwen2.5-Coder-1.5B on liero(+dos) asm->Ghidra-C pairs,
      2 hyperparam configs, eval on the SAME 12 stratified liero-dos fns with
      the daytime compile gate. (tests: does target-specific finetuning beat
      scale? = the llm4decompile lesson, done on OUR data)
  E1  Multi-turn fix loop (AutoDecompiler-style) on all daytime FAILURES of
      arms A/B/C/D, up to 3 turns of gcc/sanitize feedback. E1a restates the
      full rules every turn (MW2 lesson), E1b only sends the error (ablation).
  E2  Verifier-selected best-of-N (N=4, temp 0.7) vs daytime temp=0 single
      shot, arms A/B/C. ("throw it away if it's bad")
  E3  Cheap-model sweep under the same gate: deepseek-coder:6.7b, phi4:14b,
      deepseek-coder-v2:16b on arms B/C. ("a good harness makes cheaper
      models viable")
  E5  Arm-C prompt ablation: ban Ghidra junk tokens (swi(/SBORROW/CONCAT/
      stack0x) explicitly -> does plausibility rise with compile rate?
  E6  Cross-experiment report: compile rates, pass@turn curves, junk-token
      and identifier-preservation metrics (compile != semantics; the metric
      gap is the point), -> reports/overnight/REPORT.md.

NO engine/ changes; imports tools/asm_baseline.py + engine/draft.py read-only.
Usage: python3 tools/overnight.py {e1|e2|e3|e4|e5|e6|all} [--smoke]
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import asm_baseline as ab  # noqa: E402  (read-only reuse of the daytime harness)

OUT = ROOT / "reports" / "overnight"
OUT.mkdir(parents=True, exist_ok=True)
TARGET = ROOT / "targets" / "liero-dos"

OLLAMA = "http://localhost:11434"
NUM_CTX = 8192
FIX_TURNS = 3          # AutoDecompiler T_max=3
BO_N = 4               # best-of-N samples
PHASE_BUDGET_S = {     # soft per-phase caps so one slow phase can't eat the night
    "e1": 50 * 60, "e2": 60 * 60, "e3": 80 * 60,
    "e4": 110 * 60, "e5": 30 * 60, "e6": 20 * 60,
}
SMOKE = "--smoke" in sys.argv
FNS = ab.stratified_pick(TARGET, 2 if SMOKE else 12)  # n>=2: pick divides by n-1

JUNK_RE = re.compile(
    r"swi\s*\(|SBORROW|SCARRY|CONCAT\d|stack0x|ram\[|seg\.|CPUI|LLVM|BASIC_BLOCK|"
    r"PCodeOp|\bOP_\w+|indirect_")
FUN_REF_RE = re.compile(r"\bFUN_[0-9a-fA-F]{4}_[0-9a-fA-F]+\b")


def log(msg: str) -> None:
    print(f"[overnight {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def heartbeat(phase: str, status: str, **extra) -> None:
    d = {"phase": phase, "status": status, "ts": time.time(), **extra}
    (OUT / "status.json").write_text(json.dumps(d, indent=2))


def load_json(path: pathlib.Path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def save_json(path: pathlib.Path, rows: list) -> None:
    path.write_text(json.dumps(rows, indent=2))  # atomic enough at this size


def gen(model: str, prompt: str, temp: float = 0.0, npx: int = 1024,
        tries: int = 2) -> str:
    """ollama /api/generate raw completion; deterministic-ish with temp=0."""
    data = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": temp, "num_ctx": NUM_CTX,
                    "num_predict": npx},
    }).encode()
    for i in range(tries):
        try:
            req = urllib.request.Request(
                OLLAMA + "/api/generate", data=data,
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=900) as resp:
                return json.loads(resp.read()).get("response", "")
        except Exception as e:
            if i == tries - 1:
                raise
            log(f"  gen retry {e}")
            time.sleep(30)


def unload_all() -> None:
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        for line in r.stdout.splitlines()[1:]:
            if line.split():
                ab.ollama_unload(line.split()[0])
    except Exception as e:
        log(f"  unload_all: {e}")


def c_call(model: str, prompt: str, f: str, workdir: pathlib.Path,
           temp: float = 0.0, arm: str = "") -> dict:
    """generate -> extract_c -> compile gate; returns a row."""
    t0 = time.time()
    workdir.mkdir(parents=True, exist_ok=True)
    try:
        raw = gen(model, prompt, temp=temp)
    except Exception as e:
        return {"fn": f, "arm": arm, "compile": "fail", "bucket": "transport",
                "error": f"transport: {e}", "seconds": round(time.time() - t0, 1),
                "raw": ""}
    code = ab.extract_c(raw)
    status, err = ab.compile_c(code, workdir, f)
    return {"fn": f, "arm": arm, "compile": status, "bucket": ab.bucket(err),
            "error": err[:200], "seconds": round(time.time() - t0, 1),
            "raw": raw, "code": code}


# ---------------------------------------------------------------- junk metrics
def junk_score(text: str) -> int:
    return len(JUNK_RE.findall(text))


def ident_preserved(ref: str, out: str) -> float:
    """Fraction of FUN_* names in the Ghidra reference that survive in output."""
    want = set(FUN_REF_RE.findall(ref)) - {"FUN_xxxx"}
    if not want:
        return 1.0
    have = set(FUN_REF_RE.findall(out))
    return round(len(want & have) / len(want), 3)


# -------------------------------------------------------------------- prompts
def base_prompt(arm: str, f: str) -> str:
    """Same construction as asm_baseline.run_arm (kept byte-identical on purpose)."""
    asm_dir, dec_dir = TARGET / "asm", TARGET / "decomp"
    if arm == "A":
        return ab.LLM4_PROMPT.format(asm=ab.asm_to_ops((asm_dir / f"{f}.s").read_text()))
    if arm == "B":
        return ab.ASM_TO_C_PROMPT.format(asm=(asm_dir / f"{f}.s").read_text()[:ab.ASM_CAP])
    if arm == "C":
        return ab.DECOMP_REFINE_PROMPT.format(decomp=(dec_dir / f"{f}.c").read_text())
    raise ValueError(arm)


RESTATE_RULES = (
    "REMINDER of the rules:\n"
    "- Output ONLY compilable C (C99): exactly one function definition named "
    "exactly as requested.\n"
    "- Declare every local; implicit declarations of unseen routines are fine.\n"
    "- Preserve control flow and arithmetic exactly.\n"
    "- No markdown, no prose, no #include, no Ghidra artifacts (unaff_*, DAT_* "
    "as code, swi(), SBORROW, CONCAT, stack0x).\n"
)


def fix_prompt(arm: str, f: str, prev_code: str, err: str,
               restate: bool) -> str:
    """AutoDecompiler-style turn: prev attempt + stage-aware diagnostic feedback."""
    head = base_prompt(arm, f)
    if restate:
        head += "\n" + RESTATE_RULES
    return (
        f"{head}\n"
        f"Your previous attempt FAILED the compile gate. gcc error:\n"
        f"  {err}\n"
        f"Previous attempt:\n```c\n{prev_code}\n```\n"
        f"Fix ONLY what is needed to compile; keep semantics identical. "
        f"Output the COMPLETE corrected function, C only, no markdown.\n"
    )


# ------------------------------------------------------------------- sanity db
def daytime(arm: str) -> dict[str, dict]:
    """fn -> daytime row for arm (from the rescored results.json)."""
    rows = load_json(ROOT / "reports" / "asm_baseline" / "results.json", [])
    return {r["fn"]: r for r in rows if r.get("arm") == arm}


# mirrors draft._sanitize_pascal's rejection rules, so arm D's fix loop can
# report WHICH rule the output broke (stage-aware diagnostic feedback).
PAS_REJECT_PATTERNS = [
    (r"^Missing (procedure|function) declaration with begin",
     "output is not a Pascal routine (no `procedure/function Name` + begin)"),
    (r"\bDAT_\w+", "contains undeclared Ghidra globals DAT_*"),
    (r"\bPCode\b|\bPop\b", "contains decompiler internals PCode/Pop"),
    (r"\b(unaff|in|out)_[A-Za-z]\w*", "contains register/param noise unaff_*/in_*/out_*"),
    (r"\b(AX|BX|CX|DX|SI|DI|SP|BP|ES|DS|CS|SS)\b", "contains raw register names"),
    (r"\b0x[0-9a-fA-F]+\b", "contains C-style 0x hex literals"),
    (r"\*\(|->", "contains C pointer syntax *(...) or ->"),
    (r"\b(uint|ushort|uchar|int|short|long|float|double|undefined)\d*\b",
     "contains C type names"),
]


def pas_reject_reason(text: str) -> str:
    t = text or ""
    if not t.strip():
        return "empty output"
    for pat, why in PAS_REJECT_PATTERNS:
        if re.search(pat, t, re.M if pat.startswith("^") else 0):
            return why
    if not re.search(r"^\s*(procedure|function)\s+[A-Za-z_]\w*", t, re.M | re.I):
        return "no procedure/function declaration line"
    if "begin" not in t.lower():
        return "no begin"
    return "rejected by the Pascal gate (unspecified rule)"


# =====================================================================  E1
# Multi-turn fix loop on daytime failures. E1a restates rules each turn
# (MW2 "instructions decay" lesson); E1b sends only the error (ablation).
def phase_e1() -> dict:
    outdir = OUT / "e1"
    outdir.mkdir(exist_ok=True)
    rows_path = outdir / "results.json"
    rows = load_json(rows_path, [])
    done = {(r["arm"], r["variant"], r["fn"], r["turn"]) for r in rows}
    t_start = time.time()
    heartbeat("e1", "running")

    model_for = {"A": ab.find_llm4_model(), "B": ab.QWEN_MODEL,
                 "C": ab.QWEN_MODEL, "D": ab.QWEN_MODEL}
    for arm in "ABCD":
        day = daytime(arm)
        fails = [f for f in FNS
                 if f in day and (
                     (arm == "D" and not day[f].get("sanitize_pass"))
                     or (arm != "D" and day[f].get("compile") == "fail"))]
        if not fails:
            continue
        model = model_for[arm]
        log(f"E1 arm {arm}: {len(fails)} daytime failures, model={model}")
        for variant, restate in (("a_restate", True), ("b_bare", False)):
            for f in fails:
                if arm == "D" and variant == "b_bare":
                    continue  # D has one variant; sanitize feedback is already minimal
                if time.time() - t_start > PHASE_BUDGET_S["e1"]:
                    log("E1 time budget exhausted")
                    heartbeat("e1", "budget-exhausted", rows=len(rows))
                    save_json(rows_path, rows)
                    return {"rows": len(rows), "budget": True}
                prev = (day[f].get("code")
                        or ab.extract_c(day[f].get("raw", "")) or "")
                if arm == "D":
                    prev = day[f].get("raw", "")  # D stores raw Pascal only
                if not prev:
                    prev = day[f].get("raw", "")
                err = day[f].get("error") or pas_reject_reason(prev)
                for turn in range(1, FIX_TURNS + 1):
                    key = (arm, variant, f, turn)
                    hit = [r for r in rows
                           if (r["arm"], r.get("variant", "a"), r["fn"],
                               r["turn"]) == key]
                    if hit:  # resume: adopt stored row, chain its feedback
                        r0 = hit[-1]
                        if r0["compile"] in ("strict", "lenient", "pass"):
                            break  # already recovered in a previous run
                        prev = r0.get("code") or r0.get("clean") or prev
                        err = r0.get("error", err)
                        continue
                    if arm == "D":
                        row = self_fix_d(model, f, prev, err, variant, turn)
                    else:
                        p = fix_prompt(arm, f, prev, err, restate)
                        wdir = outdir / f"{arm}{variant[0]}" / f
                        row = c_call(model, p, f, wdir, arm=arm)
                        row["turn"] = turn
                        row["variant"] = variant
                    rows.append(row)
                    save_json(rows_path, rows)  # incremental = crash-safe
                    log(f"  E1 {arm}/{variant} {f} turn{turn}: {row['compile']}")
                    if row["compile"] in ("strict", "lenient", "pass"):
                        best = row["compile"]
                        break
                    best = row["compile"]
                    prev = row.get("code") or row.get("clean") or prev
                    err = row.get("error", err)
    unload_all() if ab.find_llm4_model() != ab.QWEN_MODEL else None
    summary = e1_summarize(rows)
    (outdir / "summary.md").write_text(summary)
    heartbeat("e1", "done", rows=len(rows))
    return {"rows": len(rows)}


def self_fix_d(model: str, f: str, prev: str, err: str,
               variant: str, turn: int) -> dict:
    """Arm D: Pascal, gate = draft._sanitize_pascal. Feed back rejection reason."""
    import draft
    t0 = time.time()
    head = (ab.DRAFT_PAS_PROMPT_HEAD
            + f"- The routine is named `{f}`; keep that exact name.\n\n"
            f"ASSEMBLY:\n{(TARGET / 'asm' / f'{f}.s').read_text()[:3000]}\n\n"
            f"REFERENCE C (Ghidra, for meaning only):\n"
            f"{(TARGET / 'decomp' / f'{f}.c').read_text()}\n")
    prompt = (head
              + (RESTATE_RULES + "- Turbo Pascal 7 output only, `procedure "
                 f"{f};` with begin...end;.\n" if variant == "a_restate" else "")
              + f"\nYour previous attempt was REJECTED by the Pascal gate: {err}\n"
                f"Previous attempt:\n```pascal\n{prev}\n```\n"
                f"Fix it. Output ONLY corrected Turbo Pascal 7 source.\n")
    wdir = OUT / "e1" / "D" / f
    wdir.mkdir(parents=True, exist_ok=True)
    try:
        raw = gen(model, prompt)
    except Exception as e:
        return {"fn": f, "arm": "D", "variant": variant, "turn": turn,
                "compile": "fail", "bucket": "transport", "error": str(e)[:200],
                "seconds": round(time.time() - t0, 1), "raw": ""}
    clean = draft._sanitize_pascal(raw)
    (wdir / f"turn{turn}.pas").write_text(clean or raw)
    # machine-readable rejection reason for the next turn
    reason = pas_reject_reason(raw) if not clean else ""
    return {"fn": f, "arm": "D", "variant": variant, "turn": turn,
            "compile": "pass" if clean else "fail",
            "bucket": "sanitize" if not clean else "ok",
            "error": reason or "ok",
            "seconds": round(time.time() - t0, 1), "raw": raw,
            "clean": clean, "code": clean or raw}


def e1_summarize(rows: list) -> None:
    md = ["# E1 multi-turn fix loop (AutoDecompiler-style, no RL)\n",
          "| arm | variant | fn | final | turns used |",
          "|---|---|---|---|---|"]
    best: dict[tuple, str] = {}
    turns: dict[tuple, int] = {}
    for r in rows:
        k = (r["arm"], r.get("variant", "a"), r["fn"])
        turns[k] = max(turns.get(k, 0), r.get("turn", 1))
        if r["compile"] in ("strict", "lenient", "pass"):
            if k not in best:
                best[k] = r["compile"]
        else:
            best.setdefault(k, "fail")
    fixable = 0
    for k in sorted(best):
        md.append(f"| {k[0]} | {k[1]} | {k[2]} | {best[k]} | {turns[k]} |")
        if best[k] != "fail":
            fixable += 1
    md.append(f"\n{fixable}/{len(best)} daytime failures recovered by the loop.")
    by_arm: dict[str, list] = {}
    for k, v in best.items():
        by_arm.setdefault(k[0], []).append(v)
    md.append("\n**recovery by arm**\n")
    for arm, vs in sorted(by_arm.items()):
        md.append(f"- arm {arm}: {sum(v != 'fail' for v in vs)}/{len(vs)} recovered")
    (OUT / "e1" / "summary.md").write_text("\n".join(md) + "\n")


# =====================================================================  E2
# Verifier-selected best-of-N ("throw it away if it's bad", MW2 lesson).
# N=4 samples at temp=0.7, pick the FIRST strict-compile, else first lenient,
# else keep none. Compares against daytime temp=0 single-shot per arm.
def phase_e2() -> dict:
    outdir = OUT / "e2"
    outdir.mkdir(exist_ok=True)
    rows_path = outdir / "results.json"
    rows = load_json(rows_path, [])
    have = {(r["arm"], r["fn"], r["sample"]) for r in rows}
    t0 = time.time()
    heartbeat("e2", "running")
    llm4 = ab.find_llm4_model()
    for arm in "ABC":
        model = llm4 if arm == "A" else ab.QWEN_MODEL
        for f in FNS:
            for s in range(1 if SMOKE else BO_N):
                if (arm, f, s) in have:
                    continue
                if time.time() - t0 > PHASE_BUDGET_S["e2"]:
                    heartbeat("e2", "budget-exhausted", rows=len(rows))
                    save_json(rows_path, rows)
                    e2_summarize(rows)
                    return {"rows": len(rows), "budget": True}
                row = c_call(model, base_prompt(arm, f), f,
                             outdir / f"{arm}{f}" / f"s{s}", temp=0.7,
                             arm=f"{arm}:bon")
                row["sample"] = s
                rows.append(row)
                save_json(rows_path, rows)
                log(f"  E2 {arm} {f} sample{s}: {row['compile']}")
        if arm == "A":
            ab.ollama_unload(llm4)
    e2_summarize(rows)
    heartbeat("e2", "done", rows=len(rows))
    return {"rows": len(rows)}


def e2_summarize(rows: list) -> None:
    md = ["# E2 best-of-N (temp 0.7, verifier-picked)\n",
          "| arm | fn | best | samples (s0..) | day-temp0 |",
          "|---|---|---|---|---|"]
    day = {a: daytime(a) for a in "ABC"}
    by: dict[tuple, list] = {}
    for r in rows:
        by.setdefault((r["arm"], r["fn"]), []).append(r)
    for (arm, f), rs in sorted(by.items()):
        arm0 = arm.split(":")[0]          # rows carry "A:bon"; day table uses "A"
        comps = [r["compile"] for r in sorted(rs, key=lambda x: x["sample"])]
        best = ("strict" if "strict" in comps else
                "lenient" if "lenient" in comps else "fail")
        d = day.get(arm0, {}).get(f, {}).get("compile", "?")
        md.append(f"| {arm} | {f} | {best} | "
                  f"{','.join(c[:3] for c in comps)} | {d} |")
    md.append("\n**roll-up: any-compile rate per arm (BoN vs temp0)**\n")
    for arm0 in "ABC":
        rs_a = [r for r in rows if r["arm"].split(":")[0] == arm0]
        fns = {r["fn"] for r in rs_a}
        bon_ok = sum(
            1 for f in fns
            if any(r["compile"] != "fail" for r in rs_a if r["fn"] == f))
        day_ok = sum(1 for f in fns
                     if day[arm0].get(f, {}).get("compile") != "fail")
        md.append(f"- arm {arm0}: BoN {bon_ok}/{len(fns)} "
                  f"vs temp0 {day_ok}/{len(fns)}")
    (OUT / "e2" / "summary.md").write_text("\n".join(md) + "\n")


# =====================================================================  E3
# Cheap-model sweep under the SAME gate ("a good harness makes cheaper
# models viable", MW2 lesson). Arms B (asm->C) and C (decomp->C), temp=0.
E3_MODELS = ["deepseek-coder:6.7b", "phi4:14b", "deepseek-coder-v2:16b"]


def phase_e3() -> dict:
    outdir = OUT / "e3"
    outdir.mkdir(exist_ok=True)
    rows_path = outdir / "results.json"
    rows = load_json(rows_path, [])
    have = {(r["model"], r["arm"], r["fn"]) for r in rows}
    t0 = time.time()
    heartbeat("e3", "running")
    for model in E3_MODELS:
        for arm in "BC":
            for f in FNS:
                if (model, arm, f) in have:
                    continue
                if time.time() - t0 > PHASE_BUDGET_S["e3"]:
                    heartbeat("e3", "budget-exhausted", rows=len(rows))
                    save_json(rows_path, rows)
                    e3_summarize(rows)
                    return {"rows": len(rows), "budget": True}
                row = c_call(model, base_prompt(arm, f), f,
                             outdir / f"{model.split(':')[0]}{arm}" / f,
                             arm=f"{arm}")
                row["model"] = model
                rows.append(row)
                save_json(rows_path, rows)
                log(f"  E3 {model} {arm} {f}: {row['compile']}")
        ab.ollama_unload(model)
    e3_summarize(rows)
    heartbeat("e3", "done", rows=len(rows))
    return {"rows": len(rows)}


def e3_summarize(rows: list) -> None:
    day = {a: daytime(a) for a in "BC"}
    md = ["# E3 cheap-model sweep (same gate, temp 0)\n",
          "| model | arm | n | strict | any-compile | qwen14b-daytime |",
          "|---|---|---|---|---|---|"]
    combos = sorted({(r["model"], r["arm"]) for r in rows})
    for model, arm in combos:
        rs = [r for r in rows if r["model"] == model and r["arm"] == arm]
        n = len(rs)
        st = sum(r["compile"] == "strict" for r in rs)
        ok = sum(r["compile"] != "fail" for r in rs)
        dn = len(day[arm])
        dok = sum(1 for v in day[arm].values() if v.get("compile") != "fail")
        md.append(f"| {model} | {arm} | {n} | {st}/{n} | {ok}/{n} "
                  f"({100*ok//max(n,1)}%) | {dok}/{dn} |")
    (OUT / "e3" / "summary.md").write_text("\n".join(md) + "\n")


# =====================================================================  E5
# Arm-C prompt ablation: explicitly BAN Ghidra junk tokens (from the daytime
# qualitative audit: swi(0x35), SBORROW22, stack0xfffe, CONCAT11 transcribed
# into compilable-but-meaningless C). Does plausibility improve?
E5_PROMPT = ab.DECOMP_REFINE_PROMPT + (
    "HARD CONSTRAINTS (violations = failure):\n"
    "- NEVER emit Ghidra internal functions or macros: swi(), SBORROW*(), "
    "SCARRY*(), CONCAT*(), stack0x* pseudo-locals, ram/seg descriptors. "
    "Replace them with the real C operations they stand for "
    "(CONCAT2(a,b) -> ((uint16_t)a<<8)|b, overflow checks -> plain arithmetic).\n"
    "- unaff_DS etc. are NOT parameters: they are segment state; fold into "
    "far pointers or drop when unused.\n"
    "- Every address must appear as (type*)(seg*16+off) or a named global, "
    "never as a bare hex literal expression.\n"
)


def phase_e5() -> dict:
    outdir = OUT / "e5"
    outdir.mkdir(exist_ok=True)
    rows_path = outdir / "results.json"
    rows = load_json(rows_path, [])
    have = {r["fn"] for r in rows}
    t0 = time.time()
    heartbeat("e5", "running")
    for f in FNS:
        if f in have:
            continue
        if time.time() - t0 > PHASE_BUDGET_S["e5"]:
            break
        p = E5_PROMPT.format(decomp=(TARGET / "decomp" / f"{f}.c").read_text())
        row = c_call(ab.QWEN_MODEL, p, f, outdir / "C2" / f, arm="C2")
        ref = (TARGET / "decomp" / f"{f}.c").read_text()
        row["junk"] = junk_score(row.get("code", ""))
        row["ident"] = ident_preserved(ref, row.get("code", ""))
        rows.append(row)
        save_json(rows_path, rows)
        log(f"  E5 C2 {f}: {row['compile']} junk={row['junk']} id={row['ident']}")
    e5_summarize(rows)
    heartbeat("e5", "done", rows=len(rows))
    return {"rows": len(rows)}


def e5_summarize(rows: list) -> None:
    c_day = daytime("C")
    n = max(len(rows), 1)
    ok = sum(r["compile"] != "fail" for r in rows)
    st = sum(r["compile"] == "strict" for r in rows)
    day_ok = sum(1 for f in FNS if c_day.get(f, {}).get("compile") != "fail")
    day_junk = 0
    day_id = []
    for f in FNS:
        d = c_day.get(f, {})
        day_junk += junk_score(d.get("code") or d.get("raw") or "")
        ref = (TARGET / "decomp" / f"{f}.c").read_text()
        day_id.append(ident_preserved(ref, d.get("code") or d.get("raw") or ""))
    md = [
        "# E5 arm-C junk-token ablation (C2 = decomp->C + hard bans)\n",
        f"- C2 any-compile: {ok}/{len(rows)}  strict: {st}/{len(rows)}  "
        f"(daytime C: {day_ok}/{len(FNS)})",
        f"- mean junk tokens/output: C2 {round(sum(r['junk'] for r in rows)/n,1)}"
        f"  vs daytime C {round(day_junk/max(len(FNS),1),1)}",
        f"- mean ident preservation: C2 {round(sum(r['ident'] for r in rows)/n,2)}"
        f"  vs daytime C {round(sum(day_id)/max(len(day_id),1),2)}\n",
        "| fn | C2 compile | day C | junk C2 | junk day | id C2 | id day |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda x: x["fn"]):
        f = r["fn"]
        d = c_day.get(f, {})
        dj = junk_score(d.get("code") or d.get("raw") or "")
        di = ident_preserved((TARGET / "decomp" / f"{f}.c").read_text(),
                             d.get("code") or d.get("raw") or "")
        md.append(f"| {f} | {r['compile']} | {d.get('compile','?')} "
                  f"| {r['junk']} | {dj} | {r['ident']} | {di} |")
    (OUT / "e5" / "summary.md").write_text("\n".join(md) + "\n")


# =====================================================================  E4
# LoRA finetune of Qwen2.5-Coder-1.5B on OUR asm->Ghidra-C pairs, then eval
# on the held-out 12 with the same gate. Runs in /tmp/ftvenv (torch). We call
# tools/e4_finetune.py as a subprocess so overnight.py stays torch-free.
def phase_e4() -> dict:
    outdir = OUT / "e4"
    outdir.mkdir(exist_ok=True)
    vpy = pathlib.Path("/tmp/ftvenv/bin/python")
    if not vpy.exists():
        (outdir / "SKIPPED.md").write_text(
            "venv /tmp/ftvenv missing - finetune not attempted.\n")
        log("E4 SKIPPED: no /tmp/ftvenv")
        heartbeat("e4", "skipped")
        return {"skipped": True}
    unload_all()  # free VRAM: training must not fight ollama
    heartbeat("e4", "running")
    t0 = time.time()
    try:
        r = subprocess.run(
            [str(vpy), str(ROOT / "tools" / "e4_finetune.py"),
             "--budget-s", str(PHASE_BUDGET_S["e4"])],
            capture_output=True, text=True,
            timeout=PHASE_BUDGET_S["e4"] + 600,
            cwd=str(ROOT))
        (outdir / "train.log").write_text(
            r.stdout + "\n--- STDERR ---\n" + r.stderr)
        log(f"E4 exit={r.returncode} ({time.time()-t0:.0f}s)")
    except subprocess.TimeoutExpired as e:
        (outdir / "train.log").write_text(
            (e.stdout or b"").decode(errors="replace")
            + "\nTIMEOUT\n" + (e.stderr or b"").decode(errors="replace"))
        log("E4 TIMEOUT")
    heartbeat("e4", "done" if (outdir / "results.json").exists() else "failed",
              seconds=round(time.time() - t0, 1))
    return {"rows": len(load_json(outdir / "results.json", []))}


# =====================================================================  E6
def phase_e6() -> dict:
    heartbeat("e6", "running")
    parts = ["# Overnight report (6h autonomous run)\n",
             f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')}. "
             f"n={len(FNS)} stratified liero-dos functions, same gate as daytime "
             "(gcc -fsyntax-only strict->lenient; arm D = _sanitize_pascal).\n",
             "Method provenance: MW2/momo5502 lessons (machine-checkable gate, "
             "restate rules, throw-away regeneration, cheap-models-plus-harness), "
             "AutoDecompiler (arXiv 2606.16162) T_max=3 fix turns, "
             "SM64DS/DecLLM compile-and-compare iteration.\n"]
    day = ROOT / "reports" / "asm_baseline" / "summary.md"
    if day.exists():
        parts.append("\n## Daytime baseline (for comparison)\n\n" + day.read_text())
    for ex, title in [("e1", "E1 multi-turn fix loop"),
                      ("e2", "E2 verifier best-of-N"),
                      ("e3", "E3 cheap-model sweep"),
                      ("e4", "E4 LoRA finetune"),
                      ("e5", "E5 junk-token ablation")]:
        sm = OUT / ex / "summary.md"
        logf = OUT / ex / "train.log"
        parts.append(f"\n## {title}\n")
        if sm.exists():
            parts.append("\n" + sm.read_text())
        elif logf.exists():
            tail = logf.read_text()[-3000:]
            parts.append("\n(see train.log tail)\n```\n" + tail + "\n```\n")
        else:
            parts.append("\n(not run or produced no summary)\n")
    # headline verdict computed from whatever exists
    parts.append("\n## Headline deltas vs daytime\n")
    e1 = load_json(OUT / "e1" / "results.json", [])
    if e1:
        for arm in "ABCD":
            rs = [r for r in e1 if r["arm"] == arm]
            rec = sum(r["compile"] in ("strict", "lenient", "pass") for r in rs)
            parts.append(f"- E1 arm {arm}: {rec}/{len(rs)} failure-rows recovered "
                          f"by >=1 fix turn\n")
    e2 = load_json(OUT / "e2" / "results.json", [])
    if e2:
        for arm in "ABC":
            rs_a = [r for r in e2 if r["arm"].split(":")[0] == arm]
            fns = {r["fn"] for r in rs_a}
            ok = sum(1 for f in fns if any(
                r["compile"] != "fail" for r in rs_a if r["fn"] == f))
            parts.append(f"- E2 arm {arm}: BoN any-compile {ok}/{len(fns)}\n")
    e4 = load_json(OUT / "e4" / "results.json", [])
    if e4:
        for cfg in sorted({r.get("cfg", "?") for r in e4}):
            rs = [r for r in e4 if r.get("cfg") == cfg]
            ok = sum(r["compile"] != "fail" for r in rs)
            parts.append(f"- E4 {cfg}: any-compile {ok}/{len(rs)} "
                          f"(daytime B asm->C was 5/12, A was 6/12)\n")
    parts.append("\nReminder: compile != semantics. Arm-C-style outputs can "
                 "compile while transcribing Ghidra junk; dat-parity remains "
                 "the semantic arbiter (not run overnight; FPC/Docker gate).\n")
    (OUT / "REPORT.md").write_text("".join(parts))
    heartbeat("e6", "done")
    log("E6 -> reports/overnight/REPORT.md")
    return {"report": str(OUT / "REPORT.md")}


def main() -> int:
    arg = next((a for a in sys.argv[1:] if a.startswith("e")), "all")
    phases = {"e1": phase_e1, "e2": phase_e2, "e3": phase_e3,
              "e4": phase_e4, "e5": phase_e5, "e6": phase_e6}
    # order: inference experiments first (ollama VRAM), finetune after (torch),
    # report last. e4 unloads ollama itself; e6 is pure-local.
    order = ["e1", "e5", "e2", "e3", "e4", "e6"]
    todo = order if arg in ("all", "e") else [arg]
    log(f"overnight start: phases={todo} smoke={SMOKE} n={len(FNS)}")
    for p in todo:
        try:
            log(f"=== {p} ===")
            phases[p]()
        except Exception:
            import traceback
            log(f"PHASE {p} CRASHED:\n{traceback.format_exc()}")
            (OUT / f"{p}_CRASH.txt").write_text(traceback.format_exc())
            heartbeat(p, "crashed")
    log("overnight finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())







