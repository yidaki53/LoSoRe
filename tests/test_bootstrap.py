import hashlib
import json

import pytest

from engine import bootstrap, frozen_source_eval, knowledge, rtl_template
from tools import liero_source_trial as trial


ROUTINE = "FUN_24dd_4141"
ANSWER = "CopySkipHighCountLowForward"
NORMALIZE_ROUTINE = "FUN_24dd_455e"
ARITHMETIC_ROUTINE = "FUN_249c_0013"


class FakeInference:
    def __init__(self, answer: str):
        self.answer = answer
        self.prompts: list[str] = []
        self.config_sha256 = "test-config-sha256"

    def request(self, prompt: str, directory):
        self.prompts.append(prompt)
        directory.mkdir(parents=True, exist_ok=False)
        (directory / "request.json").write_text("{}")
        (directory / "response.raw").write_bytes(b"{}")
        metadata = {
            "status": "complete",
            "request_sha256": "test-request-sha256",
            "response_sha256": "test-response-sha256",
            "response_format": "raw-source",
        }
        (directory / "metadata.json").write_text(json.dumps(metadata))
        return json.dumps({"response": json.dumps({"source": self.answer})})


def _setup(tmp_path, routine=ROUTINE):
    root = tmp_path
    (root / "targets" / "liero" / "asm").mkdir(parents=True)
    (root / "targets" / "liero" / "src").mkdir(parents=True)
    (root / "targets" / "liero" / "config").mkdir(parents=True)
    (root / "knowledge").mkdir(parents=True)
    (root / "targets" / "liero" / "asm" / f"{routine}.s").write_text(
        "24dd:4141  CLD\n24dd:4142  RET\n"
    )
    (root / "targets" / "liero" / "config" / "toolchain.yaml").write_text(
        "compiler: turbo-pascal-7\nplatform: dos\n"
    )
    (root / "targets" / "liero" / "functions.json").write_text(
        json.dumps({"functions": [{"name": routine}], "num_functions": 1})
    )
    recovery = {"functions": {routine: {"status": "unreviewed"}}}
    (root / "targets" / "liero" / "recovery.json").write_text(json.dumps(recovery))
    store = root / "knowledge" / "knowledge.json"
    data = knowledge.load(store)
    key = knowledge.compiler_key("turbo-pascal-7", "dos")
    data["verified_pascal_examples"][key] = [{
        "example_id": "seed-example",
        "fn": "FUN_24dd_48e1",
        "target": "liero",
        "compiler": "turbo-pascal-7",
        "platform": "dos",
        "oracle": "routine-trace-parity",
        "asm": "24dd:48e1  CLD\n",
        "pascal": "procedure FUN_24dd_48e1(param_1: Word);\nbegin\nend;",
        "verification_status": "verified",
        "language": "pascal",
        "verified_at": "2026-11-22",
    }]
    knowledge.save(data, store)
    return root, store


def _passed_suite() -> dict:
    return {"original": {"status": "passed"}, "candidate": {"status": "passed"}}


def _normalize_hypothesis() -> dict:
    return {
        "magnitude": "signed_absolute",
        "exponent_bias": 160,
        "exponent_step": -1,
        "shift_direction": "left",
        "clear_fraction_top_bit": "positive",
        "zero_input": "preserve_cx",
        "evidence": dict(trial.NORMALIZE_BINDINGS),
    }


