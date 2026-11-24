"""Persistent capability registry for evidence-driven recovery."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
from typing import Any

from tools import asmcfg

SCHEMA_VERSION = 1
STORE = pathlib.Path("knowledge/capabilities.json")
MIN_GENERALIZATION_ROUTINES = 2

_BUILTIN: dict[str, dict[str, Any]] = {
    "bounded-internal-branches": {
        "renderer": "asm-emulation-v1",
        "features_any": ["control:branch-internal"],
        "features_none": ["control:branch-external", "control:call"],
    },
    "bp-index-address-normalization": {
        "renderer": "asm-emulation-v1",
        "features_any": ["mem:bp-index"],
        "features_none": ["control:call"],
    },
    "absolute-bp-load-projection": {
        "renderer": "asm-emulation-v1",
        "features_any": ["mem:absolute-bp-load"],
        "features_none": ["control:call"],
    },
    "wide-unsigned-multiply": {
        "renderer": "asm-emulation-v1",
        "features_any": ["op:MUL", "width:16"],
        "features_none": ["control:call"],
    },
    "arena-mapped-memory": {
        "renderer": "asm-emulation-v1",
        "features_any": ["mem:bracket"],
        "features_none": ["control:call"],
    },
}


def _instructions(evidence: dict[str, Any]) -> list[str]:
    return [
        str(item).upper()
        for item in evidence.get("static_evidence", {})
        .get("assembly", {})
        .get("instructions", [])
    ]


def _operation(instruction: str) -> str:
    return instruction.split(maxsplit=1)[0].upper() if instruction.strip() else ""


def signature(evidence: dict[str, Any]) -> dict[str, Any]:
    assembly = evidence.get("static_evidence", {}).get("assembly", {})
    instructions = _instructions(evidence)
    operations = sorted({_operation(item) for item in instructions if _operation(item)})
    features: set[str] = {f"op:{item}" for item in operations}
    parsed = {
        "insts": instructions,
        "addrs": list(assembly.get("addresses", range(len(instructions)))),
        "segments": list(assembly.get("segments", [0] * len(instructions))),
    }
    bounded = asmcfg.bounded_branch_paths(parsed)
    has_branch = any(asmcfg.is_branch(item) for item in instructions)
    if has_branch:
        features.add(
            "control:branch-internal" if bounded else "control:branch-external"
        )
    if any(asmcfg.is_call(item) for item in instructions):
        features.add("control:call")
    if any(_operation(item) in {"RETF", "IRET"} for item in instructions):
        features.add("control:far-return")
    for instruction in instructions:
        for expression in re.findall(r"\[([^\]]+)\]", instruction):
            features.add("mem:bracket")
            upper = expression.upper().replace(" ", "")
            if "BP" in upper and ("SI" in upper or "DI" in upper):
                features.add("mem:bp-index")
            if "0X" in upper or upper.lstrip("+-").isdigit():
                features.add("mem:absolute")
            if "BP" in upper and "0X" not in upper:
                features.add("mem:stack-frame")
        if re.fullmatch(
            r"MOV\s+BP\s*,\s*(?:WORD PTR\s+)?(?:DS\s*:\s*)?\[\s*0X[0-9A-F]+\s*\]",
            instruction,
            flags=re.I,
        ):
            features.add("mem:absolute-bp-load")
        if _operation(instruction) in {"MUL", "DIV"} and "WORD PTR" in instruction:
            features.add("width:16")
        if _operation(instruction) in {"AAM", "AAD"}:
            features.add("arithmetic:decimal-adjust")
    tokens = sorted(features)
    return {
        "operations": operations,
        "features": sorted(item for item in features if item not in {
            f"op:{name}" for name in operations
        }),
        "tokens": tokens,
        "hash": hashlib.sha256("\n".join(tokens).encode()).hexdigest(),
    }


def _empty() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "capabilities": {},
        "gaps": {},
    }


def load(root: pathlib.Path | None = None) -> dict[str, Any]:
    path = (pathlib.Path(root) / STORE) if root is not None else STORE
    if not path.is_file():
        return _empty()
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return _empty()
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        return _empty()
    data.setdefault("capabilities", {})
    data.setdefault("gaps", {})
    return data


def save(data: dict[str, Any], root: pathlib.Path | None = None) -> None:
    path = (pathlib.Path(root) / STORE) if root is not None else STORE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def _capability_entry(capability_id: str) -> dict[str, Any]:
    builtin = _BUILTIN.get(capability_id)
    if builtin is not None:
        return dict(builtin)
    return {"renderer": "", "features_any": [], "features_none": []}


def _feature_match(entry: dict[str, Any], tokens: set[str]) -> bool:
    any_of = set(entry.get("features_any", []))
    none_of = set(entry.get("features_none", []))
    return bool(any_of & tokens) and not (none_of & tokens)


def signature_overlap(entry: dict[str, Any], sig: dict[str, Any]) -> float:
    tokens = set(sig.get("tokens", []))
    best = 0.0
    for learned in entry.get("signatures", []):
        learned_tokens = set(learned.get("tokens", []))
        if not learned_tokens or not tokens:
            continue
        best = max(best, len(learned_tokens & tokens) / len(learned_tokens | tokens))
    return best


def _signature_match(entry: dict[str, Any], tokens: set[str]) -> bool:
    probe = {"tokens": sorted(tokens)}
    return signature_overlap(entry, probe) >= 0.6


def detect(evidence: dict[str, Any]) -> list[str]:
    tokens = set(signature(evidence)["tokens"])
    return sorted(
        capability_id
        for capability_id, entry in _BUILTIN.items()
        if _feature_match(entry, tokens)
    )


def select(root: pathlib.Path | None, evidence: dict[str, Any]) -> list[str]:
    data = load(root)
    sig = signature(evidence)
    tokens = set(sig["tokens"])
    selected = set(detect(evidence))
    for capability_id, entry in data.get("capabilities", {}).items():
        usable = entry.get("status") == "verified" or (
            entry.get("status") == "candidate" and entry.get("renderer")
        )
        if usable and _signature_match(entry, tokens):
            selected.add(capability_id)
    return sorted(selected)


def observe_unsupported(
    root: pathlib.Path | None,
    target: str,
    routine: str,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    data = load(root)
    sig = signature(evidence)
    gap = data["gaps"].setdefault(sig["hash"], {
        "signature": sig,
        "count": 0,
        "examples": [],
    })
    gap["count"] += 1
    example = {"target": target, "routine": routine}
    if example not in gap["examples"]:
        gap["examples"].append(example)
        gap["examples"] = gap["examples"][-32:]
    save(data, root)
    return {"hash": sig["hash"], "count": gap["count"]}


def add_rule_capability(
    root: pathlib.Path | None,
    capability_id: str,
    rules: list[dict[str, Any]],
    evidence: dict[str, Any],
    source: str = "rule-proposal",
) -> str:
    data = load(root)
    entry = data["capabilities"].setdefault(capability_id, _capability_entry(capability_id))
    sig = signature(evidence)
    entry.update({
        "status": "candidate",
        "source": source,
        "renderer": "asm-emulation-v1",
        "rules": rules,
        "outcomes": entry.get("outcomes", {}),
    })
    signatures = entry.setdefault("signatures", [])
    if not any(item.get("hash") == sig["hash"] for item in signatures):
        signatures.append(sig)
    save(data, root)
    return capability_id


def record_outcome(
    root: pathlib.Path | None,
    target: str,
    routine: str,
    capability_ids: list[str],
    outcome: str,
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = load(root)
    sig = signature(evidence) if evidence is not None else None
    for capability_id in capability_ids:
        entry = data["capabilities"].setdefault(capability_id, _capability_entry(capability_id))
        outcomes = entry.setdefault("outcomes", {})
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        entry.setdefault("provenance", []).append({
            "target": target,
            "routine": routine,
            "outcome": outcome,
        })
        entry["provenance"] = entry["provenance"][-64:]
        if outcome == "verified" and sig is not None:
            signatures = entry.setdefault("signatures", [])
            if not any(item.get("hash") == sig["hash"] for item in signatures):
                signatures.append(sig)
            entry["renderer"] = entry.get("renderer") or "asm-emulation-v1"
            if entry.get("source") in {"rule-proposal", "gap-generalization"}:
                verified_routines = {
                    (item.get("target"), item.get("routine"))
                    for item in entry.get("provenance", [])
                    if item.get("outcome") == "verified"
                }
                generalized = len(verified_routines) >= MIN_GENERALIZATION_ROUTINES
                entry["status"] = "verified" if generalized else "candidate"
                entry["generalized"] = generalized
            else:
                entry["status"] = "verified"
    save(data, root)
    return {
        "capabilities": list(capability_ids),
        "outcome": outcome,
        "signature": sig["hash"] if sig is not None else None,
    }
