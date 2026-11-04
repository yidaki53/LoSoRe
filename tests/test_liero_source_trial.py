import hashlib
import json
import pathlib
import shutil
import struct
import sys

import pytest

from tools import liero_source_trial as trial

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("prototype", [False, True])
def test_prototype_cli_model_default_and_safe_existing_archive(
    tmp_path, monkeypatch, prototype
):
    """Oracle: exact preset default, old CLI unchanged; resume has zero requests."""
    output = tmp_path / "archive"
    argv = ["trial", "--output", str(output), "--routine", "FUN_249c_0013"]
    if prototype:
        argv += ["--prototype"]
    monkeypatch.setattr(sys, "argv", argv)
    captured = []
    monkeypatch.setattr(
        trial, "run", lambda *args: captured.append(args) or {"status": "fixture"}
    )
    monkeypatch.setattr(trial.shutil, "which", lambda name: name)
    assert trial.main() == 0
    assert captured[0][2] == (
        "qwen3:14b" if prototype else "qwen2.5-coder:14b-instruct"
    )
    if prototype:
        assert captured[0][-1] is True
        output.mkdir()
        (output / "artifacts.json").write_text("{}")
        monkeypatch.setattr(
            trial, "validate_artifacts", lambda *args, **kwargs: {"status": "replayed"}
        )
        assert trial.main() == 0
        assert len(captured) == 1
        (output / "artifacts.json").unlink()
        with pytest.raises(SystemExit):
            trial.main()
        assert len(captured) == 1


DISCOVERY_CONTROL = """procedure FUN_24dd_4141(param_1: Word; param_2, param_3: Pointer);
var src, dst: PByte; count, skip, i: LongInt;
begin
  count := param_1 and 255; skip := param_1 shr 8;
  src := PByte(param_3); dst := PByte(param_2);
  for i := 0 to count - 1 do dst[i] := src[skip+i];
  RegisterBX := param_1; RegisterDX := RegisterDS; RegisterES := RegisterDS;
  RegisterCarryFlag := LongInt(RegisterSI) + skip > 65535;
  RegisterZeroFlag := ((LongInt(RegisterSI) + skip) and 65535) = 0;
  RegisterSI := (LongInt(RegisterSI) + skip + count) and 65535;
  RegisterDI := (LongInt(RegisterDI) + count) and 65535;
  RegisterCX := 0; RegisterDirectionFlag := False;
  RegisterSP := (LongInt(RegisterSP) + 14) and 65535;
end;
"""

PACKED_HYPOTHESIS = {
    "source_start": "high_byte",
    "destination_start": "zero",
    "count": "low_byte",
    "step": 1,
    "access_order": "copy_then_step",
    "zero_count": "no_access",
    "evidence": {
        "source_start": "4152 MOV CL,BH;4154 XOR CH,CH;4156 ADD SI,CX",
        "count": "4158 MOV CL,BL",
        "transfer": "4141 CLD;415a REP MOVSB",
    },
}

ARITHMETIC_HYPOTHESIS = {
    "left_cell": 0,
    "right_cell": 1,
    "shift": 4,
    "operation": "add",
    "output_cell": 2,
    "truncate_before_add": False,
    "evidence": trial.ARITHMETIC_BINDINGS,
}
NORMALIZE_HYPOTHESIS = {
    "magnitude": "signed_absolute",
    "exponent_bias": 160,
    "exponent_step": -1,
    "shift_direction": "left",
    "clear_fraction_top_bit": "positive",
    "zero_input": "preserve_cx",
    "evidence": trial.NORMALIZE_BINDINGS,
}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("magnitude", "unsigned"),
        ("exponent_bias", 144),
        ("exponent_step", 1),
        ("shift_direction", "right"),
        ("clear_fraction_top_bit", "negative"),
        ("zero_input", "replace_ch"),
    ],
)
def test_normalization_actions_and_mutants(field, value):
    """Oracle: signed32-bit magnitude, edge/zero/minimum, exponent/fraction and near frame."""
    routine = "FUN_24dd_455e"
    inputs = trial.cases(routine, "training")
    records = b"".join(trial.expected(routine, row, 0x2000) for row in inputs)
    assert (
        trial.check_normalize_interpretation(NORMALIZE_HYPOTHESIS, inputs, records)[
            "status"
        ]
        == "passed"
    )
    mutant = {**NORMALIZE_HYPOTHESIS, field: value}
    assert (
        trial.check_normalize_interpretation(mutant, inputs, records)["status"]
        == "contradicted"
    )
    with pytest.raises(ValueError, match="unsupported normalization"):
        trial.lower_normalize_interpretation(mutant)
    assert "pushw input" not in trial.harness(routine)
    assert "mov input, %ax" in trial.harness(routine)
    assert "RegisterAX := input[0]" in trial.program(routine)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("left_cell", 1),
        ("right_cell", 0),
        ("shift", 8),
        ("operation", "or"),
        ("output_cell", 1),
        ("truncate_before_add", True),
    ],
)
def test_structured_arithmetic_actions_and_mutants(field, value):
    """Oracle: exact byte/AX/full-memory contract, not supplied model answers."""
    routine = "FUN_249c_0013"
    inputs = trial.cases(routine, "training")
    records = b"".join(trial.expected(routine, row, 0x2000) for row in inputs)
    assert (
        trial.check_arithmetic_interpretation(ARITHMETIC_HYPOTHESIS, inputs, records)[
            "status"
        ]
        == "passed"
    )
    mutant = {**ARITHMETIC_HYPOTHESIS, field: value}
    assert (
        trial.check_arithmetic_interpretation(mutant, inputs, records)["status"]
        == "contradicted"
    )
    with pytest.raises(ValueError, match="unsupported arithmetic"):
        trial.lower_arithmetic_interpretation(mutant)


@pytest.mark.parametrize("shift", [4, 8])
def test_near_ss_arithmetic_control_and_mutant(tmp_path, shift):
    """Oracle: supplied arithmetic control validates different-behavior near SS fixture."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    routine = "FUN_249c_0013"
    source = f"""procedure FUN_249c_0013(param_1: Word; param_2: Pointer);
var p: PByte; value: LongInt;
begin
  p := PByte(param_2);
  value := (LongInt(p[0]) shl {shift}) + p[1];
  RegisterAX := value and 65535; RegisterDX := p[1]; RegisterDI := param_1;
  p[2] := value and 255;
  RegisterCarryFlag := value > 65535; RegisterZeroFlag := (value and 65535) = 0;
  RegisterSP := (RegisterSP + 4) and 65535;
