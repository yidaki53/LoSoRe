"""Scoped original/Pascal comparisons, separate from source-recovery attestations."""

from __future__ import annotations

import hashlib
import json
import pathlib

from engine.fact_graph import Edge, Fact, FactGraph, Node
from engine.object_identity import load_verified_object_identities
from engine.object_setup import load_verified_object_setups
from tools.liero_compare_routine_probe import (
    ROUTINE_NAME,
)
from tools.liero_compare_routine_probe import (
    validate_saved_report as validate_compare_report,
)
from tools.liero_constructor_probe import FUNCTION, validate_saved_report
from tools.liero_copy_routine_probe import ROUTINES as COPY_ROUTINES
from tools.liero_copy_routine_probe import (
    validate_saved_report as validate_copy_report,
)


def constructor_contract_graph(
    target_root: pathlib.Path, output: pathlib.Path
) -> FactGraph:
    """Oracle: conditional capacity handoff, not universal input-open correctness."""
    root = target_root.resolve().parents[1]
    report = validate_saved_report(output, root)
    if report["status"] != "passed":
        raise ValueError(
            "failed constructor comparison cannot supply checked constraints"
        )
    (identity,) = load_verified_object_identities(target_root)
    (setup,) = load_verified_object_setups(target_root)
    prefix = {
        entry["address"]: entry["bytes_hex"]
        for entry in setup["streams"]["constructor"]["instructions"]
    }
    if prefix.get(0x2841E) != "b88000" or prefix.get(0x28421) != "ab":
        raise ValueError("constructor capacity assignment changed")
    calls = identity["calls"]
    constructor = next(call for call in calls if call["role"] == "constructor")
    opened = next(call for call in calls if call["role"] == "input_open")
    if (
        constructor["target"] != 0x28409
        or opened["target"] != 0x28487
        or constructor["argument_words_before"][:2] != opened["argument_words_before"]
    ):
        raise ValueError("constructor/input-open object handoff changed")
    graph = FactGraph()
    scope = {
        "contract_sha256": report["contract_sha256"],
        "case_count": report["case_count"],
        "observed_contract_preconditions": report["contract"]["preconditions"],
        "assumptions": [
            "The reviewed caller is reached with valid, nonwrapping object and filename arguments.",
            "Filename, stack and external writes do not alias the capacity field.",
            "Constructor returns normally; code is unchanged after MZ relocation.",
        ],
        "transfer_basis": (
            "The byte-checked constructor prefix assigns the constant 128 at object+4; "
            "the checked tail only writes the nonwrapping filename at object+48 onward. "
            "The checked caller passes the same object directly to input-open. "
            "This static field rule, not extrapolation from sampled addresses, "
            "permits the conditional handoff; COM layout assumptions are not imposed on the caller."
        ),
        "normal_program_observation": False,
    }
    for node_id, routine, stage in (
        ("constructor.capacity", FUNCTION, "return"),
        ("input_open.capacity", "FUN_24dd_36b7", "entry"),
    ):
        graph.add_node(
            Node(
                node_id,
                "object_field",
                "liero",
                {
                    "routine": routine,
                    "stage": stage,
                    "byte_offset": 4,
                    "bytes": 2,
                    "scope": scope,
                },
            )
        )
    reference = str((output / "result.json").resolve())
    graph.add_fact(
        Fact(
            "constructor.capacity.checked",
            "constructor.capacity",
            "word_value",
            128,
            "oracle-verified",
            (reference, str((target_root / "alternate_streams.json").resolve())),
            "constructor-static-and-differential-v1",
            binary_sha256=report["binary_sha256"],
            assembly_sha256=report["source_hashes"][
                "targets/liero/asm/FUN_24dd_3639.s"
            ],
        )
    )
    graph.add_edge(
        Edge(
            "constructor-to-open.capacity",
            "constructor.capacity",
            "input_open.capacity",
            "same_value",
            (
                str((target_root / "alternate_streams.json").resolve()),
                f"checked-caller-constructor-call:{constructor['address']:x}",
                f"checked-caller-input-open-call:{opened['address']:x}",
            ),
        )
    )
    graph.propagate_same_value()
    return graph


def _load_copy_checks(target_root: pathlib.Path) -> list[dict]:
    """Oracle: replayed copy fixtures bound to the current includes and runtime."""
    root = target_root.resolve().parents[1]
    checks = []
    for path in sorted((target_root / "build/copy-parity").glob("*/result.json")):
        entries = [
            {
                "function": routine,
                "reference": str(path),
                "scope": "isolated_original_vs_host_pascal",
            }
            for routine in COPY_ROUTINES
        ]
        if not (root / "extracted/liero/LIERO.EXE").is_file():
            checks.extend(
                {**entry, "status": "skipped", "reason": "BYOD unavailable"}
                for entry in entries
            )
            continue
        try:
            report = validate_copy_report(path.parent, root)
            for routine in COPY_ROUTINES:
                source = target_root / "src" / f"{routine}.inc"
                if (
                    hashlib.sha256(source.read_bytes()).hexdigest()
                    != (report["candidate_source_sha256"][routine])
                ):
                    raise ValueError(
                        f"saved copy evidence differs from current {routine}"
                    )
            runtime = target_root / "src/LieroRuntime.pas"
            if (
                hashlib.sha256(runtime.read_bytes()).hexdigest()
                != (report["candidate_runtime_sha256"])
            ):
                raise ValueError("saved copy evidence differs from current runtime")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.extend(
                {**entry, "status": "invalid", "reason": str(exc)} for entry in entries
            )
            continue
        for entry in entries:
            results = [
                result
                for result in report["results"]
                if result["routine"] == entry["function"]
            ]
            checks.append(
                {
                    **entry,
                    "status": (
                        "passed"
                        if results
                        and all(result["status"] == "passed" for result in results)
                        else "failed"
                    ),
                    "suite": report["suite"],
                    "case_count": len(results),
                    "binary_sha256": report["binary_sha256"],
                }
            )
    return checks


