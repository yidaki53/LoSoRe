import json
import pathlib
import shutil
import struct

import pytest

from tools import liero_file_probe as probe


@pytest.fixture
def successful_trace():
    """Oracle: independently specified normal fixture snapshots, not emulator output."""
    data = bytearray()
    strings = [
        b"",
        b"",
        b"ALPHA",
        b"ALPHA",
        b"BETA",
        b"BETA",
        b"BETA",
        b"ALPHA",
        b"ALPHA",
        b"ALPHA",
    ]
    positions = [
        (0, 0),
        (0, 0),
        (5, 13),
        (7, 13),
        (11, 13),
        (13, 13),
        (0, 0),
        (5, 13),
        (7, 13),
        (7, 13),
    ]
    for index in range(10):
        record = bytearray(532)
        struct.pack_into(
            "<10H",
            record,
            0,
            index + 1,
            0x1234,
            0x1234,
            0x1234,
            0xFFFE,
            0xFDF4 if index in {2, 4, 7} else 0xFDF8,
            0x202,
            0,
            0xFEFA,
            0xFDFA,
        )
        words = {
            2: 0xD7B0 if index in {0, 9} else 0xD7B1,
            4: 128,
            8: positions[index][0],
            10: positions[index][1],
            12: 0xFF7A,
            14: 0x1234,
            16: 0x420C,
            18: 0x1234,
            20: 0 if index == 0 else 0x375E,
            22: 0 if index == 0 else 0x1234,
            28: 0 if index == 0 else 0x37D3,
            30: 0 if index == 0 else 0x1234,
        }
        for offset, value in words.items():
            struct.pack_into("<H", record, 20 + offset, value)
        record[276] = len(strings[index])
        record[277 : 277 + len(strings[index])] = strings[index]
        data.extend(record)
    return bytes(data)


def test_probe_validates_exact_fixture_and_stack_handoff(successful_trace):
    """Oracle: ten required stages, checked data and preserved object pointer argument."""
    records = probe.validate_trace(successful_trace, "two_lines")
    assert len(records) == 10
    assert records[2]["sp"] + 4 == records[3]["sp"]
    assert records[2]["string_hex"] == b"ALPHA".hex()
    assert records[4]["string_hex"] == b"BETA".hex()
    assert records[7]["string_hex"] == b"ALPHA".hex()
    assert records[9]["mode"] == 0xD7B0


@pytest.mark.parametrize(
    ("stage", "offset"),
    [
        (0, 0),  # stage identifier
        (2, 10),  # retained argument stack
        (3, 14),  # I/O status
        (1, 4),  # DS preservation
        (4, 8),  # frame pointer
        (4, 16),  # object identity
        (1, 22),  # mode
        (1, 40),  # input method offset
        (1, 42),  # relocated input method segment
        (2, 28),  # consumed-buffer offset
        (2, 32),  # internal buffer pointer
        (2, 277),  # returned string
    ],
)
def test_probe_rejects_runtime_mutation(successful_trace, stage, offset):
    """Oracle: failed runtime observations cannot produce a passed probe."""
    changed = bytearray(successful_trace)
    changed[stage * 532 + offset] ^= 1
    with pytest.raises(ValueError):
        probe.validate_trace(bytes(changed), "two_lines")


@pytest.mark.parametrize("data", [b"", bytes(531), bytes(532), bytes(5321)])
def test_probe_rejects_incomplete_or_extra_snapshots(data):
    """Oracle: partial trace or emulator exit alone is not a successful observation."""
    with pytest.raises(ValueError, match="ten complete"):
        probe.decode_trace(data)


def test_probe_skips_missing_byod(tmp_path):
    """Oracle: no executable means an explicit disc-gated skip, never fabricated results."""
    result = probe.run_probe(tmp_path / "output", root=tmp_path)
    assert result["status"] == "skipped"
    assert not (tmp_path / "output").exists()


def test_probe_rejects_mismatched_original_region():
    """Oracle: never run substituted bytes under original-code provenance."""
    manifest = {"image_mapping": {"header_bytes": 64}}
    with pytest.raises(ValueError, match="does not match executable"):
        probe._build_image(
            b"\x90",
            bytes(0x20000),
            manifest,
            [{"address": "0x28409", "bytes_hex": "33d2"}],
        )


@pytest.mark.parametrize("harness", [b"", bytes(0x3500)])
def test_probe_rejects_invalid_harness_extent(harness):
    """Oracle: instrumentation must stay separate from the copied original routines."""
    with pytest.raises(ValueError, match="empty or overlaps"):
        probe._build_image(harness, b"", {"image_mapping": {"header_bytes": 64}}, [])


def test_probe_rejects_conflicting_code_overlap():
    """Oracle: original regions cannot overwrite instrumentation with different bytes."""
    binary = bytearray(0x15000)
    binary[0x14F10] = 0xCC
    with pytest.raises(ValueError, match="overlap with different bytes"):
        probe._build_image(
            b"\x90",
            bytes(binary),
            {"image_mapping": {"header_bytes": 64}},
            [{"address": "0x24ed0", "bytes_hex": "cc"}],
        )


def test_original_file_routines_in_dosbox(tmp_path):
    """Oracle: actual original instructions, DOS file services and a buffer-boundary case."""
    repository = pathlib.Path(__file__).resolve().parents[1]
    if not (repository / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD executable unavailable")
    if any(shutil.which(tool) is None for tool in ("dosbox", "as", "ld")):
        pytest.skip("DOSBox or GNU assembler/linker unavailable")
    output = tmp_path / "DOS probe with spaces"
    report = probe.run_probe(output, root=repository)
    assert report["status"] == "passed"
    assert report["oracle"] == "isolated_original_bytes_dosbox"
    assert set(report["fixtures"]) == {"two_lines", "cr_at_refill_boundary"}
    boundary = report["fixtures"]["cr_at_refill_boundary"]["snapshots"]
    assert boundary[2]["buffer_position"] == [127, 128]
    assert boundary[3]["buffer_position"] == [1, 7]
    assert boundary[4]["string_hex"] == b"BETA".hex()
    assert len(report["limitations"]) == 4
    assert json.loads((output / "result.json").read_text()) == report
