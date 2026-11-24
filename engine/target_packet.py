"""Binary-only evidence packets for target-agnostic recovery experiments."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re

from engine import instruction_facts, knowledge, matrix, routine_contract
from tools import asmcfg, binary_census

SCHEMA_VERSION = 3
PROMPT = (
    "Recover the exact Turbo Pascal procedure from binary-derived evidence only.\n"
    "Return one complete procedure with no comments and no calls to APIs or helpers "
    "not shown in the evidence.\n"
    "Do not invent history, identifiers, comments, expected outputs, or source examples.\n"
    "\nRaw routine bytes (binary evidence):\n{bytes}\n"
    "\nAssembly listing (Ghidra evidence):\n{asm}\n"
    "\nBinary-derived facts (deterministic, non-promoting):\n{facts}\n"
)
_NON_LEAF_MNEMONICS = {
    "CALL", "CALLF", "INT", "INTO", "IN", "OUT", "JMP", "JMPF", "LOOP",
    "LOOPE", "LOOPNE", "LOOPZ", "LOOPNZ", "JCXZ", "JECXZ", "IRET",
}


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _resolve_binary(root: pathlib.Path, target: str, inventory: dict) -> pathlib.Path:
    configured = inventory.get("executable_path")
    if isinstance(configured, str) and configured:
        path = pathlib.Path(configured)
        if path.is_file():
            return path
    program = inventory.get("program")
    if isinstance(program, str) and program:
        path = root / "extracted" / target / program
        if path.is_file():
            return path
    raise FileNotFoundError(
        f"no read-only binary found for target {target}; set executable_path in functions.json"
    )


def _routine_bytes(census: dict, binary: pathlib.Path, routine: str) -> dict:
    match = next(
        (item for item in census.get("routines", []) if item.get("name") == routine),
        None,
    )
    if match is None:
        raise ValueError(f"routine missing from binary census: {routine}")
    if match.get("range_class") != "file_backed_image":
        raise ValueError(f"routine is not file-backed: {routine}")
    if not match.get("entry_matches_listing"):
        raise ValueError(f"assembly entry does not match binary mapping: {routine}")
    image_offset = match.get("image_offset")
    if not isinstance(image_offset, str) or not re.fullmatch(r"0x[0-9a-f]+", image_offset):
        raise ValueError(f"routine has no usable image offset: {routine}")
    size = match.get("size_bytes_from_metadata")
    if not isinstance(size, int) or size <= 0:
        raise ValueError(f"routine has no positive size: {routine}")
    data = binary.read_bytes()
    header_bytes = census["binary"]["header_bytes"]
    file_offset = header_bytes + int(image_offset, 16)
    if file_offset + size > len(data):
        raise ValueError(f"routine bytes extend beyond binary: {routine}")
    raw = data[file_offset:file_offset + size]
    return {
        "image_offset": image_offset,
        "file_offset": f"0x{file_offset:x}",
        "size": size,
        "hex": raw.hex(),
        "sha256": _sha256_bytes(raw),
    }


def _text(path: pathlib.Path) -> str:
    return path.read_text(errors="replace") if path.is_file() else ""


def _census_record(census: dict, routine: str) -> dict:
    match = next(
        (item for item in census.get("routines", []) if item.get("name") == routine),
        None,
    )
    if match is None:
        raise ValueError(f"routine missing from binary census: {routine}")
    return match


def _static_facts(raw: bytes) -> dict:
    facts = instruction_facts.initialization_prefix(raw)
    return {
        "method": facts["oracle"],
        "assumptions": facts["assumptions"],
        "instructions": facts["instructions"],
        "writes": facts["writes"],
        "registers": facts["registers"],
        "residue": facts["residue"],
    }


def _assembly_facts(asm_text: str) -> dict:
    parsed = asmcfg.parse_ghidra_asm(asm_text)
    bounded_paths = asmcfg.bounded_branch_paths(parsed)
    operations = []
    unsafe = []
    for instruction in parsed["insts"]:
        mnemonic = instruction.split(maxsplit=1)[0].upper() if instruction.strip() else ""
        operations.append(mnemonic)
        branch = asmcfg.is_branch(instruction)
        if (
            mnemonic in _NON_LEAF_MNEMONICS and not branch
        ) or "[" in instruction or (branch and not bounded_paths):
            unsafe.append(instruction)
    return {
        "instructions": list(parsed["insts"]),
        "addresses": list(parsed["addrs"]),
        "segments": list(parsed["segments"]),
        "operations": operations,
        "unsafe": unsafe,
        "bounded_branches": bool(bounded_paths),
        "bounded_paths": len(bounded_paths),
    }


def _evidence_gate(record: dict, assembly: dict, facts: dict) -> dict:
    reasons = []
    if record.get("range_class") != "file_backed_image":
        reasons.append("routine is not file-backed")
    if record.get("entry_matches_listing") is not True:
        reasons.append("assembly entry does not match binary mapping")
    if record.get("instruction_count_matches") is not True:
        reasons.append("assembly instruction count does not match metadata")
    if record.get("direct_calls"):
        reasons.append("routine has direct calls")
    if record.get("absolute_memory_operands"):
        reasons.append("routine has absolute memory operands")
    cfg = record.get("cfg", {})
    if cfg.get("call") or cfg.get("ret") != 1:
        reasons.append("routine is not a single-return leaf")
    if not assembly["bounded_branches"]:
        reasons.append("routine has unsupported control flow")
    if assembly["unsafe"]:
        reasons.append("assembly has control flow, device or memory operands")
    if facts["writes"]:
        reasons.append("raw-byte decoder found memory writes")
    residue = facts["residue"]
    if not isinstance(residue, dict) or residue.get("bytes_hex") != "c3":
        reasons.append("raw-byte decoder does not end at a single RET residue")
    return {"passed": not reasons, "reasons": reasons}


def _packet_evidence(root: pathlib.Path, target: str, routine: str) -> tuple[dict, str]:
    target_root = root / "targets" / target
    if not target_root.is_dir():
        raise FileNotFoundError(f"target folder missing: {target_root}")
    inventory = matrix.load_inventory(target, root)
    if not any(item.get("name") == routine for item in inventory.get("functions", [])):
        raise ValueError(f"routine missing from inventory: {routine}")
    binary = _resolve_binary(root, target, inventory)
    census = binary_census.build_census(target_root, binary)
    record = _census_record(census, routine)
    rows = {row["name"]: row for row in matrix.build(target, None, root)}
    asm_text = _text(target_root / "asm" / f"{routine}.s")
    decomp_path = target_root / "decomp" / f"{routine}.c"
    declaration = routine_contract.oracle_declaration(target_root, routine)
    bytes_info = _routine_bytes(census, binary, routine)
    facts = _static_facts(bytes.fromhex(bytes_info["hex"]))
    assembly = _assembly_facts(asm_text)
    gate = _evidence_gate(record, assembly, facts)
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "target": target,
        "routine": routine,
        "binary": {
            "path": str(binary),
            "sha256": census["binary"]["sha256"],
            "size_bytes": len(binary.read_bytes()),
        },
        "address_mapping": census["address_mapping"],
        "bytes": bytes_info,
        "static_evidence": {
            "assembly": assembly,
            "gate": gate,
            "raw_byte_facts": facts,
            "record": record,
        },
        "assembly_sha256": _sha256_bytes(asm_text.encode()),
        "decompiler_sha256": _sha256_bytes(_text(decomp_path).encode()),
        "oracle_contract": (
            {"declaration": declaration} if declaration is not None else None
        ),
        "matrix": rows.get(routine, {}),
        "source_policy": {
            "binary_derived_evidence_only": True,
            "source_examples_in_prompt": False,
            "candidate_source_in_prompt": False,
            "decompiler_output_in_prompt": False,
            "online_agent_seed": None,
        },
    }
    prompt = ""
    if gate["passed"]:
        prompt = PROMPT.format(
            bytes=bytes_info["hex"],
            asm=asm_text,
            facts=json.dumps(facts, indent=2, sort_keys=True),
        )
    return evidence, prompt


def evidence_for_routine(
    root: pathlib.Path,
    target: str,
    routine: str,
    compose: bool = True,
) -> dict:
    """Return binary-derived evidence for one routine without writing a packet."""
    evidence, _ = _packet_evidence(pathlib.Path(root), target, routine)
    if compose and target == "liero":
        from engine import composed_trace

        try:
            composed = composed_trace.compose(pathlib.Path(root), target, routine)
        except (OSError, ValueError, KeyError):
            composed = None
        if composed is not None:
            raw_hex = composed["raw_hex"]
            instruction_offsets = composed["instruction_offsets"]
            raw = bytes.fromhex(raw_hex)
            composed_assembly = {
                **_assembly_facts(composed["assembly_text"]),
                "instructions": composed["instructions"],
                "addresses": composed["addresses"],
                "segments": composed["segments"],
            }
            composed_facts = {
                **_static_facts(raw),
                "method": "composed_instruction_prefix",
                "instructions": [
                    {
                        "offset": offset,
                        "bytes_hex": raw[
                            offset : (
                                instruction_offsets[index + 1]
                                if index + 1 < len(instruction_offsets)
                                else len(raw)
                            )
                        ].hex(),
                        "relocation_offset": None,
                    }
                    for index, offset in enumerate(instruction_offsets)
                ],
                "writes": [],
            }
            original_record = evidence["static_evidence"]["record"]
            composed_record = {
                **original_record,
                "direct_calls": [],
                "absolute_memory_operands": [],
                "cfg": {**original_record.get("cfg", {}), "call": 0, "ret": 1},
            }
            composed_gate = _evidence_gate(
                composed_record, composed_assembly, composed_facts
            )
            evidence = {
                **evidence,
                "static_evidence": {
                    **evidence["static_evidence"],
                    "assembly": composed_assembly,
                    "raw_byte_facts": composed_facts,
                    "gate": composed_gate,
                },
                "bytes": {
                    **evidence["bytes"],
                    "hex": raw_hex,
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "composed_asm": composed["raw_asm"],
                },
                "oracle_contract": {
                    **(evidence.get("oracle_contract") or {}),
                    "declaration": composed["declaration"],
                },
                "composed": {
                    key: composed[key]
                    for key in (
                        "assembly_text", "raw_asm", "declaration", "near",
                        "cleanup", "return_index", "callees",
                    )
                },
            }
    return evidence


def build_packet(
    root: pathlib.Path,
    target: str,
    routine: str,
    output: pathlib.Path,
) -> dict:
    """Write an evidence-only packet; no source examples or model answers enter it."""
    root = pathlib.Path(root)
    output = pathlib.Path(output)
    if not output.is_absolute():
        output = root / output
    output.mkdir(parents=True, exist_ok=False)
    evidence, prompt = _packet_evidence(root, target, routine)
    (output / "packet.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    )
    gate = evidence["static_evidence"]["gate"]
    result = {
        "status": "packet-ready" if gate["passed"] else "blocked-static-evidence",
        "target": target,
        "routine": routine,
        "output": str(output),
        "binary_sha256": evidence["binary"]["sha256"],
        "evidence_gate": gate,
        "source_policy": evidence["source_policy"],
    }
    if prompt:
        (output / "prompt.txt").write_text(prompt)
        (output / "prompt_sha256.txt").write_text(_sha256_bytes(prompt.encode()) + "\n")
        result["prompt_sha256"] = _sha256_bytes(prompt.encode())
    (output / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def build_frontier_packet(
    root: pathlib.Path,
    target: str,
    output: pathlib.Path,
    limit: int = 5,
) -> dict:
    """Select the first callee-first leaf with complete binary-derived evidence."""
    root = pathlib.Path(root)
    store = root / "knowledge" / "knowledge.json"
    data = knowledge.load(store) if store.is_file() else {}
    frontier = matrix.select_frontier(target, data, limit=limit, root=root)
    candidates = [
        row for row in frontier
        if not row.get("unverified_callees")
        and row.get("size", 0) > 0
        and row.get("instructions", 0) > 0
    ]
    skipped: list[dict] = []
    for row in candidates:
        try:
            evidence, _ = _packet_evidence(root, target, row["name"])
        except (FileNotFoundError, ValueError):
            continue
        gate = evidence["static_evidence"]["gate"]
        if gate["passed"]:
            result = build_packet(root, target, row["name"], output)
            result["frontier"] = [item["name"] for item in frontier]
            result["skipped"] = skipped
            return result
        skipped.append({"routine": row["name"], "reasons": gate["reasons"]})
    return {
        "status": "blocked-no-static-evidence-packet",
        "target": target,
        "frontier": [row["name"] for row in frontier],
        "skipped": skipped,
    }
