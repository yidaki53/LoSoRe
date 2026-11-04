"""Original cleanup port-write leaf on an owned emulated PIC; not actual sound-device parity."""

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

from engine.alternate_streams import _mz_relocation_locations
from tools import liero_four_routine_pilot as pilot
from tools.liero_file_probe import assemble_probe, run_dosbox

REGIONS = {
    "write": (
        0x135C0,
        bytes.fromhex("5589e58b16d467ec248008c075f58a46048b16d467eec9c20200"),
        (),
    ),
    "read": (
        0x135DA,
        bytes.fromhex("c80200008b16d667ec248008c074f58b16d267ec8846ff8a46ffc9c3"),
        (),
    ),
    "reset": (
        0x135F6,
        bytes.fromhex(
            "c8020000b0018b16d067ee6a019ac3019c14b0008b16d067eec646fe64e8c4ff3caa740b807efe007605fe4efeebee807efe007606c646ff01eb04c646ff008a46ffc9c3"
        ),
        (16,),
    ),
    "stop": (
        0x13A1D,
        bytes.fromhex(
            "5589e5803ecd670074076ad5e894fbeb0a6ad0e88dfb6ad3e888fba0ee678b16de67eec9c3"
        ),
        (),
    ),
    "finish": (0x138EE, bytes.fromhex("5589e5803efa67007403e8df0fe8f8fcc9cb"), ()),
    "interrupt": (
        0x148DA,
        bytes.fromhex(
            "5589e5fa8b16dc67ec0a06eb678b16dc67eea0ec6750ff36f467ff36f2679a9400cb14fbc606fa6700c9c3"
        ),
        (33,),
    ),
    "callback": (
        0x14905,
        bytes.fromhex("5589e5a1f6678b16f867a3026489160464e804f10ee8d1efc9cb"),
        (),
    ),
    "delay": (0x14B83, bytes.fromhex("5589e5b8e803f7660689d189c2b486cd15c9ca0200"), ()),
    "vector": (0x14D44, bytes.fromhex("558bec1ec556068a460ab425cd211f5dca0600"), ()),
}
CALL_SITES = {
    "callback": ((17, "near"), (21, "near")),
    "stop": ((12, "near"), (19, "near"), (24, "near")),
    "finish": ((10, "near"), (13, "near")),
    "reset": ((13, "far"), (29, "near")),
    "interrupt": ((30, "far"),),
}
CASES = tuple((status, command) for status in (0, 0x7F) for command in range(256))
BATCH = 32
RECORD_BYTES = 92


def checked_contract(root: pathlib.Path) -> dict:
    """Oracle: original bytes/relocations and signed direct calls; no hardware outcome assumptions."""
    binary, _, _ = pilot.allocator_deduction_inputs(root)
    header = int.from_bytes(binary[8:10], "little") * 16
    relocations = _mz_relocation_locations(binary, header)
    for offset, raw, expected in REGIONS.values():
        begin = header + offset
        if binary[begin : begin + len(raw)] != raw or {
            r - begin for r in relocations if begin - 1 <= r < begin + len(raw)
        } != set(expected):
            raise ValueError("cleanup dependency bytes/relocations differ")
    calls = {}
    for name, sites in CALL_SITES.items():
        module, raw, _ = REGIONS[name]
        targets = []
        for offset, kind in sites:
            if kind == "near" and raw[offset] == 0xE8:
                # All reviewed near calls stay within the135c code segment.
                ip = (
                    module
                    - 0x135C0
                    + offset
                    + 3
                    + int.from_bytes(
                        raw[offset + 1 : offset + 3], "little", signed=True
                    )
                ) & 0xFFFF
                targets.append(0x135C0 + ip)
            elif kind == "far" and raw[offset] == 0x9A:
                ip, segment = struct.unpack_from("<HH", raw, offset + 1)
                targets.append(segment * 16 + ip)
            else:
                raise ValueError("cleanup direct call opcode differs")
        calls[name] = targets
    return {
        "oracle": "original_port_leaf_ready_on_owned_dosbox_pic_vs_pascal",
        "binary_sha256": hashlib.sha256(binary).hexdigest(),
        "regions": {
            name: {
                "module_offset": off,
                "bytes_hex": raw.hex(),
                "relocations": list(rel),
            }
            for name, (off, raw, rel) in REGIONS.items()
        },
        "calls": calls,
        "write_semantics": [
            "Read port number DS67d4 each iteration; poll bit7 until clear, without a timeout.",
            "Read command low byte SS:BP+4 only after ready; high argument byte is ignored.",
            "Reload DS67d4, OUT command, LEAVE and near RET2; AH and BP preserved.",
        ],
        "fixture": [
            "Unchanged26 original leaf bytes relocated position-independently to COM2000.",
            "DS=SS=CS, SP eff0, BP2468, disjoint owned globals67c0..6800 and stack.",
            "CLI; save PIC21 mask; set ready mask00 or7f; DS67d4=0021; call original.",
            "Read PIC21 mask back after original OUT; restore saved mask/flags before DOS.",
            "512 fixed cases, every command byte under each ready mask; no busy cases.",
        ],
        "unresolved": [
            "actual sound-device status/data ports and runtime initialization/lifetime",
            "busy-to-ready device transitions, timeouts/nonreturn and interrupt/asynchronous effects",
            "reset/read loops, BIOS15 wait outcome, DOS21 vector update and callback reentry",
            "full callback/source acceptance and actual allocator-failure reachability",
        ],
        "ready_only": True,
        "actual_device_verified": False,
        "source_recovered": False,
    }


