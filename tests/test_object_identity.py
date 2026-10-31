import hashlib
import json
from pathlib import Path

import pytest

from engine import (
    object_identity,
    object_lifecycle,
    object_loops,
    object_setup,
    recovery,
)


@pytest.fixture
def identity_target(tmp_path):
    root = tmp_path / "targets" / "test"
    (root / "asm").mkdir(parents=True)
    binary = bytearray(0x20000)
    binary[:2] = b"MZ"
    binary[8:10] = (8).to_bytes(2, "little")
    binary[0x18:0x1A] = (0x1C).to_bytes(2, "little")
    regions = {}
    fixups = []
    starts = {
        "caller_prefix": 0x1A816,
        "caller": 0x1A836,
        "allocation_helper": 0x25300,
        "allocation_failure": 0x24EDF,
        "allocation_error_continuation": 0x24EEA,
        "allocation_error_zero_path": 0x24F2F,
        "allocation_error_pointer_zero_path": 0x24F5B,
        "reader": 0x28758,
        "skip": 0x286C0,
        "error_check": 0x252C4,
        "filename_helper": 0x20B03,
    }
    for name, template in object_identity._CHAIN_STREAMS.items():
        address = starts[name]
        tokens = [bytes.fromhex(raw) for raw in template.split()]
        data = b"".join(tokens)
        regions[name] = {
            "address": hex(address),
            "bytes_hex": data.hex(),
            "function": f"FUN_{name}",
        }
        offset = 128 + address - 0x10000
        binary[offset : offset + len(data)] = data
        cursor = address
        lines = []
        for raw in tokens:
            linear_segment = (
                0x1000
                if name in {"caller", "caller_prefix"}
                else 0x202C
                if name == "filename_helper"
                else 0x24DD
            )
            lines.append(
                f"{linear_segment:04x}:{cursor - linear_segment * 16:04x}  NOP\n"
            )
            if raw[0] == 0x9A:
                fixups.append(offset + cursor - address + 3)
            elif name == "allocation_error_continuation" and raw == b"\xba\x71\x19":
                fixups.append(offset + cursor - address + 1)
            cursor += len(raw)
        function = (
            "FUN_24dd_0116"
            if name
            in {
                "allocation_error_continuation",
                "allocation_error_zero_path",
                "allocation_error_pointer_zero_path",
            }
            else f"FUN_{name}"
        )
        regions[name]["function"] = function
        if name == "allocation_error_pointer_zero_path":
            lines.append("24dd:01e9  NOP\n")
        assembly = root / "asm" / f"{function}.s"
        assembly.write_text(
            assembly.read_text() + "".join(lines)
            if assembly.exists()
            else "".join(lines)
        )
    (root / "asm" / "FUN_24dd_3711.s").write_text("24dd:3711  RETF\n")
    (root / "asm" / "FUN_24dd_0642.s").write_text("24dd:065f  RET\n")
    for index, location in enumerate(fixups):
        segment, offset = divmod(location - 128, 16)
        entry = 0x1C + 4 * index
        binary[entry : entry + 2] = offset.to_bytes(2, "little")
        binary[entry + 2 : entry + 4] = segment.to_bytes(2, "little")
    binary[6:8] = len(fixups).to_bytes(2, "little")
    (tmp_path / "program.exe").write_bytes(binary)
    manifest = {
        "schema_version": 1,
        "binary": {"path": "program.exe", "sha256": hashlib.sha256(binary).hexdigest()},
        "image_mapping": {"load_segment": "0x1000", "header_bytes": 128},
        "object_identity_chains": [
            {"kind": "liero_stack_input_v1", "regions": regions}
        ],
    }
    (root / "alternate_streams.json").write_text(json.dumps(manifest))
    return root


