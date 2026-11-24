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
import hashlib
import json
import pathlib
import re

STORE = pathlib.Path("knowledge/knowledge.json")
SCHEMA_VERSION = 2


def _yaml_value(path: pathlib.Path, key: str, default: str = "unknown") -> str:
    if not path.exists():
        return default
    for line2 in path.read_text(errors="replace").splitlines():
        if line2.startswith(key + ":"):
            return line2.split(":", 1)[1].strip() or default
    return default


# examples with success_rate below this are excluded from few-shot prompts
MIN_EXAMPLE_SUCCESS_RATE = 0.3


def _empty() -> dict:
    return {"version": SCHEMA_VERSION, "updated": None,
            "targets": {}, "compilers": {}, "examples": {},
            "verified_pascal_examples": {}}


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
    data.setdefault("example_quality", {})
    data.setdefault("verified_pascal_examples", {})
    data["version"] = SCHEMA_VERSION
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


def _fn_key(example: dict) -> str:
    return example.get("example_id") or (
        f"{example.get('target')}:{example.get('fn')}"
        if example.get("target") else example.get("fn", "")
    )


def examples_for(data: dict, compiler: str, platform: str, limit: int = 3,
                 min_confidence: str = "low",
                 min_success_rate: float = MIN_EXAMPLE_SUCCESS_RATE) -> list[dict]:
    """Return up to `limit` quality-weighted few-shot examples for this toolchain.

    Gated by the toolchain's detection confidence. Examples are sorted by
    success_rate desc (highest first), then by recency (least recently used
    first). Examples with success_rate < min_success_rate are excluded unless
    they've never been used (start at rate 1.0).
    """
    from example_quality import get_weighted_examples  # noqa: E402
    key = compiler_key(compiler, platform)
    recipe = data.get("compilers", {}).get(key, {})
    if not confidence_ok(recipe, min_confidence):
        return []
    return get_weighted_examples(data, key, limit=limit,
                                 min_rate=min_success_rate)


def prior_targets_with(data: dict, compiler: str, platform: str) -> list[str]:
    """Names of targets previously done with the same toolchain (transfer signal)."""
    key = compiler_key(compiler, platform)
    return list(data.get("compilers", {}).get(key, {}).get("targets", []))


# --- example quality tracking ---

def record_example_success(data: dict, toolchain: str, example: dict,
                           store: pathlib.Path = STORE) -> None:
    """Increment success count for a few-shot example."""
    from example_quality import record_success  # noqa: E402
    record_success(data, toolchain, example, store)


def record_example_failure(data: dict, toolchain: str, example: dict,
                           store: pathlib.Path = STORE) -> None:
    """Increment failure count for a few-shot example."""
    from example_quality import record_failure  # noqa: E402
    record_failure(data, toolchain, example, store)


# --- failure catalogue ---

def record_failure(data: dict, toolchain: str, category: str, asm_snippet: str,
                   fn: str, target: str,
                   store: pathlib.Path = STORE) -> None:
    """Append a failure to the per-toolchain failures catalogue."""
    from failure_analyzer import record_failure as _rf  # noqa: E402
    _rf(data, toolchain, category, asm_snippet, fn, target, store)
    save(data, store)


def get_anti_patterns(data: dict, toolchain: str, limit: int = 8) -> list[dict]:
    """Return the most common failure categories as anti-patterns."""
    from failure_analyzer import get_anti_patterns as _gap  # noqa: E402
    return _gap(data, toolchain, limit)


# --- auto-promotion: add a newly-verified function as a few-shot example ---

def promote_verified_example(data: dict, toolchain: str, example: dict,
                             store: pathlib.Path = STORE,
                             max_examples: int = 50) -> None:
    """Add a verified (asm -> pascal) pair as a new few-shot example.

    Capped at max_examples per toolchain to keep the store bounded.
    """
    exs = data.setdefault("examples", {}).setdefault(toolchain, [])
    key = _fn_key(example)
    if any(_fn_key(e) == key for e in exs):
        return
    exs.append(dict(example))
    if len(exs) > max_examples:
        eq = data.get("example_quality", {}).get(toolchain, {})
        scored = []
        for e in exs:
            ek = _fn_key(e)
            ent = eq.get(ek, {"success_count": 0, "failure_count": 0, "last_used": None})
            s = ent.get("success_count", 0)
            f = ent.get("failure_count", 0)
            rate = s / max(1, s + f)
            used = ent.get("last_used") or "1970-01-01"
            scored.append((rate, used, e))
        scored.sort(key=lambda t: (t[0], t[1]))  # worst rate + oldest first
        data["examples"][toolchain] = [e for _, _, e in scored[:max_examples]]
    save(data, store)


