"""Bounded static AX callback closure; not an indirect-call resolution oracle."""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass

from engine.alternate_streams import (
    _bytes,
    _hex,
    load_binary_evidence,
    load_verified_streams,
)
from tools.asmcfg import is_branch, is_call, parse_ghidra_asm, resolve_branch_target


@dataclass(frozen=True)
class CallbackInstruction:
    """Oracle: restricted 8086 byte decoder, with conservative branch semantics."""

    size: int
    operation: str
    operand: int = 0


def _decode_callbacks(
    data: bytes, start: int, segment: int
) -> dict[int, CallbackInstruction]:
    """Oracle: fail-closed decoder for the reviewed, stack-neutral callbacks."""
    instructions = {}
    cursor = 0
    while cursor < len(data):
        address = start + cursor
        opcode = data[cursor]
        if opcode in {0xAC, 0xAA, 0x4E, 0xC3}:
            operation = {0xAC: "load_al", 0xAA: "keep", 0x4E: "keep", 0xC3: "ret"}
            item = CallbackInstruction(1, operation[opcode])
        elif opcode == 0xB8 and cursor + 3 <= len(data):
            item = CallbackInstruction(
                3, "set_ax", int.from_bytes(data[cursor + 1 : cursor + 3], "little")
            )
        elif data[cursor : cursor + 2] == b"\x33\xc0":
            item = CallbackInstruction(2, "set_ax", 0)
        elif data[cursor : cursor + 2] == b"\x3b\xf3" or (
            opcode == 0x3C and cursor + 2 <= len(data)
        ):
            item = CallbackInstruction(2, "keep")
        elif opcode in {0x74, 0x75, 0x76, 0x77, 0xE0, 0xE3} and cursor + 2 <= len(data):
            displacement = int.from_bytes(data[cursor + 1 : cursor + 2], signed=True)
            target = segment * 16 + (
                (address - segment * 16 + 2 + displacement) & 0xFFFF
            )
            item = CallbackInstruction(2, "branch", target)
        else:
            raise ValueError(f"unsupported callback encoding at 0x{address:x}")
        instructions[address] = item
        cursor += item.size
    for address, item in instructions.items():
        successors = [] if item.operation == "ret" else [address + item.size]
        if item.operation == "branch":
            successors.append(item.operand)
        if any(successor not in instructions for successor in successors):
            raise ValueError(f"callback successor is not a boundary at 0x{address:x}")
    return instructions


def _return_values(
    instructions: dict[int, CallbackInstruction], entry: int
) -> set[int]:
    """Oracle: finite AX dataflow, unknown AL loads and both branch outcomes."""
    pending: list[tuple[int, int | None]] = [(entry, None)]
    seen = set()
    returns = set()
    while pending:
        address, ax = pending.pop()
        if (address, ax) in seen:
            continue
        seen.add((address, ax))
        item = instructions[address]
        if item.operation == "ret":
            if ax is None:
                raise ValueError(f"callback returns unknown AX at 0x{address:x}")
            returns.add(ax)
            continue
        if item.operation == "load_al":
            ax = None
        elif item.operation == "set_ax":
            ax = item.operand
        if item.operation == "branch":
            pending.append((item.operand, ax))
        pending.append((address + item.size, ax))
    if not returns:
        raise ValueError(f"callback has no modeled return at 0x{entry:x}")
    return returns


def _bound_region(
    region: dict, binary: bytes, header: int, image_start: int
) -> tuple[int, bytes]:
    """Oracle: exact bytes at a mapped, file-backed region."""
    if not isinstance(region, dict):
        raise TypeError("callback region must be an object")
    address = _hex(region.get("address"), "callback.address")
    data = _bytes(region.get("bytes_hex"), "callback.bytes_hex")
    offset = header + address - image_start
    if offset < header or binary[offset : offset + len(data)] != data:
        raise ValueError(f"callback bytes do not match at 0x{address:x}")
    return address, data