def harness(cases: tuple[tuple[int, int], ...]) -> str:
    """Oracle: owned PIC-mask roundtrip, original IN/OUT unmodified, interrupt state restored."""
    if len(cases) != BATCH or any(case not in CASES for case in cases):
        raise ValueError("unsupported port fixture batch")
    table = "\n".join(f".byte {status}, {command}" for status, command in cases)
    return f""".code16
.global _start
_start:
    pushf
    popw %cs:saved_flags
    cli
    push %cs
    pop %ds
    push %cs
    pop %ss
    mov $0xeff0, %sp
    push %cs
    pop %es
    cld
    mov $0x21, %dx
    in %dx, %al
    mov %al, saved_mask
    mov $cases, %si
    mov $record, %bx
    mov ${len(cases)}, %cx
next_case:
    push %cx
    mov $0x67c0, %di
    mov $64, %cx
    mov $0xa5, %al
    cmpb $0, (%si)
    je fill
    mov $0x5a, %al
fill:
    rep stosb
    movw $0x21, 0x67d4
    pop %cx
    xor %ax, %ax
    mov (%si), %al
    mov $0x21, %dx
    out %al, %dx
    in %dx, %al
    mov %ax, (%bx)
    mov 0x67c0, %ah
    mov 1(%si), %al
    mov %ax, 2(%bx)
    movw $0x1357, %ss:0xeff0
    movw $0x2468, %ss:0xeff2
    mov $0x2468, %bp
    push %ax
    call original
    mov %cs, 4(%bx)
    mov %ds, 6(%bx)
    mov %ss, 8(%bx)
    mov %sp, 10(%bx)
    mov %bp, 12(%bx)
    mov %ax, 14(%bx)
    mov %dx, 16(%bx)
    pushf
    popw 18(%bx)
    mov %ss:0xeff0, %ax
    mov %ax, 20(%bx)
    mov %ss:0xeff2, %ax
    mov %ax, 22(%bx)
    in %dx, %al
    xor %ah, %ah
    mov %ax, 24(%bx)
    mov 0x67d4, %ax
    mov %ax, 26(%bx)
    push %cx
    push %si
    lea 28(%bx), %di
    mov $0x67c0, %si
    mov $64, %cx
    rep movsb
    pop %si
    pop %cx
    add $2, %si
    add ${RECORD_BYTES}, %bx
    dec %cx
    jnz next_case
    mov $0x21, %dx
    mov saved_mask, %al
    out %al, %dx
    pushw saved_flags
    popf
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, %bx
    mov $record, %dx
    mov ${len(cases) * RECORD_BYTES}, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp ${len(cases) * RECORD_BYTES}, %ax
    jne failed
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21
filename: .asciz "TRACE.BIN"
saved_flags: .word 0
saved_mask: .byte 0
cases:
{table}
.org 0x1f00
original: .space 26
.org 0x2100
record: .space {len(cases) * RECORD_BYTES}
"""


def build_image(raw: bytes) -> bytes:
    """Oracle: one disjoint original-code hole; no changed I/O/branch/return instructions."""
    if (
        len(raw) != 0x2100 + BATCH * RECORD_BYTES
        or raw[0x1F00:0x1F1A] != bytes(26)
        or 0x100 + len(raw) >= 0x67C0
    ):
        raise ValueError("port original image hole/bounds differ")
    image = bytearray(raw)
    image[0x1F00:0x1F1A] = REGIONS["write"][1]
    return bytes(image)


