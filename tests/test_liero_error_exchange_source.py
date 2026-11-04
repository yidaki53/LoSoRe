import hashlib
import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from tools.liero_file_probe import assemble_probe, run_dosbox

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROUTINE = "FUN_24dd_04ed"
RAW = bytes.fromhex("33c087061064cb")
RECORD_BYTES = 64


def actual_program():
    """Oracle: actual target include/runtime; every word plus immediate second invocation."""
    return """program ActualErrorExchange;
uses LieroRuntime;
{$I FUN_24dd_04ed.inc}
var bits: LongInt; firstResult, secondResult: Word;
    outputFile: file; row: array[0..6] of Word; written: LongInt;
begin
  if SizeOf(Integer) <> 2 then Halt(1);
  Assign(outputFile, 'PASCAL.BIN'); Rewrite(outputFile, 1);
  for bits := 0 to 65535 do
  begin
    GlobalWord6410 := Word(bits);
    RegisterAX := Word(bits) xor $ffff;
    RegisterCarryFlag := True;
    RegisterZeroFlag := False;
    RegisterDirectionFlag := (bits and 1) <> 0;
    firstResult := FUN_24dd_04ed;
    row[0] := firstResult; row[1] := RegisterAX;
    row[2] := Word(RegisterCarryFlag) + Word(RegisterZeroFlag) * $40 +
      Word(RegisterDirectionFlag) * $400;
    if (firstResult <> bits) or (RegisterAX <> bits) or
       (GlobalWord6410 <> 0) or RegisterCarryFlag or not RegisterZeroFlag or
       (RegisterDirectionFlag <> ((bits and 1) <> 0)) then Halt(2);
    secondResult := FUN_24dd_04ed;
    row[3] := secondResult; row[4] := RegisterAX;
    row[5] := Word(RegisterCarryFlag) + Word(RegisterZeroFlag) * $40 +
      Word(RegisterDirectionFlag) * $400;
    row[6] := GlobalWord6410;
    if (secondResult <> 0) or (RegisterAX <> 0) or
       (GlobalWord6410 <> 0) or RegisterCarryFlag or not RegisterZeroFlag then Halt(3);
    BlockWrite(outputFile, row, SizeOf(row), written);
    if written <> SizeOf(row) then Halt(4);
  end;
  Close(outputFile);
end.
"""