def allocator_contract_graph(
    target_root: pathlib.Path, output: pathlib.Path
) -> FactGraph:
    """Oracle: scoped allocator projection with actual caller edge, no entry applicability."""
    from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
    from engine.routine_contract import load_contract
    from tools.liero_four_routine_pilot import validate_allocator_deduction

    root = target_root.resolve().parents[1]
    report = validate_allocator_deduction(root, output)
    binary, header, _, identity = load_binary_evidence(
        target_root, json.loads((target_root / "alternate_streams.json").read_text())
    )
    caller = load_contract(target_root, "FUN_24dd_028a")
    raw = bytes.fromhex("558bec8b4606e8c0005d7203ca0200b8cb00e970fe")
    start = caller["file_offset"]
    if (
        identity != report["binary_sha256"]
        or identity != caller["binary_sha256"]
        or caller["reviewed_bytes_hex"] != raw.hex()
        or binary[start : start + len(raw)] != raw
        or any(
            start - 1 <= r < start + len(raw)
            for r in _mz_relocation_locations(binary, header)
        )
    ):
        raise ValueError("allocator caller bytes/relocations changed")
    reference = str((output / "result.json").resolve())
    graph = FactGraph()
    graph.add_node(
        Node(
            "allocator.empty-list",
            "scoped_contract",
            "liero",
            {
                "routine": "FUN_24dd_0353",
                "scope": report["scope"],
                "normal_program_applicability": "unknown",
                "source_recovered": False,
            },
        )
    )
    graph.add_node(
        Node(
            "allocator.caller",
            "call_site",
            "liero",
            {
                "routine": "FUN_24dd_028a",
                "address": 0x290,
                "entry_state": "unknown",
                "source_recovered": False,
            },
        )
    )
    graph.add_edge(
        Edge(
            "allocator.caller-to-slice",
            "allocator.caller",
            "allocator.empty-list",
            "calls_routine_with_conditional_contract",
            (reference, str((target_root / "config/routine_contracts.json").resolve())),
        )
    )
    graph.add_fact(
        Fact(
            "allocator.empty-list.checked",
            "allocator.empty-list",
            "controlled_projection",
            {"training": 64, "terminal": 48},
            "oracle-verified",
            (reference,),
            "allocator-deduction-v1",
            binary_sha256=identity,
        )
    )
    graph.add_fact(
        Fact(
            "allocator.caller.applicability",
            "allocator.caller",
            "empty_list_default_callback_at_entry",
            None,
            "unknown",
            producer="allocator-deduction-v1",
        )
    )
    for check in _load_allocator_list_checks(target_root):
        if check["status"] != "passed":
            continue
        owned = allocator_list_contract_graph(
            target_root, pathlib.Path(check["reference"]).parent
        )
        for node in owned.nodes.values():
            graph.add_node(node)
        for fact in owned.facts.values():
            graph.add_fact(fact)
        graph.add_edge(
            Edge(
                "allocator.caller-to-owned-list",
                "allocator.caller",
                "allocator.owned-list",
                "calls_routine_with_conditional_contract",
                (check["reference"],),
            )
        )
        break
    for check in _load_allocator_entry_checks(target_root):
        if check["status"] != "passed":
            continue
        observed = allocator_entry_contract_graph(
            target_root, pathlib.Path(check["reference"]).parent
        )
        for node in observed.nodes.values():
            graph.add_node(node)
        for fact in observed.facts.values():
            graph.add_fact(fact)
        for edge in observed.edges.values():
            graph.add_edge(edge)
        graph.add_edge(
            Edge(
                "allocator.caller-to-observed-context",
                "allocator.caller",
                "allocator.observed-entry",
                "has_instrumented_applicable_context_not_universal_entry_contract",
                (check["reference"],),
            )
        )
        break
    for check in _load_error_address_checks(target_root):
        if check["status"] != "passed":
            continue
        translated = error_address_contract_graph(
            target_root, pathlib.Path(check["reference"]).parent
        )
        for node in translated.nodes.values():
            graph.add_node(node)
        for fact in translated.facts.values():
            graph.add_fact(fact)
        graph.add_edge(
            Edge(
                "allocator.caller-to-error-translation",
                "allocator.caller",
                "allocator.error-address",
                "failure_transfer_has_conditional_translation_not_complete_cleanup",
                (check["reference"],),
            )
        )
        break
    for check in _load_cleanup_dispatch_checks(target_root):
        if check["status"] != "passed":
            continue
        scoped = cleanup_dispatch_contract_graph(
            target_root, pathlib.Path(check["reference"]).parent
        )
        for node in scoped.nodes.values():
            graph.add_node(node)
        for fact in scoped.facts.values():
            graph.add_fact(fact)
        graph.add_edge(
            Edge(
                "allocator.caller-to-cleanup-dispatch",
                "allocator.caller",
                "allocator.cleanup-dispatch",
                "failure_dispatch_has_checked_mechanism_not_real_callback_contract",
                (check["reference"],),
            )
        )
        break
    for check in _load_cleanup_port_checks(target_root):
        if check["status"] != "passed":
            continue
        scoped = cleanup_port_contract_graph(
            target_root, pathlib.Path(check["reference"]).parent
        )
        for node in scoped.nodes.values():
            graph.add_node(node)
        for fact in scoped.facts.values():
            graph.add_fact(fact)
        for edge in scoped.edges.values():
            graph.add_edge(edge)
        graph.add_edge(
            Edge(
                "allocator.caller-to-real-cleanup-dependencies",
                "allocator.caller",
                "allocator.cleanup-real.callback",
                "failure_callback_candidate_has_static_dependencies_not_runtime_applicability",
                (check["reference"],),
            )
        )
        break
    return graph


