"""Evidence-backed source recovery tracking for disassembled targets."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from collections import Counter

from engine import draft
from engine.alternate_streams import load_verified_streams
from engine.callbacks import load_verified_callbacks, load_verified_indirect_operands
from engine.object_identity import load_verified_object_identities
from engine.object_setup import load_verified_object_setups
from engine.scoped_verification import load_scoped_checks
from tools.asmcfg import (
    build_blocks,
    cfg_stats,
    is_branch,
    is_call,
    parse_ghidra_asm,
    resolve_branch_target,
)
from tools.report import _has_pascal_implementation

SCHEMA_VERSION = 1
EVIDENCE_FIELDS = (
    "signature_and_abi",
    "control_flow",
    "call_targets",
    "state_and_memory_effects",
    "data_references",
)
RECOVERY_STATES = {
    "unreviewed",
    "in_progress",
    "evidence_mapped",
    "source_recovered",
    "partially_recoverable",
    "unrecoverable",
}
HOST_TEST_STATUSES = {"not_run", "passed", "failed", "blocked"}
ORIGINAL_BINARY_STATUSES = HOST_TEST_STATUSES | {"not_required"}
_SHORT_JCC_MNEMONICS = (
    {"JO"},
    {"JNO"},
    {"JB", "JC", "JNAE"},
    {"JAE", "JNB", "JNC"},
    {"JE", "JZ"},
    {"JNE", "JNZ"},
    {"JBE", "JNA"},
    {"JA", "JNBE"},
    {"JS"},
    {"JNS"},
    {"JP", "JPE"},
    {"JNP", "JPO"},
    {"JL"},
    {"JGE"},
    {"JLE"},
    {"JG"},
)


def _function_names(
    target_root: pathlib.Path,
) -> tuple[set[str], int | None, set[str] | None]:
    inventory_path = target_root / "functions.json"
    expected_count = None
    metadata_names: set[str] | None = None
    if inventory_path.is_file():
        inventory = json.loads(inventory_path.read_text(errors="replace"))
        expected_count = inventory.get("num_functions")
        functions = inventory.get("functions", [])
        if not isinstance(functions, list):
            raise TypeError(f"functions must be an array in {inventory_path}")
        metadata_names = {
            item["name"]
            for item in functions
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        }
    asm_dir = target_root / "asm"
    assembly_names: set[str] = set()
    if asm_dir.is_dir():
        assembly_names.update(path.stem for path in asm_dir.glob("*.s"))
    names = assembly_names | (metadata_names or set())
    return names, expected_count, metadata_names


def _new_record(function_name: str) -> dict:
    return {
        "status": "unreviewed",
        "source_file": f"src/{function_name}.inc",
        "evidence": {field: [] for field in EVIDENCE_FIELDS},
        "reviewer": "",
        "review_notes": "",
        "unrecoverable_reason": "",
        "assembly_sha256": "",
        "source_sha256": "",
        "verification": _new_verification(),
    }


def _new_verification() -> dict:
    return {
        "host_test_status": "not_run",
        "host_test_references": [],
        "has_external_effects": None,
        "original_binary_status": "not_run",
        "original_binary_references": [],
        "original_binary_reason": "",
        "notes": "",
    }


def initialize_ledger(target_root: pathlib.Path) -> pathlib.Path:
    """Create or synchronize the manual recovery ledger without losing reviews."""
    names, _, _ = _function_names(target_root)
    if not names:
        raise ValueError(f"no functions found for {target_root}")
    path = target_root / "recovery.json"
    if path.exists():
        ledger = json.loads(path.read_text(errors="replace"))
        if ledger.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"unsupported recovery ledger schema in {path}")
        if ledger.get("target") != target_root.name:
            raise ValueError(f"recovery ledger target does not match {target_root}")
        records = ledger.get("functions")
        if not isinstance(records, dict):
            raise TypeError(f"recovery ledger functions must be an object: {path}")
    else:
        ledger = {
            "schema_version": SCHEMA_VERSION,
            "target": target_root.name,
            "functions": {},
        }
        records = ledger["functions"]

    for name in sorted(names):
        record = records.setdefault(name, _new_record(name))
        if not isinstance(record, dict):
            raise TypeError(f"{name}: recovery record must be an object")
        record.setdefault("verification", _new_verification())

    target_root.mkdir(parents=True, exist_ok=True)
    _write_ledger(path, ledger)
    return path


def _sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _instruction_addresses(target_root: pathlib.Path) -> set[int]:
    asm_dir = target_root / "asm"
    addresses = set()
    if asm_dir.is_dir():
        for path in asm_dir.glob("*.s"):
            parsed = parse_ghidra_asm(path.read_text(errors="replace"))
            addresses.update(parsed["addrs"])
    return addresses


def _unresolved_control_transfers(
    target_root: pathlib.Path,
    function_name: str,
    known_addresses: set[int],
    verified_indirect_sites: set[int] | None = None,
) -> list[dict]:
    asm_path = target_root / "asm" / f"{function_name}.s"
    if not asm_path.is_file():
        return []
    parsed = parse_ghidra_asm(asm_path.read_text(errors="replace"))
    unresolved = []
    for address, instruction, source_segment in zip(
        parsed["addrs"], parsed["insts"], parsed["segments"], strict=True
    ):
        if not (is_branch(instruction) or is_call(instruction)):
            continue
        target = resolve_branch_target(instruction, source_segment)
        if target is None and address in (verified_indirect_sites or set()):
            continue
        if target is not None and target in known_addresses:
            continue
        unresolved.append(
            {
                "address": f"0x{address:05x}",
                "instruction": instruction,
                "target": f"0x{target:05x}" if target is not None else None,
                "reason": (
                    "target is not a decoded instruction"
                    if target is not None
                    else "indirect or unparsed target"
                ),
            }
        )
    return unresolved


def _safe_source_path(target_root: pathlib.Path, raw_path: str) -> pathlib.Path:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ValueError("source_file must be a non-empty target-relative path")
    relative = pathlib.Path(raw_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"source_file must be a target-relative path: {raw_path}")
    source = target_root / relative
    if not source.resolve().is_relative_to(target_root.resolve()):
        raise ValueError(f"source_file escapes target directory: {raw_path}")
    return source


def _write_ledger(path: pathlib.Path, ledger: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def _validated_references(value: object, field: str, function_name: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(reference, str) and reference.strip() for reference in value
    ):
        raise TypeError(f"{function_name}: {field} must be a list of references")
    return value


def record_validation(
    target_root: pathlib.Path,
    function_name: str,
    host_test_status: str,
    host_test_references: list[str],
    has_external_effects: bool,
    original_binary_status: str,
    original_binary_references: list[str],
    original_binary_reason: str,
    validation_notes: str,
) -> None:
    """Record host and original-binary validation separately from source review."""
    ledger_path = target_root / "recovery.json"
    if not ledger_path.is_file():
        raise FileNotFoundError(
            f"{ledger_path} is missing; initialize the recovery ledger first"
        )
    ledger = json.loads(ledger_path.read_text(errors="replace"))
    if ledger.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported recovery ledger schema in {ledger_path}")
    if ledger.get("target") != target_root.name:
        raise ValueError(f"recovery ledger target does not match {target_root}")
    records = ledger.get("functions")
    if not isinstance(records, dict):
        raise TypeError(f"recovery ledger functions must be an object: {ledger_path}")
    record = records.get(function_name)
    if not isinstance(record, dict):
        raise KeyError(f"{function_name} is not present in {ledger_path}")

    if (
        not isinstance(host_test_status, str)
        or host_test_status not in HOST_TEST_STATUSES
    ):
        raise ValueError(f"{function_name}: invalid host-test status")
    if not isinstance(original_binary_status, str) or (
        original_binary_status not in ORIGINAL_BINARY_STATUSES
    ):
        raise ValueError(f"{function_name}: invalid original-binary status")
    if not isinstance(has_external_effects, bool):
        raise TypeError(f"{function_name}: has_external_effects must be a boolean")
    host_references = _validated_references(
        host_test_references, "host_test_references", function_name
    )
    binary_references = _validated_references(
        original_binary_references, "original_binary_references", function_name
    )
    if not isinstance(original_binary_reason, str) or not isinstance(
        validation_notes, str
    ):
        raise TypeError(f"{function_name}: validation notes and reason must be text")
    if host_test_status == "passed" and not host_references:
        raise ValueError(
            f"{function_name}: passed host tests require host test references"
        )
    if original_binary_status == "passed" and not binary_references:
        raise ValueError(
            f"{function_name}: passed original-binary checks require references"
        )
    if original_binary_status == "not_required":
        if has_external_effects:
            raise ValueError(
                f"{function_name}: external effects require original-binary verification"
            )
        if not original_binary_reason.strip():
            raise ValueError(
                f"{function_name}: not_required original-binary status requires a reason"
            )
    if not validation_notes.strip():
        raise ValueError(f"{function_name}: validation notes are required")

    verification = {
        "host_test_status": host_test_status,
        "host_test_references": host_references,
        "has_external_effects": has_external_effects,
        "original_binary_status": original_binary_status,
        "original_binary_references": binary_references,
        "original_binary_reason": original_binary_reason.strip(),
        "notes": validation_notes.strip(),
    }
    record["verification"] = verification
    _write_ledger(ledger_path, ledger)


def attest_source(
    target_root: pathlib.Path,
    function_name: str,
    reviewer: str,
    review_notes: str,
    evidence: dict[str, list[str]],
) -> None:
    """Record a reviewed recovery claim and fingerprint its current inputs."""
    ledger_path = target_root / "recovery.json"
    if not ledger_path.is_file():
        raise FileNotFoundError(
            f"{ledger_path} is missing; initialize the recovery ledger first"
        )
    ledger = json.loads(ledger_path.read_text(errors="replace"))
    if ledger.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported recovery ledger schema in {ledger_path}")
    if ledger.get("target") != target_root.name:
        raise ValueError(f"recovery ledger target does not match {target_root}")
    records = ledger.get("functions")
    if not isinstance(records, dict):
        raise TypeError(f"recovery ledger functions must be an object: {ledger_path}")
    record = records.get(function_name)
    if not isinstance(record, dict):
        raise KeyError(f"{function_name} is not present in {ledger_path}")
    if set(evidence) != set(EVIDENCE_FIELDS):
        missing = sorted(set(EVIDENCE_FIELDS) - set(evidence))
        extra = sorted(set(evidence) - set(EVIDENCE_FIELDS))
        raise ValueError(
            f"evidence categories must match required fields; missing={missing}, "
            f"extra={extra}"
        )

    record.update(
        status="source_recovered",
        reviewer=reviewer,
        review_notes=review_notes,
        evidence=evidence,
    )
    assembly_path = target_root / "asm" / f"{function_name}.s"
    source_path = _safe_source_path(target_root, record.get("source_file", ""))
    if not assembly_path.is_file():
        raise FileNotFoundError(f"assembly evidence is missing: {assembly_path}")
    if not source_path.is_file():
        raise FileNotFoundError(f"Pascal source is missing: {source_path}")
    record["assembly_sha256"] = _sha256(assembly_path)
    record["source_sha256"] = _sha256(source_path)
    recovered, reason = _validate_record(
        target_root,
        function_name,
        record,
    )
    if not recovered:
        raise ValueError(f"{function_name}: cannot attest source recovery: {reason}")
    _write_ledger(ledger_path, ledger)


def _validate_record(
    target_root: pathlib.Path,
    function_name: str,
    record: dict,
    known_addresses: set[int] | None = None,
    unresolved_transfers: list[dict] | None = None,
    verified_indirect_sites: set[int] | None = None,
) -> tuple[bool, str]:
    status = record.get("status")
    if not isinstance(status, str) or status not in RECOVERY_STATES:
        raise ValueError(f"{function_name}: invalid recovery status {status!r}")

    evidence = record.get("evidence")
    if not isinstance(evidence, dict):
        raise TypeError(f"{function_name}: evidence must be an object")
    for field in EVIDENCE_FIELDS:
        references = evidence.get(field)
        if not isinstance(references, list) or not all(
            isinstance(reference, str) and reference.strip() for reference in references
        ):
            raise ValueError(
                f"{function_name}: evidence.{field} must be a list of references"
            )

    if status in {"evidence_mapped", "source_recovered"}:
        missing = [field for field in EVIDENCE_FIELDS if not evidence[field]]
        if missing:
            raise ValueError(
                f"{function_name}: {status} requires evidence for " + ", ".join(missing)
            )

    reviewer = record.get("reviewer", "")
    notes = record.get("review_notes", "")
    reason = record.get("unrecoverable_reason", "")
    if not all(isinstance(value, str) for value in (reviewer, notes, reason)):
        raise TypeError(f"{function_name}: reviewer, notes, and reason must be text")
    reviewer = reviewer.strip()
    notes = notes.strip()
    if status == "unrecoverable" and (not reviewer or not reason.strip()):
        raise ValueError(
            f"{function_name}: unrecoverable status requires reviewer and reason"
        )
    if status == "partially_recoverable" and (not reviewer or not notes):
        raise ValueError(
            f"{function_name}: partially_recoverable requires reviewer and notes"
        )
    if status != "source_recovered":
        return False, ""
    if not reviewer or not notes:
        raise ValueError(
            f"{function_name}: source_recovered requires reviewer and review_notes"
        )

    source_file = record.get("source_file")
    if not isinstance(source_file, str) or not source_file.strip():
        raise ValueError(f"{function_name}: source_file is required")
    source_path = _safe_source_path(target_root, source_file)
    if not source_path.is_file() or not _has_pascal_implementation(source_path):
        raise ValueError(
            f"{function_name}: source_recovered requires a non-placeholder "
            f"Pascal body in {source_file}"
        )
    source = source_path.read_text(errors="replace")
    declaration = re.search(r"(?im)^\s*(?:procedure|function)\s+([A-Za-z_]\w*)", source)
    if not declaration or declaration.group(1).casefold() != function_name.casefold():
        raise ValueError(
            f"{function_name}: Pascal declaration in {source_file} does not match"
        )

    asm_path = target_root / "asm" / f"{function_name}.s"
    if not asm_path.is_file():
        return False, "assembly evidence is missing"
    expected_asm_hash = record.get("assembly_sha256", "")
    expected_source_hash = record.get("source_sha256", "")
    if not expected_asm_hash or not expected_source_hash:
        raise ValueError(
            f"{function_name}: source_recovered requires assembly and source hashes"
        )
    if _sha256(asm_path) != expected_asm_hash:
        return False, "assembly evidence changed since review"
    if _sha256(source_path) != expected_source_hash:
        return False, "Pascal source changed since review"
    if unresolved_transfers is None:
        if known_addresses is None:
            alternate_streams = load_verified_streams(target_root)
            known_addresses = _instruction_addresses(target_root)
            for stream in alternate_streams:
                known_addresses.update(stream["instruction_addresses"])
            verified_indirect_sites = {
                int(edge["address"], 16)
                for stream in alternate_streams
                for edge in stream["source_edges"]
                if edge.get("transfer_kind") in {"far_indirect", "near_register"}
            }
        unresolved_transfers = _unresolved_control_transfers(
            target_root,
            function_name,
            known_addresses,
            verified_indirect_sites,
        )
    if unresolved_transfers:
        transfer = unresolved_transfers[0]
        return (
            False,
            (
                "unresolved control-flow transfer at "
                f"{transfer['address']}: {transfer['instruction']} "
                f"({transfer['reason']})"
            ),
        )
    return True, ""


def _verification_result(
    function_name: str, record: dict, source_recovered: bool
) -> dict:
    verification = _new_verification()
    stored_verification = record.get("verification", {})
    if not isinstance(stored_verification, dict):
        raise TypeError(f"{function_name}: verification must be an object")
    verification.update(stored_verification)

    host_status = verification["host_test_status"]
    binary_status = verification["original_binary_status"]
    external_effects = verification["has_external_effects"]
    if not isinstance(host_status, str) or host_status not in HOST_TEST_STATUSES:
        raise ValueError(f"{function_name}: invalid host-test status")
    if (
        not isinstance(binary_status, str)
        or binary_status not in ORIGINAL_BINARY_STATUSES
    ):
        raise ValueError(f"{function_name}: invalid original-binary status")
    if external_effects is not None and not isinstance(external_effects, bool):
        raise TypeError(f"{function_name}: has_external_effects must be a boolean")

    host_references = _validated_references(
        verification["host_test_references"], "host_test_references", function_name
    )
    binary_references = _validated_references(
        verification["original_binary_references"],
        "original_binary_references",
        function_name,
    )
    binary_reason = verification["original_binary_reason"]
    notes = verification["notes"]
    if not isinstance(binary_reason, str) or not isinstance(notes, str):
        raise TypeError(f"{function_name}: verification notes and reason must be text")
    if host_status == "passed" and not host_references:
        raise ValueError(f"{function_name}: passed host tests require references")
    if binary_status == "passed" and not binary_references:
        raise ValueError(
            f"{function_name}: passed original-binary checks require references"
        )
    if binary_status == "not_required" and (
        external_effects is not False or not binary_reason.strip()
    ):
        raise ValueError(
            f"{function_name}: not_required original-binary status requires "
            "no external effects and a reason"
        )

    behavior_verified = (
        source_recovered
        and host_status == "passed"
        and external_effects is not None
        and (
            binary_status == "passed"
            or (external_effects is False and binary_status == "not_required")
        )
    )
    return {
        **verification,
        "behavior_verified": behavior_verified,
    }


def audit_target(target_root: pathlib.Path) -> dict:
    """Audit artifacts and explicit source-recovery attestations."""
    names, expected_count, metadata_names = _function_names(target_root)
    ledger_path = target_root / "recovery.json"
    if not ledger_path.is_file():
        raise FileNotFoundError(
            f"{ledger_path} is missing; initialize the recovery ledger first"
        )
    ledger = json.loads(ledger_path.read_text(errors="replace"))
    if ledger.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported recovery ledger schema in {ledger_path}")
    if ledger.get("target") != target_root.name:
        raise ValueError(f"recovery ledger target does not match {target_root}")
    records = ledger.get("functions")
    if not isinstance(records, dict):
        raise TypeError(f"recovery ledger functions must be an object: {ledger_path}")

    assembly_names = (
        {path.stem for path in (target_root / "asm").glob("*.s")}
        if (target_root / "asm").is_dir()
        else set()
    )
    has_metadata = metadata_names is not None
    metadata_names = metadata_names or set()
    inventory_names = set(records)
    missing_ledger = sorted(names - inventory_names)
    stale_ledger = sorted(inventory_names - names)
    missing_asm = sorted(names - assembly_names)
    state_counts: Counter[str] = Counter()
    routines = []
    alternate_streams = load_verified_streams(target_root)
    known_addresses = _instruction_addresses(target_root)
    verified_indirect_sites = {
        int(edge["address"], 16)
        for stream in alternate_streams
        for edge in stream["source_edges"]
        if edge.get("transfer_kind") in {"far_indirect", "near_register"}
    }
    for stream in alternate_streams:
        known_addresses.update(stream["instruction_addresses"])
    unresolved_recovery_count = 0

    for name in sorted(names):
        record = records.get(name)
        if not isinstance(record, dict):
            raise TypeError(f"{name}: recovery record must be an object")
        unresolved_transfers = _unresolved_control_transfers(
            target_root, name, known_addresses, verified_indirect_sites
        )
        recovered, stale_reason = _validate_record(
            target_root,
            name,
            record,
            known_addresses,
            unresolved_transfers,
            verified_indirect_sites,
        )
        unresolved_recovery_count += record["status"] == "source_recovered" and bool(
            unresolved_transfers
        )
        state_counts[record["status"]] += 1
        verification = _verification_result(name, record, recovered)

        asm_path = target_root / "asm" / f"{name}.s"
        asm_text = asm_path.read_text(errors="replace") if asm_path.is_file() else ""
        parsed = parse_ghidra_asm(asm_text)
        cfg = build_blocks(parsed["addrs"], parsed["insts"], parsed["segments"])
        decomp_path = target_root / "decomp" / f"{name}.c"
        source_path = _safe_source_path(
            target_root, record.get("source_file", f"src/{name}.inc")
        )
        routines.append(
            {
                "name": name,
                "status": record["status"],
                "source_recovered": recovered,
                "verification": verification,
                "behavior_verified": verification["behavior_verified"],
                "stale_reason": stale_reason,
                "unresolved_control_transfers": unresolved_transfers,
                "assembly_present": asm_path.is_file(),
                "instruction_count": cfg["n"],
                "cfg": cfg_stats(cfg),
                "decompiler_present": decomp_path.is_file(),
                "decompiler_usable": draft.read_decomp_seed(target_root, name)
                is not None,
                "pascal_body_present": (
                    source_path.is_file() and _has_pascal_implementation(source_path)
                ),
            }
        )

    scoped_checks = load_scoped_checks(target_root)
    recovered_count = sum(item["source_recovered"] for item in routines)
    accounted_count = recovered_count + state_counts["unrecoverable"]
    total = len(names)
    return {
        "schema_version": SCHEMA_VERSION,
        "target": target_root.name,
        "alternate_streams": alternate_streams,
        "callback_protocols": load_verified_callbacks(target_root),
        "indirect_operands": load_verified_indirect_operands(target_root),
        "object_setup_protocols": load_verified_object_setups(target_root),
        "object_identity_chains": load_verified_object_identities(target_root),
        "scoped_differential_checks": scoped_checks,
        "summary": {
            "function_count": total,
            "inventory_declared_count": expected_count,
            "declared_function_count_matches": (
                expected_count is None or expected_count == len(metadata_names)
            ),
            "metadata_functions_without_assembly": (
                sorted(metadata_names - assembly_names) if has_metadata else None
            ),
            "assembly_functions_missing_from_metadata": (
                sorted(assembly_names - metadata_names) if has_metadata else None
            ),
            "assembly_functions_present": len(assembly_names & names),
            "assembly_instruction_count": sum(
                item["instruction_count"] for item in routines
            ),
            "unresolved_control_transfers": sum(
                len(item["unresolved_control_transfers"]) for item in routines
            ),
            "verified_alternate_streams": len(alternate_streams),
            "routines_with_decoded_instructions": sum(
                item["instruction_count"] > 0 for item in routines
            ),
            "routines_with_pascal_bodies": sum(
                item["pascal_body_present"] for item in routines
            ),
            "routines_with_usable_decompiler_output": sum(
                item["decompiler_usable"] for item in routines
            ),
            "evidence_mapped": state_counts["evidence_mapped"],
            "source_recovered": recovered_count,
            "scoped_differential_routines_passed": len(
                {
                    check["function"]
                    for check in scoped_checks
                    if check["status"] == "passed"
                }
            ),
            "scoped_differential_reports_invalid": len(
                {
                    check["reference"]
                    for check in scoped_checks
                    if check["status"] == "invalid"
                }
            ),
            "host_tests_passed": sum(
                item["verification"]["host_test_status"] == "passed"
                for item in routines
            ),
            "original_binary_verified": sum(
                item["verification"]["original_binary_status"] == "passed"
                for item in routines
            ),
            "behavior_verified": sum(item["behavior_verified"] for item in routines),
            "external_effects_unverified": sum(
                item["verification"]["has_external_effects"] is True
                and item["verification"]["original_binary_status"] != "passed"
                for item in routines
            ),
            "external_effects_unclassified": sum(
                item["verification"]["has_external_effects"] is None
                for item in routines
            ),
            "source_recovered_without_behavior_verification": sum(
                item["source_recovered"] and not item["behavior_verified"]
                for item in routines
            ),
            "partially_recoverable": state_counts["partially_recoverable"],
            "unrecoverable": state_counts["unrecoverable"],
            "unreviewed": state_counts["unreviewed"],
            "in_progress": state_counts["in_progress"],
            "stale_source_recoveries": sum(
                item["status"] == "source_recovered"
                and item["stale_reason"]
                in {
                    "assembly evidence is missing",
                    "assembly evidence changed since review",
                    "Pascal source changed since review",
                }
                for item in routines
            ),
            "source_recoveries_with_unresolved_control_flow": (
                unresolved_recovery_count
            ),
            "evidence_accounted_percent": (
                round(
                    (
                        accounted_count
                        + state_counts["evidence_mapped"]
                        + state_counts["partially_recoverable"]
                    )
                    * 100
                    / total,
                    2,
                )
                if total
                else 100.0
            ),
            "source_recovery_percent": (
                round(recovered_count * 100 / total, 2) if total else 100.0
            ),
            "missing_ledger_entries": missing_ledger,
            "stale_ledger_entries": stale_ledger,
            "missing_assembly_files": missing_asm,
        },
        "routines": routines,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="target slug, e.g. liero")
    parser.add_argument(
        "--init",
        action="store_true",
        help="create/synchronize targets/<target>/recovery.json",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="write the audit JSON to this path instead of stdout",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="print only aggregate counts (default prints the per-routine ledger)",
    )
    parser.add_argument(
        "--attest",
        metavar="FUNCTION",
        help="attest a reviewed source recovery for one function",
    )
    parser.add_argument("--reviewer", help="reviewer name for --attest")
    parser.add_argument("--review-notes", help="review rationale for --attest")
    parser.add_argument(
        "--evidence",
        action="append",
        default=[],
        metavar="FIELD=REFERENCE",
        help="required evidence pointer; repeat once or more for each evidence field",
    )
    parser.add_argument(
        "--record-validation",
        metavar="FUNCTION",
        help="record host and original-binary validation for one function",
    )
    parser.add_argument(
        "--host-test-status",
        choices=sorted(HOST_TEST_STATUSES),
        help="result of the focused host behavior tests",
    )
    parser.add_argument(
        "--host-test-reference",
        action="append",
        default=[],
        help="test file or report proving the host-test result; repeat as needed",
    )
    external_effects = parser.add_mutually_exclusive_group()
    external_effects.add_argument(
        "--has-external-effects",
        dest="has_external_effects",
        action="store_true",
        help="the routine depends on DOS, BIOS, hardware, overlays, or similar",
    )
    external_effects.add_argument(
        "--no-external-effects",
        dest="has_external_effects",
        action="store_false",
        help="the routine has no external effects requiring a real environment",
    )
    parser.set_defaults(has_external_effects=None)
    parser.add_argument(
        "--original-binary-status",
        choices=sorted(ORIGINAL_BINARY_STATUSES),
        help="result of checking the routine against the original executable",
    )
    parser.add_argument(
        "--original-binary-reference",
        action="append",
        default=[],
        help="DOSBox/equivalent trace or report; repeat as needed",
    )
    parser.add_argument(
        "--original-binary-reason",
        help="required rationale when original-binary validation is not_required",
    )
    parser.add_argument(
        "--validation-notes",
        help="review notes for --record-validation",
    )
    args = parser.parse_args(argv)
    target_root = pathlib.Path("targets") / args.target
    if args.init:
        initialize_ledger(target_root)
    if args.attest:
        if not args.reviewer or not args.review_notes:
            parser.error("--attest requires --reviewer and --review-notes")
        evidence: dict[str, list[str]] = {}
        for item in args.evidence:
            field, separator, reference = item.partition("=")
            if not separator or field not in EVIDENCE_FIELDS or not reference.strip():
                parser.error(
                    "--evidence must be FIELD=REFERENCE using one of: "
                    + ", ".join(EVIDENCE_FIELDS)
                )
            evidence.setdefault(field, []).append(reference.strip())
        attest_source(
            target_root,
            args.attest,
            args.reviewer,
            args.review_notes,
            evidence,
        )
    if args.record_validation:
        required_validation = {
            "--host-test-status": args.host_test_status,
            "--has-external-effects/--no-external-effects": (args.has_external_effects),
            "--original-binary-status": args.original_binary_status,
            "--validation-notes": args.validation_notes,
        }
        missing_validation = [
            option for option, value in required_validation.items() if value is None
        ]
        if missing_validation:
            parser.error(
                "--record-validation requires " + ", ".join(missing_validation)
            )
        record_validation(
            target_root,
            args.record_validation,
            args.host_test_status,
            args.host_test_reference,
            args.has_external_effects,
            args.original_binary_status,
            args.original_binary_reference,
            args.original_binary_reason or "",
            args.validation_notes,
        )
    result = audit_target(target_root)
    if args.summary_only:
        result = {"target": result["target"], "summary": result["summary"]}
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
