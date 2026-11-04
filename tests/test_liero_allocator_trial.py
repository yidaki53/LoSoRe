import io
import json
import pathlib
import shutil
import struct
import subprocess
import urllib.error

import pytest

from tools import liero_four_routine_pilot as pilot

ROOT = pathlib.Path(__file__).resolve().parents[1]

CONTROL = (
    pilot.ALLOCATOR_INTERFACE
    + """
var rounded, off, seg: LongWord;
begin
  resultOffset := 0; resultSegment := 0; failed := false;
  if requestSize = 0 then Exit;
  savedRequest := requestSize;
  rounded := ((LongWord(requestSize) + 7) div 8) * 8;
  off := startOffset + (rounded mod 16);
  seg := startSegment + rounded div 16;
  if (off and 255) >= 16 then Inc(seg);
  off := off and $ff0f;
  if (seg > limitSegment) or ((seg = limitSegment) and (off > limitOffset)) then
  begin
    resultSegment := seg;
    failed := true
  end
  else begin
    resultOffset := startOffset; resultSegment := startSegment;
    newOffset := off; newSegment := seg;
  end;
end;
"""
)


def test_allocator_case_freeze_disjoint_suites():
    """Oracle: explicit input uniqueness/disjointness, fixed budgets."""
    training = pilot.allocator_cases("training")
    heldout = pilot.allocator_cases("heldout")
    assert len(training) == len(set(training)) == 64
    assert len(heldout) == len(set(heldout)) == 48
    assert not set(training) & set(heldout)
    with pytest.raises(ValueError):
        pilot.allocator_cases("other")


def _allocator_bytes():
    """Oracle: saved byte fixtures, not a substitute for live binary provenance."""
    contracts = json.loads(
        (ROOT / "targets/liero/config/routine_contracts.json").read_text()
    )["functions"]
    return (
        bytes.fromhex(contracts["FUN_24dd_0353"]["reviewed_bytes_hex"]),
        bytes.fromhex(contracts["FUN_24dd_04dc"]["reviewed_bytes_hex"]),
        bytes.fromhex("33c0ca0200"),
    )


def test_allocator_deduction_accounts_for_historical_semantic_failures():
    """Oracle: exact bytes establish obligations, not a model-selected sketch."""
    from engine.instruction_facts import allocator_empty_list_contract

    facts = allocator_empty_list_contract(*_allocator_bytes())
    assert facts["rounding"] == {"bias": 7, "alignment": 8, "paragraph": 16}
    assert facts["saved_request_cell"] == 0x7B3C
    assert facts["limit_order"] == ["segment", "offset"]
    assert facts["success_return"] == "old_head"
    assert facts["failure_return"] == {"AX": 0, "DX": "computed_segment", "CF": 1}
    assert facts["zero_writes"] == []
    assert facts["source_recovered"] is False
    assert len(facts["unresolved"]) == 4
    source = pilot.render_allocator_empty_source(facts)
    assert "LongWord(requestSize) + 7" in source
    assert "savedRequest := requestSize" in source
    assert "resultOffset := startOffset" in source
    assert "resultSegment := seg" in source
    from engine.routine_contract import load_contract, prompt_context

    context = prompt_context(load_contract(ROOT / "targets/liero", "FUN_24dd_0353"))
    assert "Deductive empty-list composition" in context
    assert "not AI discovery" in context
    assert "computed DX retained" in context


@pytest.mark.parametrize("dependency", range(3))
def test_allocator_deduction_rejects_every_changed_instruction_byte(dependency):
    """Oracle: this narrow composition never generalizes an unrecognized opcode."""
    from engine.instruction_facts import allocator_empty_list_contract

    inputs = list(_allocator_bytes())
    for offset in range(len(inputs[dependency])):
        changed = bytearray(inputs[dependency])
        changed[offset] ^= 1
        arguments = inputs.copy()
        arguments[dependency] = bytes(changed)
        with pytest.raises(ValueError, match="allocator"):
            allocator_empty_list_contract(*arguments)


