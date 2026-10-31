"""Validation for binary-bound alternate instruction streams."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re

from tools.asmcfg import (
    is_branch,
    is_call,
    is_cond_branch,
    parse_ghidra_asm,
    resolve_branch_target,
)

_SHORT_JCC_MNEMONICS = (
    {"JO"},
    {"JNO"},
    {"JB", "JC", "JNAE"},
    {"JAE", "JNB", "JNC"},
    {"JE", "JZ"},
    {"JNE", "JNZ"},
    {"JBE", "JNA"},
    {"JA", "JNBE"},
    {"JS"},
    {"JNS"},
    {"JP", "JPE"},
    {"JNP", "JPO"},
    {"JL"},
    {"JGE"},
    {"JLE"},
    {"JG"},
)
_LOOP_MNEMONICS = {
    0xE0: {"LOOPNE", "LOOPNZ"},
    0xE1: {"LOOPE", "LOOPZ"},
    0xE2: {"LOOP"},
    0xE3: {"JCXZ"},
}
_BRANCH_MNEMONICS = set().union(
    *_SHORT_JCC_MNEMONICS,
    {"JMP"},
    *_LOOP_MNEMONICS.values(),
)


def _hex(value: object, field: str) -> int:
    if not isinstance(value, str) or not re.fullmatch(r"0x[0-9a-fA-F]+", value):
        raise ValueError(f"alternate-stream {field} must be a hexadecimal string")
    return int(value, 16)


def _bytes(value: object, field: str) -> bytes:
    if (
        not isinstance(value, str)
        or not value
        or len(value) % 2
        or not re.fullmatch(r"[0-9a-fA-F]+", value)
    ):
        raise ValueError(f"alternate-stream {field} must be non-empty even-length hex")
    return bytes.fromhex(value)


def _repository_file(target_root: pathlib.Path, raw_path: object) -> pathlib.Path:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ValueError(
            "alternate-stream binary.path must be a repository-relative path"
        )
    relative = pathlib.Path(raw_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("alternate-stream binary.path must stay inside the repository")
    repository_root = target_root.parent.parent.resolve()
    path = (repository_root / relative).resolve()
    if not path.is_relative_to(repository_root):
        raise ValueError("alternate-stream binary.path escapes the repository")
    if not path.is_file():
        raise FileNotFoundError(f"alternate-stream binary is missing: {path}")
    return path


def _assembly_instructions(
    target_root: pathlib.Path,
) -> dict[int, list[tuple[int, str]]]:
    result: dict[int, list[tuple[int, str]]] = {}
    asm_dir = target_root / "asm"
    if not asm_dir.is_dir():
        return result
    for asm_path in asm_dir.glob("*.s"):
        parsed = parse_ghidra_asm(asm_path.read_text(errors="replace"))
        for address, segment, instruction in zip(
            parsed["addrs"],
            parsed["segments"],
            parsed["insts"],
            strict=True,
        ):
            result.setdefault(address, []).append((segment, instruction))
    return result


def _instructions(
    stream: dict,
    address: int,
    header_bytes: int,
    image_start: int,
    binary_data: bytes,
    stream_bytes: bytes,
) -> list[int]:
    entries = stream.get("instructions")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"alternate stream at 0x{address:x} has no instructions")
    instruction_addresses = []
    joined_bytes = bytearray()
    cursor = address
    for entry in entries:
        if not isinstance(entry, dict):
            raise TypeError("alternate-stream instructions must be objects")
        entry_address = _hex(entry.get("address"), "instruction.address")
        entry_bytes = _bytes(entry.get("bytes_hex"), "instruction.bytes_hex")
        if entry_address != cursor:
            raise ValueError(
                f"alternate-stream instruction boundaries are not contiguous "
                f"at 0x{cursor:x}"
            )
        file_offset = header_bytes + entry_address - image_start
        if binary_data[file_offset : file_offset + len(entry_bytes)] != entry_bytes:
            raise ValueError(
                f"alternate-stream instruction bytes do not match at 0x{entry_address:x}"
            )
        text = entry.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("alternate-stream instruction text is required")
        instruction_addresses.append(entry_address)
        joined_bytes.extend(entry_bytes)
        cursor += len(entry_bytes)
    if instruction_addresses[0] != address or bytes(joined_bytes) != stream_bytes:
        raise ValueError(
            f"alternate-stream instruction listing does not cover bytes "
            f"at 0x{address:x}"
        )
    return instruction_addresses


def _source_edge(
    edge: object,
    stream_address: int,
    header_bytes: int,
    image_start: int,
    binary_data: bytes,
    assembly: dict[int, list[tuple[int, str]]],
    instruction_addresses: set[int],
    code_segment: int | None,
) -> dict:
    if not isinstance(edge, dict):
        raise TypeError("alternate-stream source_edges must be objects")
    address = _hex(edge.get("address"), "source_edge.address")
    file_offset = _hex(edge.get("file_offset"), "source_edge.file_offset")
    raw_bytes = _bytes(edge.get("bytes_hex"), "source_edge.bytes_hex")
    target_address = _hex(edge.get("target_address"), "source_edge.target_address")
    source_instruction = edge.get("instruction")
    if not isinstance(source_instruction, str) or not source_instruction.strip():
        raise ValueError("alternate-stream source-edge instruction is required")
    transfer_kind = edge.get("transfer_kind", "direct")
    if transfer_kind not in {"direct", "far_indirect", "near_register"}:
        raise ValueError("alternate-stream source-edge transfer_kind is invalid")
    if file_offset != header_bytes + address - image_start:
        raise ValueError(
            f"alternate-stream source edge mapping is inconsistent at 0x{address:x}"
        )
    if binary_data[file_offset : file_offset + len(raw_bytes)] != raw_bytes:
        raise ValueError(
            f"alternate-stream source edge bytes do not match at 0x{address:x}"
        )
    is_short_conditional = len(raw_bytes) == 2 and (
        0x70 <= raw_bytes[0] <= 0x7F or raw_bytes[0] in _LOOP_MNEMONICS
    )
    is_near_call = len(raw_bytes) == 3 and raw_bytes[0] == 0xE8
    is_far_indirect_call = (
        len(raw_bytes) == 4
        and raw_bytes[:2] == b"\xff\x1e"
        and transfer_kind == "far_indirect"
    )
    if transfer_kind == "far_indirect" and not is_far_indirect_call:
        raise ValueError(
            f"alternate-stream far-indirect edge has invalid encoding at 0x{address:x}"
        )
    is_register_call = transfer_kind == "near_register"
    if is_register_call and (
        raw_bytes != b"\xff\xd3" or source_instruction.strip().upper() != "CALL BX"
    ):
        raise ValueError("alternate-stream register-call encoding must be CALL BX")
    if not (
        is_short_conditional or is_near_call or is_far_indirect_call or is_register_call
    ):
        raise ValueError(
            f"alternate-stream source edge is not a supported transfer at 0x{address:x}"
        )
    if is_register_call and target_address not in instruction_addresses:
        raise ValueError("register target is not a decoded instruction boundary")
    if not is_register_call and target_address != stream_address:
        raise ValueError(
            f"alternate-stream source edge at 0x{address:x} "
            f"does not target 0x{stream_address:x}"
        )
    if is_register_call:
        if (code_segment, source_instruction.strip().upper()) not in assembly.get(
            address, []
        ):
            raise ValueError("register-call code segment disagrees with assembly")
        if code_segment is None or not (
            0 <= target_address - code_segment * 16 <= 0xFFFF
        ):
            raise ValueError("register target is outside the caller code segment")
    elif not _matches_assembly_edge(
        address, raw_bytes, target_address, source_instruction, assembly
    ):
        raise ValueError(
            f"alternate-stream source edge at 0x{address:x} "
            "does not match the assembly inventory"
        )
    return edge


def _register_path_successor(address: int, raw_bytes: bytes, segment: int) -> int:
    """Oracle: decode only reviewed BX-preserving encodings; reject all others."""
    preserving_encodings = (
        (b"\xa1", 3),  # MOV AX,moffs16
        (b"\x8b\x16", 4),  # MOV DX,[disp16]
        (b"\x2b\x06", 4),  # SUB AX,[disp16]
        (b"\x1b\x16", 4),  # SBB DX,[disp16]
        (b"\x25", 3),  # AND AX,imm16
        (b"\x1e", 1),  # PUSH DS
        (b"\x8b\x3e", 4),  # MOV DI,[disp16]
        (b"\xc5\x36", 4),  # LDS SI,[disp16]
    )
    if raw_bytes[:1] == b"\xeb" and len(raw_bytes) == 2:
        displacement = int.from_bytes(raw_bytes[1:], "little", signed=True)
        return segment * 16 + ((address - segment * 16 + 2 + displacement) & 0xFFFF)
    if any(
        raw_bytes.startswith(prefix) and len(raw_bytes) == size
        for prefix, size in preserving_encodings
    ):
        return address + len(raw_bytes)
    raise ValueError(f"unsupported register-path instruction at 0x{address:x}")


def _validate_register_call(
    edge: dict,
    target_root: pathlib.Path,
    header_bytes: int,
    image_start: int,
    binary_data: bytes,
    assembly: dict[int, list[tuple[int, str]]],
    streams: list[dict],
) -> None:
    """Oracle: binary-bound, single-entry MOV BX,imm16 path to CALL BX."""
    path = edge.get("register_path")
    if not isinstance(path, dict):
        raise TypeError("register_path must be an object")
    function_name = path.get("function")
    if not isinstance(function_name, str) or not re.fullmatch(
        r"FUN_[A-Za-z0-9_]+", function_name
    ):
        raise ValueError("register_path.function must name an assembly export")
    function_path = target_root / "asm" / f"{function_name}.s"
    if not function_path.is_file():
        raise ValueError("register-path assembly export is missing")
    parsed = parse_ghidra_asm(function_path.read_text())
    call_address = _hex(edge["address"], "source_edge.address")
    if parsed["addrs"].count(call_address) != 1:
        raise ValueError("register-path call must occur once in its assembly export")
    call_index = parsed["addrs"].index(call_address)
    entries = path.get("instructions")
    if (
        not isinstance(entries, list)
        or not entries
        or not all(isinstance(entry, dict) for entry in entries)
    ):
        raise ValueError("register path requires instruction objects")
    addresses = [
        _hex(entry.get("address"), "register_path.address") for entry in entries
    ]
    if addresses != parsed["addrs"][:call_index]:
        raise ValueError("register path must cover the complete function prefix")
    segment = parsed["segments"][call_index]
    if any(item != segment for item in parsed["segments"][:call_index]):
        raise ValueError("register path must stay in the caller code segment")
    successors = dict(zip(addresses, addresses[1:] + [call_address], strict=True))
    for index, (address, entry) in enumerate(zip(addresses, entries, strict=True)):
        raw_bytes = _bytes(entry.get("bytes_hex"), "register_path.bytes_hex")
        file_offset = header_bytes + address - image_start
        if file_offset < header_bytes or (
            binary_data[file_offset : file_offset + len(raw_bytes)] != raw_bytes
        ):
            raise ValueError(f"register-path bytes do not match at 0x{address:x}")
        if index == 0:
            if (
                len(raw_bytes) != 3
                or raw_bytes[0] != 0xBB
                or segment * 16 + int.from_bytes(raw_bytes[1:], "little")
                != _hex(edge["target_address"], "source_edge.target_address")
            ):
                raise ValueError("MOV BX initializer disagrees with register target")
            successor = address + 3
        else:
            successor = _register_path_successor(address, raw_bytes, segment)
        instruction = parsed["insts"][index]
        if successor != successors[address] or (
            is_branch(instruction)
            and resolve_branch_target(instruction, segment) != successor
        ):
            raise ValueError(f"register-path successor disagrees at 0x{address:x}")

    protected_addresses = set(addresses[1:]) | {call_address}
    for asm_path in (target_root / "asm").glob("*.s"):
        other = parse_ghidra_asm(asm_path.read_text())
        if asm_path != function_path and protected_addresses.intersection(
            other["addrs"]
        ):
            raise ValueError("another assembly export bypasses register initialization")
    transfers = [
        (address, segment, instruction)
        for address, items in assembly.items()
        for segment, instruction in items
    ]
    for stream in streams:
        if not isinstance(stream, dict) or stream.get("status") != "verified":
            continue
        raw_segment = stream.get("code_segment")
        stream_segment = (
            _hex(raw_segment, "code_segment") if raw_segment is not None else None
        )
        groups = [stream["instructions"]] + [
            item["instructions"] for item in stream.get("overlapping_entries", [])
        ]
        if any(
            _hex(item["address"], "instruction.address") in protected_addresses
            for group in groups
            for item in group
        ):
            raise ValueError("alternate stream bypasses register initialization")
        transfers.extend(
            (_hex(item["address"], "instruction.address"), stream_segment, item["text"])
            for group in groups
            for item in group
        )
        entry_addresses = {_hex(stream["address"], "address")} | {
            _hex(item["address"], "overlapping_entry.address")
            for item in stream.get("overlapping_entries", [])
        }
        if entry_addresses & protected_addresses:
            raise ValueError("alternate entry bypasses register initialization")
        for transfer in stream["source_edges"] + stream.get("outgoing_calls", []):
            source_address = _hex(transfer["address"], "source_edge.address")
            target_address = _hex(
                transfer["target_address"], "source_edge.target_address"
            )
            if (
                target_address in protected_addresses
                and successors.get(source_address) != target_address
            ):
                raise ValueError("recorded edge bypasses register initialization")
    for address, source_segment, instruction in transfers:
        instruction = instruction.strip().upper()
        if not (is_branch(instruction) or is_call(instruction)):
            continue
        target = resolve_branch_target(instruction, source_segment)
        if target in protected_addresses and successors.get(address) != target:
            raise ValueError("control transfer bypasses register initialization")


def _validate_indirect_pointer(
    pointer: object,
    stream_address: int,
    source_edges: list[dict],
    header_bytes: int,
    image_start: int,
    binary_data: bytes,
    assembly: dict[int, list[tuple[int, str]]],
) -> None:
    if not isinstance(pointer, dict):
        raise TypeError("alternate-stream indirect_pointer must be an object")
    storage_offset = _hex(
        pointer.get("storage_offset"), "indirect_pointer.storage_offset"
    )
    target_offset = _hex(pointer.get("target_offset"), "indirect_pointer.target_offset")
    target_segment = _hex(
        pointer.get("target_segment"), "indirect_pointer.target_segment"
    )
    if storage_offset > 0xFFFC or target_offset > 0xFFFF or target_segment > 0xFFFF:
        raise ValueError("alternate-stream indirect pointer values must fit in 16 bits")
    if target_segment * 16 + target_offset != stream_address:
        raise ValueError("alternate-stream indirect pointer does not target its entry")

    initializers = pointer.get("initializers")
    if not isinstance(initializers, list) or len(initializers) != 2:
        raise ValueError("alternate-stream indirect pointer requires two initializers")
    expected_references = {
        (
            _hex(edge.get("address"), "source_edge.address"),
            str(edge.get("instruction", "")).strip().upper(),
        )
        for edge in source_edges
    }
    initialized_parts = set()
    for initializer in initializers:
        if not isinstance(initializer, dict):
            raise TypeError("alternate-stream pointer initializers must be objects")
        part = initializer.get("part")
        if part not in {"offset", "segment"} or part in initialized_parts:
            raise ValueError("alternate-stream pointer initializer parts are invalid")
        initialized_parts.add(part)
        address = _hex(initializer.get("address"), "pointer_initializer.address")
        file_offset = _hex(
            initializer.get("file_offset"), "pointer_initializer.file_offset"
        )
        raw_bytes = _bytes(
            initializer.get("bytes_hex"), "pointer_initializer.bytes_hex"
        )
        instruction = initializer.get("instruction")
        if not isinstance(instruction, str) or not instruction.strip():
            raise ValueError(
                "alternate-stream pointer initializer instruction is required"
            )
        if file_offset != header_bytes + address - image_start:
            raise ValueError(
                f"alternate-stream pointer initializer mapping is inconsistent "
                f"at 0x{address:x}"
            )
        if binary_data[file_offset : file_offset + len(raw_bytes)] != raw_bytes:
            raise ValueError(
                f"alternate-stream pointer initializer bytes do not match "
                f"at 0x{address:x}"
            )
        if not any(
            segment == target_segment
            and text.strip().upper() == instruction.strip().upper()
            for segment, text in assembly.get(address, [])
        ):
            raise ValueError(
                f"alternate-stream pointer initializer at 0x{address:x} "
                "does not match the assembly inventory"
            )
        if part == "offset":
            valid_encoding = (
                len(raw_bytes) == 6
                and raw_bytes[:2] == b"\xc7\x06"
                and int.from_bytes(raw_bytes[2:4], "little") == storage_offset
                and int.from_bytes(raw_bytes[4:6], "little") == target_offset
            )
        else:
            valid_encoding = (
                len(raw_bytes) == 4
                and raw_bytes[:2] == b"\x8c\x0e"
                and int.from_bytes(raw_bytes[2:4], "little") == storage_offset + 2
            )
        if not valid_encoding:
            raise ValueError(
                f"alternate-stream {part} pointer initializer has invalid encoding"
            )
        expected_references.add((address, instruction.strip().upper()))
    if initialized_parts != {"offset", "segment"}:
        raise ValueError(
            "alternate-stream indirect pointer is incompletely initialized"
        )

    referenced_offsets = f"{storage_offset:04X}|{storage_offset + 2:04X}"
    reference_pattern = re.compile(rf"\b(?:0X)?(?:{referenced_offsets})\b")
    pointer_references = set()
    for address, entries in assembly.items():
        for _, instruction in entries:
            if reference_pattern.search(instruction.upper()):
                pointer_references.add((address, instruction.strip().upper()))
    if pointer_references != expected_references:
        raise ValueError(
            "alternate-stream indirect pointer references disagree with the "
            "assembly inventory"
        )


def _matches_assembly_edge(
    address: int,
    raw_bytes: bytes,
    target_address: int,
    source_instruction: str,
    assembly: dict[int, list[tuple[int, str]]],
) -> bool:
    for segment, instruction in assembly.get(address, []):
        instruction = instruction.strip().upper()
        if instruction != source_instruction.strip().upper():
            continue
        if len(raw_bytes) == 2 and 0x70 <= raw_bytes[0] <= 0x7F:
            if (
                not is_cond_branch(instruction)
                or instruction.split(maxsplit=1)[0]
                not in _SHORT_JCC_MNEMONICS[raw_bytes[0] - 0x70]
                or resolve_branch_target(instruction, segment) != target_address
            ):
                continue
        elif len(raw_bytes) == 2 and raw_bytes[0] in _LOOP_MNEMONICS:
            if (
                instruction.split(maxsplit=1)[0] not in _LOOP_MNEMONICS[raw_bytes[0]]
                or resolve_branch_target(instruction, segment) != target_address
            ):
                continue
        elif len(raw_bytes) == 3 and raw_bytes[0] == 0xE8:
            if (
                not instruction.startswith("CALL ")
                or instruction.startswith("CALLF ")
                or resolve_branch_target(instruction, segment) != target_address
            ):
                continue
        elif len(raw_bytes) == 4 and raw_bytes[:2] == b"\xff\x1e":
            match = re.fullmatch(r"CALLF\s+\[0X([0-9A-F]+)\]", instruction)
            if not match or int(match.group(1), 16) != int.from_bytes(
                raw_bytes[2:4], "little"
            ):
                continue
        else:
            continue
        if len(raw_bytes) == 4:
            return True
        displacement = int.from_bytes(raw_bytes[1:], "little", signed=True)
        source_offset = address - segment * 16
        encoded_target = segment * 16 + (
            (source_offset + len(raw_bytes) + displacement) & 0xFFFF
        )
        if encoded_target == target_address:
            return True
    return False


def _mz_relocation_locations(binary_data: bytes, header_bytes: int) -> set[int]:
    if len(binary_data) < 0x1C or binary_data[:2] != b"MZ":
        raise ValueError("relocation-backed alternate calls require an MZ binary")
    declared_header_bytes = int.from_bytes(binary_data[0x08:0x0A], "little") * 16
    if declared_header_bytes != header_bytes:
        raise ValueError("alternate-stream header_bytes disagree with the MZ header")
    relocation_count = int.from_bytes(binary_data[0x06:0x08], "little")
    relocation_table = int.from_bytes(binary_data[0x18:0x1A], "little")
    relocation_end = relocation_table + relocation_count * 4
    if relocation_end > header_bytes or relocation_end > len(binary_data):
        raise ValueError("MZ relocation table is outside the declared header")

    locations = set()
    for index in range(relocation_count):
        entry = relocation_table + index * 4
        offset = int.from_bytes(binary_data[entry : entry + 2], "little")
        segment = int.from_bytes(binary_data[entry + 2 : entry + 4], "little")
        location = header_bytes + segment * 16 + offset
        if location + 2 > len(binary_data):
            raise ValueError("MZ relocation points outside the binary")
        locations.add(location)
    return locations


def _outgoing_far_call(
    edge: object,
    stream_instructions: dict[int, dict],
    header_bytes: int,
    image_start: int,
    load_segment: int,
    binary_data: bytes,
    relocation_locations: set[int],
    assembly: dict[int, list[tuple[int, str]]],
) -> dict:
    if not isinstance(edge, dict):
        raise TypeError("alternate-stream outgoing_calls must be objects")
    address = _hex(edge.get("address"), "outgoing_call.address")
    file_offset = _hex(edge.get("file_offset"), "outgoing_call.file_offset")
    raw_bytes = _bytes(edge.get("bytes_hex"), "outgoing_call.bytes_hex")
    relocation_file_offset = _hex(
        edge.get("relocation_file_offset"), "outgoing_call.relocation_file_offset"
    )
    target_address = _hex(edge.get("target_address"), "outgoing_call.target_address")
    instruction = stream_instructions.get(address)
    if instruction is None or not str(instruction.get("text", "")).upper().startswith(
        "CALLF "
    ):
        raise ValueError(
            f"outgoing far call is not a CALLF instruction at 0x{address:x}"
        )
    if file_offset != header_bytes + address - image_start:
        raise ValueError(f"outgoing far-call mapping is inconsistent at 0x{address:x}")
    if len(raw_bytes) != 5 or raw_bytes[0] != 0x9A:
        raise ValueError(f"outgoing far call has invalid encoding at 0x{address:x}")
    if binary_data[file_offset : file_offset + len(raw_bytes)] != raw_bytes:
        raise ValueError(f"outgoing far-call bytes do not match at 0x{address:x}")
    if _bytes(instruction.get("bytes_hex"), "instruction.bytes_hex") != raw_bytes:
        raise ValueError(
            f"outgoing far call does not match its instruction at 0x{address:x}"
        )

    target_offset = int.from_bytes(raw_bytes[1:3], "little")
    encoded_segment = int.from_bytes(raw_bytes[3:5], "little")
    encoded_target = f"CALLF 0X{encoded_segment:04X}:0X{target_offset:04X}"
    if str(instruction.get("text", "")).strip().upper() != encoded_target:
        raise ValueError(f"outgoing far-call target text disagrees at 0x{address:x}")
    expected_relocation = file_offset + 3
    if (
        relocation_file_offset != expected_relocation
        or relocation_file_offset not in relocation_locations
    ):
        raise ValueError(f"outgoing far call lacks its MZ relocation at 0x{address:x}")

    runtime_segment = (encoded_segment + load_segment) & 0xFFFF
    resolved_target = runtime_segment * 16 + target_offset
    if target_address != resolved_target:
        raise ValueError(f"outgoing far-call target is inconsistent at 0x{address:x}")
    if not any(
        segment == runtime_segment for segment, _ in assembly.get(target_address, [])
    ):
        raise ValueError(
            f"outgoing far call does not target a decoded instruction "
            f"at 0x{target_address:x}"
        )
    return {
        "address": address,
        "file_offset": file_offset,
        "relocation_file_offset": relocation_file_offset,
        "target_address": target_address,
        "runtime_segment": runtime_segment,
    }


def _branch_target(text: str) -> int:
    segmented = re.search(r"0X?([0-9A-F]{1,4}):0X?([0-9A-F]{1,4})$", text)
    if segmented:
        return int(segmented.group(1), 16) * 16 + int(segmented.group(2), 16)
    flat = re.search(r"0X([0-9A-F]{1,5})$", text)
    if flat:
        return int(flat.group(1), 16)
    raise ValueError(f"alternate-stream branch has no direct target: {text}")


def _validate_stream_branches(
    instructions: dict[int, dict],
    instruction_addresses: list[int],
    assembly: dict[int, list[tuple[int, str]]],
    stream_segment: int | None,
    known_instruction_addresses: set[int] | None = None,
) -> None:
    known_addresses = (
        set(instruction_addresses)
        if known_instruction_addresses is None
        else known_instruction_addresses
    ) | set(assembly)
    branch_instructions = []
    for address, entry in instructions.items():
        raw_bytes = _bytes(entry.get("bytes_hex"), "instruction.bytes_hex")
        text = str(entry.get("text", "")).strip().upper()
        opcode_offset = 1 if raw_bytes[0] == 0x2E else 0
        opcode = raw_bytes[opcode_offset] if len(raw_bytes) > opcode_offset else None
        mnemonic = next(
            (word for word in text.split() if word in _BRANCH_MNEMONICS), ""
        )
        if opcode in {0xEB, 0xE9, 0xE0, 0xE1, 0xE2, 0xE3} or (
            opcode is not None and 0x70 <= opcode <= 0x7F
        ):
            branch_instructions.append(
                (address, raw_bytes, text, mnemonic, opcode_offset, opcode)
            )
    if branch_instructions and stream_segment is None:
        raise ValueError("alternate stream with near branches requires code_segment")
    for (
        address,
        raw_bytes,
        text,
        mnemonic,
        opcode_offset,
        opcode,
    ) in branch_instructions:
        if opcode_offset and not text.startswith("CS "):
            raise ValueError(
                f"alternate-stream branch prefix disagrees at 0x{address:x}"
            )
        if opcode_offset == 0 and text.startswith("CS "):
            raise ValueError(
                f"alternate-stream branch prefix disagrees at 0x{address:x}"
            )
        if opcode is not None and 0x70 <= opcode <= 0x7F:
            if mnemonic not in _SHORT_JCC_MNEMONICS[opcode - 0x70]:
                raise ValueError(
                    f"alternate-stream branch opcode disagrees at 0x{address:x}"
                )
            operand_size = 1
        elif opcode == 0xEB and mnemonic == "JMP":
            operand_size = 1
        elif opcode == 0xE9 and mnemonic == "JMP":
            operand_size = 2
        elif opcode in _LOOP_MNEMONICS:
            if mnemonic not in _LOOP_MNEMONICS[opcode]:
                raise ValueError(
                    f"alternate-stream branch opcode disagrees at 0x{address:x}"
                )
            operand_size = 1
        else:
            raise ValueError(
                f"unsupported alternate-stream branch encoding at 0x{address:x}"
            )
        if len(raw_bytes) != opcode_offset + 1 + operand_size:
            raise ValueError(
                f"unsupported alternate-stream branch encoding at 0x{address:x}"
            )
        displacement = int.from_bytes(
            raw_bytes[opcode_offset + 1 :], "little", signed=True
        )
        source_offset = address - stream_segment * 16
        if not 0 <= source_offset <= 0xFFFF:
            raise ValueError(
                f"alternate-stream code_segment does not map 0x{address:x}"
            )
        encoded_target = stream_segment * 16 + (
            (source_offset + len(raw_bytes) + displacement) & 0xFFFF
        )
        if _branch_target(text) != encoded_target:
            raise ValueError(
                f"alternate-stream branch target disagrees at 0x{address:x}"
            )
        if encoded_target not in known_addresses:
            raise ValueError(
                f"alternate-stream branch target is not a decoded instruction "
                f"at 0x{encoded_target:x}"
            )


def _verified_stream(
    stream: object,
    header_bytes: int,
    image_start: int,
    load_segment: int,
    binary_data: bytes,
    assembly: dict[int, list[tuple[int, str]]],
    known_alternate_instruction_addresses: set[int] | None = None,
) -> dict | None:
    if not isinstance(stream, dict):
        raise TypeError("each alternate-stream record must be an object")
    status = stream.get("status")
    if not isinstance(status, str) or status not in {
        "verified",
        "pending_review",
        "rejected",
    }:
        raise ValueError(f"invalid alternate-stream status {status!r}")
    if status != "verified":
        return None

    address = _hex(stream.get("address"), "address")
    file_offset = _hex(stream.get("file_offset"), "file_offset")
    if file_offset != header_bytes + address - image_start:
        raise ValueError(
            f"alternate-stream address/file offset mapping is inconsistent "
            f"at 0x{address:x}"
        )
    stream_bytes = _bytes(stream.get("bytes_hex"), "bytes_hex")
    if (
        file_offset + len(stream_bytes) > len(binary_data)
        or binary_data[file_offset : file_offset + len(stream_bytes)] != stream_bytes
    ):
        raise ValueError(f"alternate-stream bytes do not match at 0x{address:x}")
    instruction_addresses = _instructions(
        stream, address, header_bytes, image_start, binary_data, stream_bytes
    )
    instruction_entries = {
        _hex(entry["address"], "instruction.address"): entry
        for entry in stream["instructions"]
    }
    overlapping_entries = stream.get("overlapping_entries", [])
    if not isinstance(overlapping_entries, list):
        raise TypeError("alternate-stream overlapping_entries must be an array")
    all_instruction_addresses = list(instruction_addresses)
    primary_instruction_addresses = set(instruction_addresses)
    stream_end = address + len(stream_bytes)
    raw_join_address = stream.get("join_address")
    join_address = (
        _hex(raw_join_address, "join_address") if raw_join_address is not None else None
    )
    if join_address is not None and (
        stream_end != join_address or join_address not in assembly
    ):
        raise ValueError(
            f"alternate-stream join is not an exported boundary at 0x{join_address:x}"
        )
    for overlapping_entry in overlapping_entries:
        if not isinstance(overlapping_entry, dict):
            raise TypeError("alternate-stream overlapping entries must be objects")
        entry_address = _hex(
            overlapping_entry.get("address"), "overlapping_entry.address"
        )
        entry_bytes = _bytes(
            overlapping_entry.get("bytes_hex"), "overlapping_entry.bytes_hex"
        )
        if (
            entry_address <= address
            or entry_address >= stream_end
            or entry_address + len(entry_bytes) > stream_end
            or entry_address in primary_instruction_addresses
        ):
            raise ValueError(
                f"alternate-stream entry at 0x{entry_address:x} does not overlap "
                f"an instruction"
            )
        raw_entry_join = overlapping_entry.get("join_address")
        if raw_entry_join is not None:
            entry_join = _hex(raw_entry_join, "overlapping_entry.join_address")
            if (
                entry_address + len(entry_bytes) != entry_join
                or entry_join not in primary_instruction_addresses
            ):
                raise ValueError(
                    f"overlapping entry at 0x{entry_address:x} does not join "
                    "a primary instruction boundary"
                )
        _instructions(
            overlapping_entry,
            entry_address,
            header_bytes,
            image_start,
            binary_data,
            entry_bytes,
        )
        for entry in overlapping_entry["instructions"]:
            instruction_address = _hex(entry["address"], "instruction.address")
            existing = instruction_entries.get(instruction_address)
            if existing is not None and existing != entry:
                raise ValueError(
                    f"alternate-stream instruction conflicts at "
                    f"0x{instruction_address:x}"
                )
            instruction_entries[instruction_address] = entry
            if instruction_address not in all_instruction_addresses:
                all_instruction_addresses.append(instruction_address)
    raw_code_segment = stream.get("code_segment")
    code_segment = (
        _hex(raw_code_segment, "code_segment") if raw_code_segment is not None else None
    )
    if code_segment is not None and code_segment > 0xFFFF:
        raise ValueError("alternate-stream code_segment must fit in 16 bits")
    if code_segment is not None:
        near_call_segments = {
            segment
            for edge in stream.get("source_edges", [])
            if isinstance(edge, dict)
            and _bytes(edge.get("bytes_hex"), "source_edge.bytes_hex")[:1] == b"\xe8"
            for segment, instruction in assembly.get(
                _hex(edge.get("address"), "source_edge.address"), []
            )
            if instruction == str(edge.get("instruction", "")).strip().upper()
        }
        if near_call_segments and code_segment not in near_call_segments:
            raise ValueError(
                f"alternate-stream code_segment disagrees with its near-call source "
                f"at 0x{address:x}"
            )
    _validate_stream_branches(
        instruction_entries,
        all_instruction_addresses,
        assembly,
        code_segment,
        set(all_instruction_addresses)
        | (known_alternate_instruction_addresses or set()),
    )
    verified_by = stream.get("verified_by")
    methods = stream.get("verification_methods")
    if not isinstance(verified_by, str) or not verified_by.strip():
        raise ValueError(f"alternate stream at 0x{address:x} lacks verifier")
    if (
        not isinstance(methods, list)
        or not methods
        or not all(isinstance(method, str) and method.strip() for method in methods)
    ):
        raise ValueError(
            f"alternate stream at 0x{address:x} lacks verification methods"
        )
    source_edges = stream.get("source_edges")
    if not isinstance(source_edges, list) or not source_edges:
        raise ValueError(f"alternate stream at 0x{address:x} lacks source edges")
    verified_edges = [
        _source_edge(
            edge,
            address,
            header_bytes,
            image_start,
            binary_data,
            assembly,
            set(all_instruction_addresses),
            code_segment,
        )
        for edge in source_edges
    ]
    indirect_edges = [
        edge for edge in verified_edges if edge.get("transfer_kind") == "far_indirect"
    ]
    pointer = stream.get("indirect_pointer")
    if bool(indirect_edges) != isinstance(pointer, dict):
        raise ValueError(
            f"alternate stream at 0x{address:x} has incomplete indirect-pointer evidence"
        )
    if indirect_edges:
        _validate_indirect_pointer(
            pointer,
            address,
            indirect_edges,
            header_bytes,
            image_start,
            binary_data,
            assembly,
        )
    outgoing_calls = stream.get("outgoing_calls", [])
    if not isinstance(outgoing_calls, list):
        raise TypeError("alternate-stream outgoing_calls must be an array")
    far_call_addresses = {
        instruction_address
        for instruction_address, entry in instruction_entries.items()
        if str(entry.get("text", "")).strip().upper().startswith("CALLF ")
    }
    outgoing_by_address = {
        _hex(edge.get("address"), "outgoing_call.address"): edge
        for edge in outgoing_calls
        if isinstance(edge, dict)
    }
    if len(outgoing_by_address) != len(outgoing_calls):
        raise ValueError(
            "alternate-stream outgoing_calls contain invalid or duplicate entries"
        )
    if set(outgoing_by_address) != far_call_addresses:
        raise ValueError(
            f"alternate stream at 0x{address:x} must record every direct far call"
        )
    relocation_locations = (
        _mz_relocation_locations(binary_data, header_bytes) if outgoing_calls else set()
    )
    verified_calls = [
        _outgoing_far_call(
            edge,
            instruction_entries,
            header_bytes,
            image_start,
            load_segment,
            binary_data,
            relocation_locations,
            assembly,
        )
        for edge in outgoing_calls
    ]
    return {
        "address": address,
        "instruction_addresses": all_instruction_addresses,
        "file_offset": file_offset,
        "binary_sha256": "",
        "verified_by": verified_by.strip(),
        "source_edges": verified_edges,
        "outgoing_calls": verified_calls,
        "code_segment": code_segment,
        "join_address": join_address,
    }


def load_binary_evidence(
    target_root: pathlib.Path, manifest: dict
) -> tuple[bytes, int, int, str]:
    """Oracle: repository-contained binary hash and explicit real-mode mapping."""
    schema_version = (
        manifest.get("schema_version") if isinstance(manifest, dict) else None
    )
    if (
        not isinstance(schema_version, int)
        or isinstance(schema_version, bool)
        or schema_version != 1
    ):
        raise ValueError("unsupported alternate-stream manifest")
    binary = manifest.get("binary")
    mapping = manifest.get("image_mapping")
    if not isinstance(binary, dict) or not isinstance(mapping, dict):
        raise TypeError("alternate-stream binary and image_mapping must be objects")

    binary_path = _repository_file(target_root, binary.get("path"))
    expected_hash = binary.get("sha256")
    if not isinstance(expected_hash, str) or not re.fullmatch(
        r"[0-9a-f]{64}", expected_hash
    ):
        raise ValueError("alternate-stream binary.sha256 must be a lowercase SHA-256")
    binary_data = binary_path.read_bytes()
    if hashlib.sha256(binary_data).hexdigest() != expected_hash:
        raise ValueError(f"alternate-stream evidence is stale for binary {binary_path}")
    load_segment = _hex(mapping.get("load_segment"), "load_segment")
    if load_segment > 0xFFFF:
        raise ValueError("alternate-stream load_segment must fit in 16 bits")
    header_bytes = mapping.get("header_bytes")
    if (
        not isinstance(header_bytes, int)
        or isinstance(header_bytes, bool)
        or header_bytes < 0
    ):
        raise ValueError("alternate-stream header_bytes must be a non-negative integer")
    return binary_data, header_bytes, load_segment, expected_hash


def load_verified_streams(target_root: pathlib.Path) -> list[dict]:
    manifest_path = target_root / "alternate_streams.json"
    if not manifest_path.is_file():
        return []
    manifest = json.loads(manifest_path.read_text(errors="replace"))
    binary_data, header_bytes, load_segment, expected_hash = load_binary_evidence(
        target_root, manifest
    )
    streams = manifest.get("streams")
    if not isinstance(streams, list):
        raise TypeError("alternate-stream streams must be an array")
    image_start = load_segment * 16
    assembly = _assembly_instructions(target_root)
    known_alternate_instruction_addresses = set()
    for stream in streams:
        if not isinstance(stream, dict) or stream.get("status") != "verified":
            continue
        instruction_groups = [stream.get("instructions", [])]
        overlapping_entries = stream.get("overlapping_entries", [])
        if isinstance(overlapping_entries, list):
            instruction_groups.extend(
                entry.get("instructions", [])
                for entry in overlapping_entries
                if isinstance(entry, dict)
            )
        for entries in instruction_groups:
            if not isinstance(entries, list):
                continue
            known_alternate_instruction_addresses.update(
                _hex(entry["address"], "instruction.address")
                for entry in entries
                if isinstance(entry, dict) and "address" in entry
            )
    validated = []
    for stream in streams:
        result = _verified_stream(
            stream,
            header_bytes,
            image_start,
            load_segment,
            binary_data,
            assembly,
            known_alternate_instruction_addresses,
        )
        if result is not None:
            result["binary_sha256"] = expected_hash
            validated.append(result)
    for stream in validated:
        for edge in stream["source_edges"]:
            if edge.get("transfer_kind") == "near_register":
                _validate_register_call(
                    edge,
                    target_root,
                    header_bytes,
                    image_start,
                    binary_data,
                    assembly,
                    streams,
                )
    return validated
