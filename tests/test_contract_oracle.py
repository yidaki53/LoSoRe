"""Tests for decomp/contract-derived original-trace fixtures."""

from __future__ import annotations

import pathlib
import struct

from engine import contract_oracle as oracle
from engine import oracle_gate, target_packet

REPO = pathlib.Path(__file__).resolve().parent.parent


def test_fixture_derives_safe_contract_leaf():
    fixture = oracle.fixture(REPO, "liero", "FUN_24dd_04dc")
    assert fixture["declaration"] == "function FUN_24dd_04dc: Longint;"
    assert fixture["kind"] == "function"
    assert fixture["params"] == []
    assert fixture["near"] is True
    assert fixture["cleanup"] == 0
    evidence = target_packet.evidence_for_routine(REPO, "liero", "FUN_24dd_04dc")
    assert fixture["bytes"] == evidence["bytes"]["hex"]
    assert oracle.supported(REPO, "liero", "FUN_24dd_04dc") is True


def test_unsafe_contract_routine_is_not_supported():
    assert oracle.supported(REPO, "liero", "FUN_24dd_010f") is False


def test_cases_are_frozen_and_bounded():
    fixture = oracle.fixture(REPO, "liero", "FUN_24dd_04dc")
    first = oracle.cases(fixture, "training")
    second = oracle.cases(fixture, "training")
    assert first == second
    assert len(first) == 56
    assert all(len(item) == oracle.CASE_BYTES for item in first)
    assert oracle.cases(fixture, "terminal") != first


def test_compare_normalizes_segments_and_unsupported_flags():
    row = bytearray(oracle.RECORD_BYTES)
    struct.pack_into("<H", row, 0, 0x1234)
    struct.pack_into("<H", row, 24, 0x8001)
    struct.pack_into("<H", row, 30, 0x24DD)
    candidate = bytearray(row)
    struct.pack_into("<H", candidate, 24, 0x0001)
    struct.pack_into("<H", candidate, 30, 0x2000)
    result = oracle.compare(bytes(row), bytes(candidate))
    assert result == {"status": "passed", "cases": 1, "matches": 1, "failures": []}

    struct.pack_into("<H", candidate, 0, 0x1235)
    result = oracle.compare(bytes(row), bytes(candidate))
    assert result["status"] == "failed"
    assert result["failures"][0]["first_different_bytes"] == [0]


def test_evaluate_routine_uses_contract_oracle_for_supported_routines(
    tmp_path, monkeypatch
):
    source = tmp_path / "candidate.inc"
    source.write_text("procedure candidate; begin end;")
    passes = {
        "compile": {"status": "passed"},
        "suites": {
            "training": {
                "original": {"status": "passed"},
                "candidate": {"status": "passed"},
            }
        },
    }
    terminal = {
        "compile": {"status": "passed"},
        "suites": {
            "terminal": {
                "original": {"status": "passed"},
                "candidate": {"status": "passed"},
            }
        },
    }
    monkeypatch.setattr(oracle, "supported", lambda *_: True)
    monkeypatch.setattr(oracle, "run_training", lambda *_: passes)
    monkeypatch.setattr(oracle, "run", lambda *_a, **_k: terminal)
    result = oracle_gate.evaluate_routine(
        tmp_path, "liero", "FUN_24dd_04dc", source, tmp_path / "eval"
    )
    assert result["status"] == "verified"
    assert result["promotion_eligible"] is True
    assert result["training"] == passes
    assert result["terminal"] == terminal
