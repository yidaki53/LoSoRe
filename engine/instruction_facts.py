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


def allocator_empty_list_contract(raw: bytes, helper: bytes, callback: bytes) -> dict:
    """Oracle: exact 0353 composition under supplied empty-list/default-callback premises.

    The list scan is bypassed only because the supplied head equals the frontier.
    This recognizer does not prove original-program entry state or memory ownership.
    """
    template = bytes.fromhex(
        "0bc07477a33c7be87f01bff6638cd98ec18bcf8cc326c43d8cc63b36f063"
        "745f263b550677eb7206263b450477e306575351268b0d268b5d0274335351"
        "268b4d04268b5d062bc81bda83e10f03c703d604f083d200240f8bf88ec2"
        "268f05268f450226894d0426895d068bcf8cc35f0726890d26895d02585af8"
        "c333c099c303c703d604f083d200240f3b16f463720877253b06f263771f06"
        "578bf98ec3a3ee638916f0632689052689550233c050ff1efe63585af8c3ff"
        "363c7bff1efe633c0172b774b6a13c7be93cff"
    )
    if (
        raw != template
        or helper != bytes.fromhex("0507008bd0d1dad1ead1ead1ea250800c3")
        or callback != bytes.fromhex("33c0ca0200")
    ):
        raise ValueError(
            "unsupported allocator/helper/default callback instruction shape"
        )
    return {
        "oracle": "exact_allocator_empty_list_composition",
        "routine_bytes_hex": raw.hex(),
        "helper_bytes_hex": helper.hex(),
        "callback_bytes_hex": callback.hex(),
        "rounding": {"bias": helper[1], "alignment": helper[14], "paragraph": 16},
        "saved_request_cell": int.from_bytes(raw[5:7], "little"),
        "limit_order": ["segment", "offset"],
        "success_return": "old_head",
        "failure_return": {"AX": 0, "DX": "computed_segment", "CF": 1},
        "zero_writes": [],
        "support": {
            "zero": [0x353, 0x355, 0x3CE, 0x3D0, 0x3D1],
            "save_and_round": [0x357, 0x35A, 0x4DC],
            "empty_list": [0x35D, 0x360, 0x362, 0x368, 0x36B, 0x36D, 0x371],
            "normalize": [0x3D2, 0x3D4, 0x3D6, 0x3D8, 0x3DB],
            "limit": [0x3DD, 0x3E1, 0x3E3, 0x3E5, 0x3E9],
            "success": [
                0x3EB,
                0x3EC,
                0x3ED,
                0x3EF,
                0x3F1,
                0x3F4,
                0x3F8,
                0x3FB,
                0x3FF,
                0x401,
                0x402,
                0x406,
                0x407,
                0x408,
                0x409,
            ],
            "failure": [0x40A, 0x40E, 0x412, 0x414, 0x3CD, 0xD6],
        },
        "preconditions": [
            "Controlled COM layout supplies DS=SS=CS and disjoint writable globals/stack.",
            "Free-list head equals frontier; both offset and segment are supplied.",
            "Only the authenticated XOR AX,AX / RETF 2 default callback is installed.",
            "Case segments are CS-relative without segment-addition wrap.",
            "Comparison covers AX/DX/CF, saved request, frontier and head only.",
        ],
        "unresolved": [
            "free-list exact-fit/split/traversal",
            "nondefault callback/retry",
            "normal-program heap provenance/lifetime",
            "full register/flag ABI",
        ],
        "source_recovered": False,
    }


