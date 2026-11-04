"""Original cleanup dispatch mechanisms and checked nonreturning error composition."""

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
from engine.evidence_archive import read_archive, seal_archive
from tools import liero_four_routine_pilot as pilot
from tools.liero_file_probe import assemble_probe, run_dosbox

RAW = bytes.fromhex("c41e02648cc00bc3741333c0a30264a30464a31064b86e010e500653cb")
CASES = tuple((seed, mode) for seed in (0xA5, 0x5A) for mode in range(4))
SNAPSHOT = 70
TRACE_BYTES = 8 + 2 * SNAPSHOT


def checked_contract(root: pathlib.Path) -> dict:
    """Oracle: original dispatch bytes and real relocation exclusions; callback provenance unproved."""
    binary, allocator, _ = pilot.allocator_deduction_inputs(root)
    start = allocator["file_offset"] + 0x16E - 0x353
    header = int.from_bytes(binary[8:10], "little") * 16
    if binary[start : start + len(RAW)] != RAW or any(
        start - 1 <= r < start + len(RAW)
        for r in _mz_relocation_locations(binary, header)
    ):
        raise ValueError("cleanup dispatch bytes or relocations differ")
    return {
        "oracle": "original_cleanup_dispatch_synthetic_callback_mechanism",
        "binary_sha256": hashlib.sha256(binary).hexdigest(),
        "file_offset": start,
        "bytes_hex": RAW.hex(),
        "entry": 0x16E,
        "null_target": 0x18B,
        "return_target": 0x16E,
        "effects": [
            "Null means both offset and segment zero; either nonzero dispatches.",
            "Clear DS6402/6404/6410 before transferring to saved ES:BX.",
            "PUSH CS,016e,ES,BX; RETF consumes target pair and leaves016e:CS return pair.",
            "A preserving RETF callback reenters016e with restored SP; cleared slot selects018b.",
        ],
        "preconditions": [
            "COM64KiB, DS=SS=CS, entrySPeff0; code/data below6000, globals63d8..6412 disjoint.",
            "Synthetic callback at physical CS:3000 records entry state then RETF; it installs no new callback.",
            "Three far representations of same owned callback: CS:3000, CS+0300:0000, CS+02ff:0010.",
            "No asynchronous memory mutation; stop018b before real cleanup/services.",
        ],
        "unresolved": [
            "actual DS6402/6404 target provenance and callback behavior, mutation/reinstallation and nonreturn",
            "actual failure reachability, arbitrary callback ABI and cleanup beyond018b",
        ],
        "source_recovered": False,
    }


def target(mode: int, segment: int) -> tuple[int, int]:
    """Oracle: explicitly owned far-pointer aliases; mode0 is the only null pointer."""
    if mode not in range(4) or not 0x10 <= segment <= 0xEFFF:
        raise ValueError("unsupported cleanup callback fixture")
    return ((0, 0), (0x3000, segment), (0, segment + 0x300), (0x10, segment + 0x2FF))[
        mode
    ]


def capture(label: str) -> str:
    """Oracle: DS-relative collector supports aliased callback CS without changing target stack."""
    return f"""
    mov %cs, {label}
    mov %ss, {label}+2
    mov %sp, {label}+4
    mov %ds, {label}+6
    mov %sp, %bp
    mov %ss:(%bp), %ax
    mov %ax, {label}+8
    mov %ss:2(%bp), %ax
    mov %ax, {label}+10
    push %ds
    pop %es
    mov $0x63d8, %si
    mov ${label}+12, %di
    mov $58, %cx
    cld
    rep movsb
"""


def harness(seed: int, mode: int) -> str:
    """Oracle: original RETF dispatch and synthetic recording callback; code/global/stack separation."""
    if (seed, mode) not in CASES:
        raise ValueError("unsupported cleanup frozen case")
    off, relative_segment = target(mode, 0x1000)
    segment_setup = (
        "xor %ax, %ax"
        if mode == 0
        else f"mov %cs, %ax\n    add ${relative_segment - 0x1000}, %ax"
    )
    return f""".code16
.global _start, collector
_start:
    jmp setup
.org 0x1000-0x100
setup:
    mov %cs, %ax
    cmp $0xefff, %ax
    ja failed
    mov %ax, %dx
    add $0x1000, %dx
    cmp %es:2, %dx
    ja failed
    cli
    mov %ax, %ss
    mov $0xeff0, %sp
    sti
    mov %ax, %ds
    mov %ax, %es
    mov %ax, record
    movw ${mode}, record+2
    movw ${seed}, record+4
    movw $0, record+6
    mov $0x63d8, %di
    mov $58, %cx
    mov ${seed}, %al
    cld
    rep stosb
    mov $first, %di
    mov ${SNAPSHOT}, %cx
    rep stosb
    movw $0x1357, 0xeff0
    movw $0x2468, 0xeff2
    movw ${off}, 0x6402
    {segment_setup}
    mov %ax, 0x6404
    jmp 0x16e
collector:
{capture("last")}
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, %bx
    mov $record, %dx
    mov ${TRACE_BYTES}, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp ${TRACE_BYTES}, %ax
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
record: .space 8
first: .space {SNAPSHOT}
last: .space {SNAPSHOT}
.org 0x3000-0x100
callback:
    incw record+6
{capture("first")}
    lret
"""


