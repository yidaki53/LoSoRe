import hashlib
import json

import pytest

from engine import run_state


def test_run_state_records_attempt_history_atomically(tmp_path):
    root = tmp_path / "targets" / "demo"
    root.mkdir(parents=True)
    source = root / "src" / "FUN_1.inc"
    source.parent.mkdir()
    source.write_text("before\n")
    assembly = root / "asm.s"
    assembly.write_text("MOV AX, BX\n")
    state = run_state.open_run(root, [assembly], {"oracle": "test"})

    attempt = run_state.start_attempt(
        state,
        "FUN_1",
        attempt=1,
        source_snapshot={source: source.read_bytes()},
    )
    run_state.finish_attempt(
        state,
        "FUN_1",
        attempt["attempt"],
        status="candidate-rejected",
        diagnostics=["syntax error"],
        source_sha256="abc123",
    )

    persisted = json.loads(state.path.read_text())
    recorded_attempt = persisted["routines"]["FUN_1"]["attempts"][0]
    assert recorded_attempt["attempt"] == 1
    assert recorded_attempt["status"] == "candidate-rejected"
    assert recorded_attempt["diagnostics"] == ["syntax error"]
    assert recorded_attempt["source_sha256"] == "abc123"
    assert recorded_attempt["started_at"] == attempt["started_at"]
    assert recorded_attempt["source_snapshot"] == {
        "src/FUN_1.inc": hashlib.sha256(b"before\n").hexdigest()
    }


def test_interrupted_attempt_restores_pre_attempt_sources(tmp_path):
    root = tmp_path / "targets" / "demo"
    source = root / "src" / "FUN_1.inc"
    source.parent.mkdir(parents=True)
    source.write_text("before\n")
    generated = source.parent / "FUN_2.inc"
    assembly = root / "asm.s"
    assembly.write_text("RET\n")
    state = run_state.open_run(root, [assembly], {"oracle": "test"})
    run_state.start_attempt(
        state,
        "FUN_1",
        attempt=1,
        source_snapshot={source: source.read_bytes()},
    )

    source.write_text("partial candidate\n")
    generated.write_text("partial generated file\n")
    run_state.restore_interrupted_attempt(state, "FUN_1", 1)

    assert source.read_text() == "before\n"
    assert not generated.exists()


def test_resume_rejects_changed_inputs_or_configuration(tmp_path):
    root = tmp_path / "targets" / "demo"
    root.mkdir(parents=True)
    assembly = root / "asm.s"
    assembly.write_text("RET\n")
    state = run_state.open_run(root, [assembly], {"oracle": "test"})
    run_id = state.run_id

    assembly.write_text("INT 21h\n")
    with pytest.raises(ValueError, match="input files changed"):
        run_state.open_run(root, [assembly], {"oracle": "test"}, run_id=run_id)

    assembly.write_text("RET\n")
    with pytest.raises(ValueError, match="configuration changed"):
        run_state.open_run(root, [assembly], {"oracle": "other"}, run_id=run_id)


def test_resume_requires_existing_run_id(tmp_path):
    root = tmp_path / "targets" / "demo"
    root.mkdir(parents=True)

    with pytest.raises(FileNotFoundError, match="run does not exist"):
        run_state.open_run(root, [], {}, run_id="missing-run")
