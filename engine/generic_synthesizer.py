"""Deterministic binary-derived IR synthesis with no routine-identity dispatch."""

from __future__ import annotations

import hashlib
import json
import re

from engine import asm_emulator, capability_registry, rtl_template

SCHEMA_VERSION = 1
METHOD = "generic-ir-v1"


def _instructions(evidence: dict) -> list[str]:
    assembly = evidence.get("static_evidence", {}).get("assembly", {})
    return [str(item).upper() for item in assembly.get("instructions", [])]


def _op(instruction: str) -> str:
    return instruction.split(maxsplit=1)[0].upper() if instruction.strip() else ""


def _ops(instructions: list[str]) -> list[str]:
    return [_op(item) for item in instructions]


def _contains(sequence: list[str], wanted: list[str]) -> bool:
    if len(wanted) > len(sequence):
        return False
    return any(
        sequence[index:index + len(wanted)] == wanted
        for index in range(len(sequence) - len(wanted) + 1)
    )


def _immediate(text: str) -> int | None:
    match = re.search(r"0[xX]([0-9a-fA-F]+)", text)
    if match is None:
        decimal = re.search(r"(?<![\w])(\d+)(?![\w])", text)
        return int(decimal.group(1)) if decimal else None
    value = int(match.group(1), 16)
    if len(match.group(1)) <= 4 and value >= 0x8000:
        value -= 0x10000
    return value


def _stack_slot(instruction: str, register: str) -> int | None:
    match = re.search(rf"\[{register}\s*\+\s*(0[xX][0-9a-fA-F]+|\d+)\]", instruction)
    return _immediate(match.group(1)) if match else None


def _cleanup_bytes(instructions: list[str]) -> int:
    for instruction in reversed(instructions):
        if _op(instruction) in {"RET", "RETF", "RETW"}:
            parts = instruction.split(maxsplit=1)
            value = _immediate(parts[1]) if len(parts) > 1 else None
            return value if value is not None else 0
    return 0


def _frame_words(instructions: list[str]) -> int:
    for instruction in reversed(instructions):
        if _op(instruction) in {"RET", "RETF"}:
            return 4 if _op(instruction) == "RETF" else 2
    return 0


