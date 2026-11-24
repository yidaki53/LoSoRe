"""Deterministic search for executable capability proposals."""

from __future__ import annotations

import hashlib
import pathlib
import re
from typing import Any

from engine import capability_registry, contract_oracle
from tools import asmcfg

RULE_ID = "code-memory-and-dos-state"
REG16 = r"(?:AX|BX|CX|DX|SI|DI|BP|SP)"
REG8 = r"(?:AL|AH|BL|BH|CL|CH|DL|DH)"
SEGMENT_BODY = r"CS|[0-9A-F]{1,4}"
ADDRESS = r"[0-9A-F]{1,8}"
BINARY_OPS = r"ADD|ADC|SUB|SBB|AND|OR|XOR|CMP|TEST"
UNARY_OPS = r"MUL|DIV|IMUL"


def _code_memory() -> str:
    return rf"(?P<segment>{SEGMENT_BODY}):\[0X(?P<address>{ADDRESS})\]"


FAMILIES: list[dict[str, Any]] = [
    {
        "id": "rewrite-mov-word",
        "kind": "rewrite",
        "match": rf"^MOV\s+(?P<dest>{REG16}),\s*WORD PTR\s+{_code_memory()}$",
        "template": "MOV {dest},WORD PTR {value}",
        "source": "code_memory",
        "segment": "segment",
        "address": "address",
    },
    {
        "id": "rewrite-mov-byte",
        "kind": "rewrite",
        "match": rf"^MOV\s+(?P<dest>{REG8}),\s*BYTE PTR\s+{_code_memory()}$",
        "template": "MOV {dest},BYTE PTR {value}",
        "source": "code_memory",
        "segment": "segment",
        "address": "address",
    },
    {
        "id": "rewrite-unary-word",
        "kind": "rewrite",
        "match": rf"^(?P<op>{UNARY_OPS})\s+WORD PTR\s+{_code_memory()}$",
        "template": "{op} WORD PTR {value}",
        "source": "code_memory",
        "segment": "segment",
        "address": "address",
    },
    {
        "id": "rewrite-unary-byte",
        "kind": "rewrite",
        "match": rf"^(?P<op>{UNARY_OPS})\s+BYTE PTR\s+{_code_memory()}$",
        "template": "{op} BYTE PTR {value}",
        "source": "code_memory",
        "segment": "segment",
        "address": "address",
    },
    {
        "id": "rewrite-binary-word",
        "kind": "rewrite",
        "match": rf"^(?P<op>{BINARY_OPS})\s+(?P<lhs>[^,]+),\s*WORD PTR\s+{_code_memory()}$",
        "template": "{op} {lhs},WORD PTR {value}",
        "source": "code_memory",
        "segment": "segment",
        "address": "address",
    },
    {
        "id": "rewrite-binary-byte",
        "kind": "rewrite",
        "match": rf"^(?P<op>{BINARY_OPS})\s+(?P<lhs>[^,]+),\s*BYTE PTR\s+{_code_memory()}$",
        "template": "{op} {lhs},BYTE PTR {value}",
        "source": "code_memory",
        "segment": "segment",
        "address": "address",
    },
    {
        "id": "flags-adc-zero",
        "kind": "flags_adc_zero",
        "match": rf"^ADC\s+(?P<target>{REG16}),\s*0X0$",
        "target": "target",
    },
]
PATTERNS = [(family, re.compile(family["match"], re.I)) for family in FAMILIES]
MEMORY_READ = re.compile(
    rf"^MOV\s+(?P<target>{REG16}),\s*(?:WORD PTR\s+)?\[0X(?P<address>{ADDRESS})\]$",
    re.I,
)
MEMORY_WRITE = re.compile(
    rf"^MOV\s+(?:WORD PTR\s+)?\[0X(?P<address>{ADDRESS})\],\s*(?P<target>{REG16})$",
    re.I,
)


