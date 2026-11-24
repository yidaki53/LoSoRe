"""Load small, reviewed routine contracts shared by drafting and probes."""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any


class RoutineContractError(ValueError):
    """A checked routine contract is missing or internally inconsistent."""


_DERIVED_RETURN = re.compile(
    r"^(RETF?)(?:\s+(?:0X)?([0-9A-F]+))?$", re.I
)
_DERIVED_ABSOLUTE = re.compile(
    r"(?:CS|SS|FS|GS)\s*:\s*\[\s*(?:0X)?[0-9A-F]{1,4}\s*\]",
    re.I,
)
_DERIVED_LITERAL_OFFSET = re.compile(
    r"(?:(?:DS|ES)\s*:\s*)?\[\s*(?:0X)?([0-9A-F]{1,4})\s*\]", re.I
)
_DERIVED_SEGMENT_WRITE = re.compile(
    r"^(?:MOV\s+(?:DS|ES)\s*,|MOV\s+\w+\s*,\s*(?:CS|DS|ES|SS)\b)", re.I
)
_DERIVED_POINTER_LOAD = re.compile(r"^L(?:DS|ES)\s+\w+\s*,\s*(.+)$", re.I)
_DERIVED_SEGMENT_REGISTER_MOVE = re.compile(
    r"^(?:"
    r"MOV\s+(DS|ES)\s*,\s*(AX|BX|CX|DX|SI|DI|BP|SP)"
    r"|MOV\s+(AX|BX|CX|DX|SI|DI|BP|SP)\s*,\s*(CS|DS|ES|SS)"
    r")$",
    re.I,
)
_DERIVED_SEGMENT_PUSH = re.compile(r"^PUSH\s+(DS|ES)\b", re.I)
_DERIVED_SEGMENT_POP = re.compile(r"^POP\s+(DS|ES)\b", re.I)
_DERIVED_DEVICE = re.compile(r"^(INT|INTO|IN|OUT|IRET)\b", re.I)
_DERIVED_REP_COUNT = re.compile(r"^MOV\s+CX,\s*(?:0X)?([0-9A-F]+)$", re.I)
_DERIVED_STRING_OPERATION = re.compile(
    r"^(?:MOVS|STOS|LODS|CMPS|SCAS)\w*", re.I
)
_DERIVED_IMMEDIATE_LOAD = re.compile(
    r"^MOV\s+(?:WORD PTR\s+)?(?:SI|DI),\s*(?:0X)?[0-9A-F]+$", re.I
)
_DERIVED_BRACKET = re.compile(r"\[([^\]]+)\]")
_DERIVED_HEX_NUMBER = re.compile(r"(?:0X)?([0-9A-F]+)", re.I)
DERIVED_REP_LIMIT = 4096


def _safe_high_absolute_xchg(instruction: str) -> bool:
    upper = instruction.strip().upper()
    return upper.startswith("XCHG") and "WORD PTR" in upper


def unsafe_absolute_memory(
    instructions: Any, allow_data_segment: bool = False
) -> bool:
    if isinstance(instructions, str):
        lines = instructions.splitlines()
    else:
        lines = [str(item) for item in instructions]
    pending_segments: list[str] = []
    for line in lines:
        instruction = line.strip()
        push = _DERIVED_SEGMENT_PUSH.match(instruction)
        if push is not None:
            pending_segments.append(push.group(1).upper())
            continue
        pop = _DERIVED_SEGMENT_POP.match(instruction)
        if pop is not None:
            if not pending_segments or pending_segments[-1] != pop.group(1).upper():
                return True
            pending_segments.pop()
            continue
        if _DERIVED_ABSOLUTE.search(instruction):
            return True
        pointer_load = _DERIVED_POINTER_LOAD.fullmatch(instruction)
        if pointer_load is not None:
            operand = pointer_load.group(1)
            for match in _DERIVED_LITERAL_OFFSET.finditer(operand):
                if int(match.group(1), 16) > 0x0FFF and not allow_data_segment:
                    return True
            for bracket in _DERIVED_BRACKET.findall(operand):
                for token in _DERIVED_HEX_NUMBER.findall(bracket):
                    if int(token, 16) > 0x0FFF and not allow_data_segment:
                        return True
            continue
        if _DERIVED_SEGMENT_WRITE.match(instruction):
            move = _DERIVED_SEGMENT_REGISTER_MOVE.fullmatch(instruction)
            if move is None:
                return True
            destination = (move.group(1) or "").upper()
            if destination in {"DS", "ES"} and destination not in pending_segments:
                return True
            continue
        allow_high_literal = allow_data_segment and _safe_high_absolute_xchg(
            instruction
        )
        for match in _DERIVED_LITERAL_OFFSET.finditer(instruction):
            if int(match.group(1), 16) > 0x0FFF and not allow_high_literal:
                return True
        for bracket in _DERIVED_BRACKET.findall(instruction):
            for token in _DERIVED_HEX_NUMBER.findall(bracket):
                if int(token, 16) > 0x0FFF and not allow_high_literal:
                    return True
    return bool(pending_segments)


