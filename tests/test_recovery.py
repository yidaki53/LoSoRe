import hashlib
import json

import pytest

from engine import recovery


def _target(tmp_path):
    root = tmp_path / "targets" / "liero"
    (root / "asm").mkdir(parents=True)
    (root / "decomp").mkdir()
    (root / "src").mkdir()
    (root / "functions.json").write_text(
        json.dumps(
            {
                "num_functions": 2,
                "functions": [{"name": "FUN_1"}, {"name": "FUN_2"}],
            }
        )
    )
    (root / "asm" / "FUN_1.s").write_text(
        "0000:0000  MOV AX,0x1\n"
        "0000:0003  JZ 0x0000:0008\n"
        "0000:0005  CALL 0x0000:0008\n"
        "0000:0008  RET\n"
    )
    (root / "asm" / "FUN_2.s").write_text("; no decoded instructions\n")
    (root / "decomp" / "FUN_1.c").write_text("void FUN_1(void) { return; }\n")
    (root / "src" / "FUN_1.inc").write_text(
        "procedure FUN_1;\nbegin\n  Inc(Value);\nend;\n"
    )
    return root


def test_scoped_audit_counts_routines_and_reports_without_promotion(
    tmp_path, monkeypatch
):
    """Oracle: multi-routine reports count once; scoped passes do not attest source."""
    root = _target(tmp_path)
    recovery.initialize_ledger(root)
    checks = [
        {"function": name, "reference": "invalid/result.json", "status": "invalid"}
        for name in ("FUN_1", "FUN_2")
    ] + [
        {"function": "FUN_1", "reference": reference, "status": "passed"}
        for reference in ("training/result.json", "heldout/result.json")
    ]
    monkeypatch.setattr(recovery, "load_scoped_checks", lambda _target: checks)

    summary = recovery.audit_target(root)["summary"]

    assert summary["scoped_differential_reports_invalid"] == 1
    assert summary["scoped_differential_routines_passed"] == 1
    assert summary["source_recovered"] == 0
    assert summary["original_binary_verified"] == 0


def _mark_recovered(root, function_name):
    recovery.initialize_ledger(root)
    evidence = {
        field: [f"{function_name} evidence at 0000:0000"]
        for field in recovery.EVIDENCE_FIELDS
    }
    recovery.attest_source(
        root,
        function_name,
        "reviewer",
        "Body checked against the listed assembly evidence.",
        evidence,
    )
    ledger_path = root / "recovery.json"
    return ledger_path


def _write_alternate_stream_evidence(root, binary):
    root.parent.parent.joinpath("extracted", "liero").mkdir(parents=True)
    binary_path = root.parent.parent / "extracted" / "liero" / "LIERO.EXE"
    binary_path.write_bytes(binary)
    (root / "alternate_streams.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "binary": {
                    "path": "extracted/liero/LIERO.EXE",
                    "sha256": hashlib.sha256(binary).hexdigest(),
                },
                "image_mapping": {
                    "load_segment": "0x1000",
                    "header_bytes": 0,
                },
                "streams": [
                    {
                        "address": "0x10010",
                        "file_offset": "0x10",
                        "bytes_hex": "90cb",
                        "instructions": [
                            {
                                "address": "0x10010",
                                "bytes_hex": "90",
                                "text": "NOP",
                            },
                            {
                                "address": "0x10011",
                                "bytes_hex": "cb",
                                "text": "RETF",
                            },
                        ],
                        "status": "verified",
                        "verified_by": "static review",
                        "verification_methods": ["raw bytes and independent decode"],
                        "source_edges": [
                            {
                                "address": "0x10000",
                                "file_offset": "0x0",
                                "bytes_hex": "7b0e",
                                "instruction": "JNP 0x1000:0010",
                                "target_address": "0x10010",
                            }
                        ],
                    }
                ],
            }
        )
    )
    return binary_path


