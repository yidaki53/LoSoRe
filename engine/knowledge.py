"""Persistent cross-target knowledge store — the "learning" component.

As each target is ingested/verified, engine/learn.py mines it and records:
  * a per-(compiler, platform) *recipe*: language, image base, calling
    conventions, and the most common instruction *idioms* / prologues;
  * *few-shot examples*: (asm head -> decompiled C) pairs for functions that
    passed an oracle, keyed by compiler so the NEXT target with the same
    toolchain inherits them.

engine/draft.py consumes examples[compiler] to seed LLM prompts (few-shot) and
to bias template selection. Over time the factory gets better at a given
compiler because it accumulates verified translations rather than starting cold.

Store path: knowledge/knowledge.json (committed — own derived data, not vendor).
"""
from __future__ import annotations
import datetime as _dt
import json
import pathlib

STORE = pathlib.Path("knowledge/knowledge.json")
SCHEMA_VERSION = 1


def _empty() -> dict:
    return {"version": SCHEMA_VERSION, "updated": None,
            "targets": {}, "compilers": {}, "examples": {}}


def load(store: pathlib.Path = STORE) -> dict:
    if not store.exists():
        return _empty()
    try:
        data = json.loads(store.read_text())
    except Exception:
        return _empty()
    data.setdefault("version", SCHEMA_VERSION)
    data.setdefault("targets", {})
    data.setdefault("compilers", {})
    data.setdefault("examples", {})
    return data


def save(data: dict, store: pathlib.Path = STORE) -> None:
    data["updated"] = _dt.date.today().isoformat()
    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


# --- queries used by draft.py ---

def compiler_key(compiler: str, platform: str) -> str:
    comp = (compiler or "unknown").strip().lower()
    plat = (platform or "unknown").strip().lower()
    return comp if comp not in ("", "unknown", "todo") else f"unknown@{plat}"


def recipe_for(data: dict, compiler: str, platform: str) -> dict:
    return data.get("compilers", {}).get(compiler_key(compiler, platform), {})


_CONF_RANK = {"low": 0, "medium": 1, "high": 2}


def confidence_ok(recipe: dict, min_conf: str = "medium") -> bool:
    """True if a toolchain's recorded detection confidence meets the floor."""
    conf = recipe.get("compiler_confidence", "low")
    return _CONF_RANK.get(conf, 0) >= _CONF_RANK.get(min_conf, 1)


def examples_for(data: dict, compiler: str, platform: str, limit: int = 3,
                 min_confidence: str = "low") -> list[dict]:
    """Return up to `limit` verified few-shot examples for this toolchain.

    Gated by the toolchain's detection confidence: low-confidence toolchains do
    not leak examples into other targets until confirmed.
    """
    key = compiler_key(compiler, platform)
    recipe = data.get("compilers", {}).get(key, {})
    if not confidence_ok(recipe, min_confidence):
        return []
    exs = data.get("examples", {}).get(key, [])
    return exs[:limit]


def prior_targets_with(data: dict, compiler: str, platform: str) -> list[str]:
    """Names of targets previously done with the same toolchain (transfer signal)."""
    key = compiler_key(compiler, platform)
    return list(data.get("compilers", {}).get(key, {}).get("targets", []))


def record_verified(data: dict, target: str, passed: list[str],
                    oracle: str, store: pathlib.Path = STORE) -> None:
    """Record which functions passed an oracle (closes the learn loop).

    verify.py calls this after a diff run; the counts feed the per-target record
    and let report.py show real (oracle-backed) progress, not just fn totals.
    """
    t = data.setdefault("targets", {}).setdefault(target, {})
    t.setdefault("verified", {})
    t["verified"][oracle] = sorted(set(passed))
    t["num_verified"] = len(t["verified"].get(oracle, []))
    save(data, store)



def stats(data: dict) -> dict:
    comps = data.get("compilers", {})
    return {
        "targets_seen": len(data.get("targets", {})),
        "toolchains_seen": len(comps),
        "examples_total": sum(len(v) for v in data.get("examples", {}).values()),
        "most_experienced": sorted(
            comps.items(), key=lambda kv: -len(kv[1].get("targets", [])))[:3],
    }
