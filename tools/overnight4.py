"""Night-4 long unsupervised run: TOUGHEST functions + finetune + recompile proof.

Answers two open goals:
  1. "tougher computations" — largest asm fns (33k lines; top-40 heaviest never
     attempted) get a best-of-N dual-judge recon push -> verified C corpus.
  2. "truly reverse-engineered + re-compiled properly" — every `real` verdict is
     promoted into the Turbo Pascal rebuild (engine/draft.py, same language) and the
     WHOLE program recompiles via Docker FPC; green exit+link = recompile proof.

Phases (ollama first, torch after unload_all):
  P0 baseline build -> P1 tough recon -> P2 promote+recompile (rollback if red)
  -> P3 LoRA finetune (e4_finetune.py) -> P4 REPORT4.md (always runs).
Crash-safe per-phase json; deadline-guarded; no engine/ changes.
Run: nohup python3 -u tools/overnight4.py all > reports/overnight4_run.log 2>&1 &
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import asm_baseline as ab   # noqa: E402
import overnight2 as n2     # noqa: E402
import overnight3 as n3     # noqa: E402  (PROV_HEADER, cand_prompt)

OUT = ROOT / "reports" / "overnight4"
RECON = OUT / "recon"
OUT.mkdir(parents=True, exist_ok=True)
RECON.mkdir(exist_ok=True)
TARGET = ROOT / "targets" / "liero-dos"

VNV_PY = "/tmp/ftvenv/bin/python"
ENDPOINT = "http://localhost:11434"
DRAFT_MODEL = n2.QWEN                       # qwen2.5-coder:14b for C->Pascal
DEADLINE_S = int(os.environ.get("LSR_N4_DEADLINE_S", 7 * 3600 + 45 * 60))
BUDGET_S = {"p0": 10 * 60, "p1": 210 * 60, "p2": 90 * 60,
            "p3": 90 * 60, "p4": 10 * 60}
N3_RECON = ROOT / "reports" / "overnight3" / "recon"
TOUGH_N = 40

# Output-token cap for P1 generation. night-2's 1024 is far too small for the
# biggest fns (their Ghidra decomp seeds are 1400+ lines), so candidates truncated
# mid-declaration -> the P1 compile rate measured the cap, not the model. 8192
# matches n2.NUM_CTX (prompt+output fit in one context).
GEN_NPX = 8192
# Retarget P1 to fns whose decomp seed can plausibly complete within GEN_NPX
# (~2k C lines). Larger single-body fns are out of reach without chunking; we
# record them as deferred rather than mis-measuring them.
MAX_DECOMP_LINES = 2200

t_start = time.time()


def capped_c_call(model, prompt, f, wdir, arm="", timeout=1500, npx=None):
    """n2.c_call but with a large output-token budget and a generous timeout.

    n2.gen's default npx=1024 truncates the biggest fns mid-declaration, and its
    hardcoded urlopen timeout=300s aborts a genuine 8k-token generation (~5-10min)
    for a 4k-line body. Both made the first run measure the harness, not the model.
    Same row keys as n2.c_call so the judge and _write_recon_corpus need no changes.
    NOTE: n2.gen doesn't thread a per-call timeout, so this builds the request
    inline (mirrors n2.gen: ollama /api/generate, stream=false, num_ctx)."""
    t0 = time.time()
    wdir.mkdir(parents=True, exist_ok=True)
    npx = npx or GEN_NPX
    data = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": 0.0, "num_ctx": n2.NUM_CTX,
                    "num_predict": npx},
    }).encode()
    raw = ""
    try:
        for attempt in range(2):
            try:
                req = urllib.request.Request(
                    n2.OLLAMA + "/api/generate", data=data,
                    headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    raw = json.loads(resp.read()).get("response", "")
                break
            except Exception:
                if attempt == 1:
                    raise
                time.sleep(30)
    except Exception as e:
        return {"fn": f, "arm": arm, "compile": "fail", "bucket": "transport",
                "error": f"transport: {e}", "seconds": round(time.time() - t0, 1),
                "raw": ""}
    code = ab.extract_c(raw)
    status, err = ab.compile_c(code, wdir, f)
    return {"fn": f, "arm": arm, "compile": status, "bucket": ab.bucket(err),
            "error": err[:200], "seconds": round(time.time() - t0, 1),
            "raw": raw, "code": code}


def log(msg: str) -> None:
    print(f"[n4 {time.strftime('%H:%M:%S')}] {msg}", flush=True)


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


def save_json(path: pathlib.Path, rows) -> None:
    path.write_text(json.dumps(rows, indent=2))


def verdict_of(fn: str) -> str:
    """Best recon verdict for fn across night-3 + night-4 corpora."""
    best, rank = "none", {"none": 0, "junk": 1, "unparsed": 1,
                          "judge-error": 2, "contested": 2, "real": 3}
    for d in (N3_RECON, RECON):
        p = d / f"{fn}.c"
        if not p.exists():
            continue
        m = re.search(r"verdict=(\S+)", p.read_text(errors="replace"))
        v = m.group(1) if m else "unparsed"
        if rank.get(v, 0) > rank.get(best, 0):
            best = v
    return best


def _decomp_lines(f: str) -> int:
    p = TARGET / "decomp" / f"{f}.c"
    try:
        return len(p.read_text().splitlines())
    except Exception:
        return 0


def tough_fns() -> tuple[list[str], list[str]]:
    """Top-N largest asm fns still not `real`-verified.

    Returns (attempt, deferred): 'attempt' are within MAX_DECOMP_LINES so a
    single GEN_NPX-capped completion can plausibly finish; 'deferred' are the
    megafns whose decomp seed alone exceeds that budget (honest, not measured)."""
    sizes = sorted(((p.stem, len(p.read_text().splitlines()))
                    for p in (TARGET / "asm").glob("FUN_*.s")),
                   key=lambda kv: -kv[1])
    cand = [f for f, _ in sizes if verdict_of(f) != "real"][:TOUGH_N]
    attempt = [f for f in cand if _decomp_lines(f) <= MAX_DECOMP_LINES]
    deferred = [f for f in cand if _decomp_lines(f) > MAX_DECOMP_LINES]
    return attempt, deferred



# ---------------------------------------------------------------- P0 build proof
def phase_p0() -> None:
    """Baseline recompile proof BEFORE tonight's edits."""
    heartbeat("p0", "running")
    (OUT / "p0").mkdir(exist_ok=True)
    log("P0: baseline full recompile (Docker FPC -Mtp)")
    t0 = time.time()
    try:
        r = subprocess.run(["make", "-C", str(TARGET), "build"],
                           capture_output=True, text=True,
                           timeout=BUDGET_S["p0"] * 0.9, cwd=str(ROOT))
        (OUT / "p0" / "build.log").write_text(
            r.stdout + "\n--- STDERR ---\n" + r.stderr)
        green = r.returncode == 0 and "Linking" in r.stdout
        nlines = next((int(w) for w in r.stdout.split()
                       if w.isdigit() and "lines" in r.stdout), None)
        save_json(OUT / "p0" / "proof.json", {
            "rc": r.returncode, "green": green, "pascal_lines": nlines,
            "seconds": round(time.time() - t0, 1)})
        log(f"P0: rc={r.returncode} green={green} ({time.time()-t0:.0f}s)")
    except subprocess.TimeoutExpired:
        save_json(OUT / "p0" / "proof.json",
                  {"rc": None, "green": False, "error": "timeout"})
        log("P0: TIMEOUT")
    heartbeat("p0", "done")


