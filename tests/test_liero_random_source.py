import hashlib
import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.routine_contract import load_contract
from tools.liero_file_probe import assemble_probe, run_dosbox

GENERATOR = bytes.fromhex(
    "a112648b1e14648bc82ef726e746d1e1d1e1d1e102e903d103d3d1e3d1e303d3"
    "02f3b105d3e302f305010083d200a3126489161464c3"
)
SCALER = bytes.fromhex("e85a008bdc8bca36f767048bc18bca36f7670403c183d2008bc2ca0200")
MULTIPLIER = 0x08088405
RECORD_SIZE = 28


def random_cases():
    """Oracle: fixed corner/state/carry cases for known manual source review, no model."""
    seeds = [0, 1, 0x1234, 0x7FFF, 0x8000, 0xFFFF]
    states = [(high << 16) | low for low in seeds for high in seeds]
    states += [((i * 0x9E3779B9) ^ 0xDEADBEEF) & 0xFFFFFFFF for i in range(256)]
    return [
        (state, bound, mode)
        for state in states
        for mode, bound in [(0, 0), (1, 0), (1, 1), (1, 2), (1, 5), (1, 65535)]
    ] + [(0xD94FA8C4, 65535, 1), (0x26B05733, 65535, 1)]


def expected_random(state, bound):
    """Oracle: independent32-bit recurrence and high-product mathematical expectation."""
    next_state = (state * MULTIPLIER + 1) & 0xFFFFFFFF
    return next_state, (next_state * bound) >> 32


def test_random_corpus_includes_full_carry_and_caller_bounds():
    """Oracle: explicit modulo32 rollover and actual caller2/5 bounds."""
    assert expected_random(0x26B05733, 65535) == (0, 0)
    assert {bound for _, bound, mode in random_cases() if mode} == {0, 1, 2, 5, 65535}


PASCAL = """program ActualRandom;
uses LieroRuntime;
{$I FUN_24dd_46b1.inc}
{$I FUN_24dd_4654.inc}
var inputFile, outputFile: file;
    args: array[0..3] of Word;
    recordWords: array[0..4] of Word;
    count: LongInt;
begin
  if SizeOf(Integer) <> 2 then Halt(1);
  Assign(inputFile, 'CASES.BIN'); Reset(inputFile, 1);
  Assign(outputFile, 'PASCAL.BIN'); Rewrite(outputFile, 1);
  CodeMemory[$46E7] := $05; CodeMemory[$46E8] := $84;
  while not Eof(inputFile) do
  begin
    BlockRead(inputFile, args, 8, count);
    if count <> 8 then Halt(2);
    FillChar(DosMemory, SizeOf(DosMemory), $A5);
    DosMemory[$6412] := Byte(args[0]);
    DosMemory[$6413] := Byte(args[0] shr 8);
    DosMemory[$6414] := Byte(args[1]);
    DosMemory[$6415] := Byte(args[1] shr 8);
    if args[3] = 0 then
    begin
      FUN_24dd_46b1;
      recordWords[0] := RegisterAX;
    end
    else recordWords[0] := Word(FUN_24dd_4654(args[2]));
    recordWords[1] := Word(DosMemory[$6412]) or (Word(DosMemory[$6413]) shl 8);
    recordWords[2] := Word(DosMemory[$6414]) or (Word(DosMemory[$6415]) shl 8);
    recordWords[3] := Word(DosMemory[$6410]) or (Word(DosMemory[$6411]) shl 8);
    recordWords[4] := Word(DosMemory[$6416]) or (Word(DosMemory[$6417]) shl 8);
    if (args[3] = 0) and (RegisterDX <> recordWords[2]) then Halt(4);
    BlockWrite(outputFile, recordWords, 10, count);
    if count <> 10 then Halt(3);
  end;
  Close(inputFile); Close(outputFile);
end.
"""

