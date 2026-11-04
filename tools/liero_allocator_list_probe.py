"""Bounded nonempty-list allocator projection using existing original-byte COM tooling."""

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

from tools import liero_four_routine_pilot as pilot
from tools.liero_file_probe import assemble_probe, run_dosbox

RECORD_BYTES = 584
PROJECTION_BYTES = 528


def validate_case(case: tuple[int, int, int, int]) -> None:
    """Oracle: finite acyclic two-node fixture, aligned owned memory and bounded split header."""
    request, first, second, offset = case
    if (
        any(type(value) is not int for value in case)
        or not 0 <= request <= 160
        or not 8 <= first <= 128
        or first % 8
        or not 0 <= second <= 128
        or second % 8
        or offset not in (0, 8)
    ):
        raise ValueError("unsupported bounded allocator list case")


def list_cases(suite: str) -> list[tuple[int, int, int, int]]:
    """Oracle: frozen disjoint request sets; developer-known topology, not generalization."""
    if suite not in ("training", "heldout"):
        raise ValueError("unknown allocator list suite")
    requests = (0, 1, 8, 16, 64, 144) if suite == "training" else (2, 9, 24, 128)
    return [
        (request, first, second, offset)
        for request in requests
        for first in (8, 32, 96)
        for second in (0, 128)
        for offset in (0, 8)
    ]


def list_contract(root: pathlib.Path) -> tuple[bytes, dict, dict]:
    """Oracle: exact bytes/real MZ exclusions plus scoped field/branch deduction."""
    binary, contract, base = pilot.allocator_deduction_inputs(root)
    raw = bytes.fromhex(base["routine_bytes_hex"])
    branches = {}
    for name, address in (
        ("sentinel", 0x371),
        ("next_paragraph", 0x377),
        ("fit_paragraph", 0x379),
        ("next_offset", 0x37F),
        ("exact", 0x38C),
    ):
        offset = address - 0x353
        branches[name] = (
            address
            + 2
            + int.from_bytes(raw[offset + 1 : offset + 2], "little", signed=True)
        )
    facts = {
        "oracle": "exact_allocator_nonempty_list_under_owned_fixture",
        "binary_sha256": base["binary_sha256"],
        "allocator_bytes_hex": raw.hex(),
        "helper_bytes_hex": base["helper_bytes_hex"],
        "callback_bytes_hex": base["callback_bytes_hex"],
        "branches": branches,
        "node_fields": {
            "next_offset": 0,
            "next_segment": 2,
            "size_offset": 4,
            "size_paragraphs": 6,
        },
        "selection": "unsigned size paragraphs then offset; first fit, exact bypasses split",
        "split": "new header after rounded allocation; remaining pair uses SUB/SBB then offset AND15",
        "predecessor": "CX:BX identifies predecessor next-pointer cell, initially DS63f6",
        "heap_window": [0x8000, 0x8200],
        "node_origins": [[0, 0x800], [0, 0x810]],
        "frontier": [0, 0x900],
        "limit": [0, 0xA00],
        "preconditions": [
            "COM allocation covers64KiB; DS=SS=CS, stackeff0, no asynchronous mutation.",
            "Nodes at8000+offset/8100+offset, aligned0 or8, sizes8..128; absent second has size0.",
            "Next chain is first->second->frontier or first->frontier; no cycles.",
            "Every accessed header and remainder header is within owned8000..8200.",
            "Code/harness below6000, globals63d8..6402/7b3c, frontier9000, stackeff0 are disjoint.",
            "Only original default callback00d6 is installed; relative segments cannot wrap.",
        ],
        "unresolved": [
            "arbitrary list topology/aliasing and normal-program heap lifetime",
            "nondefault callback targets/effects/retry",
            "full register/flag ABI and actual028a/010f applicability",
        ],
        "source_recovered": False,
    }
    return binary, contract, facts


def _replace_once(source: str, old: str, new: str) -> str:
    """Oracle: exact existing harness anchor; drift is an error rather than a patched guess."""
    if source.count(old) != 1:
        raise ValueError("allocator base harness shape changed")
    return source.replace(old, new, 1)


