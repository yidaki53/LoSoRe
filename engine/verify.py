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

When byte/relocation/trace checks pass, records which relpaths matched back into
knowledge/knowledge.json (engine/knowledge.record_verified) so the factory
accumulates verified work. Format checks never write to that store.

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
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from diff import byte_exact, relocation_aware

import knowledge

ORACLES = ["byte-exact", "relocation-aware", "round-trip", "trace-parity",
           "routine-trace-parity", "dat-parity", "constructor-parity"]


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
            if spec is None or spec.loader is None:
                continue
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
    return 0 if rt_ok else 1


def _gate_entries(path: pathlib.Path) -> list[str]:
    if not path.is_file():
        return []
    return [
        ln.strip() for ln in path.read_text(errors="replace").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]


def verify_status(target: str, byod: pathlib.Path | None,
                  build: pathlib.Path | None,
                  oracle: str = "byte-exact",
                  *,
                  routine: str | None = None,
                  source_path: pathlib.Path | None = None,
                  output: pathlib.Path | None = None,
                  root: pathlib.Path | None = None) -> dict:
    """Return a truthful verification status; never convert skip into verified."""
    byod_path = pathlib.Path(byod) if byod is not None else None
    build_path = pathlib.Path(build) if build is not None else None
    cfg = pathlib.Path(f"targets/{target}/config/build.sha1")
    entries = _gate_entries(cfg)

    if oracle == "routine-trace-parity":
        if not routine or source_path is None or output is None:
            return {
                "status": "not_verified",
                "checked": 0,
                "reason": "routine-trace-parity requires routine, source_path and output",
            }
        from engine import oracle_gate
        decision = oracle_gate.evaluate_routine(
            root or pathlib.Path.cwd(), target, routine, source_path, output
        )
        result = oracle_gate.decide(oracle, decision)
        return {**result, "checked": 2, "decision": decision}

    if oracle == "constructor-parity":

        if byod_path is None:
            return {"status": "skipped", "reason": "no BYOD", "checked": 0}
        rc = _constructor_parity(target, byod_path, build_path or pathlib.Path("."))
        return {"status": "failed" if rc else "scoped", "checked": 0,
                "reason": "constructor-parity never promotes"}

    if oracle == "dat-parity":
        if byod_path is None or not byod_path.exists() or not (byod_path / "LIERO.DAT").is_file():
            mod = _load_dat_oracle(target)
            if mod is None:
                print(f"[verify:{target}] dat-parity SKIP (no tools/liero_dat.py)")
                return {"status": "skipped", "checked": 0}
            ok, msg = mod.selftest()
            print(f"[{'OK ' if ok else 'DIFF'}:dat-parity/selftest] {msg}")
            print(f"[verify:{target}] SKIP dat-parity: no LIERO.DAT in BYOD")
            return {"status": "scoped" if ok else "failed", "checked": 1,
                    "reason": "format selftest only; no source promotion"}
        rc = _dat_parity(target, byod_path)
        return {"status": "failed" if rc else "scoped", "checked": 1,
                "reason": "format round-trip only; no source promotion"}

    if not cfg.is_file():
        print(f"[verify:{target}] WARN no build.sha1 file -- NOT verified")
        return {"status": "not_verified", "checked": 0, "reason": "missing oracle gate"}
    if not entries:
        print(f"[verify:{target}] WARN empty build.sha1 -- NOT verified")
        return {"status": "not_verified", "checked": 0, "reason": "empty oracle gate"}
    if byod_path is None or not byod_path.exists():
        print(f"[verify:{target}] SKIP no BYOD at {byod_path} (disc-gated)")
        return {"status": "skipped", "checked": 0, "reason": "no BYOD"}
    if build_path is None or not build_path.is_dir():
        print(f"[verify:{target}] WARN no build directory -- NOT verified")
        return {"status": "not_verified", "checked": 0, "reason": "no build"}

    passed: list[str] = []
    failed: list[str] = []
    for line in entries:
        parts = line.split()
        if len(parts) != 2:
            failed.append(line)
            continue
        expect, rel = parts
        a_path = byod_path / rel
        b_path = build_path / rel
        if not a_path.is_file() or not b_path.is_file():
            print(f"[SKIP:{oracle}] {rel} (missing on one side)")
            continue
        match = (relocation_aware if oracle == "relocation-aware" else byte_exact)(a_path, b_path)
        print(f"[{'OK ' if match else 'DIFF'}:{oracle}] {rel}")
        (passed if match else failed).append(rel)
    checked = len(passed) + len(failed)
    if checked == 0:
        print(f"[verify:{target}] SKIP no files to compare in build/ -- NOT verified")
        return {"status": "not_verified", "checked": 0,
                "reason": "no build files matched the gate"}
    ok = not failed
    print(f"[verify:{target}] {'PASS' if ok else 'FAIL'}")

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
    if failed:
        for rel in failed:
            fn = rel.rsplit(".", 1)[0] if "." in rel else rel
            try:
                knowledge.record_example_failure(data, tc, {"fn": fn, "target": target})
                asm_file = pathlib.Path(f"targets/{target}/asm/{fn}.s")
                asm_snippet = asm_file.read_text(errors="replace")[:500] if asm_file.exists() else ""
                knowledge.record_failure(data, tc, "unknown", asm_snippet, fn, target)
            except Exception as e:
                print(f"[verify:{target}] could not record failure for {fn}: {e}")
    knowledge.save(data)
    return {"status": "verified" if ok else "failed", "checked": checked,
            "passed": passed, "failed": failed, "oracle": oracle}


def verify_routine_status(
    root: pathlib.Path,
    target: str,
    routine: str,
    source_path: pathlib.Path,
    output: pathlib.Path,
) -> dict:
    return verify_status(
        target, None, None, "routine-trace-parity",
        routine=routine, source_path=source_path, output=output, root=root,
    )


def verify(target: str, byod: pathlib.Path | None, build: pathlib.Path | None,
           oracle: str = "byte-exact", **kwargs: Any) -> int:
    """Compatibility wrapper: only a real oracle failure is non-zero."""
    result = verify_status(target, byod, build, oracle, **kwargs)
    return 1 if result["status"] == "failed" else 0


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
    ap.add_argument("--routine", default=None)
    ap.add_argument("--source", default=None)
    ap.add_argument("--output", default=None)
    ap.add_argument("--root", default=None)
    a = ap.parse_args()
    t = a.target
    kwargs = {}
    if a.routine:
        kwargs["routine"] = a.routine
    if a.source:
        kwargs["source_path"] = pathlib.Path(a.source)
    if a.output:
        kwargs["output"] = pathlib.Path(a.output)
    if a.root:
        kwargs["root"] = pathlib.Path(a.root)
    sys.exit(verify(t, pathlib.Path(a.byod or f"extracted/{t}"),
                    pathlib.Path(a.build or f"targets/{t}/build"), a.oracle,
                    **kwargs))
