import pathlib

from engine import asm_emulator, capability_dsl, capability_proposer, capability_registry


def _evidence(tmp_path, instructions=None):
    binary = tmp_path / "binary.bin"
    data = bytearray(0x100)
    data[0x20] = 0x34
    data[0x21] = 0x12
    binary.write_bytes(data)
    return {
        "target": "synthetic",
        "routine": "FN",
        "binary": {"path": str(binary)},
        "address_mapping": {"load_segment_inferred_from_entry": 0x191},
        "fixture_cs": 0x191,
        "static_evidence": {
            "assembly": {
                "instructions": instructions or ["MOV AX,WORD PTR CS:[0X0020]"],
                "addresses": list(range(len(instructions or ["MOV AX,WORD PTR CS:[0X0020]"]))),
                "segments": [0x191] * len(instructions or ["MOV AX,WORD PTR CS:[0X0020]"]),
            }
        },
    }


def test_code_memory_rule_maps_code_operand_to_runtime_mirror(tmp_path):
    evidence = _evidence(tmp_path)
    proposals = capability_proposer.propose_for_evidence(tmp_path, evidence)
    assert len(proposals) == 1
    compiled = capability_dsl.compile_rules([proposals[0][1]])
    assert capability_dsl.rewrite(
        compiled, "MOV AX,WORD PTR CS:[0X0020]", evidence
    ) == "MOV AX,WORD PTR CodeMemory[0X0020]"


def test_emulator_applies_learned_rule(tmp_path):
    evidence = _evidence(tmp_path, ["MOV AX,WORD PTR CS:[0X0020]", "RET"])
    evidence["oracle_contract"] = {"declaration": "function FN: Word;"}
    proposals = capability_proposer.propose_for_evidence(tmp_path, evidence)
    evidence["capability_rules"] = [rule for _, rule in proposals]
    source = asm_emulator.translate(evidence)
    assert "CodeMemory[$20]" in source or "CodeMemory[$21]" in source


def test_memory_rules_model_persistent_absolute_state(tmp_path):
    evidence = _evidence(
        tmp_path,
        [
            "MOV AX,WORD PTR [0X6412]",
            "MOV BX,WORD PTR [0X6414]",
            "MOV WORD PTR [0X6412],AX",
            "MOV WORD PTR [0X6414],AX",
            "RET",
        ],
    )
    evidence["oracle_contract"] = {"declaration": "function FN: Word;"}
    proposals = capability_proposer.propose_for_evidence(tmp_path, evidence)
    assert {rule["id"] for _, rule in proposals} == {
        "memory-read-absolute-6412",
        "memory-read-absolute-6414",
        "memory-write-absolute-6412",
        "memory-write-absolute-6414",
    }
    evidence["capability_rules"] = [rule for _, rule in proposals]
    compiled = capability_dsl.compile_rules([rule for _, rule in proposals])
    read = capability_dsl.apply(compiled, "MOV AX,WORD PTR [0X6412]", evidence)
    assert read[0].startswith("if (Word(DosMemory[$6412])")
    assert read[-1] == "RegisterAX := emuAbsState0;"
    read_high = capability_dsl.apply(compiled, "MOV AX,WORD PTR [0X6414]", evidence)
    assert read_high[-1] == "RegisterAX := emuAbsState1;"
    assert capability_dsl.apply(
        compiled, "MOV WORD PTR [0X6412],AX", evidence
    ) == [
        "emuAbsState0 := RegisterAX;",
        "emuAbsState0Mirror := RegisterAX;",
        "DosMemory[$6412] := Byte(RegisterAX);",
        "DosMemory[$6413] := Byte((RegisterAX shr 8) and $ff);",
    ]
    assert capability_dsl.apply(
        compiled, "MOV WORD PTR [0X6414],AX", evidence
    ) == [
        "emuAbsState1 := RegisterAX;",
        "emuAbsState1Mirror := RegisterAX;",
        "DosMemory[$6414] := Byte(RegisterAX);",
        "DosMemory[$6415] := Byte((RegisterAX shr 8) and $ff);",
    ]
    source = asm_emulator.translate(evidence)
    assert "emuAbsState0: LongInt;" in source
    assert "emuAbsState0Mirror: LongInt;" in source
    assert "DosMemory[$6414] := Byte(RegisterAX);" in source
    assert "LEmuSetW(RegisterDS, $6414, RegisterAX);" not in source

    evidence["absolute_memory"] = True
    assert capability_dsl.apply(
        compiled, "MOV AX,WORD PTR [0X6412]", evidence
    ) == ["RegisterAX := LEmuMemW(RegisterDS, $6412);"]