def allocator_frontier(
    target_root: pathlib.Path, output: pathlib.Path
) -> dict[str, dict]:
    """Oracle: checked projection does not discharge list/callback or actual caller premises."""
    from tools.liero_four_routine_pilot import (
        allocator_deduction_freeze,
        allocator_deduction_inputs,
        validate_allocator_deduction,
    )

    root = target_root.resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {
            "allocator.empty-list": {
                "premise_sha256": hashlib.sha256(b"missing Liero BYOD").hexdigest(),
                "checked": False,
                "blockers": ["Liero BYOD unavailable"],
                "blocker_kind": "environment",
            }
        }
    _, _, facts = allocator_deduction_inputs(root)
    premise = hashlib.sha256(
        json.dumps(allocator_deduction_freeze(root, facts), sort_keys=True).encode()
    ).hexdigest()
    checked, blockers = False, []
    if (output / "result.json").is_file():
        try:
            validate_allocator_deduction(root, output)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            blockers = [f"allocator evidence invalid or terminally failed: {exc}"]
        else:
            checked = True
    return {
        "allocator.empty-list": {
            "premise_sha256": premise,
            "checked": checked,
            "blockers": blockers,
            "blocker_kind": "method",
        },
        "allocator.remaining-paths": {
            "premise_sha256": premise,
            "checked": False,
            "blockers": (
                ([] if checked else ["checked empty-list/default-callback result"])
                + [
                    "arbitrary free-list topology and node alias/lifetime contract",
                    "nondefault callback targets, effects and retry contract",
                ]
            ),
        },
        "allocator.caller028a": {
            "premise_sha256": premise,
            "checked": False,
            "blockers": [
                "0353 contract beyond checked scoped contexts",
                "entry applicability outside measured context and later heap/callback lifetime",
                "010f dynamic error/cleanup contract and full far-call ABI",
            ],
        },
    }


def _load_allocator_checks(target_root: pathlib.Path) -> list[dict]:
    """Oracle: explicit stale/absent-input outcomes for discoverable allocator reports."""
    from tools.liero_four_routine_pilot import validate_allocator_deduction

    checks = []
    root = target_root.resolve().parents[1]
    for path in sorted(
        (target_root / "build/allocator-deduction").glob("*/result.json")
    ):
        entry = {
            "function": "FUN_24dd_0353",
            "reference": str(path),
            "scope": "controlled_empty_list_default_callback_projection",
        }
        if not (root / "extracted/liero/LIERO.EXE").is_file():
            checks.append({**entry, "status": "skipped", "reason": "BYOD unavailable"})
            continue
        try:
            report = validate_allocator_deduction(root, path.parent)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append({**entry, "status": "invalid", "reason": str(exc)})
        else:
            checks.append(
                {
                    **entry,
                    "status": report["status"],
                    "case_count": 112,
                    "binary_sha256": report["binary_sha256"],
                    "source_recovered": False,
                    "automatic_discovery": False,
                }
            )
    return checks


def allocator_list_contract_graph(
    target_root: pathlib.Path, output: pathlib.Path
) -> FactGraph:
    """Oracle: checked owned-node memory, not arbitrary list topology or caller applicability."""
    from tools.liero_allocator_list_probe import list_contract, validate_report

    root = target_root.resolve().parents[1]
    report = validate_report(root, output)
    _, _, contract = list_contract(root)
    reference = str((output / "result.json").resolve())
    graph = FactGraph()
    graph.add_node(
        Node(
            "allocator.owned-list",
            "scoped_contract",
            "liero",
            {
                "routine": "FUN_24dd_0353",
                "preconditions": contract["preconditions"],
                "heap_window": contract["heap_window"],
                "source_recovered": False,
            },
        )
    )
    graph.add_fact(
        Fact(
            "allocator.owned-list.checked",
            "allocator.owned-list",
            "owned_list_projection",
            {
                "training": report["training"]["cases"],
                "terminal": report["heldout"]["cases"],
                "heap_words_per_case": 256,
                "selection": contract["selection"],
            },
            "oracle-verified",
            (reference,),
            "allocator-owned-list-v1",
            binary_sha256=contract["binary_sha256"],
        )
    )
    for name in ("arbitrary_topology", "nondefault_callback", "actual_caller"):
        graph.add_fact(
            Fact(
                f"allocator.owned-list.{name}",
                "allocator.owned-list",
                name,
                None,
                "unknown",
                producer="allocator-owned-list-v1",
            )
        )
    return graph