def _export(target_root: pathlib.Path, name: object) -> dict:
    """Oracle: exact named assembly export, without path traversal."""
    if (
        not isinstance(name, str)
        or not name.startswith("FUN_")
        or not all(
            character.isascii() and (character.isalnum() or character == "_")
            for character in name
        )
    ):
        raise ValueError("callback function must name an assembly export")
    return parse_ghidra_asm((target_root / "asm" / f"{name}.s").read_text())


# This exact dispatcher shape saves AX below five other saved registers, calls
# the refill routine, then restores the six words in reverse order.
_DISPATCH_PREFIX = bytes.fromhex(
    "833e106400753526817f02b1d7752e268b7708263b770a742b"
    "1e06535226c5570c268b5f0a0703da03f2fcffd0"
    "2bf28cc25b071f268977080bc07508c3c70610646800c3"
    "505152570653"
)
_DISPATCH_SUFFIX = bytes.fromhex("5b075f5a5958268b7708263b770a75bcc3")
_DISPATCH_SIZES = (
    5,
    2,
    6,
    2,
    4,
    4,
    2,
    1,
    1,
    1,
    1,
    4,
    4,
    1,
    2,
    2,
    1,
    2,
    2,
    2,
    1,
    1,
    1,
    4,
    2,
    2,
    1,
    6,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    3,
    1,
    1,
    1,
    1,
    1,
    1,
    4,
    4,
    2,
    1,
)


def _dispatcher(
    protocol: dict,
    target_root: pathlib.Path,
    binary: bytes,
    header: int,
    image_start: int,
    segment: int,
) -> dict:
    """Oracle: reviewed Liero dispatcher bytes and exported instruction boundaries."""
    region = protocol.get("dispatcher")
    address, data = _bound_region(region, binary, header, image_start)
    call_offset = len(_DISPATCH_PREFIX)
    if (
        len(data) != call_offset + 3 + len(_DISPATCH_SUFFIX)
        or data[:call_offset] != _DISPATCH_PREFIX
        or data[call_offset] != 0xE8
        or data[call_offset + 3 :] != _DISPATCH_SUFFIX
    ):
        raise ValueError("unsupported callback dispatcher shape")
    refill = segment * 16 + (
        (
            address
            - segment * 16
            + call_offset
            + 3
            + int.from_bytes(
                data[call_offset + 1 : call_offset + 3], "little", signed=True
            )
        )
        & 0xFFFF
    )
    if refill != _hex(region.get("refill_target"), "callback.refill_target"):
        raise ValueError("callback refill target disagrees with encoded call")
    parsed = _export(target_root, region.get("function"))
    boundaries = []
    cursor = address
    for size in _DISPATCH_SIZES:
        boundaries.append(cursor)
        cursor += size
    if cursor != address + len(data) or parsed["addrs"] != boundaries:
        raise ValueError("callback dispatcher assembly boundaries disagree")
    if set(parsed["segments"]) != {segment} or not (
        0 <= address - segment * 16 <= 0xFFFF - len(data) + 1
    ):
        raise ValueError("callback dispatcher code segment disagrees")
    call_site = address + 43
    refill_site = address + call_offset
    if (
        parsed["insts"][boundaries.index(call_site)].upper() != "CALL AX"
        or resolve_branch_target(
            parsed["insts"][boundaries.index(refill_site)], segment
        )
        != refill
    ):
        raise ValueError("callback dispatcher assembly calls disagree")
    return {
        "entry": address,
        "call_site": call_site,
        "refill_call_site": refill_site,
        "refill_target": refill,
        "ax_preserved_across_refill": True,
    }