def test_bootstrap_promotes_only_after_training_and_terminal_parity(tmp_path, monkeypatch):
    root, store = _setup(tmp_path)
    fake = FakeInference(ANSWER)
    monkeypatch.setattr(bootstrap.trial, "compile_candidate", lambda *a, **k: {"status": "passed"})
    monkeypatch.setattr(
        frozen_source_eval, "run_training",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"training": _passed_suite()}},
    )
    terminal_calls = []

    def fake_run(*args, **kwargs):
        terminal_calls.append(args)
        return {"compile": {"status": "passed"}, "suites": {"terminal": _passed_suite()}}

    monkeypatch.setattr(frozen_source_eval, "run", fake_run)
    result = bootstrap.run_bootstrap(
        root, "liero", ROUTINE, tmp_path / "trials" / "bootstrap",
        methods=["bootstrap-packed-v1"],
        models=["qwen2.5-coder:1.5b"],
        identity={"name": "qwen2.5-coder:1.5b", "digest": "test-digest"},
        inference_factory=lambda _: fake,
    )

    assert result["status"] == "verified"
    assert len(result["promotions"]) == 1
    assert len(terminal_calls) == 1
    assert "FUN_24dd_48e1" in fake.prompts[0]
    source_path = root / "targets" / "liero" / "src" / f"{ROUTINE}.inc"
    assert source_path.is_file()
    recovery = json.loads((root / "targets" / "liero" / "recovery.json").read_text())
    assert recovery["functions"][ROUTINE]["status"] == "source_recovered"
    recovery_data = knowledge.load(store)
    assert ROUTINE in recovery_data["targets"]["liero"]["verified"]["routine-trace-parity"]
    assert recovery_data["total_verified"] == 1


def test_bootstrap_replaces_unverified_conflicting_source(tmp_path, monkeypatch):
    root, store = _setup(tmp_path)
    stale = "procedure stale;\nbegin\nend;\n"
    (root / "targets" / "liero" / "src" / f"{ROUTINE}.inc").write_text(stale)
    monkeypatch.setattr(bootstrap.trial, "compile_candidate", lambda *a, **k: {"status": "passed"})
    monkeypatch.setattr(
        frozen_source_eval, "run_training",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"training": _passed_suite()}},
    )
    monkeypatch.setattr(
        frozen_source_eval, "run",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"terminal": _passed_suite()}},
    )

    result = bootstrap.run_bootstrap(
        root, "liero", ROUTINE, tmp_path / "trials" / "bootstrap",
        methods=["bootstrap-packed-v1"],
        models=["qwen2.5-coder:1.5b"],
        identity={"name": "qwen2.5-coder:1.5b", "digest": "test-digest"},
        inference_factory=lambda _: FakeInference(ANSWER),
    )

    assert result["status"] == "verified"
    promotion = result["promotions"][0]
    assert promotion["status"] == "promoted"
    assert promotion["previous_source_sha256"] == hashlib.sha256(stale.encode()).hexdigest()
    archive = tmp_path / "trials" / "bootstrap" / "bootstrap-packed-v1" / "qwen2-5-coder-1-5b"
    assert (archive / "previous_source.inc").read_text() == stale
    assert ROUTINE in knowledge.load(store)["targets"]["liero"]["verified"]["routine-trace-parity"]


def test_bootstrap_refuses_verified_conflicting_source(tmp_path, monkeypatch):
    root, store = _setup(tmp_path)
    existing = "procedure verified_variant;\nbegin\nend;\n"
    (root / "targets" / "liero" / "src" / f"{ROUTINE}.inc").write_text(existing)
    data = knowledge.load(store)
    target = data.setdefault("targets", {}).setdefault("liero", {})
    target.setdefault("verified", {})["routine-trace-parity"] = [ROUTINE]
    knowledge.save(data, store)
    monkeypatch.setattr(bootstrap.trial, "compile_candidate", lambda *a, **k: {"status": "passed"})
    monkeypatch.setattr(
        frozen_source_eval, "run_training",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"training": _passed_suite()}},
    )
    monkeypatch.setattr(
        frozen_source_eval, "run",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"terminal": _passed_suite()}},
    )

    result = bootstrap.run_bootstrap(
        root, "liero", ROUTINE, tmp_path / "trials" / "bootstrap",
        methods=["bootstrap-packed-v1"],
        models=["qwen2.5-coder:1.5b"],
        identity={"name": "qwen2.5-coder:1.5b", "digest": "test-digest"},
        inference_factory=lambda _: FakeInference(ANSWER),
    )

    assert result["status"] == "promotion-conflict"
    assert result["promotions"][0]["status"] == "promotion-conflict"
    assert (root / "targets" / "liero" / "src" / f"{ROUTINE}.inc").read_text() == existing