def compile_actual(directory):
    """Oracle: checked actual target source, isolated runtime units and compiler output."""
    target = ROOT / "targets/liero/src"
    (directory / "actual_exchange.pas").write_text(actual_program())
    compiled = subprocess.run(
        [
            "fpc",
            "-Mtp",
            "-Cr",
            f"-Fu{target}",
            f"-Fi{target}",
            "-FU.",
            "actual_exchange.pas",
        ],
        cwd=directory,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (directory / "fpc.log").write_bytes(compiled.stdout + compiled.stderr)
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    executed = subprocess.run(
        [str(directory / "actual_exchange")],
        cwd=directory,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (directory / "runtime.log").write_bytes(executed.stdout + executed.stderr)
    assert executed.returncode == 0, executed.stdout + executed.stderr
    return (directory / "PASCAL.BIN").read_bytes()


def test_actual_error_exchange_all_words_and_modeled_flags(tmp_path):
    """Oracle: actual source/runtime exhaustiveness; fails on stale AX/CF/ZF mirrors."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    data = compile_actual(tmp_path)
    assert len(data) == 65536 * 14
    for bits in range(65536):
        flags = 0x40 + (bits & 1) * 0x400
        assert struct.unpack_from("<7H", data, bits * 14) == (
            bits,
            bits,
            flags,
            0,
            0,
            flags,
            0,
        )


def original_harness():
    """Oracle: exact far-return leaf, owned DS window disjoint from code/stack/capture."""
    return """.code16
.global _start
_start:
    push %cs
    pop %ds
    push %cs
    pop %es
    cli
    push %cs
    pop %ss
    mov $0xeff0, %sp
    sti
    cld
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, handle
next_case:
    cld
    mov $0x6400, %di
    mov $32, %cx
    mov $0xa5, %al
    testw $1, counter
    jz fill
    mov $0x5a, %al
fill:
    rep stosb
    mov counter, %ax
    mov %ax, 0x6410
    not %ax
    movw $0x1357, %ss:0xeff0
    movw $0x2468, %ss:0xeff2
    mov $0x6789, %bp
    mov $0x1357, %bx
    mov $0x2468, %cx
    mov $0x369c, %dx
    mov $0x4567, %si
    mov $0x5678, %di
    cld
    testw $1, counter
    jz invoke
    std
invoke:
    stc
    mov %sp, snapshot+10
    push %cs
    call original
    mov %ax, snapshot
    pushf
    popw snapshot+4
    push %cs
    call original
    mov %ax, snapshot+2
    pushf
    popw snapshot+6
    mov %bp, snapshot+8
    mov %sp, snapshot+12
    mov %ds, snapshot+14
    mov %ss, snapshot+16
    mov %bx, snapshot+18
    mov %cx, snapshot+20
    mov %dx, snapshot+22
    mov %si, snapshot+24
    mov %di, snapshot+26
    mov %ss:0xeff0, %ax
    mov %ax, snapshot+28
    mov %ss:0xeff2, %ax
    mov %ax, snapshot+30
    cld
    mov $snapshot, %si
    mov used, %di
    add $buffer, %di
    mov $32, %cx
    rep movsb
    mov $0x6400, %si
    mov $32, %cx
    rep movsb
    addw $64, used
    cmpw $4096, used
    jne advance
    mov handle, %bx
    mov $buffer, %dx
    mov $4096, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $4096, %ax
    jne failed
    movw $0, used
advance:
    incw counter
    jnz next_case
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
original:
    .byte 0x33,0xc0,0x87,0x06,0x10,0x64,0xcb
filename: .asciz "TRACE.BIN"
handle: .word 0
counter: .word 0
used: .word 0
snapshot: .space 32
buffer: .space 4096
"""


def validate_original(trace):
    """Oracle: exhaustive global exchange and defined flags, surrounding bytes/stack/registers."""
    if len(trace) != 65536 * RECORD_BYTES:
        raise ValueError("exchange trace is incomplete")
    segment = struct.unpack_from("<H", trace, 14)[0]
    for bits in range(65536):
        record = trace[bits * RECORD_BYTES : (bits + 1) * RECORD_BYTES]
        words = struct.unpack("<16H", record[:32])
        flags = 0x44 + (bits & 1) * 0x400
        expected = (
            bits,
            0,
            words[2],
            words[3],
            0x6789,
            0xEFF0,
            0xEFF0,
            segment,
            segment,
            0x1357,
            0x2468,
            0x369C,
            0x4567,
            0x5678,
            0x1357,
            0x2468,
        )
        memory = bytearray([0x5A if bits & 1 else 0xA5] * 32)
        struct.pack_into("<H", memory, 16, 0)
        if (
            not 0x100 <= segment <= 0x9000
            or words != expected
            or any(value & 0xCC5 != flags for value in words[2:4])
            or record[32:] != memory
        ):
            raise ValueError(f"exchange state differs at input {bits}")


def test_original_vs_actual_error_exchange_all_words(tmp_path):
    """Oracle: all seven original bytes/relocations plus actual installed source, not a projection."""
    target = ROOT / "targets/liero"
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD/probe tools unavailable")
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    offset = header + (0x24DD - base) * 16 + 0x04ED
    assert binary[offset : offset + 7] == RAW
    assert not any(
        offset - 1 <= r < offset + 7 for r in _mz_relocation_locations(binary, header)
    )
    paths = (
        target / f"src/{ROUTINE}.inc",
        target / "src/LieroRuntime.pas",
        target / f"asm/{ROUTINE}.s",
        ROOT / "tools/liero_file_probe.py",
        ROOT / "engine/alternate_streams.py",
        pathlib.Path(__file__),
    )
    identities = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }
    freeze = {
        "function": ROUTINE,
        "binary_sha256": identity,
        "file_offset": offset,
        "original_bytes_hex": RAW.hex(),
        "source_hashes": identities,
        "cases": "All65536 pending words; initialAX=not(input), CF1, DF=input bit0; two calls per case.",
        "budget": "one original execution; one actual-source compilation/execution;30s subprocess limits; no model/repair/holdout",
        "preconditions": "Original DS=SS=CS is supplied; globals6400..6420, code/capture below6000 and stackeff0 are owned/disjoint; no concurrent/asynchronous cell mutation.",
        "limitations": "Complete straight-line source semantics in logical-global/register model; not native ABI, atomicity across host threads, actual caller DS/lifetime or normal reachability. PF/SF/OF original-only, AF undefined.",
    }
    (tmp_path / "freeze.json").write_text(json.dumps(freeze, indent=2) + "\n")
    (tmp_path / "sources").mkdir()
    for path in paths:
        shutil.copy2(path, tmp_path / "sources" / path.name)
    (tmp_path / "harness.S").write_text(original_harness())
    image = assemble_probe(tmp_path / "harness.S", tmp_path)
    assert len(image) + 0x100 < 0x6000
    assert image.count(RAW) == 1
    (tmp_path / "PROBE.COM").write_bytes(image)
    run_dosbox(tmp_path)
    trace = (tmp_path / "TRACE.BIN").read_bytes()
    validate_original(trace)
    actual = compile_actual(tmp_path)
    assert len(actual) == 65536 * 14
    for bits in range(65536):
        flags = struct.unpack_from("<H", trace, bits * RECORD_BYTES + 4)[0] & 0x441
        assert struct.unpack_from("<7H", actual, bits * 14) == (
            bits,
            bits,
            flags,
            0,
            0,
            flags,
            0,
        )
    for path, digest in identities.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    result = {
        "status": "exhaustive-error-word-actual-source-pass",
        "cases": 65536,
        "original_calls": 131072,
        "actual_target_source": True,
        "source_hashes": identities,
        "binary_sha256": identity,
        "static_review": "XOR establishes zero/CF0/ZF1/PF1/SF0/OF0; XCHG returns old6410 and stores0 without changing flags; RETF consumes only far return, no calls/branches.",
        "original_only": "Other registers/stack and surrounding32 bytes; PF/SF/OF, not host ABI.",
        "limitations": freeze["limitations"],
        "artifact_hashes": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in tmp_path.iterdir()
            if path.is_file()
        },
    }
    (tmp_path / "result.json").write_text(json.dumps(result, indent=2) + "\n")


@pytest.mark.parametrize("offset", [0, 2, 4, 6, 8, 12, 14, 18, 30, 32, 48, 63])
def test_original_snapshot_mutation_rejected(offset):
    """Oracle: synthetic mutation mechanism; no original execution or recovery claim."""
    records = bytearray()
    for bits in range(65536):
        flags = 0x44 + (bits & 1) * 0x400
        records.extend(
            struct.pack(
                "<16H",
                bits,
                0,
                flags,
                flags,
                0x6789,
                0xEFF0,
                0xEFF0,
                0x2000,
                0x2000,
                0x1357,
                0x2468,
                0x369C,
                0x4567,
                0x5678,
                0x1357,
                0x2468,
            )
        )
        memory = bytearray([0x5A if bits & 1 else 0xA5] * 32)
        records.extend(memory[:16] + b"\0\0" + memory[18:])
    validate_original(records)
    records[offset] ^= 0x80 if offset in (4, 6) else 1
    with pytest.raises(ValueError):
        validate_original(records)