def list_harness(case_path: pathlib.Path, count: int) -> str:
    """Oracle: reuse COM runner with explicit owned nodes and complete512-byte heap capture."""
    if type(count) is not int or not 1 <= count <= 16:
        raise ValueError(
            "allocator list batch must fit disjoint code/records below6000"
        )
    source = pilot.allocator_harness(case_path, count)
    begin = source.index("    mov 2(%si), %ax\n")
    end = source.index("    mov (%si), %ax\n", begin)
    setup = """
    movw $0, 0x63ee
    mov %cs, %ax
    add $0x900, %ax
    mov %ax, 0x63f0
    mov %ax, %dx
    movw $0, 0x63f2
    mov %cs, %ax
    add $0xa00, %ax
    mov %ax, 0x63f4
    mov 6(%si), %di
    mov %di, 0x63f6
    add $0x8000, %di
    mov %cs, %ax
    add $0x800, %ax
    mov %ax, 0x63f8
    cmpw $0, 4(%si)
    je one_node
    mov 6(%si), %ax
    mov %ax, (%di)
    mov %cs, %ax
    add $0x810, %ax
    mov %ax, 2(%di)
    jmp first_size
one_node:
    movw $0, (%di)
    mov %dx, 2(%di)
first_size:
    mov 2(%si), %ax
    mov %ax, %bx
    and $15, %ax
    mov %ax, 4(%di)
    shr $4, %bx
    mov %bx, 6(%di)
    cmpw $0, 4(%si)
    je initialized
    add $0x100, %di
    movw $0, (%di)
    mov %dx, 2(%di)
    mov 4(%si), %ax
    mov %ax, %bx
    and $15, %ax
    mov %ax, 4(%di)
    shr $4, %bx
    mov %bx, 6(%di)
initialized:
    movw $0xd6, 0x63fe
    mov %cs, %ax
    mov %ax, 0x6400
"""
    source = source[:begin] + setup + source[end:]
    source = source.replace("mov $128, %cx", "mov $512, %cx")
    source = _replace_once(source, "add $10, %si", "add $8, %si")
    source = source.replace(str(count * 200), str(count * RECORD_BYTES))
    return source


def _original_batch(
    root: pathlib.Path, output: pathlib.Path, cases: list[tuple]
) -> bytes:
    """Oracle: actual allocator/helper/default bytes, existing DOSBox and owned COM allocation."""
    for case in cases:
        validate_case(case)
    binary, contract, _ = list_contract(root)
    output.mkdir()
    case_path = output / "CASES.BIN"
    case_path.write_bytes(b"".join(struct.pack("<4H", *case) for case in cases))
    path = output / "harness.S"
    path.write_text(list_harness(case_path.resolve(), len(cases)))
    harness = assemble_probe(path, output)
    if len(harness) + 0x100 >= 0x6000:
        raise ValueError("allocator list harness overlaps globals")
    image = bytearray(harness)
    for address, size in ((0x353, 203), (0x4DC, 17)):
        raw = binary[
            contract["file_offset"] + address - 0x353 : contract["file_offset"]
            + address
            - 0x353
            + size
        ]
        begin = address - 0x100
        if any(image[begin : begin + size]):
            raise ValueError("allocator original bytes overlap list harness")
        image[begin : begin + size] = raw
    (output / "PROBE.COM").write_bytes(image)
    run_dosbox(output)
    trace = (output / "TRACE.BIN").read_bytes()
    original_projection(trace, cases)
    return trace


def original(root: pathlib.Path, output: pathlib.Path, cases: list[tuple]) -> bytes:
    """Oracle: predeclared16-case batching keeps records disjoint from global/heap cells."""
    output.mkdir()
    return b"".join(
        _original_batch(root, output / f"part-{begin // 16}", cases[begin : begin + 16])
        for begin in range(0, len(cases), 16)
    )


def original_projection(trace: bytes, cases: list[tuple]) -> tuple[bytes, list[int]]:
    """Oracle: complete original records, protected globals and relative result plus full heap."""
    if len(trace) != len(cases) * RECORD_BYTES:
        raise ValueError("allocator list original trace shape differs")
    records, segments = [], []
    for index, case in enumerate(cases):
        row = trace[index * RECORD_BYTES : (index + 1) * RECORD_BYTES]
        fields = struct.unpack_from("<8H", row)
        memory = row[16:72]
        segment = struct.unpack_from("<H", memory, 40)[0]
        expected = {
            0x63EE: fields[3],
            0x63F0: segment + fields[4],
            0x63F2: 0,
            0x63F4: segment + 0xA00,
            0x63F6: fields[5],
            0x63F8: segment + fields[6],
            0x63FE: 0xD6,
            0x6400: segment,
        }
        allowed = {byte for cell in expected for byte in (cell, cell + 1)}
        if (
            not 0 < segment <= 0xEFFF
            or fields[2] not in (0, 1)
            or fields[7] != (case[0] if case[0] else 0xA5A5)
            or any(
                struct.unpack_from("<H", memory, cell - 0x63D8)[0] != value
                for cell, value in expected.items()
            )
            or any(
                value != 0xA5
                for cell, value in enumerate(memory, 0x63D8)
                if cell not in allowed
            )
        ):
            raise ValueError(
                "allocator list original globals/segment projection differs"
            )
        records.append(row[:16] + row[72:])
        segments.append(segment)
    return b"".join(records), segments


