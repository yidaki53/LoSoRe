"""Original SS-byte arithmetic integration; controls are not model recovery."""

import json
import shutil
import struct
import subprocess

import pytest

from engine.routine_contract import load_contract
from tools import liero_nibble_caller as caller
from tools import liero_source_trial as trial


def test_actual_nibble_argument_provenance_and_contract(monkeypatch):
    """Oracle: original near call PUSH BP and SS/ES/DS direction; never decompiler text."""
    if not (trial.ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("BYOD unavailable")
    contract = caller.contract(trial.ROOT)
    assert contract["call_site"] == "249c:005d"
    assert contract["callee_entry"] == "249c:0013"
    assert contract["relocations"] == []
    stored = load_contract(trial.ROOT / "targets/liero", "FUN_249c_0013")
    assert stored is not None
    assert stored["declaration"] == "procedure FUN_249c_0013(param_1: Integer);"
    assert stored["reviewed_bytes_hex"] == contract["callee_bytes"]
    assert "RegisterSS" in stored["memory_model"] and "active" in stored["memory_model"]
    assert "0000/3930/04f4" in stored["prompt"]
    monkeypatch.setattr(caller, "CALLER", b"\x90" + caller.CALLER[1:])
    with pytest.raises(ValueError, match="bytes differ"):
        caller.contract(trial.ROOT)


def test_arithmetic_caller_full_state_and_instrumentation_mutants():
    """Oracle: all256 shortstring lengths, entire local arena/stack and explicit capture writes."""
    inputs = caller.cases("training")
    assert len(inputs) == 256 and inputs != caller.cases("terminal")
    records = []
    for data in inputs:
        row = bytearray(caller.expected(data, 0x2000, native=True))
        struct.pack_into("<HH", row, 32 + 0x474, 0x456, 0x2000)
        records.append(bytes(row))
    trace = b"".join(records)
    assert (
        caller.compare(
            inputs, trace, native=True, return_offset=0x456, return_segment=0x2000
        )["matches"]
        == 256
    )
    for offset in (
        0,
        2,
        8,
        10,
        12,
        14,
        16,
        32 + 0x36F,
        32 + 0x372,
        32 + 0x474,
        32 + 0x47E,
    ):
        mutant = bytearray(trace)
        mutant[offset] ^= 1
        assert (
            caller.compare(
                inputs,
                bytes(mutant),
                native=True,
                return_offset=0x456,
                return_segment=0x2000,
            )["status"]
            == "failed"
        )
    with pytest.raises(ValueError, match="partial"):
        caller.compare(
            inputs, trace[:-1], native=True, return_offset=0x456, return_segment=0x2000
        )
    assert "    cli\n    mov $0x1234" in caller.harness()
    assert "    sti\n    mov output_handle" in caller.harness()


def test_original_arithmetic_caller_and_installed_source_replay(tmp_path):
    """Oracle: actual original512-case differential; this regression is not another live model recovery."""
    if not (trial.ROOT / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(n) for n in ("as", "ld", "fpc", "dosbox")
    ):
        pytest.skip("original caller dependencies unavailable")
    output = tmp_path / "caller"
    result = caller.run(trial.ROOT, output)
    assert result["training"]["matches"] == result["terminal"]["matches"] == 256
    assert result["model_requests"] == 0 and result["source_installed"] is True
    assert result["whole_caller_accepted"] is False
    assert caller.replay(trial.ROOT, output) == result
    candidate = output / "host-training/candidate.inc"
    candidate.write_text(candidate.read_text() + "\n{ changed }\n")
    with pytest.raises(ValueError, match="artifact changed"):
        caller.replay(trial.ROOT, output)
    assert (
        json.loads((output / "freeze.json").read_text())["contract"][
            "whole_caller_accepted"
        ]
        is False
    )


def test_installed_nibble_source_exhaustive_cells_and_segment_wrap(tmp_path):
    """Oracle: complete byte-pair arithmetic and existing segmented-memory runtime."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    program = """program IntegratedNibble;
uses LieroRuntime;
{$I FUN_249c_0013.inc}
var first, second, caseIndex: LongInt; argument, cell0, cell1, cell2: Word;
    expectedValue, physical0, physical1, physical2: LongInt;
const offsets: array[0..5] of Word = (0,1,259,260,261,$ffff);
begin
  RegisterSS := $2000; argument := $8400;
  for first := 0 to 255 do
    for second := 0 to 255 do begin
      RealModeMemory[$282fb] := first; RealModeMemory[$282fc] := second;
      RegisterAX := $ffff; RegisterDX := $ffff; RegisterBX := $1357;
      RegisterCX := $2468; RegisterBP := $6789; RegisterSP := $eff0;
      RegisterSI := $abcd; RegisterDS := $1234; RegisterES := $3456;
      RegisterCarryFlag := True; RegisterZeroFlag := True;
      RegisterDirectionFlag := True;
      FUN_249c_0013(Integer(argument));
      expectedValue := first * 16 + second;
      if (RegisterAX <> expectedValue) or (RegisterDX <> second) or
         (RealModeMemory[$282fd] <> (expectedValue and 255)) or
         (RealModeMemory[$282fb] <> first) or (RealModeMemory[$282fc] <> second) or
         (RegisterDI <> argument) or (RegisterSP <> $eff4) or
         (RegisterBP <> $6789) or (RegisterBX <> $1357) or (RegisterCX <> $2468) or
         (RegisterSI <> $abcd) or (RegisterDS <> $1234) or (RegisterES <> $3456) or
         (RegisterSS <> $2000) or RegisterCarryFlag or
         (RegisterZeroFlag <> (expectedValue = 0)) or not RegisterDirectionFlag then Halt(1);
    end;
  for caseIndex := 0 to 5 do begin
    argument := offsets[caseIndex]; RegisterSS := $ffff;
    cell0 := (LongInt(argument) - 261) and $ffff;
    cell1 := (LongInt(argument) - 260) and $ffff;
    cell2 := (LongInt(argument) - 259) and $ffff;
    physical0 := (LongInt(RegisterSS) * 16 + cell0) and $fffff;
    physical1 := (LongInt(RegisterSS) * 16 + cell1) and $fffff;
    physical2 := (LongInt(RegisterSS) * 16 + cell2) and $fffff;
    RealModeMemory[physical0] := 17; RealModeMemory[physical1] := 3;
    RegisterSP := $fffe; RegisterDirectionFlag := False;
    FUN_249c_0013(Integer(argument));
    if (RegisterAX <> 275) or (RealModeMemory[physical2] <> 19) or
       (RegisterDI <> argument) or (RegisterSP <> 2) or RegisterDirectionFlag then Halt(2);
  end;
  Writeln('65536 byte pairs and6 segmented-offset boundaries passed');
end.
"""
    (tmp_path / "probe.pas").write_text(program)
    build = subprocess.run(
        [
            "fpc",
            "-Mtp",
            "-Cr",
            f"-Fu{trial.ROOT / 'targets/liero/src'}",
            f"-Fi{trial.ROOT / 'targets/liero/src'}",
            "-FU.",
            "probe.pas",
        ],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    execution = subprocess.run(
        [str(tmp_path / "probe")],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert execution.returncode == 0, execution.stdout + execution.stderr
    assert b"65536 byte pairs" in execution.stdout


def test_cursor_service_original_and_installed_projection(tmp_path, monkeypatch):
    """Oracle: original BIOS query/BDA and Pascal logical position only, never full ABI parity."""
    if not (trial.ROOT / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(n) for n in ("as", "ld", "fpc", "dosbox")
    ):
        pytest.skip("original cursor dependencies unavailable")
    output = tmp_path / "cursor"
    result = caller.run_cursor(trial.ROOT, output)
    assert result["matches"] == result["logical_cursor_matches"] == 16
    assert result["logical_word_boundary_cases"] == 65536
    assert result["pascal_parity"] is False and not result["whole_routine_accepted"]
    assert caller.replay_cursor(trial.ROOT, output) == result
    contract = caller.text_dependency_contracts(trial.ROOT)
    assert not contract["FUN_24dd_04f4"]["whole_routine_resolved"]
    assert not contract["FUN_24dd_3899"]["whole_routine_resolved"]
    assert "Output-mode396c" in contract["FUN_24dd_3899"]["blockers"][1]
    assert "010f" in contract["FUN_24dd_04f4"]["error_path"]
    source = load_contract(trial.ROOT / "targets/liero", "FUN_249c_0000")
    assert (
        source is not None
        and source["declaration"]
        == "procedure FUN_249c_0000(columnWord, rowWord: Word);"
    )
    assert source["reviewed_bytes_hex"] == caller.CURSOR_BYTES.hex()
    stored = load_contract(trial.ROOT / "targets/liero", "FUN_24dd_3899")
    assert (
        stored is not None
        and stored["reviewed_bytes_hex"] == caller.BUFFER_WRITE_BYTES.hex()
    )
    target = trial.ROOT / "targets/liero"
    binary, header, base, _ = caller.load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    relocations = caller._mz_relocation_locations(binary, header)
    for stream in stored["output_linkage"]["streams"]:
        start = header + (stream["segment"] - base) * 16 + stream["offset"]
        raw = bytes.fromhex(stream["bytes"])
        assert binary[start : start + len(raw)] == raw
        assert (
            sorted(p - start for p in relocations if start - 1 <= p < start + len(raw))
            == stream["relocations"]
        )
    monkeypatch.setattr(
        caller, "ERROR_CHECK_BYTES", b"\x90" + caller.ERROR_CHECK_BYTES[1:]
    )
    with pytest.raises(ValueError, match="original bytes"):
        caller.text_dependency_contracts(trial.ROOT)
    (output / "host/CURSOR.BIN").write_bytes(b"\0" * 96)
    with pytest.raises(ValueError, match="artifact changed"):
        caller.replay_cursor(trial.ROOT, output)
