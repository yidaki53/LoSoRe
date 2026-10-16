"""Verify loop: oracle diff. Green with no game data (skip). NEVER a vacuous PASS.

Oracles:
  * byte-exact / relocation-aware / round-trip / trace-parity
      -> per-relpath diff of build/ vs BYOD, driven by config/build.sha1.
         An EMPTY build.sha1 is a WARN ("not verified"), NOT a pass.
  * dat-parity
      -> runs the target's format oracle (targets/<slug>/tools/liero_dat.py):
         a fixture selftest (always, real regression guard) + a BYOD round-trip
         when the disc is present.

When checks pass, records which relpaths matched back into knowledge/knowledge.json
(engine/knowledge.record_verified) so the factory accumulates verified work.
"""
from __future__ import annotations
import argparse, importlib.util, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from diff import byte_exact, relocation_aware  # noqa: E402
import knowledge  # noqa: E402

ORACLES = ["byte-exact", "relocation-aware", "round-trip", "trace-parity", "dat-parity"]


def _load_dat_oracle(target: str):
    """Import the target's format oracle (targets/<slug>/tools/liero_dat.py).

    Falls back to a sibling target that shares the format (e.g. liero-dos reuses
    liero's DAT oracle) so byte-identical targets still get the real selftest.
    """
    candidates = [pathlib.Path(f"targets/{target}/tools/liero_dat.py")]
    if target != "liero":
        candidates.append(pathlib.Path("targets/liero/tools/liero_dat.py"))
    for p in candidates:
        if p.exists():
            spec = importlib.util.spec_from_file_location(f"{target}_liero_dat", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    return None


def _dat_parity(target: str, byod: pathlib.Path) -> int:
    mod = _load_dat_oracle(target)
    if mod is None:
        print(f"[verify:{target}] dat-parity SKIP (no tools/liero_dat.py)")
        return 0
    ok, msg = mod.selftest()
    print(f"[{'OK ' if ok else 'DIFF'}:dat-parity/selftest] {msg}")
    if not ok:
        return 1
    dat = byod / "LIERO.DAT"
    if not dat.exists():
        print(f"[verify:{target}] dat-parity selftest PASS (no BYOD round-trip)")
        return 0
    rt_ok, cov, notes = mod.round_trip(dat.read_bytes())
    print(f"[{'OK ' if rt_ok else 'DIFF'}:dat-parity/round-trip] coverage={cov:.0%}")
    if rt_ok:
        knowledge.record_verified(knowledge.load(), target, ["LIERO.DAT"], "dat-parity")
    return 0 if rt_ok else 1


def verify(target: str, byod: pathlib.Path, build: pathlib.Path, oracle: str = "byte-exact") -> int:
    if oracle == "dat-parity":
        if not byod.exists():
            print(f"[verify:{target}] SKIP no BYOD at {byod} (disc-gated, CI passes)")
            return 0
        ok = _dat_parity(target, byod) == 0
        print(f"[verify:{target}] {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1

    cfg = pathlib.Path(f"targets/{target}/config/build.sha1")
    if not byod.exists():
        print(f"[verify:{target}] SKIP no BYOD at {byod} (disc-gated, CI passes)")
        return 0
    if not cfg.exists():
        print(f"[verify:{target}] no oracle config — NOT verified (residue build only)")
        return 0
    entries = [ln.strip() for ln in cfg.read_text().splitlines()
               if ln.strip() and not ln.strip().startswith("#")]
    if not entries:
        # An empty oracle gate means NOTHING was checked — this is not a pass.
        print(f"[verify:{target}] WARN empty build.sha1 — NOT verified "
              f"(residue build only; add '<sha1> <relpath>' entries to gate)")
        return 0
    ok = True
    passed: list[str] = []
    for line in entries:
        expect, rel = line.split()
        match = (relocation_aware if oracle == "relocation-aware" else byte_exact)(byod / rel, build / rel)
        print(f"[{'OK ' if match else 'DIFF'}:{oracle}] {rel}")
        ok = ok and match
        if match:
            passed.append(rel)
    print(f"[verify:{target}] {'PASS' if ok else 'FAIL'}")
    if passed:  # close the learn loop: record oracle-verified relpaths
        knowledge.record_verified(knowledge.load(), target, passed, oracle)
        print(f"[verify:{target}] recorded {len(passed)} verified -> knowledge store")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--byod", default=None)
    ap.add_argument("--build", default=None)
    ap.add_argument("--oracle", default="byte-exact", choices=ORACLES)
    a = ap.parse_args()
    t = a.target
    sys.exit(verify(t, pathlib.Path(a.byod or f"extracted/{t}"),
                    pathlib.Path(a.build or f"targets/{t}/build"), a.oracle))
