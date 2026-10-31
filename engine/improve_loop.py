"""Bounded, compile-gated iteration for assembly-backed Pascal routines."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from collections.abc import Iterator
from contextlib import contextmanager, nullcontext
from typing import Any

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT))
sys.path.insert(0, str(REPOSITORY_ROOT / "engine"))

import draft
import fact_graph
import verify

import knowledge
from engine import ingest, recovery, run_state
from tools.report import _has_pascal_implementation

DEFAULT_MAX_ITERATIONS = 10
DEFAULT_SATURATION_WINDOW = 3
DEFAULT_FUNCTIONS_PER_ITERATION = 5
DEFAULT_MAX_ATTEMPTS_PER_FUNCTION = 3
DEFAULT_LOCAL_MODEL = "qwen2.5-coder:14b-instruct-q4_K_M"
DEFAULT_LOCAL_ENDPOINT = "http://localhost:11434"
FUNCTION_ORACLES = {"byte-exact", "relocation-aware"}


def _run(
    cmd: list[str], cwd: pathlib.Path | None = None
) -> tuple[int, str, str]:
    """Run a command; return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd, check=False, capture_output=True, text=True, cwd=cwd
    )
    return result.returncode, result.stdout, result.stderr


def _draft(
    target: str,
    fn: str | None = None,
    model: str | None = None,
    endpoint: str | None = None,
    retry_existing: bool = False,
    repair_note: str = "",
    cwd: pathlib.Path | None = None,
    function_only: bool = False,
    capture_dir: pathlib.Path | None = None,
    temperature: float = 0.0,
    localized_repair: bool = False,
) -> int:
    """Draft one function and pass any earlier compiler diagnostics to the LLM."""
    command = [
        sys.executable,
        str(REPOSITORY_ROOT / "engine" / "draft.py"),
        "--target",
        target,
        "--llm",
        "--skip-compile-gate",
    ]
    if fn:
        command.extend(["--fn", fn])
    if retry_existing:
        command.append("--retry-existing")
    if function_only:
        command.append("--function-only")
    if localized_repair:
        command.append("--localized-repair")
    if repair_note:
        command.extend(["--repair-note", repair_note])
    if capture_dir:
        command.extend(["--capture-dir", str(capture_dir)])
    command.extend(["--temperature", str(temperature)])
    model = model or os.environ.get("LSR_LLM_MODEL") or DEFAULT_LOCAL_MODEL
    endpoint = (
        endpoint
        or os.environ.get("LSR_LLM_ENDPOINT")
        or DEFAULT_LOCAL_ENDPOINT
    )
    if model:
        command.extend(["--model", model])
    if endpoint:
        command.extend(["--endpoint", endpoint])

    returncode, stdout, stderr = _run(command, cwd=cwd)
    if stdout.strip():
        print(stdout.strip())
    if stderr.strip():
        print(stderr.strip())
    if "[llm-endpoint]" in stdout:
        returncode = returncode or 3
    if returncode:
        print(
            f"[improve:{target}] draft failed for {fn or 'target'} "
            f"(exit {returncode})"
        )
    return returncode


@contextmanager
def _candidate_workspace(
    target_root: pathlib.Path,
    target: str,
    byod: pathlib.Path,
) -> Iterator[tuple[pathlib.Path, pathlib.Path]]:
    """Create an isolated target copy for one draft/build/oracle attempt."""
    with tempfile.TemporaryDirectory(prefix=f"losore-{target}-candidate-") as raw:
        workspace = pathlib.Path(raw)
        candidate_target = workspace / "targets" / target
        candidate_target.parent.mkdir(parents=True)
        shutil.copytree(
            target_root,
            candidate_target,
            ignore=shutil.ignore_patterns(
                "build", "runs", "__pycache__", "core.[0-9]*"
            ),
        )
        for name in ("engine", "tools", "compilers"):
            source = REPOSITORY_ROOT / name
            if source.exists():
                (workspace / name).symlink_to(source, target_is_directory=True)

        binary = ingest.pick_binary(byod) if byod.is_dir() else None
        if binary is not None:
            binary_destination = workspace / "extracted" / target / binary.name
            binary_destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(binary, binary_destination)
        yield workspace, candidate_target


def _run_function_oracle(
    oracle: str, root: pathlib.Path, output: pathlib.Path
) -> dict[str, Any]:
    if oracle != "liero-compare-routine-probe":
        raise ValueError(f"unsupported function oracle: {oracle}")
    from tools.liero_compare_routine_probe import (
        run_probe,
        validate_saved_report,
    )

    report = run_probe(root, output)
    validated = validate_saved_report(output, root)
    if report != validated:
        raise ValueError("routine oracle report changed during validation")
    return validated