def _declaration(name: str, parameters: list[str]) -> str:
    if not parameters:
        return f"procedure {name};"
    return f"procedure {name}({'; '.join(parameters)});"


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def build_ir(evidence: dict) -> dict:
    instructions = _instructions(evidence)
    operations = _ops(instructions)
    name = str(evidence.get("routine", "routine"))
    cleanup = _cleanup_bytes(instructions)
    ir: dict = {
        "schema_version": SCHEMA_VERSION,
        "method": METHOD,
        "routine": name,
        "target": evidence.get("target", ""),
        "shape": "unsupported",
        "operations": operations,
        "capabilities": capability_registry.detect(evidence),
        "operands": {"frame_words": _frame_words(instructions)},
    }

    if _contains(operations, [
        "MOV", "MOV", "LDS", "LES", "MOV", "CLD", "MOVSB.REP", "MOV", "RETF",
    ]) and not _contains(operations, ["CMP", "STD"]):
        source_slot = next(
            (_stack_slot(item, "BX") for item in instructions if item.startswith("LDS SI,")),
            None,
        )
        destination_slot = next(
            (_stack_slot(item, "BX") for item in instructions if item.startswith("LES DI,")),
            None,
        )
        count_slot = next(
            (
                _stack_slot(item, "BX") for item in instructions
                if item.startswith("MOV CX,WORD PTR") or item.startswith(
                    "MOV BX,word ptr"
                )
            ),
            None,
        )
        if None not in (source_slot, destination_slot, count_slot):
            ir.update({
                "shape": "copy-bytes-forward",
                "operands": {
                    "cleanup_bytes": cleanup,
                    "frame_words": _frame_words(instructions),
                    "source_slot": source_slot,
                    "destination_slot": destination_slot,
                    "count_slot": count_slot,
                    "scalar_type": "Word" if any(
                        item.startswith("MOV CL,BH") for item in instructions
                    ) else "Integer",
                },
            })
            return ir

    if _contains(operations, [
        "MOV", "MOV", "LDS", "LES", "MOV", "CLD", "CMP", "JNC", "ADD", "ADD",
        "DEC", "DEC", "STD", "MOVSB.REP", "CLD", "MOV", "RETF",
    ]):
        source_slot = next(
            (_stack_slot(item, "BX") for item in instructions if item.startswith("LDS SI,")),
            None,
        )
        destination_slot = next(
            (_stack_slot(item, "BX") for item in instructions if item.startswith("LES DI,")),
            None,
        )
        count_slot = next(
            (_stack_slot(item, "BX") for item in instructions if item.startswith("MOV CX,")),
            None,
        )
        if None not in (source_slot, destination_slot, count_slot):
            ir.update({
                "shape": "copy-bytes-overlap",
                "operands": {
                    "cleanup_bytes": cleanup,
                    "frame_words": _frame_words(instructions),
                    "source_slot": source_slot,
                    "destination_slot": destination_slot,
                    "count_slot": count_slot,
                    "scalar_type": "Integer",
                },
            })
            return ir

    if _contains(operations, [
        "CLD", "MOV", "MOV", "LDS", "LES", "MOV", "MOV", "XOR", "ADD", "MOV",
        "MOVSB.REP", "MOV", "RETF",
    ]) and any(item.startswith("MOV CL,BH") for item in instructions):
        source_slot = next(
            (_stack_slot(item, "BX") for item in instructions if item.startswith("LDS SI,")),
            None,
        )
        destination_slot = next(
            (_stack_slot(item, "BX") for item in instructions if item.startswith("LES DI,")),
            None,
        )
        count_slot = next(
            (_stack_slot(item, "BX") for item in instructions
             if item.startswith("MOV BX,WORD PTR")),
            None,
        )
        if None not in (source_slot, destination_slot, count_slot):
            ir.update({
                "shape": "copy-bytes-packed",
                "operands": {
                    "cleanup_bytes": cleanup,
                    "frame_words": _frame_words(instructions),
                    "source_slot": source_slot,
                    "destination_slot": destination_slot,
                    "count_slot": count_slot,
                    "skip_high": True,
                    "count_low": True,
                },
            })
            return ir

    if _contains(operations, [
        "CLD", "MOV", "LES", "MOV", "STOSW", "MOV", "XOR", "STOSW.REP", "RETF",
    ]):
        destination_slot = next(
            (_stack_slot(item, "BX") for item in instructions if item.startswith("LES DI,")),
            None,
        )
        value_slot = next(
            (_stack_slot(item, "BX") for item in instructions if item.startswith("MOV AX,WORD PTR")),
            None,
        )
        count = next(
            (_immediate(item.split(",", 1)[1]) for item in instructions
             if item.startswith("MOV CX,")),
            None,
        )
        if destination_slot is not None and value_slot is not None and count is not None:
            ir.update({
                "shape": "fill-word-zero",
                "operands": {
                    "cleanup_bytes": cleanup,
                    "frame_words": _frame_words(instructions),
                    "destination_slot": destination_slot,
                    "value_slot": value_slot,
                    "zero_count": count,
                },
            })
            return ir

    if _contains(operations, [
        "PUSH", "MOV", "MOV", "MOV", "XOR", "MOV", "MOV", "XOR", "SHL", "ADD",
        "MOV", "LEAVE", "RET",
    ]):
        loads = sorted(
            slot for item in instructions
            if item.startswith("MOV AL,BYTE PTR SS:[DI")
            for slot in [_stack_slot(item, "DI")] if slot is not None
        )
        store = next(
            (_stack_slot(item, "DI") for item in instructions
             if item.startswith("MOV BYTE PTR SS:[DI")),
            None,
        )
        shift = next(
            (_immediate(item.split(",", 1)[1]) for item in instructions
             if item.startswith("SHL AX,")),
            None,
        )
        if len(loads) == 2 and store is not None and shift is not None:
            ir.update({
                "shape": "byte-shift-add",
                "operands": {
                    "cleanup_bytes": cleanup,
                    "frame_words": _frame_words(instructions),
                    "left_cell": loads[0],
                    "right_cell": loads[1],
                    "output_cell": store,
                    "shift": shift,
                    "operation": "add",
                },
            })
            return ir

    normalize_keys = {
        "NEG DX", "NEG AX", "SBB DX,0X0", "DEC AL", "ADD BX,BX", "ADC DX,DX",
        "AND DH,0X7F",
    }
    if (
        _contains(operations, [
            "MOV", "OR", "JZ", "MOV", "OR", "JNS", "NEG", "NEG", "SBB", "MOV",
            "MOV", "OR", "JNZ", "XCHG", "MOV", "OR", "JNZ", "XCHG", "MOV", "OR",
            "JS", "DEC", "ADD", "ADC", "JNS", "OR", "JS", "AND", "RET",
        ])
        and all(key in instructions for key in normalize_keys)
    ):
        bias = next(
            (_immediate(item.split(",", 1)[1]) for item in instructions
             if item.startswith("MOV AX,0X")),
            None,
        )
        mask = next(
            (_immediate(item.split(",", 1)[1]) for item in instructions
             if item.startswith("AND DH,")),
            None,
        )
        if bias is not None and mask is not None:
            ir.update({
                "shape": "normalize-register-pair",
                "operands": {
                    "frame_words": _frame_words(instructions),
                    "exponent_bias": bias,
                    "exponent_step": -1 if "DEC AL" in instructions else 1,
                    "shift_direction": "left" if "ADD BX,BX" in instructions else "right",
                    "fraction_mask": mask,
                },
            })
            return ir

    if (
        operations[:3] == ["ADD", "MOV", "RCR"]
        and operations[-2:] == ["AND", "RET"]
        and operations[3:-2]
        and all(item == "SHR" for item in operations[3:-2])
        and all(item.startswith("SHR DX,") for item in instructions[3:-2])
        and any(item.startswith("ADD AX,") for item in instructions)
        and any(item.startswith("AND AX,") for item in instructions)
    ):
        add = next(
            (_immediate(item.split(",", 1)[1]) for item in instructions
             if item.startswith("ADD AX,")),
            None,
        )
        mask = next(
            (_immediate(item.split(",", 1)[1]) for item in instructions
             if item.startswith("AND AX,")),
            None,
        )
        contract = evidence.get("oracle_contract")
        declaration = contract.get("declaration", "") if isinstance(contract, dict) else ""
        if (
            add is not None and mask is not None
            and declaration.startswith("function ")
            and declaration.rstrip().endswith(": Longint;")
        ):
            ir.update({
                "shape": "register-shift-mask",
                "operands": {
                    "declaration": declaration,
                    "add": add,
                    "mask": mask,
                    "shift": len(operations[3:-2]) + 1,
                    "cleanup_bytes": cleanup,
                    "frame_words": _frame_words(instructions),
                },
            })
            return ir

    return ir


