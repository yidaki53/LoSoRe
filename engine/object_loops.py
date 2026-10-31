"""Restricted static oracle for Liero's post-gate file-reading caller loops."""

from __future__ import annotations

import pathlib

from engine.alternate_streams import _mz_relocation_locations
from engine.callbacks import (
    _DISPATCH_PREFIX,
    _DISPATCH_SIZES,
    _DISPATCH_SUFFIX,
    _bound_region,
    _decode_callbacks,
    _export,
    _return_values,
)


def _dispatcher_template() -> str:
    """Oracle: reuse the existing reviewed dispatcher instruction partition."""
    data = _DISPATCH_PREFIX + bytes.fromhex("e83301") + _DISPATCH_SUFFIX
    tokens = []
    cursor = 0
    for size in _DISPATCH_SIZES:
        tokens.append(data[cursor : cursor + size].hex())
        cursor += size
    if cursor != len(data):
        raise ValueError("reviewed dispatcher partition disagrees")
    return " ".join(tokens)


_LOOP_STREAMS = {
    "caller_tail": (
        0xA879,
        """
        ff46fe 80befcfd00 75d8 837efeff 7e5a 8dbefcfe 16 57
        9ab736dd14 9af404dd14 ff76fe 9a5446dd14 8986fafd 31c0
        3b86fafd 7f36 8946fc eb03 ff46fc 8dbefcfe 16 57 8a4604
        30e4 6bf815 81c7ec66 1e 57 6a14 9a8839dd14 9af038dd14
        9af404dd14 8b46fc 3b86fafd 75cf 8dbefcfe 16 57
        9a1137dd14 9af404dd14 c9 c20200
    """,
    ),
    "constructor_tail": (
        0x366D,
        """
        b94f00 0bd2 7509 ac 3ac8 7604 8ac8 e308 ac 0ac0 7403 aa e2f8
        32c0 aa 1f ca0800
    """,
    ),
    "random": (
        0x4654,
        """
        e85a00 8bdc 8bca 36f76704 8bc1 8bca 36f76704 03c1 83d200
        8bc2 ca0200
    """,
    ),
    "random_core": (
        0x46B1,
        """
        a11264 8b1e1464 8bc8 2ef726e746 d1e1 d1e1 d1e1 02e9
        03d1 03d3 d1e3 d1e3 03d3 02f3 b105 d3e3 02f3 050100
        83d200 a31264 89161464 c3
    """,
    ),
    "refill": (0x396C, "06 53 26ff5f14 0bc0 7403 a31064 c3"),
    "optional_method": (0x397A, "06 53 26ff5f18 0bc0 7403 a31064 c3"),
    "dispatcher": (0x37EC, _dispatcher_template()),
    "callback_skip": (
        0x390E,
        """
        ac 3c0d 740c 3c1a 7411 3bf3 75f3 b80e39 c3 3bf3 7409
        ac 3c0a 7401 4e 33c0 c3 b82339 c3
    """,
    ),
    "callback_read": (
        0x39AB,
        """
        ac 3c0d 740f 3c1a 740b aa 3bf3 e0f2 e305 b8ab39 c3 4e 33c0 c3
    """,
    ),
}


def _streams(regions: dict, binary: bytes, header: int, load_segment: int) -> dict:
    """Oracle: fixed-entry exact bytes, all instructions partitioned and file-backed."""
    if not isinstance(regions, dict) or set(regions) != set(_LOOP_STREAMS):
        raise ValueError("caller loops require all reviewed regions")
    streams = {}
    for name, (entry, template) in _LOOP_STREAMS.items():
        address, data = _bound_region(regions[name], binary, header, load_segment * 16)
        segment = (
            load_segment if name == "caller_tail" else (load_segment + 0x14DD) & 0xFFFF
        )
        tokens = [bytes.fromhex(raw) for raw in template.split()]
        if address != segment * 16 + entry or data != b"".join(tokens):
            raise ValueError(f"caller loops disagree with reviewed {name} bytes")
        instructions = {}
        cursor = address
        for raw in tokens:
            instructions[cursor] = raw
            cursor += len(raw)
        if cursor > segment * 16 + 0x10000:
            raise ValueError("caller loop region crosses code segment")
        streams[name] = instructions
    return streams


