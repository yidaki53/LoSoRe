import json

import pytest

from engine import generic_synthesizer, oracle_gate, verify


def _evidence(name, instructions, hex_bytes="c3"):
    return {
        "schema_version": 3,
        "target": "synthetic",
        "routine": name,
        "bytes": {"hex": hex_bytes},
        "static_evidence": {
            "assembly": {"instructions": list(instructions), "operations": [],
                         "unsafe": []},
            "gate": {"passed": True, "reasons": []},
            "raw_byte_facts": {"residue": {"bytes_hex": "c3"}},
        },
        "source_policy": {"binary_derived_evidence_only": True},
    }


COPY = [
    "MOV BX,SP",
    "MOV DX,DS",
    "LDS SI,SS:[BX + 0xa]",
    "LES DI,SS:[BX + 0x6]",
    "MOV CX,word ptr SS:[BX + 0x4]",
    "CLD",
    "MOVSB.REP ES:DI,SI",
    "MOV DX,DS",
    "RETF 0xa",
]

PACKED = [
    "CLD",
    "MOV BX,SP",
    "MOV DX,DS",
    "LDS SI,SS:[BX + 0xa]",
    "LES DI,SS:[BX + 0x6]",
    "MOV BX,word ptr SS:[BX + 0x4]",
    "MOV CL,BH",
    "XOR CH,CH",
    "ADD SI,CX",
    "MOV CL,BL",
    "MOVSB.REP ES:DI,SI",
    "MOV DX,DS",
    "RETF 0xa",
]

ARITHMETIC = [
    "PUSH BP",
    "MOV BP,SP",
    "MOV DI,word ptr [BP + 0x4]",
    "MOV AL,byte ptr SS:[DI + 0xfefc]",
    "XOR AH,AH",
    "MOV DX,AX",
    "MOV AL,byte ptr SS:[DI + 0xfefb]",
    "XOR AH,AH",
    "SHL AX,0x4",
    "ADD AX,DX",
    "MOV byte ptr SS:[DI + 0xfefd],AL",
    "LEAVE",
    "RET 0x2",
]

SHIFT_MASK = [
    "ADD AX,0x7",
    "MOV DX,AX",
    "RCR DX,0x1",
    "SHR DX,0x1",
    "SHR DX,0x1",
    "SHR DX,0x1",
    "AND AX,0x8",
    "RET",
]


def test_generic_synthesizer_builds_ir_from_instruction_shape():
    result = generic_synthesizer.synthesize(_evidence("FN_A", COPY))
    assert result["status"] == "synthesized"
    assert result["ir"]["shape"] == "copy-bytes-forward"
    assert result["ir"]["operands"]["cleanup_bytes"] == 10
    assert "procedure FN_A" in result["source"]
    assert "UNMATCHED" not in result["source"]


def test_generic_synthesizer_does_not_branch_on_routine_identity():
    first = generic_synthesizer.synthesize(_evidence("FN_A", COPY))["source"]
    second = generic_synthesizer.synthesize(_evidence("FN_B", COPY))["source"]
    assert first.replace("FN_A", "FN") == second.replace("FN_B", "FN")


def test_generic_synthesizer_recognizes_supported_shapes_without_identifiers():
    expected = {
        "copy-bytes-forward": COPY,
        "copy-bytes-packed": PACKED,
        "byte-shift-add": ARITHMETIC,
    }
    for shape, instructions in expected.items():
        result = generic_synthesizer.synthesize(_evidence("ANY", instructions))
        assert result["status"] == "synthesized"
        assert result["ir"]["shape"] == shape


def test_generic_synthesizer_recognizes_register_shift_mask_without_identifier():
    evidence = _evidence("ANY", SHIFT_MASK)
    evidence["oracle_contract"] = {"declaration": "function ANY: Longint;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert result["ir"]["shape"] == "register-shift-mask"
    assert result["ir"]["operands"]["add"] == 7
    assert result["ir"]["operands"]["mask"] == 8
    assert result["ir"]["operands"]["shift"] == 4
    assert "adjustedAX := (LongInt(RegisterAX) + 7) and $ffff;" in result["source"]
    assert "highWord := adjustedAX shr 4;" in result["source"]
    assert "RegisterAX := adjustedAX and $8;" in result["source"]
    assert "RegisterZeroFlag := False;" in result["source"]


def test_generic_synthesizer_rejects_unknown_shape():
    result = generic_synthesizer.synthesize(_evidence("ANY", ["MOV AX,1", "RET"]))
    assert result["status"] == "unsupported"
    assert result["source"] == ""


def test_oracle_gate_runs_terminal_once_and_promotes_only_on_full_parity():
    calls = []

    class Evaluator:
        @staticmethod
        def run_training(*args, **kwargs):
            calls.append("training")
            return {"compile": {"status": "passed"},
                    "suites": {"training": {"original": {"status": "passed"},
                                            "candidate": {"status": "passed"}}}}

        @staticmethod
        def run(*args, **kwargs):
            calls.append("terminal")
            return {"compile": {"status": "passed"},
                    "suites": {"terminal": {"original": {"status": "passed"},
                                            "candidate": {"status": "passed"}}}}

    decision = oracle_gate.evaluate_routine(
        "/repo", "target", "FN", "/repo/candidate.inc", "/repo/trial", Evaluator
    )
    assert calls == ["training", "terminal"]
    assert decision["status"] == "verified"
    assert decision["promotion_eligible"] is True
    assert oracle_gate.decide("dat-parity", decision)["status"] == "scoped"


def test_oracle_gate_does_not_run_terminal_after_training_failure():
    calls = []

    class Evaluator:
        @staticmethod
        def run_training(*args, **kwargs):
            calls.append("training")
            return {"compile": {"status": "passed"},
                    "suites": {"training": {"original": {"status": "passed"},
                                            "candidate": {"status": "failed"}}}}

        @staticmethod
        def run(*args, **kwargs):
            calls.append("terminal")

    decision = oracle_gate.evaluate_routine(
        "/repo", "target", "FN", "/repo/candidate.inc", "/repo/trial", Evaluator
    )
    assert calls == ["training"]
    assert decision["status"] == "failed"
    assert decision["promotion_eligible"] is False


def test_verify_lists_routine_trace_parity_oracle():
    assert "routine-trace-parity" in verify.ORACLES
