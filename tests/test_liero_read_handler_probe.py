import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_read_handler_probe as probe


@pytest.fixture
def successful_read():
    """Oracle: independently specified file/open state and exact refill memory effects."""
    capacity, payload = probe.fixtures()["length-129"]
    state = bytearray(512)
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
    state[128:256] = b"\xa5" * 128
    records, candidate = bytearray(), bytearray()
    position = 0
    for stage in range(1, 11):
        if stage >= 3:
            invalid = stage == 10
            if invalid:
                struct.pack_into("<H", state, 0, 0xFFFF)
            chunk = b"" if invalid else payload[position : position + capacity]
            position += len(chunk)
            struct.pack_into("<HH", state, 8, 0, len(chunk))
            state[128 : 128 + len(chunk)] = chunk
            candidate.extend(struct.pack("<H", 6 if invalid else 0) + state)
        records.extend(
            struct.pack(
                "<10H",
                stage,
                0x1234,
                0x1234,
                0x1234,
                0xFFFE,
                0xFDF8,
                0x202,
                6 if stage == 10 else 0,
                0xFEFA,
                0xFDFA,
            )
            + state
        )
    return bytes(records), bytes(candidate), capacity, payload


def test_refill_contract_checks_short_read_eof_and_invalid_handle(successful_read):
    """Oracle: distinct successful/EOF/error returns with exact unchanged buffer tails."""
    result = probe.compare(*successful_read)
    assert result["status"] == "passed"
    assert [call["bytes_read"] for call in result["calls"]] == [
        128,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    assert [call["expected_return"] for call in result["calls"]] == [0] * 7 + [6]


@pytest.mark.parametrize("offset", [0, 2, 6, 10, 12, 14, 50, 130, 257, 258, 513])
def test_refill_rejects_candidate_return_or_memory_changes(successful_read, offset):
    """Oracle: no return, pointer, destination or unchanged-buffer masking."""
    trace, candidate, capacity, payload = successful_read
    changed = bytearray(candidate)
    changed[offset] ^= 1
    assert probe.compare(trace, bytes(changed), capacity, payload)["status"] == "failed"


@pytest.mark.parametrize("offset", [0, 2, 4, 6, 8, 10, 16, 18])
def test_refill_rejects_original_abi_changes(successful_read, offset):
    """Oracle: stage order, preserved segments, stack cleanup and object identity."""
    trace, candidate, capacity, payload = successful_read
    changed = bytearray(trace)
    changed[2 * 532 + offset] ^= 1
    with pytest.raises(ValueError):
        probe.compare(bytes(changed), candidate, capacity, payload)


def test_refill_does_not_accept_original_and_candidate_agreeing_on_wrong_bytes(
    successful_read,
):
    """Oracle: independent file contract prevents correlated implementations passing."""
    trace, candidate, capacity, payload = successful_read
    dos, host = bytearray(trace), bytearray(candidate)
    dos[2 * 532 + 20 + 128] ^= 1
    host[2 + 128] ^= 1
    assert (
        probe.compare(bytes(dos), bytes(host), capacity, payload)["status"] == "failed"
    )


@pytest.mark.parametrize("size", [0, 513, 514, 4111, 4113])
def test_refill_rejects_incomplete_candidate(successful_read, size):
    """Oracle: eight complete Pascal records, not just process success."""
    trace, _, capacity, payload = successful_read
    with pytest.raises(ValueError, match="Pascal refill records"):
        probe.compare(trace, bytes(size), capacity, payload)


def test_refill_skips_missing_original(tmp_path):
    """Oracle: absent BYOD skips without creating successful-looking artifacts."""
    assert probe.run_probe(tmp_path / "run", tmp_path)["status"] == "skipped"
    assert not (tmp_path / "run").exists()


def test_refill_real_dos_pascal_and_compiled_mutant(tmp_path):
    """Oracle: actual original refill, actual Pascal body and deliberately wrong body."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    if not all(shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")):
        pytest.skip("DOSBox/assembler/FPC unavailable")
    output = tmp_path / "refill"
    result = probe.run_probe(output, root)
    assert result["status"] == "passed"
    assert result["call_count"] == 96
    assert probe.validate_saved_report(output, root) == result
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
    candidate = output / "candidate"
    source = candidate / "FUN_24dd_375e.inc"
    original = source.read_text()
    assert "capacity := objectWords^;" in original
    source.write_text(original.replace("capacity := objectWords^;", "capacity := 127;"))
    executable = probe.compile_candidate(candidate)
    fixture = output / "length-129"
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
    capacity, payload = probe.fixtures()["length-129"]
    compared = probe.compare(
        (fixture / "TRACE.BIN").read_bytes(), mutant.read_bytes(), capacity, payload
    )
    assert compared["status"] == "failed"
    assert compared["calls"][0]["status"] == "failed"
    with pytest.raises(ValueError, match="artifact"):
        probe.validate_saved_report(output, root)
