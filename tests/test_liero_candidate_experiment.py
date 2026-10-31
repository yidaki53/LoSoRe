import json
import sys
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import liero_candidate_experiment as experiment


def test_settings_matrix_has_eight_combinations():
    settings = experiment.build_settings_matrix(
        models=["model-a", "model-b"],
        prompt_profiles=["learned-context", "base-prompt"],
        temperatures=[0.0, 0.3],
        max_tokens=768,
    )

    assert len(settings) == 8
    assert len({
        (item.model, item.prompt_profile, item.temperature)
        for item in settings
    }) == 8


def test_function_panel_includes_requested_function_and_size_strata(tmp_path):
    asm = tmp_path / "asm"
    asm.mkdir()
    sizes = [1, 2, 3, 4, 5]
    for index, size in enumerate(sizes):
        name = f"FUN_{index:04d}"
        (asm / f"{name}.s").write_text(
            "0000:0000  RET\n" * size
        )

    panel = experiment.select_function_panel(
        tmp_path, requested_function="FUN_0002", panel_size=4
    )

    assert len(panel) == 4
    assert panel[0] == "FUN_0002"
    assert len(set(panel)) == 4
    assert panel[1:] == ["FUN_0000", "FUN_0003", "FUN_0004"]


def test_candidate_order_prioritizes_accepted_and_compiling_output():
    rows = [
        {"function": "FUN_1", "accepted": False, "candidate_build_passed": True},
        {"function": "FUN_1", "accepted": True, "candidate_build_passed": False},
        {"function": "FUN_1", "accepted": True, "candidate_build_passed": True},
    ]

    ordered = experiment.rank_candidates(rows)

    assert ordered == [rows[2], rows[1], rows[0]]


def test_experiment_refuses_nonlocal_inference_endpoint():
    with pytest.raises(ValueError, match="local Ollama"):
        experiment._local_api_root("https://example.invalid")


def test_trial_artifact_metadata_includes_hashes(tmp_path):
    asm_dir = tmp_path / "asm"
    asm_dir.mkdir()
    asm_file = asm_dir / "FUN_0001.s"
    asm_file.write_text("0000:0000  RET\n")

    result = experiment.input_fingerprints(tmp_path, "FUN_0001")

    assert result["assembly_sha256"]
    assert result["target_input_sha256"]
    assert Path(asm_file).is_file()


def test_mlflow_trial_logging_uses_saved_capture_artifacts(tmp_path):
    capture = tmp_path / "capture"
    capture.mkdir()
    (capture / "compiler_output.txt").write_text("compile output")
    events = []

    class FakeMlflow:
        def start_run(self, **_kwargs):
            return nullcontext()

        def log_params(self, _params):
            pass

        def set_tags(self, _tags):
            pass

        def log_metrics(self, _metrics):
            pass

        def log_artifacts(self, _path, artifact_path):
            events.append(("artifacts", artifact_path))

        def log_text(self, _text, artifact_file):
            events.append(("text", artifact_file))

        def active_run(self):
            return SimpleNamespace(info=SimpleNamespace(run_id="test-run"))

    row = {
        "run_name": "trial",
        "target": "liero",
        "function": "FUN_1",
        "settings": {
            "model": "local",
            "prompt_profile": "base-prompt",
            "temperature": 0.0,
            "max_tokens": 768,
        },
        "assembly_sha256": "assembly",
        "decomp_sha256": None,
        "baseline_source_sha256": "source",
        "prompt_sha256": "prompt",
        "generation_succeeded": True,
        "accepted": True,
        "candidate_changed": True,
        "candidate_build_attempted": True,
        "candidate_build_attempts": 1,
        "candidate_build_passed": True,
        "candidate_build_status": "passed",
        "compile_repair_attempts": 0,
        "generation_seconds": 0.1,
        "build_seconds": 0.2,
    }

    run_id = experiment._log_trial(
        FakeMlflow(), "experiment", row, capture, "inputs", "model"
    )

    assert run_id == "test-run"
    assert ("artifacts", "candidate") in events
    assert ("text", "trial.json") in events


