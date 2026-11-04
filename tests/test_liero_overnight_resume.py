import json
import subprocess
from types import SimpleNamespace

import pytest

from tools import liero_overnight_resume as resume


def test_any_holdout_attempt_blocks_continuation(tmp_path):
    """Oracle: even an empty or crashed heldout attempt is terminal."""
    prior, output = tmp_path / "prior", tmp_path / "new"
    prior.mkdir()
    (prior / "candidate" / "heldout").mkdir(parents=True)
    with pytest.raises(ValueError, match="heldout"):
        resume.check_no_holdout(prior, output)


def test_worker_native_crash_is_reported_without_retry(tmp_path, monkeypatch):
    """Oracle: reproduce observed signal exit in an isolated child."""
    calls = []

    def crashed(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, -11)

    monkeypatch.setattr(resume.subprocess, "run", crashed)
    with pytest.raises(RuntimeError, match="worker exit -11"):
        resume.invoke_worker(
            tmp_path / "prior",
            tmp_path / "worker",
            tmp_path / "source",
            {"seed": 1, "batch": 0, "count": 2},
        )
    assert len(calls) == 1
    assert (tmp_path / "worker.worker.log").exists()
    assert "faulthandler" in calls[0]


def setup_history(tmp_path, monkeypatch, *, terminal_failure=False):
    """Oracle: scripted frozen history, one completed batch per candidate."""
    prior = tmp_path / "prior"
    prior.mkdir()
    freeze = {
        "optimise": True,
        "string_sketch": True,
        "routines": {resume.ROUTINE: {"deductive_constraints": {}}},
        "stress_training": {
            "maximum_seconds": 1000,
            "maximum_batches": 3,
            "cases_per_batch": 2,
            "seed": 42,
            "maximum_artifact_bytes": 10**8,
        },
    }
    candidates = []
    for index in range(2):
        directory = prior / f"candidate-{index}"
        directory.mkdir()
        (directory / "candidate.inc").write_text("x" * (index + 1))
        (directory / "sketch.json").write_text(json.dumps({"index": index}))
        batch = directory / "stress" / "batch-00000"
        batch.mkdir(parents=True)
        (batch / "result.json").write_text("{}")
        candidates.append(
            {
                "directory": directory.name,
                "source_sha256": resume.pilot.digest(directory / "candidate.inc"),
                "status": "eligible",
            }
        )
    for name, value in {
        "freeze.json": freeze,
        "search.json": {
            "status": "running",
            "candidates": candidates,
            "artifact_bytes": 100,
        },
        "progress.json": {"status": "running", "elapsed_seconds": 10},
    }.items():
        (prior / name).write_text(json.dumps(value))

    def validate(root, directory):
        index = int(directory.parts[directory.parts.index("prior") + 1].split("-")[1])
        report = {
            "status": "passed",
            "case_count": 2,
            "source_sha256": candidates[index]["source_sha256"],
        }
        if directory.name.startswith("batch"):
            report["stress_corpus"] = {"seed": 42, "batch": 0, "count": 2}
        return report

    module = SimpleNamespace(
        digest=resume.pilot.digest,
        validate_leaf_probe=validate,
        validate_leaf_freeze=lambda *_: None,
        render_shortstring_sketch=lambda sketch, *_: "x" * (sketch["index"] + 1),
        leaf_cases=lambda *_: [None] * 264,
    )
    monkeypatch.setattr(resume, "load_frozen", lambda *_: (module, freeze))
    calls = []

    def worker(old, destination, source, descriptor):
        destination.mkdir(parents=True)
        calls.append(descriptor)
        if descriptor is None:
            assert (destination.parent / "attempted.json").is_file()
            selection = json.loads((destination.parents[1] / "search.json").read_text())
            assert selection["status"] == "selected"
        return {
            "status": "failed" if descriptor is None and terminal_failure else "passed",
            "case_count": 264 if descriptor is None else 2,
            "source_sha256": resume.pilot.digest(source),
        }

    monkeypatch.setattr(resume, "invoke_worker", worker)
    return prior, calls, freeze, module


@pytest.mark.parametrize("terminal_failure", [False, True])
def test_resume_preserves_history_and_budget_and_one_terminal_holdout(
    tmp_path,
    monkeypatch,
    terminal_failure,
):
    """Oracle: replayed batch zero is not rerun or counted as new evidence."""
    prior, calls, _, _ = setup_history(
        tmp_path,
        monkeypatch,
        terminal_failure=terminal_failure,
    )
    old_history = (prior / "search.json").read_bytes()
    result = resume.resume(prior, tmp_path / "continued")
    assert result["status"] == ("failed" if terminal_failure else "passed")
    assert [row["batch"] for row in calls if row is not None] == [1, 1, 2, 2]
    assert calls.count(None) == 1
    assert result["new_comparison_cases"] == 8
    assert result["replayed_candidate_batches"] == 2
    assert result["source_recovered"] == result["examples_promoted"] == 0
    assert (prior / "search.json").read_bytes() == old_history
    frozen = json.loads((tmp_path / "continued" / "resume-freeze.json").read_text())
    assert frozen["remaining_seconds"] == 810
    assert frozen["model_requests_added"] == 0


