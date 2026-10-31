import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_constructor_probe as probe


def original_trace(cases, segment=0x1234):
    """Oracle: independent synthetic framing for comparator rejection tests only."""
    trace = bytearray()
    for index, case in enumerate(cases):
        data = bytearray(probe.expected_case(case.data, segment))
        struct.pack_into("<H", data, 290, segment)
        name = case.data[1 : 1 + min(case.data[0], 79)].split(b"\0", 1)[0]
        trace.extend(
            struct.pack(
                "<10H",
                index,
                segment,
                segment,
                segment,
                0xFFFE,
                0xFFFE,
                segment,
                probe.OBJECT_OFFSET + 49 + len(name),
                probe.OBJECT_OFFSET,
                0x6800,
            )
        )
        trace.extend(data)
    return bytes(trace)


@pytest.fixture
def samples():
    """Oracle: short corpus exercises zero, boundary and embedded-NUL records."""
    cases = probe.constructor_cases()
    return [cases[0], cases[78], cases[79], cases[255], cases[-1]]


def test_constructor_corpus_has_all_lengths_and_dirty_initial_states():
    """Oracle: coverage is fixed before generation, not selected from passing cases."""
    cases = probe.constructor_cases()
    assert len(cases) == 778
    assert len({case.name for case in cases}) == len(cases)
    assert all(len(case.data) == 544 for case in cases)
    for start in (0, 256, 512):
        assert [case.data[0] for case in cases[start : start + 256]] == list(range(256))
    assert {case.name for case in cases} >= {"two_lines", "cr_at_refill_boundary"}


def test_constructor_normalizes_only_checked_code_segment(samples):
    """Oracle: actual buffer-pointer segment remains compared, not normalized away."""
    trace = original_trace(samples, 0x4321)
    candidate = b"".join(probe.expected_case(case.data, 0x4321) for case in samples)
    result = probe.compare_cases(samples, trace, candidate)
    assert result["status"] == "passed"
    assert len(result["cases"]) == len(samples)


@pytest.mark.parametrize(
    "offset", [0, 255, 256, 271, 272, 284, 286, 288, 290, 320, 400, 543]
)
def test_constructor_rejects_candidate_pointer_string_and_protected_memory_mutations(
    samples, offset
):
    """Oracle: no ignored bytes except the explicitly checked original relocation."""
    candidate = bytearray(
        b"".join(probe.expected_case(case.data, 0x1234) for case in samples)
    )
    candidate[offset] ^= 1
    result = probe.compare_cases(samples, original_trace(samples), bytes(candidate))
    assert result["status"] == "failed"
    assert result["cases"][0]["differences"][0]["offset"] == offset


def test_constructor_rejects_identical_but_out_of_contract_writes(samples):
    """Oracle: mutually agreeing implementations cannot overwrite a protected guard."""
    candidate = bytearray(
        b"".join(probe.expected_case(case.data, 0x1234) for case in samples)
    )
    trace = bytearray(original_trace(samples))
    candidate[543] ^= 1
    trace[20 + 543] ^= 1
    assert (
        probe.compare_cases(samples, bytes(trace), bytes(candidate))["status"]
        == "failed"
    )


@pytest.mark.parametrize("offset", [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 310])
def test_constructor_rejects_original_abi_identity_or_relocation_mutations(
    samples, offset
):
    """Oracle: stack, call identity and relocation checks precede any normalization."""
    trace = bytearray(original_trace(samples))
    trace[offset] ^= 1
    with pytest.raises(ValueError):
        probe.decode_original(bytes(trace), len(samples))


def test_constructor_rejects_truncated_or_extra_results(samples):
    """Oracle: partial emulator/candidate output is not a pass."""
    trace = original_trace(samples)
    candidate = b"".join(probe.expected_case(case.data, 0x1234) for case in samples)
    for damaged in (trace[:-1], trace + b"\0", b""):
        with pytest.raises(ValueError):
            probe.compare_cases(samples, damaged, candidate)
    for damaged in (candidate[:-1], candidate + b"\0", b""):
        with pytest.raises(ValueError):
            probe.compare_cases(samples, trace, damaged)


def test_constructor_missing_byod_skips(tmp_path):
    """Oracle: missing original inputs never create evidence."""
    assert probe.run_probe(tmp_path / "output", tmp_path)["status"] == "skipped"
    assert not (tmp_path / "output").exists()


def test_actual_original_constructor_matches_pascal(tmp_path):
    """Oracle: real original bytes versus compiled actual Pascal, not synthetic framing."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    if any(shutil.which(tool) is None for tool in ("fpc", "dosbox", "as", "ld")):
        pytest.skip("FPC/DOSBox/GNU assembler/linker unavailable")
    output = tmp_path / "constructor parity with spaces"
    result = probe.run_probe(output, root)
    assert result["status"] == "passed"
    assert result["case_count"] == 778
    assert all(case["status"] == "passed" for case in result["cases"])
    assert json.loads((output / "result.json").read_text()) == result
    assert probe.validate_saved_report(output, root) == result

    from engine.fact_graph import Fact
    from engine.scoped_verification import constructor_contract_graph

    graph = constructor_contract_graph(root / "targets/liero", output)
    inherited = graph.facts_for("input_open.capacity", "word_value")
    assert len(inherited) == 1
    assert inherited[0].value == 128
    assert inherited[0].status == "derived"
    assert inherited[0].supports == ("constructor.capacity.checked",)
    scope = graph.nodes["input_open.capacity"].attributes["scope"]
    assert "SP=FFFE" in scope["observed_contract_preconditions"][0]
    assert all("SP=FFFE" not in assumption for assumption in scope["assumptions"])
    assert "static field rule" in scope["transfer_basis"]
    assert not graph.conflicts()
    graph.add_fact(
        Fact(
            "wrong-capacity",
            "input_open.capacity",
            "word_value",
            256,
            "observed",
            ("test-only-contradiction",),
            "test",
        )
    )
    assert len(graph.conflicts()) == 1

    stored = output / "result.json"
    for field, value in (
        ("status", "failed"),
        ("case_count", 1),
        ("contract", {}),
        ("source_hashes", {}),
        ("artifact_hashes", {}),
    ):
        changed = {**result, field: value}
        stored.write_text(json.dumps(changed))
        with pytest.raises(ValueError):
            probe.validate_saved_report(output, root)
    stored.write_text(json.dumps(result))

    candidate_source = output / "candidate/FUN_24dd_3639.inc"
    source = candidate_source.read_text()
    candidate_source.write_text(
        source.replace("maximumNameLength := 79", "maximumNameLength := 78")
    )
    executable = probe._compile_candidate(output / "candidate")
    damaged = output / "MUTANT.BIN"
    subprocess.run(
        [
            str(executable),
            str(output / "CASES.BIN"),
            str(damaged),
            str(result["segment"]),
        ],
        check=True,
        capture_output=True,
        timeout=30,
    )
    mutant = probe.compare_cases(
        probe.constructor_cases(),
        (output / "TRACE.BIN").read_bytes(),
        damaged.read_bytes(),
    )
    assert mutant["status"] == "failed"
    assert any(
        row["case"] == "ones-length-79" and row["status"] == "failed"
        for row in mutant["cases"]
    )
    with pytest.raises(ValueError, match="stale constructor artifact"):
        probe.validate_saved_report(output, root)
