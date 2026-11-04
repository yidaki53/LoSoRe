import json
import pathlib
import shutil
import subprocess

import pytest

from tools import liero_allocator_list_probe as probe

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_list_contract_authenticates_branches_and_bounds():
    """Oracle: actual binary-backed branch destinations, not exported listing addresses."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    _, _, facts = probe.list_contract(ROOT)
    assert facts["branches"] == {
        "sentinel": 0x3D2,
        "next_paragraph": 0x364,
        "fit_paragraph": 0x381,
        "next_offset": 0x364,
        "exact": 0x3C1,
    }
    assert facts["node_fields"] == {
        "next_offset": 0,
        "next_segment": 2,
        "size_offset": 4,
        "size_paragraphs": 6,
    }
    assert facts["heap_window"] == [0x8000, 0x8200]
    assert facts["source_recovered"] is False


def test_list_corpora_are_bounded_disjoint_and_cover_selection():
    """Oracle: predeclared one/two-node inputs, not arbitrary cyclic free lists."""
    training, heldout = probe.list_cases("training"), probe.list_cases("heldout")
    assert len(training) == len(set(training)) == 72
    assert len(heldout) == len(set(heldout)) == 48
    assert not set(training) & set(heldout)
    for case in training + heldout:
        probe.validate_case(case)
    with pytest.raises(ValueError):
        probe.list_cases("unknown")
    assert {case[2] == 0 for case in training} == {True, False}


@pytest.mark.parametrize(
    "case",
    [
        (1, 0, 0, 0),
        (1, 129, 0, 0),
        (1, 8, 1, 0),
        (65535, 8, 0, 0),
        (1, 8, 0, 1),
        (1, 8, 0, 16),
    ],
)
def test_list_memory_gate_rejects_unsupported_inputs(case):
    """Oracle: node/split writes require explicit aligned nonwrapping fixture bounds."""
    with pytest.raises(ValueError):
        probe.validate_case(case)


def test_list_harness_retains_original_allocator_and_guard_capture(tmp_path):
    """Oracle: strict adaptation of existing COM setup with disclosed two-node initialization."""
    text = probe.list_harness(tmp_path / "CASES.BIN", 16)
    assert "call 0x353" in text
    assert "mov $512, %cx" in text
    assert "mov $0x8200" not in text
    assert "add $0x900" in text
    assert "add $8, %si" in text
    assert "mov $9344, %cx" in text
    with pytest.raises(ValueError):
        probe.list_harness(tmp_path / "CASES.BIN", 72)


def test_list_missing_byod_skips_without_artifacts(tmp_path):
    """Oracle: missing original input cannot become a pass or compiler-only result."""
    assert probe.run(tmp_path, tmp_path / "run")["status"] == "skipped"
    assert not (tmp_path / "run").exists()


def test_list_candidate_contains_checked_structural_obligations():
    """Oracle: deterministic model-memory renderer, not an unverified malloc replacement."""
    source = probe.candidate_source()
    assert "savedRequest := requestSize" in source
    assert "remaining := available - rounded" in source
    assert "Link(nextOffset, nextSegment)" in source
    assert "predecessor" in source
    assert "LongWord(requestSize) + 7" in source
    assert "HeapIndex" in source


def test_list_trace_partial_output_is_explicit_failure():
    """Oracle: exact complete record shape required before any score."""
    with pytest.raises(ValueError, match="shape"):
        probe.original_projection(b"partial", [(1, 8, 0, 0)])


@pytest.mark.parametrize(
    "failure",
    ["none", "training", "heldout", "runtime", "drift", "terminal-drift", "partial"],
)
def test_list_fixed_candidate_budget_and_terminal_gate(tmp_path, monkeypatch, failure):
    """Oracle: injected comparisons prove no retries or terminal feedback on failures."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    calls = []

    def original(root, output, cases):
        """Oracle: injected original bytes, no DOS execution."""
        calls.append(output.name)
        return bytes(len(cases) * probe.PROJECTION_BYTES)

    def projection(data, cases):
        """Oracle: synthetic projection, not a claim of guard validation."""
        return data, [0x2000] * len(cases)

    def candidate(output, cases, segments):
        """Oracle: injected runtime/mismatch/drift, no compiler execution."""
        calls.append(output.name)
        if failure == "runtime":
            raise subprocess.CalledProcessError(201, ["synthetic-candidate"])
        if failure == "drift" or (
            failure == "terminal-drift" and output.name == "candidate-heldout"
        ):
            (output.parent / "freeze.json").write_text("{}")
        if failure == "partial":
            return b"partial"
        value = int(output.name == f"candidate-{failure}")
        return bytes([value]) * (len(cases) * probe.PROJECTION_BYTES)

    monkeypatch.setattr(probe, "original", original)
    monkeypatch.setattr(probe, "original_projection", projection)
    monkeypatch.setattr(probe, "candidate", candidate)
    output = tmp_path / "frozen"
    result = probe.run(ROOT, output)
    assert result["status"] == ("passed" if failure == "none" else "failed")
    assert result["model_requests"] == 0
    assert result["heldout_evaluations"] == int(
        failure in {"none", "heldout", "terminal-drift"}
    )
    assert ("original-heldout" in calls) == (
        failure in {"none", "heldout", "terminal-drift"}
    )
    assert calls.count("candidate-training") == 1
    assert result["source_promoted"] is False
    assert result["routine_recovered"] is False
    assert result["automatic_discovery"] is False
    assert (output / "result.json").is_file()