def test_incomplete_original_batch_blocks_resume_instead_of_refunding(
    tmp_path, monkeypatch
):
    """Oracle: interrupted outcome cannot be silently retried as new evaluation."""
    prior, _, freeze, module = setup_history(tmp_path, monkeypatch)
    (prior / "candidate-0" / "stress" / "batch-00001").mkdir()
    row = json.loads((prior / "search.json").read_text())["candidates"][0]
    with pytest.raises(ValueError, match="incomplete original batch"):
        resume.recover_candidate(module, prior, row, freeze)


def test_changed_candidate_blocks_history_replay(tmp_path, monkeypatch):
    """Oracle: no source change between measured history and continuation."""
    prior, _, freeze, module = setup_history(tmp_path, monkeypatch)
    row = json.loads((prior / "search.json").read_text())["candidates"][0]
    (prior / row["directory"] / "candidate.inc").write_text("changed")
    with pytest.raises(ValueError, match="source changed"):
        resume.recover_candidate(module, prior, row, freeze)


def test_changed_current_method_cannot_borrow_frozen_measurements(tmp_path):
    """Oracle: archived code must authenticate before executing or replaying it."""
    (tmp_path / "freeze.json").write_text(json.dumps({"method_sha256": "wrong"}))
    (tmp_path / "pilot-method.py").write_text("raise RuntimeError('must not execute')")
    with pytest.raises(ValueError, match="frozen pilot differs"):
        resume.load_frozen(tmp_path)


def test_supervisor_reports_failure_instead_of_stale_running(tmp_path, monkeypatch):
    """Oracle: child/native diagnostic errors must become persistent terminal state."""
    prior, output = tmp_path / "prior", tmp_path / "continued"
    prior.mkdir()

    def broken_resume(*_):
        output.mkdir()
        resume.pilot.save(output / "progress.json", {"status": "running"})
        raise RuntimeError("worker exit -11")

    monkeypatch.setattr(resume, "resume", broken_resume)
    monkeypatch.setattr(
        resume.sys,
        "argv",
        [
            "resume",
            "--prior",
            str(prior),
            "--output",
            str(output),
        ],
    )
    with pytest.raises(RuntimeError, match="worker exit"):
        resume.main()
    assert json.loads((output / "failure.json").read_text())["status"] == "failed"
    assert json.loads((output / "progress.json").read_text())["stage"] == "stopped"


def test_continuation_claim_prevents_simultaneous_duplicate_search(
    tmp_path, monkeypatch
):
    """Oracle: the same interrupted experiment cannot launch two selected holdouts."""
    prior, _, _, _ = setup_history(tmp_path, monkeypatch)
    (prior / "continuation-claim.json").write_text('{"existing":"other-run"}')
    with pytest.raises(FileExistsError):
        resume.resume(prior, tmp_path / "continued")


def setup_interrupted_continuation(tmp_path, monkeypatch):
    """Oracle: fixed complete history plus one native-failed worker with no outcome."""
    prior, _, freeze, module = setup_history(tmp_path, monkeypatch)
    continued = tmp_path / "continued"
    continued.mkdir()
    original_rows = json.loads((prior / "search.json").read_text())["candidates"]
    recovered = [
        resume.recover_candidate(module, prior, row, freeze) for row in original_rows
    ]
    method = continued / "supervisor-method.py"
    method.write_text("frozen supervisor")
    resumed = {
        "prior": str(prior),
        "prior_freeze_sha256": module.digest(prior / "freeze.json"),
        "prior_search_sha256": module.digest(prior / "search.json"),
        "prior_progress_sha256": module.digest(prior / "progress.json"),
        "supervisor_sha256": module.digest(method),
        "candidates": recovered,
    }
    search = {
        "status": "running",
        "candidates": [
            {**row, "training_cases": row["training_cases"] + 2} for row in recovered
        ],
    }
    for index in range(2):
        batch = continued / f"candidate-{index}" / "stress" / "batch-00001"
        batch.mkdir(parents=True)
        (batch / "result.json").write_text("{}")
    log = continued / "candidate-0" / "stress" / "batch-00002.worker.log"
    log.write_text("Fatal Python error: Segmentation fault")
    for name, value in {
        "resume-freeze.json": resumed,
        "search.json": search,
        "failure.json": {"status": "failed", "reason": "worker exit -11"},
        "process-exit.json": {"exit_code": 1},
    }.items():
        (continued / name).write_text(json.dumps(value))
    old_validate = module.validate_leaf_probe

    def validate(root, directory):
        if directory.is_relative_to(prior):
            return old_validate(root, directory)
        index = int(
            directory.parts[directory.parts.index("continued") + 1].split("-")[1]
        )
        return {
            "status": "passed",
            "case_count": 2,
            "suite": "training",
            "source_sha256": recovered[index]["source_sha256"],
            "stress_corpus": {"seed": 42, "batch": 1, "count": 2},
        }

    module.validate_leaf_probe = validate
    return prior, continued


