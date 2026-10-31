import json
import pathlib
import shutil
import subprocess
import urllib.error

import pytest

from tools import liero_four_routine_pilot as pilot


def test_prefix_transfer_requires_global_bound_and_retains_return_residue(tmp_path):
    """Oracle: shared rules retain unknown writes without caller bounds and unknown RET."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    before = pilot.digest(root / "engine/instruction_facts.py")
    output = tmp_path / "transfer"
    report = pilot.run_prefix_transfer(root, output, "FUN_24dd_492c")
    assert report["status"] == "unsupported"
    assert report["routine_recovered"] is False
    assert report["model_requests"] == 0
    assert report["prefix"]["registers"]["di"]["amount"] == 0x6426
    assert report["prefix"]["registers"]["di"]["kind"] == "constant"
    assert report["prefix"]["writes"] == []
    assert report["prefix"]["residue"]["offset"] == 15
    assert report["prefix"]["residue"]["bytes_hex"].startswith("f3ab")
    bounded = pilot.run_prefix_transfer(
        root,
        tmp_path / "bounded",
        "FUN_24dd_492c",
        data_window=(0, 65536),
    )
    assert bounded["prefix"]["residue"]["offset"] == 17
    assert bounded["prefix"]["residue"]["bytes_hex"] == "c3"
    assert bounded["prefix"]["writes"][0]["byte_offset"] == 0x6426
    assert bounded["prefix"]["writes"][0]["word_count"] == 0xB96
    assert bounded["prefix"]["writes"][0]["address_space"] == "entry_ds"
    assert not bounded["routine_recovered"]
    assert pilot.validate_prefix_transfer(root, tmp_path / "bounded") == bounded
    assert (
        report["rules_sha256"]
        == before
        == pilot.digest(root / "engine/instruction_facts.py")
    )
    assert pilot.validate_prefix_transfer(root, output) == report
    stored = output / "result.json"
    original = stored.read_text()
    changed = json.loads(original)
    changed["routine_recovered"] = True
    stored.write_text(json.dumps(changed))
    with pytest.raises(ValueError, match="disagrees"):
        pilot.validate_prefix_transfer(root, output)
    stored.write_text(original)
    rule_snapshot = output / "instruction_facts.py"
    rule_snapshot.write_text("tampered")
    with pytest.raises(ValueError, match="snapshot"):
        pilot.validate_prefix_transfer(root, output)


def test_frozen_prefix_transfer_cli_preserves_unsupported_exit(tmp_path, monkeypatch):
    """Oracle: a saved unsupported result must not become a successful recovery exit."""
    monkeypatch.setattr(
        pilot.sys,
        "argv",
        [
            "pilot",
            "--output",
            str(tmp_path / "out"),
            "--prefix-transfer-routine",
            "FUN_24dd_492c",
        ],
    )
    monkeypatch.setattr(
        pilot,
        "run_prefix_transfer",
        lambda *_: {"status": "unsupported", "routine_recovered": False},
    )
    assert pilot.main() == 1
    monkeypatch.setattr(
        pilot.sys,
        "argv",
        [
            "pilot",
            "--output",
            str(tmp_path / "out"),
            "--prefix-transfer-routine",
            "FUN_24dd_492c",
            "--automatic-constructor-repair",
        ],
    )
    with pytest.raises(SystemExit) as error:
        pilot.main()
    assert error.value.code == 2


def test_frozen_prefix_transfer_byod_skips_without_writing(tmp_path):
    """Oracle: absent user binary is a skip, never invented static evidence."""
    output = tmp_path / "out"
    assert (
        pilot.run_prefix_transfer(tmp_path, output, "FUN_24dd_492c")["status"]
        == "skipped"
    )
    assert not output.exists()


def test_instruction_prefix_derives_changed_constants_and_relative_offsets():
    """Oracle: transfer rules derive new values, not a stored constructor answer."""
    raw = bytes.fromhex(
        "33d2 8bdc 1e 36c47f08 36c57704 fc 33c0 ab "
        "b81122 ab b83400 ab 33c0 ab ab ab 8d4574 ab 8cc0 ab "
        "b85544 ab b8dd14 ab 33c0 b90e00 f3ab b94f00 0bd2"
    )
    relocation = raw.index(bytes.fromhex("b8dd14")) + 1
    facts = pilot.initialization_prefix(raw, relocation_offsets={relocation})
    # The relocation is at the setup-segment immediate, not a guessed pointer.
    assert facts["writes"][1]["value"]["amount"] == 0x2211
    assert facts["writes"][2]["value"]["amount"] == 0x34
    assert facts["writes"][6]["value"]["kind"] == "object_offset"
    assert facts["writes"][6]["value"]["amount"] == 128
    assert facts["writes"][7]["value"]["kind"] == "object_segment"
    assert facts["writes"][8]["value"]["amount"] == 0x4455
    assert facts["writes"][9]["value"]["amount"] == 0x24DD
    assert facts["next_object_offset"] == 48
    assert facts["registers"]["cx"]["amount"] == 79
    assert facts["residue"]["reason"] == "unsupported opcode"
    changed = raw.replace(bytes.fromhex("8d4574"), bytes.fromhex("8d4564"))
    assert (
        pilot.initialization_prefix(changed, relocation_offsets={relocation})["writes"][
            6
        ]["value"]["amount"]
        == 112
    )
    assert facts["instructions"][0]["bytes_hex"] == "33d2"


@pytest.mark.parametrize(
    "raw",
    [
        "ab",
        "f3ab",
        "36c47f08ab",
        "36c47f08fcab",
        "36c47f08fc33c0fdab",
        "b801",
        "36c47f08fc33c0e90000ab",
    ],
)
def test_instruction_prefix_does_not_step_over_unknown_state(raw):
    """Oracle: unresolved operands, DF, truncation and transfers block subsequent stores."""
    facts = pilot.initialization_prefix(bytes.fromhex(raw))
    assert facts["residue"] is not None
    assert facts["writes"] == []


@pytest.mark.parametrize("offset", [0, 1, 2])
def test_instruction_prefix_rejects_relocation_on_non_immediate(offset):
    """Oracle: relocations cannot be silently applied to an opcode or partial operand."""
    with pytest.raises(ValueError, match="relocation"):
        pilot.initialization_prefix(
            bytes.fromhex("33c0b81122"), relocation_offsets={offset}
        )


def test_constructor_instruction_facts_are_bound_and_do_not_fix_proposals(tmp_path):
    """Oracle: current binary-derived fields reject known bad saved proposal shapes."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    facts = pilot.constructor_instruction_facts(root)
    saved = tmp_path / "instruction-facts.json"
    saved.write_text(json.dumps(facts))
    assert pilot.validate_constructor_instruction_facts(saved, root) == facts
    tampered = json.loads(saved.read_text())
    tampered["constraints"]["capacity_word"]["value"] = 0
    saved.write_text(json.dumps(tampered))
    with pytest.raises(ValueError, match="disagree"):
        pilot.validate_constructor_instruction_facts(saved, root)
    expected, _ = pilot.render_constructor_sketch(_constructor_sketch_response())
    assert {field: claim["value"] for field, claim in facts["constraints"].items()} == {
        field: expected[field] for field in facts["constraints"]
    }
    assert facts["unresolved_fields"] == [
        "name_limit",
        "stop_at_nul",
        "use_length_prefix",
    ]
    assert "name_limit" not in facts["constraints"]
    assert facts["prefix"]["residue"]["offset"] == 0x3670 - 0x3639
    schema = pilot.constrain_constructor_schema(facts)
    for field, claim in facts["constraints"].items():
        assert schema["properties"][field]["enum"] == [claim["value"]]
        bad = {**expected, field: (claim["value"] + 1) % 65536}
        before = bad.copy()
        with pytest.raises(ValueError, match="instruction conflicts"):
            pilot.check_constructor_constraints(bad, facts)
        assert bad == before
    # Staleness is rejected through the existing manifest loader.
    copied = pilot.snapshot(root, tmp_path / "workspace")
    binary = copied / "extracted/liero/LIERO.EXE"
    data = bytearray(binary.read_bytes())
    data[facts["file_offset"]] ^= 1
    binary.write_bytes(data)
    with pytest.raises(ValueError, match="stale"):
        pilot.constructor_instruction_facts(copied)