def test_bootstrap_does_not_run_terminal_when_training_fails(tmp_path, monkeypatch):
    root, store = _setup(tmp_path)
    fake = FakeInference(ANSWER)
    monkeypatch.setattr(bootstrap.trial, "compile_candidate", lambda *a, **k: {"status": "passed"})
    monkeypatch.setattr(
        frozen_source_eval, "run_training",
        lambda *a, **k: {
            "compile": {"status": "passed"},
            "suites": {"training": {"original": {"status": "passed"}, "candidate": {"status": "failed"}}},
        },
    )
    terminal_calls = []
    monkeypatch.setattr(
        frozen_source_eval, "run",
        lambda *a, **k: terminal_calls.append(a),
    )

    result = bootstrap.run_bootstrap(
        root, "liero", ROUTINE, tmp_path / "trials" / "bootstrap",
        methods=["bootstrap-packed-v1"],
        models=["qwen2.5-coder:1.5b"],
        identity={"name": "qwen2.5-coder:1.5b", "digest": "test-digest"},
        inference_factory=lambda _: fake,
    )

    assert result["status"] == "blocked-no-training-pass"
    assert not terminal_calls
    assert not result["promotions"]
    recovery_data = knowledge.load(store)
    verified = recovery_data["targets"].get("liero", {}).get("verified", {}).get("routine-trace-parity", [])
    assert ROUTINE not in verified


def test_frozen_source_eval_training_only_never_runs_terminal(tmp_path, monkeypatch):
    root, _ = _setup(tmp_path)
    source_path = tmp_path / "candidate.inc"
    source_path.write_text(f"procedure {ROUTINE}(param_1: Word);\nbegin\nend;")
    monkeypatch.setattr(frozen_source_eval.trial, "cases", lambda *a: [b"x"])
    monkeypatch.setattr(
        frozen_source_eval.trial, "compile_candidate",
        lambda *a, **k: {"status": "passed"},
    )
    seen = []

    def fake_original(*args, **kwargs):
        seen.append("original")
        return {"status": "passed"}

    def fake_candidate(*args, **kwargs):
        seen.append("candidate")
        return {"status": "passed"}

    monkeypatch.setattr(frozen_source_eval.trial, "original", fake_original)
    monkeypatch.setattr(frozen_source_eval.trial, "run_candidate", fake_candidate)
    result = frozen_source_eval.run_training(
        root, tmp_path / "training", source_path, ROUTINE
    )

    assert set(result["suites"]) == {"training"}
    assert seen == ["original", "candidate"]


def test_move_forward_renderer_requires_move():
    declaration = "procedure FUN_24dd_3d68(param_1: Integer; param_2, param_3: Pointer);"
    source = rtl_template.render_move_forward_v2("FUN_24dd_3d68", declaration, "Move")
    assert "for i := 0 to count - 1 do dst[i] := src[i];" in source
    assert "RegisterSP := (RegisterSP + 14) and 65535;" in source
    assert "RegisterCarryFlag" not in source
    assert rtl_template.render_move_forward_v2("FUN_24dd_3d68", declaration, "FillChar") is None


def test_bootstrap_refuses_non_promoting_oracle(tmp_path):
    root, _ = _setup(tmp_path)
    with pytest.raises(ValueError):
        bootstrap.run_bootstrap(
            root, "liero", ROUTINE, tmp_path / "trials" / "bootstrap",
            oracle="dat-parity",
        )


def test_normalize_classifier_requires_closed_evidence():
    answer = json.dumps(_normalize_hypothesis(), sort_keys=True)
    assert json.loads(rtl_template.classify_normalize(answer)) == _normalize_hypothesis()
    mutant = _normalize_hypothesis()
    mutant["evidence"] = {}
    assert rtl_template.classify_normalize(json.dumps(mutant)) == "UNKNOWN"
    assert rtl_template.classify_normalize("not JSON") == "UNKNOWN"