def test_reconcile_native_failure_replays_without_authorizing_holdout(
    tmp_path, monkeypatch
):
    """Oracle: unknown attempt blocks acceptance even when all prior checks passed."""
    prior, continued = setup_interrupted_continuation(tmp_path, monkeypatch)
    result = resume.reconcile_interruption(prior, continued, tmp_path / "closure")
    assert result["status"] == "closed-incomplete"
    assert result["total_completed_stress_comparisons"] == 8
    assert result["continued_stress_comparisons_replayed"] == 4
    assert result["selection_allowed"] is False
    assert result["heldout_evaluations"] == 0
    assert len(result["unknown_attempts"]) == 1
    assert result["source_recovered"] == result["examples_promoted"] == 0


def test_reconcile_rejects_modified_frozen_provenance(tmp_path, monkeypatch):
    """Oracle: reconciliation cannot borrow reports from changed continuation history."""
    prior, continued = setup_interrupted_continuation(tmp_path, monkeypatch)
    (continued / "supervisor-method.py").write_text("changed")
    with pytest.raises(ValueError, match="provenance"):
        resume.reconcile_interruption(prior, continued, tmp_path / "closure")


def test_reconcile_cannot_erase_an_existing_holdout_attempt(tmp_path, monkeypatch):
    """Oracle: terminal holdout policy applies to closure as well as resume."""
    prior, continued = setup_interrupted_continuation(tmp_path, monkeypatch)
    (continued / "heldout").mkdir()
    with pytest.raises(ValueError, match="heldout"):
        resume.reconcile_interruption(prior, continued, tmp_path / "closure")


def test_transfer_assessment_does_not_invent_new_rules_or_probe_eligibility(
    tmp_path, monkeypatch
):
    """Oracle: fixed bytes can match a shape without a new routine having a checked probe."""
    root = tmp_path / "root"
    asm = root / "targets/liero/asm"
    asm.mkdir(parents=True)
    rules = root / "engine/instruction_facts.py"
    rules.parent.mkdir()
    rules.write_text("unchanged")
    for name in (
        "FUN_24dd_4905",
        "FUN_24dd_9999",
        "FUN_24dd_8888",
        "FUN_24dd_7777",
        "FUN_24dd_6666",
    ):
        (asm / f"{name}.s").write_text("entry identity")
    raw = "8bdc36c47f08368b4f06368a4704fcf3aaca0800"

    def report(_root, routine):
        if routine.endswith("6666"):
            raise ValueError(
                "prefix transfer routine lies outside the file-backed image"
            )
        if routine.endswith("7777"):
            raise ValueError(
                "initialization relocation lies outside the supplied bytes"
            )
        return {
            "prefix": {"instructions": []},
            "routine_bytes_hex": "c3" if routine.endswith("8888") else raw,
            "routine_sha256": routine,
        }

    module = SimpleNamespace(
        digest=resume.pilot.digest,
        prefix_transfer_report=report,
        LEAF_PANEL={"FUN_24dd_4905": (0x4905, 20)},
    )
    monkeypatch.setattr(resume, "ROOT", root)
    monkeypatch.setattr(
        resume, "load_frozen", lambda *_: (module, {"method_sha256": "frozen"})
    )
    result = resume.assess_sketch_transfer(tmp_path / "prior", tmp_path / "assessment")
    assert result["entries_examined"] == 5
    assert result["new_supported_entries"] == 1
    new = next(row for row in result["supported"] if not row["previously_evaluated"])
    assert new["new_probe_eligible"] is False
    assert result["expansion_allowed"] is False
    assert result["source_recovered"] == 0
    assert len(result["unsupported"]) == 3
    assert any("entry boundary" in row["reason"] for row in result["unsupported"])
    assert any("outside file-backed" in row["reason"] for row in result["unsupported"])
