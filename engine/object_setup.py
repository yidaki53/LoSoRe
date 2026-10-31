"""Restricted static oracle for Liero file-object setup, not runtime parity."""

from __future__ import annotations

import json
import pathlib

from engine.alternate_streams import (
    _bytes,
    _hex,
    _mz_relocation_locations,
    load_binary_evidence,
)
from engine.object_lifecycle import verify_input_lifecycle

# Each token is one independently reviewed 8086 instruction, including prefixes.
# Exact templates deliberately reject variants whose effects have not been reviewed.
_REVIEWED_STREAMS = {
    "constructor": """
        33d2 8bdc 1e 36c47f08 36c57704 fc 33c0 ab b8b0d7 ab b88000 ab
        33c0 ab ab ab 8d4574 ab 8cc0 ab b80c42 ab b8dd14 ab
        33c0 b90e00 f3ab
    """,
    "setup": """
        8bdc 1e 36c57f04 33c9 890d b8003d 817d02b1d7 740d b002 ff05
        817d02b3d7 7402 b43c 807d3000 7409 8d5530 cd21 725a 8905
        b85e37 badd14 33c9 33db 817d02b1d7 742f 8b1d b80044 cd21
        f6c280 b8b337 badd14 8bc8 8bda 7514 817d02b3d7 7503 e82b00
        b88e37 badd14 33c9 33db c74502b2d7 894514 895516 894d18
        895d1a c7451cd337 c7451edd14 33c0 1f ca0400
    """,
    "helper": """
        33d2 33c9 8b1d b80242 cd21 2d8000 83da00 7304 33c0 33d2
        8bca 8bd0 8b1d b80042 cd21 8d958000 b98000 8b1d b43f cd21
        7302 33c0 33db 3bd8 7420 80b980001a 7403 43 ebf2 8bd3 2bd0
        b9ffff 8b1d b80242 cd21 33c9 8b1d b440 cd21 c3
    """,
}


def _stream(
    region: dict, name: str, binary: bytes, header: int, image_start: int
) -> dict:
    """Oracle: complete exact-template instruction partition and local successors."""
    if not isinstance(region, dict):
        raise TypeError("object setup region must be an object")
    address = _hex(region.get("address"), "object_setup.address")
    data = _bytes(region.get("bytes_hex"), "object_setup.bytes_hex")
    offset = header + address - image_start
    if offset < header or binary[offset : offset + len(data)] != data:
        raise ValueError(f"object setup bytes do not match at 0x{address:x}")
    tokens = [bytes.fromhex(token) for token in _REVIEWED_STREAMS[name].split()]
    if data != b"".join(tokens):
        raise ValueError(f"object setup does not match reviewed {name} stream")
    instructions = {}
    cursor = address
    for token in tokens:
        instructions[cursor] = token
        cursor += len(token)
    branches = []
    calls = []
    for site, raw in instructions.items():
        if raw[0] in {0x72, 0x73, 0x74, 0x75, 0xEB, 0xE8}:
            target = site + len(raw) + int.from_bytes(raw[1:], "little", signed=True)
            edge = {"address": site, "target": target}
            if raw[0] == 0xE8:
                calls.append(edge)
            else:
                if target not in instructions:
                    raise ValueError("object setup branch is not a local boundary")
                branches.append(edge)
        if (
            raw[0] not in {0xC3, 0xCA, 0xEB}
            and site + len(raw) not in instructions
            and name != "constructor"
        ):
            raise ValueError("object setup stream falls beyond its last instruction")
    return {
        "entry": address,
        "file_offset": offset,
        "byte_count": len(data),
        "instructions": instructions,
        "branches": branches,
        "near_calls": calls,
        "return_sites": [
            site for site, raw in instructions.items() if raw[0] in {0xC3, 0xCA}
        ],
        "dos_interrupt_sites": [
            site for site, raw in instructions.items() if raw == b"\xcd\x21"
        ],
        "scope": "constructor prefix" if name == "constructor" else "complete routine",
    }


