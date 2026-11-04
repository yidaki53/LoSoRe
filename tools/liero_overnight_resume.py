"""Resume interrupted frozen leaf stress training with short-lived workers."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import pathlib
import shutil
import signal
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import liero_four_routine_pilot as pilot

ROUTINE = "FUN_24dd_3b22"


def load_frozen(prior: pathlib.Path):
    """Oracle: authenticate archived method against unchanged repository method."""
    freeze = json.loads((prior / "freeze.json").read_text())
    method = prior / "pilot-method.py"
    if (
        pilot.digest(method) != freeze["method_sha256"]
        or pilot.digest(ROOT / "tools/liero_four_routine_pilot.py")
        != freeze["method_sha256"]
    ):
        raise ValueError("frozen pilot differs from archived/current method")
    spec = importlib.util.spec_from_file_location("liero_frozen_overnight", method)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load frozen pilot")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate_leaf_freeze(ROOT, prior, freeze)
    return module, freeze


def check_no_holdout(prior: pathlib.Path, output: pathlib.Path) -> None:
    """Oracle: any attempted heldout is terminal, even without a saved result."""
    if any(prior.glob("**/heldout")) or any(output.glob("**/heldout")):
        raise ValueError("cannot resume after any heldout attempt")


def recover_candidate(module, prior: pathlib.Path, row: dict, freeze: dict) -> dict:
    """Oracle: replay contiguous saved training; incomplete/failed work is not refunded."""
    relative = pathlib.Path(row["directory"])
    directory = (prior / relative).resolve()
    if relative.is_absolute() or not directory.is_relative_to(prior.resolve()):
        raise ValueError("candidate path escapes original experiment")
    source = directory / "candidate.inc"
    if module.digest(source) != row["source_sha256"]:
        raise ValueError("candidate source changed")
    sketch = json.loads((directory / "sketch.json").read_text())
    contract = freeze["routines"][ROUTINE]["deductive_constraints"]
    rendered = module.render_shortstring_sketch(sketch, ROUTINE, contract)
    if source.read_text() != rendered:
        raise ValueError("candidate no longer matches recorded typed sketch")
    baseline = module.validate_leaf_probe(ROOT, directory / "training")
    if baseline["status"] != "passed":
        raise ValueError("candidate baseline did not pass")
    paths = sorted((directory / "stress").glob("batch-*"))
    if len(paths) > freeze["stress_training"]["maximum_batches"]:
        raise ValueError("history exceeds original coverage budget")
    if paths != [directory / "stress" / f"batch-{i:05d}" for i in range(len(paths))]:
        raise ValueError("stress history has gaps")
    cases = baseline["case_count"]
    status = "eligible"
    options = freeze["stress_training"]
    for index, path in enumerate(paths):
        if not (path / "result.json").is_file():
            raise ValueError(
                f"incomplete original batch cannot be silently retried: {path}"
            )
        report = module.validate_leaf_probe(ROOT, path)
        if report["source_sha256"] != row["source_sha256"] or report[
            "stress_corpus"
        ] != {
            "seed": options["seed"],
            "batch": index,
            "count": options["cases_per_batch"],
        }:
            raise ValueError("saved training differs from fixed source/corpus")
        cases += report["case_count"]
        if report["status"] != "passed":
            status = "stress-rejected"
            if index != len(paths) - 1:
                raise ValueError("work continued after candidate rejection")
    return {
        "directory": str(relative),
        "source_sha256": row["source_sha256"],
        "status": status,
        "training_cases": cases,
        "replayed_batches": len(paths),
    }


def run_worker(
    prior: pathlib.Path,
    output: pathlib.Path,
    source: pathlib.Path,
    descriptor: dict | None,
) -> dict:
    """Oracle: isolated original/compiled-Pascal check; crashes remain explicit failures."""
    module, _ = load_frozen(prior)
    source_root = source.resolve()
    if not source_root.is_relative_to(prior.resolve()):
        raise ValueError("worker source escapes prior experiment")
    result = module.run_leaf_probe(
        ROOT,
        output,
        ROUTINE,
        source_root.read_text(),
        "heldout" if descriptor is None else "training",
        stress=descriptor,
    )
    module.validate_leaf_probe(ROOT, output)
    return {
        "status": result["status"],
        "case_count": result["case_count"],
        "source_sha256": result["source_sha256"],
    }


def invoke_worker(
    prior: pathlib.Path,
    destination: pathlib.Path,
    source: pathlib.Path,
    descriptor: dict | None,
) -> dict:
    """Oracle: bounded child process with faulthandler; no automatic retry or hidden failure."""
    command = [
        sys.executable,
        "-X",
        "faulthandler",
        str(pathlib.Path(__file__).resolve()),
        "--prior",
        str(prior),
        "--output",
        str(destination),
        "--worker-source",
        str(source),
    ]
    if descriptor is not None:
        command.extend(["--worker-corpus", json.dumps(descriptor)])
    log = destination.parent / (destination.name + ".worker.log")
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("xb") as stream:
        completed = subprocess.run(
            command,
            stdout=stream,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
    if completed.returncode:
        raise RuntimeError(f"worker exit {completed.returncode}; diagnostic log: {log}")
    result = json.loads((destination / "result.json").read_text())
    return {
        "status": result["status"],
        "case_count": result["case_count"],
        "source_sha256": result["source_sha256"],
    }


def resume(prior: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: same finite search/budget, authenticated replay, one terminal selected holdout."""
    prior, output = prior.resolve(), output.resolve()
    check_no_holdout(prior, output)
    module, freeze = load_frozen(prior)
    history = json.loads((prior / "search.json").read_text())
    progress = json.loads((prior / "progress.json").read_text())
    if (
        freeze.get("optimise") is not True
        or freeze.get("string_sketch") is not True
        or history["status"] != "running"
        or len(history["candidates"]) != 2
        or (prior / "result.json").exists()
    ):
        raise ValueError("not an interrupted two-candidate stress search")
    # Reserve the bounded in-flight worker duration missing from the stale heartbeat.
    elapsed = progress["elapsed_seconds"] + 180
    options = freeze["stress_training"]
    if (
        type(elapsed) not in (int, float)
        or not 0 <= elapsed < options["maximum_seconds"]
    ):
        raise ValueError("original elapsed budget invalid/exhausted")
    output.mkdir(parents=True, exist_ok=False)
    with (prior / "continuation-claim.json").open("x") as claim:
        json.dump(
            {"output": str(output), "pid": os.getpid(), "started_at_unix": time.time()},
            claim,
        )
    pilot.save(
        output / "progress.json", {"status": "running", "stage": "replaying-history"}
    )
    started = time.monotonic()
    candidates = []
    for row in history["candidates"]:
        candidates.append(recover_candidate(module, prior, row, freeze))
        pilot.save(
            output / "progress.json",
            {
                "status": "running",
                "supervisor_pid": os.getpid(),
                "stage": "replaying-history",
                "candidates_replayed": len(candidates),
                "batches_replayed": sum(c["replayed_batches"] for c in candidates),
            },
        )
    counts = [row["replayed_batches"] for row in candidates]
    if max(counts) - min(counts) > 1:
        raise ValueError(
            "interrupted matched training history differs by more than one batch"
        )
    resume_freeze = {
        "prior": str(prior),
        "prior_freeze_sha256": module.digest(prior / "freeze.json"),
        "prior_search_sha256": module.digest(prior / "search.json"),
        "prior_progress_sha256": module.digest(prior / "progress.json"),
        "supervisor_sha256": module.digest(pathlib.Path(__file__)),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "prior_elapsed_seconds": elapsed,
        "remaining_seconds": options["maximum_seconds"] - elapsed,
        "candidates": candidates,
        "model_requests_added": 0,
        "policy": "No worker retry; same candidates/corpora/ranking; replay is not new evidence; one terminal holdout.",
    }
    pilot.save(output / "resume-freeze.json", resume_freeze)
    shutil.copy2(pathlib.Path(__file__), output / "supervisor-method.py")
    state = {
        "status": "running",
        "supervisor_pid": os.getpid(),
        "candidates": candidates,
        "prior": str(prior),
        "batches_completed": min(counts),
        "replayed_candidate_batches": sum(counts),
        "new_comparison_cases": 0,
        "source_recovered": 0,
        "examples_promoted": 0,
    }
    used = history["artifact_bytes"]
    stop = "coverage-budget-complete"
    for batch in range(min(counts), options["maximum_batches"]):
        if time.monotonic() - started >= resume_freeze["remaining_seconds"]:
            stop = "time-budget-exhausted"
            break
        if (
            used >= options["maximum_artifact_bytes"]
            or shutil.disk_usage(output).free < 2 * 1024**3
        ):
            raise RuntimeError("disk-budget-exhausted")
        module.validate_leaf_freeze(ROOT, prior, freeze)
        if (
            module.digest(prior / "freeze.json") != resume_freeze["prior_freeze_sha256"]
            or module.digest(prior / "search.json")
            != resume_freeze["prior_search_sha256"]
            or module.digest(prior / "progress.json")
            != resume_freeze["prior_progress_sha256"]
        ):
            raise ValueError("original history changed during continuation")
        eligible = [row for row in candidates if row["status"] == "eligible"]
        if not eligible:
            stop = "no-passing-candidate"
            break
        descriptor = {
            "seed": options["seed"],
            "batch": batch,
            "count": options["cases_per_batch"],
        }
        for index, row in enumerate(candidates):
            if row["status"] != "eligible" or batch < row["replayed_batches"]:
                continue
            destination = (
                output / f"candidate-{index}" / "stress" / f"batch-{batch:05d}"
            )
            pilot.save(
                output / "progress.json",
                {
                    **state,
                    "stage": "isolated-stress-worker",
                    "batch": batch,
                    "candidate": row["source_sha256"],
                    "worker_started_at_unix": time.time(),
                },
            )
            source = prior / row["directory"] / "candidate.inc"
            if module.digest(source) != row["source_sha256"]:
                raise ValueError("candidate changed before worker")
            report = invoke_worker(prior, destination, source, descriptor)
            if (
                report["source_sha256"] != row["source_sha256"]
                or report["case_count"] != descriptor["count"]
            ):
                raise ValueError("worker source/case identity mismatch")
            row["training_cases"] += report["case_count"]
            row["last_training_reference"] = str(destination)
            state["new_comparison_cases"] += report["case_count"]
            if report["status"] != "passed":
                row["status"] = "stress-rejected"
            used += sum(p.stat().st_size for p in destination.rglob("*") if p.is_file())
        state["batches_completed"] = batch + 1
        pilot.save(output / "search.json", state)
        if batch % 10 == 0:
            print(
                json.dumps(
                    {
                        "batch": batch + 1,
                        "new_comparison_cases": state["new_comparison_cases"],
                    }
                ),
                flush=True,
            )
    eligible = [row for row in candidates if row["status"] == "eligible"]
    state["stop_reason"] = stop
    if not eligible:
        state["status"] = "failed"
    else:
        selected = min(
            eligible,
            key=lambda row: (
                (prior / row["directory"] / "candidate.inc").stat().st_size,
                row["source_sha256"],
            ),
        )
        state.update(
            status="selected", selected_source_sha256=selected["source_sha256"]
        )
        pilot.save(output / "search.json", state)
        check_no_holdout(prior, output)
        destination = output / "heldout"
        destination.mkdir()
        pilot.save(
            destination / "attempted.json", {"selected": selected["source_sha256"]}
        )
        # The marker prevents a killed/failed holdout from being retried on resume.
        report = invoke_worker(
            prior,
            destination / "comparison",
            prior / selected["directory"] / "candidate.inc",
            None,
        )
        if report["source_sha256"] != selected["source_sha256"] or report[
            "case_count"
        ] != len(module.leaf_cases(ROUTINE, "heldout")):
            raise ValueError("terminal heldout source/case identity mismatch")
        state.update(
            status=report["status"],
            heldout_cases=report["case_count"],
            reference=str(destination / "comparison"),
        )
    pilot.save(output / "search.json", state)
    pilot.save(output / "result.json", state)
    pilot.save(output / "progress.json", {**state, "stage": "finished"})
    return state