def test_stack_chain_preserves_same_object_and_leftover_argument(identity_target):
    (chain,) = object_identity.load_verified_object_identities(identity_target)
    assert chain["object"] == "SS:BP-0x104"
    assert chain["function_entry"] == 0x1A816
    assert chain["entry_gate"] == {
        "oracle": "exact_original_bytes_and_relative_targets",
        "condition": "AL != 0 after the filename check",
        "success_target": 0x1A836,
        "failure_target": 0x1A8F3,
        "local_stack_reservation_bytes": 0x206,
        "filename_helper_entry": 0x20B03,
        "filename_helper_cleanup_bytes": 4,
        "filename_helper_evidence": "exact_bytes_and_static_return_paths",
        "filename_helper_return_contract": (
            "AL is zero if subordinate AX is nonzero or the copied path is "
            "empty; otherwise AL is one."
        ),
        "filename_helper_subordinate_semantics": "unverified",
    }
    assert chain["allocation_call"] == {
        "oracle": "exact_original_bytes_and_relocated_far_target",
        "target": 0x25300,
        "request_ax": 0x206,
        "following_stack_reservation_bytes": 0x206,
        "helper_success_exit": "RETF",
        "helper_success_stack_cleanup_bytes": 0,
        "helper_checks": ["AX + 0x200", "SP", "DS:[0x640e]"],
        "helper_failure_exit": "AX=0xca; tail transfer through FUN_24dd_010f",
        "helper_failure_target": 0x24EDF,
        "failure_transfer": {
            "oracle": "exact_bytes_and_exported_instruction_boundary",
            "popped_words": ["far return IP into CX", "far return CS into BX"],
            "continuation": 0x24EEA,
            "continuation_function": "FUN_24dd_0116",
            "error_code": 0xCA,
            "data_segment": 0x2971,
            "interrupts_enabled": True,
            "error_code_store_offset": 0x6406,
            "return_address_test": "CX | BX",
            "caller_return_ip": 0xA821,
            "caller_return_cs": 0x1000,
            "caller_return_test_value": 0xB821,
            "caller_return_test_result": "nonzero; zero-branch not taken",
            "zero_branch_target": 0x24F36,
            "next_test": "DS:[0x63e4] == 0",
            "next_test_result": "unknown",
            "next_zero_branch_target": 0x24F2F,
            "next_zero_branch_target_function": "FUN_24dd_0116",
            "next_zero_path": {
                "oracle": "exact_original_bytes_and_exported_instruction_boundaries",
                "entry": 0x24F2F,
                "stored_return_ip": 0xA821,
                "stored_adjusted_return_segment": (
                    "0x1000 - DS:[0x640c] - 0x10 (16-bit)"
                ),
                "loaded_error_handler_pointer": "ES:BX from DS:[0x6402]",
                "pointer_test": "ES | BX",
                "pointer_test_result": "unknown",
                "pointer_zero_branch_target": 0x24F5B,
                "pointer_zero_path": {
                    "oracle": "exact_original_bytes_and_exported_instruction_boundaries",
                    "entry": 0x24F5B,
                    "report_helper_calls": [
                        {
                            "target": 0x284E1,
                            "pushed_pointer_offset": 0x78F0,
                            "pointer_segment": "DS",
                        },
                        {
                            "target": 0x284E1,
                            "pushed_pointer_offset": 0x79F0,
                            "pointer_segment": "DS",
                        },
                    ],
                    "interrupt_vector_loop": {
                        "vector_table_offset": 0x7AF0,
                        "vector_count_initial": 0x13,
                        "handler_offset_table": "CS:0x0239",
                        "dos_function": "INT 21h/AH=25h",
                        "loop_target": 0x24F77,
                    },
                    "saved_return_test": "DS:[0x6408] | DS:[0x640a]",
                    "saved_return_zero_branch_target": 0x24FB9,
                    "saved_return_test_result": "unknown after report/helper and interrupt calls",
                    "continuation_after_saved_return_test": "unreviewed",
                },
            },
        },
    }
    assert chain["read_destination"] == "SS:BP-0x204"
    assert chain["read_limit"] == 255
    assert chain["reader_cleanup_bytes"] == 6
    assert chain["skip_cleanup_bytes"] == 4
    assert chain["object_argument_retained_after_reader"] is True
    assert chain["stack_words_remaining"] == 0
    assert chain["resolves_call_sites"] is False
    assert chain["method_slot_preservation"] == "not_proven_across_callees"
    assert chain["status_normal_return_condition"] == "DS:[0x6410] == 0"
    assert chain["status_nonzero_path"] == "jumps_outside_reviewed_region"
    assert [call["role"] for call in chain["calls"]] == [
        "constructor",
        "input_open",
        "error_check",
        "reader",
        "skip",
        "error_check",
    ]