def _load_allocator_list_checks(target_root: pathlib.Path) -> list[dict]:
    """Oracle: source-bound list reports surfaced as scoped evidence, never source attestation."""
    from tools.liero_allocator_list_probe import validate_report

    checks = []
    root = target_root.resolve().parents[1]
    for path in sorted((target_root / "build/allocator-list").glob("*/result.json")):
        entry = {
            "function": "FUN_24dd_0353",
            "reference": str(path),
            "scope": "owned_two_node_list_default_callback_projection",
        }
        if not (root / "extracted/liero/LIERO.EXE").is_file():
            checks.append({**entry, "status": "skipped", "reason": "BYOD unavailable"})
            continue
        try:
            report = validate_report(root, path.parent)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append({**entry, "status": "invalid", "reason": str(exc)})
        else:
            checks.append(
                {
                    **entry,
                    "status": "passed",
                    "case_count": report["training"]["cases"]
                    + report["heldout"]["cases"],
                    "source_recovered": False,
                    "automatic_discovery": False,
                }
            )
    return checks


def allocator_entry_contract_graph(
    target_root: pathlib.Path, output: pathlib.Path
) -> FactGraph:
    """Oracle: measured call-point allocation origin, never an unbounded pointer lifetime."""
    from engine.alternate_streams import _mz_relocation_locations
    from tools.liero_allocator_entry_probe import entry_contract, validate_report

    root = target_root.resolve().parents[1]
    report = validate_report(root, output)
    binary, contract, _ = entry_contract(root)
    startup = contract["startup"]
    error_offset = startup["startup"]["file_offset"] + 0x10F
    error_prefix = allocator_error_transfer_constraints(
        binary[error_offset : error_offset + 26],
        {
            r - error_offset
            for r in _mz_relocation_locations(binary, startup["mz"]["header_bytes"])
            if error_offset - 1 <= r < error_offset + 26
        },
    )
    measured = report["measurement"]
    reference = str((output / "result.json").resolve())
    graph = FactGraph()
    graph.add_node(
        Node(
            "allocator.observed-entry",
            "execution_context",
            "liero",
            {
                "routine": "FUN_24dd_028a",
                "caller": "entry",
                "call_offset": 0xE50E,
                "return_offset": 0xE513,
                "source_recovered": False,
                "scope": "one instrumented DOSBox entry/return, no universal applicability",
            },
        )
    )
    graph.add_node(
        Node(
            "allocator.buffer6684",
            "allocation_origin",
            "liero",
            {
                "cell": 0x6684,
                "request_bytes": 64000,
                "valid_at_main_offset": 0xE51A,
                "later_lifetime": "unknown",
            },
        )
    )
    graph.add_edge(
        Edge(
            "allocator.observed-entry-to-buffer",
            "allocator.observed-entry",
            "allocator.buffer6684",
            "observed_allocation_result_stored_at_call_endpoint",
            (reference,),
        )
    )
    graph.add_fact(
        Fact(
            "allocator.observed-entry.applicability",
            "allocator.observed-entry",
            "empty_list_default_callback_in_measured_context",
            {
                "entry_ds": measured["before_registers"]["DS"],
                "entry_ss_sp": [
                    measured["before_registers"]["SS"],
                    measured["before_registers"]["SP"],
                ],
                "callback": measured["callback"],
                "limit": measured["limit"],
                "original_executions": 1,
                "pascal_projection_cases": 1,
                "full_abi_verified": False,
            },
            "oracle-verified",
            (reference,),
            "allocator-actual-entry-v1",
            binary_sha256=contract["binary_sha256"],
        )
    )
    graph.add_fact(
        Fact(
            "allocator.observed-entry.error_prefix_bytes",
            "allocator.observed-entry",
            "static_error_transfer_prefix_not_executed_failure_path",
            error_prefix,
            "observed",
            (str((root / "extracted/liero/LIERO.EXE").resolve()),),
            "allocator-error-prefix-byte-review",
            binary_sha256=contract["binary_sha256"],
        )
    )
    graph.add_fact(
        Fact(
            "allocator.buffer6684.origin",
            "allocator.buffer6684",
            "allocation_origin_in_measured_context",
            {
                "far_pointer": measured["result_pointer"],
                "physical_bounds": measured["allocation_physical"],
                "valid_at_main_offset": 0xE51A,
                "caller_global_bytes_checked": measured["protected_global_bytes"],
            },
            "oracle-verified",
            (reference,),
            "allocator-actual-entry-v1",
            binary_sha256=contract["binary_sha256"],
        )
    )
    for owner, name in (
        ("allocator.observed-entry", "universal_entry_applicability"),
        ("allocator.observed-entry", "error_transfer010f"),
        ("allocator.buffer6684", "later_lifetime_and_aliasing"),
    ):
        graph.add_fact(
            Fact(
                f"{owner}.{name}",
                owner,
                name,
                None,
                "unknown",
                producer="allocator-actual-entry-v1",
            )
        )
    return graph