def test_constructor_fact_conflict_never_reaches_candidate_oracle(
    tmp_path, monkeypatch
):
    """Oracle: raw model contradictions survive as rejected evidence, not repaired success."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    facts = pilot.constructor_instruction_facts(root)
    calls = []

    def probe(_root, output, _kind, _suite):
        calls.append(output.name)
        assert output.name.startswith("control")
        return {"status": "passed"}

    def request(_prompt, *_args, schema):
        assert schema["properties"]["mode_word"]["enum"] == [0xD7B0]
        return json.dumps(_constructor_sketch_response(mode_word=0))

    monkeypatch.setattr(pilot, "probe", probe)
    monkeypatch.setattr(pilot, "request", request)
    result = pilot.run_routine(
        root,
        tmp_path / "trial",
        "constructor",
        "local",
        "local",
        1,
        automatic_constructor_repair=True,
        constructor_instruction_constraints=True,
    )
    assert result["status"] == "failed"
    assert result["unique_candidates"] == 0
    assert calls == ["control-training", "control-heldout"]
    assert "instruction conflicts" in result["attempts"][0]["reason"]
    assert result["attempts"][0]["sketch"]["mode_word"] == 0
    assert (tmp_path / "trial/proposal-01/raw-response.json").is_file()
    assert not (tmp_path / "trial/proposal-01/workspace").exists()
    assert facts["constraints"]["mode_word"]["value"] == 0xD7B0


@pytest.mark.parametrize("value", [0, 1, 32768, 65535])
def test_instruction_prefix_constant_and_relocation_wrap(value):
    """Oracle: supported MOV/XOR/STOS transfer arithmetic is independent of target constants."""
    raw = (
        bytes.fromhex("8bdc36c47f08fc")
        + b"\xb8"
        + value.to_bytes(2, "little")
        + b"\xab"
    )
    facts = pilot.initialization_prefix(
        raw, relocation_offsets={8}, load_segment=0x1000
    )
    assert facts["residue"] is None
    assert facts["writes"][0]["value"]["amount"] == (value + 0x1000) & 65535
    assert json.loads(json.dumps(facts)) == facts


def _sketch_response(**changes):
    """Oracle: test hypothesis, never supplied as the model's recovered answer."""
    sketch = {
        "handle_byte_offset": 0,
        "operator": "<=",
        "threshold": 4,
        "then_return": "zero",
        "else_return": "dos_close_status",
        **changes,
    }
    return {"response": json.dumps(sketch)}


