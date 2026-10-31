import json
import pathlib
import shutil
import struct
import subprocess
import sys

import pytest

from tools import liero_read_handler_probe as probe


@pytest.fixture
def successful_close():
    """Oracle: fixed open snapshot and independent close/no-write expectations."""
    state = bytearray((index * 37 + 19) % 256 for index in range(512))
    for offset, value in {
        0: 5,
        2: 0xD7B1,
        4: 128,
        12: 0xFF7A,
        14: 0x1234,
        16: 0x420C,
        18: 0x1234,
        20: 0x375E,
        22: 0x1234,
        28: 0x37D3,
        30: 0x1234,
    }.items():
        struct.pack_into("<H", state, offset, value)
    trace, candidate = bytearray(), bytearray()
    for stage in range(1, 11):
        status = 0 if stage < 9 else 6
        if stage >= 3:
            handle = stage - 3 if stage <= 7 else 5 if stage <= 9 else 0xFFFF
            struct.pack_into("<H", state, 0, handle)
            calls = max(0, stage - 7)
            candidate.extend(struct.pack("<HH", status, calls) + state)
        trace.extend(
            struct.pack(
                "<10H",
                stage,
                0x1234,
                0x1234,
                0x1234,
                0xFFFE,
                0xFDF8,
                0x202,
                status,
                0xFEFA,
                0xFDFA,
            )
            + state
        )
    return bytes(trace), bytes(candidate)


def test_close_reserved_live_repeated_and_invalid_handles(successful_close):
    """Oracle: handles 0..4 skip DOS, a real close succeeds, repeat/FFFF return 6."""
    result = probe.compare_close(*successful_close)
    assert result["status"] == "passed"
    assert [row["expected_return"] for row in result["calls"]] == [0] * 6 + [6, 6]
    assert [row["adapter_calls"] for row in result["calls"]] == [0] * 5 + [1, 2, 3]
    assert [row["handle"] for row in result["calls"]] == list(range(5)) + [5, 5, 0xFFFF]


@pytest.mark.parametrize("offset", [0, 2, 4, 6, 8, 12, 16, 52, 132, 259, 260, 515])
def test_close_rejects_candidate_return_adapter_or_memory_changes(
    successful_close, offset
):
    """Oracle: reserved-handle callbacks and any object/destination writes are rejected."""
    trace, candidate = successful_close
    changed = bytearray(candidate)
    changed[offset] ^= 1
    assert probe.compare_close(trace, bytes(changed))["status"] == "failed"


@pytest.mark.parametrize("offset", [0, 2, 4, 6, 8, 10, 16, 18])
def test_close_rejects_original_abi_changes(successful_close, offset):
    """Oracle: original RETF 4, preserved segments and object identity remain checked."""
    trace, candidate = successful_close
    changed = bytearray(trace)
    changed[2 * 532 + offset] ^= 1
    with pytest.raises(ValueError):
        probe.compare_close(bytes(changed), candidate)


def test_close_rejects_correlated_memory_write(successful_close):
    """Oracle: original/candidate agreement alone cannot excuse a spurious field reset."""
    trace, candidate = successful_close
    dos, host = bytearray(trace), bytearray(candidate)
    dos[2 * 532 + 20 + 8] ^= 1
    host[4 + 8] ^= 1
    assert probe.compare_close(bytes(dos), bytes(host))["status"] == "failed"


@pytest.mark.parametrize("size", [0, 515, 516, 4127, 4129])
def test_close_rejects_partial_or_extra_output(successful_close, size):
    """Oracle: require all eight complete candidate records."""
    trace, _ = successful_close
    with pytest.raises(ValueError, match="Pascal close records"):
        probe.compare_close(trace, bytes(size))


def test_close_skips_missing_original(tmp_path):
    """Oracle: BYOD gating must not create fabricated evidence."""
    assert (
        probe.run_probe(tmp_path / "run", tmp_path, handler="close")["status"]
        == "skipped"
    )
    assert not (tmp_path / "run").exists()