def _relocations(streams: dict, binary: bytes, header: int, load_segment: int) -> list:
    """Oracle: every expected code-segment immediate has its exact MZ fixup."""
    locations = _mz_relocation_locations(binary, header)
    expected = []
    occupied = set()
    for stream in streams.values():
        for site, raw in stream["instructions"].items():
            offset = header + site - load_segment * 16
            occupied.update(range(offset, offset + len(raw)))
            if raw in {b"\xba\xdd\x14", b"\xb8\xdd\x14"}:
                expected.append(offset + 1)
            elif raw == b"\xc7\x45\x1e\xdd\x14":
                expected.append(offset + 3)
    overlapping_locations = {
        location
        for location in locations
        if location in occupied or location + 1 in occupied
    }
    if overlapping_locations - set(expected):
        raise ValueError("object setup has an unexpected MZ relocation")
    if not set(expected) <= locations:
        raise ValueError("object setup segment word lacks MZ relocation")
    table = int.from_bytes(binary[0x18:0x1A], "little")
    count = int.from_bytes(binary[6:8], "little")
    entries = [
        header
        + int.from_bytes(binary[index + 2 : index + 4], "little") * 16
        + int.from_bytes(binary[index : index + 2], "little")
        for index in range(table, table + count * 4, 4)
    ]
    if any(entries.count(offset) != 1 for offset in expected):
        raise ValueError("object setup segment relocation must occur once")
    return [
        {
            "file_offset": offset,
            "encoded_segment": 0x14DD,
            "loaded_segment": (0x14DD + load_segment) & 0xFFFF,
        }
        for offset in expected
    ]


def _setup_outcomes(stream: dict, mode: int, load_segment: int) -> list[dict]:
    """Oracle: finite local constant propagation; DOS/helper effects are conditional."""
    instructions = stream["instructions"]
    # AX, DX, CX, BX; slot words are tracked separately from all other object fields.
    pending = [(stream["entry"], (None,) * 4, None, ((2, mode),), False)]
    seen = set()
    outcomes = set()
    while pending:
        state = pending.pop()
        if state in seen:
            continue
        seen.add(state)
        site, registers, zero, stored, helper_called = state
        registers = list(registers)
        words = dict(stored)
        raw = instructions[site]
        opcode = raw[0]
        successor = site + len(raw)
        if opcode in {0xB8, 0xBA, 0xB9}:
            index = {0xB8: 0, 0xBA: 1, 0xB9: 2}[opcode]
            registers[index] = int.from_bytes(raw[1:], "little")
            if raw == b"\xba\xdd\x14":
                registers[index] = (registers[index] + load_segment) & 0xFFFF
        elif raw in {b"\x33\xc9", b"\x33\xdb", b"\x33\xc0"}:
            registers[{0xC9: 2, 0xDB: 3, 0xC0: 0}[raw[1]]] = 0
            zero = True
        elif raw[:3] == b"\x81\x7d\x02":
            zero = words[2] == int.from_bytes(raw[3:], "little")
        elif raw == b"\x8b\xc8":
            registers[2] = registers[0]
        elif raw == b"\x8b\xda":
            registers[3] = registers[1]
        elif raw == b"\x8b\x1d":
            registers[3] = None
        elif opcode in {0xB0, 0xB4}:
            ax = registers[0]
            registers[0] = (
                None
                if ax is None
                else (
                    (ax & 0xFF00) | raw[1]
                    if opcode == 0xB0
                    else (ax & 0x00FF) | (raw[1] << 8)
                )
            )
        elif raw in {b"\x80\x7d\x30\x00", b"\xf6\xc2\x80"}:
            zero = None
        elif raw == b"\xcd\x21" or opcode == 0xE8:
            registers = [None] * 4
            zero = None
            helper_called |= opcode == 0xE8
        elif opcode == 0x89 and raw[1] in {0x45, 0x55, 0x4D, 0x5D}:
            index = {0x45: 0, 0x55: 1, 0x4D: 2, 0x5D: 3}[raw[1]]
            words[raw[2]] = registers[index]
        elif raw[:3] in {b"\xc7\x45\x1c", b"\xc7\x45\x1e"}:
            value = int.from_bytes(raw[3:], "little")
            if raw[2] == 0x1E:
                value = (value + load_segment) & 0xFFFF
            words[raw[2]] = value
        elif raw == b"\xc7\x45\x02\xb2\xd7":
            words[2] = 0xD7B2
        elif opcode == 0xCA:
            if any(value is None for value in words.values()):
                raise ValueError("object setup returns an unknown method-slot value")
            outcomes.add((tuple(sorted(words.items())), helper_called))
            continue
        if opcode in {0x72, 0x74, 0x75}:
            taken = (
                None
                if opcode == 0x72 or zero is None
                else (zero if opcode == 0x74 else not zero)
            )
            target = successor + int.from_bytes(raw[1:], "little", signed=True)
            if taken is not False:
                pending.append(
                    (
                        target,
                        tuple(registers),
                        zero,
                        tuple(sorted(words.items())),
                        helper_called,
                    )
                )
            if taken is True:
                continue
        pending.append(
            (
                successor,
                tuple(registers),
                zero,
                tuple(sorted(words.items())),
                helper_called,
            )
        )
    result = []
    for stored, helper_called in sorted(outcomes):
        words = dict(stored)
        slots = {
            f"0x{offset:x}": f"0x{words[offset + 2]:04x}:{words[offset]:04x}"
            for offset in (0x14, 0x18, 0x1C)
            if offset in words
        }
        result.append(
            {
                "method_slots": slots,
                "helper_called": helper_called,
                "writes_methods": bool(slots),
                "resulting_mode": f"0x{words[2]:04x}",
            }
        )
    return result