def _read_sketch_response(**changes):
    """Oracle: independently named fixture for the scoped refill contract."""
    return {
        "response": json.dumps(
            {
                "handle_byte_offset": 0,
                "capacity_byte_offset": 4,
                "position_byte_offset": 8,
                "available_byte_offset": 10,
                "clear_on_error": True,
                "count_value": "bytes_read",
                "return_value": "dos_read_status",
                **changes,
            }
        )
    }


def _constructor_sketch_response(**changes):
    """Oracle: test fixture from the existing binary-bound write contract."""
    return {
        "response": json.dumps(
            {
                "mode_word": 0xD7B0,
                "capacity_word": 128,
                "buffer_byte_offset": 128,
                "setup_offset": 0x420C,
                "setup_segment": 0x24DD,
                "zero_word_count": 14,
                "name_byte_offset": 48,
                "name_limit": 79,
                "stop_at_nul": True,
                "use_length_prefix": True,
                **changes,
            }
        )
    }


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("mode_word", True),
        ("capacity_word", -1),
        ("setup_offset", 65536),
        ("zero_word_count", 119),
        ("name_byte_offset", 129),
        ("name_limit", 128),
        ("stop_at_nul", 1),
        ("use_length_prefix", "yes"),
    ],
)
def test_constructor_sketch_rejects_unsafe_or_untyped_fields(field, value):
    """Oracle: schema bounds prevent host out-of-object writes, not semantic acceptance."""
    with pytest.raises(ValueError):
        pilot.render_constructor_sketch(_constructor_sketch_response(**{field: value}))


def test_constructor_training_selects_cap_repair_without_heldout_leakage(tmp_path):
    """Oracle: an off-by-one copy cap must fail original-byte training before repair."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD or probe toolchain unavailable")
    seed = tmp_path / "seed"
    seed.mkdir()
    workspace = pilot.snapshot(root, seed / "workspace")
    response = _constructor_sketch_response(name_limit=78)
    sketch, source = pilot.render_constructor_sketch(response)
    (workspace / "targets/liero/src/FUN_24dd_3639.inc").write_text(source)
    (seed / "raw-response.json").write_text(json.dumps(response))
    (seed / "sketch.json").write_text(json.dumps(sketch))
    training = pilot.probe(workspace, seed / "training", "constructor", "training")
    assert training["status"] == "failed"
    repair = pilot.run_sketch_repair(
        root,
        tmp_path / "repair",
        seed,
        kind="constructor",
        seen_sources={pilot.digest(seed / "training/candidate/FUN_24dd_3639.inc")},
    )
    assert repair["status"] == "passed"
    selected = repair["hypotheses"][-1]
    assert selected["hypothesis"] == "name-limit-plus-one"
    assert selected["training_cases_passed"] == 514
    assert selected["heldout_status"] == "passed"
    assert sum("heldout_status" in row for row in repair["hypotheses"]) == 1


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("handle_byte_offset", True),
        ("capacity_byte_offset", 255),
        ("position_byte_offset", -2),
        ("available_byte_offset", 3),
        ("clear_on_error", 1),
        ("count_value", "asm"),
        ("return_value", "halt"),
    ],
)
def test_read_sketch_rejects_invalid_semantic_fields(field, value):
    """Oracle: no invalid-input defaults or implicit type coercion."""
    with pytest.raises(ValueError):
        pilot.render_read_sketch(_read_sketch_response(**{field: value}))


def test_read_repair_has_five_distinct_single_field_alternatives():
    """Oracle: fixed alternatives preserve offsets and do not encode a chosen winner."""
    sketch, _ = pilot.render_read_sketch(_read_sketch_response(clear_on_error=False))
    alternatives = pilot.repair_hypotheses("read", sketch)
    assert len(alternatives) == 5
    assert len({json.dumps(value, sort_keys=True) for _, value in alternatives}) == 5
    for _, value in alternatives:
        assert sum(value[key] != sketch[key] for key in sketch) == 1
        for key in pilot.READ_SKETCH_SCHEMA["required"][:4]:
            assert value[key] == sketch[key]


def test_read_error_clear_mutant_repaired_with_binary_training_only(tmp_path):
    """Oracle: real independent refill counterexamples select a bounded state repair."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD or probe toolchain unavailable")
    seed = tmp_path / "seed"
    seed.mkdir()
    workspace = pilot.snapshot(root, seed / "workspace")
    response = _read_sketch_response(clear_on_error=False)
    sketch, source = pilot.render_read_sketch(response)
    (workspace / "targets/liero/src/FUN_24dd_375e.inc").write_text(source)
    (seed / "raw-response.json").write_text(json.dumps(response))
    (seed / "sketch.json").write_text(json.dumps(sketch))
    report = pilot.probe(workspace, seed / "training", "read", "training")
    assert report["status"] == "failed"
    assert all(
        row["calls"][-1]["status"] == "failed" for row in report["fixtures"].values()
    )
    seen = {pilot.digest(seed / "training/candidate/FUN_24dd_375e.inc")}
    repair = pilot.run_sketch_repair(
        root,
        tmp_path / "repair",
        seed,
        kind="read",
        seen_sources=seen,
    )
    assert repair["status"] == "passed"
    assert repair["hypotheses"][0]["reused_seed_report"]
    assert repair["hypotheses"][1]["hypothesis"] == "toggle-error-clear"
    assert repair["hypotheses"][1]["training_calls_passed"] == 64
    assert repair["hypotheses"][1]["heldout_status"] == "passed"
    assert len(repair["hypotheses"]) == 2
    _, oversized = pilot.render_read_sketch(
        _read_sketch_response(capacity_byte_offset=2)
    )
    (workspace / "targets/liero/src/FUN_24dd_375e.inc").write_text(oversized)
    with pytest.raises(subprocess.CalledProcessError) as failure:
        pilot.probe(workspace, seed / "oversized", "read", "training")
    assert failure.value.returncode == 9