def string_destination_mode(instructions: Any) -> bool:
    if isinstance(instructions, str):
        lines = instructions.splitlines()
    else:
        lines = [str(item) for item in instructions]
    return any(
        _DERIVED_STRING_OPERATION.match(
            re.sub(r"^(?:L[DE]S|REP)\s+", "", line.strip(), flags=re.I)
        )
        for line in lines
    )


def absolute_memory_mode(instructions: Any) -> bool:
    if isinstance(instructions, str):
        lines = instructions.splitlines()
    else:
        lines = [str(item) for item in instructions]
    if any(_DERIVED_LITERAL_OFFSET.search(line.strip()) for line in lines):
        return True
    return any(_DERIVED_STRING_OPERATION.match(line.strip()) for line in lines) and any(
        _DERIVED_IMMEDIATE_LOAD.match(line.strip()) for line in lines
    )


def load_contracts(path: pathlib.Path) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RoutineContractError(f"could not read routine contracts: {path}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise RoutineContractError(f"unsupported routine contract file: {path}")
    functions = data.get("functions")
    if not isinstance(functions, dict):
        raise RoutineContractError(
            f"routine contract functions must be an object: {path}"
        )
    contracts: dict[str, dict[str, Any]] = {}
    for name, contract in functions.items():
        if not isinstance(name, str) or not isinstance(contract, dict):
            raise RoutineContractError(f"invalid routine contract entry: {path}")
        declaration = contract.get("declaration")
        if not isinstance(declaration, str) or not _declaration_matches(
            declaration, name
        ):
            raise RoutineContractError(
                f"{name}: checked declaration is missing or names another routine"
            )
        prompt = contract.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            raise RoutineContractError(f"{name}: contract prompt must be non-empty")
        for field in (
            "instruction_semantics",
            "scoped_instruction_semantics",
            "fixture_flag_table",
        ):
            value = contract.get(field)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise RoutineContractError(
                    f"{name}: {field} must be a non-empty string"
                )
        repair_region = contract.get("localized_repair_region")
        if repair_region is not None and (
            not isinstance(repair_region, dict)
            or any(
                not isinstance(repair_region.get(field), str)
                or not repair_region[field].strip()
                or "\n" in repair_region[field]
                or "\r" in repair_region[field]
                for field in ("start", "end")
            )
        ):
            raise RoutineContractError(f"{name}: invalid localized repair region")
        if not isinstance(contract.get("oracle"), str):
            raise RoutineContractError(f"{name}: oracle id must be a string")
        arguments = contract.get("arguments", [])
        if not isinstance(arguments, list) or any(
            not isinstance(argument, dict)
            or any(
                not isinstance(argument.get(field), str) or not argument[field].strip()
                for field in ("name", "role", "representation")
            )
            for argument in arguments
        ):
            raise RoutineContractError(f"{name}: invalid argument contract")
        memory_model = contract.get("memory_model")
        if memory_model is not None and not isinstance(memory_model, str):
            raise RoutineContractError(f"{name}: memory model must be a string")
        observed_outputs = contract.get("observed_outputs", [])
        if not isinstance(observed_outputs, list) or any(
            not isinstance(output, str) or not output.strip()
            for output in observed_outputs
        ):
            raise RoutineContractError(f"{name}: invalid observed outputs")
        contracts[name] = contract
    for name, contract in contracts.items():
        callees = contract.get("callee_contracts", [])
        if not isinstance(callees, list) or any(
            not isinstance(callee, str) or callee == name or callee not in contracts
            for callee in callees
        ):
            raise RoutineContractError(f"{name}: invalid or missing callee contract")
        if len(set(callees)) != len(callees):
            raise RoutineContractError(f"{name}: duplicate callee contract")
    return contracts


def prompt_context(contract: dict[str, Any]) -> str:
    """Oracle: render supplied scoped facts, not dependency or source acceptance."""
    details = [f"Checked declaration: {contract['declaration']}"]
    if contract.get("scope"):
        details.append(f"Scope: {contract['scope']}")
    if contract.get("arguments"):
        details.append(
            "Arguments:\n"
            + "\n".join(
                f"- {argument['name']} ({argument['role']}): "
                f"{argument['representation']}"
                for argument in contract["arguments"]
            )
        )
    if contract.get("memory_model"):
        details.append(f"Memory model: {contract['memory_model']}")
    if contract.get("observed_outputs"):
        details.append("Observed outputs: " + ", ".join(contract["observed_outputs"]))
    for field, label in (
        ("instruction_semantics", "Instruction-level semantics"),
        ("scoped_instruction_semantics", "Scoped instruction-level semantics"),
        ("fixture_flag_table", "Original trace flag table"),
    ):
        if contract.get(field):
            details.append(f"{label}:\n{contract[field]}")
    return "\n".join(details) + "\n" + contract["prompt"]


def load_contract(
    target_root: pathlib.Path, function_name: str
) -> dict[str, Any] | None:
    contracts_path = target_root / "config" / "routine_contracts.json"
    return load_contracts(contracts_path).get(function_name)


def _signed_frame_params(instructions: list[str]) -> set[int]:
    result: set[int] = set()
    signed_branch = re.compile(r"^J(?:GE|LE|JL|JG)\b", re.I)
    cmp_instruction = re.compile(r"^CMP\b", re.I)
    frame_slot = re.compile(r"\bBP\s*\+\s*0X([0-9A-F]+)\b", re.I)
    for index, instruction in enumerate(instructions):
        if signed_branch.match(instruction.strip()) is None:
            continue
        for previous in reversed(instructions[:index]):
            if cmp_instruction.match(previous.strip()) is None:
                continue
            for expression in re.findall(r"\[([^\]]+)\]", previous.upper()):
                match = frame_slot.search(expression)
                if match is None:
                    continue
                offset = int(match.group(1), 16)
                if offset >= 4 and (offset - 4) % 2 == 0:
                    result.add((offset - 4) // 2 + 1)
            break
    return result


def _returns_ax_value(instructions: list[str]) -> bool:
    returns = [
        index
        for index, instruction in enumerate(instructions)
        if re.match(r"^RET(?:F)?\b", instruction.strip(), re.I)
    ]
    if len(returns) != 1:
        return False
    tail = instructions[max(0, returns[0] - 8):returns[0]]
    local_load = re.compile(
        r"^MOV\s+AX\s*,\s*(?:WORD PTR\s+)?\[\s*BP\s*"
        r"(?:[+-]\s*)?(?:[+-]\s*)?0X[0-9A-F]+\s*\]$",
        re.I,
    )
    memory_exchange = re.compile(
        r"^XCHG\s+(?:AX\s*,\s*(?:WORD PTR\s+)?\[[^\]]+\]"
        r"|(?:WORD PTR\s+)?\[[^\]]+\]\s*,\s*AX)$",
        re.I,
    )
    return any(
        local_load.match(instruction.strip())
        or memory_exchange.match(instruction.strip())
        for instruction in tail
    )


def derived_declaration(
    target_root: pathlib.Path, function_name: str
) -> str | None:
    from tools import asmcfg

    asm_path = target_root / "asm" / f"{function_name}.s"
    if not asm_path.is_file():
        return None
    parsed = asmcfg.parse_ghidra_asm(asm_path.read_text(errors="replace"))
    instructions = parsed["insts"]
    if not instructions:
        return None
    if not asmcfg.bounded_branch_paths(parsed):
        return None
    if any(
        asmcfg.is_call(inst) or _DERIVED_DEVICE.match(inst)
        for inst in instructions
    ) or unsafe_absolute_memory(
        instructions, allow_data_segment=absolute_memory_mode(instructions)
    ):
        return None
    for instruction in instructions:
        match = _DERIVED_REP_COUNT.fullmatch(instruction.strip())
        if match is not None and int(match.group(1), 16) > DERIVED_REP_LIMIT:
            return None
    returns = []
    for instruction in instructions:
        match = _DERIVED_RETURN.fullmatch(instruction)
        if match is not None:
            returns.append(match)
    if len(returns) != 1:
        return None
    cleanup_text = returns[0].group(2)
    cleanup = int(cleanup_text, 16) if cleanup_text else 0
    if cleanup % 2 or cleanup > 16:
        return None
    signed = _signed_frame_params(instructions)
    params = "; ".join(
        f"param_{index}: {'Integer' if index in signed else 'Word'}"
        for index in range(1, cleanup // 2 + 1)
    )
    signature = f"procedure {function_name}({params});" if params else (
        f"procedure {function_name};"
    )
    if _returns_ax_value(instructions):
        signature = signature.replace("procedure ", "function ", 1)
        signature = signature.rstrip(";") + ": Word;"
    return signature


def oracle_declaration(
    target_root: pathlib.Path, function_name: str
) -> str | None:
    contract = load_contract(target_root, function_name)
    if contract is not None:
        return contract["declaration"]
    return derived_declaration(target_root, function_name)


def pascal_declaration(source: str, function_name: str) -> str | None:
    for line in source.splitlines():
        if line.lstrip().startswith("//"):
            continue
        if _declaration_matches(line.strip(), function_name):
            return line.strip()
    return None


def _declaration_matches(declaration: str, function_name: str) -> bool:
    return bool(
        re.match(
            rf"^(?:procedure|function)\s+{re.escape(function_name)}\b"
            r"(?:\s*\([^()\r\n]*\))?\s*(?::\s*[^;\r\n]+)?;\s*$",
            declaration.strip(),
            re.IGNORECASE,
        )
    )
