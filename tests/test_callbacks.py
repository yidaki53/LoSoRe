import hashlib
import json
from pathlib import Path

import pytest

from engine import callbacks, recovery


@pytest.fixture
def protocol_target(tmp_path):
    root = tmp_path / "targets" / "test"
    (root / "asm").mkdir(parents=True)
    binary_path = tmp_path / "program.exe"
    dispatcher = bytes.fromhex(
        "833e106400753526817f02b1d7752e268b7708263b770a742b"
        "1e06535226c5570c268b5f0a0703da03f2fcffd0"
        "2bf28cc25b071f268977080bc07508c3c70610646800c3"
        "505152570653e833015b075f5a5958268b7708263b770a75bcc3"
    )
    seed = bytes.fromhex("b8000133d2e878ff")
    family = bytes.fromhex("ac3c0d7404b80001c3b80d01c3ac33c0c3")
    binary = bytearray(0x110)
    binary[: len(dispatcher)] = dispatcher
    binary[0x80:0x88] = seed
    binary[0x100:] = family
    binary_path.write_bytes(binary)
    offsets = [
        0,
        5,
        7,
        13,
        15,
        19,
        23,
        25,
        26,
        27,
        28,
        29,
        33,
        37,
        38,
        40,
        42,
        43,
        45,
        47,
        49,
        50,
        51,
        52,
        56,
        58,
        60,
        61,
        67,
        68,
        69,
        70,
        71,
        72,
        73,
        74,
        77,
        78,
        79,
        80,
        81,
        82,
        83,
        87,
        91,
        93,
    ]
    (root / "asm" / "FUN_dispatch.s").write_text(
        "".join(
            f"1000:{offset:04x}  "
            + {43: "CALL AX", 74: "CALL 0x1000:0180"}.get(offset, "NOP")
            + "\n"
            for offset in offsets
        )
    )
    (root / "asm" / "FUN_seed.s").write_text(
        "1000:0080  MOV AX,0x100\n1000:0083  XOR DX,DX\n1000:0085  CALL 0x1000:0000\n"
    )
    manifest = {
        "schema_version": 1,
        "binary": {"path": "program.exe", "sha256": hashlib.sha256(binary).hexdigest()},
        "image_mapping": {"load_segment": "0x1000", "header_bytes": 0},
        "streams": [],
        "callback_protocols": [
            {
                "kind": "liero_buffered_ax_v1",
                "code_segment": "0x1000",
                "dispatcher": {
                    "function": "FUN_dispatch",
                    "address": "0x10000",
                    "bytes_hex": dispatcher.hex(),
                    "refill_target": "0x10180",
                },
                "seeds": [
                    {
                        "function": "FUN_seed",
                        "address": "0x10080",
                        "bytes_hex": seed.hex(),
                    }
                ],
                "callbacks": [{"address": "0x10100", "bytes_hex": family.hex()}],
            }
        ],
    }
    (root / "alternate_streams.json").write_text(json.dumps(manifest))
    return root


def test_callback_closure_discovers_continuation_and_zero_exit(protocol_target):
    (result,) = callbacks.load_verified_callbacks(protocol_target)

    assert result["initial_targets"] == [0x10100]
    assert result["candidate_targets"] == [0x10100, 0x1010D]
    assert result["returns_ax"] == {"0x10100": [0x100, 0x10D], "0x1010d": [0]}
    assert result["call_site"] == 0x1002B
    assert result["exported_entry_call_sites"] == [0x10085]
    assert result["refill_target"] == 0x10180
    assert result["ax_preserved_across_refill"] is True
    assert result["resolves_call_site"] is False
    assert result["remaining_obligations"]


def test_callback_report_does_not_resolve_indirect_call(protocol_target):
    recovery.initialize_ledger(protocol_target)

    result = recovery.audit_target(protocol_target)

    assert len(result["callback_protocols"]) == 1
    assert result["summary"]["unresolved_control_transfers"] >= 1
    dispatcher = next(r for r in result["routines"] if r["name"] == "FUN_dispatch")
    assert any(
        transfer["instruction"] == "CALL AX"
        for transfer in dispatcher["unresolved_control_transfers"]
    )


