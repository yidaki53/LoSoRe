"""Night-2 overnight suite (run 2): deeper finetunes + semantic audit.

Window: launch ~21:50 -> hard finish 06:00. Deadline guard before every
phase; F6 (report) always runs so REPORT2.md exists at wake-up.

Phase order (VRAM: ollama phases first, torch phases after unload_all):
  F1  cfgA-long: reload night-1 lora_cfgA, +4 epochs at seq 2048,
      eval on night-1's 12 (continuity) + fresh 60-fn panel.
  F2  cfgC-wide: fresh LoRA r=64/a=128, 3 epochs, seq 2048, same eval.
  F6a interim report (crash safety).
  F3  DUAL-JUDGE semantic audit (qwen14b + phi4, agreement required):
      every compiling output (F1, F2, daytime C) graded 1-5 vs its Ghidra
      reference + asm. both>=4 = real; either<=2 = junk; else contested.
  F4  arm-C prompt sweep: {junk-bans, +signature, +summary-first} x
      {qwen14b, phi4} on the 60-fn panel.
  F5  best-of-N (N=4, temp 0.7, verifier-picked) phi4 + qwen14b, arms
      B and C, 60 fns, budget-capped.
  F6  final REPORT2.md with promotion recommendations.

Anti-leakage: EXCLUDE = panel60 + night-1 12; both excluded from BOTH
targets' training sets. Night-1 artifacts (reports/overnight/*) are
read-only inputs, never overwritten. All night-2 output -> reports/overnight2/.

No engine/ changes. Run: python3 -u tools/overnight2.py all
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
import asm_baseline as ab  # noqa: E402

OUT = ROOT / "reports" / "overnight2"
OUT.mkdir(parents=True, exist_ok=True)
TARGET = ROOT / "targets" / "liero-dos"
NIGHT1 = ROOT / "reports" / "overnight"

OLLAMA = "http://localhost:11434"
NUM_CTX = 8192
DEADLINE_S = 7 * 3600 + 45 * 60   # stop starting new work; F6 still runs
PANEL_N = 60

t_start = time.time()
PHASE_BUDGET_S = {"f1": 150 * 60, "f2": 120 * 60, "f3": 60 * 60,
                  "f4": 75 * 60, "f5": 75 * 60, "f6": 10 * 60}

QWEN = "qwen2.5-coder:14b"
PHI = "phi4:14b"
LLM4_PREFIX = "llm4decompile"


def log(msg: str) -> None:
    print(f"[n2 {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def elapsed() -> float:
    return time.time() - t_start


def out_of_time() -> bool:
    return elapsed() > DEADLINE_S


def heartbeat(phase: str, status: str, **extra) -> None:
    (OUT / "status.json").write_text(json.dumps(
        {"phase": phase, "status": status, "ts": time.time(),
         "elapsed_min": round(elapsed() / 60, 1), **extra}, indent=2))


def load_json(path: pathlib.Path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def save_json(path: pathlib.Path, rows: list) -> None:
    path.write_text(json.dumps(rows, indent=2))


def night1_fns() -> list[str]:
    """The 12 stratified fns from night 1 (continuity reference)."""
    # prefer the COMPLETE daytime 12 (arm A has all fns; e1 only failures)
    rows = [r for r in load_json(ROOT / "reports" / "asm_baseline"
                                 / "results.json", []) if r.get("arm") == "A"]
    if rows:
        return sorted({r["fn"] for r in rows})
    return sorted({r["fn"] for r in
                   load_json(NIGHT1 / "e1" / "results.json", [])})


PANEL = ab.stratified_pick(TARGET, PANEL_N)          # fresh 60-fn panel
N1_FNS = night1_fns()                                  # night-1's 12
EXCLUDE = sorted(set(PANEL) | set(N1_FNS))            # never trained on
TRAIN_EXCLUDE_FILE = OUT / "exclude.txt"


def gen(model: str, prompt: str, temp: float = 0.0, npx: int = 1024,
        tries: int = 2) -> str:
    """ollama /api/generate raw completion with retry."""
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
            with urllib.request.urlopen(req, timeout=300) as resp:
                return json.loads(resp.read()).get("response", "")
        except Exception as e:
            if i == tries - 1:
                raise
            log(f"  gen retry: {e}")
            time.sleep(30)


def unload_all() -> None:
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        for line in r.stdout.splitlines()[1:]:
            if line.split():
                ab.ollama_unload(line.split()[0])
    except Exception as e:
        log(f"  unload_all: {e}")


def c_call(model: str, prompt: str, f: str, wdir: pathlib.Path,
           temp: float = 0.0, arm: str = "") -> dict:
    """generate -> extract_c -> compile gate (mkdir first: night-1 lesson)."""
    t0 = time.time()
    wdir.mkdir(parents=True, exist_ok=True)
    try:
        raw = gen(model, prompt, temp=temp)
    except Exception as e:
        return {"fn": f, "arm": arm, "compile": "fail", "bucket": "transport",
                "error": f"transport: {e}", "seconds": round(time.time()-t0, 1),
                "raw": ""}
    code = ab.extract_c(raw)
    status, err = ab.compile_c(code, wdir, f)
    return {"fn": f, "arm": arm, "compile": status, "bucket": ab.bucket(err),
            "error": err[:200], "seconds": round(time.time()-t0, 1),
            "raw": raw, "code": code}


# ------------------------------------------------------------- judge (F3)
JUDGE_PROMPT = """You are auditing a machine-generated C translation of a 16-bit
DOS x86 function. The Ghidra decompiler's own C output is the ground-truth
reference. Both are approximations of the original 8086 assembly.

