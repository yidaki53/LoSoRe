"""Generic composition of verified external calls into routine-trace evidence."""

from __future__ import annotations

import pathlib
import re
from typing import Any

from engine import knowledge, matrix, routine_contract, target_packet
from tools import asmcfg

_CALL_REL16 = b"\xe8"
_JMP_SHORT = b"\xeb"
_JMP_REL16 = b"\xe9"
_CALL_FAR = b"\x9a"
_JMP_FAR = b"\xea"


def _verified(target: str, root: pathlib.Path) -> set[str]:
    store = root / "knowledge" / "knowledge.json"
    if not store.is_file():
        return set()
    data = knowledge.load(store)
    result: set[str] = set()
    for names in data.get("targets", {}).get(target, {}).get("verified", {}).values():
        result.update(names)
    return result


def _linear(address: str | None) -> int | None:
    if not address:
        return None
    match = re.fullmatch(r"(?:0x)?([0-9a-f]{1,4}):(?:0x)?([0-9a-f]{1,4})", address, re.I)
    if match is None:
        return None
    return (int(match.group(1), 16) << 4) + int(match.group(2), 16)


def _parse(root: pathlib.Path, target: str, routine: str) -> dict:
    path = root / "targets" / target / "asm" / f"{routine}.s"
    if not path.is_file():
        raise ValueError(f"missing assembly for composed routine: {routine}")
    return asmcfg.parse_ghidra_asm(path.read_text(errors="replace"))


def _raw(root: pathlib.Path, target: str, routine: str) -> bytes:
    evidence = target_packet.evidence_for_routine(
        root, target, routine, compose=False
    )
    return bytes.fromhex(evidence["bytes"]["hex"])


def _return_info(instructions: list[str]) -> tuple[bool, int, int]:
    returns = [
        (index, match)
        for index, instruction in enumerate(instructions)
        if (match := re.fullmatch(
            r"\b(RETF|RET)(?:\s+(?:0x)?([0-9a-f]+))?\b",
            instruction,
            re.I,
        )) is not None
    ]
    if not returns:
        raise ValueError("composed routine must have a return")
    index, match = returns[0]
    near = match.group(1).upper() == "RET"
    cleanup = int(match.group(2), 16) if match.group(2) else 0
    return near, cleanup, index