def _relocations(
    streams: dict, binary: bytes, header: int, load_segment: int
) -> list[int]:
    """Oracle: exact far-call fixups, no other loader rewrites of checked code."""
    occupied = set()
    expected = []
    for instructions in streams.values():
        for address, raw in instructions.items():
            offset = header + address - load_segment * 16
            occupied.update(range(offset, offset + len(raw)))
            if raw[0] == 0x9A:
                expected.append(offset + 3)
    locations = _mz_relocation_locations(binary, header)
    overlaps = {
        location
        for location in locations
        if location in occupied or location + 1 in occupied
    }
    if overlaps != set(expected):
        raise ValueError("caller loop relocations disagree")
    table = int.from_bytes(binary[0x18:0x1A], "little")
    count = int.from_bytes(binary[6:8], "little")
    entries = [
        header
        + int.from_bytes(binary[i : i + 2], "little")
        + 16 * int.from_bytes(binary[i + 2 : i + 4], "little")
        for i in range(table, table + count * 4, 4)
    ]
    if any(entries.count(location) != 1 for location in expected):
        raise ValueError("caller loop relocation must occur exactly once")
    return expected


def _branches(streams: dict) -> list[dict]:
    """Oracle: every direct branch/near call reaches a reviewed instruction boundary."""
    boundaries = {site for instructions in streams.values() for site in instructions}
    backedges = []
    for name, instructions in streams.items():
        for address, raw in instructions.items():
            is_reviewed_near_jump = name == "caller_prefix" and raw[0] == 0xE9
            if (
                raw[0]
                in {
                    0x74,
                    0x75,
                    0x76,
                    0x7E,
                    0x7F,
                    0xEB,
                    0xE0,
                    0xE2,
                    0xE3,
                    0xE8,
                }
                or is_reviewed_near_jump
            ):
                target = (
                    address + len(raw) + int.from_bytes(raw[1:], "little", signed=True)
                )
                if target not in boundaries:
                    raise ValueError("caller loop edge misses a reviewed boundary")
                if name == "caller" and target < address:
                    backedges.append({"address": address, "target": target})
    return backedges


def _call(raw: bytes, stack: tuple[str, ...], address: int, segment: int) -> dict:
    """Oracle: exact Pascal far-call argument shapes at every caller site."""
    offset = int.from_bytes(raw[1:3], "little")
    if int.from_bytes(raw[3:5], "little") != 0x14DD:
        raise ValueError("caller loop far-call segment disagrees")
    expected = {
        0x3639: (("SS", "BP-0x104", "CS", "0xa80c"), 8, "constructor"),
        0x36B7: (("SS", "BP-0x104"), 4, "input_open"),
        0x3711: (("SS", "BP-0x104"), 4, "close"),
        0x4654: (("BP-0x2:value",), 2, "random"),
        0x38F0: (("SS", "BP-0x104"), 4, "skip"),
        0x04F4: ((), 0, "error_check"),
    }
    if offset == 0x3988:
        allowed = {
            ("SS", "BP-0x104", "SS", "BP-0x204", "255"),
            ("SS", "BP-0x104", "DS", "global_destination", "20"),
        }
        cleanup, role = 6, "reader"
        if stack not in allowed:
            raise ValueError("caller loop reader arguments disagree")
    elif offset in expected:
        arguments, cleanup, role = expected[offset]
        if stack != arguments:
            raise ValueError(f"caller loop {role} arguments disagree")
    else:
        raise ValueError("caller loop has an unmodeled call")
    return {
        "address": address,
        "role": role,
        "target": segment * 16 + offset,
        "cleanup_bytes": cleanup,
        "argument_words_before": list(stack),
    }