def projection(trace: bytes, cases: list | tuple) -> bytes:
    """Oracle: all64 globals, declared registers/stack and observed PIC readback per case."""
    if len(trace) != len(cases) * RECORD_BYTES:
        raise ValueError("port trace record count differs")
    projected = bytearray()
    segment = None
    for index, (status, command) in enumerate(cases):
        record = trace[index * RECORD_BYTES : (index + 1) * RECORD_BYTES]
        words = struct.unpack("<14H", record[:28])
        seed = 0xA5 if status == 0 else 0x5A
        argument = seed * 256 + command
        cs, flags = words[2], words[9]
        segment = cs if segment is None else segment
        expected = (
            status,
            argument,
            segment,
            segment,
            segment,
            0xEFF0,
            0x2468,
            argument,
            0x21,
            flags,
            0x1357,
            0x2468,
            command,
            0x21,
        )
        memory = bytearray([seed] * 64)
        struct.pack_into("<H", memory, 0x14, 0x21)
        if (
            not 0x100 <= cs <= 0x9000
            or words != expected
            or flags & 0xEC5 != 0x44
            or record[28:] != memory
        ):
            raise ValueError("port global/register/stack/readback differs")
        projected.extend(struct.pack("<3H", command, argument, 0xEFF0))
    return bytes(projected)


def candidate_program() -> str:
    """Oracle: reviewed ready-only Pascal projection, no guessed busy/device implementation."""
    return """program PortReady;
type TRow = array[0..2] of Word;
var f: file; row: TRow; statusIndex, command: Word; status, seed, portValue: Byte;
    written: Word;
procedure WriteReady(argument: Word; status: Byte; var destination: Byte);
begin
  if (status and $80) <> 0 then Halt(3);
  destination := argument and $ff;
end;
begin
  Assign(f, 'PASCAL.BIN'); Rewrite(f, 1);
  for statusIndex := 0 to 1 do
  begin
    if statusIndex = 0 then begin status := 0; seed := $a5 end
    else begin status := $7f; seed := $5a end;
    for command := 0 to 255 do
    begin
      WriteReady(Word(seed) * 256 + command, status, portValue);
      row[0] := portValue; row[1] := Word(seed) * 256 + portValue; row[2] := $eff0;
      BlockWrite(f, row, SizeOf(row), written);
      if written <> SizeOf(row) then Halt(2);
    end;
  end;
  Close(f);
end.
"""


def freeze_method(root: pathlib.Path) -> dict:
    """Oracle: fixed512-case mechanism budget; no model, repairs or terminal generalization."""
    paths = (
        "tools/liero_cleanup_port_probe.py",
        "tools/liero_file_probe.py",
        "tools/liero_four_routine_pilot.py",
        "engine/alternate_streams.py",
        "engine/instruction_facts.py",
        "engine/routine_contract.py",
        "targets/liero/config/routine_contracts.json",
    )
    return {
        "contract": checked_contract(root),
        "cases": [list(case) for case in CASES],
        "pascal_sha256": hashlib.sha256(candidate_program().encode()).hexdigest(),
        "method_hashes": {name: pilot.digest(root / name) for name in paths},
        "budget": {
            "original_cases": 512,
            "original_batches": 16,
            "pascal_executions": 1,
            "model_requests": 0,
            "repairs": 0,
        },
        "scope": "PIC ready-path mechanism, not actual sound hardware or training/heldout trial",
    }


