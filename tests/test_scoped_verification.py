import hashlib
import json

import pytest

from engine import scoped_verification, verify
from tools import liero_copy_routine_probe as copy_probe


def _copy_report_fixture(tmp_path):
    """Oracle: saved copy evidence must bind to current source bytes."""
    target = tmp_path / "targets/liero"
    output = target / "build/copy-parity/training"
    output.mkdir(parents=True)
    (tmp_path / "extracted/liero").mkdir(parents=True)
    (tmp_path / "extracted/liero/LIERO.EXE").write_bytes(b"fixture")
    (target / "src").mkdir()
    hashes = {}
    for routine in copy_probe.ROUTINES:
        content = f"procedure {routine}; begin end;".encode()
        (target / "src" / f"{routine}.inc").write_bytes(content)
        hashes[routine] = hashlib.sha256(content).hexdigest()
    runtime = b"unit LieroRuntime;"
    (target / "src/LieroRuntime.pas").write_bytes(runtime)
    report = {
        "status": "passed",
        "suite": "training",
        "case_count": 4,
        "binary_sha256": "fixture",
        "candidate_source_sha256": hashes,
        "candidate_runtime_sha256": hashlib.sha256(runtime).hexdigest(),
        "results": [
            {"routine": routine, "status": "passed"}
            for routine, _ in copy_probe.TRAINING_CASES
        ],
    }
    (output / "result.json").write_text(json.dumps(report))
    return target, output, report


def test_copy_scoped_reports_are_replayed_without_recovery_promotion(
    tmp_path, monkeypatch
):
    """Oracle: replayed scoped success remains separate from source recovery."""
    target, output, report = _copy_report_fixture(tmp_path)
    calls = []

    def replay(saved_output, root):
        calls.append((saved_output, root))
        return report

    monkeypatch.setattr(scoped_verification, "validate_copy_report", replay)

    checks = scoped_verification.load_scoped_checks(target)

    assert calls == [(output, tmp_path)]
    assert {check["function"] for check in checks} == set(copy_probe.ROUTINES)
    assert all(check["status"] == "passed" for check in checks)
    assert all(check["case_count"] == 2 for check in checks)
    assert all(check["suite"] == "training" for check in checks)
    assert not (target / "recovery.json").exists()


@pytest.mark.parametrize(
    "filename", ["FUN_24dd_0582.inc", "FUN_24dd_05e8.inc", "LieroRuntime.pas"]
)
def test_copy_scoped_reports_reject_changed_current_sources(
    tmp_path, monkeypatch, filename
):
    """Oracle: a historical passing candidate cannot validate changed sources."""
    target, _, report = _copy_report_fixture(tmp_path)
    monkeypatch.setattr(
        scoped_verification, "validate_copy_report", lambda *_args: report
    )
    (target / "src" / filename).write_text("changed")

    checks = scoped_verification.load_scoped_checks(target)

    assert len(checks) == 2
    assert all(check["status"] == "invalid" for check in checks)
    assert all("current" in check["reason"] for check in checks)


def test_copy_scoped_reports_disc_gate_and_reject_unbound_success(tmp_path):
    """Oracle: missing BYOD skips; an unbound success never passes."""
    target, output, _ = _copy_report_fixture(tmp_path)
    binary = tmp_path / "extracted/liero/LIERO.EXE"
    binary.unlink()
    checks = scoped_verification.load_scoped_checks(target)
    assert len(checks) == 2
    assert all(check["status"] == "skipped" for check in checks)

    binary.write_bytes(b"fixture")
    (output / "result.json").write_text('{"status":"passed"}')
    checks = scoped_verification.load_scoped_checks(target)
    assert all(check["status"] == "invalid" for check in checks)


def test_copy_scoped_reports_preserve_per_routine_failure(tmp_path, monkeypatch):
    """Oracle: failed copy cases must not be hidden by another routine's pass."""
    target, _, report = _copy_report_fixture(tmp_path)
    report["status"] = "failed"
    report["results"][0]["status"] = "failed"
    monkeypatch.setattr(
        scoped_verification, "validate_copy_report", lambda *_args: report
    )

    checks = scoped_verification.load_scoped_checks(target)

    assert [check["status"] for check in checks] == ["failed", "passed"]


def test_scoped_report_loader_marks_invalid_result_without_promotion(tmp_path):
    """Oracle: unbound stored success cannot certify a routine."""
    root = tmp_path / "targets/liero"
    output = root / "build/constructor-parity/attempt"
    output.mkdir(parents=True)
    (tmp_path / "extracted/liero").mkdir(parents=True)
    (tmp_path / "extracted/liero/LIERO.EXE").write_bytes(b"test-not-original")
    (output / "result.json").write_text(json.dumps({"status": "passed"}))
    checks = scoped_verification.load_scoped_checks(root)
    assert checks[0]["status"] == "invalid"
    assert "unrecognized" in checks[0]["reason"]
    assert not (root / "recovery.json").exists()


def test_scoped_report_loader_disc_gates_existing_reports(tmp_path):
    """Oracle: no source executable means no newly validated report."""
    root = tmp_path / "targets/liero"
    output = root / "build/constructor-parity/attempt"
    output.mkdir(parents=True)
    (output / "result.json").write_text('{"status":"passed"}')
    assert scoped_verification.load_scoped_checks(root)[0]["status"] == "skipped"


def test_comparator_scoped_report_loader_rejects_unbound_success(tmp_path):
    root = tmp_path / "targets/liero"
    output = root / "build/comparator-parity/attempt"
    output.mkdir(parents=True)
    (tmp_path / "extracted/liero").mkdir(parents=True)
    (tmp_path / "extracted/liero/LIERO.EXE").write_bytes(b"test-not-original")
    (output / "result.json").write_text(json.dumps({"status": "passed"}))

    checks = scoped_verification.load_scoped_checks(root)

    assert checks[0]["function"] == "FUN_24dd_3f86"
    assert checks[0]["status"] == "invalid"
    assert "unrecognized" in checks[0]["reason"]
    assert not (root / "recovery.json").exists()


def test_constructor_oracle_missing_byod_does_not_promote(tmp_path, capsys):
    """Oracle: missing input explicitly skips before generation or learning."""
    assert (
        verify.verify(
            "liero", tmp_path / "absent", tmp_path / "build", "constructor-parity"
        )
        == 0
    )
    assert "SKIP" in capsys.readouterr().out
    assert not (tmp_path / "build").exists()