def allocator_error_transfer_constraints(
    raw: bytes, relocation_offsets: set[int]
) -> dict:
    """Oracle: exact bytes/real DS relocation; distinguish010f->011a from alternate0116 entry."""
    expected = bytes.fromhex("595beb07b8ff0033c933dbba71198edafba306648bc10bc3743d")
    if raw != expected or relocation_offsets != {12}:
        raise ValueError("allocator error-prefix bytes/DS relocation differ")
    destination = 0x111 + 2 + int.from_bytes(raw[3:4], "little", signed=True)
    return {
        "oracle": "static_exact_error_prefix_not_failure_execution",
        "bytes_hex": raw.hex(),
        "file_slice_bytes": len(raw),
        "entry": 0x10F,
        "jump_target": destination,
        "stack_effect": "POP CX=caller returnIP; POP BX=caller returnCS; SP+=4, request remains on stack",
        "skipped_entry": {"offset": 0x116, "effect": "XOR CX,CX; XOR BX,BX"},
        "source_ds": {
            "immediate_relative_to_load": 0x1971,
            "relocation_offset": 12,
            "instruction": "MOV DX,relocated1971; MOV DS,DX",
        },
        "writes": [
            {"ds_offset": 0x6406, "value": "entry AX (028a failure supplies203)"}
        ],
        "interrupts": "STI enables interrupts; asynchronous effects are not proven by these bytes",
        "next_branch": {
            "offset": 0x127,
            "zero_target": 0x166,
            "nonzero_fallthrough": 0x129,
        },
        "unresolved": [
            "subsequent63e4-dependent ES traversal, callbacks/cleanup, external services and nonreturn behavior"
        ],
        "failure_path_executed": False,
        "routine_recovered": False,
    }


def error_address_contract_graph(
    target_root: pathlib.Path, output: pathlib.Path
) -> FactGraph:
    """Oracle: checked descriptor translation only; provenance/cleanup remain unresolved neighbors."""
    from tools.liero_error_address_probe import checked_contract, validate_report

    root = target_root.resolve().parents[1]
    report = validate_report(root, output)
    _, contract = checked_contract(root)
    reference = str((output / "result.json").resolve())
    graph = FactGraph()
    graph.add_node(
        Node(
            "allocator.error-address",
            "scoped_contract",
            "liero",
            {
                "routine": "FUN_24dd_0116",
                "entry": contract["entry"],
                "stop_before": contract["stop"],
                "preconditions": contract["preconditions"],
                "source_recovered": False,
            },
        )
    )
    graph.add_fact(
        Fact(
            "allocator.error-address.checked",
            "allocator.error-address",
            "owned_descriptor_translation",
            {
                "training": report["training"]["cases"],
                "terminal": report["heldout"]["cases"],
                "descriptor_bytes_checked_per_case": 512,
                "global_bytes_checked_per_case": 58,
                "fields": contract["fields"],
                "semantics": contract["semantics"],
                "actual_failure_path_observed": False,
            },
            "oracle-verified",
            (reference,),
            "error-address-v1",
            binary_sha256=contract["binary_sha256"],
        )
    )
    for name in (
        "actual_descriptor_provenance",
        "arbitrary_topology",
        "cleanup_callbacks_and_services",
    ):
        graph.add_fact(
            Fact(
                f"allocator.error-address.{name}",
                "allocator.error-address",
                name,
                None,
                "unknown",
                producer="error-address-v1",
            )
        )
    return graph


def _load_error_address_checks(target_root: pathlib.Path) -> list[dict]:
    """Oracle: scoped error-address comparisons cannot promote full error handling or source status."""
    from tools.liero_error_address_probe import validate_report

    root = target_root.resolve().parents[1]
    checks = []
    for path in sorted((target_root / "build/error-address").glob("*/result.json")):
        entry = {
            "function": "FUN_24dd_0116",
            "reference": str(path),
            "scope": "owned_descriptor_error_address_translation_before_cleanup",
        }
        if not (root / "extracted/liero/LIERO.EXE").is_file():
            checks.append({**entry, "status": "skipped", "reason": "BYOD unavailable"})
            continue
        try:
            report = validate_report(root, path.parent)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append({**entry, "status": "invalid", "reason": str(exc)})
        else:
            checks.append(
                {
                    **entry,
                    "status": "passed",
                    "case_count": report["training"]["cases"]
                    + report["heldout"]["cases"],
                    "source_recovered": False,
                    "automatic_discovery": False,
                }
            )
    return checks


