"""Binary-derived instruction emulation renderer with no routine-identity dispatch."""

from __future__ import annotations

import re
from typing import Any

from engine import capability_dsl
from tools import asmcfg

SCHEMA_VERSION = 1
METHOD = "asm-emulation-v1"
FIXTURE_CS = 0x191

DECL = re.compile(
    r"^(procedure|function)\s+(\w+)"
    r"(?:\s*\((.*)\))?"
    r"\s*(?::\s*([\w^]+))?\s*;$",
    re.I,
)
REG16 = {"AX", "BX", "CX", "DX", "SI", "DI", "BP", "SP"}
REG8 = {"AL", "AH", "BL", "BH", "CL", "CH", "DL", "DH"}
SEGMENTS = {"DS", "ES", "SS", "CS"}
OPERAND_MASK = {1: 0xFF, 2: 0xFFFF}
UNSUPPORTED = re.compile(
    r"^(CALL|CALLF|INT|INTO|LOOP\w*|IRET|IN|OUT)\b",
    re.I,
)
_BRANCH_CONDITIONS = {
    "JZ": "RegisterZeroFlag",
    "JE": "RegisterZeroFlag",
    "JNZ": "not RegisterZeroFlag",
    "JNE": "not RegisterZeroFlag",
    "JC": "RegisterCarryFlag",
    "JB": "RegisterCarryFlag",
    "JNAE": "RegisterCarryFlag",
    "JNC": "not RegisterCarryFlag",
    "JAE": "not RegisterCarryFlag",
    "JNB": "not RegisterCarryFlag",
    "JS": "RegisterSignFlag",
    "JNS": "not RegisterSignFlag",
    "JO": "RegisterOverflowFlag",
    "JNO": "not RegisterOverflowFlag",
    "JL": "RegisterSignFlag <> RegisterOverflowFlag",
    "JNGE": "RegisterSignFlag <> RegisterOverflowFlag",
    "JGE": "RegisterSignFlag = RegisterOverflowFlag",
    "JNL": "RegisterSignFlag = RegisterOverflowFlag",
    "JLE": "RegisterZeroFlag or (RegisterSignFlag <> RegisterOverflowFlag)",
    "JNG": "RegisterZeroFlag or (RegisterSignFlag <> RegisterOverflowFlag)",
    "JG": "(not RegisterZeroFlag) and (RegisterSignFlag = RegisterOverflowFlag)",
    "JNLE": "(not RegisterZeroFlag) and (RegisterSignFlag = RegisterOverflowFlag)",
    "JA": "(not RegisterCarryFlag) and (not RegisterZeroFlag)",
    "JNBE": "(not RegisterCarryFlag) and (not RegisterZeroFlag)",
    "JBE": "RegisterCarryFlag or RegisterZeroFlag",
    "JNA": "RegisterCarryFlag or RegisterZeroFlag",
    "JCXZ": "RegisterCX = 0",
    "JECXZ": "RegisterCX = 0",
}


class Unsupported(Exception):
    pass


def _split_operands(text: str) -> list[str]:
    result: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(text):
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        elif char == "," and depth == 0:
            result.append(text[start:index].strip())
            start = index + 1
    result.append(text[start:].strip())
    return result


def _number(text: str) -> int | None:
    value = text.strip()
    if re.fullmatch(r"0[xX][0-9a-fA-F]+", value):
        return int(value, 16)
    if re.fullmatch(r"\d+", value):
        return int(value, 10)
    return None


def _offset_expression(text: str) -> str:
    expression = "0"
    for match in re.finditer(r"([+-]?)\s*(0[xX][0-9a-fA-F]+|\d+|[A-Za-z]+)", text):
        sign, term = match.groups()
        if term.upper() in REG16:
            value = "Register" + term.upper()
        else:
            number = _number(term)
            if number is None:
                raise Unsupported(f"unsupported memory term: {term}")
            value = f"${number:x}"
        if sign == "-":
            expression += f" - ({value})"
        elif sign == "+":
            expression += f" + ({value})"
        else:
            expression = f"({value})"
    return f"(({expression}) and $ffff)"


