"""Bounded original011a..016d error-address translation versus Pascal; stop before cleanup."""

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

RAW = bytes.fromhex(
    "ba71198edafba306648bc10bc3743da1e4630bc0742f8ec026a110000bc0741b"
    "2bc37717f7d83d00107310ba1000f7e203c17207263b060800720626a11400ebd1"
    "8bc88cc32b1e0c6483eb10890e0864891e0a64"
)
WINDOW = (0x63D8, 0x6412)
RECORD_BYTES = 16 + WINDOW[1] - WINDOW[0] + 512
Case = tuple[int, int, int, int, int, int, int]


def checked_contract(root: pathlib.Path) -> tuple[bytes, dict]:
    """Oracle: actual original instruction bytes and exclusive source-DS MZ relocation."""
    binary, allocator, _ = pilot.allocator_deduction_inputs(root)
    start = allocator["file_offset"] + 0x11A - 0x353
    header = int.from_bytes(binary[8:10], "little") * 16
    if binary[start : start + len(RAW)] != RAW or {
        r - start
        for r in _mz_relocation_locations(binary, header)
        if start - 1 <= r < start + len(RAW)
    } != {1}:
        raise ValueError("error translation bytes or exclusive DS relocation differ")
    return binary, {
        "oracle": "owned_two_descriptor_error_translation_original_vs_pascal",
        "binary_sha256": pilot.digest(root / "extracted/liero/LIERO.EXE"),
        "file_offset": start,
        "bytes_hex": RAW.hex(),
        "relocation_offsets": [1],
        "entry": 0x11A,
        "stop": 0x16E,
        "branches": {
            "zero_caller": 0x166,
            "end_chain": 0x15F,
            "skip_descriptor": 0x155,
            "found": 0x15B,
            "next": 0x12C,
        },
        "fields": {"size_exclusive": 8, "base_paragraph": 16, "next_segment": 20},
        "semantics": [
            "Nonzero caller pair scans DS63e4 segment chain; null chain falls back to original caller pair.",
            "Skip zero descriptor base, base above caller segment, paragraph difference>=4096, offset carry, or offset>=size.",
            "First matching descriptor returns computed offset and descriptor segment; otherwise original caller offset/segment.",
            "Normalize nonzero caller path segment by subtracting saved PSP DS640c and16 modulo65536.",
            "Zero caller pair bypasses chain and normalization and stores zero/zero.",
            "DS6406 receives entryAX; DS6408/640a receive translated pair; no other writes before016e.",
        ],
        "preconditions": [
            "Controlled COM DS=SS=CS with64KiB allocation, code/records below6000, stackeff0.",
            "Source DS relocated to COM CS through original relocation word only; other source bytes unchanged.",
            "Zero/one/two acyclic descriptors at CS+0800/0810, fields inside owned8000..8200.",
            "DS63e4 initial chain and DS640c=CS-16 are supplied fixture state, not actual runtime provenance.",
            "Only entry011a projection is executed; jump at016e stops before cleanup/callbacks/services.",
            "STI remains original; no asynchronous guest memory mutation within measured regions is modeled.",
        ],
        "unresolved": [
            "actual63e4 descriptor provenance, arbitrary chain topology/aliasing and lifetime",
            "010f caller-stack transfer not executed in this fixture",
            "016e cleanup callbacks, services, failure termination and full ABI",
        ],
        "source_recovered": False,
    }


def cases(suite: str) -> list[Case]:
    """Oracle: frozen branch/boundary fixtures; disjoint request-offset values, not unseen recovery."""
    if suite not in ("training", "heldout"):
        raise ValueError("unknown error translation suite")
    offsets = (0, 1, 7, 0x7FFF, 0xFFFF) if suite == "training" else (8, 16, 0x8000)
    topologies = (
        (0, 0, 0, 0, 0),
        (1, 0, 0xFFFF, 0, 0),
        (1, 0x4001, 0xFFFF, 0, 0),
        (1, 0x4000, 1, 0, 0),
        (1, 0x4000, 0xFFFF, 0, 0),
        (1, 0x3FFF, 16, 0, 0),
        (1, 0x3FFF, 0xFFFF, 0, 0),
        (1, 0x3000, 0xFFFF, 0, 0),
        (1, 0x3001, 0xFFFF, 0, 0),
        (2, 0, 0xFFFF, 0x4000, 0xFFFF),
        (2, 0x4000, 1, 0x4000, 0xFFFF),
        (2, 0x4000, 0xFFFF, 0x4000, 0xFFFF),
    )
    result = [
        (offset, 0x4000, *topology) for offset in offsets for topology in topologies
    ]
    result.append(
        (0, 0, 2, 0x4000, 0xFFFF, 0x4000, 0xFFFF)
        if suite == "training"
        else (0, 0, 0, 0, 0, 0, 0)
    )
    return result


