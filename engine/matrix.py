"""Recovery Matrix: callee-first frontier over the function inventory."""

from __future__ import annotations

import json
import pathlib
import re

BASE = pathlib.Path(__file__).resolve().parent.parent

_CALL_RE = re.compile(
    r"(?im)^\s*[0-9a-f]{4}:[0-9a-f]{4}\s+CALL(?:F|NEAR)?\s+"
    r"(?:0x)?([0-9a-f]+)(?::(0x)?([0-9a-f]+))?"
)
_ENTRY_RE = re.compile(r"^\s*(?:0x)?([0-9a-f]{1,4}):(?:0x)?([0-9a-f]{1,4})\s*$", re.I)


def _addr(entry: str | None) -> int | None:
    if not entry:
        return None
    match = _ENTRY_RE.match(entry)
    if not match:
        return None
    return (int(match.group(1), 16) << 4) + int(match.group(2), 16)


def _resolve_root(root: pathlib.Path | None) -> pathlib.Path:
    return BASE if root is None else pathlib.Path(root)


def load_inventory(target: str, root: pathlib.Path | None = None) -> dict:
    path = _resolve_root(root) / "targets" / target / "functions.json"
    if not path.is_file():
        return {"functions": [], "num_functions": 0}
    return json.loads(path.read_text(errors="replace"))


def load_recovery(target: str, root: pathlib.Path | None = None) -> dict:
    path = _resolve_root(root) / "targets" / target / "recovery.json"
    if not path.is_file():
        return {"functions": {}}
    return json.loads(path.read_text(errors="replace"))


def callee_map(
    target: str, inventory: dict, root: pathlib.Path | None = None
) -> dict[str, list[str]]:
    by_addr = {}
    for fn in inventory.get("functions", []):
        addr = _addr(fn.get("entry"))
        if addr is not None:
            by_addr[addr] = fn["name"]
    result: dict[str, list[str]] = {}
    asm_dir = _resolve_root(root) / "targets" / target / "asm"
    for fn in inventory.get("functions", []):
        name = fn["name"]
        path = asm_dir / f"{name}.s"
        calls: list[str] = []
        if path.is_file():
            text = path.read_text(errors="replace")
            for match in _CALL_RE.finditer(text):
                if match.group(2) is not None or match.group(3) is not None:
                    segment = match.group(1)
                    offset = match.group(3) or match.group(1)
                    addr = (int(segment, 16) << 4) + int(offset, 16)
                else:
                    addr = int(match.group(1), 16)
                callee = by_addr.get(addr)
                if callee and callee != name and callee not in calls:
                    calls.append(callee)
        result[name] = calls
    return result


def build(
    target: str, data: dict | None = None, root: pathlib.Path | None = None
) -> list[dict]:
    inventory = load_inventory(target, root)
    recovery = load_recovery(target, root)
    calls = callee_map(target, inventory, root)
    knowledge = data or {}
    target_data = knowledge.get("targets", {}).get(target, {})
    verified: set[str] = set()
    for names in target_data.get("verified", {}).values():
        verified.update(names)
    candidates = target_data.get("candidates", {})
    history = knowledge.get("function_history", {}).get(target, {})

    rows = []
    for fn in inventory.get("functions", []):
        name = fn["name"]
        meta = recovery.get("functions", {}).get(name, {})
        attempts = history.get(name, {}).get("attempts", candidates.get(name, {}).get("attempts", 0))
        status = "verified" if name in verified else candidates.get(name, {}).get("status", meta.get("status", "unreviewed"))
        rows.append({
            "name": name,
            "entry": fn.get("entry"),
            "size": fn.get("size", 0),
            "instructions": fn.get("num_instructions", 0),
            "status": status,
            "attempts": attempts,
            "callees": calls.get(name, []),
            "unverified_callees": [
                callee for callee in calls.get(name, [])
                if callee not in verified
                and candidates.get(callee, {}).get("status") not in {"compiled", "verified"}
            ],
        })
    return rows


def select_frontier(target: str, data: dict, limit: int = 5,
                    only: set[str] | None = None,
                    root: pathlib.Path | None = None) -> list[dict]:
    rows = build(target, data, root)
    eligible = [
        row for row in rows
        if row["status"] not in {"verified", "unrecoverable"}
        and row["attempts"] < 3
        and (only is None or row["name"] in only)
    ]
    eligible.sort(key=lambda row: (
        len(row["unverified_callees"]),
        row["size"],
        row["name"],
    ))
    return eligible[:limit]


def summary(target: str, data: dict, root: pathlib.Path | None = None) -> dict:
    rows = build(target, data, root)
    statuses: dict[str, int] = {}
    for row in rows:
        statuses[row["status"]] = statuses.get(row["status"], 0) + 1
    return {
        "target": target,
        "total": len(rows),
        "statuses": statuses,
        "frontier": [row["name"] for row in select_frontier(target, data, limit=10)],
    }