@pytest.mark.parametrize(
    "field,value",
    [
        ("saved_request_cell", 0),
        ("rounding", {"bias": 0, "alignment": 1, "paragraph": 16}),
        ("limit_order", ["offset", "segment"]),
        ("success_return", "new_frontier"),
        ("failure_return", {"AX": 0, "DX": 0, "CF": 1}),
    ],
)
def test_allocator_renderer_rejects_contradictory_obligations(field, value):
    """Oracle: do not silently correct a contradictory source-generation contract."""
    from engine.instruction_facts import allocator_empty_list_contract

    facts = allocator_empty_list_contract(*_allocator_bytes())
    facts[field] = value
    with pytest.raises(ValueError, match="obligations"):
        pilot.render_allocator_empty_source(facts)


@pytest.mark.parametrize("failure", ["none", "training", "heldout", "partial", "drift"])
def test_allocator_deduction_has_no_model_or_retry_budget(
    tmp_path, monkeypatch, failure
):
    """Oracle: injected execution; complete shapes and frozen methods gate validation."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    calls = []

    def original(root, output, cases, binary, contract):
        """Oracle: fixed synthetic original rows, not original execution."""
        calls.append(output.name)
        return [[0] * 8 for _ in cases]

    def candidate(output, source, cases):
        """Oracle: injected mismatches, partial output or premise drift."""
        calls.append(output.name)
        if failure == "drift" and output.name.endswith("training"):
            freeze = output.parent / "freeze.json"
            freeze.write_text("{}")
        count = len(cases) - int(failure == "partial")
        value = int(output.name == f"candidate-{failure}")
        return [[value] * 8 for _ in range(count)]

    def no_model(*args, **kwargs):
        """Oracle: deduction must not call a model identity or generation endpoint."""
        pytest.fail("deduced semantics do not need a model")

    monkeypatch.setattr(pilot, "allocator_original", original)
    monkeypatch.setattr(pilot, "allocator_candidate", candidate)
    monkeypatch.setattr(pilot, "request", no_model)
    monkeypatch.setattr(pilot, "leaf_model_identity", no_model)
    output = tmp_path / "deduced"
    result = pilot.run_allocator_deduction(ROOT, output)
    reaches_heldout = failure in {"none", "heldout"}
    assert result["model_requests"] == 0
    assert result["heldout_evaluations"] == int(reaches_heldout)
    assert ("original-heldout" in calls) == reaches_heldout
    assert result["status"] == ("passed" if failure == "none" else "failed")
    assert result["source_promoted"] is False
    assert result["routine_recovered"] is False
    assert result["automatic_discovery"] is False
    assert (output / "result.json").is_file()
    assert (output / "obligations.json").is_file()
    assert (output / "candidate.inc").read_text().startswith("procedure FUN_24dd_0353")


def test_allocator_deduction_missing_original_skips(tmp_path):
    """Oracle: no BYOD means no deduction run or success-shaped artifacts."""
    result = pilot.run_allocator_deduction(tmp_path, tmp_path / "deduced")
    assert result["status"] == "skipped"
    assert not (tmp_path / "deduced").exists()


def _deduction_fixture(tmp_path, monkeypatch):
    """Oracle: synthetic artifacts exercise replay/invalidation, not DOS execution."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")

    def rows(cases):
        """Oracle: developer-known projection used only to construct synthetic evidence."""
        results = []
        for request, offset, segment, limit_offset, limit_segment in cases:
            row = [0, 0, 0, offset, segment, offset, segment, 0xA5A5]
            if request:
                rounded = (request + 7) // 8 * 8
                off = offset + rounded % 16
                seg = segment + rounded // 16 + (off >= 16)
                off %= 16
                row[7] = request
                if (seg, off) > (limit_segment, limit_offset):
                    row[:3] = [0, seg, 1]
                else:
                    row[:3] = [offset, segment, 0]
                    row[3:7] = [off, seg, off, seg]
            results.append(row)
        return results

    def original(root, output, cases, binary, contract):
        """Oracle: synthetic guard-valid records with authenticated copied dependencies."""
        output.mkdir()
        case_path = output / "CASES.BIN"
        case_path.write_bytes(b"".join(struct.pack("<5H", *case) for case in cases))
        (output / "harness.S").write_text(
            pilot.allocator_harness(case_path.resolve(), len(cases))
        )
        image = bytearray(0x5000)
        for offset, raw in zip((0x353, 0x4DC), _allocator_bytes()[:2], strict=True):
            image[offset - 0x100 : offset - 0x100 + len(raw)] = raw
        (output / "PROBE.COM").write_bytes(image)
        records = []
        for case, row in zip(cases, rows(cases), strict=True):
            memory = bytearray([0xA5] * 56)
            for cell, value in (
                (0x63EE, row[3]),
                (0x63F0, 0x2000 + row[4]),
                (0x63F2, case[3]),
                (0x63F4, 0x2000 + case[4]),
                (0x63F6, row[5]),
                (0x63F8, 0x2000 + row[6]),
                (0x63FE, 0xD6),
                (0x6400, 0x2000),
            ):
                struct.pack_into("<H", memory, cell - 0x63D8, value)
            records.append(struct.pack("<8H", *row) + memory + bytes([0xA5] * 128))
        (output / "TRACE.BIN").write_bytes(b"".join(records))
        return pilot.allocator_original_rows(b"".join(records), cases)

    def candidate(output, source, cases):
        """Oracle: synthetic host records; no compiler success is claimed by this fixture."""
        output.mkdir()
        (output / "candidate.inc").write_text(source)
        (output / "probe.pas").write_text(pilot.allocator_candidate_program(cases))
        (output / "probe").write_bytes(b"synthetic executable identity")
        for name in ("compile.log", "execution.log"):
            (output / name).write_text("synthetic replay fixture\n")
        (output / "PASCAL.BIN").write_bytes(
            b"".join(struct.pack("<8H", *row) for row in rows(cases))
        )
        return rows(cases)

    monkeypatch.setattr(pilot, "allocator_original", original)
    monkeypatch.setattr(pilot, "allocator_candidate", candidate)
    output = tmp_path / "deduced"
    assert pilot.run_allocator_deduction(ROOT, output)["status"] == "passed"
    return output


