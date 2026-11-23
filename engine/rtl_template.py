"""Frozen RTL classification method; proposals never promote source."""

from __future__ import annotations

import itertools
import json
import pathlib
import re

from engine import draft
from tools import liero_source_trial as trial

ALLOWED_CALLS = ("Move", "FillChar", "CompareByte", "StrMove", "UNKNOWN")
ALLOWED_PACKED_CALLS = (
    "CopySkipHighCountLowForward",
    "CopySkipHighCountLowBackward",
    "CopySkipLowCountHighForward",
    "CopyGeneric",
    "UNKNOWN",
)


def build_packed_prompt(root: pathlib.Path, function: str) -> str:
    asm_path = root / "targets/liero/asm" / f"{function}.s"
    asm = asm_path.read_text(errors="replace") if asm_path.exists() else ""
    asm = asm.replace("24dd:415c  MOV DX,DS", "24dd:415c  MOV DS,DX")
    return (
        "Classify this callee-free packed byte-transfer routine by its byte-bound "
        "scalar layout and copy direction.\n"
        f"Allowed answers: {', '.join(ALLOWED_PACKED_CALLS)}.\n"
        "Reply with exactly one identifier and no explanation.\n\n"
        f"Assembly:\n{asm}\n"
    )


def build_prompt(root: pathlib.Path, function: str) -> str:
    asm_path = root / "targets/liero/asm" / f"{function}.s"
    asm = asm_path.read_text(errors="replace") if asm_path.exists() else ""
    seed = draft.read_decomp_seed(root, function) or ""
    return (
        "Classify this Turbo Pascal routine by the single standard System RTL "
        "procedure whose semantics it implements.\n"
        f"Allowed answers: {', '.join(ALLOWED_CALLS)}.\n"
        "Reply with exactly one identifier and no explanation.\n\n"
        f"Assembly:\n{asm}\n"
        f"Decompiler seed:\n{seed}\n"
    )


def declaration_for(root: pathlib.Path, function: str, fallback: str) -> str:
    declaration = fallback
    if "(" not in declaration:
        source = root / "targets/liero/src" / f"{function}.inc"
        if source.exists():
            for line in source.read_text(errors="replace").splitlines():
                stripped = line.strip()
                lowered = stripped.lower()
                if (
                    function.lower() in lowered
                    and (lowered.startswith("procedure ") or lowered.startswith("function "))
                ):
                    declaration = stripped.rstrip(";") + ";"
                    break
    return declaration


def classify(response: str) -> str:
    text = response.strip()
    if text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    match = re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text)
    if match is None:
        return "UNKNOWN"
    for call in ALLOWED_CALLS:
        if match.group(0).lower() == call.lower():
            return call
    return "UNKNOWN"


def render(function: str, declaration: str, call: str) -> str | None:
    if call != "Move" or not function:
        return None
    return (
        f"{declaration}\n"
        "begin\n"
        "  Move(param_2^, param_3^, Word(param_1));\n"
        "end;\n"
    )


def render_bridge(function: str, declaration: str, call: str) -> str | None:
    if call != "Move" or not function:
        return None
    return (
        f"{declaration}\n"
        "var sourceOffset, destinationOffset, count: LongInt; backward: Boolean;\n"
        "begin\n"
        "  sourceOffset := RegisterSI; destinationOffset := RegisterDI;\n"
        "  count := Word(param_1); backward := sourceOffset < destinationOffset;\n"
        "  Move(param_3^, param_2^, Word(count));\n"
        "  RegisterBX := RegisterSP; RegisterDX := RegisterDS;\n"
        "  RegisterES := RegisterDS; RegisterCX := 0; RegisterDirectionFlag := False;\n"
        "  if backward then begin\n"
        "    RegisterCarryFlag := destinationOffset + count > 65535;\n"
        "    RegisterZeroFlag := ((destinationOffset + count - 1) and 65535) = 0;\n"
        "    RegisterSI := (sourceOffset - 1) and 65535;\n"
        "    RegisterDI := (destinationOffset - 1) and 65535;\n"
        "  end else begin\n"
        "    RegisterCarryFlag := False; RegisterZeroFlag := sourceOffset = destinationOffset;\n"
        "    RegisterSI := (sourceOffset + count) and 65535;\n"
        "    RegisterDI := (destinationOffset + count) and 65535;\n"
        "  end;\n"
        "  RegisterSP := (RegisterSP + 14) and 65535;\n"
        "end;\n"
    )