def _write_indirect_stream_evidence(root, target_offset="0x0010"):
    (root / "asm" / "FUN_1.s").write_text("1000:0000  CALLF [0x0020]\n")
    (root / "asm" / "FUN_2.s").write_text(
        "1000:0004  MOV word ptr [0x0020],0x10\n"
        "1000:000a  MOV word ptr [0x0022],CS\n"
        "1000:0010  XOR AX,AX\n"
        "1000:0012  RETF 0x2\n"
    )
    binary = bytearray(0x15)
    binary[0:4] = bytes.fromhex("ff1e2000")
    binary[4:10] = bytes.fromhex("c70620001000")
    binary[10:14] = bytes.fromhex("8c0e2200")
    binary[0x10:0x15] = bytes.fromhex("33c0ca0200")
    _write_alternate_stream_evidence(root, binary)
    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["streams"] = [
        {
            "address": "0x10010",
            "file_offset": "0x10",
            "code_segment": "0x1000",
            "bytes_hex": "33c0ca0200",
            "instructions": [
                {"address": "0x10010", "bytes_hex": "33c0", "text": "XOR AX,AX"},
                {"address": "0x10012", "bytes_hex": "ca0200", "text": "RETF 0X2"},
            ],
            "status": "verified",
            "verified_by": "static review",
            "verification_methods": [
                "Raw executable bytes independently disassembled",
                "Pointer initializer and all references checked against assembly",
            ],
            "source_edges": [
                {
                    "address": "0x10000",
                    "file_offset": "0x0",
                    "bytes_hex": "ff1e2000",
                    "instruction": "CALLF [0X0020]",
                    "target_address": "0x10010",
                    "transfer_kind": "far_indirect",
                }
            ],
            "indirect_pointer": {
                "storage_offset": "0x0020",
                "target_offset": target_offset,
                "target_segment": "0x1000",
                "initializers": [
                    {
                        "part": "offset",
                        "address": "0x10004",
                        "file_offset": "0x4",
                        "bytes_hex": "c70620001000",
                        "instruction": "MOV WORD PTR [0X0020],0X10",
                    },
                    {
                        "part": "segment",
                        "address": "0x1000a",
                        "file_offset": "0xa",
                        "bytes_hex": "8c0e2200",
                        "instruction": "MOV WORD PTR [0X0022],CS",
                    },
                ],
            },
        }
    ]
    manifest_path.write_text(json.dumps(manifest))
    return manifest_path


def test_initialize_and_audit_keep_compile_separate_from_recovery(tmp_path):
    root = _target(tmp_path)
    path = recovery.initialize_ledger(root)

    assert path.is_file()
    result = recovery.audit_target(root)

    assert result["summary"]["function_count"] == 2
    assert result["summary"]["assembly_instruction_count"] == 4
    assert result["summary"]["routines_with_pascal_bodies"] == 1
    assert result["summary"]["source_recovered"] == 0
    assert result["summary"]["source_recovery_percent"] == 0
    assert result["summary"]["external_effects_unclassified"] == 2
    assert result["routines"][0]["cfg"]["blocks"] == 3
    assert result["routines"][0]["cfg"]["call"] == 1
    assert result["routines"][0]["verification"]["host_test_status"] == "not_run"


def test_source_recovered_requires_evidence_review_and_content_hashes(tmp_path):
    root = _target(tmp_path)
    ledger_path = _mark_recovered(root, "FUN_1")

    result = recovery.audit_target(root)

    assert result["summary"]["source_recovered"] == 1
    assert result["summary"]["source_recovery_percent"] == 50

    source = root / "src" / "FUN_1.inc"
    source.write_text(source.read_text() + "{ changed after review }\n")
    result = recovery.audit_target(root)
    assert result["summary"]["source_recovered"] == 0
    assert result["routines"][0]["stale_reason"] == (
        "Pascal source changed since review"
    )
    assert ledger_path.is_file()