def _protocol(record: dict, binary: bytes, header: int, load_segment: int) -> dict:
    """Oracle: exact reviewed code, local CFG and conditional method-slot outcomes."""
    if not isinstance(record, dict) or record.get("kind") != "liero_file_object_v1":
        raise ValueError("unsupported object setup protocol")
    regions = record.get("regions")
    if not isinstance(regions, dict) or set(regions) != set(_REVIEWED_STREAMS):
        raise ValueError("object setup requires constructor, setup and helper regions")
    if not all(isinstance(region, dict) for region in regions.values()):
        raise TypeError("object setup regions must be objects")
    spans = [
        (
            _hex(region.get("address"), "object_setup.address"),
            len(_bytes(region.get("bytes_hex"), "object_setup.bytes_hex")),
        )
        for region in regions.values()
    ]
    for index, (start, size) in enumerate(spans):
        if any(
            start < other + length and other < start + size
            for other, length in spans[:index]
        ):
            raise ValueError("object setup regions overlap")
    streams = {
        name: _stream(regions[name], name, binary, header, load_segment * 16)
        for name in _REVIEWED_STREAMS
    }
    runtime_segment = (0x14DD + load_segment) & 0xFFFF
    if streams["setup"]["entry"] != runtime_segment * 16 + 0x420C:
        raise ValueError("constructor pointer does not target setup entry")
    if any(
        not 0
        <= stream["entry"] - runtime_segment * 16
        <= 0x10000 - stream["byte_count"]
        for stream in streams.values()
    ):
        raise ValueError("object setup region is outside the relocated code segment")
    calls = streams["setup"]["near_calls"]
    if len(calls) != 1 or calls[0]["target"] != streams["helper"]["entry"]:
        raise ValueError("object setup call does not target helper")
    relocated = _relocations(streams, binary, header, load_segment)
    mode_outcomes = {
        f"0x{mode:x}": _setup_outcomes(streams["setup"], mode, load_segment)
        for mode in (0xD7B1, 0xD7B2, 0xD7B3)
    }
    protocol = {
        "kind": record["kind"],
        "streams": {
            name: {
                **{
                    key: value for key, value in stream.items() if key != "instructions"
                },
                "instructions": [
                    {"address": address, "bytes_hex": raw.hex()}
                    for address, raw in stream["instructions"].items()
                ],
            }
            for name, stream in streams.items()
        },
        "relocated_segment_words": relocated,
        "constructor_method_slots": {
            "0x10": f"0x{runtime_segment:04x}:420c",
            "0x14": "0x0000:0000",
            "0x18": "0x0000:0000",
            "0x1c": "0x0000:0000",
        },
        "mode_outcomes": mode_outcomes,
        "analysis": "conditional_static_overapproximation",
        "resolves_call_sites": False,
        "assumptions": [
            "Execution starts at the setup entry with a valid far object argument.",
            "DOS interrupts return normally and preserve DS, DI, and a valid stack.",
            "DOS/helper buffer writes do not alias method slots, stack or code.",
            "Code is immutable after normal MZ relocation.",
        ],
        "remaining_obligations": [
            "Prove runtime object identity and reachability of these entry paths.",
            "Prove caller mode transitions, later slot writes and indirect target coverage.",
            "Validate DOS/helper behavior against the original binary.",
        ],
    }
    if "input_lifecycle_regions" in record:
        protocol["input_lifecycle"] = verify_input_lifecycle(
            record["input_lifecycle_regions"], binary, header, load_segment, protocol
        )
    return protocol


def load_verified_object_setups(target_root: pathlib.Path) -> list[dict]:
    """Oracle: optional hash-bound setup evidence; never a source attestation."""
    path = target_root / "alternate_streams.json"
    if not path.is_file():
        return []
    manifest = json.loads(path.read_text())
    records = (
        manifest.get("object_setup_protocols", [])
        if isinstance(manifest, dict)
        else None
    )
    if not isinstance(records, list):
        raise TypeError("object_setup_protocols must be an array")
    if not records:
        return []
    binary, header, load_segment, binary_hash = load_binary_evidence(
        target_root, manifest
    )
    return [
        {
            **_protocol(record, binary, header, load_segment),
            "binary_sha256": binary_hash,
        }
        for record in records
    ]