def _persist_candidate(
    run: run_state.RecoveryRun,
    function_name: str,
    attempt: int,
    contents: bytes,
) -> tuple[str, str]:
    function_key = hashlib.sha256(function_name.encode()).hexdigest()
    destination = (
        run.path.parent
        / f"{run.run_id}.candidates"
        / function_key
        / f"{attempt}.inc"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(contents)
    relative = destination.relative_to(run.target_root).as_posix()
    return relative, hashlib.sha256(contents).hexdigest()


def _duplicate_candidate_attempt(
    run: run_state.RecoveryRun,
    function_name: str,
    candidate_hash: str | None,
    current_attempt: int,
) -> int | None:
    if candidate_hash is None:
        return None
    attempts = (
        run.data.get("routines", {}).get(function_name, {}).get("attempts", [])
    )
    for previous in attempts:
        if (
            previous.get("attempt") != current_attempt
            and previous.get("source_sha256") == candidate_hash
        ):
            return previous["attempt"]
    return None


def _generation_evidence(
    root: pathlib.Path,
    capture_dir: pathlib.Path | None,
    function_name: str,
    previous_candidate: bytes | None,
    model: str,
    temperature: float,
) -> dict[str, Any]:
    if capture_dir is None:
        return {"status": "not-captured"}
    capture_root = capture_dir / function_name
    metadata_path = capture_root / "capture.json"
    evidence: dict[str, Any] = {
        "status": "missing",
        "capture_path": capture_root.resolve().relative_to(
            root.resolve()
        ).as_posix(),
        "model": model,
        "temperature": temperature,
        "previous_candidate_sha256": (
            hashlib.sha256(previous_candidate).hexdigest()
            if previous_candidate is not None
            else None
        ),
    }
    if not metadata_path.is_file():
        return evidence
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        evidence.update(status="invalid", error=str(exc))
        return evidence
    if not isinstance(metadata, dict):
        evidence.update(status="invalid", error="capture metadata is not an object")
        return evidence
    for key in ("prompt_sha256", "completion_sha256"):
        value = metadata.get(key)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            evidence.update(
                status="invalid",
                error=f"capture metadata has invalid {key}",
            )
            return evidence
    evidence.update(
        status="captured",
        prompt_sha256=metadata.get("prompt_sha256"),
        completion_sha256=metadata.get("completion_sha256"),
        generated_routine_sha256=metadata.get("candidate_sha256"),
        repair_mode=metadata.get("repair_mode", "full-routine"),
        prompt_chars=len((capture_root / "prompt.txt").read_text(encoding="utf-8"))
        if (capture_root / "prompt.txt").is_file()
        else None,
    )
    return evidence


def _previous_candidate(
    run: run_state.RecoveryRun, function_name: str
) -> bytes | None:
    attempts = (
        run.data.get("routines", {}).get(function_name, {}).get("attempts", [])
    )
    if not attempts:
        return None
    evidence = attempts[-1].get("evidence", {})
    relative = evidence.get("candidate_path")
    expected_hash = evidence.get("candidate_sha256")
    if not isinstance(relative, str) or not isinstance(expected_hash, str):
        return None
    candidate = run.target_root / relative
    try:
        candidate.resolve().relative_to(run.target_root.resolve())
    except ValueError as exc:
        raise ValueError(f"{function_name}: persisted candidate path escapes target") from exc
    if not candidate.is_file():
        return None
    contents = candidate.read_bytes()
    if hashlib.sha256(contents).hexdigest() != expected_hash:
        raise ValueError(f"{function_name}: persisted candidate hash changed")
    return contents


def _verify(
    target: str,
    byod: pathlib.Path,
    build: pathlib.Path,
    oracle: str = "dat-parity",
) -> int:
    """Run the selected oracle separately from compile-success accounting."""
    returncode, _, stderr = _run(
        [
            sys.executable,
            "engine/verify.py",
            "--target",
            target,
            "--byod",
            str(byod),
            "--build",
            str(build),
            "--oracle",
            oracle,
        ]
    )
    if returncode:
        print(f"[improve:{target}] {oracle} oracle returned {returncode}: {stderr.strip()}")
    return returncode


def _compile_status(root: pathlib.Path) -> tuple[set[str], list[str]]:
    """Compile the full target and return failing routine stems and diagnostics."""
    try:
        return draft._compile_errors(root)
    except (OSError, subprocess.SubprocessError) as exc:
        return {"_MAKE_FAILED"}, [f"target build could not run: {exc}"]


def _verified_functions(
    data: dict, target: str, oracle: str, function_names: set[str]
) -> set[str]:
    """Return verified paths that correspond to known assembly functions."""
    entries = (
        data.get("targets", {})
        .get(target, {})
        .get("verified", {})
        .get(oracle, [])
    )
    return {
        pathlib.Path(entry).stem
        for entry in entries
        if pathlib.Path(entry).stem in function_names
    }


def _binary_verified_functions(data: dict, target: str, function_names: set[str]) -> set[str]:
    """Exclude format and trace checks from function-level binary verification."""
    verified = data.get("targets", {}).get(target, {}).get("verified", {})
    return set().union(
        *(
            _verified_functions(data, target, oracle, function_names)
            for oracle in FUNCTION_ORACLES
            if oracle in verified
        )
    )


def _meaningful_functions(root: pathlib.Path, function_names: set[str]) -> set[str]:
    source = root / "src"
    return {
        fn
        for fn in function_names
        if (source / f"{fn}.inc").is_file()
        and _has_pascal_implementation(source / f"{fn}.inc")
    }


def _has_assembly_instructions(path: pathlib.Path) -> bool:
    return bool(
        re.search(
            r"(?m)^\s*[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}\s+[A-Za-z][A-Za-z0-9.]*\b",
            path.read_text(errors="replace"),
        )
    )


def _direct_call_dependencies(
    root: pathlib.Path, function_names: set[str]
) -> dict[str, set[str]]:
    """Map each routine to known in-target direct callees from assembly."""
    _, dependencies = _assembly_call_graph(root, function_names)
    return dependencies


def _assembly_call_graph(
    root: pathlib.Path, function_names: set[str]
) -> tuple[fact_graph.FactGraph, dict[str, set[str]]]:
    """Build the assembly graph and its known in-target direct-call map."""
    dependencies = {fn: set() for fn in function_names}
    assembly_paths = {
        fn: root / "asm" / f"{fn}.s"
        for fn in function_names
        if (root / "asm" / f"{fn}.s").is_file()
    }
    graph = fact_graph.FactGraph.from_assembly(root.name, assembly_paths)
    for edge in graph.edges.values():
        if edge.relation != "direct_call":
            continue
        caller = graph.nodes[edge.source].attributes["caller"]
        callee = graph.nodes[edge.target].attributes["name"]
        if caller != callee:
            dependencies[caller].add(callee)
    return graph, dependencies


def _source_recovered_functions(root: pathlib.Path) -> set[str]:
    """Return only hash-current, reviewer-attested source recoveries."""
    if not (root / "recovery.json").is_file():
        return set()
    report = recovery.audit_target(root)
    return {
        routine["name"]
        for routine in report["routines"]
        if routine["source_recovered"]
    }


def _dependency_components(
    dependencies: dict[str, set[str]],
) -> list[set[str]]:
    """Collapse mutually recursive routines so each cycle is handled as a unit."""
    next_index = 0
    indices: dict[str, int] = {}
    low_links: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[set[str]] = []

    def visit(function_name: str) -> None:
        nonlocal next_index
        indices[function_name] = next_index
        low_links[function_name] = next_index
        next_index += 1
        stack.append(function_name)
        on_stack.add(function_name)

        for callee in sorted(dependencies[function_name]):
            if callee not in indices:
                visit(callee)
                low_links[function_name] = min(
                    low_links[function_name], low_links[callee]
                )
            elif callee in on_stack:
                low_links[function_name] = min(
                    low_links[function_name], indices[callee]
                )

        if low_links[function_name] != indices[function_name]:
            return
        component = set()
        while True:
            member = stack.pop()
            on_stack.remove(member)
            component.add(member)
            if member == function_name:
                break
        components.append(component)

    for function_name in sorted(dependencies):
        if function_name not in indices:
            visit(function_name)
    return components


def _unresolved_external_dependencies(
    component: set[str],
    dependencies: dict[str, set[str]],
    component_for: dict[str, set[str]],
    recovered: set[str],
) -> set[str]:
    """Require every member of an external recursive group to be reviewed."""
    unresolved = set()
    for member in component:
        for callee in dependencies[member] - component:
            if not component_for[callee] <= recovered:
                unresolved.add(callee)
    return unresolved


def _select_candidates(
    root: pathlib.Path,
    function_names: set[str],
    attempted: Counter[str],
    failed: set[str],
    max_attempts_per_function: int,
    limit: int,
) -> list[str]:
    """Select dependency-ready routines before their callers."""
    meaningful = _meaningful_functions(root, function_names)
    dependencies = _direct_call_dependencies(root, function_names)
    recovered = _source_recovered_functions(root)
    components = _dependency_components(dependencies)
    component_for = {
        function_name: component
        for component in components
        for function_name in component
    }
    candidates = []
    for fn in function_names:
        if attempted[fn] >= max_attempts_per_function:
            continue
        if fn in meaningful and fn not in failed:
            continue
        component = component_for[fn]
        if _unresolved_external_dependencies(
            component, dependencies, component_for, recovered
        ):
            continue

        asm_path = root / "asm" / f"{fn}.s"
        if not asm_path.is_file() or not _has_assembly_instructions(asm_path):
            continue
        decomp_seed = draft.read_decomp_seed(root, fn)
        candidates.append(
            (
                len(component),
                0 if fn in failed else 1,
                0 if decomp_seed is not None else 1,
                asm_path.stat().st_size,
                fn,
            )
        )
    candidates.sort()
    return [entry[4] for entry in candidates[:limit]]


def _has_dependency_blocked_candidates(
    root: pathlib.Path,
    function_names: set[str],
    attempted: Counter[str],
    max_attempts_per_function: int,
) -> bool:
    """Distinguish unresolved prerequisites from ordinary attempt exhaustion."""
    return bool(_dependency_blockers(
        root, function_names, attempted, max_attempts_per_function
    ))


def _dependency_blockers(
    root: pathlib.Path,
    function_names: set[str],
    attempted: Counter[str],
    max_attempts_per_function: int,
) -> list[dict]:
    """Describe unresolved direct routine dependencies without guessing targets."""
    graph, dependencies = _assembly_call_graph(root, function_names)
    recovered = _source_recovered_functions(root)
    component_for = {
        function_name: component
        for component in _dependency_components(dependencies)
        for function_name in component
    }
    blockers = []
    for fn in sorted(function_names):
        asm_path = root / "asm" / f"{fn}.s"
        if (
            attempted[fn] >= max_attempts_per_function
            or fn in recovered
            or not asm_path.is_file()
            or not _has_assembly_instructions(asm_path)
        ):
            continue
        component = component_for[fn]
        unresolved = _unresolved_external_dependencies(
            component, dependencies, component_for, recovered
        )
        if not unresolved:
            continue
        component_key = tuple(sorted(component))
        for edge in graph.edges.values():
            if edge.relation != "direct_call":
                continue
            call_site = graph.nodes[edge.source]
            caller = call_site.attributes["caller"]
            callee = graph.nodes[edge.target].attributes["name"]
            if caller not in component or callee not in unresolved:
                continue
            blockers.append(
                {
                    "function": fn,
                    "callee": callee,
                    "component": list(component_key),
                    "call_site": call_site.id,
                    "evidence_refs": list(edge.evidence_refs),
                }
            )
    return blockers


def _unresolved_call_targets(
    root: pathlib.Path, function_names: set[str]
) -> list[dict]:
    """Report unresolved calls separately from proven in-target dependencies."""
    graph, _ = _assembly_call_graph(root, function_names)
    return graph.unresolved_call_targets()


def _snapshot_source(root: pathlib.Path, target: str) -> dict[pathlib.Path, bytes]:
    source = root / "src"
    paths = set(source.glob("*.inc"))
    paths.add(source / f"{target}.pas")
    return {path: path.read_bytes() for path in paths if path.is_file()}


def _restore_source(
    root: pathlib.Path, target: str, snapshot: dict[pathlib.Path, bytes]
) -> None:
    source = root / "src"
    current = set(source.glob("*.inc"))
    current.add(source / f"{target}.pas")
    for path in current - snapshot.keys():
        if path.is_file():
            path.unlink()
    for path, contents in snapshot.items():
        path.write_bytes(contents)


def _example_count(data: dict) -> int:
    return sum(len(items) for items in data.get("examples", {}).values())


def _run_inputs(root: pathlib.Path, byod: pathlib.Path) -> list[pathlib.Path]:
    inputs = [
        root / "config" / "target.yaml",
        root / "config" / "toolchain.yaml",
        root / "functions.json",
        root / "config" / "routine_contracts.json",
        *sorted((root / "asm").glob("*.s")),
    ]
    binary = ingest.pick_binary(byod) if byod.is_dir() else None
    if binary:
        inputs.append(binary)
    return inputs


def _resume_attempt_history(run: run_state.RecoveryRun) -> tuple[
    Counter[str], set[str], dict[str, str]
]:
    attempted: Counter[str] = Counter()
    failed = set()
    repair_notes = {}
    for function_name, routine in run.data.get("routines", {}).items():
        attempts = routine.get("attempts", [])
        if not isinstance(attempts, list):
            raise TypeError(f"{function_name}: persisted attempts must be a list")
        attempted[function_name] = len(attempts)
        if not attempts:
            continue
        latest = attempts[-1]
        if latest.get("status") == "started":
            raise ValueError(
                f"{function_name}: interrupted attempt was not restored"
            )
        if latest.get("status") in {
            "candidate-rejected",
            "candidate-oracle-rejected",
            "candidate-oracle-blocked",
            "interrupted-restored",
        }:
            failed.add(function_name)
            diagnostics = latest.get("diagnostics", [])
            if diagnostics:
                repair_notes[function_name] = "\n".join(diagnostics[:12])
            elif latest.get("status") == "interrupted-restored":
                repair_notes[function_name] = (
                    "The prior generation was interrupted and its partial source "
                    "was restored. Generate a complete candidate from the assembly."
                )
        elif latest.get("status") in {
            "candidate-compiled",
            "candidate-scoped-pass",
        }:
            source = run.target_root / "src" / f"{function_name}.inc"
            source_hash = (
                hashlib.sha256(source.read_bytes()).hexdigest()
                if source.is_file()
                else None
            )
            if source_hash != latest.get("source_sha256"):
                raise ValueError(
                    f"{function_name}: compiled source changed since the run "
                    "was recorded"
                )
    return attempted, failed, repair_notes


def _empty_summary(target: str, reason: str) -> dict:
    return {
        "target": target,
        "iterations": 0,
        "functions_total": 0,
        "functions_generated": 0,
        "functions_meaningful": 0,
        "functions_compilable": 0,
        "whole_target_build_passed": False,
        "functions_verified": 0,
        "functions_binary_verified": 0,
        "functions_scoped_oracle_passed": 0,
        "function_oracle": None,
        "functions_source_recovered": None,
        "evidence_accounted_percent": None,
        "source_recovery_ledger": "not-audited",
        "functions_failed": 0,
        "candidate_failures": 0,
        "examples_added": 0,
        "failures_by_category": {},
        "saturated": False,
        "blocked": False,
        "dependency_blockers": [],
        "unresolved_call_targets": [],
        "errors": [],
        "stop_reason": reason,
    }


def _source_recovery_metrics(root: pathlib.Path) -> dict:
    """Report only reviewer-attested source recovery from the evidence ledger."""
    ledger_path = root / "recovery.json"
    if not ledger_path.is_file():
        return {
            "functions_source_recovered": None,
            "evidence_accounted_percent": None,
            "source_recovery_ledger": "missing",
        }

    summary = recovery.audit_target(root)["summary"]
    return {
        "functions_source_recovered": summary["source_recovered"],
        "evidence_accounted_percent": summary["evidence_accounted_percent"],
        "source_recovery_ledger": "present",
    }


def improve(
    target: str,
    byod: pathlib.Path | None = None,
    build: pathlib.Path | None = None,
    oracle: str | None = "dat-parity",
    model: str | None = None,
    endpoint: str | None = None,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    saturation_window: int = DEFAULT_SATURATION_WINDOW,
    functions_per_iteration: int = DEFAULT_FUNCTIONS_PER_ITERATION,
    max_attempts_per_function: int = DEFAULT_MAX_ATTEMPTS_PER_FUNCTION,
    resume_run_id: str | None = None,
    function_oracle: str | None = None,
    only_functions: set[str] | None = None,
    temperature: float = 0.0,
    localized_repair: bool = False,
) -> dict:
    """Iterate on Liero-style Pascal candidates, bounded by attempts and saturation.

    A candidate is retained only when it is meaningful and compiles in the
    full target context. When configured, a function-specific oracle is an
    additional strict gate; scoped passes do not certify whole-routine
    recovery.
    """
    if min(
        max_iterations,
        saturation_window,
        functions_per_iteration,
        max_attempts_per_function,
    ) < 1:
        raise ValueError("iteration and attempt limits must be positive")
    if not 0.0 <= temperature <= 2.0:
        raise ValueError("temperature must be between 0.0 and 2.0")
    if localized_repair and (
        function_oracle != "liero-compare-routine-probe"
        or max_attempts_per_function > 2
    ):
        raise ValueError(
            "localized repair requires the Liero routine oracle and at most "
            "two attempts per function"
        )

    root = (pathlib.Path("targets") / target).resolve()
    asm_dir = root / "asm"
    function_names = (
        {path.stem for path in asm_dir.glob("*.s")} if asm_dir.is_dir() else set()
    )
    if only_functions is not None:
        unknown = only_functions - function_names
        if unknown:
            raise ValueError(f"unknown assembly routine(s): {', '.join(sorted(unknown))}")
        function_names &= only_functions
    if function_oracle is not None:
        if function_oracle != "liero-compare-routine-probe":
            raise ValueError(f"unsupported function oracle: {function_oracle}")
        if target != "liero" or only_functions != {"FUN_24dd_3f86"}:
            raise ValueError(
                "liero-compare-routine-probe requires only FUN_24dd_3f86 on liero"
            )
        contract = draft.routine_contract.load_contract(
            root, "FUN_24dd_3f86"
        )
        if contract is None or contract["oracle"] != function_oracle:
            raise ValueError(
                "routine oracle does not match the checked routine contract"
            )
    language, _, _ = draft.detect_language(target)
    byod = byod or pathlib.Path(f"extracted/{target}")
    build = build or root / "build"
    effective_model = model or os.environ.get("LSR_LLM_MODEL") or DEFAULT_LOCAL_MODEL
    effective_endpoint = (
        endpoint
        or os.environ.get("LSR_LLM_ENDPOINT")
        or DEFAULT_LOCAL_ENDPOINT
    )
    run = run_state.open_run(
        root,
        _run_inputs(root, byod),
        {
            "stage": "improve",
            "oracle": oracle or "none",
            "model": effective_model,
            "endpoint": effective_endpoint,
            "max_iterations": max_iterations,
            "saturation_window": saturation_window,
            "functions_per_iteration": functions_per_iteration,
            "max_attempts_per_function": max_attempts_per_function,
            "temperature": temperature,
            "byod": str(byod.resolve()),
            "build": str(build.resolve()),
            "function_oracle": function_oracle,
            "only_functions": sorted(only_functions) if only_functions else None,
            "localized_repair": localized_repair,
        },
        run_id=resume_run_id,
    )
    if resume_run_id:
        stage = run.data.get("stages", {}).get("improve", {})
        if (
            isinstance(stage, dict)
            and stage.get("stop_reason") == "duplicate-candidate"
            and isinstance(stage.get("summary"), dict)
        ):
            return stage["summary"]
    run.data["status"] = "in_progress"
    run_state.update_stage(run, "improve", status="in_progress")
    for function_name, routine in run.data.get("routines", {}).items():
        for attempt in routine.get("attempts", []):
            if attempt.get("status") != "started":
                continue
            run_state.restore_interrupted_attempt(
                run, function_name, attempt["attempt"]
            )
            run_state.finish_attempt(
                run,
                function_name,
                attempt["attempt"],
                status="interrupted-restored",
                diagnostics=[
                    "Generation was interrupted; pre-attempt sources were restored."
                ],
            )
    if not function_names or language != "pascal":
        reason = (
            "no-assembly-functions"
            if not function_names
            else f"unsupported-language:{language}"
        )
        print(f"[improve:{target}] SKIP {reason}")
        summary = _empty_summary(target, reason)
        summary["run_id"] = run.run_id
        run.data["status"] = "completed"
        run_state.update_stage(
            run,
            "improve",
            status="completed",
            stop_reason=reason,
            summary=summary,
        )
        run_state.update_stage(run, "run", status="completed")
        return summary

    initial_data = knowledge.load()
    initial_examples = _example_count(initial_data)
    initial_meaningful = _meaningful_functions(root, function_names)
    compile_errors, compile_diagnostics = _compile_status(root)
    if compile_errors:
        message = "; ".join(compile_diagnostics) or ", ".join(sorted(compile_errors))
        print(f"[improve:{target}] BLOCKED: baseline build is not green: {message}")
        summary = _empty_summary(target, "baseline-build-failed")
        summary.update(
            functions_total=len(function_names),
            functions_generated=sum(
                (root / "src" / f"{fn}.inc").is_file() for fn in function_names
            ),
            functions_meaningful=len(initial_meaningful),
            candidate_failures=0,
            blocked=True,
            errors=[message],
        )
        run_state.update_stage(
            run,
            "improve",
            status="blocked",
            stop_reason="baseline-build-failed",
            errors=[message],
            summary=summary,
        )
        run.data["status"] = "blocked"
        run_state.update_stage(run, "run", status="blocked")
        summary["run_id"] = run.run_id
        return summary

    compiled_functions = set(initial_meaningful)
    attempted, failed, repair_notes = _resume_attempt_history(run)
    errors: list[str] = []
    candidate_failures = sum(
        attempt.get("status") in {
            "candidate-rejected",
            "candidate-oracle-rejected",
            "candidate-duplicate",
        }
        for routine in run.data.get("routines", {}).values()
        for attempt in routine.get("attempts", [])
    )
    scoped_oracle_passes = sum(
        attempt.get("status") == "candidate-scoped-pass"
        for routine in run.data.get("routines", {}).values()
        for attempt in routine.get("attempts", [])
    )
    iterations = 0
    no_gain_count = 0
    saturated = False
    blocked = False
    stop_reason = "maximum-iterations"

    for iteration in range(1, max_iterations + 1):
        candidates = _select_candidates(
            root,
            function_names,
            attempted,
            failed,
            max_attempts_per_function,
            functions_per_iteration,
        )
        if not candidates:
            dependency_blocked = _has_dependency_blocked_candidates(
                root,
                function_names,
                attempted,
                max_attempts_per_function,
            )
            stop_reason = (
                "unresolved-dependencies"
                if dependency_blocked
                else "no-eligible-candidates"
            )
            if dependency_blocked:
                print(
                    f"[improve:{target}] deferred callers with unresolved "
                    "direct callees; attest resolved callees before retrying"
                )
            break

        iterations = iteration
        print(f"\n=== improve:{target} iteration {iteration}/{max_iterations} ===")
        newly_compiled = 0
        for fn in candidates:
            attempted[fn] += 1
            previous_candidate = _previous_candidate(run, fn)
            snapshot = _snapshot_source(root, target)
            attempt = run_state.start_attempt(
                run,
                fn,
                attempted[fn],
                source_snapshot=snapshot,
            )
            generation_capture_dir = None
            if function_oracle:
                function_key = hashlib.sha256(fn.encode()).hexdigest()
                generation_capture_dir = (
                    run.path.parent
                    / f"{run.run_id}.generations"
                    / function_key
                    / f"attempt-{attempt['attempt']}"
                )
            workspace_context = (
                _candidate_workspace(root, target, byod)
                if function_oracle
                else nullcontext((None, root))
            )
            with workspace_context as (workspace, evaluation_root):
                candidate = evaluation_root / "src" / f"{fn}.inc"
                if previous_candidate is not None:
                    candidate.write_bytes(previous_candidate)
                use_localized_repair = (
                    localized_repair
                    and previous_candidate is not None
                    and repair_notes.get(fn, "").startswith(
                        "ORIGINAL-ORACLE FAILURE:"
                    )
                )
                try:
                    draft_rc = _draft(
                        target,
                        fn=fn,
                        model=model,
                        endpoint=endpoint,
                        retry_existing=candidate.is_file(),
                        repair_note=repair_notes.get(fn, ""),
                        cwd=workspace,
                        function_only=bool(function_oracle),
                        capture_dir=generation_capture_dir,
                        temperature=temperature,
                        localized_repair=use_localized_repair,
                    )
                except (OSError, subprocess.SubprocessError) as exc:
                    _restore_source(root, target, snapshot)
                    message = f"draft command failed for {fn}: {exc}"
                    generation_evidence = _generation_evidence(
                        root,
                        generation_capture_dir,
                        fn,
                        previous_candidate,
                        effective_model,
                        temperature,
                    )
                    run_state.finish_attempt(
                        run, fn, attempt["attempt"], status="blocked",
                        diagnostics=[message],
                        evidence={"generation": generation_evidence},
                    )
                    errors.append(message)
                    blocked = True
                    stop_reason = "draft-command-failed"
                    print(f"[improve:{target}] BLOCKED: {message}")
                    break

                generation_evidence = _generation_evidence(
                    root,
                    generation_capture_dir,
                    fn,
                    previous_candidate,
                    effective_model,
                    temperature,
                )
                if draft_rc != 0:
                    _restore_source(root, target, snapshot)
                    message = f"draft command returned {draft_rc} for {fn}"
                    run_state.finish_attempt(
                        run, fn, attempt["attempt"], status="blocked",
                        diagnostics=[message],
                        evidence={"generation": generation_evidence},
                    )
                    errors.append(message)
                    blocked = True
                    stop_reason = "draft-command-failed"
                    break

                if (
                    function_oracle
                    and generation_evidence["status"] != "captured"
                ):
                    _restore_source(root, target, snapshot)
                    message = (
                        f"generation input capture is "
                        f"{generation_evidence['status']} for {fn}"
                    )
                    run_state.finish_attempt(
                        run,
                        fn,
                        attempt["attempt"],
                        status="candidate-generation-blocked",
                        diagnostics=[message],
                        evidence={"generation": generation_evidence},
                    )
                    errors.append(message)
                    blocked = True
                    stop_reason = "generation-capture-invalid"
                    break

                meaningful = (
                    candidate.is_file()
                    and _has_pascal_implementation(candidate)
                )
                candidate_contents = candidate.read_bytes() if candidate.is_file() else b""
                candidate_hash = (
                    hashlib.sha256(candidate_contents).hexdigest()
                    if candidate_contents
                    else None
                )
                evidence: dict[str, Any] = {"generation": generation_evidence}
                candidate_path = None
                if candidate_contents:
                    candidate_path, persisted_hash = _persist_candidate(
                        run, fn, attempt["attempt"], candidate_contents
                    )
                    evidence.update(
                        candidate_path=candidate_path,
                        candidate_sha256=persisted_hash,
                    )

                duplicate_attempt = _duplicate_candidate_attempt(
                    run, fn, candidate_hash, attempt["attempt"]
                )
                if function_oracle and duplicate_attempt is not None:
                    message = (
                        f"candidate output repeats attempt {duplicate_attempt} "
                        f"(sha256 {candidate_hash}); stopping bounded repair"
                    )
                    evidence["duplicate_of_attempt"] = duplicate_attempt
                    _restore_source(root, target, snapshot)
                    candidate_failures += 1
                    failed.add(fn)
                    run_state.finish_attempt(
                        run,
                        fn,
                        attempt["attempt"],
                        status="candidate-duplicate",
                        diagnostics=[message],
                        source_sha256=candidate_hash,
                        evidence=evidence,
                    )
                    print(f"[improve:{target}] STOP: {message}")
                    stop_reason = "duplicate-candidate"
                    break

                candidate_errors, diagnostics = _compile_status(evaluation_root)
                if not candidate_errors and meaningful and function_oracle:
                    oracle_output = (
                        root
                        / "build"
                        / "comparator-parity"
                        / run.run_id
                        / fn
                        / f"attempt-{attempt['attempt']}"
                    )
                    try:
                        oracle_report = _run_function_oracle(
                            function_oracle, workspace, oracle_output
                        )
                    except (
                        OSError,
                        subprocess.SubprocessError,
                        RuntimeError,
                        ValueError,
                        KeyError,
                        TypeError,
                    ) as exc:
                        message = (
                            f"routine oracle infrastructure error for {fn}: "
                            f"{type(exc).__name__}: {exc}"
                        )
                        evidence["function_oracle"] = {
                            "name": function_oracle,
                            "status": "error",
                            "output_path": oracle_output.relative_to(root).as_posix(),
                        }
                        run_state.finish_attempt(
                            run,
                            fn,
                            attempt["attempt"],
                            status="candidate-oracle-blocked",
                            diagnostics=[message],
                            source_sha256=candidate_hash,
                            evidence=evidence,
                        )
                        errors.append(message)
                        blocked = True
                        stop_reason = "function-oracle-error"
                        break

                    oracle_status = oracle_report.get("status")
                    report_path = oracle_output / "result.json"
                    oracle_evidence: dict[str, Any] = {
                        "name": function_oracle,
                        "status": oracle_status,
                        "output_path": oracle_output.relative_to(root).as_posix(),
                        "case_count": oracle_report.get("case_count"),
                        "cases": oracle_report.get("cases", []),
                    }
                    if report_path.is_file():
                        oracle_evidence["report_sha256"] = hashlib.sha256(
                            report_path.read_bytes()
                        ).hexdigest()
                    evidence["function_oracle"] = oracle_evidence

                    if not report_path.is_file():
                        message = (
                            f"routine oracle did not persist its result report for {fn}"
                        )
                        oracle_evidence["status"] = "error"
                        run_state.finish_attempt(
                            run,
                            fn,
                            attempt["attempt"],
                            status="candidate-oracle-blocked",
                            diagnostics=[message],
                            source_sha256=candidate_hash,
                            evidence=evidence,
                        )
                        errors.append(message)
                        blocked = True
                        stop_reason = "function-oracle-report-missing"
                        break

                    if oracle_status == "failed":
                        mismatches = [
                            (
                                f"{case.get('name')}: expected flags "
                                f"0x{case.get('expected_flags', 0):04x}, got "
                                f"0x{case.get('candidate_flags', 0):04x}; "
                                f"stack_balanced={case.get('stack_balanced')}; "
                                f"memory_changed="
                                f"{case.get('candidate_memory_changed')}"
                            )
                            for case in oracle_report.get("cases", [])
                            if case.get("status") != "passed"
                        ]
                        message = "\n".join(mismatches) or (
                            "routine oracle reported failure without case details"
                        )
                        diagnostics = mismatches or [message]
                        repair_notes[fn] = (
                            "ORIGINAL-ORACLE FAILURE:\n" + message
                        )
                        failed.add(fn)
                        candidate_failures += 1
                        run_state.finish_attempt(
                            run,
                            fn,
                            attempt["attempt"],
                            status="candidate-oracle-rejected",
                            diagnostics=diagnostics[:12],
                            source_sha256=candidate_hash,
                            evidence=evidence,
                        )
                        print(
                            f"[improve:{target}] routine oracle FAIL: {fn}"
                        )
                        for diagnostic in diagnostics[:8]:
                            print(f"[improve:{target}] {diagnostic}")
                        continue

                    if oracle_status != "passed":
                        message = (
                            f"routine oracle returned {oracle_status!r} for {fn}; "
                            "candidate is not verified"
                        )
                        run_state.finish_attempt(
                            run,
                            fn,
                            attempt["attempt"],
                            status="candidate-oracle-blocked",
                            diagnostics=[message],
                            source_sha256=candidate_hash,
                            evidence=evidence,
                        )
                        errors.append(message)
                        blocked = True
                        stop_reason = "function-oracle-not-passed"
                        break

                    candidate_destination = root / "src" / f"{fn}.inc"
                    candidate_destination.write_bytes(candidate_contents)
                    installed_errors, installed_diagnostics = _compile_status(root)
                    if installed_errors:
                        _restore_source(root, target, snapshot)
                        message = (
                            "candidate passed in isolation but failed when installed: "
                            + (
                                "; ".join(installed_diagnostics)
                                or ", ".join(sorted(installed_errors))
                            )
                        )
                        failed.add(fn)
                        candidate_failures += 1
                        repair_notes[fn] = "\n".join(installed_diagnostics[:12])
                        run_state.finish_attempt(
                            run,
                            fn,
                            attempt["attempt"],
                            status="candidate-rejected",
                            diagnostics=installed_diagnostics[:12] or [message],
                            source_sha256=candidate_hash,
                            evidence=evidence,
                        )
                        print(f"[improve:{target}] {message}")
                        continue

                    scoped_oracle_passes += 1
                    evidence["function_oracle"]["status"] = "passed"
                    status = "candidate-scoped-pass"
                elif not candidate_errors and meaningful:
                    status = "candidate-compiled"
                else:
                    status = "candidate-rejected"

                if status in {"candidate-compiled", "candidate-scoped-pass"}:
                    if fn not in compiled_functions:
                        newly_compiled += 1
                    compiled_functions.add(fn)
                    failed.discard(fn)
                    repair_notes.pop(fn, None)
                    run_state.finish_attempt(
                        run,
                        fn,
                        attempt["attempt"],
                        status=status,
                        source_sha256=candidate_hash,
                        evidence=evidence or None,
                    )
                    print(f"[improve:{target}] routine compile PASS: {fn}")
                    continue

                _restore_source(root, target, snapshot)
                candidate_failures += 1
                failed.add(fn)
                if diagnostics:
                    repair_notes[fn] = "\n".join(diagnostics[:12])
                elif candidate_errors:
                    repair_notes[fn] = (
                        "Compiler reported failing routine(s): "
                        + ", ".join(sorted(candidate_errors))
                    )
                else:
                    repair_notes[fn] = (
                        "The previous output is still a generated skeleton, not a "
                        "meaningful Pascal implementation. Translate from the assembly."
                    )
                run_state.finish_attempt(
                    run,
                    fn,
                    attempt["attempt"],
                    status="candidate-rejected",
                    diagnostics=diagnostics[:12] or repair_notes[fn].splitlines(),
                    source_sha256=candidate_hash,
                    evidence=evidence or None,
                )
                print(
                    f"[improve:{target}] routine compile "
                    f"{'FAIL' if candidate_errors else 'SKIP'}: {fn}"
                )
                for diagnostic in diagnostics[:8]:
                    print(f"[improve:{target}] {diagnostic}")

                restored_errors, restored_diagnostics = _compile_status(root)
                if restored_errors:
                    message = (
                        "restoring the previous candidate did not recover the baseline "
                        "build: "
                        + ("; ".join(restored_diagnostics) or ", ".join(sorted(restored_errors)))
                    )
                    errors.append(message)
                    blocked = True
                    stop_reason = "rollback-build-failed"
                    print(f"[improve:{target}] BLOCKED: {message}")
                    break

                if "_MAKE_FAILED" in candidate_errors:
                    message = "; ".join(diagnostics) or "compiler infrastructure failed"
                    errors.append(message)
                    blocked = True
                    stop_reason = "compiler-unavailable"
                    break

        if blocked or stop_reason == "duplicate-candidate":
            break
        no_gain_count = 0 if newly_compiled else no_gain_count + 1
        if newly_compiled:
            print(f"[improve:{target}] added {newly_compiled} compilable routine(s)")
        if no_gain_count >= saturation_window:
            saturated = True
            stop_reason = "saturated"
            print(
                f"[improve:{target}] saturated: no new compilable routines for "
                f"{saturation_window} iterations"
            )
            break

    final_errors, final_diagnostics = _compile_status(root)
    whole_target_build_passed = not final_errors
    if final_errors:
        message = "; ".join(final_diagnostics) or ", ".join(sorted(final_errors))
        errors.append(f"final target build failed: {message}")
        compiled_functions.clear()
        blocked = True
        stop_reason = "final-build-failed"

    meaningful_functions = _meaningful_functions(root, function_names)
    if whole_target_build_passed:
        compiled_functions = meaningful_functions

    oracle_exit_code = None
    if oracle and oracle != "none":
        try:
            oracle_exit_code = _verify(target, byod, build, oracle=oracle)
        except (OSError, subprocess.SubprocessError) as exc:
            errors.append(f"{oracle} oracle command failed: {exc}")

    final_data = knowledge.load()
    binary_verified = _binary_verified_functions(final_data, target, function_names)
    failures_by_category = _summarise_failures(
        final_data, knowledge.compiler_key("turbo-pascal-7", "dos")
    )
    total_functions = len(function_names)
    generated_count = sum(
        (root / "src" / f"{fn}.inc").is_file() for fn in function_names
    )
    summary = {
        "target": target,
        "run_id": run.run_id,
        "iterations": iterations,
        "functions_total": total_functions,
        "functions_generated": generated_count,
        "functions_meaningful": len(meaningful_functions),
        "functions_compilable": len(compiled_functions),
        "whole_target_build_passed": whole_target_build_passed,
        "functions_verified": len(binary_verified),
        "functions_binary_verified": len(binary_verified),
        "functions_scoped_oracle_passed": scoped_oracle_passes,
        **_source_recovery_metrics(root),
        "functions_failed": candidate_failures,
        "candidate_failures": candidate_failures,
        "examples_added": max(0, _example_count(final_data) - initial_examples),
        "failures_by_category": failures_by_category,
        "oracle": oracle,
        "oracle_exit_code": oracle_exit_code,
        "function_oracle": function_oracle,
        "saturated": saturated,
        "blocked": blocked,
        "dependency_blockers": _dependency_blockers(
            root,
            function_names,
            attempted,
            max_attempts_per_function,
        ),
        "unresolved_call_targets": _unresolved_call_targets(
            root, function_names
        ),
        "errors": errors,
        "stop_reason": stop_reason,
    }
    run_state.update_stage(
        run,
        "improve",
        status="blocked" if blocked else "completed",
        stop_reason=stop_reason,
        iterations=iterations,
        summary=summary,
    )
    run.data["status"] = "blocked" if blocked else "completed"
    run_state.update_stage(run, "run", status=run.data["status"])
    return summary


def _summarise_failures(data: dict, toolchain: str) -> dict[str, int]:
    """Summarise failure counts by category from the knowledge store."""
    failures = data.get("compilers", {}).get(toolchain, {}).get("failures", {})
    return {category: entry.get("count", 0) for category, entry in failures.items()}


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Run the improve loop")
    parser.add_argument("--target", required=True)
    parser.add_argument("--byod", default=None)
    parser.add_argument("--build", default=None)
    parser.add_argument(
        "--oracle",
        default="dat-parity",
        choices=["none", *verify.ORACLES],
    )
    parser.add_argument(
        "--function-oracle",
        default=None,
        choices=["liero-compare-routine-probe"],
    )
    parser.add_argument(
        "--fn",
        action="append",
        default=None,
        help="restrict the improve run to this routine (repeatable)",
    )
    parser.add_argument("--model", default=None)
    parser.add_argument("--endpoint", default=None)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-iterations", type=int, default=DEFAULT_MAX_ITERATIONS)
    parser.add_argument(
        "--saturation-window", type=int, default=DEFAULT_SATURATION_WINDOW
    )
    parser.add_argument(
        "--functions-per-iteration",
        type=int,
        default=DEFAULT_FUNCTIONS_PER_ITERATION,
    )
    parser.add_argument(
        "--max-attempts-per-function",
        type=int,
        default=DEFAULT_MAX_ATTEMPTS_PER_FUNCTION,
    )
    parser.add_argument(
        "--resume-run",
        default=None,
        help="resume an improve run only when its input and configuration hashes match",
    )
    parser.add_argument(
        "--localized-repair",
        action="store_true",
        help=(
            "repair only the checked routine-contract region after an "
            "original-oracle failure (requires at most two attempts)"
        ),
    )
    args = parser.parse_args()
    result = improve(
        args.target,
        byod=pathlib.Path(args.byod) if args.byod else None,
        build=pathlib.Path(args.build) if args.build else None,
        oracle=None if args.oracle == "none" else args.oracle,
        model=args.model,
        endpoint=args.endpoint,
        max_iterations=args.max_iterations,
        saturation_window=args.saturation_window,
        functions_per_iteration=args.functions_per_iteration,
        max_attempts_per_function=args.max_attempts_per_function,
        resume_run_id=args.resume_run,
        function_oracle=args.function_oracle,
        only_functions=set(args.fn) if args.fn else None,
        temperature=args.temperature,
        localized_repair=args.localized_repair,
    )
    print(json.dumps(result, indent=2))