def _memory_rules(instructions: list[str]) -> list[dict[str, Any]]:
    read_addresses: list[str] = []
    write_addresses: list[str] = []
    for item in instructions:
        read = MEMORY_READ.fullmatch(item)
        if read is not None:
            address = read.group("address").upper()
            if address not in read_addresses:
                read_addresses.append(address)
            continue
        write = MEMORY_WRITE.fullmatch(item)
        if write is not None:
            address = write.group("address").upper()
            if address not in write_addresses:
                write_addresses.append(address)
    addresses = list(dict.fromkeys([*read_addresses, *write_addresses]))
    variables = {
        address: f"emuAbsState{index}" for index, address in enumerate(addresses)
    }
    rules: list[dict[str, Any]] = []
    for address in read_addresses:
        rules.append({
            "id": f"memory-read-absolute-{address}",
            "kind": "memory_read",
            "match": rf"^MOV\s+(?P<target>{REG16}),\s*(?:WORD PTR\s+)?\[0X(?P<address>{address})\]$",
            "target": "target",
            "address": "address",
            "variable": variables[address],
        })
    for address in write_addresses:
        rules.append({
            "id": f"memory-write-absolute-{address}",
            "kind": "memory_write",
            "match": rf"^MOV\s+(?:WORD PTR\s+)?\[0X(?P<address>{address})\],\s*(?P<target>{REG16})$",
            "target": "target",
            "address": "address",
            "variable": variables[address],
        })
    return rules


def _external_exit_rule(evidence: dict[str, Any]) -> dict[str, Any] | None:
    declaration = str(
        evidence.get("oracle_contract", {}).get("declaration", "")
    ).lower()
    if not declaration.startswith("procedure"):
        return None
    assembly = evidence.get("static_evidence", {}).get("assembly", {})
    addresses = [int(item) for item in assembly.get("addresses", [])]
    segments = [int(item) for item in assembly.get("segments", [])]
    instructions = [str(item).upper() for item in assembly.get("instructions", [])]
    if not addresses or len(addresses) != len(segments) != len(instructions):
        return None
    known = set(addresses)
    targets: set[int] = set()
    for instruction, segment in zip(instructions, segments):
        if not asmcfg.is_branch(instruction):
            continue
        target = asmcfg.resolve_branch_target(instruction, segment)
        if target is not None and target not in known:
            targets.add(target)
    if len(targets) != 1:
        return None
    return {
        "id": "external-exit",
        "kind": "external_exit",
        "match": r"^J[A-Z]+(?:\s+[A-Z]+)?\s+[0-9A-F]{1,4}:[0-9A-F]{1,4}$",
    }


def _hardware_flags_rule(
    root: pathlib.Path | None,
    evidence: dict[str, Any],
    instructions: list[str],
) -> dict[str, Any] | None:
    if root is None or not any(item in {"PUSHF", "POPF"} for item in instructions):
        return None
    target = str(evidence.get("target", ""))
    routine = str(evidence.get("routine", ""))
    if not target or not routine:
        return None
    try:
        fixture = contract_oracle.fixture(root, target, routine)
    except (OSError, ValueError, KeyError):
        return None
    if fixture.get("bytes_sha256") != evidence.get("bytes", {}).get("sha256"):
        return None
    return {
        "id": "hardware-flags-word",
        "kind": "flags_hardware_word",
        "match": r"^PUSHF$",
    }


def _rules(matched: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {key: value for key, value in family.items() if key != "pattern"}
        for family in matched
    ]


def _capability_id(rules: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256(
        "\n".join(f"{rule['id']}:{rule['match']}" for rule in rules).encode()
    ).hexdigest()[:12]
    return f"rule-{RULE_ID}-{digest}"


def propose_for_evidence(
    root: pathlib.Path | None,
    evidence: dict[str, Any],
    include_hardware: bool = True,
) -> list[tuple[str, dict[str, Any]]]:
    instructions = [
        str(item).upper()
        for item in evidence.get("static_evidence", {})
        .get("assembly", {})
        .get("instructions", [])
    ]
    if not instructions:
        return []
    matched: dict[str, dict[str, Any]] = {}
    for item in instructions:
        for family, pattern in PATTERNS:
            if pattern.fullmatch(item) is not None:
                matched[family["id"]] = family
    for rule in _memory_rules(instructions):
        matched[rule["id"]] = rule
    external_rule = _external_exit_rule(evidence)
    if external_rule is not None:
        matched[external_rule["id"]] = external_rule
    if include_hardware:
        flags_rule = _hardware_flags_rule(root, evidence, instructions)
        if flags_rule is not None:
            matched[flags_rule["id"]] = flags_rule
    if not matched:
        return []
    selected = [matched[key] for key in sorted(matched)]
    rules = _rules(selected)
    capability_id = _capability_id(rules)
    existing = capability_registry.load(root).get("capabilities", {}).get(capability_id, {})
    if existing.get("rules"):
        return [(capability_id, dict(rule)) for rule in existing["rules"]]
    capability_registry.add_rule_capability(
        root, capability_id, rules, evidence, source="rule-proposal"
    )
    return [(capability_id, dict(rule)) for rule in rules]
