import json
import struct

import pytest

from tools.binary_census import build_census


def _make_mz(image_size=64, extra_paragraphs=2):
    header_size = 32
    file_size = header_size + image_size
    pages, last_page_bytes = divmod(file_size, 512)
    if last_page_bytes:
        pages += 1
    data = bytearray(file_size)
    struct.pack_into(
        "<14H",
        data,
        0,
        0x5A4D,
        last_page_bytes,
        pages,
        1,
        header_size // 16,
        extra_paragraphs,
        0xFFFF,
        0,
        0x20,
        0,
        0x10,
        0,
        0x1C,
        0,
    )
    struct.pack_into("<HH", data, 0x1C, 4, 0)
    return bytes(data)


def _target(tmp_path, image_size=64):
    root = tmp_path / "targets" / "test-target"
    (root / "asm").mkdir(parents=True)
    (root / "decomp").mkdir()
    entries = [
        {
            "name": "entry",
            "entry": "1000:0010",
            "size": 4,
            "num_instructions": 3,
        },
        {
            "name": "FUN_1000_0016",
            "entry": "1000:0016",
            "size": 4,
            "num_instructions": 0,
        },
        {
            "name": "FUN_1000_0042",
            "entry": "1000:0042",
            "size": 1,
            "num_instructions": 0,
        },
    ]
    (root / "functions.json").write_text(
        json.dumps({"program": "TEST.EXE", "num_functions": 3, "functions": entries})
    )
    (root / "asm" / "entry.s").write_text(
        "; entry  entry=1000:0010 size=4\n"
        "1000:0010  MOV AX,[0x0030]\n"
        "1000:0012  CALL 0x2000:0016\n"
        "1000:0015  RET\n"
    )
    (root / "asm" / "FUN_1000_0016.s").write_text(
        "; FUN_1000_0016  entry=1000:0016 size=4\n"
        "1000:0016  RET\n"
    )
    (root / "asm" / "FUN_1000_0042.s").write_text(
        "; FUN_1000_0042  entry=1000:0042 size=1\n"
    )
    binary = tmp_path / "TEST.EXE"
    binary.write_bytes(_make_mz(image_size=image_size))
    return root, binary


def test_census_maps_mz_entry_and_only_counts_decoded_file_backed_ranges(
    tmp_path,
):
    root, binary = _target(tmp_path)

    report = build_census(root, binary)

    assert report["binary"]["declared_file_size_matches"]
    assert report["binary"]["load_image_bytes"] == 64
    assert report["binary"]["relocation_count"] == 1
    assert report["address_mapping"]["entry_mapping_valid"]
    assert report["address_mapping"]["load_segment_inferred_from_entry"] == "1000"
    assert report["summary"]["assembly_instruction_count_total"] == 4
    assert report["summary"]["instruction_count_mismatch_count"] == 1
    assert report["summary"]["functions_by_range_class"] == {
        "file_backed_image": 2,
        "minimum_allocated_uninitialized_tail": 1,
    }
    assert report["summary"]["file_backed_function_range_count"] == 2
    assert report["summary"]["file_backed_function_union_bytes"] == 8
    assert report["summary"]["unclassified_file_backed_bytes"] == 56
    assert report["summary"]["empty_assembly_exports"] == [
        "FUN_1000_0042"
    ]
    assert report["routines"][0]["cfg"]["call"] == 1
    assert report["summary"]["direct_call_edge_count"] == 1
    assert report["summary"]["direct_calls_to_exported_entries"] == 1
    assert report["summary"]["calls_without_static_target_count"] == 0
    assert report["routines"][0]["direct_calls"][0]["target_functions"] == [
        "FUN_1000_0016"
    ]
    assert report["routines"][0]["direct_calls"][0]["target_flat_address"] == (
        "0x10016"
    )
    assert report["routines"][0]["absolute_memory_operands"] == ["0x0030"]
    assert report["unclassified_file_backed_ranges"] == [
        {"start": "0x00000", "end": "0x00010", "bytes": 16},
        {"start": "0x00014", "end": "0x00016", "bytes": 2},
        {"start": "0x0001a", "end": "0x00040", "bytes": 38},
    ]
    assert not report["routines"][2]["included_in_file_backed_coverage"]


def test_census_rejects_non_mz_binary(tmp_path):
    root, binary = _target(tmp_path)
    binary.write_bytes(b"not an MZ executable" + bytes(64))

    with pytest.raises(ValueError, match="MZ signature"):
        build_census(root, binary)


def test_census_rejects_relocation_table_beyond_header(tmp_path):
    root, binary = _target(tmp_path)
    malformed = bytearray(_make_mz())
    struct.pack_into("<H", malformed, 0x06, 3)
    binary.write_bytes(malformed)

    with pytest.raises(ValueError, match="relocation table"):
        build_census(root, binary)
