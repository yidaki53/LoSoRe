"""Bounded source/structured trials and scoped evidence exports for supported Liero leaves.

Oracle: unchanged original instructions, actual Pascal/runtime and complete
manual review are distinct gates. This runner never installs or promotes source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import re
import shutil
import struct
import subprocess
import urllib.error
from collections.abc import Callable

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.evidence_archive import read_archive, seal_archive
from engine.routine_contract import pascal_declaration
from tools import liero_four_routine_pilot as pilot
from tools.liero_file_probe import assemble_probe, run_dosbox

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARENA = 4096
CASE_BYTES = 8 + ARENA
RECORD_BYTES = 32 + ARENA
PANEL = {
    "FUN_24dd_40d6": {
        "offset": 0x40D6,
        "bytes": "fc8bdc36c47f06368b4704abb90f0033c0f3abca0200",
        "signature": "procedure FUN_24dd_40d6(param_1: Word; param_2: Pointer);",
        "arguments": 6,
        "cleanup": 2,
    },
    "FUN_24dd_3d68": {
        "offset": 0x3D68,
        "bytes": "8bdc8cda36c5770a36c47f06368b4f04fcf3a48edaca0a00",
        "signature": (
            "procedure FUN_24dd_3d68(param_1: Integer; param_2, param_3: Pointer);"
        ),
        "arguments": 10,
        "cleanup": 10,
    },
    "FUN_24dd_48e1": {
        "offset": 0x48E1,
        "bytes": "8bdc8cda36c5770a36c47f06368b4f04fc3bf7730703f103f94e4ffdf3a4fc8edaca0a00",
        "signature": "procedure FUN_24dd_48e1(param_1: Integer; param_2, param_3: Pointer);",
        "arguments": 10,
        "cleanup": 10,
    },
}
DEFAULT_PANEL = ("FUN_24dd_40d6", "FUN_24dd_3d68")
DISCOVERY_PANEL = {
    "FUN_24dd_455e": {
        "offset": 0x455E,
        "bytes": "8bd80bda74358aee0bd27907f7daf7d883da008bd8b8a0000bd2750c87d3b0900af6750486f2b0880bd27808fec803db13d279f80aed780380e67fc3",
        "signature": "procedure FUN_24dd_455e;",
        "arguments": 0,
        "cleanup": 0,
        "near": True,
    },
    "FUN_249c_0013": {
        "segment": 0x249C,
        "offset": 0x0013,
        "bytes": "5589e58b7e04368a85fcfe30e48bd0368a85fbfe30e4c1e00403c2368885fdfec9c20200",
        "signature": "procedure FUN_249c_0013(param_1: Word; param_2: Pointer);",
        "arguments": 2,
        "cleanup": 2,
        "near": True,
    },
    "FUN_24dd_4141": {
        "offset": 0x4141,
        "bytes": "fc8bdc8cda36c5770a36c47f06368b5f048acf32ed03f18acbf3a48edaca0a00",
        "signature": "procedure FUN_24dd_4141(param_1: Word; param_2, param_3: Pointer);",
        "arguments": 10,
        "cleanup": 10,
    },
}


def routine_spec(routine: str) -> dict:
    """Oracle: explicitly supported byte-bound trial specs; default legacy panel unchanged."""
    if routine in PANEL:
        return PANEL[routine]
    return DISCOVERY_PANEL[routine]


SCOPE = (
    "Sequential logical host-pointer/register model. Original DS=ES=SS=CS is "
    "supplied; arena [8000,9000), code/capture below6000, stack nearEFF0 "
    "are writable, owned and disjoint. Parameters designate valid arena ranges "
    "without 16-bit offset wrap; copy ranges may overlap, including identical "
    "pointers. No asynchronous mutation. Native host ABI, arbitrary segment "
    "aliases/wrap, real caller provenance and normal reachability are not accepted."
)
CALIBRATION = {
    "CalibrateMask": {
        "body": """procedure CalibrateMask(value: Word; target: Pointer);
var p: PByte; old: Byte;
begin
  p := PByte(target); old := p^;
  p^ := old xor (value and $ff);
end;""",
        "effects": (
            "RegisterAX becomes old (zero extended); RegisterBX becomes entry "
            "RegisterSP; RegisterSP increases by6 modulo65536; RegisterCarryFlag "
            "becomes False; RegisterZeroFlag becomes (written byte =0). "
            "All other mirrors, including RegisterDirectionFlag, are preserved."
        ),
    },
    "CalibratePair": {
        "body": """procedure CalibratePair(value: Word; target: Pointer);
var p: PByte; old: Byte;
begin
  p := PByte(target); old := p^;
  p^ := value shr 8;
  Inc(p); p^ := old xor (value and $ff);
end;""",
        "effects": (
            "RegisterAX becomes old (zero extended); RegisterBX becomes entry "
            "RegisterSP; RegisterSP increases by6 modulo65536; RegisterDI "
            "increases by2 modulo65536; RegisterCX becomes0; "
            "RegisterDirectionFlag becomes False. All other mirrors, including "
            "RegisterCarryFlag and RegisterZeroFlag, are preserved."
        ),
    },
}


def calibration_prompt(name: str) -> str:
    """Oracle: supplied known-source body plus explicit adapter contract, not recovery."""
    spec = CALIBRATION[name]
    return f"""Return JSON with only a source field containing this entire Pascal
procedure with the following logical register effects added. This is a disclosed
known-source adapter calibration, not decompilation. Preserve the memory behavior
of the supplied body exactly. Use target as the host pointer; do not address
memory through numeric register mirrors, segments or a DOS stack.
Available from LieroRuntime: PByte, Word, LongInt; numeric Word mirrors:
RegisterAX, RegisterBX, RegisterCX, RegisterDX, RegisterSI, RegisterDI,
RegisterSP, RegisterBP, RegisterDS, RegisterES, RegisterSS; Boolean mirrors:
RegisterCarryFlag, RegisterZeroFlag, RegisterDirectionFlag.
{spec["effects"]}
SP/DI can initially be65535: use LongInt widening and bitmask $ffff.
No helpers, assembler, services, directives or additional globals.
Supplied body:
{spec["body"]}
"""


def calibration_program(name: str) -> str:
    """Oracle: exhaustive scalar inputs, complete dirty arena and actual runtime mirrors."""
    if name not in CALIBRATION:
        raise ValueError("unknown calibration task")
    return f"""program CalibrationProbe;
uses LieroRuntime;
{{$I candidate.inc}}
var bits: LongInt; j: Integer; arena: array[0..31] of Byte;
    row: array[0..15] of Word; outputFile: file; written: LongInt;
begin
  Assign(outputFile, 'CALIB.BIN'); Rewrite(outputFile, 1);
  for bits := 0 to 65535 do begin
    for j := 0 to 31 do arena[j] := (bits + j * 17) and $ff;
    RegisterAX := $1234; RegisterBX := $1357; RegisterCX := $2468;
    RegisterDX := $369c; RegisterSI := $4567; RegisterDI := Word(bits);
    RegisterSP := Word(bits); RegisterBP := $6789;
    RegisterDS := $2000; RegisterES := $3000; RegisterSS := $4000;
    RegisterCarryFlag := (bits and 1) <> 0;
    RegisterZeroFlag := (bits and 2) <> 0;
    RegisterDirectionFlag := (bits and 4) <> 0;
    {name}(Word(bits), @arena[1 + (bits and 15)]);
    row[0] := RegisterAX; row[1] := RegisterBX; row[2] := RegisterCX;
    row[3] := RegisterDX; row[4] := RegisterSI; row[5] := RegisterDI;
    row[6] := RegisterSP; row[7] := RegisterBP;
    row[8] := RegisterDS; row[9] := RegisterES; row[10] := RegisterSS;
    row[11] := Word(RegisterCarryFlag); row[12] := Word(RegisterZeroFlag);
    row[13] := Word(RegisterDirectionFlag); row[14] := 0; row[15] := 0;
    BlockWrite(outputFile, row, 32, written); if written <> 32 then Halt(1);
    BlockWrite(outputFile, arena, 32, written); if written <> 32 then Halt(2);
  end;
  Close(outputFile);
end.
"""


def calibration_compare(name: str, data: bytes) -> dict:
    """Oracle: independent exhaustive supplied-source contract, not Liero original bytes."""
    if name not in CALIBRATION or len(data) != 65536 * 64:
        raise ValueError("unknown task or incomplete calibration output")
    failures = []
    for bits in range(65536):
        memory = bytearray((bits + j * 17) & 255 for j in range(32))
        index = 1 + (bits & 15)
        old = memory[index]
        memory[index] = old ^ (bits & 255)
        pair = name == "CalibratePair"
        if pair:
            memory[index] = bits >> 8
            memory[index + 1] = old ^ (bits & 255)
        row = (
            old,
            bits,
            0 if pair else 0x2468,
            0x369C,
            0x4567,
            (bits + 2) & 65535 if pair else bits,
            (bits + 6) & 65535,
            0x6789,
            0x2000,
            0x3000,
            0x4000,
            int(bool(bits & 1)) if pair else 0,
            int(bool(bits & 2)) if pair else int(memory[index] == 0),
            0 if pair else int(bool(bits & 4)),
            0,
            0,
        )
        expected = struct.pack("<16H", *row) + memory
        if data[bits * 64 : (bits + 1) * 64] != expected:
            failures.append(bits)
    return {
        "status": "failed" if failures else "passed",
        "cases": 65536,
        "matches": 65536 - len(failures),
        "first_failures": failures[:12],
    }


def run_calibration(
    root: pathlib.Path, output: pathlib.Path, model: str, endpoint: str
) -> dict:
    """Oracle: one proposal/task, known bodies and exhaustive adapter checks; no weights."""
    output.mkdir(parents=True, exist_ok=False)
    paths = [
        pathlib.Path(__file__),
        root / "engine/evidence_archive.py",
        root / "tests/test_liero_source_trial.py",
        root / "targets/liero/src/LieroRuntime.pas",
        root / "tools/liero_four_routine_pilot.py",
    ]
    (output / "sources").mkdir()
    for path in paths:
        shutil.copy2(path, output / "sources" / path.name)
    frozen = {
        "model": pilot.leaf_model_identity(model, endpoint),
        "tasks": CALIBRATION,
        "prompt_hashes": {
            n: hashlib.sha256(calibration_prompt(n).encode()).hexdigest()
            for n in CALIBRATION
        },
        "source_hashes": {str(p.relative_to(root)): pilot.digest(p) for p in paths},
        "budget": "one request per task, no repair,2048 tokens,temperature0,600s request/30s process",
        "acceptance": "both tasks pass all65536 values and complete supplied-source/adapter review before a separately frozen recovery run",
        "disclosure": "Developer-supplied bodies and explicit output contracts; syntax/representation calibration, not unseen recovery or independent Liero binary evidence",
        "weights_changed": False,
    }
    pilot.save(output / "freeze.json", frozen)
    results = {}
    for name in CALIBRATION:
        directory = output / name
        directory.mkdir()
        text = calibration_prompt(name)
        (directory / "prompt.txt").write_text(text)
        try:
            raw = pilot.request(text, model, endpoint)
            (directory / "response.json").write_text(raw)
            source = pilot.candidate_source(json.loads(raw), name)
        except (ValueError, KeyError, urllib.error.URLError, TimeoutError) as error:
            results[name] = {"status": "proposal-failed", "error": str(error)}
            continue
        (directory / "candidate.inc").write_text(source)
        (directory / "probe.pas").write_text(calibration_program(name))
        compiled = subprocess.run(
            [
                "fpc",
                "-Mtp",
                "-Cr",
                f"-Fu{root / 'targets/liero/src'}",
                "-FU.",
                "probe.pas",
            ],
            cwd=directory,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (directory / "compile.log").write_bytes(compiled.stdout + compiled.stderr)
        if compiled.returncode:
            results[name] = {
                "status": "compile-failed",
                "returncode": compiled.returncode,
            }
            continue
        try:
            runtime = subprocess.run(
                [str(directory / "probe")],
                cwd=directory,
                capture_output=True,
                timeout=30,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            (directory / "runtime.log").write_bytes(
                (error.stdout or b"") + (error.stderr or b"")
            )
            results[name] = {"status": "runtime-timeout"}
            continue
        (directory / "runtime.log").write_bytes(runtime.stdout + runtime.stderr)
        results[name] = (
            {"status": "runtime-failed", "returncode": runtime.returncode}
            if runtime.returncode
            else calibration_compare(name, (directory / "CALIB.BIN").read_bytes())
        )
    for name, digest in frozen["source_hashes"].items():
        if pilot.digest(root / name) != digest:
            raise ValueError("calibration inputs changed during execution")
    if pilot.leaf_model_identity(model, endpoint) != frozen["model"]:
        raise ValueError("calibration model changed")
    passed = all(r["status"] == "passed" for r in results.values())
    report = {
        "tasks": results,
        "status": "review-required" if passed else "blocked",
        "new_recoveries": 0,
        "weights_changed": False,
        "recovery_frontier_reopened": False,
    }
    pilot.save(output / "result.json", report)
    seal_archive(output)
    return report


def calibration_context(
    root: pathlib.Path, output: pathlib.Path, *, historical: bool = False
) -> str:
    """Oracle: bind reviewed known-source examples; never trust a pass label alone."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    result = json.loads(archive["result.json"])
    # Reviews were historically added after sealing and have their own bindings.
    review = json.loads((output / "review.json").read_text())
    if (
        result["status"] != "review-required"
        or review["status"] != "calibration-reviewed"
        or review["freeze_sha256"] != hashlib.sha256(archive["freeze.json"]).hexdigest()
        or review["artifacts_sha256"]
        != hashlib.sha256(archive["artifacts.json"]).hexdigest()
        or frozen["tasks"] != CALIBRATION
    ):
        raise ValueError("calibration acceptance/review identities disagree")
    for name, digest in frozen["source_hashes"].items():
        if (
            hashlib.sha256(archive["sources/" + pathlib.Path(name).name]).hexdigest()
            != digest
        ):
            raise ValueError("calibration source snapshot changed")
    runtime = "targets/liero/src/LieroRuntime.pas"
    if (
        not historical
        and pilot.digest(root / runtime) != frozen["source_hashes"][runtime]
    ):
        raise ValueError("calibration runtime changed")
    text = (
        "\nDisclosed known-source adapter calibration examples follow. These are "
        "supplied-body examples, not Liero recoveries or learned weights. Adapt "
        "the host-pointer/numeric-mirror distinction, not their memory algorithm. "
        "Infer the target algorithm only from its original instructions.\n"
    )
    for name in CALIBRATION:
        replay = calibration_compare(name, archive[f"{name}/CALIB.BIN"])
        if (
            replay != result["tasks"][name]
            or replay["status"] != "passed"
            or review["source_hashes"][name]
            != hashlib.sha256(archive[f"{name}/candidate.inc"]).hexdigest()
            or not review["review"][name].strip()
            or hashlib.sha256(archive[f"{name}/prompt.txt"]).hexdigest()
            != frozen["prompt_hashes"][name]
        ):
            raise ValueError("calibration source/review/output mismatch")
        text += calibration_prompt(name) + "\nReviewed answer:\n"
        text += archive[f"{name}/candidate.inc"].decode() + "\n"
    return text


def cases(routine: str, suite: str) -> list[bytes]:
    """Oracle: predeclared disjoint deterministic inputs, no outcome-based selection."""
    if routine not in {*PANEL, *DISCOVERY_PANEL} or suite not in {
        "training",
        "terminal",
    }:
        raise ValueError("unknown source trial routine or suite")
    rng = random.Random(20261103 + (suite == "terminal"))
    counts = (0, 1, 2, 3, 7, 15, 16, 31, 32, 127, 255, 256, 511, 1024)
    result = []
    for index in range(56):
        source = 0x8200 + rng.randrange(128)
        count = counts[index % len(counts)]
        destination = (source, source + 1, source - 1, 0x8800)[index % 4]
        if routine.endswith("40d6"):
            count = (
                (0, 1, 0x7FFF, 0x8000, 0xFFFF)[index]
                if index < 5
                else rng.randrange(65536)
            )
            destination = (
                0x8000 if index == 0 else 0x8FE0 if index == 1 else destination
            )
        flags = sum(
            bit
            for shift, bit in enumerate((1, 4, 0x40, 0x80, 0x400, 0x800))
            if index & (1 << shift)
        )
        if routine.endswith("4141"):
            count = (0, 1, 2, 3, 7, 15, 31, 127, 255)[index % 9] | (
                (0, 1, 7, 31, 255)[index % 5] << 8
            )
        if routine == "FUN_249c_0013":
            count = 0x8400 + rng.randrange(128)
        if routine == "FUN_24dd_455e":
            edges = (
                0,
                1,
                255,
                256,
                65535,
                65536,
                0x7FFFFFFF,
                0x80000000,
                0xFFFFFFFF,
                0xFFFFFF00,
            )
            value = edges[index] if index < len(edges) else rng.randrange(1 << 32)
            count, source = value & 65535, value >> 16
        result.append(
            struct.pack("<4H", count, source, destination, flags) + rng.randbytes(ARENA)
        )
    return result