def build_image(raw: bytes, collector: int) -> bytes:
    """Oracle: original29 bytes unchanged, explicit stop JMP only; writable code hole and owned bounds."""
    if not 0x1000 < collector < 0x3000 or not 0x3000 < len(raw) + 0x100 < 0x6000:
        raise ValueError("cleanup harness collector/code bounds differ")
    image = bytearray(raw)
    begin = 0x16E - 0x100
    if any(image[begin : begin + len(RAW) + 3]):
        raise ValueError("cleanup original-code hole occupied")
    image[begin : begin + len(RAW)] = RAW
    struct.pack_into("<BH", image, 0x18B - 0x100, 0xE9, (collector - 0x18E) & 65535)
    return bytes(image)


def projection(trace: bytes, case: tuple[int, int]) -> list[int]:
    """Oracle: both callback/reentry endpoints, real RETF return pair and all58 global bytes."""
    if len(trace) != TRACE_BYTES:
        raise ValueError("cleanup trace requires both complete endpoints")
    seed, mode = case
    segment, observed_mode, observed_seed, count = struct.unpack_from("<4H", trace)
    _, seg = target(mode, segment)
    if (observed_seed, observed_mode, count) != (seed, mode, int(mode != 0)):
        raise ValueError("cleanup callback selection/count differs")
    expected = bytearray([seed] * 58)
    for cell, value in ((0x6402, 0), (0x6404, 0)):
        struct.pack_into("<H", expected, cell - 0x63D8, value)
    if mode:
        struct.pack_into("<H", expected, 0x6410 - 0x63D8, 0)
        first = trace[8 : 8 + SNAPSHOT]
        if (
            struct.unpack_from("<6H", first)
            != (seg, segment, 0xEFEC, segment, 0x16E, segment)
            or first[12:] != expected
        ):
            raise ValueError("cleanup pre-callback clear/far-return contract differs")
    elif trace[8 : 8 + SNAPSHOT] != bytes([seed] * SNAPSHOT):
        raise ValueError("null cleanup unexpectedly invoked callback")
    last = trace[8 + SNAPSHOT :]
    if (
        struct.unpack_from("<6H", last)
        != (segment, segment, 0xEFF0, segment, 0x1357, 0x2468)
        or last[12:] != expected
    ):
        raise ValueError("cleanup reentry/stack/global residue differs")
    return [count, 0xEFEC if mode else 0, 0xEFF0, 0, 0, 0 if mode else seed * 257]


def candidate_program() -> str:
    """Oracle: Pascal dispatch-state projection, synthetic callback continuation explicitly assumed."""
    statements = "\n".join(f"  Run({seed}, {mode});" for seed, mode in CASES)
    return f"""program CleanupProjection;
var f: file; row: array[0..5] of Word; written: LongInt;
procedure Run(seed, mode: Word);
var callbackOffset, callbackSegment, pending: Word;
begin
  callbackOffset := 0; callbackSegment := 0; pending := seed * 257;
  case mode of
    1: begin callbackOffset := $3000; callbackSegment := $1000 end;
    2: callbackSegment := $1300;
    3: begin callbackOffset := $10; callbackSegment := $12ff end;
  end;
  row[0] := 0; row[1] := 0; row[2] := $eff0;
  if (callbackOffset <> 0) or (callbackSegment <> 0) then
  begin
    callbackOffset := 0; callbackSegment := 0; pending := 0;
    row[0] := 1; row[1] := $efec;
  end;
  row[3] := callbackOffset; row[4] := callbackSegment; row[5] := pending;
  BlockWrite(f, row, SizeOf(row), written);
  if written <> SizeOf(row) then Halt(2);
end;
begin
  Assign(f, 'PASCAL.BIN'); Rewrite(f, 1);
{statements}
  Close(f);
end.
"""


