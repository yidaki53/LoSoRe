import hashlib
import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.routine_contract import load_contract
from tools import liero_four_routine_pilot as pilot
from tools.liero_file_probe import assemble_probe, run_dosbox

RAW = bytes.fromhex(
    "5589e5804e0a0074318b5e0c8b4e0e83f9007c2681f99d007f2083fb007c1b"
    "81fb9d007f15c47e06c1e30601dfc1e30201df01cf8a460a268805c9ca0a00"
)
ARENA_SIZE = 65536 + 16
RECORD_SIZE = 16 + ARENA_SIZE


def draw_sketch(guard_style="early_exit"):
    """Oracle: developer-supplied topology control, not a model recovery."""
    return {
        "guard_style": guard_style,
        "skip_zero": True,
        "stride": 320,
        "coordinate_order": "row_column",
        "maximum_coordinate": 157,
    }


@pytest.mark.parametrize("position", range(len(RAW)))
def test_draw_sketch_rejects_changed_original_bytes(position):
    """Oracle: every instruction/operand byte is required, not a listing guess."""
    mutated = bytearray(RAW)
    mutated[position] ^= 1
    with pytest.raises(ValueError, match="original-byte"):
        pilot.render_draw_sketch(draw_sketch(), bytes(mutated))


@pytest.mark.parametrize(
    "change",
    [
        {"guard_style": "begin Halt(1) end"},
        {"skip_zero": False},
        {"skip_zero": 1},
        {"stride": 158},
        {"stride": True},
        {"coordinate_order": "column_row"},
        {"maximum_coordinate": 158},
        {"source": "Pointer(param_1)^ := 0;"},
    ],
)
def test_draw_sketch_rejects_unsafe_or_conflicting_proposals(change):
    """Oracle: incompatible semantics/text never silently repaired into safe code."""
    proposal = draw_sketch()
    proposal.update(change)
    with pytest.raises(ValueError):
        pilot.render_draw_sketch(proposal, RAW)


@pytest.mark.parametrize("proposal", [None, [], {}, {"guard_style": "early_exit"}])
def test_draw_sketch_rejects_incomplete_proposals(proposal):
    """Oracle: no missing-field defaults or empty proposal pass."""
    with pytest.raises(ValueError):
        pilot.render_draw_sketch(proposal, RAW)


def test_draw_execution_gate_rejects_any_nonrendered_source():
    """Oracle: only exact closed-renderer output executes; no sanitizing arbitrary Pascal."""
    proposal = draw_sketch()
    source = pilot.render_draw_sketch(proposal, RAW)
    pilot.validate_draw_candidate(source, proposal, RAW)
    for changed in (
        source.replace("Byte(param_2)", "param_2"),
        source.replace("RealModeMemory[pixelAddress]", "Pointer(pixelAddress)^"),
        source + "\nprocedure Extra; begin end;\n",
        source.replace("Longint(param_3)", "param_3"),
    ):
        with pytest.raises(ValueError, match="rendered"):
            pilot.validate_draw_candidate(changed, proposal, RAW)


@pytest.mark.parametrize("guard_style", ["early_exit", "nested"])
def test_typed_draw_compiles_and_matches_projection(tmp_path, guard_style):
    """Oracle: renderer regression against independent memory expectations, not original recovery."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    proposal = draw_sketch(guard_style)
    source = pilot.render_draw_sketch(proposal, RAW)
    pilot.validate_draw_candidate(source, proposal, RAW)
    (tmp_path / "FUN_1ec2_0dc8.inc").write_text(source)
    shutil.copy2(root / "targets/liero/src/LieroRuntime.pas", tmp_path)
    (tmp_path / "actual_draw.pas").write_text(PASCAL)
    inputs = draw_cases()
    (tmp_path / "CASES.BIN").write_bytes(
        b"".join(struct.pack("<5H", *(v & 65535 for v in case)) for case in inputs)
    )
    compiled = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-FU.", "actual_draw.pas"],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    executed = subprocess.run(
        [str(tmp_path / "actual_draw")],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert executed.returncode == 0, executed.stdout + executed.stderr
    output = (tmp_path / "PASCAL.BIN").read_bytes()
    assert len(output) == len(inputs) * ARENA_SIZE
    for index, case in enumerate(inputs):
        assert output[index * ARENA_SIZE : (index + 1) * ARENA_SIZE] == expected_arena(
            case, index, segmented=False
        )


def draw_cases():
    """Oracle: frozen grids, signed bounds/colors, and one excluded offset-wrap control."""
    cases = [(offset, 1, 0, 0, 1) for offset in (0, 256, 15138)]
    coordinates = [
        (-32768, 0),
        (-1, 0),
        (0, -32768),
        (0, -1),
        (0, 0),
        (157, 157),
        (158, 0),
        (0, 158),
        (32767, 0),
        (0, 32767),
    ]
    cases += [
        (256, color, row, column, 0)
        for row, column in coordinates
        for color in (0, 1, 127, 128, 255)
    ]
    cases.append((15139, 255, 157, 157, 0))
    return cases


def expected_arena(case, index, *, segmented):
    """Oracle: complete arena expectation, not generated-source acceptance."""
    offset, color, row, column, grid = case
    expected = bytearray([0xA5 if index % 2 == 0 else 0x5A]) * ARENA_SIZE
    points = (
        ((y, x, ((y + x) & 127) + 1) for y in range(158) for x in range(158))
        if grid
        else [(row, column, color)]
    )
    for y, x, value in points:
        if value and 0 <= y <= 157 and 0 <= x <= 157:
            address = offset + y * 320 + x
            if segmented:
                address &= 65535
            expected[address] = value
    return expected


PASCAL = """program ActualDraw;
uses LieroRuntime;
{$I FUN_1ec2_0dc8.inc}
var inputFile, outputFile: file;
    args: array[0..4] of Word;
    stage, index, row, column, signedRow, signedColumn: Integer;
    count: LongInt;
