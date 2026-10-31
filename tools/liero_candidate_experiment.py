"""Run isolated, MLflow-tracked Pascal candidate sweeps for Liero."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_MODELS = (
    "qwen2.5-coder:14b-instruct-q4_K_M",
    "qwen3:14b",
)
DEFAULT_PROMPT_PROFILES = ("learned-context", "base-prompt")
DEFAULT_TEMPERATURES = (0.0, 0.3)
DEFAULT_FUNCTION = "FUN_24dd_0582"
DEFAULT_ENDPOINT = "http://localhost:11434"
DEFAULT_MAX_TOKENS = 768
DEFAULT_COMPILE_REPAIR_ROUNDS = 1
PROMPT_PROFILES = set(DEFAULT_PROMPT_PROFILES)
SCRATCH_IGNORE = shutil.ignore_patterns(
    "__pycache__", "*.pyc", "build", ".venv", ".git"
)


@dataclass(frozen=True)
class TrialSettings:
    model: str
    prompt_profile: str
    temperature: float
    max_tokens: int


def build_settings_matrix(
    models: list[str],
    prompt_profiles: list[str],
    temperatures: list[float],
    max_tokens: int,
) -> list[TrialSettings]:
    if max_tokens < 1:
        raise ValueError("max_tokens must be positive")
    if not models:
        raise ValueError("at least one model is required")
    if not prompt_profiles or set(prompt_profiles) - PROMPT_PROFILES:
        raise ValueError(
            f"prompt profiles must be selected from {sorted(PROMPT_PROFILES)}"
        )
    if not temperatures or any(not 0.0 <= value <= 2.0 for value in temperatures):
        raise ValueError("temperatures must be between 0.0 and 2.0")
    return [
        TrialSettings(model, profile, temperature, max_tokens)
        for model, profile, temperature in itertools.product(
            models, prompt_profiles, temperatures
        )
    ]


def _has_instructions(path: pathlib.Path) -> bool:
    return bool(re.search(
        r"(?m)^\s*[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}\s+[A-Za-z][A-Za-z0-9.]*\b",
        path.read_text(errors="replace"),
    ))


def select_function_panel(
    target_root: pathlib.Path,
    requested_function: str = DEFAULT_FUNCTION,
    panel_size: int = 4,
) -> list[str]:
    if panel_size < 2:
        raise ValueError("panel_size must be at least 2")
    requested_path = target_root / "asm" / f"{requested_function}.s"
    if not requested_path.is_file() or not _has_instructions(requested_path):
        raise ValueError(f"requested function has no usable assembly: {requested_path}")

    candidates = sorted(
        (path.stat().st_size, path.stem)
        for path in (target_root / "asm").glob("FUN_*.s")
        if path.stem != requested_function and _has_instructions(path)
    )
    needed = panel_size - 1
    if len(candidates) < needed:
        raise ValueError(
            f"requested {needed} additional routines but found {len(candidates)}"
        )
    if needed == 1:
        selected = [candidates[(len(candidates) - 1) // 2][1]]
    else:
        indexes = sorted({
            round(index * (len(candidates) - 1) / (needed - 1))
            for index in range(needed)
        })
        selected = [candidates[index][1] for index in indexes]
    return [requested_function, *selected]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hash_paths(root: pathlib.Path, paths: list[pathlib.Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def input_fingerprints(
    target_root: pathlib.Path, function_name: str
) -> dict[str, str | None]:
    assembly = target_root / "asm" / f"{function_name}.s"
    decomp = target_root / "decomp" / f"{function_name}.c"
    source = target_root / "src" / f"{function_name}.inc"
    input_files = [
        path
        for directory in ("asm", "decomp", "config", "src")
        for path in (target_root / directory).rglob("*")
        if path.is_file()
    ]
    input_files.extend(
        path for path in (target_root / "functions.json", target_root / "Makefile")
        if path.is_file()
    )
    return {
        "assembly_sha256": (
            _sha256(assembly.read_bytes()) if assembly.is_file() else None
        ),
        "decomp_sha256": _sha256(decomp.read_bytes()) if decomp.is_file() else None,
        "baseline_source_sha256": (
            _sha256(source.read_bytes()) if source.is_file() else None
        ),
        "target_input_sha256": _hash_paths(target_root, input_files),
    }


def rank_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            not row.get("accepted", False),
            row.get("candidate_build_passed") is not True,
            row.get("duration_seconds", float("inf")),
        ),
    )


def _local_api_root(endpoint: str) -> str:
    parsed = urllib.parse.urlparse(endpoint)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
        "localhost", "127.0.0.1", "::1",
    }:
        raise ValueError("candidate experiments only support a local Ollama endpoint")
    root = endpoint.rstrip("/")
    for suffix in ("/v1/chat/completions", "/chat/completions", "/v1", "/api"):
        if root.endswith(suffix):
            root = root[: -len(suffix)].rstrip("/")
    return root


def _ollama_model_digests(endpoint: str, models: list[str]) -> dict[str, str]:
    api_root = _local_api_root(endpoint)
    request = urllib.request.Request(f"{api_root}/api/tags")
    with urllib.request.urlopen(request, timeout=15) as response:
        entries = json.loads(response.read()).get("models", [])
    available = {
        item.get("name"): item.get("digest", "")
        for item in entries
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    missing = sorted(set(models) - available.keys())
    if missing:
        raise RuntimeError(f"local Ollama is missing requested models: {missing}")
    return {model: available[model] for model in models}


def _copy_scratch_repository(
    source_root: pathlib.Path,
    scratch_root: pathlib.Path,
    target: str,
) -> pathlib.Path:
    scratch_repo = scratch_root / "workspace"
    scratch_repo.mkdir(parents=True)
    for directory in ("engine", "tools", "compilers"):
        shutil.copytree(
            source_root / directory,
            scratch_repo / directory,
            ignore=SCRATCH_IGNORE,
        )
    target_parent = scratch_repo / "targets"
    target_parent.mkdir()
    shutil.copytree(
        source_root / "targets" / target,
        target_parent / target,
        ignore=SCRATCH_IGNORE,
    )
    knowledge_source = source_root / "knowledge" / "knowledge.json"
    if not knowledge_source.is_file():
        raise FileNotFoundError(f"knowledge store is missing: {knowledge_source}")
    knowledge_dir = scratch_repo / "knowledge"
    knowledge_dir.mkdir()
    shutil.copy2(knowledge_source, knowledge_dir / "knowledge.json")
    return scratch_repo


def _run_build(target_root: pathlib.Path) -> tuple[int, str, float]:
    started = time.monotonic()
    try:
        result = subprocess.run(
            ["make", "build"],
            cwd=target_root,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return 125, f"build command failed: {exc}", time.monotonic() - started
    return (
        result.returncode,
        result.stdout + result.stderr,
        time.monotonic() - started,
    )


def _create_trial_command(
    repo_root: pathlib.Path,
    target: str,
    function_name: str,
    settings: TrialSettings,
    endpoint: str,
    capture_dir: pathlib.Path,
    repair_note: str = "",
) -> list[str]:
    command = [
        str(pathlib.Path(sys.executable)),
        "engine/draft.py",
        "--target",
        target,
        "--fn",
        function_name,
        "--llm",
        "--model",
        settings.model,
        "--endpoint",
        endpoint,
        "--temperature",
        str(settings.temperature),
        "--max-tokens",
        str(settings.max_tokens),
        "--prompt-profile",
        settings.prompt_profile,
        "--capture-dir",
        str(capture_dir),
        "--retry-existing",
        "--skip-compile-gate",
        "--disable-adapter",
    ]
    if repair_note:
        command.extend(["--repair-note", repair_note])
    return command


def _load_capture(path: pathlib.Path, function_name: str) -> dict[str, Any]:
    metadata = path / function_name / "capture.json"
    if not metadata.is_file():
        return {
            "sanitizer_accepted": False,
            "rejection_reason": "generation-capture-missing",
        }
    try:
        return json.loads(metadata.read_text())
    except json.JSONDecodeError:
        return {
            "sanitizer_accepted": False,
            "rejection_reason": "generation-capture-invalid",
        }


def _log_trial(
    mlflow: Any,
    experiment_name: str,
    row: dict[str, Any],
    capture_dir: pathlib.Path,
    target_input_hash: str,
    model_digest: str,
) -> str:
    with mlflow.start_run(run_name=row["run_name"], experiment_id=experiment_name):
        settings = row["settings"]
        mlflow.log_params({
            "target": row["target"],
            "function": row["function"],
            "model": settings["model"],
            "model_digest": model_digest,
            "prompt_profile": settings["prompt_profile"],
            "temperature": settings["temperature"],
            "max_tokens": settings["max_tokens"],
            "target_input_sha256": target_input_hash,
            "assembly_sha256": row["assembly_sha256"] or "missing",
            "decomp_sha256": row["decomp_sha256"] or "missing",
            "baseline_source_sha256": row["baseline_source_sha256"] or "missing",
            "prompt_sha256": row["prompt_sha256"] or "missing",
        })
        mlflow.set_tags({
            "inference_endpoint": "local-ollama",
            "candidate_only": "true",
            "oracle_type": "none",
            "compile_check": "candidate-isolated-whole-target-fpc-mtp",
            "candidate_build_status": row["candidate_build_status"],
            "semantic_verification": "not-performed",
        })
        metrics = {
            "generation_succeeded": float(row["generation_succeeded"]),
            "sanitizer_accepted": float(row["accepted"]),
            "candidate_changed": float(row["candidate_changed"]),
            "candidate_build_attempted": float(
                row["candidate_build_attempted"]
            ),
            "candidate_build_attempts": row["candidate_build_attempts"],
            "compile_repair_attempts": row["compile_repair_attempts"],
            "generation_seconds": row["generation_seconds"],
            "build_seconds": row["build_seconds"],
        }
        if row["candidate_build_passed"] is not None:
            metrics["candidate_build_passed"] = float(
                row["candidate_build_passed"]
            )
        mlflow.log_metrics(metrics)
        if capture_dir.is_dir():
            mlflow.log_artifacts(str(capture_dir), artifact_path="candidate")
        mlflow.log_text(json.dumps(row, indent=2, sort_keys=True), "trial.json")
        return mlflow.active_run().info.run_id


def _run_trial(
    repo_root: pathlib.Path,
    target: str,
    function_name: str,
    settings: TrialSettings,
    endpoint: str,
    capture_dir: pathlib.Path,
    repair_rounds: int = 1,
) -> dict[str, Any]:
    if repair_rounds < 0:
        raise ValueError("repair_rounds cannot be negative")

    candidate_path = repo_root / "targets" / target / "src" / f"{function_name}.inc"
    baseline_hash = _sha256(candidate_path.read_bytes())
    generation_outputs: list[str] = []
    compiler_outputs: list[str] = []
    generation_seconds = 0.0
    build_seconds = 0.0
    compile_attempts = 0
    repair_attempts = 0
    initial_build_passed: bool | None = None
    build_code: int | None = None
    capture: dict[str, Any] = {}
    generation_succeeded = False
    repair_note = ""

    for attempt in range(repair_rounds + 1):
        attempt_dir = capture_dir / f"attempt-{attempt + 1:02d}"
        attempt_dir.mkdir(parents=True, exist_ok=True)
        command = _create_trial_command(
            repo_root,
            target,
            function_name,
            settings,
            endpoint,
            attempt_dir,
            repair_note,
        )
        started = time.monotonic()
        try:
            generation = subprocess.run(
                command,
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=600,
                check=False,
            )
            attempt_output = generation.stdout + generation.stderr
            generation_succeeded = generation.returncode == 0
        except (OSError, subprocess.SubprocessError) as exc:
            attempt_output = f"generation failed: {exc}"
            generation_succeeded = False
        generation_seconds += time.monotonic() - started
        generation_outputs.append(
            f"=== generation attempt {attempt + 1} ===\n{attempt_output}"
        )
        (attempt_dir / "generation_output.txt").write_text(attempt_output)
        capture = _load_capture(attempt_dir, function_name)
        candidate_changed = _sha256(candidate_path.read_bytes()) != baseline_hash
        accepted = capture.get("sanitizer_accepted", False)
        if not generation_succeeded or not accepted or not candidate_changed:
            break

        build_code, compiler_output, attempt_build_seconds = _run_build(
            repo_root / "targets" / target
        )
        build_seconds += attempt_build_seconds
        compile_attempts += 1
        compiler_outputs.append(
            f"=== candidate build attempt {compile_attempts} ===\n"
            f"{compiler_output}"
        )
        (attempt_dir / "compiler_output.txt").write_text(compiler_output)
        if compile_attempts == 1:
            initial_build_passed = build_code == 0
        if build_code == 0 or attempt == repair_rounds:
            break

        diagnostics = _candidate_compile_diagnostics(
            compiler_output, function_name
        )
        if not diagnostics:
            break
        repair_note = diagnostics
        repair_attempts += 1

    candidate_hash = _sha256(candidate_path.read_bytes())
    accepted = capture.get("sanitizer_accepted", False)
    candidate_changed = candidate_hash != baseline_hash
    if compile_attempts:
        build_status = "passed" if build_code == 0 else "failed"
    elif not generation_succeeded:
        build_status = "skipped-generation-failed"
    elif not accepted:
        build_status = "skipped-rejected"
    else:
        build_status = "skipped-unchanged"
    return {
        "generation_succeeded": generation_succeeded,
        "generation_attempts": len(generation_outputs),
        "generation_output": "\n".join(generation_outputs),
        "accepted": accepted,
        "rejection_reason": capture.get("rejection_reason"),
        "prompt_sha256": capture.get("prompt_sha256"),
        "completion_sha256": capture.get("completion_sha256"),
        "candidate_sha256": candidate_hash,
        "llm_candidate_sha256": capture.get("candidate_sha256"),
        "candidate_changed": candidate_changed,
        "candidate_build_attempted": compile_attempts > 0,
        "candidate_build_attempts": compile_attempts,
        "candidate_build_passed": (
            build_code == 0 if compile_attempts else None
        ),
        "initial_candidate_build_passed": initial_build_passed,
        "candidate_build_status": build_status,
        "compile_repair_attempts": repair_attempts,
        "build_return_code": build_code,
        "generation_seconds": generation_seconds,
        "build_seconds": build_seconds,
        "duration_seconds": generation_seconds + build_seconds,
        "compiler_output": "\n".join(compiler_outputs),
    }


def _candidate_compile_diagnostics(
    compiler_output: str, function_name: str
) -> str:
    source_name = f"{function_name}.inc"
    lines = compiler_output.splitlines()
    errors = []
    for index, line in enumerate(lines):
        if source_name not in line or not (
            "Error:" in line or "Fatal:" in line
        ):
            continue
        errors.append(line)
        errors.extend(
            context for context in lines[index + 1:index + 3]
            if "Found declaration:" in context
        )
    return "\n".join(errors)


def _write_summary(output_dir: pathlib.Path, summary: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    settings = summary["settings_summary"]
    lines = [
        "# Liero candidate experiment",
        "",
        "A candidate build is attempted only for a sanitizer-accepted draft that",
        "changes the original routine. Build passes do not establish semantic",
        "equivalence or source recovery.",
        "",
        f"- Baseline build passed: **{summary['baseline_build_passed']}**",
        f"- Functions: {', '.join(summary['functions'])}",
        f"- Candidate generations: {len(summary['trials'])}",
        "",
        (
            "| Model | Prompt profile | Temperature | Accepted | Changed | "
            "Build attempted | Candidate build pass | Both |"
        ),
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in settings:
        candidate_build_rate = (
            f"{row['candidate_build_passed']}/"
            f"{row['candidate_build_attempted']}"
            if row["candidate_build_attempted"]
            else "n/a"
        )
        lines.append(
            f"| {row['model']} | {row['prompt_profile']} | "
            f"{row['temperature']} | {row['accepted']}/{row['total']} | "
            f"{row['candidate_changed']}/{row['total']} | "
            f"{row['candidate_build_attempted']}/{row['total']} | "
            f"{candidate_build_rate} | "
            f"{row['accepted_and_build_passed']}/{row['total']} |"
        )
    lines.extend(["", "## Provisional per-function shortlist", ""])
    for function_name in summary["functions"]:
        ranked = rank_candidates([
            row for row in summary["trials"] if row["function"] == function_name
        ])
        best = ranked[0]
        lines.append(
            f"- `{function_name}`: `{best['settings']['model']}`, "
            f"{best['settings']['prompt_profile']}, temperature "
            f"{best['settings']['temperature']}; accepted={best['accepted']}, "
            f"candidate_build_status={best['candidate_build_status']}, "
            f"MLflow run "
            f"`{best.get('mlflow_run_id', 'unavailable')}`."
        )
    lines.extend([
        "",
        "A shortlist is not a recovery attestation. Review each candidate against",
        "its assembly, ABI, calls, state effects, and data references.",
    ])
    (output_dir / "summary.md").write_text("\n".join(lines) + "\n")


def _settings_summary(trials: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, float], list[dict[str, Any]]] = {}
    for row in trials:
        settings = row["settings"]
        key = (
            settings["model"],
            settings["prompt_profile"],
            settings["temperature"],
        )
        groups.setdefault(key, []).append(row)
    summaries = []
    for key, rows in sorted(groups.items()):
        attempted = sum(row["candidate_build_attempted"] for row in rows)
        passed = sum(
            row["candidate_build_passed"] is True for row in rows
        )
        summaries.append({
            "model": key[0],
            "prompt_profile": key[1],
            "temperature": key[2],
            "total": len(rows),
            "accepted": sum(row["accepted"] for row in rows),
            "candidate_changed": sum(row["candidate_changed"] for row in rows),
            "candidate_build_attempted": attempted,
            "candidate_build_passed": passed,
            "candidate_build_pass_rate": (
                passed / attempted if attempted else None
            ),
            "accepted_and_build_passed": sum(
                row["accepted"]
                and row["candidate_changed"]
                and row["candidate_build_passed"] is True
                for row in rows
            ),
        })
    return summaries


def run_experiment(
    target: str = "liero",
    functions: list[str] | None = None,
    panel_size: int = 4,
    models: list[str] | None = None,
    prompt_profiles: list[str] | None = None,
    temperatures: list[float] | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    endpoint: str = DEFAULT_ENDPOINT,
    tracking_dir: pathlib.Path | None = None,
    output_dir: pathlib.Path | None = None,
    scratch_root: pathlib.Path | None = None,
    compile_repair_rounds: int = DEFAULT_COMPILE_REPAIR_ROUNDS,
) -> dict[str, Any]:
    import mlflow

    if compile_repair_rounds < 0:
        raise ValueError("compile_repair_rounds cannot be negative")
    source_target = ROOT / "targets" / target
    models = list(DEFAULT_MODELS) if models is None else models
    prompt_profiles = (
        list(DEFAULT_PROMPT_PROFILES)
        if prompt_profiles is None
        else prompt_profiles
    )
    temperatures = (
        list(DEFAULT_TEMPERATURES) if temperatures is None else temperatures
    )
    settings = build_settings_matrix(
        models, prompt_profiles, temperatures, max_tokens
    )
    functions = (
        select_function_panel(source_target, DEFAULT_FUNCTION, panel_size)
        if functions is None
        else functions
    )
    if not functions:
        raise ValueError("at least one function is required")
    if len(set(functions)) != len(functions):
        raise ValueError("function panel contains duplicate names")
    missing = [
        function for function in functions
        if not (source_target / "asm" / f"{function}.s").is_file()
    ]
    if missing:
        raise FileNotFoundError(f"assembly is missing for functions: {missing}")
    missing_pascal = [
        function for function in functions
        if not (source_target / "src" / f"{function}.inc").is_file()
    ]
    if missing_pascal:
        raise FileNotFoundError(
            f"Pascal source is missing for functions: {missing_pascal}"
        )
    toolchain_text = (
        source_target / "config" / "toolchain.yaml"
    ).read_text(errors="replace").lower()
    if not any(
        line.strip() == "language: pascal"
        for line in toolchain_text.splitlines()
    ):
        raise ValueError(f"{target} is not configured as a Pascal target")

    model_digests = _ollama_model_digests(endpoint, models)
    tracking_dir = tracking_dir or ROOT / "mlruns"
    if output_dir is None:
        run_stamp = (
            time.strftime("%Y%m%d-%H%M%S", time.gmtime())
            + f"-{time.time_ns() % 1_000_000_000:09d}"
        )
        output_dir = (
            ROOT / "reports" / "liero-candidate-experiment" / run_stamp
        )
    elif output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(
            f"experiment report directory is not empty: {output_dir}"
        )
    scratch_root = (
        scratch_root
        or pathlib.Path.home() / ".cache" / "losore" / "experiments"
    )
    tracking_dir.mkdir(parents=True, exist_ok=True)
    scratch_root.mkdir(parents=True, exist_ok=True)
    tracking_uri = f"sqlite:///{(tracking_dir.resolve() / 'mlflow.db').as_posix()}"
    artifact_root = tracking_dir.resolve() / "artifacts"
    artifact_root.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(tracking_uri)
    mlflow_client = mlflow.MlflowClient(tracking_uri=tracking_uri)
    experiment_name = "LoSoRe Liero candidate sweep"
    experiment = mlflow_client.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow_client.create_experiment(
            experiment_name,
            artifact_location=artifact_root.as_uri(),
        )
        experiment = mlflow_client.get_experiment(experiment_id)
    trials: list[dict[str, Any]] = []
    baseline_code: int | None = None
    baseline_output = ""
    baseline_build_passed = False

    with tempfile.TemporaryDirectory(
        prefix="liero-candidate-sweep-",
        dir=scratch_root,
    ) as scratch_name:
        scratch_path = pathlib.Path(scratch_name)
        scratch_repo = _copy_scratch_repository(ROOT, scratch_path, target)
        scratch_target = scratch_repo / "targets" / target
        baseline_code, baseline_output, _ = _run_build(scratch_target)
        baseline_build_passed = baseline_code == 0
        if not baseline_build_passed:
            raise RuntimeError(
                "scratch baseline build failed; candidate compile comparisons "
                f"would be inconclusive:\n{baseline_output[-6000:]}"
            )

        for function_name in functions:
            source_candidate = source_target / "src" / f"{function_name}.inc"
            clean_candidate = source_candidate.read_bytes()
            fingerprints = input_fingerprints(source_target, function_name)
            for setting in settings:
                scratch_candidate = scratch_target / "src" / f"{function_name}.inc"
                scratch_candidate.write_bytes(clean_candidate)
                run_name = (
                    f"{function_name}-{setting.model}-{setting.prompt_profile}"
                    f"-t{setting.temperature}"
                ).replace(":", "-")
                capture_dir = scratch_path / "captures" / run_name
                capture_dir.mkdir(parents=True, exist_ok=True)
                result = _run_trial(
                    scratch_repo,
                    target,
                    function_name,
                    setting,
                    endpoint,
                    capture_dir,
                    repair_rounds=compile_repair_rounds,
                )
                capture_dir.joinpath("generation_output.txt").write_text(
                    result.pop("generation_output")
                )
                (capture_dir / "compiler_output.txt").write_text(
                    result.pop("compiler_output")
                )
                (capture_dir / "candidate.inc").write_bytes(
                    scratch_candidate.read_bytes()
                )
                row = {
                    "run_name": run_name,
                    "target": target,
                    "function": function_name,
                    "settings": asdict(setting),
                    "oracle_type": "none",
                    **fingerprints,
                    **result,
                    "model_digest": model_digests[setting.model],
                }
                row["mlflow_run_id"] = _log_trial(
                    mlflow,
                    experiment.experiment_id,
                    row,
                    capture_dir,
                    fingerprints["target_input_sha256"] or "",
                    model_digests[setting.model],
                )
                trials.append(row)

    summary = {
        "target": target,
        "functions": functions,
        "baseline_build_passed": baseline_build_passed,
        "baseline_build_return_code": baseline_code,
        "baseline_build_output": baseline_output,
        "tracking_uri": tracking_uri,
        "experiment_id": experiment.experiment_id,
        "output_dir": str(output_dir.resolve()),
        "trials": trials,
        "settings_summary": _settings_summary(trials),
    }
    _write_summary(output_dir, summary)
    return summary


def _csv_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="liero")
    parser.add_argument(
        "--functions",
        default=None,
        help="comma-separated function names",
    )
    parser.add_argument("--panel-size", type=int, default=4)
    parser.add_argument("--models", default=",".join(DEFAULT_MODELS))
    parser.add_argument(
        "--prompt-profiles",
        default=",".join(DEFAULT_PROMPT_PROFILES),
    )
    parser.add_argument(
        "--temperatures",
        default=",".join(str(value) for value in DEFAULT_TEMPERATURES),
    )
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    parser.add_argument(
        "--compile-repair-rounds",
        type=int,
        default=DEFAULT_COMPILE_REPAIR_ROUNDS,
        help="bounded compiler-feedback retries for accepted candidates",
    )
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--tracking-dir", type=pathlib.Path, default=ROOT / "mlruns")
    parser.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=None,
    )
    parser.add_argument(
        "--scratch-root",
        type=pathlib.Path,
        default=pathlib.Path.home() / ".cache" / "losore" / "experiments",
    )
    args = parser.parse_args()
    summary = run_experiment(
        target=args.target,
        functions=_csv_list(args.functions) if args.functions else None,
        panel_size=args.panel_size,
        models=_csv_list(args.models),
        prompt_profiles=_csv_list(args.prompt_profiles),
        temperatures=[float(value) for value in _csv_list(args.temperatures)],
        max_tokens=args.max_tokens,
        compile_repair_rounds=args.compile_repair_rounds,
        endpoint=args.endpoint,
        tracking_dir=args.tracking_dir,
        output_dir=args.output_dir,
        scratch_root=args.scratch_root,
    )
    print(json.dumps({
        "target": summary["target"],
        "functions": summary["functions"],
        "candidate_runs": len(summary["trials"]),
        "summary_dir": summary["output_dir"],
        "tracking_uri": summary["tracking_uri"],
    }, indent=2))


if __name__ == "__main__":
    main()
