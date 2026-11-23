"""Bounded self-bootstrapping from frozen representations to oracle-verified data."""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

from engine import (
    draft,
    frozen_source_eval,
    knowledge,
    oracle_gate,
    rtl_template,
)
from engine.local_trial_inference import TrialInference, save
from tools import liero_four_routine_pilot as pilot
from tools import liero_source_trial as trial

BASE = pathlib.Path(__file__).resolve().parent.parent
ENDPOINT = "http://127.0.0.1:11434"
ORACLE = "routine-trace-parity"
PROMOTING_ORACLES = {ORACLE}
SOURCE_FILES = (
    "engine/bootstrap.py",
    "engine/draft.py",
    "engine/frozen_source_eval.py",
    "engine/knowledge.py",
    "engine/local_trial_inference.py",
    "engine/rl_engine.py",
    "engine/rtl_template.py",
    "tools/liero_four_routine_pilot.py",
    "tools/liero_source_trial.py",
)
CLASSIFICATION_BUDGET = {
    "max_tokens": 64,
    "context_tokens": 8192,
    "timeout_seconds": 600,
    "reasoning": "off",
}
NORMALIZE_BUDGET = {
    "max_tokens": 1024,
    "context_tokens": 8192,
    "timeout_seconds": 600,
    "reasoning": "off",
}


def _slug(model: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in model)


def _yaml_value(path: pathlib.Path, key: str, default: str = "unknown") -> str:
    if not path.is_file():
        return default
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip() or default
    return default


def _toolchain_key(root: pathlib.Path, target: str) -> str:
    path = root / "targets" / target / "config" / "toolchain.yaml"
    return knowledge.compiler_key(
        _yaml_value(path, "compiler"), _yaml_value(path, "platform")
    )


def verified_context(root: pathlib.Path, target: str, routine: str, limit: int = 2) -> str:
    store = root / "knowledge" / "knowledge.json"
    data = knowledge.load(store)
    key = _toolchain_key(root, target)
    examples = [
        item for item in data.get("verified_pascal_examples", {}).get(key, [])
        if item.get("target") == target
        and item.get("fn") != routine
        and item.get("verification_status") == "verified"
    ]
    examples.sort(key=lambda item: (item.get("verified_at", ""), item.get("fn", "")))
    if not examples:
        return ""
    parts = [
        "\nPreviously oracle-verified routines in this target are constraints only; "
        "answer the classification question with one identifier.\n"
    ]
    for item in examples[-limit:]:
        parts.append(
            f"--- {item.get('fn')} verified by {item.get('oracle')} ---\n"
            f"ASM:\n{item.get('asm', '')[:400]}\n"
            f"PASCAL:\n{item.get('pascal', '')[:600]}\n"
        )
    return "".join(parts)


def _declaration(root: pathlib.Path, routine: str) -> str:
    fallback = draft._decl_for(root, routine, None, set())
    return rtl_template.declaration_for(root, routine, fallback)


def _packed_declaration(root: pathlib.Path, routine: str) -> str:
    return trial.routine_spec(routine)["signature"]


def _byte_backed_declaration(root: pathlib.Path, routine: str) -> str:
    try:
        return trial.routine_spec(routine)["signature"]
    except KeyError:
        return _declaration(root, routine)