def _seed_target(
    seed: dict,
    target_root: pathlib.Path,
    binary: bytes,
    header: int,
    image_start: int,
    segment: int,
    dispatcher: int,
) -> tuple[int, int]:
    """Oracle: MOV AX,imm16 followed only by reviewed AX-preserving seed bytes."""
    address, data = _bound_region(seed, binary, header, image_start)
    if not (0 <= address - segment * 16 <= 0x10000 - len(data)):
        raise ValueError("callback seed is outside code segment")
    if len(data) < 6 or data[0] != 0xB8 or data[-3] != 0xE8:
        raise ValueError("callback seed requires MOV AX followed by a near call")
    preserving = (
        b"\x33\xd2",
        b"\x8b\x4e",
        b"\x8b\x7e",
        b"\x8b\x56",
        b"\xb9",
        b"\x8d\x7e",
        b"\x8c\xd2",
        b"\x47",
    )
    sizes = (2, 3, 3, 3, 3, 3, 2, 1)
    cursor = 3
    boundaries = [address]
    while cursor < len(data) - 3:
        size = next(
            (
                size
                for prefix, size in zip(preserving, sizes, strict=True)
                if data[cursor:].startswith(prefix)
            ),
            None,
        )
        if size is None or cursor + size > len(data) - 3:
            raise ValueError("unsupported AX-preserving callback seed instruction")
        boundaries.append(address + cursor)
        cursor += size
    call_site = address + cursor
    boundaries.append(call_site)
    target = segment * 16 + (
        (
            call_site
            - segment * 16
            + 3
            + int.from_bytes(data[-2:], "little", signed=True)
        )
        & 0xFFFF
    )
    if target != dispatcher:
        raise ValueError("callback seed call does not target dispatcher")
    parsed = _export(target_root, seed.get("function"))
    if address not in parsed["addrs"]:
        raise ValueError("callback seed initializer is not exported")
    start = parsed["addrs"].index(address)
    end = start + len(boundaries)
    if (
        parsed["addrs"][start:end] != boundaries
        or set(parsed["segments"][start:end]) != {segment}
        or resolve_branch_target(parsed["insts"][end - 1], segment) != dispatcher
    ):
        raise ValueError("callback seed assembly path disagrees")
    return segment * 16 + int.from_bytes(data[1:3], "little"), call_site


def _known_entry_calls(target_root: pathlib.Path, entry: int) -> set[int]:
    """Oracle: direct calls to the dispatcher in the exported assembly inventory."""
    calls = set()
    for path in (target_root / "asm").glob("*.s"):
        parsed = parse_ghidra_asm(path.read_text())
        for address, segment, instruction in zip(
            parsed["addrs"], parsed["segments"], parsed["insts"], strict=True
        ):
            if (
                is_call(instruction)
                and resolve_branch_target(instruction, segment) == entry
            ):
                calls.add(address)
    return calls


