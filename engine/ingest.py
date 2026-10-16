"""Ingest: Ghidra headless export -> targets/<slug>/asm/ (+ decomp/, functions.json).

Runs the Java post-script tools/ghidra/ExportFuncs.java which writes, per target:
  targets/<slug>/asm/<func>.s      raw instruction listing
  targets/<slug>/decomp/<func>.c   best-effort decompiler output (draft seed)
  targets/<slug>/functions.json    metadata (name, entry, size, cc, ...)

Disc-gated: SKIP (pass) without extracted/<target>/ or without analyzeHeadless.

Env knobs:
  LSR_GHIDRA         path to ghidra install dir (default: auto-detect ~/tools/ghidra_*)
  LSR_GHIDRA_PROJ    scratch project dir (default: <tmp>/lsr_proj_<target>; must pre-exist)
  LSR_PROCESSOR      force processor spec (else auto-detect by loader)
"""
from __future__ import annotations
import argparse, glob, os, pathlib, shutil, subprocess, sys


def find_ghidra() -> str | None:
    """Locate a Ghidra install dir (contains support/analyzeHeadless)."""
    env = os.environ.get("LSR_GHIDRA")
    cands = [env] if env else []
    cands += sorted(glob.glob(os.path.expanduser("~/tools/ghidra_*_PUBLIC")), reverse=True)
    cands += sorted(glob.glob("/opt/ghidra*"), reverse=True)
    cands += sorted(glob.glob("/usr/share/ghidra*"), reverse=True)
    for c in cands:
        if c and os.path.exists(os.path.join(c, "support", "analyzeHeadless")):
            return c
    # fall back to PATH
    return None  # analyzeHeadless on PATH handled by caller


def pick_binary(src: pathlib.Path) -> pathlib.Path | None:
    """Choose the main executable to analyze: prefer *.EXE (largest), else *.exe."""
    exes = sorted(src.glob("*.EXE")) + sorted(src.glob("*.exe"))
    if not exes:
        # any MZ/PE file
        exes = [p for p in src.iterdir()
                if p.is_file() and p.read_bytes()[:2] in (b"MZ", b"\x7fE")]
    if not exes:
        return None
    return max(exes, key=lambda p: p.stat().st_size)


def ingest(target: str, processor: str | None = None, timeout: int = 1800) -> int:
    root = pathlib.Path("targets") / target
    src = pathlib.Path("extracted") / target
    if not src.exists():
        print(f"[ingest:{target}] SKIP no BYOD (disc-gated) at {src}")
        return 0

    ghidra = find_ghidra()
    if ghidra:
        ah = os.path.join(ghidra, "support", "analyzeHeadless")
    else:
        ah = shutil.which("analyzeHeadless")
    if not ah or not os.path.exists(ah):
        print(f"[ingest:{target}] SKIP analyzeHeadless not installed "
              f"(set LSR_GHIDRA to your ghidra install)")
        return 0

    binary = pick_binary(src)
    if not binary:
        print(f"[ingest:{target}] SKIP no executable found in {src}")
        return 0

    # scratch project dir must pre-exist and contain no spaces
    proj = os.environ.get("LSR_GHIDRA_PROJ") or os.path.join(
        "/tmp", f"lsr_proj_{target}")
    shutil.rmtree(proj, ignore_errors=True)
    os.makedirs(proj, exist_ok=True)

    outdir = root / "_lsr_export"
    shutil.rmtree(outdir, ignore_errors=True)
    # clear prior staged outputs so re-ingest is idempotent (no stale fns)
    for sub in ("asm", "decomp"):
        d = root / sub
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)

    scripts = pathlib.Path("tools/ghidra").resolve()
    env = dict(os.environ, LSR_OUTDIR=str(outdir.resolve()))
    proc = processor or os.environ.get("LSR_PROCESSOR")
    cmd = [ah, proj, target, "-import", str(binary.resolve()), "-overwrite",
           "-postScript", "ExportFuncs.java", "-scriptPath", str(scripts)]
    if proc:
        cmd += ["-processor", proc]
    print(f"[ingest:{target}] {' '.join(cmd)}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        print(f"[ingest:{target}] FAIL analyzeHeadless timed out after {timeout}s")
        return 1
    log = r.stdout + r.stderr
    for line in log.splitlines():
        if "ExportFuncs" in line or "ERROR" in line or "Exception" in line:
            print("  " + line.strip())

    fns = outdir / "functions.json"
    if r.returncode != 0 or not fns.exists():
        print(f"[ingest:{target}] FAIL (rc={r.returncode}); see log tail:")
        print("\n".join(log.splitlines()[-15:]))
        return 1

    # stage: asm/*.s -> targets/<slug>/asm/ ; decomp/*.c -> decomp/ ; functions.json
    n_asm = n_dec = 0
    for f in (outdir / "asm").glob("*.s"):
        shutil.copy2(f, root / "asm" / f.name); n_asm += 1
    if (outdir / "decomp").exists():
        (root / "decomp").mkdir(exist_ok=True)
        for f in (outdir / "decomp").glob("*.c"):
            shutil.copy2(f, root / "decomp" / f.name); n_dec += 1
    shutil.copy2(fns, root / "functions.json")

    print(f"[ingest:{target}] OK {n_asm} asm, {n_dec} decomp -> targets/{target}/{{asm,decomp}}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--processor", default=None, help="e.g. 'x86:LE:16:Real Mode'")
    ap.add_argument("--timeout", type=int, default=1800)
    a = ap.parse_args()
    sys.exit(ingest(a.target, a.processor, a.timeout))

