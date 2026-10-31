"""Hash-bound, atomic persistence for resumable recovery runs."""

from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import re
import shutil
import uuid
from dataclasses import dataclass
from typing import Any

SCHEMA_VERSION = 1
RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


@dataclass
class RecoveryRun:
    target_root: pathlib.Path
    path: pathlib.Path
    data: dict[str, Any]

    @property
    def run_id(self) -> str:
        return str(self.data["run_id"])


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fingerprints(paths: list[pathlib.Path]) -> dict[str, str | None]:
    fingerprints = {}
    for path in sorted({item.resolve() for item in paths}, key=str):
        fingerprints[str(path)] = _sha256(path) if path.is_file() else None
    return fingerprints


def _configuration_hash(configuration: dict[str, Any]) -> str:
    serialized = json.dumps(configuration, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


def _write(run: RecoveryRun) -> None:
    run.data["updated_at"] = datetime.datetime.now(datetime.UTC).isoformat()
    temporary = run.path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(run.data, indent=2, sort_keys=True) + "\n")
    temporary.replace(run.path)


def _snapshot_directory(
    run: RecoveryRun, function_name: str, attempt: int
) -> pathlib.Path:
    function_key = hashlib.sha256(function_name.encode()).hexdigest()
    return run.path.parent / f"{run.run_id}.snapshots" / function_key / str(attempt)


def _store_source_snapshot(
    run: RecoveryRun,
    function_name: str,
    attempt: int,
    source_snapshot: dict[pathlib.Path, bytes],
) -> dict[str, str]:
    destination = _snapshot_directory(run, function_name, attempt)
    if destination.exists():
        if destination.is_dir():
            shutil.rmtree(destination)
        else:
            destination.unlink()
    temporary = destination.with_name(f".{attempt}.{uuid.uuid4().hex}.tmp")
    manifest = {}
    try:
        temporary.mkdir(parents=True)
        for path, contents in source_snapshot.items():
            relative = path.resolve().relative_to(run.target_root).as_posix()
            if not relative.startswith("src/"):
                raise ValueError(f"attempt snapshot is outside src/: {path}")
            snapshot_path = temporary / relative
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            snapshot_path.write_bytes(contents)
            manifest[relative] = hashlib.sha256(contents).hexdigest()
        temporary.replace(destination)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return manifest


def restore_interrupted_attempt(
    run: RecoveryRun, function_name: str, attempt: int
) -> None:
    """Restore a persisted pre-generation source snapshot after interruption."""
    routine = run.data.get("routines", {}).get(function_name)
    if not isinstance(routine, dict):
        raise KeyError(f"{function_name}: no persisted routine attempt")
    record = next(
        (item for item in routine.get("attempts", []) if item.get("attempt") == attempt),
        None,
    )
    if record is None or record.get("status") != "started":
        raise ValueError(f"{function_name}: attempt {attempt} is not interrupted")
    manifest = record.get("source_snapshot")
    if not isinstance(manifest, dict):
        raise TypeError(f"{function_name}: attempt snapshot is missing")

    snapshot_root = _snapshot_directory(run, function_name, attempt)
    restored = {}
    for relative, expected_hash in manifest.items():
        source = pathlib.PurePosixPath(relative)
        if (
            source.is_absolute()
            or len(source.parts) != 2
            or source.parts[0] != "src"
            or ".." in source.parts
            or not (
                source.suffix == ".inc"
                or source.name == f"{run.target_root.name}.pas"
            )
        ):
            raise ValueError(f"{function_name}: invalid snapshot path {relative!r}")
        source_path = run.target_root.joinpath(*source.parts)
        contents = (snapshot_root / source).read_bytes()
        if hashlib.sha256(contents).hexdigest() != expected_hash:
            raise ValueError(f"{function_name}: snapshot is corrupt for {relative}")
        restored[source_path] = contents

    source_dir = run.target_root / "src"
    expected_paths = set(restored)
    current_paths = set(source_dir.glob("*.inc"))
    current_paths.add(source_dir / f"{run.target_root.name}.pas")
    for path in current_paths - expected_paths:
        if path.is_file():
            path.unlink()
    for path, contents in restored.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".restore.tmp")
        temporary.write_bytes(contents)
        temporary.replace(path)