def test_list_comparison_checks_all_heap_words():
    """Oracle: any of256 heap words, including guard residue, changes the full case result."""
    baseline = bytes(probe.PROJECTION_BYTES)
    for byte in range(16, probe.PROJECTION_BYTES):
        mutant = bytearray(baseline)
        mutant[byte] = 1
        assert probe.compare(baseline, bytes(mutant), 1)["passed"] == 0
    with pytest.raises(ValueError):
        probe.compare(baseline, baseline[:-1], 1)


def test_list_replay_unbound_pass_rejected(tmp_path):
    """Oracle: success metadata alone cannot validate list recovery."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    (tmp_path / "result.json").write_text(json.dumps({"status": "passed"}))
    (tmp_path / "freeze.json").write_text("{}")
    with pytest.raises(ValueError):
        probe.validate_report(ROOT, tmp_path)


@pytest.mark.parametrize(
    "mutation",
    ["none", "metadata", "COM", "Pascal", "heap", "method", "missing", "escape"],
)
def test_list_saved_replay_tampering_and_graph(tmp_path, monkeypatch, mutation):
    """Oracle: saved evidence replay only, never another heldout evaluation."""
    saved = ROOT / "targets/liero/build/allocator-list/owned-two-node-v1"
    if not (saved / "result.json").is_file():
        pytest.skip("frozen original-list evidence unavailable")
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    copied = tmp_path / "copy"
    shutil.copytree(saved, copied)
    harness = probe.list_harness

    def saved_harness(path, count):
        """Oracle: copied assembly retains disclosed original absolute incbin path."""
        return harness(saved / path.relative_to(copied), count)

    monkeypatch.setattr(probe, "list_harness", saved_harness)
    report = json.loads((copied / "result.json").read_text())
    paths = {
        "COM": "original-heldout/part-0/PROBE.COM",
        "Pascal": "candidate-heldout/probe.pas",
        "heap": "candidate-heldout/PASCAL.BIN",
        "method": "methods/liero_allocator_list_probe.py",
    }
    if mutation in paths:
        name = paths[mutation]
        path = copied / name
        data = bytearray(path.read_bytes())
        data[-1] ^= 1
        path.write_bytes(data)
        report["artifact_hashes"][name] = probe.pilot.digest(path)
    elif mutation == "metadata":
        report["heldout_evaluations"] = 2
    elif mutation == "missing":
        report["artifact_hashes"].pop("original-heldout/part-0/PROBE.COM")
    elif mutation == "escape":
        report["artifact_hashes"]["../outside"] = "0" * 64
    probe.pilot.save(copied / "result.json", report)
    if mutation != "none":
        with pytest.raises(ValueError):
            probe.validate_report(ROOT, copied)
        return
    from engine.scoped_verification import allocator_list_contract_graph

    assert probe.validate_report(ROOT, copied)["heldout"]["passed"] == 48
    graph = allocator_list_contract_graph(ROOT / "targets/liero", copied)
    assert graph.facts["allocator.owned-list.checked"].status == "oracle-verified"
    for name in ("arbitrary_topology", "nondefault_callback", "actual_caller"):
        assert graph.facts[f"allocator.owned-list.{name}"].status == "unknown"
    assert not graph.conflicts()
    assert not graph.propagate_same_value()
