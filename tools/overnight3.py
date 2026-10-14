"""Night-3: "The Libre Reconstruction" — build a verified clean-C corpus.

Night-1/2 lesson: the small model imitates Ghidra's SHAPE, not meaning
(F3: ~2/3 of its compiles are judged junk). Tonight the evaluators become
manufacturers: gate + dual judges produce judge-verified clean C for all
~294 liero-dos functions, and that VERIFIED C (not Ghidra pseudocode) is
the finetune target for the distilled 1.5B. The artifact: a complete,
provenance-annotated, human-readable reconstruction — the preservation
goal made concrete.

Phases (each crash-safe, incremental JSON, deadline-guarded):
  G1  mass generation: phi4-sumfirst + qwen-bans arm-C on ALL 294 fns
      -> compile gate (two candidates per function).
  G2  dual-judge audit (judge-outer batching): grade every compiling
      candidate; agreed-real (both >=4) become the clean-C dataset;
      best candidate per fn ranked by (verdict, mean score).
  G3  distill-finetune: 1.5B trained on asm -> judge-verified clean C
      (only if >= MIN_DISTILL pairs); eval on the night-2 60-panel.
      FALLBACK: if too few pairs, skip training and carry on.
  G4  full-corpus reconstruction: distilled model (or best-available
      generator) drafts all 294; compile-gate; stratified sample judged;
      emit recon/*.c (provenance headers) + README + REPORT3.md.

Finish <= 06:00: deadline guard before every sub-step; report always runs.
NO engine/ changes. Run: python3 -u tools/overnight3.py all
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import asm_baseline as ab      # noqa: E402  (compile gate, prompts)
import overnight2 as n2        # noqa: E402  (gen, judges, panel, verdicts)

OUT = ROOT / "reports" / "overnight3"
OUT.mkdir(parents=True, exist_ok=True)
TARGET = ROOT / "targets" / "liero-dos"

DEADLINE_S = 7 * 60 * 60 + 40 * 60          # stop new work at ~05:40
MIN_DISTILL = 80                            # agreed-real pairs needed to train
VNV_PY = "/tmp/ftvenv/bin/python"
PANEL = n2.PANEL                            # night-2's 60 for G3 eval
ALL_FNS = sorted(p.stem for p in (TARGET / "asm").glob("FUN_*.s")
                 if (TARGET / "decomp" / f"{p.stem}.c").exists())

t_start = time.time()
BUDGET_S = {"g1": 130 * 60, "g2": 160 * 60, "g3": 90 * 60, "g4": 160 * 60}


def log(msg: str) -> None:
    print(f"[n3 {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def elapsed() -> float:
    return time.time() - t_start


def out_of_time() -> bool:
    return elapsed() > DEADLINE_S


def budget_left(phase: str, t0: float) -> bool:
    return (not out_of_time()) and (time.time() - t0 < BUDGET_S[phase])


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


# ----------------------------------------------------------------- G1: generate
SUMFIRST_BANS = (
    n2.JUNK_BANS
    + "\nFirst write ONE short comment line summarizing what the function "
      "does, then output the complete C function.\n"
)


def cand_prompt(f: str, style: str) -> str:
    dec = (TARGET / "decomp" / f"{f}.c").read_text()
    if style == "sumfirst":
        return ab.DECOMP_REFINE_PROMPT.format(decomp=dec) + SUMFIRST_BANS
    return ab.DECOMP_REFINE_PROMPT.format(decomp=dec) + n2.JUNK_BANS


def phase_g1() -> None:
    heartbeat("g1", "running")
    outdir = OUT / "g1"
    outdir.mkdir(exist_ok=True)
    rows_path = outdir / "results.json"
    rows = load_json(rows_path, [])
    have = {(r["model"], r["fn"]) for r in rows}
    # priority: phi4-sumfirst (night-2 best) then qwen-bans
    plan = [(n2.PHI, "sumfirst"), (n2.QWEN, "bans")]
    t0 = time.time()
    for model, style in plan:
        for f in ALL_FNS:
            if (model, f) in have:
                continue
            if not budget_left("g1", t0):
                log("G1 budget/deadline hit")
                break
            row = n2.c_call(model, cand_prompt(f, style), f,
                            outdir / "gen" / f, arm=f"G1:{style}")
            row["model"], row["style"] = model, style
            rows.append(row)
            save_json(rows_path, rows)
            if len(rows) % 20 == 0:
                ok = sum(r["compile"] != "fail" for r in rows)
                log(f"  G1 progress {len(rows)}/{2*len(ALL_FNS)} compiles={ok}")
        ab.ollama_unload(model)
    ok = sum(r["compile"] != "fail" for r in rows)
    (outdir / "summary.md").write_text(
        f"# G1 mass generation\n- candidates: {len(rows)}, compiles: {ok}\n")
    heartbeat("g1", "done", rows=len(rows))


# --------------------------------------------------------------- G2: judge
def best_candidate(rows: list) -> dict | None:
    """Rank by (verdict, mean score); agreed-real first, then score."""
    rank = {"real": 3, "contested": 2, "judge-error": 1, "junk": 0}
    def sc(r):
        q = (r.get("qwen") or {}).get("score") or 0
        p = (r.get("phi") or {}).get("score") or 0
        return (rank.get(r.get("verdict"), 0), q + p)
    good = [r for r in rows if r.get("compile") != "fail" and r.get("code")]
    return max(good, key=sc) if good else None


def phase_g2() -> None:
    heartbeat("g2", "running")
    outdir = OUT / "g2"
    outdir.mkdir(exist_ok=True)
    rows_path = outdir / "results.json"
    rows = load_json(rows_path, [])
    partial = {r["key"]: r for r in rows}
    cand = load_json(OUT / "g1" / "results.json", [])
    todo = [(r["model"], r["fn"], r["code"]) for r in cand
            if r["compile"] != "fail" and r.get("code")]
    log(f"G2: {len(todo)} compiling candidates to judge (dual)")
    t0 = time.time()
    for jmodel, jkey in ((n2.QWEN, "qwen"), (n2.PHI, "phi")):
        for _model, f, code in todo:
            if not budget_left("g2", t0):
                log("G2 budget/deadline hit")
                g2_finish(partial, rows_path)
                return
            key = f"{_model}|{f}"   # per-CANDIDATE: two candidates per fn
            r = partial.setdefault(key, {"fn": f, "model": _model, "key": key})
            ref = (TARGET / "decomp" / f"{f}.c").read_text()
            r[jkey] = n2.judge_once(jmodel, f, ref, code)
            save_json(rows_path, list(partial.values()))
            if len(partial) % 10 == 0:
                log(f"  G2 progress judged={len(partial)}")
        ab.ollama_unload(jmodel)
    g2_finish(partial, rows_path)
    heartbeat("g2", "done", rows=len(partial))


def g2_finish(partial: dict, rows_path: pathlib.Path) -> None:
    """Pair judge scores, compute verdicts, write dataset + summary."""
    final = []
    for r in partial.values():
        q, p = r.get("qwen"), r.get("phi")
        if q and p:
            r["verdict"] = n2.dual_verdict(q, p)
        else:
            r["verdict"] = "judge-error"
        final.append(r)
    save_json(rows_path, final)
    real = [r for r in final if r.get("verdict") == "real"]
    (OUT / "g2" / "real_pairs.json").write_text(json.dumps(
        [{"fn": r["fn"], "model": r.get("model"), "verdict": "real",
          "qwen": (r.get("qwen") or {}).get("score"),
          "phi": (r.get("phi") or {}).get("score")} for r in real], indent=2))
    by = {v: sum(r["verdict"] == v for r in final)
          for v in ("real", "contested", "junk", "judge-error")}
    (OUT / "g2" / "summary.md").write_text(
        f"# G2 dual-judge audit\n"
        f"- candidates judged: {len(final)}\n"
        f"- real: {by['real']}  contested: {by['contested']}  "
        f"junk: {by['junk']}  error: {by['judge-error']}\n"
        f"- distill dataset (>= {MIN_DISTILL} needed): {by['real']}\n")
    log(f"G2 done: real={by['real']} (need >= {MIN_DISTILL} to distill)")


# --------------------------------------------------------------- G3: distill
def phase_g3() -> None:
    """Subprocess to the torch worker: train distilled LoRA, eval panel,
    then generate the FULL 294-fn corpus with the distilled model."""
    real = load_json(OUT / "g2" / "real_pairs.json", [])
    if len(real) < MIN_DISTILL:
        (OUT / "g3").mkdir(exist_ok=True)
        (OUT / "g3" / "SKIPPED.md").write_text(
            f"only {len(real)} agreed-real pairs (< {MIN_DISTILL}); "
            f"corpus falls back to G1 candidates.\n")
        log(f"G3 SKIPPED: {len(real)} real pairs < {MIN_DISTILL}")
        heartbeat("g3", "skipped", real_pairs=len(real))
        return
    heartbeat("g3", "running")
    (OUT / "g3").mkdir(exist_ok=True)
    exclude = sorted(set(PANEL) | set(n2.N1_FNS))   # panel = eval, never train
    (OUT / "exclude.txt").write_text("\n".join(exclude))
    t0 = time.time()
    log(f"G3: launching g3_distill.py with {len(real)} verified pairs")
    try:
        r = subprocess.run(
            [VNV_PY, str(ROOT / "tools" / "g3_distill.py"),
             "--budget-s", str(BUDGET_S["g3"]),
             "--exclude-file", str(OUT / "exclude.txt"),
             "--panel", ",".join(PANEL)],
            capture_output=True, text=True,
            timeout=BUDGET_S["g3"] + 900, cwd=str(ROOT), env=dict(os.environ))
        (OUT / "g3" / "train.log").write_text(
            r.stdout + "\n--- STDERR ---\n" + r.stderr)
        log(f"G3 exit={r.returncode} ({time.time()-t0:.0f}s)")
    except subprocess.TimeoutExpired as e:
        (OUT / "g3" / "train.log").write_text(
            (e.stdout or b"").decode(errors="replace") + "\nTIMEOUT\n")
        log("G3 TIMEOUT")
    heartbeat("g3", "done" if (OUT / "g4" / "results.json").exists()
              else "failed")


# --------------------------------------------------------------- G4: corpus
PROV_HEADER = """\
/* Libre Reconstruction — LoSoRe preservation project
 * Function:  {fn}
 * Generated: {date} by {gen}
 * Gate:      gcc -fsyntax-only = {compile}
 * Dual-judge: qwen={qwen} phi={phi} verdict={verdict}
 * THIS IS MACHINE-GENERATED C. Verify against the assembly before use.
 */