end;
"""
    assert (
        trial.compile_candidate(ROOT, tmp_path / "candidate", routine, source)["status"]
        == "passed"
    )
    result = trial.run_candidate(
        tmp_path / "candidate", routine, trial.cases(routine, "training")
    )
    assert result["status"] == ("passed" if shift == 4 else "failed")
    assert "push %cs\n    call original" not in trial.harness(routine)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_start", "low_byte"),
        ("destination_start", "high_byte"),
        ("count", "word"),
        ("step", -1),
        ("access_order", "step_then_copy"),
        ("zero_count", "one_access"),
    ],
)
def test_packed_interpretation_mutants_fail_byte_and_memory_checks(field, value):
    """Oracle: supplied hypotheses test independent checker; never model recovery credit."""
    routine = "FUN_24dd_4141"
    inputs = trial.cases(routine, "training")
    records = b"".join(trial.expected(routine, row, 0x2000) for row in inputs)
    assert (
        trial.check_packed_interpretation(PACKED_HYPOTHESIS, inputs, records)["status"]
        == "passed"
    )
    mutant = {**PACKED_HYPOTHESIS, field: value}
    result = trial.check_packed_interpretation(mutant, inputs, records)
    assert result["instruction_status"] == "contradicted"
    assert result["memory_status"] == "contradicted"
    with pytest.raises(ValueError, match="unsupported packed"):
        trial.lower_packed_interpretation(mutant)


def test_packed_citations_and_mechanical_lowering_full_state(tmp_path):
    """Oracle: typed control execution and citation mutation, not live model generalization."""
    routine = "FUN_24dd_4141"
    inputs = trial.cases(routine, "training")
    records = b"".join(trial.expected(routine, row, 0x2000) for row in inputs)
    mutant = {
        **PACKED_HYPOTHESIS,
        "evidence": {**PACKED_HYPOTHESIS["evidence"], "transfer": "415a"},
    }
    assert (
        trial.check_packed_interpretation(mutant, inputs, records)["instruction_status"]
        == "contradicted"
    )
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    source = trial.compose_residual(
        trial.lower_packed_interpretation(PACKED_HYPOTHESIS), routine
    )
    assert (
        trial.compile_candidate(ROOT, tmp_path / "candidate", routine, source)["status"]
        == "passed"
    )
    assert (
        trial.run_candidate(tmp_path / "candidate", routine, inputs)["status"]
        == "passed"
    )


def test_packed_checked_pipeline_generates_only_one_interpretation_request(
    tmp_path, monkeypatch
):
    """Oracle: supplied hypothesis and synthetic original records exercise orchestration, not live recovery."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    routine = "FUN_24dd_4141"
    requests = []

    def propose(text, model, endpoint, **kwargs):
        requests.append(kwargs)
        assert kwargs["schema"] == trial.PACKED_SCHEMA
        return json.dumps({"response": json.dumps({"hypotheses": [PACKED_HYPOTHESIS]})})

    def synthetic_original(root, output, routine, inputs):
        output.mkdir(parents=True)
        (output / "CASES.BIN").write_bytes(b"".join(inputs))
        (output / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(routine, row, 0x2000) for row in inputs)
        )

    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"name": "fixture"}
    )
    monkeypatch.setattr(trial.pilot, "request", propose)
    monkeypatch.setattr(trial, "original", synthetic_original)
    output = tmp_path / "trial"
    result = trial.run(
        ROOT,
        output,
        "fixture",
        "http://localhost:11434",
        routines=(routine,),
        enforce_outputs=True,
        residual=True,
        interpretation_first=True,
    )
    assert result["model_requests"] == 1
    assert len(requests) == 1 and requests[0]["max_generated_tokens"] == 4096
    assert result["routines"][routine]["attempts"][0]["model_request"] is False
    assert result["binary_terminal_passes"] == 1
    assert result["accepted_source_recoveries"] == 0
    assert trial.validate_artifacts(ROOT, output) == result


@pytest.mark.parametrize(
    ("routine", "hypothesis"),
    [
        ("FUN_249c_0013", ARITHMETIC_HYPOTHESIS),
        ("FUN_24dd_455e", NORMALIZE_HYPOTHESIS),
    ],
)
def test_arithmetic_pipeline_export_and_mutation_rejection(
    tmp_path, monkeypatch, routine, hypothesis
):
    """Oracle: synthetic orchestration and real compiler; never substitute for live model trial."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    requests = []

    def propose(*args, **kwargs):
        requests.append(kwargs)
        assert kwargs["schema"] == trial.structured_schema(routine)
        return json.dumps({"response": json.dumps({"hypotheses": [hypothesis]})})

    def synthetic_original(root, output, name, inputs):
        output.mkdir(parents=True)
        (output / "CASES.BIN").write_bytes(b"".join(inputs))
        (output / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(name, row, 0x2000) for row in inputs)
        )

    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"name": "fixture"}
    )
    monkeypatch.setattr(trial.pilot, "request", propose)
    monkeypatch.setattr(trial, "original", synthetic_original)
    archive = tmp_path / "trial"
    result = trial.run(
        ROOT,
        archive,
        "fixture",
        "http://localhost:11434",
        routines=(routine,),
        enforce_outputs=True,
        interpretation_first=True,
        thinking=True,
    )
    assert result["model_requests"] == 1 and result["binary_terminal_passes"] == 1
    assert len(requests) == 1 and requests[0]["max_generated_tokens"] == 8192
    assert trial.validate_artifacts(ROOT, archive) == result
    source = archive / routine / "attempt-1/candidate.inc"
    review = {
        "routine": routine,
        "source_sha256": trial.pilot.digest(source),
        "status": "accepted-scoped-composition",
        "scope": "Test fixture only",
        "review": ["Test review, not recovery evidence"],
        "obligations": ["Native ABI"],
        "whole_routine_accepted": False,
    }
    trial.pilot.save(archive / "source-review.json", review)
    destination = tmp_path / "export"
    manifest = trial.export_trial(ROOT, archive, destination)
    assert (
        manifest["routines"][routine]["review_status"] == "accepted-scoped-composition"
    )
    assert manifest["export_model_requests"] == 0 and not manifest["weights_changed"]
    assert trial.validate_export(ROOT, destination)["new_model_requests"] == 0
    assert len(requests) == 1
    assert not list(destination.rglob("*.COM")) and not list(
        destination.rglob("LIERO.EXE")
    )
    trial.pilot.save(
        destination / "manifest.json", {**manifest, "weights_changed": True}
    )
    with pytest.raises(ValueError, match="cannot claim"):
        trial.validate_export(ROOT, destination)
    trial.pilot.save(destination / "manifest.json", manifest)
    copied = destination / "evidence" / routine / "attempt-1/candidate.inc"
    copied.write_text(copied.read_text() + "\n{ changed }\n")
    with pytest.raises(ValueError, match="export evidence changed"):
        trial.validate_export(ROOT, destination)
    trial.pilot.save(
        archive / "source-review.json", {**review, "source_sha256": "incorrect"}
    )
    with pytest.raises(ValueError, match="source review"):
        trial.export_trial(ROOT, archive, tmp_path / "bad-export")
    assert not (tmp_path / "bad-export").exists()
    with pytest.raises(ValueError, match="outside"):
        trial.export_trial(ROOT, archive, archive / "nested")


def test_packed_evidence_completion_cannot_change_actions(tmp_path, monkeypatch):
    """Oracle: one supplied citation response preserves immutable prior memory actions."""
    routine = "FUN_24dd_4141"
    inputs = trial.cases(routine, "training")
    records = b"".join(trial.expected(routine, row, 0x2000) for row in inputs)
    context = {"routine": routine, "hypothesis": PACKED_HYPOTHESIS}

    def propose(*args, **kwargs):
        assert kwargs["schema"]["required"] == ["source_start", "count", "transfer"]
        return json.dumps({"response": json.dumps(PACKED_HYPOTHESIS["evidence"])})

    monkeypatch.setattr(trial.pilot, "request", propose)
    result = trial.complete_binding(
        tmp_path / "binding",
        "fixture",
        "http://localhost:11434",
        "evidence only",
        context,
        inputs,
        records,
    )
    assert result["selected"] == PACKED_HYPOTHESIS
    assert result["model_requests"] == 1


def test_supplied_bindings_freeze_facts_not_action_choices(tmp_path, monkeypatch):
    """Oracle: byte-derived citation assistance leaves every model behavioral alternative available."""
    schema = trial.packed_schema(True)
    properties = schema["properties"]["hypotheses"]["items"]["properties"]
    for name, values in trial.PACKED_FIELDS.items():
        assert properties[name]["enum"] == values
        assert "const" not in properties[name]
    for name, value in trial.PACKED_BINDINGS.items():
        assert properties["evidence"]["properties"][name]["const"] == value
    hypothesis = {**PACKED_HYPOTHESIS, "evidence": trial.PACKED_BINDINGS}
    inputs = trial.cases("FUN_24dd_4141", "training")
    records = b"".join(trial.expected("FUN_24dd_4141", row, 0x2000) for row in inputs)
    assert (
        trial.check_packed_interpretation(hypothesis, inputs, records)["status"]
        == "passed"
    )
    wrong = {**hypothesis, "count": "high_byte"}
    assert (
        trial.check_packed_interpretation(wrong, inputs, records)["status"]
        == "contradicted"
    )
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"name": "fixture"}
    )
    output = tmp_path / "freeze"
    frozen = trial.freeze(
        ROOT,
        output,
        "fixture",
        "http://localhost:11434",
        routines=("FUN_24dd_4141",),
        residual=True,
        interpretation_first=True,
        enforce_outputs=True,
        supplied_bindings=True,
    )
    assert frozen["interpretation_first"]["schema"] == schema
    assert frozen["supplied_instruction_bindings"] == trial.PACKED_BINDINGS
    assert frozen["interpretation_first"]["prompt_sha256"] == trial.pilot.digest(
        output / "interpretation.prompt.txt"
    )


@pytest.mark.parametrize("skip", ["argument shr 8", "0"])
def test_packed_residual_composes_full_state_not_just_memory(tmp_path, skip):
    """Oracle: supplied residual controls validate deterministic ABI partition, not model credit."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    routine = "FUN_24dd_4141"
    body = f"""var p, q: PByte; i, count, skip: LongInt;
begin
  p := PByte(source); q := PByte(destination);
  count := argument and 255; skip := {skip};
  for i := 0 to count - 1 do q[i] := p[skip+i];
end;
"""
    source = trial.compose_residual(body, routine)
    assert (
        trial.compile_candidate(ROOT, tmp_path / "candidate", routine, source)["status"]
        == "passed"
    )
    result = trial.run_candidate(
        tmp_path / "candidate", routine, trial.cases(routine, "training")
    )
    assert result["status"] == ("passed" if skip != "0" else "failed")
    assert (
        "Register"
        not in trial.residual_prompt(ROOT, routine).split("Original bytes:")[1]
    )
    with pytest.raises(ValueError, match="without ABI"):
        trial.compose_residual("begin RegisterSP := 0; end;", routine)