Score the CANDIDATE's semantic fidelity to the reference:

SCORE: <1-5>
FLAWS: <semicolon-separated, max 3 short items>
CONFIDENCE: <high|medium|low>

Rules:
- 5 = control flow, arithmetic and memory accesses all match the reference
  (or match the ASSEMBLY where the reference itself is odd).
- 4 = matches except trivial naming/cosmetic differences.
- 3 = partially matches; some operations wrong or missing, overall shape right.
- 2 = mostly wrong: different control flow or wrong core computation.
- 1 = unrelated/hallucinated function.
- 16-bit segmented semantics (far pointers, segment regs) matter; dropping a
  far call the reference made caps the score at 2.
- Junk tokens (swi/SBORROW/CONCAT/stack0x) = automatic score 2.
- If the reference itself is unclear so you cannot tell, score 3 and write
  "contested" in FLAWS.
- Do NOT reward compilability; that was already checked elsewhere.

REFERENCE (Ghidra C):
{ref}

CANDIDATE (model output):
{cand}
"""


def judge_once(model: str, f: str, ref: str, cand: str) -> dict:
    asm = (TARGET / "asm" / f"{f}.s").read_text()[:2500]
    prompt = (JUDGE_PROMPT.format(ref=ref[:3000], cand=cand[:3000])
              + f"\nASSEMBLY (truncated, for tie-breaking only):\n{asm}\n")
    try:
        raw = gen(model, prompt, npx=300)
    except Exception as e:
        return {"score": None, "flaws": f"transport: {e}", "confidence": "none"}
    m = re.search(r"SCORE:\s*([1-5])", raw)
    flaws = re.search(r"FLAWS:\s*(.+)", raw)
    conf = re.search(r"CONFIDENCE:\s*(\w+)", raw)
    return {"score": int(m.group(1)) if m else None,
            "flaws": (flaws.group(1).strip()[:200] if flaws else ""),
            "confidence": (conf.group(1).lower() if conf else "?")}


def dual_verdict(s1: dict, s2: dict) -> str:
    """Agreement rule: both >=4 real; either <=2 junk; else contested."""
    a, b = s1.get("score"), s2.get("score")
    if a is None or b is None:
        return "judge-error"
    if a >= 4 and b >= 4:
        return "real"
    if a <= 2 or b <= 2:
        return "junk"
    return "contested"


# ============================================================ F1 / F2 (train)
VNV_PY = "/tmp/ftvenv/bin/python"


def run_train(variant: str, budget_s: int) -> None:
    """Shell out to the torch worker (keeps overnight2.py torch-free)."""
    outdir = OUT / variant
    outdir.mkdir(parents=True, exist_ok=True)
    TRAIN_EXCLUDE_FILE.write_text("\n".join(EXCLUDE))
    log(f"{variant}: launching f2_train.py (budget {budget_s//60}min, "
        f"{len(EXCLUDE)} stems excluded)")
    t0 = time.time()
    try:
        r = subprocess.run(
            [VNV_PY, str(ROOT / "tools" / "f2_train.py"),
             "--variant", variant, "--budget-s", str(budget_s),
             "--exclude-file", str(TRAIN_EXCLUDE_FILE),
             "--eval-f1", ",".join(N1_FNS),
             "--eval-panel", ",".join(PANEL)],
            capture_output=True, text=True,
            timeout=budget_s + 900, cwd=str(ROOT),
            env={**__import__("os").environ})
        (outdir / "train.log").write_text(
            r.stdout + "\n--- STDERR ---\n" + r.stderr)
        log(f"{variant}: exit={r.returncode} ({time.time()-t0:.0f}s)")
    except subprocess.TimeoutExpired as e:
        (outdir / "train.log").write_text(
            (e.stdout or b"").decode(errors="replace") + "\nTIMEOUT\n"
            + (e.stderr or b"").decode(errors="replace"))
        log(f"{variant}: TIMEOUT")


def phase_f1() -> None:
    heartbeat("f1", "running")
    unload_all()                      # free VRAM before torch
    run_train("f1", PHASE_BUDGET_S["f1"])
    heartbeat("f1", "done" if (OUT / "f1" / "results.json").exists()
              else "failed")


def phase_f2() -> None:
    heartbeat("f2", "running")
    unload_all()
    run_train("f2", PHASE_BUDGET_S["f2"])
    heartbeat("f2", "done" if (OUT / "f2" / "results.json").exists()
              else "failed")


# ============================================================ F4 (prompt sweep)
JUNK_BANS = (
    "HARD CONSTRAINTS (violations = failure):\n"
    "- NEVER emit Ghidra internals: swi(), SBORROW*(), SCARRY*(), CONCAT*(), "
    "stack0x* pseudo-locals, ram/seg descriptors. Replace them with the real "
    "C they stand for (CONCAT2(a,b) -> ((uint16_t)a<<8)|b).\n"
    "- unaff_DS etc. are segment state, not parameters: fold into far "
    "pointers or drop when unused.\n"
    "- Addresses appear as (type*)(seg*16+off) or a named global, never bare "
    "hex expressions.\n"
)


def f4_prompts(f: str) -> dict[str, str]:
    """Three arm-C variants, all building on night-1 E5's junk bans."""
    dec = (TARGET / "decomp" / f"{f}.c").read_text()
    sig = dec.strip().splitlines()[0] if dec.strip() else ""
    base = ab.DECOMP_REFINE_PROMPT.format(decomp=dec)
    return {
        "bans": base + JUNK_BANS,
        "sig": base + JUNK_BANS
        + f"\nThe function's Ghidra signature is: {sig}\n"
          "Keep parameter/return semantics consistent with it.\n",
        "sumfirst": base + JUNK_BANS
        + "\nFirst write ONE short comment line summarizing what the function "
          "does, then output the complete C function.\n",
    }


