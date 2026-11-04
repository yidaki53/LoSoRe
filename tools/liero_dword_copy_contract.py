"""Developer-authored exact dword-copy contract and finite original/Pascal check."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import struct
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from tools.liero_file_probe import run_dosbox
from tools.liero_four_routine_pilot import save

ROUTINE = "FUN_1ec2_0000"
SEEDS = (0xA5, 0x5A, 0xFF)


def digest(data: bytes) -> str:
    """Oracle: immutable source/input/trace identity."""
    return hashlib.sha256(data).hexdigest()


def dword_copy_contract(raw: bytes) -> dict:
    """Oracle: exact complete x86 leaf shape, not historical source/ABI acceptance."""
    if raw != bytes.fromhex("5589e51ec5760cc47e088b4e06c1e90266f3a51fc9ca0a00"):
        raise ValueError("unsupported exact dword-copy shape")
    return {
        "oracle": "exact_dword_copy_shape_under_scoped_far_call_preconditions",
        "routine_bytes_hex": raw.hex(),
        "routine_sha256": digest(raw),
        "entry_sp_slots": {
            "source_far_pointer": 10,
            "destination_far_pointer": 6,
            "count_word": 4,
        },
        "frame_bp_slots": {
            "source_far_pointer": 12,
            "destination_far_pointer": 8,
            "count_word": 6,
        },
        "copy_bytes": "4 * (unsigned_count_word // 4)",
        "unwritten_tail_bytes": "unsigned_count_word % 4",
        "direction": "forward only under entry DF=0; routine does not clear DF",
        "far_return_cleanup_bytes": 10,
        "minimum_cpu": "80386 (66h MOVSD operand override)",
        "support_offsets": [0, 1, 3, 4, 7, 10, 13, 16, 19, 20, 21],
        "preconditions": [
            "Entry DF=0; source and destination pointers address readable/writable nonwrapping ranges of 4*(count//4) bytes.",
            "Source and destination are disjoint; no memmove or aliasing semantics are certified.",
            "Caller stack including saved BP/DS, return address and arguments is valid, writable and disjoint from both buffers and code.",
            "Entry SP is at least 4; far return plus ten-byte cleanup does not wrap SP.",
            "Original callee is entered at its first instruction on an 80386-or-later real-mode CPU.",
        ],
        "limitations": [
            "Static contract and finite memory execution are separate; no ordinary caller provenance is established.",
            "Entry DF=1, overlapping pointers, wrapping ranges, interrupts and external mutations remain outside scope.",
            "Historical manual Pascal body exists but is not read/used; projection below is developer-authored from this contract.",
            "No full register/flag/host ABI translation, source attestation or training promotion.",
        ],
        "routine_recovered": False,
    }


def checked_contract(root: pathlib.Path) -> tuple[bytes, dict]:
    """Oracle: actual original bytes, explicit mapping and absence of overlapping relocations."""
    target = root / "targets/liero"
    manifest_path = target / "alternate_streams.json"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads(manifest_path.read_text())
    )
    if header != int.from_bytes(binary[8:10], "little") * 16:
        raise ValueError("mapping disagrees with MZ header")
    offset = header + (0x1EC2 - base) * 16
    if not header <= offset < offset + 24 <= len(binary):
        raise ValueError("copy routine outside file-backed image")
    if any(
        offset - 1 <= location < offset + 24
        for location in _mz_relocation_locations(binary, header)
    ):
        raise ValueError("relocation overlaps copy routine")
    raw = binary[offset : offset + 24]
    contract = dword_copy_contract(raw)
    contract.update(
        {"function": ROUTINE, "binary_sha256": identity, "file_offset": offset}
    )
    return raw, contract


def cases() -> list[tuple[int, int, bytes]]:
    """Oracle: fixed known-slice development corpus, no heldout or adaptive selection."""
    result = []
    for seed in SEEDS:
        for count in range(258):
            source = bytes((index * 37 + seed + count) & 255 for index in range(256))
            arena = (
                source
                + bytes([seed ^ 0xFF] * 16)
                + bytes([seed] * 256)
                + bytes([seed ^ 0x55] * 16)
            )
            result.append((seed, count, arena))
    return result


def compare_outputs(
    original: bytes, pascal: bytes, inputs: list[tuple[int, int, bytes]]
) -> dict:
    """Oracle: all source/destination/guard bytes and separately original-only SP/DS checks."""
    if inputs != cases():
        raise ValueError("dword-copy input corpus differs from frozen cases")
    if len(original) != len(inputs) * 552 or len(pascal) != len(inputs) * 544:
        raise ValueError("dword-copy output shape mismatch")
    for index, (_, count, arena) in enumerate(inputs):
        record = original[index * 552 : (index + 1) * 552]
        before, after, ds_before, ds_after = struct.unpack("<4H", record[544:])
        if before != 0xFFFE or after != before or ds_before != ds_after:
            raise ValueError(
                f"original-only stack/DS observation failed at case {index}"
            )
        copied = 4 * (count // 4)
        expected = bytearray(arena)
        expected[272 : 272 + copied] = arena[:copied]
        if (
            record[:544] != expected
            or pascal[index * 544 : (index + 1) * 544] != expected
        ):
            raise ValueError(
                f"full-arena original/Pascal memory mismatch at case {index}"
            )
    return {
        "status": "scoped-memory-pass",
        "cases": len(inputs),
        "bytes_checked": len(inputs) * 544,
        "per_case_arena_bytes": 544,
        "original_only_sp_balanced": True,
        "original_only_ds_preserved": True,
        "routine_recovered": False,
        "oracle": "finite_original_com_vs_developer_pascal_memory_projection",
    }


def harness_source() -> str:
    """Oracle: isolated COM harness with disjoint valid near-end stack and fixed arena."""
    return """
