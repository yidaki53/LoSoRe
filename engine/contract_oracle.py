"""Decomp/contract-derived original-trace oracle for safe Liero routines."""

from __future__ import annotations

import hashlib
import json
import pathlib
import random
import re
import shutil
import struct
import subprocess
from typing import Any

from engine import asm_emulator, routine_contract, target_packet
from tools import asmcfg
from tools import liero_four_routine_pilot as pilot
from tools import liero_source_trial as trial
from tools.liero_file_probe import assemble_probe, run_dosbox

ARENA = 4096
HOST_SEGMENT = 0x191
CASE_BYTES = 8 + ARENA
RECORD_BYTES = 32 + ARENA
FIXTURE_BP = 0x6789
_UNSAFE = re.compile(r"\b(CALLF?|INT|INTO|IN|OUT|LOOP\w*|IRET)\b", re.I)
_ABSOLUTE = re.compile(
    r"(?:(?:DS|ES)\s*:\s*)?\[\s*(?:0X)?[0-9A-F]{1,4}\s*\]", re.I
)
_RET = re.compile(r"\b(RETF|RET)(?:\s+(?:0x)?([0-9a-f]+))?\b", re.I)
_DECL = re.compile(
    r"^(procedure|function)\s+(\w+)"
    r"(?:\s*\((.*)\))?"
    r"\s*(?::\s*([\w^]+))?\s*;$",
    re.I,
)
_SIZES = {
    "byte": 2,
    "char": 2,
    "integer": 2,
    "word": 2,
    "boolean": 2,
    "longint": 4,
    "pointer": 2,
    "pbyte": 2,
}
_POINTERS = {"pointer", "pbyte"}


def _contract(root: pathlib.Path, target: str, routine: str) -> dict[str, Any]:
    if target != "liero":
        raise ValueError("contract oracle supports only liero")
    path = root / "targets" / target / "config" / "routine_contracts.json"
    data = json.loads(path.read_text())
    contract = data.get("functions", {}).get(routine)
    if not isinstance(contract, dict):
        raise ValueError(f"no checked contract for routine: {routine}")
    return contract


def _declaration(root: pathlib.Path, target: str, routine: str) -> str:
    contract = _contract(root, target, routine)
    declaration = contract.get("declaration")
    if not isinstance(declaration, str):
        raise ValueError(f"contract declaration missing for routine: {routine}")
    if not _DECL.fullmatch(declaration.strip()):
        raise ValueError(f"unsupported contract declaration: {declaration}")
    path = root / "targets" / target / "decomp" / f"{routine}.c"
    decomp = path.read_text(errors="replace")
    if routine not in decomp:
        raise ValueError(f"decompilation does not contain routine: {routine}")
    return declaration.strip()


def _fixture_declaration(
    root: pathlib.Path, target: str, routine: str
) -> tuple[dict[str, Any] | None, str, str]:
    if target != "liero":
        raise ValueError("contract oracle supports only liero")
    try:
        contract = _contract(root, target, routine)
        return contract, _declaration(root, target, routine), "reviewed"
    except (OSError, ValueError):
        if routine_contract.load_contract(root / "targets" / target, routine) is not None:
            raise
    declaration = routine_contract.derived_declaration(
        root / "targets" / target, routine
    )
    if declaration is None or _DECL.fullmatch(declaration.strip()) is None:
        raise ValueError(f"no checked oracle declaration for routine: {routine}")
    return None, declaration.strip(), "derived"


def _parse_declaration(declaration: str) -> dict[str, Any]:
    match = _DECL.fullmatch(declaration.strip())
    if match is None:
        raise ValueError(f"unsupported contract declaration: {declaration}")
    kind, name, params_text, return_text = match.groups()
    params = []
    if params_text and params_text.strip():
        for group in params_text.split(";"):
            names_text, type_text = (part.strip() for part in group.split(":", 1))
            type_name = type_text.lower().strip()
            if type_name not in _SIZES:
                raise ValueError(f"unsupported contract parameter type: {type_text}")
            for param_name in (part.strip() for part in names_text.split(",")):
                if not re.fullmatch(r"\w+", param_name):
                    raise ValueError(f"unsupported contract parameter name: {param_name}")
                params.append({"name": param_name, "type": type_name})
    return_type = None
    if kind.lower() == "function":
        return_type = (return_text or "").lower().strip() or "word"
        if return_type not in _SIZES:
            raise ValueError(f"unsupported contract return type: {return_text}")
    return {
        "kind": kind.lower(),
        "name": name,
        "params": params,
        "return_type": return_type,
    }