def freeze_method(root: pathlib.Path) -> dict:
    """Oracle: one disclosed mechanism corpus, no model/generalization/terminal claims."""
    paths = (
        "tools/liero_cleanup_dispatch_probe.py",
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
            "original_cases": len(CASES),
            "pascal_executions": 1,
            "model_requests": 0,
            "repairs": 0,
        },
        "scope": "synthetic callback mechanism, no training or heldout trial, not actual target recovery",
    }


def run(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: fixed original cases and Pascal state projection, no retries after failure."""
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
        "routine_recovered": False,
        "source_promoted": False,
        "model_requests": 0,
        "synthetic_callback": True,
        "actual_callback_recovered": False,
        "unresolved": freeze["contract"]["unresolved"],
    }
    try:
        expected = bytearray()
        for index, case in enumerate(CASES):
            directory = output / f"case-{index}"
            directory.mkdir()
            (directory / "harness.S").write_text(harness(*case))
            raw = assemble_probe(directory / "harness.S", directory)
            symbols = subprocess.run(
                ["nm", str(directory / "probe.o")],
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            ).stdout
            (directory / "symbols.txt").write_text(symbols)
            labels = {
                line.split()[-1]: int(line.split()[0], 16) + 0x100
                for line in symbols.splitlines()
            }
            (directory / "PROBE.COM").write_bytes(build_image(raw, labels["collector"]))
            run_dosbox(directory)
            expected.extend(
                struct.pack(
                    "<6H", *projection((directory / "TRACE.BIN").read_bytes(), case)
                )
            )
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
            raise ValueError("cleanup original/Pascal projection differs")
        if (
            freeze_method(root) != freeze
            or json.loads((output / "freeze.json").read_text()) != freeze
            or (output / "probe.pas").read_text() != candidate_program()
        ):
            raise ValueError("cleanup frozen method/premises/source changed")
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
    """Oracle: exact saved image/source/global/stack replay; hashes are integrity, not execution attestation."""
    current = freeze_method(root)
    freeze = json.loads((output / "freeze.json").read_text())
    if set(freeze.get("method_hashes", {})) != set(current["method_hashes"]):
        raise ValueError("cleanup frozen method inventory differs")
    current["method_hashes"] = freeze["method_hashes"]
    report = json.loads((output / "result.json").read_text())
    if (
        current != freeze
        or report["freeze_sha256"] != pilot.digest(output / "freeze.json")
        or report["status"] != "passed"
        or report["cases"] != len(CASES)
        or report["oracle"] != freeze["contract"]["oracle"]
        or report["unresolved"] != freeze["contract"]["unresolved"]
        or report["routine_recovered"] is not False
        or report["source_promoted"] is not False
        or report["actual_callback_recovered"] is not False
        or report["synthetic_callback"] is not True
        or report["model_requests"] != 0
        or (output / "probe.pas").read_text() != candidate_program()
    ):
        raise ValueError("cleanup report/source/premises invalid")
    required = {
        "freeze.json",
        "probe.pas",
        "probe",
        "PASCAL.BIN",
        "compile.log",
        "execution.log",
    }
    expected = bytearray()
    for index, case in enumerate(CASES):
        prefix = f"case-{index}"
        directory = output / prefix
        required.update(
            f"{prefix}/{name}"
            for name in (
                "harness.S",
                "harness.bin",
                "symbols.txt",
                "PROBE.COM",
                "TRACE.BIN",
            )
        )
        if (directory / "harness.S").read_text() != harness(*case):
            raise ValueError("cleanup saved harness differs")
        labels = {
            line.split()[-1]: int(line.split()[0], 16) + 0x100
            for line in (directory / "symbols.txt").read_text().splitlines()
        }
        if (directory / "PROBE.COM").read_bytes() != build_image(
            (directory / "harness.bin").read_bytes(), labels["collector"]
        ):
            raise ValueError("cleanup original image differs")
        expected.extend(
            struct.pack(
                "<6H", *projection((directory / "TRACE.BIN").read_bytes(), case)
            )
        )
    if (output / "PASCAL.BIN").read_bytes() != expected:
        raise ValueError("cleanup saved Pascal/original differs")
    for name, identity in freeze["method_hashes"].items():
        path = f"methods/{pathlib.Path(name).name}"
        required.add(path)
        if pilot.digest(output / path) != identity:
            raise ValueError("cleanup saved method differs")
    if not required <= report["artifact_hashes"].keys():
        raise ValueError("cleanup required hashes missing")
    for name, identity in report["artifact_hashes"].items():
        path = (output / name).resolve()
        if not path.is_relative_to(output.resolve()) or pilot.digest(path) != identity:
            raise ValueError("cleanup artifact changed")
    return report


def main() -> int:
    """Oracle: pass/failure/skip CLI, replay without original/candidate execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--terminating", action="store_true")
    parser.add_argument("--open-output", action="store_true")
    parser.add_argument("--text-error", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    if args.open_output and not args.terminating:
        parser.error("--open-output requires --terminating")
    if args.text_error and not args.open_output:
        parser.error("--text-error requires --open-output")
    if args.terminating:
        result = (
            replay_exit(
                ROOT, output, open_output=args.open_output, text_error=args.text_error
            )
            if args.replay
            else run_exit(
                ROOT, output, open_output=args.open_output, text_error=args.text_error
            )
        )
    else:
        result = validate_report(ROOT, output) if args.replay else run(ROOT, output)
    print(
        json.dumps(
            {key: value for key, value in result.items() if key != "artifact_hashes"},
            indent=2,
        )
    )
    return 0 if result["status"] in {"passed", "skipped"} else 1


EXIT_CASES = tuple(
    (code, offset, entry)
    for code in (1, 5, 106, 203, 255, 0x1234, 0xFF00)
    for offset in (0, 0x3456)
    for entry in (0, 1)
)
EXIT_SOURCES = tuple(
    "targets/liero/src/" + name
    for name in (
        "LieroRuntime.pas",
        "FUN_24dd_010f.inc",
        "FUN_24dd_04f4.inc",
        "FUN_24dd_3711.inc",
        "FUN_24dd_01f0.inc",
        "FUN_24dd_01fe.inc",
        "FUN_24dd_020a.inc",
        "FUN_24dd_0218.inc",
        "FUN_24dd_021f.inc",
        "FUN_24dd_022a.inc",
        "FUN_24dd_0232.inc",
    )
) + (
    "targets/liero/tests/probe_liero_error_exit.pas",
    "tools/liero_error_exit_probe.S",
    "tools/liero_cleanup_dispatch_probe.py",
)

OPEN_EXIT_CASES = tuple(
    (203, 0x3456, entry, scenario, used)
    for entry in (0, 1)
    for scenario in range(5)
    for used in (0, 1, 7, 128)
)
OPEN_EXIT_SOURCES = EXIT_SOURCES + tuple(
    "targets/liero/src/" + name
    for name in (
        "FUN_24dd_374d.inc",
        "FUN_24dd_37b3.inc",
        "FUN_24dd_37d3.inc",
    )
)


TEXT_EXIT_CASES = tuple(
    (6 if scenario == 1 else 5, 0x155, 2, scenario, 0) for scenario in (1, 2, 4)
)
TEXT_EXIT_SOURCES = (
    OPEN_EXIT_SOURCES
    + tuple(
        "targets/liero/src/" + name
        for name in (
            "FUN_24dd_375e.inc",
            "FUN_24dd_396c.inc",
            "FUN_24dd_397a.inc",
            "FUN_24dd_3899.inc",
            "FUN_24dd_3930.inc",
            "FUN_249c_0000.inc",
            "FUN_249c_0013.inc",
            "FUN_249c_0037.inc",
        )
    )
    + (
        "tools/liero_text_probe.py",
        "tools/liero_nibble_caller.py",
        "tools/liero_write_handler_probe.py",
    )
)


def exit_contract(
    root: pathlib.Path, *, open_output: bool = False, text_error: bool = False
) -> tuple[dict, dict[int, bytes]]:
    """Oracle: actual original error entry/termination, original calls and MZ DS fixup."""
    binary, allocator, _ = pilot.allocator_deduction_inputs(root)
    origin = allocator["file_offset"] - 0x353
    regions = {
        ip: binary[origin + ip : origin + end]
        for ip, end in ((0x10F, 0x264), (0x4F4, 0x502), (0x3711, 0x374D))
    }
    if open_output:
        regions.update(
            {
                ip: binary[origin + ip : origin + end]
                for ip, end in ((0x374D, 0x375E), (0x37B3, 0x37EC))
            }
        )
        if regions[0x374D] != bytes.fromhex(
            "0657065726ff190bc07403a310645f07c3"
        ) or regions[0x37B3] != bytes.fromhex(
            "8bdc1e36c47f0426c5550c33c926874d08268b1db440cd21720233c01fca0400"
            "8bdc36c47f04268b1d83fb047606b43ecd21720233c0ca0400"
        ):
            raise ValueError("open cleanup dispatch/write/close bytes differ")
    text_contract = None
    if text_error:
        if not open_output:
            raise ValueError("text error requires checked open cleanup")
        from tools.liero_text_probe import original

        text_contract, text_regions = original(root)
        regions.update(
            {
                ip: raw
                for ip, raw in text_regions.items()
                if ip not in (0x1000, 0x37B3, 0x04F4)
            }
        )
        regions[0x3000] = text_regions[0x1000]
    if (
        regions[0x4F4] != bytes.fromhex("833e1064007501cba11064e90dfc")
        or regions[0x10F][:17] != bytes.fromhex("595beb07b8ff0033c933dbba71198edafb")
        or regions[0x10F][0x1E9 - 0x10F : 0x1F0 - 0x10F]
        != bytes.fromhex("a10664b44ccd21")
    ):
        raise ValueError("terminating original error bytes differ")
    header = int.from_bytes(binary[8:10], "little") * 16
    relocations = _mz_relocation_locations(binary, header)
    for ip, raw in regions.items():
        if ip == 0x3000:
            continue
        actual = {
            r - origin - ip
            for r in relocations
            if origin + ip - 1 <= r < origin + ip + len(raw)
        }
        if actual != ({12} if ip == 0x10F else set()):
            raise ValueError("terminating error MZ fixups differ")
    contract = {
        "oracle": "original010f-04f4-closed-object-actual-DOS-termination",
        "binary_sha256": hashlib.sha256(binary).hexdigest(),
        "regions": {str(ip): raw.hex() for ip, raw in regions.items()},
        "mz_DS_fixup": 0x11B,
        "scope": "empty descriptor/callback chains, closed D7B0 objects, owned saved vectors; diagnostic AH06 and real AH25/4c",
        "limitations": [
            "Not open-object flush/close, descriptor chains or actual cleanup callback provenance.",
            "INT21 saved/restored target is the disclosed observing fixture hook.",
            "Not integrated text-error, native Pascal ABI or normal-program reachability.",
        ],
        "whole_routine_accepted": False,
    }
    if open_output:
        contract.update(
            oracle="original010f-open-default-objects-flush-close-termination",
            scope="empty descriptor/callback chains, inputD7B1 and outputD7B2 with checked37b3/37d3 methods; actual DOS file/error6 or labeled injected5/6",
            limitations=[
                "Not integrated text-error caller, descriptor chains, actual cleanup callbacks, native ABI or normal-game reachability.",
                "INT21 saved/restored target is the disclosed observing fixture hook.",
                "Injected shortwrite/error outcomes are mechanism checks, not observed DOS errors.",
            ],
        )
    if text_error:
        contract.update(
            oracle="complete-original0037-nonzero04f4-open-cleanup-termination",
            text_contract=text_contract,
            scope="whole0037 text body to nonzero04f4 and010f, empty chains, checked default input/output cleanup, actual original0155:(CS+300) caller pair",
            limitations=[
                "Not descriptor chains, actual cleanup callbacks, native ABI or normal-game reachability.",
                "Video/input snapshot is at first output service before error diagnostics, not final diagnostic console screen.",
                "One actual invalid-handle6 case; other errors are explicitly injected mechanism cases.",
            ],
        )
    return contract, regions


def exit_assembly(raw: bytes, case: tuple[int, ...]) -> bytes:
    """Oracle: frozen declared error code/caller pair and direct or check entry."""
    code, offset, entry = case[:3]
    if (
        case not in EXIT_CASES
        and case not in OPEN_EXIT_CASES
        and case not in TEXT_EXIT_CASES
    ):
        raise ValueError("unsupported terminating error case")
    prefix = (
        f".set ERROR_CODE, {code}\n.set CALLER_OFFSET, {offset}\n"
        f".set ERROR_CHECK, {entry}\n"
    ).encode()
    if len(case) == 5:
        prefix += f".set OPEN_OUTPUT, 1\n.set SCENARIO, {case[3]}\n.set USED, {case[4]}\n".encode()
    if case in TEXT_EXIT_CASES:
        prefix += b".set TEXT_ERROR, 1\n"
    return prefix + raw


def exit_image(raw: bytes, regions: dict[int, bytes], segment: int = 0) -> bytes:
    """Oracle: original unchanged branches/calls; exactly authenticated DS relocation."""
    if not 0x1000 < len(raw) + 0x100 < 0x6000:
        raise ValueError("terminating harness bounds differ")
    image = bytearray(raw)
    required = max(ip + len(content) - 0x100 for ip, content in regions.items())
    if len(image) < required:
        image.extend(bytes(required - len(image)))
    for ip, content in regions.items():
        start = ip - 0x100
        if any(image[start : start + len(content)]):
            raise ValueError("terminating original-code hole occupied")
        image[start : start + len(content)] = content
    if segment:
        struct.pack_into("<H", image, 0x11B - 0x100, segment)
    else:
        # Patch the authenticated relocated immediate at runtime, before entry.
        # The COM loader does not perform MZ relocation.
        raise ValueError("terminating image requires explicit relocation binding")
    return bytes(image)


def exit_expected(trace: bytes, case: tuple[int, ...]) -> bytes:
    """Oracle: independently specified entire endpoint, vectors and diagnostic sequence."""
    if case in TEXT_EXIT_CASES:
        return text_exit_expected(trace, case)
    if len(case) == 5:
        return open_exit_expected(trace, case)
    if len(trace) != 885:
        raise ValueError("terminating error trace incomplete")
    code, offset, _ = case
    segment, ax, ds, ss, sp, bp, restores, count = struct.unpack_from("<8H", trace)
    text = (
        f"Runtime error {code & 255:03d} at 0200:{offset:04X}.\r\n".encode()
        if offset
        else b""
    )
    if (ax, ds, ss, sp, bp, restores, count) != (
        0x4C00 | (code & 255),
        segment,
        segment,
        0xEFEE,
        0x6789,
        19,
        len(text),
    ) or not 16 <= segment <= 0xDFFF:
        raise ValueError("terminating error exit/register/service state differs")
    globals_ = bytearray([0xA5] * 58)
    for cell, value in (
        (0x63E4, 0),
        (0x6402, 0),
        (0x6404, 0),
        (0x6406, code),
        (0x6408, offset),
        (0x640A, 0x200 if offset else 0),
        (0x640C, segment - 16),
        (0x6410, 0x67),
    ):
        struct.pack_into("<H", globals_, cell - 0x63D8, value)
    objects = bytearray(588)
    struct.pack_into("<H", objects, 2, 0xD7B0)
    struct.pack_into("<H", objects, 258, 0xD7B0)
    objects[512:] = trace[74 + 512 : 662]
    vectors = bytes.fromhex("00021b2123243435363738393a3b3c3d3e3f75")
    expected = (
        struct.pack("<8H", segment, ax, ds, ss, sp, bp, 19, len(text))
        + globals_
        + objects
        + vectors
        + objects[512:]
        + text
        + bytes(128 - len(text))
    )
    if trace != expected:
        raise ValueError(
            "terminating error global/object/vector/diagnostic residue differs"
        )
    return expected


def open_exit_expected(trace: bytes, case: tuple[int, ...]) -> bytes:
    """Oracle: flush-before-close even after failure; independent entire state/service sequence."""
    text_error = case in TEXT_EXIT_CASES
    if len(trace) != 1037 or (case not in OPEN_EXIT_CASES and not text_error):
        raise ValueError("open cleanup trace/case incomplete")
    code, offset, _, scenario, used = case
    segment = struct.unpack_from("<H", trace)[0]
    handle = struct.unpack_from("<H", trace, 885)[0]
    if not 16 <= segment <= 0xDFFF or not (
        handle == 0xFFFF if scenario == 1 else 4 < handle < 0xFFFF
    ):
        raise ValueError("open cleanup segment/handle identity differs")
    caller_segment = 0x300 if text_error else 0x200
    text = f"Runtime error {code & 255:03d} at {caller_segment:04X}:{offset:04X}.\r\n".encode()
    header = struct.pack(
        "<8H",
        segment,
        0x4C00 | (code & 255),
        segment,
        segment,
        0xDED2 if text_error else 0xEFEE,
        0xDFE2 if text_error else 0x6789,
        19,
        len(text),
    )
    if trace[:16] != header:
        raise ValueError("open cleanup termination/frame differs")
    sticky = 6 if scenario in (1, 3, 4) else 5 if scenario == 2 else code
    globals_ = bytearray([0xA5] * 58)
    for cell, value in (
        (0x63E4, 0),
        (0x6402, 0),
        (0x6404, 0),
        (0x6406, code),
        (0x6408, offset),
        (0x640A, caller_segment),
        (0x640C, segment - 16),
        (0x6410, sticky),
    ):
        struct.pack_into("<H", globals_, cell - 0x63D8, value)
    objects = bytearray(588)
    for relative, value in (
        (2, 0xD7B0),
        (28, 0x37D3),
        (30, segment),
        (256, handle),
        (258, 0xD7B0),
        (260, 128),
        (268, 0x7A70),
        (270, segment),
        (276, 0x37B3),
        (278, segment),
        (284, 0x37D3),
        (286, segment),
    ):
        struct.pack_into("<H", objects, relative, value)
    objects[384:512] = b"A" * 128
    if text_error:
        objects[384:386] = b"\r\n"
        struct.pack_into("<2H", objects, 280, 0x37B3, segment)
    objects[512:] = trace[586:662]
    vectors = bytes.fromhex("00021b2123243435363738393a3b3c3d3e3f75")
    service = struct.pack(
        "<12H",
        handle,
        2 if text_error else 1,
        1,
        used,
        0xD7B2,
        0,
        0xD7B2,
        0,
        handle,
        segment,
        0x7A70,
        0x12,
    )
    expected = (
        header
        + globals_
        + objects
        + vectors
        + objects[512:]
        + text
        + bytes(128 - len(text))
        + service
        + (b"\r\n" + bytes(126) if text_error else b"A" * used + bytes(128 - used))
    )
    if trace != expected:
        raise ValueError("open cleanup memory/service/diagnostic residue differs")
    return expected


def text_exit_expected(trace: bytes, case: tuple[int, ...]) -> bytes:
    """Oracle: actual text return address and whole video/input at first failing service."""
    if len(trace) != 5299 or case not in TEXT_EXIT_CASES:
        raise ValueError("integrated text error trace incomplete")
    open_exit_expected(trace[:1037], case)
    video = bytearray(b"\x2e\x4f" * 2000)
    position = (2 * 80 + 3) * 2
    video[position : position + 4] = b"A\x07B\x32"
    source = b"\x05A\x00\x02\x03B" + bytes(250)
    tail = struct.pack("<3H", 2, 0xD7B2, 0) + video + source
    if trace[1037:] != tail:
        raise ValueError("integrated text video/input/first-service differs")
    return trace


def run_exit(
    root: pathlib.Path,
    output: pathlib.Path,
    *,
    open_output: bool = False,
    text_error: bool = False,
) -> dict:
    """Oracle: freeze, original termination, installed source termination, immutable archive."""
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "BYOD original unavailable"}
    contract, regions = exit_contract(
        root, open_output=open_output, text_error=text_error
    )
    panel = (
        TEXT_EXIT_CASES
        if text_error
        else OPEN_EXIT_CASES
        if open_output
        else EXIT_CASES
    )
    inventory = TEXT_EXIT_SOURCES
    for tool in ("as", "ld", "dosbox", "fpc"):
        if not shutil.which(tool):
            raise FileNotFoundError(f"terminating error probe requires {tool}")
    sources = {name: (root / name).read_bytes() for name in inventory}
    output.mkdir()
    for name, raw in sources.items():
        path = output / "methods" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    pilot.save(
        output / "freeze.json",
        {
            "contract": contract,
            "cases": panel,
            "sources": {
                name: hashlib.sha256(raw).hexdigest() for name, raw in sources.items()
            },
            "policy": "Known human byte-derived recovery; no model/holdout/source promotion.",
        },
    )
    host = output / "host"
    host.mkdir()
    for name, raw in sources.items():
        if name.startswith("targets/"):
            (host / pathlib.Path(name).name).write_bytes(raw)
    build = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fi.", "-Fu.", "-FU.", "probe_liero_error_exit.pas"],
        cwd=host,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (host / "compile.log").write_bytes(build.stdout + build.stderr)
    build.check_returncode()
    for index, case in enumerate(panel):
        directory = output / f"case-{index}"
        directory.mkdir()
        assembly = exit_assembly(sources["tools/liero_error_exit_probe.S"], case)
        (directory / "harness.S").write_bytes(assembly)
        raw = assemble_probe(directory / "harness.S", directory)
        image = exit_image(raw, regions, 0x1971)
        (directory / "PROBE.COM").write_bytes(image)
        run_dosbox(directory)
        trace = (directory / "TRACE.BIN").read_bytes()
        exit_expected(trace, case)
        segment = struct.unpack_from("<H", trace)[0]
        handle = struct.unpack_from("<H", trace, 885)[0] if open_output else None
        code = bytearray(65536)
        for ip, content in regions.items():
            code[ip : ip + len(content)] = content
        struct.pack_into("<H", code, 0x11B, segment)
        (host / "CODE.BIN").write_bytes(code)
        (host / "VECTORS.BIN").write_bytes(trace[74 + 512 : 662])
        arguments = [
            str(host / "probe_liero_error_exit"),
            str(segment),
            *map(str, case),
        ]
        if handle is not None:
            arguments.append(str(handle))
        execution = subprocess.run(
            arguments,
            cwd=host,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (directory / "host.log").write_bytes(execution.stdout + execution.stderr)
        if execution.returncode != case[0] & 255:
            raise ValueError(
                f"installed error handler did not terminate with status {case[0] & 255}"
            )
        candidate = (host / "PASCAL.BIN").read_bytes()
        (directory / "PASCAL.BIN").write_bytes(candidate)
        if candidate != trace:
            raise ValueError(f"installed terminating error differs at case {index}")
        if open_output:
            if len(case) != 5:
                raise ValueError("open cleanup requires a complete service case")
            expected_output = b"A" * case[4] if case[3] == 0 else b""
            if (directory / "OUTPUT.BIN").read_bytes() != expected_output or (
                host / "OUTPUT.BIN"
            ).read_bytes() != expected_output:
                raise ValueError("open cleanup actual file output differs")
            (directory / "HOST-OUTPUT.BIN").write_bytes(
                (host / "OUTPUT.BIN").read_bytes()
            )
    if exit_contract(root, open_output=open_output, text_error=text_error)[
        0
    ] != contract or any(
        (root / name).read_bytes() != raw for name, raw in sources.items()
    ):
        raise ValueError("terminating error method changed during evaluation")
    result = {
        "status": "passed",
        "cases": len(panel),
        "matches": len(panel),
        "scope": contract["scope"],
        "whole_routine_accepted": False,
        "source_promotions": 0,
        "limitations": contract["limitations"],
    }
    pilot.save(output / "result.json", result)
    seal_archive(output)
    return result


def replay_exit(
    root: pathlib.Path,
    output: pathlib.Path,
    *,
    open_output: bool = False,
    text_error: bool = False,
) -> dict:
    """Oracle: sealed no-execution replay; all terminating endpoints independently checked."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    panel = (
        TEXT_EXIT_CASES
        if text_error
        else OPEN_EXIT_CASES
        if open_output
        else EXIT_CASES
    )
    contract, regions = exit_contract(
        root, open_output=open_output, text_error=text_error
    )
    if (
        frozen["contract"] != contract
        or frozen["cases"] != [list(case) for case in panel]
        or set(frozen["sources"])
        not in (set(EXIT_SOURCES), set(OPEN_EXIT_SOURCES), set(TEXT_EXIT_SOURCES))
    ):
        raise ValueError("terminating error frozen contract differs")
    for name, identity in frozen["sources"].items():
        raw = archive["methods/" + name]
        if hashlib.sha256(raw).hexdigest() != identity:
            raise ValueError("terminating source differs")
        if (
            name.startswith("targets/")
            and archive["host/" + pathlib.Path(name).name] != raw
        ):
            raise ValueError("terminating candidate source differs")
    for index, case in enumerate(panel):
        prefix = f"case-{index}/"
        if archive[prefix + "harness.S"] != exit_assembly(
            archive["methods/tools/liero_error_exit_probe.S"], case
        ):
            raise ValueError("terminating harness differs")
        if archive[prefix + "PROBE.COM"] != exit_image(
            archive[prefix + "harness.bin"], regions, 0x1971
        ):
            raise ValueError("terminating original image differs")
        expected = exit_expected(archive[prefix + "TRACE.BIN"], case)
        if archive[prefix + "PASCAL.BIN"] != expected:
            raise ValueError("terminating candidate endpoint differs")
        if open_output:
            if len(case) != 5:
                raise ValueError("open cleanup requires a complete service case")
            expected_output = b"A" * case[4] if case[3] == 0 else b""
            if (
                archive[prefix + "OUTPUT.BIN"] != expected_output
                or archive[prefix + "HOST-OUTPUT.BIN"] != expected_output
            ):
                raise ValueError("open cleanup saved output differs")
    result = json.loads(archive["result.json"])
    if result != {
        "status": "passed",
        "cases": len(panel),
        "matches": len(panel),
        "scope": contract["scope"],
        "whole_routine_accepted": False,
        "source_promotions": 0,
        "limitations": contract["limitations"],
    }:
        raise ValueError("terminating result claims differ")
    return result


if __name__ == "__main__":
    raise SystemExit(main())