def candidate_source() -> str:
    """Oracle: deductive bounded memory projection; names are descriptive, not recovered spelling."""
    return """
type THeap = array[0..255] of Word;
procedure FUN_24dd_0353(requestSize, codeSegment: Word;
  var resultOffset, resultSegment, frontierOffset, frontierSegment,
  headOffset, headSegment, savedRequest: Word; var failed: Word; var heap: THeap);
var rounded, available, remaining: LongWord;
    nodeOffset, nodeSegment, nextOffset, nextSegment: Word;
    splitOffset, splitSegment: Word;
    predecessor, index, splitIndex: Integer; traversed: Integer;
function HeapIndex(off, seg: Word): Integer;
var address: LongInt;
begin
  address := (LongInt(seg) - codeSegment) * 16 + off - $8000;
  if (address < 0) or (address > 504) or ((address and 1) <> 0) then Halt(3);
  HeapIndex := address div 2;
end;
procedure Link(off, seg: Word);
begin
  if predecessor = -1 then begin headOffset := off; headSegment := seg end
  else begin heap[predecessor] := off; heap[predecessor+1] := seg end;
end;
begin
  resultOffset := 0; resultSegment := 0; failed := 0;
  if requestSize = 0 then Exit;
  savedRequest := requestSize;
  rounded := ((LongWord(requestSize) + 7) div 8) * 8;
  predecessor := -1; nodeOffset := headOffset; nodeSegment := headSegment;
  traversed := 0;
  while nodeSegment <> frontierSegment do begin
    Inc(traversed); if traversed > 2 then Halt(4);
    index := HeapIndex(nodeOffset, nodeSegment);
    available := LongWord(heap[index+3]) * 16 + heap[index+2];
    if rounded <= available then begin
      nextOffset := heap[index]; nextSegment := heap[index+1];
      if rounded <> available then begin
        remaining := available - rounded;
        splitOffset := (LongWord(nodeOffset) + rounded mod 16) and $ffff;
        splitSegment := nodeSegment + rounded div 16;
        if (splitOffset and 255) >= 16 then Inc(splitSegment);
        splitOffset := splitOffset and $ff0f;
        splitIndex := HeapIndex(splitOffset, splitSegment);
        heap[splitIndex] := nextOffset; heap[splitIndex+1] := nextSegment;
        heap[splitIndex+2] := remaining mod 16;
        heap[splitIndex+3] := remaining div 16;
        nextOffset := splitOffset; nextSegment := splitSegment;
      end;
      Link(nextOffset, nextSegment);
      resultOffset := nodeOffset; resultSegment := nodeSegment-codeSegment;
      Exit;
    end;
    predecessor := index;
    nodeOffset := heap[index]; nodeSegment := heap[index+1];
  end;
  splitOffset := (LongWord(nodeOffset) + rounded mod 16) and $ffff;
  splitSegment := nodeSegment + rounded div 16;
  if (splitOffset and 255) >= 16 then Inc(splitSegment);
  splitOffset := splitOffset and $ff0f;
  if (splitSegment > codeSegment+$a00) or
    ((splitSegment = codeSegment+$a00) and (splitOffset > 0)) then begin
    resultSegment := splitSegment-codeSegment; failed := 1; Exit;
  end;
  frontierOffset := splitOffset; frontierSegment := splitSegment;
  Link(splitOffset, splitSegment);
  resultOffset := nodeOffset; resultSegment := nodeSegment-codeSegment;
end;
"""


