"""Tests for decomp/contract-derived original-trace fixtures."""

from __future__ import annotations

import pathlib
import struct

from engine import contract_oracle as oracle
from engine import oracle_gate, routine_contract, target_packet

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
    harness = oracle.program(fixture)
    assert "input: array[0..7] of Word" in harness
    assert "flagsWord := Word(arena[0]) or (Word(arena[1]) shl 8);" in harness
    assert "RegisterFlagsWord := flagsWord or $202;" in harness


def test_composed_fixture_attaches_proposed_capability_rules(monkeypatch):
    seen = []

    def capture(evidence):
        seen.append(evidence)
        return True

    monkeypatch.setattr(oracle.asm_emulator, "supported", capture)
    fixture = oracle.fixture(REPO, "liero", "FUN_24dd_4654")
    assert fixture["declaration_source"] == "derived-composed"
    assert seen and seen[-1]["capability_rules"]


def test_derived_declaration_infers_signed_word_result():
    declaration = routine_contract.derived_declaration(
        REPO / "targets/liero", "FUN_1ec2_086b"
    )
    assert declaration == (
        "function FUN_1ec2_086b(param_1: Word; param_2: Integer): Word;"
    )


def test_derived_declaration_infers_word_result_from_absolute_xchg(tmp_path):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (asm_dir / "FN.s").write_text(
        "1000:0000  XOR AX,AX\n"
        "1000:0002  XCHG word ptr [0x6410],AX\n"
        "1000:0007  RETF\n"
    )
    assert routine_contract.derived_declaration(target, "FN") == (
        "function FN: Word;"
    )


def test_harness_loads_arguments_from_current_case():
    harness = oracle.harness(oracle.fixture(REPO, "liero", "FUN_1ec2_086b"))
    assert "mov input+0, %ax" in harness
    assert "mov input+2, %ax" in harness
    assert "mov %ax, %ss:0xefec" in harness
    assert "mov %ax, %ss:0xefee" in harness


def test_program_assigns_arguments_before_stack_writes():
    text = oracle.program(oracle.fixture(REPO, "liero", "FUN_1ec2_086b"))
    assert text.index("arg_0 := ") < text.index(
        "RealModeMemory[(LongInt($191) shl 4) + entry"
    )


def test_absolute_harness_maps_arena_into_data_segment():
    fixture = {
        "bytes": "c3",
        "params": [],
        "near": True,
        "cleanup": 0,
        "args_bytes": 0,
        "absolute_memory": True,
    }
    text = oracle.harness(fixture)
    assert "mov $0x48, %ah" in text
    assert "mov data_segment, %ax" in text
    assert "xor %di, %di" in text
    assert "mov $0x8000, %di" in text
    fixture["absolute_memory"] = False
    plain = oracle.harness(fixture)
    assert "data_segment" not in plain


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


def test_compare_honors_scoped_flag_mask():
    row = bytearray(oracle.RECORD_BYTES)
    struct.pack_into("<H", row, 24, 0x0841)
    candidate = bytearray(row)
    struct.pack_into("<H", candidate, 24, 0x0001)
    assert oracle.compare(bytes(row), bytes(candidate))["failures"][0]["first_different_bytes"] == [24]
    result = oracle.compare(bytes(row), bytes(candidate), flag_mask=0)
    assert result == {"status": "passed", "cases": 1, "matches": 1, "failures": []}


def test_fixture_propagates_contract_scoping():
    scoped = oracle.fixture(REPO, "liero", "FUN_24dd_3e95")
    assert scoped["flag_mask"] == "0x0"
    registered = oracle.fixture(REPO, "liero", "FUN_24dd_23c0")
    assert registered["register_inputs"] == {"SI": 0}


def test_argument_masks_are_applied_before_projection():
    fixture = oracle.fixture(REPO, "liero", "FUN_24dd_4905")
    data = struct.pack("<4H", 0xFFFF, 0xFFFF, 0x8200, 0) + bytes(oracle.CASE_BYTES - 8)
    values = oracle._argument_values(fixture, data)
    assert values == [(0xFFFF, "byte"), (0x3F, "word"), (0x8200, "pointer")]