def test_flags_rule_preserves_zero_flag_for_adc_zero(tmp_path):
    evidence = _evidence(tmp_path, ["ADC DX,0X0", "RET"])
    evidence["oracle_contract"] = {"declaration": "procedure FN;"}
    proposals = capability_proposer.propose_for_evidence(tmp_path, evidence)
    assert proposals[0][1]["kind"] == "flags_adc_zero"
    evidence["capability_rules"] = [rule for _, rule in proposals]
    source = asm_emulator.translate(evidence)
    assert "emuAdcZeroCarry: Boolean;" in source
    assert "RegisterCarryFlag := emuAdcZeroCarry;" in source
    assert source.rindex("RegisterCarryFlag") > source.rindex("RegisterDX := emuAdcZeroResult;")


def test_function_source_binds_parameters_to_emulated_registers(tmp_path):
    evidence = _evidence(tmp_path, ["MOV AX,BX", "RET"])
    evidence["oracle_contract"] = {
        "declaration": "function FN(param_1: Word; param_2: Integer): Word;"
    }
    source = asm_emulator.translate(evidence)
    assert "RegisterAX := Word(param_1);" in source
    assert "RegisterBX := Word(param_2);" in source
    assert "LEmuSetW(RegisterSS, ((RegisterSP + 2) and $ffff), Word(param_1));" in source
    assert "LEmuSetW(RegisterSS, ((RegisterSP + 4) and $ffff), Word(param_2));" in source
    assert "FN := RegisterAX;" in source


def test_far_procedure_source_binds_parameters_after_far_frame(tmp_path):
    evidence = _evidence(tmp_path, ["MOV AX,BX", "RETF 0X2"])
    evidence["oracle_contract"] = {
        "declaration": "procedure FN(param_1: Word; param_2: Word);"
    }
    source = asm_emulator.translate(evidence)
    assert "LEmuSetW(RegisterSS, ((RegisterSP + 4) and $ffff), Word(param_1));" in source
    assert "LEmuSetW(RegisterSS, ((RegisterSP + 6) and $ffff), Word(param_2));" in source


def test_hardware_flags_rule_uses_full_flags_word(tmp_path):
    evidence = _evidence(
        tmp_path, ["XOR AX,AX", "PUSHF", "POP BX", "PUSH BX", "POPF", "RET"]
    )
    evidence["oracle_contract"] = {"declaration": "procedure FN;"}
    evidence["capability_rules"] = [{
        "id": "hardware-flags-word",
        "kind": "flags_hardware_word",
        "match": r"^PUSHF$",
    }]
    source = asm_emulator.translate(evidence)
    assert "LEmuPush(RegisterFlagsWord);" in source
    assert "LEmuSetFlagsWord(Word(" in source
    assert "procedure LEmuSetResultFlags" in source
    assert "Word(Word(RegisterCarryFlag)" not in source


def test_rules_adapt_to_byte_registers_and_numeric_segments(tmp_path):
    evidence = _evidence(tmp_path, ["MOV AL,BYTE PTR CS:[0X20]"])
    byte_proposals = capability_proposer.propose_for_evidence(tmp_path, evidence)
    assert byte_proposals[0][1]["source"] == "code_memory"
    compiled = capability_dsl.compile_rules([byte_proposals[0][1]])
    assert capability_dsl.rewrite(
        compiled, "MOV AL,BYTE PTR CS:[0X20]", evidence
    ) == "MOV AL,BYTE PTR CodeMemory[0X0020]"

    evidence2 = _evidence(tmp_path, ["MOV BX,WORD PTR 0191:[0X0030]"])
    data = bytearray(pathlib.Path(evidence2["binary"]["path"]).read_bytes())
    data[0x40:0x42] = bytes([0x34, 0x12])
    pathlib.Path(evidence2["binary"]["path"]).write_bytes(data)
    evidence2["static_evidence"]["assembly"]["segments"] = [0x250]
    evidence2["address_mapping"]["load_segment_inferred_from_entry"] = 0x190
    word_proposals = capability_proposer.propose_for_evidence(tmp_path, evidence2)
    compiled2 = capability_dsl.compile_rules([word_proposals[0][1]])
    assert capability_dsl.rewrite(
        compiled2, "MOV BX,WORD PTR 0191:[0X0030]", evidence2
    ) == "MOV BX,WORD PTR CodeMemory[0X0030]"


def test_rules_use_routine_image_to_file_delta_for_segment_lengths(tmp_path):
    evidence = _evidence(tmp_path, ["MOV AX,WORD PTR 0100:[0X0020]"])
    binary = pathlib.Path(evidence["binary"]["path"])
    data = bytearray(0x1230)
    data[0x1220:0x1222] = bytes([0x34, 0x12])
    binary.write_bytes(data)
    evidence["bytes"] = {
        "file_offset": "0x1200",
        "image_offset": "0x1000",
    }
    evidence["address_mapping"] = {}
    proposals = capability_proposer.propose_for_evidence(tmp_path, evidence)
    compiled = capability_dsl.compile_rules([proposals[0][1]])
    assert capability_dsl.rewrite(
        compiled, "MOV AX,WORD PTR 0100:[0X0020]", evidence
    ) == "MOV AX,WORD PTR CodeMemory[0X0020]"