def test_normalize_renderer_requires_supported_hypothesis():
    declaration = trial.routine_spec(NORMALIZE_ROUTINE)["signature"]
    answer = rtl_template.classify_normalize(
        json.dumps(_normalize_hypothesis(), sort_keys=True)
    )
    source = rtl_template.render_normalize(NORMALIZE_ROUTINE, declaration, answer)
    assert source is not None
    assert source.startswith(declaration + "\n")
    assert rtl_template.render_normalize(NORMALIZE_ROUTINE, declaration, "UNKNOWN") is None
    mutant = _normalize_hypothesis()
    mutant["magnitude"] = "unsigned"
    mutant_answer = rtl_template.classify_normalize(json.dumps(mutant))
    assert mutant_answer != "UNKNOWN"
    assert rtl_template.render_normalize(NORMALIZE_ROUTINE, declaration, mutant_answer) is None


def test_normalize_label_classifier_uses_closed_oracle_values():
    label = "signed_absolute|160|-1|left|positive|preserve_cx"
    assert rtl_template.classify_normalize_label(label) == label
    assert rtl_template.classify_normalize_label("```\n" + label + "\n```") == label
    assert rtl_template.classify_normalize_label("unsigned|160|-1|left|positive|preserve_cx") == (
        "unsigned|160|-1|left|positive|preserve_cx"
    )
    assert rtl_template.classify_normalize_label("not-a-label") == "UNKNOWN"


def test_normalize_label_renderer_requires_oracle_support():
    declaration = trial.routine_spec(NORMALIZE_ROUTINE)["signature"]
    label = "signed_absolute|160|-1|left|positive|preserve_cx"
    source = rtl_template.render_normalize_label(NORMALIZE_ROUTINE, declaration, label)
    assert source is not None
    assert source.startswith(declaration + "\n")
    unsupported = "unsigned|160|-1|left|positive|preserve_cx"
    assert rtl_template.render_normalize_label(NORMALIZE_ROUTINE, declaration, unsupported) is None
    assert rtl_template.render_normalize_label(NORMALIZE_ROUTINE, declaration, "UNKNOWN") is None


def test_bootstrap_normalize_promotes_only_after_training_and_terminal_parity(tmp_path, monkeypatch):
    root, store = _setup(tmp_path, NORMALIZE_ROUTINE)
    fake = FakeInference(json.dumps(_normalize_hypothesis(), sort_keys=True))
    monkeypatch.setattr(bootstrap.trial, "compile_candidate", lambda *a, **k: {"status": "passed"})
    monkeypatch.setattr(
        frozen_source_eval, "run_training",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"training": _passed_suite()}},
    )
    terminal_calls = []

    def fake_run(*args, **kwargs):
        terminal_calls.append(args)
        return {"compile": {"status": "passed"}, "suites": {"terminal": _passed_suite()}}

    monkeypatch.setattr(frozen_source_eval, "run", fake_run)
    result = bootstrap.run_bootstrap(
        root, "liero", NORMALIZE_ROUTINE, tmp_path / "trials" / "bootstrap",
        methods=["bootstrap-normalize-v1"],
        models=["qwen2.5-coder:1.5b"],
        identity={"name": "qwen2.5-coder:1.5b", "digest": "test-digest"},
        inference_factory=lambda _: fake,
    )

    assert result["status"] == "verified"
    assert len(result["promotions"]) == 1
    assert len(terminal_calls) == 1
    assert "register normalization" in fake.prompts[0].lower()
    assert "signed_absolute" in fake.prompts[0]
    assert "procedure FUN_24dd_455e" not in fake.prompts[0]
    source_path = root / "targets" / "liero" / "src" / f"{NORMALIZE_ROUTINE}.inc"
    assert source_path.is_file()
    assert NORMALIZE_ROUTINE in knowledge.load(store)["targets"]["liero"]["verified"]["routine-trace-parity"]