class _Translator:
    def __init__(self, evidence: dict[str, Any]):
        self.evidence = evidence
        contract = evidence.get("oracle_contract")
        declaration = contract.get("declaration", "") if isinstance(contract, dict) else ""
        match = DECL.fullmatch(declaration.strip())
        if match is None:
            raise Unsupported("checked declaration required for instruction emulation")
        self.kind, self.name, self.params_text, self.return_type = match.groups()
        self.kind = self.kind.lower()
        self.return_type = (self.return_type or "").lower()
        assembly = evidence.get("static_evidence", {}).get("assembly", {})
        self.instructions = [
            str(item).upper() for item in assembly.get("instructions", [])
        ]
        if not self.instructions:
            raise Unsupported("no instructions for instruction emulation")
        self.return_cleanup = 0
        self.entry_frame_bytes = 2
        for instruction in self.instructions:
            match = re.match(r"^RET(?:F)?(?:\s+0X([0-9A-F]+))?$", instruction.strip(), re.I)
            if match is not None:
                cleanup = int(match.group(1), 16) if match.group(1) else 0
                self.entry_frame_bytes = 4 if instruction.strip().upper().startswith("RETF") else 2
                self.return_cleanup = self.entry_frame_bytes + cleanup
                break
        if self.kind == "procedure":
            signed_params = self._signed_frame_params()
            if signed_params and self.params_text:
                groups = []
                for index, group in enumerate(self.params_text.split(";"), 1):
                    names, type_name = (part.strip() for part in group.split(":", 1))
                    if index in signed_params and type_name.lower() == "word":
                        type_name = "Integer"
                    groups.append(f"{names}: {type_name}")
                self.params_text = "; ".join(groups)
            if self._returns_ax_value():
                self.kind = "function"
                self.return_type = "word"
        self.addresses = [int(item) for item in assembly.get("addresses", [])]
        self.segments = [int(item) for item in assembly.get("segments", [])]
        raw_hex = str((evidence.get("bytes") or {}).get("hex", ""))
        self.raw = bytes.fromhex(raw_hex) if raw_hex else b""
        facts = (evidence.get("static_evidence") or {}).get("raw_byte_facts") or {}
        self.raw_offsets = [
            int(item["offset"]) for item in facts.get("instructions", [])
            if isinstance(item, dict) and "offset" in item
        ]
        if (
            len(self.raw_offsets) + 1 == len(self.instructions)
            and asmcfg.is_ret(self.instructions[-1])
        ):
            self.raw_offsets.append(-1)
        if len(self.raw_offsets) != len(self.instructions):
            self.raw_offsets = []
        self.index_by_address = {
            address: index for index, address in enumerate(self.addresses)
        }
        try:
            self.rules = capability_dsl.compile_rules(
                list(evidence.get("capability_rules", []))
            )
        except ValueError as exc:
            raise Unsupported(f"invalid capability rules: {exc}") from exc
        external_exit_enabled = any(
            rule["kind"] == "external_exit" for rule in self.rules
        )
        self.flags_hardware_word = any(
            rule["kind"] == "flags_hardware_word" for rule in self.rules
        )
        self.branch_targets: dict[int, int] = {}
        self.inlined_calls: dict[int, int] = {}
        self.call_return_indices: dict[int, int] = {}
        self.call_return_adjustments: dict[int, int] = {}
        self.external_branches: set[int] = set()
        self.external_exit: int | None = None
        for index, instruction in enumerate(self.instructions):
            if asmcfg.is_call(instruction):
                if index >= len(self.addresses) or index >= len(self.segments):
                    raise Unsupported("call without address metadata")
                target = asmcfg.resolve_branch_target(
                    instruction, self.segments[index]
                )
                destination = (
                    self.index_by_address.get(target) if target is not None else None
                )
                if destination is None or destination <= index:
                    raise Unsupported("unsupported call target")
                frame_words = 4 if instruction.upper().startswith("CALLF") else 2
                return_index = next(
                    (
                        candidate for candidate in range(destination, len(self.instructions))
                        if asmcfg.is_ret(self.instructions[candidate])
                    ),
                    None,
                )
                if return_index is None:
                    raise Unsupported("inlined call has no return")
                self.inlined_calls[index] = destination
                self.call_return_indices[index] = return_index
                self.call_return_adjustments[return_index] = frame_words
                continue
            if not asmcfg.is_branch(instruction):
                continue
            if index >= len(self.addresses) or index >= len(self.segments):
                raise Unsupported("branch without address metadata")
            target = asmcfg.resolve_branch_target(
                instruction, self.segments[index]
            )
            if target is None:
                raise Unsupported("unresolved branch target")
            destination = self.index_by_address.get(target)
            if destination is None:
                if not external_exit_enabled:
                    raise Unsupported("unsupported branch target")
                if self.kind != "procedure":
                    raise Unsupported("external branch in function")
                if self.external_exit is not None and self.external_exit != target:
                    raise Unsupported("multiple external branch targets")
                self.external_exit = target
                self.external_branches.add(index)
                continue
            self.branch_targets[index] = destination
        self.labels: set[int] = set()
        self.labels.update(self.branch_targets.values())
        self.lines: list[str] = []
        self.temps: list[tuple[str, str]] = []
        self.temp = 0
        self.state_variables = capability_dsl.state_variables(self.rules)
        self.extra_variables = [
            variable
            for variable in capability_dsl.variables(self.rules)
            if variable[0] not in self.state_variables
        ]

    def _next_temp(self, boolean: bool = False, kind: str = "LongInt") -> str:
        self.temp += 1
        name = f"emuTemp{self.temp}"
        self.temps.append((name, "Boolean" if boolean else kind))
        return name

    def _operand_size(self, operand: str, fallback: int = 2) -> int:
        upper = operand.upper()
        if "BYTE PTR" in upper:
            return 1
        if "WORD PTR" in upper:
            return 2
        if "DWORD PTR" in upper:
            return 4
        clean = re.sub(r"^(BYTE|WORD|DWORD)\s+PTR\s+", "", upper)
        if clean in REG8:
            return 1
        if clean in REG16 or clean in SEGMENTS:
            return 2
        memory = re.search(r"(?:[A-Z]{2}:)?\[.*\]", clean)
        if memory:
            return fallback
        number = _number(clean)
        if number is not None:
            return fallback
        if re.fullmatch(r"CODEMEMORY\[0X[0-9A-F]{1,8}\]", clean):
            return fallback
        raise Unsupported(f"cannot infer operand size: {operand}")

    def _clean(self, operand: str) -> str:
        value = re.sub(r"^(BYTE|WORD|DWORD)\s+PTR\s+", "", operand.strip(), flags=re.I)
        return value.upper()

    def _register_expression(self, reg: str) -> str:
        if reg in REG16 or reg in SEGMENTS:
            return "Register" + reg
        if reg in REG8:
            base, half = reg[0], reg[1]
            if half == "L":
                return f"(Register{base}X and $ff)"
            return f"(Register{base}X shr 8) and $ff"
        raise Unsupported(f"unsupported register: {reg}")

    def _register_assignment(self, reg: str, value: str) -> str:
        if reg in REG16 or reg in SEGMENTS:
            return f"Register{reg} := {value};"
        if reg in REG8:
            base, half = reg[0], reg[1]
            full = f"Register{base}X"
            if half == "L":
                return f"{full} := ({full} and $ff00) or ({value} and $ff);"
            return f"{full} := ({full} and $ff) or (({value} and $ff) shl 8);"
        raise Unsupported(f"unsupported register: {reg}")

    def _raw_segment_move(self, index: int, operation: str) -> list[str] | None:
        if operation != "MOV" or not self.raw or len(self.raw_offsets) != len(self.instructions):
            return None
        offset = self.raw_offsets[index]
        if offset < 0 or offset + 1 >= len(self.raw):
            return None
        opcode = self.raw[offset]
        if opcode not in (0x8C, 0x8E):
            return None
        modrm = self.raw[offset + 1]
        if modrm & 0xC0 != 0xC0:
            return None
        segment = ("ES", "CS", "SS", "DS")[(modrm >> 3) & 3]
        register = ("AX", "CX", "DX", "BX", "SP", "BP", "SI", "DI")[modrm & 7]
        return [register, segment] if opcode == 0x8C else [segment, register]

    def _memory(self, operand: str) -> tuple[str, str, int]:
        clean = self._clean(operand)
        match = re.fullmatch(r"(?:([A-Z]{2}):)?\[(.*)\]", clean)
        if match is None:
            raise Unsupported(f"unsupported operand: {operand}")
        prefix, expression = match.groups()
        if prefix and prefix not in SEGMENTS:
            raise Unsupported(f"unsupported segment prefix: {prefix}")
        size = self._operand_size(operand, 2)
        if re.fullmatch(r"\s*(?:0[xX][0-9a-fA-F]+|\d+)\s*", expression):
            if prefix not in (None, "DS", "ES"):
                raise Unsupported(f"unsupported absolute segment: {prefix}")
            return (
                f"Register{prefix or 'DS'}",
                f"({_offset_expression(expression)} and $ffff)",
                size,
            )
        segment = prefix or ("SS" if "BP" in expression else "DS")
        return f"Register{segment}", _offset_expression(expression), size

    def _read(self, operand: str, size: int | None = None) -> str:
        clean = self._clean(operand)
        resolved = size or self._operand_size(operand)
        if clean == "CS":
            return f"${FIXTURE_CS:x}"
        if clean in REG16 or clean in REG8 or clean in SEGMENTS:
            return self._register_expression(clean)
        number = _number(clean)
        if number is not None:
            return f"${number:x}"
        code_memory = re.fullmatch(r"CODEMEMORY\[0X([0-9A-F]{1,8})\]", clean)
        if code_memory is not None:
            address = int(code_memory.group(1), 16)
            if resolved == 1:
                return f"CodeMemory[${address:x}]"
            if resolved == 2:
                return (
                    f"(Word(CodeMemory[${address:x}]) or "
                    f"(Word(CodeMemory[${address + 1:x}]) shl 8))"
                )
            raise Unsupported("dword code-memory reads are not supported")
        segment, offset, memory_size = self._memory(operand)
        if resolved != memory_size and memory_size != 4:
            raise Unsupported(f"operand size mismatch: {operand}")
        if resolved == 1:
            return f"LEmuMemB({segment}, {offset})"
        if resolved == 2:
            return f"LEmuMemW({segment}, {offset})"
        raise Unsupported("dword reads are not supported")

    def _write(self, operand: str, value: str, size: int | None = None) -> str:
        clean = self._clean(operand)
        resolved = size or self._operand_size(operand)
        if clean in REG16 or clean in REG8 or clean in SEGMENTS:
            return self._register_assignment(clean, value)
        segment, offset, memory_size = self._memory(operand)
        if resolved != memory_size:
            raise Unsupported(f"operand size mismatch: {operand}")
        if resolved == 1:
            return f"LEmuSetB({segment}, {offset}, {value});"
        if resolved == 2:
            return f"LEmuSetW({segment}, {offset}, {value});"
        raise Unsupported("dword writes are not supported")

    def _emit_flags(
        self,
        result: str,
        carry: str,
        mask: int,
        overflow: str = "False",
    ) -> None:
        sign_bit = (mask >> 1) + 1
        if self.flags_hardware_word:
            self.lines.append(
                f"LEmuSetResultFlags({result}, {carry}, {overflow});"
            )
            return
        self.lines.append(f"RegisterCarryFlag := {carry};")
        self.lines.append(f"RegisterZeroFlag := ({result}) = 0;")
        self.lines.append(f"RegisterSignFlag := (({result}) and ${sign_bit:x}) <> 0;")
        self.lines.append(f"RegisterOverflowFlag := {overflow};")

    def _emit_binary(self, operation: str, operands: list[str]) -> None:
        if len(operands) != 2:
            raise Unsupported(f"unsupported {operation} operands")
        size = self._operand_size(operands[0])
        mask = OPERAND_MASK.get(size)
        if mask is None:
            raise Unsupported(f"unsupported binary operand width: {size}")
        left = self._read(operands[0], size)
        right = self._read(operands[1], size)
        result = self._next_temp()
        carry = self._next_temp(boolean=True)
        sign_bit = (mask >> 1) + 1
        self.lines.append(f"{result} := ({left}) and ${mask:x};")
        right_expr = f"(({right}) and ${mask:x})"
        overflow = "False"
        if operation in {"ADD", "ADC"}:
            if operation == "ADD":
                self.lines.append(
                    f"{carry} := LongInt({result}) + LongInt({right_expr}) > ${mask:x};"
                )
                expression = f"LongInt({result}) + LongInt({right_expr})"
            else:
                self.lines.append(
                    f"{carry} := LongInt({result}) + LongInt({right_expr}) + "
                    f"LongInt(RegisterCarryFlag) > ${mask:x};"
                )
                expression = (
                    f"LongInt({result}) + LongInt({right_expr}) + "
                    "LongInt(RegisterCarryFlag)"
                )
            overflow = (
                f"(LongInt(({left}) xor ({result})) and "
                f"LongInt(({right}) xor ({result})) and ${sign_bit:x}) <> 0"
            )
        elif operation in {"SUB", "CMP", "SBB"}:
            if operation == "SBB":
                self.lines.append(
                    f"{carry} := LongInt({result}) < LongInt({right_expr}) + "
                    "LongInt(RegisterCarryFlag);"
                )
                expression = (
                    f"LongInt({result}) - LongInt({right_expr}) - "
                    "LongInt(RegisterCarryFlag)"
                )
            else:
                self.lines.append(
                    f"{carry} := LongInt({result}) < LongInt({right_expr});"
                )
                expression = f"LongInt({result}) - LongInt({right_expr})"
            overflow = (
                f"(LongInt(({left}) xor ({right})) and "
                f"LongInt(({left}) xor ({result})) and ${sign_bit:x}) <> 0"
            )
        elif operation in {"AND", "OR", "XOR"}:
            self.lines.append(f"{carry} := False;")
            symbol = {"AND": "and", "OR": "or", "XOR": "xor"}[operation]
            expression = f"LongInt({result}) {symbol} LongInt({right_expr})"
        else:
            raise Unsupported(f"unsupported binary operation: {operation}")
        self.lines.append(f"{result} := ({expression}) and ${mask:x};")
        self._emit_flags(result, carry, mask, overflow)
        if operation != "CMP":
            self.lines.append(self._write(operands[0], result, size))

    def _emit_shift(self, operation: str, operands: list[str]) -> None:
        if len(operands) != 2:
            raise Unsupported(f"unsupported {operation} operands")
        size = self._operand_size(operands[0])
        mask = OPERAND_MASK.get(size)
        if mask is None:
            raise Unsupported(f"unsupported shift operand width: {size}")
        width = 8 if size == 1 else 16
        sign_bit = (mask >> 1) + 1
        value = self._read(operands[0], size)
        count = self._read(operands[1], 2)
        result = self._next_temp()
        carry = self._next_temp(boolean=True)
        count_name = self._next_temp()
        self.lines.append(f"{count_name} := ({count}) and $1f;")
        self.lines.append(f"{result} := ({value}) and ${mask:x};")
        self.lines.append(f"if {count_name} = 0 then begin")
        self.lines.append(f"  {carry} := RegisterCarryFlag;")
        self.lines.append(
            f"end else if {count_name} >= {width} then begin"
        )
        self.lines.append(f"  {result} := 0;")
        self.lines.append(f"  {carry} := False;")
        self.lines.append("  RegisterZeroFlag := True;")
        self.lines.append("end else begin")
        if operation == "SHL":
            self.lines.append(
                f"  {carry} := (({result}) shr ({width} - {count_name})) and 1 <> 0;"
            )
            expression = f"({result} shl {count_name}) and ${mask:x}"
        elif operation == "SHR":
            self.lines.append(
                f"  {carry} := (({result}) shr ({count_name} - 1)) and 1 <> 0;"
            )
            expression = f"({result} shr {count_name}) and ${mask:x}"
        else:
            raise Unsupported(f"unsupported shift: {operation}")
        self.lines.append(f"  {result} := {expression};")
        self.lines.append(f"  RegisterZeroFlag := ({result}) = 0;")
        self.lines.append("end;")
        self.lines.append(f"RegisterSignFlag := (({result}) and ${sign_bit:x}) <> 0;")
        self.lines.append("RegisterOverflowFlag := False;")
        self.lines.append(self._write(operands[0], result, size))

    def _emit_incdec(self, operation: str, operand: str) -> None:
        size = self._operand_size(operand)
        mask = OPERAND_MASK.get(size)
        if mask is None:
            raise Unsupported(f"unsupported increment operand width: {size}")
        value = self._read(operand, size)
        result = self._next_temp()
        delta = 1 if operation == "INC" else -1
        sign_bit = (mask >> 1) + 1
        overflow_value = sign_bit - 1 if operation == "INC" else sign_bit
        self.lines.append(
            f"{result} := (LongInt({value}) + {delta}) and ${mask:x};"
        )
        self.lines.append(f"RegisterZeroFlag := ({result}) = 0;")
        self.lines.append(f"RegisterSignFlag := (({result}) and ${sign_bit:x}) <> 0;")
        self.lines.append(f"RegisterOverflowFlag := ({value}) = ${overflow_value:x};")
        self.lines.append(self._write(operand, result, size))

    def _emit_mul(self, operands: list[str]) -> None:
        if len(operands) != 1:
            raise Unsupported("unsupported MUL operands")
        operand = operands[0]
        size = self._operand_size(operand)
        value = self._read(operand, size)
        product = self._next_temp(kind="Int64")
        if size == 1:
            self.lines.append(f"{product} := Int64(RegisterAX and $ff) * Int64({value});")
            self.lines.append(f"RegisterAX := Word({product} and $ffff);")
            self.lines.append(f"RegisterCarryFlag := {product} > $ff;")
            self.lines.append(f"RegisterZeroFlag := (RegisterAX and $ff) = 0;")
            self.lines.append("RegisterSignFlag := (RegisterAX and $80) <> 0;")
            self.lines.append("RegisterOverflowFlag := False;")
        elif size == 2:
            self.lines.append(f"{product} := Int64(RegisterAX) * Int64({value});")
            self.lines.append(f"RegisterAX := Word({product} and $ffff);")
            self.lines.append(f"RegisterDX := Word(({product} shr 16) and $ffff);")
            self.lines.append(f"RegisterCarryFlag := RegisterDX <> 0;")
            self.lines.append("RegisterZeroFlag := RegisterAX = 0;")
            self.lines.append("RegisterSignFlag := (RegisterAX and $8000) <> 0;")
            self.lines.append("RegisterOverflowFlag := False;")
        else:
            raise Unsupported("unsupported MUL width")

    def _emit_div(self, operands: list[str]) -> None:
        if len(operands) != 1:
            raise Unsupported("unsupported DIV operands")
        operand = operands[0]
        size = self._operand_size(operand)
        value = self._read(operand, size)
        quotient = self._next_temp(kind="Int64")
        remainder = self._next_temp(kind="Int64")
        dividend = self._next_temp(kind="Int64")
        if size == 1:
            self.lines.append(f"{dividend} := Int64(RegisterAX);")
        elif size == 2:
            self.lines.append(f"{dividend} := Int64(RegisterDX) * 65536 + RegisterAX;")
        else:
            raise Unsupported("unsupported DIV width")
        if size == 1:
            self.lines.append(f"{quotient} := {dividend} div Int64({value});")
            self.lines.append(f"{remainder} := {dividend} mod Int64({value});")
            self.lines.append(self._register_assignment("AL", quotient))
            self.lines.append(self._register_assignment("AH", remainder))
        else:
            self.lines.append(f"{quotient} := {dividend} div Int64({value});")
            self.lines.append(f"{remainder} := {dividend} mod Int64({value});")
            self.lines.append(self._register_assignment("AX", quotient))
            self.lines.append(self._register_assignment("DX", remainder))
        self.lines.append("RegisterCarryFlag := False;")
        self.lines.append(f"RegisterZeroFlag := ({quotient}) = 0;")
        self.lines.append("RegisterSignFlag := (RegisterAX and $8000) <> 0;")
        self.lines.append("RegisterOverflowFlag := False;")

    def _emit_decimal_adjust(self, operation: str, operands: list[str]) -> None:
        if len(operands) > 1:
            raise Unsupported(f"unsupported {operation} operands")
        base = _number(operands[0]) if operands else 0x0A
        if base is None or base < 1 or base > 0xFF:
            raise Unsupported(f"unsupported {operation} base")
        self.lines.append("RegisterCarryFlag := False;")
        if operation == "AAM":
            quotient = self._next_temp()
            remainder = self._next_temp()
            self.lines.append(f"{quotient} := (RegisterAX and $ff) div {base};")
            self.lines.append(f"{remainder} := (RegisterAX and $ff) mod {base};")
            self.lines.append(self._register_assignment("AH", quotient))
            self.lines.append(self._register_assignment("AL", remainder))
        else:
            self.lines.append(self._register_assignment(
                "AL",
                f"(((RegisterAX shr 8) and $ff) * {base} + "
                "(RegisterAX and $ff)) and $ff",
            ))
            self.lines.append(self._register_assignment("AH", "0"))
        self.lines.append("RegisterZeroFlag := (RegisterAX and $ff) = 0;")
        self.lines.append("RegisterSignFlag := (RegisterAX and $80) <> 0;")
        self.lines.append("RegisterOverflowFlag := False;")

    def _emit_test(self, operands: list[str]) -> None:
        if len(operands) != 2:
            raise Unsupported("unsupported TEST operands")
        size = self._operand_size(operands[0])
        mask = OPERAND_MASK.get(size)
        if mask is None:
            raise Unsupported(f"unsupported TEST operand width: {size}")
        left = self._read(operands[0], size)
        right = self._read(operands[1], size)
        result = self._next_temp()
        self.lines.append(
            f"{result} := (({left}) and ${mask:x}) and (({right}) and ${mask:x});"
        )
        self.lines.append("RegisterCarryFlag := False;")
        self.lines.append(f"RegisterZeroFlag := ({result}) = 0;")
        self.lines.append(f"RegisterSignFlag := (({result}) and ${(mask >> 1) + 1:x}) <> 0;")
        self.lines.append("RegisterOverflowFlag := False;")

    def _emit_neg_not(self, operation: str, operand: str) -> None:
        size = self._operand_size(operand)
        mask = OPERAND_MASK.get(size)
        if mask is None:
            raise Unsupported(f"unsupported {operation} operand width: {size}")
        value = self._next_temp()
        result = self._next_temp()
        sign_bit = (mask >> 1) + 1
        self.lines.append(f"{value} := ({self._read(operand, size)}) and ${mask:x};")
        self.lines.append("RegisterOverflowFlag := False;")
        if operation == "NEG":
            self.lines.append(
                f"{result} := (0 - LongInt({value})) and ${mask:x};"
            )
            self.lines.append(f"RegisterCarryFlag := {value} <> 0;")
            self.lines.append(f"RegisterZeroFlag := ({result}) = 0;")
            self.lines.append(f"RegisterSignFlag := (({result}) and ${sign_bit:x}) <> 0;")
            self.lines.append(f"RegisterOverflowFlag := ({value}) = ${sign_bit:x};")
        elif operation == "NOT":
            self.lines.append(f"{result} := LongInt(not {value}) and ${mask:x};")
            self.lines.append(f"RegisterSignFlag := (({result}) and ${sign_bit:x}) <> 0;")
        else:
            raise Unsupported(f"unsupported operation: {operation}")
        self.lines.append(self._write(operand, result, size))

    def _emit_sign_extend(self, operation: str) -> None:
        if operation == "CWD":
            self.lines.append(
                "RegisterDX := $ffff; if (RegisterAX and $8000) = 0 then RegisterDX := 0;"
            )
        elif operation == "CBW":
            self.lines.append("RegisterAX := RegisterAX and $ff;")
            self.lines.append(
                "if (RegisterAX and $80) <> 0 then RegisterAX := RegisterAX or $ff00;"
            )
        else:
            raise Unsupported(f"unsupported operation: {operation}")

    def _emit_imul(self, operands: list[str]) -> None:
        if len(operands) == 1:
            left = "RegisterAX"
            right = self._read(operands[0], 2)
            destination = None
        elif len(operands) == 2:
            left = self._read(operands[0], 2)
            right = self._read(operands[1], 2)
            destination = operands[0]
        elif len(operands) == 3:
            left = self._read(operands[1], 2)
            right = self._read(operands[2], 2)
            destination = operands[0]
        else:
            raise Unsupported("unsupported IMUL operands")
        product = self._next_temp()
        self.lines.append(
            f"{product} := "
            f"LEmuSigned16(Word(({left}) and $ffff)) * "
            f"LEmuSigned16(Word(({right}) and $ffff));"
        )
        self.lines.append(
            f"RegisterCarryFlag := ({product} < -32768) or ({product} > 32767);"
        )
        self.lines.append(f"RegisterSignFlag := ({product} < 0);")
        self.lines.append("RegisterOverflowFlag := RegisterCarryFlag;")
        if destination is None:
            self.lines.append(
                f"RegisterAX := Word({product} and $ffff);"
            )
            self.lines.append(
                f"RegisterDX := Word(({product} shr 16) and $ffff);"
            )
        else:
            self.lines.append(
                self._write(destination, f"Word({product} and $ffff)", 2)
            )

    def _emit_rotate(self, operation: str, operands: list[str]) -> None:
        if len(operands) != 2:
            raise Unsupported(f"unsupported {operation} operands")
        size = self._operand_size(operands[0])
        mask = OPERAND_MASK.get(size)
        if mask is None:
            raise Unsupported(f"unsupported {operation} operand width: {size}")
        width = 8 if size == 1 else 16
        sign_bit = (mask >> 1) + 1
        value = self._read(operands[0], size)
        count = self._read(operands[1], 2)
        result = self._next_temp()
        carry = self._next_temp(boolean=True)
        count_name = self._next_temp()
        bit = self._next_temp(boolean=True)
        self.lines.append(f"{count_name} := ({count}) and $1f;")
        self.lines.append(f"{result} := ({value}) and ${mask:x};")
        self.lines.append(f"if {count_name} = 0 then begin")
        self.lines.append(f"  {carry} := RegisterCarryFlag;")
        self.lines.append("end else begin")
        self.lines.append(f"  {count_name} := {count_name} mod {width + 1};")
        self.lines.append(f"  while {count_name} > 0 do begin")
        if operation == "RCL":
            self.lines.append(
                f"    {bit} := (({result}) shr {width - 1}) and 1 <> 0;"
            )
            self.lines.append(
                f"    {result} := ((({result} shl 1) and ${mask:x}) or "
                "LongInt(RegisterCarryFlag)) and ${mask:x};"
            )
        elif operation == "RCR":
            self.lines.append(f"    {bit} := ({result}) and 1 <> 0;")
            self.lines.append(
                f"    {result} := (({result} shr 1) or "
                f"(LongInt(RegisterCarryFlag) shl {width - 1})) and ${mask:x};"
            )
        else:
            raise Unsupported(f"unsupported rotate: {operation}")
        self.lines.append(f"    RegisterCarryFlag := {bit};")
        self.lines.append(f"    Dec({count_name});")
        self.lines.append("  end;")
        self.lines.append("end;")
        self.lines.append(f"RegisterSignFlag := (({result}) and ${sign_bit:x}) <> 0;")
        self.lines.append(self._write(operands[0], result, size))

    def _emit_string(self, operation: str, operand_text: str) -> None:
        base, _, suffix = operation.partition(".")
        suffix = suffix.upper()
        rep = suffix in {"REP", "REPE", "REPZ", "REPNE", "REPNZ"}
        size = {
            "MOVSB": 1, "MOVSW": 2, "MOVSD": 4,
            "STOSB": 1, "STOSW": 2,
            "LODSB": 1, "LODSW": 2,
            "CMPSB": 1, "CMPSW": 2,
            "SCASB": 1, "SCASW": 2,
        }.get(base)
        if size is None:
            raise Unsupported(f"unsupported string operation: {operation}")
        operands = _split_operands(operand_text) if operand_text else []
        destination_segment = "RegisterES"
        source_segment = "RegisterDS"
        for operand in operands:
            match = re.fullmatch(r"([A-Z]{2}):[A-Z]+", self._clean(operand))
            if match and match.group(1) in SEGMENTS:
                segment = f"Register{match.group(1)}"
                if base.startswith(("STOS", "MOVS", "CMPS", "SCAS")):
                    destination_segment = segment
                else:
                    source_segment = segment
        self.lines.append("emuStep := 1;")
        self.lines.append("if RegisterDirectionFlag then emuStep := -1;")
        if suffix in {"REPE", "REPZ"}:
            condition = "(RegisterCX <> 0) and RegisterZeroFlag"
        elif suffix in {"REPNE", "REPNZ"}:
            condition = "(RegisterCX <> 0) and (not RegisterZeroFlag)"
        else:
            condition = "RegisterCX <> 0"
        prefix = f"while {condition} do\n  begin\n" if rep else "begin\n"
        suffix_text = "    Dec(RegisterCX);\n  end;\n" if rep else "end;\n"
        body = []
        is_store = base.startswith("STOS")
        is_move = base.startswith("MOVS")
        is_compare = base.startswith(("CMPS", "SCAS"))
        is_scas = base.startswith("SCAS")
        value_words = size // 2 if size > 1 else 1
        if is_compare:
            left = self._next_temp()
            right = self._next_temp()
            difference = self._next_temp()
            carry = self._next_temp(boolean=True)
            overflow = self._next_temp(boolean=True)
            parity = self._next_temp(boolean=True)
            parity_byte = self._next_temp()
            mask = 0xFF if size == 1 else 0xFFFF
            sign_bit = 0x80 if size == 1 else 0x8000
            source = (
                f"LEmuMemB({source_segment}, RegisterSI)" if size == 1
                else f"LEmuMemW({source_segment}, RegisterSI)"
            )
            destination = (
                f"(RegisterAX and $ff)" if is_scas and size == 1 else
                "RegisterAX" if is_scas else
                f"LEmuMemB({destination_segment}, RegisterDI)" if size == 1
                else f"LEmuMemW({destination_segment}, RegisterDI)"
            )
            body.extend([
                f"{left} := LongInt({source});",
                f"{right} := LongInt({destination});",
                f"{difference} := ({left} - {right}) and ${mask:x};",
                f"{carry} := {left} < {right};",
                f"{overflow} := (({left} xor {right}) and "
                f"({left} xor {difference}) and ${sign_bit:x}) <> 0;",
                f"RegisterCarryFlag := {carry};",
                f"RegisterZeroFlag := ({difference} and ${mask:x}) = 0;",
                f"RegisterSignFlag := (({difference}) and ${sign_bit:x}) <> 0;",
                f"RegisterOverflowFlag := {overflow};",
                f"{parity} := True;",
                f"{parity_byte} := {difference} and $ff;",
            ])
            for bit_index in range(8):
                body.append(
                    f"if (({parity_byte} shr {bit_index}) and 1) <> 0 "
                    f"then {parity} := not {parity};"
                )
            body.append(f"RegisterParityFlag := {parity};")
        elif is_store:
            for word_index in range(value_words):
                offset = word_index * 2
                value = (
                    f"(RegisterAX and $ff)" if size == 1
                    else f"((RegisterAX shr {offset * 8}) and $ffff)"
                )
                if size == 1:
                    body.append(
                        f"LEmuSetB({destination_segment}, RegisterDI, {value});"
                    )
                else:
                    body.append(
                        f"LEmuSetW({destination_segment}, "
                        f"(LongInt(RegisterDI) + {offset}) and $ffff, {value});"
                    )
        elif is_move:
            if size == 1:
                body.append(
                    f"LEmuSetB({destination_segment}, RegisterDI, "
                    f"LEmuMemB({source_segment}, RegisterSI));"
                )
            else:
                for word_index in range(value_words):
                    offset = word_index * 2
                    body.append(
                        f"LEmuSetW({destination_segment}, "
                        f"(LongInt(RegisterDI) + {offset}) and $ffff, "
                        f"LEmuMemW({source_segment}, "
                        f"(LongInt(RegisterSI) + {offset}) and $ffff));"
                    )
        else:
            if size == 1:
                body.append(f"RegisterAX := (RegisterAX and $ff00) or LEmuMemB({source_segment}, RegisterSI);")
            else:
                body.append(f"RegisterAX := LEmuMemW({source_segment}, RegisterSI);")
        if is_move or base.startswith("LODS") or base.startswith("CMPS"):
            body.append(
                f"RegisterSI := (LongInt(RegisterSI) + emuStep * {size}) and $ffff;"
            )
        if is_move or is_store or is_compare:
            body.append(
                f"RegisterDI := (LongInt(RegisterDI) + emuStep * {size}) and $ffff;"
            )
        self.lines.append(prefix)
        self.lines.extend("    " + line for line in body)
        self.lines.append(suffix_text)

    def _branch_condition(self, operation: str) -> str | None:
        if operation in {"JMP", "JMPF"}:
            return None
        condition = _BRANCH_CONDITIONS.get(operation)
        if condition is None:
            raise Unsupported(f"unsupported branch: {operation}")
        return condition

    def _execution_order(self) -> list[int]:
        order: list[int] = []
        covered: set[int] = set()

        def walk(start: int, end: int) -> None:
            index = start
            while index <= end:
                if index not in covered:
                    order.append(index)
                    covered.add(index)
                if index in self.inlined_calls:
                    destination = self.inlined_calls[index]
                    return_index = self.call_return_indices[index]
                    walk(destination, return_index)
                index += 1

        walk(0, len(self.instructions) - 1)
        return order

    def translate(self) -> str:
        for index in self._execution_order():
            instruction = self.instructions[index]
            if index in self.labels:
                self.lines.append(f"emuL{index}:")
            operation, _, operand_text = instruction.partition(" ")
            operation = operation.upper().strip()
            operand_text = operand_text.strip()
            if index in self.inlined_calls:
                frame_words = 4 if operation.startswith("CALLF") else 2
                self.lines.append(
                    f"RegisterSP := (RegisterSP - {frame_words}) and $ffff;"
                )
                continue
            if UNSUPPORTED.match(operation):
                raise Unsupported(f"unsupported operation: {operation}")
            if asmcfg.is_branch(instruction):
                if index in self.external_branches:
                    condition = self._branch_condition(operation)
                    if condition is None:
                        self.lines.append("goto emuExit;")
                    else:
                        self.lines.append(f"if {condition} then goto emuExit;")
                    continue
                destination = self.branch_targets.get(index)
                if destination is None:
                    raise Unsupported(f"unsupported branch: {operation}")
                self.labels.add(destination)
                condition = self._branch_condition(operation)
                if condition is None:
                    self.lines.append(f"goto emuL{destination};")
                else:
                    self.lines.append(f"if {condition} then goto emuL{destination};")
                continue
            if self.rules:
                try:
                    rewritten = capability_dsl.rewrite(
                        self.rules, instruction, self.evidence
                    )
                except (OSError, ValueError) as exc:
                    raise Unsupported(
                        f"capability rule failed: {exc}"
                    ) from exc
                if rewritten is not None:
                    instruction = rewritten
                    operation, _, operand_text = instruction.partition(" ")
                    operation = operation.upper().strip()
                    operand_text = operand_text.strip()
                else:
                    try:
                        rendered = capability_dsl.apply(
                            self.rules, instruction, self.evidence
                        )
                    except (OSError, ValueError) as exc:
                        raise Unsupported(
                            f"capability rule failed: {exc}"
                        ) from exc
                    if rendered is not None:
                        self.lines.extend(rendered)
                        continue
            operands = _split_operands(operand_text) if operand_text else []
            if operation == "CLD":
                self.lines.append("RegisterDirectionFlag := False;")
            elif operation == "STD":
                self.lines.append("RegisterDirectionFlag := True;")
            elif operation == "MOV":
                operands = self._raw_segment_move(index, operation) or operands
                if len(operands) != 2:
                    raise Unsupported("unsupported MOV operands")
                size = self._operand_size(operands[0])
                self.lines.append(
                    self._write(operands[0], self._read(operands[1], size), size)
                )
            elif operation in {"ADD", "ADC", "SUB", "SBB", "AND", "OR", "XOR", "CMP"}:
                self._emit_binary(operation, operands)
            elif operation == "TEST":
                self._emit_test(operands)
            elif operation in {"SHL", "SHR"}:
                self._emit_shift(operation, operands)
            elif operation in {"RCL", "RCR"}:
                self._emit_rotate(operation, operands)
            elif operation in {"INC", "DEC"} and len(operands) == 1:
                self._emit_incdec(operation, operands[0])
            elif operation in {"NEG", "NOT"} and len(operands) == 1:
                self._emit_neg_not(operation, operands[0])
            elif operation in {"CWD", "CBW"} and not operands:
                self._emit_sign_extend(operation)
            elif operation == "CLC" and not operands:
                self.lines.append("RegisterCarryFlag := False;")
            elif operation == "STC" and not operands:
                self.lines.append("RegisterCarryFlag := True;")
            elif operation == "CMC" and not operands:
                self.lines.append("RegisterCarryFlag := not RegisterCarryFlag;")
            elif operation == "ENTER" and len(operands) == 2:
                frame_size = _number(operands[0])
                nesting = _number(operands[1])
                if frame_size is None or nesting != 0 or frame_size > 0xffff:
                    raise Unsupported(f"unsupported ENTER operands: {operand_text}")
                self.lines.append("LEmuPush(RegisterBP);")
                self.lines.append("RegisterBP := RegisterSP;")
                self.lines.append(
                    f"RegisterSP := (RegisterSP - {frame_size}) and $ffff;"
                )
            elif operation == "MUL":
                self._emit_mul(operands)
            elif operation == "DIV":
                self._emit_div(operands)
            elif operation == "IMUL":
                self._emit_imul(operands)
            elif operation in {"AAM", "AAD"}:
                self._emit_decimal_adjust(operation, operands)
            elif operation == "XCHG" and len(operands) == 2:
                size = self._operand_size(operands[0])
                temp = self._next_temp()
                self.lines.append(f"{temp} := {self._read(operands[0], size)};")
                self.lines.append(
                    self._write(operands[0], self._read(operands[1], size), size)
                )
                self.lines.append(self._write(operands[1], temp, size))
            elif operation in {"LEA", "LES", "LDS"} and len(operands) == 2:
                clean = self._clean(operands[1])
                match = re.fullmatch(r"(?:([A-Z]{2}):)?\[(.*)\]", clean)
                if match is None:
                    raise Unsupported(f"unsupported {operation} memory operand")
                prefix, expression = match.groups()
                segment = prefix or ("SS" if "BP" in expression else "DS")
                offset = _offset_expression(expression)
                if operation == "LEA":
                    self.lines.append(self._register_assignment(
                        self._clean(operands[0]), offset))
                    continue
                self.lines.append(self._register_assignment(
                    self._clean(operands[0]), f"LEmuMemW(Register{segment}, {offset})"))
                self.lines.append(self._register_assignment(
                    "ES" if operation == "LES" else "DS",
                    f"LEmuMemW(Register{segment}, ({offset} + 2) and $ffff)"))
            elif operation == "PUSH" and len(operands) == 1:
                size = self._operand_size(operands[0])
                self.lines.append(f"LEmuPush({self._read(operands[0], size)});")
            elif operation == "POP" and len(operands) == 1:
                size = self._operand_size(operands[0])
                self.lines.append(self._write(operands[0], "LEmuPop()", size))
            elif operation == "PUSHF" and not operands:
                if self.flags_hardware_word:
                    self.lines.append("LEmuPush(RegisterFlagsWord);")
                else:
                    flags = self._next_temp()
                    self.lines.extend([
                        f"{flags} := Word(Word(RegisterCarryFlag) or "
                        "(Word(RegisterZeroFlag) shl 6) or "
                        "(Word(RegisterSignFlag) shl 7) or "
                        "(Word(RegisterDirectionFlag) shl 10) or "
                        "(Word(RegisterOverflowFlag) shl 11));",
                        f"LEmuPush({flags});",
                    ])
            elif operation == "POPF" and not operands:
                flags = self._next_temp()
                if self.flags_hardware_word:
                    self.lines.extend([
                        f"{flags} := LEmuPop();",
                        f"LEmuSetFlagsWord(Word({flags}));",
                    ])
                else:
                    self.lines.extend([
                        f"{flags} := LEmuPop();",
                        f"RegisterCarryFlag := ({flags} and $1) <> 0;",
                        f"RegisterZeroFlag := ({flags} and $40) <> 0;",
                        f"RegisterSignFlag := ({flags} and $80) <> 0;",
                        f"RegisterDirectionFlag := ({flags} and $400) <> 0;",
                        f"RegisterOverflowFlag := ({flags} and $800) <> 0;",
                    ])
            elif operation == "LEAVE":
                self.lines.append("RegisterSP := RegisterBP;")
                self.lines.append("RegisterBP := LEmuPop();")
            elif operation in {"RET", "RETF"}:
                if index in self.call_return_adjustments:
                    self.lines.append(
                        "RegisterSP := (RegisterSP + "
                        f"{self.call_return_adjustments[index]}) and $ffff;"
                    )
                if self.kind == "function":
                    if self.return_type == "longint":
                        result = "(LongInt(RegisterDX) shl 16) + RegisterAX"
                    elif self.return_type in {"byte", "boolean"}:
                        result = "RegisterAX and $ff"
                    else:
                        result = "RegisterAX"
                    self.lines.append(f"{self.name} := {result};")
            elif operation.startswith(("MOVS", "STOS", "LODS", "CMPS", "SCAS")):
                self._emit_string(operation, operand_text)
            else:
                raise Unsupported(f"unsupported operation: {operation}")
        if self.external_branches:
            self.lines.append("emuExit:")
        if self.flags_hardware_word:
            self.lines = [self._flags_word_line(line) for line in self.lines]
        return self._source()

    def _flags_word_line(self, line: str) -> str:
        helpers = {
            "RegisterCarryFlag": "LEmuSetCarryFlag",
            "RegisterParityFlag": "LEmuSetParityFlag",
            "RegisterZeroFlag": "LEmuSetZeroFlag",
            "RegisterSignFlag": "LEmuSetSignFlag",
            "RegisterDirectionFlag": "LEmuSetDirectionFlag",
            "RegisterOverflowFlag": "LEmuSetOverflowFlag",
        }
        match = re.fullmatch(r"(\s*)(\w+)\s*:=\s*(.+);", line)
        if match is None:
            return line
        indent, name, expression = match.groups()
        helper = helpers.get(name)
        if helper is None:
            return line
        return f"{indent}{helper}({expression});"

    def _signed_frame_params(self) -> set[int]:
        result: set[int] = set()
        signed_branch = re.compile(r"^J(?:GE|LE|JL|JG)\b", re.I)
        cmp_instruction = re.compile(r"^CMP\b", re.I)
        frame_slot = re.compile(r"\bBP\s*\+\s*0X([0-9A-F]+)\b", re.I)
        for index, instruction in enumerate(self.instructions):
            if signed_branch.match(instruction.strip()) is None:
                continue
            for previous in reversed(self.instructions[:index]):
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

    def _returns_ax_value(self) -> bool:
        returns = [
            index
            for index, instruction in enumerate(self.instructions)
            if re.match(r"^RET(?:F)?\b", instruction.strip(), re.I)
        ]
        if len(returns) != 1:
            return False
        tail = self.instructions[max(0, returns[0] - 8):returns[0]]
        local_load = re.compile(
            r"^MOV\s+AX\s*,\s*(?:WORD PTR\s+)?\[\s*BP\s*"
            r"(?:[+-]\s*)?(?:[+-]\s*)?0X[0-9A-F]+\s*\]$",
            re.I,
        )
        return any(local_load.match(instruction.strip()) for instruction in tail)

    def _source(self) -> str:
        params = []
        param_names: list[str] = []
        if self.params_text and self.params_text.strip():
            for group in self.params_text.split(";"):
                names, type_name = (part.strip() for part in group.split(":", 1))
                for param in (part.strip() for part in names.split(",")):
                    params.append(f"{param}: {type_name.title()}")
                    param_names.append(param)
        declaration = (
            f"procedure {self.name}({'; '.join(params)});" if params
            else f"procedure {self.name};"
        )
        if self.kind == "function":
            declaration = declaration.replace("procedure ", "function ", 1)
            declaration = declaration.rstrip(";") + f": {self.return_type.title()};"
        helper_declarations = [
            "{$IFNDEF LEMU_RUNTIME_HELPERS}",
            "function LEmuMemB(segmentWord, offsetWord: Word): Byte; forward;",
            "function LEmuMemW(segmentWord, offsetWord: Word): Word; forward;",
            "procedure LEmuSetB(segmentWord, offsetWord: Word; value: Byte); forward;",
            "procedure LEmuSetW(segmentWord, offsetWord: Word; value: Word); forward;",
            "procedure LEmuPush(value: Word); forward;",
            "function LEmuPop: Word; forward;",
            "function LEmuSigned16(valueWord: Word): LongInt; forward;",
        ]
        if self.flags_hardware_word:
            helper_declarations.extend([
                "procedure LEmuSetFlagBit(maskValue: LongInt; flagValue: Boolean); forward;",
                "procedure LEmuSetCarryFlag(flagValue: Boolean); forward;",
                "procedure LEmuSetParityFlag(flagValue: Boolean); forward;",
                "procedure LEmuSetZeroFlag(flagValue: Boolean); forward;",
                "procedure LEmuSetSignFlag(flagValue: Boolean); forward;",
                "procedure LEmuSetDirectionFlag(flagValue: Boolean); forward;",
                "procedure LEmuSetOverflowFlag(flagValue: Boolean); forward;",
                "procedure LEmuSetResultFlags(valueWord: LongInt; carryValue, overflowValue: Boolean); forward;",
                "procedure LEmuSetFlagsWord(valueWord: Word); forward;",
            ])
        helper_declarations.append("{$ENDIF}")
        helpers = [
            "{$IFNDEF LEMU_RUNTIME_HELPERS}",
            "function LEmuMemB(segmentWord, offsetWord: Word): Byte;",
            "begin",
            "  LEmuMemB := RealModeMemory[((LongInt(segmentWord) shl 4) + offsetWord) and $fffff];",
            "end;",
            "function LEmuMemW(segmentWord, offsetWord: Word): Word;",
            "var address: LongInt;",
            "begin",
            "  address := ((LongInt(segmentWord) shl 4) + offsetWord) and $fffff;",
            "  LEmuMemW := RealModeMemory[address] or (RealModeMemory[address + 1] shl 8);",
            "end;",
            "procedure LEmuSetB(segmentWord, offsetWord: Word; value: Byte);",
            "begin",
            "  RealModeMemory[((LongInt(segmentWord) shl 4) + offsetWord) and $fffff] := value;",
            "end;",
            "procedure LEmuSetW(segmentWord, offsetWord: Word; value: Word);",
            "var address: LongInt;",
            "begin",
            "  address := ((LongInt(segmentWord) shl 4) + offsetWord) and $fffff;",
            "  RealModeMemory[address] := value and $ff;",
            "  RealModeMemory[address + 1] := (value shr 8) and $ff;",
            "end;",
            "procedure LEmuPush(value: Word);",
            "begin",
            "  RegisterSP := (RegisterSP - 2) and $ffff;",
            "  LEmuSetW(RegisterSS, RegisterSP, value);",
            "end;",
            "function LEmuPop: Word;",
            "begin",
            "  LEmuPop := LEmuMemW(RegisterSS, RegisterSP);",
            "  RegisterSP := (RegisterSP + 2) and $ffff;",
            "end;",
            "function LEmuSigned16(valueWord: Word): LongInt;",
            "var signedValue: LongInt;",
            "begin",
            "  signedValue := LongInt(valueWord);",
            "  if (valueWord and $8000) <> 0 then signedValue := signedValue - $10000;",
            "  LEmuSigned16 := signedValue;",
            "end;",
            "{$DEFINE LEMU_RUNTIME_HELPERS}",
            "{$ENDIF}",
        ]
        if self.flags_hardware_word:
            helpers.extend([
                "procedure LEmuSetFlagBit(maskValue: LongInt; flagValue: Boolean);",
                "begin",
                "  if flagValue then",
                "    RegisterFlagsWord := RegisterFlagsWord or Word(maskValue)",
                "  else",
                "    RegisterFlagsWord := RegisterFlagsWord and Word(maskValue xor $ffff);",
                "end;",
                "procedure LEmuSetCarryFlag(flagValue: Boolean);",
                "begin",
                "  RegisterCarryFlag := flagValue;",
                "  LEmuSetFlagBit($1, flagValue);",
                "end;",
                "procedure LEmuSetParityFlag(flagValue: Boolean);",
                "begin",
                "  RegisterParityFlag := flagValue;",
                "  LEmuSetFlagBit($4, flagValue);",
                "end;",
                "procedure LEmuSetZeroFlag(flagValue: Boolean);",
                "begin",
                "  RegisterZeroFlag := flagValue;",
                "  LEmuSetFlagBit($40, flagValue);",
                "end;",
                "procedure LEmuSetSignFlag(flagValue: Boolean);",
                "begin",
                "  RegisterSignFlag := flagValue;",
                "  LEmuSetFlagBit($80, flagValue);",
                "end;",
                "procedure LEmuSetDirectionFlag(flagValue: Boolean);",
                "begin",
                "  RegisterDirectionFlag := flagValue;",
                "  LEmuSetFlagBit($400, flagValue);",
                "end;",
                "procedure LEmuSetOverflowFlag(flagValue: Boolean);",
                "begin",
                "  RegisterOverflowFlag := flagValue;",
                "  LEmuSetFlagBit($800, flagValue);",
                "end;",
                "procedure LEmuSetResultFlags(valueWord: LongInt; carryValue, overflowValue: Boolean);",
                "var bitIndex: LongInt; parityValue: Boolean;",
                "begin",
                "  RegisterFlagsWord := (RegisterFlagsWord or $2) and $ffc7;",
                "  LEmuSetCarryFlag(carryValue);",
                "  LEmuSetZeroFlag((valueWord and $ffff) = 0);",
                "  LEmuSetSignFlag((valueWord and $8000) <> 0);",
                "  LEmuSetOverflowFlag(overflowValue);",
                "  parityValue := True;",
                "  for bitIndex := 0 to 7 do",
                "    if ((valueWord shr bitIndex) and 1) <> 0 then parityValue := not parityValue;",
                "  LEmuSetParityFlag(parityValue);",
                "end;",
                "procedure LEmuSetFlagsWord(valueWord: Word);",
                "begin",
                "  RegisterFlagsWord := ((valueWord and $0fff) or $7002) and $ffd7;",
                "  RegisterCarryFlag := (valueWord and $1) <> 0;",
                "  RegisterParityFlag := (valueWord and $4) <> 0;",
                "  RegisterZeroFlag := (valueWord and $40) <> 0;",
                "  RegisterSignFlag := (valueWord and $80) <> 0;",
                "  RegisterDirectionFlag := (valueWord and $400) <> 0;",
                "  RegisterOverflowFlag := (valueWord and $800) <> 0;",
                "end;",
            ])
        target_forward = [
            "{$IFNDEF LEMU_GENERATED_FORWARDS}",
            declaration.rstrip(";") + "; forward;",
            "{$ENDIF}",
        ]
        label_names = [f"emuL{index}" for index in sorted(self.labels)]
        if self.external_branches:
            label_names.append("emuExit")
        label_line = "label " + ", ".join(label_names) + ";" if label_names else ""
        global_state = (
            ["var", *[f"  {name}: LongInt;" for name in self.state_variables]]
            if self.state_variables
            else []
        )
        lines = [
            *global_state,
            *target_forward,
            *helper_declarations,
            declaration,
            *([label_line] if label_line else []),
            "var emuStep: LongInt;",
            *[
                f"    {name}: {kind};"
                for name, kind in (*self.extra_variables, *self.temps)
            ],
            "begin",
        ]
        entry_registers = ("RegisterAX", "RegisterBX", "RegisterCX", "RegisterDX",
                           "RegisterSI", "RegisterDI")
        for index, param in enumerate(param_names):
            if index < len(entry_registers):
                lines.append(f"  {entry_registers[index]} := Word({param});")
        for index, param in enumerate(param_names):
            offset = self.entry_frame_bytes + index * 2
            lines.append(
                f"  LEmuSetW(RegisterSS, ((RegisterSP + {offset}) and $ffff), "
                f"Word({param}));"
            )
        lines.extend("  " + line for line in self.lines)
        lines.append("end;")
        lines.extend(helpers)
        return "\n".join(lines) + "\n"


def translate(evidence: dict[str, Any]) -> str:
    return _Translator(evidence).translate()


def supported(evidence: dict[str, Any]) -> bool:
    try:
        return bool(translate(evidence))
    except Unsupported:
        return False