def bounded_byte_fill_contract(raw: bytes) -> dict:
    """Oracle: exact stack-load/CLD/REP STOSB leaf shape; bounds are caller obligations.

    This recognizes one complete far-return shape without extending the generic
    initialization-prefix return gate. It does not establish normal-program
    reachability, valid pointers or a historical Pascal declaration.
    """
    if (
        len(raw) != 20
        or raw[:5] != bytes.fromhex("8bdc36c47f")
        or raw[6:9] != bytes.fromhex("368b4f")
        or raw[10:13] != bytes.fromhex("368a47")
        or raw[14:18] != bytes.fromhex("fcf3aaca")
    ):
        raise ValueError("unsupported bounded byte-fill instruction shape")
    slots = [raw[5], raw[9], raw[13]]
    cleanup = int.from_bytes(raw[18:20], "little")
    if (
        any(slot < 4 or slot % 2 for slot in slots)
        or len(set(slots)) != 3
        or set(slots) != {slots[0], slots[0] - 2, slots[0] - 4}
        or not slots[2] < slots[1] < slots[0]
        or cleanup < slots[0]
    ):
        raise ValueError(
            "byte-fill stack slots lack a supported disjoint argument layout"
        )
    return {
        "oracle": "exact_byte_shape_under_scoped_far_call_preconditions",
        "destination_far_pointer_slot": slots[0],
        "count_word_slot": slots[1],
        "value_low_byte_slot": slots[2],
        "memory_operation": "write count copies of value to destination, zero count writes nothing",
        "support_offsets": [0, 2, 6, 10, 14, 15],
        "far_return_cleanup_bytes": cleanup,
        "preconditions": [
            "Entry SS:SP argument cells and return address are valid and disjoint from destination.",
            "Destination far pointer is valid, writable and nonwrapping for the unsigned count.",
            "Count is independently bounded by the supplied object allocation.",
        ],
        "limitations": "Memory contract only; no host ABI or normal-program acceptance.",
    }


def bounded_shortstring_contract(raw: bytes) -> dict:
    """Oracle: exact zero-mode initialization/shortstring shape, under disjoint bounds.

    The alternate DX path is unreachable because the complete entry clears DX.
    No arbitrary branch, relocated operand, aliased pointer or return is certified.
    """
    template = bytes.fromhex(
        "33d28bdc1e36c47f0836c57704fc33c0abb8b0d7ab33c0b91600f3ab"
        "b94f000bd27509ac3ac876048ac8e308ac0ac07403aae2f832c0aa1fca0800"
    )
    parameters = {8, 12, 18, 19, 24, 25, 29, 30, 57, 58}
    if len(raw) != len(template) or any(
        actual != expected
        for offset, (actual, expected) in enumerate(zip(raw, template))
        if offset not in parameters
    ):
        raise ValueError("unsupported bounded shortstring composition shape")
    destination_slot, source_slot = raw[8], raw[12]
    word_count = int.from_bytes(raw[24:26], "little")
    limit = int.from_bytes(raw[29:31], "little")
    cleanup = int.from_bytes(raw[57:59], "little")
    initialization_bytes = 4 + 2 * word_count
    if (
        source_slot != 4
        or destination_slot != 8
        or cleanup < destination_slot
        or not 1 <= limit <= 255
        or initialization_bytes > 256
    ):
        raise ValueError("shortstring arguments or memory spans lack supported bounds")
    prefix = initialization_prefix(raw)
    if prefix["residue"]["offset"] != 31:
        raise ValueError("shortstring prefix contract is not established")
    return {
        "oracle": "exact_shortstring_composition_under_scoped_far_call_preconditions",
        "routine_bytes_hex": raw.hex(),
        "destination_far_pointer_slot": destination_slot,
        "source_far_pointer_slot": source_slot,
        "prefix_writes": prefix["writes"],
        "text_destination_offset": initialization_bytes,
        "source_length_offset": 0,
        "source_text_offset": 1,
        "maximum_text_bytes": limit,
        "length_operation": "unsigned min(source[0], maximum_text_bytes)",
        "termination": "stop before first NUL or bounded length, then append one NUL",
        "write_order": "prefix writes, copied nonzero text bytes, final NUL",
        "support_offsets": [
            0,
            2,
            4,
            5,
            9,
            13,
            14,
            16,
            17,
            20,
            21,
            23,
            26,
            28,
            31,
            33,
            35,
            36,
            38,
            40,
            42,
            44,
            45,
            47,
            49,
            50,
            52,
            54,
            55,
            56,
        ],
        "unreachable_branch": {
            "offset": 33,
            "reason": "DX is zero from entry XOR; no intervening DX write",
        },
        "far_return_cleanup_bytes": cleanup,
        "preconditions": [
            "Entry SS:SP argument cells and return address are valid and disjoint from both objects.",
            "Source and destination are disjoint nonwrapping far-pointer allocations.",
            "Source holds its length byte and at least min(length, limit) text bytes.",
            "Destination has a valid 256-byte initialization window and is writable through text_destination_offset + limit inclusive.",
        ],
        "limitations": "Scoped memory contract, not historical Pascal, full ABI or normal-program provenance.",
    }


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