@pytest.mark.parametrize("retest_seed", [True, False])
def test_branch_repair_only_swaps_returns_and_gates_heldout(
    tmp_path, monkeypatch, retest_seed
):
    """Oracle: unchanged failure and swapped success retain separate evidence."""
    seed = tmp_path / "seed"
    (seed / "training/candidate").mkdir(parents=True)
    response = _sketch_response(then_return="dos_close_status", else_return="zero")
    sketch, source = pilot.render_close_sketch(response)
    (seed / "raw-response.json").write_text(json.dumps(response))
    (seed / "sketch.json").write_text(json.dumps(sketch))
    (seed / "training/candidate/FUN_24dd_37d3.inc").write_text(source)
    (seed / "training/result.json").write_text("{}")
    root = tmp_path / "root"
    binary = root / "extracted/liero/LIERO.EXE"
    binary.parent.mkdir(parents=True)
    binary.write_bytes(b"original")
    (root / "targets/liero/src").mkdir(parents=True)
    (root / "targets/liero/recovery.json").write_text("{}")
    for routine, _, _ in pilot.PANEL.values():
        (root / f"targets/liero/src/{routine}.inc").write_text("protected")
    monkeypatch.setattr(
        pilot.handler,
        "validate_saved_report",
        lambda *_args: {
            "contract": pilot.handler.CLOSE_CONTRACT,
            "status": "failed",
            "binary_sha256": pilot.digest(binary),
        },
    )

    def snapshot(_root, path):
        (path / "targets/liero/src").mkdir(parents=True)
        return path

    calls = []

    def probe(workspace, _output, _kind, suite):
        calls.append((workspace.parent.name, suite))
        status = "failed" if workspace.parent.name == "unchanged" else "passed"
        return {
            "status": status,
            "fixtures": {"case": {"calls": [{"status": status}] * 8}},
        }

    monkeypatch.setattr(pilot, "snapshot", snapshot)
    monkeypatch.setattr(pilot, "probe", probe)
    seen = {pilot.digest(seed / "training/candidate/FUN_24dd_37d3.inc")}
    result = pilot.run_close_branch_repair(
        root,
        tmp_path / "out",
        seed,
        retest_seed=retest_seed,
        seen_sources=None if retest_seed else seen,
    )
    assert result["status"] == "passed"
    assert result["model_requests"] == 0
    assert calls == (
        [
            ("unchanged", "training"),
        ]
        if retest_seed
        else []
    ) + [
        ("swapped", "training"),
        ("swapped", "heldout" if retest_seed else "heldout-v2"),
    ]
    left, right = result["hypotheses"]
    if retest_seed:
        assert left["training_calls_passed"] == 0
    else:
        assert left["reused_seed_report"]
    assert right["training_calls_passed"] == 8
    for key in ("handle_byte_offset", "operator", "threshold"):
        assert left["sketch"][key] == right["sketch"][key]
    assert left["sketch"]["then_return"] == right["sketch"]["else_return"]
    calls.clear()
    duplicate = pilot.run_close_branch_repair(
        root,
        tmp_path / "duplicate",
        seed,
        retest_seed=False,
        seen_sources={item["source_sha256"] for item in result["hypotheses"]},
    )
    assert duplicate["status"] == "failed"
    assert duplicate["hypotheses"][-1]["reason"] == "duplicate candidate"
    assert calls == []
    (seed / "sketch.json").write_text("{}")
    with pytest.raises(ValueError, match="disagrees"):
        pilot.run_close_branch_repair(root, tmp_path / "rejected", seed)


