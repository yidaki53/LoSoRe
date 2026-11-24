"""Generic blocker triage and leverage ranking for unverified routines."""

from __future__ import annotations

import pathlib
import re
from typing import Any

from engine import knowledge, matrix
from tools import asmcfg

SCHEMA_VERSION = 1
MIN_HIT_RATE = 0.25
DEFAULT_MIN_GROUP_COUNT = 2
FOCUS_PRIORITY_BONUS = 8.0

_FAR_TRANSFER = re.compile(r"^(?:JMPF|RETF)\b")
_RETURN = re.compile(r"^(?:RET|IRET|RETW|RETF)\b")
_DEVICE_SERVICE = re.compile(r"^(?:INT\b|INTO\b|IN\b|OUT\b|IRET\b)")
_FAR_POINTER_LOAD = re.compile(r"^(?:LES|LDS)\b")
_ABSOLUTE_MEMORY = re.compile(r"\[\s*(?:0X)?[0-9A-F]+\s*\]", re.I)
_STRING_MEMORY = re.compile(
    r"^(?:REP\s+)?(?:MOVS|STOS|LODS|CMPS|SCAS)[BWD]?(?:\.[A-Z]+)?\b", re.I)
_FRAME_POINTER = re.compile(r"\[(?:BP|EBP)\b|\b(?:ENTER|LEAVE)\b", re.I)


def _root(repo_root: pathlib.Path | None) -> pathlib.Path:
    return matrix.BASE if repo_root is None else pathlib.Path(repo_root)


def _data(repo_root: pathlib.Path | None, target: str, data: dict | None) -> dict:
    if data is not None:
        return data
    store = _root(repo_root) / "knowledge" / "knowledge.json"
    if store.is_file():
        return knowledge.load(store)
    return {}


def _entry_addresses(inventory: dict) -> dict[int, str]:
    addresses: dict[int, str] = {}
    for fn in inventory.get("functions", []):
        entry = matrix._addr(fn.get("entry"))
        if entry is not None:
            addresses[entry] = fn["name"]
    return addresses


def _parsed_routines(
    repo_root: pathlib.Path, target: str, inventory: dict
) -> dict[str, dict]:
    asm_dir = repo_root / "targets" / target / "asm"
    parsed: dict[str, dict] = {}
    for fn in inventory.get("functions", []):
        name = fn["name"]
        path = asm_dir / f"{name}.s"
        if not path.is_file():
            continue
        parsed[name] = asmcfg.parse_ghidra_asm(path.read_text(errors="replace"))
    return parsed


def _transfer_targets(
    parsed: dict,
    entry_addresses: dict[int, str],
    unverified_names: set[str],
) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {
        "known": set(),
        "unverified": set(),
        "external": set(),
        "indirect": set(),
    }
    insts = parsed.get("insts", [])
    segments = parsed.get("segments", [None] * len(insts))
    addresses = set(parsed.get("addrs", []))
    for index, instruction in enumerate(insts):
        if not (asmcfg.is_call(instruction) or asmcfg.is_branch(instruction)):
            continue
        segment = segments[index] if index < len(segments) else None
        target_addr = asmcfg.resolve_branch_target(instruction, segment)
        if target_addr is None:
            result["indirect"].add("indirect")
            continue
        if target_addr in entry_addresses and target_addr not in addresses:
            target_name = entry_addresses[target_addr]
            result["known"].add(target_name)
            if target_name in unverified_names:
                result["unverified"].add(target_name)
        elif target_addr not in entry_addresses and target_addr not in addresses:
            result["external"].add(hex(target_addr))
    return result