"""


def best_corpus_rows() -> list[dict]:
    """Per fn: distilled output if it compiled, else best G1 candidate
    ranked by G2 verdict. Merges both, never drops a fn silently."""
    out: dict[str, dict] = {}
    for r in load_json(OUT / "g4" / "results.json", []):
        if r.get("compile") != "fail" and r.get("code"):
            out[r["fn"]] = r               # distilled corpus (G3)
    g1 = load_json(OUT / "g1" / "results.json", [])
    g2 = {r["key"]: r for r in load_json(OUT / "g2" / "results.json", [])}
    by_fn: dict[str, list] = {}
    for r in g1:
        if r["compile"] != "fail" and r.get("code"):
            rr = dict(r)
            j = g2.get(f'{r["model"]}|{r["fn"]}') or {}
            rr["verdict"] = j.get("verdict", "judge-error")
            rr["qwen_score"] = (j.get("qwen") or {}).get("score")
            rr["phi_score"] = (j.get("phi") or {}).get("score")
            by_fn.setdefault(r["fn"], []).append(rr)
    for f, v in by_fn.items():
        if f not in out and (best := best_candidate(v)):
            out[f] = best
    return sorted(out.values(), key=lambda r: r["fn"])


def phase_g4() -> None:
    heartbeat("g4", "running")
    (OUT / "g4").mkdir(exist_ok=True)
    rows = best_corpus_rows()
    rows_path = OUT / "g4" / "corpus.json"
    save_json(rows_path, rows)
    log(f"G4: corpus candidates for {len(rows)}/{len(ALL_FNS)} fns")

    # fresh judge-sample for the DISTILLED corpus only (G1-sourced fns
    # already carry G2 verdicts; distilled outputs were never judged)
    sample_path = OUT / "g4" / "judge_sample.json"
    sample = load_json(sample_path, [])
    distilled = bool(load_json(OUT / "g4" / "results.json", []))
    if distilled and len(sample) < 40:
        have = {r["fn"] for r in sample}
        pool = sorted((r for r in rows if r["fn"] not in have),
                      key=lambda r: r["fn"])
        stride = max(1, len(pool) // 40)
        picks, t0 = pool[::stride][:40], time.time()
        for r in picks:
            if not budget_left("g4", t0):
                break
            ref = (TARGET / "decomp" / f'{r["fn"]}.c').read_text()
            s1 = n2.judge_once(n2.QWEN, r["fn"], ref, r["code"])
            s2 = n2.judge_once(n2.PHI, r["fn"], ref, r["code"])
            sample.append({"fn": r["fn"], "qwen": s1, "phi": s2,
                           "verdict": n2.dual_verdict(s1, s2)})
            save_json(sample_path, sample)
        vmap = {r["fn"]: r for r in sample}
        for r in rows:
            if r["fn"] in vmap and not r.get("qwen_score"):
                v = vmap[r["fn"]]
                r["qwen_score"] = (v["qwen"] or {}).get("score")
                r["phi_score"] = (v["phi"] or {}).get("score")
                r["verdict"] = v["verdict"]
        save_json(rows_path, rows)

    # emit recon/*.c with provenance headers + README + index
    recon = OUT / "recon"
    recon.mkdir(exist_ok=True)
    date = time.strftime("%Y-%m-%d")
    for r in rows:
        if r.get("generator", "").startswith("distilled"):
            gen = f'distilled-Qwen2.5-Coder-1.5B ({r["generator"]})'
        else:
            gen = f'{r.get("model", "?")} ({r.get("style", "?")})'
        hdr = PROV_HEADER.format(
            fn=r["fn"], date=date, gen=gen, compile=r.get("compile", "?"),
            qwen=r.get("qwen_score", "-"), phi=r.get("phi_score", "-"),
            verdict=r.get("verdict", "not-judged"))
        (recon / f'{r["fn"]}.c').write_text(hdr + "\n" + r["code"] + "\n")
    vcount: dict[str, int] = {}
    for r in rows:
        v = r.get("verdict", "not-judged")
        vcount[v] = vcount.get(v, 0) + 1
    (OUT / "g4" / "index.json").write_text(json.dumps(
        {"generated": date, "n": len(rows), "of_total": len(ALL_FNS),
         "verdicts": vcount, "methods": "see REPORT3.md"}, indent=2))
    (recon / "README.md").write_text(
        "# Libre Reconstruction of liero-dos (machine-generated C)\n\n"
        f"- Functions reconstructed: {len(rows)}/{len(ALL_FNS)}\n"
        f"- Verdicts: {vcount}\n"
        "- Every file carries a provenance header: generator, compile-gate "
        "result, dual-judge scores.\n"
        "- MACHINE OUTPUT: a *starting point* for human restoration, not a "
        "substitute for it. Verify semantics against the assembly (or run "
        "the dat-parity oracle) before trusting any function.\n"
        "- Purpose: preservation of lost proprietary source as FOSS-"
        "aligned cultural heritage.\n")
    (OUT / "g4" / "summary.md").write_text(
        f"# G4 corpus\n- emitted {len(rows)} files to recon/\n"
        f"- verdicts: {vcount}\n")
    heartbeat("g4", "done", n=len(rows), verdicts=vcount)


# --------------------------------------------------------------- G5: report
def phase_g5() -> None:
    heartbeat("g5", "running")
    parts = ["# Night-3 report: The Libre Reconstruction\n",
             f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')} after "
             f"{elapsed()/60:.0f} min.\n",
             "Artifact: reports/overnight3/recon/ (machine-reconstructed "
             "clean C with provenance headers).\n"]
    for ex, title in [("g1", "G1 mass generation"), ("g2", "G2 dual-judge"),
                      ("g3", "G3 distill"), ("g4", "G4 corpus")]:
        parts.append(f"\n## {title}\n")
        sm = OUT / ex / "summary.md"
        parts.append(sm.read_text() if sm.exists() else "(not run)\n")
    g4 = load_json(OUT / "g4" / "index.json", {})
    parts.append("\n## Verdict on the distillation hypothesis\n")
    if g4:
        parts.append(f"- corpus size: {g4.get('n')}/{g4.get('of_total')}, "
                     f"verdicts: {g4.get('verdicts')}\n")
    parts.append(
        "- Night-2 F3 said ~2/3 of the small model's compiles were junk "
        "when trained on Ghidra pseudocode. G3 retrains it on judge-"
        "verified clean C instead; G4's judge sample is the answer.\n"
        "- Compile != semantics remains: only dual-agreement 'real' "
        "verdicts count as preserved source.\n")
    (OUT / "REPORT3.md").write_text("".join(parts))
    heartbeat("g5", "done")
    log("G5 -> reports/overnight3/REPORT3.md")


def main() -> int:
    phases = {"g1": phase_g1, "g2": phase_g2, "g3": phase_g3,
              "g4": phase_g4, "g5": phase_g5}
    order = ["g1", "g2", "g3", "g4", "g5"]
    log(f"night-3 start: {len(ALL_FNS)} fns, panel={len(PANEL)}, "
        f"deadline={DEADLINE_S//3600}h{(DEADLINE_S%3600)//60}m")
    heartbeat("night3", "running")
    for p in order:
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
    phase_g5()                    # report always runs
    log("night-3 finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())