@pytest.mark.parametrize(
    "listing",
    [
        "1000:0090  JMP 0x1000:002b\n",
        "1000:0090  CALL 0x1000:0019\n",
        "1000:0090  JMP 0x1000:0083\n",
        "1000:0090  JMP 0x1000:0081\n",
        "1000:0090  JMP 0x1000:0001\n",
        "1000:0090  JMP 0x1000:0000\n",
        "1000:002b  CALL AX\n",
        "1000:0083  XOR DX,DX\n",
    ],
)
def test_callback_rejects_exported_initialization_bypasses(protocol_target, listing):
    (protocol_target / "asm" / "FUN_bypass.s").write_text(listing)
    with pytest.raises(ValueError, match="bypasses callback initialization"):
        callbacks.load_verified_callbacks(protocol_target)


def test_callback_allows_direct_entry_at_seed_initializer(protocol_target):
    (protocol_target / "asm" / "FUN_entry.s").write_text("1000:0090  JMP 0x1000:0080\n")
    (protocol,) = callbacks.load_verified_callbacks(protocol_target)
    assert protocol["known_entry_bypass_check"]["status"] == "passed"


@pytest.mark.parametrize("target, displacement", [("0X1002B", "89"), ("0X10083", "e1")])
def test_callback_rejects_verified_stream_bypass(protocol_target, target, displacement):
    manifest_path = protocol_target / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    binary_path = protocol_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    binary[0x90:0x92] = bytes.fromhex("7b0e")
    raw = f"eb{displacement}"
    binary[0xA0:0xA2] = bytes.fromhex(raw)
    binary_path.write_bytes(binary)
    (protocol_target / "asm" / "FUN_stream_caller.s").write_text(
        "1000:0090  JNP 0x1000:00a0\n"
    )
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    manifest["streams"] = [
        {
            "address": "0x100a0",
            "file_offset": "0xa0",
            "code_segment": "0x1000",
            "bytes_hex": raw,
            "instructions": [
                {
                    "address": "0x100a0",
                    "bytes_hex": raw,
                    "text": f"JMP {target}",
                }
            ],
            "status": "verified",
            "verified_by": "test oracle",
            "verification_methods": ["binary-bound branch decode"],
            "source_edges": [
                {
                    "address": "0x10090",
                    "file_offset": "0x90",
                    "bytes_hex": "7b0e",
                    "instruction": "JNP 0X1000:00A0",
                    "target_address": "0x100a0",
                }
            ],
        }
    ]
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match="bypasses callback initialization"):
        callbacks.load_verified_callbacks(protocol_target)


@pytest.mark.parametrize(
    ("raw", "segment", "operand"),
    [
        ("26ff5f14", "ES", "[BX+0X14]"),
        ("26ff5f18", "ES", "[BX+0X18]"),
        ("26ff19", "ES", "[BX+DI]"),
        ("ff5f14", "DS", "[BX+0X14]"),
        ("36ff5f14", "SS", "[BX+0X14]"),
    ],
)
def test_far_operand_provenance_uses_encoded_segment(
    protocol_target, raw, segment, operand
):
    path = protocol_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    binary_path = protocol_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    data = bytes.fromhex(raw)
    binary[0x90 : 0x90 + len(data)] = data
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    instruction = f"CALLF {segment}:{operand}"
    (protocol_target / "asm" / "FUN_indirect.s").write_text(
        f"1000:0090  {instruction}\n"
    )
    manifest["indirect_operands"] = [
        {
            "function": "FUN_indirect",
            "address": "0x10090",
            "bytes_hex": raw,
        }
    ]
    path.write_text(json.dumps(manifest))

    (record,) = callbacks.load_verified_indirect_operands(protocol_target)

    assert record["pointer_segment_register"] == segment
    assert record["pointer_operand"] == operand
    assert record["instruction"] == instruction
    assert record["resolves_call_site"] is False


def test_far_operand_provenance_rejects_omitted_override(protocol_target):
    path = protocol_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    binary_path = protocol_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    binary[0x90:0x94] = bytes.fromhex("26ff5f14")
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    (protocol_target / "asm" / "FUN_indirect.s").write_text(
        "1000:0090  CALLF [BX + 0x14]\n"
    )
    manifest["indirect_operands"] = [
        {
            "function": "FUN_indirect",
            "address": "0x10090",
            "bytes_hex": "26ff5f14",
        }
    ]
    path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match="indirect operand disagrees with assembly"):
        callbacks.load_verified_indirect_operands(protocol_target)