def validate_case(case: Case) -> None:
    """Oracle: no dynamic pointers/cycles outside owned descriptor initialization."""
    if len(case) != 7 or any(
        type(value) is not int or not 0 <= value <= 65535 for value in case
    ):
        raise ValueError("unsupported error translation case words")
    if case[2] not in (0, 1, 2):
        raise ValueError("unsupported error translation descriptor count")


def descriptor_memory(case: Case, segment: int) -> bytes:
    """Oracle: exact owned512-byte initialization, including untouched descriptor/guard bytes."""
    memory = bytearray([0xA5] * 512)
    for index in range(case[2]):
        base = index * 0x100
        following = segment + 0x810 if index == 0 and case[2] == 2 else 0
        for field, value in (
            (8, case[4 + index * 2]),
            (16, case[3 + index * 2]),
            (20, following),
        ):
            struct.pack_into("<H", memory, base + field, value)
    return bytes(memory)


def harness(case_path: pathlib.Path, count: int) -> str:
    """Oracle: bounded capture below globals, original entry/stop, no fake cleanup or return."""
    if not 1 <= count <= 16:
        raise ValueError("error translation capture batch exceeds16")
    return f""".code16
.global _start
_start:
    jmp setup
.org 0x1000-0x100
setup:
    mov %cs, %ax
    cmp $0xefff, %ax
    ja failed
    mov %cs, %dx
    add $0x1000, %dx
    cmp %es:2, %dx
    ja failed
    cli
    mov %ax, %ss
    mov $0xeff0, %sp
    sti
    mov %ax, %ds
    mov %ax, %es
    mov %ax, 0x11b
    mov $inputs, %bp
    mov $records, %di
    mov ${count}, %dx
    mov %dx, remaining
next_case:
    push %di
    mov $0x63d8, %di
    mov $58, %cx
    mov $0xa5, %al
    cld
    rep stosb
    mov $0x8000, %di
    mov $512, %cx
    rep stosb
    mov %cs, %ax
    sub $16, %ax
    mov %ax, 0x640c
    movw $0, 0x63e4
    cmpw $0, 4(%bp)
    je initialized
    mov %cs, %ax
    add $0x800, %ax
    mov %ax, 0x63e4
    mov 6(%bp), %ax
    mov %ax, 0x8010
    mov 8(%bp), %ax
    mov %ax, 0x8008
    movw $0, 0x8014
    cmpw $2, 4(%bp)
    jne initialized
    mov %cs, %ax
    add $0x810, %ax
    mov %ax, 0x8014
    mov 10(%bp), %ax
    mov %ax, 0x8110
    mov 12(%bp), %ax
    mov %ax, 0x8108
    movw $0, 0x8114
initialized:
    pop %di
    mov (%bp), %cx
    mov 2(%bp), %bx
    mov $203, %ax
    jmp 0x11a
collector:
    mov %ax, 14(%di)
    mov %cs, (%di)
    mov %cx, 2(%di)
    mov %bx, 4(%di)
    mov %ds, 6(%di)
    mov %es, 8(%di)
    mov %sp, 10(%di)
    pushf
    popw 12(%di)
    push %cs
    pop %es
    add $16, %di
    mov $0x63d8, %si
    mov $58, %cx
    cld
    rep movsb
    mov $0x8000, %si
    mov $512, %cx
    rep movsb
    add $14, %bp
    decw remaining
    jnz next_case
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, %bx
    mov $records, %dx
    mov ${count * RECORD_BYTES}, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp ${count * RECORD_BYTES}, %ax
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
remaining: .word 0
inputs: .incbin "{case_path}"
records: .space {count * RECORD_BYTES}
"""


def build_image(assembly: bytes) -> bytes:
    """Oracle: copied original bytes with exactly one runtime DS relocation and explicit stop JMP."""
    if len(assembly) + 0x100 >= 0x6000 or len(assembly) < 0x1000 - 0x100:
        raise ValueError("error translation harness/global bounds differ")
    image = bytearray(assembly)
    begin = 0x11A - 0x100
    if any(image[begin : begin + len(RAW) + 3]):
        raise ValueError("error translation copied bytes overlap harness")
    image[begin : begin + len(RAW)] = RAW
    return bytes(image)