def run(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: original leaf/Pascal ready projection; first error ends experiment without retry."""
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "Liero BYOD unavailable"}
    freeze = freeze_method(root)
    output.mkdir(parents=True, exist_ok=False)
    pilot.save(output / "freeze.json", freeze)
    (output / "probe.pas").write_text(candidate_program())
    (output / "methods").mkdir()
    for name in freeze["method_hashes"]:
        shutil.copy2(root / name, output / "methods" / pathlib.Path(name).name)
    report = {
        "status": "failed",
        "oracle": freeze["contract"]["oracle"],
        "source_recovered": False,
        "actual_device_verified": False,
        "ready_only": True,
        "model_requests": 0,
        "unresolved": freeze["contract"]["unresolved"],
    }
    try:
        expected = bytearray()
        for index in range(0, len(CASES), BATCH):
            directory = output / f"batch-{index // BATCH}"
            directory.mkdir()
            cases = CASES[index : index + BATCH]
            (directory / "harness.S").write_text(harness(cases))
            raw = assemble_probe(directory / "harness.S", directory)
            (directory / "PROBE.COM").write_bytes(build_image(raw))
            run_dosbox(directory)
            expected.extend(projection((directory / "TRACE.BIN").read_bytes(), cases))
        for name, command in (
            ("compile.log", ["fpc", "-Mtp", "-Cr", "probe.pas"]),
            ("execution.log", [str((output / "probe").resolve())]),
        ):
            result = subprocess.run(
                command, cwd=output, capture_output=True, timeout=30, check=False
            )
            (output / name).write_bytes(result.stdout + result.stderr)
            result.check_returncode()
        if (output / "PASCAL.BIN").read_bytes() != expected:
            raise ValueError("port original/Pascal projection differs")
        if (
            freeze_method(root) != freeze
            or json.loads((output / "freeze.json").read_text()) != freeze
            or (output / "probe.pas").read_text() != candidate_program()
        ):
            raise ValueError("port frozen method/source changed")
        report.update(status="passed", cases=len(CASES))
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        report.update(
            error=f"{type(exc).__name__}: {exc}", stop_reason="first-error-no-retry"
        )
    report["freeze_sha256"] = pilot.digest(output / "freeze.json")
    report["artifact_hashes"] = {
        str(p.relative_to(output)): pilot.digest(p)
        for p in output.rglob("*")
        if p.is_file()
    }
    pilot.save(output / "result.json", report)
    return report


def validate_report(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: saved original images, whole traces and frozen Pascal; not execution attestation."""
    freeze = freeze_method(root)
    report = json.loads((output / "result.json").read_text())
    if (
        json.loads((output / "freeze.json").read_text()) != freeze
        or report["freeze_sha256"] != pilot.digest(output / "freeze.json")
        or report["status"] != "passed"
        or report["cases"] != len(CASES)
        or report["oracle"] != freeze["contract"]["oracle"]
        or report["unresolved"] != freeze["contract"]["unresolved"]
        or report["source_recovered"] is not False
        or report["actual_device_verified"] is not False
        or report["ready_only"] is not True
        or report["model_requests"] != 0
        or (output / "probe.pas").read_text() != candidate_program()
    ):
        raise ValueError("port report/source/premises invalid")
    required = {
        "freeze.json",
        "probe.pas",
        "probe",
        "PASCAL.BIN",
        "compile.log",
        "execution.log",
    }
    expected = bytearray()
    for index in range(0, len(CASES), BATCH):
        prefix = f"batch-{index // BATCH}"
        directory = output / prefix
        cases = CASES[index : index + BATCH]
        required.update(
            f"{prefix}/{name}"
            for name in ("harness.S", "harness.bin", "PROBE.COM", "TRACE.BIN")
        )
        if (directory / "harness.S").read_text() != harness(cases) or (
            directory / "PROBE.COM"
        ).read_bytes() != build_image((directory / "harness.bin").read_bytes()):
            raise ValueError("port saved original harness/image differs")
        expected.extend(projection((directory / "TRACE.BIN").read_bytes(), cases))
    if (output / "PASCAL.BIN").read_bytes() != expected:
        raise ValueError("port saved Pascal/original differs")
    for name, identity in freeze["method_hashes"].items():
        path = f"methods/{pathlib.Path(name).name}"
        required.add(path)
        if pilot.digest(output / path) != identity:
            raise ValueError("port saved method differs")
    if not required <= report["artifact_hashes"].keys():
        raise ValueError("port required hashes missing")
    for name, identity in report["artifact_hashes"].items():
        path = (output / name).resolve()
        if not path.is_relative_to(output.resolve()) or pilot.digest(path) != identity:
            raise ValueError("port artifact changed")
    return report


def main() -> int:
    """Oracle: explicit pass/failure/skip; replay performs no guest/model execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    result = validate_report(ROOT, output) if args.replay else run(ROOT, output)
    print(
        json.dumps(
            {key: value for key, value in result.items() if key != "artifact_hashes"},
            indent=2,
        )
    )
    return int(result["status"] == "failed")


if __name__ == "__main__":
    raise SystemExit(main())