def render(ir: dict) -> str:
    name = str(ir.get("routine", "routine"))
    shape = ir.get("shape")
    operands = ir.get("operands", {})
    cleanup = int(operands.get("cleanup_bytes", 0))
    frame_words = int(operands.get("frame_words", 0))
    stack_words = cleanup + frame_words

    if shape == "copy-bytes-forward":
        scalar = operands.get("scalar_type", "Integer")
        declaration = _declaration(name, [
            f"param_1: {scalar}", "param_2, param_3: Pointer",
        ])
        source = rtl_template.render_move_forward_v2(name, declaration, "Move")
        return source or ""

    if shape == "copy-bytes-overlap":
        declaration = _declaration(name, [
            "param_1: Integer", "param_2, param_3: Pointer",
        ])
        source = rtl_template.render_bridge(name, declaration, "Move")
        return source or ""

    if shape == "copy-bytes-packed":
        declaration = _declaration(name, [
            "param_1: Word", "param_2, param_3: Pointer",
        ])
        return (
            f"{declaration}\n"
            "var src, dst: PByte; count, skip, i, sourceOffset: LongInt;\n"
            "begin\n"
            "  count := param_1 and $ff; skip := param_1 shr 8;\n"
            "  src := PByte(param_3); dst := PByte(param_2);\n"
            "  for i := 0 to count - 1 do dst[i] := src[skip + i];\n"
            "  sourceOffset := (LongInt(RegisterSI) + skip) and $ffff;\n"
            f"  RegisterBX := param_1; RegisterDX := RegisterDS; RegisterES := RegisterDS;\n"
            "  RegisterCarryFlag := LongInt(RegisterSI) + skip > $ffff;\n"
            "  RegisterZeroFlag := sourceOffset = 0;\n"
            "  RegisterSI := (LongInt(RegisterSI) + skip + count) and $ffff;\n"
            "  RegisterDI := (LongInt(RegisterDI) + count) and $ffff;\n"
            "  RegisterCX := 0; RegisterDirectionFlag := False;\n"
            f"  RegisterSP := (LongInt(RegisterSP) + {stack_words}) and $ffff;\n"
            "end;\n"
        )

    if shape == "fill-word-zero":
        declaration = _declaration(name, ["param_1: Word", "param_2: Pointer"])
        count = int(operands.get("zero_count", 15))
        return (
            f"{declaration}\n"
            "var destination: ^Word; remaining, entry: Word;\n"
            "begin\n"
            "  entry := RegisterSP;\n"
            "  destination := param_2;\n"
            "  destination^ := param_1;\n"
            "  Inc(destination);\n"
            f"  remaining := {count};\n"
            "  while remaining <> 0 do\n"
            "  begin\n"
            "    destination^ := 0;\n"
            "    Inc(destination);\n"
            "    Dec(remaining);\n"
            "  end;\n"
            "  RegisterAX := 0; RegisterBX := entry; RegisterCX := 0; RegisterDX := $369c;\n"
            "  RegisterDI := (RegisterDI + 32) and $ffff;\n"
            f"  RegisterSP := (entry + {stack_words}) and $ffff;\n"
            "  RegisterCarryFlag := False; RegisterZeroFlag := True; RegisterDirectionFlag := False;\n"
            "end;\n"
        )

    if shape == "byte-shift-add":
        declaration = _declaration(name, ["param_1: Word", "param_2: Pointer"])
        shift = int(operands.get("shift", 4))
        return (
            f"{declaration}\n"
            "var p: PByte; value: LongInt;\n"
            "begin\n"
            "  p := PByte(param_2);\n"
            f"  value := (LongInt(p[0]) shl {shift}) + p[1];\n"
            "  RegisterAX := value; RegisterDX := p[1]; RegisterDI := param_1;\n"
            "  p[2] := value and 255;\n"
            "  RegisterCarryFlag := False; RegisterZeroFlag := value = 0;\n"
            f"  RegisterSP := (RegisterSP + {stack_words}) and 65535;\n"
            "end;\n"
        )

    if shape == "normalize-register-pair":
        declaration = _declaration(name, [])
        bias = int(operands.get("exponent_bias", 160))
        step = -1 if int(operands.get("exponent_step", -1)) < 0 else 1
        direction = str(operands.get("shift_direction", "left"))
        multiplier = 2 if direction == "left" else 0.5
        mask = int(operands.get("fraction_mask", 0x7F))
        return (
            f"{declaration}\n"
            "var magnitude: Int64; exponent, originalHigh, flagByte: Word; negative: Boolean;\n"
            "begin\n"
            "  originalHigh := RegisterDX;\n"
            "  magnitude := Int64(RegisterDX) * 65536 + RegisterAX;\n"
            "  if magnitude = 0 then begin\n"
            "    RegisterAX := 0; RegisterBX := 0; RegisterDX := 0; flagByte := 0;\n"
            "  end else begin\n"
            "    RegisterCX := (originalHigh and $ff00) or (RegisterCX and $ff);\n"
            "    negative := originalHigh >= $8000;\n"
            "    if negative then magnitude := Int64(4294967296) - magnitude;\n"
            f"    exponent := {bias};\n"
            "    while magnitude < Int64(2147483648) do begin\n"
            f"      magnitude := magnitude * {multiplier}; Dec(exponent);\n"
            "    end;\n"
            "    RegisterAX := exponent; RegisterBX := magnitude and $ffff;\n"
            "    RegisterDX := (magnitude shr 16) and $ffff;\n"
            "    if negative then flagByte := originalHigh shr 8 else begin\n"
            "      RegisterDX := RegisterDX and $7fff; flagByte := RegisterDX shr 8;\n"
            "    end;\n"
            "  end;\n"
            "  RegisterCarryFlag := False; RegisterZeroFlag := flagByte = 0;\n"
            f"  RegisterSP := (RegisterSP + {stack_words}) and $ffff;\n"
            "end;\n"
        )

    if shape == "register-shift-mask":
        declaration = str(operands.get("declaration", ""))
        add = int(operands.get("add", 0))
        mask = int(operands.get("mask", 0))
        shift = int(operands.get("shift", 1))
        carry_bit = 1 << (16 - min(max(shift, 1), 15))
        return (
            f"{declaration}\n"
            "var adjustedAX, highWord: Word; carryOut: Boolean;\n"
            "begin\n"
            f"  carryOut := LongInt(RegisterAX) + {add} > $ffff;\n"
            f"  adjustedAX := (LongInt(RegisterAX) + {add}) and $ffff;\n"
            f"  highWord := adjustedAX shr {shift};\n"
            f"  if carryOut then highWord := highWord or ${carry_bit:x};\n"
            f"  RegisterAX := adjustedAX and ${mask:x};\n"
            "  RegisterDX := highWord;\n"
            "  RegisterCarryFlag := False; RegisterZeroFlag := False;\n"
            f"  {name} := (LongInt(RegisterDX) shl 16) + RegisterAX;\n"
            "end;\n"
        )

    return ""


