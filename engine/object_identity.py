"""Conditional argument-identity evidence for a concrete Liero input caller."""

from __future__ import annotations

import json
import pathlib

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.callbacks import _bound_region, _export
from engine.object_loops import verify_caller_loops
from engine.object_setup import load_verified_object_setups

_CHAIN_STREAMS = {
    "caller_prefix": """
        55 89e5 b80602 9a3005dd14 81ec0602 bf0ca8 0e 57
        9a43082c10 08c0 7503 e9bd00
    """,
    "allocation_helper": """
        050002 720d 2bc4 7309 f7d8 3b060e64 7201 cb b8ca00 e9c7fb
    """,
    "allocation_failure": "59 5b eb07",
    "allocation_error_continuation": """
        ba7119 8eda fb a30664 8bc1 0bc3 743d a1e463 0bc0 742f
    """,
    "allocation_error_zero_path": """
        2b1e0c64 83eb10 890e0864 891e0a64 c41e0264 8cc0 0bc3 7413
    """,
    "allocation_error_pointer_zero_path": """
        b8f078 1e 50 0e e87d35 b8f079 1e 50 0e e87435
        bff07a be3902 b91300 90 fc 2eac b425 1e c515 cd21
        1f 83c704 e2f0 a10864 0b060a64 7429
    """,
    "caller": """
        8dbefcfe 16 57 bf0ca8 0e 57 9a3936dd14
        8dbefcfe 16 57 9ab736dd14 9af404dd14 c746feffff
        8dbefcfe 16 57 8dbefcfd 16 57 68ff00 9a8839dd14
        9af038dd14 9af404dd14
    """,
    "reader": """
        55 8bec c45e0c b8ab39 8b4e06 8b7e08 8b560a 47 e84efe
        8bc7 c47e08 2bc7 48 aa 5d ca0600
    """,
    "skip": """
        55 8bec c45e06 b80e39 33d2 e8eefe 750a 26837f1a00 7403
        e87000 5d ca0400
    """,
    "error_check": "833e106400 7501 cb a11064 e90dfc",
    "filename_helper": """
        c8820100 8cd3 8ec3 8cdb fc 8dbefefe c57606 ac aa 91 30ed
        f3a4 8edb 8dbe7efe 16 57 8dbefefe 16 57 9a223bdd14
        c606226400 8dbe7efe 16 57 688000 9a5d3bdd14
        8dbe7efe 16 57 9ade3bdd14 9aed04dd14 09c0 7507
        80befefe00 7504 b000 eb02 b001 8846ff 8a46ff c9 ca0400
    """,
}


def _chain_regions(
    record: dict, root: pathlib.Path, binary: bytes, header: int, load_segment: int
) -> dict:
    """Oracle: exact reviewed bytes and exported instruction boundaries."""
    regions = record.get("regions")
    if not isinstance(regions, dict) or set(regions) != set(_CHAIN_STREAMS):
        raise ValueError("identity chain requires all reviewed regions")
    result = {}
    for name, template in _CHAIN_STREAMS.items():
        region = regions[name]
        start, data = _bound_region(region, binary, header, load_segment * 16)
        tokens = [bytes.fromhex(raw) for raw in template.split()]
        if data != b"".join(tokens):
            raise ValueError(f"identity chain disagrees with reviewed {name} bytes")
        instructions = {}
        cursor = start
        for raw in tokens:
            instructions[cursor] = raw
            cursor += len(raw)
        parsed = _export(root, region.get("function"))
        if start not in parsed["addrs"]:
            raise ValueError("identity chain region is not exported")
        index = parsed["addrs"].index(start)
        if parsed["addrs"][index : index + len(tokens)] != list(instructions):
            raise ValueError("identity chain assembly boundaries disagree")
        expected_segment = (
            load_segment
            if name in {"caller", "caller_prefix"}
            else 0x202C
            if name == "filename_helper"
            else (load_segment + 0x14DD) & 0xFFFF
        )
        if set(parsed["segments"][index : index + len(tokens)]) != {expected_segment}:
            raise ValueError("identity chain assembly segment disagrees")
        if (
            not expected_segment * 16
            <= start
            < cursor
            <= expected_segment * 16 + 0x10000
        ):
            raise ValueError("identity chain region crosses its code segment")
        result[name] = instructions
    return result