def open_run(
    target_root: pathlib.Path,
    input_files: list[pathlib.Path],
    configuration: dict[str, Any],
    run_id: str | None = None,
) -> RecoveryRun:
    """Create a run or resume it only when its input and config fingerprints match."""
    root = target_root.resolve()
    run_dir = root / "runs"
    run_dir.mkdir(parents=True, exist_ok=True)
    fingerprints = _fingerprints(input_files)
    config_hash = _configuration_hash(configuration)

    if run_id is not None:
        if not RUN_ID_PATTERN.fullmatch(run_id):
            raise ValueError(f"invalid run id: {run_id!r}")
        path = run_dir / f"{run_id}.json"
        if not path.is_file():
            raise FileNotFoundError(f"run does not exist: {path}")
        data = json.loads(path.read_text())
        if data.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"unsupported run state schema in {path}")
        if data.get("target") != root.name:
            raise ValueError(f"run target does not match {root.name}")
        if data.get("input_fingerprints") != fingerprints:
            raise ValueError("input files changed since the run was recorded")
        if data.get("configuration_sha256") != config_hash:
            raise ValueError("configuration changed since the run was recorded")
        if not isinstance(data.get("routines"), dict):
            raise TypeError(f"run routines must be an object: {path}")
        return RecoveryRun(root, path, data)

    now = datetime.datetime.now(datetime.UTC)
    new_run_id = f"{now.strftime('%Y%m%dT%H%M%S.%fZ')}-{uuid.uuid4().hex[:8]}"
    path = run_dir / f"{new_run_id}.json"
    data = {
        "schema_version": SCHEMA_VERSION,
        "run_id": new_run_id,
        "target": root.name,
        "status": "in_progress",
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "input_fingerprints": fingerprints,
        "configuration": configuration,
        "configuration_sha256": config_hash,
        "stages": {},
        "routines": {},
    }
    run = RecoveryRun(root, path, data)
    _write(run)
    return run


def update_stage(run: RecoveryRun, stage: str, **values: Any) -> None:
    """Persist the latest status and details for a named pipeline stage."""
    if not stage.strip():
        raise ValueError("stage name must not be empty")
    record = run.data.setdefault("stages", {}).setdefault(stage, {})
    record.update(values)
    record["updated_at"] = datetime.datetime.now(datetime.UTC).isoformat()
    _write(run)


def start_attempt(
    run: RecoveryRun,
    function_name: str,
    attempt: int,
    *,
    source_snapshot: dict[pathlib.Path, bytes] | None = None,
) -> dict[str, Any]:
    """Persist an attempt before generation begins, so interruption is visible."""
    if not function_name.strip() or attempt < 1:
        raise ValueError("function name and positive attempt number are required")
    routine = run.data.setdefault("routines", {}).setdefault(
        function_name, {"attempts": []}
    )
    attempts = routine.setdefault("attempts", [])
    if any(entry.get("attempt") == attempt for entry in attempts):
        raise ValueError(f"{function_name}: attempt {attempt} already exists")
    if source_snapshot is None:
        raise ValueError("a source snapshot is required before generation starts")
    snapshot_manifest = _store_source_snapshot(
        run, function_name, attempt, source_snapshot
    )
    record = {
        "attempt": attempt,
        "status": "started",
        "started_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "diagnostics": [],
        "source_snapshot": snapshot_manifest,
    }
    attempts.append(record)
    routine["status"] = "in_progress"
    _write(run)
    return record


def finish_attempt(
    run: RecoveryRun,
    function_name: str,
    attempt: int,
    *,
    status: str,
    diagnostics: list[str] | None = None,
    source_sha256: str | None = None,
    evidence: dict[str, Any] | None = None,
) -> None:
    """Complete an attempt record while retaining its start time and history."""
    routine = run.data.get("routines", {}).get(function_name)
    if not isinstance(routine, dict):
        raise KeyError(f"{function_name}: no persisted routine attempt")
    entry = next(
        (item for item in routine.get("attempts", []) if item.get("attempt") == attempt),
        None,
    )
    if entry is None:
        raise KeyError(f"{function_name}: attempt {attempt} does not exist")
    if entry.get("status") != "started":
        raise ValueError(f"{function_name}: attempt {attempt} is already complete")
    entry.update(
        status=status,
        diagnostics=list(diagnostics or []),
        source_sha256=source_sha256,
        finished_at=datetime.datetime.now(datetime.UTC).isoformat(),
    )
    if evidence is not None:
        entry["evidence"] = evidence
    routine["status"] = status
    _write(run)