ASSEMBLY = """
.code16
.global _start
_start:
    push %cs
    pop %ds
    mov $0x1000, %bx
    mov $0x4a00, %ax
    int $0x21
    jc failed
    mov $0x1000, %bx
    mov $0x4800, %ax
    int $0x21
    jc failed
    mov %ax, arena_segment
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, handle
next_case:
    mov arena_segment, %ax
    mov %ax, %es
    xor %di, %di
    cld
    mov $0xa5a5, %ax
    mov $32768, %cx
    rep stosw
    mov index, %si
    shl $3, %si
    add $cases, %si
    mov (%si), %ax
    mov %ax, %es:0x6412
    mov 2(%si), %ax
    mov %ax, %es:0x6414
    mov %sp, before_sp
    mov $0x1234, %bp
    std
    cmpw $0, 6(%si)
    je generator_call
    pushw 4(%si)
    mov arena_segment, %ax
    mov %ax, %ds
    push %cs
    call scaler
    jmp snapshot
generator_call:
    mov arena_segment, %ax
    mov %ax, %ds
    call generator
snapshot:
    mov %ax, %cs:record
    mov %dx, %cs:record+2
    mov 0x6412, %ax
    mov %ax, %cs:record+4
    mov 0x6414, %ax
    mov %ax, %cs:record+6
    mov %cs:before_sp, %ax
    mov %ax, %cs:record+8
    mov %sp, %cs:record+10
    mov %bp, %cs:record+12
    pushf
    pop %ax
    and $0x400, %ax
    mov %ax, %cs:record+14
    mov %ds, %cs:record+16
    mov %ss, %cs:record+18
    mov 0x6410, %ax
    mov %ax, %cs:record+20
    mov 0x6416, %ax
    mov %ax, %cs:record+22
    mov %es, %cs:record+24
    mov %cs, %cs:record+26
    push %cs
    pop %ds
    cld
    mov handle, %bx
    mov $record, %dx
    mov $28, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $28, %ax
    jne failed
    incw index
    cmpw $CASE_COUNT, index
    jne next_case
    mov handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    cld
    mov $0x4c01, %ax
    int $0x21
handle: .word 0
arena_segment: .word 0
before_sp: .word 0
index: .word 0
record: .space 28
filename: .asciz "TRACE.BIN"
cases: .incbin "CASES.BIN"
.org 0x4554
scaler: .incbin "scaler.bin"
.org 0x45b1
generator: .incbin "generator.bin"
.incbin "multiplier.bin"
"""


