"""Conservative straight-line 8086 initialization facts, not a general emulator."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class _Value:
    kind: str
    amount: int
    support: tuple[int, ...]


def _value_record(value: _Value) -> dict:
    """Oracle: JSON-native identity/provenance record for exact saved-fact replay."""
    return {"kind": value.kind, "amount": value.amount, "support": list(value.support)}


def initialization_prefix(
    raw: bytes,
    *,
    relocation_offsets: set[int] | None = None,
    load_segment: int = 0x1000,
    data_window: tuple[int, int] | None = None,
) -> dict:
    """Oracle: byte transfer rules under explicit SS:entry-stack object/source bindings."""
    if not raw or type(load_segment) is not int or not 0 <= load_segment <= 65535:
        raise ValueError("initialization prefix needs bytes and a 16-bit load segment")
    if data_window is not None and (
        type(data_window) is not tuple
        or len(data_window) != 2
        or any(type(value) is not int for value in data_window)
        or not 0 <= data_window[0] < data_window[1] <= 65536
    ):
        raise ValueError("data window must be a nonempty half-open 16-bit offset range")
    relocations = set() if relocation_offsets is None else set(relocation_offsets)
    if any(
        type(offset) is not int or not 0 <= offset < len(raw) - 1
        for offset in relocations
    ):
        raise ValueError("initialization relocation lies outside the supplied bytes")
    names = ("ax", "cx", "dx", "bx", "sp", "bp", "si", "di")
    registers: dict[str, _Value] = {"sp": _Value("entry_stack", 0, ())}
    instructions, writes = [], []
    direction_clear = False
    direction_support: tuple[int, ...] = ()
    segment: _Value | None = None
    segments = {
        name: _Value(f"entry_{name}", 0, ()) for name in ("es", "cs", "ss", "ds")
    }
    stack: list[_Value] = []
    cursor = 0
    while cursor < len(raw):
        prior_sp = registers["sp"]
        start = cursor
        opcode = raw[start]
        size = 0
        reason = "unsupported opcode"
        immediate_relocation = None
        if 0xB8 <= opcode <= 0xBF and start + 3 <= len(raw):
            size = 3
            value = int.from_bytes(raw[start + 1 : start + 3], "little")
            if start + 1 in relocations:
                value = (value + load_segment) & 65535
                immediate_relocation = start + 1
            registers[names[opcode - 0xB8]] = _Value("constant", value, (start,))
        elif opcode in (0x33, 0x31, 0x8B, 0x89, 0x2B, 0x29) and start + 2 <= len(raw):
            modrm = raw[start + 1]
            if modrm >= 0xC0:
                target, source = (modrm >> 3) & 7, modrm & 7
                if opcode in (0x31, 0x89, 0x29):
                    target, source = source, target
                if opcode in (0x31, 0x33) and target == source:
                    size = 2
                    registers[names[target]] = _Value("constant", 0, (start,))
                elif opcode in (0x89, 0x8B) and names[source] in registers:
                    size = 2
                    value = registers[names[source]]
                    registers[names[target]] = replace(
                        value, support=(*value.support, start)
                    )
                elif opcode in (0x2B, 0x29):
                    left, right = (
                        registers.get(names[target]),
                        registers.get(names[source]),
                    )
                    if (
                        left is not None
                        and right is not None
                        and left.kind == right.kind == "constant"
                    ):
                        size = 2
                        registers[names[target]] = _Value(
                            "constant",
                            (left.amount - right.amount) & 65535,
                            (*left.support, *right.support, start),
                        )
        elif opcode == 0xD1 and start + 2 <= len(raw) and raw[start + 1] & 0xF8 == 0xE8:
            name = names[raw[start + 1] & 7]
            value = registers.get(name)
            if value is not None and value.kind == "constant":
                size = 2
                registers[name] = replace(
                    value,
                    amount=value.amount >> 1,
                    support=(*value.support, start),
                )
        elif raw[start : start + 2] == b"\x8d\x45" and start + 3 <= len(raw):
            # LEA AX,[DI+disp8] preserves the initial-object origin as DI advances.
            value = registers.get("di")
            if value is not None and value.kind == "object_offset":
                size = 3
                displacement = int.from_bytes(
                    raw[start + 2 : start + 3], "little", signed=True
                )
                registers["ax"] = replace(
                    value,
                    amount=(value.amount + displacement) & 65535,
                    support=(*value.support, start),
                )
        elif raw[start : start + 2] == b"\x8c\xc0" and segment is not None:
            size = 2
            registers["ax"] = replace(segment, support=(*segment.support, start))
        elif raw[start : start + 4] in (b"\x36\xc4\x7f\x08", b"\x36\xc5\x77\x04"):
            value = registers.get("bx")
            if (
                value is not None
                and value.kind == "entry_stack"
                and value.amount == 0
                and segments["ss"].kind == "entry_ss"
            ):
                size = 4
                if raw[start + 1] == 0xC4:
                    registers["di"] = _Value(
                        "object_offset", 0, (*value.support, start)
                    )
                    segment = _Value("object_segment", 0, (*value.support, start))
                    segments["es"] = segment
                else:
                    registers["si"] = _Value(
                        "source_offset", 0, (*value.support, start)
                    )
                    segments["ds"] = _Value(
                        "source_segment", 0, (*value.support, start)
                    )
        elif (
            opcode in (0x06, 0x0E, 0x16, 0x1E)
            and registers["sp"].kind == "entry_stack"
            and segments["ss"].kind == "entry_ss"
        ):
            size = 1
            name = {0x06: "es", 0x0E: "cs", 0x16: "ss", 0x1E: "ds"}[opcode]
            stack.append(
                replace(segments[name], support=(*segments[name].support, start))
            )
            value = registers["sp"]
            registers["sp"] = replace(
                value, amount=value.amount - 2, support=(*value.support, start)
            )
        elif (
            opcode in (0x07, 0x17, 0x1F)
            and stack
            and registers["sp"].kind == "entry_stack"
            and segments["ss"].kind == "entry_ss"
        ):
            size = 1
            name = {0x07: "es", 0x17: "ss", 0x1F: "ds"}[opcode]
            value = stack.pop()
            segments[name] = replace(value, support=(*value.support, start))
            if name == "es":
                segment = segments[name]
            value = registers["sp"]
            registers["sp"] = replace(
                value,
                amount=value.amount + 2,
                support=(*value.support, start),
            )
            if name == "ss":
                # A changed SS invalidates the tracked entry stack address.
                registers["sp"] = _Value("unknown_stack", 0, (start,))
                stack.clear()
        elif opcode == 0xFC:
            size = 1
            direction_clear = True
            direction_support = (start,)
        elif opcode == 0xAB or raw[start : start + 2] == b"\xf3\xab":
            value, destination = registers.get("ax"), registers.get("di")
            count = registers.get("cx") if opcode == 0xF3 else _Value("constant", 1, ())
            object_destination = (
                destination is not None
                and destination.kind == "object_offset"
                and segment is not None
                and segment.kind == "object_segment"
            )
            data_destination = (
                destination is not None
                and destination.kind == "constant"
                and segment is not None
                and segment.kind == "entry_ds"
                and data_window is not None
            )
            lower, upper = data_window if data_destination else (0, 256)
            if (
                direction_clear
                and segment is not None
                and value is not None
                and destination is not None
                and (object_destination or data_destination)
                and count is not None
                and count.kind == "constant"
                and lower <= destination.amount
                and destination.amount + 2 * count.amount <= upper
            ):
                size = 2 if opcode == 0xF3 else 1
                writes.append(
                    {
                        "byte_offset": destination.amount,
                        "word_count": count.amount,
                        "value": _value_record(value),
                        "support": [
                            *destination.support,
                            *segment.support,
                            *direction_support,
                            *count.support,
                            start,
                        ],
                    }
                )
                if data_destination:
                    writes[-1]["address_space"] = "entry_ds"
                    writes[-1]["segment"] = _value_record(segment)
                    writes[-1]["data_window"] = list(data_window)
                    writes[-1]["support"] = sorted(
                        set(writes[-1]["support"] + list(value.support))
                    )
                elif count.amount:
                    # Object writes are not established to be disjoint from the operand stack.
                    stack.clear()
                registers["di"] = replace(
                    destination,
                    amount=(destination.amount + 2 * count.amount) & 65535,
                    support=(*destination.support, start),
                )
                if opcode == 0xF3:
                    registers["cx"] = _Value("constant", 0, (*count.support, start))
            else:
                reason = "unknown store operand/direction or object bound exceeded"
        if not size:
            break
        if (
            opcode not in (0x06, 0x0E, 0x16, 0x1E, 0x07, 0x17, 0x1F)
            and registers["sp"] != prior_sp
        ):
            stack.clear()
        overlapping = {
            offset
            for offset in relocations
            if offset < start + size and offset + 2 > start
        }
        if overlapping != (
            {immediate_relocation} if immediate_relocation is not None else set()
        ):
            raise ValueError("initialization relocation is not an immediate word")
        instructions.append(
            {
                "offset": start,
                "bytes_hex": raw[start : start + size].hex(),
                "relocation_offset": immediate_relocation,
            }
        )
        cursor += size
    destination = registers.get("di")
    return {
        "oracle": "static_supported_instruction_prefix",
        "assumptions": [
            "Entry SS:SP+8 is a valid 256-byte nonwrapping object pointer.",
            "Entry SS:SP+4 is a valid source pointer; no prior instruction is skipped.",
            "Logical MZ relocation adds the supplied load segment modulo 65536.",
        ]
        + (
            [
                f"Entry DS offsets [{data_window[0]}, {data_window[1]}) are valid writable nonaliasing memory.",
                "Operand stack models only supported segment pushes/pops; stack memory effects are not write facts.",
            ]
            if data_window is not None
            else []
        ),
        "instructions": instructions,
        "writes": writes,
        "registers": {name: _value_record(value) for name, value in registers.items()},
        "next_object_offset": destination.amount if destination is not None else None,
        "residue": {
            "offset": cursor,
            "reason": reason,
            "bytes_hex": raw[cursor:].hex(),
        }
        if cursor < len(raw)
        else None,
    }