def cleanup_callback_write_constraints(root: pathlib.Path) -> dict:
    """Oracle: two exact original write-site prefixes; no exhaustive writer or reachability claim."""
    from engine.alternate_streams import _mz_relocation_locations
    from tools.liero_four_routine_pilot import allocator_deduction_inputs

    binary, _, _ = allocator_deduction_inputs(root)
    header = int.from_bytes(binary[8:10], "little") * 16
    installer = bytes.fromhex("a102648b160464a3f6678916f867b84513ba5c13a3026489160464")
    restorer = bytes.fromhex("5589e5a1f6678b16f867a3026489160464")
    relocations = _mz_relocation_locations(binary, header)
    for offset, raw, expected in (
        (0x138C8, installer, {18}),
        (0x14905, restorer, set()),
    ):
        begin = header + offset
        if (
            binary[begin : begin + len(raw)] != raw
            or {r - begin for r in relocations if begin - 1 <= r < begin + len(raw)}
            != expected
        ):
            raise ValueError("cleanup callback write-site bytes/relocations differ")
    return {
        "oracle": "static_exact_callback_write_sites_not_lifetime_proof",
        "installer_module_offset": 0x138C8,
        "installer_bytes_hex": installer.hex(),
        "saved_previous_pointer_cells": [0x67F6, 0x67F8],
        "installed_target_relative_to_load": {"offset": 0x1345, "segment": 0x135C},
        "installer_segment_relocation_offset": 18,
        "restorer_module_offset": 0x14905,
        "restorer_bytes_hex": restorer.hex(),
        "restorer_effect": "copy saved67f6/67f8 back to6402/6404 before unresolved calls",
        "unresolved": [
            "entryDS provenance, actual installer execution/lifetime",
            "restorer callees and callback ABI/effects/reentry",
            "other writers/aliasing",
        ],
        "actual_callback_recovered": False,
    }


def cleanup_dispatch_contract_graph(
    target_root: pathlib.Path, output: pathlib.Path
) -> FactGraph:
    """Oracle: original dispatch/synthetic callback only; real callback provenance remains partial."""
    from tools.liero_cleanup_dispatch_probe import checked_contract, validate_report

    root = target_root.resolve().parents[1]
    report = validate_report(root, output)
    contract = checked_contract(root)
    writes = cleanup_callback_write_constraints(root)
    reference = str((output / "result.json").resolve())
    graph = FactGraph()
    graph.add_node(
        Node(
            "allocator.cleanup-dispatch",
            "scoped_contract",
            "liero",
            {
                "routine": "FUN_24dd_0116",
                "entry": 0x16E,
                "stop_before": 0x18B,
                "preconditions": contract["preconditions"],
                "source_recovered": False,
            },
        )
    )
    graph.add_fact(
        Fact(
            "allocator.cleanup-dispatch.mechanism",
            "allocator.cleanup-dispatch",
            "clear_before_transfer_and_far_reentry_with_synthetic_callback",
            {
                "cases": report["cases"],
                "global_bytes_per_endpoint": 58,
                "synthetic_callback": True,
                "actual_callback_recovered": False,
                "effects": contract["effects"],
            },
            "oracle-verified",
            (reference,),
            "cleanup-dispatch-mechanism-v1",
            binary_sha256=contract["binary_sha256"],
        )
    )
    graph.add_fact(
        Fact(
            "allocator.cleanup-dispatch.write-sites",
            "allocator.cleanup-dispatch",
            "static_installer_and_restorer_prefixes",
            writes,
            "observed",
            (str((root / "extracted/liero/LIERO.EXE").resolve()),),
            "cleanup-callback-write-site-review",
            binary_sha256=contract["binary_sha256"],
        )
    )
    for name in (
        "actual_callback_contract",
        "runtime_installation_lifetime",
        "cleanup_after018b",
    ):
        graph.add_fact(
            Fact(
                f"allocator.cleanup-dispatch.{name}",
                "allocator.cleanup-dispatch",
                name,
                None,
                "unknown",
                producer="cleanup-dispatch-mechanism-v1",
            )
        )
    return graph


def _load_cleanup_dispatch_checks(target_root: pathlib.Path) -> list[dict]:
    """Oracle: synthetic controls remain separately labelled, not actual callback verification."""
    from tools.liero_cleanup_dispatch_probe import validate_report

    root = target_root.resolve().parents[1]
    checks = []
    for path in sorted((target_root / "build/cleanup-dispatch").glob("*/result.json")):
        entry = {
            "function": "FUN_24dd_0116",
            "reference": str(path),
            "scope": "cleanup_dispatch_synthetic_callback_mechanism",
        }
        if not (root / "extracted/liero/LIERO.EXE").is_file():
            checks.append({**entry, "status": "skipped", "reason": "BYOD unavailable"})
            continue
        try:
            report = validate_report(root, path.parent)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append({**entry, "status": "invalid", "reason": str(exc)})
        else:
            checks.append(
                {
                    **entry,
                    "status": "passed",
                    "case_count": report["cases"],
                    "source_recovered": False,
                    "automatic_discovery": False,
                    "synthetic_callback": True,
                    "actual_callback_recovered": False,
                }
            )
    return checks