def expected(routine: str, data: bytes, segment: int) -> bytes:
    """Oracle: independent declared-state contract, not model source or a native ABI."""
    if routine not in {*PANEL, *DISCOVERY_PANEL} or len(data) != CASE_BYTES:
        raise ValueError("invalid source trial case")
    argument, source, destination, flags = struct.unpack_from("<4H", data)
    memory = bytearray(data[8:])
    if routine == "FUN_24dd_455e":
        value = (source << 16) | argument
        cx = 0x2468
        ax, bx, dx = 0, 0, 0
        flag_byte = 0
        if value:
            cx = (source & 0xFF00) | 0x68
            negative = bool(value & 0x80000000)
            magnitude = (1 << 32) - value if negative else value
            ax = 160
            while magnitude < 0x80000000:
                magnitude <<= 1
                ax -= 1
            bx = magnitude & 65535
            dx = (magnitude >> 16) & (65535 if negative else 32767)
            flag_byte = source >> 8 if negative else dx >> 8
        final_flags = (
            (flags & 0x400)
            | int(flag_byte.bit_count() % 2 == 0) * 4
            | int(flag_byte == 0) * 0x40
            | (flag_byte & 0x80)
        )
        return (
            struct.pack(
                "<16H",
                ax,
                bx,
                cx,
                dx,
                source,
                destination,
                0x6789,
                0xEFEE,
                0xEFF0,
                segment,
                segment,
                segment,
                final_flags,
                0x1357,
                0x2468,
                segment,
            )
            + memory
        )
    if routine == "FUN_249c_0013":
        if not 0x8105 <= argument < 0x9000:
            raise ValueError("SS-relative byte cells outside owned arena")
        first, second = memory[argument - 0x8105], memory[argument - 0x8104]
        value = (first << 4) + second
        memory[argument - 0x8103] = value & 255
        entry = 0xEFF0 - 4
        final_flags = (
            (flags & 0x400)
            | int((value & 255).bit_count() % 2 == 0) * 4
            | int(value == 0) * 0x40
            | (value & 0x8000) >> 8
        )
        row = (
            value,
            0x1357,
            0x2468,
            second,
            source,
            argument,
            0x6789,
            entry,
            0xEFF0,
            segment,
            segment,
            segment,
            final_flags,
            0x1357,
            0x2468,
            segment,
        )
        return struct.pack("<16H", *row) + memory
    entry = 0xEFF0 - routine_spec(routine)["arguments"] - 4
    ax, cx, dx, si, di = 0x1234, 0, segment, source, destination
    if routine.endswith("40d6"):
        if not 0x8000 <= destination <= 0x9000 - 32:
            raise ValueError("initializer destination outside owned arena")
        memory[destination - 0x8000 : destination - 0x8000 + 32] = struct.pack(
            "<H", argument
        ) + bytes(30)
        ax, dx, di, flags = 0, 0x369C, destination + 32, 0x44
    else:
        skip = argument >> 8 if routine.endswith("4141") else 0
        count = argument & 255 if routine.endswith("4141") else argument
        if not (
            0x8000 <= source <= source + skip + count <= 0x9000
            and 0x8000 <= destination <= destination + count <= 0x9000
        ):
            raise ValueError("copy pointers/count outside owned arena")
        backward = routine.endswith("48e1") and source < destination
        indices = range(count - 1, -1, -1) if backward else range(count)
        for offset in indices:
            memory[destination - 0x8000 + offset] = memory[
                source + skip - 0x8000 + offset
            ]
        si, di, flags = source + skip + count, destination + count, flags & ~0x400
        if routine.endswith("4141"):
            value = (source + skip) & 65535
            flags = (
                int(source + skip > 65535)
                | int((value & 255).bit_count() % 2 == 0) * 4
                | int(value == 0) * 0x40
                | (value & 0x8000) >> 8
                | int(bool(~(source ^ skip) & (source ^ value) & 0x8000)) * 0x800
            )
        if routine.endswith("48e1"):
            if backward:
                # Last DEC DI defines PF/ZF/SF/OF; CF survives the prior ADD DI,CX.
                value = (destination + argument - 1) & 65535
                flags = (
                    int(destination + argument > 65535)
                    | int((value & 255).bit_count() % 2 == 0) * 4
                    | int(value == 0) * 0x40
                    | (value & 0x8000) >> 8
                    | int(value == 0x7FFF) * 0x800
                )
                si, di = source - 1, destination - 1
            else:
                value = (source - destination) & 65535
                flags = (
                    int(source < destination)
                    | int((value & 255).bit_count() % 2 == 0) * 4
                    | int(value == 0) * 0x40
                    | (value & 0x8000) >> 8
                    | int(bool((source ^ destination) & (source ^ value) & 0x8000))
                    * 0x800
                )
    row = (
        ax,
        argument if routine.endswith("4141") else entry,
        cx,
        dx,
        si,
        di,
        0x6789,
        entry,
        entry + 4 + routine_spec(routine)["cleanup"],
        segment,
        segment,
        segment,
        flags & 0xCC5,
        0x1357,
        0x2468,
        segment,
    )
    return struct.pack("<16H", *row) + memory


def harness(routine: str) -> str:
    """Oracle: owned COM invocation of unchanged bytes with exact far-call cleanup."""
    if routine not in {*PANEL, *DISCOVERY_PANEL}:
        raise ValueError("unknown source trial routine")
    args = (
        "push %cs\n    pushw input+4\n    pushw input"
        if routine.endswith("40d6")
        else "push %cs\n    pushw input+2\n    push %cs\n"
        "    pushw input+4\n    pushw input"
    )
    raw = ", ".join(
        "0x" + routine_spec(routine)["bytes"][i : i + 2]
        for i in range(0, len(routine_spec(routine)["bytes"]), 2)
    )
    near = routine_spec(routine).get("near", False)
    if near:
        args = "pushw input" if routine_spec(routine)["arguments"] else ""
    return_bytes = 2 if near else 4
    call_prefix = "" if near else "push %cs"
    text = f""".code16
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
    cld
    mov $0xeff0, %sp
    mov input_handle, %bx
    mov $input, %dx
    mov ${CASE_BYTES}, %cx
    mov $0x3f00, %ax
    int $0x21
    jc failed
    or %ax, %ax
    jz finished
    cmp ${CASE_BYTES}, %ax
    jne failed
    mov $input+8, %si
    mov $0x8000, %di
    mov ${ARENA}, %cx
    rep movsb
    movw $0x1357, %ss:0xeff0
    movw $0x2468, %ss:0xeff2
    {args}
    mov %sp, %ax
    sub ${return_bytes}, %ax
    mov %ax, snapshot+14
    mov $0x6789, %bp
    mov $0x1357, %bx
    mov $0x2468, %cx
    mov $0x369c, %dx
    mov input+2, %si
    mov input+4, %di
    mov input+6, %ax
    or $0x202, %ax
    push %ax
    popf
    mov $0x1234, %ax
    {call_prefix}
    call original
    mov %ax, snapshot
    mov %bx, snapshot+2
    mov %cx, snapshot+4
    mov %dx, snapshot+6
    mov %si, snapshot+8
    mov %di, snapshot+10
    mov %bp, snapshot+12
    mov %sp, snapshot+16
    mov %ds, snapshot+18
    mov %es, snapshot+20
    mov %ss, snapshot+22
    pushf
    popw snapshot+24
    mov %ss:0xeff0, %ax
    mov %ax, snapshot+26
    mov %ss:0xeff2, %ax
    mov %ax, snapshot+28
    mov %cs, %ax
    mov %ax, snapshot+30
    cld
    mov $0x8000, %si
    mov $snapshot+32, %di
    mov ${ARENA}, %cx
    rep movsb
    mov output_handle, %bx
    mov $snapshot, %dx
    mov ${RECORD_BYTES}, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp ${RECORD_BYTES}, %ax
    jne failed
    jmp next_case
finished:
    mov output_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21
input_name: .asciz "CASES.BIN"
output_name: .asciz "TRACE.BIN"
input_handle: .word 0
output_handle: .word 0
original: .byte {raw}
input: .space {CASE_BYTES}
snapshot: .space {RECORD_BYTES}
"""
    if routine == "FUN_24dd_455e":
        text = text.replace("mov $0x369c, %dx", "mov input+2, %dx").replace(
            "mov $0x1234, %ax", "mov input, %ax"
        )
    return text


def program(routine: str) -> str:
    """Oracle: candidate include and actual runtime; logical register/arena observations."""
    if routine not in {*PANEL, *DISCOVERY_PANEL}:
        raise ValueError("unknown source trial routine")
    scalar = "input[0]" if routine.endswith("4141") else "Integer(input[0])"
    call = (
        f"{routine}(input[0], @arena[input[2] - $8000]);"
        if routine.endswith("40d6")
        else f"{routine}({scalar}, @arena[input[2] - $8000], @arena[input[1] - $8000]);"
    )
    if routine == "FUN_249c_0013":
        call = f"{routine}(input[0], @arena[input[0] - $8105]);"
    if routine == "FUN_24dd_455e":
        call = "RegisterAX := input[0]; RegisterDX := input[1]; FUN_24dd_455e;"
    return_bytes = 2 if routine_spec(routine).get("near") else 4
    return f"""program SourceTrial;
uses LieroRuntime;
{{$I candidate.inc}}
var arena: array[0..4095] of Byte;
    input: array[0..3] of Word; row: array[0..15] of Word;
    inputFile, outputFile: file; transferred: LongInt; entry: Word;
begin
  if SizeOf(Integer) <> 2 then Halt(1);
  Assign(inputFile, 'CASES.BIN'); Reset(inputFile, 1);
  Assign(outputFile, 'PASCAL.BIN'); Rewrite(outputFile, 1);
  while not Eof(inputFile) do
  begin
    BlockRead(inputFile, input, 8, transferred);
    if transferred <> 8 then Halt(2);
    BlockRead(inputFile, arena, 4096, transferred);
    if transferred <> 4096 then Halt(3);
    RegisterAX := $1234; RegisterBX := $1357; RegisterCX := $2468;
    RegisterDX := $369c; RegisterSI := input[1]; RegisterDI := input[2];
    RegisterDS := $2000; RegisterES := $2000; RegisterSS := $2000;
    RegisterBP := $6789;
    entry := $eff0 - {routine_spec(routine)["arguments"]} - {return_bytes};
    RegisterSP := entry;
    RegisterCarryFlag := (input[3] and 1) <> 0;
    RegisterZeroFlag := (input[3] and $40) <> 0;
    RegisterDirectionFlag := (input[3] and $400) <> 0;
    {call}
    row[0] := RegisterAX; row[1] := RegisterBX; row[2] := RegisterCX;
    row[3] := RegisterDX; row[4] := RegisterSI; row[5] := RegisterDI;
    row[6] := RegisterBP; row[7] := entry; row[8] := RegisterSP;
    row[9] := RegisterDS; row[10] := RegisterES; row[11] := RegisterSS;
    row[12] := Word(RegisterCarryFlag) + Word(RegisterZeroFlag) * $40 +
      Word(RegisterDirectionFlag) * $400;
    row[13] := $1357; row[14] := $2468; row[15] := $2000;
    BlockWrite(outputFile, row, 32, transferred);
    if transferred <> 32 then Halt(4);
    BlockWrite(outputFile, arena, 4096, transferred);
    if transferred <> 4096 then Halt(5);
  end;
  Close(inputFile); Close(outputFile);
end.
"""


def compare(routine: str, inputs: list[bytes], trace: bytes, *, native: bool) -> dict:
    """Oracle: exact records/full arena; native-only flags/stack are not host parity."""
    if len(trace) != len(inputs) * RECORD_BYTES:
        raise ValueError("partial or extra source-trial output")
    failures = []
    for index, data in enumerate(inputs):
        row = bytearray(trace[index * RECORD_BYTES : (index + 1) * RECORD_BYTES])
        segment = struct.unpack_from("<H", row, 30)[0] if native else 0x2000
        if not 0x100 <= segment <= 0x9000:
            raise ValueError("invalid original segment")
        want = bytearray(expected(routine, data, segment))
        flags = struct.unpack_from("<H", row, 24)[0] & (0xCC5 if native else 0x441)
        struct.pack_into("<H", row, 24, flags)
        if not native:
            struct.pack_into(
                "<H", want, 24, struct.unpack_from("<H", want, 24)[0] & 0x441
            )
        if row != want:
            differences = [
                i for i, (a, b) in enumerate(zip(row, want, strict=True)) if a != b
            ]
            failures.append({"case": index, "first_different_bytes": differences[:12]})
    return {
        "status": "failed" if failures else "passed",
        "cases": len(inputs),
        "matches": len(inputs) - len(failures),
        "failures": failures,
    }


def compile_candidate(
    root: pathlib.Path, output: pathlib.Path, routine: str, source: str
) -> dict:
    """Oracle: FPC compiles exact proposed bytes against the actual target runtime."""
    output.mkdir(parents=True, exist_ok=False)
    (output / "candidate.inc").write_text(source)
    (output / "probe.pas").write_text(program(routine))
    command = [
        "fpc",
        "-Mtp",
        "-Cr",
        f"-Fu{root / 'targets/liero/src'}",
        "-FU.",
        "probe.pas",
    ]
    result = subprocess.run(
        command, cwd=output, capture_output=True, timeout=30, check=False
    )
    (output / "compile.log").write_bytes(result.stdout + result.stderr)
    return {
        "status": "passed" if result.returncode == 0 else "compile-failed",
        "returncode": result.returncode,
    }