def test_typed_guidance_is_opt_in_and_freezes_actual_prompt(tmp_path, monkeypatch):
    """Oracle: exact frozen assistance, token limit and prompt identities; not semantic recovery."""
    routine = "FUN_24dd_4141"
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"name": "test"}
    )
    output = tmp_path / "trial"
    frozen = trial.freeze(
        ROOT,
        output,
        "test",
        "http://localhost:11434",
        routines=(routine,),
        enforce_outputs=True,
        typed_memory_guidance=True,
    )
    text = (output / f"{routine}.prompt.txt").read_text()
    assert "destination[index] := source[expression]" in text
    assert "Low/High return TYPE bounds" in text
    assert DISCOVERY_CONTROL not in text
    assert frozen["budgets"]["maximum_generated_tokens"] == 4096
    assert frozen["prompt_hashes"][routine] == trial.pilot.digest(
        output / f"{routine}.prompt.txt"
    )
    assert "Typed Pascal representation guidance" not in trial.trial_prompt(
        ROOT, routine, "", True
    )
    with pytest.raises(ValueError, match="single4141"):
        trial.freeze(
            ROOT,
            tmp_path / "invalid",
            "test",
            "http://localhost:11434",
            routines=("FUN_24dd_48e1",),
            enforce_outputs=True,
            typed_memory_guidance=True,
        )


def test_request_transmits_explicit_budget_and_preserves_default(monkeypatch):
    """Oracle: actual serialized Ollama request, no live generation."""
    payloads = []

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self):
            return b'{"response":"{}"}'

    def capture(request, timeout):
        payloads.append(json.loads(request.data))
        assert timeout == 600
        return Response()

    monkeypatch.setattr(trial.pilot.urllib.request, "urlopen", capture)
    trial.pilot.request("test", "model", "http://localhost:11434")
    trial.pilot.request(
        "test", "model", "http://localhost:11434", max_generated_tokens=4096
    )
    assert [p["options"]["num_predict"] for p in payloads] == [2048, 4096]
    assert all("think" not in p for p in payloads)
    trial.pilot.request("test", "model", "http://localhost:11434", think=True)
    assert payloads[-1]["think"] is True
    with pytest.raises(ValueError, match="thinking setting"):
        trial.pilot.request("test", "model", "http://localhost:11434", think="true")
    for invalid in (0, -1, True):
        with pytest.raises(ValueError, match="positive integer"):
            trial.pilot.request(
                "test", "model", "http://localhost:11434", max_generated_tokens=invalid
            )


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("", ""),
        ("skip := param_1 shr 8", "skip := 0"),
        ("count := param_1 and 255", "count := 1"),
        ("for i := 0 to count - 1", "for i := count - 1 downto 0"),
        ("RegisterBX := param_1", "RegisterBX := RegisterSP"),
        ("RegisterDX := RegisterDS", "RegisterDX := 0"),
        (
            "RegisterZeroFlag := ((LongInt(RegisterSI) + skip) and 65535) = 0",
            "RegisterZeroFlag := True",
        ),
        ("RegisterSP := (LongInt(RegisterSP) + 14) and 65535", "RegisterSP := 0"),
    ],
)
def test_new_unresolved_packed_copy_exact_output_shape(tmp_path, old, new):
    """Oracle: supplied control tests new packed-byte fixture, not live model recovery."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    routine = "FUN_24dd_4141"
    source = DISCOVERY_CONTROL
    if old:
        source = source.replace(old, new)
    assert (
        trial.compile_candidate(ROOT, tmp_path / "candidate", routine, source)["status"]
        == "passed"
    )
    assessment = trial.run_candidate(
        tmp_path / "candidate", routine, trial.cases(routine, "training")
    )
    assert assessment["status"] == ("failed" if old else "passed")
    obligations = trial.output_obligations(
        routine, bytes.fromhex(trial.routine_spec(routine)["bytes"])
    )
    assert obligations["outputs"]["RegisterBX"] == "packed param_1, not entry SP"
    assert "MOV DS,DX" in trial.instruction_listing(ROOT, routine)
    assert "high byte is unsigned source skip" in trial.prompt(ROOT, routine)
    assert routine not in trial.PANEL


INTERPRETATION_CONTROL = {
    "condition": "source_lt_destination",
    "zero_count": "no_access",
    "forward_start": "zero",
    "backward_start": "count_minus_one",
    "forward_step": 1,
    "backward_step": -1,
    "access_order": "copy_then_step",
    "repeat": "count_times",
    "evidence": {
        "branch": "48f2 CMP and48f4JNC",
        "setup": "48f6ADD48faDEC48fcSTD",
        "transfer": "48fdREP",
    },
}


@pytest.mark.parametrize("field", list(trial.INTERPRETATION_FIELDS))
def test_interpretation_checks_each_memory_alternative(field):
    """Oracle: synthetic original-state rows and exact-byte instruction constraints."""
    inputs = trial.cases("FUN_24dd_48e1", "training")
    records = b"".join(trial.expected("FUN_24dd_48e1", row, 0x2000) for row in inputs)
    assert (
        trial.check_interpretation(INTERPRETATION_CONTROL, inputs, records)["status"]
        == "passed"
    )
    mutant = {
        **INTERPRETATION_CONTROL,
        field: next(
            value
            for value in trial.INTERPRETATION_FIELDS[field]
            if value != INTERPRETATION_CONTROL[field]
        ),
    }
    checked = trial.check_interpretation(mutant, inputs, records)
    assert checked["status"] == "contradicted"
    assert checked["instruction_conflicts"]
    assert checked["probability_correct"] is None


def test_interpretation_retains_competing_hypotheses_and_training_counterexamples(
    tmp_path, monkeypatch
):
    """Oracle: scripted hypotheses, no live model or native recovery."""
    inputs = trial.cases("FUN_24dd_48e1", "training")
    records = b"".join(trial.expected("FUN_24dd_48e1", row, 0x2000) for row in inputs)
    wrong = {**INTERPRETATION_CONTROL, "backward_step": 1}

    def request(*args, **kwargs):
        """Oracle: two retained competing hypotheses."""
        assert kwargs["schema"] == trial.INTERPRETATION_SCHEMA
        return json.dumps(
            {"response": json.dumps({"hypotheses": [wrong, INTERPRETATION_CONTROL]})}
        )

    monkeypatch.setattr(trial.pilot, "request", request)
    result = trial.interpret_memory(
        ROOT, tmp_path / "interpretation", "scripted", "local", inputs, records
    )
    assert result["selected"] == INTERPRETATION_CONTROL
    assert result["model_requests"] == 1
    assert result["history"][0]["hypotheses"][0]["assessment"]["counterexamples"]


def test_interpretation_rejects_changed_bytes_and_unauthenticated_state(monkeypatch):
    """Oracle: byte and original fixture mutations cannot support interpretations."""
    inputs = trial.cases("FUN_24dd_48e1", "training")
    records = b"".join(trial.expected("FUN_24dd_48e1", row, 0x2000) for row in inputs)
    mutated = bytearray(records)
    mutated[0] ^= 1
    with pytest.raises(ValueError, match="complete fixture"):
        trial.check_interpretation(INTERPRETATION_CONTROL, inputs, bytes(mutated))
    monkeypatch.setitem(
        trial.PANEL,
        "FUN_24dd_48e1",
        {
            **trial.PANEL["FUN_24dd_48e1"],
            "bytes": "00" * 36,
        },
    )
    with pytest.raises(ValueError, match="byte identity"):
        trial.check_interpretation(INTERPRETATION_CONTROL, inputs, records)


RESIDUAL_CONTROL = """var s, d: PByte; i: LongInt;
begin
  s := PByte(source); d := PByte(destination);
  if backward and (count > 0) then begin
    Inc(s, count - 1); Inc(d, count - 1);
  end;
  for i := 1 to count do begin
    d^ := s^;
    if backward then begin Dec(s); Dec(d) end
    else begin Inc(s); Inc(d) end;
  end;
