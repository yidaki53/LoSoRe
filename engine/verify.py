"""Verify loop: oracle diff. Green with no game data (skip). NEVER a vacuous PASS.

Oracles:
  * byte-exact / relocation-aware / round-trip / trace-parity
      -> per-relpath diff of build/ vs BYOD, driven by config/build.sha1.
         An EMPTY build.sha1 is a WARN ("not verified"), NOT a pass.
  * dat-parity
      -> runs the target's format oracle (targets/<slug>/tools/liero_dat.py):
         a fixture selftest (always, real regression guard) + a BYOD round-trip
         when the disc is present.
  * constructor-parity
      -> original Liero constructor versus host Pascal over a fixed guarded
         corpus; reports scoped results and constraints, without any promotion.

When checks pass, records which relpaths matched back into knowledge/knowledge.json
(engine/knowledge.record_verified) so the factory accumulates verified work.

NEW (self-improvement):
  * On pass: retain an actual Pascal function body only when its matching
    function-level oracle passed; format-level checks do not certify drafts.
  * On fail: record_example_failure() + record_failure() via the specialised
    failure-classification LLM, so bad translations lose weight and the
    improve loop can avoid repeating mistakes.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import re
import sys
import uuid

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from diff import byte_exact, relocation_aware

import knowledge

ORACLES = ["byte-exact", "relocation-aware", "round-trip", "trace-parity", "dat-parity",
           "constructor-parity"]


def _yaml_value(path: pathlib.Path, key: str, default: str = "unknown") -> str:
    if not path.exists():
        return default
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip() or default
    return default


def _pascal_routine(path: pathlib.Path) -> str:
    text = path.read_text(errors="replace")
    declaration = re.search(
        r"(?im)^\s*(procedure|function)\s+[A-Za-z_]\w*", text
    )
    if not declaration:
        return ""
    body = text[declaration.start():]
    endings = list(re.finditer(r"(?im)^\s*end\s*;\s*$", body))
    return body[:endings[-1].end()].strip() if endings else ""


def _calling_convention(target: str, fn: str) -> str | None:
    metadata = pathlib.Path(f"targets/{target}/functions.json")
    if not metadata.exists():
        return None
    functions = json.loads(metadata.read_text(errors="replace")).get("functions", [])
    for function in functions:
        if function.get("name") == fn:
            return function.get("calling_convention")
    return None


def _promote_verified_pascal(target: str, relpaths: list[str], oracle: str,
                             data: dict, toolchain: str) -> None:
    root = pathlib.Path("targets") / target
    config = root / "config"
    compiler = _yaml_value(config / "toolchain.yaml", "compiler",
                           _yaml_value(config / "target.yaml", "compiler"))
    platform = _yaml_value(config / "toolchain.yaml", "platform",
                           _yaml_value(config / "target.yaml", "platform"))
    language = _yaml_value(config / "toolchain.yaml", "language",
                           _yaml_value(config / "target.yaml", "language"))
    confidence = _yaml_value(config / "toolchain.yaml", "compiler_confidence", "low")
    if language.lower() != "pascal" or not knowledge.confidence_ok(
        {"compiler_confidence": confidence}, "medium"
    ):
        return

    asm_dir = root / "asm"
    for relpath in relpaths:
        fn = pathlib.PurePosixPath(relpath).stem
        asm_file = asm_dir / f"{fn}.s"
        pascal_file = root / "src" / f"{fn}.inc"
        if (not fn or fn.startswith("_") or not asm_file.is_file()
                or not pascal_file.is_file()):
            continue
        pascal = _pascal_routine(pascal_file)
        if not pascal:
            continue
        example = {
            "fn": fn,
            "target": target,
            "compiler": compiler,
            "platform": platform,
            "language": "pascal",
            "oracle": oracle,
            "verification_status": "verified",
            "calling_convention": _calling_convention(target, fn),
            "asm": asm_file.read_text(errors="replace"),
            "decomp_c": (root / "decomp" / f"{fn}.c").read_text(errors="replace")
            if (root / "decomp" / f"{fn}.c").is_file() else "",
            "pascal": pascal,
        }
        try:
            example_id = knowledge.promote_verified_pascal_example(
                data, toolchain, example
            )
        except ValueError as exc:
            print(f"[verify:{target}] not training {fn}: {exc}")
            continue
        knowledge.record_example_success(
            data, toolchain, {**example, "example_id": example_id}
        )
        print(f"[verify:{target}] learned verified Pascal pair {fn} ({oracle})")


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
        data = knowledge.load()
        knowledge.record_verified(data, target, ["LIERO.DAT"], "dat-parity")
        knowledge.save(data)
    return 0 if rt_ok else 1


def verify(target: str, byod: pathlib.Path, build: pathlib.Path, oracle: str = "byte-exact") -> int:
    if oracle == "constructor-parity":
        return _constructor_parity(target, byod, build)
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
    failed: list[str] = []
    for line in entries:
        expect, rel = line.split()
        match = (relocation_aware if oracle == "relocation-aware" else byte_exact)(byod / rel, build / rel)
        print(f"[{'OK ' if match else 'DIFF'}:{oracle}] {rel}")
        ok = ok and match
        if match:
            passed.append(rel)
        else:
            failed.append(rel)
    print(f"[verify:{target}] {'PASS' if ok else 'FAIL'}")

    # --- self-improvement feedback ---
    data = knowledge.load()
    config = pathlib.Path(f"targets/{target}/config")
    compiler = _yaml_value(config / "toolchain.yaml", "compiler",
                           _yaml_value(config / "target.yaml", "compiler"))
    platform = _yaml_value(config / "toolchain.yaml", "platform",
                           _yaml_value(config / "target.yaml", "platform"))
    tc = knowledge.compiler_key(compiler, platform)

    if passed:
        knowledge.record_verified(data, target, passed, oracle)
        print(f"[verify:{target}] recorded {len(passed)} verified -> knowledge store")
        _promote_verified_pascal(target, passed, oracle, data, tc)
        knowledge.save(data)

    if failed:
        # Record failures for negative feedback
        for rel in failed:
            fn = rel.rsplit(".", 1)[0] if "." in rel else rel
            try:
                knowledge.record_example_failure(data, tc,
                                                 {"fn": fn, "target": target})
                asm_file = pathlib.Path(f"targets/{target}/asm/{fn}.s")
                asm_snippet = asm_file.read_text(errors="replace")[:500] if asm_file.exists() else ""
                knowledge.record_failure(
                    data, tc, "unknown", asm_snippet, fn, target,
                )
            except Exception as e:
                print(f"[verify:{target}] could not record failure for {fn}: {e}")
        knowledge.save(data)

    return 0 if ok else 1


def _constructor_parity(target: str, byod: pathlib.Path, build: pathlib.Path) -> int:
    """Oracle: scoped memory-effect comparison; never promote knowledge or source."""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
    from engine.scoped_verification import constructor_contract_graph
    from tools.liero_constructor_probe import run_probe

    if target != "liero":
        raise ValueError("constructor-parity currently supports only the Liero contract")
    if not (byod / "LIERO.EXE").is_file():
        print(f"[verify:{target}] constructor-parity SKIP no BYOD executable")
        return 0
    if byod.resolve() != pathlib.Path("extracted/liero").resolve():
        raise ValueError("constructor-parity requires the hash-bound extracted/liero input")
    output = build.resolve() / "constructor-parity" / uuid.uuid4().hex
    report = run_probe(output, root=pathlib.Path.cwd())
    if report["status"] == "passed":
        graph = constructor_contract_graph(pathlib.Path("targets/liero"), output)
        if graph.conflicts():
            raise ValueError("constructor handoff constraints conflict")
        graph.save(output / "constraints.json")
    print(f"[verify:{target}] constructor-parity {report['status'].upper()} "
          f"({report.get('case_count', 0)} cases; scoped, no promotion): {output}")
    return 1 if report["status"] == "failed" else 0


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
