from __future__ import annotations

import hashlib
import shutil
import struct
from pathlib import Path

import pytest

from tools.liero_compare_routine_probe import (
    CANDIDATE_RECORD_SIZE,
    HELD_OUT_CASE_COUNT,
    HELD_OUT_SUITE,
    ORIGINAL_RECORD_SIZE,
    TRAINING_SUITE,
    CompareCase,
    _validate_artifact_hashes,
    compare_cases,
    encode_cases,
    expected_flag_mask,
    fixture_cases,
    fixture_suite,
    fixture_suite_sha256,
    held_out_fixture_cases,
)

ROOT = Path(__file__).resolve().parents[1]


def _snapshots(cases: list[CompareCase], *, candidate: bool) -> bytes:
    records = bytearray()
    for case in cases:
        flags = expected_flag_mask(case)
        if candidate:
            records.extend(struct.pack("<H", flags))
        else:
            records.extend(
                struct.pack(
                    "<10H",
                    len(records) // ORIGINAL_RECORD_SIZE + 1,
                    0x1234,
                    0x1234,
                    0x1234,
                    0x1234,
                    0xFFFE,
                    0xFFFE,
                    flags,
                    case.dest_offset,
                    case.source_offset,
                )
            )
        records.extend(case.dest)
        records.extend(case.source)
    return bytes(records)


def test_fixture_coverage_includes_boundaries_and_orderings() -> None:
    cases = fixture_cases()

    assert len(cases) >= 8
    assert any(not case.dest[0] and not case.source[0] for case in cases)
    assert any(case.dest[0] == 255 and case.source[0] == 255 for case in cases)
    assert any(expected_flag_mask(case) & 1 for case in cases)
    assert any(not expected_flag_mask(case) & 1 for case in cases)
    assert encode_cases(cases)[:4] == struct.pack(
        "<HH", cases[0].dest_offset, cases[0].source_offset
    )


def test_held_out_suite_is_deterministic_and_distinct_from_training() -> None:
    first = held_out_fixture_cases()
    second = held_out_fixture_cases()

    assert len(first) == HELD_OUT_CASE_COUNT == 64
    assert first == second
    assert len({case.name for case in first}) == HELD_OUT_CASE_COUNT
    assert {case.dest[0] for case in first} >= {0, 1, 2, 127, 128, 254, 255}
    assert {case.source[0] for case in first} >= {0, 1, 2, 127, 128, 254, 255}
    assert any(b"\x00" in case.dest[1:] for case in first)
    assert any(b"\x00" in case.source[1:] for case in first)
    assert fixture_suite(TRAINING_SUITE) == fixture_cases()
    assert fixture_suite(HELD_OUT_SUITE) == first
    assert fixture_suite_sha256(HELD_OUT_SUITE) == fixture_suite_sha256(HELD_OUT_SUITE)
    assert {case.name for case in first}.isdisjoint(
        case.name for case in fixture_cases()
    )
    assert all(
        len(case.dest) == len(case.source) == 256
        and expected_flag_mask(case) in (0, 0x0001, 0x0040)
        for case in first
    )


def test_held_out_suite_covers_empty_vs_nonempty_length_orderings() -> None:
    cases = held_out_fixture_cases()

    assert any(
        case.dest[0] == 0 and case.source[0] > 0 and expected_flag_mask(case) == 0
        for case in cases
    )
    assert any(
        case.source[0] == 0 and case.dest[0] > 0 and expected_flag_mask(case) == 0x0001
        for case in cases
    )


def test_fixture_suite_rejects_unknown_identity() -> None:
    with pytest.raises(ValueError, match="unknown comparator fixture suite"):
        fixture_suite("unregistered-suite")


def test_pair_comparison_accepts_expected_flags_and_unchanged_memory() -> None:
    cases = fixture_cases()

    result = compare_cases(
        cases,
        _snapshots(cases, candidate=False),
        _snapshots(cases, candidate=True),
    )

    assert result["status"] == "passed"
    assert result["case_count"] == len(cases)
    assert all(case["status"] == "passed" for case in result["cases"])


def test_pair_comparison_rejects_candidate_flag_mutation() -> None:
    cases = fixture_cases()
    original = _snapshots(cases, candidate=False)
    candidate = bytearray(_snapshots(cases, candidate=True))
    candidate[0] ^= 0x40

    result = compare_cases(cases, original, bytes(candidate))

    assert result["status"] == "failed"
    assert result["cases"][0]["candidate_flags"] != result["cases"][0]["expected_flags"]


def test_pair_comparison_rejects_candidate_memory_mutation() -> None:
    cases = fixture_cases()
    original = _snapshots(cases, candidate=False)
    candidate = bytearray(_snapshots(cases, candidate=True))
    candidate[CANDIDATE_RECORD_SIZE + 2] ^= 1

    result = compare_cases(cases, original, bytes(candidate))

    assert result["status"] == "failed"
    assert result["cases"][1]["candidate_memory_changed"]


def test_trace_decoder_rejects_truncation_and_unbalanced_stack() -> None:
    cases = fixture_cases()
    original = bytearray(_snapshots(cases, candidate=False))

    with pytest.raises(ValueError, match="trace size"):
        compare_cases(cases, bytes(original[:-1]), _snapshots(cases, candidate=True))

    original[12:14] = struct.pack("<H", 0xFFFC)
    result = compare_cases(cases, bytes(original), _snapshots(cases, candidate=True))
    assert result["status"] == "failed"
    assert result["cases"][0]["stack_balanced"] is False


def test_saved_evidence_rejects_stale_and_partial_artifacts(tmp_path: Path) -> None:
    artifact = tmp_path / "TRACE.BIN"
    artifact.write_bytes(b"complete trace")
    hashes = {"TRACE.BIN": hashlib.sha256(artifact.read_bytes()).hexdigest()}
    _validate_artifact_hashes(tmp_path, hashes)

    artifact.write_bytes(b"changed trace")
    with pytest.raises(ValueError, match="stale comparator artifact"):
        _validate_artifact_hashes(tmp_path, hashes)

    artifact.unlink()
    with pytest.raises(ValueError, match="missing or unexpected"):
        _validate_artifact_hashes(tmp_path, hashes)


@pytest.mark.skipif(shutil.which("fpc") is None, reason="Free Pascal is unavailable")
def test_compiled_pascal_mutation_is_detected(tmp_path: Path) -> None:
    from tools.liero_compare_routine_probe import (
        candidate_source_paths,
        compile_candidate,
        run_candidate,
    )

    cases = fixture_cases()
    candidate_dir = (
        tmp_path / f"deep-run-{'x' * 90}" / f"candidate-dir-{'y' * 90}" / "candidate"
    )
    candidate_dir.mkdir(parents=True)
    for source in candidate_source_paths(ROOT):
        shutil.copy2(source, candidate_dir / source.name)

    include = candidate_dir / "FUN_24dd_3f86.inc"
    source = include.read_text(encoding="utf-8")
    mutated = source.replace(
        "RegisterCarryFlag := sourceLength < destinationLength;",
        "RegisterCarryFlag := False;",
    )
    assert mutated != source
    include.write_text(mutated, encoding="utf-8")

    executable = compile_candidate(candidate_dir)
    case_path = candidate_dir.parent / "CASES.BIN"
    candidate_path = candidate_dir.parent / "PASCAL.BIN"
    case_path.write_bytes(encode_cases(cases))
    run_candidate(executable, case_path, candidate_path, 0x1234)

    result = compare_cases(
        cases,
        _snapshots(cases, candidate=False),
        candidate_path.read_bytes(),
    )
    assert result["status"] == "failed"