begin
  if SizeOf(Integer) <> 2 then Halt(1);
  Assign(inputFile, 'CASES.BIN'); Reset(inputFile, 1);
  Assign(outputFile, 'PASCAL.BIN'); Rewrite(outputFile, 1);
  stage := 0;
  while not Eof(inputFile) do
  begin
    BlockRead(inputFile, args, 10, count);
    if count <> 10 then Halt(2);
    if stage mod 2 = 0 then FillChar(RealModeMemory, SizeOf(RealModeMemory), $A5)
    else FillChar(RealModeMemory, SizeOf(RealModeMemory), $5A);
    if args[4] <> 0 then
      for row := 0 to 157 do
        for column := 0 to 157 do
          FUN_1ec2_0dc8($30000 + LongInt(args[0]),
            Chr(((row + column) and 127) + 1), row, column)
    else
    begin
      if args[2] < 32768 then signedRow := args[2]
      else signedRow := LongInt(args[2]) - 65536;
      if args[3] < 32768 then signedColumn := args[3]
      else signedColumn := LongInt(args[3]) - 65536;
      FUN_1ec2_0dc8($30000 + LongInt(args[0]), Chr(args[1]),
        signedRow, signedColumn);
    end;
    BlockWrite(outputFile, RealModeMemory[$30000], 65552, count);
    if count <> 65552 then Halt(3);
    Inc(stage);
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
    mov $0x1001, %bx
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
    mov $0xa5a5, %ax
    testw $1, stage
    jz clear_arena
    mov $0x5a5a, %ax
clear_arena:
    cld
    mov $32768, %cx
    rep stosw
    mov arena_segment, %dx
    add $0x1000, %dx
    mov %dx, %es
    mov $8, %cx
    rep stosw
    mov stage, %si
    imul $10, %si
    add $cases, %si
    movw $0, row
    movw $0, column
invoke:
    mov $0x1234, %bp
    mov %sp, before_sp
    mov 6(%si), %ax
    cmpw $0, 8(%si)
    je push_column
    mov column, %ax
push_column:
    push %ax
    mov 4(%si), %ax
    cmpw $0, 8(%si)
    je push_row
    mov row, %ax
push_row:
    push %ax
    mov 2(%si), %ax
    cmpw $0, 8(%si)
    je push_color
    mov row, %ax
    add column, %ax
    and $127, %ax
    inc %ax
push_color:
    or $0x5a00, %ax
    push %ax
    pushw arena_segment
    pushw (%si)
    std
    push %cs
    call original
    pushf
    pop %dx
    mov %bp, metadata+2
    mov %sp, metadata+6
    and $0x400, %dx
    mov %dx, metadata+8
    mov %ds, metadata+10
    mov %ss, metadata+12
    mov %cs, metadata+14
    cld
    cmpw $0, 8(%si)
    je snapshot
    incw column
    cmpw $158, column
    jne invoke
    movw $0, column
    incw row
    cmpw $158, row
    jne invoke
snapshot:
    mov stage, %ax
    mov %ax, metadata
    mov before_sp, %ax
    mov %ax, metadata+4
    mov $metadata, %dx
    mov $16, %cx
    call write
    mov arena_segment, %ax
    mov %ax, %ds
    xor %dx, %dx
    mov $0xff00, %cx
    call write
    mov $0xff00, %dx
    mov $256, %cx
    call write
    push %cs
    pop %ds
    mov arena_segment, %ax
    add $0x1000, %ax
    mov %ax, %ds
    xor %dx, %dx
    mov $16, %cx
    call write
    push %cs
    pop %ds
    incw stage
    cmpw $CASE_COUNT, stage
    jne next_case
    mov handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
write:
    mov %cs:handle, %bx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp %cx, %ax
    jne failed
    ret
failed:
    mov $0x4c01, %ax
    int $0x21