def test_derived_absolute_fixture_masks_index_registers(tmp_path, monkeypatch):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (target / "config").mkdir()
    (target / "config" / "routine_contracts.json").write_text(
        '{"schema_version": 1, "functions": {}}'
    )
    (asm_dir / "FN.s").write_text(
        "1000:0000  MOV SI,0X5DC\n"
        "1000:0003  MOV CX,0X6\n"
        "1000:0006  MOVSW.REP ES:DI,SI\n"
        "1000:0008  RET\n"
    )
    monkeypatch.setattr(
        target_packet,
        "evidence_for_routine",
        lambda *_args, **_kwargs: {"bytes": {"hex": "c3"}},
    )
    fixture = oracle.fixture(tmp_path, "liero", "FN")
    assert fixture["absolute_memory"] is True
    assert fixture["flag_mask"] == 0
    assert fixture["register_masks"] == {"1": "0x0fff", "2": "0x0fff"}
    words = struct.unpack_from("<4H", oracle.cases(fixture, "training")[0])
    assert words[1] <= 0x0FFF
    assert words[2] <= 0x0FFF


def test_derived_string_fixture_keeps_destination_in_arena(tmp_path, monkeypatch):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (target / "config").mkdir()
    (target / "config" / "routine_contracts.json").write_text(
        '{"schema_version": 1, "functions": {}}'
    )
    (asm_dir / "FN.s").write_text(
        "1000:0000  MOV AX,0X10\n"
        "1000:0003  STOSW ES:DI\n"
        "1000:0004  RET\n"
    )
    monkeypatch.setattr(
        target_packet,
        "evidence_for_routine",
        lambda *_args, **_kwargs: {"bytes": {"hex": "c3"}},
    )
    fixture = oracle.fixture(tmp_path, "liero", "FN")
    assert fixture["absolute_memory"] is False
    assert fixture["register_masks"] == {"2": "0x0fff"}
    assert fixture["register_bases"] == {"2": "0x8000"}
    words = struct.unpack_from("<4H", oracle.cases(fixture, "training")[0])
    assert 0x8000 <= words[2] <= 0x8FFF


def test_derived_division_fixture_avoids_zero_low_bytes(tmp_path, monkeypatch):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (target / "config").mkdir()
    (target / "config" / "routine_contracts.json").write_text(
        '{"schema_version": 1, "functions": {}}'
    )
    (asm_dir / "FN.s").write_text("1000:0000  DIV BL\n1000:0002  RET\n")
    monkeypatch.setattr(
        target_packet,
        "evidence_for_routine",
        lambda *_args, **_kwargs: {"bytes": {"hex": "c3"}},
    )
    fixture = oracle.fixture(tmp_path, "liero", "FN")
    assert fixture["nonzero_low_bytes"] is True
    assert fixture["register_masks"] == {str(index): "0x00ff" for index in range(4)}
    assert all(
        1 <= word <= 0xFF
        for case in oracle.cases(fixture, "training")
        for word in struct.unpack_from("<4H", case)
    )


def test_derived_absolute_bp_load_stays_inside_arena(tmp_path, monkeypatch):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (target / "config").mkdir()
    (target / "config" / "routine_contracts.json").write_text(
        '{"schema_version": 1, "functions": {}}'
    )
    (asm_dir / "FN.s").write_text(
        "1000:0000  MOV BP,word ptr [0xd8]\n"
        "1000:0004  MOV AX,word ptr [BP + 0x4]\n"
        "1000:0008  RET\n"
    )
    monkeypatch.setattr(
        target_packet,
        "evidence_for_routine",
        lambda *_args, **_kwargs: {"bytes": {"hex": "c3"}},
    )
    fixture = oracle.fixture(tmp_path, "liero", "FN")
    assert fixture["absolute_memory"] is True
    assert fixture["memory_words"] == {"0xd8": "0x8000"}
    case = oracle.cases(fixture, "training")[0]
    assert case[8 + 0xd8:8 + 0xda] == b"\x00\x80"


def test_derived_bp_index_memory_stays_inside_arena(tmp_path, monkeypatch):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (target / "config").mkdir()
    (target / "config" / "routine_contracts.json").write_text(
        '{"schema_version": 1, "functions": {}}'
    )
    (asm_dir / "FN.s").write_text(
        "1000:0000  MOV AL,byte ptr [BP + SI + -0x28]\n"
        "1000:0004  INC SI\n"
        "1000:0006  OR AL,AL\n"
        "1000:0009  JNZ 0x1000:000e\n"
        "1000:000b  MOV AL,0x30\n"
        "1000:000e  RET\n"
    )
    monkeypatch.setattr(
        target_packet,
        "evidence_for_routine",
        lambda *_args, **_kwargs: {"bytes": {"hex": "c3"}},
    )
    fixture = oracle.fixture(tmp_path, "liero", "FN")
    assert fixture["register_masks"] == {"1": "0x07ff"}
    assert fixture["register_bases"] == {"1": "0x189f"}
    assert fixture["flag_mask"] == 0
    words = struct.unpack_from("<4H", oracle.cases(fixture, "training")[0])
    address = (oracle.FIXTURE_BP + words[1] - 0x28) & 0xFFFF
    assert 0x8000 <= address <= 0x87FF


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