def candidate_program(cases: list[tuple], segments: list[int]) -> str:
    """Oracle: same declared initial owned memory, absolute segment words and relative result."""
    calls = "\n".join(
        f"  Run({','.join(str(v) for v in (*case, segment))});"
        for case, segment in zip(cases, segments, strict=True)
    )
    return (
        """program AllocatorListProjection;
{$I candidate.inc}
var f: file; n: LongInt;
procedure Run(requestSize, firstSize, secondSize, off, seg: Word);
var heap: THeap; row: array[0..7] of Word; failed: Word;
    ro, rs, fo, fs, ho, hs, saved: Word; i: Integer;
begin
  for i := 0 to 255 do heap[i] := $a5a5;
  i := off div 2;
  heap[i] := 0; heap[i+1] := seg+$900;
  if secondSize <> 0 then begin
    heap[i] := off; heap[i+1] := seg+$810;
    heap[i+128] := 0; heap[i+129] := seg+$900;
    heap[i+130] := secondSize mod 16; heap[i+131] := secondSize div 16;
  end;
  heap[i+2] := firstSize mod 16; heap[i+3] := firstSize div 16;
  fo := 0; fs := seg+$900; ho := off; hs := seg+$800; saved := $a5a5;
  FUN_24dd_0353(requestSize,seg,ro,rs,fo,fs,ho,hs,saved,failed,heap);
  row[0] := ro; row[1] := rs; row[2] := failed;
  row[3] := fo; row[4] := fs-seg; row[5] := ho; row[6] := hs-seg; row[7] := saved;
  BlockWrite(f,row,SizeOf(row),n); if n <> SizeOf(row) then Halt(2);
  BlockWrite(f,heap,SizeOf(heap),n); if n <> SizeOf(heap) then Halt(2);
end;
begin
  Assign(f,'PASCAL.BIN'); Rewrite(f,1);
"""
        + calls
        + """
  Close(f);
end.
"""
    )


def candidate(output: pathlib.Path, cases: list[tuple], segments: list[int]) -> bytes:
    """Oracle: compile and execute exact deterministic Pascal under range checks."""
    output.mkdir()
    (output / "candidate.inc").write_text(candidate_source())
    (output / "probe.pas").write_text(candidate_program(cases, segments))
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
    if len(data) != len(cases) * PROJECTION_BYTES:
        raise ValueError("allocator list Pascal trace shape differs")
    return data


def freeze_method(root: pathlib.Path, facts: dict) -> dict:
    """Oracle: frozen source/probe/corpora; original bytes derived from current MZ evidence."""
    paths = (
        "tools/liero_allocator_list_probe.py",
        "tools/liero_four_routine_pilot.py",
        "tools/liero_file_probe.py",
        "engine/instruction_facts.py",
        "engine/routine_contract.py",
        "engine/alternate_streams.py",
        "targets/liero/config/routine_contracts.json",
        "targets/liero/alternate_streams.json",
    )
    return {
        "strategy": "deductive-owned-two-node-allocator-v1",
        "contract": facts,
        "source_sha256": hashlib.sha256(candidate_source().encode()).hexdigest(),
        "method_hashes": {name: pilot.digest(root / name) for name in paths},
        "training": [list(case) for case in list_cases("training")],
        "heldout": [list(case) for case in list_cases("heldout")],
        "budget": {"candidates": 1, "model_requests": 0, "terminal_evaluations": 1},
        "scope": "Developer-derived two-node bounded memory model; not unseen-routine recovery.",
    }


def compare(original_data: bytes, candidate_data: bytes, count: int) -> dict:
    """Oracle: complete528-byte case projections; all256 heap words compared, not guard-only."""
    if len(original_data) != count * PROJECTION_BYTES or len(candidate_data) != len(
        original_data
    ):
        raise ValueError("allocator list comparison trace shape differs")
    mismatches = [
        index
        for index in range(count)
        if original_data[index * PROJECTION_BYTES : (index + 1) * PROJECTION_BYTES]
        != candidate_data[index * PROJECTION_BYTES : (index + 1) * PROJECTION_BYTES]
    ]
    return {
        "cases": count,
        "passed": count - len(mismatches),
        "mismatch_indices": mismatches,
    }