def _declaration(root: pathlib.Path, target: str, routine: str,
                 instructions: list[str], return_index: int) -> str:
    signed = routine_contract._signed_frame_params(instructions)
    cleanup = 0
    match = re.fullmatch(
        r"\b(?:RETF|RET)(?:\s+(?:0x)?([0-9a-f]+))?\b",
        instructions[return_index],
        re.I,
    )
    if match is not None and match.group(1):
        cleanup = int(match.group(1), 16)
    params = "; ".join(
        f"param_{index}: {'Integer' if index in signed else 'Word'}"
        for index in range(1, cleanup // 2 + 1)
    )
    signature = f"procedure {routine}({params});" if params else (
        f"procedure {routine};"
    )
    if routine_contract._returns_ax_value(instructions[:return_index + 1]):
        signature = signature.replace("procedure ", "function ", 1)
        signature = signature.rstrip(";") + ": Word;"
    return signature


def _byte_ranges(parsed: dict, raw: bytes, routine: str,
                 inventory: dict) -> dict[int, int]:
    entry = next(
        (item.get("entry") for item in inventory.get("functions", [])
         if item.get("name") == routine),
        None,
    )
    start = _linear(entry)
    if start is None or not parsed["addrs"]:
        raise ValueError(f"cannot map assembly bytes for {routine}")
    result: dict[int, int] = {}
    for index, address in enumerate(parsed["addrs"]):
        next_address = (
            parsed["addrs"][index + 1]
            if index + 1 < len(parsed["addrs"])
            else start + len(raw)
        )
        length = next_address - address
        if length <= 0 or address - start + length > len(raw):
            raise ValueError(f"invalid assembly byte range for {routine}")
        result[index] = length
    return result


def _patch_branch(raw: bytes, offset: int, length: int, label: str,
                  far: bool) -> list[str]:
    opcode = raw[offset]
    if far and opcode in _CALL_FAR + _JMP_FAR:
        return [
            f".byte 0x{opcode:02x}",
            f".word {label}",
            ".word 0x191",
        ]
    if opcode == 0xEB and length == 2:
        return [".byte 0xeb", f".byte {label} - . - 1"]
    if opcode in (0xE8, 0xE9) and length == 3:
        return [f".byte 0x{opcode:02x}", f".word {label} - ."]
    raise ValueError(f"unsupported external transfer encoding: 0x{opcode:02x}")


def compose(root: pathlib.Path, target: str, routine: str) -> dict[str, Any] | None:
    if target != "liero":
        return None
    root = pathlib.Path(root)
    caller = _parse(root, target, routine)
    if not caller["insts"]:
        return None
    external: list[tuple[int, int]] = []
    for index, instruction in enumerate(caller["insts"]):
        if not (asmcfg.is_call(instruction) or asmcfg.is_branch(instruction)):
            continue
        address = caller["addrs"][index]
        if address not in caller["addrs"]:
            continue
        transfer = asmcfg.resolve_branch_target(instruction, caller["segments"][index])
        if transfer is not None and transfer not in caller["addrs"]:
            external.append((index, transfer))
    if not external:
        return None
    verified = _verified(target, root)
    inventory = matrix.load_inventory(target, root)
    blocks: list[dict[str, Any]] = []

    caller_raw = _raw(root, target, routine)
    blocks.append({
        "routine": routine,
        "parsed": caller,
        "raw": caller_raw,
        "entry": caller["addrs"][0],
        "suffix": 0,
    })

    for _, transfer in external:
        candidates = []
        for item in inventory.get("functions", []):
            name = item.get("name")
            if name not in verified or name == routine:
                continue
            parsed = _parse(root, target, name)
            if transfer in parsed["addrs"]:
                candidates.append((name, parsed))
        if len(candidates) != 1:
            return None
        callee, parsed = candidates[0]
        if any(block["routine"] == callee for block in blocks):
            continue
        start_index = parsed["addrs"].index(transfer)
        raw = _raw(root, target, callee)
        blocks.append({
            "routine": callee,
            "parsed": parsed,
            "raw": raw,
            "entry": parsed["addrs"][start_index],
            "suffix": start_index,
        })

    instructions: list[str] = []
    addresses: list[int] = []
    segments: list[int] = []
    for block in blocks:
        start = block["suffix"]
        instructions.extend(block["parsed"]["insts"][start:])
        addresses.extend(block["parsed"]["addrs"][start:])
        segments.extend(block["parsed"]["segments"][start:])

    try:
        near, cleanup, return_index = _return_info(instructions)
        declaration = _declaration(root, target, routine, instructions, return_index)
    except ValueError:
        return None

    label_by_address = {
        address: f"composedBlock{index}"
        for index, block in enumerate(blocks[1:], 1)
        for address in block["parsed"]["addrs"][block["suffix"]:]
    }
    asm_lines: list[str] = []
    image = bytearray()
    instruction_offsets: list[int] = []
    for block_index, block in enumerate(blocks):
        if block_index:
            asm_lines.append(f"composedBlock{block_index}:")
        parsed = block["parsed"]
        raw = block["raw"]
        ranges = _byte_ranges(parsed, raw, block["routine"], inventory)
        entry = parsed["addrs"][0]
        cursor = 0
        for index, instruction in enumerate(parsed["insts"][block["suffix"]:], block["suffix"]):
            offset = parsed["addrs"][index] - entry
            length = ranges[index]
            start = len(image)
            transfer = None
            if asmcfg.is_call(instruction) or asmcfg.is_branch(instruction):
                transfer = asmcfg.resolve_branch_target(
                    instruction, parsed["segments"][index]
                )
            if (
                transfer is not None
                and transfer in label_by_address
                and transfer not in parsed["addrs"]
            ):
                far = bool(re.match(r"^(CALLF|JMPF)\b", instruction, re.I))
                asm_lines.extend(
                    _patch_branch(raw, offset, length, label_by_address[transfer], far)
                )
                image.extend(bytes([raw[offset]]) + bytes(max(0, length - 1)))
            else:
                encoded = raw[offset:offset + length]
                asm_lines.append(
                    ".byte " + ", ".join(
                        f"0x{byte:02x}" for byte in encoded
                    )
                )
                image.extend(encoded)
            instruction_offsets.append(start)
            cursor = offset + length
        if cursor != len(raw):
            encoded = raw[cursor:]
            asm_lines.append(
                ".byte " + ", ".join(
                    f"0x{byte:02x}" for byte in encoded
                )
            )
            image.extend(encoded)

    return {
        "instructions": instructions,
        "addresses": addresses,
        "segments": segments,
        "assembly_text": "\n".join(
            f"{address:04x}:{segment:04x}  {instruction}"
            for address, segment, instruction in zip(addresses, segments, instructions)
        ),
        "raw_hex": image.hex(),
        "instruction_offsets": instruction_offsets,
        "raw_asm": "\n".join(asm_lines),
        "declaration": declaration,
        "near": near,
        "cleanup": cleanup,
        "return_index": return_index,
        "callees": [block["routine"] for block in blocks[1:]],
    }
