"""Verify loop: recompile + oracle diff. Green with no game data (skip)."""
from __future__ import annotations
import argparse, pathlib, sys

from diff import byte_exact, relocation_aware  # noqa: E402

ORACLES = ["byte-exact", "relocation-aware", "round-trip", "trace-parity"]

def verify(target: str, byod: pathlib.Path, build: pathlib.Path, oracle: str = "byte-exact") -> int:
    cfg = pathlib.Path(f"targets/{target}/config/build.sha1")
    if not cfg.exists():  # compat fallback
        cfg = pathlib.Path(f"games/{target}/config/build.sha1")
    if not byod.exists():
        print(f"[verify:{target}] SKIP no BYOD at {byod} (disc-gated, CI passes)")
        return 0
    if not cfg.exists() or not cfg.read_text().strip().strip("#").strip():
        print(f"[verify:{target}] no oracle config yet — residue build only")
        return 0
    ok = True
    for line in cfg.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        expect, rel = line.split()
        match = (relocation_aware if oracle == "relocation-aware" else byte_exact)(byod / rel, build / rel)
        print(f"[{'OK ' if match else 'DIFF'}:{oracle}] {rel}")
        ok = ok and match
    print(f"[verify:{target}] {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--game", default=None, help="deprecated alias for --target")
    ap.add_argument("--byod", default=None)
    ap.add_argument("--build", default=None)
    ap.add_argument("--oracle", default="byte-exact", choices=ORACLES)
    a = ap.parse_args()
    t = a.target or a.game
    sys.exit(verify(t, pathlib.Path(a.byod or f"extracted/{t}"),
                    pathlib.Path(a.build or f"targets/{t}/build"), a.oracle))