def _call_relocations(
    instructions: dict, binary: bytes, header: int, load_segment: int
) -> list[int]:
    """Oracle: each far call has exactly one segment fixup and no other code fixups."""
    locations = _mz_relocation_locations(binary, header)
    expected = []
    occupied = set()
    for name, region in instructions.items():
        for address, raw in region.items():
            offset = header + address - load_segment * 16
            occupied.update(range(offset, offset + len(raw)))
            if raw[0] == 0x9A:
                expected.append(offset + 3)
            elif name == "allocation_error_continuation" and raw == b"\xba\x71\x19":
                expected.append(offset + 1)
    overlapping = {
        location
        for location in locations
        if location in occupied or location + 1 in occupied
    }
    if overlapping != set(expected):
        raise ValueError("identity chain far-call relocations disagree")
    table = int.from_bytes(binary[0x18:0x1A], "little")
    count = int.from_bytes(binary[6:8], "little")
    actual = [
        header
        + int.from_bytes(binary[i + 2 : i + 4], "little") * 16
        + int.from_bytes(binary[i : i + 2], "little")
        for i in range(table, table + count * 4, 4)
    ]
    if any(actual.count(location) != 1 for location in expected):
        raise ValueError("identity chain relocation must occur once")
    return expected


def _stack_handoff(instructions: dict, load_segment: int) -> list[dict]:
    """Oracle: symbolic caller argument stack under explicit normal-return summaries."""
    stack = []
    di = ""
    calls = []
    summaries = {
        0x3639: ("constructor", 8),
        0x36B7: ("input_open", 4),
        0x04F4: ("error_check", 0),
        0x3988: ("reader", 6),
        0x38F0: ("skip", 4),
    }
    object_words = ["SS", "BP-0x104"]
    for address, raw in instructions["caller"].items():
        if raw[:2] == b"\x8d\xbe":
            displacement = int.from_bytes(raw[2:], "little", signed=True)
            di = f"BP-0x{-displacement:x}"
        elif raw[0] == 0xBF:
            di = f"0x{int.from_bytes(raw[1:], 'little'):x}"
        elif raw == b"\x16":
            stack.append("SS")
        elif raw == b"\x0e":
            stack.append("CS")
        elif raw == b"\x57":
            stack.append(di)
        elif raw[0] == 0x68:
            stack.append(str(int.from_bytes(raw[1:], "little")))
        elif raw[0] == 0x9A:
            offset = int.from_bytes(raw[1:3], "little")
            segment = (int.from_bytes(raw[3:5], "little") + load_segment) & 0xFFFF
            role, cleanup = summaries[offset]
            if role == "constructor" and stack != [*object_words, "CS", "0xa80c"]:
                raise ValueError("constructor object argument disagrees")
            if role in {"input_open", "skip"} and stack != object_words:
                raise ValueError("object argument identity changed")
            if role == "reader" and stack != [*object_words, "SS", "BP-0x204", "255"]:
                raise ValueError("reader object/destination arguments disagree")
            if role == "reader":
                cleanup = int.from_bytes(
                    list(instructions["reader"].values())[-1][1:], "little"
                )
            elif role == "skip":
                cleanup = int.from_bytes(
                    list(instructions["skip"].values())[-1][1:], "little"
                )
            calls.append(
                {
                    "address": address,
                    "target": segment * 16 + offset,
                    "role": role,
                    "cleanup_bytes": cleanup,
                    "argument_words_before": list(stack),
                }
            )
            if cleanup:
                if cleanup // 2 > len(stack):
                    raise ValueError("identity chain argument stack underflow")
                del stack[-(cleanup // 2) :]
    if stack:
        raise ValueError("identity chain leaves unexpected argument words")
    return calls


def _identity(
    record: dict, root: pathlib.Path, binary: bytes, header: int, load_segment: int
) -> dict:
    """Oracle: bounded caller-to-callee argument identity, not method-state continuity."""
    if not isinstance(record, dict) or record.get("kind") != "liero_stack_input_v1":
        raise ValueError("unsupported object identity chain")
    instructions = _chain_regions(record, root, binary, header, load_segment)
    relocations = _call_relocations(instructions, binary, header, load_segment)
    prefix_entry = min(instructions["caller_prefix"])
    success_branch = instructions["caller_prefix"][prefix_entry + 0x1B]
    failure_branch = instructions["caller_prefix"][prefix_entry + 0x1D]
    if success_branch[0] != 0x75 or failure_branch[0] != 0xE9:
        raise ValueError("caller entry gate disagrees with reviewed branches")
    success_target = (
        prefix_entry
        + 0x1B
        + len(success_branch)
        + int.from_bytes(success_branch[1:], "little", signed=True)
    )
    failure_target = (
        prefix_entry
        + 0x1D
        + len(failure_branch)
        + int.from_bytes(failure_branch[1:], "little", signed=True)
    )
    if success_target != min(instructions["caller"]):
        raise ValueError("caller entry gate does not reach the reviewed body")
    allocation_call_address = prefix_entry + 0x06
    allocation_call = instructions["caller_prefix"][allocation_call_address]
    allocation_target_segment = (
        int.from_bytes(allocation_call[3:5], "little") + load_segment
    ) & 0xFFFF
    allocation_target = allocation_target_segment * 16 + int.from_bytes(
        allocation_call[1:3], "little"
    )
    allocation_helper = instructions["allocation_helper"]
    allocation_helper_entry = min(allocation_helper)
    allocation_helper_return = allocation_helper[allocation_helper_entry + 0x11]
    allocation_error_jump = allocation_helper[allocation_helper_entry + 0x15]
    allocation_error_target = (
        allocation_helper_entry
        + 0x18
        + int.from_bytes(allocation_error_jump[1:], "little", signed=True)
    )
    if (
        allocation_call[0] != 0x9A
        or allocation_target != allocation_helper_entry
        or instructions["caller_prefix"][prefix_entry + 0x03] != b"\xb8\x06\x02"
        or instructions["caller_prefix"][prefix_entry + 0x0B] != b"\x81\xec\x06\x02"
    ):
        raise ValueError("allocation call, request, or stack reservation disagrees")
    if (
        allocation_helper_return != b"\xcb"
        or allocation_error_jump[:1] != b"\xe9"
        or allocation_error_target != allocation_helper_entry - 0x421
    ):
        raise ValueError(
            "allocation helper return or external failure transfer disagrees"
        )
    allocation_failure = instructions["allocation_failure"]
    allocation_failure_entry = min(allocation_failure)
    allocation_continuation_jump = allocation_failure[allocation_failure_entry + 2]
    allocation_continuation = (
        allocation_failure_entry
        + 4
        + int.from_bytes(allocation_continuation_jump[1:], "little", signed=True)
    )
    shared_error = _export(root, "FUN_24dd_0116")
    error_continuation = instructions["allocation_error_continuation"]
    error_entry = min(error_continuation)
    error_branch = error_continuation[error_entry + 0x0D]
    error_branch_target = (
        error_entry + 0x0F + int.from_bytes(error_branch[1:], "little", signed=True)
    )
    global_error_branch = error_continuation[error_entry + 0x14]
    global_error_branch_target = (
        error_entry
        + 0x16
        + int.from_bytes(global_error_branch[1:], "little", signed=True)
    )
    error_zero_path = instructions["allocation_error_zero_path"]
    error_zero_path_entry = min(error_zero_path)
    error_pointer_branch = error_zero_path[error_zero_path_entry + 0x17]
    error_pointer_branch_target = (
        error_zero_path_entry
        + 0x19
        + int.from_bytes(error_pointer_branch[1:], "little", signed=True)
    )
    pointer_zero_path = instructions["allocation_error_pointer_zero_path"]
    pointer_zero_path_entry = min(pointer_zero_path)
    first_report_call = pointer_zero_path[pointer_zero_path_entry + 6]
    second_report_call = pointer_zero_path[pointer_zero_path_entry + 0x0F]
    first_report_target = (
        pointer_zero_path_entry
        + 9
        + int.from_bytes(first_report_call[1:], "little", signed=True)
    )
    second_report_target = (
        pointer_zero_path_entry
        + 0x12
        + int.from_bytes(second_report_call[1:], "little", signed=True)
    )
    vector_loop = pointer_zero_path[pointer_zero_path_entry + 0x2A]
    vector_loop_target = (
        pointer_zero_path_entry
        + 0x2C
        + int.from_bytes(vector_loop[1:], "little", signed=True)
    )
    report_return_branch = pointer_zero_path[pointer_zero_path_entry + 0x33]
    report_return_branch_target = (
        pointer_zero_path_entry
        + 0x35
        + int.from_bytes(report_return_branch[1:], "little", signed=True)
    )
    caller_return_ip = prefix_entry - load_segment * 16 + 0x0B
    if (
        allocation_error_target != allocation_failure_entry
        or allocation_failure[allocation_failure_entry] != b"\x59"
        or allocation_failure[allocation_failure_entry + 1] != b"\x5b"
        or allocation_continuation_jump[:1] != b"\xeb"
        or allocation_continuation not in shared_error["addrs"]
        or allocation_continuation != error_entry
    ):
        raise ValueError("allocation failure stub does not reach the checked handler")
    if (
        error_continuation[error_entry] != b"\xba\x71\x19"
        or error_continuation[error_entry + 3] != b"\x8e\xda"
        or error_continuation[error_entry + 5] != b"\xfb"
        or error_continuation[error_entry + 6] != b"\xa3\x06\x64"
        or error_continuation[error_entry + 9] != b"\x8b\xc1"
        or error_continuation[error_entry + 11] != b"\x0b\xc3"
        or error_branch[:1] != b"\x74"
        or error_continuation[error_entry + 0x0F] != b"\xa1\xe4\x63"
        or error_continuation[error_entry + 0x12] != b"\x0b\xc0"
        or global_error_branch[:1] != b"\x74"
        or caller_return_ip == 0
    ):
        raise ValueError("shared allocation-error prefix disagrees with its template")
    if error_branch_target not in shared_error["addrs"]:
        raise ValueError("allocation-error zero branch misses its exported boundary")
    if global_error_branch_target not in shared_error["addrs"]:
        raise ValueError("allocation-error global branch misses its exported boundary")
    if (
        global_error_branch_target != error_zero_path_entry
        or error_pointer_branch[:1] != b"\x74"
        or error_pointer_branch_target not in shared_error["addrs"]
    ):
        raise ValueError("allocation-error zero path disagrees with its branch targets")
    report_helper = _export(root, "FUN_24dd_3711")
    if (
        pointer_zero_path_entry != error_pointer_branch_target
        or first_report_call[:1] != b"\xe8"
        or second_report_call[:1] != b"\xe8"
        or first_report_target != min(report_helper["addrs"])
        or second_report_target != min(report_helper["addrs"])
        or pointer_zero_path[pointer_zero_path_entry + 0x24] != b"\xcd\x21"
        or pointer_zero_path[pointer_zero_path_entry + 0x2A][:1] != b"\xe2"
        or vector_loop_target not in shared_error["addrs"]
        or report_return_branch[:1] != b"\x74"
        or report_return_branch_target not in shared_error["addrs"]
    ):
        raise ValueError(
            "allocation-error pointer-zero path disagrees with its template"
        )
    filename_call_address = prefix_entry + 0x14
    filename_call = instructions["caller_prefix"][filename_call_address]
    filename_target_segment = (
        int.from_bytes(filename_call[3:5], "little") + load_segment
    ) & 0xFFFF
    filename_target = filename_target_segment * 16 + int.from_bytes(
        filename_call[1:3], "little"
    )
    helper = instructions["filename_helper"]
    helper_return = list(helper.values())[-1]
    if filename_call[0] != 0x9A or filename_target != min(helper):
        raise ValueError("filename-check call does not reach the reviewed helper")
    if helper_return != b"\xca\x04\x00":
        raise ValueError("filename-check helper cleanup disagrees")
    calls = _stack_handoff(instructions, load_segment)
    reader = next(call for call in calls if call["role"] == "reader")
    skip = next(call for call in calls if call["role"] == "skip")
    for call in calls:
        if call["role"] in {"reader", "skip", "error_check"} and call["target"] != min(
            instructions[call["role"]]
        ):
            raise ValueError("identity chain call does not target recorded callee")
    identity = {
        "kind": record["kind"],
        "entry": min(instructions["caller"]),
        "function_entry": prefix_entry,
        "entry_gate": {
            "oracle": "exact_original_bytes_and_relative_targets",
            "condition": "AL != 0 after the filename check",
            "success_target": success_target,
            "failure_target": failure_target,
            "local_stack_reservation_bytes": int.from_bytes(
                instructions["caller_prefix"][prefix_entry + 0x0B][2:4],
                "little",
            ),
            "filename_helper_entry": filename_target,
            "filename_helper_cleanup_bytes": int.from_bytes(
                helper_return[1:], "little"
            ),
            "filename_helper_evidence": "exact_bytes_and_static_return_paths",
            "filename_helper_return_contract": (
                "AL is zero if subordinate AX is nonzero or the copied path is "
                "empty; otherwise AL is one."
            ),
            "filename_helper_subordinate_semantics": "unverified",
        },
        "allocation_call": {
            "oracle": "exact_original_bytes_and_relocated_far_target",
            "target": allocation_target,
            "request_ax": 0x206,
            "following_stack_reservation_bytes": 0x206,
            "helper_success_exit": "RETF",
            "helper_success_stack_cleanup_bytes": 0,
            "helper_checks": ["AX + 0x200", "SP", "DS:[0x640e]"],
            "helper_failure_exit": "AX=0xca; tail transfer through FUN_24dd_010f",
            "helper_failure_target": allocation_error_target,
            "failure_transfer": {
                "oracle": "exact_bytes_and_exported_instruction_boundary",
                "popped_words": ["far return IP into CX", "far return CS into BX"],
                "continuation": allocation_continuation,
                "continuation_function": "FUN_24dd_0116",
                "error_code": 0xCA,
                "data_segment": (0x1971 + load_segment) & 0xFFFF,
                "interrupts_enabled": True,
                "error_code_store_offset": 0x6406,
                "return_address_test": "CX | BX",
                "caller_return_ip": caller_return_ip,
                "caller_return_cs": load_segment,
                "caller_return_test_value": (caller_return_ip | load_segment),
                "caller_return_test_result": "nonzero; zero-branch not taken",
                "zero_branch_target": error_branch_target,
                "next_test": "DS:[0x63e4] == 0",
                "next_test_result": "unknown",
                "next_zero_branch_target": global_error_branch_target,
                "next_zero_branch_target_function": "FUN_24dd_0116",
                "next_zero_path": {
                    "oracle": "exact_original_bytes_and_exported_instruction_boundaries",
                    "entry": error_zero_path_entry,
                    "stored_return_ip": caller_return_ip,
                    "stored_adjusted_return_segment": (
                        f"0x{load_segment:04x} - DS:[0x640c] - 0x10 (16-bit)"
                    ),
                    "loaded_error_handler_pointer": "ES:BX from DS:[0x6402]",
                    "pointer_test": "ES | BX",
                    "pointer_test_result": "unknown",
                    "pointer_zero_branch_target": error_pointer_branch_target,
                    "pointer_zero_path": {
                        "oracle": "exact_original_bytes_and_exported_instruction_boundaries",
                        "entry": pointer_zero_path_entry,
                        "report_helper_calls": [
                            {
                                "target": first_report_target,
                                "pushed_pointer_offset": 0x78F0,
                                "pointer_segment": "DS",
                            },
                            {
                                "target": second_report_target,
                                "pushed_pointer_offset": 0x79F0,
                                "pointer_segment": "DS",
                            },
                        ],
                        "interrupt_vector_loop": {
                            "vector_table_offset": 0x7AF0,
                            "vector_count_initial": 0x13,
                            "handler_offset_table": "CS:0x0239",
                            "dos_function": "INT 21h/AH=25h",
                            "loop_target": vector_loop_target,
                        },
                        "saved_return_test": "DS:[0x6408] | DS:[0x640a]",
                        "saved_return_zero_branch_target": report_return_branch_target,
                        "saved_return_test_result": "unknown after report/helper and interrupt calls",
                        "continuation_after_saved_return_test": "unreviewed",
                    },
                },
            },
        },
        "object": "SS:BP-0x104",
        "read_destination": "SS:BP-0x204",
        "read_limit": 255,
        "reader_cleanup_bytes": reader["cleanup_bytes"],
        "skip_cleanup_bytes": skip["cleanup_bytes"],
        "object_argument_retained_after_reader": True,
        "stack_words_remaining": 0,
        "calls": calls,
        "relocation_file_offsets": relocations,
        "status_normal_return_condition": "DS:[0x6410] == 0",
        "status_nonzero_path": "jumps_outside_reviewed_region",
        "caller_direct_stores": [{"base": "SS:BP", "displacement": -2, "bytes": 2}],
        "method_slot_preservation": "not_proven_across_callees",
        "resolves_call_sites": False,
        "assumptions": [
            "The allocator's normal RETF path preserves caller BP/SS and live stack words.",
            "The filename-check callee returns normally; its subordinate side effects are unverified.",
            "Calls return normally, preserving caller BP/SS and live argument words.",
            "Constructor and input-open summaries remove 8 and 4 argument bytes.",
            "DS:[0x6410] is zero at each status-check call; its nonzero path is out of scope.",
            "Buffer and external writes do not alias the object or live stack words.",
        ],
        "remaining_obligations": [
            "Validate input-open and close/reopen effects on this same object.",
            "Prove method slots survive all intervening calls and external effects.",
            "Verify the shared allocator-error continuation and filename-check subordinate effects.",
        ],
    }
    if "loop_regions" in record:
        identity["caller_loops"] = verify_caller_loops(
            record["loop_regions"],
            root,
            binary,
            header,
            load_segment,
            {
                name: stream
                for name, stream in instructions.items()
                if name
                not in {
                    "allocation_failure",
                    "allocation_error_continuation",
                    "allocation_error_zero_path",
                    "allocation_error_pointer_zero_path",
                }
            },
            record["regions"]["caller"]["function"],
        )
    return identity


def load_verified_object_identities(root: pathlib.Path) -> list[dict]:
    """Oracle: optional binary-bound concrete argument-identity chains."""
    path = root / "alternate_streams.json"
    if not path.is_file():
        return []
    manifest = json.loads(path.read_text())
    records = (
        manifest.get("object_identity_chains", [])
        if isinstance(manifest, dict)
        else None
    )
    if not isinstance(records, list):
        raise TypeError("object_identity_chains must be an array")
    if not records:
        return []
    binary, header, load_segment, binary_hash = load_binary_evidence(root, manifest)
    protocols = (
        load_verified_object_setups(root)
        if any(
            isinstance(record, dict) and "input_setup_protocol_kind" in record
            for record in records
        )
        else []
    )
    result = []
    for record in records:
        identity = {
            **_identity(record, root, binary, header, load_segment),
            "binary_sha256": binary_hash,
        }
        if "input_setup_protocol_kind" in record:
            _link_input_setup(identity, record["input_setup_protocol_kind"], protocols)
        result.append(identity)
    return result


def _link_input_setup(identity: dict, kind: object, protocols: list[dict]) -> None:
    """Oracle: same-binary input-open target and checked wrapper cleanup."""
    matches = [
        protocol
        for protocol in protocols
        if protocol["kind"] == kind
        and protocol["binary_sha256"] == identity["binary_sha256"]
    ]
    if len(matches) != 1 or "input_lifecycle" not in matches[0]:
        raise ValueError("identity requires one matching checked input lifecycle")
    lifecycle = matches[0]["input_lifecycle"]
    (call,) = [call for call in identity["calls"] if call["role"] == "input_open"]
    if (
        call["target"] != lifecycle["streams"]["input_entry"]["entry"]
        or call["cleanup_bytes"] != lifecycle["open_cleanup_bytes"]
    ):
        raise ValueError("identity input-open disagrees with checked lifecycle")
    (success,) = [
        outcome
        for outcome in lifecycle["open_from_closed"]
        if outcome["mode"] == "0xd7b1"
    ]
    identity["input_open_evidence"] = {
        "protocol_kind": kind,
        "entry": call["target"],
        "cleanup_bytes": lifecycle["open_cleanup_bytes"],
        "success_method_slots": success["method_slots"],
        "analysis": lifecycle["analysis"],
        "resolves_call_sites": False,
    }
    identity["assumptions"][2] = (
        "Constructor summary removes 8 argument bytes; input-open cleanup is byte-checked."
    )
    identity["remaining_obligations"][0] = (
        "Extend same-object caller evidence beyond this slice to its reopen and close calls."
    )
    if "caller_loops" in identity:
        _compose_caller_loops(identity, matches[0])


def _compose_caller_loops(identity: dict, setup: dict) -> None:
    """Oracle: compose same-object loop footprints with checked lifecycle methods."""
    loops = identity["caller_loops"]
    lifecycle = setup["input_lifecycle"]
    constructor = setup["streams"]["constructor"]
    if (
        constructor["entry"] + constructor["byte_count"]
        != loops["constructor_tail_entry"]
        or loops["constructor_cleanup_bytes"] != 8
    ):
        raise ValueError("caller loop constructor does not join checked setup prefix")
    for call in loops["calls"]:
        if call["role"] in {"input_open", "close"}:
            name = "input_entry" if call["role"] == "input_open" else "close"
            cleanup = lifecycle[
                "open_cleanup_bytes" if name == "input_entry" else "close_cleanup_bytes"
            ]
            if (
                call["target"] != lifecycle["streams"][name]["entry"]
                or call["cleanup_bytes"] != cleanup
            ):
                raise ValueError("caller loop does not match checked lifecycle call")
    methods = identity["input_open_evidence"]["success_method_slots"]
    if (
        methods["0x18"] != "0x0000:0000"
        or not lifecycle["input_handler_method_slots_preserved"]
    ):
        raise ValueError("caller loop optional-method exclusion is not established")
    loops["slot_continuity"] = "conditional_on_normal_zero_status_and_nonaliasing"
    loops["input_method_slots"] = methods
    loops["optional_slot_0x18_call"] = "excluded_by_zero_segment_guard_on_input_path"
    loops["post_close_mode"] = "0xd7b0"
    identity["method_slot_preservation"] = "conditional_for_post_gate_caller"
    identity["assumptions"][2] = (
        "Constructor cleanup and both input-open/close wrappers are byte-checked."
    )
    identity["assumptions"] = list(
        dict.fromkeys(
            [
                *identity["assumptions"],
                *setup["assumptions"],
                *lifecycle["assumptions"],
                *loops["assumptions"],
            ]
        )
    )
    identity["remaining_obligations"] = list(loops["remaining_obligations"])