@pytest.mark.parametrize("heldout_status", ["passed", "failed"])
@pytest.mark.parametrize("kind", ["close", "read", "constructor"])
def test_automatic_close_repair_stops_after_selected_holdout(
    tmp_path, monkeypatch, heldout_status, kind
):
    """Oracle: failed proposal automatically triggers repair without another request."""

    def snapshot(_root, path):
        (path / "targets/liero/src").mkdir(parents=True)
        return path

    calls = []
    monkeypatch.setattr(pilot, "snapshot", snapshot)
    monkeypatch.setattr(pilot, "assembly", lambda *_: "original bytes")
    monkeypatch.setattr(
        pilot,
        "probe",
        lambda _root, path, *_: {
            "status": "passed" if "control" in path.name else "failed"
        },
    )
    monkeypatch.setattr(
        pilot,
        "request",
        lambda *_args, **_kwargs: json.dumps(
            _sketch_response(then_return="dos_close_status", else_return="zero")
            if kind == "close"
            else _read_sketch_response(clear_on_error=False)
            if kind == "read"
            else _constructor_sketch_response(name_limit=78)
        ),
    )

    def repair(root, output, seed, *, retest_seed, seen_sources, **kwargs):
        calls.append(seed.name)
        assert not retest_seed
        assert len(seen_sources) == 1
        assert kwargs == ({"kind": kind} if kind != "close" else {})
        return {
            "status": heldout_status,
            "hypotheses": [
                {"training_status": "passed", "heldout_status": heldout_status}
            ],
        }

    monkeypatch.setattr(
        pilot,
        "run_close_branch_repair" if kind == "close" else "run_sketch_repair",
        repair,
    )
    result = pilot.run_routine(
        tmp_path,
        tmp_path / "run",
        kind,
        "local",
        "local",
        4,
        constrained_close=kind == "close",
        automatic_close_repair=kind == "close",
        automatic_read_repair=kind == "read",
        automatic_constructor_repair=kind == "constructor",
    )
    assert result["status"] == heldout_status
    assert result["selected_by"] == (
        "deterministic-branch-repair"
        if kind == "close"
        else "deterministic-state-repair"
    )
    assert ("accepted_by" in result) == (heldout_status == "passed")
    assert len(result["attempts"]) == 1
    assert result["attempts"][0]["training_status"] == "failed"
    assert calls == ["proposal-01"]


def test_constructor_feedback_retains_valid_json_and_explicit_omissions():
    """Oracle: large byte mismatches cannot truncate retry JSON mid-value."""
    cases = [
        {
            "case": f"pattern-{i}",
            "status": "failed",
            "differences": [
                {"offset": j, "original": 255, "pascal": 0, "contract": 255}
                for j in range(544)
            ],
        }
        for i in range(514)
    ]
    text = pilot.training_feedback(
        {
            "function": pilot.PANEL["constructor"][0],
            "status": "failed",
            "cases": cases,
        }
    )
    feedback = json.loads(text)
    assert len(text) < 12000
    assert feedback["failed_case_count"] == 514
    assert feedback["omitted_failed_cases"] == 506
    assert len(feedback["failed_cases"]) == 8
    assert feedback["failed_cases"][0]["difference_count"] == 544
    assert len(feedback["failed_cases"][0]["differences"]) == 8


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("handle_byte_offset", True),
        ("handle_byte_offset", 1),
        ("handle_byte_offset", 256),
        ("threshold", -1),
        ("threshold", 65536),
        ("threshold", 4.0),
        ("operator", "asm"),
        ("then_return", "Halt(0)"),
        ("else_return", "unresolved"),
    ],
)
def test_close_sketch_rejects_invalid_values(field, value):
    """Oracle: invalid sketch input is rejected, never silently repaired."""
    with pytest.raises(ValueError):
        pilot.render_close_sketch(_sketch_response(**{field: value}))
    with pytest.raises(ValueError):
        pilot.render_close_sketch({"response": '{"source":"inline assembly"}'})


def test_close_sketch_renders_competing_hypotheses_without_correcting_them():
    """Oracle: renderer fixes syntax/interface, not model-selected semantics."""
    sketch, source = pilot.render_close_sketch(_sketch_response(threshold=3))
    assert sketch["threshold"] == 3
    assert "if handle <= 3 then" in source
    assert "dosClose(handle)" in source
    assert pilot.CLOSE_INTERFACE in source
    _, other = pilot.render_close_sketch(
        _sketch_response(
            handle_byte_offset=2, operator=">", then_return="handle", else_return="zero"
        )
    )
    assert "Inc(objectWord, 1)" in other
    assert "FUN_24dd_37d3 := handle" in other


def test_close_sketch_request_uses_schema(tmp_path, monkeypatch):
    """Oracle: model receives structural constraints, not the correct threshold."""
    monkeypatch.setattr(pilot, "snapshot", lambda *_args: tmp_path)
    monkeypatch.setattr(pilot, "probe", lambda *_args: {"status": "passed"})
    monkeypatch.setattr(pilot, "assembly", lambda *_args: "original instruction bytes")
    messages = []

    def fake_request(prompt, _model, _endpoint, *, schema):
        messages.append(prompt)
        assert schema == pilot.CLOSE_SKETCH_SCHEMA
        return json.dumps({"response": "{}"})

    monkeypatch.setattr(pilot, "request", fake_request)
    result = pilot.run_routine(
        tmp_path,
        tmp_path / "run",
        "close",
        "local",
        "local",
        1,
        constrained_close=True,
    )
    assert result["status"] == "failed"
    assert "single word load" in result["search_scope"]
    assert "NEVER Pascal or assembly" in messages[0]
    assert json.loads((tmp_path / "run/proposal-schema.json").read_text()) == (
        pilot.CLOSE_SKETCH_SCHEMA
    )
    with pytest.raises(ValueError, match="limited to"):
        pilot.run_routine(
            tmp_path,
            tmp_path / "other",
            "read",
            "local",
            "local",
            1,
            constrained_close=True,
        )


