"""Shared oracle gate for routine promotion, RL outcomes and DL eligibility."""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

from engine import (
    contract_oracle,
    frozen_source_eval,
    knowledge,
    model_training,
    rl_engine,
)
from tools import liero_four_routine_pilot as pilot

DEFAULT_ORACLE = "routine-trace-parity"
PROMOTING_ORACLES = {
    "byte-exact",
    "relocation-aware",
    "round-trip",
    "trace-parity",
    DEFAULT_ORACLE,
}
NON_PROMOTING_ORACLES = {"dat-parity", "constructor-parity"}


def routine_trace_supported(
    target: str, routine: str, root: pathlib.Path | str | None = None
) -> bool:
    if target != "liero":
        return False
    from tools import liero_source_trial as trial
    if routine in {*trial.PANEL, *trial.DISCOVERY_PANEL}:
        return True
    root_path = pathlib.Path(root) if root is not None else pathlib.Path(__file__).resolve().parent.parent
    return contract_oracle.supported(root_path, target, routine)


def routine_trace_blocker(
    target: str, routine: str, root: pathlib.Path | str | None = None
) -> str | None:
    root_path = pathlib.Path(root) if root is not None else pathlib.Path(__file__).resolve().parent.parent
    if routine_trace_supported(target, routine, root_path):
        return None
    try:
        contract_oracle.fixture(root_path, target, routine)
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"
    return None


def _yaml_value(path: pathlib.Path, key: str, default: str = "unknown") -> str:
    if not path.is_file():
        return default
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip() or default
    return default


def _toolchain_key(root: pathlib.Path, target: str) -> str:
    path = root / "targets" / target / "config" / "toolchain.yaml"
    return knowledge.compiler_key(
        _yaml_value(path, "compiler"), _yaml_value(path, "platform")
    )


def _append_unique(items: list[str], values: list[str]) -> None:
    for value in values:
        if value not in items:
            items.append(value)


def suite_passed(result: dict, suite: str) -> bool:
    if result.get("compile", {}).get("status") != "passed":
        return False
    entry = result.get("suites", {}).get(suite, {})
    return (
        entry.get("original", {}).get("status") == "passed"
        and entry.get("candidate", {}).get("status") == "passed"
    )


def evaluate_routine(
    root: pathlib.Path | str,
    target: str,
    routine: str,
    source_path: pathlib.Path | str,
    output: pathlib.Path | str,
    evaluator: Any = frozen_source_eval,
) -> dict:
    root_path = pathlib.Path(root)
    source = pathlib.Path(source_path)
    output_path = pathlib.Path(output)
    if evaluator is frozen_source_eval and contract_oracle.supported(
        root_path, target, routine
    ):
        evaluator = contract_oracle
    training_output = output_path / "training"
    terminal_output = output_path / "terminal"

    training = evaluator.run_training(root_path, training_output, source, routine)
    training_passed = suite_passed(training, "training")
    decision: dict = {
        "oracle": DEFAULT_ORACLE,
        "status": "failed",
        "promotion_eligible": False,
        "training": training,
        "terminal": {},
    }
    if not training_passed:
        decision["reason"] = "training parity did not pass"
        return decision

    terminal = evaluator.run(
        root_path,
        terminal_output,
        source,
        routine,
        suites=("terminal",),
    )
    terminal_passed = suite_passed(terminal, "terminal")
    decision["terminal"] = terminal
    if terminal_passed:
        decision["status"] = "verified"
        decision["promotion_eligible"] = True
        decision["reason"] = "training and terminal parity passed"
    else:
        decision["reason"] = "terminal parity did not pass"
    return decision


def decide(oracle: str, decision: dict) -> dict:
    if oracle in NON_PROMOTING_ORACLES:
        return {
            "oracle": oracle,
            "status": "scoped",
            "promotion_eligible": False,
            "reason": f"{oracle} never promotes source",
        }
    promoted = bool(decision.get("promotion_eligible")) and decision.get("status") == "verified"
    return {
        "oracle": oracle,
        "status": "verified" if promoted else "failed",
        "promotion_eligible": promoted,
        "reason": decision.get("reason", ""),
    }


