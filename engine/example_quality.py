"""Example quality tracking for few-shot examples.

Each verified example in knowledge.json accumulates success/failure counts.
Examples with success_rate < 0.3 are excluded from few-shot prompts so the
factory stops leaning on bad translations.

Data model (added to knowledge.json):
  "example_quality": {
    "<toolchain>": {
      "<fn_key>": {
        "success_count": 5,
        "failure_count": 1,
        "last_used": "2026-10-27"
      }
    }
  }

fn_key is normally the function name (unique within a toolchain's examples).
"""

from __future__ import annotations

import datetime as _dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import knowledge  # noqa: E402

MIN_SUCCESS_RATE = 0.3  # examples below this are excluded from few-shot

MIN_TYPE_PATTERN_RATE = 0.3  # type patterns below this success rate are excluded from prompts


def _fn_key(example: dict) -> str:
    """Prefer stable pair IDs while preserving legacy function-name keys."""
    return example.get("example_id") or example.get("fn", "")


def record_success(
    data: dict,
    toolchain: str,
    example: dict,
    store: pathlib.Path = knowledge.STORE,
) -> None:
    """Increment success count for an example and recompute its rate."""
    eq = data.setdefault("example_quality", {})
    tc = eq.setdefault(toolchain, {})
    key = _fn_key(example)
    entry = tc.setdefault(key, {"success_count": 0, "failure_count": 0, "last_used": None})
    entry["success_count"] += 1
    entry["last_used"] = _dt.date.today().isoformat()
    knowledge.save(data, store)


def record_failure(
    data: dict,
    toolchain: str,
    example: dict,
    store: pathlib.Path = knowledge.STORE,
) -> None:
    """Increment failure count for an example and recompute its rate."""
    eq = data.setdefault("example_quality", {})
    tc = eq.setdefault(toolchain, {})
    key = _fn_key(example)
    entry = tc.setdefault(key, {"success_count": 0, "failure_count": 0, "last_used": None})
    entry["failure_count"] += 1
    entry["last_used"] = _dt.date.today().isoformat()
    knowledge.save(data, store)


def success_rate(entry: dict) -> float:
    """Compute success_rate from an entry dict."""
    s = entry.get("success_count", 0)
    f = entry.get("failure_count", 0)
    total = s + f
    if total == 0:
        return 1.0  # unused examples start with neutral/high rate
    return s / total


def get_weighted_examples(
    data: dict,
    toolchain: str,
    limit: int = 3,
    min_rate: float = MIN_SUCCESS_RATE,
) -> list[dict]:
    """Return up to `limit` examples sorted by success_rate desc, then recency.

    Filters out examples with success_rate < min_rate (unless they've never
    been used, which start at rate 1.0).
    """
    exs = data.get("examples", {}).get(toolchain, [])
    eq = data.get("example_quality", {}).get(toolchain, {})

    scored = []
    for ex in exs:
        key = _fn_key(ex)
        entry = eq.get(key, {"success_count": 0, "failure_count": 0, "last_used": None})
        rate = success_rate(entry)
        used = entry.get("last_used") or "1970-01-01"
        if rate < min_rate and entry.get("success_count", 0) + entry.get("failure_count", 0) > 0:
            continue  # exclude low-quality, used examples
        scored.append((rate, used, ex))

    # Sort by rate desc, then by last_used asc (older first = less recently used)
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [ex for _, _, ex in scored[:limit]]


def _type_pattern_fn_key(pattern_name: str) -> str:
    """Get key for type pattern tracking."""
    return pattern_name


def record_type_pattern_success(
    data: dict,
    toolchain: str,
    pattern_name: str,
    store: pathlib.Path = knowledge.STORE,
) -> None:
    """Increment success count for a type pattern and recompute its rate."""
    eq = data.setdefault("type_pattern_quality", {})
    tc = eq.setdefault(toolchain, {})
    key = _type_pattern_fn_key(pattern_name)
    entry = tc.setdefault(key, {"success_count": 0, "failure_count": 0, "last_used": None})
    entry["success_count"] += 1
    entry["last_used"] = _dt.date.today().isoformat()
    knowledge.save(data, store)


def record_type_pattern_failure(
    data: dict,
    toolchain: str,
    pattern_name: str,
    store: pathlib.Path = knowledge.STORE,
) -> None:
    """Increment failure count for a type pattern and recompute its rate."""
    eq = data.setdefault("type_pattern_quality", {})
    tc = eq.setdefault(toolchain, {})
    key = _type_pattern_fn_key(pattern_name)
    entry = tc.setdefault(key, {"success_count": 0, "failure_count": 0, "last_used": None})
    entry["failure_count"] += 1
    entry["last_used"] = _dt.date.today().isoformat()
    knowledge.save(data, store)


def type_pattern_success_rate(entry: dict) -> float:
    """Compute success rate from a type pattern entry dict."""
    s = entry.get("success_count", 0)
    f = entry.get("failure_count", 0)
    total = s + f
    if total == 0:
        return 1.0  # unused patterns start with neutral/high rate
    return s / total


def get_weighted_type_patterns(
    data: dict,
    toolchain: str,
    limit: int = 3,
    min_rate: float = MIN_TYPE_PATTERN_RATE,
) -> list[tuple[str, dict]]:
    """Return up to `limit` type patterns sorted by success_rate desc.

    Filters out patterns with success_rate < min_rate (unless they've never
    been used, which start at rate 1.0).
    Returns list of (pattern_name, entry_dict) tuples.
    """
    eq = data.get("type_pattern_quality", {}).get(toolchain, {})
    scored = []
    for pattern_name, entry in eq.items():
        rate = type_pattern_success_rate(entry)
        used = entry.get("last_used") or "1970-01-01"
        if rate < min_rate and entry.get("success_count", 0) + entry.get("failure_count", 0) > 0:
            continue  # exclude low-quality, used patterns
        scored.append((rate, used, pattern_name, entry))

    # Sort by rate desc, then by last_used asc (older first = less recently used)
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [(pattern_name, entry) for _, _, pattern_name, entry in scored[:limit]]


def get_all_type_patterns(
    data: dict,
    toolchain: str,
) -> dict[str, dict]:
    """Return all type patterns for a toolchain."""
    eq = data.get("type_pattern_quality", {}).get(toolchain, {})
    return eq