def _load_allocator_entry_checks(target_root: pathlib.Path) -> list[dict]:
    """Oracle: actual caller observations are separate from synthetic corpus and whole-source counts."""
    from tools.liero_allocator_entry_probe import validate_report

    checks = []
    root = target_root.resolve().parents[1]
    for path in sorted((target_root / "build/allocator-entry").glob("*/result.json")):
        entry = {
            "function": "FUN_24dd_028a",
            "reference": str(path),
            "scope": "instrumented_actual_64000_caller_entry_return_projection",
        }
        if not (root / "extracted/liero/LIERO.EXE").is_file():
            checks.append({**entry, "status": "skipped", "reason": "BYOD unavailable"})
            continue
        try:
            validate_report(root, path.parent)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append({**entry, "status": "invalid", "reason": str(exc)})
        else:
            checks.append(
                {
                    **entry,
                    "status": "passed",
                    "case_count": 1,
                    "source_recovered": False,
                    "automatic_discovery": False,
                }
            )
    return checks


def cleanup_sound_initialization_constraints(root: pathlib.Path) -> dict:
    """Oracle: exact sound-base argument/port stores, not configured hardware or reachability."""
    from engine.alternate_streams import _mz_relocation_locations
    from tools.liero_four_routine_pilot import allocator_deduction_inputs

    binary, _, _ = allocator_deduction_inputs(root)
    header = int.from_bytes(binary[8:10], "little") * 16
    initializer = bytes.fromhex(
        "c80600008b460c050600a3d0678b460c050a00a3d267"
        "8b460c050c00a3d4678b460c050e00a3d667e885ff"
    )
    caller = bytes.fromhex("ff36d265a0d46550a0d56550a0d665509a86005c13")
    relocations = _mz_relocation_locations(binary, header)
    for offset, raw, expected in (
        (0x13646, initializer, set()),
        (0x24E, caller, {19}),
    ):
        begin = header + offset
        if (
            binary[begin : begin + len(raw)] != raw
            or {r - begin for r in relocations if begin - 1 <= r < begin + len(raw)}
            != expected
        ):
            raise ValueError("sound initialization bytes/relocations differ")
    ports = {}
    for index, name in enumerate(("reset", "read", "write", "status")):
        start = 4 + index * 9
        ports[name] = {
            "cell": int.from_bytes(initializer[start + 7 : start + 9], "little"),
            "base_delta": int.from_bytes(initializer[start + 4 : start + 6], "little"),
        }
    return {
        "oracle": "static_exact_sound_initialization_not_device_protocol",
        "initializer_module_offset": 0x13646,
        "initializer_bytes_hex": initializer.hex(),
        "caller_module_offset": 0x24E,
        "caller_bytes_hex": caller.hex(),
        "caller_segment_relocation_offset": 19,
        "base_argument": {"caller_cell": 0x65D2, "width": 16, "callee_bp_offset": 12},
        "ports": ports,
        "arithmetic": "unsigned16(base + delta) modulo65536",
        "actual_base_value": None,
        "runtime_reachability": "unknown",
        "unresolved": [
            "caller DS and configured DS65d2 value/lifetime at this call",
            "reset/read/device outcomes before callback installation",
            "later port-cell writes/aliasing and callback entry DS/lifetime",
        ],
        "source_recovered": False,
    }


def cleanup_port_contract_graph(
    target_root: pathlib.Path, output: pathlib.Path
) -> FactGraph:
    """Oracle: static real callback dependencies and owned PIC ready path, not sound-device parity."""
    from tools.liero_cleanup_port_probe import checked_contract, validate_report

    root = target_root.resolve().parents[1]
    report = validate_report(root, output)
    contract = checked_contract(root)
    reference = str((output / "result.json").resolve())
    binary_reference = str((root / "extracted/liero/LIERO.EXE").resolve())
    graph = FactGraph()
    targets = {}
    for name, region in contract["regions"].items():
        node_id = f"allocator.cleanup-real.{name}"
        targets[region["module_offset"]] = node_id
        graph.add_node(
            Node(
                node_id,
                "conditional_routine_contract",
                "liero",
                {
                    "module_offset": region["module_offset"],
                    "source_recovered": False,
                    "actual_device_verified": False,
                    "runtime_applicability": "unknown",
                },
            )
        )
        graph.add_fact(
            Fact(
                f"{node_id}.bytes",
                node_id,
                "original_bytes_and_actual_relocations",
                region,
                "observed",
                (binary_reference,),
                "cleanup-port-dependency-review",
                binary_sha256=contract["binary_sha256"],
            )
        )
    for caller, callees in contract["calls"].items():
        for index, callee in enumerate(callees):
            graph.add_edge(
                Edge(
                    f"allocator.cleanup-real.{caller}.call-{index}",
                    f"allocator.cleanup-real.{caller}",
                    targets[callee],
                    "static_direct_call_not_runtime_reachability",
                    (binary_reference,),
                )
            )
    graph.add_fact(
        Fact(
            "allocator.cleanup-real.write.pic-ready",
            "allocator.cleanup-real.write",
            "original_ready_path_owned_pic_vs_pascal",
            {
                "cases": report["cases"],
                "ready_masks": [0, 0x7F],
                "command_bytes": 256,
                "globals_checked_per_case": 64,
                "semantics": contract["write_semantics"],
                "actual_device_verified": False,
                "busy_path_executed": False,
            },
            "oracle-verified",
            (reference,),
            "cleanup-port-pic-ready-v1",
            binary_sha256=contract["binary_sha256"],
        )
    )
    for name, predicate in (
        ("write", "actual_sound_device_and_busy_transitions"),
        ("callback", "actual_installation_lifetime_and_reentry"),
        ("delay", "bios15_wait_outcome"),
        ("vector", "dos21_vector_update_outcome"),
        ("reset", "actual_reset_read_protocol"),
    ):
        graph.add_fact(
            Fact(
                f"allocator.cleanup-real.{name}.unresolved",
                f"allocator.cleanup-real.{name}",
                predicate,
                None,
                "unknown",
                producer="cleanup-port-dependency-review",
            )
        )
    initialization = cleanup_sound_initialization_constraints(root)
    init_id = "allocator.cleanup-real.sound-init"
    graph.add_node(
        Node(
            init_id,
            "conditional_initialization",
            "liero",
            {
                "source_recovered": False,
                "actual_device_verified": False,
                "runtime_applicability": "unknown",
            },
        )
    )
    graph.add_fact(
        Fact(
            f"{init_id}.static",
            init_id,
            "base_argument_to_port_cells_before_reset",
            initialization,
            "observed",
            (binary_reference,),
            "cleanup-sound-initialization-review",
            binary_sha256=contract["binary_sha256"],
        )
    )
    graph.add_fact(
        Fact(
            f"{init_id}.runtime",
            init_id,
            "actual_configured_base_and_installation_lifetime",
            None,
            "unknown",
            producer="cleanup-sound-initialization-review",
        )
    )
    for name in ("write", "reset"):
        graph.add_edge(
            Edge(
                f"{init_id}.to-{name}",
                init_id,
                f"allocator.cleanup-real.{name}",
                "initializes_port_cell_used_by_not_runtime_provenance",
                (binary_reference,),
            )
        )
    return graph