@pytest.mark.parametrize(
    ("raw", "returns"),
    [
        ("33c0c3", {0}),
        ("b83412c3", {0x1234}),
        ("7404b80100c3b80200c3", {1, 2}),
        ("ac3c0d75fbb83412c3", {0x1234}),
        ("b83412aa4e3bf3c3", {0x1234}),
        ("e00233c0b83412c3", {0x1234}),
        ("e304b80100c3b80200c3", {1, 2}),
        ("7604b80100c3b80200c3", {1, 2}),
        ("7704b80100c3b80200c3", {1, 2}),
    ],
)
def test_callback_ax_dataflow_overapproximates_branches(raw, returns):
    instructions = callbacks._decode_callbacks(bytes.fromhex(raw), 0x10000, 0x1000)
    assert callbacks._return_values(instructions, 0x10000) == returns


@pytest.mark.parametrize(
    ("raw", "error"),
    [
        ("c3", "unknown AX"),
        ("b83412acc3", "unknown AX"),
        ("b83412", "successor is not a boundary"),
        ("7401b83412c3", "successor is not a boundary"),
        ("75fc33c0c3", "successor is not a boundary"),
        ("b834", "unsupported callback encoding"),
        ("3c", "unsupported callback encoding"),
        ("74", "unsupported callback encoding"),
        ("50b83412c3", "unsupported callback encoding"),
        ("e8000033c0c3", "unsupported callback encoding"),
        ("cb", "unsupported callback encoding"),
        ("b001c3", "unsupported callback encoding"),
        ("ebfe", "unsupported callback encoding"),
    ],
)
def test_callback_ax_dataflow_rejects_unproven_effects(raw, error):
    with pytest.raises(ValueError, match=error):
        instructions = callbacks._decode_callbacks(bytes.fromhex(raw), 0x10000, 0x1000)
        callbacks._return_values(instructions, 0x10000)


@pytest.mark.parametrize(
    ("change", "error"),
    [
        ("stale-binary", "stale for binary"),
        ("wrong-callback-bytes", "callback bytes do not match"),
        ("unmodeled-callback", "unsupported callback encoding"),
        ("unknown-return", "unknown AX"),
        ("missing-continuation", "not a decoded boundary"),
        ("interior-return", "not a decoded boundary"),
        ("wrong-refill", "refill target disagrees"),
        ("clobbered-refill-restore", "unsupported callback dispatcher shape"),
        ("wrong-refill-branch", "unsupported callback dispatcher shape"),
        ("wrong-seed-call", "does not target dispatcher"),
        ("seed-ax-clobber", "unsupported AX-preserving"),
        ("seed-assembly-gap", "seed assembly path disagrees"),
        ("dispatcher-assembly-gap", "dispatcher assembly boundaries disagree"),
        ("wrong-segment", "code segment disagrees"),
        ("overlapping-regions", "callback regions overlap"),
        ("missing-seeds", "requires seed paths"),
        ("missing-regions", "requires callback regions"),
        ("wrong-kind", "unsupported callback protocol"),
        ("uncovered-caller", "do not cover exported dispatcher calls"),
        ("duplicate-seed", "seed call sites must be unique"),
        ("invalid-function", "must name an assembly export"),
        ("wrong-callback-segment", "region is outside code segment"),
        ("wrong-dispatcher-call", "dispatcher assembly calls disagree"),
        ("wrong-seed-cs", "seed assembly path disagrees"),
    ],
)
def test_callback_protocol_rejects_mutated_evidence(protocol_target, change, error):
    manifest_path = protocol_target / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    protocol = manifest["callback_protocols"][0]
    binary_path = protocol_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    if change == "stale-binary":
        binary[0] ^= 1
    elif change == "wrong-callback-bytes":
        protocol["callbacks"][0]["bytes_hex"] = "33c0c3"
    elif change in {
        "unmodeled-callback",
        "unknown-return",
        "missing-continuation",
        "interior-return",
    }:
        family = bytearray.fromhex(protocol["callbacks"][0]["bytes_hex"])
        if change == "unmodeled-callback":
            family[0] = 0x50
        elif change == "unknown-return":
            family[0] = 0xC3
        else:
            family[10] = 0x20 if change == "missing-continuation" else 0x0F
        binary[0x100 : 0x100 + len(family)] = family
        protocol["callbacks"][0]["bytes_hex"] = family.hex()
    elif change == "wrong-refill":
        protocol["dispatcher"]["refill_target"] = "0x10181"
    elif change in {"clobbered-refill-restore", "wrong-refill-branch"}:
        binary[82 if change == "clobbered-refill-restore" else 92] ^= 1
        protocol["dispatcher"]["bytes_hex"] = binary[:94].hex()
    elif change in {"wrong-seed-call", "seed-ax-clobber"}:
        binary[0x86 if change == "wrong-seed-call" else 0x84] ^= 1
        protocol["seeds"][0]["bytes_hex"] = binary[0x80:0x88].hex()
    elif change in {"seed-assembly-gap", "dispatcher-assembly-gap"}:
        filename = "FUN_seed.s" if change == "seed-assembly-gap" else "FUN_dispatch.s"
        path = protocol_target / "asm" / filename
        lines = path.read_text().splitlines()
        del lines[1]
        path.write_text("\n".join(lines))
    elif change == "wrong-segment":
        protocol["code_segment"] = "0x1001"
    elif change == "overlapping-regions":
        protocol["callbacks"] *= 2
    elif change == "missing-seeds":
        protocol["seeds"] = []
    elif change == "missing-regions":
        protocol["callbacks"] = []
    elif change == "wrong-kind":
        protocol["kind"] = "generic"
    elif change == "uncovered-caller":
        (protocol_target / "asm" / "FUN_extra.s").write_text(
            "1000:0090  CALL 0x1000:0000\n"
        )
    elif change == "duplicate-seed":
        protocol["seeds"] *= 2
    elif change == "invalid-function":
        protocol["dispatcher"]["function"] = "../FUN_dispatch"
    elif change == "wrong-callback-segment":
        protocol["callbacks"][0]["address"] = "0x20000"
        binary.extend(bytes(0x20010 - len(binary)))
        family = bytes.fromhex(protocol["callbacks"][0]["bytes_hex"])
        binary[0x10000 : 0x10000 + len(family)] = family
    elif change == "wrong-dispatcher-call":
        path = protocol_target / "asm" / "FUN_dispatch.s"
        path.write_text(path.read_text().replace("CALL AX", "CALL BX"))
    elif change == "wrong-seed-cs":
        path = protocol_target / "asm" / "FUN_seed.s"
        path.write_text(path.read_text().replace("1000:0083", "1001:0073"))
    binary_path.write_bytes(binary)
    if change != "stale-binary":
        manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match=error):
        callbacks.load_verified_callbacks(protocol_target)