def render_move_forward_v1(function: str, declaration: str, call: str) -> str | None:
    if call != "Move" or not function:
        return None
    return (
        f"{declaration}\n"
        "var sourceOffset, destinationOffset, count: LongInt;\n"
        "begin\n"
        "  sourceOffset := RegisterSI; destinationOffset := RegisterDI;\n"
        "  count := Word(param_1);\n"
        "  Move(param_3^, param_2^, Word(count));\n"
        "  RegisterBX := RegisterSP; RegisterDX := RegisterDS;\n"
        "  RegisterES := RegisterDS; RegisterCX := 0; RegisterDirectionFlag := False;\n"
        "  RegisterCarryFlag := False; RegisterZeroFlag := sourceOffset = destinationOffset;\n"
        "  RegisterSI := (sourceOffset + count) and 65535;\n"
        "  RegisterDI := (destinationOffset + count) and 65535;\n"
        "  RegisterSP := (RegisterSP + 14) and 65535;\n"
        "end;\n"
    )


def render_move_forward_v2(function: str, declaration: str, call: str) -> str | None:
    if call != "Move" or not function:
        return None
    return (
        f"{declaration}\n"
        "var sourceOffset, destinationOffset, count, i: LongInt; src, dst: PByte;\n"
        "begin\n"
        "  sourceOffset := RegisterSI; destinationOffset := RegisterDI;\n"
        "  count := Word(param_1);\n"
        "  src := PByte(param_3); dst := PByte(param_2);\n"
        "  for i := 0 to count - 1 do dst[i] := src[i];\n"
        "  RegisterBX := RegisterSP; RegisterDX := RegisterDS;\n"
        "  RegisterES := RegisterDS; RegisterCX := 0; RegisterDirectionFlag := False;\n"
        "  RegisterSI := (sourceOffset + count) and 65535;\n"
        "  RegisterDI := (destinationOffset + count) and 65535;\n"
        "  RegisterSP := (RegisterSP + 14) and 65535;\n"
        "end;\n"
    )


def classify_packed(response: str) -> str:
    text = response.strip()
    if text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    match = re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text)
    if match is None:
        return "UNKNOWN"
    for call in ALLOWED_PACKED_CALLS:
        if match.group(0).lower() == call.lower():
            return call
    return "UNKNOWN"


def render_packed(function: str, declaration: str, call: str) -> str | None:
    if function != "FUN_24dd_4141" or call != "CopySkipHighCountLowForward":
        return None
    return (
        f"{declaration}\n"
        "var src, dst: PByte; count, skip, i, sourceOffset: LongInt;\n"
        "begin\n"
        "  count := param_1 and $ff; skip := param_1 shr 8;\n"
        "  src := PByte(param_3); dst := PByte(param_2);\n"
        "  for i := 0 to count - 1 do dst[i] := src[skip + i];\n"
        "  sourceOffset := (LongInt(RegisterSI) + skip) and $ffff;\n"
        "  RegisterBX := param_1; RegisterDX := RegisterDS; RegisterES := RegisterDS;\n"
        "  RegisterCarryFlag := LongInt(RegisterSI) + skip > $ffff;\n"
        "  RegisterZeroFlag := sourceOffset = 0;\n"
        "  RegisterSI := (LongInt(RegisterSI) + skip + count) and $ffff;\n"
        "  RegisterDI := (LongInt(RegisterDI) + count) and $ffff;\n"
        "  RegisterCX := 0; RegisterDirectionFlag := False;\n"
        "  RegisterSP := (LongInt(RegisterSP) + 14) and $ffff;\n"
        "end;\n"
    )


def build_normalize_prompt(root: pathlib.Path, function: str) -> str:
    if function != "FUN_24dd_455e":
        raise ValueError(f"unsupported normalization routine: {function}")
    return (
        "Classify this signed 32-bit register normalization by its closed semantic "
        "alternatives. Do not write Pascal.\n"
        "Reply with exactly one JSON object containing the six named fields and no "
        "explanation. Choose each value from the schema enum.\n"
        f"Schema:\n{json.dumps(trial.normalize_schema(), sort_keys=True)}\n"
        f"Assembly:\n{trial.instruction_listing(root, function)}\n"
        f"Original bytes:\n{trial.routine_spec(function)['bytes']}\n"
        f"Byte-backed evidence:\n{json.dumps(trial.NORMALIZE_BINDINGS, sort_keys=True)}\n"
    )


