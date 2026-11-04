import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_error_address_probe as probe

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture
def contract():
    """Oracle: actual original bytes, DS relocation and current BYOD availability."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    return probe.checked_contract(ROOT)[1]


def test_original_error_translation_contract_and_corpora(contract):
    """Oracle: original prefix only; actual failure/cleanup is not accepted."""
    assert len(probe.RAW) == 84
    assert contract["entry"] == 0x11A
    assert contract["stop"] == 0x16E
    assert contract["relocation_offsets"] == [1]
    assert contract["fields"] == {
        "size_exclusive": 8,
        "base_paragraph": 16,
        "next_segment": 20,
    }
    assert contract["source_recovered"] is False
    training, heldout = probe.cases("training"), probe.cases("heldout")
    assert len(training) == len(set(training)) == 61
    assert len(heldout) == len(set(heldout)) == 37
    assert not set(training) & set(heldout)
    for case in training + heldout:
        probe.validate_case(case)
    with pytest.raises(ValueError):
        probe.cases("unknown")


@pytest.mark.parametrize(
    "case",
    [
        (0, 0, 3, 0, 0, 0, 0),
        (0, 0, 1, -1, 0, 0, 0),
        (0, 0, 0),
        (0, True, 0, 0, 0, 0, 0),
    ],
)
def test_unowned_topology_and_invalid_words_rejected(case):
    """Oracle: explicit bounded-input error, not pointer fallback."""
    with pytest.raises(ValueError):
        probe.validate_case(case)


def test_harness_assembles_and_preserves_original_prefix(tmp_path, contract):
    """Oracle: actual GNU assembly and read-only original bytes; no DOS execution."""
    inputs = probe.cases("training")[:16]
    path = tmp_path / "CASES.BIN"
    path.write_bytes(b"".join(struct.pack("<7H", *case) for case in inputs))
    text = probe.harness(path, len(inputs))
    (tmp_path / "harness.S").write_text(text)
    raw = probe.assemble_probe(tmp_path / "harness.S", tmp_path)
    image = probe.build_image(raw)
    assert image[0x1A : 0x1A + 84] == probe.RAW
    assert "mov %ax, 0x11b" in text
    assert "jmp 0x11a" in text
    assert "rep movsb" in text
    assert len(image) + 0x100 < 0x6000
    with pytest.raises(ValueError):
        probe.harness(path, 17)
    with pytest.raises(ValueError):
        probe.build_image(bytes(0x6000))
    mutant = bytearray(raw)
    mutant[0x1A] = 1
    with pytest.raises(ValueError):
        probe.build_image(bytes(mutant))


def test_original_projection_checks_all_owned_memory_and_register_premises():
    """Oracle: synthetic record mechanism, not binary-backed parity."""
    case = (1, 0x4000, 2, 0x4000, 20, 0x4000, 32)
    segment, cx, bx = 0x2000, 1, 0x800
    globals_ = bytearray([0xA5] * 58)
    for cell, value in (
        (0x63E4, 0x2800),
        (0x640C, 0x1FF0),
        (0x6406, 203),
        (0x6408, cx),
        (0x640A, bx),
    ):
        struct.pack_into("<H", globals_, cell - probe.WINDOW[0], value)
    record = struct.pack("<8H", segment, cx, bx, segment, 0x2800, 0xEFF0, 0x200, 1)
    trace = record + globals_ + probe.descriptor_memory(case, segment)
    assert probe.projection(trace, [case]) == (struct.pack("<2H", cx, bx), [segment])
    for index in (0, 6, 8, 10, 13, *range(16, 16 + 58 + 512)):
        mutant = bytearray(trace)
        mutant[index] ^= 2 if index == 13 else 1
        with pytest.raises(ValueError):
            probe.projection(bytes(mutant), [case])
    with pytest.raises(ValueError):
        probe.projection(trace[:-1], [case])


def test_missing_byod_skips_without_creating_output(tmp_path):
    """Oracle: absent original never becomes compilation-only pass."""
    assert probe.run(tmp_path, tmp_path / "run")["status"] == "skipped"
    assert not (tmp_path / "run").exists()


@pytest.mark.parametrize(
    "failure",
    ["none", "training", "heldout", "partial", "runtime", "drift", "terminal-drift"],
)
def test_frozen_candidate_training_terminal_budget(
    contract, tmp_path, monkeypatch, failure
):
    """Oracle: injected trace/candidate results test no repair, no retries and complete-suite gates."""
    calls = []

    def original(root, output, cases):
        """Oracle: synthetic original capture, not DOS execution."""
        calls.append("original")
        return bytes(4 * len(cases))

    def projection(trace, cases):
        """Oracle: synthetic complete result shape."""
        return trace, [0x2000] * len(cases)

    def candidate(output, cases, segments):
        """Oracle: injected mismatch/runtime/drift, not a model recovery."""
        calls.append(output.name)
        if failure == "runtime":
            raise subprocess.CalledProcessError(201, ["synthetic"])
        if failure == "drift" or (
            failure == "terminal-drift" and output.name.endswith("heldout")
        ):
            (output.parent / "freeze.json").write_text("{}")
        if failure == "partial":
            return b"partial"
        return bytes([int(output.name == f"candidate-{failure}")]) * (len(cases) * 4)

    monkeypatch.setattr(probe, "original_batch", original)
    monkeypatch.setattr(probe, "projection", projection)
    monkeypatch.setattr(probe, "candidate", candidate)
    result = probe.run(ROOT, tmp_path / "run")
    assert result["status"] == ("passed" if failure == "none" else "failed")
    assert result["model_requests"] == 0
    assert result["heldout_evaluations"] == int(
        failure in {"none", "heldout", "terminal-drift"}
    )
    assert calls.count("candidate-training") == 1
    assert calls.count("candidate-heldout") == int(
        failure in {"none", "heldout", "terminal-drift"}
    )
    assert result["source_promoted"] is False
    assert result["routine_recovered"] is False


@pytest.mark.parametrize(
    "mutation",
    [
        "none",
        "heap",
        "output",
        "source",
        "image",
        "method",
        "missing",
        "promotion",
        "escape",
    ],
)
def test_saved_error_translation_replay_and_rehashed_tampering(
    tmp_path, monkeypatch, mutation
):
    """Oracle: frozen original evidence replay only; never rerun terminal suite."""
    saved = ROOT / "targets/liero/build/error-address/owned-descriptors-v1"
    if (
        not (saved / "result.json").is_file()
        or not (ROOT / "extracted/liero/LIERO.EXE").is_file()
    ):
        pytest.skip("saved error translation evidence/BYOD unavailable")
    copied = tmp_path / "copy"
    shutil.copytree(saved, copied)
    original_harness = probe.harness

    def copied_harness(path, count):
        """Oracle: absolute incbin path remains bound to original saved assembly."""
        return original_harness(saved / path.relative_to(copied), count)

    monkeypatch.setattr(probe, "harness", copied_harness)
    report = json.loads((copied / "result.json").read_text())
    paths = {
        "heap": "original-heldout/part-0/TRACE.BIN",
        "output": "candidate-heldout/PASCAL.BIN",
        "source": "candidate-heldout/probe.pas",
        "image": "original-heldout/part-0/PROBE.COM",
        "method": "methods/liero_error_address_probe.py",
    }
    if mutation in paths:
        name = paths[mutation]
        path = copied / name
        data = bytearray(path.read_bytes())
        data[-1] ^= 1
        path.write_bytes(data)
        report["artifact_hashes"][name] = probe.pilot.digest(path)
    elif mutation == "missing":
        report["artifact_hashes"].pop("original-heldout/part-0/TRACE.BIN")
    elif mutation == "promotion":
        report["routine_recovered"] = True
    elif mutation == "escape":
        report["artifact_hashes"]["../outside"] = "0" * 64
    probe.pilot.save(copied / "result.json", report)
    if mutation != "none":
        with pytest.raises(ValueError):
            probe.validate_report(ROOT, copied)
    else:
        from engine.scoped_verification import error_address_contract_graph

        assert probe.validate_report(ROOT, copied)["heldout"]["passed"] == 37
        graph = error_address_contract_graph(ROOT / "targets/liero", copied)
        checked = graph.facts["allocator.error-address.checked"]
        assert checked.status == "oracle-verified"
        assert checked.value["descriptor_bytes_checked_per_case"] == 512
        assert checked.value["actual_failure_path_observed"] is False
        for name in (
            "actual_descriptor_provenance",
            "arbitrary_topology",
            "cleanup_callbacks_and_services",
        ):
            assert graph.facts[f"allocator.error-address.{name}"].status == "unknown"
        assert not graph.propagate_same_value()
        assert not graph.conflicts()


def test_error_translation_audit_and_combined_graph_do_not_unlock_cleanup(contract):
    """Oracle: existing graph adds only a conditional error dependency; real failure path stays unknown."""
    from engine.scoped_verification import allocator_contract_graph, load_scoped_checks

    evidence = ROOT / "targets/liero/build/error-address/owned-descriptors-v1"
    empty = ROOT / "targets/liero/build/allocator-deduction/deductive-v1"
    if not all((path / "result.json").is_file() for path in (evidence, empty)):
        pytest.skip("combined saved evidence unavailable")
    graph = allocator_contract_graph(ROOT / "targets/liero", empty)
    assert graph.facts["allocator.error-address.checked"].status == "oracle-verified"
    assert (
        graph.facts["allocator.observed-entry.error_transfer010f"].status == "unknown"
    )
    assert (
        graph.facts["allocator.error-address.cleanup_callbacks_and_services"].status
        == "unknown"
    )
    assert graph.facts["allocator.caller.applicability"].status == "unknown"
    assert not graph.conflicts()
    checks = [
        check
        for check in load_scoped_checks(ROOT / "targets/liero")
        if check["scope"] == "owned_descriptor_error_address_translation_before_cleanup"
    ]
    assert len(checks) == 1
    assert checks[0]["case_count"] == 98
    assert checks[0]["source_recovered"] is False


@pytest.mark.parametrize("available", [True, False])
def test_error_translation_audit_rejects_stale_or_missing_input(
    tmp_path, monkeypatch, available
):
    """Oracle: stale artifacts and absent BYOD never become a scoped pass."""
    from engine.scoped_verification import _load_error_address_checks

    target = tmp_path / "targets/liero"
    saved = target / "build/error-address/saved"
    saved.mkdir(parents=True)
    (saved / "result.json").write_text("{}")
    if available:
        original = tmp_path / "extracted/liero/LIERO.EXE"
        original.parent.mkdir(parents=True)
        original.touch()

    def rejected(*args):
        """Oracle: injected integrity failure, not original-byte acceptance."""
        raise ValueError("changed method")

    monkeypatch.setattr(probe, "validate_report", rejected)
    assert _load_error_address_checks(target)[0]["status"] == (
        "invalid" if available else "skipped"
    )