@pytest.mark.parametrize(
    ("accepted", "change_candidate", "expected_status"),
    [
        (False, True, "skipped-rejected"),
        (True, False, "skipped-unchanged"),
    ],
)
def test_trial_skips_build_for_rejected_or_unchanged_candidate(
    tmp_path, monkeypatch, accepted, change_candidate, expected_status
):
    repo = tmp_path / "repo"
    target = repo / "targets/liero"
    (target / "src").mkdir(parents=True)
    candidate = target / "src/FUN_0001.inc"
    candidate.write_text("baseline")
    build_calls = []

    def fake_generation(command, **_kwargs):
        capture_dir = Path(command[command.index("--capture-dir") + 1])
        if change_candidate:
            candidate.write_text("draft")
        metadata_dir = capture_dir / "FUN_0001"
        metadata_dir.mkdir(parents=True)
        (metadata_dir / "capture.json").write_text(json.dumps({
            "sanitizer_accepted": accepted,
            "rejection_reason": None if accepted else "incomplete-routine",
        }))
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(experiment.subprocess, "run", fake_generation)
    monkeypatch.setattr(
        experiment,
        "_run_build",
        lambda _root: (build_calls.append(True) or (0, "", 0.1)),
    )

    result = experiment._run_trial(
        repo,
        "liero",
        "FUN_0001",
        experiment.TrialSettings("local-model", "base-prompt", 0.0, 128),
        "http://localhost:11434",
        tmp_path / "captures",
        repair_rounds=0,
    )

    assert build_calls == []
    assert result["candidate_build_attempted"] is False
    assert result["candidate_build_passed"] is None
    assert result["candidate_build_status"] == expected_status


def test_trial_repairs_candidate_using_function_compile_errors(
    tmp_path, monkeypatch
):
    repo = tmp_path / "repo"
    target = repo / "targets/liero"
    (target / "src").mkdir(parents=True)
    candidate = target / "src/FUN_0001.inc"
    candidate.write_text("baseline")
    commands = []
    build_calls = []
    compiler_error = (
        "FUN_0001.inc(3,4) Error: Wrong number of parameters\n"
        "_forward.inc(142,11) Error: Found declaration: FUN_0001;"
    )

    def fake_generation(command, **_kwargs):
        commands.append(command)
        candidate.write_text(f"draft-{len(commands)}")
        capture_dir = Path(command[command.index("--capture-dir") + 1])
        metadata_dir = capture_dir / "FUN_0001"
        metadata_dir.mkdir(parents=True)
        (metadata_dir / "capture.json").write_text(json.dumps({
            "sanitizer_accepted": True,
            "prompt_sha256": f"prompt-{len(commands)}",
        }))
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    def fake_build(_target):
        build_calls.append(True)
        if len(build_calls) == 1:
            return 1, compiler_error, 0.1
        return 0, "", 0.1

    monkeypatch.setattr(experiment.subprocess, "run", fake_generation)
    monkeypatch.setattr(experiment, "_run_build", fake_build)

    result = experiment._run_trial(
        repo,
        "liero",
        "FUN_0001",
        experiment.TrialSettings("local-model", "base-prompt", 0.0, 128),
        "http://localhost:11434",
        tmp_path / "captures",
        repair_rounds=1,
    )

    assert len(build_calls) == 2
    assert "--repair-note" in commands[1]
    assert commands[1][commands[1].index("--repair-note") + 1] == (
        "FUN_0001.inc(3,4) Error: Wrong number of parameters\n"
        "_forward.inc(142,11) Error: Found declaration: FUN_0001;"
    )
    assert result["candidate_build_attempts"] == 2
    assert result["compile_repair_attempts"] == 1
    assert result["initial_candidate_build_passed"] is False
    assert result["candidate_build_passed"] is True
    assert result["candidate_build_status"] == "passed"


def test_candidate_compile_diagnostics_ignore_other_functions():
    output = (
        "FUN_0002.inc(1,1) Error: unrelated failure\n"
        "FUN_0001.inc(3,4) Error: invalid pointer type\n"
        "_forward.inc(142,11) Error: Found declaration: FUN_0001;"
    )

    assert experiment._candidate_compile_diagnostics(output, "FUN_0001") == (
        "FUN_0001.inc(3,4) Error: invalid pointer type\n"
        "_forward.inc(142,11) Error: Found declaration: FUN_0001;"
    )


