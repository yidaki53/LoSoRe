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

EMULATED = [
    "CLD",
    "MOV BX,SP",
    "MOV DX,DS",
    "LES DI,SS:[BX + 0x8]",
    "LDS SI,SS:[BX + 0x4]",
    "LODSB SI",
    "STOSB ES:DI",
    "MOV CL,AL",
    "XOR CH,CH",
    "MOVSB.REP ES:DI,SI",
    "MOV DX,DS",
    "RETF 0x4",
]


STOS_SEQUENCE = [
    "MOV AX,0x5dc",
    "MOV CX,CS",
    "STOSB ES:DI",
    "RET",
]

BYTE_FLAGS = [
    "MOV AL,0xff",
    "ADD AL,0x2",
    "RET",
]

LINEAR_ALU = [
    "ENTER 0x4,0x0",
    "CWD",
    "TEST AX,0x1",
    "NEG BX",
    "NOT CX",
    "CLC",
    "RET",
]

SIGNED_MULTIPLY = [
    "IMUL AX,0x2",
    "RCL DX,0x1",
    "CBW",
    "RET",
]

DECIMAL_ADJUST = [
    "AAM 0xa",
    "AAD 0xa",
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


def test_generic_synthesizer_renders_bounded_internal_branches():
    instructions = [
        "CMP AX,0x0",
        "JGE 0x1000:0008",
        "MOV AX,0x1",
        "RET",
    ]
    evidence = _evidence("ANY", instructions)
    evidence["static_evidence"]["assembly"].update({
        "addresses": [0x10000, 0x10003, 0x10005, 0x10008],
        "segments": [0x1000, 0x1000, 0x1000, 0x1000],
    })
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert result["ir"]["shape"] == "asm-emulation-v1"
    assert "label emuL3;" in result["source"]
    assert "if RegisterSignFlag = RegisterOverflowFlag then goto emuL3;" in result["source"]
    assert "RegisterSignFlag :=" in result["source"]
    assert "RegisterOverflowFlag :=" in result["source"]


def test_generic_synthesizer_rejects_external_branches():
    evidence = _evidence("ANY", ["JMP 0x2000:9000"])
    evidence["static_evidence"]["assembly"].update({
        "addresses": [0x10000],
        "segments": [0x1000],
    })
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "unsupported"


def test_generic_synthesizer_emulates_binary_derived_instructions():
    evidence = _evidence("ANY", EMULATED)
    evidence["oracle_contract"] = {
        "declaration": "procedure ANY(param_1, param_2: Pointer);"
    }
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert result["ir"]["shape"] == "asm-emulation-v1"
    assert "LEmuMemW(RegisterSS, (((RegisterBX) + ($8)) and $ffff))" in result["source"]
    assert "MOVS" not in result["source"]
    assert "ANY" not in result["source"].replace("procedure ANY", "procedure FN")


def test_generic_synthesizer_emulation_has_no_routine_identity_dispatch():
    def source_for(name):
        evidence = _evidence(name, EMULATED)
        evidence["oracle_contract"] = {
            "declaration": f"procedure {name}(param_1, param_2: Pointer);"
        }
        return generic_synthesizer.synthesize(evidence)["source"]

    assert source_for("FN_A").replace("FN_A", "FN") == source_for("FN_B").replace("FN_B", "FN")


def test_generic_synthesizer_emulates_store_without_source_pointer():
    evidence = _evidence("ANY", STOS_SEQUENCE)
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert result["ir"]["shape"] == "asm-emulation-v1"
    assert "RegisterCX := $191;" in result["source"]
    assert "RegisterCS" not in result["source"]
    assert "RegisterSI" not in result["source"]
    assert "LEmuSetB(RegisterES, RegisterDI, (RegisterAX and $ff));" in result["source"]


def test_generic_synthesizer_emulates_mapped_absolute_memory():
    evidence = _evidence("ANY", ["MOV BYTE PTR [0X65EE],0X0", "RET"])
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert "LEmuSetB(RegisterDS, (((($65ee)) and $ffff) and $ffff), $0);" in result["source"]


def test_generic_synthesizer_emulates_high_absolute_memory_xchg():
    evidence = _evidence("ANY", ["XCHG word ptr [0X6410],AX", "RET"])
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert "LEmuMemW(RegisterDS, (((($6410)) and $ffff) and $ffff))" in result["source"]
    assert "LEmuSetW(RegisterDS, (((($6410)) and $ffff) and $ffff), RegisterAX)" in result["source"]


def test_generic_synthesizer_composed_evidence_uses_inlined_call_emulation():
    evidence = _evidence(
        "ANY", ["CALL 0X2000:1000", "RET", "RET"]
    )
    evidence["static_evidence"]["assembly"]["addresses"] = [0x20000, 0x20003, 0x21000]
    evidence["static_evidence"]["assembly"]["segments"] = [0x2000, 0x2000, 0x2000]
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    evidence["composed"] = {"callees": ["CALLEE"]}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert result["ir"]["shape"] == "asm-emulation-v1"
    assert "RegisterSP := (RegisterSP - 2) and $ffff;" in result["source"]
    assert "RegisterSP := (RegisterSP + 2) and $ffff;" in result["source"]


def test_generic_synthesizer_emulates_byte_width_flags():
    evidence = _evidence("ANY", BYTE_FLAGS)
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert "emuTemp1 := ((RegisterAX and $ff)) and $ff;" in result["source"]
    assert "emuTemp2 := LongInt(emuTemp1) + LongInt((($2) and $ff)) > $ff;" in result["source"]
    assert "emuTemp1 := (LongInt(emuTemp1) + LongInt((($2) and $ff))) and $ff;" in result["source"]


def test_generic_synthesizer_emulates_linear_alu_classes():
    evidence = _evidence("ANY", LINEAR_ALU)
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert "RegisterSP := (RegisterSP - 4) and $ffff;" in result["source"]
    assert "RegisterDX := $ffff;" in result["source"]
    assert "RegisterCarryFlag := False;" in result["source"]
    assert "RegisterCarryFlag := emuTemp" in result["source"]
    assert "LongInt(not emuTemp" in result["source"]


def test_generic_synthesizer_emulates_signed_multiply_and_rotate():
    evidence = _evidence("ANY", SIGNED_MULTIPLY)
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert "LEmuSigned16(Word((RegisterAX) and $ffff))" in result["source"]
    assert "RegisterCarryFlag := (emuTemp" in result["source"]
    assert "while emuTemp" in result["source"]
    assert "if (RegisterAX and $80) <> 0 then RegisterAX := RegisterAX or $ff00;" in result["source"]


def test_generic_synthesizer_emulates_decimal_adjust():
    evidence = _evidence("ANY", DECIMAL_ADJUST)
    evidence["oracle_contract"] = {"declaration": "procedure ANY;"}
    result = generic_synthesizer.synthesize(evidence)
    assert result["status"] == "synthesized"
    assert "div 10;" in result["source"]
    assert "mod 10;" in result["source"]
    assert "((RegisterAX shr 8) and $ff) * 10" in result["source"]
    assert "RegisterZeroFlag := (RegisterAX and $ff) = 0;" in result["source"]


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
