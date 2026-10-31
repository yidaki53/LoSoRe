"""Scoped original/Pascal comparisons, separate from source-recovery attestations."""

from __future__ import annotations

import hashlib
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
    return checks