def test_derived_declaration_uses_stack_cleanup_and_rejects_large_rep(tmp_path):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (target / "config").mkdir()
    (target / "config" / "routine_contracts.json").write_text(
        '{"schema_version": 1, "functions": {}}'
    )
    path = asm_dir / "FN.s"
    path.write_text("1000:0000  MOV AX,1\n1000:0002  RETF 0x4\n")
    assert routine_contract.derived_declaration(target, "FN") == (
        "procedure FN(param_1: Word; param_2: Word);"
    )
    path.write_text("1000:0000  MOV BYTE PTR [0X05EE],0X0\n1000:0005  RETF\n")
    assert routine_contract.derived_declaration(target, "FN") == "procedure FN;"
    path.write_text("1000:0000  MOV BYTE PTR [0X65EE],0X0\n1000:0005  RETF\n")
    assert routine_contract.derived_declaration(target, "FN") is None
    path.write_text("1000:0000  MOV DI,AX\n1000:0002  MOV BYTE PTR [DI+0X67FC],0X0\n1000:0007  RET\n")
    assert routine_contract.derived_declaration(target, "FN") is None
    path.write_text("1000:0000  MOV AX,CS:[0X1234]\n1000:0004  RET\n")
    assert routine_contract.derived_declaration(target, "FN") is None
    path.write_text("1000:0000  MOV CX,CS\n1000:0002  MOV DS,CX\n1000:0004  RET\n")
    assert routine_contract.derived_declaration(target, "FN") is None
    path.write_text(
        "1000:0000  CMP AX,0x0\n"
        "1000:0003  JGE 0x1000:000a\n"
        "1000:0005  MOV AX,0x1\n"
        "1000:0008  JMP 0x1000:000a\n"
        "1000:000a  RET\n"
    )
    assert routine_contract.derived_declaration(target, "FN") == "procedure FN;"
    path.write_text("1000:0000  JMP 0x2000:9000\n")
    assert routine_contract.derived_declaration(target, "FN") is None
    path.write_text(
        "1000:0000  CMP AX,0x0\n"
        "1000:0003  JL 0x1000:0000\n"
        "1000:0005  RET\n"
    )
    assert routine_contract.derived_declaration(target, "FN") is None
    path.write_text(
        "1000:0000  MOV CX,0x3e80\n"
        "1000:0003  MOVSB.REP ES:DI,SI\n"
        "1000:0005  RET\n"
    )
    assert routine_contract.derived_declaration(target, "FN") is None


def test_derived_oracle_fixture_uses_asm_metadata(tmp_path, monkeypatch):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (target / "config").mkdir()
    (target / "config" / "routine_contracts.json").write_text(
        '{"schema_version": 1, "functions": {}}'
    )
    (asm_dir / "FN.s").write_text("1000:0000  RET\n")
    monkeypatch.setattr(
        target_packet, "evidence_for_routine",
        lambda *_args, **_kwargs: {"bytes": {"hex": "c3"}},
    )
    fixture = oracle.fixture(tmp_path, "liero", "FN")
    assert fixture["declaration"] == "procedure FN;"
    assert fixture["declaration_source"] == "derived"
    assert fixture["kind"] == "procedure"
    assert fixture["params"] == []


def test_call_arg_casts_unsigned_integer_within_pascal_range():
    assert oracle._call_arg(49468, "integer") == "Integer(Word(LongInt(49468) and $ffff))"
    assert oracle._call_arg(49468, "word") == "Word(LongInt(49468) and $ffff)"
    assert oracle._call_arg(49468, "byte") == "Byte(LongInt(49468) and $ff)"


def test_high_absolute_memory_word_fixture_is_supported():
    fixture = oracle.fixture(REPO, "liero", "FUN_24dd_04ed")
    assert fixture["declaration"] == "function FUN_24dd_04ed: Word;"
    assert fixture["absolute_memory"] is True
    assert oracle.supported(REPO, "liero", "FUN_24dd_04ed") is True


def test_composed_fixture_inlines_verified_callee():
    fixture = oracle.fixture(REPO, "liero", "FUN_24dd_462e")
    assert fixture["declaration_source"] == "derived-composed"
    assert fixture["declaration"] == "procedure FUN_24dd_462e;"
    assert fixture["raw_asm"].startswith(".byte 0xe8\n.word composedBlock1 - .\n")
    assert "composedBlock1:" in fixture["raw_asm"]