# ---------------------------------------------------------------- P1 tough recon
def _write_recon_corpus(rows, partial) -> tuple[int, list[str]]:
    """Best candidate per fn -> recon/{fn}.c in night-3 provenance format."""
    rank = {"real": 3, "contested": 2, "judge-error": 1, "junk": 0}
    best: dict[str, dict] = {}
    for r in partial.values():
        cand = next((g for g in rows
                     if g["model"] == r["model"] and g["fn"] == r["fn"]
                     and g["compile"] != "fail" and g.get("code")), None)
        if not cand:
            continue
        r2 = dict(r)
        r2["code"], r2["compile"] = cand["code"], cand["compile"]
        q = (r2.get("qwen") or {}).get("score") or 0
        cur = best.get(r2["fn"])
        key = (rank.get(r2["verdict"], 0), q)
        if cur is None or key > (rank.get(cur["verdict"], 0),
                                 (cur.get("qwen") or {}).get("score") or 0):
            best[r2["fn"]] = r2
    n = 0
    for f, r in best.items():
        header = n3.PROV_HEADER.format(
            fn=f, date=time.strftime("%Y-%m-%d"), gen=f"n4:{r['model']}",
            compile=r["compile"], qwen=(r.get("qwen") or {}).get("score"),
            phi=(r.get("phi") or {}).get("score"), verdict=r["verdict"])
        (RECON / f"{f}.c").write_text(header + "\n" + r["code"])
        n += 1
    real_fns = sorted(f for f, r in best.items() if r["verdict"] == "real")
    return n, real_fns