def test_scratch_copy_is_independent_of_repository_sources(tmp_path):
    for path in ("engine", "tools", "compilers", "targets/liero/src"):
        (tmp_path / path).mkdir(parents=True, exist_ok=True)
    (tmp_path / "targets/liero/src/FUN_0001.inc").write_text("baseline")
    (tmp_path / "knowledge").mkdir()
    (tmp_path / "knowledge/knowledge.json").write_text("{}")

    scratch = experiment._copy_scratch_repository(
        tmp_path, tmp_path / "scratch", "liero"
    )
    (scratch / "targets/liero/src/FUN_0001.inc").write_text("candidate")

    assert (tmp_path / "targets/liero/src/FUN_0001.inc").read_text() == "baseline"


def test_experiment_runs_trials_only_in_scratch_copy(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    target = repo / "targets/liero"
    for path in (
        "engine",
        "tools",
        "compilers",
        "targets/liero/asm",
        "targets/liero/src",
        "targets/liero/config",
        "knowledge",
    ):
        (repo / path).mkdir(parents=True, exist_ok=True)
    (target / "asm/FUN_0001.s").write_text("0000:0000  RET\n")
    (target / "src/FUN_0001.inc").write_text("original")
    (target / "config/toolchain.yaml").write_text("language: pascal\n")
    (repo / "knowledge/knowledge.json").write_text("{}")
    monkeypatch.setattr(experiment, "ROOT", repo)
    monkeypatch.setattr(
        experiment,
        "_ollama_model_digests",
        lambda _endpoint, models: {name: "digest" for name in models},
    )
    monkeypatch.setattr(experiment, "_run_build", lambda _target: (0, "", 0.1))
    mlflow_config = {}

    def set_tracking_uri(uri):
        mlflow_config["tracking_uri"] = uri

    class FakeMlflowClient:
        def __init__(self, tracking_uri):
            assert tracking_uri.startswith("sqlite:///")

        def get_experiment_by_name(self, _name):
            return None

        def create_experiment(self, name, artifact_location):
            mlflow_config["experiment_name"] = name
            mlflow_config["artifact_location"] = artifact_location
            return "test"

        def get_experiment(self, experiment_id):
            return SimpleNamespace(experiment_id=experiment_id)

    monkeypatch.setitem(
        sys.modules,
        "mlflow",
        SimpleNamespace(
            set_tracking_uri=set_tracking_uri,
            MlflowClient=FakeMlflowClient,
        ),
    )

    def fake_trial(repo_root, _target_name, function_name, _settings,
                   _endpoint, capture_dir, repair_rounds=1):
        assert repair_rounds == 1
        candidate = repo_root / "targets" / "liero" / "src" / f"{function_name}.inc"
        assert candidate.read_text() == "original"
        candidate.write_text("experimental candidate")
        return {
            "generation_succeeded": True,
            "generation_attempts": 1,
            "accepted": True,
            "rejection_reason": None,
            "prompt_sha256": "prompt",
            "completion_sha256": "completion",
            "candidate_sha256": "candidate",
            "llm_candidate_sha256": "candidate",
            "candidate_changed": True,
            "candidate_build_attempted": True,
            "candidate_build_attempts": 1,
            "candidate_build_passed": True,
            "initial_candidate_build_passed": True,
            "candidate_build_status": "passed",
            "compile_repair_attempts": 0,
            "build_return_code": 0,
            "generation_seconds": 0.1,
            "build_seconds": 0.1,
            "duration_seconds": 0.2,
            "generation_output": "",
            "compiler_output": "",
        }

    monkeypatch.setattr(experiment, "_run_trial", fake_trial)
    monkeypatch.setattr(experiment, "_log_trial", lambda *_args: "test-run")

    summary = experiment.run_experiment(
        target="liero",
        functions=["FUN_0001"],
        models=["local-model"],
        prompt_profiles=["base-prompt"],
        temperatures=[0.0, 0.3],
        tracking_dir=tmp_path / "tracking",
        output_dir=tmp_path / "reports",
        scratch_root=tmp_path / "scratch",
    )

    assert len(summary["trials"]) == 2
    assert all(
        row["accepted"] and row["candidate_build_passed"]
        for row in summary["trials"]
    )
    assert (target / "src/FUN_0001.inc").read_text() == "original"
    assert (tmp_path / "reports/summary.md").is_file()
    assert mlflow_config["tracking_uri"].startswith("sqlite:///")
    assert mlflow_config["artifact_location"].endswith("/tracking/artifacts")