def run_candidate(output: pathlib.Path, routine: str, inputs: list[bytes]) -> dict:
    """Oracle: complete actual candidate output or explicit runtime/timeout failure."""
    (output / "CASES.BIN").write_bytes(b"".join(inputs))
    try:
        result = subprocess.run(
            [str(output / "probe")],
            cwd=output,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        (output / "runtime.log").write_bytes(
            (error.stdout or b"") + (error.stderr or b"")
        )
        return {"status": "runtime-timeout"}
    (output / "runtime.log").write_bytes(result.stdout + result.stderr)
    if result.returncode:
        return {"status": "runtime-failed", "returncode": result.returncode}
    return compare(routine, inputs, (output / "PASCAL.BIN").read_bytes(), native=False)


def original(
    root: pathlib.Path, output: pathlib.Path, routine: str, inputs: list[bytes]
) -> dict:
    """Oracle: exact byte-authenticated routine, no instruction substitutions."""
    output.mkdir(parents=True, exist_ok=False)
    (output / "harness.S").write_text(harness(routine))
    image = assemble_probe(output / "harness.S", output)
    if len(image) + 0x100 >= 0x6000:
        raise ValueError("source trial harness overlaps protected arena")
    if image.count(bytes.fromhex(routine_spec(routine)["bytes"])) != 1:
        raise ValueError("original leaf bytes missing or duplicated")
    (output / "PROBE.COM").write_bytes(image)
    (output / "CASES.BIN").write_bytes(b"".join(inputs))
    run_dosbox(output)
    result = compare(routine, inputs, (output / "TRACE.BIN").read_bytes(), native=True)
    if result["status"] != "passed":
        raise ValueError("original execution disagrees with frozen static contract")
    pilot.save(output / "result.json", result)
    return result


def instruction_listing(root: pathlib.Path, routine: str) -> str:
    """Oracle: exported reference with explicitly byte-backed corrections."""
    assembly = (root / f"targets/liero/asm/{routine}.s").read_text()
    if routine.endswith("3d68"):
        assembly = assembly.replace("24dd:3d7b  MOV DX,DS", "24dd:3d7b  MOV DS,DX")
    if routine.endswith("4141"):
        assembly = assembly.replace("24dd:415c  MOV DX,DS", "24dd:415c  MOV DS,DX")
    if routine.endswith("48e1"):
        assembly = assembly.replace("24dd:4900  MOV DX,DS", "24dd:4900  MOV DS,DX")
        raw = bytes.fromhex(PANEL[routine]["bytes"])
        if raw[19:21] != bytes.fromhex("7307"):
            raise ValueError("move conditional branch bytes changed")
        destination = (
            PANEL[routine]["offset"]
            + 21
            + int.from_bytes(raw[20:21], "little", signed=True)
        )
        assembly = assembly.replace(
            "24dd:48f4  JNC 0x2000:96cd", f"24dd:48f4  JNC 24dd:{destination:04x}"
        )
    return assembly


def prompt(root: pathlib.Path, routine: str) -> str:
    """Oracle: byte-backed instructions and representation, never the existing body."""
    assembly = instruction_listing(root, routine)
    if routine == "FUN_249c_0013":
        return f"""Return JSON with only source, containing exactly this complete Pascal routine include:
{routine_spec(routine)["signature"]}
No unit/interface/implementation/program declarations, helpers, services or directives.
This is a supplied host projection of original SS-relative memory. param_1 is
the original near stack argument. PByte(param_2)[0] corresponds to SS:[param_1-261],
[1] to SS:[param_1-260], [2] to SS:[param_1-259]. All three are owned valid bytes;
do not address DOS memory. Infer arithmetic and the written byte from bytes.
Preserve all other memory. Use LongInt locals.
Provide logical register effects: AX is the untruncated arithmetic result, DX is
the zero-extended byte originally loaded first (cell1), DI is param_1, SP advances4.
CF/ZF from final16bit ADD, all other mirrors including DF preserved.
Host interface and mirror obligations are human assistance, not recovered native ABI.
{assembly}
Original bytes: {routine_spec(routine)["bytes"]}
"""
    scalar = (
        "param_1 is a packed Word: high byte is unsigned source skip; low byte is "
        "unsigned copy count. Source traversal is always forward even for overlap."
        if routine.endswith("4141")
        else "param_1 bits are the original unsigned word count."
    )
    return f"""Recover this entire callee-free Turbo Pascal routine from instructions.
Return JSON with only a source field containing a complete include.
Do not use assembler, compiler directives, services, libraries, or other routines.
Required declaration: {routine_spec(routine)["signature"]}
Runtime supplies PByte, Word, LongInt, and these mutable mirrors:
RegisterAX, RegisterBX, RegisterCX, RegisterDX, RegisterSI, RegisterDI,
RegisterBP, RegisterSP, RegisterDS, RegisterES, RegisterSS: Word;
RegisterCarryFlag, RegisterZeroFlag, RegisterDirectionFlag: Boolean.
Do not introduce AX/BX/etc aliases. Use these exact full names.
param_2 is a host pointer to the original destination. For the copy param_3 is
a host pointer to the original source. {scalar}
Mirror SI/DI designate input source/destination
offsets, ES the destination segment; DS/SS are entry segments. Mirror SP is
callee entry after the original far call. Model all available register and flag
outputs, including RETF's numeric SP change (4 plus its immediate).
Host pointers are not numeric 16-bit offsets: do not cast host pointers to Word.
Pointer parameters already resolve the checked original pointers.
This is high-level Pascal using the supplied parameters, NOT an emulator.
Do not read or dereference a numeric register/stack/segment. The host process has
no original DOS stack. Use param_1 for the scalar argument and param_2/param_3
for all memory accesses. Only PByte(param_2), PByte(param_3), local pointers
derived from them, pointer increments and dereferences are allowed.
The mirror SI/DI offsets are only numeric observations, never host addresses.
The previous training run's invalid numeric-pointer emulation crashed; repeated
identical code is not a repair. No PWord, Pointer(...), Ptr(...), RealModeMemory,
DosMemory, Move or FillChar calls. Implement memory operations with byte pointers.
Preserve unmodified mirrors. Full native flags not represented here are outside
the host model. Use explicit unsigned widening/masking where overflow matters.
{SCOPE}
Original bytes: {routine_spec(routine)["bytes"]}
The following listing has been checked against these bytes; in the copy the
last MOV is DS,DX (8eda), correcting the exported listing.
{assembly}
"""


def output_obligations(routine: str, raw: bytes) -> dict:
    """Oracle: recognized complete original shapes; explicit scoped outputs, no candidate fix."""
    if (
        routine not in {*PANEL, *DISCOVERY_PANEL}
        or raw.hex() != routine_spec(routine)["bytes"]
    ):
        raise ValueError("unrecognized complete routine bytes")
    if routine in ("FUN_249c_0013", "FUN_24dd_455e"):
        return {
            "oracle": "original near arithmetic projection",
            "original_bytes_hex": raw.hex(),
            "declaration": routine_spec(routine)["signature"],
            "near_return_bytes": 2,
            "ret_immediate": routine_spec(routine)["cleanup"],
            "outputs": {
                "AX/BX/DX": "Normalized exponent and32-bit fraction; zero input returns zeros",
                "CX": "Entry CL preserved; CH original DH for nonzero, entry CH for zero",
                "SP": "entry+2",
                "others": "SI/DI/BP/DS/ES/SS and DF preserved; CF clear, ZF from final byte logical operation",
            }
            if routine == "FUN_24dd_455e"
            else {
                "AX": "16bit arithmetic",
                "DX": "cell1 zeroextended",
                "DI": "param_1",
                "SP": "entry+4",
            },
            "scope": SCOPE,
            "assistance": "Human host projection and mirror contract, no body supplied",
        }
    cleanup = int.from_bytes(raw[-2:], "little")
    if raw[-3] != 0xCA:
        raise ValueError("unsupported far return")
    outputs = {
        "RegisterBX": "entry RegisterSP",
        "RegisterCX": "0",
        "RegisterSP": f"(entry RegisterSP + {cleanup + 4}) mod65536",
        "RegisterDirectionFlag": "False",
        "RegisterBP/RegisterSS": "preserved",
    }
    if routine.endswith("40d6"):
        outputs.update(
            {
                "RegisterAX": "0",
                "RegisterDX/RegisterSI/RegisterDS": "preserved",
                "RegisterDI": "(entry destination offset +32) mod65536",
                "RegisterES": "destination segment",
                "RegisterCarryFlag": "False",
                "RegisterZeroFlag": "True",
            }
        )
    else:
        outputs.update(
            {
                "RegisterAX": "preserved",
                "RegisterDX": "entry RegisterDS",
                "RegisterDS": "restored to entry value (8eda is MOV DS,DX)",
                "RegisterES": "destination segment",
                "RegisterSI": "(entry source offset + unsigned count) mod65536",
                "RegisterDI": "(entry destination offset + unsigned count) mod65536",
                "RegisterCarryFlag/RegisterZeroFlag": "preserved",
            }
        )
        if routine.endswith("48e1"):
            outputs.update(
                {
                    "RegisterSI": "if entry source offset < destination offset: source-1 mod65536, even count0; otherwise source+count mod65536",
                    "RegisterDI": "if entry source offset < destination offset: destination-1 mod65536, even count0; otherwise destination+count mod65536",
                    "RegisterCarryFlag/RegisterZeroFlag": "if source>=destination: CF=(source<destination), ZF=(source=destination) from CMP; otherwise CF from16bit ADD destination,count, ZF=((destination+count-1) mod65536=0) from final DEC DI. REP/CLD preserve these.",
                }
            )
        if routine.endswith("4141"):
            outputs.update(
                {
                    "RegisterBX": "packed param_1, not entry SP",
                    "RegisterSI": "(entry source offset + high_byte(param_1) + low_byte(param_1)) mod65536",
                    "RegisterDI": "(entry destination offset + low_byte(param_1)) mod65536",
                    "RegisterCarryFlag/RegisterZeroFlag": "CF/ZF from16-bit ADD sourceOffset,high_byte(param_1); REP preserves flags",
                }
            )
    return {
        "oracle": "complete exact-byte shape under supplied owned pointer/register model",
        "original_bytes_hex": raw.hex(),
        "declaration": routine_spec(routine)["signature"],
        "retf_immediate": cleanup,
        "far_return_bytes": 4,
        "outputs": outputs,
        "scope": SCOPE,
        "assistance": "Manually derived byte-backed output obligations, not model-discovered facts; memory body still proposed, no automatic repair or wrapper.",
    }


def check_declaration(routine: str, source: str) -> dict | None:
    """Oracle: exact canonical interface using the existing declaration reader."""
    actual = pascal_declaration(source, routine)
    normalize = lambda value: re.sub(r"\s+", "", value or "").casefold()
    if normalize(actual) != normalize(routine_spec(routine)["signature"]):
        return {
            "status": "declaration-rejected",
            "required": routine_spec(routine)["signature"],
            "actual": actual,
        }
    return None


def trial_prompt(
    root: pathlib.Path,
    routine: str,
    context: str,
    enforce_outputs: bool,
    typed_memory_guidance: bool = False,
) -> str:
    """Oracle: explicit assistance frozen before generation, not repaired source."""
    text = context + prompt(root, routine)
    if enforce_outputs:
        text += "\nMandatory byte-backed output obligations:\n" + json.dumps(
            output_obligations(routine, bytes.fromhex(routine_spec(routine)["bytes"])),
            indent=2,
        )
    if typed_memory_guidance:
        if routine != "FUN_24dd_4141" or not enforce_outputs:
            raise ValueError(
                "typed memory guidance requires4141 with output obligations"
            )
        text += """
Typed Pascal representation guidance (human assistance, not a supplied routine body):
Declare local source and destination as PByte; bind them only using
PByte(param_3) and PByte(param_2). PByte indexing reads/writes byte data:
destination[index] := source[expression]. Derive the expression, traversal
order and bounds from the instructions; emit actual destination memory writes.
Use LongInt for loop bounds/arithmetic so a zero-count upper bound is -1.
Extract packed bytes using param_1 and $FF and param_1 shr 8, not Low/High:
Low/High return TYPE bounds, not the low/high bytes of a scalar in Pascal.
RegisterSI/DI are numeric original pointer-offset mirrors; they are not pointer
contents. Never dereference parameters to obtain segment or offset mirrors.
Keep host memory pointers separate from original RegisterSI/DI state. Only
update required mirrors from entry mirrors and instruction-derived arithmetic.
Return one complete JSON source string with declaration, local var section,
byte-copy logic and all required outputs. No helper routines or supplied body.
"""
    return text


def residual_prompt(
    root: pathlib.Path, routine: str, *, structured: bool = True
) -> str:
    """Oracle: supplied ABI partition; memory algorithm must still be inferred."""
    if routine == "FUN_24dd_4141":
        return f"""Infer the memory body from the original bytes below.
Return JSON with only a source field containing optional var declarations and
begin ... end; . Do NOT emit procedure, function, unit, interface, implementation
or program declarations. A human-authored wrapper supplies the routine and ABI.
MemoryBody(argument: Word; source, destination: Pointer) receives the packed
original argument and valid host pointers. Runtime supplies PByte and LongInt.
Bind local PByte pointers with PByte(source) and PByte(destination).
PByte indexing is byte data access, not segment/offset extraction.
Use LongInt for loop bounds; packed bytes can be extracted with and $FF / shr 8.
Infer address arithmetic, order and repeat count from the instructions.
Emit memory writes, not Register symbols. No helpers, services, Move, FillChar,
assembler, compiler directives or numeric pointer casts. No target body supplied.
{SCOPE}
Original bytes: {routine_spec(routine)["bytes"]}
{instruction_listing(root, routine)}
"""
    if routine != "FUN_24dd_48e1":
        raise ValueError("residual partition supports only byte-reviewed48e1")
    output_obligations(routine, bytes.fromhex(PANEL[routine]["bytes"]))
    output = (
        'Return JSON with only a "source" field containing the Pascal body.'
        if structured
        else "Output only raw Pascal body text, no JSON or markdown."
    )
    return f"""Infer only the memory behavior of these original instructions.
The containing routine and ABI effects are independently supplied by a checked
wrapper. The residual interface is MemoryBody(count: Word; source, destination:
Pointer; backward: Boolean). Do not emit that declaration.
{output}
The body has optional local var declarations, then begin ... end; .
No procedure/function/unit/program declarations, assembler, services, libraries,
compiler directives or Register symbols. Runtime supplies PByte, Word and LongInt.
source and destination are valid host pointers resolving original SI and DI;
count is the original unsigned CX byte count. backward is the original numeric
offset comparison source < destination, not host pointer ordering.
Use PByte(source), PByte(destination), local derived pointers, increments and
dereferences. Do not cast host pointers to Word or dereference DOS offsets.
Infer traversal and count0 behavior from the original bytes, not from a supplied
Pascal algorithm. Do not alter memory beyond the specified byte ranges.
{SCOPE}
Original bytes: {PANEL[routine]["bytes"]}
Byte-backed listing corrections: final8eda is MOV DS,DX; short JNC7307 targets
24dd:48fd (next instruction48f6 plus signed displacement7).
{instruction_listing(root, routine)}
"""


def compose_residual(body: str, routine: str = "FUN_24dd_48e1") -> str:
    """Oracle: complete byte-bound48e1 wrapper, not model-inferred ABI."""
    if routine not in ("FUN_24dd_48e1", "FUN_24dd_4141"):
        raise ValueError("unsupported residual wrapper")
    output_obligations(routine, bytes.fromhex(routine_spec(routine)["bytes"]))
    if re.search(
        r"\b(?:Register\w*|unit|program|uses|procedure|function|asm|external|"
        r"halt|assign|reset|rewrite|blockread|blockwrite|exec|PWord|Ptr|Move|FillChar|"
        r"RealModeMemory|DosMemory)\b|\bPointer\s*\(|"
        r"\bPByte\s*\(\s*(?!(?:source|destination)\s*\))|\{\$|\(\*\$",
        body,
        re.IGNORECASE,
    ) or not re.match(
        r"\s*(?:var\b[\s\S]*?)?begin\b[\s\S]*end;\s*$", body, re.IGNORECASE
    ):
        raise ValueError(
            "residual must be a Pascal body without ABI writes or services"
        )
    if routine == "FUN_24dd_4141":
        return f"""procedure FUN_24dd_4141(param_1: Word; param_2, param_3: Pointer);
var sourceOffset, destinationOffset, skip, count: LongInt;
procedure MemoryBody(argument: Word; source, destination: Pointer);
{body}
begin
  sourceOffset := RegisterSI; destinationOffset := RegisterDI;
  skip := param_1 shr 8; count := param_1 and 255;
  MemoryBody(param_1, param_3, param_2);
  RegisterBX := param_1; RegisterDX := RegisterDS; RegisterES := RegisterDS;
  RegisterCarryFlag := sourceOffset + skip > 65535;
  RegisterZeroFlag := ((sourceOffset + skip) and 65535) = 0;
  RegisterSI := (sourceOffset + skip + count) and 65535;
  RegisterDI := (destinationOffset + count) and 65535;
  RegisterCX := 0; RegisterDirectionFlag := False;
  RegisterSP := (RegisterSP + 14) and 65535;
end;
"""
    return f"""procedure FUN_24dd_48e1(param_1: Integer; param_2, param_3: Pointer);
var sourceOffset, destinationOffset, count: LongInt; backward: Boolean;
procedure MemoryBody(count: Word; source, destination: Pointer; backward: Boolean);
{body}
begin
  sourceOffset := RegisterSI; destinationOffset := RegisterDI;
  count := Word(param_1); backward := sourceOffset < destinationOffset;
  MemoryBody(Word(count), param_3, param_2, backward);
  RegisterBX := RegisterSP; RegisterDX := RegisterDS;
  RegisterES := RegisterDS; RegisterCX := 0; RegisterDirectionFlag := False;
  if backward then begin
    RegisterCarryFlag := destinationOffset + count > 65535;
    RegisterZeroFlag := ((destinationOffset + count - 1) and 65535) = 0;
    RegisterSI := (sourceOffset - 1) and 65535;
    RegisterDI := (destinationOffset - 1) and 65535;
  end else begin
    RegisterCarryFlag := False; RegisterZeroFlag := sourceOffset = destinationOffset;
    RegisterSI := (sourceOffset + count) and 65535;
    RegisterDI := (destinationOffset + count) and 65535;
  end;
  RegisterSP := (RegisterSP + 14) and 65535;
end;
"""


INTERPRETATION_BYTES = bytes.fromhex(
    "8bdc8cda36c5770a36c47f06368b4f04fc3bf7730703f103f94e4ffdf3a4fc8edaca0a00"
)
INTERPRETATION_FIELDS = {
    "condition": ["source_lt_destination", "source_ge_destination"],
    "zero_count": ["no_access", "one_access"],
    "forward_start": ["zero", "count_minus_one"],
    "backward_start": ["zero", "count_minus_one"],
    "forward_step": [1, -1],
    "backward_step": [1, -1],
    "access_order": ["copy_then_step", "step_then_copy"],
    "repeat": ["count_times", "count_plus_one"],
}
INTERPRETATION_SCHEMA = {
    "type": "object",
    "properties": {
        "hypotheses": {
            "type": "array",
            "minItems": 1,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    **{
                        name: {
                            "type": "integer"
                            if isinstance(values[0], int)
                            else "string",
                            "enum": values,
                        }
                        for name, values in INTERPRETATION_FIELDS.items()
                    },
                    "evidence": {
                        "type": "object",
                        "properties": {
                            name: {"type": "string"}
                            for name in ("branch", "setup", "transfer")
                        },
                        "required": ["branch", "setup", "transfer"],
                        "additionalProperties": False,
                    },
                },
                "required": [*INTERPRETATION_FIELDS, "evidence"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["hypotheses"],
    "additionalProperties": False,
}


PACKED_FIELDS = {
    "source_start": ["high_byte", "low_byte", "zero"],
    "destination_start": ["zero", "high_byte", "low_byte"],
    "count": ["low_byte", "high_byte", "word"],
    "step": [1, -1],
    "access_order": ["copy_then_step", "step_then_copy"],
    "zero_count": ["no_access", "one_access"],
}
PACKED_SCHEMA = {
    "type": "object",
    "properties": {
        "hypotheses": {
            "type": "array",
            "minItems": 1,
            "maxItems": 3,
            "items": {
                "type": "object",
                "properties": {
                    **{
                        name: {
                            "type": "integer" if name == "step" else "string",
                            "enum": values,
                        }
                        for name, values in PACKED_FIELDS.items()
                    },
                    "evidence": {
                        "type": "object",
                        "properties": {
                            name: {"type": "string"}
                            for name in ("source_start", "count", "transfer")
                        },
                        "required": ["source_start", "count", "transfer"],
                        "additionalProperties": False,
                    },
                },
                "required": [*PACKED_FIELDS, "evidence"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["hypotheses"],
    "additionalProperties": False,
}


PACKED_BINDINGS = {
    "source_start": "4152:8acf MOV CL,BH;4154:32ed XOR CH,CH;4156:03f1 ADD SI,CX",
    "count": "4158:8acb MOV CL,BL",
    "transfer": "4141:fc CLD;415a:f3a4 REP MOVSB",
}


def packed_schema(supplied_bindings: bool) -> dict:
    """Oracle: frozen byte-derived citation facts, never supplied behavioral action choices."""
    schema = json.loads(json.dumps(PACKED_SCHEMA))
    if supplied_bindings:
        schema["properties"]["hypotheses"]["items"]["properties"]["evidence"] = {
            "type": "object",
            "properties": {
                name: {"type": "string", "const": value}
                for name, value in PACKED_BINDINGS.items()
            },
            "required": list(PACKED_BINDINGS),
            "additionalProperties": False,
        }
    return schema


def check_packed_interpretation(
    hypothesis: dict, inputs: list[bytes], records: bytes
) -> dict:
    """Oracle: byte-bound packed-copy actions plus independent original-training memory."""
    routine = "FUN_24dd_4141"
    raw = "fc8bdc8cda36c5770a36c47f06368b5f048acf32ed03f18acbf3a48edaca0a00"
    if routine_spec(routine)["bytes"] != raw:
        raise ValueError("packed interpretation byte identity changed")
    if set(hypothesis) != {*PACKED_FIELDS, "evidence"}:
        raise ValueError("packed interpretation fields differ")
    for name, values in PACKED_FIELDS.items():
        if (
            type(hypothesis[name]) is not type(values[0])
            or hypothesis[name] not in values
        ):
            raise ValueError("invalid packed alternative: " + name)
    evidence = hypothesis["evidence"]
    if (
        not isinstance(evidence, dict)
        or set(evidence) != {"source_start", "count", "transfer"}
        or any(not isinstance(v, str) for v in evidence.values())
    ):
        raise ValueError("invalid packed interpretation evidence")
    required = {
        "source_start": ("high_byte", "4152:8acf 4154:32ed 4156:03f1"),
        "destination_start": ("zero", "414a:36c47f06"),
        "count": ("low_byte", "4158:8acb 415a:f3a4"),
        "step": (1, "4141:fc"),
        "access_order": ("copy_then_step", "415a:f3a4"),
        "zero_count": ("no_access", "415a:f3a4"),
    }
    conflicts = [
        {
            "field": name,
            "proposed": hypothesis[name],
            "required": value,
            "evidence": fact,
        }
        for name, (value, fact) in required.items()
        if hypothesis[name] != value
    ]
    for name, addresses in {
        "source_start": ("4152", "4154", "4156"),
        "count": ("4158",),
        "transfer": ("4141", "415a"),
    }.items():
        if any(address not in evidence[name].lower() for address in addresses):
            conflicts.append(
                {"field": "evidence." + name, "required_addresses": list(addresses)}
            )
    if (
        not inputs
        or compare(routine, inputs, records, native=True)["status"] != "passed"
    ):
        raise ValueError("packed original training contract failed")
    matches, counterexamples = 0, []
    for index, data in enumerate(inputs):
        argument, source, destination, _ = struct.unpack_from("<4H", data)
        values = {
            "high_byte": argument >> 8,
            "low_byte": argument & 255,
            "zero": 0,
            "word": argument,
        }
        count = values[hypothesis["count"]]
        if not count:
            count = int(hypothesis["zero_count"] == "one_access")
        memory = bytearray(data[8:])
        valid = True
        for i in range(count):
            step = hypothesis["step"] * (
                i + (hypothesis["access_order"] == "step_then_copy")
            )
            src = source - 0x8000 + values[hypothesis["source_start"]] + step
            dst = destination - 0x8000 + values[hypothesis["destination_start"]] + step
            if not (0 <= src < ARENA and 0 <= dst < ARENA):
                valid = False
                break
            memory[dst] = memory[src]
        observed = records[index * RECORD_BYTES + 32 : (index + 1) * RECORD_BYTES]
        if valid and memory == observed:
            matches += 1
        elif len(counterexamples) < 3:
            counterexamples.append(
                {"case": index, "argument": argument, "out_of_bounds": not valid}
            )
    return {
        "status": "passed"
        if not conflicts and matches == len(inputs)
        else "contradicted",
        "instruction_conflicts": conflicts,
        "training_memory_matches": matches,
        "training_cases": len(inputs),
        "required_case_recall": matches / len(inputs),
        "memory_status": "passed" if matches == len(inputs) else "contradicted",
        "instruction_status": "passed" if not conflicts else "contradicted",
        "counterexamples": counterexamples,
        "probability_correct": None,
        "sensitivity": None,
        "scope": "Enumerated byte-bound packed-copy memory interpretation; not native ABI or whole routine.",
    }


def lower_packed_interpretation(hypothesis: dict) -> str:
    """Oracle: human typed renderer of checked model actions, not model-written Pascal."""
    supported = {
        "source_start": "high_byte",
        "destination_start": "zero",
        "count": "low_byte",
        "step": 1,
        "access_order": "copy_then_step",
        "zero_count": "no_access",
    }
    if any(
        type(hypothesis.get(n)) is not type(v) or hypothesis[n] != v
        for n, v in supported.items()
    ):
        raise ValueError("unsupported packed interpretation")
    return """var src, dst: PByte; skip, count, i: LongInt;
begin
  src := PByte(source); dst := PByte(destination);
  skip := argument shr 8; count := argument and 255;
  for i := 0 to count - 1 do dst[i] := src[skip + i];
end;
"""


ARITHMETIC_FIELDS = {
    "left_cell": [0, 1],
    "right_cell": [0, 1],
    "shift": [0, 4, 8],
    "operation": ["add", "or", "xor"],
    "output_cell": [0, 1, 2],
    "truncate_before_add": [False, True],
}
ARITHMETIC_BINDINGS = {
    "loads": "0019:368a85fcfe SS:[DI-260];0022:368a85fbfe SS:[DI-261]",
    "arithmetic": "0029:c1e004 SHL AX,4;002c:03c2 ADD AX,DX",
    "store": "002e:368885fdfe SS:[DI-259] := AL",
}
NORMALIZE_FIELDS = {
    "magnitude": ["signed_absolute", "unsigned"],
    "exponent_bias": [136, 144, 160],
    "exponent_step": [-1, 1],
    "shift_direction": ["left", "right"],
    "clear_fraction_top_bit": ["positive", "negative", "never"],
    "zero_input": ["preserve_cx", "replace_ch"],
}
NORMALIZE_BINDINGS = {
    "sign": "456a:f7da NEG DX;456c:f7d8 NEG AX;456e:83da00 SBB DX,0",
    "normalization": "4573:b8a000 MOV AX,160;458a:fec8 DEC AL;458c:03db ADD BX,BX;458e:13d2 ADC DX,DX",
    "fraction": "4592:0aed OR CH,CH;4594:7803 JS;4596:80e67f AND DH,127",
}


def normalize_schema() -> dict:
    """Oracle: closed register-normalization alternatives, byte citations supplied."""
    schema = arithmetic_schema()
    item = schema["properties"]["hypotheses"]["items"]
    item["properties"] = {
        name: {
            "type": "integer" if type(values[0]) is int else "string",
            "enum": values,
        }
        for name, values in NORMALIZE_FIELDS.items()
    }
    item["properties"]["evidence"] = {
        "type": "object",
        "properties": {
            n: {"type": "string", "const": v} for n, v in NORMALIZE_BINDINGS.items()
        },
        "required": list(NORMALIZE_BINDINGS),
        "additionalProperties": False,
    }
    item["required"] = [*NORMALIZE_FIELDS, "evidence"]
    return schema


def check_normalize_interpretation(
    hypothesis: dict, inputs: list[bytes], records: bytes
) -> dict:
    """Oracle: byte-backed sign/normalization semantics and original complete training state."""
    if (
        set(hypothesis) != {*NORMALIZE_FIELDS, "evidence"}
        or hypothesis["evidence"] != NORMALIZE_BINDINGS
    ):
        raise ValueError("normalization schema/bindings differ")
    for name, values in NORMALIZE_FIELDS.items():
        if (
            type(hypothesis[name]) is not type(values[0])
            or hypothesis[name] not in values
        ):
            raise ValueError("normalization alternative invalid")
    if (
        not inputs
        or compare("FUN_24dd_455e", inputs, records, native=True)["status"] != "passed"
    ):
        raise ValueError("normalization original fixture differs")
    supported = {
        "magnitude": "signed_absolute",
        "exponent_bias": 160,
        "exponent_step": -1,
        "shift_direction": "left",
        "clear_fraction_top_bit": "positive",
        "zero_input": "preserve_cx",
    }
    conflicts = [
        {"field": n, "proposed": hypothesis[n], "required": v}
        for n, v in supported.items()
        if hypothesis[n] != v
    ]
    matches = 0
    for index, data in enumerate(inputs):
        low, high = struct.unpack_from("<2H", data)
        value = (high << 16) | low
        cx = (
            (high & 0xFF00) | 0x68
            if value or hypothesis["zero_input"] == "replace_ch"
            else 0x2468
        )
        ax, bx, dx = 0, 0, 0
        negative = bool(value & 0x80000000)
        if value:
            magnitude = (
                (1 << 32) - value
                if negative and hypothesis["magnitude"] == "signed_absolute"
                else value
            )
            ax = hypothesis["exponent_bias"]
            for _ in range(32):
                if magnitude & 0x80000000:
                    break
                magnitude = (
                    (magnitude << 1) & 0xFFFFFFFF
                    if hypothesis["shift_direction"] == "left"
                    else magnitude >> 1
                )
                ax = (ax + hypothesis["exponent_step"]) & 255
            bx, dx = magnitude & 65535, magnitude >> 16
            if hypothesis["clear_fraction_top_bit"] == (
                "negative" if negative else "positive"
            ):
                dx &= 32767
        observed = struct.unpack_from("<4H", records, index * RECORD_BYTES)
        if (ax, bx, cx, dx) == observed:
            matches += 1
    return {
        "status": "passed"
        if not conflicts and matches == len(inputs)
        else "contradicted",
        "instruction_conflicts": conflicts,
        "training_register_matches": matches,
        "training_memory_matches": len(inputs),
        "training_cases": len(inputs),
        "required_case_recall": matches / len(inputs),
        "memory_status": "passed",
        "instruction_status": "passed" if not conflicts else "contradicted",
        "counterexamples": [],
        "probability_correct": None,
        "sensitivity": None,
        "scope": "DX:AX signed integer register normalization, no memory writes; not native real type identification.",
    }


def lower_normalize_interpretation(hypothesis: dict) -> str:
    """Oracle: typed checked normalization; mirrors and interface supplied, no model source credit."""
    supported = {
        "magnitude": "signed_absolute",
        "exponent_bias": 160,
        "exponent_step": -1,
        "shift_direction": "left",
        "clear_fraction_top_bit": "positive",
        "zero_input": "preserve_cx",
    }
    if any(
        type(hypothesis.get(n)) is not type(v) or hypothesis[n] != v
        for n, v in supported.items()
    ):
        raise ValueError("unsupported normalization lowering")
    return """procedure FUN_24dd_455e;
var magnitude: Int64; exponent, originalHigh, flagByte: Word; negative: Boolean;
begin
  originalHigh := RegisterDX;
  magnitude := Int64(RegisterDX) * 65536 + RegisterAX;
  if magnitude = 0 then begin
    RegisterAX := 0; RegisterBX := 0; RegisterDX := 0; flagByte := 0;
  end else begin
    RegisterCX := (originalHigh and $ff00) or (RegisterCX and $ff);
    negative := originalHigh >= $8000;
    if negative then magnitude := Int64(4294967296) - magnitude;
    exponent := 160;
    while magnitude < Int64(2147483648) do begin
      magnitude := magnitude * 2; Dec(exponent);
    end;
    RegisterAX := exponent; RegisterBX := magnitude and $ffff;
    RegisterDX := (magnitude shr 16) and $ffff;
    if negative then flagByte := originalHigh shr 8 else begin
      RegisterDX := RegisterDX and $7fff; flagByte := RegisterDX shr 8;
    end;
  end;
  RegisterCarryFlag := False; RegisterZeroFlag := flagByte = 0;
  RegisterSP := (RegisterSP + 2) and $ffff;
end;
"""


def structured_schema(routine: str, supplied_bindings: bool = False) -> dict:
    """Oracle: single dispatch for supported interpretation formats, legacy defaults preserved."""
    if routine == "FUN_24dd_455e":
        return normalize_schema()
    if routine == "FUN_249c_0013":
        return arithmetic_schema()
    if routine == "FUN_24dd_4141":
        return packed_schema(supplied_bindings)
    return INTERPRETATION_SCHEMA


def structured_checker(routine: str) -> Callable[[dict, list[bytes], bytes], dict]:
    """Oracle: byte/full-state checker dispatch, not model-based acceptance."""
    return {
        "FUN_24dd_455e": check_normalize_interpretation,
        "FUN_249c_0013": check_arithmetic_interpretation,
        "FUN_24dd_4141": check_packed_interpretation,
    }.get(routine, check_interpretation)


def structured_lowering(routine: str, hypothesis: dict) -> str:
    """Oracle: supported human-authored lowering, unsupported routines raise explicitly."""
    return {
        "FUN_24dd_455e": lower_normalize_interpretation,
        "FUN_249c_0013": lower_arithmetic_interpretation,
        "FUN_24dd_4141": lower_packed_interpretation,
    }[routine](hypothesis)


def arithmetic_schema() -> dict:
    """Oracle: supplied byte facts with competing model arithmetic actions."""
    item = {
        "type": "object",
        "properties": {
            **{
                name: {
                    "type": "boolean"
                    if name == "truncate_before_add"
                    else "string"
                    if name == "operation"
                    else "integer",
                    "enum": values,
                }
                for name, values in ARITHMETIC_FIELDS.items()
            },
            "evidence": {
                "type": "object",
                "properties": {
                    n: {"type": "string", "const": v}
                    for n, v in ARITHMETIC_BINDINGS.items()
                },
                "required": list(ARITHMETIC_BINDINGS),
                "additionalProperties": False,
            },
        },
        "required": [*ARITHMETIC_FIELDS, "evidence"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "hypotheses": {
                "type": "array",
                "minItems": 1,
                "maxItems": 3,
                "items": item,
            }
        },
        "required": ["hypotheses"],
        "additionalProperties": False,
    }


def check_arithmetic_interpretation(
    hypothesis: dict, inputs: list[bytes], records: bytes
) -> dict:
    """Oracle: original36-byte arithmetic contract and complete declared-state training records."""
    routine = "FUN_249c_0013"
    raw = "5589e58b7e04368a85fcfe30e48bd0368a85fbfe30e4c1e00403c2368885fdfec9c20200"
    if routine_spec(routine)["bytes"] != raw or set(hypothesis) != {
        *ARITHMETIC_FIELDS,
        "evidence",
    }:
        raise ValueError("arithmetic bytes/schema differ")
    for name, values in ARITHMETIC_FIELDS.items():
        if (
            type(hypothesis[name]) is not type(values[0])
            or hypothesis[name] not in values
        ):
            raise ValueError("invalid arithmetic alternative: " + name)
    if hypothesis["evidence"] != ARITHMETIC_BINDINGS:
        raise ValueError("arithmetic supplied bindings differ")
    supported = {
        "left_cell": 0,
        "right_cell": 1,
        "shift": 4,
        "operation": "add",
        "output_cell": 2,
        "truncate_before_add": False,
    }
    conflicts = [
        {"field": n, "proposed": hypothesis[n], "required": v}
        for n, v in supported.items()
        if hypothesis[n] != v
    ]
    if (
        not inputs
        or compare(routine, inputs, records, native=True)["status"] != "passed"
    ):
        raise ValueError("arithmetic original fixture differs")
    matches, counterexamples = 0, []
    for index, data in enumerate(inputs):
        argument = struct.unpack_from("<H", data)[0]
        memory = bytearray(data[8:])
        start = argument - 0x8105
        left = memory[start + hypothesis["left_cell"]] << hypothesis["shift"]
        if hypothesis["truncate_before_add"]:
            left &= 255
        right = memory[start + hypothesis["right_cell"]]
        value = (
            left + right
            if hypothesis["operation"] == "add"
            else left | right
            if hypothesis["operation"] == "or"
            else left ^ right
        )
        memory[start + hypothesis["output_cell"]] = value & 255
        observed = records[index * RECORD_BYTES : (index + 1) * RECORD_BYTES]
        if (
            memory == observed[32:]
            and (value & 65535) == struct.unpack_from("<H", observed)[0]
        ):
            matches += 1
        elif len(counterexamples) < 3:
            counterexamples.append(
                {
                    "case": index,
                    "left": memory[start],
                    "right": right,
                    "proposed_ax": value & 65535,
                }
            )
    return {
        "status": "passed"
        if not conflicts and matches == len(inputs)
        else "contradicted",
        "instruction_conflicts": conflicts,
        "training_memory_matches": matches,
        "training_cases": len(inputs),
        "required_case_recall": matches / len(inputs),
        "memory_status": "passed" if matches == len(inputs) else "contradicted",
        "instruction_status": "passed" if not conflicts else "contradicted",
        "counterexamples": counterexamples,
        "probability_correct": None,
        "sensitivity": None,
        "scope": "Original SS-byte projection and AX arithmetic; not native pointer ABI.",
    }


def lower_arithmetic_interpretation(hypothesis: dict) -> str:
    """Oracle: typed human renderer of checked model arithmetic, not generated Pascal credit."""
    supported = {
        "left_cell": 0,
        "right_cell": 1,
        "shift": 4,
        "operation": "add",
        "output_cell": 2,
        "truncate_before_add": False,
    }
    if any(
        type(hypothesis.get(n)) is not type(v) or hypothesis[n] != v
        for n, v in supported.items()
    ):
        raise ValueError("unsupported arithmetic lowering")
    return """procedure FUN_249c_0013(param_1: Word; param_2: Pointer);
var p: PByte; value: LongInt;
begin
  p := PByte(param_2);
  value := (LongInt(p[0]) shl 4) + p[1];
  RegisterAX := value; RegisterDX := p[1]; RegisterDI := param_1;
  p[2] := value and 255;
  RegisterCarryFlag := False; RegisterZeroFlag := value = 0;
  RegisterSP := (RegisterSP + 4) and 65535;
end;
"""


def interpretation_prompt(root: pathlib.Path, routine: str = "FUN_24dd_48e1") -> str:
    """Oracle: alternative vocabulary is assistance, not a supplied solution."""
    if routine == "FUN_24dd_455e":
        return (
            "Interpret register normalization only, not Pascal. Propose1-3 competing hypotheses. "
            "Input integer register pair DX:AX; BX, CX and output exponent/fraction are observable. "
            "Infer signed magnitude handling,32-bit shift direction, general exponent bias and decrement/increment, "
            "fraction high bit treatment according to input sign and CX preservation on zero. "
            "Describe equivalent semantics of word/byte fast paths, not just the small-word branch.\n"
            + instruction_listing(root, routine)
            + "\nOriginal bytes:"
            + routine_spec(routine)["bytes"]
            + "\nCopy supplied instruction evidence exactly:"
            + json.dumps(NORMALIZE_BINDINGS)
        )
    if routine == "FUN_249c_0013":
        return (
            "Interpret byte arithmetic only, not Pascal. Propose1-3 competing hypotheses "
            "from original instructions. Cell0=SS:[argument-261], cell1=SS:[argument-260], "
            "cell2=SS:[argument-259]. Choose shifted left cell, right cell, shift, operation, "
            "output cell and whether truncation occurs before addition. AX remains16bit; "
            "memory stores one byte. Human interface/bindings supplied, no action tuple.\n"
            + instruction_listing(root, routine)
            + "\nOriginal bytes:"
            + routine_spec(routine)["bytes"]
            + "\nCopy these supplied byte-backed evidence strings exactly:"
            + json.dumps(ARITHMETIC_BINDINGS)
        )
    if routine == "FUN_24dd_4141":
        return (
            "Interpret memory actions only, no Pascal. Propose1-3 competing hypotheses in "
            "the JSON schema. argument is the original unsigned packed Word from SS; source/"
            "destination origins come from LDS/LES. Choose source/destination starting index, "
            "repeat count, step, access order and zero-count access from original instructions. "
            "Do not use conventional memmove assumptions. Evidence must explicitly cite each "
            "relevant instruction address: source_start for count setup and ADD SI; count for "
            "final MOV CL; transfer for direction setup and REP. No certainty percentage.\n"
            + instruction_listing(root, routine)
            + "\nOriginal bytes: "
            + routine_spec(routine)["bytes"]
        )
    return (
        "Interpret only memory actions, not Pascal. Propose 1-3 competing hypotheses "
        "in the required JSON schema. source/destination are resolved host pointer "
        "origins from LDS/LES; count is unsigned CX. Explain the traversal by choosing "
        "condition (when backward setup executes), zero_count memory access, each "
        "branch's starting byte index and per-byte step, access_order and repeat. "
        "Evidence fields must cite exact original instruction addresses: branch for "
        "CMP/JNC, setup for ADD/DEC/STD, transfer for REP MOVSB/CLD. "
        "Do not infer traversal from conventional memmove behavior; use bytes. "
        "No source body or certainty percentage is requested.\n"
        + instruction_listing(root, "FUN_24dd_48e1")
        + "\nOriginal bytes: "
        + PANEL["FUN_24dd_48e1"]["bytes"]
    )


def check_interpretation(hypothesis: dict, inputs: list[bytes], records: bytes) -> dict:
    """Oracle: exact instruction constraints plus original training memory, no holdout."""
    if bytes.fromhex(PANEL["FUN_24dd_48e1"]["bytes"]) != INTERPRETATION_BYTES:
        raise ValueError("interpretation byte identity changed")
    output_obligations("FUN_24dd_48e1", bytes.fromhex(PANEL["FUN_24dd_48e1"]["bytes"]))
    if set(hypothesis) != {*INTERPRETATION_FIELDS, "evidence"}:
        raise ValueError("interpretation fields differ from frozen schema")
    for name, values in INTERPRETATION_FIELDS.items():
        if (
            type(hypothesis[name]) is not type(values[0])
            or hypothesis[name] not in values
        ):
            raise ValueError("invalid interpretation alternative: " + name)
    if set(hypothesis["evidence"]) != {"branch", "setup", "transfer"} or any(
        not isinstance(value, str) for value in hypothesis["evidence"].values()
    ):
        raise ValueError("interpretation evidence is incomplete")
    required = {
        "condition": ("source_lt_destination", "48f2/48f4:3bf77307"),
        "zero_count": ("no_access", "48fd:f3a4"),
        "forward_start": ("zero", "48f4:7307 skips setup"),
        "backward_start": ("count_minus_one", "48f6..48fb:03f103f94e4f"),
        "forward_step": (1, "48f1:fc"),
        "backward_step": (-1, "48fc:fd"),
        "access_order": ("copy_then_step", "48fd:f3a4 x86 string instruction"),
        "repeat": ("count_times", "48fd:f3a4"),
    }
    conflicts = [
        {
            "field": name,
            "proposed": hypothesis[name],
            "required": value,
            "evidence": evidence,
        }
        for name, (value, evidence) in required.items()
        if hypothesis[name] != value
    ]
    for name, addresses in {
        "branch": ("48f2", "48f4"),
        "setup": ("48f6", "48fa", "48fc"),
        "transfer": ("48fd",),
    }.items():
        if any(
            address not in hypothesis["evidence"][name].lower() for address in addresses
        ):
            conflicts.append(
                {"field": "evidence." + name, "required_addresses": list(addresses)}
            )
    if len(records) != len(inputs) * RECORD_BYTES:
        raise ValueError("interpretation original record shape differs")
    if (
        not inputs
        or compare("FUN_24dd_48e1", inputs, records, native=True)["status"] != "passed"
    ):
        raise ValueError(
            "interpretation original training does not satisfy complete fixture"
        )
    matches, counterexamples = 0, []
    for index, data in enumerate(inputs):
        count, source, destination, _ = struct.unpack_from("<4H", data)
        backward = (
            source < destination
            if hypothesis["condition"] == "source_lt_destination"
            else source >= destination
        )
        branch = "backward" if backward else "forward"
        start = 0 if hypothesis[branch + "_start"] == "zero" else count - 1
        step = hypothesis[branch + "_step"]
        memory = bytearray(data[8:])
        iterations = count + (hypothesis["repeat"] == "count_plus_one")
        if count == 0:
            iterations = int(hypothesis["zero_count"] == "one_access")
        valid = True
        for iteration in range(iterations):
            offset = start + step * (
                iteration + (hypothesis["access_order"] == "step_then_copy")
            )
            src, dst = source - 0x8000 + offset, destination - 0x8000 + offset
            if not (0 <= src < ARENA and 0 <= dst < ARENA):
                valid = False
                break
            memory[dst] = memory[src]
        observed = records[index * RECORD_BYTES + 32 : (index + 1) * RECORD_BYTES]
        if valid and memory == observed:
            matches += 1
        elif len(counterexamples) < 3:
            counterexamples.append(
                {
                    "case": index,
                    "count": count,
                    "source": source,
                    "destination": destination,
                    "out_of_bounds": not valid,
                    "differing_offsets": [
                        i for i, (a, b) in enumerate(zip(memory, observed)) if a != b
                    ][:8],
                }
            )
    return {
        "status": "passed"
        if not conflicts and matches == len(inputs)
        else "contradicted",
        "instruction_conflicts": conflicts,
        "training_memory_matches": matches,
        "training_cases": len(inputs),
        "required_case_recall": matches / len(inputs),
        "memory_status": "passed" if matches == len(inputs) else "contradicted",
        "instruction_status": "passed" if not conflicts else "contradicted",
        "counterexamples": counterexamples,
        "probability_correct": None,
        "sensitivity": None,
        "scope": "Checked enumerated memory interpretation on original training; not source/native ABI acceptance.",
    }


def interpret_memory(
    root: pathlib.Path,
    output: pathlib.Path,
    model: str,
    endpoint: str,
    inputs: list[bytes],
    records: bytes,
    routine: str = "FUN_24dd_48e1",
    supplied_bindings: bool = False,
    thinking: bool = False,
) -> dict:
    """Oracle: bounded interpretation/repair, retain alternatives without circular confidence."""
    output.mkdir()
    text = interpretation_prompt(root, routine)
    schema = structured_schema(routine, supplied_bindings)
    if supplied_bindings:
        text += (
            "\nHuman-supplied original-byte instruction bindings; not model-discovered evidence. "
            "Copy these evidence strings exactly; infer all six action fields yourself. "
            "No Pascal body or accepted action tuple is supplied:\n"
            + json.dumps(PACKED_BINDINGS)
        )
    checker = structured_checker(routine)
    history, seen = [], set()
    selected = None
    for number in (1, 2):
        (output / f"prompt-{number}.txt").write_text(text)
        try:
            response = (
                pilot.request(
                    text,
                    model,
                    endpoint,
                    schema=schema,
                    max_generated_tokens=8192,
                    think=True,
                )
                if thinking
                else (
                    pilot.request(
                        text, model, endpoint, schema=schema, max_generated_tokens=4096
                    )
                    if routine == "FUN_24dd_4141"
                    else pilot.request(text, model, endpoint, schema=schema)
                )
            )
            (output / f"response-{number}.json").write_text(response)
            proposal = json.loads(json.loads(response)["response"])
            if (
                set(proposal) != {"hypotheses"}
                or not 1 <= len(proposal["hypotheses"]) <= 3
            ):
                raise ValueError("expected one to three interpretation hypotheses")
            attempts = []
            for hypothesis in proposal["hypotheses"]:
                if supplied_bindings and hypothesis.get("evidence") != PACKED_BINDINGS:
                    raise ValueError(
                        "proposal differs from supplied original-byte bindings"
                    )
                identity = hashlib.sha256(
                    json.dumps(hypothesis, sort_keys=True).encode()
                ).hexdigest()
                assessment = checker(hypothesis, inputs, records)
                attempts.append(
                    {
                        "hypothesis": hypothesis,
                        "assessment": assessment,
                        "duplicate": identity in seen,
                    }
                )
                seen.add(identity)
                if assessment["status"] == "passed" and selected is None:
                    selected = hypothesis
            result = {"attempt": number, "hypotheses": attempts}
        except (
            ValueError,
            KeyError,
            TypeError,
            urllib.error.URLError,
            TimeoutError,
        ) as error:
            result = {
                "attempt": number,
                "status": "interpretation-proposal-failed",
                "error": str(error),
            }
        history.append(result)
        pilot.save(output / "history.json", history)
        if selected is not None:
            break
        text += (
            "\nTraining-only contradictions; revise memory interpretation:\n"
            + json.dumps(result)
        )
    result = {
        "status": "passed" if selected else "blocked",
        "selected": selected,
        "history": history,
        "model_requests": len(history),
    }
    pilot.save(output / "result.json", result)
    return result


BINDING_SCHEMA = INTERPRETATION_SCHEMA["properties"]["hypotheses"]["items"][
    "properties"
]["evidence"]


def binding_context(root: pathlib.Path, predecessor: pathlib.Path) -> dict:
    """Oracle: authenticated prior training hypothesis, no new memory discovery."""
    result = validate_artifacts(root, predecessor, historical=True)
    frozen = json.loads((predecessor / "freeze.json").read_text())
    if frozen.get("binding_completion") or not frozen.get("interpretation_first"):
        raise ValueError(
            "binding completion requires an initial interpretation archive"
        )
    if any(record["terminal"] is not None for record in result["routines"].values()):
        raise ValueError(
            "binding completion cannot consume evaluated terminal outcomes"
        )
    if len(result["routines"]) != 1 or next(iter(result["routines"])) not in (
        "FUN_24dd_48e1",
        "FUN_24dd_4141",
    ):
        raise ValueError("binding completion requires a single supported copy routine")
    routine = next(iter(result["routines"]))
    checker = (
        check_packed_interpretation
        if routine == "FUN_24dd_4141"
        else check_interpretation
    )
    interpretation = result["routines"][routine]["interpretation"]
    if interpretation["status"] != "blocked":
        raise ValueError(
            "binding completion requires a previously blocked interpretation"
        )
    inputs = cases(routine, "training")
    records = (predecessor / routine / "original-training/TRACE.BIN").read_bytes()
    for proposal in interpretation["history"]:
        for index, alternative in enumerate(proposal.get("hypotheses", [])):
            hypothesis = alternative["hypothesis"]
            assessment = checker(hypothesis, inputs, records)
            conflicts = assessment["instruction_conflicts"]
            if (
                assessment["memory_status"] == "passed"
                and conflicts
                and all(
                    conflict["field"].startswith("evidence.") for conflict in conflicts
                )
            ):
                return {
                    **({"routine": routine} if routine == "FUN_24dd_4141" else {}),
                    "path": str(predecessor.resolve()),
                    "artifacts_sha256": pilot.digest(predecessor / "artifacts.json"),
                    "result_sha256": pilot.digest(predecessor / "result.json"),
                    "attempt": proposal["attempt"],
                    "hypothesis_index": index,
                    "hypothesis": hypothesis,
                    "assessment": assessment,
                    "disclosure": (
                        "First prior training-memory-matching, action-compatible hypothesis; "
                        "only evidence fields may change. Reused support is not independent "
                        "discovery. Completion prompt supplies citation obligations."
                    ),
                }
    raise ValueError(
        "no prior action-compatible hypothesis with only citation conflicts"
    )


def binding_prompt(root: pathlib.Path, context: dict) -> str:
    """Oracle: fixed prior memory actions and disclosed citation-completion assistance."""
    routine = context.get("routine", "FUN_24dd_48e1")
    names = (
        "source_start, count, transfer"
        if routine == "FUN_24dd_4141"
        else "branch, setup, transfer"
    )
    return (
        "Complete instruction citations only; do not generate Pascal or change memory actions. "
        f"Return the JSON object with {names} evidence strings. "
        "Cite each required instruction address explicitly, not an address range. "
        "Use the original bytes and listing below; explain each cited instruction's role. "
        "This is evidence completion of an existing training-memory-matching hypothesis, "
        "not a new semantic discovery or correctness probability.\n"
        "Immutable prior hypothesis:\n"
        + json.dumps(context["hypothesis"])
        + "\nTraining-only missing citation obligations:\n"
        + json.dumps(context["assessment"]["instruction_conflicts"])
        + "\n"
        + instruction_listing(root, routine)
        + "\nOriginal bytes: "
        + routine_spec(routine)["bytes"]
    )


def complete_binding(
    output: pathlib.Path,
    model: str,
    endpoint: str,
    text: str,
    context: dict,
    inputs: list[bytes],
    records: bytes,
) -> dict:
    """Oracle: one evidence-only request, unchanged actions/checker, no holdout feedback."""
    output.mkdir()
    (output / "prompt-1.txt").write_text(text)
    selected = None
    routine = context.get("routine", "FUN_24dd_48e1")
    schema = (
        PACKED_SCHEMA["properties"]["hypotheses"]["items"]["properties"]["evidence"]
        if routine == "FUN_24dd_4141"
        else BINDING_SCHEMA
    )
    checker = (
        check_packed_interpretation
        if routine == "FUN_24dd_4141"
        else check_interpretation
    )
    try:
        response = pilot.request(text, model, endpoint, schema=schema)
        (output / "response-1.json").write_text(response)
        evidence = json.loads(json.loads(response)["response"])
        hypothesis = {**context["hypothesis"], "evidence": evidence}
        assessment = checker(hypothesis, inputs, records)
        proposal = {
            "attempt": 1,
            "hypotheses": [
                {"hypothesis": hypothesis, "assessment": assessment, "duplicate": False}
            ],
        }
        if assessment["status"] == "passed":
            selected = hypothesis
    except (
        ValueError,
        KeyError,
        TypeError,
        urllib.error.URLError,
        TimeoutError,
    ) as error:
        proposal = {
            "attempt": 1,
            "status": "binding-proposal-failed",
            "error": str(error),
        }
    result = {
        "status": "passed" if selected else "blocked",
        "selected": selected,
        "history": [proposal],
        "model_requests": 1,
        "binding_only": True,
    }
    pilot.save(output / "history.json", result["history"])
    pilot.save(output / "result.json", result)
    return result


def lowering_context(root: pathlib.Path, predecessor: pathlib.Path) -> dict:
    """Oracle: authenticated selected interpretation, no terminal-feedback reuse."""
    result = validate_artifacts(root, predecessor, historical=True)
    frozen = json.loads((predecessor / "freeze.json").read_text())
    if frozen.get("mechanical_lowering"):
        raise ValueError(
            "lowering requires an interpretation archive, not a lowering retry"
        )
    if set(result["routines"]) != {"FUN_24dd_48e1"}:
        raise ValueError("lowering requires the single48e1 panel")
    record = result["routines"]["FUN_24dd_48e1"]
    if record["terminal"] is not None:
        raise ValueError("lowering cannot consume evaluated terminal outcomes")
    interpretation = record.get("interpretation")
    if not interpretation or interpretation["status"] != "passed":
        raise ValueError("lowering requires a selected checked interpretation")
    hypothesis = interpretation["selected"]
    assessment = check_interpretation(
        hypothesis,
        cases("FUN_24dd_48e1", "training"),
        (predecessor / "FUN_24dd_48e1/original-training/TRACE.BIN").read_bytes(),
    )
    if assessment["status"] != "passed":
        raise ValueError("selected interpretation no longer satisfies its contract")
    return {
        "path": str(predecessor.resolve()),
        "artifacts_sha256": pilot.digest(predecessor / "artifacts.json"),
        "result_sha256": pilot.digest(predecessor / "result.json"),
        "hypothesis": hypothesis,
        "assessment": assessment,
        "origin_model": frozen["model"],
        "disclosure": "Human-authored typed lowering of a prior model interpretation; not model-generated Pascal or weight improvement.",
    }


def lower_interpretation(hypothesis: dict) -> str:
    """Oracle: typed mechanical lowering of the supported checked48e1 action contract."""
    supported = {
        "condition": "source_lt_destination",
        "zero_count": "no_access",
        "forward_start": "zero",
        "backward_start": "count_minus_one",
        "forward_step": 1,
        "backward_step": -1,
        "access_order": "copy_then_step",
        "repeat": "count_times",
    }
    if any(
        type(hypothesis.get(name)) is not type(value) or hypothesis[name] != value
        for name, value in supported.items()
    ):
        raise ValueError("unsupported memory interpretation for typed lowering")
    return """var src, dst: PByte; i: LongInt;
begin
  src := PByte(source);
  dst := PByte(destination);
  if backward then begin
    for i := LongInt(count) - 1 downto 0 do
      dst[i] := src[i];
  end else begin
    for i := 0 to LongInt(count) - 1 do
      dst[i] := src[i];
  end;
end;
"""


def synthetic_residual_dataset(output: pathlib.Path) -> list[dict]:
    """Oracle: FPC compiler-backed synthetic pairs, never Liero gold source."""
    output.mkdir(parents=True, exist_ok=False)
    examples = []
    for operation in ("xor", "and", "+", "or"):
        for value in (1, 3, 7, 15, 31, 63, 127, 255):
            directory = output / f"{operation.replace('+', 'add')}-{value}"
            directory.mkdir()
            body = f"""var p: PByte; i: LongInt;
begin
  p := PByte(destination);
  for i := 1 to count do begin
    p^ := (p^ {operation} {value}) and 255; Inc(p);
  end;
end;"""
            program_source = f"""program Synthetic;
type PByte = ^Byte;
procedure MemoryBody(count: Word; source, destination: Pointer; backward: Boolean);
{body}
var data: array[0..255] of Byte; i: Integer;
begin
  for i := 0 to 255 do data[i] := i;
  MemoryBody(256, nil, @data, False);
  for i := 0 to 255 do WriteLn(data[i]);
end.
"""
            source = directory / "synthetic.pas"
            source.write_text(program_source)
            build = subprocess.run(
                [
                    "fpc",
                    "-O1",
                    "-al",
                    "-a",
                    str(source),
                    "-FE" + str(directory),
                    "-FU" + str(directory),
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            (directory / "compile.log").write_text(build.stdout + build.stderr)
            if build.returncode:
                raise RuntimeError("synthetic compile failed: " + str(directory))
            execution = subprocess.run(
                [str(directory / "synthetic")],
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            actual = [int(row) for row in execution.stdout.splitlines()]
            expected_values = [
                (i ^ value)
                if operation == "xor"
                else (i & value)
                if operation == "and"
                else (i + value) & 255
                if operation == "+"
                else i | value
                for i in range(256)
            ]
            if actual != expected_values:
                raise ValueError("synthetic execution disagrees: " + str(directory))
            (directory / "observations.json").write_text(json.dumps(actual))
            assembly = (directory / "synthetic.s").read_text()
            match = re.search(
                r"(?m)^P\$SYNTHETIC_\$\$_MEMORYBODY[^\n]*:\n([\s\S]*?)\.size", assembly
            )
            if match is None:
                raise ValueError("compiler listing lacks isolated MemoryBody")
            instructions = "\n".join(
                line.strip()
                for line in match[1].splitlines()
                if line.startswith("\t") and not line.lstrip().startswith((".", "#"))
            )
            text = (
                "Compiler-backed synthetic x86_64 FPC memory routine, not TurboPascal7. "
                "Infer the memory behavior from these compiler instructions. Output only "
                "declaration-free Pascal var/begin/end; body for MemoryBody(count: Word; "
                "source, destination: Pointer; backward: Boolean). Use host PByte pointers, "
                "no units, assembler or Register symbols. No JSON or markdown.\n"
                + instructions
            )
            examples.append(
                {
                    "target": "synthetic-development-or"
                    if operation == "or"
                    else "synthetic-training",
                    "family": operation,
                    "task": "synthetic_residual",
                    "trust_status": "compiler-backed-synthetic",
                    "source_type": "synthetic-fpc-x86_64",
                    "prompt": text,
                    "completion": body,
                    "source_sha256": pilot.digest(source),
                    "assembly_sha256": pilot.digest(directory / "synthetic.s"),
                    "oracle": "FPC compile plus all256 byte values under supplied arena",
                }
            )
    pilot.save(output / "dataset.json", examples)
    return examples


def proposal_assessment(attempt: dict) -> dict:
    """Oracle: measured fixture recall, not a probability of routine correctness."""
    evaluated = attempt.get("cases", 0)
    matches = attempt.get("matches", 0)
    return {
        "probability_correct": None,
        "probability_reason": "No independently calibrated estimator of whole-routine correctness.",
        "required_case_recall": matches / evaluated if evaluated else None,
        "matched_required_cases": matches if evaluated else None,
        "evaluated_required_cases": evaluated,
        "metric_scope": "Complete-state agreement on the declared deterministic fixture corpus; not statistical population recall or sensitivity.",
        "sensitivity": None,
        "sensitivity_reason": "No labeled positive/negative behavioral classification corpus.",
        "source_review": "pending" if attempt["status"] == "passed" else "not_eligible",
    }


def finalize_rejected_local_trial(output: pathlib.Path) -> dict:
    """Oracle: recover rejected-run bookkeeping only; never execute or promote."""
    if (output / "result.json").exists():
        raise ValueError("refuse to replace a finalized trial")
    frozen = json.loads((output / "freeze.json").read_text())
    hashes = frozen["model"].get("file_hashes")
    if not hashes or any(
        pilot.digest(pathlib.Path(path)) != digest for path, digest in hashes.items()
    ):
        raise ValueError("local model identity missing or changed")
    for name, digest in frozen["source_hashes"].items():
        if pilot.digest(output / "sources" / pathlib.Path(name).name) != digest:
            raise ValueError("archived method snapshot changed")
    records = {}
    for routine in frozen["regions"]:
        record = json.loads((output / routine / "selection.json").read_text())
        if record["selected"] is not None or record["terminal"] is not None:
            raise ValueError("bookkeeping repair supports rejected candidates only")
        if any(
            attempt["status"] in {"passed", "failed"} for attempt in record["attempts"]
        ):
            raise ValueError(
                "bookkeeping repair must not reinterpret executed candidates"
            )
        directory = output / routine / "original-training"
        inputs = cases(routine, "training")
        if (directory / "CASES.BIN").read_bytes() != b"".join(inputs) or compare(
            routine, inputs, (directory / "TRACE.BIN").read_bytes(), native=True
        )["status"] != "passed":
            raise ValueError("saved original training evidence differs")
        records[routine] = record
    result = {
        "routines": records,
        "attempted_routines": len(records),
        "binary_terminal_passes": 0,
        "accepted_source_recoveries": 0,
        "source_review_required": True,
        "examples_promoted": 0,
        "weights_changed": False,
        "model_requests": sum(
            sum(attempt.get("model_request", True) for attempt in record["attempts"])
            + record.get("interpretation", {}).get("model_requests", 0)
            for record in records.values()
        ),
        "frontier_status": "stopped-below-yield-floor",
        "finalization_repair": "Archived local-weight identities checked instead of incorrect Ollama identity comparison. No new generation, execution, selection or feedback.",
    }
    pilot.save(output / "result.json", result)
    seal_archive(output)
    return result


def evaluate_synthetic_residual(
    dataset: pathlib.Path, output: pathlib.Path, example: dict, body: str
) -> dict:
    """Oracle: retained compiler-backed byte cases, not original Liero parity."""
    output.mkdir(parents=True, exist_ok=False)
    (output / "proposal.inc").write_text(body)
    try:
        compose_residual(body)
    except ValueError as error:
        return {"status": "representation-rejected", "error": str(error)}
    sources = [
        path
        for path in dataset.glob("*/synthetic.pas")
        if pilot.digest(path) == example["source_sha256"]
    ]
    if len(sources) != 1:
        raise ValueError("synthetic source identity is not unique")
    original = sources[0].read_text()
    if original.count(example["completion"]) != 1:
        raise ValueError("synthetic completion differs from compiler source")
    source = output / "synthetic.pas"
    source.write_text(original.replace(example["completion"], body))
    build = subprocess.run(
        ["fpc", str(source), "-FE" + str(output), "-FU" + str(output)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    (output / "compile.log").write_text(build.stdout + build.stderr)
    if build.returncode:
        return {"status": "compile-failed"}
    execution = subprocess.run(
        [str(output / "synthetic")],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    (output / "execution.txt").write_text(execution.stdout + execution.stderr)
    if execution.returncode:
        return {"status": "runtime-failed", "exit_code": execution.returncode}
    actual = [int(row) for row in execution.stdout.splitlines()]
    expected_values = json.loads((sources[0].parent / "observations.json").read_text())
    if len(actual) != len(expected_values):
        return {"status": "shape-failed"}
    matches = sum(a == b for a, b in zip(actual, expected_values))
    return {
        "status": "passed" if matches == len(actual) else "failed",
        "cases": len(actual),
        "matches": matches,
        "required_case_recall": matches / len(actual),
        "probability_correct": None,
        "scope": "Synthetic byte-value agreement at supplied count256, not complete Liero state.",
    }


def training_state_feedback(routine: str, inputs: list[bytes], data: bytes) -> dict:
    """Oracle: named training-only counterexamples, no terminal inputs or source rewriting."""
    if len(data) != len(inputs) * RECORD_BYTES:
        raise ValueError("incomplete training feedback output")
    names = (
        "AX",
        "BX",
        "CX",
        "DX",
        "SI",
        "DI",
        "BP",
        "entrySP",
        "returnSP",
        "DS",
        "ES",
        "SS",
        "flagsCF/ZF/DF",
        "guard0",
        "guard1",
        "fixtureCS",
    )
    examples = []
    for index, inputs_row in enumerate(inputs):
        row = data[index * RECORD_BYTES : (index + 1) * RECORD_BYTES]
        want = expected(routine, inputs_row, 0x2000)
        actual_words = list(struct.unpack_from("<16H", row))
        expected_words = list(struct.unpack_from("<16H", want))
        actual_words[12] &= 0x441
        expected_words[12] &= 0x441
        differences = {
            name: {"actual": actual, "expected": expected}
            for name, actual, expected in zip(
                names, actual_words, expected_words, strict=True
            )
            if actual != expected
        }
        memory = [i for i in range(ARENA) if row[32 + i] != want[32 + i]]
        if differences or memory:
            examples.append(
                {
                    "training_case": index,
                    "input_words": list(struct.unpack_from("<4H", inputs_row)),
                    "state": differences,
                    "first_arena_offsets": memory[:8],
                }
            )
        if len(examples) == 3:
            break
    return {"oracle": "training-only complete declared state", "examples": examples}


def freeze(
    root: pathlib.Path,
    output: pathlib.Path,
    model: str,
    endpoint: str,
    training_from: pathlib.Path | None = None,
    calibration_from: pathlib.Path | None = None,
    routines: tuple[str, ...] | None = None,
    enforce_outputs: bool = False,
    residual: bool = False,
    local_base: pathlib.Path | None = None,
    local_adapter: pathlib.Path | None = None,
    interpretation_first: bool = False,
    binding_from: pathlib.Path | None = None,
    lowering_from: pathlib.Path | None = None,
    typed_memory_guidance: bool = False,
    supplied_bindings: bool = False,
    thinking: bool = False,
) -> dict:
    """Oracle: freeze binary, source disclosure, suites, methods and local model before runs."""
    selected = tuple(PANEL) if routines is None else routines
    if (
        thinking
        and selected not in (("FUN_249c_0013",), ("FUN_24dd_455e",))
        and (
            selected != ("FUN_24dd_4141",)
            or not interpretation_first
            or binding_from
            or not residual
            or local_base
        )
    ):
        raise ValueError("thinking requires fresh single4141 interpretation residual")
    if supplied_bindings and (
        selected != ("FUN_24dd_4141",)
        or not interpretation_first
        or binding_from
        or lowering_from
        or not residual
        or local_base
        or not enforce_outputs
    ):
        raise ValueError(
            "supplied bindings require fresh single4141 interpretation residual"
        )
    if selected == ("FUN_24dd_4141",) and (lowering_from or local_base):
        raise ValueError("4141 residual supports Ollama memory-body generation only")
    if typed_memory_guidance and (
        selected != ("FUN_24dd_4141",)
        or not enforce_outputs
        or residual
        or local_base
        or interpretation_first
        or binding_from
        or lowering_from
    ):
        raise ValueError(
            "typed memory guidance requires Ollama single4141 with output obligations"
        )
    lowering = None
    if lowering_from is not None:
        if (
            not residual
            or interpretation_first
            or binding_from
            or local_base
            or calibration_from
            or training_from is None
            or training_from.resolve() != lowering_from.resolve()
        ):
            raise ValueError(
                "lowering requires residual with training from the same archive and no inference modes"
            )
        lowering = lowering_context(root, lowering_from)
    if interpretation_first and (
        (not residual and selected not in (("FUN_249c_0013",), ("FUN_24dd_455e",)))
        or local_base
        or calibration_from
    ):
        raise ValueError(
            "interpretation-first requires Ollama supported residual without calibration"
        )
    if selected == ("FUN_24dd_455e",) and (
        not interpretation_first or not enforce_outputs or binding_from or lowering_from
    ):
        raise ValueError(
            "normalization requires fresh checked interpretation and output enforcement"
        )
    binding = None
    if binding_from is not None:
        if (
            not interpretation_first
            or training_from is None
            or training_from.resolve() != binding_from.resolve()
        ):
            raise ValueError(
                "binding completion requires interpretation-first and training from the same archive"
            )
        binding = binding_context(root, binding_from)
        if binding.get("routine", "FUN_24dd_48e1") != selected[0]:
            raise ValueError("binding predecessor routine differs")
    if residual and selected not in (("FUN_24dd_48e1",), ("FUN_24dd_4141",)):
        raise ValueError("residual requires a single supported copy routine")
    if (
        not selected
        or len(set(selected)) != len(selected)
        or any(n not in {*PANEL, *DISCOVERY_PANEL} for n in selected)
    ):
        raise ValueError("invalid source trial panel")
    context = (
        "" if calibration_from is None else calibration_context(root, calibration_from)
    )
    if calibration_from is not None and training_from is None:
        raise ValueError("calibrated recovery requires authenticated training replay")
    manifest = json.loads((root / "targets/liero/alternate_streams.json").read_text())
    binary, header, base, identity = load_binary_evidence(
        root / "targets/liero", manifest
    )
    regions = {}
    for routine in selected:
        spec = routine_spec(routine)
        offset = header + (spec.get("segment", 0x24DD) - base) * 16 + spec["offset"]
        raw = bytes.fromhex(spec["bytes"])
        if binary[offset : offset + len(raw)] != raw or any(
            offset - 1 <= r < offset + len(raw)
            for r in _mz_relocation_locations(binary, header)
        ):
            raise ValueError("original leaf bytes/relocations disagree")
        regions[routine] = {"file_offset": offset, "bytes_hex": raw.hex()}
    paths = [
        pathlib.Path(__file__),
        root / "engine/evidence_archive.py",
        root / "tools/liero_four_routine_pilot.py",
        root / "tools/liero_file_probe.py",
        root / "engine/alternate_streams.py",
        root / "engine/routine_contract.py",
        root / "targets/liero/src/LieroRuntime.pas",
        root / "tests/test_liero_source_trial.py",
    ]
    if local_base:
        if not residual:
            raise ValueError("explicit local training inference requires residual mode")
        paths += [root / "engine/model_adapter.py"]
    paths += [
        root / f"targets/liero/{kind}/{routine}.{extension}"
        for routine in selected
        for kind, extension in (("src", "inc"), ("asm", "s"))
    ]
    output.mkdir(parents=True, exist_ok=False)
    (output / "sources").mkdir()
    for path in paths:
        shutil.copy2(path, output / "sources" / path.name)
    result = {
        "model": (
            {"kind": "mechanical-lowering", "origin_model": lowering["origin_model"]}
            if lowering is not None
            else (
                {
                    "name": str(local_base.resolve()),
                    "adapter": str(local_adapter.resolve()) if local_adapter else None,
                    "file_hashes": {
                        str(path.resolve()): pilot.digest(path)
                        for directory in (
                            [local_base] + ([local_adapter] if local_adapter else [])
                        )
                        for path in sorted(directory.iterdir())
                        if path.suffix in {".json", ".safetensors"}
                    },
                }
                if local_base
                else pilot.leaf_model_identity(model, endpoint)
            )
        ),
        "binary_sha256": identity,
        "regions": regions,
        "scope": SCOPE,
        "prior_knowledge": "Both routines already have manual unreviewed Pascal drafts and host tests. Bodies/decompiler withheld from prompts; not an unseen-routine/generalization benchmark.",
        "strategy": (
            "v2: explicit host-pointer representation; no supplied target body or loop topology"
            if calibration_from is None
            else "v3: reviewed known-source adapter examples; no supplied target body or loop topology"
        ),
        "calibration": None
        if calibration_from is None
        else {
            "path": str(calibration_from),
            "review_sha256": pilot.digest(calibration_from / "review.json"),
            "artifacts_sha256": pilot.digest(calibration_from / "artifacts.json"),
            "disclosure": "v3: supplied known-source adapter examples; not unseen recovery or weights",
        },
        "predecessor": None
        if training_from is None
        else {
            "path": str(training_from),
            "artifacts_sha256": pilot.digest(training_from / "artifacts.json"),
            "result_sha256": pilot.digest(training_from / "result.json"),
            "training_only_feedback": True,
            "replayed_evidence_is_not_independent": True,
        },
        "budgets": {
            "attempts_per_routine": 2,
            "repairs_per_routine": 1,
            "terminal_evaluations_per_selected": 1,
            "model_timeout_seconds": 600,
            "subprocess_timeout_seconds": 30,
            "temperature": 0,
            "maximum_generated_tokens": 2048,
            "yield_floor": 0.25,
            "batch_size": len(selected),
        },
        "policy": "First complete training pass selected; terminal once, no terminal feedback/repair. Deduplicate candidates per routine. Stop expansion if accepted/attempted <25%. Never install/promote/train automatically.",
        "source_hashes": {str(p.relative_to(root)): pilot.digest(p) for p in paths},
        "prompt_hashes": {
            routine: hashlib.sha256(
                (
                    residual_prompt(root, routine, structured=local_base is None)
                    if residual
                    else trial_prompt(
                        root, routine, context, enforce_outputs, typed_memory_guidance
                    )
                ).encode()
            ).hexdigest()
            for routine in selected
        },
        "corpora": {
            routine: {
                suite: hashlib.sha256(b"".join(cases(routine, suite))).hexdigest()
                for suite in ("training", "terminal")
            }
            for routine in selected
        },
        "output_obligations": {
            n: output_obligations(n, bytes.fromhex(routine_spec(n)["bytes"]))
            for n in selected
        }
        if enforce_outputs
        else None,
    }
    if typed_memory_guidance:
        result["strategy"] = (
            "v9: typed memory representation guidance and4096token budget; no supplied target body"
        )
        result["typed_memory_guidance"] = True
        result["budgets"]["maximum_generated_tokens"] = 4096
    if selected == ("FUN_24dd_48e1",):
        result["prior_knowledge"] = (
            "48e1 has no implemented Pascal body, source review or host test before "
            "this milestone. A developer-written fixture control exists in the "
            "trial tests but is withheld from prompts. Human read its listing/"
            "decompiler to scope the experiment; "
            "neither decompiler nor a supplied target body/loop is sent to model. "
            "Byte-backed output obligations and host representation are supplied. "
            "Implementation-unresolved assisted PoC, not a blind benchmark."
        )
    if selected == ("FUN_24dd_4141",):
        result["prior_knowledge"] = (
            "4141 is a callee-free implementation-unresolved leaf selected by original-byte "
            "full census triage. Human reviewed bytes/listing/decompiler to define fixture "
            "and exact signature; supplied packed-word/ABI constraints are assistance. "
            "No installed body, no blind-discovery or untouched-generalization claim."
        )
    if enforce_outputs:
        result["strategy"] = (
            "v4: exact declaration gate, full byte-backed output obligations and named training counterexamples; no source patching"
        )
    if selected in (("FUN_249c_0013",), ("FUN_24dd_455e",)):
        result["prior_knowledge"] = (
            "Arithmetic leaf with human-derived host projection/mirror obligations, closed alternatives, oracle and lowerer. "
            "Earlier measurements and installed source may already establish behavior; their source snapshots are frozen. "
            "Neither correct action tuple nor installed body sent to model. Not an unseen-routine benchmark or independent source recovery."
        )
    if calibration_from is not None:
        calibration_model = json.loads((calibration_from / "freeze.json").read_text())[
            "model"
        ]
        if result["model"] != calibration_model:
            raise ValueError("calibration and recovery model identities differ")
    pilot.save(output / "freeze.json", result)
    for routine in selected:
        (output / f"{routine}.prompt.txt").write_text(
            residual_prompt(root, routine, structured=local_base is None)
            if residual
            else trial_prompt(
                root, routine, context, enforce_outputs, typed_memory_guidance
            )
        )
    result["residual_partition"] = residual
    if interpretation_first:
        interpretation_text = interpretation_prompt(root, selected[0])
        if supplied_bindings:
            interpretation_text += (
                "\nHuman-supplied original-byte instruction bindings; not model-discovered evidence. "
                "Copy these evidence strings exactly; infer all six action fields yourself. "
                "No Pascal body or accepted action tuple is supplied:\n"
                + json.dumps(PACKED_BINDINGS)
            )
        result["interpretation_first"] = {
            "schema": structured_schema(selected[0], supplied_bindings),
            "prompt_sha256": hashlib.sha256(interpretation_text.encode()).hexdigest(),
            "maximum_requests": 2,
            "maximum_hypotheses_per_request": 3,
            "policy": "Exact-byte/static and original-training memory agreement before Pascal generation; no terminal interpretation feedback.",
        }
        (output / "interpretation.prompt.txt").write_text(interpretation_text)
        result["budgets"]["maximum_total_model_requests"] = 4
        if selected in (("FUN_249c_0013",), ("FUN_24dd_455e",)):
            result["supplied_instruction_bindings"] = (
                NORMALIZE_BINDINGS
                if selected == ("FUN_24dd_455e",)
                else ARITHMETIC_BINDINGS
            )
            result["interpretation_first"]["mechanical_lowering"] = True
            result["budgets"].update(
                {
                    "attempts_per_routine": 1,
                    "repairs_per_routine": 0,
                    "maximum_total_model_requests": 2,
                    "maximum_generated_tokens": 8192 if thinking else 4096,
                }
            )
    if residual:
        result["residual_output_format"] = "raw-pascal" if local_base else "source-json"
        result["strategy"] = (
            "v6: standalone consistent residual prompt, backend-specific output format, "
            "byte-derived short-branch target; unchanged wrapper and full-state gates"
        )
        result["residual_scope"] = (
            "Static wrapper uses supplied entry RegisterSI/DI as original source/"
            "destination argument offsets, and entryDS as destination segment. "
            "These bindings hold in this owned fixture, not arbitrary callers."
        )
        if selected == ("FUN_24dd_4141",):
            result["strategy"] = (
                "v10: model-only packed-copy memory body, supplied byte-bound ABI wrapper; not full model source recovery"
            )
            result["budgets"]["maximum_generated_tokens"] = 4096
            if interpretation_first:
                result["strategy"] = (
                    "v11: checked competing packed-memory interpretations and mechanical typed lowering; no model-written Pascal credit"
                )
                result["budgets"].update(
                    {
                        "attempts_per_routine": 1,
                        "repairs_per_routine": 0,
                        "maximum_total_model_requests": 2,
                    }
                )
                result["interpretation_first"]["mechanical_lowering"] = True
                if supplied_bindings:
                    result["supplied_instruction_bindings"] = PACKED_BINDINGS
                    result["strategy"] = (
                        "v13: supplied original-byte instruction bindings, model-chosen actions, unchanged checks, mechanical Pascal"
                    )
    if binding is not None:
        text = binding_prompt(root, binding)
        (output / "interpretation.prompt.txt").write_text(text)
        result["binding_completion"] = binding
        result["interpretation_first"].update(
            {
                "schema": BINDING_SCHEMA,
                "prompt_sha256": hashlib.sha256(text.encode()).hexdigest(),
                "maximum_requests": 1,
                "maximum_hypotheses_per_request": 1,
            }
        )
        result["budgets"]["maximum_total_model_requests"] = 3
        if selected == ("FUN_24dd_4141",):
            result["interpretation_first"]["schema"] = PACKED_SCHEMA["properties"][
                "hypotheses"
            ]["items"]["properties"]["evidence"]
            result["budgets"]["maximum_total_model_requests"] = 1
        result["strategy"] = (
            "v12: immutable packed-memory actions, one evidence completion, mechanical typed Pascal; no model-written source credit"
            if selected == ("FUN_24dd_4141",)
            else "v7: immutable prior memory interpretation, one evidence-only completion then generated residual; unchanged gates"
        )
    if lowering is not None:
        body = lower_interpretation(lowering["hypothesis"])
        (output / "lowered-residual.inc").write_text(body)
        result["mechanical_lowering"] = {
            **lowering,
            "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
        }
        result["strategy"] = (
            "v8: typed mechanical lowering from checked interpretation; not model-generated source"
        )
        result["budgets"].update(
            {
                "attempts_per_routine": 1,
                "repairs_per_routine": 0,
                "maximum_total_model_requests": 0,
            }
        )
    if thinking:
        result["thinking"] = True
        result["budgets"]["maximum_generated_tokens"] = 8192
        result["strategy"] = (
            "v14: explicit Ollama thinking option,8192token cap, unchanged original-state gates"
        )
    pilot.save(output / "freeze.json", result)
    return result


def run(
    root: pathlib.Path,
    output: pathlib.Path,
    model: str,
    endpoint: str,
    training_from: pathlib.Path | None = None,
    calibration_from: pathlib.Path | None = None,
    routines: tuple[str, ...] | None = None,
    enforce_outputs: bool = False,
    residual: bool = False,
    local_base: pathlib.Path | None = None,
    local_adapter: pathlib.Path | None = None,
    interpretation_first: bool = False,
    binding_from: pathlib.Path | None = None,
    lowering_from: pathlib.Path | None = None,
    typed_memory_guidance: bool = False,
    supplied_bindings: bool = False,
    thinking: bool = False,
) -> dict:
    """Oracle: training-only selection, one terminal evaluation, no automatic source acceptance."""
    frozen = (
        freeze(
            root,
            output,
            model,
            endpoint,
            training_from,
            calibration_from,
            routines,
            enforce_outputs,
            residual,
            local_base,
            local_adapter,
            interpretation_first,
            binding_from,
            lowering_from,
            typed_memory_guidance,
            supplied_bindings,
            thinking,
        )
        if routines is not None
        or enforce_outputs
        or residual
        or local_base
        or interpretation_first
        or binding_from is not None
        or lowering_from is not None
        or typed_memory_guidance
        or supplied_bindings
        or thinking
        else (
            freeze(root, output, model, endpoint, training_from, calibration_from)
            if calibration_from is not None
            else (
                freeze(root, output, model, endpoint)
                if training_from is None
                else freeze(root, output, model, endpoint, training_from)
            )
        )
    )
    results = {}
    for routine in frozen.get("regions", PANEL):
        training = cases(routine, "training")
        if training_from is None:
            original(root, output / routine / "original-training", routine, training)
        else:
            predecessor = json.loads((training_from / "result.json").read_text())
            previous_freeze = json.loads((training_from / "freeze.json").read_text())
            if (
                previous_freeze["binary_sha256"] != frozen["binary_sha256"]
                or previous_freeze["corpora"].get(routine) != frozen["corpora"][routine]
                or previous_freeze["regions"].get(routine) != frozen["regions"][routine]
            ):
                raise ValueError("predecessor binary/regions/corpora differ")
            if any(
                record["terminal"] is not None
                for record in predecessor["routines"].values()
            ):
                raise ValueError(
                    "changed strategy must not consume evaluated terminal outcomes"
                )
            source_directory = training_from / routine / "original-training"
            artifact_hashes = json.loads((training_from / "artifacts.json").read_text())
            for path in source_directory.iterdir():
                if (
                    path.is_file()
                    and pilot.digest(path)
                    != artifact_hashes[str(path.relative_to(training_from))]
                ):
                    raise ValueError("predecessor training artifact changed")
            if (source_directory / "CASES.BIN").read_bytes() != b"".join(training):
                raise ValueError("predecessor training corpus differs")
            if (
                compare(
                    routine,
                    training,
                    (source_directory / "TRACE.BIN").read_bytes(),
                    native=True,
                )["status"]
                != "passed"
            ):
                raise ValueError("predecessor original training trace differs")
            shutil.copytree(source_directory, output / routine / "original-training")
        attempts, seen, selected = [], set(), None
        text = (output / f"{routine}.prompt.txt").read_text()
        interpretation = None
        if lowering_from is not None:
            context = frozen["mechanical_lowering"]
            interpretation = {
                "status": "passed",
                "selected": context["hypothesis"],
                "history": [
                    {
                        "attempt": 0,
                        "hypotheses": [
                            {
                                "hypothesis": context["hypothesis"],
                                "assessment": context["assessment"],
                                "duplicate": True,
                            }
                        ],
                    }
                ],
                "model_requests": 0,
                "reused_interpretation": True,
            }
        if interpretation_first:
            records = (output / routine / "original-training/TRACE.BIN").read_bytes()
            if binding_from is not None:
                interpretation = complete_binding(
                    output / routine / "interpretation",
                    model,
                    endpoint,
                    (output / "interpretation.prompt.txt").read_text(),
                    frozen["binding_completion"],
                    training,
                    records,
                )
            else:
                interpretation = interpret_memory(
                    root,
                    output / routine / "interpretation",
                    model,
                    endpoint,
                    training,
                    records,
                    routine,
                    supplied_bindings,
                    thinking,
                )
            if interpretation["status"] != "passed":
                results[routine] = {
                    "attempts": [],
                    "selected": None,
                    "terminal": None,
                    "source_review": "not_eligible",
                    "interpretation": interpretation,
                }
                pilot.save(output / routine / "selection.json", results[routine])
                continue
            text += (
                "\nChecked model-proposed memory interpretation (exact instruction "
                "constraints and original training memory agreement; not a Pascal pass):\n"
                + json.dumps(interpretation["selected"])
                + (
                    "\nThe human-authored typed renderer lowers these checked actions; "
                    "no Pascal generation request or model-written source credit."
                    if routine in ("FUN_24dd_4141", "FUN_249c_0013")
                    else "\nGenerate the declaration-free Pascal memory body implementing this "
                    "checked interpretation. Use source/destination/count, not SI/DI/CX "
                    "as Pascal identifiers. No numeric DOS pointers."
                )
            )
        packed_lowering = interpretation_first and routine in (
            "FUN_24dd_4141",
            "FUN_249c_0013",
            "FUN_24dd_455e",
        )
        for number in range(
            1, 2 if lowering_from is not None or packed_lowering else 3
        ):
            directory = output / routine / f"attempt-{number}"
            response_path = output / routine / f"response-{number}.json"
            source = None
            try:
                (output / routine / f"prompt-{number}.txt").write_text(text)
                if lowering_from is not None or packed_lowering:
                    if packed_lowering and interpretation is None:
                        raise ValueError(
                            "mechanical lowering requires checked interpretation"
                        )
                    lowered_source = (
                        (output / "lowered-residual.inc").read_text()
                        if lowering_from is not None
                        else structured_lowering(routine, interpretation["selected"])
                        if interpretation is not None
                        else None
                    )
                    if lowered_source is None:
                        raise ValueError("missing mechanical source")
                    response = json.dumps(
                        {
                            "response": json.dumps({"source": lowered_source}),
                            "origin": "mechanical-lowering-not-model-output",
                        }
                    )
                elif local_base:
                    from engine.model_adapter import generate_with_adapter

                    generated = generate_with_adapter(
                        text,
                        str(local_base),
                        str(local_adapter) if local_adapter else "",
                        max_new_tokens=2048,
                        quantized=True,
                    )
                    if generated.lstrip().startswith(("{",)):
                        proposal_text = generated
                    else:
                        proposal_text = json.dumps({"source": generated})
                    response = json.dumps({"response": proposal_text})
                else:
                    response = (
                        pilot.request(
                            text,
                            model,
                            endpoint,
                            max_generated_tokens=8192,
                            think=True,
                        )
                        if thinking and not interpretation_first
                        else (
                            pilot.request(
                                text,
                                model,
                                endpoint,
                                max_generated_tokens=frozen["budgets"][
                                    "maximum_generated_tokens"
                                ],
                            )
                            if typed_memory_guidance
                            or (residual and routine == "FUN_24dd_4141")
                            else pilot.request(text, model, endpoint)
                        )
                    )
                response_path.write_text(response)
                if residual:
                    proposal = json.loads(json.loads(response)["response"])
                    if set(proposal) != {"source"} or not isinstance(
                        proposal["source"], str
                    ):
                        raise ValueError("residual proposal must contain only source")
                    parsed = proposal["source"]
                    (output / routine / f"residual-{number}.inc").write_text(parsed)
                    parsed = compose_residual(parsed, routine)
                else:
                    parsed = pilot.candidate_source(json.loads(response), routine)
                source = (
                    "{ Oracle: original-byte differential trial; complete source review "
                    "required. Native ABI/caller provenance not established. }\n"
                    + parsed
                )
            except (ValueError, KeyError, urllib.error.URLError, TimeoutError) as error:
                attempt = {"status": "proposal-failed", "error": str(error)}
            else:
                source_hash = hashlib.sha256(source.encode()).hexdigest()
                if source_hash in seen:
                    attempt = {"status": "duplicate", "source_sha256": source_hash}
                else:
                    seen.add(source_hash)
                    declaration_error = (
                        check_declaration(routine, source) if enforce_outputs else None
                    )
                    if declaration_error is not None:
                        attempt = declaration_error
                    elif not residual and re.search(
                        r"\b(PWord|Ptr|Move|FillChar|RealModeMemory|DosMemory)\b|"
                        r"\bPByte\s*\(\s*(?!param_[23]\s*\))|"
                        r"\bPointer\s*\(|\b(?:AX|BX|CX|DX|SI|DI|SP|BP|SS|DS|ES|DirectionFlag)\s*:=",
                        source,
                        re.IGNORECASE,
                    ):
                        attempt = {
                            "status": "representation-rejected",
                            "error": "use provided parameters and full mirror names; numeric address emulation is forbidden",
                        }
                    else:
                        attempt = compile_candidate(root, directory, routine, source)
                        if attempt["status"] == "passed":
                            attempt = run_candidate(directory, routine, training)
                            if enforce_outputs and attempt["status"] == "failed":
                                attempt["state_feedback"] = training_state_feedback(
                                    routine,
                                    training,
                                    (directory / "PASCAL.BIN").read_bytes(),
                                )
                    attempt["source_sha256"] = source_hash
                    if attempt["status"] == "compile-failed":
                        attempt["compiler_feedback"] = (
                            directory / "compile.log"
                        ).read_text()[-4000:]
            attempt["assessment"] = proposal_assessment(attempt)
            if lowering_from is not None or packed_lowering:
                attempt["model_request"] = False
                attempt["source_origin"] = "mechanical-lowering"
            attempts.append(attempt)
            pilot.save(output / routine / "training.json", attempts)
            if attempt["status"] == "passed":
                selected = number
                break
            text += (
                "\nTraining-only failure; replace the declaration-free residual body:\n"
                if residual
                else "\nTraining-only failure; fix the entire include:\n"
            ) + json.dumps(attempt)
            if source is not None:
                text += (
                    "\nPrevious proposed residual body:\n" + proposal["source"]
                    if residual
                    else "\nPrevious proposed include:\n" + source
                )
        record = {
            "attempts": attempts,
            "selected": selected,
            "terminal": None,
            "source_review": "pending" if selected else "not_eligible",
        }
        if interpretation is not None:
            record["interpretation"] = interpretation
        pilot.save(output / routine / "selection.json", record)
        if selected:
            terminal = cases(routine, "terminal")
            original(root, output / routine / "original-terminal", routine, terminal)
            candidate = output / routine / f"attempt-{selected}"
            # Separate output directory retains every training artifact and the same executable.
            destination = output / routine / "terminal"
            destination.mkdir()
            shutil.copy2(candidate / "probe", destination / "probe")
            record["terminal"] = run_candidate(destination, routine, terminal)
            record["terminal"]["assessment"] = proposal_assessment(record["terminal"])
            record["source_review"] = (
                "pending"
                if record["terminal"]["status"] == "passed"
                else "not_eligible"
            )
            pilot.save(output / routine / "selection.json", record)
        results[routine] = record
    for path, digest in frozen["source_hashes"].items():
        if pilot.digest(root / path) != digest:
            raise ValueError("source trial inputs changed during evaluation")
    if (
        binding_from is not None
        and binding_context(root, binding_from) != frozen["binding_completion"]
    ):
        raise ValueError("binding predecessor changed during evaluation")
    if lowering_from is not None:
        current = lowering_context(root, lowering_from)
        if any(current[key] != frozen["mechanical_lowering"][key] for key in current):
            raise ValueError("lowering predecessor changed during evaluation")
    if local_base:
        if any(
            pilot.digest(pathlib.Path(path)) != digest
            for path, digest in frozen["model"]["file_hashes"].items()
        ):
            raise ValueError("local training model files changed during evaluation")
    elif (
        lowering_from is None
        and pilot.leaf_model_identity(model, endpoint) != frozen["model"]
    ):
        raise ValueError("local model identity changed during evaluation")
    if calibration_from is not None:
        calibration_context(root, calibration_from)
        if (
            pilot.digest(calibration_from / "review.json")
            != frozen["calibration"]["review_sha256"]
        ):
            raise ValueError("calibration review changed during recovery")
    result = {
        "routines": results,
        "attempted_routines": len(results),
        "binary_terminal_passes": sum(
            r["terminal"] is not None and r["terminal"]["status"] == "passed"
            for r in results.values()
        ),
        "accepted_source_recoveries": 0,
        "source_review_required": True,
        "examples_promoted": 0,
        "weights_changed": False,
    }
    result["model_requests"] = sum(
        sum(attempt.get("model_request", True) for attempt in r["attempts"])
        + r.get("interpretation", {}).get("model_requests", 0)
        for r in results.values()
    )
    result["frontier_status"] = (
        "source-review-required"
        if result["binary_terminal_passes"]
        else "stopped-below-yield-floor"
    )
    pilot.save(output / "result.json", result)
    seal_archive(output)
    return result


def validate_artifacts(
    root: pathlib.Path, output: pathlib.Path, *, historical: bool = False
) -> dict:
    """Oracle: read-only saved corpus/trace/source replay, never another original run."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    binding = frozen.get("binding_completion")
    if binding is not None:
        predecessor = pathlib.Path(binding["path"])
        if (
            pilot.digest(predecessor / "artifacts.json") != binding["artifacts_sha256"]
            or pilot.digest(predecessor / "result.json") != binding["result_sha256"]
        ):
            raise ValueError("binding predecessor identity changed")
        if not historical and binding_context(root, predecessor) != binding:
            raise ValueError("binding predecessor interpretation differs")
    lowering = frozen.get("mechanical_lowering")
    if lowering is not None:
        predecessor = pathlib.Path(lowering["path"])
        if (
            pilot.digest(predecessor / "artifacts.json") != lowering["artifacts_sha256"]
            or pilot.digest(predecessor / "result.json") != lowering["result_sha256"]
            or hashlib.sha256(archive["lowered-residual.inc"]).hexdigest()
            != lowering["body_sha256"]
        ):
            raise ValueError("lowering predecessor or body identity changed")
        if not historical:
            context = lowering_context(root, predecessor)
            if any(context[key] != lowering[key] for key in context):
                raise ValueError("lowering context differs from saved evidence")
            if (
                lower_interpretation(context["hypothesis"])
                != archive["lowered-residual.inc"].decode()
            ):
                raise ValueError("lowering body differs from checked interpretation")
    calibration = frozen.get("calibration")
    if calibration is not None:
        directory = pathlib.Path(calibration["path"])
        calibration_context(root, directory, historical=historical)
        if (
            pilot.digest(directory / "review.json") != calibration["review_sha256"]
            or pilot.digest(directory / "artifacts.json")
            != calibration["artifacts_sha256"]
        ):
            raise ValueError("source trial calibration identity changed")
    if pilot.digest(root / "extracted/liero/LIERO.EXE") != frozen["binary_sha256"]:
        raise ValueError("source trial original binary identity changed")
    for routine, region in frozen["regions"].items():
        if region["bytes_hex"] != routine_spec(routine)["bytes"]:
            raise ValueError("historical routine differs from current replay contract")
        if (
            hashlib.sha256(archive[f"{routine}.prompt.txt"]).hexdigest()
            != frozen["prompt_hashes"][routine]
        ):
            raise ValueError("source trial frozen prompt changed")
    interpretation_freeze = frozen.get("interpretation_first")
    if (
        interpretation_freeze
        and hashlib.sha256(archive["interpretation.prompt.txt"]).hexdigest()
        != interpretation_freeze["prompt_sha256"]
    ):
        raise ValueError("frozen interpretation prompt changed")
    # Installed source can legitimately replace the disclosed old drafts after review.
    for name, digest in frozen["source_hashes"].items():
        if (
            hashlib.sha256(archive["sources/" + pathlib.Path(name).name]).hexdigest()
            != digest
        ):
            raise ValueError("source trial frozen input snapshot changed: " + name)
        if historical:
            continue
        if name in {f"targets/liero/src/{routine}.inc" for routine in PANEL}:
            continue
        if pilot.digest(root / name) != digest:
            raise ValueError("source trial method/runtime changed: " + name)
    result = json.loads(archive["result.json"])
    for routine, record in result["routines"].items():
        interpretation = record.get("interpretation")
        if lowering is not None:
            if (
                interpretation is None
                or interpretation["selected"] != lowering["hypothesis"]
            ):
                raise ValueError("lowering used another interpretation")
            if (
                len(record["attempts"]) != 1
                or record["attempts"][0].get("model_request") is not False
            ):
                raise ValueError(
                    "lowering must have one mechanical attempt and no model request"
                )
            if archive[f"{routine}/residual-1.inc"] != archive["lowered-residual.inc"]:
                raise ValueError("evaluated residual differs from frozen lowering")
        if interpretation is not None and not historical:
            inputs = cases(routine, "training")
            original_records = archive[f"{routine}/original-training/TRACE.BIN"]
            selected_interpretation = None
            for proposal in interpretation["history"]:
                for alternative in proposal.get("hypotheses", []):
                    if binding is not None and any(
                        alternative["hypothesis"][name] != binding["hypothesis"][name]
                        for name in (
                            PACKED_FIELDS
                            if routine == "FUN_24dd_4141"
                            else INTERPRETATION_FIELDS
                        )
                    ):
                        raise ValueError("binding completion changed memory actions")
                    checker = structured_checker(routine)
                    checked = checker(
                        alternative["hypothesis"], inputs, original_records
                    )
                    if checked != alternative["assessment"]:
                        raise ValueError(
                            "saved interpretation assessment differs from replay"
                        )
                    if (
                        checked["status"] == "passed"
                        and selected_interpretation is None
                    ):
                        selected_interpretation = alternative["hypothesis"]
            if selected_interpretation != interpretation["selected"]:
                raise ValueError(
                    "interpretation selection differs from training checks"
                )
            if selected_interpretation is None and record["attempts"]:
                raise ValueError("Pascal generated without checked interpretation")
        for number, attempt in enumerate(record.get("attempts", []), 1):
            if attempt["status"] not in {"passed", "failed"}:
                continue
            directory = f"{routine}/attempt-{number}"
            if (
                hashlib.sha256(archive[f"{directory}/candidate.inc"]).hexdigest()
                != attempt["source_sha256"]
            ):
                raise ValueError("training candidate identity changed")
            replay = compare(
                routine,
                cases(routine, "training"),
                archive[f"{directory}/PASCAL.BIN"],
                native=False,
            )
            if any(attempt[key] != replay[key] for key in replay):
                raise ValueError("source trial training candidate replay disagrees")
        for suite in ("training", "terminal"):
            directory = f"{routine}/original-{suite}"
            if not any(name.startswith(directory + "/") for name in archive):
                if suite == "terminal" and record["selected"] is None:
                    continue
                raise ValueError("missing source trial original suite")
            inputs = cases(routine, suite)
            payload = b"".join(inputs)
            if (
                hashlib.sha256(payload).hexdigest() != frozen["corpora"][routine][suite]
                or archive[f"{directory}/CASES.BIN"] != payload
                or compare(
                    routine, inputs, archive[f"{directory}/TRACE.BIN"], native=True
                )["status"]
                != "passed"
            ):
                raise ValueError("source trial original corpus/trace disagrees")
        selected = record["selected"]
        if selected is not None:
            candidate = f"{routine}/attempt-{selected}"
            if (
                hashlib.sha256(archive[f"{candidate}/candidate.inc"]).hexdigest()
                != record["attempts"][selected - 1]["source_sha256"]
            ):
                raise ValueError("selected source identity disagrees")
            for suite, directory in (
                ("training", candidate),
                ("terminal", f"{routine}/terminal"),
            ):
                saved = (
                    record["attempts"][selected - 1]
                    if suite == "training"
                    else record["terminal"]
                )
                if saved["status"] in {"passed", "failed"}:
                    replay = compare(
                        routine,
                        cases(routine, suite),
                        archive[f"{directory}/PASCAL.BIN"],
                        native=False,
                    )
                    if any(saved[key] != replay[key] for key in replay):
                        raise ValueError("source trial candidate replay disagrees")
    return result


def export_trial(
    root: pathlib.Path,
    archive: pathlib.Path,
    destination: pathlib.Path,
    caller_archive: pathlib.Path | None = None,
) -> dict:
    """Oracle: frozen archive replay and exact scoped review; no inference, execution or promotion."""
    if destination.resolve().is_relative_to(archive.resolve()):
        raise ValueError("export destination must be outside frozen archive")
    result = validate_artifacts(root, archive, historical=True)
    frozen = json.loads((archive / "freeze.json").read_text())
    review_path = archive / "source-review.json"
    review = json.loads(review_path.read_text()) if review_path.exists() else None
    entries = {}
    for routine, record in result["routines"].items():
        selected = record["selected"]
        entry = {
            "selected": selected,
            "attempts": record["attempts"],
            "terminal": record["terminal"],
            "interpretation": record.get("interpretation"),
            "review_status": "pending",
            "whole_routine_accepted": False,
        }
        if selected is not None:
            source = archive / routine / f"attempt-{selected}/candidate.inc"
            entry["source_sha256"] = pilot.digest(source)
            if review is not None and review.get("routine") == routine:
                if (
                    review.get("source_sha256") != entry["source_sha256"]
                    or review.get("status") != "accepted-scoped-composition"
                    or not review.get("scope")
                    or not review.get("review")
                    or not review.get("obligations")
                    or review.get("whole_routine_accepted") is not False
                ):
                    raise ValueError(
                        "source review does not bind exact scoped candidate"
                    )
                entry["review_status"] = review["status"]
                entry["review"] = review
        entries[routine] = entry
    caller_result = None
    if caller_archive is not None:
        from tools import liero_move_caller

        caller_result = liero_move_caller.replay_packed(root, caller_archive)
    destination.mkdir(parents=True, exist_ok=False)
    included = {}
    sources = [("evidence", archive)]
    if caller_archive is not None:
        sources.append(("caller-evidence", caller_archive))
    for folder, directory in sources:
        names = set(json.loads((directory / "artifacts.json").read_text()))
        if (directory / "source-review.json").exists():
            names.add("source-review.json")
        for name in sorted(names):
            path = (directory / name).resolve()
            if not path.is_relative_to(directory.resolve()):
                raise ValueError("export source outside archive")
            if path.suffix.lower() not in {
                ".json",
                ".txt",
                ".inc",
                ".pas",
                ".py",
                ".s",
            } and path.name not in {"CASES.BIN", "TRACE.BIN", "PASCAL.BIN"}:
                continue
            target = destination / folder / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            included[str(target.relative_to(destination))] = pilot.digest(target)
    manifest = {
        "format": "losore-scoped-prototype-v1",
        "archive": str(archive.resolve()),
        "binary_sha256": frozen["binary_sha256"],
        "model": frozen["model"],
        "budgets": frozen["budgets"],
        "scope": frozen["scope"],
        "prior_knowledge": frozen.get("prior_knowledge"),
        "supplied_instruction_bindings": frozen.get("supplied_instruction_bindings"),
        "corpora": frozen["corpora"],
        "regions": frozen["regions"],
        "routines": entries,
        "files": included,
        "model_requests": result["model_requests"],
        "source_installed": False,
        "examples_promoted": 0,
        "weights_changed": False,
        "terminal_reexecuted": False,
        "export_model_requests": 0,
        "caller_composition": caller_result,
        "limitations": [
            "Assisted scoped recovery; human byte contracts, interface, checker and renderer.",
            "Scoped static review is not user signoff, native ABI or whole-program acceptance.",
            "No statistical accuracy, blind generalization or learned weight improvement claim.",
            "Private original data remains BYOD; full original executable and compiled binaries excluded.",
        ],
    }
    pilot.save(destination / "manifest.json", manifest)
    return manifest


def validate_export(root: pathlib.Path, destination: pathlib.Path) -> dict:
    """Oracle: exported file identities and independently replayed full original/host records."""
    manifest = json.loads((destination / "manifest.json").read_text())
    if manifest["format"] != "losore-scoped-prototype-v1":
        raise ValueError("unsupported prototype export")
    if (
        manifest["source_installed"] is not False
        or manifest["weights_changed"] is not False
        or manifest["examples_promoted"] != 0
        or manifest["export_model_requests"] != 0
    ):
        raise ValueError("export cannot claim source/training/weight promotion")
    for name, digest in manifest["files"].items():
        path = (destination / name).resolve()
        if (
            not path.is_relative_to(destination.resolve())
            or pilot.digest(path) != digest
        ):
            raise ValueError("export evidence changed: " + name)
    evidence = destination / "evidence"
    frozen = json.loads((evidence / "freeze.json").read_text())
    result = json.loads((evidence / "result.json").read_text())
    if (
        pilot.digest(root / "extracted/liero/LIERO.EXE") != manifest["binary_sha256"]
        or manifest["binary_sha256"] != frozen["binary_sha256"]
        or manifest["model"] != frozen["model"]
        or manifest["budgets"] != frozen["budgets"]
        or manifest["corpora"] != frozen["corpora"]
        or manifest["regions"] != frozen["regions"]
        or set(manifest["routines"]) != set(result["routines"])
    ):
        raise ValueError("export binary/freeze identity differs")
    for routine, entry in manifest["routines"].items():
        record = result["routines"][routine]
        if (
            entry["selected"] != record["selected"]
            or entry["attempts"] != record["attempts"]
            or entry["terminal"] != record["terminal"]
        ):
            raise ValueError("export result differs")
        if (
            entry["review_status"] not in {"pending", "accepted-scoped-composition"}
            or entry["whole_routine_accepted"] is not False
        ):
            raise ValueError("export cannot promote scoped review")
        if entry["selected"] is None:
            continue
        selected = evidence / routine / f"attempt-{entry['selected']}"
        if pilot.digest(selected / "candidate.inc") != entry["source_sha256"]:
            raise ValueError("export selected source differs")
        if entry["review_status"] != "pending":
            review = json.loads((evidence / "source-review.json").read_text())
            if (
                entry.get("review") != review
                or entry["review_status"] != review["status"]
                or review["source_sha256"] != entry["source_sha256"]
                or review["whole_routine_accepted"] is not False
            ):
                raise ValueError("export review changed")
        for suite in ("training", "terminal"):
            inputs = cases(routine, suite)
            payload = b"".join(inputs)
            original = evidence / routine / f"original-{suite}"
            candidate = (
                selected if suite == "training" else evidence / routine / "terminal"
            )
            if (original / "CASES.BIN").read_bytes() != payload or hashlib.sha256(
                payload
            ).hexdigest() != manifest["corpora"][routine][suite]:
                raise ValueError("export corpus differs")
            native = compare(
                routine, inputs, (original / "TRACE.BIN").read_bytes(), native=True
            )
            host = compare(
                routine, inputs, (candidate / "PASCAL.BIN").read_bytes(), native=False
            )
            saved = (
                entry["attempts"][entry["selected"] - 1]
                if suite == "training"
                else entry["terminal"]
            )
            if native["status"] != "passed" or any(host[k] != saved[k] for k in host):
                raise ValueError("export full-state replay differs")
    if manifest.get("caller_composition") is not None:
        from tools import liero_move_caller

        caller = destination / "caller-evidence"
        freeze = json.loads((caller / "freeze.json").read_text())
        saved = json.loads((caller / "result.json").read_text())
        if (
            freeze["contract"] != liero_move_caller.packed_caller_contract(root)
            or saved != manifest["caller_composition"]
        ):
            raise ValueError("export caller contract/result differs")
        for suite in ("training", "terminal"):
            if suite not in saved:
                continue
            inputs = liero_move_caller.packed_cases(suite)
            for prefix, native in (("original", True), ("host", False)):
                trace = (
                    caller
                    / f"{prefix}-{suite}"
                    / ("TRACE.BIN" if native else "PASCAL.BIN")
                )
                checked = liero_move_caller.packed_compare(
                    inputs, trace.read_bytes(), native=native
                )
                if (native and checked["status"] != "passed") or (
                    not native and checked != saved[suite]
                ):
                    raise ValueError("export caller trace differs")
    return {
        "status": "export-replay-passed",
        "routines": len(manifest["routines"]),
        "new_model_requests": 0,
        "terminal_reexecuted": False,
        "whole_routines_promoted": 0,
    }


def main() -> int:
    """Oracle: explicit bounded local experiment, BYOD absence degrades to skip."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument(
        "--model",
        help="Prototype defaults to qwen3:14b; legacy trials keep qwen2.5-coder:14b-instruct.",
    )
    parser.add_argument("--training-from", type=pathlib.Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--historical", action="store_true")
    parser.add_argument("--calibrate", action="store_true")
    parser.add_argument("--calibration-from", type=pathlib.Path)
    parser.add_argument(
        "--routine", choices=(*PANEL, *DISCOVERY_PANEL), action="append"
    )
    parser.add_argument("--enforce-outputs", action="store_true")
    parser.add_argument("--residual", action="store_true")
    parser.add_argument("--local-base", type=pathlib.Path)
    parser.add_argument("--local-adapter", type=pathlib.Path)
    parser.add_argument("--interpretation-first", action="store_true")
    parser.add_argument("--binding-from", type=pathlib.Path)
    parser.add_argument("--lowering-from", type=pathlib.Path)
    parser.add_argument("--typed-memory-guidance", action="store_true")
    parser.add_argument("--supplied-bindings", action="store_true")
    parser.add_argument("--thinking", action="store_true")
    parser.add_argument(
        "--prototype",
        action="store_true",
        help="Checked single-routine local-model preset; existing outputs are replayed, never rerun.",
    )
    parser.add_argument(
        "--export",
        type=pathlib.Path,
        help="Replay --output archive and export reviewable scoped evidence; no generation.",
    )
    parser.add_argument("--validate-export", action="store_true")
    parser.add_argument(
        "--caller-from",
        type=pathlib.Path,
        help="Include replay-checked packed caller evidence with --export.",
    )
    args = parser.parse_args()
    if args.model is None:
        args.model = "qwen3:14b" if args.prototype else "qwen2.5-coder:14b-instruct"
    if args.caller_from and not args.export:
        parser.error("--caller-from requires --export")
    if args.validate_export:
        print(json.dumps(validate_export(ROOT, args.output.resolve()), indent=2))
        return 0
    if args.export:
        print(
            json.dumps(
                export_trial(
                    ROOT,
                    args.output.resolve(),
                    args.export.resolve(),
                    args.caller_from.resolve() if args.caller_from else None,
                )["routines"],
                indent=2,
            )
        )
        return 0
    if args.prototype:
        supported = {"FUN_24dd_4141", "FUN_249c_0013", "FUN_24dd_455e"}
        if (
            not args.routine
            or len(args.routine) != 1
            or args.routine[0] not in supported
        ):
            parser.error(
                "--prototype requires one supported packed/arithmetic/normalization routine"
            )
        if (
            args.local_base
            or args.local_adapter
            or args.calibrate
            or args.calibration_from
            or args.binding_from
            or args.lowering_from
            or args.typed_memory_guidance
        ):
            parser.error(
                "--prototype cannot mix calibration/backend/alternate strategies"
            )
        args.interpretation_first = args.enforce_outputs = args.thinking = True
        args.residual = args.routine == ["FUN_24dd_4141"]
        args.supplied_bindings = args.residual
        if args.output.exists():
            if not (args.output / "artifacts.json").is_file():
                parser.error(
                    "partial archive: preserve it and select a new --output; never resume through holdout"
                )
            args.replay = args.historical = True
    if args.local_adapter and not args.local_base:
        parser.error("--local-adapter requires --local-base")
    if args.calibrate:
        if args.training_from or args.calibration_from:
            parser.error("--calibrate cannot be combined with recovery/replay options")
        if args.replay:
            calibration_context(ROOT, args.output.resolve(), historical=args.historical)
            print(
                json.dumps({"status": "calibration-replay-passed", "new_recoveries": 0})
            )
            return 0
        if args.historical:
            parser.error("--historical requires --replay")
        if not shutil.which("fpc"):
            raise FileNotFoundError("source calibration requires FPC")
        print(
            json.dumps(
                run_calibration(
                    ROOT, args.output.resolve(), args.model, "http://localhost:11434"
                ),
                indent=2,
            )
        )
        return 0
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        print(json.dumps({"status": "skipped", "reason": "BYOD unavailable"}))
        return 0
    if args.replay:
        print(
            json.dumps(
                validate_artifacts(
                    ROOT, args.output.resolve(), historical=args.historical
                ),
                indent=2,
            )
        )
        return 0
    if args.historical:
        parser.error("--historical requires --replay")
    missing = [tool for tool in ("fpc", "as", "ld", "dosbox") if not shutil.which(tool)]
    if missing:
        raise FileNotFoundError("source trial requires: " + ", ".join(missing))
    print(
        json.dumps(
            run(
                ROOT,
                args.output.resolve(),
                args.model,
                "http://localhost:11434",
                None if args.training_from is None else args.training_from.resolve(),
                None
                if args.calibration_from is None
                else args.calibration_from.resolve(),
                tuple(args.routine) if args.routine else DEFAULT_PANEL,
                args.enforce_outputs,
                args.residual,
                args.local_base,
                args.local_adapter,
                args.interpretation_first,
                None if args.binding_from is None else args.binding_from.resolve(),
                None if args.lowering_from is None else args.lowering_from.resolve(),
                args.typed_memory_guidance,
                args.supplied_bindings,
                args.thinking,
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