def phase_p1() -> None:
    """Best-of-N recon for the toughest (largest) asm fns, then dual-judge."""
    heartbeat("p1", "running")
    (OUT / "p1").mkdir(exist_ok=True)
    fns, deferred = tough_fns()
    save_json(OUT / "p1" / "targets.json", fns)
    save_json(OUT / "p1" / "deferred.json", deferred)
    log(f"P1: {len(fns)} tough fns (<= {MAX_DECOMP_LINES} decomp lines), "
        f"{len(deferred)} megafns deferred; top-5: {', '.join(fns[:5])}")
    gen_path = OUT / "p1" / "gen.json"
    rows = load_json(gen_path, [])
    # Drop the 1024-npx truncated rows from the first (mis-measured) run so they
    # don't satisfy the `have` skip and shadow a fresh 8192-npx regeneration.
    stale = [r for r in rows if str(r.get("arm", "")).startswith("P1:")]
    rows = [r for r in rows if not str(r.get("arm", "")).startswith("P1:")]
    if stale:
        log(f"P1: discarding {len(stale)} stale npx=1024 rows for regeneration")
    have = {(r["model"], r["fn"]) for r in rows}
    t0 = time.time()
    for model, style in ((n2.PHI, "sumfirst"), (n2.QWEN, "bans")):
        for f in fns:
            if (model, f) in have:
                continue
            if not budget_left("p1", t0):
                log("P1 gen budget/deadline hit"); break
            row = capped_c_call(model, n3.cand_prompt(f, style), f,
                                OUT / "p1" / "gen" / f, arm=f"P1:{style}")
            row["model"], row["style"] = model, style
            rows.append(row)
            save_json(gen_path, rows)
        ab.ollama_unload(model)
    ncomp = sum(r["compile"] != "fail" for r in rows)
    log(f"P1 gen done: {len(rows)} candidates, {ncomp} compile")

    jud_path = OUT / "p1" / "judge.json"
    partial = {r["key"]: r for r in load_json(jud_path, [])}
    todo = [(r["model"], r["fn"], r["code"]) for r in rows
            if r["compile"] != "fail" and r.get("code")]
    t0 = time.time()
    for jmodel, jkey in ((n2.QWEN, "qwen"), (n2.PHI, "phi")):
        for _m, f, code in todo:
            if not budget_left("p1", t0):
                log("P1 judge budget hit"); break
            key = f"{_m}|{f}"
            r = partial.setdefault(key, {"fn": f, "model": _m, "key": key})
            ref = (TARGET / "decomp" / f"{f}.c").read_text()
            r[jkey] = n2.judge_once(jmodel, f, ref, code)
            save_json(jud_path, list(partial.values()))
        ab.ollama_unload(jmodel)
    for r in partial.values():
        q, p = r.get("qwen"), r.get("phi")
        r["verdict"] = n2.dual_verdict(q, p) if q and p else "judge-error"
    save_json(jud_path, list(partial.values()))
    by = {v: sum(r["verdict"] == v for r in partial.values())
          for v in ("real", "contested", "junk", "judge-error")}
    log(f"P1 judge done: {by}")
    n_written, real_fns = _write_recon_corpus(rows, partial)
    save_json(OUT / "p1" / "real_fns.json", real_fns)
    (OUT / "p1" / "summary.md").write_text(
        f"# P1 tough-fn recon\n- targets: {len(fns)}\n"
        f"- candidates: {len(rows)}, compiles: {ncomp}\n"
        f"- verdicts: {by}\n- recon written: {n_written}, real: "
        f"{len(real_fns)}\n")
    log(f"P1: wrote {n_written} recon; {len(real_fns)} real")
    heartbeat("p1", "done", real=len(real_fns))