def test_allocator_replay_and_graph_keep_caller_applicability_unknown(
    tmp_path, monkeypatch
):
    """Oracle: revalidated synthetic projection cannot become a real caller contract."""
    from engine.scoped_verification import allocator_contract_graph, allocator_frontier

    output = _deduction_fixture(tmp_path, monkeypatch)
    report = pilot.validate_allocator_deduction(ROOT, output)
    assert report["training"]["passed"] == 64
    assert report["heldout"]["passed"] == 48
    graph = allocator_contract_graph(ROOT / "targets/liero", output)
    assert graph.facts["allocator.empty-list.checked"].status == "oracle-verified"
    assert graph.facts["allocator.caller.applicability"].status == "unknown"
    assert graph.propagate_same_value() == []
    assert graph.conflicts() == []
    frontier = allocator_frontier(ROOT / "targets/liero", output)
    assert frontier["allocator.empty-list"]["checked"] is True
    assert not any(
        "checked empty-list" in blocker
        for blocker in frontier["allocator.remaining-paths"]["blockers"]
    )
    assert frontier["allocator.caller028a"]["checked"] is False
    assert len(frontier["allocator.caller028a"]["blockers"]) == 3


@pytest.mark.parametrize(
    "filename,content",
    [
        ("candidate.inc", b"changed"),
        ("candidate-heldout/PASCAL.BIN", b"partial"),
        ("candidate-training/probe.pas", b"other program"),
        ("original-training/TRACE.BIN", b"partial"),
        ("obligations.json", b"{}"),
        ("freeze.json", b"{}"),
        ("review.json", b"{}"),
    ],
)
def test_allocator_replay_invalidates_changed_evidence(
    tmp_path, monkeypatch, filename, content
):
    """Oracle: changed premises/artifacts close the checked frontier without rerunning."""
    from engine.scoped_verification import allocator_frontier

    output = _deduction_fixture(tmp_path, monkeypatch)
    before = allocator_frontier(ROOT / "targets/liero", output)
    (output / filename).write_bytes(content)
    with pytest.raises((ValueError, KeyError)):
        pilot.validate_allocator_deduction(ROOT, output)
    after = allocator_frontier(ROOT / "targets/liero", output)
    assert before["allocator.empty-list"]["checked"] is True
    assert after["allocator.empty-list"]["checked"] is False
    assert after["allocator.empty-list"]["blockers"]
    assert "checked empty-list" in after["allocator.remaining-paths"]["blockers"][0]