handle: .word 0
arena_segment: .word 0
before_sp: .word 0
stage: .word 0
row: .word 0
column: .word 0
metadata: .space 16
filename: .asciz "TRACE.BIN"
cases: .incbin "CASES.BIN"
original: .incbin "original.bin"
"""


def test_actual_draw_source_and_original_offset_wrap(tmp_path):
    """Oracle: original62-byte paths, scoped actual-source memory, excluded wrap counterexample."""
    root = pathlib.Path(__file__).resolve().parents[1]
    target = root / "targets/liero"
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD/probe tools unavailable")
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    offset = header + (0x1EC2 - base) * 16 + 0x0DC8
    assert offset == 69976
    assert binary[offset : offset + 62] == RAW
    assert not any(
        offset - 1 <= location < offset + 62
        for location in _mz_relocation_locations(binary, header)
    )
    assert {i: i + 2 + RAW[i + 1] for i in (7, 18, 24, 29, 35)} == {
        7: 58,
        18: 58,
        24: 58,
        29: 58,
        35: 58,
    }
    contract = load_contract(target, "FUN_1ec2_0dc8")
    assert contract["reviewed_bytes_hex"] == RAW.hex()
    assert contract["binary_sha256"] == identity
    assert contract["file_offset"] == offset
    assert contract["scope"] == "nonwrapping-linear-memory-effects-only"
    inputs = draw_cases()
    source_files = [
        target / "src/FUN_1ec2_0dc8.inc",
        target / "src/LieroRuntime.pas",
        target / "config/routine_contracts.json",
        pathlib.Path(__file__),
        root / "tools/liero_file_probe.py",
        root / "engine/alternate_streams.py",
        target / "alternate_streams.json",
    ]
    hashes = {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in source_files
    }
    freeze = {
        "function": "FUN_1ec2_0dc8",
        "binary_sha256": identity,
        "source_hashes": hashes,
        "cases": inputs,
        "budget": "one original execution; one actual-source compilation/execution; 30s each; no model/repair",
        "scope": contract["scope"],
        "premises": "DOS AH48 allocates65552 writable bytes outside retained COM code/DS/SS64K. Valid nonaliasing frame/arguments; no asynchronous mutation.",
        "limitations": "Source models linear addresses, not far-offset wrap or CPU/stack-write ABI. Caller buffer provenance and normal-program reachability unknown.",
    }
    (tmp_path / "freeze.json").write_text(json.dumps(freeze, indent=2) + "\n")
    sources = tmp_path / "sources"
    sources.mkdir()
    for path in source_files:
        shutil.copy2(path, sources / path.name)
    (tmp_path / "original.bin").write_bytes(RAW)
    (tmp_path / "CASES.BIN").write_bytes(
        b"".join(
            struct.pack("<5H", *(value & 65535 for value in case)) for case in inputs
        )
    )
    assembly = tmp_path / "harness.S"
    assembly.write_text(
        ASSEMBLY.replace("CASE_COUNT", str(len(inputs))).replace(
            '.incbin "', f'.incbin "{tmp_path}/'
        )
    )
    image = assemble_probe(assembly, tmp_path)
    assert len(image) < 0xF000
    (tmp_path / "PROBE.COM").write_bytes(image)
    run_dosbox(tmp_path)
    program = tmp_path / "actual_draw.pas"
    program.write_text(PASCAL)
    compiled = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fusources", "-Fisources", "-FU.", program.name],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (tmp_path / "fpc.log").write_bytes(compiled.stdout + compiled.stderr)
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    executed = subprocess.run(
        [str(tmp_path / "actual_draw")],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (tmp_path / "runtime.log").write_bytes(executed.stdout + executed.stderr)
    assert executed.returncode == 0, executed.stdout + executed.stderr
    trace = (tmp_path / "TRACE.BIN").read_bytes()
    pascal = (tmp_path / "PASCAL.BIN").read_bytes()
    assert len(trace) == len(inputs) * RECORD_SIZE
    assert len(pascal) == len(inputs) * ARENA_SIZE
    for index, case in enumerate(inputs):
        stage, bp, before, after, df, ds, ss, cs = struct.unpack_from(
            "<8H", trace, index * RECORD_SIZE
        )
        assert stage == index and bp == 0x1234
        assert before == after == 0xFFFE and df == 0x400 and ds == ss == cs
        original = trace[index * RECORD_SIZE + 16 : (index + 1) * RECORD_SIZE]
        actual = pascal[index * ARENA_SIZE : (index + 1) * ARENA_SIZE]
        assert original == expected_arena(case, index, segmented=True), index
        assert actual == expected_arena(case, index, segmented=False), index
        if index < len(inputs) - 1:
            assert actual == original, index
        else:
            assert actual != original
            assert original[0] == actual[65536] == 255
            assert original[65536] == actual[0] != 255
    for relative, expected_hash in hashes.items():
        assert (
            hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected_hash
        )
    result = {
        "status": "scoped-pass-with-excluded-offset-wrap-counterexample",
        "scoped_cases": len(inputs) - 1,
        "grid_writes": 3 * 158 * 158,
        "scoped_arena_bytes_checked": (len(inputs) - 1) * ARENA_SIZE,
        "offset_wrap_counterexamples": 1,
        "source_recovered": False,
        "source_hashes": hashes,
        "limitations": freeze["limitations"],
        "artifact_hashes": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in tmp_path.iterdir()
            if path.is_file()
        },
    }
    (tmp_path / "result.json").write_text(json.dumps(result, indent=2) + "\n")
