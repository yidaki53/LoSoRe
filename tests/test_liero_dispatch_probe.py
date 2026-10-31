import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_read_handler_probe as probe


def test_dispatch_skips_missing_original(tmp_path):
    """Oracle: explicit BYOD gate, never fabricated dispatcher results."""
    assert (
        probe.run_probe(tmp_path / "run", tmp_path, handler="dispatch")["status"]
        == "skipped"
    )
    assert not (tmp_path / "run").exists()


def test_dispatch_original_leaves_synthetic_clobber_and_mutants(tmp_path):
    """Oracle: actual dispatcher composed with actual leaves; synthetic methods stay labeled."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    if not all(shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")):
        pytest.skip("DOSBox/assembler/FPC unavailable")
    output = tmp_path / "dispatch"
    result = probe.run_probe(output, root, handler="dispatch")
    assert result["status"] == "passed"
    assert result["call_count"] == 24
    assert probe.validate_saved_report(output, root) == result
    rows = result["fixtures"]["dispatch-short"]["calls"]
    assert [row["expected_return"] for row in rows] == [
        0,
        0,
        6,
        0,
        6,
        0x1234,
        0,
        0xFFFF,
    ]
    assert [row["expected_status"] for row in rows] == [
        0x55AA,
        0x55AA,
        6,
        6,
        6,
        0x1234,
        0x1234,
        0xFFFF,
    ]
    assert [row["method_kind"] for row in rows] == [
        "read",
        "close",
        "close",
        "close",
        "read",
        "synthetic",
        "synthetic",
        "synthetic",
    ]
    fixture = output / "dispatch-short"
    trace = (fixture / "TRACE.BIN").read_bytes()
    candidate = (fixture / "PASCAL.BIN").read_bytes()
    _, payload = probe.fixtures("dispatch")["dispatch-short"]
    for offset in (0, 2, 8, 24, 132, 260, 511):
        changed = bytearray(candidate)
        changed[offset] ^= 1
        assert (
            probe.compare_dispatch(trace, bytes(changed), payload)["status"] == "failed"
        )
    for offset in (0, 2, 4, 6, 8, 10, 16, 18):
        changed = bytearray(trace)
        changed[2 * 532 + offset] ^= 1
        with pytest.raises(ValueError):
            probe.compare_dispatch(bytes(changed), candidate, payload)
    for size in (0, len(candidate) - 1, len(candidate) + 1):
        with pytest.raises(ValueError, match="Pascal dispatch records"):
            probe.compare_dispatch(trace, bytes(size), payload)
    directory = output / "candidate"
    source = directory / "FUN_24dd_374d.inc"
    original = source.read_text()
    for name, old, new in (
        ("clear-status", "if RegisterAX <> 0 then", "if True then"),
        ("restore-offset", "RegisterDI := savedOffset;", "RegisterDI := 0;"),
        ("restore-segment", "RegisterES := savedSegment;", "RegisterES := 0;"),
    ):
        assert old in original
        source.write_text(original.replace(old, new))
        executable = probe.compile_candidate(directory, handler="dispatch")
        mutant = output / (name + ".BIN")
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
        comparison = probe.compare_dispatch(trace, mutant.read_bytes(), payload)
        assert comparison["status"] == "failed", name
    with pytest.raises(ValueError, match="artifact"):
        probe.validate_saved_report(output, root)
    source.write_text(original)
    executable = probe.compile_candidate(directory, handler="dispatch")
    invalid_state = output / "UNKNOWN.BIN"
    state = bytearray((fixture / "STATE.BIN").read_bytes())
    struct.pack_into("<H", state, 20, 0xDEAD)
    invalid_state.write_bytes(state)
    rejected = subprocess.run(
        [
            str(executable),
            str(invalid_state),
            str(fixture / "INPUT.TXT"),
            str(output / "UNKNOWN-RESULT.BIN"),
            "128",
        ],
        check=False,
        capture_output=True,
        timeout=30,
    )
    assert rejected.returncode == 12
    driver = directory / "probe_liero_dispatch_handler.pas"
    driver_source = driver.read_text()
    assert "LieroDispatchMethod := InvokeMethod;" in driver_source
    driver.write_text(
        driver_source.replace(
            "LieroDispatchMethod := InvokeMethod;", "LieroDispatchMethod := nil;"
        )
    )
    executable = probe.compile_candidate(directory, handler="dispatch")
    rejected = subprocess.run(
        [
            str(executable),
            str(fixture / "STATE.BIN"),
            str(fixture / "INPUT.TXT"),
            str(output / "NO-RESOLVER.BIN"),
            "128",
        ],
        check=False,
        capture_output=True,
        timeout=30,
    )
    assert rejected.returncode == 211