@pytest.mark.parametrize(
    "change",
    [
        "pointer",
        "cleanup",
        "call-target",
        "relocation",
        "assembly",
        "stale",
        "duplicate-relocation",
        "unexpected-relocation",
        "status-clobber",
        "caller-store",
        "entry-gate",
        "filename-helper-cleanup",
        "allocation-call-target",
        "allocation-helper-bytes",
        "allocation-helper-exit",
        "allocation-failure-pop",
        "allocation-failure-continuation",
        "allocation-continuation-boundary",
        "allocation-continuation-branch",
        "allocation-continuation-global-branch",
        "allocation-continuation-global-target",
        "allocation-continuation-zero-path",
        "allocation-continuation-pointer-branch",
        "allocation-continuation-pointer-target",
        "allocation-error-report-bytes",
        "allocation-error-report-helper-call",
        "allocation-error-report-branch",
        "allocation-error-report-branch-target",
        "allocation-continuation-relocation",
    ],
)
def test_stack_chain_rejects_mutation(identity_target, change):
    path = identity_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    regions = manifest["object_identity_chains"][0]["regions"]
    binary_path = identity_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    if change == "assembly":
        (identity_target / "asm" / "FUN_reader.s").write_text("24dd:3988  NOP\n")
    elif change == "allocation-continuation-boundary":
        (identity_target / "asm" / "FUN_24dd_0116.s").write_text(
            "24dd:011b  MOV DX,0x2971\n"
        )
    elif change == "allocation-continuation-relocation":
        binary[0x1C + 2 * 4 : 0x1C + 3 * 4] = bytes(4)
    elif change == "allocation-continuation-global-target":
        assembly = identity_target / "asm" / "FUN_24dd_0116.s"
        assembly.write_text(assembly.read_text().replace("24dd:015f", "24dd:0160"))
    elif change == "allocation-continuation-pointer-target":
        assembly = identity_target / "asm" / "FUN_24dd_0116.s"
        assembly.write_text(assembly.read_text().replace("24dd:018b", "24dd:018c"))
    elif change == "allocation-error-report-branch-target":
        assembly = identity_target / "asm" / "FUN_24dd_0116.s"
        assembly.write_text(assembly.read_text().replace("24dd:01e9", "24dd:01ea"))
    elif change == "relocation":
        binary[0x1C:0x20] = bytes(4)
    elif change in {"duplicate-relocation", "unexpected-relocation"}:
        entry = 0x1C + 6 * 4
        if change == "duplicate-relocation":
            binary[entry : entry + 4] = binary[0x1C:0x20]
        else:
            segment, offset = divmod(0x1A835 - 0x10000, 16)
            binary[entry : entry + 2] = offset.to_bytes(2, "little")
            binary[entry + 2 : entry + 4] = segment.to_bytes(2, "little")
        binary[6:8] = (7).to_bytes(2, "little")
    elif change == "stale":
        binary[-1] ^= 1
    else:
        name, relative = {
            "pointer": ("caller", 2),
            "cleanup": ("reader", 33),
            "call-target": ("caller", 12),
            "status-clobber": ("error_check", 0),
            "caller-store": ("caller", 32),
            "entry-gate": ("caller_prefix", 0x1C),
            "filename-helper-cleanup": (
                "filename_helper",
                len(
                    bytes.fromhex(
                        "".join(
                            object_identity._CHAIN_STREAMS["filename_helper"].split()
                        )
                    )
                )
                - 3,
            ),
            "allocation-call-target": ("caller_prefix", 7),
            "allocation-helper-bytes": ("allocation_helper", 0),
            "allocation-helper-exit": ("allocation_helper", 21),
            "allocation-failure-pop": ("allocation_failure", 0),
            "allocation-failure-continuation": ("allocation_failure", 3),
            "allocation-continuation-branch": ("allocation_error_continuation", 13),
            "allocation-continuation-global-branch": (
                "allocation_error_continuation",
                20,
            ),
            "allocation-continuation-zero-path": (
                "allocation_error_zero_path",
                0,
            ),
            "allocation-continuation-pointer-branch": (
                "allocation_error_zero_path",
                23,
            ),
            "allocation-error-report-bytes": (
                "allocation_error_pointer_zero_path",
                0,
            ),
            "allocation-error-report-helper-call": (
                "allocation_error_pointer_zero_path",
                7,
            ),
            "allocation-error-report-branch": (
                "allocation_error_pointer_zero_path",
                51,
            ),
        }[change]
        raw = bytearray.fromhex(regions[name]["bytes_hex"])
        raw[relative] ^= 1
        offset = 128 + int(regions[name]["address"], 16) - 0x10000
        binary[offset : offset + len(raw)] = raw
        regions[name]["bytes_hex"] = raw.hex()
    binary_path.write_bytes(binary)
    if change != "stale":
        manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        object_identity.load_verified_object_identities(identity_target)


