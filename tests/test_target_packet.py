import json
import struct

import pytest

from engine import target_packet


def _make_mz(image_size=64):
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
        2,
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
    data[header_size + 0x08:header_size + 0x0A] = bytes.fromhex("eb07")
    data[header_size + 0x16:header_size + 0x1B] = bytes.fromhex("33c08bd8c3")
    return bytes(data)


def _target(tmp_path):
    root = tmp_path
    target_root = root / "targets" / "demo"
    (target_root / "asm").mkdir(parents=True)
    (target_root / "config").mkdir()
    (target_root / "decomp").mkdir()
    functions = [
        {"name": "entry", "entry": "1000:0010", "size": 4, "num_instructions": 3},
        {"name": "FUN_1000_0008", "entry": "1000:0008", "size": 2, "num_instructions": 1},
        {"name": "FUN_1000_0016", "entry": "1000:0016", "size": 5, "num_instructions": 3},
    ]
    (target_root / "functions.json").write_text(json.dumps({
        "program": "DEMO.EXE", "num_functions": 3, "functions": functions,
    }))
    (target_root / "asm" / "entry.s").write_text(
        "; entry entry=1000:0010 size=4\n"
        "1000:0010  MOV AX,[0x0030]\n"
        "1000:0012  CALLF 0x1000:0016\n"
        "1000:0015  RET\n"
    )
    (target_root / "asm" / "FUN_1000_0008.s").write_text(
        "; FUN_1000_0008 entry=1000:0008 size=2\n"
        "1000:0008  JMP 0x1000:0010\n"
    )
    (target_root / "asm" / "FUN_1000_0016.s").write_text(
        "; FUN_1000_0016 entry=1000:0016 size=4\n"
        "1000:0016  XOR AX,AX\n"
        "1000:0018  MOV BX,AX\n"
        "1000:001a  RET\n"
    )
    (target_root / "decomp" / "FUN_1000_0016.c").write_text(
        "void FUN_1000_0016(void) { return; }\n"
    )
    (target_root / "config" / "routine_contracts.json").write_text(json.dumps({
        "schema_version": 1,
        "functions": {
            "FUN_1000_0016": {
                "declaration": "function FUN_1000_0016: Longint;",
                "prompt": "Infer the routine from binary evidence.",
                "oracle": "routine-trace-parity",
            }
        },
    }))
    (target_root / "recovery.json").write_text(json.dumps({"functions": {
        "entry": {"status": "unreviewed"},
        "FUN_1000_0008": {"status": "unreviewed"},
        "FUN_1000_0016": {"status": "unreviewed"},
    }}))
    binary = root / "extracted" / "demo" / "DEMO.EXE"
    binary.parent.mkdir(parents=True)
    binary.write_bytes(_make_mz())
    return root


def test_target_packet_is_binary_derived_and_contains_no_source_examples(tmp_path):
    root = _target(tmp_path)
    result = target_packet.build_packet(
        root, "demo", "FUN_1000_0016", tmp_path / "packet"
    )

    assert result["status"] == "packet-ready"
    assert result["source_policy"] == {
        "binary_derived_evidence_only": True,
        "source_examples_in_prompt": False,
        "candidate_source_in_prompt": False,
        "decompiler_output_in_prompt": False,
        "online_agent_seed": None,
    }
    assert result["evidence_gate"] == {"passed": True, "reasons": []}
    packet = json.loads((tmp_path / "packet" / "packet.json").read_text())
    assert packet["bytes"]["hex"] == "33c08bd8c3"
    assert packet["oracle_contract"]["declaration"] == (
        "function FUN_1000_0016: Longint;"
    )
    assert packet["binary"]["sha256"] == result["binary_sha256"]
    assert packet["static_evidence"]["raw_byte_facts"]["registers"]["ax"]["kind"] == "constant"
    prompt = (tmp_path / "packet" / "prompt.txt").read_text()
    assert "33c08bd8c3" in prompt
    assert "XOR AX,AX" in prompt
    assert '"kind": "constant"' in prompt
    assert "Allowed answers" not in prompt
    assert "void FUN_1000_0016" not in prompt
    assert "function FUN_1000_0016" not in prompt
    assert "Previously oracle-verified" not in prompt
    assert "PASCAL:" not in prompt


def test_frontier_packet_selects_unblocked_leaf(tmp_path):
    root = _target(tmp_path)
    result = target_packet.build_frontier_packet(
        root, "demo", tmp_path / "frontier-packet"
    )

    assert result["status"] == "packet-ready"
    assert result["routine"] == "FUN_1000_0016"
    assert result["frontier"][0] == "FUN_1000_0008"
    assert result["skipped"][0]["routine"] == "FUN_1000_0008"


def test_target_packet_blocks_tail_jump_without_prompt(tmp_path):
    root = _target(tmp_path)
    result = target_packet.build_packet(
        root, "demo", "FUN_1000_0008", tmp_path / "blocked-packet"
    )

    assert result["status"] == "blocked-static-evidence"
    assert result["evidence_gate"]["passed"] is False
    assert not (tmp_path / "blocked-packet" / "prompt.txt").exists()


def test_target_packet_rejects_missing_binary(tmp_path):
    root = _target(tmp_path)
    (root / "extracted" / "demo" / "DEMO.EXE").unlink()
    with pytest.raises(FileNotFoundError, match="no read-only binary"):
        target_packet.build_packet(root, "demo", "FUN_1000_0016", tmp_path / "missing")