def phase_f4() -> None:
    outdir = OUT / "f4"
    outdir.mkdir(exist_ok=True)
    rows_path = outdir / "results.json"
    rows = load_json(rows_path, [])
    have = {(r["model"], r["variant"], r["fn"]) for r in rows}
    heartbeat("f4", "running")
    t0 = time.time()
    for model in (PHI, QWEN):
        for variant in ("bans", "sig", "sumfirst"):
            for f in PANEL:
                if (model, variant, f) in have:
                    continue
                if out_of_time() or time.time() - t0 > PHASE_BUDGET_S["f4"]:
                    log("F4 budget/deadline hit")
                    heartbeat("f4", "budget-exhausted", rows=len(rows))
                    f4_summarize(rows)
                    return
                p = f4_prompts(f)[variant]
                row = c_call(model, p, f, outdir / f"{model.split(':')[0]}_{variant}" / f,
                             arm=f"C4:{variant}")
                row["model"], row["variant"] = model, variant
                rows.append(row)
                save_json(rows_path, rows)
                log(f"  F4 {model} {variant} {f}: {row['compile']}")
        ab.ollama_unload(model)
    f4_summarize(rows)
    heartbeat("f4", "done", rows=len(rows))


def f4_summarize(rows: list) -> None:
    md = ["# F4 arm-C prompt sweep (60-fn panel)\n",
          "| model | variant | n | strict | any-compile |", "|---|---|---|---|---|"]
    for model in (PHI, QWEN):
        for variant in ("bans", "sig", "sumfirst"):
            rs = [r for r in rows if r["model"] == model and r["variant"] == variant]
            if not rs:
                continue
            st = sum(r["compile"] == "strict" for r in rs)
            ok = sum(r["compile"] != "fail" for r in rs)
            md.append(f"| {model} | {variant} | {len(rs)} | {st}/{len(rs)} | "
                      f"{ok}/{len(rs)} ({100*ok//len(rs)}%) |")
    (OUT / "f4" / "summary.md").write_text("\n".join(md) + "\n")