def _blockers(
    row: dict,
    parsed: dict,
    entry_addresses: dict[int, str],
    unverified_names: set[str],
) -> list[str]:
    insts = parsed.get("insts", [])
    blockers: set[str] = set()
    if not insts:
        blockers.add("missing-assembly")
    if any(asmcfg.is_call(inst) for inst in insts):
        blockers.add("direct-call")
    if any(_FAR_TRANSFER.match(inst) for inst in insts):
        blockers.add("far-transfer")
    if any(_DEVICE_SERVICE.match(inst) for inst in insts):
        blockers.add("device-service")
    if any(_FAR_POINTER_LOAD.match(inst) for inst in insts):
        blockers.add("far-pointer-load")
    if any(_ABSOLUTE_MEMORY.search(inst) for inst in insts):
        blockers.add("absolute-memory")
    if any(asmcfg.is_branch(inst) for inst in insts):
        blockers.add("branch-control-flow")
    if any(_STRING_MEMORY.match(inst) for inst in insts):
        blockers.add("string-memory")
    if any(_FRAME_POINTER.search(inst) for inst in insts):
        blockers.add("frame-pointer")
    if insts and insts[-1] != "RET":
        if _RETURN.match(insts[-1]):
            blockers.add("return-immediate")
        else:
            blockers.add("missing-return")
    if row.get("unverified_callees"):
        blockers.add("unverified-callee")
    if any(asmcfg.is_branch(inst) for inst in insts):
        if not asmcfg.bounded_branch_paths(parsed):
            blockers.add("unsupported-control-flow")
    transfers = _transfer_targets(parsed, entry_addresses, unverified_names)
    if transfers["unverified"]:
        blockers.add("unverified-callee")
    if transfers["known"]:
        blockers.add("composed-transfer")
    if transfers["external"]:
        blockers.add("external-transfer")
    if transfers["indirect"]:
        blockers.add("indirect-transfer")
    if not blockers:
        blockers.add("leaf-decode")
    return sorted(blockers)


