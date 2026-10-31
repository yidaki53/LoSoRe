"""Check whether a target can run the complete local recovery pipeline."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ingest

DEFAULT_LOCAL_MODEL = "qwen2.5-coder:14b-instruct-q4_K_M"
DEFAULT_LOCAL_ENDPOINT = "http://localhost:11434"


def _yaml_value(path: pathlib.Path, key: str) -> str | None:
    if not path.is_file():
        return None
    for line in path.read_text(errors="replace").splitlines():
        match = re.match(rf"^{re.escape(key)}\s*:\s*(.*?)\s*$", line)
        if match:
            return match.group(1).strip("\"'")
    return None


def _check(name: str, status: str, detail: str) -> dict[str, str]:
    return {"name": name, "status": status, "detail": detail}


def _model_check(endpoint: str, model: str) -> dict[str, str]:
    base = endpoint.rstrip("/")
    if base.endswith("/v1/chat/completions"):
        base = base[: -len("/chat/completions")].rstrip("/")
    if base.endswith("/v1"):
        paths = ("/v1/models", "/api/tags")
        base = base[:-3]
    elif ":11434" in base:
        paths = ("/api/tags", "/v1/models")
    else:
        paths = ("/v1/models", "/api/tags")
    errors = []
    for suffix in paths:
        try:
            request = urllib.request.Request(base + suffix)
            with urllib.request.urlopen(request, timeout=2) as response:
                payload = json.loads(response.read())
            if not isinstance(payload, dict):
                errors.append(f"{suffix} returned an invalid response")
                continue
            models = payload.get("models", payload.get("data", []))
            model_ids = [
                str(item.get("name") or item.get("id") or "")
                for item in models
                if isinstance(item, dict)
            ]
            if model_ids and model in model_ids:
                return _check("llm", "ready", f"{model} available at {endpoint}")
            if model_ids:
                return _check(
                    "llm",
                    "blocked",
                    f"model {model!r} is not listed at {endpoint}; available: "
                    + ", ".join(model_ids),
                )
            errors.append(f"{suffix} returned no model list")
        except (OSError, ValueError, urllib.error.URLError) as exc:
            errors.append(f"{suffix}: {exc}")
    return _check("llm", "blocked", f"cannot confirm model {model!r}: " + "; ".join(errors))


def _scratch_check(target: str) -> dict[str, str]:
    scratch = pathlib.Path(
        os.environ.get("LSR_GHIDRA_PROJ")
        or pathlib.Path(tempfile.gettempdir()) / f"lsr_proj_{target}"
    ).expanduser()
    writable_path = scratch
    while not writable_path.exists() and writable_path != writable_path.parent:
        writable_path = writable_path.parent
    if not writable_path.is_dir() or not os.access(writable_path, os.W_OK | os.X_OK):
        return _check(
            "scratch",
            "blocked",
            f"scratch path is not writable: {writable_path}; set LSR_GHIDRA_PROJ "
            "to a writable path",
        )
    if " " in str(scratch):
        return _check(
            "scratch",
            "blocked",
            f"Ghidra project path contains spaces: {scratch}; set "
            "LSR_GHIDRA_PROJ to a path without spaces",
        )
    return _check("scratch", "ready", f"Ghidra scratch root is writable: {scratch}")


def _docker_check(makefile: pathlib.Path) -> dict[str, str]:
    if not makefile.is_file() or "docker " not in makefile.read_text(errors="replace"):
        return _check("build_runtime", "skipped", "target Makefile does not declare Docker")
    docker = shutil.which("docker")
    if not docker:
        return _check("build_runtime", "blocked", "Docker is required by the target Makefile")
    try:
        result = subprocess.run(
            [docker, "info", "--format", "{{.ServerVersion}}"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return _check("build_runtime", "blocked", f"Docker daemon check failed: {exc}")
    if result.returncode:
        detail = result.stderr.strip() or "docker info returned a nonzero status"
        return _check("build_runtime", "blocked", detail)
    return _check("build_runtime", "ready", f"Docker daemon {result.stdout.strip()}")


def preflight(target: str, workspace: pathlib.Path) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", target):
        return {
            "target": target,
            "status": "blocked",
            "checks": [],
            "blockers": ["target slug must contain only letters, digits, '_' or '-'"],
            "warnings": [],
        }

    root = workspace.resolve()
    target_root = root / "targets" / target
    target_config = target_root / "config" / "target.yaml"
    toolchain_config = target_root / "config" / "toolchain.yaml"
    byod = root / "extracted" / target
    checks = []

    if not target_config.is_file():
        checks.append(_check("target_config", "blocked", f"missing {target_config}"))
    else:
        checks.append(_check("target_config", "ready", str(target_config)))
    if not toolchain_config.is_file():
        checks.append(_check("toolchain_config", "blocked", f"missing {toolchain_config}"))
    else:
        checks.append(_check("toolchain_config", "ready", str(toolchain_config)))
    for key in ("language", "compiler"):
        value = _yaml_value(toolchain_config, key)
        if not value or value.lower() == "todo":
            checks.append(
                _check("toolchain", "blocked", f"{key} is missing or unresolved")
            )

    configured_slug = _yaml_value(target_config, "slug")
    if configured_slug and configured_slug != target:
        checks.append(
            _check(
                "target_identity",
                "blocked",
                f"target config slug {configured_slug!r} does not match {target!r}",
            )
        )

    if not byod.is_dir():
        checks.append(_check("binary", "blocked", f"missing BYOD directory {byod}"))
    else:
        binary = ingest.pick_binary(byod)
        if binary is None:
            checks.append(_check("binary", "blocked", f"no executable found in {byod}"))
        else:
            digest = hashlib.sha256()
            with binary.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            checks.append(
                _check(
                    "binary",
                    "ready",
                    f"{binary} ({binary.stat().st_size} bytes, "
                    f"sha256={digest.hexdigest()})",
                )
            )

    ghidra = ingest.find_ghidra()
    analyze_headless = (
        pathlib.Path(ghidra) / "support" / "analyzeHeadless"
        if ghidra
        else pathlib.Path(shutil.which("analyzeHeadless") or "")
    )
    if not analyze_headless.is_file() or not os.access(analyze_headless, os.X_OK):
        checks.append(
            _check("ghidra", "blocked", "analyzeHeadless not found; set LSR_GHIDRA")
        )
    else:
        checks.append(_check("ghidra", "ready", str(analyze_headless)))
    java = shutil.which("java")
    checks.append(
        _check("java", "ready", java)
        if java
        else _check("java", "blocked", "java not found on PATH")
    )
    checks.append(_scratch_check(target))
    checks.append(_docker_check(target_root / "Makefile"))

    endpoint = os.environ.get("LSR_LLM_ENDPOINT", DEFAULT_LOCAL_ENDPOINT)
    model = os.environ.get("LSR_LLM_MODEL", DEFAULT_LOCAL_MODEL)
    checks.append(_model_check(endpoint, model))

    oracle = _yaml_value(toolchain_config, "oracle") or _yaml_value(
        target_config, "oracle"
    )
    if oracle in (None, "", "none", "dat-parity"):
        checks.append(
            _check(
                "behavior_oracle",
                "warning",
                f"{oracle or 'no oracle'} does not establish routine behavior; "
                "recovery claims remain unverified without a function-level oracle",
            )
        )
    else:
        checks.append(_check("behavior_oracle", "ready", f"configured oracle: {oracle}"))

    training_model = os.environ.get("LSR_TRAIN_MODEL")
    if training_model and pathlib.Path(training_model).expanduser().is_dir():
        checks.append(_check("training", "ready", "optional local training model found"))
    elif training_model:
        checks.append(
            _check(
                "training",
                "skipped",
                f"optional training model path does not exist: {training_model}",
            )
        )
    else:
        checks.append(_check("training", "skipped", "optional local training not configured"))

    blockers = [item["detail"] for item in checks if item["status"] == "blocked"]
    warnings = [item["detail"] for item in checks if item["status"] == "warning"]
    return {
        "target": target,
        "status": "blocked" if blockers else "ready",
        "checks": checks,
        "blockers": blockers,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--workspace", type=pathlib.Path, default=pathlib.Path.cwd())
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args(argv)
    report = preflight(args.target, args.workspace)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"[preflight:{args.target}] {report['status'].upper()}")
        for item in report["checks"]:
            print(f"  {item['status'].upper():7} {item['name']}: {item['detail']}")
    return 1 if report["blockers"] else 0


if __name__ == "__main__":
    sys.exit(main())