# ============================================================ F5 (best-of-N)
def phase_f5() -> None:
    outdir = OUT / "f5"
    outdir.mkdir(exist_ok=True)
    rows_path = outdir / "results.json"
    rows = load_json(rows_path, [])
    have = {(r["model"], r["arm"], r["fn"], r["sample"]) for r in rows}
    heartbeat("f5", "running")
    t0 = time.time()
    # priority order: phi arm C (E3's best), phi arm B, then qwen arm C
    plan = [(PHI, "C"), (PHI, "B"), (QWEN, "C"), (QWEN, "B")]
    for model, arm in plan:
        for f in PANEL:
            for s in range(4):
                if (model, arm, f, s) in have:
                    continue
                if out_of_time() or time.time() - t0 > PHASE_BUDGET_S["f5"]:
                    log("F5 budget/deadline hit")
                    heartbeat("f5", "budget-exhausted", rows=len(rows))
                    f5_summarize(rows)
                    return
                p = ab.DECOMP_REFINE_PROMPT.format(
                    decomp=(TARGET / "decomp" / f"{f}.c").read_text()) \
                    if arm == "C" else ab.ASM_TO_C_PROMPT.format(
                        asm=(TARGET / "asm" / f"{f}.s").read_text()[:ab.ASM_CAP])
                row = c_call(model, p, f,
                             outdir / f"{model.split(':')[0]}{arm}{f}" / f"s{s}",
                             temp=0.7, arm=arm)
                row["model"], row["sample"] = model, s
                rows.append(row)
                save_json(rows_path, rows)
                log(f"  F5 {model} {arm} {f} s{s}: {row['compile']}")
        ab.ollama_unload(model)
    f5_summarize(rows)
    heartbeat("f5", "done", rows=len(rows))