def _load_cleanup_port_checks(target_root: pathlib.Path) -> list[dict]:
    """Oracle: ready-only PIC control cannot attest actual device or complete callback behavior."""
    from tools.liero_cleanup_port_probe import validate_report

    root = target_root.resolve().parents[1]
    checks = []
    for path in sorted((target_root / "build/cleanup-port").glob("*/result.json")):
        entry = {
            "function": "FUN_235c_0000",
            "reference": str(path),
            "scope": "original_port_leaf_ready_on_owned_pic_vs_pascal",
        }
        if not (root / "extracted/liero/LIERO.EXE").is_file():
            checks.append({**entry, "status": "skipped", "reason": "BYOD unavailable"})
            continue
        try:
            report = validate_report(root, path.parent)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append({**entry, "status": "invalid", "reason": str(exc)})
        else:
            checks.append(
                {
                    **entry,
                    "status": "passed",
                    "case_count": report["cases"],
                    "source_recovered": False,
                    "automatic_discovery": False,
                    "ready_only": True,
                    "actual_device_verified": False,
                }
            )
    return checks


def load_scoped_checks(target_root: pathlib.Path) -> list[dict]:
    """Oracle: revalidated reports; stale/invalid artifacts are explicit non-passes."""
    if target_root.name != "liero":
        return []
    root = target_root.resolve().parents[1]
    checks = []
    for path in sorted(
        (target_root / "build/constructor-parity").glob("*/result.json")
    ):
        entry = {
            "function": FUNCTION,
            "reference": str(path),
            "scope": "isolated_original_vs_host_pascal",
        }
        if not (root / "extracted/liero/LIERO.EXE").is_file():
            checks.append({**entry, "status": "skipped", "reason": "BYOD unavailable"})
            continue
        try:
            report = validate_saved_report(path.parent, root)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append({**entry, "status": "invalid", "reason": str(exc)})
            continue
        checks.append(
            {
                **entry,
                "status": report["status"],
                "case_count": report["case_count"],
                "contract_sha256": report["contract_sha256"],
            }
        )
    for path in sorted((target_root / "build/comparator-parity").glob("*/result.json")):
        entry = {
            "function": ROUTINE_NAME,
            "reference": str(path),
            "scope": "isolated_original_vs_host_pascal",
        }
        if not (root / "extracted/liero/LIERO.EXE").is_file():
            checks.append({**entry, "status": "skipped", "reason": "BYOD unavailable"})
            continue
        try:
            report = validate_compare_report(path.parent, root)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append({**entry, "status": "invalid", "reason": str(exc)})
            continue
        checks.append(
            {
                **entry,
                "status": report["status"],
                "case_count": report["case_count"],
                "binary_sha256": report["original_binary_sha256"],
            }
        )
    checks.extend(_load_copy_checks(target_root))
    checks.extend(_load_allocator_checks(target_root))
    checks.extend(_load_allocator_list_checks(target_root))
    checks.extend(_load_allocator_entry_checks(target_root))
    checks.extend(_load_error_address_checks(target_root))
    checks.extend(_load_cleanup_dispatch_checks(target_root))
    checks.extend(_load_cleanup_port_checks(target_root))
    return checks