def test_close_sketch_training_failure_blocks_heldout_and_stops_duplicate(
    tmp_path, monkeypatch
):
    """Oracle: compilable sketch gets no heldout feedback after training failure."""
    roots = []

    def workspace(_root, path):
        source = path / "targets/liero/src/FUN_24dd_37d3.inc"
        source.parent.mkdir(parents=True)
        source.write_text("original")
        roots.append(path)
        return path

    calls = []

    def fake_probe(_root, output, _kind, suite):
        calls.append((output.name, suite))
        if output.name.startswith("control"):
            return {"status": "passed"}
        return {
            "status": "failed",
            "fixtures": {
                "case": {
                    "calls": [{"handle": 0, "original_return": 0, "pascal_return": 6}]
                }
            },
        }

    messages = []

    def fake_request(prompt, *_args, schema):
        assert schema == pilot.CLOSE_SKETCH_SCHEMA
        messages.append(prompt)
        return json.dumps(
            _sketch_response(then_return="dos_close_status", else_return="zero")
        )

    monkeypatch.setattr(pilot, "snapshot", workspace)
    monkeypatch.setattr(pilot, "probe", fake_probe)
    monkeypatch.setattr(pilot, "assembly", lambda *_args: "instructions")
    monkeypatch.setattr(pilot, "request", fake_request)
    result = pilot.run_routine(
        tmp_path,
        tmp_path / "run",
        "close",
        "local",
        "local",
        4,
        constrained_close=True,
    )
    assert result["status"] == "failed"
    assert result["unique_candidates"] == 1
    assert result["reason"] == "duplicate candidate"
    assert len(roots) == 2
    assert calls == [
        ("control-training", "training"),
        ("control-heldout", "heldout"),
        ("training", "training"),
    ]
    assert '"pascal_return": 6' in messages[1]
    assert (tmp_path / "run/proposal-01/sketch.json").is_file()


def test_close_sketch_real_binary_rejects_compiled_wrong_threshold(tmp_path):
    """Oracle: restricted syntax does not make a wrong hypothesis a passing routine."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file() or any(
        shutil.which(tool) is None for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("BYOD or probe tools unavailable")
    output = tmp_path / "control"
    report = pilot.handler.run_probe(output, root, handler="close", suite="training")
    assert report["status"] == "passed"
    directory = output / "candidate"
    source = directory / "FUN_24dd_37d3.inc"
    fixture = output / "handle-lifecycle"
    for threshold, expected in ((4, "passed"), (3, "failed")):
        _, rendered = pilot.render_close_sketch(_sketch_response(threshold=threshold))
        source.write_text(rendered)
        executable = pilot.handler.compile_candidate(directory, handler="close")
        candidate_output = output / f"sketch-{threshold}.bin"
        subprocess.run(
            [
                str(executable),
                str(fixture / "STATE.BIN"),
                str(fixture / "INPUT.TXT"),
                str(candidate_output),
                "128",
            ],
            check=True,
            capture_output=True,
            timeout=30,
        )
        comparison = pilot.handler.compare_close(
            (fixture / "TRACE.BIN").read_bytes(), candidate_output.read_bytes()
        )
        assert comparison["status"] == expected


def test_fixed_suites_are_disjoint_and_cover_existing_corpora():
    """Oracle: frozen holdouts are not training inputs."""
    training = pilot.constructor.constructor_cases("training")
    heldout = pilot.constructor.constructor_cases("heldout")
    assert len(training) == 514
    assert len(heldout) == 264
    assert {case.data for case in training}.isdisjoint(case.data for case in heldout)
    assert len(training) + len(heldout) == len(pilot.constructor.constructor_cases())
    for kind in ("read", "close"):
        train = pilot.handler.fixtures(kind, "training")
        held = pilot.handler.fixtures(kind, "heldout")
        assert train.keys().isdisjoint(held)
        assert set(train.values()).isdisjoint(held.values())
    with pytest.raises(ValueError):
        pilot.constructor.constructor_cases("typo")
    with pytest.raises(ValueError):
        pilot.handler.fixtures("read", "typo")


def test_training_gate_and_duplicate_stop(tmp_path, monkeypatch):
    """Oracle: failing training never exposes candidate heldout, duplicates stop."""
    root = tmp_path / "source"
    source = root / "targets/liero/src/FUN_24dd_37d3.inc"
    source.parent.mkdir(parents=True)
    source.write_text("original")
    calls = []

    def fake_probe(_root, output, _kind, suite):
        calls.append((output.name, suite))
        return {"status": "passed" if output.name.startswith("control") else "failed"}

    monkeypatch.setattr(pilot, "snapshot", lambda *_args: root)
    monkeypatch.setattr(pilot, "probe", fake_probe)
    monkeypatch.setattr(pilot, "assembly", lambda *_args: "original instructions")
    monkeypatch.setattr(
        pilot,
        "request",
        lambda *_args: json.dumps(
            {
                "response": json.dumps(
                    {"source": "function FUN_24dd_37d3: Word; begin end;"}
                )
            }
        ),
    )
    result = pilot.run_routine(root, tmp_path / "run", "close", "local", "local", 4)
    assert calls == [
        ("control-training", "training"),
        ("control-heldout", "heldout"),
        ("training", "training"),
    ]
    assert len(result["attempts"]) == 2
    assert result["attempts"][-1]["reason"] == "duplicate candidate"
    assert result["status"] == "failed"


def test_heldout_failure_never_feeds_another_candidate(tmp_path, monkeypatch):
    """Oracle: selected candidate sees heldout once, with no heldout repair."""
    root = tmp_path / "source"
    source = root / "targets/liero/src/FUN_24dd_37d3.inc"
    source.parent.mkdir(parents=True)
    source.write_text("original")
    monkeypatch.setattr(pilot, "snapshot", lambda *_args: root)
    monkeypatch.setattr(pilot, "assembly", lambda *_args: "original instructions")
    monkeypatch.setattr(
        pilot,
        "probe",
        lambda _root, path, *_args: {
            "status": "failed" if path.name == "heldout" else "passed"
        },
    )
    monkeypatch.setattr(
        pilot,
        "request",
        lambda *_args: json.dumps(
            {
                "response": json.dumps(
                    {"source": "function FUN_24dd_37d3: Word; begin end;"}
                )
            }
        ),
    )
    result = pilot.run_routine(root, tmp_path / "run", "close", "local", "local", 4)
    assert result["status"] == "failed"
    assert len(result["attempts"]) == 1
    assert result["attempts"][0]["training_status"] == "passed"
    assert result["attempts"][0]["heldout_status"] == "failed"


def test_failed_control_blocks_generation(tmp_path, monkeypatch):
    """Oracle: invalid positive control blocks the routine before model use."""
    monkeypatch.setattr(pilot, "snapshot", lambda *_args: tmp_path)
    monkeypatch.setattr(pilot, "probe", lambda *_args: {"status": "failed"})
    monkeypatch.setattr(pilot, "request", lambda *_args: pytest.fail("model called"))
    result = pilot.run_routine(tmp_path, tmp_path / "run", "close", "local", "local", 4)
    assert result["status"] == "blocked"
    assert not result["attempts"]


def test_byod_gate_and_budget(tmp_path):
    """Oracle: no executable skips; oversized budgets fail before any work."""
    assert (
        pilot.run_pilot(tmp_path, tmp_path / "out", model="local")["status"]
        == "skipped"
    )
    with pytest.raises(ValueError):
        pilot.run_pilot(tmp_path, tmp_path / "out", model="local", budget=5)


def test_candidate_rejects_directives_and_file_services():
    """Oracle: generated code cannot replace the probe's compiler mode or adapters."""
    for source in (
        "{$I malicious.inc} procedure FUN_24dd_3639; begin end;",
        "procedure FUN_24dd_3639; begin Halt(0); end;",
    ):
        with pytest.raises(ValueError):
            pilot.candidate_source(
                {"response": json.dumps({"source": source})}, "FUN_24dd_3639"
            )