def test_actual_random_source_and_scaled_returns(tmp_path):
    """Oracle: exact original code/CS constant, allocated DS state, actual target source.

    Finite state/bound memory+return differential; not caller DS provenance/full ABI.
    """
    root = pathlib.Path(__file__).resolve().parents[1]
    target = root / "targets/liero"
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD/probe tools unavailable")
    manifest_path = target / "alternate_streams.json"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads(manifest_path.read_text())
    )
    scaler_offset = header + (0x24DD - base) * 16 + 0x4654
    generator_offset = header + (0x24DD - base) * 16 + 0x46B1
    assert binary[scaler_offset : scaler_offset + len(SCALER)] == SCALER
    assert binary[generator_offset : generator_offset + 54] == GENERATOR
    assert binary[generator_offset + 54 : generator_offset + 56] == b"\x05\x84"
    assert not any(
        start - 1 <= r < start + size
        for r in _mz_relocation_locations(binary, header)
        for start, size in ((scaler_offset, 29), (generator_offset, 56))
    )
    assert 0x4654 + 3 + int.from_bytes(SCALER[1:3], "little", signed=True) == 0x46B1
    for routine, raw, offset in (
        ("FUN_24dd_4654", SCALER, scaler_offset),
        ("FUN_24dd_46b1", GENERATOR, generator_offset),
    ):
        contract = load_contract(target, routine)
        assert contract["reviewed_bytes_hex"] == raw.hex()
        assert contract["binary_sha256"] == identity
        assert contract["file_offset"] == offset
    inputs = random_cases()
    files = [
        target / "src/FUN_24dd_46b1.inc",
        target / "src/FUN_24dd_4654.inc",
        target / "src/LieroRuntime.pas",
        target / "config/routine_contracts.json",
        target / "asm/FUN_24dd_4654.s",
        target / "asm/FUN_24dd_46b1.s",
        pathlib.Path(__file__),
        manifest_path,
        root / "tools/liero_file_probe.py",
        root / "engine/alternate_streams.py",
    ]
    hashes = {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in files
    }
    freeze = {
        "binary_sha256": identity,
        "source_hashes": hashes,
        "cases": inputs,
        "generator_offset": generator_offset,
        "scaler_offset": scaler_offset,
        "constant": "original CS:46e7=8405h; Python recurrence08088405h",
        "premises": "AH48-allocated64K DS is writable; state6412..6415 disjoint from retained COM CS/SS stack/code/corpus; source DosMemory mirrors that DS, CodeMemory46e7..46e8 initialized from original CS. No asynchronous mutations.",
        "budget": "one original execution, one actual-source compilation/execution;30s subprocesses; no model/holdout",
        "limitations": "Finite inputs and original-only BP/SP/DF/DS/SS/ES observations, not full host CPU ABI/normal reachability/caller state provenance.",
    }
    (tmp_path / "freeze.json").write_text(json.dumps(freeze, indent=2) + "\n")
    (tmp_path / "sources").mkdir()
    for path in files:
        shutil.copy2(path, tmp_path / "sources" / path.name)
    (tmp_path / "scaler.bin").write_bytes(SCALER)
    (tmp_path / "generator.bin").write_bytes(GENERATOR)
    (tmp_path / "multiplier.bin").write_bytes(b"\x05\x84")
    (tmp_path / "CASES.BIN").write_bytes(
        b"".join(
            struct.pack("<4H", state & 65535, state >> 16, bound, mode)
            for state, bound, mode in inputs
        )
    )
    assembly = tmp_path / "harness.S"
    assembly.write_text(
        ASSEMBLY.replace("CASE_COUNT", str(len(inputs))).replace(
            '.incbin "', f'.incbin "{tmp_path}/'
        )
    )
    image = assemble_probe(assembly, tmp_path)
    assert image[0x4554 : 0x4554 + 29] == SCALER
    assert image[0x45B1 : 0x45B1 + 56] == GENERATOR + b"\x05\x84"
    assert len(inputs) * 8 + 0x100 + 1024 < 0x4654
    (tmp_path / "PROBE.COM").write_bytes(image)
    run_dosbox(tmp_path)
    (tmp_path / "actual_random.pas").write_text(PASCAL)
    compiled = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fusources", "-Fisources", "-FU.", "actual_random.pas"],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (tmp_path / "fpc.log").write_bytes(compiled.stdout + compiled.stderr)
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    executed = subprocess.run(
        [str(tmp_path / "actual_random")],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (tmp_path / "runtime.log").write_bytes(executed.stdout + executed.stderr)
    assert executed.returncode == 0, executed.stdout + executed.stderr
    original = (tmp_path / "TRACE.BIN").read_bytes()
    actual = (tmp_path / "PASCAL.BIN").read_bytes()
    assert len(original) == len(inputs) * RECORD_SIZE
    assert len(actual) == len(inputs) * 10
    for index, (state, bound, mode) in enumerate(inputs):
        ax, dx, low, high, before, after, bp, df, ds, ss, left, right, es, cs = (
            struct.unpack_from("<14H", original, index * RECORD_SIZE)
        )
        next_state, scaled = expected_random(state, bound)
        assert low | (high << 16) == next_state, index
        assert ax == (scaled if mode else next_state & 65535), index
        if not mode:
            assert dx == next_state >> 16, index
        assert before == after == 0xFFFE and bp == 0x1234 and df == 0x400
        assert ds == es and ds != ss and ss == cs
        assert left == right == 0xA5A5
        assert struct.unpack_from("<5H", actual, index * 10) == (
            ax,
            low,
            high,
            left,
            right,
        ), index
    for relative, expected_hash in hashes.items():
        assert (
            hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected_hash
        )
    result = {
        "status": "scoped-state-and-scaled-return-pass",
        "cases": len(inputs),
        "generator_cases": sum(mode == 0 for _, _, mode in inputs),
        "scale_cases": sum(mode == 1 for _, _, mode in inputs),
        "source_hashes": hashes,
        "limitations": freeze["limitations"],
        "source_promoted": False,
        "artifact_hashes": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in tmp_path.iterdir()
            if path.is_file()
        },
    }
    (tmp_path / "result.json").write_text(json.dumps(result, indent=2) + "\n")