def test_source_recovery_rejects_unresolved_direct_transfer(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("0000:0000  JMP 0x2000:53bb\n")
    recovery.initialize_ledger(root)
    routine = recovery.audit_target(root)["routines"][0]

    assert routine["unresolved_control_transfers"] == [
        {
            "address": "0x00000",
            "instruction": "JMP 0X2000:53BB",
            "target": "0x053bb",
            "reason": "target is not a decoded instruction",
        }
    ]

    with pytest.raises(ValueError, match="unresolved control-flow transfer"):
        _mark_recovered(root, "FUN_1")


def test_audit_invalidates_recovered_source_with_new_unresolved_edge(tmp_path):
    root = _target(tmp_path)
    _mark_recovered(root, "FUN_1")
    asm_path = root / "asm" / "FUN_1.s"
    asm_path.write_text("0000:0000  JMP 0x2000:53bb\n")
    ledger_path = root / "recovery.json"
    ledger = json.loads(ledger_path.read_text())
    ledger["functions"]["FUN_1"]["assembly_sha256"] = hashlib.sha256(
        asm_path.read_bytes()
    ).hexdigest()
    ledger_path.write_text(json.dumps(ledger))

    result = recovery.audit_target(root)

    assert result["summary"]["source_recovered"] == 0
    assert result["summary"]["stale_source_recoveries"] == 0
    assert result["summary"]["source_recoveries_with_unresolved_control_flow"] == 1
    assert result["routines"][0]["stale_reason"].startswith(
        "unresolved control-flow transfer"
    )


def test_source_recovery_accepts_far_target_at_known_instruction_alias(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text(
        "24dd:0582  MOV AX,0x0576\n24dd:0585  JMP 0x2000:53bb\n"
    )
    (root / "asm" / "FUN_2.s").write_text("24dd:05eb  MOV CX,CS\n")

    _mark_recovered(root, "FUN_1")

    assert recovery.audit_target(root)["summary"]["source_recovered"] == 1


def test_source_recovery_accepts_near_target_after_segment_wrap(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1ec2:14cd  CALL 0X2000:FF06\n")
    (root / "asm" / "FUN_2.s").write_text("1ec2:12e6  RETF 0XC\n")

    _mark_recovered(root, "FUN_1")

    result = recovery.audit_target(root)
    assert result["summary"]["source_recovered"] == 1
    assert result["routines"][0]["unresolved_control_transfers"] == []


def test_audit_accepts_binary_bound_verified_alternate_entry(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1000:0000  JNP 0x1000:0010\n")
    binary = bytearray(0x12)
    binary[0:2] = bytes.fromhex("7b0e")
    binary[0x10:0x12] = bytes.fromhex("90cb")
    _write_alternate_stream_evidence(root, binary)
    recovery.initialize_ledger(root)

    audit = recovery.audit_target(root)
    routine = audit["routines"][0]

    assert routine["unresolved_control_transfers"] == []
    assert audit["alternate_streams"][0]["address"] == 0x10010
    assert audit["summary"]["unresolved_control_transfers"] == 0
    assert audit["summary"]["verified_alternate_streams"] == 1


def test_audit_resolves_binary_bound_static_far_indirect_calls(tmp_path):
    root = _target(tmp_path)
    _write_indirect_stream_evidence(root)
    recovery.initialize_ledger(root)

    audit = recovery.audit_target(root)

    assert audit["routines"][0]["unresolved_control_transfers"] == []
    assert audit["summary"]["unresolved_control_transfers"] == 0
    assert audit["alternate_streams"][0]["address"] == 0x10010


def test_audit_rejects_indirect_pointer_that_does_not_target_stream(tmp_path):
    root = _target(tmp_path)
    _write_indirect_stream_evidence(root, target_offset="0x0011")
    recovery.initialize_ledger(root)

    with pytest.raises(ValueError, match="does not target its entry"):
        recovery.audit_target(root)


def _write_register_stream_evidence(root):
    (root / "asm" / "FUN_1.s").write_text(
        "1000:0000  MOV BX,0x12\n"
        "1000:0003  JMP 0x1000:0008\n"
        "1000:0008  MOV AX,[0x20]\n"
        "1000:000b  CALL BX\n"
        "1000:000d  RETF\n"
    )
    (root / "asm" / "FUN_2.s").write_text("; no decoded instructions\n")
    binary = bytearray(0x15)
    binary[:5] = bytes.fromhex("bb1200eb03")
    binary[8:14] = bytes.fromhex("a12000ffd3cb")
    binary[0x10:] = bytes.fromhex("90908cdbc3")
    _write_alternate_stream_evidence(root, binary)
    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    stream = manifest["streams"][0]
    stream.update(
        code_segment="0x1000",
        bytes_hex="90908cdbc3",
        instructions=[
            {"address": "0x10010", "bytes_hex": "90", "text": "NOP"},
            {"address": "0x10011", "bytes_hex": "90", "text": "NOP"},
            {"address": "0x10012", "bytes_hex": "8cdb", "text": "MOV BX,DS"},
            {"address": "0x10014", "bytes_hex": "c3", "text": "RET"},
        ],
        source_edges=[
            {
                "address": "0x1000b",
                "file_offset": "0xb",
                "bytes_hex": "ffd3",
                "instruction": "CALL BX",
                "target_address": "0x10012",
                "transfer_kind": "near_register",
                "register_path": {
                    "function": "FUN_1",
                    "instructions": [
                        {"address": "0x10000", "bytes_hex": "bb1200"},
                        {"address": "0x10003", "bytes_hex": "eb03"},
                        {"address": "0x10008", "bytes_hex": "a12000"},
                    ],
                },
            }
        ],
    )
    manifest_path.write_text(json.dumps(manifest))
    recovery.initialize_ledger(root)
    return manifest_path


def test_audit_resolves_register_call_to_interior_stream_boundary(tmp_path):
    root = _target(tmp_path)
    _write_register_stream_evidence(root)

    audit = recovery.audit_target(root)

    assert audit["routines"][0]["unresolved_control_transfers"] == []
    assert audit["alternate_streams"][0]["source_edges"][0]["target_address"] == (
        "0x10012"
    )


@pytest.mark.parametrize(
    "write_evidence",
    [_write_indirect_stream_evidence, _write_register_stream_evidence],
)
def test_source_attestation_accepts_validated_indirect_call(tmp_path, write_evidence):
    root = _target(tmp_path)
    write_evidence(root)

    _mark_recovered(root, "FUN_1")

    assert recovery.audit_target(root)["summary"]["source_recovered"] == 1


@pytest.mark.parametrize(
    ("change", "error"),
    [
        ("wrong-target", "register target"),
        ("missing-step", "complete function prefix"),
        ("clobber", "unsupported register-path instruction"),
        ("wrong-bytes", "register-path bytes"),
        ("wrong-jump", "register-path successor"),
        ("bypass-entry", "bypasses register initialization"),
        ("shared-export", "bypasses register initialization"),
        ("alternate-bypass", "bypasses register initialization"),
        ("wrong-cs", "register-call code segment"),
        ("non-boundary", "decoded instruction boundary"),
        ("wrong-opcode", "register-call encoding"),
        ("ax-callback", "register-call encoding"),
        ("no-path", "register_path must be an object"),
    ],
)
def test_audit_rejects_incomplete_register_call_proof(tmp_path, change, error):
    root = _target(tmp_path)
    manifest_path = _write_register_stream_evidence(root)
    manifest = json.loads(manifest_path.read_text())
    stream = manifest["streams"][0]
    edge = stream["source_edges"][0]
    path = edge["register_path"]["instructions"]
    binary_path = root.parent.parent / "extracted" / "liero" / "LIERO.EXE"
    binary = bytearray(binary_path.read_bytes())
    if change == "wrong-target":
        edge["target_address"] = "0x10010"
    elif change == "missing-step":
        del path[1]
    elif change == "clobber":
        binary[8:11] = bytes.fromhex("bb1100")
        path[2]["bytes_hex"] = "bb1100"
        assembly_path = root / "asm" / "FUN_1.s"
        assembly_path.write_text(
            assembly_path.read_text().replace("MOV AX,[0x20]", "MOV BX,0x11")
        )
    elif change == "wrong-bytes":
        path[0]["bytes_hex"] = "bb1300"
    elif change == "wrong-jump":
        binary[4] = 4
        path[1]["bytes_hex"] = "eb04"
    elif change == "bypass-entry":
        (root / "asm" / "FUN_2.s").write_text("1000:0020  JMP 0x1000:0008\n")
    elif change == "shared-export":
        (root / "asm" / "FUN_2.s").write_text(
            "1000:0007  NOP\n1000:0008  MOV AX,[0x20]\n1000:000b  CALL BX\n"
        )
    elif change == "alternate-bypass":
        stream["bytes_hex"] = "ebf68cdbc3"
        binary[0x10:0x12] = bytes.fromhex("ebf6")
        stream["instructions"][:2] = [
            {
                "address": "0x10010",
                "bytes_hex": "ebf6",
                "text": "JMP 0X1000:0008",
            }
        ]
    elif change == "wrong-cs":
        stream["code_segment"] = "0x1001"
    elif change == "non-boundary":
        edge["target_address"] = "0x10013"
    elif change == "wrong-opcode":
        binary[0xB:0xD] = bytes.fromhex("ffd0")
        edge["bytes_hex"] = "ffd0"
    elif change == "ax-callback":
        binary[0xB:0xD] = bytes.fromhex("ffd0")
        edge["bytes_hex"] = "ffd0"
        edge["instruction"] = "CALL AX"
        assembly_path = root / "asm" / "FUN_1.s"
        assembly_path.write_text(
            assembly_path.read_text().replace("CALL BX", "CALL AX")
        )
    elif change == "no-path":
        del edge["register_path"]
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    manifest_path.write_text(json.dumps(manifest))

    exception = TypeError if change == "no-path" else ValueError
    with pytest.raises(exception, match=error):
        recovery.audit_target(root)


def test_audit_accepts_branch_to_another_verified_alternate_stream(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text(
        "1000:0000  JNP 0x1000:0010\n1000:0002  JNP 0x1000:0012\n"
    )
    binary = bytearray(0x14)
    binary[0:2] = bytes.fromhex("7b0e")
    binary[2:4] = bytes.fromhex("7b0e")
    binary[0x10:0x12] = bytes.fromhex("eb00")
    binary[0x12:0x14] = bytes.fromhex("90cb")
    _write_alternate_stream_evidence(root, binary)

    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["streams"][0].update(
        {
            "bytes_hex": "eb00",
            "code_segment": "0x1000",
            "instructions": [
                {
                    "address": "0x10010",
                    "bytes_hex": "eb00",
                    "text": "JMP 0X1000:0012",
                }
            ],
        }
    )
    manifest["streams"].append(
        {
            "address": "0x10012",
            "file_offset": "0x12",
            "bytes_hex": "90cb",
            "instructions": [
                {
                    "address": "0x10012",
                    "bytes_hex": "90",
                    "text": "NOP",
                },
                {
                    "address": "0x10013",
                    "bytes_hex": "cb",
                    "text": "RETF",
                },
            ],
            "status": "verified",
            "verified_by": "static review",
            "verification_methods": ["raw bytes and independent decode"],
            "source_edges": [
                {
                    "address": "0x10002",
                    "file_offset": "0x2",
                    "bytes_hex": "7b0e",
                    "instruction": "JNP 0X1000:0012",
                    "target_address": "0x10012",
                }
            ],
        }
    )
    manifest_path.write_text(json.dumps(manifest))
    recovery.initialize_ledger(root)

    audit = recovery.audit_target(root)

    assert audit["summary"]["verified_alternate_streams"] == 2
    assert audit["summary"]["unresolved_control_transfers"] == 0
    assert audit["routines"][0]["unresolved_control_transfers"] == []


def test_audit_accepts_near_call_source_edge_to_verified_alternate_entry(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1e7d:01af  CALL 0x1000:e7d0\n")
    binary = bytearray(0xE982)
    binary[0xE97F:0xE982] = bytes.fromhex("e84efe")
    binary[0xE7D0:0xE7D2] = bytes.fromhex("90cb")
    _write_alternate_stream_evidence(root, binary)
    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["streams"][0].update(
        {
            "address": "0x1e7d0",
            "file_offset": "0xe7d0",
            "instructions": [
                {
                    "address": "0x1e7d0",
                    "bytes_hex": "90",
                    "text": "NOP",
                },
                {
                    "address": "0x1e7d1",
                    "bytes_hex": "cb",
                    "text": "RETF",
                },
            ],
        }
    )
    manifest["streams"][0]["source_edges"][0].update(
        {
            "address": "0x1e97f",
            "file_offset": "0xe97f",
            "bytes_hex": "e84efe",
            "instruction": "CALL 0X1000:E7D0",
            "target_address": "0x1e7d0",
        }
    )
    manifest_path.write_text(json.dumps(manifest))
    recovery.initialize_ledger(root)

    audit = recovery.audit_target(root)

    assert audit["summary"]["verified_alternate_streams"] == 1
    assert audit["routines"][0]["unresolved_control_transfers"] == []


def test_audit_accepts_loop_source_edge_to_verified_alternate_entry(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1000:0000  LOOP 0x1000:0010\n")
    binary = bytearray(0x12)
    binary[0:2] = bytes.fromhex("e20e")
    binary[0x10:0x12] = bytes.fromhex("90cb")
    _write_alternate_stream_evidence(root, binary)
    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["streams"][0]["source_edges"][0].update(
        {
            "address": "0x10000",
            "file_offset": "0x0",
            "bytes_hex": "e20e",
            "instruction": "LOOP 0X1000:0010",
            "target_address": "0x10010",
        }
    )
    manifest_path.write_text(json.dumps(manifest))
    recovery.initialize_ledger(root)

    audit = recovery.audit_target(root)

    assert audit["summary"]["verified_alternate_streams"] == 1
    assert audit["routines"][0]["unresolved_control_transfers"] == []


def test_audit_validates_relocated_far_call_from_alternate_stream(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1000:0000  CALL 0X1000:0010\n")
    (root / "asm" / "FUN_2.s").write_text("1001:0020  RETF\n")

    binary = bytearray(0x54)
    binary[0:2] = b"MZ"
    binary[0x06:0x08] = (1).to_bytes(2, "little")
    binary[0x08:0x0A] = (2).to_bytes(2, "little")
    binary[0x18:0x1A] = (0x1C).to_bytes(2, "little")
    binary[0x1C:0x20] = bytes.fromhex("13000000")
    binary[0x20:0x23] = bytes.fromhex("e80d00")
    binary[0x30:0x36] = bytes.fromhex("9a20000100c3")
    binary[0x50] = 0xCB
    _write_alternate_stream_evidence(root, binary)

    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["image_mapping"]["header_bytes"] = 0x20
    manifest["streams"][0].update(
        {
            "address": "0x10010",
            "file_offset": "0x30",
            "bytes_hex": "9a20000100c3",
            "instructions": [
                {
                    "address": "0x10010",
                    "bytes_hex": "9a20000100",
                    "text": "CALLF 0X0001:0X0020",
                },
                {
                    "address": "0x10015",
                    "bytes_hex": "c3",
                    "text": "RETF",
                },
            ],
            "source_edges": [
                {
                    "address": "0x10000",
                    "file_offset": "0x20",
                    "bytes_hex": "e80d00",
                    "instruction": "CALL 0X1000:0010",
                    "target_address": "0x10010",
                }
            ],
            "outgoing_calls": [
                {
                    "address": "0x10010",
                    "file_offset": "0x30",
                    "bytes_hex": "9a20000100",
                    "relocation_file_offset": "0x33",
                    "target_address": "0x10030",
                }
            ],
        }
    )
    manifest_path.write_text(json.dumps(manifest))
    recovery.initialize_ledger(root)

    audit = recovery.audit_target(root)

    assert audit["summary"]["verified_alternate_streams"] == 1
    assert (
        audit["alternate_streams"][0]["outgoing_calls"][0]["target_address"] == 0x10030
    )
    manifest["streams"][0]["outgoing_calls"][0]["relocation_file_offset"] = "0x34"
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="lacks its MZ relocation"):
        recovery.audit_target(root)


def test_audit_rejects_alternate_stream_branch_with_wrong_target(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1000:0000  JNP 0x1000:0010\n")
    binary = bytearray(0x13)
    binary[0:2] = bytes.fromhex("7b0e")
    binary[0x10:0x13] = bytes.fromhex("eb00cb")
    _write_alternate_stream_evidence(root, binary)
    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["streams"][0].update(
        {
            "bytes_hex": "eb00cb",
            "code_segment": "0x1000",
            "instructions": [
                {
                    "address": "0x10010",
                    "bytes_hex": "eb00",
                    "text": "JMP 0X10011",
                },
                {
                    "address": "0x10012",
                    "bytes_hex": "cb",
                    "text": "RETF",
                },
            ],
        }
    )
    manifest_path.write_text(json.dumps(manifest))
    recovery.initialize_ledger(root)

    with pytest.raises(ValueError, match="branch target disagrees"):
        recovery.audit_target(root)


def test_audit_accepts_prefixed_loop_to_overlapping_entry(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1000:0000  JNP 0x1000:0010\n")
    binary = bytearray(0x17)
    binary[0:2] = bytes.fromhex("7b0e")
    binary[0x10:0x17] = bytes.fromhex("2ee201b8cb00cb")
    _write_alternate_stream_evidence(root, binary)
    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["streams"][0].update(
        {
            "bytes_hex": "2ee201b8cb00cb",
            "code_segment": "0x1000",
            "instructions": [
                {
                    "address": "0x10010",
                    "bytes_hex": "2ee201",
                    "text": "CS LOOP 0X10014",
                },
                {
                    "address": "0x10013",
                    "bytes_hex": "b8cb00",
                    "text": "MOV AX,0XCB",
                },
                {
                    "address": "0x10016",
                    "bytes_hex": "cb",
                    "text": "RETF",
                },
            ],
            "overlapping_entries": [
                {
                    "address": "0x10014",
                    "bytes_hex": "cb",
                    "instructions": [
                        {
                            "address": "0x10014",
                            "bytes_hex": "cb",
                            "text": "RETF",
                        }
                    ],
                }
            ],
        }
    )
    manifest_path.write_text(json.dumps(manifest))
    recovery.initialize_ledger(root)

    audit = recovery.audit_target(root)

    assert audit["summary"]["verified_alternate_streams"] == 1
    assert audit["alternate_streams"][0]["instruction_addresses"] == [
        0x10010,
        0x10013,
        0x10016,
        0x10014,
    ]

    manifest["streams"][0]["instructions"][0]["text"] = "CS LOOPE 0X10014"
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="branch opcode disagrees"):
        recovery.audit_target(root)

    manifest["streams"][0]["instructions"][0]["text"] = "CS LOOP 0X10015"
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="branch target disagrees"):
        recovery.audit_target(root)


def test_audit_does_not_accept_pending_alternate_stream(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1000:0000  JNP 0x1000:0010\n")
    binary = bytearray(0x12)
    binary[0:2] = bytes.fromhex("7b0e")
    binary[0x10:0x12] = bytes.fromhex("90cb")
    _write_alternate_stream_evidence(root, binary)
    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["streams"][0]["status"] = "pending_review"
    manifest_path.write_text(json.dumps(manifest))
    recovery.initialize_ledger(root)

    audit = recovery.audit_target(root)

    assert audit["alternate_streams"] == []
    assert len(audit["routines"][0]["unresolved_control_transfers"]) == 1


def test_audit_rejects_alternate_stream_evidence_for_changed_binary(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1000:0000  JNP 0x1000:0010\n")
    binary = bytearray(0x12)
    binary[0:2] = bytes.fromhex("7b0e")
    binary[0x10:0x12] = bytes.fromhex("90cb")
    binary_path = _write_alternate_stream_evidence(root, binary)
    binary_path.write_bytes(binary + b"\x00")
    recovery.initialize_ledger(root)

    with pytest.raises(ValueError, match="evidence is stale"):
        recovery.audit_target(root)


def test_audit_rejects_alternate_stream_instruction_boundary_mismatch(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1000:0000  JNP 0x1000:0010\n")
    binary = bytearray(0x12)
    binary[0:2] = bytes.fromhex("7b0e")
    binary[0x10:0x12] = bytes.fromhex("90cb")
    _write_alternate_stream_evidence(root, binary)
    manifest_path = root / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["streams"][0]["instructions"][1]["address"] = "0x10012"
    manifest_path.write_text(json.dumps(manifest))
    recovery.initialize_ledger(root)

    with pytest.raises(ValueError, match="boundaries are not contiguous"):
        recovery.audit_target(root)


def test_audit_rejects_alternate_stream_source_edge_not_in_assembly(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("1000:0000  JNZ 0x1000:0010\n")
    binary = bytearray(0x12)
    binary[0:2] = bytes.fromhex("7b0e")
    binary[0x10:0x12] = bytes.fromhex("90cb")
    _write_alternate_stream_evidence(root, binary)
    recovery.initialize_ledger(root)

    with pytest.raises(ValueError, match="does not match the assembly inventory"):
        recovery.audit_target(root)


def test_source_recovery_rejects_indirect_control_transfer(tmp_path):
    root = _target(tmp_path)
    (root / "asm" / "FUN_1.s").write_text("0000:0000  CALL AX\n")

    with pytest.raises(ValueError, match="unresolved control-flow transfer"):
        _mark_recovered(root, "FUN_1")


def test_source_recovery_attestation_rejects_placeholder_body(tmp_path):
    root = _target(tmp_path)
    (root / "src" / "FUN_1.inc").write_text(
        "procedure FUN_1;\nbegin\n  { TODO: translate from asm }\nend;\n"
    )
    with pytest.raises(ValueError, match="non-placeholder Pascal body"):
        _mark_recovered(root, "FUN_1")


def test_source_recovery_attestation_requires_matching_pascal_declaration(tmp_path):
    root = _target(tmp_path)
    (root / "src" / "FUN_1.inc").write_text(
        "procedure FUN_OTHER;\nbegin\n  Inc(Value);\nend;\n"
    )

    with pytest.raises(ValueError, match="declaration .* does not match"):
        _mark_recovered(root, "FUN_1")


def test_unrecoverable_requires_review_and_reason(tmp_path):
    root = _target(tmp_path)
    ledger_path = recovery.initialize_ledger(root)
    ledger = json.loads(ledger_path.read_text())
    ledger["functions"]["FUN_2"]["status"] = "unrecoverable"
    ledger_path.write_text(json.dumps(ledger))

    with pytest.raises(ValueError, match="requires reviewer and reason"):
        recovery.audit_target(root)


def test_ledger_sync_preserves_reviews_and_keeps_stale_entries(tmp_path):
    root = _target(tmp_path)
    ledger_path = _mark_recovered(root, "FUN_1")
    ledger = json.loads(ledger_path.read_text())
    ledger["functions"]["FUN_REMOVED"] = ledger["functions"]["FUN_1"]
    ledger_path.write_text(json.dumps(ledger))
    (root / "asm" / "FUN_3.s").write_text("0000:0010  RET\n")

    recovery.initialize_ledger(root)
    updated = json.loads(ledger_path.read_text())
    result = recovery.audit_target(root)

    assert updated["functions"]["FUN_1"]["status"] == "source_recovered"
    assert updated["functions"]["FUN_3"]["status"] == "unreviewed"
    assert "FUN_REMOVED" in result["summary"]["stale_ledger_entries"]


def test_source_file_cannot_escape_target_directory(tmp_path):
    root = _target(tmp_path)
    ledger_path = _mark_recovered(root, "FUN_1")
    ledger = json.loads(ledger_path.read_text())
    ledger["functions"]["FUN_1"]["source_file"] = "../outside.pas"
    ledger_path.write_text(json.dumps(ledger))

    with pytest.raises(ValueError, match="target-relative path"):
        recovery.audit_target(root)


def test_attestation_requires_all_evidence_categories(tmp_path):
    root = _target(tmp_path)
    recovery.initialize_ledger(root)

    with pytest.raises(ValueError, match="evidence categories must match"):
        recovery.attest_source(
            root,
            "FUN_1",
            "reviewer",
            "Reviewed source.",
            {"signature_and_abi": ["functions.json#FUN_1"]},
        )


def test_behavior_verification_requires_recovered_source_and_host_tests(tmp_path):
    root = _target(tmp_path)
    _mark_recovered(root, "FUN_1")

    recovery.record_validation(
        root,
        "FUN_1",
        host_test_status="passed",
        host_test_references=["tests/test_runtime.pas"],
        has_external_effects=False,
        original_binary_status="not_required",
        original_binary_references=[],
        original_binary_reason="Pure arithmetic routine; no external effects.",
        validation_notes="All boundary cases passed.",
    )
    result = recovery.audit_target(root)

    assert result["summary"]["host_tests_passed"] == 1
    assert result["summary"]["original_binary_verified"] == 0
    assert result["summary"]["behavior_verified"] == 1
    assert result["routines"][0]["behavior_verified"] is True


def test_external_effects_require_original_binary_verification(tmp_path):
    root = _target(tmp_path)
    recovery.initialize_ledger(root)

    with pytest.raises(ValueError, match="external effects require"):
        recovery.record_validation(
            root,
            "FUN_1",
            host_test_status="passed",
            host_test_references=["tests/test_runtime.pas"],
            has_external_effects=True,
            original_binary_status="not_required",
            original_binary_references=[],
            original_binary_reason="Only a host stub was tested.",
            validation_notes="Host contract test passed.",
        )


def test_external_effects_are_verified_only_with_binary_evidence(tmp_path):
    root = _target(tmp_path)
    _mark_recovered(root, "FUN_1")

    recovery.record_validation(
        root,
        "FUN_1",
        host_test_status="passed",
        host_test_references=["tests/test_runtime.pas"],
        has_external_effects=True,
        original_binary_status="passed",
        original_binary_references=["reports/dosbox-trace.txt"],
        original_binary_reason="",
        validation_notes="Host and original-binary probes agreed.",
    )
    result = recovery.audit_target(root)

    assert result["summary"]["original_binary_verified"] == 1
    assert result["summary"]["external_effects_unverified"] == 0
    assert result["summary"]["behavior_verified"] == 1


def test_passed_validation_requires_evidence_references(tmp_path):
    root = _target(tmp_path)
    recovery.initialize_ledger(root)

    with pytest.raises(ValueError, match="host test references"):
        recovery.record_validation(
            root,
            "FUN_1",
            host_test_status="passed",
            host_test_references=[],
            has_external_effects=False,
            original_binary_status="not_run",
            original_binary_references=[],
            original_binary_reason="",
            validation_notes="No test evidence.",
        )


def test_ledger_sync_preserves_validation_results(tmp_path):
    root = _target(tmp_path)
    recovery.initialize_ledger(root)
    recovery.record_validation(
        root,
        "FUN_1",
        host_test_status="passed",
        host_test_references=["tests/test_runtime.pas"],
        has_external_effects=False,
        original_binary_status="not_required",
        original_binary_references=[],
        original_binary_reason="No external effects.",
        validation_notes="Host test passed.",
    )

    recovery.initialize_ledger(root)

    result = recovery.audit_target(root)
    assert result["summary"]["host_tests_passed"] == 1
    assert result["routines"][0]["verification"]["host_test_references"] == [
        "tests/test_runtime.pas"
    ]