end;"""


@pytest.mark.parametrize("structured", [True, False])
def test_residual_prompt_has_one_consistent_output_contract(structured):
    """Oracle: actual prompt must not request full include and residual together."""
    text = trial.residual_prompt(ROOT, "FUN_24dd_48e1", structured=structured)
    assert "Required declaration:" not in text
    assert "complete include" not in text
    assert "param_2" not in text and "param_3" not in text
    assert "Model all available register" not in text
    assert "24dd:48f4  JNC 24dd:48fd" in text
    assert "0x2000:96cd" not in text
    assert "PByte(source)" in text and "PByte(destination)" in text
    assert ("Return JSON" in text) == structured
    assert ("Output only raw Pascal" in text) != structured
    assert RESIDUAL_CONTROL not in text


def test_residual_composition_full_state(tmp_path):
    """Oracle: supplied control validates wrapper, not model inference."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    source = trial.compose_residual(RESIDUAL_CONTROL)
    directory = tmp_path / "composed"
    assert (
        trial.compile_candidate(ROOT, directory, "FUN_24dd_48e1", source)["status"]
        == "passed"
    )
    assert (
        trial.run_candidate(
            directory, "FUN_24dd_48e1", trial.cases("FUN_24dd_48e1", "training")
        )["status"]
        == "passed"
    )
    wrong = source.replace("RegisterSP + 14", "RegisterSP + 10")
    directory = tmp_path / "wrong"
    assert (
        trial.compile_candidate(ROOT, directory, "FUN_24dd_48e1", wrong)["status"]
        == "passed"
    )
    assert (
        trial.run_candidate(
            directory, "FUN_24dd_48e1", trial.cases("FUN_24dd_48e1", "training")
        )["status"]
        == "failed"
    )


@pytest.mark.parametrize(
    "body",
    [
        "begin RegisterSP := 0; end;",
        "begin asm end; end;",
        "procedure Other; begin end;",
        "begin Move(source^, destination^, count); end;",
    ],
)
def test_residual_rejects_abi_and_services(body):
    """Oracle: static residual partition guard."""
    with pytest.raises(ValueError):
        trial.compose_residual(body)


def test_residual_accepts_pascal_hex_constants():
    """Oracle: valid constants are not compiler directives."""
    assert "$FF" in trial.compose_residual("var value: Byte; begin value := $FF; end;")


def test_rejected_local_finalization_does_not_repeat_evaluation(tmp_path, monkeypatch):
    """Oracle: saved rejected selection and synthetic original-contract rows."""
    routine = "FUN_24dd_48e1"
    model = tmp_path / "model.json"
    model.write_text("{}")
    directory = tmp_path / routine
    native = directory / "original-training"
    native.mkdir(parents=True)
    inputs = trial.cases(routine, "training")
    (native / "CASES.BIN").write_bytes(b"".join(inputs))
    (native / "TRACE.BIN").write_bytes(
        b"".join(trial.expected(routine, row, 0x2000) for row in inputs)
    )
    record = {
        "attempts": [{"status": "proposal-failed"}],
        "selected": None,
        "terminal": None,
        "source_review": "not_eligible",
    }
    (directory / "selection.json").write_text(json.dumps(record))
    frozen = {
        "model": {"file_hashes": {str(model): trial.pilot.digest(model)}},
        "source_hashes": {},
        "regions": {routine: {}},
    }
    (tmp_path / "freeze.json").write_text(json.dumps(frozen))
    monkeypatch.setattr(
        trial.pilot, "request", lambda *args: pytest.fail("must not generate")
    )
    result = trial.finalize_rejected_local_trial(tmp_path)
    assert result["model_requests"] == 1
    assert result["binary_terminal_passes"] == 0
    assert "No new generation" in result["finalization_repair"]
    with pytest.raises(ValueError, match="replace"):
        trial.finalize_rejected_local_trial(tmp_path)


def test_proposal_assessment_does_not_invent_correctness_probability():
    """Oracle: exact measured fixture counts, unknown correctness remains unknown."""
    checked = trial.proposal_assessment(
        {"status": "failed", "cases": 56, "matches": 28}
    )
    assert checked["required_case_recall"] == 0.5
    assert checked["probability_correct"] is None
    rejected = trial.proposal_assessment({"status": "proposal-failed"})
    assert rejected["required_case_recall"] is None
    assert rejected["evaluated_required_cases"] == 0


def test_synthetic_family_corpus_and_measured_retention(tmp_path):
    """Oracle: actual FPC synthetic execution, no original Liero recovery."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    dataset = tmp_path / "data"
    examples = trial.synthetic_residual_dataset(dataset)
    training = [row for row in examples if row["target"] == "synthetic-training"]
    development = [row for row in examples if row["target"] != "synthetic-training"]
    assert len(training) == 24 and len(development) == 8
    assert {row["family"] for row in training}.isdisjoint(
        {row["family"] for row in development}
    )
    result = trial.evaluate_synthetic_residual(
        dataset, tmp_path / "correct", examples[0], examples[0]["completion"]
    )
    assert result["required_case_recall"] == 1.0
    wrong = trial.evaluate_synthetic_residual(
        dataset, tmp_path / "wrong", examples[0], "begin end;"
    )
    assert wrong["required_case_recall"] == 0.0
    assert wrong["probability_correct"] is None


# Disclosed hand-written controls test the fixture, never count as model proposals.
CONTROLS = {
    "FUN_24dd_40d6": """
procedure FUN_24dd_40d6(param_1: Word; param_2: Pointer);
var i: Integer; p: PByte;
begin
  p := PByte(param_2);
  p^ := param_1 and $ff; Inc(p); p^ := param_1 shr 8; Inc(p);
  for i := 1 to 30 do begin p^ := 0; Inc(p) end;
  RegisterBX := RegisterSP;
  RegisterAX := 0; RegisterCX := 0;
  RegisterDI := (LongInt(RegisterDI) + 32) and $ffff;
  RegisterCarryFlag := False; RegisterZeroFlag := True;
  RegisterDirectionFlag := False;
  RegisterSP := (LongInt(RegisterSP) + 6) and $ffff;
end;
""",
    "FUN_24dd_3d68": """