def test_stack_chain_optional(tmp_path):
    assert object_identity.load_verified_object_identities(tmp_path) == []


def test_identity_rejects_missing_linked_lifecycle(identity_target):
    """Oracle: requested setup evidence cannot silently fall back to a callee assumption."""
    path = identity_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    manifest["object_identity_chains"][0]["input_setup_protocol_kind"] = "missing"
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="matching checked input lifecycle"):
        object_identity.load_verified_object_identities(identity_target)


@pytest.fixture
def loop_target(identity_target):
    """Oracle: complete synthetic post-gate caller and all new byte-bound dependencies."""
    path = identity_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    binary_path = identity_target.parent.parent / "program.exe"
    old = binary_path.read_bytes()
    binary = bytearray(old[:128] + bytes(128) + old[128:])
    binary[8:10] = (16).to_bytes(2, "little")
    manifest["image_mapping"]["header_bytes"] = 256
    regions = {}
    for name, (entry, template) in object_loops._LOOP_STREAMS.items():
        address = (0x10000 if name == "caller_tail" else 0x24DD0) + entry
        data = bytes.fromhex("".join(template.split()))
        offset = 256 + address - 0x10000
        binary[offset : offset + len(data)] = data
        regions[name] = {"address": hex(address), "bytes_hex": data.hex()}
        if name == "caller_tail":
            cursor = address
            lines = []
            for token in template.split():
                lines.append(f"1000:{cursor - 0x10000:04x}  NOP\n")
                cursor += len(bytes.fromhex(token))
            with (identity_target / "asm" / "FUN_caller.s").open("a") as stream:
                stream.write("".join(lines))
    # Keep one fixup per far call, including the original six in the prefix.
    base_fixup_count = int.from_bytes(binary[6:8], "little")
    fixups = [
        int.from_bytes(binary[i : i + 2], "little")
        + 16 * int.from_bytes(binary[i + 2 : i + 4], "little")
        for i in range(0x1C, 0x1C + base_fixup_count * 4, 4)
    ]
    tail_address = int(regions["caller_tail"]["address"], 16)
    cursor = tail_address
    for token in object_loops._LOOP_STREAMS["caller_tail"][1].split():
        raw = bytes.fromhex(token)
        if raw[0] == 0x9A:
            fixups.append(cursor - 0x10000 + 3)
        cursor += len(raw)
    for index, location in enumerate(fixups):
        segment, offset = divmod(location, 16)
        entry = 0x1C + index * 4
        binary[entry : entry + 2] = offset.to_bytes(2, "little")
        binary[entry + 2 : entry + 4] = segment.to_bytes(2, "little")
    binary[6:8] = len(fixups).to_bytes(2, "little")
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    record = manifest["object_identity_chains"][0]
    record["loop_regions"] = regions
    path.write_text(json.dumps(manifest))
    return identity_target


def test_full_caller_stack_and_callback_effects(loop_target):
    """Oracle: local CFG fixed point, including both loop backedges."""
    (chain,) = object_identity.load_verified_object_identities(loop_target)
    loops = chain["caller_loops"]
    assert loops["entry"] == 0x1A836
    assert loops["end"] == 0x1A8F7
    assert loops["backedges"] == [
        {"address": 0x1A881, "target": 0x1A85B},
        {"address": 0x1A8E1, "target": 0x1A8B2},
    ]
    assert loops["stack_balanced_at_return"] is True
    assert len(loops["calls"]) == 14
    assert loops["object_calls"] == [
        0x1A841,
        0x1A84C,
        0x1A86A,
        0x1A86F,
        0x1A88F,
        0x1A8CB,
        0x1A8D0,
        0x1A8E9,
    ]
    assert loops["direct_local_store_offsets"] == [-0x206, -4, -2]
    assert loops["random_helper_writes"] == ["DS:0x6412/2", "DS:0x6414/2"]
    assert loops["callback_targets"] == [0x286DE, 0x286F3, 0x2877B]
    assert loops["callback_write_kind"] == "ES:DI byte stores only"
    assert loops["global_destination_offset_range"] == [0x66EC, 0x7BEB]
    assert loops["resolves_call_sites"] is False
    assert loops["slot_continuity"] == "unlinked_callee_summaries"
    assert chain["method_slot_preservation"] == "not_proven_across_callees"
    assert len(loops["relocation_file_offsets"]) == 20
    assert loops["assumptions"] and loops["remaining_obligations"]