def test_arithmetic_label_classifier_uses_closed_oracle_values():
    label = "0|1|4|add|2|False"
    assert rtl_template.classify_arithmetic_label(label) == label
    assert rtl_template.classify_arithmetic_label("```\n" + label + "\n```") == label
    mutant = "0|1|8|add|2|False"
    assert rtl_template.classify_arithmetic_label(mutant) == mutant
    assert rtl_template.classify_arithmetic_label("not-a-label") == "UNKNOWN"


def test_arithmetic_label_renderer_requires_oracle_support():
    declaration = trial.routine_spec(ARITHMETIC_ROUTINE)["signature"]
    label = "0|1|4|add|2|False"
    source = rtl_template.render_arithmetic_label(ARITHMETIC_ROUTINE, declaration, label)
    assert source is not None
    assert source.startswith(declaration + "\n")
    mutant = "0|1|8|add|2|False"
    assert rtl_template.render_arithmetic_label(ARITHMETIC_ROUTINE, declaration, mutant) is None
    assert rtl_template.render_arithmetic_label(ARITHMETIC_ROUTINE, declaration, "UNKNOWN") is None


def test_bootstrap_arithmetic_label_promotes_only_after_parity(tmp_path, monkeypatch):
    root, store = _setup(tmp_path, ARITHMETIC_ROUTINE)
    label = "0|1|4|add|2|False"
    fake = FakeInference(label)
    monkeypatch.setattr(bootstrap.trial, "compile_candidate", lambda *a, **k: {"status": "passed"})
    monkeypatch.setattr(
        frozen_source_eval, "run_training",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"training": _passed_suite()}},
    )
    monkeypatch.setattr(
        frozen_source_eval, "run",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"terminal": _passed_suite()}},
    )
    result = bootstrap.run_bootstrap(
        root, "liero", ARITHMETIC_ROUTINE, tmp_path / "trials" / "bootstrap",
        methods=["bootstrap-arithmetic-v1"],
        models=["qwen2.5-coder:1.5b"],
        identity={"name": "qwen2.5-coder:1.5b", "digest": "test-digest"},
        inference_factory=lambda _: fake,
    )

    assert result["status"] == "verified"
    assert len(result["promotions"]) == 1
    assert "left_cell|right_cell|shift|operation|output_cell|truncate_before_add" in fake.prompts[0]
    assert "Schema" not in fake.prompts[0]
    assert ARITHMETIC_ROUTINE in knowledge.load(store)["targets"]["liero"]["verified"]["routine-trace-parity"]


def test_bootstrap_normalize_label_promotes_only_after_parity(tmp_path, monkeypatch):
    root, store = _setup(tmp_path, NORMALIZE_ROUTINE)
    label = "signed_absolute|160|-1|left|positive|preserve_cx"
    fake = FakeInference(label)
    monkeypatch.setattr(bootstrap.trial, "compile_candidate", lambda *a, **k: {"status": "passed"})
    monkeypatch.setattr(
        frozen_source_eval, "run_training",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"training": _passed_suite()}},
    )
    monkeypatch.setattr(
        frozen_source_eval, "run",
        lambda *a, **k: {"compile": {"status": "passed"}, "suites": {"terminal": _passed_suite()}},
    )
    result = bootstrap.run_bootstrap(
        root, "liero", NORMALIZE_ROUTINE, tmp_path / "trials" / "bootstrap",
        methods=["bootstrap-normalize-v2"],
        models=["qwen2.5-coder:1.5b"],
        identity={"name": "qwen2.5-coder:1.5b", "digest": "test-digest"},
        inference_factory=lambda _: fake,
    )

    assert result["status"] == "verified"
    assert len(result["promotions"]) == 1
    assert "magnitude|exponent_bias|exponent_step|shift_direction|clear_fraction_top_bit|zero_input" in fake.prompts[0]
    assert "Schema" not in fake.prompts[0]
    assert NORMALIZE_ROUTINE in knowledge.load(store)["targets"]["liero"]["verified"]["routine-trace-parity"]