def _derived_absolute_memory_words(instructions: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    pattern = re.compile(r"^MOV\s+BP\s*,\s*(?:WORD PTR\s+)?(?:DS\s*:\s*)?\[\s*0X([0-9A-F]+)\s*\]$", re.I)
    for instruction in instructions:
        match = pattern.fullmatch(instruction.strip())
        if match is not None:
            result[hex(int(match.group(1), 16))] = "0x8000"
    return result


def _derived_memory_register_masks(instructions: list[str]) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for instruction in instructions:
        for expression in re.findall(r"\[([^\]]+)\]", instruction.upper()):
            displacement = 0
            for sign, token in re.findall(
                r"([+-]?)\s*(0X[0-9A-F]+|\d+)", expression
            ):
                value = int(token, 16) if token.startswith("0X") else int(token)
                displacement += -value if sign == "-" else value
            if "BP" in expression:
                for register, index in (("SI", 1), ("DI", 2)):
                    if register in expression:
                        base = (0x8000 - (FIXTURE_BP + displacement)) & 0xFFFF
                        result.setdefault(str(index), ("0x07ff", hex(base)))
            elif "BX" in expression:
                base = (0x8000 - displacement) & 0xFFFF
                result.setdefault("1", ("0x0fff", hex(base)))
    return result


def _derived_code_memory_windows(
    instructions: list[str], raw_hex: str
) -> list[dict[str, int]]:
    raw = bytes.fromhex(raw_hex)
    segment_names = ("ES", "CS", "SS", "DS")
    register_names = ("AX", "CX", "DX", "BX", "SP", "BP", "SI", "DI")
    cs_registers: set[str] = set()
    code_segments: set[str] = set()
    for offset in range(len(raw) - 1):
        opcode, modrm = raw[offset], raw[offset + 1]
        if modrm & 0xC0 != 0xC0:
            continue
        segment = segment_names[(modrm >> 3) & 3]
        register = register_names[modrm & 7]
        if opcode == 0x8C and segment == "CS":
            cs_registers.add(register)
        elif opcode == 0x8E and register in cs_registers:
            code_segments.add(segment)
    if "DS" not in code_segments and "ES" not in code_segments:
        return []
    source_offset: int | None = None
    immediate: int | None = None
    count: int | None = None
    for instruction in instructions:
        text = instruction.strip()
        load = re.fullmatch(
            r"MOV\s+AX\s*,\s*(?:WORD PTR\s+)?(?:0X)?([0-9A-F]+)", text, re.I
        )
        if load is not None:
            immediate = int(load.group(1), 16)
            continue
        if re.fullmatch(r"XCHG\s+AX\s*,\s*SI", text, re.I) and immediate is not None:
            source_offset = immediate
            continue
        rep_count = re.fullmatch(
            r"MOV\s+CX\s*,\s*(?:0X)?([0-9A-F]+)", text, re.I
        )
        if rep_count is not None:
            count = int(rep_count.group(1), 16)
            continue
        string_op = re.fullmatch(r"MOVS(B|W)\.REP\s+ES:DI\s*,\s*SI", text, re.I)
        if (
            string_op is not None
            and source_offset is not None
            and count is not None
            and "DS" in code_segments
        ):
            byte_count = count * (2 if string_op.group(1).upper() == "W" else 1)
            return [{
                "code_offset": source_offset,
                "arena_offset": 0x0F00,
                "byte_count": byte_count,
            }]
    return []


def fixture(root: pathlib.Path, target: str, routine: str) -> dict[str, Any]:
    from engine import capability_proposer

    root = pathlib.Path(root)
    evidence = target_packet.evidence_for_routine(root, target, routine)
    composed = evidence.get("composed")
    if composed is not None:
        contract = None
        declaration = composed["declaration"]
        declaration_source = "derived-composed"
        insts = list(evidence["static_evidence"]["assembly"]["instructions"])
        asm = composed["assembly_text"]
        near = composed["near"]
        cleanup = composed["cleanup"]
        raw_asm = composed["raw_asm"]
        code_memory_windows = _derived_code_memory_windows(
            insts, evidence["bytes"]["hex"]
        )
    parsed_asm: dict[str, Any] | None = None
    if composed is None:
        contract, declaration, declaration_source = _fixture_declaration(
            root, target, routine
        )
        asm_path = root / "targets" / target / "asm" / f"{routine}.s"
        asm = asm_path.read_text(errors="replace")
        parsed_asm = asmcfg.parse_ghidra_asm(asm)
        insts = parsed_asm["insts"]
        raw_asm = None
        if (
            _UNSAFE.search(asm)
            or not asmcfg.bounded_branch_paths(parsed_asm)
            or (
                declaration_source in {"derived", "derived-composed"}
                and routine_contract.unsafe_absolute_memory(
                    insts, allow_data_segment=routine_contract.absolute_memory_mode(insts)
                )
            )
        ):
            raise ValueError(f"routine is not a safe contract-oracle leaf: {routine}")
        returns = _RET.findall(asm)
        if len(returns) != 1 or len(re.findall(r"\bRET(?:F)?\b", asm, re.I)) != 1:
            raise ValueError(f"contract oracle requires one return: {routine}")
        near = returns[0][0].upper() == "RET"
        cleanup = int(returns[0][1], 16) if returns[0][1] else 0
        code_memory_windows = _derived_code_memory_windows(
            insts, evidence["bytes"]["hex"]
        )
    declaration_info = _parse_declaration(declaration)
    absolute_memory = declaration_source in {"derived", "derived-composed"} and (
        routine_contract.absolute_memory_mode(insts)
    )
    if absolute_memory and any(
        item["type"] in _POINTERS for item in declaration_info["params"]
    ):
        raise ValueError(f"absolute memory fixture cannot use pointer arguments: {routine}")
    raw = bytes.fromhex(evidence["bytes"]["hex"])
    if not raw:
        raise ValueError(f"contract oracle routine has no bytes: {routine}")
    args_bytes = sum(_SIZES[item["type"]] for item in declaration_info["params"])
    if declaration_source in {"derived", "derived-composed"}:
        evidence_assembly = (evidence.get("static_evidence") or {}).get("assembly") or {}
        asm_addresses = evidence_assembly.get("addresses") or (
            parsed_asm["addrs"] if parsed_asm is not None else []
        )
        asm_segments = evidence_assembly.get("segments") or (
            parsed_asm["segments"] if parsed_asm is not None else []
        )
        capability_rules = [
            rule
            for _, rule in capability_proposer.propose_for_evidence(
                root, evidence, include_hardware=False
            )
        ]
        emu_evidence = {
            "bytes": evidence["bytes"],
            "capability_rules": capability_rules,
            "static_evidence": {
                "assembly": {
                    "instructions": insts,
                    "addresses": asm_addresses,
                    "segments": asm_segments,
                },
                "raw_byte_facts": (
                    evidence.get("static_evidence", {}).get("raw_byte_facts", {})
                ),
            },
            "oracle_contract": {"declaration": declaration},
        }
        if not asm_emulator.supported(emu_evidence):
            raise ValueError(f"derived oracle declaration is not emulatable: {routine}")
    contract_fields = contract or {}
    register_masks = dict(contract_fields.get("register_masks", {}))
    register_bases = dict(contract_fields.get("register_bases", {}))
    memory_words = dict(contract_fields.get("memory_words", {}))
    if absolute_memory and declaration_source in {"derived", "derived-composed"}:
        for offset, value in _derived_absolute_memory_words(insts).items():
            memory_words.setdefault(offset, value)
    nonzero_low_bytes = declaration_source in {"derived", "derived-composed"} and any(
        inst.upper().startswith("DIV") for inst in insts
    )
    undefined_arithmetic_flags = declaration_source in {"derived", "derived-composed"} and any(
        inst.upper().startswith(("AAM", "AAD")) for inst in insts
    )
    has_branches = any(asmcfg.is_branch(inst) for inst in insts)
    if absolute_memory and declaration_source in {"derived", "derived-composed"}:
        register_masks.setdefault("1", "0x0fff")
        register_masks.setdefault("2", "0x0fff")
    elif declaration_source in {"derived", "derived-composed"} and (
        routine_contract.string_destination_mode(insts)
    ):
        register_masks.setdefault("2", "0x0eff" if code_memory_windows else "0x0fff")
        register_bases.setdefault("2", "0x8000")
    elif declaration_source in {"derived", "derived-composed"}:
        for index_text, (mask, base) in _derived_memory_register_masks(insts).items():
            register_masks.setdefault(index_text, mask)
            register_bases.setdefault(index_text, base)
    if nonzero_low_bytes:
        for index in range(4):
            register_masks.setdefault(str(index), "0x00ff")
    return {
        "target": target,
        "routine": routine,
        "declaration": declaration,
        "declaration_source": declaration_source,
        "kind": declaration_info["kind"],
        "name": declaration_info["name"],
        "params": declaration_info["params"],
        "return_type": declaration_info["return_type"],
        "args_bytes": args_bytes,
        "bytes": raw.hex(),
        "bytes_sha256": hashlib.sha256(raw).hexdigest(),
        "raw_asm": raw_asm,
        "code_memory_windows": code_memory_windows,
        "absolute_memory": absolute_memory,
        "near": near,
        "cleanup": cleanup,
        "flag_mask": contract_fields.get(
            "flag_mask",
            0
            if declaration_source in {"derived", "derived-composed"}
            and (absolute_memory or undefined_arithmetic_flags or has_branches)
            else 0x441,
        ),
        "register_inputs": contract_fields.get("register_inputs", {}),
        "argument_masks": contract_fields.get("argument_masks", {}),
        "register_masks": register_masks,
        "register_bases": register_bases,
        "memory_words": memory_words,
        "nonzero_low_bytes": nonzero_low_bytes,
    }


def supported(root: pathlib.Path, target: str, routine: str) -> bool:
    try:
        fixture(root, target, routine)
    except Exception:
        return False
    return True


def cases(fixture_data: dict[str, Any], suite: str) -> list[bytes]:
    if suite not in {"training", "terminal"}:
        raise ValueError(f"unknown suite: {suite}")
    rng = random.Random(20261123 + (suite == "terminal"))
    result: list[bytes] = []
    for _ in range(56):
        words = [rng.randrange(65536) for _ in range(4)]
        for index_text, mask in fixture_data.get("register_masks", {}).items():
            index = int(index_text)
            if 0 <= index < len(words):
                limit = int(mask, 0) if isinstance(mask, str) else int(mask)
                words[index] &= limit
        for index_text, base in fixture_data.get("register_bases", {}).items():
            index = int(index_text)
            if 0 <= index < len(words):
                offset = int(base, 0) if isinstance(base, str) else int(base)
                words[index] = (words[index] + offset) & 0xFFFF
        if fixture_data.get("nonzero_low_bytes"):
            words = [word | 1 if word & 0xFF == 0 else word for word in words]
        for arg_index, arg in enumerate(fixture_data["params"]):
            if arg["type"] in _POINTERS:
                words[arg_index % 4] = 0x8200 + rng.randrange(128)
        flags = rng.randrange(65536)
        arena = bytearray(flags.to_bytes(2, "little")) + bytearray(rng.randbytes(ARENA - 2))
        for offset_text, value_text in fixture_data.get("memory_words", {}).items():
            offset = int(offset_text, 0) if isinstance(offset_text, str) else int(offset_text)
            value = int(value_text, 0) if isinstance(value_text, str) else int(value_text)
            if offset < 0 or offset + 1 >= ARENA:
                raise ValueError("contract memory word outside owned arena")
            arena[offset] = value & 0xff
            arena[offset + 1] = (value >> 8) & 0xff
        result.append(struct.pack("<4H", *words) + bytes(arena))
    return result


def corpus_hash(fixture_data: dict[str, Any], suite: str) -> str:
    return hashlib.sha256(b"".join(cases(fixture_data, suite))).hexdigest()


def _word_at(data: bytes, index: int) -> int:
    if index < 4:
        return struct.unpack_from("<H", data, index * 2)[0]
    offset = 8 + (index - 4) * 2
    if offset + 2 > len(data):
        raise ValueError("contract case has too few argument words")
    return struct.unpack_from("<H", data, offset)[0]


def _argument_values(fixture_data: dict[str, Any], data: bytes) -> list[tuple[int, str]]:
    values = []
    index = 0
    for arg in fixture_data["params"]:
        type_name = arg["type"]
        if type_name == "longint":
            low = _word_at(data, index)
            high = _word_at(data, index + 1)
            index += 2
            values.append((low | (high << 16), type_name))
            continue
        value = _word_at(data, index)
        mask = fixture_data.get("argument_masks", {}).get(str(index))
        if mask is not None:
            value &= int(mask, 0) if isinstance(mask, str) else int(mask)
        index += 1
        if type_name in _POINTERS:
            if not 0x8000 <= value <= 0x9000 - 32:
                raise ValueError("contract pointer argument outside owned arena")
        values.append((value, type_name))
    return values


def _push_args(values: list[tuple[int, str]]) -> str:
    lines = []
    for value, type_name in reversed(values):
        if type_name in _POINTERS:
            lines.append("push %cs")
            lines.append(f"pushw ${value}")
        elif type_name == "longint":
            lines.append(f"pushw ${(value >> 16) & 0xffff}")
            lines.append(f"pushw ${value & 0xffff}")
        else:
            lines.append(f"pushw ${value & 0xffff}")
    return "\n    ".join(lines)


def _call_arg(value: int | str, type_name: str) -> str:
    if type_name in _POINTERS:
        return f"@arena[{value} - $8000]"
    if type_name == "longint":
        return f"LongInt({value})"
    if type_name == "byte":
        return f"Byte(LongInt({value}) and $ff)"
    if type_name == "char":
        return f"Chr(LongInt({value}) and $ff)"
    if type_name == "integer":
        return f"Integer(Word(LongInt({value}) and $ffff))"
    return f"Word(LongInt({value}) and $ffff)"


def harness(fixture_data: dict[str, Any]) -> str:
    sample = cases(fixture_data, "training")[0]
    raw = ", ".join(
        "0x" + fixture_data["bytes"][index:index + 2]
        for index in range(0, len(fixture_data["bytes"]), 2)
    )
    raw_block = fixture_data.get("raw_asm") or f"    .byte {raw}"
    return_bytes = 2 if fixture_data["near"] else 4
    call_prefix = "" if fixture_data["near"] else "push %cs"
    caller_cleanup = 0 if fixture_data["cleanup"] else fixture_data["args_bytes"]
    register_sources = {"AX": 0, "BX": 1, "CX": 2, "DX": 3, "SI": 1, "DI": 2}
    register_sources.update(fixture_data.get("register_inputs", {}))
    register_lines = "\n".join(
        f"    mov input+{register_sources[name] * 2}, %{name.lower()}"
        for name in ("BX", "CX", "DX", "SI", "DI")
    )
    ax_source = register_sources["AX"]
    absolute = bool(fixture_data.get("absolute_memory"))
    data_segment_setup = (
        "    mov $0x1000, %bx\n"
        "    mov $0x4a, %ah\n"
        "    int $0x21\n"
        "    jc failed\n"
        "    mov $0x1000, %bx\n"
        "    mov $0x48, %ah\n"
        "    int $0x21\n"
        "    jc failed\n"
        "    mov %ax, data_segment\n"
    ) if absolute else ""
    code_memory_setup = "".join(
        "    push %ds\n"
        "    push %es\n"
        "    push %cs\n"
        "    pop %ds\n"
        "    push %cs\n"
        "    pop %es\n"
        "    cld\n"
        f"    mov $input+8+{window['arena_offset']}, %si\n"
        f"    mov ${window['code_offset']}, %di\n"
        f"    mov ${window['byte_count']}, %cx\n"
        "    rep movsb\n"
        "    pop %es\n"
        "    pop %ds\n"
        for window in fixture_data.get("code_memory_windows", [])
    )
    arena_copy_in = (
        "    push %cs\n"
        "    pop %ds\n"
        "    mov data_segment, %ax\n"
        "    mov %ax, %es\n"
        "    mov $input+8, %si\n"
        "    xor %di, %di\n"
        f"    mov ${ARENA}, %cx\n"
        "    rep movsb\n"
        "    mov $input, %si\n"
        "    mov $0x8000, %di\n"
        f"    mov ${ARENA}, %cx\n"
        "    rep movsb\n"
    ) if absolute else ""
    data_segment_set = (
        "    mov data_segment, %ax\n"
        "    mov %ax, %ds\n"
        "    mov %ax, %es\n"
        "    pop %ax\n"
    ) if absolute else ""
    data_segment_restore = "    push %cs\n    pop %ds\n" if absolute else ""
    input_ax_store = "    push %ax\n" if absolute else ""
    data_segment_label = "data_segment: .word 0\n" if absolute else ""
    arena_copy_out = (
        "    cld\n"
        "    mov data_segment, %ax\n"
        "    mov %ax, %ds\n"
        "    push %cs\n"
        "    pop %es\n"
        "    xor %si, %si\n"
        "    mov $snapshot+32, %di\n"
        f"    mov ${ARENA}, %cx\n"
        "    rep movsb\n"
        "    push %cs\n"
        "    pop %ds\n"
    ) if absolute else (
        "    cld\n"
        "    mov $0x8000, %si\n"
        "    mov $snapshot+32, %di\n"
        f"    mov ${ARENA}, %cx\n"
        "    rep movsb\n"
    )
    return f""".code16
.global _start
_start:
    push %cs
    pop %ds
    push %cs
    pop %es
    cli
    push %cs
    pop %ss
    mov $0xeff0, %sp
    sti
    cld
    mov $input_name, %dx
    mov $0x3d00, %ax
    int $0x21
    jc failed
    mov %ax, input_handle
    mov $output_name, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, output_handle
{data_segment_setup}next_case:
    cld
    mov $0xeff0, %sp
    mov input_handle, %bx
    mov $input, %dx
    mov ${CASE_BYTES}, %cx
    mov $0x3f00, %ax
    int $0x21
    jc failed
    or %ax, %ax
    jz finished
    cmp ${CASE_BYTES}, %ax
    jne failed
{arena_copy_in}    mov $input+8, %si
    mov $0x8000, %di
    mov ${ARENA}, %cx
    rep movsb
    movw $0x1357, %ss:0xeff0
    movw $0x2468, %ss:0xeff2
{code_memory_setup}{_assembly_stack_setup(fixture_data)}
    mov %sp, %ax
    sub ${return_bytes}, %ax
    mov %ax, snapshot+14
    mov $0x{FIXTURE_BP:x}, %bp
{register_lines}
    mov input+8, %ax
    or $0x202, %ax
    push %ax
    popf
    mov input+{ax_source * 2}, %ax
{input_ax_store}{data_segment_set}    {call_prefix}
    call original
    add ${caller_cleanup}, %sp
{data_segment_restore}    mov %ax, snapshot
    mov %bx, snapshot+2
    mov %cx, snapshot+4
    mov %dx, snapshot+6
    mov %si, snapshot+8
    mov %di, snapshot+10
    mov %bp, snapshot+12
    mov %sp, snapshot+16
    mov %ds, snapshot+18
    mov %es, snapshot+20
    mov %ss, snapshot+22
    pushf
    popw snapshot+24
    mov %ss:0xeff0, %ax
    mov %ax, snapshot+26
    mov %ss:0xeff2, %ax
    mov %ax, snapshot+28
    mov %cs, %ax
    mov %ax, snapshot+30
{arena_copy_out}    mov output_handle, %bx
    mov $snapshot, %dx
    mov ${RECORD_BYTES}, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp ${RECORD_BYTES}, %ax
    jne failed
    jmp next_case
finished:
    mov output_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21
input_name: .asciz "CASES.BIN"
output_name: .asciz "TRACE.BIN"
input_handle: .word 0
output_handle: .word 0
{data_segment_label}original:
{raw_block}
input: .space {CASE_BYTES}
snapshot: .space {RECORD_BYTES}
"""


def _stack_words(values: list[tuple[int, str]]) -> list[int]:
    pushed: list[int] = []
    for value, type_name in reversed(values):
        if type_name in _POINTERS:
            pushed.extend((HOST_SEGMENT, value & 0xffff))
        elif type_name == "longint":
            pushed.extend(((value >> 16) & 0xffff, value & 0xffff))
        else:
            pushed.append(value & 0xffff)
    return list(reversed(pushed))


def _symbolic_word(index: int, mask: int | None = None) -> str:
    if index < 4:
        expression = f"LongInt(input[{index}])"
    else:
        offset = (index - 4) * 2
        expression = (
            f"(LongInt(Word(arena[{offset}])) or "
            f"(LongInt(Word(arena[{offset + 1}])) shl 8))"
        )
    if mask is not None:
        expression = f"({expression} and ${mask:x})"
    return f"Word({expression} and $ffff)"


def _symbolic_argument_words(fixture_data: dict[str, Any]) -> list[str]:
    expressions: list[str] = []
    index = 0
    for arg in fixture_data["params"]:
        type_name = arg["type"]
        mask = fixture_data.get("argument_masks", {}).get(str(index))
        mask_value = int(mask, 0) if mask is not None else None
        if type_name in _POINTERS or type_name == "longint":
            expressions.append(_symbolic_word(index, mask_value))
            expressions.append(_symbolic_word(index + 1))
            index += 2
        else:
            expressions.append(_symbolic_word(index, mask_value))
            index += 1
    return expressions


def _assembly_stack_setup(fixture_data: dict[str, Any]) -> str:
    words: list[tuple[int | None, int | None, bool]] = []
    index = 0
    for arg in fixture_data["params"]:
        type_name = arg["type"]
        mask_text = fixture_data.get("argument_masks", {}).get(str(index))
        mask = int(mask_text, 0) if mask_text is not None else None
        if type_name in _POINTERS:
            words.extend(((None, None, True), (index, mask, False)))
            index += 2
        elif type_name == "longint":
            words.extend(((index, mask, False), (index + 1, None, False)))
            index += 2
        else:
            words.append((index, mask, False))
            index += 1
    memory_words = words
    stack_base = 0xeff0 - len(memory_words) * 2
    lines = [f"    mov ${stack_base:#x}, %sp"]
    for word_index, (source, mask, segment) in enumerate(memory_words):
        address = stack_base + word_index * 2
        if segment:
            lines.append(f"    movw ${HOST_SEGMENT}, %ss:0x{address:x}")
            continue
        assert source is not None
        if source < 4:
            source_offset = source * 2
        else:
            source_offset = 8 + (source - 4) * 2
        lines.append(f"    mov input+{source_offset}, %ax")
        if mask is not None:
            lines.append(f"    and ${mask:x}, %ax")
        lines.append(f"    mov %ax, %ss:0x{address:x}")
    return "\n".join(lines)


def _symbolic_stack_words(fixture_data: dict[str, Any]) -> list[str]:
    expressions = _symbolic_argument_words(fixture_data)
    pushed: list[str] = []
    param_index = 0
    for arg in reversed(fixture_data["params"]):
        type_name = arg["type"]
        if type_name in _POINTERS:
            pushed.extend((str(HOST_SEGMENT), expressions[param_index + 1]))
            param_index += 2
        elif type_name == "longint":
            pushed.extend((expressions[param_index], expressions[param_index + 1]))
            param_index += 2
        else:
            pushed.append(expressions[param_index])
            param_index += 1
    return list(reversed(pushed))


def program(fixture_data: dict[str, Any]) -> str:
    word_expressions = _symbolic_argument_words(fixture_data)
    arg_vars = "\n".join(
        f"  arg_{index}: Word;" for index in range(len(word_expressions))
    )
    arg_assignments = "\n".join(
        f"  arg_{index} := {expression};"
        for index, expression in enumerate(word_expressions)
    )
    call_expressions: list[str] = []
    word_index = 0
    for arg in fixture_data["params"]:
        type_name = arg["type"]
        if type_name in _POINTERS:
            call_expressions.append(f"@arena[arg_{word_index + 1} - $8000]")
            word_index += 2
        elif type_name == "longint":
            call_expressions.append(
                f"LongInt((LongInt(arg_{word_index}) shl 16) or arg_{word_index + 1})"
            )
            word_index += 2
        else:
            call_expressions.append(_call_arg(f"arg_{word_index}", type_name))
            word_index += 1
    args = ", ".join(call_expressions)
    call = f"{fixture_data['name']}({args});" if args else f"{fixture_data['name']};"
    if fixture_data["kind"] == "function":
        call = f"contractResult := LongInt({fixture_data['name']}({args}));"
    return_bytes = 2 if fixture_data["near"] else 4
    register_sources = {"AX": 0, "BX": 1, "CX": 2, "DX": 3, "SI": 1, "DI": 2}
    register_sources.update(fixture_data.get("register_inputs", {}))
    register_lines = " ".join(
        f"Register{name} := input[{register_sources[name]}];"
        for name in ("AX", "BX", "CX", "DX", "SI", "DI")
    )
    arena_base = "$0" if fixture_data.get("absolute_memory") else "$8000"
    words = _symbolic_stack_words(fixture_data)
    stack_writes = "\n".join(
        f"  RealModeMemory[(LongInt(${HOST_SEGMENT:x}) shl 4) + entry + {return_bytes} + {offset * 2}] := Byte(arg_{offset});\n"
        f"  RealModeMemory[(LongInt(${HOST_SEGMENT:x}) shl 4) + entry + {return_bytes} + {offset * 2} + 1] := Byte(arg_{offset} shr 8);"
        for offset, _ in enumerate(words)
    )
    code_memory_writes = "\n".join(
        f"  for i := 0 to {window['byte_count'] - 1} do\n"
        f"    RealModeMemory[(LongInt(${HOST_SEGMENT:x}) shl 4) + "
        f"{window['code_offset']} + i] := arena[{window['arena_offset']} + i];"
        for window in fixture_data.get("code_memory_windows", [])
    )
    if code_memory_writes:
        code_memory_writes += "\n"
    if stack_writes:
        stack_writes += "\n"
    return f"""program ContractTrial;
uses LieroRuntime;
{{$I candidate.inc}}
    var arena: array[0..4095] of Byte;
    input: array[0..7] of Word; row: array[0..15] of Word;
    inputFile, outputFile: file; transferred: LongInt;
    entry: Word; contractResult: LongInt; flagsWord: Word; i: Word;
{arg_vars}
begin
  if SizeOf(Integer) <> 2 then Halt(1);
  Assign(inputFile, 'CASES.BIN'); Reset(inputFile, 1);
  Assign(outputFile, 'PASCAL.BIN'); Rewrite(outputFile, 1);
  while not Eof(inputFile) do
  begin
    BlockRead(inputFile, input, 8, transferred);
    if transferred <> 8 then Halt(2);
    BlockRead(inputFile, arena, 4096, transferred);
    if transferred <> 4096 then Halt(3);
    entry := $eff0 - {len(words) * 2} - {return_bytes};
    {register_lines}
    flagsWord := Word(arena[0]) or (Word(arena[1]) shl 8);
    RegisterFlagsWord := flagsWord or $202;
    RegisterParityFlag := (RegisterFlagsWord and $4) <> 0;
    RegisterSP := entry; RegisterBP := ${FIXTURE_BP:x};
    RegisterDS := ${HOST_SEGMENT:x}; RegisterES := ${HOST_SEGMENT:x}; RegisterSS := ${HOST_SEGMENT:x};
    for i := 0 to 4095 do
      RealModeMemory[(LongInt(${HOST_SEGMENT:x}) shl 4) + {arena_base} + i] := arena[i];
{arg_assignments}{code_memory_writes}{stack_writes}
    flagsWord := Word(arena[0]) or (Word(arena[1]) shl 8);
    RegisterCarryFlag := (flagsWord and 1) <> 0;
    RegisterZeroFlag := (flagsWord and $40) <> 0;
    RegisterDirectionFlag := (flagsWord and $400) <> 0;
    RegisterSignFlag := (flagsWord and $80) <> 0;
    RegisterOverflowFlag := (flagsWord and $800) <> 0;
    {call}
    for i := 0 to 4095 do
      arena[i] := RealModeMemory[(LongInt(${HOST_SEGMENT:x}) shl 4) + {arena_base} + i];
    row[0] := RegisterAX; row[1] := RegisterBX; row[2] := RegisterCX;
    row[3] := RegisterDX; row[4] := RegisterSI; row[5] := RegisterDI;
    row[6] := RegisterBP; row[7] := entry; row[8] := RegisterSP;
    row[9] := RegisterDS; row[10] := RegisterES; row[11] := RegisterSS;
    row[12] := Word(RegisterCarryFlag) + Word(RegisterZeroFlag) * $40 +
      Word(RegisterDirectionFlag) * $400;
    row[13] := $1357; row[14] := $2468; row[15] := ${HOST_SEGMENT:x};
    BlockWrite(outputFile, row, 32, transferred);
    if transferred <> 32 then Halt(4);
    BlockWrite(outputFile, arena, 4096, transferred);
    if transferred <> 4096 then Halt(5);
  end;
  Close(inputFile); Close(outputFile);
end.
"""


def compile_candidate(
    root: pathlib.Path,
    output: pathlib.Path,
    fixture_data: dict[str, Any],
    source: str,
) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    (output / "candidate.inc").write_text(source)
    (output / "probe.pas").write_text(program(fixture_data))
    command = [
        "fpc",
        "-Mtp",
        "-Cr",
        f"-Fu{root.resolve() / 'targets/liero/src'}",
        "-FU.",
        "probe.pas",
    ]
    result = subprocess.run(
        command, cwd=output, capture_output=True, timeout=30, check=False
    )
    (output / "compile.log").write_bytes(result.stdout + result.stderr)
    return {
        "status": "passed" if result.returncode == 0 else "compile-failed",
        "returncode": result.returncode,
    }


def original(
    output: pathlib.Path,
    fixture_data: dict[str, Any],
    inputs: list[bytes],
) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    (output / "harness.S").write_text(harness(fixture_data))
    image = assemble_probe(output / "harness.S", output)
    raw = bytes.fromhex(fixture_data["bytes"])
    if not fixture_data.get("raw_asm") and image.count(raw) != 1:
        raise ValueError("contract-original routine bytes missing or duplicated")
    if len(image) + 0x100 >= 0x6000:
        raise ValueError("contract-original harness overlaps protected arena")
    (output / "PROBE.COM").write_bytes(image)
    (output / "CASES.BIN").write_bytes(b"".join(inputs))
    run_dosbox(output)
    trace = (output / "TRACE.BIN").read_bytes()
    if len(trace) != len(inputs) * RECORD_BYTES:
        raise ValueError("contract-original trace has wrong length")
    result = {"status": "passed", "cases": len(inputs)}
    pilot.save(output / "result.json", result)
    return result


def run_candidate(
    output: pathlib.Path,
    fixture_data: dict[str, Any],
    inputs: list[bytes],
    original_trace: bytes,
) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    (output / "CASES.BIN").write_bytes(b"".join(inputs))
    try:
        result = subprocess.run(
            [str(output / "probe")],
            cwd=output,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        (output / "runtime.log").write_bytes((error.stdout or b"") + (error.stderr or b""))
        return {"status": "runtime-timeout"}
    (output / "runtime.log").write_bytes(result.stdout + result.stderr)
    if result.returncode:
        return {"status": "runtime-failed", "returncode": result.returncode}
    trace = (output / "PASCAL.BIN").read_bytes()
    flag_mask = fixture_data.get("flag_mask", 0x441)
    if isinstance(flag_mask, str):
        flag_mask = int(flag_mask, 0)
    return compare(original_trace, trace, flag_mask=int(flag_mask))


def compare(original_trace: bytes, candidate_trace: bytes, flag_mask: int = 0x441) -> dict:
    if len(original_trace) != len(candidate_trace) or len(original_trace) % RECORD_BYTES:
        raise ValueError("partial or extra contract-oracle output")
    checked = (0, 2, 4, 6, 8, 10, 12, 14, 24, 26, 28)
    failures = []
    count = len(original_trace) // RECORD_BYTES
    for index in range(count):
        start = index * RECORD_BYTES
        original = bytearray(original_trace[start:start + RECORD_BYTES])
        candidate = bytearray(candidate_trace[start:start + RECORD_BYTES])
        differences = []
        for offset in checked:
            if offset == 24:
                mask = flag_mask
                left = struct.unpack_from("<H", original, offset)[0] & mask
                right = struct.unpack_from("<H", candidate, offset)[0] & mask
                if left != right:
                    differences.append(offset)
            elif original[offset:offset + 2] != candidate[offset:offset + 2]:
                differences.append(offset)
        if original[14:16] != candidate[16:18]:
            differences.append(16)
        if original[32:] != candidate[32:]:
            differences.append(32)
        if differences:
            failures.append({"case": index, "first_different_bytes": differences[:12]})
    return {
        "status": "failed" if failures else "passed",
        "cases": count,
        "matches": count - len(failures),
        "failures": failures,
    }


def run(
    root: pathlib.Path,
    output: pathlib.Path,
    source_path: pathlib.Path,
    routine: str,
    suites: tuple[str, ...] = ("training", "terminal"),
) -> dict:
    root_path = pathlib.Path(root)
    source = pathlib.Path(source_path).read_text()
    fixture_data = fixture(root_path, "liero", routine)
    output = pathlib.Path(output)
    output.mkdir(parents=True, exist_ok=False)
    result: dict[str, Any] = {
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "source_path": str(pathlib.Path(source_path).resolve()),
        "compile": {"status": "pending"},
        "suites": {},
    }
    pilot.save(output / "freeze.json", {
        "routine": routine,
        "source_sha256": result["source_sha256"],
        "fixture_sha256": fixture_data["bytes_sha256"],
        "corpora": {suite: corpus_hash(fixture_data, suite) for suite in suites},
        "policy": "training first, terminal once only if training passes",
        "budget": "no model requests, no repair, no source promotion",
    })
    pilot.save(output / "result.json", result)
    result["compile"] = compile_candidate(
        root_path, output / "candidate", fixture_data, source
    )
    pilot.save(output / "result.json", result)
    if result["compile"]["status"] != "passed":
        return result
    for suite in suites:
        inputs = cases(fixture_data, suite)
        original_dir = output / f"original-{suite}"
        original_result = original(original_dir, fixture_data, inputs)
        original_trace = (original_dir / "TRACE.BIN").read_bytes()
        candidate_dir = output / f"candidate-{suite}"
        candidate_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output / "candidate" / "probe", candidate_dir / "probe")
        candidate_result = run_candidate(
            candidate_dir, fixture_data, inputs, original_trace
        )
        result["suites"][suite] = {
            "original": original_result,
            "candidate": candidate_result,
        }
        pilot.save(output / "result.json", result)
        if suite == "training" and candidate_result["status"] != "passed":
            break
    return result


def run_training(
    root: pathlib.Path,
    output: pathlib.Path,
    source_path: pathlib.Path,
    routine: str,
) -> dict:
    return run(root, output, source_path, routine, suites=("training",))