def original_batch(
    root: pathlib.Path, output: pathlib.Path, inputs: list[Case]
) -> bytes:
    """Oracle: original prefix with relocated DS plus stop before external cleanup; actual DOSBox."""
    checked_contract(root)
    for case in inputs:
        validate_case(case)
    output.mkdir()
    path = output / "CASES.BIN"
    path.write_bytes(b"".join(struct.pack("<7H", *case) for case in inputs))
    (output / "harness.S").write_text(harness(path.resolve(), len(inputs)))
    raw = assemble_probe(output / "harness.S", output)
    image = bytearray(build_image(raw))
    symbols = subprocess.run(
        ["nm", str(output / "probe.o")],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    ).stdout
    (output / "symbols.txt").write_text(symbols)
    labels = {
        line.split()[-1]: int(line.split()[0], 16) + 0x100
        for line in symbols.splitlines()
    }
    struct.pack_into(
        "<BH", image, 0x16E - 0x100, 0xE9, (labels["collector"] - 0x171) & 65535
    )
    (output / "PROBE.COM").write_bytes(image)
    run_dosbox(output)
    trace = (output / "TRACE.BIN").read_bytes()
    projection(trace, inputs)
    return trace


def projection(trace: bytes, inputs: list[Case]) -> tuple[bytes, list[int]]:
    """Oracle: complete trace, all512 descriptor bytes and58 globals; only declared stores allowed."""
    if len(trace) != len(inputs) * RECORD_BYTES:
        raise ValueError("error translation trace shape differs")
    result, segments = bytearray(), []
    for index, case in enumerate(inputs):
        row = trace[index * RECORD_BYTES : (index + 1) * RECORD_BYTES]
        segment, cx, bx, ds, es, sp, flags, _ = struct.unpack_from("<8H", row)
        if (
            not 0x10 <= segment <= 0xEFFF
            or ds != segment
            or sp != 0xEFF0
            or not flags & 0x200
        ):
            raise ValueError("error translation segment/stack/IF premise differs")
        if es not in (segment, segment + 0x800, segment + 0x810):
            raise ValueError("error translation escaped declared descriptors")
        expected = bytearray([0xA5] * 58)
        for cell, value in (
            (0x63E4, segment + 0x800 if case[2] else 0),
            (0x640C, segment - 16),
            (0x6406, 203),
            (0x6408, cx),
            (0x640A, bx),
        ):
            struct.pack_into("<H", expected, cell - WINDOW[0], value)
        if row[16:74] != expected or row[74:] != descriptor_memory(case, segment):
            raise ValueError(
                "error translation global/descriptor memory residue differs"
            )
        result.extend(struct.pack("<2H", cx, bx))
        segments.append(segment)
    return bytes(result), segments


def candidate_source() -> str:
    """Oracle: deterministic Pascal of known byte-derived scoped semantics, not historical identifiers."""
    return """procedure TranslateError(callerOffset, callerSegment, codeSegment,
  nodeCount, firstBase, firstSize, secondBase, secondSize: Word;
  var translatedOffset, translatedSegment: Word);
var index, baseParagraph, bound, nodeSegment: Word; delta, position: LongWord;
begin
  translatedOffset := callerOffset; translatedSegment := callerSegment;
  if (callerOffset = 0) and (callerSegment = 0) then Exit;
  for index := 1 to nodeCount do
  begin
    if index = 1 then
    begin baseParagraph := firstBase; bound := firstSize; nodeSegment := codeSegment + $800 end
    else
    begin baseParagraph := secondBase; bound := secondSize; nodeSegment := codeSegment + $810 end;
    if (baseParagraph <> 0) and (baseParagraph <= callerSegment) then
    begin
      delta := LongWord(callerSegment) - baseParagraph;
      if delta < $1000 then
      begin
        position := delta * 16 + callerOffset;
        if (position <= $ffff) and (position < bound) then
        begin
          translatedOffset := position; translatedSegment := nodeSegment;
          Break
        end
      end
    end
  end;
  translatedSegment := (LongWord(translatedSegment) + $10000 - codeSegment) and $ffff;
end;
"""


def candidate_program(inputs: list[Case], segments: list[int]) -> str:
    """Oracle: exact observed COM segment supplies normalization, not native pointers."""
    if len(inputs) != len(segments):
        raise ValueError("error translation candidate segment count differs")
    statements = "\n".join(
        f"  Run({case[0]}, {case[1]}, {segment}, {', '.join(map(str, case[2:]))});"
        for case, segment in zip(inputs, segments, strict=True)
    )
    return f"""program ErrorAddressProjection;
{{$I candidate.inc}}
var f: file; row: array[0..1] of Word; written: LongInt;
procedure Run(callerOffset, callerSegment, codeSegment, nodeCount,
  firstBase, firstSize, secondBase, secondSize: Word);
begin
  TranslateError(callerOffset, callerSegment, codeSegment, nodeCount,
    firstBase, firstSize, secondBase, secondSize, row[0], row[1]);
  BlockWrite(f, row, SizeOf(row), written);
  if written <> SizeOf(row) then Halt(2);
end;
begin
  Assign(f, 'PASCAL.BIN'); Rewrite(f, 1);
{statements}
  Close(f);
end.
"""


