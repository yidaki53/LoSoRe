import json
import pathlib
import shutil
import subprocess

import pytest

from tools import liero_read_handler_probe as probe


def test_buffer_skips_missing_original(tmp_path):
    """Oracle: absent original executable produces no fabricated run."""
    assert (
        probe.run_probe(tmp_path / "run", tmp_path, handler="buffer")["status"]
        == "skipped"
    )
    assert not (tmp_path / "run").exists()


def test_buffer_include_dependencies_compile_in_target(tmp_path):
    """Oracle: complete target compiles with real forwards and dependency include order."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    source = root / "targets/liero/src"
    result = subprocess.run(
        [
            "fpc",
            "-Mtp",
            f"-Fi{source}",
            f"-Fu{source}",
            f"-FU{tmp_path}",
            f"-FE{tmp_path}",
            str(source / "liero.pas"),
        ],
        check=False,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, (result.stdout + result.stderr).decode()


def test_buffer_original_pascal_and_mutants(tmp_path):
    """Oracle: actual dispatcher, refill bridge and callback continuation composition."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    if not all(shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")):
        pytest.skip("DOSBox/assembler/FPC unavailable")
    output = tmp_path / "buffer"
    result = probe.run_probe(output, root, handler="buffer")
    assert result["status"] == "passed"
    assert result["call_count"] == 8 * len(probe.fixtures("buffer"))
    assert probe.validate_saved_report(output, root) == result
    report_path = output / "result.json"
    original_report = report_path.read_bytes()
    forged_report = json.loads(original_report)
    forged_report["fixtures"]["buffer-cr-boundary"]["calls"][0]["position"] += 1
    report_path.write_text(json.dumps(forged_report))
    with pytest.raises(ValueError, match="comparison disagrees"):
        probe.validate_saved_report(output, root)
    report_path.write_bytes(original_report)
    directory = output / "candidate"
    fixture = output / "buffer-cr-boundary"
    capacity, payload = probe.fixtures("buffer")["buffer-cr-boundary"]
    trace = (fixture / "TRACE.BIN").read_bytes()
    candidate = (fixture / "PASCAL.BIN").read_bytes()
    for offset in (0, 10, 34, 36, 38, 40, 130, 258, 514 + 10):
        changed = bytearray(candidate)
        changed[offset] ^= 1
        assert (
            probe.compare_buffer(trace, bytes(changed), capacity, payload)["status"]
            == "failed"
        )
    with pytest.raises(ValueError, match="Pascal buffer records"):
        probe.compare_buffer(trace, candidate[:-1], capacity, payload)
    changed_trace = bytearray(trace)
    changed_trace[2 * 532 + 10] ^= 1
    with pytest.raises(ValueError):
        probe.compare_buffer(bytes(changed_trace), candidate, capacity, payload)
    candidate_path = fixture / "PASCAL.BIN"
    candidate_path.write_bytes(candidate[:-1])
    with pytest.raises(ValueError, match="stale refill artifact"):
        probe.validate_saved_report(output, root)
    candidate_path.write_bytes(candidate)
    for filename, old, new in (
        ("FUN_24dd_3923.inc", "if character <> 10 then", "if True then"),
        ("FUN_24dd_37ec.inc", "RegisterAX := savedCallback;", "RegisterAX := $390E;"),
        ("FUN_24dd_37ec.inc", "if GlobalWord6410 <> 0 then", "if False then"),
    ):
        source = directory / filename
        original = source.read_text()
        assert old in original
        source.write_text(original.replace(old, new))
        executable = probe.compile_candidate(directory, handler="buffer")
        mutant = output / "MUTANT.BIN"
        subprocess.run(
            [
                str(executable),
                str(fixture / "STATE.BIN"),
                str(fixture / "INPUT.TXT"),
                str(mutant),
                str(capacity),
            ],
            check=True,
            capture_output=True,
            timeout=30,
        )
        assert (
            probe.compare_buffer(trace, mutant.read_bytes(), capacity, payload)[
                "status"
            ]
            == "failed"
        )
        source.write_text(original)
    executable = probe.compile_candidate(directory, handler="buffer")
    for unsupported in (
        "unknown-callback",
        "unknown-method",
        "nil-source",
        "bad-count",
        "missing-adapter",
    ):
        rejected = subprocess.run(
            [
                str(executable),
                str(fixture / "STATE.BIN"),
                str(fixture / "INPUT.TXT"),
                str(output / "REJECTED.BIN"),
                str(capacity),
                unsupported,
            ],
            check=False,
            capture_output=True,
            timeout=30,
        )
        assert rejected.returncode == 211