procedure FUN_24dd_3d68(param_1: Integer; param_2, param_3: Pointer);
var remaining: Word; destination, source: PByte;
begin
  remaining := Word(param_1);
  destination := PByte(param_2); source := PByte(param_3);
  while remaining <> 0 do begin
    destination^ := source^; Inc(destination); Inc(source); Dec(remaining)
  end;
  RegisterBX := RegisterSP; RegisterCX := 0; RegisterDX := RegisterDS;
  RegisterSI := (LongInt(RegisterSI) + Word(param_1)) and $ffff;
  RegisterDI := (LongInt(RegisterDI) + Word(param_1)) and $ffff;
  RegisterDirectionFlag := False;
  RegisterSP := (LongInt(RegisterSP) + 14) and $ffff;
end;
""",
}
CONTROLS["FUN_24dd_48e1"] = """
procedure FUN_24dd_48e1(param_1: Integer; param_2, param_3: Pointer);
var count, left: Word; p, q: PByte; src, dst: LongInt;
begin
  src := RegisterSI; dst := RegisterDI; count := Word(param_1);
  RegisterBX := RegisterSP; RegisterDX := RegisterDS;
  p := PByte(param_3); q := PByte(param_2); left := count;
  if src < dst then begin
    RegisterCarryFlag := dst + count > 65535;
    RegisterZeroFlag := ((dst + count - 1) and $ffff) = 0;
    if count <> 0 then begin
      Inc(p, count - 1); Inc(q, count - 1);
      while left <> 0 do begin q^ := p^; Dec(left);
        if left <> 0 then begin Dec(p); Dec(q) end
      end
    end;
    RegisterSI := (src - 1) and $ffff;
    RegisterDI := (dst - 1) and $ffff;
  end else begin
    RegisterCarryFlag := False; RegisterZeroFlag := src = dst;
    while left <> 0 do begin q^ := p^; Inc(p); Inc(q); Dec(left) end;
    RegisterSI := (src + count) and $ffff;
    RegisterDI := (dst + count) and $ffff;
  end;
  RegisterCX := 0; RegisterDirectionFlag := False;
  RegisterSP := (LongInt(RegisterSP) + 14) and $ffff;
end;
"""


@pytest.mark.parametrize("routine", trial.PANEL)
def test_source_trial_corpus_frozen_disjoint_owned(routine):
    """Oracle: fixed source domains/boundaries and no terminal outcome feedback."""
    training = trial.cases(routine, "training")
    terminal = trial.cases(routine, "terminal")
    assert len(training) == len(terminal) == 56
    assert len(set(training)) == 56
    assert not set(training) & set(terminal)
    assert training == trial.cases(routine, "training")
    for data in training + terminal:
        assert len(data) == trial.CASE_BYTES
        assert len(trial.expected(routine, data, 0x2000)) == trial.RECORD_BYTES
    with pytest.raises(ValueError):
        trial.cases(routine, "other")
    with pytest.raises(ValueError):
        trial.expected(routine, training[0][:-1], 0x2000)


@pytest.mark.parametrize("routine", trial.PANEL)
@pytest.mark.parametrize(
    "offset", [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 4127]
)
def test_source_trial_rejects_mutated_native_records(routine, offset):
    """Oracle: synthetic corrupted observations; not independent original evidence."""
    inputs = trial.cases(routine, "training")[:2]
    trace = bytearray(
        b"".join(trial.expected(routine, data, 0x2000) for data in inputs)
    )
    assert trial.compare(routine, inputs, trace, native=True)["status"] == "passed"
    trace[offset] ^= 1
    assert trial.compare(routine, inputs, trace, native=True)["status"] == "failed"
    with pytest.raises(ValueError, match="partial"):
        trial.compare(routine, inputs, trace[:-1], native=True)


def test_copy_contract_is_forward_not_memmove():
    """Oracle: destructive forward overlap, signed-word count and pointer bounds."""
    data = struct.pack("<4H", 7, 0x8000, 0x8001, 0x441) + bytes(range(256)) * 16
    expected = trial.expected("FUN_24dd_3d68", data, 0x2000)
    assert expected[32:40] == bytes(8)
    assert struct.unpack_from("<H", expected, 24)[0] == 0x41
    bad = struct.pack("<4H", 0xFFFF, 0x8000, 0x8001, 0) + data[8:]
    with pytest.raises(ValueError, match="outside"):
        trial.expected("FUN_24dd_3d68", bad, 0x2000)


@pytest.mark.parametrize("routine", trial.PANEL)
def test_complete_output_obligations_and_exact_declaration_gate(routine):
    """Oracle: recognized full bytes, exact signature; no inferred acceptance from assignment text."""
    raw = bytes.fromhex(trial.PANEL[routine]["bytes"])
    contract = trial.output_obligations(routine, raw)
    assert contract["far_return_bytes"] == 4
    assert contract["retf_immediate"] == trial.PANEL[routine]["cleanup"]
    assert "RegisterSP" in contract["outputs"]
    assert trial.check_declaration(routine, CONTROLS[routine]) is None
    wrong = CONTROLS[routine].replace("param_1: ", "param_1, unexpected: ", 1)
    assert trial.check_declaration(routine, wrong)["status"] == "declaration-rejected"
    for offset in range(len(raw)):
        mutant = bytearray(raw)
        mutant[offset] ^= 1
        with pytest.raises(ValueError, match="unrecognized"):
            trial.output_obligations(routine, mutant)


def test_named_training_counterexample_includes_far_return_and_registers():
    """Oracle: synthetic v3 failure pattern; no source patching or terminal feedback."""
    routine = "FUN_24dd_3d68"
    inputs = trial.cases(routine, "training")[:2]
    data = bytearray(
        b"".join(trial.expected(routine, value, 0x2000) for value in inputs)
    )
    for offset in (4, 8, 10, 16):
        data[offset] ^= 1
    feedback = trial.training_state_feedback(routine, inputs, data)
    assert set(feedback["examples"][0]["state"]) == {"CX", "SI", "DI", "returnSP"}
    assert feedback["examples"][0]["first_arena_offsets"] == []


def test_unresolved_move_owns_zero_count_and_both_directions():
    """Oracle: unchanged36-byte shape; backward zero count still changes numeric offsets."""
    for count, source, destination in (
        (0, 0x8000, 0x8001),
        (7, 0x8000, 0x8001),
        (7, 0x8001, 0x8000),
        (0, 0x8000, 0x8000),
    ):
        data = (
            struct.pack("<4H", count, source, destination, 0) + bytes(range(256)) * 16
        )
        result = trial.expected("FUN_24dd_48e1", data, 0x2000)
        expected = bytearray(data[8:])
        expected[destination - 0x8000 : destination - 0x8000 + count] = data[
            8 + source - 0x8000 : 8 + source - 0x8000 + count
        ]
        assert result[32:] == expected
        si, di = struct.unpack_from("<2H", result, 8)
        assert (si, di) == (
            (source - 1, destination - 1)
            if source < destination
            else (source + count, destination + count)
        )


@pytest.mark.parametrize("routine", trial.PANEL)
def test_disclosed_controls_compile_against_actual_runtime(tmp_path, routine):
    """Oracle: supplied fixture controls only, no original execution or recovery count."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    output = tmp_path / "candidate"
    assert (
        trial.compile_candidate(ROOT, output, routine, CONTROLS[routine])["status"]
        == "passed"
    )
    assert (
        trial.run_candidate(output, routine, trial.cases(routine, "training"))["status"]
        == "passed"
    )
    if shutil.which("as") and shutil.which("ld"):
        (tmp_path / "harness.S").write_text(trial.harness(routine))
        image = trial.assemble_probe(tmp_path / "harness.S", tmp_path)
        assert len(image) + 0x100 < 0x6000
        assert image.count(bytes.fromhex(trial.PANEL[routine]["bytes"])) == 1