def f5_summarize(rows: list) -> None:
    md = ["# F5 best-of-N (temp 0.7, verifier-picked, 60-fn panel)\n",
          "single-shot references: night-1 E3 (12 fns) + F4 bans (60 fns)\n",
          "| model | arm | n | strict | BoN any-compile | BoN strict |",
          "|---|---|---|---|---|---|"]
    for model in (PHI, QWEN):
        for arm in ("B", "C"):
            fns = {r["fn"] for r in rows if r["model"] == model and r["arm"] == arm}
            if not fns:
                continue
            bon_ok = sum(1 for f in fns if any(
                r["compile"] != "fail" for r in rows
                if r["model"] == model and r["arm"] == arm and r["fn"] == f))
            bon_st = sum(1 for f in fns if any(
                r["compile"] == "strict" for r in rows
                if r["model"] == model and r["arm"] == arm and r["fn"] == f))
            md.append(f"| {model} | {arm} | {len(fns)} | — | {bon_ok}/{len(fns)} "
                      f"({100*bon_ok//len(fns)}%) | {bon_st}/{len(fns)} |")
    (OUT / "f5" / "summary.md").write_text("\n".join(md) + "\n")


# ============================================================ F3 (dual judge)
def f3_finish(rows: list, partial: dict, rows_path: pathlib.Path) -> None:
    """Pair qwen/phi partial rows -> verdicts; rewrite results + summary."""
    final = []
    for r in partial.values():
        q, p = r.get("qwen"), r.get("phi")
        if q and p:
            r["verdict"] = dual_verdict(q, p)
        else:
            r["verdict"] = "judge-error"
        final.append(r)
    save_json(rows_path, final)
    f3_summarize(final)


def phase_f3() -> None:
    outdir = OUT / "f3"
    outdir.mkdir(exist_ok=True)
    rows_path = outdir / "results.json"
    rows = load_json(rows_path, [])
    have = {(r["source"], r["fn"]) for r in rows}
    heartbeat("f3", "running")
    t0 = time.time()

    # gather compilable candidates: F1 cfgA2, F2 cfgC, night-1 daytime C
    targets: list[tuple[str, str, str]] = []   # (source, fn, code)
    for src, d, tag in (("cfgA2", OUT / "f1", "cfgA2"),
                        ("cfgC", OUT / "f2", "cfgC")):
        for r in load_json(d / "results.json", []):
            if r.get("compile") != "fail" and (r.get("code") or ""):
                targets.append((src, r["fn"], r["code"]))
    for r in load_json(ROOT / "reports" / "asm_baseline" / "results.json", []):
        if r.get("arm") == "C" and r.get("compile") != "fail":
            code = r.get("code") or ab.extract_c(r.get("raw", ""))
            if code:
                targets.append(("daytimeC", r["fn"], code))

    log(f"F3: {len(targets)} compilable candidates to judge (dual)")
    todo = [(src, f, code) for src, f, code in targets if (src, f) not in have]
    # judge-outer: ollama caches each model 5min; alternating judges per
    # candidate would reload both models hundreds of times.
    partial = {r["key"]: r for r in rows}   # key = src|fn
    for jmodel, jkey in ((QWEN, "qwen"), (PHI, "phi")):
        for src, f, code in todo:
            if out_of_time() or time.time() - t0 > PHASE_BUDGET_S["f3"]:
                log("F3 budget/deadline hit")
                heartbeat("f3", "budget-exhausted", rows=len(rows))
                f3_finish(rows, partial, rows_path)
                return
            ref = (TARGET / "decomp" / f"{f}.c").read_text()
            key = f"{src}|{f}"
            r = partial.setdefault(key, {"source": src, "fn": f, "key": key})
            r[jkey] = judge_once(jmodel, f, ref, code)
            save_json(rows_path, list(partial.values()))
            log(f"  F3[{jkey}] {src} {f}: {r[jkey]['score']}")
        ab.ollama_unload(jmodel)
    f3_finish(rows, partial, rows_path)
    f3_finish(rows, partial, rows_path)
    heartbeat("f3", "done", rows=len(rows))


