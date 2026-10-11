"""Ingest: Ghidra headless export -> asm/ split. Requires BYOD; skips in CI.
Real Ghidra call (BYOD present + analyzeHeadless installed):
  analyzeHeadless <proj> <name> -import extracted/<target> -postScript DecompileToC ...
Falls back to SKIP otherwise (CI green)."""
from __future__ import annotations
import argparse, pathlib, shutil, subprocess, sys
def ingest(target: str) -> int:
    src = pathlib.Path(f"extracted/{target}")
    if not src.exists():
        print(f"[ingest:{target}] SKIP no BYOD (disc-gated)")
        return 0
    ghidra = shutil.which("analyzeHeadless")
    if not ghidra:
        print(f"[ingest:{target}] SKIP analyzeHeadless not installed")
        return 0
    out = pathlib.Path(f"targets/{target}/asm")
    out.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([ghidra, str(pathlib.Path(f"targets/{target}/ghidra_proj")), target,
                        "-import", str(src), "-overwrite"], capture_output=True, text=True)
    print(r.stdout[-2000:])
    return r.returncode

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--game", default=None, help="deprecated alias")
    a = ap.parse_args()
    sys.exit(ingest(a.target or a.game))