METHODS: dict[str, dict[str, Any]] = {
    "bootstrap-move-v1": {
        "routine": None,
        "budget": dict(CLASSIFICATION_BUDGET),
        "response_format": "raw-source",
        "build_prompt": lambda root, routine, context: (
            rtl_template.build_prompt(root, routine) + context
        ),
        "classify": rtl_template.classify,
        "renderer": rtl_template.render_bridge,
        "declaration": _declaration,
    },
    "bootstrap-move-forward-v1": {
        "routine": None,
        "budget": dict(CLASSIFICATION_BUDGET),
        "response_format": "raw-source",
        "build_prompt": lambda root, routine, context: (
            rtl_template.build_prompt(root, routine) + context
        ),
        "classify": rtl_template.classify,
        "renderer": rtl_template.render_move_forward_v1,
        "declaration": _byte_backed_declaration,
    },
    "bootstrap-move-forward-v2": {
        "routine": None,
        "budget": dict(CLASSIFICATION_BUDGET),
        "response_format": "raw-source",
        "build_prompt": lambda root, routine, context: (
            rtl_template.build_prompt(root, routine) + context
        ),
        "classify": rtl_template.classify,
        "renderer": rtl_template.render_move_forward_v2,
        "declaration": _byte_backed_declaration,
    },
    "bootstrap-packed-v1": {
        "routine": "FUN_24dd_4141",
        "budget": dict(CLASSIFICATION_BUDGET),
        "response_format": "raw-source",
        "build_prompt": lambda root, routine, context: (
            rtl_template.build_packed_prompt(root, routine) + context
        ),
        "classify": rtl_template.classify_packed,
        "renderer": rtl_template.render_packed,
        "declaration": _packed_declaration,
    },
    "bootstrap-normalize-v1": {
        "routine": "FUN_24dd_455e",
        "budget": dict(NORMALIZE_BUDGET),
        "response_format": "raw-source",
        "build_prompt": lambda root, routine, context: (
            rtl_template.build_normalize_prompt(root, routine) + context
        ),
        "classify": rtl_template.classify_normalize,
        "renderer": rtl_template.render_normalize,
        "declaration": _byte_backed_declaration,
    },
    "bootstrap-normalize-v2": {
        "routine": "FUN_24dd_455e",
        "budget": dict(CLASSIFICATION_BUDGET),
        "response_format": "raw-source",
        "build_prompt": lambda root, routine, context: (
            rtl_template.build_normalize_label_prompt(root, routine) + context
        ),
        "classify": rtl_template.classify_normalize_label,
        "renderer": rtl_template.render_normalize_label,
        "declaration": _byte_backed_declaration,
    },
    "bootstrap-arithmetic-v1": {
        "routine": "FUN_249c_0013",
        "budget": dict(CLASSIFICATION_BUDGET),
        "response_format": "raw-source",
        "build_prompt": lambda root, routine, context: (
            rtl_template.build_arithmetic_label_prompt(root, routine) + context
        ),
        "classify": rtl_template.classify_arithmetic_label,
        "renderer": rtl_template.render_arithmetic_label,
        "declaration": _byte_backed_declaration,
    },
}


def source_hashes(root: pathlib.Path) -> dict[str, str]:
    hashes = {}
    for relpath in SOURCE_FILES:
        path = root / relpath
        if path.is_file():
            hashes[relpath] = pilot.digest(path)
    return hashes


def write_config(
    path: pathlib.Path,
    method: str,
    model: str,
    identity: dict | None = None,
    verify: bool = True,
) -> TrialInference:
    config = {
        "backend": "ollama",
        "endpoint": ENDPOINT,
        "model": model,
        "identity": identity or pilot.leaf_model_identity(model, ENDPOINT),
        "max_tokens": METHODS[method]["budget"]["max_tokens"],
        "context_tokens": METHODS[method]["budget"]["context_tokens"],
        "timeout_seconds": METHODS[method]["budget"]["timeout_seconds"],
        "reasoning": METHODS[method]["budget"]["reasoning"],
        "response_format": METHODS[method]["response_format"],
        "generation_budget_file": None,
    }
    save(path, config)
    inference = TrialInference.from_file(path)
    if verify and inference.identity() != config["identity"]:
        raise ValueError(f"model identity changed before bootstrap: {model}")
    return inference


def _suite_passed(result: dict, suite: str) -> bool:
    record = result.get("suites", {}).get(suite, {})
    return bool(
        result.get("compile", {}).get("status") == "passed"
        and record.get("original", {}).get("status") == "passed"
        and record.get("candidate", {}).get("status") == "passed"
    )