def test_close_boundary_holdout_rejects_signed_comparison(tmp_path):
    """Oracle: high-bit handles are original DOS errors, not signed reserved handles."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD or probe toolchain unavailable")
    output = tmp_path / "boundary"
    report = probe.run_probe(output, root, handler="close", suite="heldout-v2")
    assert report["status"] == "passed"
    assert report["call_count"] == 16
    assert probe.validate_saved_report(output, root) == report
    cases = report["fixtures"]["heldout-close-boundaries"]["calls"]
    assert [row["handle"] for row in cases[:5]] == [6, 7, 255, 0x8000, 0xFFFE]
    assert [row["original_return"] for row in cases[:5]] == [6] * 5
    directory = output / "candidate"
    source = directory / "FUN_24dd_37d3.inc"
    source.write_text(
        source.read_text().replace("handle <= 4", "Smallint(handle) <= 4")
    )
    executable = probe.compile_candidate(directory, "close")
    fixture = output / "heldout-close-boundaries"
    mutant = output / "MUTANT.BIN"
    subprocess.run(
        [
            str(executable),
            str(fixture / "STATE.BIN"),
            str(fixture / "INPUT.TXT"),
            str(mutant),
            "129",
        ],
        check=True,
        capture_output=True,
        timeout=30,
    )
    result = probe.compare_close(
        (fixture / "TRACE.BIN").read_bytes(),
        mutant.read_bytes(),
        boundaries=True,
    )
    assert result["status"] == "failed"
    assert result["calls"][3]["status"] == "failed"
    assert result["calls"][4]["status"] == "failed"


def test_unknown_handler_does_not_skip_or_fall_back(tmp_path):
    """Oracle: a misspelled oracle is an input error, even without BYOD."""
    with pytest.raises(ValueError, match="unknown file handler"):
        probe.run_probe(tmp_path / "run", tmp_path, handler="clsoe")
    assert not (tmp_path / "run").exists()


def test_standalone_close_cli_selects_stronger_holdout(tmp_path, monkeypatch):
    """Oracle: the reusable probe exposes the same explicit suite as the pilot."""
    calls = []

    def run(output, *, handler, suite):
        calls.append((handler, suite))
        return {"status": "passed"}

    monkeypatch.setattr(probe, "run_probe", run)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "probe",
            "--output",
            str(tmp_path / "out"),
            "--handler",
            "close",
            "--suite",
            "heldout-v2",
        ],
    )
    assert probe.main() == 0
    assert calls == [("close", "heldout-v2")]


def test_close_original_pascal_and_boundary_mutant(tmp_path):
    """Oracle: real DOS closes and a compiled candidate with a wrong reserved-handle cap."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    if not all(shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")):
        pytest.skip("DOSBox/assembler/FPC unavailable")
    output = tmp_path / "close"
    result = probe.run_probe(output, root, handler="close")
    assert result["status"] == "passed"
    assert result["call_count"] == 8
    assert probe.validate_saved_report(output, root) == result
    trace_path = output / "handle-lifecycle/TRACE.BIN"
    trace = trace_path.read_bytes()
    opened = probe.checked_records(trace)[1]
    assert opened["object"][8:12] == b"\xaa\x55\xff\xff"
    assert opened["object"][128:] == b"\xa5" * 128
    assert opened["destination"] == b"\x5a" * 256
    changed = bytearray(trace)
    changed[2 * 532 + 20 + 8] ^= 1
    trace_path.write_bytes(changed)
    with pytest.raises(ValueError, match="stale refill artifact"):
        probe.validate_saved_report(output, root)
    trace_path.write_bytes(trace)
    stored = output / "result.json"
    for field, value in (
        ("status", "failed"),
        ("call_count", 1),
        ("contract", {}),
        ("source_hashes", {}),
        ("artifact_hashes", {}),
        ("fixtures", {}),
    ):
        stored.write_text(json.dumps({**result, field: value}))
        with pytest.raises(ValueError):
            probe.validate_saved_report(output, root)
    stored.write_text(json.dumps(result))
    directory = output / "candidate"
    source = directory / "FUN_24dd_37d3.inc"
    original = source.read_text()
    assert "handle <= 4" in original
    source.write_text(original.replace("handle <= 4", "handle <= 3"))
    executable = probe.compile_candidate(directory, handler="close")
    fixture = output / "handle-lifecycle"
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
    compared = probe.compare_close(
        (fixture / "TRACE.BIN").read_bytes(), mutant.read_bytes()
    )
    assert compared["status"] == "failed"
    assert compared["calls"][4]["status"] == "failed"
    with pytest.raises(ValueError, match="artifact"):
        probe.validate_saved_report(output, root)