def _pascal_anchors(asm_text: str) -> set[str]:
    """Extract stable instruction, branch, call, and constant anchors."""
    mnemonics = re.findall(
        r"(?m)^\s*[0-9a-fA-F:]+\s+([A-Za-z][A-Za-z0-9.]*)", asm_text
    )
    constants = re.findall(r"\b(?:0x[0-9a-fA-F]+|[0-9a-fA-F]+:[0-9a-fA-F]+)\b",
                           asm_text.lower())
    return {f"m:{token.lower()}" for token in mnemonics} | {
        f"c:{token}" for token in constants
    }


def _example_quality(data: dict, toolchain: str, example: dict) -> float:
    from example_quality import success_rate  # noqa: E402

    entry = data.get("example_quality", {}).get(toolchain, {}).get(
        _fn_key(example), {}
    )
    return success_rate(entry)


def promote_verified_pascal_example(
    data: dict,
    toolchain: str,
    example: dict,
    store: pathlib.Path = STORE,
) -> str:
    """Store a Pascal function pair only when its matching oracle passed."""
    required = ("fn", "target", "compiler", "platform", "oracle", "asm", "pascal")
    missing = [field for field in required if not str(example.get(field, "")).strip()]
    if missing:
        raise ValueError(f"verified Pascal example missing: {', '.join(missing)}")
    if example.get("verification_status") != "verified":
        raise ValueError("Pascal examples require function-level oracle verification")
    if example.get("language", "").lower() != "pascal":
        raise ValueError("only Pascal outputs can enter the Pascal training corpus")

    pascal = example["pascal"].strip()
    if not re.search(r"(?im)^\s*(procedure|function)\s+[A-Za-z_]\w*", pascal):
        raise ValueError("verified Pascal example has no routine declaration")
    if re.search(r"\bTODO\b|UNMATCHED", pascal, re.IGNORECASE):
        raise ValueError("placeholder Pascal routines cannot enter the corpus")

    digest_input = "\0".join(
        (toolchain, example["target"], example["fn"], example["asm"], pascal)
    )
    example_id = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()
    record = {
        "example_id": example_id,
        "fn": example["fn"],
        "target": example["target"],
        "compiler": example["compiler"],
        "platform": example["platform"],
        "language": "pascal",
        "calling_convention": example.get("calling_convention"),
        "asm": example["asm"],
        "decomp_c": example.get("decomp_c", ""),
        "pascal": pascal,
        "verification_status": "verified",
        "oracle": example["oracle"],
        "verified_at": _dt.date.today().isoformat(),
    }
    examples = data.setdefault("verified_pascal_examples", {}).setdefault(
        toolchain, []
    )
    if not any(item.get("example_id") == example_id for item in examples):
        examples.append(record)
    save(data, store)
    return example_id


def prune_stale_verified_examples(
    data: dict,
    target: str,
    store: pathlib.Path = STORE,
) -> list[str]:
    verified: set[str] = set()
    for names in data.get("targets", {}).get(target, {}).get("verified", {}).values():
        verified.update(names)
    removed: list[str] = []
    for key, examples in data.get("verified_pascal_examples", {}).items():
        kept = []
        for example in examples:
            if example.get("target") == target and example.get("fn") not in verified:
                removed.append(f"{key}:{example.get('fn')}")
                continue
            kept.append(example)
        data["verified_pascal_examples"][key] = kept
    if removed:
        save(data, store)
    return removed


def verified_pascal_examples_for(
    data: dict,
    compiler: str,
    platform: str,
    query_asm: str,
    exclude_target: str | None = None,
    calling_convention: str | None = None,
    limit: int = 3,
    min_success_rate: float = MIN_EXAMPLE_SUCCESS_RATE,
) -> list[dict]:
    """Retrieve verified same-toolchain Pascal pairs by structural anchors."""
    key = compiler_key(compiler, platform)
    query_anchors = _pascal_anchors(query_asm)
    candidates = []
    for example in data.get("verified_pascal_examples", {}).get(key, []):
        if example.get("verification_status") != "verified":
            continue
        if example.get("language") != "pascal" or not example.get("oracle"):
            continue
        if exclude_target and example.get("target") == exclude_target:
            continue
        quality = _example_quality(data, key, example)
        if quality < min_success_rate:
            continue
        anchors = _pascal_anchors(example.get("asm", ""))
        union = query_anchors | anchors
        overlap = len(query_anchors & anchors) / len(union) if union else 0.0
        convention_match = bool(
            calling_convention
            and example.get("calling_convention") == calling_convention
        )
        score = overlap + (0.25 if convention_match else 0.0) + quality * 0.1
        candidates.append((score, quality, example.get("verified_at", ""), example))

    candidates.sort(key=lambda item: (-item[0], -item[1], item[2]))
    return [item[3] for item in candidates[:limit]]


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

    # --- NEW: Compute and store coverage ---
    total_funcs = data.get("targets", {}).get(target, {}).get("_total_functions", 0)
    if total_funcs == 0:
        # Try to compute from functions.json
        funcs_path = pathlib.Path(f"targets/{target}/functions.json")
        if funcs_path.exists():
            import json as _json
            funcs = _json.loads(funcs_path.read_text(errors="replace")).get("functions", [])
            total_funcs = len(funcs)
            data["targets"][target]["_total_functions"] = total_funcs

    if total_funcs > 0:
        coverage = len(t["verified"].get(oracle, [])) / total_funcs
        t["coverage"] = round(coverage, 4)
        t["coverage_oracle"] = oracle

    # --- NEW: Record verified Pascal examples ---
    _record_verified_pascal_examples(data, target, passed, oracle)

    save(data, store)



