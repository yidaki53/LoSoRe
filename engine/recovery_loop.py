"""Unified RL-guided recovery loop with Matrix ordering and truthful gates."""

from __future__ import annotations

import argparse
import json
import pathlib
import uuid
from typing import Any

BASE = pathlib.Path(__file__).resolve().parent.parent
TARGETS = BASE / "targets"
KNOWLEDGE = BASE / "knowledge"

DEFAULT_MODELS = [
    "losore-llm4decompile-22b-v2:Q4_K_M",
    "qwen2.5-coder:14b-instruct-q4_K_M",
]

NON_PROMOTING_ORACLES = {"dat-parity", "constructor-parity"}


def _merge_legacy_rl_state(data: dict, knowledge_dir: pathlib.Path) -> None:
    legacy_path = knowledge_dir / "rl_state.json"
    if not legacy_path.is_file():
        return
    try:
        legacy = json.loads(legacy_path.read_text(errors="replace"))
    except Exception:
        return
    for key in ("q_table", "experience_buffer", "function_history", "epsilon",
                "cumulative_reward", "total_attempts", "total_verified",
                "total_failed", "verified_pascal_examples"):
        if key not in data and key in legacy:
            data[key] = legacy[key]


def _coverage(data: dict, target: str) -> float:
    target_data = data.get("targets", {}).get(target, {})
    verified: set[str] = set()
    for names in target_data.get("verified", {}).values():
        verified.update(names)
    total = target_data.get("num_functions", 0)
    return len(verified) / total if total else 0.0


def _recent_success_rate(data: dict, lang_key: str) -> float:
    attempts = data.get("total_attempts", 0)
    if not attempts:
        return 0.0
    return data.get("total_verified", 0) / attempts


def _validate_candidate(root: pathlib.Path, fn: str, run_compile_gate: bool,
                        draft_module: Any) -> dict:
    src = root / "src" / f"{fn}.inc"
    if not src.is_file():
        return {"parse": False, "compile": False, "reason": "no candidate file"}
    text = src.read_text(errors="replace")
    parse = text.rstrip().endswith("end;") and "UNMATCHED until verify passes" in text
    if "via skeleton" in text:
        parse = False
    if not parse:
        return {"parse": False, "compile": False, "reason": "unparsed or skeleton candidate"}
    if not run_compile_gate:
        return {"parse": True, "compile": None, "reason": "compile gate disabled"}
    broken, lines = draft_module._compile_errors(root)
    compile_ok = fn not in broken and "_MAKE_FAILED" not in broken
    return {
        "parse": True,
        "compile": compile_ok,
        "reason": "" if compile_ok else "; ".join(lines[:5]),
    }


def _toolchain_key(root: pathlib.Path, target: str,
                   knowledge_module: Any) -> str:
    path = root / "targets" / target / "config" / "toolchain.yaml"
    compiler = "unknown"
    platform = "unknown"
    if path.is_file():
        for line in path.read_text(errors="replace").splitlines():
            if line.startswith("compiler:"):
                compiler = line.split(":", 1)[1].strip() or compiler
            elif line.startswith("platform:"):
                platform = line.split(":", 1)[1].strip() or platform
    return knowledge_module.compiler_key(compiler, platform)


def _record_verified_function(data: dict, target: str, fn: str, oracle: str,
                              knowledge_module: Any) -> None:
    target_data = data.setdefault("targets", {}).setdefault(target, {})
    verified = target_data.setdefault("verified", {})
    names = verified.setdefault(oracle, [])
    if fn not in names:
        names.append(fn)
    knowledge_module.record_verified(data, target, sorted(names), oracle)