def test_snapshot_copies_only_probe_inputs_and_contains_original(tmp_path):
    """Oracle: snapshots exclude opaque runtime files and retain contained BYOD."""
    root = tmp_path / "repository"
    for relative in (
        "engine",
        "tools",
        "targets/liero/asm",
        "targets/liero/decomp",
        "targets/liero/config",
        "targets/liero/src",
        "targets/liero/tests",
    ):
        (root / relative).mkdir(parents=True)
    binary = root / "extracted/liero/LIERO.EXE"
    binary.parent.mkdir(parents=True)
    binary.write_bytes(b"fixture")
    (root / "targets/liero/core.1").write_bytes(b"not-a-probe-input")
    (root / "targets/liero/alternate_streams.json").write_text("{}")

    workspace = pilot.snapshot(root, tmp_path / "workspace")

    copied = workspace / "extracted/liero/LIERO.EXE"
    assert copied.read_bytes() == binary.read_bytes()
    assert copied.resolve().is_relative_to(workspace.resolve())
    assert not (workspace / "targets/liero/core.1").exists()
    assert (workspace / "targets/liero/alternate_streams.json").is_file()


def test_compiler_diagnostics_reach_retry_and_workspaces_stay_isolated(
    tmp_path, monkeypatch
):
    """Oracle: retries receive actual compiler errors, not merely an exit code."""
    roots = []

    def fake_snapshot(_root, output):
        source = output / "targets/liero/src/FUN_24dd_37d3.inc"
        source.parent.mkdir(parents=True)
        source.write_text("original")
        roots.append(output)
        return output

    def fake_probe(_root, output, *_args):
        if output.name.startswith("control"):
            return {"status": "passed"}
        raise subprocess.CalledProcessError(
            1, ["fpc"], output=b'Error: Identifier not found "TLieroDosClose"'
        )

    prompts = []

    def fake_request(prompt, *_args):
        prompts.append(prompt)
        return json.dumps(
            {
                "response": json.dumps(
                    {"source": "function FUN_24dd_37d3: Word; begin end;"}
                )
            }
        )

    monkeypatch.setattr(pilot, "snapshot", fake_snapshot)
    monkeypatch.setattr(pilot, "probe", fake_probe)
    monkeypatch.setattr(pilot, "assembly", lambda *_args: "instructions")
    monkeypatch.setattr(pilot, "request", fake_request)
    pilot.run_routine(tmp_path, tmp_path / "run", "close", "local", "local", 4)

    assert 'Identifier not found "TLieroDosClose"' in prompts[1]
    assert len(roots) == 2
    assert roots[0].name == "control-workspace"
    assert (roots[0] / "targets/liero/src/FUN_24dd_37d3.inc").read_text() == "original"


