"""Safe executable rule DSL for learned recovery capabilities."""

from __future__ import annotations

import re
from typing import Any

REG16 = {"AX", "BX", "CX", "DX", "SI", "DI", "BP", "SP"}
REG8 = {"AL", "AH", "BL", "BH", "CL", "CH", "DL", "DH"}
SOURCES = {"code_memory"}
KINDS = {
    "rewrite",
    "memory_read",
    "memory_write",
    "flags_adc_zero",
    "external_exit",
    "flags_hardware_word",
}
EXTRA_VARIABLES = {
    "flags_adc_zero": [
        ("emuAdcZeroCarry", "Boolean"),
        ("emuAdcZeroResult", "LongInt"),
    ],
    "flags_hardware_word": [("emuHardwareFlags", "LongInt")],
}
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_PLACEHOLDER = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
_TEMPLATE_CHARS = re.compile(r"^[A-Za-z0-9_ {},:\[\]+*/()$\-]+$")


def validate_rule(rule: dict[str, Any]) -> None:
    kind = rule.get("kind")
    if kind not in KINDS:
        raise ValueError("unsupported capability rule kind")
    if not isinstance(rule.get("match"), str):
        raise ValueError("capability rule match must be a string")
    try:
        re.compile(rule["match"], re.I)
    except re.error as exc:
        raise ValueError("invalid capability rule match") from exc
    if kind not in {"rewrite", "external_exit", "flags_hardware_word"} and not _IDENTIFIER.fullmatch(
        str(rule.get("target", ""))
    ):
        raise ValueError("capability rule target must be a named group")
    if kind == "rewrite":
        template = str(rule.get("template", ""))
        if not _TEMPLATE_CHARS.fullmatch(template):
            raise ValueError("unsafe capability rule template")
        groups = set(re.compile(rule["match"], re.I).groupindex)
        if any(
            name != "value" and name not in groups
            for name in _PLACEHOLDER.findall(template)
        ):
            raise ValueError("unknown capability rule template group")
    source = str(rule.get("source", ""))
    source_optional = (
        kind.startswith("memory")
        or kind in {"flags_adc_zero", "external_exit", "flags_hardware_word"}
    )
    if source:
        if source_optional or source not in SOURCES:
            raise ValueError("unsupported capability rule source")
    elif not source_optional:
        raise ValueError("unsupported capability rule source")
    if kind.startswith("memory") and not _IDENTIFIER.fullmatch(
        str(rule.get("variable", ""))
    ):
        raise ValueError("memory capability state variable must be an identifier")
    required: list[str] = []
    if source in SOURCES or kind.startswith("memory"):
        required.append("address")
    if source in SOURCES:
        required.append("segment")
    for key in required:
        value = str(rule.get(key, ""))
        if not _IDENTIFIER.fullmatch(value) and not re.fullmatch(r"\d+", value):
            raise ValueError(f"invalid capability rule {key} group")