@pytest.fixture
def linked_loop_target(loop_target):
    """Oracle: independently byte-checked setup and lifecycle linked to the full caller."""
    path = loop_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    binary_path = loop_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    setup_regions = {}
    starts = {"constructor": 0x28409, "setup": 0x28FDC, "helper": 0x29069}
    for name, template in object_setup._REVIEWED_STREAMS.items():
        address = starts[name]
        data = bytes.fromhex("".join(template.split()))
        offset = 256 + address - 0x10000
        binary[offset : offset + len(data)] = data
        setup_regions[name] = {"address": hex(address), "bytes_hex": data.hex()}
    lifecycle_regions = {}
    for name, (entry, template) in object_lifecycle._INPUT_STREAMS.items():
        address = 0x24DD0 + entry
        data = bytes.fromhex("".join(template.split()))
        offset = 256 + address - 0x10000
        binary[offset : offset + len(data)] = data
        lifecycle_regions[name] = {"address": hex(address), "bytes_hex": data.hex()}
    setup_fixup_start = int.from_bytes(binary[6:8], "little")
    for index, address in enumerate(
        [0x28433, 0x29011, 0x2902C, 0x29042, 0x29061], setup_fixup_start
    ):
        segment, offset = divmod(address - 0x10000, 16)
        entry = 0x1C + 4 * index
        binary[entry : entry + 2] = offset.to_bytes(2, "little")
        binary[entry + 2 : entry + 4] = segment.to_bytes(2, "little")
    binary[6:8] = (setup_fixup_start + 5).to_bytes(2, "little")
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    manifest["object_setup_protocols"] = [
        {
            "kind": "liero_file_object_v1",
            "regions": setup_regions,
            "input_lifecycle_regions": lifecycle_regions,
        }
    ]
    manifest["object_identity_chains"][0]["input_setup_protocol_kind"] = (
        "liero_file_object_v1"
    )
    path.write_text(json.dumps(manifest))
    return loop_target


def test_linked_loop_continuity_is_conditional(linked_loop_target):
    """Oracle: caller closure is promoted only to a conditional, scoped static statement."""
    (chain,) = object_identity.load_verified_object_identities(linked_loop_target)
    assert chain["method_slot_preservation"] == "conditional_for_post_gate_caller"
    loops = chain["caller_loops"]
    assert (
        loops["slot_continuity"] == "conditional_on_normal_zero_status_and_nonaliasing"
    )
    assert loops["input_method_slots"]["0x14"] == "0x24dd:375e"
    assert loops["input_method_slots"]["0x18"] == "0x0000:0000"
    assert (
        loops["optional_slot_0x18_call"]
        == "excluded_by_zero_segment_guard_on_input_path"
    )
    assert loops["post_close_mode"] == "0xd7b0"
    assert any("physically alias" in assumption for assumption in chain["assumptions"])
    assert any("succeed" in assumption for assumption in chain["assumptions"])
    assert not chain["resolves_call_sites"]