def candidate(output: pathlib.Path, inputs: list[Case], segments: list[int]) -> bytes:
    """Oracle: actual FPC-Mtp-Cr compile/run of exact frozen candidate."""
    output.mkdir()
    (output / "candidate.inc").write_text(candidate_source())
    (output / "probe.pas").write_text(candidate_program(inputs, segments))
    for name, command in (
        ("compile.log", ["fpc", "-Mtp", "-Cr", "probe.pas"]),
        ("execution.log", [str((output / "probe").resolve())]),
    ):
        result = subprocess.run(
            command, cwd=output, capture_output=True, timeout=30, check=False
        )
        (output / name).write_bytes(result.stdout + result.stderr)
        result.check_returncode()
    data = (output / "PASCAL.BIN").read_bytes()
    if len(data) != 4 * len(inputs):
        raise ValueError("error translation Pascal trace shape differs")
    return data


def freeze_method(root: pathlib.Path, contract: dict) -> dict:
    """Oracle: candidate/corpora/method/budget fixed before either execution suite."""
    paths = (
        "tools/liero_error_address_probe.py",
        "tools/liero_four_routine_pilot.py",
        "tools/liero_file_probe.py",
        "engine/alternate_streams.py",
        "engine/instruction_facts.py",
        "engine/routine_contract.py",
        "targets/liero/config/routine_contracts.json",
        "targets/liero/alternate_streams.json",
    )
    return {
        "contract": contract,
        "source_sha256": hashlib.sha256(candidate_source().encode()).hexdigest(),
        "method_hashes": {name: pilot.digest(root / name) for name in paths},
        "training": [list(case) for case in cases("training")],
        "heldout": [list(case) for case in cases("heldout")],
        "budget": {
            "candidates": 1,
            "model_requests": 0,
            "repairs": 0,
            "terminal_evaluations": 1,
        },
        "scope": "developer-known prefix, owned descriptor fixture; not automatic recovery or actual error-path reachability",
    }


def compare(expected: bytes, observed: bytes, count: int) -> dict:
    """Oracle: complete output pairs only; original memory guards checked separately before scoring."""
    if len(expected) != count * 4 or len(observed) != len(expected):
        raise ValueError("error translation comparison shape differs")
    mismatches = [
        i
        for i in range(count)
        if expected[i * 4 : i * 4 + 4] != observed[i * 4 : i * 4 + 4]
    ]
    return {
        "cases": count,
        "passed": count - len(mismatches),
        "mismatch_indices": mismatches,
    }