def test_composed_fixture_patches_short_branch_and_mirrors_code_window():
    evidence = target_packet.evidence_for_routine(REPO, "liero", "FUN_24dd_0582")
    facts = evidence["static_evidence"]["raw_byte_facts"]["instructions"]
    instructions = evidence["static_evidence"]["assembly"]["instructions"]
    assert "composedBlock1 - . - 1" in evidence["bytes"]["composed_asm"]
    assert len(facts) == len(instructions)
    assert [item["offset"] for item in facts] == sorted(item["offset"] for item in facts)
    fixture = oracle.fixture(REPO, "liero", "FUN_24dd_0582")
    assert fixture["declaration_source"] == "derived-composed"
    assert fixture["code_memory_windows"] == [{
        "code_offset": 1398,
        "arena_offset": 3840,
        "byte_count": 12,
    }]
    assert "mov $input+8+3840, %si" in oracle.harness(fixture)
    assert "+ 1398 + i] := arena[3840 + i]" in oracle.program(fixture)


def test_derived_declaration_allows_balanced_register_segment_moves(tmp_path):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (asm_dir / "FN.s").write_text(
        "1000:0000  PUSH DS\n"
        "1000:0001  MOV CX,CS\n"
        "1000:0003  MOV DS,CX\n"
        "1000:0005  MOV AX,0X400\n"
        "1000:0008  XCHG AX,SI\n"
        "1000:0009  CLD\n"
        "1000:000A  MOV CX,0X4\n"
        "1000:000D  MOVSW.REP ES:DI,SI\n"
        "1000:000F  SUB DI,0X8\n"
        "1000:0012  XCHG AX,SI\n"
        "1000:0013  POP DS\n"
        "1000:0014  RET\n"
    )
    assert routine_contract.derived_declaration(target, "FN") == "procedure FN;"


def test_derived_declaration_allows_owned_pointer_loads(tmp_path):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (asm_dir / "FN.s").write_text(
        "1000:0000  LDS SI,SS:[BX + 0X4]\n"
        "1000:0003  LES DI,SS:[BX + 0X6]\n"
        "1000:0006  RET\n"
    )

    assert routine_contract.derived_declaration(target, "FN") == "procedure FN;"


def test_code_memory_window_comes_from_register_segment_move_and_string_source():
    instructions = [
        "MOV CX,CS", "MOV DS,CX", "MOV AX,0X400", "XCHG AX,SI",
        "CLD", "MOV CX,0X4", "MOVSW.REP ES:DI,SI", "RET",
    ]
    windows = oracle._derived_code_memory_windows(
        instructions, "b800048cc98ed996fcb90600f3a5c3"
    )
    assert windows == [{
        "code_offset": 0x400, "arena_offset": 0x0F00, "byte_count": 8,
    }]


def test_code_memory_window_is_mirrored_in_both_harnesses(tmp_path, monkeypatch):
    target = tmp_path / "targets" / "liero"
    asm_dir = target / "asm"
    asm_dir.mkdir(parents=True)
    (target / "config").mkdir()
    (target / "config" / "routine_contracts.json").write_text(
        '{"schema_version": 1, "functions": {}}'
    )
    (asm_dir / "FN.s").write_text(
        "1000:0000  PUSH DS\n"
        "1000:0001  MOV CX,CS\n"
        "1000:0003  MOV DS,CX\n"
        "1000:0005  MOV AX,0X400\n"
        "1000:0008  XCHG AX,SI\n"
        "1000:0009  CLD\n"
        "1000:000A  MOV CX,0X4\n"
        "1000:000D  MOVSW.REP ES:DI,SI\n"
        "1000:000F  SUB DI,0X8\n"
        "1000:0012  XCHG AX,SI\n"
        "1000:0013  POP DS\n"
        "1000:0014  RET\n"
    )
    monkeypatch.setattr(
        target_packet,
        "evidence_for_routine",
        lambda *_args, **_kwargs: {
            "bytes": {"hex": "b800048cc98ed996fcb90600f3a583ef0c961fc3"}
        },
    )
    fixture = oracle.fixture(tmp_path, "liero", "FN")
    assert fixture["code_memory_windows"] == [{
        "code_offset": 0x400, "arena_offset": 0x0F00, "byte_count": 8,
    }]
    assert "mov $input+8+3840, %si" in oracle.harness(fixture)
    assert "mov $1024, %di" in oracle.harness(fixture)
    assert "+ 1024 + i] := arena[3840 + i];" in oracle.program(fixture)