.code16
.global _start
_start:
    push %cs
    pop %ds
    cld
    mov $input_name, %dx
    mov $0x3d00, %ax
    int $0x21
    jc failed
    mov %ax, input_handle
    mov $output_name, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, output_handle
next_case:
    mov input_handle, %bx
    mov $case_count, %dx
    mov $546, %cx
    mov $0x3f00, %ax
    int $0x21
    jc failed
    test %ax, %ax
    jz done
    cmp $546, %ax
    jne failed
    mov %sp, stack_before
    mov %ds, ds_before
    cld
    push %ds
    push $arena
    push %ds
    push $arena+272
    push case_count
    push %cs
    call original
    mov %sp, stack_after
    mov %ds, ds_after
    mov output_handle, %bx
    mov $arena, %dx
    mov $552, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $552, %ax
    jne failed
    jmp next_case
done:
    mov output_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov input_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21
original:
.incbin "original.bin"
input_name: .asciz "CASES.BIN"
output_name: .asciz "TRACE.BIN"
input_handle: .word 0
output_handle: .word 0
case_count: .word 0
arena: .space 544
stack_before: .word 0
stack_after: .word 0
ds_before: .word 0
ds_after: .word 0
"""


PASCAL_SOURCE = """program DwordCopyProjection;
type TArena = array[0..543] of Byte;
var arena: TArena; count: Word; i, copied, got, written: LongInt;
    inputFile, outputFile: file;
begin
  Assign(inputFile, 'CASES.BIN'); Reset(inputFile, 1);
  Assign(outputFile, 'PASCAL.BIN'); Rewrite(outputFile, 1);
  while not Eof(inputFile) do
  begin
    BlockRead(inputFile, count, 2, got);
    if got <> 2 then Halt(1);
    BlockRead(inputFile, arena, 544, got);
    if got <> 544 then Halt(1);
    copied := (LongInt(count) div 4) * 4;
    if copied > 256 then Halt(1);
    if copied > 0 then
      for i := 0 to copied - 1 do arena[272 + i] := arena[i];
    BlockWrite(outputFile, arena, 544, written);
    if written <> 544 then Halt(1);
  end;
  Close(inputFile); Close(outputFile);