def run(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: one frozen candidate, training gates exactly one terminal suite; no repair/retry."""
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "Liero BYOD unavailable"}
    _, contract = checked_contract(root)
    freeze = freeze_method(root, contract)
    output.mkdir(parents=True, exist_ok=False)
    pilot.save(output / "freeze.json", freeze)
    (output / "candidate.inc").write_text(candidate_source())
    (output / "methods").mkdir()
    for name in freeze["method_hashes"]:
        shutil.copy2(root / name, output / "methods" / pathlib.Path(name).name)
    result = {
        "status": "failed",
        "oracle": contract["oracle"],
        "model_requests": 0,
        "heldout_evaluations": 0,
        "source_promoted": False,
        "routine_recovered": False,
        "unresolved": contract["unresolved"],
    }

    def validate_frozen() -> None:
        """Oracle: fail closed on before/after source/method/premise drift."""
        _, current = checked_contract(root)
        if (
            freeze_method(root, current) != freeze
            or json.loads((output / "freeze.json").read_text()) != freeze
            or (output / "candidate.inc").read_text() != candidate_source()
        ):
            raise ValueError("error translation freeze/premises/source changed")

    try:
        for suite in ("training", "heldout"):
            validate_frozen()
            inputs = cases(suite)
            if suite == "heldout":
                result["heldout_evaluations"] = 1
            directory = output / f"original-{suite}"
            directory.mkdir()
            trace = b"".join(
                original_batch(
                    root, directory / f"part-{begin // 16}", inputs[begin : begin + 16]
                )
                for begin in range(0, len(inputs), 16)
            )
            expected, segments = projection(trace, inputs)
            observed = candidate(output / f"candidate-{suite}", inputs, segments)
            result[suite] = compare(expected, observed, len(inputs))
            validate_frozen()
            if result[suite]["mismatch_indices"]:
                result["stop_reason"] = f"{suite}-failure-no-retry"
                break
        else:
            result.update(
                status="passed", stop_reason="bounded-error-translation-validated"
            )
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        result.update(
            error=f"{type(exc).__name__}: {exc}", stop_reason="first-error-no-retry"
        )
    result["freeze_sha256"] = pilot.digest(output / "freeze.json")
    result["artifact_hashes"] = {
        str(path.relative_to(output)): pilot.digest(path)
        for path in output.rglob("*")
        if path.is_file()
    }
    pilot.save(output / "result.json", result)
    return result


def validate_report(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: saved original image/corpus/memory/Pascal replay; never another terminal evaluation."""
    _, contract = checked_contract(root)
    freeze = freeze_method(root, contract)
    report = json.loads((output / "result.json").read_text())
    if (
        json.loads((output / "freeze.json").read_text()) != freeze
        or report["freeze_sha256"] != pilot.digest(output / "freeze.json")
        or report["status"] != "passed"
        or report["oracle"] != contract["oracle"]
        or report["unresolved"] != contract["unresolved"]
        or report["heldout_evaluations"] != 1
        or report["model_requests"] != 0
        or report["source_promoted"] is not False
        or report["routine_recovered"] is not False
        or (output / "candidate.inc").read_text() != candidate_source()
    ):
        raise ValueError("error translation report/source/freeze invalid")
    required = {"freeze.json", "candidate.inc"}
    for name, identity in freeze["method_hashes"].items():
        saved = f"methods/{pathlib.Path(name).name}"
        required.add(saved)
        if pilot.digest(output / saved) != identity:
            raise ValueError("error translation saved method differs")
    for suite in ("training", "heldout"):
        inputs = cases(suite)
        traces = []
        for begin in range(0, len(inputs), 16):
            batch = inputs[begin : begin + 16]
            prefix = f"original-{suite}/part-{begin // 16}"
            directory = output / prefix
            required.update(
                f"{prefix}/{name}"
                for name in (
                    "CASES.BIN",
                    "harness.S",
                    "harness.bin",
                    "symbols.txt",
                    "PROBE.COM",
                    "TRACE.BIN",
                )
            )
            if (directory / "CASES.BIN").read_bytes() != b"".join(
                struct.pack("<7H", *case) for case in batch
            ) or (directory / "harness.S").read_text() != harness(
                (directory / "CASES.BIN").resolve(), len(batch)
            ):
                raise ValueError("error translation saved corpus/harness differs")
            labels = {
                line.split()[-1]: int(line.split()[0], 16) + 0x100
                for line in (directory / "symbols.txt").read_text().splitlines()
            }
            image = bytearray(build_image((directory / "harness.bin").read_bytes()))
            struct.pack_into(
                "<BH", image, 0x16E - 0x100, 0xE9, (labels["collector"] - 0x171) & 65535
            )
            if bytes(image) != (directory / "PROBE.COM").read_bytes():
                raise ValueError("error translation saved original image differs")
            data = (directory / "TRACE.BIN").read_bytes()
            projection(data, batch)
            traces.append(data)
        expected, segments = projection(b"".join(traces), inputs)
        prefix = f"candidate-{suite}"
        directory = output / prefix
        required.update(
            f"{prefix}/{name}"
            for name in (
                "candidate.inc",
                "probe.pas",
                "probe",
                "compile.log",
                "execution.log",
                "PASCAL.BIN",
            )
        )
        if (directory / "candidate.inc").read_text() != candidate_source() or (
            directory / "probe.pas"
        ).read_text() != candidate_program(inputs, segments):
            raise ValueError("error translation saved Pascal source differs")
        measured = compare(
            expected, (directory / "PASCAL.BIN").read_bytes(), len(inputs)
        )
        if measured != report[suite] or measured["passed"] != len(inputs):
            raise ValueError("error translation saved comparison differs or failed")
    if not required <= report["artifact_hashes"].keys():
        raise ValueError("error translation required artifact hashes missing")
    for name, identity in report["artifact_hashes"].items():
        path = (output / name).resolve()
        if not path.is_relative_to(output.resolve()) or pilot.digest(path) != identity:
            raise ValueError("error translation saved artifact changed")
    return report


def main() -> int:
    """Oracle: pass/failure/skip CLI; replay does not run original or Pascal again."""
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
    return 0 if result["status"] in {"passed", "skipped"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