def test_allocator_replay_rejects_missing_hashes_and_promotion(tmp_path, monkeypatch):
    """Oracle: success-shaped reports cannot remove identities or claim recovery."""
    output = _deduction_fixture(tmp_path, monkeypatch)
    path = output / "result.json"
    original = json.loads(path.read_text())
    for update in ({"artifact_hashes": {}}, {"routine_recovered": True}):
        path.write_text(json.dumps({**original, **update}))
        with pytest.raises(ValueError):
            pilot.validate_allocator_deduction(ROOT, output)


def test_allocator_puzzle_reuses_checked_evidence_and_never_tries_callers(
    tmp_path, monkeypatch
):
    """Oracle: existing scheduler sees one checked piece and explicit dependent blockers."""
    output = _deduction_fixture(tmp_path, monkeypatch)

    def no_comparison(*args):
        """Oracle: resumption cannot rerun the terminal suite."""
        pytest.fail("checked allocator evidence must be replayed, not re-executed")

    monkeypatch.setattr(pilot, "run_allocator_deduction", no_comparison)
    result = pilot.run_allocator_puzzle(ROOT, output)
    assert result["status"] == "scoped-frontier-blocked"
    assert result["new_comparisons"] == 0
    assert result["automatic_new_recoveries"] == 0
    assert result["puzzle"]["checked_passes"] == 1
    assert result["puzzle"]["measurements"] == []
    assert len(result["puzzle"]["leftovers"]) == 2
    assert (output / "contract-graph.json").is_file()


def test_allocator_puzzle_checks_one_ready_piece_and_removes_only_that_blocker(
    tmp_path, monkeypatch
):
    """Oracle: end-to-end scheduler adapter uses injected comparisons, not compilation as proof."""
    _deduction_fixture(tmp_path, monkeypatch)
    result = pilot.run_allocator_puzzle(ROOT, tmp_path / "fresh")
    assert result["known_scope_checked"] is True
    assert result["new_comparisons"] == 1
    assert len(result["puzzle"]["measurements"]) == 1
    assert result["puzzle"]["measurements"][0]["piece"] == "allocator.empty-list"
    assert len(result["puzzle"]["leftovers"]) == 2
    assert result["source_recovered"] == 0


def test_allocator_changed_premise_invalidates_checked_frontier(tmp_path, monkeypatch):
    """Oracle: a changed contract/method identity cannot retain a checked result."""
    from engine.scoped_verification import allocator_frontier

    output = _deduction_fixture(tmp_path, monkeypatch)
    before = allocator_frontier(ROOT / "targets/liero", output)
    freeze = pilot.allocator_deduction_freeze

    def changed(root, facts):
        """Oracle: injected premise change, without editing repository inputs."""
        return {**freeze(root, facts), "known_scope": "changed premise"}

    monkeypatch.setattr(pilot, "allocator_deduction_freeze", changed)
    after = allocator_frontier(ROOT / "targets/liero", output)
    assert after["allocator.empty-list"]["checked"] is False
    assert (
        before["allocator.empty-list"]["premise_sha256"]
        != after["allocator.empty-list"]["premise_sha256"]
    )
    assert after["allocator.caller028a"]["blockers"]


def test_allocator_original_control(tmp_path):
    """Oracle: developer-known control, separate preflight; not generated-candidate evidence."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD/probe tools unavailable")
    from engine.alternate_streams import load_binary_evidence
    from engine.routine_contract import load_contract

    target = ROOT / "targets/liero"
    binary, _, _, _ = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    contract = load_contract(target, "FUN_24dd_0353")
    cases = [
        (0, 0, 0x800, 0, 0x801),
        (1, 0, 0x800, 0, 0x800),
        (1, 8, 0x800, 0, 0x801),
        (16, 0, 0x800, 0, 0x801),
    ]
    original = pilot.allocator_original(
        ROOT, tmp_path / "original", cases, binary, contract
    )
    candidate = pilot.allocator_candidate(tmp_path / "control", CONTROL, cases)
    assert original == candidate
    assert original[0] == [0, 0, 0, 0, 0x800, 0, 0x800, 0xA5A5]
    assert original[1] == [0, 0x800, 1, 0, 0x800, 0, 0x800, 1]
    assert original[2] == [8, 0x800, 0, 0, 0x801, 0, 0x801, 1]


def test_allocator_compiler_failure_preserves_candidate(tmp_path):
    """Oracle: invalid candidate never becomes a baseline compile pass."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    with pytest.raises(subprocess.CalledProcessError):
        pilot.allocator_candidate(
            tmp_path / "bad", "not pascal", [(0, 0, 0x800, 0, 0x801)]
        )
    assert (tmp_path / "bad/candidate.inc").read_text() == "not pascal"
    assert (tmp_path / "bad/compile.log").stat().st_size
    assert not (tmp_path / "bad/PASCAL.BIN").exists()