def compile_rules(rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compiled = []
    for rule in rules:
        validate_rule(rule)
        compiled.append({**rule, "regex": re.compile(rule["match"], re.I)})
    return compiled


def variables(rules: list[dict[str, Any]]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for rule in rules:
        variables_for_rule = list(EXTRA_VARIABLES.get(str(rule.get("kind")), []))
        variable = str(rule.get("variable", ""))
        if variable:
            variables_for_rule.append((variable, "LongInt"))
        for item in variables_for_rule:
            if item not in result:
                result.append(item)
    return result


def state_variables(rules: list[dict[str, Any]]) -> list[str]:
    result: list[str] = []
    for rule in rules:
        if not str(rule.get("kind", "")).startswith("memory"):
            continue
        variable = str(rule.get("variable", ""))
        if variable and variable not in result:
            result.append(variable)
        mirror = f"{variable}Mirror" if variable else ""
        if mirror and mirror not in result:
            result.append(mirror)
    return result


def _group(match: re.Match[str], name: str) -> str:
    try:
        value = match.group(name)
    except IndexError as exc:
        raise ValueError(f"missing capability rule group: {name}") from exc
    if value is None:
        raise ValueError(f"missing capability rule group: {name}")
    return value.upper()


def _absolute_offset(match: re.Match[str], rule: dict[str, Any], evidence: dict[str, Any]) -> int:
    address_text = _group(match, str(rule["address"]))
    if not re.fullmatch(r"[0-9A-F]{1,8}", address_text):
        raise ValueError("invalid absolute address in capability rule")
    address = int(address_text, 16)
    if evidence.get("absolute_memory"):
        return address & 0xFFFF
    return address & 0xFFFF


def apply(
    rules: list[dict[str, Any]],
    instruction: str,
    evidence: dict[str, Any],
) -> list[str] | None:
    upper = instruction.upper()
    for rule in rules:
        if rule["kind"] in {"rewrite", "external_exit", "flags_hardware_word"}:
            continue
        match = rule["regex"].fullmatch(upper)
        if match is None:
            continue
        target = _group(match, str(rule["target"]))
        if rule["kind"] == "flags_adc_zero":
            register = f"Register{target}"
            if target not in REG16:
                raise ValueError("flag capability target is not a 16-bit register")
            return [
                f"emuAdcZeroCarry := LongInt({register}) + "
                "LongInt(RegisterCarryFlag) > $ffff;",
                f"emuAdcZeroResult := (LongInt({register}) + "
                "LongInt(RegisterCarryFlag)) and $ffff;",
                f"{register} := emuAdcZeroResult;",
                "RegisterCarryFlag := emuAdcZeroCarry;",
                "RegisterSignFlag := ((emuAdcZeroResult) and $8000) <> 0;",
                "RegisterOverflowFlag := False;",
            ]
        if target not in REG16:
            raise ValueError("memory capability target is not a 16-bit register")
        offset = _absolute_offset(match, rule, evidence)
        variable = str(rule.get("variable", ""))
        if rule["kind"] == "memory_read":
            if evidence.get("absolute_memory"):
                return [f"Register{target} := LEmuMemW(RegisterDS, ${offset:04x});"]
            address = int(_group(match, str(rule["address"])), 16)
            mirror = f"{variable}Mirror"
            word = (
                f"(Word(DosMemory[${address:04x}]) or "
                f"(Word(DosMemory[${address + 1:04x}]) shl 8))"
            )
            return [
                f"if {word} <> {mirror} then begin",
                f"  {variable} := {word};",
                f"  {mirror} := {word};",
                "end;",
                f"Register{target} := {variable};",
            ]
        if rule["kind"] == "memory_write":
            if evidence.get("absolute_memory"):
                return [f"LEmuSetW(RegisterDS, ${offset:04x}, Register{target});"]
            address = int(_group(match, str(rule["address"])), 16)
            mirror = f"{variable}Mirror"
            return [
                f"{variable} := Register{target};",
                f"{mirror} := Register{target};",
                f"DosMemory[${address:04x}] := Byte(Register{target});",
                f"DosMemory[${address + 1:04x}] := Byte((Register{target} shr 8) and $ff);",
            ]
    return None


def rewrite(
    rules: list[dict[str, Any]],
    instruction: str,
    evidence: dict[str, Any],
) -> str | None:
    upper = instruction.upper()
    for rule in rules:
        if rule["kind"] != "rewrite":
            continue
        match = rule["regex"].fullmatch(upper)
        if match is None:
            continue
        address = int(_group(match, str(rule["address"])), 16)
        rendered_value = f"CodeMemory[0X{address:04X}]"
        replacements = {
            name: match.group(name)
            for name in match.re.groupindex
            if name not in {rule["segment"], rule["address"]}
        }
        replacements["value"] = rendered_value
        try:
            return _PLACEHOLDER.sub(
                lambda item: replacements[item.group(1)], str(rule["template"])
            )
        except KeyError as exc:
            raise ValueError(f"missing capability rule template group: {exc}") from exc
    return None