def _append_unique(items: list[str], values: list[str]) -> None:
    for value in values:
        if value not in items:
            items.append(value)


def _promote(
    root: pathlib.Path,
    target: str,
    routine: str,
    method: str,
    source_path: pathlib.Path,
    eval_dir: pathlib.Path,
    archive: str,
) -> dict:
    gate = {
        "oracle": ORACLE,
        "status": "verified",
        "promotion_eligible": True,
        "reason": "training and terminal routine parity passed",
    }
    return oracle_gate.promote(
        root, target, routine, method, source_path, eval_dir, archive,
        oracle=ORACLE, gate=gate, action=method,
    )


def _run_method(
    root: pathlib.Path,
    output: pathlib.Path,
    target: str,
    routine: str,
    method: str,
    model: str,
    context: str,
    identity: dict | None,
    inference_factory: Any,
) -> dict:
    spec = METHODS[method]
    directory = output / method / _slug(model)
    directory.mkdir(parents=True, exist_ok=False)
    prompt = spec["build_prompt"](root, routine, context)
    prompt_path = directory / "prompt.txt"
    prompt_path.write_text(prompt)
    prompt_sha256 = pilot.digest(prompt_path)
    context_sha256 = hashlib.sha256(context.encode()).hexdigest()
    arm: dict[str, Any] = {
        "method": method,
        "model": model,
        "target": target,
        "routine": routine,
        "status": "pending",
        "prompt_sha256": prompt_sha256,
        "verified_context_sha256": context_sha256,
        "no_terminal_feedback_reuse": True,
    }
    pilot.save(directory / "arm.json", arm)
    try:
        config_path = directory / "inference.json"
        configured = write_config(
            config_path, method, model, identity=identity,
            verify=identity is None,
        )
        inference = inference_factory(config_path) if inference_factory else configured
        freeze = {
            "target": target,
            "routine": routine,
            "method": method,
            "model": model,
            "identity": configured.config["identity"],
            "prompt_sha256": prompt_sha256,
            "verified_context_sha256": context_sha256,
            "source_hashes": source_hashes(root),
            "budget": spec["budget"],
            "response_format": spec["response_format"],
            "oracle": ORACLE,
            "policy": "one request, compile gate, training-only selection, terminal once after training",
        }
        pilot.save(directory / "freeze.json", freeze)
        arm.update({
            "identity": configured.config["identity"],
            "config_sha256": configured.config_sha256,
            "source_hashes": freeze["source_hashes"],
        })
        request_dir = directory / "request-1"
        response = inference.request(prompt, request_dir)
        proposal = json.loads(json.loads(response)["response"])
        classification = spec["classify"](proposal["source"])
        arm["classification"] = classification
        source = spec["renderer"](
            routine, spec["declaration"](root, routine), classification
        )
        if source is None:
            arm.update(status="unsupported", error="unsupported classification")
            pilot.save(directory / "arm.json", arm)
            return arm
        rendered = directory / "rendered_source.inc"
        rendered.write_text(source)
        candidate = pilot.candidate_source(
            {"response": json.dumps({"source": source})}, routine
        )
        compile_result = trial.compile_candidate(
            root, directory / "compile", routine, candidate
        )
        arm.update({
            "compile": compile_result,
            "compile_status": compile_result["status"],
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "status": "valid-source" if compile_result["status"] == "passed" else "compile-failed",
        })
    except Exception as error:
        arm.update(status="failed", error=f"{type(error).__name__}: {error}")
    metadata_path = directory / "request-1" / "metadata.json"
    metadata = json.loads(metadata_path.read_text()) if metadata_path.is_file() else {}
    arm.update({
        "request_sha256": metadata.get("request_sha256"),
        "response_sha256": metadata.get("response_sha256"),
        "response_format": metadata.get("response_format", spec["response_format"]),
    })
    pilot.save(directory / "arm.json", arm)
    return arm