@pytest.mark.parametrize("terminal_pass", [True, False])
@pytest.mark.parametrize("representation_rejected", [False, True])
def test_selection_saved_before_terminal_and_never_repaired(
    tmp_path, monkeypatch, terminal_pass, representation_rejected
):
    """Oracle: scripted orchestration, not a live model or original experiment."""
    calls = []

    def freeze(root, output, model, endpoint):
        """Oracle: synthetic immutable method identity for control-flow test."""
        output.mkdir()
        for routine in trial.PANEL:
            (output / f"{routine}.prompt.txt").write_text("frozen prompt")
        return {"source_hashes": {}, "model": {"digest": "scripted"}}

    def original(root, output, routine, inputs):
        """Oracle: scripted stage order, no execution."""
        output.mkdir(parents=True)
        if output.name == "original-terminal":
            saved = json.loads((output.parent / "selection.json").read_text())
            assert saved["selected"] == 2
        calls.append((routine, output.name))

    def request(prompt, model, endpoint):
        """Oracle: two proposals per routine; repair sees training only."""
        assert "terminal" not in prompt
        source = "PByte(RegisterDS)^ := 0;" if representation_rejected else prompt
        return json.dumps({"response": json.dumps({"source": source})})

    def compile(root, output, routine, source):
        """Oracle: executable placeholder only for the scripted runner."""
        output.mkdir()
        (output / "probe").write_text("not executable")
        return {"status": "passed"}

    def candidate(output, routine, inputs):
        """Oracle: first training failure, second pass; fixed terminal decision."""
        calls.append((routine, output.name))
        passed = output.name == "attempt-2" or (
            output.name == "terminal" and terminal_pass
        )
        return {"status": "passed" if passed else "failed"}

    monkeypatch.setattr(trial, "freeze", freeze)
    monkeypatch.setattr(trial, "original", original)
    monkeypatch.setattr(trial.pilot, "request", request)
    monkeypatch.setattr(
        trial.pilot, "candidate_source", lambda response, routine: response["response"]
    )
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"digest": "scripted"}
    )
    monkeypatch.setattr(trial, "compile_candidate", compile)
    monkeypatch.setattr(trial, "run_candidate", candidate)
    result = trial.run(ROOT, tmp_path / "trial", "scripted", "local")
    assert result["binary_terminal_passes"] == (
        len(trial.PANEL) if terminal_pass and not representation_rejected else 0
    )
    assert result["accepted_source_recoveries"] == 0
    assert not result["weights_changed"]
    for routine in trial.PANEL:
        stages = [stage for fn, stage in calls if fn == routine]
        assert stages == (
            ["original-training"]
            if representation_rejected
            else [
                "original-training",
                "attempt-1",
                "attempt-2",
                "original-terminal",
                "terminal",
            ]
        )
        if representation_rejected:
            assert [r["status"] for r in result["routines"][routine]["attempts"]] == [
                "representation-rejected",
                "duplicate",
            ]
            assert result["frontier_status"] == "stopped-below-yield-floor"
    artifacts = json.loads((tmp_path / "trial/artifacts.json").read_text())
    for path, digest in artifacts.items():
        assert (
            hashlib.sha256((tmp_path / "trial" / path).read_bytes()).hexdigest()
            == digest
        )


def test_source_trial_saved_trace_replay_and_tamper_rejection(tmp_path, monkeypatch):
    """Oracle: synthetic trace replay and real input identities, not native execution."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("BYOD unavailable")
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"digest": "scripted"}
    )
    output = tmp_path / "trial"
    trial.freeze(ROOT, output, "scripted", "local")
    result = {"routines": {}}
    for routine in trial.PANEL:
        directory = output / routine / "original-training"
        directory.mkdir(parents=True)
        inputs = trial.cases(routine, "training")
        (directory / "CASES.BIN").write_bytes(b"".join(inputs))
        (directory / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(routine, data, 0x2000) for data in inputs)
        )
        result["routines"][routine] = {"selected": None}
    trial.pilot.save(output / "result.json", result)
    trial.pilot.save(
        output / "artifacts.json",
        {
            str(p.relative_to(output)): trial.pilot.digest(p)
            for p in output.rglob("*")
            if p.is_file()
        },
    )
    assert trial.validate_artifacts(ROOT, output) == result
    (output / "result.json").write_text("{}")
    with pytest.raises(ValueError, match="artifact changed"):
        trial.validate_artifacts(ROOT, output)


@pytest.mark.parametrize("routine", trial.PANEL)
def test_installed_source_matches_declared_state(tmp_path, routine):
    """Oracle: actual installed include/runtime, full arena and available register mirrors."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    source = (ROOT / f"targets/liero/src/{routine}.inc").read_text()
    directory = tmp_path / "actual"
    assert (
        trial.compile_candidate(ROOT, directory, routine, source)["status"] == "passed"
    )
    result = trial.run_candidate(directory, routine, trial.cases(routine, "training"))
    record = json.loads((ROOT / "targets/liero/recovery.json").read_text())[
        "functions"
    ][routine]
    if result["status"] != "passed" and record["status"] != "source_recovered":
        pytest.xfail(
            "Unreviewed existing source omits modeled register/flag effects; no generated candidate accepted"
        )
    assert result["status"] == "passed", result


@pytest.mark.parametrize("already_terminal", [False, True])
def test_changed_strategy_replays_training_and_rejects_terminal_feedback(
    tmp_path, monkeypatch, already_terminal
):
    """Oracle: synthetic originals and disclosed controls, never live recovery evidence."""
    if not shutil.which("fpc") or not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("FPC/BYOD unavailable")
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"digest": "scripted"}
    )
    predecessor = tmp_path / "old"
    trial.freeze(ROOT, predecessor, "scripted", "local")
    records = {}
    for routine in trial.PANEL:
        directory = predecessor / routine / "original-training"
        directory.mkdir(parents=True)
        inputs = trial.cases(routine, "training")
        (directory / "CASES.BIN").write_bytes(b"".join(inputs))
        (directory / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(routine, data, 0x2000) for data in inputs)
        )
        records[routine] = {
            "terminal": {"status": "failed"} if already_terminal else None
        }
    trial.pilot.save(predecessor / "result.json", {"routines": records})
    trial.pilot.save(
        predecessor / "artifacts.json",
        {
            str(p.relative_to(predecessor)): trial.pilot.digest(p)
            for p in predecessor.rglob("*")
            if p.is_file()
        },
    )
    calls = []

    def original(root, output, routine, inputs):
        """Oracle: synthetic terminal trace; training must be replayed, not executed."""
        assert output.name == "original-terminal"
        output.mkdir(parents=True)
        (output / "CASES.BIN").write_bytes(b"".join(inputs))
        (output / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(routine, data, 0x2000) for data in inputs)
        )
        calls.append(routine)

    def request(prompt, *args):
        """Oracle: known control body, not a model response."""
        routine = next(name for name in trial.PANEL if name in prompt)
        return json.dumps({"response": json.dumps({"source": CONTROLS[routine]})})

    monkeypatch.setattr(trial, "original", original)
    monkeypatch.setattr(trial.pilot, "request", request)
    if already_terminal:
        with pytest.raises(ValueError, match="terminal outcomes"):
            trial.run(ROOT, tmp_path / "new", "scripted", "local", predecessor)
        assert calls == []
    else:
        result = trial.run(ROOT, tmp_path / "new", "scripted", "local", predecessor)
        assert result["binary_terminal_passes"] == len(trial.PANEL)
        assert calls == list(trial.PANEL)
        assert trial.validate_artifacts(ROOT, tmp_path / "new") == result


