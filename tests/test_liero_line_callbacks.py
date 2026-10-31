import json
import pathlib
import shutil
import subprocess

import pytest

from tools import liero_read_handler_probe as probe


def test_callbacks_skip_missing_original(tmp_path):
    """Oracle: missing BYOD is a skip without fabricated callback traces."""
    assert (
        probe.run_probe(tmp_path / "run", tmp_path, handler="callbacks")["status"]
        == "skipped"
    )
    assert not (tmp_path / "run").exists()


def test_line_callbacks_original_pascal_and_mutants(tmp_path):
    """Oracle: actual read/skip callbacks, exact memory, offsets, counts and continuations."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    if not all(shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")):
        pytest.skip("DOSBox/assembler/FPC unavailable")
    output = tmp_path / "callbacks"
    result = probe.run_probe(output, root, handler="callbacks")
    assert result["status"] == "passed"
    assert result["call_count"] == 8 * len(probe.fixtures("callbacks"))
    assert probe.validate_saved_report(output, root) == result
    report_path = output / "result.json"
    saved_report = report_path.read_bytes()
    changed_report = json.loads(saved_report)
    changed_report["fixtures"]["line-crlf"]["calls"][0]["consumed"] += 1
    report_path.write_text(json.dumps(changed_report))
    with pytest.raises(ValueError, match="comparison disagrees"):
        probe.validate_saved_report(output, root)
    report_path.write_bytes(saved_report)
    fixture = output / "line-crlf"
    _, payload = probe.fixtures("callbacks")["line-crlf"]
    trace = (fixture / "TRACE.BIN").read_bytes()
    candidate = (fixture / "PASCAL.BIN").read_bytes()
    for offset in (0, 2, 10, 22, 130, 258, 505, 507, 509, 511):
        changed = bytearray(candidate)
        changed[offset] ^= 1
        assert (
            probe.compare_callbacks(trace, bytes(changed), payload)["status"]
            == "failed"
        )
    changed = bytearray(trace)
    changed[2 * 532 + 10] ^= 1
    with pytest.raises(ValueError):
        probe.compare_callbacks(bytes(changed), candidate, payload)
    with pytest.raises(ValueError, match="Pascal callback records"):
        probe.compare_callbacks(trace, candidate[:-1], payload)
    candidate_path = fixture / "PASCAL.BIN"
    candidate_path.write_bytes(candidate[:-1])
    with pytest.raises(ValueError, match="stale refill artifact"):
        probe.validate_saved_report(output, root)
    candidate_path.write_bytes(candidate)
    for filename, old, new in (
        ("FUN_24dd_39ab.inc", "Dec(sourceOffset);", "sourceOffset := sourceOffset;"),
        ("FUN_24dd_390e.inc", "if character <> 10 then", "if True then"),
        ("FUN_24dd_39ab.inc", "count := $FFFF", "count := 0"),
    ):
        directory = output / "candidate"
        source = directory / filename
        original = source.read_text()
        assert old in original
        source.write_text(original.replace(old, new))
        executable = probe.compile_candidate(directory, handler="callbacks")
        mutant = output / "MUTANT.BIN"
        subprocess.run(
            [
                str(executable),
                str(fixture / "STATE.BIN"),
                str(fixture / "INPUT.TXT"),
                str(mutant),
                "128",
            ],
            check=True,
            capture_output=True,
            timeout=30,
        )
        assert (
            probe.compare_callbacks(trace, mutant.read_bytes(), payload)["status"]
            == "failed"
        )
        source.write_text(original)