def _check_initialization_bypasses(
    protocol: dict, target_root: pathlib.Path, seed_calls: set[int]
) -> dict:
    """Oracle: exported and verified-stream entry/transfer inventory, not runtime."""
    regions = [protocol["dispatcher"], *protocol["seeds"]]
    protected = [
        (
            _hex(region["address"], "callback.address"),
            _hex(region["address"], "callback.address")
            + len(_bytes(region["bytes_hex"], "callback.bytes_hex")),
            region["function"],
        )
        for region in regions
    ]
    dispatcher_entry = protected[0][0]
    transfers = []
    exports = list((target_root / "asm").glob("*.s"))
    for path in exports:
        parsed = parse_ghidra_asm(path.read_text())
        for address, segment, instruction in zip(
            parsed["addrs"], parsed["segments"], parsed["insts"], strict=True
        ):
            for start, end, owner in protected:
                if start <= address < end and path.stem != owner:
                    raise ValueError("another export bypasses callback initialization")
            if is_branch(instruction) or is_call(instruction):
                transfers.append(
                    (address, resolve_branch_target(instruction, segment), path.stem)
                )
    verified_streams = load_verified_streams(target_root)
    if verified_streams:
        manifest = json.loads((target_root / "alternate_streams.json").read_text())
        for stream in manifest["streams"]:
            if stream.get("status") != "verified":
                continue
            segment = (
                _hex(stream["code_segment"], "code_segment")
                if stream.get("code_segment") is not None
                else None
            )
            groups = [stream["instructions"]] + [
                entry["instructions"] for entry in stream.get("overlapping_entries", [])
            ]
            for entry in (entry for group in groups for entry in group):
                address = _hex(entry["address"], "instruction.address")
                if any(start <= address < end for start, end, _ in protected):
                    raise ValueError(
                        "alternate stream bypasses callback initialization"
                    )
                instruction = entry["text"].strip().upper()
                if is_branch(instruction) or is_call(instruction):
                    transfers.append(
                        (address, resolve_branch_target(instruction, segment), None)
                    )
            for edge in stream["source_edges"] + stream.get("outgoing_calls", []):
                transfers.append(
                    (
                        _hex(edge["address"], "source_edge.address"),
                        _hex(edge["target_address"], "source_edge.target_address"),
                        None,
                    )
                )
    for source, target, owner in transfers:
        if target is None:
            continue
        for start, end, expected_owner in protected:
            if not start <= target < end:
                continue
            if target == start:
                if start != dispatcher_entry or source in seed_calls:
                    continue
            elif start <= source < end and owner == expected_owner:
                continue
            raise ValueError("known transfer bypasses callback initialization")
    return {
        "status": "passed",
        "assembly_exports_checked": len(exports),
        "verified_streams_checked": len(verified_streams),
        "scope": "known instruction entries and recorded transfers only",
    }


def _validate_protocol(
    protocol: dict,
    target_root: pathlib.Path,
    binary: bytes,
    header: int,
    load_segment: int,
) -> dict:
    """Oracle: local callback closure under explicitly conditional refill semantics."""
    if not isinstance(protocol, dict) or protocol.get("kind") != "liero_buffered_ax_v1":
        raise ValueError("unsupported callback protocol")
    segment = _hex(protocol.get("code_segment"), "callback.code_segment")
    if segment > 0xFFFF:
        raise ValueError("callback code segment must fit in 16 bits")
    image_start = load_segment * 16
    dispatcher = _dispatcher(
        protocol, target_root, binary, header, image_start, segment
    )
    regions = protocol.get("callbacks")
    seeds = protocol.get("seeds")
    if not isinstance(regions, list) or not regions:
        raise ValueError("callback protocol requires callback regions")
    if not isinstance(seeds, list) or not seeds:
        raise ValueError("callback protocol requires seed paths")
    families = {}
    occupied = set()
    for region in regions:
        address, data = _bound_region(region, binary, header, image_start)
        if not (0 <= address - segment * 16 <= 0x10000 - len(data)):
            raise ValueError("callback region is outside code segment")
        span = set(range(address, address + len(data)))
        if occupied & span:
            raise ValueError("callback regions overlap")
        occupied.update(span)
        instructions = _decode_callbacks(data, address, segment)
        for boundary in instructions:
            families[boundary] = instructions
    seed_paths = [
        _seed_target(
            seed, target_root, binary, header, image_start, segment, dispatcher["entry"]
        )
        for seed in seeds
    ]
    seed_calls = {site for _, site in seed_paths}
    if len(seed_calls) != len(seed_paths):
        raise ValueError("callback seed call sites must be unique")
    if seed_calls != _known_entry_calls(target_root, dispatcher["entry"]):
        raise ValueError("callback seeds do not cover exported dispatcher calls")
    bypass_check = _check_initialization_bypasses(protocol, target_root, seed_calls)
    initial = {target for target, _ in seed_paths}
    pending = list(initial)
    transitions = {}
    while pending:
        entry = pending.pop()
        if entry in transitions:
            continue
        if entry not in families:
            raise ValueError(f"callback target is not a decoded boundary: 0x{entry:x}")
        returned = _return_values(families[entry], entry)
        transitions[entry] = sorted(returned)
        pending.extend(segment * 16 + value for value in returned if value)
    return {
        **dispatcher,
        "kind": protocol["kind"],
        "initial_targets": sorted(initial),
        "exported_entry_call_sites": sorted(seed_calls),
        "known_entry_bypass_check": bypass_check,
        "candidate_targets": sorted(transitions),
        "returns_ax": {
            f"0x{entry:x}": values for entry, values in sorted(transitions.items())
        },
        "analysis": "conservative_static_overapproximation",
        "resolves_call_site": False,
        "assumptions": [
            "Execution starts on one of the recorded MOV AX seed paths.",
            "Callbacks execute immutable code with valid buffers and a valid stack.",
            "Buffer writes do not alias code or live stack words.",
            "Refill returns normally without changing saved stack words or code.",
        ],
        "remaining_obligations": [
            "Exclude entries outside the exported and verified-stream inventory.",
            "Account for the object-relative far calls made by the refill routine.",
        ],
    }