end.
"""


def run_contract_probe(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: one frozen finite execution, persistent failures and no promotion/retries."""
    raw, contract = checked_contract(root)
    missing = [
        tool for tool in ("as", "ld", "dosbox", "fpc") if shutil.which(tool) is None
    ]
    if missing:
        raise FileNotFoundError("copy probe tools unavailable: " + ", ".join(missing))
    output.mkdir(parents=True, exist_ok=False)
    inputs = cases()
    payload = b"".join(struct.pack("<H", count) + arena for _, count, arena in inputs)
    method_paths = (
        root / "tools/liero_dword_copy_contract.py",
        root / "tools/liero_file_probe.py",
        root / "engine/alternate_streams.py",
        root / "tools/liero_four_routine_pilot.py",
        root / "targets/liero/alternate_streams.json",
    )
    freeze = {
        "contract": contract,
        "counts": [0, 257],
        "seeds": list(SEEDS),
        "cases": len(inputs),
        "case_bytes_sha256": digest(payload),
        "pascal_sha256": digest(PASCAL_SOURCE.encode()),
        "harness_sha256": digest(harness_source().encode()),
        "method_hashes": {
            str(path.relative_to(root)): digest(path.read_bytes())
            for path in method_paths
        },
        "budget": "one DOSBox execution and one host-Pascal execution; 30s subprocess limits; no retries/holdout/model",
        "disclosure": "Developer-authored known-manual-slice contract/projection; no manual source read or learned recovery.",
    }
    save(output / "freeze.json", freeze)
    (output / "methods").mkdir()
    for path in method_paths:
        shutil.copy2(path, output / "methods" / path.name)
    (output / "original.bin").write_bytes(raw)
    (output / "CASES.BIN").write_bytes(payload)
    (output / "projection.pas").write_text(PASCAL_SOURCE)
    (output / "harness.S").write_text(harness_source())
    try:
        # GNU as resolves .incbin relative to its process working directory.
        completed = subprocess.run(
            ["as", "--32", "-o", "probe.o", "harness.S"],
            cwd=output,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (output / "assembler.log").write_bytes(completed.stdout + completed.stderr)
        completed.check_returncode()
        completed = subprocess.run(
            [
                "ld",
                "-m",
                "elf_i386",
                "-Ttext",
                "0x100",
                "--oformat",
                "binary",
                "-o",
                "PROBE.COM",
                "probe.o",
            ],
            cwd=output,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (output / "linker.log").write_bytes(completed.stdout + completed.stderr)
        completed.check_returncode()
        run_dosbox(output)
        compiled = subprocess.run(
            ["fpc", "-Mtp", "-Cr", "projection.pas"],
            cwd=output,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (output / "fpc.log").write_bytes(compiled.stdout + compiled.stderr)
        compiled.check_returncode()
        executed = subprocess.run(
            [str(output / "projection")],
            cwd=output,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (output / "pascal.log").write_bytes(executed.stdout + executed.stderr)
        executed.check_returncode()
        result = compare_outputs(
            (output / "TRACE.BIN").read_bytes(),
            (output / "PASCAL.BIN").read_bytes(),
            inputs,
        )
        for relative, expected in freeze["method_hashes"].items():
            if digest((root / relative).read_bytes()) != expected:
                raise ValueError("frozen method/input changed")
        if digest((output / "CASES.BIN").read_bytes()) != freeze["case_bytes_sha256"]:
            raise ValueError("frozen corpus changed")
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        save(
            output / "failure.json",
            {
                "status": "failed",
                "error": str(error),
                "error_type": type(error).__name__,
                "retry_allowed": False,
            },
        )
        raise
    result["freeze_sha256"] = digest((output / "freeze.json").read_bytes())
    result["artifact_hashes"] = {
        path.name: digest(path.read_bytes())
        for path in output.iterdir()
        if path.is_file()
    }
    result["limitations"] = contract["limitations"]
    result["source_promoted"] = False
    save(output / "result.json", result)
    return result


def main() -> None:
    """Oracle: fresh-directory explicit finite experiment, no target mutation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    if not (args.root / "extracted/liero/LIERO.EXE").is_file():
        print(json.dumps({"status": "skipped", "reason": "Liero BYOD unavailable"}))
        return
    print(
        json.dumps(
            run_contract_probe(args.root.resolve(), args.output.resolve()), indent=2
        )
    )


if __name__ == "__main__":
    main()