def test_enforced_single_unresolved_panel_rejects_wrong_signature_before_compile(
    tmp_path, monkeypatch
):
    """Oracle: scripted model/control execution, no original recovery claim."""
    if not shutil.which("fpc") or not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("FPC/BYOD unavailable")
    routine = "FUN_24dd_48e1"
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"digest": "scripted"}
    )
    requests = []

    def request(prompt, *args):
        """Oracle: first wrong interface, then supplied fixture body."""
        requests.append(prompt)
        assert "Mandatory byte-backed output obligations" in prompt
        source = CONTROLS[routine]
        if len(requests) == 1:
            source = source.replace("param_1: Integer", "param_1, extra: Integer")
        else:
            assert "declaration-rejected" in prompt
        return json.dumps({"response": json.dumps({"source": source})})

    def original(root, output, fn, inputs):
        """Oracle: synthetic original contract rows, no DOS execution."""
        output.mkdir(parents=True)
        (output / "CASES.BIN").write_bytes(b"".join(inputs))
        (output / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(fn, row, 0x2000) for row in inputs)
        )

    monkeypatch.setattr(trial.pilot, "request", request)
    monkeypatch.setattr(trial, "original", original)
    output = tmp_path / "single"
    result = trial.run(
        ROOT, output, "scripted", "local", routines=(routine,), enforce_outputs=True
    )
    assert result["attempted_routines"] == 1
    assert result["binary_terminal_passes"] == 1
    assert not (output / routine / "attempt-1/compile.log").exists()
    assert (
        result["routines"][routine]["attempts"][0]["status"] == "declaration-rejected"
    )
    frozen = json.loads((output / "freeze.json").read_text())
    assert "no implemented Pascal body" in frozen["prior_knowledge"]
    assert frozen["budgets"]["batch_size"] == 1
    assert trial.validate_artifacts(ROOT, output) == result


CALIBRATION_ADAPTERS = {
    "CalibrateMask": """
  RegisterAX := old;
  RegisterBX := RegisterSP;
  RegisterSP := (LongInt(RegisterSP) + 6) and $ffff;
  RegisterCarryFlag := False;
  RegisterZeroFlag := p^ = 0;
""",
    "CalibratePair": """
  RegisterAX := old;
  RegisterBX := RegisterSP;
  RegisterSP := (LongInt(RegisterSP) + 6) and $ffff;
  RegisterDI := (LongInt(RegisterDI) + 2) and $ffff;
  RegisterCX := 0;
  RegisterDirectionFlag := False;
""",
}


@pytest.mark.parametrize("passes", [True, False])
def test_interpretation_gates_pascal_and_never_reads_terminal_before_selection(
    tmp_path, monkeypatch, passes
):
    """Oracle: supplied interpretation/body controls, complete-state fixture execution."""
    if not shutil.which("fpc") or not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("FPC/BYOD unavailable")
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"digest": "scripted"}
    )
    requests = []

    def original(root, output, routine, inputs):
        """Oracle: controlled fixture records, not live original evidence."""
        if output.name == "original-terminal":
            assert requests == ["interpretation", "source"]
            assert (tmp_path / "trial" / routine / "selection.json").exists()
        output.mkdir(parents=True)
        (output / "CASES.BIN").write_bytes(b"".join(inputs))
        (output / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(routine, data, 0x2000) for data in inputs)
        )

    def request(text, *args, schema=None):
        """Oracle: scripted hypothesis then declaration-free known memory control."""
        if schema is not None:
            requests.append("interpretation")
            assert "Original bytes:" in text
            hypothesis = (
                INTERPRETATION_CONTROL
                if passes
                else {**INTERPRETATION_CONTROL, "backward_step": 1}
            )
            return json.dumps({"response": json.dumps({"hypotheses": [hypothesis]})})
        requests.append("source")
        assert "Checked model-proposed memory interpretation" in text
        return json.dumps({"response": json.dumps({"source": RESIDUAL_CONTROL})})

    monkeypatch.setattr(trial, "original", original)
    monkeypatch.setattr(trial.pilot, "request", request)
    result = trial.run(
        ROOT,
        tmp_path / "trial",
        "scripted",
        "local",
        routines=("FUN_24dd_48e1",),
        residual=True,
        interpretation_first=True,
    )
    assert result["model_requests"] == 2
    assert result["binary_terminal_passes"] == int(passes)
    assert requests == (
        ["interpretation", "source"] if passes else ["interpretation", "interpretation"]
    )
    assert trial.validate_artifacts(ROOT, tmp_path / "trial") == result


@pytest.mark.parametrize("completion", ["bound", "incomplete", "action-injection"])
def test_binding_completion_freezes_prior_actions_and_only_then_requests_pascal(
    tmp_path, monkeypatch, completion
):
    """Oracle: scripted citation completion and composed fixture controls, not live recovery."""
    if not shutil.which("fpc") or not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("FPC/BYOD unavailable")
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"digest": "scripted"}
    )
    prior = tmp_path / "prior"
    current = tmp_path / "completion"
    incomplete = {
        **INTERPRETATION_CONTROL,
        "evidence": {
            "branch": "24dd:48f2",
            "setup": "24dd:48f6-24dd:48fb",
            "transfer": "24dd:48fd",
        },
    }
    requests = []

    def original(root, output, routine, inputs):
        """Oracle: supplied full original fixture state, terminal only after selection."""
        if output.name == "original-terminal":
            assert completion == "bound"
            assert requests == ["binding", "source"]
            assert (current / routine / "selection.json").exists()
        output.mkdir(parents=True)
        (output / "CASES.BIN").write_bytes(b"".join(inputs))
        (output / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(routine, row, 0x2000) for row in inputs)
        )

    def request(text, *args, schema=None):
        """Oracle: initial incomplete citations then evidence-only response."""
        if schema == trial.INTERPRETATION_SCHEMA:
            return json.dumps({"response": json.dumps({"hypotheses": [incomplete]})})
        if schema == trial.BINDING_SCHEMA:
            requests.append("binding")
            assert "Immutable prior hypothesis" in text
            evidence = (
                INTERPRETATION_CONTROL if completion != "incomplete" else incomplete
            )["evidence"]
            if completion == "action-injection":
                evidence = {**evidence, "backward_step": 1}
            return json.dumps({"response": json.dumps(evidence)})
        requests.append("source")
        return json.dumps({"response": json.dumps({"source": RESIDUAL_CONTROL})})

    monkeypatch.setattr(trial, "original", original)
    monkeypatch.setattr(trial.pilot, "request", request)
    trial.run(
        ROOT,
        prior,
        "scripted",
        "local",
        routines=("FUN_24dd_48e1",),
        residual=True,
        interpretation_first=True,
    )
    identity = trial.pilot.digest(prior / "artifacts.json")
    context = trial.binding_context(ROOT, prior)
    assert context["hypothesis"] == incomplete
    assert context["assessment"]["required_case_recall"] == 1
    result = trial.run(
        ROOT,
        current,
        "scripted",
        "local",
        training_from=prior,
        routines=("FUN_24dd_48e1",),
        residual=True,
        interpretation_first=True,
        binding_from=prior,
    )
    assert requests == (["binding", "source"] if completion == "bound" else ["binding"])
    assert result["binary_terminal_passes"] == int(completion == "bound")
    assert result["model_requests"] == len(requests)
    assert trial.pilot.digest(prior / "artifacts.json") == identity
    freeze = json.loads((current / "freeze.json").read_text())
    assert freeze["binding_completion"] == context
    assert freeze["budgets"]["maximum_total_model_requests"] == 3
    assert freeze["interpretation_first"]["maximum_requests"] == 1
    assert trial.validate_artifacts(ROOT, current) == result
    with pytest.raises(ValueError, match="initial interpretation archive"):
        trial.binding_context(ROOT, current)
    with pytest.raises(ValueError, match="same archive"):
        trial.freeze(
            ROOT,
            tmp_path / "invalid",
            "scripted",
            "local",
            routines=("FUN_24dd_48e1",),
            residual=True,
            interpretation_first=True,
            binding_from=prior,
        )
    (prior / "result.json").write_text("{}")
    with pytest.raises(ValueError, match="predecessor identity"):
        trial.validate_artifacts(ROOT, current, historical=True)


@pytest.mark.parametrize("field", list(trial.INTERPRETATION_FIELDS))
def test_typed_lowering_refuses_unsupported_actions(field):
    """Oracle: mechanical lowering supports only the checked48e1 memory contract."""
    mutant = {
        **INTERPRETATION_CONTROL,
        field: next(
            value
            for value in trial.INTERPRETATION_FIELDS[field]
            if value != INTERPRETATION_CONTROL[field]
        ),
    }
    with pytest.raises(ValueError, match="unsupported memory interpretation"):
        trial.lower_interpretation(mutant)