def reconcile_interruption(
    prior: pathlib.Path,
    continuation: pathlib.Path,
    output: pathlib.Path,
) -> dict:
    """Oracle: replay finished training; native-crash residue blocks original selection.

    Diagnostic reruns cannot supply the missing original outcome or authorize
    changing the frozen stop rule to reach a holdout.
    """
    prior, continuation = prior.resolve(), continuation.resolve()
    check_no_holdout(prior, continuation)
    if output.exists():
        raise FileExistsError(output)
    module, freeze = load_frozen(prior)
    resumed = json.loads((continuation / "resume-freeze.json").read_text())
    search = json.loads((continuation / "search.json").read_text())
    failure = json.loads((continuation / "failure.json").read_text())
    exit_record = json.loads((continuation / "process-exit.json").read_text())
    if (
        resumed["prior"] != str(prior)
        or resumed["prior_freeze_sha256"] != module.digest(prior / "freeze.json")
        or resumed["prior_search_sha256"] != module.digest(prior / "search.json")
        or resumed["prior_progress_sha256"] != module.digest(prior / "progress.json")
        or resumed["supervisor_sha256"]
        != module.digest(continuation / "supervisor-method.py")
        or failure["status"] != "failed"
        or exit_record["exit_code"] == 0
        or search["status"] != "running"
        or len(search["candidates"]) != len(resumed["candidates"])
    ):
        raise ValueError(
            "continuation failure/history does not match frozen provenance"
        )
    original_rows = json.loads((prior / "search.json").read_text())["candidates"]
    if len(original_rows) != len(resumed["candidates"]):
        raise ValueError("continuation candidate count changed")
    checked, original_cases, new_cases = [], 0, 0
    options = freeze["stress_training"]
    artifact_identities = {}
    unknown = []
    for index, row in enumerate(original_rows):
        recovered = recover_candidate(module, prior, row, freeze)
        frozen_row = resumed["candidates"][index]
        if recovered != frozen_row:
            raise ValueError(
                "replayed original candidate differs from continuation freeze"
            )
        original_cases += recovered["replayed_batches"] * options["cases_per_batch"]
        stress = continuation / f"candidate-{index}" / "stress"
        paths = sorted(path for path in stress.glob("batch-*") if path.is_dir())
        expected = recovered["replayed_batches"]
        measured = 0
        for path in paths:
            if (
                path.name != f"batch-{expected:05d}"
                or expected >= options["maximum_batches"]
            ):
                raise ValueError(
                    "continuation training history has gaps or exceeds budget"
                )
            if not (path / "result.json").is_file():
                unknown.append(str(path))
                break
            report = module.validate_leaf_probe(ROOT, path)
            if (
                report["source_sha256"] != recovered["source_sha256"]
                or report["suite"] != "training"
                or report["stress_corpus"]
                != {
                    "seed": options["seed"],
                    "batch": expected,
                    "count": options["cases_per_batch"],
                }
                or report["case_count"] != options["cases_per_batch"]
                or report["status"] != "passed"
            ):
                raise ValueError(
                    "continuation source/corpus/outcome differs from checked search"
                )
            artifact_identities[
                str((path / "result.json").relative_to(continuation))
            ] = module.digest(path / "result.json")
            new_cases += report["case_count"]
            measured += 1
            expected += 1
        for log in sorted(stress.glob("batch-*.worker.log")):
            if not (
                stress / log.name.removesuffix(".worker.log") / "result.json"
            ).is_file():
                unknown.append(str(log))
        checkpoint = search["candidates"][index]
        if (
            checkpoint["source_sha256"] != recovered["source_sha256"]
            or checkpoint["status"] != "eligible"
            or checkpoint["training_cases"]
            > recovered["training_cases"] + measured * options["cases_per_batch"]
        ):
            raise ValueError("search checkpoint claims unsupported candidate results")
        checked.append(
            {
                **recovered,
                "continued_batches_replayed": measured,
                "last_completed_batch": expected - 1,
            }
        )
    if not unknown:
        raise ValueError(
            "no interrupted worker residue found; review stop classification"
        )
    result = {
        "status": "closed-incomplete",
        "stop_reason": "native-worker-crash-unresolved",
        "prior": str(prior),
        "continuation": str(continuation),
        "original_stress_comparisons_replayed": original_cases,
        "continued_stress_comparisons_replayed": new_cases,
        "total_completed_stress_comparisons": original_cases + new_cases,
        "candidates": checked,
        "unknown_attempts": unknown,
        "heldout_evaluations": 0,
        "selection_allowed": False,
        "source_recovered": 0,
        "examples_promoted": 0,
        "limitations": "Finite known-slice memory checks; replay is not new evidence. Diagnostic reruns cannot replace failed original work.",
        "history_hashes": {
            str(path): module.digest(path)
            for path in (
                prior / "freeze.json",
                continuation / "resume-freeze.json",
                continuation / "search.json",
                continuation / "failure.json",
                continuation / "process-exit.json",
            )
        },
        "completed_report_hashes": artifact_identities,
        "reconciler_sha256": module.digest(pathlib.Path(__file__)),
    }
    output.mkdir(parents=True)
    pilot.save(output / "result.json", result)
    shutil.copy2(pathlib.Path(__file__), output / "reconciler-method.py")
    return result


