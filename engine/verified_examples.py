"""Verified Pascal examples management for few-shot learning.

Manages the recording and retrieval of verified Pascal function bodies
that have passed oracle verification. These serve as few-shot prompts
for draft generation, improving quality over time as more functions
are verified.

Phase 3: Example Management (from implementation_plan.md)
"""

from __future__ import annotations

import hashlib
import json
import pathlib


def compiler_key(compiler: str, platform: str) -> str:
    """Compute compiler key for knowledge base lookup."""
    comp = (compiler or "unknown").strip().lower()
    plat = (platform or "unknown").strip().lower()
    return comp if comp not in ("", "unknown", "todo") else f"unknown@{plat}"


def record_verified_pascal(target: str, fn: str, pascal_body: str, oracle: str,
                           data: dict = None) -> str:
    """Record a verified Pascal example for a passed function.

    Args:
        target: Target slug (e.g. "liero")
        fn: Function name
        pascal_body: Pascal procedure/function body
        oracle: Oracle that verified the function
        data: Knowledge base dict (optional, uses default store if None)

    Returns:
        example_id: SHA256 hash identifying this example
    """
    from engine.knowledge import _yaml_value, STORE, save

    # Get compiler/platform info for this target
    config_dir = pathlib.Path(f"targets/{target}/config")
    toolchain = {
        "compiler": _yaml_value(config_dir / "toolchain.yaml", "compiler", ""),
        "platform": _yaml_value(config_dir / "toolchain.yaml", "platform", ""),
    }

    key = compiler_key(toolchain["compiler"], toolchain["platform"])

    # Generate example_id from hash of (toolchain, fn, asm, pascal)
    asm_file = pathlib.Path(f"targets/{target}/asm/{fn}.s")
    asm_body = ""
    if asm_file.is_file():
        asm_body = asm_file.read_text(errors="replace")

    digest_input = "\0".join(
        (toolchain["compiler"], target, fn, asm_body, pascal_body)
    )
    example_id = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()

    # Check if example already exists in verified_pascal_examples
    store = STORE if data is None else data
    examples = store.setdefault("verified_pascal_examples", {}).setdefault(
        key, []
    )

    if not any(item.get("example_id") == example_id for item in examples):
        record = {
            "example_id": example_id,
            "fn": fn,
            "target": target,
            "compiler": toolchain["compiler"],
            "platform": toolchain["platform"],
            "language": "pascal",
            "calling_convention": None,
            "asm": asm_body,
            "decomp_c": "",
            "pascal": pascal_body,
            "verification_status": "verified",
            "oracle": oracle,
            "verified_at": __import__("datetime").date.today().isoformat(),
        }
        examples.append(record)

    # Update example quality tracking
    if key not in data.setdefault("compilers", {}):
        data.setdefault("compilers", {})[key] = {}
    if fn not in data["compilers"][key].setdefault("targets", []):
        data["compilers"][key].setdefault("targets", []).append(fn)

    save(store, STORE)
    return example_id


def get_verified_examples(target: str, compiler: str, platform: str,
                          query_asm: str = "", limit: int = 3,
                          min_success_rate: float = 0.3) -> list[dict]:
    """Retrieve verified same-toolchain Pascal pairs by structural anchors.

    Args:
        target: Target slug
        compiler: Compiler name
        platform: Platform name
        query_asm: Assembly text to match against
        limit: Maximum number of examples to return
        min_success_rate: Minimum success rate threshold

    Returns:
        List of verified example dicts matching the query
    """
    from engine.knowledge import _yaml_value, load, STORE

    key = compiler_key(compiler, platform)
    data = load(STORE)

    # Get verified examples for this toolchain
    examples = data.get("verified_pascal_examples", {}).get(key, [])

    # Filter by verification status and oracle
    filtered = []
    for ex in examples:
        if ex.get("verification_status") != "verified":
            continue
        if not ex.get("oracle"):
            continue
        if ex.get("success_rate", 1.0) < min_success_rate:
            continue

        # Compute structural anchor overlap
        ex_asm = ex.get("asm", "")
        query_anchors = set()
        for match in __import__("re").finditer(r"(?i)(push|mov|pushf|pushds)", query_asm):
            query_anchors.add(match.group(1).lower())
        ex_anchors = set()
        for match in __import__("re").finditer(r"(?i)(push|mov|pushf|pushds)", ex_asm):
            ex_anchors.add(match.group(1).lower())

        overlap = len(query_anchors & ex_anchors)
        quality = ex.get("success_rate", 1.0)
        filtered.append((ex, quality, overlap))

    # Sort by quality * overlap, then by recency
    filtered.sort(key=lambda x: (x[1] * x[2], -x[0].get("verified_at", "")), reverse=True)

    filtered_examples = [ex for ex, _q, _o in filtered[:limit]]
    return filtered_examples
    filtered = [ex for ex, _q, _o in filtered[:limit]]
    return filtered


def update_example_quality(example_id: str, success: bool) -> None:
    """Update the quality tracking for a verified example."""
    from engine.knowledge import load, save, STORE

    data = load(STORE)

    # Search through verified_pascal_examples
    for key, ex_list in data.get("verified_pascal_examples", {}).items():
        for ex in ex_list:
            if ex.get("example_id") == example_id:
                if success:
                    ex["success_rate"] = min(ex.get("success_rate", 0) + 0.1, 1.0)
                else:
                    ex["success_rate"] = max(ex.get("success_rate", 1.0) - 0.1, 0.0)
                ex["attempts"] = ex.get("attempts", 0) + 1
                break

    save(data, STORE)