def run_recovery(
    target: str,
    max_iterations: int = 10,
    oracle: str = "routine-trace-parity",
    available_models: list[str] | None = None,
    byod: pathlib.Path | None = None,
    build: pathlib.Path | None = None,
    endpoint: str | None = None,
    max_tokens: int = 768,
    only_functions: set[str] | None = None,
    run_compile_gate: bool = True,
    root: pathlib.Path | None = None,
) -> dict:
    from engine import (
        draft,
        generic_synthesizer,
        knowledge,
        matrix,
        oracle_gate,
        rl_engine,
        target_packet,
        verify,
    )

    repo_root = pathlib.Path(root) if root is not None else BASE
    store = (
        repo_root / "knowledge" / "knowledge.json"
        if root is not None else pathlib.Path(knowledge.STORE)
    )
    models = list(available_models or DEFAULT_MODELS)
    data = knowledge.load(store)
    _merge_legacy_rl_state(data, store.parent)
    data["current_target"] = target
    lang_key = rl_engine.rl_lang_key(target)
    toolchain = _toolchain_key(repo_root, target, knowledge)
    target_data = data.setdefault("targets", {}).setdefault(target, {})
    target_data.setdefault("verified", {})
    target_data.setdefault("candidates", {})
    target_data.setdefault(
        "num_functions",
        matrix.load_inventory(target, repo_root).get("num_functions", 295),
    )

    target_root = repo_root / "targets" / target
    byod_path = pathlib.Path(byod) if byod else repo_root / "extracted" / target
    build_path = pathlib.Path(build) if build else target_root / "build"

    frontier = matrix.select_frontier(
        target, data, limit=max_iterations, only=only_functions, root=repo_root)
    outcomes: dict[str, int] = {}
    iterations = 0

    for row in frontier:
        fn = row["name"]
        iterations += 1
        data["current_function"] = fn
        coverage_before = _coverage(data, target)
        verified_examples = len(
            data.get("verified_pascal_examples", {}).get(toolchain, [])
        )
        state = rl_engine.encode_state(
            lang_key,
            coverage_before,
            _recent_success_rate(data, lang_key),
            instruction_count=row["instructions"],
            callee_resolved=not row["unverified_callees"],
            blocker="callees" if row["unverified_callees"] else None,
            verified_examples=verified_examples,
            example_quality=knowledge.recipe_for(data, "turbo-pascal-7", "dos"),
        )
        action = rl_engine.select_recovery_action(
            data, lang_key, instruction_count=row["instructions"],
            callee_resolved=not row["unverified_callees"],
            blocker="callees" if row["unverified_callees"] else None,
            available_models=models, state=state,
        )

        outcome = "failed"
        detail: dict[str, Any] = {}
        rl_recorded = False
        next_state = rl_engine.encode_state(
            lang_key,
            coverage_before,
            _recent_success_rate(data, lang_key),
            instruction_count=row["instructions"],
            callee_resolved=True,
            verified_examples=verified_examples,
        )

        if oracle == oracle_gate.DEFAULT_ORACLE:
            trial_dir = (
                repo_root / "trials" / "autonomous" / target / fn / uuid.uuid4().hex
            )
            trial_dir.mkdir(parents=True, exist_ok=False)
            method = generic_synthesizer.METHOD
            if not oracle_gate.routine_trace_supported(target, fn, root=repo_root):
                fixture_gate = {
                    "oracle": oracle,
                    "status": "skipped",
                    "promotion_eligible": False,
                    "reason": "no routine-trace fixture for target routine",
                }
                result = oracle_gate.record_gate_outcome(
                    data, lang_key, fn, fixture_gate, action["action"],
                    state=state, next_state=next_state, method=method,
                )
                detail = {
                    "pipeline": "target-packet/generic-ir/routine-trace-parity",
                    "gate": result,
                }
                outcome = result["outcome"]
                rl_recorded = True
                (trial_dir / "result.json").write_text(json.dumps({
                    "status": outcome,
                    "target": target,
                    "routine": fn,
                    "oracle": oracle,
                    "method": method,
                    "detail": detail,
                }, indent=2, sort_keys=True) + "\n")
            else:
                try:
                    evidence = target_packet.evidence_for_routine(repo_root, target, fn)
                    synthesis = generic_synthesizer.synthesize(evidence)
                    evidence_summary = {
                        "binary_sha256": evidence.get("binary", {}).get("sha256", ""),
                        "bytes_sha256": evidence.get("bytes", {}).get("sha256", ""),
                        "assembly_sha256": evidence.get("assembly_sha256", ""),
                        "evidence_gate": evidence.get("static_evidence", {}).get("gate", {}),
                        "source_policy": evidence.get("source_policy", {}),
                    }
                    synthesis_summary = {
                        key: synthesis[key]
                        for key in ("status", "method", "schema_version", "ir",
                                    "ir_sha256", "source_sha256", "source_policy")
                    }
                    detail = {
                        "pipeline": "target-packet/generic-ir/routine-trace-parity",
                        "evidence": evidence_summary,
                        "synthesis": synthesis_summary,
                    }
                    (trial_dir / "evidence.json").write_text(
                        json.dumps(evidence_summary, indent=2, sort_keys=True) + "\n"
                    )
                    (trial_dir / "synthesis.json").write_text(
                        json.dumps(synthesis_summary, indent=2, sort_keys=True) + "\n"
                    )
                    if synthesis["status"] != "synthesized":
                        gate: dict[str, Any] = {
                            "oracle": oracle,
                            "status": "skipped",
                            "promotion_eligible": False,
                            "reason": "generic synthesis produced no supported source",
                        }
                        result = oracle_gate.record_gate_outcome(
                            data, lang_key, fn, gate, action["action"],
                            state=state, next_state=next_state, method=method,
                        )
                        detail["gate"] = result
                        outcome = result["outcome"]
                        rl_recorded = True
                    else:
                        candidate = trial_dir / "candidate.inc"
                        candidate.write_text(synthesis["source"])
                        (trial_dir / "arm.json").write_text(json.dumps({
                            "status": "pending",
                            "target": target,
                            "routine": fn,
                            "method": method,
                            "oracle": oracle,
                            "evidence": evidence_summary,
                            "synthesis": synthesis_summary,
                            "action": action["action"],
                            "state": state,
                            "no_terminal_feedback_reuse": True,
                        }, indent=2, sort_keys=True) + "\n")
                        gate_result = verify.verify_routine_status(
                            repo_root, target, fn, candidate, trial_dir
                        )
                        detail["verification"] = gate_result
                        if (
                            gate_result.get("status") == "verified"
                            and gate_result.get("promotion_eligible")
                        ):
                            promotion = oracle_gate.promote(
                                repo_root, target, fn, method, candidate,
                                trial_dir / "terminal", str(trial_dir / "arm.json"),
                                oracle=oracle,
                                gate=gate_result.get("decision", gate_result),
                                action=action["action"], store=store, data=data,
                                state=state,
                            )
                            detail["promotion"] = promotion
                            if promotion["status"] == "promoted":
                                outcome = "verified"
                                rl_recorded = True
                            else:
                                failed_gate = {
                                    "oracle": oracle,
                                    "status": "failed",
                                    "promotion_eligible": False,
                                    "reason": promotion.get("reason", "promotion refused"),
                                }
                                record = oracle_gate.record_gate_outcome(
                                    data, lang_key, fn, failed_gate, action["action"],
                                    state=state, next_state=next_state, method=method,
                                )
                                detail["gate"] = record
                                outcome = record["outcome"]
                                rl_recorded = True
                        else:
                            record = oracle_gate.record_gate_outcome(
                                data, lang_key, fn, gate_result, action["action"],
                                state=state, next_state=next_state, method=method,
                                decision=gate_result.get("decision"),
                            )
                            detail["gate"] = record
                            outcome = record["outcome"]
                            rl_recorded = True
                except Exception as exc:
                    detail = {
                        "pipeline": "target-packet/generic-ir/routine-trace-parity",
                        "reason": f"{type(exc).__name__}: {exc}",
                    }
                    if not rl_recorded:
                        failure_gate = {
                            "oracle": oracle,
                            "status": "failed",
                            "promotion_eligible": False,
                            "reason": detail["reason"],
                        }
                        record = oracle_gate.record_gate_outcome(
                            data, lang_key, fn, failure_gate, action["action"],
                            state=state, next_state=next_state, method=method,
                        )
                        detail["gate"] = record
                        outcome = record["outcome"]
                        rl_recorded = True
            (trial_dir / "result.json").write_text(json.dumps({
                "status": outcome,
                "target": target,
                "routine": fn,
                "oracle": oracle,
                "method": method,
                "detail": detail,
            }, indent=2, sort_keys=True) + "\n")
        else:
            try:
                draft.draft(
                    target,
                    fn=fn,
                    use_llm=True,
                    model=action["model"],
                    endpoint=endpoint,
                    temperature=action["temperature"],
                    max_tokens=max_tokens,
                    retry_existing=True,
                    function_only=True,
                    run_compile_gate=False,
                )
                detail = _validate_candidate(target_root, fn, run_compile_gate, draft)
                outcome = (
                    "compiled"
                    if detail.get("compile") is not False and detail.get("parse")
                    else "failed"
                )
                result = verify.verify_status(target, byod_path, build_path, oracle)
                detail["verification"] = result
                if result["status"] == "verified":
                    outcome = "verified"
                elif result["status"] == "failed":
                    outcome = "failed"
                elif result["status"] == "compiled":
                    outcome = "compiled"
                elif outcome != "compiled":
                    outcome = "skipped"
            except Exception as exc:
                detail = {"reason": f"{type(exc).__name__}: {exc}"}
                outcome = "failed"

            if outcome == "verified" and oracle not in NON_PROMOTING_ORACLES:
                _record_verified_function(data, target, fn, oracle, knowledge)
            coverage_after = _coverage(data, target)
            next_state = rl_engine.encode_state(
                lang_key,
                coverage_after,
                _recent_success_rate(data, lang_key),
                instruction_count=row["instructions"],
                callee_resolved=True,
                verified_examples=len(
                    data.get("verified_pascal_examples", {}).get(toolchain, [])
                ),
            )
            gate = {
                "oracle": oracle,
                "status": outcome,
                "promotion_eligible": outcome == "verified",
                "reason": "legacy draft verification",
            }
            record = oracle_gate.record_gate_outcome(
                data, lang_key, fn, gate, action["action"],
                state=state, next_state=next_state,
                method="legacy-draft",
            )
            outcome = record["outcome"]
            rl_recorded = True

        if not rl_recorded:
            gate = {
                "oracle": oracle,
                "status": outcome,
                "promotion_eligible": outcome == "verified",
                "reason": "unrecorded recovery outcome",
            }
            record = oracle_gate.record_gate_outcome(
                data, lang_key, fn, gate, action["action"],
                state=state, next_state=next_state,
                method="unknown",
            )
            outcome = record["outcome"]

        target_data["candidates"][fn] = {
            "status": outcome,
            "attempts": data["function_history"][target][fn]["attempts"],
            "action": action["action"],
            "detail": detail,
        }
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        print(f"[recovery:{target}] {fn}: {outcome} ({action['action']})")
        knowledge.save(data, store)

        attempts = data.get("total_attempts", 0)
        if attempts >= 12 and data.get("total_verified", 0) / attempts < 0.25:
            print(f"[recovery:{target}] STOP yield floor: "
                  f"{data.get('total_verified', 0)}/{attempts} verified")
            break

    summary = {
        "target": target,
        "iterations": iterations,
        "oracle": oracle,
        "outcomes": outcomes,
        "coverage": _coverage(data, target),
        "total_attempts": data.get("total_attempts", 0),
        "total_verified": data.get("total_verified", 0),
        "cumulative_reward": data.get("cumulative_reward", 0.0),
        "epsilon": data.get("epsilon", 0.15),
        "dl_status": oracle_gate.dl_status(repo_root, target, data, store=store),
        "frontier": matrix.summary(target, data, root=repo_root),
    }
    knowledge.save(data, store)
    return summary


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the unified recovery loop")
    parser.add_argument("--target", required=True)
    parser.add_argument("--max-iterations", type=int, default=10)
    parser.add_argument(
        "--oracle",
        default="routine-trace-parity",
        choices=["dat-parity", "byte-exact", "relocation-aware", "round-trip",
                 "trace-parity", "routine-trace-parity", "constructor-parity"],
    )
    parser.add_argument("--model", action="append", default=None)
    parser.add_argument("--endpoint", default=None)
    parser.add_argument("--byod", default=None)
    parser.add_argument("--build", default=None)
    parser.add_argument("--max-tokens", type=int, default=768)
    parser.add_argument("--only", action="append", default=None)
    parser.add_argument("--no-compile-gate", action="store_true")
    parser.add_argument("--root", default=None)
    args = parser.parse_args(argv)

    result = run_recovery(
        target=args.target,
        max_iterations=args.max_iterations,
        oracle=args.oracle,
        available_models=args.model,
        byod=pathlib.Path(args.byod) if args.byod else None,
        build=pathlib.Path(args.build) if args.build else None,
        endpoint=args.endpoint,
        max_tokens=args.max_tokens,
        only_functions=set(args.only) if args.only else None,
        run_compile_gate=not args.no_compile_gate,
        root=pathlib.Path(args.root) if args.root else None,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