def _stack_flow(instructions: dict, segment: int) -> tuple[list[dict], int]:
    """Oracle: finite CFG worklist; both conditional edges and loop fixed points."""
    pending = [(min(instructions), (), "unknown")]
    seen = set()
    calls = {}
    returns = set()
    while pending:
        state = pending.pop()
        if state in seen:
            continue
        seen.add(state)
        address, stack, di = state
        raw = instructions[address]
        successor = address + len(raw)
        if raw[:2] == b"\x8d\xbe":
            di = f"BP-0x{-int.from_bytes(raw[2:], 'little', signed=True):x}"
        elif raw[0] == 0xBF:
            di = f"0x{int.from_bytes(raw[1:], 'little'):x}"
        elif raw == b"\x6b\xf8\x15":
            di = "scaled_input_byte"
        elif raw == b"\x81\xc7\xec\x66":
            if di != "scaled_input_byte":
                raise ValueError("caller global destination expression disagrees")
            di = "global_destination"
        elif raw[0] in {0x16, 0x0E, 0x1E, 0x57, 0x68, 0x6A}:
            word = {
                0x16: "SS",
                0x0E: "CS",
                0x1E: "DS",
                0x57: di,
                0x68: str(int.from_bytes(raw[1:], "little")),
                0x6A: str(int.from_bytes(raw[1:], "little", signed=True)),
            }[raw[0]]
            stack = (*stack, word)
        elif raw == b"\xff\x76\xfe":
            stack = (*stack, "BP-0x2:value")
        elif raw[0] == 0x9A:
            call = _call(raw, stack, address, segment)
            if address in calls and calls[address] != call:
                raise ValueError("caller loop call has path-dependent arguments")
            calls[address] = call
            cleanup = call["cleanup_bytes"] // 2
            if cleanup:
                stack = stack[:-cleanup]
            di = "unknown"
        elif raw[0] in {0x74, 0x75, 0x7E, 0x7F, 0xEB}:
            target = successor + int.from_bytes(raw[1:], "little", signed=True)
            pending.append((target, stack, di))
            if raw[0] == 0xEB:
                continue
        elif raw[0] == 0xC2:
            if stack:
                raise ValueError("caller loop argument stack is not balanced")
            returns.add(address)
            continue
        # All other instructions are fixed by the reviewed template: local
        # counters/comparisons, byte-index arithmetic and the frame epilogue.
        if successor not in instructions:
            raise ValueError("caller loop falls outside reviewed instructions")
        pending.append((successor, stack, di))
    if not returns:
        raise ValueError("caller loop has no modeled return")
    return [calls[site] for site in sorted(calls)], len(seen)


def _local_stores(caller: dict) -> list[int]:
    """Oracle: explicit word stores/increments in the exact reviewed caller."""
    offsets = set()
    for raw in caller.values():
        if raw[:2] in {b"\xc7\x46", b"\xff\x46", b"\x89\x46"}:
            offsets.add(int.from_bytes(raw[2:3], "little", signed=True))
        elif raw[:2] == b"\x89\x86":
            offsets.add(int.from_bytes(raw[2:4], "little", signed=True))
    return sorted(offsets)


def _random_stores(instructions: dict) -> list[str]:
    """Oracle: direct DS-relative stores in the checked PRNG core."""
    stores = []
    for raw in instructions.values():
        if raw[0] == 0xA3:
            stores.append(int.from_bytes(raw[1:], "little"))
        elif raw[:2] == b"\x89\x16":
            stores.append(int.from_bytes(raw[2:], "little"))
    return [f"DS:0x{offset:x}/2" for offset in stores]