def test_rules_take_cs_segment_from_evidence(tmp_path):
    evidence = _evidence(tmp_path, ["MOV AX,WORD PTR CS:[0X0020]"])
    evidence["static_evidence"]["assembly"]["segments"] = [0x200]
    evidence["address_mapping"]["load_segment_inferred_from_entry"] = 0x200
    proposals = capability_proposer.propose_for_evidence(tmp_path, evidence)
    compiled = capability_dsl.compile_rules([proposals[0][1]])
    assert capability_dsl.rewrite(
        compiled, "MOV AX,WORD PTR CS:[0X0020]", evidence
    ) == "MOV AX,WORD PTR CodeMemory[0X0020]"


def test_rules_rewrite_new_operation_patterns(tmp_path):
    evidence = _evidence(tmp_path, ["MUL WORD PTR CS:[0X0020]"])
    proposals = capability_proposer.propose_for_evidence(tmp_path, evidence)
    assert proposals[0][1]["id"] == "rewrite-unary-word"
    compiled = capability_dsl.compile_rules([proposals[0][1]])
    assert capability_dsl.rewrite(
        compiled, "MUL WORD PTR CS:[0X0020]", evidence
    ) == "MUL WORD PTR CodeMemory[0X0020]"


def test_proposer_learns_code_memory_without_binary_mapping(tmp_path):
    evidence = _evidence(tmp_path)
    evidence.pop("binary")
    assert capability_proposer.propose_for_evidence(tmp_path, evidence)


def test_rule_capability_needs_two_verified_routines(tmp_path):
    evidence = _evidence(tmp_path)
    capability_id, _ = capability_proposer.propose_for_evidence(tmp_path, evidence)[0]
    capability_registry.record_outcome(
        tmp_path, "synthetic", "FN", [capability_id], "verified", evidence,
    )
    entry = capability_registry.load(tmp_path)["capabilities"][capability_id]
    assert entry["status"] == "candidate"
    assert entry["generalized"] is False
    capability_registry.record_outcome(
        tmp_path, "synthetic", "FN2", [capability_id], "verified", evidence,
    )
    entry = capability_registry.load(tmp_path)["capabilities"][capability_id]
    assert entry["status"] == "verified"
    assert entry["generalized"] is True


def test_emulator_executes_inlined_call_before_caller_epilogue(tmp_path):
    instructions = [
        "PUSH BP",
        "MOV BP,SP",
        "CALL 0X2:0010",
        "LEAVE",
        "RET",
        "MOV AX,0X1",
        "RETF 0X2",
    ]
    binary = tmp_path / "binary.bin"
    binary.write_bytes(bytes(0x100))
    evidence = {
        "target": "synthetic",
        "routine": "FN",
        "binary": {"path": str(binary)},
        "address_mapping": {"load_segment_inferred_from_entry": 0x2},
        "fixture_cs": 0x2,
        "oracle_contract": {"declaration": "function FN: Word;"},
        "static_evidence": {
            "assembly": {
                "instructions": instructions,
                "addresses": [0x20, 0x21, 0x22, 0x23, 0x24, 0x30, 0x31],
                "segments": [0x2] * len(instructions),
            }
        },
    }
    translator = asm_emulator._Translator(evidence)
    assert translator._execution_order() == [0, 1, 2, 5, 6, 3, 4]


def test_emulator_models_repeat_compare_and_scan(tmp_path):
    evidence = _evidence(
        tmp_path,
        [
            "CLD",
            "MOV CX,0X4",
            "CMPSB.REPE ES:DI,SI",
            "SCASB.REPNE ES:DI",
            "RET",
        ],
    )
    evidence["oracle_contract"] = {"declaration": "procedure FN;"}
    source = asm_emulator.translate(evidence)

    assert "while (RegisterCX <> 0) and RegisterZeroFlag do" in source
    assert "while (RegisterCX <> 0) and (not RegisterZeroFlag) do" in source
    assert "LEmuMemB(RegisterDS, RegisterSI)" in source
    assert "LEmuMemB(RegisterES, RegisterDI)" in source
    assert source.count(
        "RegisterSI := (LongInt(RegisterSI) + emuStep * 1) and $ffff;"
    ) >= 1
    assert source.count(
        "RegisterDI := (LongInt(RegisterDI) + emuStep * 1) and $ffff;"
    ) >= 2