def f3_summarize(rows: list) -> None:
    md = ["# F3 dual-judge semantic audit (qwen14b + phi4, agreement rule)\n",
          "verdict: both>=4 real; either<=2 junk; else contested\n",
          "| source | n judged | real | contested | junk | judge-error |",
          "|---|---|---|---|---|---|"]
    for src in ("cfgA2", "cfgC", "daytimeC"):
        rs = [r for r in rows if r["source"] == src]
        if not rs:
            continue
        c = {v: sum(r["verdict"] == v for r in rs)
             for v in ("real", "contested", "junk", "judge-error")}
        md.append(f"| {src} | {len(rs)} | {c['real']} | {c['contested']} | "
                  f"{c['junk']} | {c['judge-error']} |")
    md.append("\n**per-function**\n")
    md.append("| source | fn | qwen | phi | verdict | flaws(qwen) |")
    md.append("|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: (x["source"], x["fn"])):
        md.append(f"| {r['source']} | {r['fn']} | {r['qwen'].get('score')} | "
                  f"{r['phi'].get('score')} | {r['verdict']} | "
                  f"{r['qwen'].get('flaws','')[:80]} |")
    (OUT / "f3" / "summary.md").write_text("\n".join(md) + "\n")


# ============================================================ F6 (report)
def phase_f6() -> None:
    heartbeat("f6", "running")
    parts = ["# Night-2 overnight report (run 2)\n",
             f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')} after "
             f"{elapsed()/60:.0f} min. Panel = {len(PANEL)} stratified fns "
             f"(+{len(N1_FNS)} night-1 fns for continuity). "
             f"{len(EXCLUDE)} stems excluded from training on BOTH targets.\n",
             "Night-1 REPORT.md is the reference; this report only ADDS to it.\n"]
    for ex, title in [("f1", "F1 cfgA-long (reload +4 epochs, seq 2048)"),
                      ("f2", "F2 cfgC-wide (r=32, seq 1024)"),
                      ("f3", "F3 dual-judge semantic audit"),
                      ("f4", "F4 arm-C prompt sweep"),
                      ("f5", "F5 best-of-N")]:
        sm = OUT / ex / "summary.md"
        logf = OUT / ex / "train.log"
        parts.append(f"\n## {title}\n")
        if sm.exists():
            parts.append("\n" + sm.read_text())
        elif logf.exists():
            parts.append("\n(train.log tail)\n```\n"
                         + logf.read_text()[-2500:] + "\n```\n")
        else:
            parts.append("\n(not run)\n")
    parts.append("\n## Promotion recommendations\n")
    parts.append("- Compile != semantics: F3 is the arbiter for whether F1/F2 "
                 "compiles are real; trust dual-agreement verdicts only.\n"
                 "- F4/F5 deltas are vs night-1 single-shot; only promote to "
                 "engine/ with BOTH compile AND dual-judge agreement.\n")
    (OUT / "REPORT2.md").write_text("".join(parts))
    heartbeat("f6", "done")
    log("F6 -> reports/overnight2/REPORT2.md")


def main() -> int:
    phases = {"f1": phase_f1, "f2": phase_f2, "f3": phase_f3,
              "f4": phase_f4, "f5": phase_f5, "f6": phase_f6}
    order = ["f1", "f2", "f6", "f3", "f4", "f5"]  # f6 twice: interim+final
    arg = next((a for a in sys.argv[1:] if a.startswith("f")), "all")
    if arg not in ("all", "f6"):
        order = [arg] + ["f6"]   # single-phase run: do it, then report
    log(f"night-2 start: panel={len(PANEL)} n1={len(N1_FNS)} "
        f"exclude={len(EXCLUDE)} deadline={DEADLINE_S//3600}h"
        f"{(DEADLINE_S%3600)//60}m")
    heartbeat("night2", "running")
    for i, p in enumerate(order):
        if p == "f6" and i == 2:
            phase_f6()            # interim report after training
            continue
        if out_of_time():
            log(f"deadline reached before {p}; skipping")
            heartbeat(p, "skipped-deadline")
            continue
        try:
            log(f"=== {p} ===")
            phases[p]()
        except Exception:
            import traceback
            tb = traceback.format_exc()
            log(f"PHASE {p} CRASHED:\n{tb}")
            (OUT / f"{p}_CRASH.txt").write_text(tb)
            heartbeat(p, "crashed")
    phase_f6()                    # final report, always
    log("night-2 finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())