def dl_readiness(
    root: pathlib.Path,
    target: str,
    data: dict | None = None,
    store: pathlib.Path | None = None,
) -> dict:
    root_path = pathlib.Path(root)
    store_path = store or root_path / "knowledge" / "knowledge.json"
    state = knowledge.load(store_path) if data is None else data
    toolchain = _toolchain_key(root_path, target)
    return model_training.training_readiness(
        state, toolchain, targets_root=root_path / "targets"
    )


def dl_status(
    root: pathlib.Path,
    target: str,
    data: dict | None = None,
    store: pathlib.Path | None = None,
) -> dict:
    readiness = dl_readiness(root, target, data, store)
    eligible = not readiness["pascal_corpus_blockers"]
    return {
        "status": "eligible" if eligible else "blocked",
        "oracle_gated": True,
        "readiness": readiness,
    }


def reward_for(outcome: str) -> float:
    if outcome == "verified":
        return 1.0
    if outcome == "compiled" or outcome == "scoped":
        return 0.25
    if outcome == "skipped":
        return 0.0
    return -0.5


def record_gate_outcome(
    data: dict,
    lang_key: str,
    fn: str,
    gate: dict,
    action: str,
    state: str | None = None,
    next_state: str | None = None,
    method: str | None = None,
    decision: dict | None = None,
) -> dict:
    status = gate.get("status")
    outcome = "verified" if status == "verified" else (
        "compiled" if status == "compiled" else (
            "skipped" if status in {"scoped", "skipped", "not_verified"} else "failed"
        )
    )
    reward = reward_for(outcome)
    rl_engine.record_recovery_outcome(
        data, lang_key, fn, outcome, reward, outcome == "verified", action,
        state=state, next_state=next_state,
    )
    record = {
        "outcome": outcome,
        "reward": reward,
        "verified": outcome == "verified",
        "oracle": gate.get("oracle", DEFAULT_ORACLE),
        "gate_status": gate.get("status"),
        "promotion_eligible": bool(gate.get("promotion_eligible")),
        "method": method,
        "decision": decision,
    }
    replay = data.get("experience_buffer", {}).get(lang_key, [])
    if replay:
        replay[-1]["gate_outcome"] = record
    return record