def assess_sketch_transfer(prior: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: fixed-shape eligibility census, not new semantics or routine acceptance."""
    module, freeze = load_frozen(prior)
    if output.exists():
        raise FileExistsError(output)
    from engine.instruction_facts import (
        bounded_byte_fill_contract,
        bounded_shortstring_contract,
    )

    paths = sorted((ROOT / "targets/liero/asm").glob("FUN_*.s"))
    output.mkdir(parents=True)
    pilot.save(
        output / "freeze.json",
        {
            "method_sha256": freeze["method_sha256"],
            "rules_sha256": module.digest(ROOT / "engine/instruction_facts.py"),
            "assessor_sha256": module.digest(pathlib.Path(__file__)),
            "entries": {path.name: module.digest(path) for path in paths},
            "policy": "No opcode/grammar additions or target Pascal reads; exact unrelocated byte shapes only.",
            "maximum_entries": len(paths),
            "model_requests": 0,
        },
    )
    supported, unsupported = [], []
    for path in paths:
        routine = path.stem
        try:
            report = module.prefix_transfer_report(ROOT, routine)
        except ValueError as exc:
            blockers = {
                "initialization relocation lies outside the supplied bytes": "MZ relocation overlaps exported entry boundary; cannot bind a complete frozen leaf shape",
                "prefix transfer routine lies outside the file-backed image": "Exported entry range is outside file-backed image; no complete bytes for frozen shape",
            }
            if str(exc) not in blockers:
                raise
            unsupported.append(
                {
                    "function": routine,
                    "reason": blockers[str(exc)],
                }
            )
            continue
        prefix = report["prefix"]
        if any(row["relocation_offset"] is not None for row in prefix["instructions"]):
            unsupported.append(
                {
                    "function": routine,
                    "reason": "relocated operands outside fixed leaf probe",
                }
            )
            continue
        raw = bytes.fromhex(report["routine_bytes_hex"])
        contract = None
        kind = None
        for name, recognizer in (
            ("fill", bounded_byte_fill_contract),
            ("shortstring", bounded_shortstring_contract),
        ):
            try:
                proposed = recognizer(raw)
            except ValueError:
                continue
            contract, kind = proposed, name
            break
        if contract is None:
            unsupported.append(
                {
                    "function": routine,
                    "reason": "outside frozen complete-byte vocabulary",
                }
            )
        else:
            supported.append(
                {
                    "function": routine,
                    "shape": kind,
                    "contract": contract,
                    "routine_sha256": report["routine_sha256"],
                    "previously_evaluated": routine in module.LEAF_PANEL,
                    "new_probe_eligible": routine in module.LEAF_PANEL,
                }
            )
    result = {
        "status": "assessed",
        "entries_examined": len(paths),
        "supported": supported,
        "unsupported": unsupported,
        "new_supported_entries": sum(
            not row["previously_evaluated"] for row in supported
        ),
        "model_requests": 0,
        "source_recovered": 0,
        "examples_promoted": 0,
        "expansion_allowed": False,
        "limitations": "Exact-shape eligibility only, not whole binary coverage; unseen shapes require new reviewed contracts and cannot be counted as frozen transfer.",
    }
    pilot.save(output / "result.json", result)
    return result


def main() -> int:
    """Oracle: explicit worker/supervisor exits; no source installation or promotion."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prior", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--worker-source", type=pathlib.Path)
    parser.add_argument("--worker-corpus")
    parser.add_argument("--reconcile-continuation", type=pathlib.Path)
    parser.add_argument("--assess-transfer", action="store_true")
    args = parser.parse_args()
    if (
        sum(
            bool(value)
            for value in (
                args.worker_source,
                args.reconcile_continuation,
                args.assess_transfer,
            )
        )
        > 1
    ):
        parser.error("worker, reconciliation and transfer modes are mutually exclusive")
    if args.reconcile_continuation or args.assess_transfer:
        if args.worker_corpus:
            parser.error("--worker-corpus requires worker mode")
        result = (
            reconcile_interruption(args.prior, args.reconcile_continuation, args.output)
            if args.reconcile_continuation
            else assess_sketch_transfer(args.prior, args.output)
        )
        print(
            json.dumps(
                {
                    key: value
                    for key, value in result.items()
                    if key
                    not in {"completed_report_hashes", "unsupported", "supported"}
                },
                indent=2,
            )
        )
        return 0
    if args.worker_source:
        result = run_worker(
            args.prior,
            args.output,
            args.worker_source,
            json.loads(args.worker_corpus) if args.worker_corpus else None,
        )
        print(json.dumps(result), flush=True)
        return 0
    if args.worker_corpus:
        parser.error("--worker-corpus requires --worker-source")
    existed = args.output.exists()

    def interrupted(signum, _frame):
        raise InterruptedError(f"supervisor received signal {signum}")

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    try:
        result = resume(args.prior, args.output)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        if not existed and args.output.is_dir():
            failure = {
                "status": "failed",
                "error_type": type(exc).__name__,
                "reason": str(exc),
            }
            pilot.save(args.output / "failure.json", failure)
            pilot.save(args.output / "progress.json", {**failure, "stage": "stopped"})
        raise
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