def load_verified_callbacks(target_root: pathlib.Path) -> list[dict]:
    """Oracle: hash-bound local AX protocol evidence, never recovery attestation."""
    manifest_path = target_root / "alternate_streams.json"
    if not manifest_path.is_file():
        return []
    manifest = json.loads(manifest_path.read_text())
    protocols = (
        manifest.get("callback_protocols", []) if isinstance(manifest, dict) else None
    )
    if not isinstance(protocols, list):
        raise TypeError("callback_protocols must be an array")
    if not protocols:
        return []
    binary, header, load_segment, binary_hash = load_binary_evidence(
        target_root, manifest
    )
    return [
        {
            **_validate_protocol(protocol, target_root, binary, header, load_segment),
            "binary_sha256": binary_hash,
        }
        for protocol in protocols
    ]


def load_verified_indirect_operands(target_root: pathlib.Path) -> list[dict]:
    """Oracle: restricted far-memory call byte decode; not a target-value proof."""
    manifest_path = target_root / "alternate_streams.json"
    if not manifest_path.is_file():
        return []
    manifest = json.loads(manifest_path.read_text())
    entries = (
        manifest.get("indirect_operands", []) if isinstance(manifest, dict) else None
    )
    if not isinstance(entries, list):
        raise TypeError("indirect_operands must be an array")
    if not entries:
        return []
    binary, header, load_segment, binary_hash = load_binary_evidence(
        target_root, manifest
    )
    records = []
    seen = set()
    for entry in entries:
        address, raw = _bound_region(entry, binary, header, load_segment * 16)
        if address in seen:
            raise ValueError("indirect operand addresses must be unique")
        seen.add(address)
        segment = "DS"
        if raw[0] in {0x26, 0x36}:
            segment = {0x26: "ES", 0x36: "SS"}[raw[0]]
            raw = raw[1:]
        operands = {
            b"\xff\x19": "[BX+DI]",
            b"\xff\x5f\x14": "[BX+0X14]",
            b"\xff\x5f\x18": "[BX+0X18]",
        }
        if raw not in operands:
            raise ValueError("unsupported indirect far-call operand encoding")
        operand = operands[raw]
        instruction = f"CALLF {segment}:{operand}"
        parsed = _export(target_root, entry.get("function"))
        matches = [
            text.replace(" ", "")
            for site, text in zip(parsed["addrs"], parsed["insts"], strict=True)
            if site == address
        ]
        accepted = {instruction.replace(" ", "")}
        if segment == "DS":
            accepted.add(f"CALLF{operand}")
        if len(matches) != 1 or matches[0] not in accepted:
            raise ValueError("indirect operand disagrees with assembly")
        records.append(
            {
                "address": address,
                "instruction": instruction,
                "pointer_segment_register": segment,
                "pointer_operand": operand,
                "binary_sha256": binary_hash,
                "resolves_call_site": False,
            }
        )
    return records