def promote(
    root: pathlib.Path,
    target: str,
    routine: str,
    method: str,
    source_path: pathlib.Path,
    eval_dir: pathlib.Path,
    archive: str,
    oracle: str = DEFAULT_ORACLE,
    gate: dict | None = None,
    action: str | None = None,
    store: pathlib.Path | None = None,
    data: dict | None = None,
    state: str | None = None,
    next_state: str | None = None,
    allow_supersede: bool = False,
) -> dict:
    if oracle not in PROMOTING_ORACLES:
        return {
            "status": "refused",
            "reason": f"{oracle} never promotes source",
            "routine": routine,
            "method": method,
        }
    if gate is None:
        return {
            "status": "refused",
            "reason": "promotion requires an explicit oracle gate decision",
            "routine": routine,
            "method": method,
        }
    verdict = decide(oracle, gate)
    if verdict["status"] != "verified":
        return {
            "status": "refused",
            "reason": verdict["reason"],
            "routine": routine,
            "method": method,
            "decision": verdict,
        }
    root = pathlib.Path(root)
    source_path = pathlib.Path(source_path)
    source = source_path.read_text()
    source_sha256 = hashlib.sha256(source.encode()).hexdigest()
    src_dir = root / "targets" / target / "src"
    src_path = src_dir / f"{routine}.inc"
    store = store or root / "knowledge" / "knowledge.json"
    if data is None:
        data = knowledge.load(store)
    verified: set[str] = set()
    for names in data.get("targets", {}).get(target, {}).get("verified", {}).values():
        verified.update(names)
    previous_source = src_path.read_text() if src_path.is_file() else None
    previous_source_sha256 = (
        hashlib.sha256(previous_source.encode()).hexdigest()
        if previous_source is not None else ""
    )
    if routine in verified and previous_source != source and not allow_supersede:
        return {
            "status": "promotion-conflict",
            "reason": "target already oracle-verified with a different source",
            "routine": routine,
            "method": method,
            "source_sha256": source_sha256,
            "previous_source_sha256": previous_source_sha256,
            "target": str(src_path.relative_to(root)),
        }
    src_dir.mkdir(parents=True, exist_ok=True)
    if previous_source != source:
        if previous_source is not None:
            preserved = pathlib.Path(archive).parent / "previous_source.inc"
            preserved.write_text(previous_source)
        src_path.write_text(source)

    asm_path = root / "targets" / target / "asm" / f"{routine}.s"
    assembly_sha256 = pilot.digest(asm_path) if asm_path.is_file() else ""
    rel_source = str(src_path.relative_to(root))
    ledger_source = f"src/{routine}.inc"
    rel_result = str(eval_dir.relative_to(root))
    recovery_path = root / "targets" / target / "recovery.json"
    recovery = json.loads(recovery_path.read_text())
    functions = recovery.setdefault("functions", {})
    entry = functions.setdefault(routine, {})
    evidence = entry.setdefault("evidence", {})
    _append_unique(
        evidence.setdefault("state_and_memory_effects", []), [rel_result, archive]
    )
    verification = entry.setdefault("verification", {})
    _append_unique(verification.setdefault("host_test_references", []), [rel_result, archive])
    verification["host_test_status"] = "passed"
    verification["notes"] = (
        f"{method}: compile passed; original and candidate matched the frozen "
        f"training and terminal routine suites. Source sha256 {source_sha256}. "
        "This is routine-level scoped evidence, not full-game or DOSBox visual parity."
    )
    entry.update({
        "status": "source_recovered",
        "source_file": ledger_source,
        "source_sha256": source_sha256,
        "assembly_sha256": assembly_sha256,
        "reviewer": method,
        "review_notes": verification["notes"],
        "unrecoverable_reason": "",
    })
    recovery_path.write_text(json.dumps(recovery, indent=2, sort_keys=True) + "\n")

    target_data = data.setdefault("targets", {}).setdefault(target, {})
    target_data.setdefault("num_functions", len(functions))
    routines = target_data.setdefault("verified", {}).setdefault(oracle, [])
    if routine not in routines:
        routines.append(routine)
    target_data["verified"][oracle] = sorted(routines)
    target_data["num_verified"] = len(routines)
    target_data["coverage"] = round(len(routines) / target_data["num_functions"], 4)
    target_data["coverage_oracle"] = oracle
    key = _toolchain_key(root, target)
    knowledge.promote_verified_pascal_example(data, key, {
        "fn": routine,
        "target": target,
        "compiler": _yaml_value(
            root / "targets" / target / "config" / "toolchain.yaml", "compiler"
        ),
        "platform": _yaml_value(
            root / "targets" / target / "config" / "toolchain.yaml", "platform"
        ),
        "oracle": oracle,
        "asm": asm_path.read_text(errors="replace") if asm_path.is_file() else "",
        "pascal": source,
        "verification_status": "verified",
        "language": "pascal",
    }, store)

    lang_key = rl_engine.rl_lang_key(target)
    verified_examples = len(data.get("verified_pascal_examples", {}).get(key, []))
    if state is None:
        state = rl_engine.encode_state(
            lang_key, target_data["coverage"], 0.0,
            verified_examples=verified_examples,
        )
    if next_state is None:
        next_state = rl_engine.encode_state(
            lang_key, target_data["coverage"], 1.0,
            verified_examples=verified_examples,
        )
    record = record_gate_outcome(
        data, lang_key, routine, verdict, action or method,
        state=state, next_state=next_state, method=method, decision=gate,
    )
    knowledge.save(data, store)
    return {
        "status": "promoted",
        "routine": routine,
        "method": method,
        "oracle": oracle,
        "source_sha256": source_sha256,
        "previous_source_sha256": previous_source_sha256,
        "target": rel_source,
        "evidence": [rel_result, archive],
        "rl_outcome": record,
        "dl_readiness": dl_readiness(root, target, data, store),
    }