# ---------------------------------------------------------------- P2 promote+build
def _src_backup() -> pathlib.Path:
    bak = OUT / "src_backup"
    if bak.exists():
        return bak
    bak.mkdir(parents=True)
    for p in (TARGET / "src").glob("FUN_*.inc"):
        (bak / p.name).write_bytes(p.read_bytes())
    return bak


def _build_ok(timeout_s: float) -> tuple[bool, str]:
    try:
        r = subprocess.run(["make", "-C", str(TARGET), "build"],
                           capture_output=True, text=True,
                           timeout=timeout_s, cwd=str(ROOT))
        return (r.returncode == 0 and "Linking" in r.stdout,
                r.stdout + "\n--- STDERR ---\n" + r.stderr)
    except subprocess.TimeoutExpired:
        return False, "timeout"


def phase_p2() -> None:
    """Promote real verdicts to Pascal, then prove the full recompile.

    If the recompile breaks, roll src/ back from the pre-phase backup and record
    the delta — the working tree is never left broken."""
    heartbeat("p2", "running")
    (OUT / "p2").mkdir(exist_ok=True)
    real_fns = sorted(set(load_json(OUT / "p1" / "real_fns.json", []))
                      | {p.stem for p in RECON.glob("*.c")
                         if "verdict=real" in p.read_text(errors="replace")})
    if not real_fns:
        log("P2: no real verdicts; skipping promotion")
        (OUT / "p2" / "summary.md").write_text(
            "# P2 promote+recompile\nNo `real` verdicts to promote.\n")
        heartbeat("p2", "skipped-no-real"); return
    bak = _src_backup()
    log(f"P2: promoting {len(real_fns)} real fns to Pascal "
        f"(draft.py --llm {DRAFT_MODEL})")
    t0 = time.time()
    promoted, failed = [], []
    for f in real_fns:
        if not budget_left("p2", t0):
            break
        try:
            # draft.py skips any fn whose src/*.inc already exists (idempotence),
            # so a leftover skeleton would make the LLM path silently never run.
            # Remove it (and any stray .c) to force a fresh recon-seeded translate.
            for stale in (TARGET / "src" / f"{f}.inc", TARGET / "src" / f"{f}.c"):
                if stale.exists():
                    stale.unlink()
            r = subprocess.run(
                [sys.executable, str(ROOT / "engine" / "draft.py"),
                 "--target", "liero-dos", "--fn", f, "--llm",
                 "--model", DRAFT_MODEL, "--endpoint", ENDPOINT,
                 "--recon-dir", str(RECON), "--recon-verdicts", "real"],
                capture_output=True, text=True, timeout=900, cwd=str(ROOT))
            inc = TARGET / "src" / f"{f}.inc"
            ok = (r.returncode == 0 and inc.exists()
                  and "TODO: translate" not in inc.read_text(errors="replace"))
            if not ok:
                log(f"P2: {f} not promoted rc={r.returncode} "
                    f"{(r.stderr or r.stdout or '').strip()[-160:]}")
            (promoted if ok else failed).append(f)
        except Exception as e:
            failed.append(f"{f}:{e}")
    ok, logtxt = _build_ok(BUDGET_S["p2"] * 0.5)
    (OUT / "p2" / "build.log").write_text(logtxt)
    result = {"promoted": promoted, "failed": failed, "build_green": ok,
              "elapsed_min": round((time.time() - t0) / 60, 1)}
    if ok:
        log(f"P2: BUILD GREEN — {len(promoted)} promoted+proven")
        hb = ("done", len(promoted))
    else:
        log("P2: BUILD RED — rolling src/ back to backup")
        for p in (TARGET / "src").glob("FUN_*.inc"):
            src = bak / p.name
            if src.exists():
                p.write_bytes(src.read_bytes())
        ok2, _ = _build_ok(BUDGET_S["p2"] * 0.5)
        result.update(build_green_after_rollback=ok2,
                      orig_promoted=promoted, promoted=[])
        log(f"P2: rollback rebuild green={ok2}")
        hb = ("rolled-back", None)
    save_json(OUT / "p2" / "result.json", result)
    (OUT / "p2" / "summary.md").write_text(
        f"# P2 promote+recompile\n- real fns: {len(real_fns)}\n"
        f"- promoted: {len(result['promoted'])}, failed: {len(failed)}\n"
        f"- build_green: {result['build_green']}\n")
    heartbeat("p2", hb[0], promoted=hb[1] or 0)