@pytest.mark.parametrize(
    "change",
    [
        "missing-lifecycle",
        "missing-tail",
        "extra-relocation",
        "duplicate-fixup",
        "wrong-placement",
        "assembly",
    ],
)
def test_loop_link_rejects_incomplete_evidence(linked_loop_target, change):
    """Oracle: no continuity statement from incomplete dependencies or loader rewrites."""
    path = linked_loop_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    record = manifest["object_identity_chains"][0]
    binary_path = linked_loop_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    if change == "missing-lifecycle":
        del manifest["object_setup_protocols"][0]["input_lifecycle_regions"]
    elif change == "missing-tail":
        del record["loop_regions"]["constructor_tail"]
    elif change == "wrong-placement":
        record["loop_regions"]["random_core"]["address"] = "0x29482"
    elif change == "assembly":
        assembly = linked_loop_target / "asm" / "FUN_caller.s"
        assembly.write_text(assembly.read_text().replace("1000:a8e9", "1001:a8d9"))
    else:
        entry = 0x1C + 19 * 4
        if change == "duplicate-fixup":
            binary[entry : entry + 4] = binary[0x34:0x38]
        else:
            segment, offset = divmod(0x285BB - 0x10000, 16)
            binary[entry : entry + 2] = offset.to_bytes(2, "little")
            binary[entry + 2 : entry + 4] = segment.to_bytes(2, "little")
        binary[6:8] = (20).to_bytes(2, "little")
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        object_identity.load_verified_object_identities(linked_loop_target)


@pytest.mark.parametrize(
    ("name", "before", "after"),
    [
        ("caller_tail", "8dbefcfe", "8dbefafe"),
        ("caller_tail", "75d8", "75d9"),
        ("caller_tail", "c20200", "c20400"),
        ("caller_tail", "8986fafd", "898610ff"),
        ("random_core", "a31264", "a31464"),
        ("refill", "26ff5f14", "26ff5f18"),
        ("callback_read", "aa", "ab"),
        ("constructor_tail", "ca0800", "ca0600"),
    ],
)
def test_loop_evidence_rejects_changed_effects(loop_target, name, before, after):
    """Oracle: rehashed changes to pointers, stores, branches and cleanup fail closed."""
    path = loop_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    region = manifest["object_identity_chains"][0]["loop_regions"][name]
    assert before in region["bytes_hex"]
    region["bytes_hex"] = region["bytes_hex"].replace(before, after, 1)
    binary_path = loop_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    raw = bytes.fromhex(region["bytes_hex"])
    offset = 256 + int(region["address"], 16) - 0x10000
    binary[offset : offset + len(raw)] = raw
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError):
        object_identity.load_verified_object_identities(loop_target)


def test_liero_concrete_identity_chain():
    repository = Path(__file__).resolve().parents[1]
    if not (repository / "extracted" / "liero" / "LIERO.EXE").is_file():
        pytest.skip("Liero BYOD executable unavailable")
    report = recovery.audit_target(repository / "targets" / "liero")
    (chain,) = report["object_identity_chains"]
    assert chain["entry"] == 0x1A836
    assert chain["function_entry"] == 0x1A816
    assert chain["entry_gate"]["success_target"] == 0x1A836
    assert chain["entry_gate"]["failure_target"] == 0x1A8F3
    assert chain["object"] == "SS:BP-0x104"
    assert [call["address"] for call in chain["calls"]] == [
        0x1A841,
        0x1A84C,
        0x1A851,
        0x1A86A,
        0x1A86F,
        0x1A874,
    ]
    assert len(chain["relocation_file_offsets"]) == 13
    assert chain["allocation_call"]["failure_transfer"]["caller_return_ip"] == 0xA821
    assert chain["allocation_call"]["failure_transfer"]["caller_return_cs"] == 0x1000
    assert (
        chain["allocation_call"]["failure_transfer"]["caller_return_test_result"]
        == "nonzero; zero-branch not taken"
    )
    assert chain["input_open_evidence"]["success_method_slots"]["0x14"] == "0x24dd:375e"
    assert chain["input_open_evidence"]["cleanup_bytes"] == 4
    assert chain["method_slot_preservation"] == "conditional_for_post_gate_caller"
    loops = chain["caller_loops"]
    assert (
        loops["slot_continuity"] == "conditional_on_normal_zero_status_and_nonaliasing"
    )
    assert (
        loops["optional_slot_0x18_call"]
        == "excluded_by_zero_segment_guard_on_input_path"
    )
    assert loops["post_close_mode"] == "0xd7b0"
    assert len(loops["calls"]) == 14
    assert len(loops["relocation_file_offsets"]) == 20
    (protocol,) = report["object_setup_protocols"]
    assert "input_lifecycle" in protocol
    assert len(protocol["input_lifecycle"]["reopen_from_input"]) == 4
    assert report["summary"]["unresolved_control_transfers"] == 13