def stats(data: dict) -> dict:
    comps = data.get("compilers", {})
    eq_total = 0
    for tc_eq in data.get("example_quality", {}).values():
        for ent in tc_eq.values():
            eq_total += ent.get("success_count", 0) + ent.get("failure_count", 0)
    failure_total = 0
    for tc in comps.values():
        for cat in tc.get("failures", {}).values():
            failure_total += cat.get("count", 0)

    # Compute coverage summary
    targets_seen = len(data.get("targets", {}))
    total_verified = 0
    total_functions = 0
    coverage_by_target = {}

    for target, tdata in data.get("targets", {}).items():
        verified_count = len(tdata.get("verified", {}).get("dat-parity", []))
        # Try to get total functions
        funcs_path = pathlib.Path(f"targets/{target}/functions.json")
        if funcs_path.exists():
            import json as _json
            funcs = _json.loads(funcs_path.read_text(errors="replace")).get("functions", [])
            fn_count = len(funcs)
        else:
            fn_count = 0
        total_functions += fn_count
        total_verified += verified_count
        coverage = verified_count / fn_count if fn_count > 0 else 0
        coverage_by_target[target] = {
            "verified": verified_count,
            "total": fn_count,
            "coverage_pct": round(coverage * 100, 1)
        }

    return {
        "targets_seen": targets_seen,
        "toolchains_seen": len(comps),
        "examples_total": sum(len(v) for v in data.get("examples", {}).values()),
        "example_quality_entries": eq_total,
        "failure_catalogue_entries": failure_total,
        "most_experienced": sorted(
            comps.items(), key=lambda kv: -len(kv[1].get("targets", [])))[:3],
        "coverage_summary": {
            "total_verified": total_verified,
            "total_functions": total_functions,
            "overall_coverage_pct": round(total_verified / total_functions * 100, 1) if total_functions > 0 else 0,
            "coverage_by_target": coverage_by_target,
        }
    }


def _record_verified_pascal_examples(data: dict, target: str, passed: list[str],
                                     oracle: str) -> None:
    """Record verified Pascal examples for passed functions.

    Reads the Pascal and ASM files for each passed function and records
    them in the verified_pascal_examples section of the knowledge base.
    """
    import json as _json
    t = data["targets"].get(target, {})
    passed_set = set(passed)

    # Get compiler/platform info for this target
    config_dir = pathlib.Path(f"targets/{target}/config")
    toolchain = {
        "compiler": _yaml_value(config_dir / "toolchain.yaml", "compiler", ""),
        "platform": _yaml_value(config_dir / "toolchain.yaml", "platform", ""),
    }

    for fn in passed_set:
        # Read the Pascal file if it exists
        pascal_file = pathlib.Path(f"targets/{target}/src/{fn}.inc")
        if pascal_file.is_file():
            pascal_body = pascal_file.read_text(errors="replace")
            # Read asm file for anchors
            asm_file = pathlib.Path(f"targets/{target}/asm/{fn}.s")
            asm_body = ""
            if asm_file.is_file():
                asm_body = asm_file.read_text(errors="replace")

            # Generate example_id
            digest_input = "\0".join(
                (toolchain["compiler"], target, fn, asm_body, pascal_body)
            )
            example_id = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()

            # Check if example already exists
            examples = data.setdefault("verified_pascal_examples", {}).setdefault(
                compiler_key(toolchain["compiler"], toolchain["platform"]), []
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
                    "verified_at": _dt.date.today().isoformat(),
                }
                examples.append(record)

            # Update example quality
            key = compiler_key(toolchain["compiler"], toolchain["platform"])
            if key not in data.setdefault("compilers", {}):
                data.setdefault("compilers", {})[key] = {}
            if fn not in data["compilers"][key].setdefault("targets", []):
                data["compilers"][key].setdefault("targets", []).append(fn)