def _call_graph(
    target: str,
    inventory: dict,
    root: pathlib.Path,
    parsed: dict[str, dict],
    entry_addresses: dict[int, str],
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    calls: dict[str, set[str]] = {
        name: set(targets)
        for name, targets in matrix.callee_map(target, inventory, root).items()
    }
    jumps: dict[str, set[str]] = {}
    for source, parsed_routine in parsed.items():
        insts = parsed_routine.get("insts", [])
        segments = parsed_routine.get("segments", [None] * len(insts))
        targets: set[str] = set()
        for index, instruction in enumerate(insts):
            if not asmcfg.is_branch(instruction):
                continue
            segment = segments[index] if index < len(segments) else None
            target_addr = asmcfg.resolve_branch_target(instruction, segment)
            if target_addr is None:
                continue
            target_name = entry_addresses.get(target_addr)
            if target_name and target_name != source:
                targets.add(target_name)
        if targets:
            jumps[source] = targets
    return calls, jumps


def _invert(graph: dict[str, set[str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for source, targets in graph.items():
        for target_name in targets:
            result.setdefault(target_name, set()).add(source)
    return result


def _transitive_callers(name: str, callers: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    pending = list(callers.get(name, ()))
    while pending:
        caller = pending.pop()
        if caller == name or caller in seen:
            continue
        seen.add(caller)
        pending.extend(callers.get(caller, ()))
    return seen


def _score(
    row: dict,
    direct: set[str],
    transitive: set[str],
    jumps: set[str],
    rows_by_name: dict[str, dict],
) -> float:
    unlockable = {
        caller for caller in direct
        if name_in_callees(row["name"], rows_by_name.get(caller, {}))
    }
    unverified_direct = {
        caller for caller in direct
        if rows_by_name.get(caller, {}).get("status") not in {"verified", "unrecoverable"}
    }
    unverified_transitive = {
        caller for caller in transitive - direct
        if rows_by_name.get(caller, {}).get("status") not in {"verified", "unrecoverable"}
    }
    size = float(row.get("size", 0) or 0)
    score = (
        6.0 * len(unlockable)
        + 3.0 * len(unverified_direct)
        + 1.0 * len(unverified_transitive)
        + 2.0 * len(jumps)
        + max(0.0, 0.5 - size / 200.0)
    )
    return round(score, 4)


def name_in_callees(name: str, row: dict) -> bool:
    return name in set(row.get("unverified_callees", []))


def focus_priority(
    report: dict, bonus: float = FOCUS_PRIORITY_BONUS
) -> dict[str, float]:
    priority = {
        name: float(score)
        for name, score in report.get("priority", {}).items()
    }
    focus = report.get("next_capability")
    if not focus:
        return priority
    for group in report.get("groups", []):
        if group.get("capability") != focus:
            continue
        for name in group.get("routines", []):
            priority[name] = priority.get(name, 0.0) + float(bonus)
        break
    return priority


def analyze(
    repo_root: pathlib.Path | None,
    target: str,
    data: dict | None = None,
    min_group_count: int = DEFAULT_MIN_GROUP_COUNT,
) -> dict:
    root = _root(repo_root)
    knowledge_data = _data(repo_root, target, data)
    inventory = matrix.load_inventory(target, root)
    rows = matrix.build(target, knowledge_data, root)
    rows_by_name = {row["name"]: row for row in rows}
    verified_names = {
        row["name"] for row in rows if row.get("status") == "verified"
    }
    unverified_names = {
        row["name"] for row in rows
        if row.get("status") not in {"verified", "unrecoverable"}
    }
    entry_addresses = _entry_addresses(inventory)
    parsed = _parsed_routines(root, target, inventory)
    calls, jumps = _call_graph(target, inventory, root, parsed, entry_addresses)
    callers = _invert(calls)
    jump_callers = _invert(jumps)
    graph = {
        name: set(targets) for name, targets in calls.items()
    }
    for name, targets in jumps.items():
        graph.setdefault(name, set()).update(targets)
    all_callers = _invert(graph)

    attempts = int(knowledge_data.get("total_attempts", 0) or 0)
    verified = int(knowledge_data.get("total_verified", 0) or 0)
    hit_rate = round(verified / attempts, 4) if attempts else 0.0
    stop = attempts >= 12 and hit_rate < MIN_HIT_RATE

    routines: list[dict[str, Any]] = []
    priority: dict[str, float] = {}
    for row in rows:
        name = row["name"]
        eligible = (
            row.get("status") not in {"verified", "unrecoverable"}
            and int(row.get("attempts", 0) or 0) < 3
        )
        direct = set(all_callers.get(name, ()))
        transitive = _transitive_callers(name, all_callers)
        branch_refs = set(jump_callers.get(name, ()))
        unlockable = {
            caller for caller in direct
            if name_in_callees(name, rows_by_name.get(caller, {}))
        }
        score = 0.0 if stop or not eligible else _score(
            row, direct, transitive, branch_refs, rows_by_name
        )
        routines.append({
            "name": name,
            "entry": row.get("entry"),
            "size": row.get("size", 0),
            "instructions": row.get("instructions", 0),
            "status": row.get("status"),
            "attempts": row.get("attempts", 0),
            "eligible": eligible,
            "blockers": _blockers(
                row, parsed.get(name, {}), entry_addresses, unverified_names
            ),
            "direct_callers": sorted(direct),
            "transitive_callers": sorted(transitive),
            "branch_referenced_by": sorted(branch_refs),
            "unlockable_callers": sorted(unlockable),
            "priority": score,
        })
        if eligible and score > 0:
            priority[name] = score

    grouped: dict[str, dict[str, Any]] = {}
    for routine in routines:
        if not routine["eligible"]:
            continue
        for blocker in routine["blockers"]:
            group = grouped.setdefault(blocker, {
                "capability": blocker,
                "routine_count": 0,
                "leverage": 0.0,
                "routines": [],
                "unlockable_callers": set(),
            })
            group["routine_count"] += 1
            group["leverage"] += routine["priority"]
            group["routines"].append(routine["name"])
            group["unlockable_callers"].update(routine["unlockable_callers"])
    groups = []
    for group in grouped.values():
        groups.append({
            "capability": group["capability"],
            "routine_count": group["routine_count"],
            "leverage": round(float(group["leverage"]), 4),
            "routines": sorted(group["routines"]),
            "unlockable_callers": sorted(group["unlockable_callers"]),
        })
    groups.sort(key=lambda group: (
        -group["leverage"], -group["routine_count"], group["capability"]
    ))
    eligible_groups = [
        group for group in groups if group["routine_count"] >= min_group_count
    ]
    next_capability = None if stop or not eligible_groups else eligible_groups[0]["capability"]

    return {
        "schema_version": SCHEMA_VERSION,
        "target": target,
        "total_routines": len(rows),
        "verified_routines": len(verified_names),
        "coverage": round(len(verified_names) / len(rows), 4) if rows else 0.0,
        "attempts": attempts,
        "total_verified": verified,
        "hit_rate": hit_rate,
        "stop": stop,
        "stop_reason": (
            f"yield below {MIN_HIT_RATE:.0%}" if stop else None
        ),
        "eligible_routines": sum(1 for routine in routines if routine["eligible"]),
        "priority": priority,
        "next_capability": next_capability,
        "groups": groups,
        "routines": routines,
    }