@pytest.mark.parametrize("response", ["invalid-envelope", '{"response":"not-json"}'])
def test_malformed_model_responses_are_retained(tmp_path, monkeypatch, response):
    """Oracle: rejected raw output remains inspectable and cannot become a pass."""
    monkeypatch.setattr(pilot, "snapshot", lambda *_args: tmp_path)
    monkeypatch.setattr(pilot, "probe", lambda *_args: {"status": "passed"})
    monkeypatch.setattr(pilot, "assembly", lambda *_args: "instructions")
    monkeypatch.setattr(pilot, "request", lambda *_args: response)
    result = pilot.run_routine(tmp_path, tmp_path / "run", "close", "local", "local", 1)
    assert result["status"] == "failed"
    assert (tmp_path / "run/proposal-01/raw-response.json").read_text() == response


def test_model_connection_error_is_persisted_as_blocked(tmp_path, monkeypatch):
    """Oracle: service errors block explicitly rather than counting a failed candidate."""
    monkeypatch.setattr(pilot, "snapshot", lambda *_args: tmp_path)
    monkeypatch.setattr(pilot, "probe", lambda *_args: {"status": "passed"})
    monkeypatch.setattr(pilot, "assembly", lambda *_args: "instructions")

    def unavailable(*_args):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(pilot, "request", unavailable)
    result = pilot.run_routine(tmp_path, tmp_path / "run", "close", "local", "local", 4)
    assert result["status"] == "blocked"
    assert "offline" in result["reason"]
    assert json.loads((tmp_path / "run/result.json").read_text()) == result


def test_recovered_retrieval_excludes_stale_unchecked_and_pilot_bodies(
    tmp_path, monkeypatch
):
    """Oracle: scoped local retrieval does not promote or leak evaluation targets."""
    target = tmp_path / "targets/liero"
    (target / "src").mkdir(parents=True)
    (target / "asm").mkdir()
    name = "FUN_checked"
    source = target / "src" / f"{name}.inc"
    source.write_text("{ old UNMATCHED commentary }\nprocedure FUN_checked; begin end;")
    (target / "asm" / f"{name}.s").write_text("24dd:0010 XOR AX,AX\n")
    ledger = {
        "functions": {
            name: {
                "source_file": f"src/{name}.inc",
                "review_notes": "reviewed",
                "verification": {"notes": "host test only"},
            }
        }
    }
    ledger_path = target / "recovery.json"
    ledger_path.write_text(json.dumps(ledger))
    before = ledger_path.read_bytes()
    routines = [
        {"name": name, "source_recovered": True, "behavior_verified": True},
        {"name": "FUN_stale", "source_recovered": False, "behavior_verified": True},
        {"name": "FUN_unchecked", "source_recovered": True, "behavior_verified": False},
        *(
            {"name": entry[0], "source_recovered": True, "behavior_verified": True}
            for entry in pilot.PANEL.values()
        ),
    ]
    monkeypatch.setattr(pilot, "audit_target", lambda _target: {"routines": routines})

    examples = pilot.recovered_examples(tmp_path, "24dd:0000 XOR AX,AX\n")

    assert [example["fn"] for example in examples] == [name]
    assert examples[0]["pascal"] == "procedure FUN_checked; begin end;"
    assert examples[0]["source_sha256"] == pilot.digest(source)
    assert "NOT binary parity" in examples[0]["oracle"]
    assert ledger_path.read_bytes() == before
    with pytest.raises(ValueError, match="no current"):
        pilot.recovered_context([])


def test_recovered_prompt_enforces_close_interface_before_compilation(
    tmp_path, monkeypatch
):
    """Oracle: examples do not permit omitted callback declarations or self examples."""
    monkeypatch.setattr(pilot, "snapshot", lambda *_args: tmp_path)
    calls = []

    def control(_root, path, *_args):
        calls.append(path.name)
        return {"status": "passed"}

    monkeypatch.setattr(pilot, "probe", control)
    monkeypatch.setattr(pilot, "assembly", lambda *_args: "instructions")
    monkeypatch.setattr(
        pilot,
        "recovered_examples",
        lambda *_args: [
            {
                "fn": "FUN_checked",
                "oracle": "host only",
                "asm": "24dd:0000 XOR AX,AX",
                "pascal": "procedure FUN_checked; begin end;",
            }
        ],
    )
    prompts = []

    def missing_type(prompt, *_args):
        prompts.append(prompt)
        return json.dumps(
            {
                "response": json.dumps(
                    {"source": "function FUN_24dd_37d3: Word; begin end;"}
                )
            }
        )

    monkeypatch.setattr(pilot, "request", missing_type)
    result = pilot.run_routine(
        tmp_path, tmp_path / "run", "close", "local", "local", 1, use_recovered=True
    )
    assert result["status"] == "failed"
    assert "Missing or changed" in result["attempts"][0]["reason"]
    assert "procedure FUN_checked" in prompts[0]
    assert pilot.CLOSE_INTERFACE in prompts[0]
    assert calls == ["control-training", "control-heldout"]
    assert (tmp_path / "run/recovered-examples.json").is_file()