@pytest.mark.parametrize(
    "training_pass,heldout_pass", [(False, False), (True, False), (True, True)]
)
@pytest.mark.parametrize("scaffold", [False, True])
def test_allocator_trial_one_proposal_and_no_heldout_feedback(
    tmp_path, monkeypatch, training_pass, heldout_pass, scaffold
):
    """Oracle: injected proposal/probes, no model/original execution; enforce no retries."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    calls = []

    def request(prompt, model, endpoint, *, schema=None):
        """Oracle: deterministic fake proposal."""
        calls.append("model")
        if scaffold:
            assert (
                schema["properties"]["source"]["pattern"]
                == "^procedure FUN_24dd_0353.*$"
            )
        return json.dumps({"response": json.dumps({"source": CONTROL})})

    def original(root, output, cases, binary, contract):
        """Oracle: deterministic fake original result."""
        assert (output.parent / "freeze.json").is_file()
        calls.append(output.name)
        return [[0] * 8] * len(cases)

    def candidate(output, source, cases):
        """Oracle: injected mismatch distinguishes training/heldout."""
        calls.append(output.name)
        passed = training_pass if output.name.endswith("training") else heldout_pass
        return [[0 if passed else 1] * 8] * len(cases)

    monkeypatch.setattr(pilot, "request", request)
    monkeypatch.setattr(
        pilot, "leaf_model_identity", lambda *args: {"name": "fake", "digest": "fake"}
    )
    monkeypatch.setattr(pilot, "allocator_original", original)
    monkeypatch.setattr(pilot, "allocator_candidate", candidate)
    previous = None
    if scaffold:
        previous = tmp_path / "previous"
        previous.mkdir()
        (previous / "freeze.json").write_text("{}")
        (previous / "result.json").write_text(
            json.dumps(
                {
                    "status": "failed",
                    "heldout_evaluations": 0,
                    "error": "ValueError: proposal lacks the required routine",
                    "freeze_sha256": pilot.digest(previous / "freeze.json"),
                }
            )
        )
    result = pilot.run_allocator_trial(
        ROOT,
        tmp_path / "trial",
        "fake",
        "http://localhost:11434",
        scaffold_from=previous,
    )
    assert calls.count("model") == 1
    assert result["heldout_evaluations"] == int(training_pass)
    assert result["source_promoted"] is False
    assert result["routine_recovered"] is False
    assert result["expansion_allowed"] is False
    assert ("original-heldout" in calls) == training_pass
    assert result["status"] == (
        "scoped-pass-awaiting-review" if training_pass and heldout_pass else "failed"
    )


def test_allocator_absent_input_skips(tmp_path, monkeypatch):
    """Oracle: no disc input, no request/output or fabricated pass."""
    monkeypatch.setattr(pathlib.Path, "is_file", lambda self: False)
    result = pilot.run_allocator_trial(
        tmp_path, tmp_path / "trial", "fake", "http://localhost:11434"
    )
    assert result["status"] == "skipped"
    assert not (tmp_path / "trial").exists()


def test_allocator_runtime_failure_preserves_partial_trace_and_blocks_holdout(
    tmp_path, monkeypatch
):
    """Oracle: injected runtime201; partial output is failure, not a scored pass."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    calls = []

    def request(*args, **kwargs):
        """Oracle: one deterministic proposal, no live model."""
        calls.append("model")
        return json.dumps({"response": json.dumps({"source": CONTROL})})

    def original(root, output, cases, binary, contract):
        """Oracle: fake original output; any heldout execution fails this test."""
        assert output.name == "original-training"
        calls.append(output.name)
        return [[0] * 8] * len(cases)

    def candidate(output, source, cases):
        """Oracle: preserve partial output before raising the actual runtime error type."""
        assert output.name == "candidate-training"
        calls.append(output.name)
        output.mkdir()
        (output / "candidate.inc").write_text(source)
        (output / "compile.log").write_text("compiled\n")
        (output / "execution.log").write_text("Runtime error 201\n")
        (output / "PASCAL.BIN").write_bytes(bytes(16))
        raise subprocess.CalledProcessError(201, [str(output / "probe")])

    monkeypatch.setattr(pilot, "request", request)
    monkeypatch.setattr(pilot, "leaf_model_identity", lambda *args: {"digest": "fake"})
    monkeypatch.setattr(pilot, "allocator_original", original)
    monkeypatch.setattr(pilot, "allocator_candidate", candidate)
    output = tmp_path / "trial"
    result = pilot.run_allocator_trial(ROOT, output, "fake", "http://localhost:11434")
    assert calls == ["model", "original-training", "candidate-training"]
    assert result["status"] == "failed"
    assert result["heldout_evaluations"] == 0
    assert result["source_promoted"] is False
    assert result["stop_reason"] == "first-error-no-retry"
    assert "exit status 201" in result["error"]
    assert "training" not in result
    assert not (output / "candidate-heldout").exists()
    assert not (output / "original-heldout").exists()
    assert (output / "candidate-training/PASCAL.BIN").stat().st_size == 16
    assert "candidate-training/PASCAL.BIN" in result["artifact_hashes"]