def verify_caller_loops(
    regions: dict,
    root: pathlib.Path,
    binary: bytes,
    header: int,
    load_segment: int,
    base_streams: dict,
    caller_function: str,
) -> dict:
    """Oracle: conditional post-gate caller identity and reviewed callee write footprint."""
    streams = _streams(regions, binary, header, load_segment)
    caller = {**base_streams["caller"], **streams.pop("caller_tail")}
    if min(caller) != load_segment * 16 + 0xA836:
        raise ValueError("caller loop prefix is not at the reviewed entry")
    streams["caller"] = caller
    parsed = _export(root, caller_function)
    start = parsed["addrs"].index(min(caller))
    if parsed["addrs"][start : start + len(caller)] != list(caller):
        raise ValueError("caller loop exported instruction boundaries disagree")
    if set(parsed["segments"][start : start + len(caller)]) != {load_segment}:
        raise ValueError("caller loop exported segment disagrees")
    all_streams = {**base_streams, **streams}
    relocations = _relocations(all_streams, binary, header, load_segment)
    backedges = _branches(all_streams)
    segment = (load_segment + 0x14DD) & 0xFFFF
    calls, state_count = _stack_flow(caller, segment)
    local_offsets = _local_stores(caller)
    if any(offset <= -5 and offset + 1 >= -0x104 for offset in local_offsets):
        raise ValueError("caller direct store overlaps the file object")
    callback_targets = set()
    for name in ("callback_skip", "callback_read"):
        instructions = streams[name]
        start = min(instructions)
        decoded = _decode_callbacks(b"".join(instructions.values()), start, segment)
        pending = [start]
        while pending:
            target = pending.pop()
            if target in callback_targets:
                continue
            callback_targets.add(target)
            for value in _return_values(decoded, target):
                if value:
                    pending.append(segment * 16 + value)
    return {
        "entry": min(caller),
        "end": max(caller) + len(caller[max(caller)]),
        "analysis": "conditional_static_caller_loop_continuity",
        "slot_continuity": "unlinked_callee_summaries",
        "streams": {
            name: {
                "entry": min(instructions),
                "byte_count": sum(map(len, instructions.values())),
                "instruction_count": len(instructions),
            }
            for name, instructions in streams.items()
        },
        "calls": calls,
        "object_calls": [
            call["address"]
            for call in calls
            if call["role"] not in {"random", "error_check"}
        ],
        "backedges": backedges,
        "cfg_states_checked": state_count,
        "stack_balanced_at_return": True,
        "relocation_file_offsets": relocations,
        "direct_local_store_offsets": local_offsets,
        "random_helper_writes": _random_stores(streams["random_core"]),
        "callback_targets": sorted(callback_targets),
        "callback_write_kind": "ES:DI byte stores only",
        "constructor_cleanup_bytes": int.from_bytes(
            list(streams["constructor_tail"].values())[-1][1:], "little"
        ),
        "constructor_tail_entry": min(streams["constructor_tail"]),
        "local_destination_bp_range": [-0x204, -0x105],
        "global_destination_offset_range": [0x66EC, 0x66EC + 255 * 21 + 20],
        "object_bp_range": [-0x104, -5],
        "resolves_call_sites": False,
        "assumptions": [
            "Execution reaches 1000:A836 with an allocated, nonwrapping BP/SS frame.",
            "Calls and DOS return normally, preserving BP, SS, DS and live stack arguments.",
            "Both input opens succeed and the checked status helper returns on zero status.",
            "Checked setup/input/close methods are unchanged; external writes do not alias slots or stack.",
            "DS status, PRNG words and global destination do not physically alias SS object or live stack.",
            "Constructor filename writes remain inside the object and do not wrap.",
            "Read buffers and callback destinations are valid and do not wrap or overwrite live arguments.",
        ],
        "remaining_obligations": [
            "Establish physical DS/SS non-aliasing and valid buffer/count invariants at runtime.",
            "Validate the pre-gate frame-allocation and existence-check callees before claiming whole-function coverage.",
            "Observe actual DOS behavior; no termination, input validity or original-binary parity is proved.",
        ],
    }
