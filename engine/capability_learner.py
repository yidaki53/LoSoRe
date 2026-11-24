"""Gap-driven capability proposal and reuse prioritization."""

from __future__ import annotations

import pathlib
from typing import Any

from engine import capability_registry as registry

MIN_BASE_OVERLAP = 0.35
MIN_GAP_COUNT = 2


def propose(
    root: pathlib.Path | None = None,
    min_gap_count: int = MIN_GAP_COUNT,
    min_base_overlap: float = MIN_BASE_OVERLAP,
) -> list[str]:
    data = registry.load(root)
    bases = [
        (capability_id, entry)
        for capability_id, entry in data.get("capabilities", {}).items()
        if entry.get("status") == "verified" and entry.get("renderer")
    ]
    proposals: list[str] = []
    for gap_hash, gap in data.get("gaps", {}).items():
        if int(gap.get("count", 0)) < min_gap_count:
            continue
        capability_id = f"gap-{gap_hash[:12]}"
        if capability_id in data.get("capabilities", {}):
            continue
        signature = gap.get("signature", {})
        best_id = ""
        best_entry: dict[str, Any] = {}
        best_score = 0.0
        for base_id, base_entry in bases:
            score = registry.signature_overlap(base_entry, signature)
            if score > best_score:
                best_id, best_entry, best_score = base_id, base_entry, score
        usable = best_score >= min_base_overlap
        data["capabilities"][capability_id] = {
            "status": "candidate",
            "source": "gap-generalization",
            "renderer": best_entry.get("renderer", "") if usable else "",
            "base_capability": best_id if usable else "",
            "similarity": best_score,
            "gap_hash": gap_hash,
            "gap_count": int(gap.get("count", 0)),
            "signatures": [signature] if signature else [],
            "outcomes": {},
        }
        proposals.append(capability_id)
    if proposals:
        registry.save(data, root)
    return sorted(proposals)


def frontier_priority(root: pathlib.Path | None, target: str) -> dict[str, float]:
    data = registry.load(root)
    scores: dict[str, float] = {}
    for gap_hash, gap in data.get("gaps", {}).items():
        examples = [
            item for item in gap.get("examples", [])
            if item.get("target") == target and item.get("routine")
        ]
        if not examples:
            continue
        weight = 1.0 + min(int(gap.get("count", 0)), 8) * 0.25
        for item in examples:
            routine = str(item["routine"])
            scores[routine] = scores.get(routine, 0.0) + weight / len(examples)
    for capability_id, entry in data.get("capabilities", {}).items():
        if entry.get("source") != "gap-generalization":
            continue
        if entry.get("status") not in {"candidate", "verified"}:
            continue
        if not entry.get("renderer"):
            continue
        gap_hash = str(entry.get("gap_hash", ""))
        gap = data.get("gaps", {}).get(gap_hash, {})
        examples = [
            item for item in gap.get("examples", [])
            if item.get("target") == target and item.get("routine")
        ]
        for item in examples:
            routine = str(item["routine"])
            scores[routine] = scores.get(routine, 0.0) + 1.0 / max(len(examples), 1)
    return scores
