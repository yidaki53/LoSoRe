"""Pinned local benchmark for Matrix leaf 48e1 across two Ollama models."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import draft, rtl_template
from engine.local_trial_inference import InferenceFailure, TrialInference, save
from tools import liero_four_routine_pilot as pilot
from tools import liero_source_trial as trial

ENDPOINT = "http://127.0.0.1:11434"
ROUTINE = "FUN_24dd_48e1"
PROFILE_ROUTINES = {
    "packed-copy-v1": "FUN_24dd_4141",
    "packed-copy-v2": "FUN_24dd_4141",
}
MODELS = (
    "losore-llm4decompile-22b-v2:Q4_K_M",
    "qwen2.5-coder:1.5b",
)
BUDGETS = {
    "source-json": {
        "max_tokens": 2048,
        "context_tokens": 8192,
        "timeout_seconds": 600,
        "reasoning": "off",
    },
    "raw-source": {
        "max_tokens": 4096,
        "context_tokens": 16384,
        "timeout_seconds": 600,
        "reasoning": "default",
    },
    "pascal-no-asm": {
        "max_tokens": 4096,
        "context_tokens": 16384,
        "timeout_seconds": 600,
        "reasoning": "default",
    },
    "rtl-template": {
        "max_tokens": 64,
        "context_tokens": 8192,
        "timeout_seconds": 600,
        "reasoning": "off",
    },
    "rtl-template-v2": {
        "max_tokens": 64,
        "context_tokens": 8192,
        "timeout_seconds": 600,
        "reasoning": "off",
    },
    "rtl-template-v3": {
        "max_tokens": 64,
        "context_tokens": 8192,
        "timeout_seconds": 600,
        "reasoning": "off",
    },
    "packed-copy-v1": {
        "max_tokens": 64,
        "context_tokens": 8192,
        "timeout_seconds": 600,
        "reasoning": "off",
    },
    "packed-copy-v2": {
        "max_tokens": 64,
        "context_tokens": 8192,
        "timeout_seconds": 600,
        "reasoning": "off",
    },
}
RESPONSE_FORMATS = {
    "source-json": "source-json",
    "raw-source": "raw-source",
    "pascal-no-asm": "raw-source",
    "rtl-template": "raw-source",
    "rtl-template-v2": "raw-source",
    "rtl-template-v3": "raw-source",
    "packed-copy-v1": "raw-source",
    "packed-copy-v2": "raw-source",
}
REPRESENTATION_SOURCE_FILES = (
    "targets/liero/asm/FUN_24dd_48e1.s",
    "targets/liero/src/FUN_24dd_48e1.inc",
    "targets/liero/asm/FUN_24dd_4141.s",
    "targets/liero/src/FUN_24dd_4141.inc",
    "targets/liero/src/LieroRuntime.pas",
    "config/target.yaml",
    "config/toolchain.yaml",
    "engine/draft.py",
    "engine/local_trial_inference.py",
    "engine/rtl_template.py",
    "tools/benchmark_matrix_models.py",
)


def slug(model: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in model)


def profile_routine(profile: str) -> str:
    return PROFILE_ROUTINES.get(profile, ROUTINE)


def write_config(path: pathlib.Path, model: str, profile: str) -> TrialInference:
    config = {
        "backend": "ollama",
        "endpoint": ENDPOINT,
        "model": model,
        "identity": pilot.leaf_model_identity(model, ENDPOINT),
        "max_tokens": BUDGETS[profile]["max_tokens"],
        "context_tokens": BUDGETS[profile]["context_tokens"],
        "timeout_seconds": BUDGETS[profile]["timeout_seconds"],
        "reasoning": BUDGETS[profile]["reasoning"],
        "response_format": RESPONSE_FORMATS[profile],
        "generation_budget_file": None,
    }
    save(path, config)
    inference = TrialInference.from_file(path)
    if inference.identity() != config["identity"]:
        raise ValueError(f"model identity changed before benchmark: {model}")
    return inference


def summarize_arm(model: str, directory: pathlib.Path) -> dict:
    freeze = json.loads((directory / "freeze.json").read_text())
    result = json.loads((directory / "result.json").read_text())
    statuses: dict[str, int] = {}
    for record in result["routines"].values():
        for attempt in record["attempts"]:
            status = attempt.get("status", "unknown")
            statuses[status] = statuses.get(status, 0) + 1
    return {
        "model": model,
        "digest": freeze["model"]["digest"],
        "config_sha256": freeze["inference"]["config_sha256"],
        "prompt_sha256": freeze["prompt_hashes"][ROUTINE],
        "training_sha256": freeze["corpora"][ROUTINE]["training"],
        "terminal_sha256": freeze["corpora"][ROUTINE]["terminal"],
        "source_hashes": freeze["source_hashes"],
        "budgets": freeze["budgets"],
        "model_requests": result["model_requests"],
        "binary_terminal_passes": result["binary_terminal_passes"],
        "accepted_source_recoveries": result["accepted_source_recoveries"],
        "examples_promoted": result["examples_promoted"],
        "weights_changed": result["weights_changed"],
        "frontier_status": result["frontier_status"],
        "attempt_statuses": statuses,
    }


def build_prompt(profile: str) -> str:
    routine = profile_routine(profile)
    if profile == "source-json":
        return trial.trial_prompt(ROOT, ROUTINE, "", True)
    if profile.startswith("packed-copy"):
        return rtl_template.build_packed_prompt(ROOT, routine)
    if profile.startswith("rtl-template"):
        return rtl_template.build_prompt(ROOT, ROUTINE)
    asm = (ROOT / "targets/liero/asm" / f"{ROUTINE}.s").read_text(errors="replace")[:3000]
    seed = draft.read_decomp_seed(ROOT, ROUTINE)
    declaration = draft._decl_for(ROOT, ROUTINE, None, set())
    base = draft._build_pascal_prompt(
        ROOT, "liero", ROUTINE, asm, seed, "Ghidra", declaration, set()
    )
    suffix = (
        "\nReturn the complete include as plain Pascal text only. "
        "Do not emit JSON, markdown fences, explanations, or output-obligations metadata.\n"
    )
    if profile == "pascal-no-asm":
        suffix += (
            "Do not use inline assembly, `asm` blocks, `assembler`, or absolute "
            "memory/segment operations. Express the routine with ordinary Turbo "
            "Pascal statements and standard RTL calls only.\n"
        )
    return base + suffix


def representation_source_hashes() -> dict[str, str]:
    return {
        relpath: pilot.digest(ROOT / relpath)
        for relpath in REPRESENTATION_SOURCE_FILES
        if (ROOT / relpath).exists()
    }


def run_full(output: pathlib.Path, profile: str, models: tuple[str, ...]) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    arms = {}
    for model in models:
        directory = output / slug(model)
        directory.mkdir()
        inference = write_config(directory / "inference.json", model, profile)
        trial.run(
            ROOT,
            directory / "trial",
            model,
            ENDPOINT,
            routines=(ROUTINE,),
            enforce_outputs=True,
            inference=inference,
        )
        arms[model] = summarize_arm(model, directory / "trial")

    first = next(iter(arms.values()))
    comparison = {
        "routine": ROUTINE,
        "endpoint": ENDPOINT,
        "profile": profile,
        "models": list(models),
        "identical_prompt": all(
            arm["prompt_sha256"] == first["prompt_sha256"] for arm in arms.values()
        ),
        "identical_training_corpus": all(
            arm["training_sha256"] == first["training_sha256"]
            for arm in arms.values()
        ),
        "identical_terminal_corpus": all(
            arm["terminal_sha256"] == first["terminal_sha256"]
            for arm in arms.values()
        ),
        "identical_source_hashes": all(
            arm["source_hashes"] == first["source_hashes"] for arm in arms.values()
        ),
        "arms": arms,
    }
    if not all(
        comparison[key]
        for key in (
            "identical_prompt",
            "identical_training_corpus",
            "identical_terminal_corpus",
            "identical_source_hashes",
        )
    ):
        raise ValueError("benchmark arms are not frozen to identical inputs")
    save(output / "comparison.json", comparison)
    return comparison


def run_representation(
    output: pathlib.Path, profile: str, models: tuple[str, ...]
) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    routine = profile_routine(profile)
    prompt = build_prompt(profile)
    prompt_path = output / "prompt.txt"
    prompt_path.write_text(prompt)
    prompt_sha256 = pilot.digest(prompt_path)
    frozen_arms: dict[str, dict] = {}
    for model in models:
        directory = output / slug(model)
        directory.mkdir()
        inference = write_config(directory / "inference.json", model, profile)
        frozen_arms[model] = {
            "model": model,
            "digest": inference.config["identity"]["digest"],
            "config_sha256": inference.config_sha256,
            "config": inference.config,
        }
    freeze = {
        "routine": routine,
        "endpoint": ENDPOINT,
        "profile": profile,
        "representation_only": True,
        "no_oracle": True,
        "models": list(models),
        "prompt_sha256": prompt_sha256,
        "prompt_bytes": len(prompt.encode()),
        "source_hashes": representation_source_hashes(),
        "budgets": BUDGETS[profile],
        "arms": frozen_arms,
    }
    save(output / "freeze.json", freeze)

    arms: dict[str, dict] = {}
    if profile.startswith("packed-copy"):
        declaration = trial.routine_spec(routine)["signature"]
    else:
        declaration = rtl_template.declaration_for(
            ROOT, routine, draft._decl_for(ROOT, routine, None, set())
        )
    for model in models:
        directory = output / slug(model)
        inference = TrialInference.from_file(directory / "inference.json")
        status = "pending"
        error = None
        source_sha256 = None
        classification = None
        compile_status = None
        try:
            response = inference.request(prompt, directory / "inference-1")
            normalized = json.loads(response)
            proposal = json.loads(normalized["response"])
            if profile.startswith("rtl-template") or profile.startswith("packed-copy"):
                if profile.startswith("packed-copy"):
                    classification = rtl_template.classify_packed(proposal["source"])
                    renderer = rtl_template.render_packed
                else:
                    classification = rtl_template.classify(proposal["source"])
                    renderer = (
                        rtl_template.render_bridge
                        if profile == "rtl-template-v3"
                        else rtl_template.render
                    )
                source = renderer(routine, declaration, classification)
                if source is None:
                    raise ValueError("unsupported RTL classification")
                (directory / "rendered_source.inc").write_text(source)
                source = pilot.candidate_source(
                    {"response": json.dumps({"source": source})}, routine
                )
                compile_status = trial.compile_candidate(
                    ROOT, directory / "compile", routine, source
                )["status"]
                status = (
                    "valid-source" if compile_status == "passed" else "compile-failed"
                )
                if status == "compile-failed":
                    error = compile_status
            else:
                source = pilot.candidate_source(
                    {"response": json.dumps(proposal)}, routine
                )
                status = "valid-source"
            source_sha256 = hashlib.sha256(source.encode()).hexdigest()
        except InferenceFailure as failure:
            status = failure.kind
            error = str(failure)
        except (ValueError, KeyError, TypeError) as failure:
            status = "format"
            error = str(failure)
        metadata_path = directory / "inference-1/metadata.json"
        metadata = (
            json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
        )
        arms[model] = {
            "model": model,
            "digest": frozen_arms[model]["digest"],
            "config_sha256": frozen_arms[model]["config_sha256"],
            "status": status,
            "error": error,
            "source_sha256": source_sha256,
            "classification": classification,
            "compile_status": compile_status,
            "request_sha256": metadata.get("request_sha256"),
            "response_sha256": metadata.get("response_sha256"),
            "response_format": metadata.get("response_format", profile),
            "elapsed_seconds": metadata.get("elapsed_seconds"),
        }
    comparison = {
        "routine": routine,
        "endpoint": ENDPOINT,
        "profile": profile,
        "representation_only": True,
        "no_oracle": True,
        "models": list(models),
        "identical_prompt": True,
        "prompt_sha256": prompt_sha256,
        "source_hashes": freeze["source_hashes"],
        "budgets": BUDGETS[profile],
        "arms": arms,
    }
    save(output / "comparison.json", comparison)
    return comparison


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument(
        "--profile", choices=tuple(BUDGETS), default="source-json"
    )
    parser.add_argument("--representation-only", action="store_true")
    parser.add_argument("--models", nargs="+", default=list(MODELS))
    args = parser.parse_args()
    output = args.output.resolve()
    models = tuple(args.models)
    if args.representation_only:
        result = run_representation(output, args.profile, models)
    elif args.profile == "source-json":
        result = run_full(output, args.profile, models)
    else:
        parser.error("--profile raw-source requires --representation-only")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