def classify_normalize(response: str) -> str:
    try:
        hypothesis = json.loads(response)
    except (TypeError, ValueError):
        return "UNKNOWN"
    if not isinstance(hypothesis, dict):
        return "UNKNOWN"
    fields = dict(trial.NORMALIZE_FIELDS)
    if set(hypothesis) != {*fields, "evidence"}:
        return "UNKNOWN"
    if hypothesis["evidence"] != trial.NORMALIZE_BINDINGS:
        return "UNKNOWN"
    for name, values in fields.items():
        if type(hypothesis[name]) is not type(values[0]) or hypothesis[name] not in values:
            return "UNKNOWN"
    return json.dumps(hypothesis, sort_keys=True, separators=(",", ":"))


def render_normalize(function: str, declaration: str, hypothesis_json: str) -> str | None:
    if function != "FUN_24dd_455e" or hypothesis_json == "UNKNOWN":
        return None
    try:
        hypothesis = json.loads(hypothesis_json)
    except (TypeError, ValueError):
        return None
    if not isinstance(hypothesis, dict) or classify_normalize(
        json.dumps(hypothesis, sort_keys=True)
    ) == "UNKNOWN":
        return None
    try:
        return trial.structured_lowering(function, hypothesis)
    except (KeyError, TypeError, ValueError):
        return None


NORMALIZE_LABELS = {
    "|".join(str(value) for value in values): {
        name: value for name, value in zip(trial.NORMALIZE_FIELDS, values)
    }
    for values in itertools.product(*trial.NORMALIZE_FIELDS.values())
}


def build_normalize_label_prompt(root: pathlib.Path, function: str) -> str:
    if function != "FUN_24dd_455e":
        raise ValueError(f"unsupported normalization routine: {function}")
    return (
        "Classify this signed 32-bit register normalization by the exact "
        "field sequence magnitude|exponent_bias|exponent_step|shift_direction|"
        "clear_fraction_top_bit|zero_input.\n"
        f"Allowed values by position: {json.dumps(trial.NORMALIZE_FIELDS, sort_keys=True)}.\n"
        "Reply with exactly one label and no explanation; do not write JSON or Pascal.\n"
        f"Assembly:\n{trial.instruction_listing(root, function)}\n"
        f"Original bytes:\n{trial.routine_spec(function)['bytes']}\n"
        f"Byte-backed evidence:\n{json.dumps(trial.NORMALIZE_BINDINGS, sort_keys=True)}\n"
    )


def classify_normalize_label(response: str) -> str:
    text = response.strip()
    if text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    if text in NORMALIZE_LABELS:
        return text
    return "UNKNOWN"


def render_normalize_label(function: str, declaration: str, label: str) -> str | None:
    if function != "FUN_24dd_455e" or label not in NORMALIZE_LABELS:
        return None
    hypothesis = {**NORMALIZE_LABELS[label], "evidence": dict(trial.NORMALIZE_BINDINGS)}
    try:
        return trial.structured_lowering(function, hypothesis)
    except (KeyError, TypeError, ValueError):
        return None


ARITHMETIC_LABELS = {
    "|".join(str(value) for value in values): {
        name: value for name, value in zip(trial.ARITHMETIC_FIELDS, values)
    }
    for values in itertools.product(*trial.ARITHMETIC_FIELDS.values())
}


def build_arithmetic_label_prompt(root: pathlib.Path, function: str) -> str:
    if function != "FUN_249c_0013":
        raise ValueError(f"unsupported arithmetic routine: {function}")
    return (
        "Classify this SS-relative byte arithmetic routine by the exact field "
        "sequence left_cell|right_cell|shift|operation|output_cell|truncate_before_add.\n"
        f"Allowed values by position: {json.dumps(trial.ARITHMETIC_FIELDS, sort_keys=True)}.\n"
        "Reply with exactly one label and no explanation; do not write JSON or Pascal.\n"
        f"Assembly:\n{trial.instruction_listing(root, function)}\n"
        f"Original bytes:\n{trial.routine_spec(function)['bytes']}\n"
        f"Byte-backed evidence:\n{json.dumps(trial.ARITHMETIC_BINDINGS, sort_keys=True)}\n"
    )


def classify_arithmetic_label(response: str) -> str:
    text = response.strip()
    if text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()
    if text in ARITHMETIC_LABELS:
        return text
    return "UNKNOWN"


def render_arithmetic_label(function: str, declaration: str, label: str) -> str | None:
    if function != "FUN_249c_0013" or label not in ARITHMETIC_LABELS:
        return None
    hypothesis = {
        **ARITHMETIC_LABELS[label],
        "evidence": dict(trial.ARITHMETIC_BINDINGS),
    }
    try:
        return trial.structured_lowering(function, hypothesis)
    except (KeyError, TypeError, ValueError):
        return None