def run(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: one frozen deductive candidate, training gates a single terminal suite."""
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "Liero BYOD unavailable"}
    _, _, facts = list_contract(root)
    freeze = freeze_method(root, facts)
    output.mkdir(parents=True, exist_ok=False)
    pilot.save(output / "freeze.json", freeze)
    (output / "candidate.inc").write_text(candidate_source())
    (output / "methods").mkdir()
    for name in freeze["method_hashes"]:
        shutil.copy2(root / name, output / "methods" / pathlib.Path(name).name)
    result = {
        "status": "failed",
        "function": "FUN_24dd_0353",
        "oracle": facts["oracle"],
        "model_requests": 0,
        "heldout_evaluations": 0,
        "routine_recovered": False,
        "source_promoted": False,
        "automatic_discovery": False,
        "unresolved": facts["unresolved"],
    }

    def validate_frozen() -> None:
        """Oracle: reject changes before or after a suite, including terminal validation."""
        _, _, current = list_contract(root)
        if (
            freeze_method(root, current) != freeze
            or json.loads((output / "freeze.json").read_text()) != freeze
            or (output / "candidate.inc").read_text() != candidate_source()
        ):
            raise ValueError("allocator list freeze/premises changed")

    try:
        for suite in ("training", "heldout"):
            validate_frozen()
            cases = list_cases(suite)
            if suite == "heldout":
                result["heldout_evaluations"] = 1
            trace = original(root, output / f"original-{suite}", cases)
            expected, segments = original_projection(trace, cases)
            observed = candidate(output / f"candidate-{suite}", cases, segments)
            result[suite] = compare(expected, observed, len(cases))
            validate_frozen()
            if result[suite]["mismatch_indices"]:
                result["stop_reason"] = f"{suite}-failure-no-retry"
                break
        else:
            result.update(status="passed", stop_reason="bounded-list-scope-validated")
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
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
    """Oracle: exact source/harness/case/artifact replay under current original-byte contracts."""
    _, contract, facts = list_contract(root)
    freeze = freeze_method(root, facts)
    report = json.loads((output / "result.json").read_text())
    if (
        json.loads((output / "freeze.json").read_text()) != freeze
        or report["freeze_sha256"] != pilot.digest(output / "freeze.json")
        or (output / "candidate.inc").read_text() != candidate_source()
        or report["status"] != "passed"
        or report["function"] != "FUN_24dd_0353"
        or report["oracle"] != facts["oracle"]
        or report["model_requests"] != 0
        or report["heldout_evaluations"] != 1
        or report["unresolved"] != facts["unresolved"]
        or any(
            report[field] is not False
            for field in ("routine_recovered", "source_promoted", "automatic_discovery")
        )
    ):
        raise ValueError("allocator list report/source/premises invalid")
    required = {"freeze.json", "candidate.inc"}
    for name, identity in freeze["method_hashes"].items():
        artifact = f"methods/{pathlib.Path(name).name}"
        required.add(artifact)
        if pilot.digest(output / artifact) != identity:
            raise ValueError("allocator list saved method differs")
    for suite in ("training", "heldout"):
        cases = list_cases(suite)
        traces = []
        for begin in range(0, len(cases), 16):
            batch = cases[begin : begin + 16]
            prefix = f"original-{suite}/part-{begin // 16}"
            directory = output / prefix
            required.update(
                f"{prefix}/{name}"
                for name in (
                    "CASES.BIN",
                    "harness.S",
                    "harness.bin",
                    "PROBE.COM",
                    "TRACE.BIN",
                )
            )
            if (directory / "CASES.BIN").read_bytes() != b"".join(
                struct.pack("<4H", *case) for case in batch
            ) or (directory / "harness.S").read_text() != list_harness(
                (directory / "CASES.BIN").resolve(), len(batch)
            ):
                raise ValueError("allocator list saved cases/harness differ")
            image = bytearray((directory / "harness.bin").read_bytes())
            if len(image) + 0x100 >= 0x6000:
                raise ValueError("allocator saved harness overlaps globals")
            for address, raw in (
                (0x353, bytes.fromhex(contract["reviewed_bytes_hex"])),
                (0x4DC, bytes.fromhex(facts["helper_bytes_hex"])),
            ):
                offset = address - 0x100
                if any(image[offset : offset + len(raw)]):
                    raise ValueError("allocator saved code overlaps harness")
                image[offset : offset + len(raw)] = raw
            if bytes(image) != (directory / "PROBE.COM").read_bytes():
                raise ValueError("allocator saved COM image differs")
            trace = (directory / "TRACE.BIN").read_bytes()
            original_projection(trace, batch)
            traces.append(trace)
        expected, segments = original_projection(b"".join(traces), cases)
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
        ).read_text() != candidate_program(cases, segments):
            raise ValueError("allocator list saved Pascal source differs")
        measured = compare(
            expected, (directory / "PASCAL.BIN").read_bytes(), len(cases)
        )
        if measured != report[suite] or measured["passed"] != len(cases):
            raise ValueError("allocator list saved comparisons differ or failed")
    if not required <= report["artifact_hashes"].keys():
        raise ValueError("allocator list required artifact identities missing")
    for name, identity in report["artifact_hashes"].items():
        path = (output / name).resolve()
        if not path.is_relative_to(output.resolve()) or pilot.digest(path) != identity:
            raise ValueError("allocator list artifact changed")
    return report


def main() -> int:
    """Oracle: CLI distinguishes verified scoped results, failure and missing-input skip."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    result = (
        validate_report(ROOT, args.output) if args.replay else run(ROOT, args.output)
    )
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"passed", "skipped"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