def test_typed_lowering_uses_no_model_and_checks_complete_composition(
    tmp_path, monkeypatch
):
    """Oracle: supplied interpretation, mechanical emitter, original-fixture control rows."""
    if not shutil.which("fpc") or not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("FPC/BYOD unavailable")
    prior, output = tmp_path / "prior", tmp_path / "lowering"
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"digest": "scripted"}
    )

    def original(root, directory, routine, inputs):
        """Oracle: synthetic complete original observations; selection before terminal."""
        if directory.name == "original-terminal":
            assert (output / routine / "selection.json").exists()
        directory.mkdir(parents=True)
        (directory / "CASES.BIN").write_bytes(b"".join(inputs))
        (directory / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(routine, row, 0x2000) for row in inputs)
        )

    def request(text, *args, schema=None):
        """Oracle: prior supplied interpretation plus deliberately uncompilable body."""
        if schema == trial.INTERPRETATION_SCHEMA:
            return json.dumps(
                {"response": json.dumps({"hypotheses": [INTERPRETATION_CONTROL]})}
            )
        return json.dumps(
            {"response": json.dumps({"source": "begin UnknownSymbol := 0; end;"})}
        )

    monkeypatch.setattr(trial, "original", original)
    monkeypatch.setattr(trial.pilot, "request", request)
    trial.run(
        ROOT,
        prior,
        "scripted",
        "local",
        routines=("FUN_24dd_48e1",),
        residual=True,
        interpretation_first=True,
    )
    context = trial.lowering_context(ROOT, prior)

    def no_model(*args, **kwargs):
        """Oracle: lowering must not invoke inference or query model service."""
        pytest.fail("mechanical lowering contacted model")

    monkeypatch.setattr(trial.pilot, "request", no_model)
    monkeypatch.setattr(trial.pilot, "leaf_model_identity", no_model)
    result = trial.run(
        ROOT,
        output,
        "unused",
        "local",
        training_from=prior,
        routines=("FUN_24dd_48e1",),
        residual=True,
        enforce_outputs=True,
        lowering_from=prior,
    )
    assert result["model_requests"] == 0
    assert result["binary_terminal_passes"] == 1
    assert result["accepted_source_recoveries"] == 0
    record = result["routines"]["FUN_24dd_48e1"]
    assert record["attempts"][0]["source_origin"] == "mechanical-lowering"
    assert record["attempts"][0]["assessment"]["required_case_recall"] == 1
    assert record["terminal"]["assessment"]["required_case_recall"] == 1
    assert trial.validate_artifacts(ROOT, output) == result
    assert (
        json.loads((output / "freeze.json").read_text())["mechanical_lowering"][
            "origin_model"
        ]
        == context["origin_model"]
    )
    with pytest.raises(ValueError, match="lowering retry"):
        trial.lowering_context(ROOT, output)
    with pytest.raises(ValueError, match="no inference modes"):
        trial.freeze(
            ROOT,
            tmp_path / "invalid",
            "unused",
            "local",
            training_from=prior,
            routines=("FUN_24dd_48e1",),
            residual=True,
            interpretation_first=True,
            lowering_from=prior,
        )
    (output / "lowered-residual.inc").write_text("begin end;")
    with pytest.raises(ValueError, match="artifact changed"):
        trial.validate_artifacts(ROOT, output, historical=True)
    prior_result = json.loads((prior / "result.json").read_text())
    prior_result["routines"]["FUN_24dd_48e1"]["terminal"] = {"status": "failed"}
    trial.pilot.save(prior / "result.json", prior_result)
    hashes = json.loads((prior / "artifacts.json").read_text())
    hashes["result.json"] = trial.pilot.digest(prior / "result.json")
    trial.pilot.save(prior / "artifacts.json", hashes)
    with pytest.raises(ValueError, match="evaluated terminal"):
        trial.lowering_context(ROOT, prior)


@pytest.mark.parametrize("failure", ["none", "compile", "state"])
def test_known_source_calibration_gate_and_disclosure(tmp_path, monkeypatch, failure):
    """Oracle: disclosed supplied adapters and exhaustive host checks, not live model."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    calls = []

    def request(prompt, *args):
        """Oracle: supplied known bodies; never a model recovery."""
        name = next(n for n in trial.CALIBRATION if n in prompt)
        calls.append(name)
        body = trial.CALIBRATION[name]["body"]
        added = CALIBRATION_ADAPTERS[name]
        if failure == "compile":
            added = "UnknownSymbol := 0;"
        elif failure == "state":
            added = added.replace("RegisterAX := old", "RegisterAX := 123")
        source = body[:-4] + added + "end;"
        return json.dumps({"response": json.dumps({"source": source})})

    monkeypatch.setattr(trial.pilot, "request", request)
    monkeypatch.setattr(
        trial.pilot, "leaf_model_identity", lambda *args: {"digest": "scripted"}
    )
    output = tmp_path / "calibration"
    result = trial.run_calibration(ROOT, output, "scripted", "local")
    assert calls == list(trial.CALIBRATION)
    assert result["status"] == ("review-required" if failure == "none" else "blocked")
    assert not result["recovery_frontier_reopened"]
    assert result["new_recoveries"] == 0
    assert not result["weights_changed"]
    frozen = json.loads((output / "freeze.json").read_text())
    assert "Developer-supplied" in frozen["disclosure"]
    if failure != "compile":
        name = "CalibrateMask"
        data = bytearray((output / name / "CALIB.BIN").read_bytes())
        data[31] ^= 1
        assert trial.calibration_compare(name, data)["status"] == "failed"
        with pytest.raises(ValueError, match="incomplete"):
            trial.calibration_compare(name, data[:-1])
    if failure == "none":
        with pytest.raises(FileNotFoundError):
            trial.calibration_context(ROOT, output)
        review = {
            "status": "calibration-reviewed",
            "freeze_sha256": trial.pilot.digest(output / "freeze.json"),
            "artifacts_sha256": trial.pilot.digest(output / "artifacts.json"),
            "source_hashes": {
                n: trial.pilot.digest(output / n / "candidate.inc")
                for n in trial.CALIBRATION
            },
            "review": {
                n: "Scripted test review, not live evidence" for n in trial.CALIBRATION
            },
        }
        trial.pilot.save(output / "review.json", review)
        context = trial.calibration_context(ROOT, output)
        assert "not Liero recoveries" in context
        assert "RegisterAX := old" in context
        for n in trial.CALIBRATION:
            assert n in context
        if (ROOT / "extracted/liero/LIERO.EXE").is_file():
            predecessor = tmp_path / "predecessor"
            predecessor.mkdir()
            trial.pilot.save(predecessor / "artifacts.json", {})
            trial.pilot.save(predecessor / "result.json", {})
            frozen = trial.freeze(
                ROOT,
                tmp_path / "recovery-freeze",
                "scripted",
                "local",
                predecessor,
                output,
            )
            assert frozen["calibration"]["review_sha256"] == trial.pilot.digest(
                output / "review.json"
            )
            for name in trial.PANEL:
                prompt = (
                    tmp_path / "recovery-freeze" / f"{name}.prompt.txt"
                ).read_text()
                assert "CalibrateMask" in prompt
                assert trial.PANEL[name]["signature"] in prompt
            monkeypatch.setattr(
                trial.pilot, "leaf_model_identity", lambda *args: {"digest": "changed"}
            )
            with pytest.raises(ValueError, match="model identities differ"):
                trial.freeze(
                    ROOT,
                    tmp_path / "wrong-model",
                    "changed",
                    "local",
                    predecessor,
                    output,
                )
        review["source_hashes"]["CalibrateMask"] = "0" * 64
        trial.pilot.save(output / "review.json", review)
        with pytest.raises(ValueError, match="source/review"):
            trial.calibration_context(ROOT, output)