def test_callback_evidence_is_optional(tmp_path):
    assert callbacks.load_verified_callbacks(tmp_path) == []
    (tmp_path / "alternate_streams.json").write_text('{"callback_protocols": []}')
    assert callbacks.load_verified_callbacks(tmp_path) == []


def test_callback_evidence_rejects_invalid_container(tmp_path):
    (tmp_path / "alternate_streams.json").write_text('{"callback_protocols": {}}')
    with pytest.raises(TypeError, match="must be an array"):
        callbacks.load_verified_callbacks(tmp_path)


def test_liero_callback_closure_when_byod_binary_is_available():
    repository = Path(__file__).resolve().parents[1]
    if not (repository / "extracted" / "liero" / "LIERO.EXE").is_file():
        pytest.skip("Liero BYOD executable is not available")

    (protocol,) = callbacks.load_verified_callbacks(repository / "targets" / "liero")

    expected = {
        "0x286de": [0, 0x390E, 0x3923],
        "0x286f3": [0],
        "0x2877b": [0, 0x39AB],
        "0x287f6": [0, 0x3A26, 0x3A37],
        "0x28807": [0, 0x3A37],
        "0x2888a": [0, 0x3ABA, 0x3ACB],
        "0x2889b": [0, 0x3ACB],
    }
    assert protocol["returns_ax"] == expected
    assert protocol["candidate_targets"] == sorted(int(entry, 16) for entry in expected)
    assert protocol["exported_entry_call_sites"] == [
        0x286CB,
        0x2876B,
        0x287D3,
        0x28863,
    ]
    assert protocol["call_site"] == 0x285E7
    assert protocol["refill_target"] == 0x2873C
    assert protocol["ax_preserved_across_refill"] is True
    assert protocol["resolves_call_site"] is False
    assert protocol["known_entry_bypass_check"] == {
        "status": "passed",
        "assembly_exports_checked": 295,
        "verified_streams_checked": 12,
        "scope": "known instruction entries and recorded transfers only",
    }

    operands = callbacks.load_verified_indirect_operands(
        repository / "targets" / "liero"
    )
    assert [(entry["address"], entry["pointer_operand"]) for entry in operands] == [
        (0x28521, "[BX+DI]"),
        (0x2873E, "[BX+0X14]"),
        (0x2874C, "[BX+0X18]"),
    ]
    assert all(entry["pointer_segment_register"] == "ES" for entry in operands)
    assert all(entry["resolves_call_site"] is False for entry in operands)
