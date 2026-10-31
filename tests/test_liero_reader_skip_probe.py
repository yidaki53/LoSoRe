import json
import pathlib
import shutil
import subprocess

import pytest

from tools import liero_read_handler_probe as probe


def test_reader_skip_skips_missing_original(tmp_path):
    """Oracle: missing BYOD remains a skip."""
    assert (
        probe.run_probe(tmp_path / "run", tmp_path, handler="wrappers")["status"]
        == "skipped"
    )
    assert not (tmp_path / "run").exists()


def test_reader_skip_wrappers_retain_object_argument_and_match_original(tmp_path):
    """Oracle: actual wrappers, optional method and modeled far-argument handoff."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    if not all(shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")):
        pytest.skip("DOSBox/assembler/FPC unavailable")
    output = tmp_path / "wrappers"
    report = probe.run_probe(output, root, handler="wrappers")
    assert report["status"] == "passed"
    assert report["call_count"] == 8
    assert probe.validate_saved_report(output, root) == report

    fixture = output / "wrapper-error"
    trace = (fixture / "TRACE.BIN").read_bytes()
    candidate = (fixture / "PASCAL.BIN").read_bytes()
    for offset in (0, 2, 8, 24, 262, 514, 516, 518):
        changed = bytearray(candidate)
        changed[offset] ^= 1
        assert probe.compare_wrappers(trace, bytes(changed))["status"] == "failed"
    with pytest.raises(ValueError, match="Pascal wrapper records"):
        probe.compare_wrappers(trace, candidate[:-1])

    mutant_candidate = tmp_path / "candidate-mutant"
    shutil.copytree(output / "candidate", mutant_candidate)
    source = mutant_candidate / "FUN_24dd_3988.inc"
    original = source.read_text()
    source.write_text(original.replace("RegisterDI := 1;", "RegisterDI := 0;"))
    executable = probe.compile_candidate(mutant_candidate, handler="wrappers")
    mutant = tmp_path / "MUTANT.BIN"
    subprocess.run(
        [
            str(executable),
            str(fixture / "STATE.BIN"),
            str(fixture / "INPUT.TXT"),
            str(mutant),
            "1",
        ],
        check=True,
        capture_output=True,
        timeout=30,
    )
    assert probe.compare_wrappers(trace, mutant.read_bytes())["status"] == "failed"

    unsupported_state = tmp_path / "unsupported-state.bin"
    state = bytearray((fixture / "STATE.BIN").read_bytes())
    state[24:26] = b"\x01\x04"
    unsupported_state.write_bytes(state)
    rejected = subprocess.run(
        [
            str(output / "candidate" / probe.candidate_name("wrappers")),
            str(unsupported_state),
            str(fixture / "INPUT.TXT"),
            str(tmp_path / "unsupported-output.bin"),
            "1",
        ],
        check=False,
        capture_output=True,
        timeout=30,
    )
    assert rejected.returncode != 0

    saved_report = (output / "result.json").read_bytes()
    forged = json.loads(saved_report)
    forged["fixtures"]["wrapper-error"]["calls"][1]["retained_active"] = 1
    (output / "result.json").write_text(json.dumps(forged))
    with pytest.raises(ValueError, match="comparison disagrees"):
        probe.validate_saved_report(output, root)
    (output / "result.json").write_bytes(saved_report)