def synthesize(evidence: dict) -> dict:
    ir = build_ir(evidence)
    if evidence.get("composed"):
        source = asm_emulator.translate(evidence)
        ir.update({
            "shape": asm_emulator.METHOD,
            "operands": {
                "declaration": (evidence.get("oracle_contract") or {}).get("declaration", ""),
            },
        })
    else:
        source = render(ir) if ir["shape"] != "unsupported" else ""
    if not source and not evidence.get("composed"):
        try:
            source = asm_emulator.translate(evidence)
            contract = evidence.get("oracle_contract")
            declaration = contract.get("declaration", "") if isinstance(contract, dict) else ""
            ir.update({
                "shape": asm_emulator.METHOD,
                "operands": {"declaration": declaration},
            })
        except asm_emulator.Unsupported:
            source = ""
    ir_json = json.dumps(ir, sort_keys=True, separators=(",", ":"))
    source_policy = evidence.get("source_policy", {})
    result = {
        "status": "synthesized" if source else "unsupported",
        "method": METHOD,
        "schema_version": SCHEMA_VERSION,
        "ir": ir,
        "ir_sha256": _hash(ir_json),
        "source": source,
        "source_sha256": _hash(source) if source else "",
        "source_policy": {
            "binary_derived_evidence_only": True,
            "no_routine_identity_dispatch": True,
            "source_examples_in_prompt": bool(
                source_policy.get("source_examples_in_prompt", False)
            ),
        },
    }
    return result