def run_bootstrap(
    root: pathlib.Path,
    target: str,
    routine: str,
    output: pathlib.Path,
    methods: list[str] | None = None,
    models: list[str] | None = None,
    oracle: str = ORACLE,
    identity: dict | None = None,
    inference_factory: Any = None,
) -> dict:
    if oracle not in PROMOTING_ORACLES:
        raise ValueError(f"bootstrap requires a promoting oracle, got {oracle}")
    root = pathlib.Path(root)
    output = pathlib.Path(output)
    if not output.is_absolute():
        output = root / output
    output.mkdir(parents=True, exist_ok=False)
    selected = list(methods or METHODS)
    unknown = set(selected) - set(METHODS)
    if unknown:
        raise ValueError(f"unknown bootstrap methods: {', '.join(sorted(unknown))}")
    model_names = list(models or ["qwen2.5-coder:1.5b"])
    context = verified_context(root, target, routine)
    result: dict[str, Any] = {
        "target": target,
        "routine": routine,
        "oracle": oracle,
        "output": str(output),
        "methods": [],
        "promotions": [],
        "status": "pending",
        "policy": "training-only selection; terminal once per training pass; no feedback reuse",
    }
    pilot.save(output / "result.json", result)
    for method in selected:
        spec = METHODS[method]
        if spec["routine"] and spec["routine"] != routine:
            result["methods"].append({
                "method": method, "status": "not-applicable",
                "routine": spec["routine"],
            })
            pilot.save(output / "result.json", result)
            continue
        for model in model_names:
            arm = _run_method(
                root, output, target, routine, method, model, context,
                identity, inference_factory or TrialInference.from_file,
            )
            if arm["status"] == "valid-source":
                source_path = output / method / _slug(model) / "rendered_source.inc"
                training = frozen_source_eval.run_training(
                    root, output / method / _slug(model) / "training",
                    source_path, routine,
                )
                arm["training"] = {
                    "compile": training["compile"],
                    "suites": training["suites"],
                    "passed": _suite_passed(training, "training"),
                }
                if arm["training"]["passed"]:
                    terminal = frozen_source_eval.run(
                        root, output / method / _slug(model) / "terminal",
                        source_path, routine,
                    )
                    arm["terminal"] = {
                        "compile": terminal["compile"],
                        "suites": terminal["suites"],
                        "passed": _suite_passed(terminal, "terminal"),
                    }
                    if arm["terminal"]["passed"]:
                        promotion = _promote(
                            root, target, routine, method, source_path,
                            output / method / _slug(model) / "terminal",
                            str(output / method / _slug(model) / "arm.json"),
                        )
                        arm["promotion"] = promotion
                        result["promotions"].append(promotion)
            result["methods"].append(arm)
            pilot.save(output / "result.json", result)
    attempts = len([item for item in result["methods"] if item.get("status") != "not-applicable"])
    successes = len([
        item for item in result["promotions"] if item.get("status") == "promoted"
    ])
    conflicts = len([
        item for item in result["promotions"] if item.get("status") == "promotion-conflict"
    ])
    result["attempts"] = attempts
    result["yield"] = round(successes / attempts, 4) if attempts else 0.0
    if successes:
        result["status"] = "verified"
    elif conflicts:
        result["status"] = "promotion-conflict"
    elif any(item.get("terminal", {}).get("passed") is False for item in result["methods"]):
        result["status"] = "terminal-failed"
    elif any(item.get("training", {}).get("passed") is False for item in result["methods"]):
        result["status"] = "blocked-no-training-pass"
    elif any(item.get("status") == "valid-source" for item in result["methods"]):
        result["status"] = "blocked-no-training-pass"
    else:
        result["status"] = "blocked-no-compiled-source"
    pilot.save(output / "result.json", result)
    return result