# ---------------------------------------------------------------- P3 finetune
def phase_p3() -> None:
    """LoRA finetune experiment (asm->C on our pairs), torch worker."""
    heartbeat("p3", "running")
    (OUT / "p3").mkdir(exist_ok=True)
    n2.unload_all()                       # free VRAM before torch
    budget = BUDGET_S["p3"]
    log(f"P3: launching e4_finetune.py --budget-s {budget}")
    t0 = time.time()
    try:
        r = subprocess.run(
            [VNV_PY, str(ROOT / "tools" / "e4_finetune.py"),
             "--budget-s", str(budget)],
            capture_output=True, text=True, timeout=budget + 900,
            cwd=str(ROOT), env=dict(os.environ))
        (OUT / "p3" / "train.log").write_text(
            r.stdout + "\n--- STDERR ---\n" + r.stderr)
        log(f"P3: exit={r.returncode} ({time.time()-t0:.0f}s)")
    except subprocess.TimeoutExpired as e:
        (OUT / "p3" / "train.log").write_text(
            (e.stdout or b"").decode(errors="replace") + "\nTIMEOUT\n")
        log("P3: TIMEOUT")
    heartbeat("p3", "done" if (OUT / "p3" / "train.log").exists()
              else "failed")


# ---------------------------------------------------------------- P4 report
def phase_p4() -> None:
    """REPORT4.md rollup — always runs, even after a crash/deadline."""
    heartbeat("p4", "running")
    parts = ["# Night-4 overnight report\n",
             f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')} after "
             f"{elapsed()/60:.0f} min.\n",
             "\nGoal: toughest-function recon + recompile proof + finetune.\n"]
    for ex, title in [("p0", "P0 baseline recompile (pre-edit proof)"),
                      ("p1", "P1 tough-fn recon (top-40 largest, best-of-N)"),
                      ("p2", "P2 promote real -> Pascal + full recompile"),
                      ("p3", "P3 LoRA finetune (asm->C)")]:
        parts.append(f"\n## {title}\n")
        got = False
        for fn in ("summary.md", "result.json", "proof.json", "train.log"):
            p = OUT / ex / fn
            if p.exists():
                parts.append("\n```\n" + p.read_text()[-3000:] + "\n```\n")
                got = True
                break
        if not got:
            parts.append("(not run)\n")
    parts.append("\n## Reproduce\n```\nnohup python3 -u tools/overnight4.py all "
                 "> reports/overnight4_run.log 2>&1 &\n```\n")
    (OUT / "REPORT4.md").write_text("".join(parts))
    heartbeat("p4", "done")
    log("P4 -> reports/overnight4/REPORT4.md")


def main() -> int:
    order = ["p0", "p1", "p2", "p3", "p4"]
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg != "all" and arg in ("p0", "p1", "p2", "p3"):
        order = [arg, "p4"]
    log(f"night-4 start: deadline={DEADLINE_S//3600}h"
        f"{(DEADLINE_S%3600)//60}m tough_n={TOUGH_N}")
    heartbeat("night4", "running")
    fns = {"p0": phase_p0, "p1": phase_p1, "p2": phase_p2,
           "p3": phase_p3, "p4": phase_p4}
    for p in order:
        if out_of_time() and p != "p4":
            log(f"deadline reached before {p}; skipping")
            heartbeat(p, "skipped-deadline"); continue
        try:
            log(f"=== {p} ===")
            fns[p]()
        except Exception:
            import traceback
            tb = traceback.format_exc()
            log(f"PHASE {p} CRASHED:\n{tb}")
            (OUT / f"{p}_CRASH.txt").write_text(tb)
            heartbeat(p, "crashed")
    log("night-4 finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())