def test_model_http_error_retains_backend_reason(monkeypatch):
    """Oracle: explicit service rejection, never a success-shaped proposal."""

    def rejected(*args, **kwargs):
        """Oracle: deterministic HTTP failure without network."""
        raise urllib.error.HTTPError(
            "http://localhost:11434/api/generate",
            400,
            "Bad Request",
            None,
            io.BytesIO(b'{"error":"Pattern must start and end with anchors"}'),
        )

    monkeypatch.setattr(pilot.urllib.request, "urlopen", rejected)
    with pytest.raises(ValueError, match="local model HTTP 400.*Pattern"):
        pilot.request("test", "fake", "http://localhost:11434")


def test_allocator_freeze_change_stops_before_original_or_holdout(
    tmp_path, monkeypatch
):
    """Oracle: modified prompt cannot enter training, much less heldout."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    output = tmp_path / "trial"

    def request(*args, **kwargs):
        """Oracle: simulate external prompt mutation after proposal."""
        (output / "prompt.txt").write_text("changed")
        return json.dumps({"response": json.dumps({"source": CONTROL})})

    def forbidden(*args):
        """Oracle: no binary execution allowed after drift."""
        pytest.fail("original executed after freeze drift")

    monkeypatch.setattr(pilot, "request", request)
    monkeypatch.setattr(pilot, "allocator_original", forbidden)
    monkeypatch.setattr(pilot, "leaf_model_identity", lambda *args: {"digest": "fake"})
    result = pilot.run_allocator_trial(ROOT, output, "fake", "http://localhost:11434")
    assert result["status"] == "failed"
    assert result["heldout_evaluations"] == 0
    assert "freeze/method/model changed" in result["error"]


@pytest.mark.parametrize("reason", ["heldout", "candidate", "second-retry"])
def test_allocator_format_retry_cannot_reopen_evaluated_or_retried_run(
    tmp_path, reason
):
    """Oracle: no format retry after candidate/holdout exposure or a prior retry."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    previous = tmp_path / "previous"
    previous.mkdir()
    (previous / "freeze.json").write_text(
        json.dumps(
            {
                "proposal_mode": "declaration-constrained-known-slice"
                if reason == "second-retry"
                else "source-json",
            }
        )
    )
    (previous / "result.json").write_text(
        json.dumps(
            {
                "status": "failed",
                "heldout_evaluations": int(reason == "heldout"),
                "candidate_sha256": "candidate" if reason == "candidate" else None,
                "error": "ValueError: proposal lacks the required routine",
                "freeze_sha256": pilot.digest(previous / "freeze.json"),
            }
        )
    )
    with pytest.raises(ValueError, match="format retry"):
        pilot.run_allocator_trial(
            ROOT,
            tmp_path / "trial",
            "fake",
            "http://localhost:11434",
            scaffold_from=previous,
        )
    assert not (tmp_path / "trial").exists()
