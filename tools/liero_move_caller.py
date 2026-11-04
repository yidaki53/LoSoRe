"""Original three-byte caller slice and scoped typed Pascal composition."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import shutil
import struct
import subprocess

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.evidence_archive import read_archive, seal_archive
from tools import liero_source_trial as trial

ROOT = trial.ROOT
METHODS = (
    "tools/liero_move_caller.py",
    "tools/liero_source_trial.py",
    "tools/liero_four_routine_pilot.py",
    "engine/evidence_archive.py",
    "targets/liero/src/LieroRuntime.pas",
)
CALLER = bytes.fromhex(
    "8a460430e48bf88bf7d1e701f781c7d8661e578a460430e48bf88a85680030e48bf88bf7d1e701f781c726581e576a039ae148dd14"
)
BASE = 0x5800
PROLOGUE = bytes.fromhex("5589e5b806009a3005dd1483ec06")
STACK_CHECK = bytes.fromhex("050002720d2bc47309f7d83b060e647201cbb8ca00e9c7fb")
PACKED_CALLER = bytes.fromhex(
    "8d7eb016576a019ad640dd148d7ed016576a209a4141dd14c746fc0100"
)


def packed_caller_contract(root: pathlib.Path) -> dict:
    """Oracle: exact caller/initializer/copier bytes and both actual MZ relocations."""
    target = root / "targets/liero"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    start = header + 0x92D5
    locations = {
        p - start
        for p in _mz_relocation_locations(binary, header)
        if start <= p < start + len(PACKED_CALLER)
    }
    if (
        base != 0x1000
        or binary[start : start + len(PACKED_CALLER)] != PACKED_CALLER
        or locations != {10, 22}
    ):
        raise ValueError("packed caller original bytes/relocations differ")
    for routine in ("FUN_24dd_40d6", "FUN_24dd_4141"):
        spec = trial.routine_spec(routine)
        at = header + 0x14DD * 16 + spec["offset"]
        raw = bytes.fromhex(spec["bytes"])
        if binary[at : at + len(raw)] != raw:
            raise ValueError("packed caller callee bytes differ")
    return {
        "binary_sha256": identity,
        "caller": "FUN_1000_929a",
        "slice": "1000:92d5..92f2",
        "caller_bytes": PACKED_CALLER.hex(),
        "relocation_offsets": sorted(locations),
        "initializer": trial.routine_spec("FUN_24dd_40d6"),
        "copier": trial.routine_spec("FUN_24dd_4141"),
        "source": "SS:[BP-0x50]",
        "destination": "SS:[BP-0x30]",
        "packed": 32,
        "stack": "40d6 RETF2 consumes the word but retains pushed SS:offset (4bytes);4141 RETF10 consumes packed word, destination and retained source.",
        "source_parameter": "Two16-bit far-pointer words; Longint and far Pointer have the same stack width. Native type identity remains unknown.",
        "premises": "BP points to owned writable SS frame, both32-byte ranges nonaliasing with code/stack, DS=SS in host projection.",
        "obligations": [
            "Preceding caller/prologue and remainder",
            "Normal-program reachability",
            "Native TP7 types and ABI",
            "Different DS/SS, aliasing and wrapping",
        ],
        "source_recovery": False,
    }


def packed_cases(suite: str) -> list[bytes]:
    """Oracle: frozen twelve disjoint original caller frames, not random population recall."""
    if suite not in {"training", "terminal"}:
        raise ValueError("unknown packed caller suite")
    rng = random.Random(20261105 if suite == "training" else 20261106)
    return [
        struct.pack("<4H", 0x8400 + i * 16, 0, 0, (i % 2) * 0x441)
        + rng.randbytes(trial.ARENA)
        for i in range(12)
    ]


def packed_expected(data: bytes, segment: int, *, native: bool) -> bytes:
    """Oracle: original initializer, retained stack pointer, copier and local assignment."""
    bp, reserved1, reserved2, entry_flags = struct.unpack_from("<4H", data)
    if (
        len(data) != trial.CASE_BYTES
        or bp not in range(0x8400, 0x84C0, 16)
        or reserved1
        or reserved2
        or entry_flags not in (0, 0x441)
    ):
        raise ValueError("packed caller input outside owned frame")
    memory = bytearray(data[8:])
    source, destination = bp - 0x50, bp - 0x30
    memory[source - 0x8000 : source - 0x8000 + 32] = b"\x01" + b"\0" * 31
    memory[destination - 0x8000 : destination - 0x8000 + 32] = memory[
        source - 0x8000 : source - 0x8000 + 32
    ]
    struct.pack_into("<H", memory, bp - 4 - 0x8000, 1)
    flags = 0x80 | (4 if (source & 255).bit_count() % 2 == 0 else 0)
    return (
        struct.pack(
            "<16H",
            0,
            32,
            0,
            segment,
            source + 32,
            destination + 32,
            bp,
            0xEFEC,
            0xEFF0,
            segment,
            segment,
            segment,
            flags if native else 0,
            0x1357,
            0x2468,
            segment,
        )
        + memory
    )


def packed_compare(inputs: list[bytes], trace: bytes, *, native: bool) -> dict:
    """Oracle: complete caller memory/register/stack records; native and host flags distinct."""
    if len(trace) != len(inputs) * trial.RECORD_BYTES:
        raise ValueError("partial packed caller trace")
    failures = []
    for index, data in enumerate(inputs):
        row = bytearray(
            trace[index * trial.RECORD_BYTES : (index + 1) * trial.RECORD_BYTES]
        )
        segment = struct.unpack_from("<H", row, 30)[0] if native else 0x2000
        if not 0x100 <= segment <= 0x9000:
            raise ValueError("packed caller fixture segment invalid")
        struct.pack_into(
            "<H",
            row,
            24,
            struct.unpack_from("<H", row, 24)[0] & (0xCC5 if native else 0x441),
        )
        want = packed_expected(data, segment, native=native)
        if row != want:
            failures.append(
                {
                    "case": index,
                    "bytes": [
                        j
                        for j, (a, b) in enumerate(zip(row, want, strict=True))
                        if a != b
                    ][:12],
                }
            )
    return {
        "status": "failed" if failures else "passed",
        "cases": len(inputs),
        "matches": len(inputs) - len(failures),
        "failures": failures,
    }


def packed_harness() -> str:
    """Oracle: original caller and two callees in DOS allocation, original MZ segment relocations."""
    text = trial.harness("FUN_24dd_4141")
    setup = """
    mov $0x1000, %bx
    mov $0x4a00, %ax
    int $0x21
    jc failed
    mov $0x1a00, %bx
    mov $0x4800, %ax
    int $0x21
    jc failed
    mov %ax, caller_pointer+2
    mov %ax, %es
    mov $caller_bytes, %si
    mov $0x92d5, %di
    mov $30, %cx
    rep movsb
    add $0x14dd, %ax
    mov %ax, %es:0x92df
    mov %ax, %es:0x92eb
    mov %ax, %es
    mov $initializer_bytes, %si
    mov $0x40d6, %di
    mov $21, %cx
    rep movsb
    mov $original, %si
    mov $0x4141, %di
    mov $32, %cx
    rep movsb
    push %cs
    pop %es
"""
    text = text.replace(
        "    mov $input_name, %dx", setup + "    mov $input_name, %dx", 1
    )
    start = text.index("    push %cs\n    pushw input+2")
    end = text.index("    mov %sp, %ax", start)
    text = text[:start] + text[end:]
    text = text.replace("sub $4, %ax", "sub $4, %ax").replace(
        "mov $0x6789, %bp", "mov input, %bp"
    )
    text = text.replace("    push %cs\n    call original", "    lcall *caller_pointer")
    return text.replace(
        "input_name:",
        "caller_pointer: .word 0x92d5,0\ncaller_bytes: .byte "
        + ",".join(hex(b) for b in PACKED_CALLER)
        + ",0xcb\ninitializer_bytes: .byte "
        + ",".join(
            hex(b) for b in bytes.fromhex(trial.routine_spec("FUN_24dd_40d6")["bytes"])
        )
        + "\ninput_name:",
        1,
    )


def packed_program() -> str:
    """Oracle: human caller/initializer wrapper using exact selected packed Pascal, no model credit."""
    text = trial.program("FUN_24dd_4141")
    start = text.index("    FUN_24dd_4141(")
    end = text.index("\n    row[0]", start)
    body = """
    FillChar(arena[input[0] - $8050], 32, 0);
    arena[input[0] - $8050] := 1;
    RegisterAX := 0; RegisterSI := input[0] - $50;
    RegisterDI := input[0] - $30; RegisterBP := input[0];
    RegisterSP := $efde;
    FUN_24dd_4141(32, @arena[input[0] - $8030], @arena[input[0] - $8050]);
    RegisterSP := (RegisterSP + 4) and 65535;
    arena[input[0] - $8004] := 1; arena[input[0] - $8003] := 0;"""
    text = text[:start] + body + text[end:]
    return text.replace("entry := $eff0 - 10 - 4", "entry := $efec")


def run_packed(
    root: pathlib.Path, output: pathlib.Path, predecessor: pathlib.Path
) -> dict:
    """Oracle: byte-bound caller composition with selected scoped source; training then terminal once."""
    contract = packed_caller_contract(root)
    prior = trial.validate_artifacts(root, predecessor, historical=True)
    record = prior["routines"]["FUN_24dd_4141"]
    if record["selected"] is None or record["terminal"]["status"] != "passed":
        raise ValueError("packed caller requires passing frozen predecessor")
    source = (
        predecessor
        / "FUN_24dd_4141"
        / f"attempt-{record['selected']}"
        / "candidate.inc"
    )
    output.mkdir()
    (output / "methods").mkdir()
    for name in METHODS:
        shutil.copy2(root / name, output / "methods" / pathlib.Path(name).name)
    candidate = output / "candidate"
    build = trial.compile_candidate(
        root, candidate, "FUN_24dd_4141", source.read_text()
    )
    if build["status"] != "passed":
        raise ValueError("packed predecessor compile failed")
    (candidate / "probe.pas").write_text(packed_program())
    compilation = subprocess.run(
        ["fpc", "-Mtp", "-Cr", f"-Fu{root / 'targets/liero/src'}", "-FU.", "probe.pas"],
        cwd=candidate,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (candidate / "compile.log").write_bytes(compilation.stdout + compilation.stderr)
    if compilation.returncode:
        raise ValueError("packed caller compilation failed")
    trial.pilot.save(
        output / "freeze.json",
        {
            "contract": contract,
            "method_hashes": {
                name: trial.pilot.digest(root / name) for name in METHODS
            },
            "candidate_sha256": trial.pilot.digest(source),
            "predecessor": str(predecessor),
            "predecessor_artifacts_sha256": trial.pilot.digest(
                predecessor / "artifacts.json"
            ),
            "harness_sha256": hashlib.sha256(packed_harness().encode()).hexdigest(),
            "host_sha256": hashlib.sha256(packed_program().encode()).hexdigest(),
            "corpora": {
                s: hashlib.sha256(b"".join(packed_cases(s))).hexdigest()
                for s in ("training", "terminal")
            },
        },
    )
    result = {
        "model_requests": 0,
        "whole_routine_accepted": False,
        "scope": contract["premises"],
    }
    for suite in ("training", "terminal"):
        inputs = packed_cases(suite)
        original = output / f"original-{suite}"
        original.mkdir()
        (original / "harness.S").write_text(packed_harness())
        image = trial.assemble_probe(original / "harness.S", original)
        if len(image) + 0x100 >= 0x6000 or image.count(PACKED_CALLER) != 1:
            raise ValueError(
                "packed caller image overlaps arena or lacks original bytes"
            )
        (original / "PROBE.COM").write_bytes(image)
        (original / "CASES.BIN").write_bytes(b"".join(inputs))
        trial.run_dosbox(original)
        native = packed_compare(
            inputs, (original / "TRACE.BIN").read_bytes(), native=True
        )
        trial.pilot.save(original / "result.json", native)
        if native["status"] != "passed":
            raise ValueError("original packed caller contradicts derived contract")
        host = output / f"host-{suite}"
        host.mkdir()
        shutil.copy2(candidate / "probe", host / "probe")
        (host / "CASES.BIN").write_bytes(b"".join(inputs))
        execution = subprocess.run(
            [str(host / "probe")],
            cwd=host,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (host / "runtime.log").write_bytes(execution.stdout + execution.stderr)
        if execution.returncode:
            raise ValueError("packed caller host execution failed")
        result[suite] = packed_compare(
            inputs, (host / "PASCAL.BIN").read_bytes(), native=False
        )
        if result[suite]["status"] != "passed":
            break
    trial.pilot.save(output / "result.json", result)
    frozen = json.loads((output / "freeze.json").read_text())
    if any(
        trial.pilot.digest(root / name) != digest
        for name, digest in frozen["method_hashes"].items()
    ):
        raise ValueError("packed caller methods changed during evaluation")
    seal_archive(output)
    return result


def replay_packed(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: all immutable caller artifacts and both original/host corpora, no execution."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    for name, digest in frozen.get("method_hashes", {}).items():
        if (
            hashlib.sha256(archive["methods/" + pathlib.Path(name).name]).hexdigest()
            != digest
        ):
            raise ValueError("packed caller method snapshot changed")
    if (
        frozen["contract"] != packed_caller_contract(root)
        or hashlib.sha256(archive["candidate/candidate.inc"]).hexdigest()
        != frozen["candidate_sha256"]
    ):
        raise ValueError("packed caller source/byte contract changed")
    predecessor = pathlib.Path(frozen["predecessor"])
    if (
        trial.pilot.digest(predecessor / "artifacts.json")
        != frozen["predecessor_artifacts_sha256"]
    ):
        raise ValueError("packed predecessor changed")
    trial.validate_artifacts(root, predecessor, historical=True)
    result = json.loads(archive["result.json"])
    for suite in ("training", "terminal"):
        if suite not in result:
            if suite == "terminal" and result["training"]["status"] != "passed":
                continue
            raise ValueError("packed caller suite missing")
        inputs = packed_cases(suite)
        payload = b"".join(inputs)
        if hashlib.sha256(payload).hexdigest() != frozen["corpora"][suite]:
            raise ValueError("packed caller frozen corpus differs")
        for prefix, native in (("original", True), ("host", False)):
            directory = f"{prefix}-{suite}"
            if archive[f"{directory}/CASES.BIN"] != payload:
                raise ValueError("packed caller inputs changed")
            checked = packed_compare(
                inputs,
                archive[f"{directory}/" + ("TRACE.BIN" if native else "PASCAL.BIN")],
                native=native,
            )
            if checked["status"] != "passed" if native else checked != result[suite]:
                raise ValueError("packed caller trace replay differs")
    return result


def stack_check_contract(raw: bytes, request: int, sp: int, minimum: int) -> dict:
    """Oracle: exact unsigned ADD/SUB/NEG/CMP branches; failure dispatch not resolved."""
    if raw != STACK_CHECK or any(
        type(v) is not int or not 0 <= v <= 65535 for v in (request, sp, minimum)
    ):
        raise ValueError("unsupported stack-check bytes or word inputs")
    total = request + 512
    available = sp - total
    reason = (
        "add-carry"
        if total > 65535
        else "sub-no-borrow"
        if total >= sp
        else "below-minimum"
        if available < minimum
        else None
    )
    return {
        "status": "error-dispatch" if reason else "returns",
        "reason": reason,
        "available": available if reason is None else None,
        "failure_target": "24dd:010f",
        "failure_ax": 202,
        "scope": "Arithmetic/control flow contract; error callee/reachability unresolved.",
    }


def caller_contract(root: pathlib.Path, *, prologue: bool = False) -> dict:
    """Oracle: actual original bytes and MZ relocation, not exported disassembly."""
    target = root / "targets/liero"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    offset = header + 0x5F9
    if base != 0x1000 or binary[offset : offset + len(CALLER)] != CALLER:
        raise ValueError("unsupported original move caller bytes")
    relocations = {
        p - offset
        for p in _mz_relocation_locations(binary, header)
        if offset - 1 <= p < offset + len(CALLER)
    }
    callee_offset = header + 0x14DD * 16 + 0x48E1
    if (
        relocations != {51}
        or binary[callee_offset : callee_offset + 36] != trial.INTERPRETATION_BYTES
    ):
        raise ValueError("move caller relocation or callee bytes disagree")
    report = {
        "binary_sha256": identity,
        "caller": "FUN_1000_05eb",
        "slice": "1000:05f9..062e",
        "call": "1000:0629",
        "caller_bytes": CALLER.hex(),
        "relocation_offsets": [51],
        "source": "DS:(0x66d8 + 3*unsigned byte SS:[BP+4])",
        "destination": "DS:(0x5826 + 3*unsigned byte DS:[0x68+argument])",
        "count": 3,
        "call_target": "load+14dd:48e1",
        "premises": "Owned DS arena, readable lookup cell, independent writable SS stack/frame; argument and lookup0..15 in execution corpus.",
        "unknown": [
            "Preceding stack-check call/prologue contract",
            "Normal-program reachability",
            "Other callers, separate segments, wrap and stack/global aliasing",
            "Native TP7 ABI",
        ],
        "source_recovery": False,
    }
    if prologue:
        start = header + 0x5EB
        stack = header + 0x14DD * 16 + 0x530
        locations = {
            p - start
            for p in _mz_relocation_locations(binary, header)
            if start - 1 <= p < start + len(PROLOGUE)
        }
        if (
            binary[start : start + len(PROLOGUE)] != PROLOGUE
            or locations != {9}
            or binary[stack : stack + 24] != STACK_CHECK
            or binary[header + 0x95D : header + 0x961] != bytes.fromhex("c9c20200")
        ):
            raise ValueError("original prologue/stack-check bytes or relocation differ")
        report.update(
            slice="1000:05eb..062e",
            prologue_bytes=PROLOGUE.hex(),
            stack_check_bytes=STACK_CHECK.hex(),
            stack_check=stack_check_contract(STACK_CHECK, 6, 0xEFE6, 0xE6),
            stack_check_entry_sp=0xEFE6,
            copy_entry_sp=0xEFD6,
            calling_convention="Near caller: saved BP and near return precede BP+4 argument; external far bridge removes its frame.",
            minimum_cell="proven entry DS:[640e], readable owned cell",
            remaining="Failure dispatch24dd:010f, normal-program entry premises and remainder after062e unresolved.",
        )
    return report


def cases(suite: str, *, prologue: bool = False) -> list[bytes]:
    """Oracle: frozen disjoint owned-state seeds; same scoped caller boundary."""
    if suite not in {"training", "terminal"}:
        raise ValueError("unknown caller suite")
    rng = random.Random(
        (20261105 if suite == "training" else 20261106) + (10 if prologue else 0)
    )
    rows = [
        struct.pack("<4H", argument, lookup, 0, flags)
        + bytes(rng.randrange(256) for _ in range(trial.ARENA))
        for argument, lookup in ((0, 0), (1, 15), (15, 1), (15, 15), (7, 3), (3, 7))
        for flags in (0, 0x441)
    ]
    if prologue:
        prepared = []
        for index, row in enumerate(rows):
            memory = bytearray(row)
            struct.pack_into(
                "<H", memory, 8 + 0x640E - BASE, (0, 0xE6, 0xEDE0)[index % 3]
            )
            prepared.append(bytes(memory))
        return prepared
    return rows


def expected(
    data: bytes, segment: int, *, native: bool, prologue: bool = False
) -> bytes:
    """Oracle: derived caller arithmetic and unchanged callee effects in owned bounds."""
    if len(data) != trial.CASE_BYTES or not 0x100 <= segment <= 0x9000:
        raise ValueError("invalid owned caller record or segment")
    argument, lookup, reserved, entry_flags = struct.unpack_from("<4H", data)
    if argument > 15 or lookup > 15 or reserved or entry_flags not in (0, 0x441):
        raise ValueError("caller input outside frozen owned scope")
    if (
        prologue
        and stack_check_contract(
            STACK_CHECK, 6, 0xEFE6, struct.unpack_from("<H", data, 8 + 0x640E - BASE)[0]
        )["status"]
        != "returns"
    ):
        raise ValueError("prologue corpus reaches unresolved error dispatch")
    source, destination = 0x66D8 + 3 * argument, 0x5826 + 3 * lookup
    memory = bytearray(data[8:])
    for i in range(3):
        memory[destination - BASE + i] = memory[source - BASE + i]
    value = source - destination
    flags = int((value & 255).bit_count() % 2 == 0) * 4 | (value & 0x8000) >> 8
    row = (
        lookup,
        0xEFD6 if prologue else 0xEFDE,
        0,
        segment,
        source + 3,
        destination + 3,
        0x6789 if prologue else 0xEFF4,
        0xEFD6 if prologue else 0xEFDE,
        0xEFF0,
        segment,
        segment,
        segment,
        flags if native else 0,
        0x1357,
        0x2468,
        segment,
    )
    return struct.pack("<16H", *row) + memory


def compare(
    inputs: list[bytes], trace: bytes, *, native: bool, prologue: bool = False
) -> dict:
    """Oracle: complete arena and declared state, host CF/ZF/DF distinct from native flags."""
    if len(trace) != len(inputs) * trial.RECORD_BYTES:
        raise ValueError("partial caller trace")
    failures = []
    for i, data in enumerate(inputs):
        row = bytearray(trace[i * trial.RECORD_BYTES : (i + 1) * trial.RECORD_BYTES])
        segment = struct.unpack_from("<H", row, 30)[0] if native else 0x2000
        struct.pack_into(
            "<H",
            row,
            24,
            struct.unpack_from("<H", row, 24)[0] & (0xCC5 if native else 0x441),
        )
        want = expected(data, segment, native=native, prologue=prologue)
        if row != want:
            failures.append(
                {
                    "case": i,
                    "bytes": [j for j, (a, b) in enumerate(zip(row, want)) if a != b][
                        :12
                    ],
                }
            )
    return {
        "status": "failed" if failures else "passed",
        "cases": len(inputs),
        "matches": len(inputs) - len(failures),
        "failures": failures,
        "required_case_recall": (len(inputs) - len(failures)) / len(inputs),
        "probability_correct": None,
        "sensitivity": None,
    }


def harness(*, prologue: bool = False) -> str:
    """Oracle: original caller/callee bytes with actual MZ relocation in owned DOS allocation."""
    text = trial.harness("FUN_24dd_48e1")
    setup = """
    mov $0x1000, %bx
    mov $0x4a00, %ax
    int $0x21
    jc failed
    mov $0x1a00, %bx
    mov $0x4800, %ax
    int $0x21
    jc failed
    mov %ax, caller_pointer+2
    mov %ax, %es
    mov $caller_bytes, %si
    mov $0x5f9, %di
    mov $54, %cx
    rep movsb
    add $0x14dd, %ax
    mov %ax, %es:0x62c
    mov %ax, %es
    mov $original, %si
    mov $0x48e1, %di
    mov $36, %cx
    rep movsb
    push %cs
    pop %es
"""
    text = text.replace(
        "    mov $input_name, %dx", setup + "    mov $input_name, %dx", 1
    )
    text = text.replace("$0x8000", "$0x5800")
    start = text.index("    push %cs\n    pushw input+2")
    end = text.index("    mov %sp, %ax", start)
    text = (
        text[:start]
        + """
    mov input, %ax
    mov %ax, %ss:0xeff8
    mov %ax, %bx
    mov input+2, %al
    mov %al, 0x68(%bx)
"""
        + text[end:]
    )
    text = text.replace("sub $4, %ax", "sub $18, %ax")
    text = text.replace("$0x6789, %bp", "$0xeff4, %bp")
    text = text.replace("mov input+2, %si", "mov $0x1111, %si")
    text = text.replace("mov input+4, %di", "mov $0x2222, %di")
    text = text.replace("    push %cs\n    call original", "    lcall *caller_pointer")
    text = text.replace(
        "input_name:",
        "caller_pointer: .word 0x5f9, 0\ncaller_bytes: .byte "
        + ",".join(hex(b) for b in CALLER)
        + ",0xcb\ninput_name:",
        1,
    )
    if prologue:
        raw = PROLOGUE + CALLER
        text = text.replace("mov $0x5f9, %di", "mov $0x5eb, %di")
        text = text.replace("mov $54, %cx", f"mov ${len(raw) + 6}, %cx")
        text = text.replace(
            "mov %ax, %es:0x62c", "mov %ax, %es:0x5f4\n    mov %ax, %es:0x62c"
        )
        text = text.replace(
            "    mov $36, %cx\n    rep movsb\n    push %cs\n    pop %es\n",
            """
    mov $36, %cx
    rep movsb
    mov $stack_bytes, %si
    mov $0x530, %di
    mov $24, %cx
    rep movsb
    mov caller_pointer+2, %es
    mov $bridge_bytes, %si
    mov $0x500, %di
    mov $24, %cx
    rep movsb
    push %cs
    pop %es
""",
            1,
        )
        text = text.replace("mov %ax, %ss:0xeff8", "push %ax")
        text = text.replace("sub $18, %ax", "sub $24, %ax")
        text = text.replace("mov $0xeff4, %bp", "mov $0x6789, %bp")
        old = (
            "caller_pointer: .word 0x5f9, 0\ncaller_bytes: .byte "
            + ",".join(hex(b) for b in CALLER)
            + ",0xcb"
        )
        new = (
            "caller_pointer: .word 0x500, 0\nbridge_bytes: .byte 0x2e,0x8f,0x06,0xc0,0x04,0x2e,0x8f,0x06,0xc2,0x04,0xe8,0xde,0x00,0x2e,0xff,0x36,0xc2,0x04,0x2e,0xff,0x36,0xc0,0x04,0xcb\ncaller_bytes: .byte "
            + ",".join(hex(b) for b in raw)
            + ",0x89,0xec,0x5d,0xc2,0x02,0x00\nstack_bytes: .byte "
            + ",".join(hex(b) for b in STACK_CHECK)
        )
        if old not in text:
            raise ValueError("caller harness payload template differs")
        text = text.replace(old, new)
    return text


def program(source: str, *, prologue: bool = False) -> tuple[str, str]:
    """Oracle: caller-composed wrapper loads logical arguments, not arbitrary entry mirrors."""
    composed = source.replace(
        "sourceOffset := RegisterSI; destinationOffset := RegisterDI;",
        "sourceOffset := $66d8 + 3 * inputArgument; destinationOffset := $5826 + 3 * inputLookup;",
    )
    if composed == source:
        raise ValueError("caller composition requires reviewed residual wrapper")
    program = trial.program("FUN_24dd_48e1")
    program = program.replace(
        "{$I candidate.inc}",
        "var inputArgument, inputLookup: Word;\n{$I candidate.inc}",
    )
    program = program.replace("$8000", "$5800").replace(
        "RegisterBP := $6789", "RegisterBP := $eff4"
    )
    program = program.replace("entry := $eff0 - 10 - 4", "entry := $efde")
    call = "FUN_24dd_48e1(Integer(input[0]), @arena[input[2] - $5800], @arena[input[1] - $5800]);"
    if call not in program:
        raise ValueError("caller host template call differs")
    program = program.replace(
        call,
        """inputArgument := input[0]; inputLookup := input[1];
    RegisterAX := inputLookup; RegisterSI := 2 * inputLookup;
    RegisterDI := $5826 + 3 * inputLookup;
    FUN_24dd_48e1(3, @arena[RegisterDI - $5800],
      @arena[$66d8 + 3 * inputArgument - $5800]);
    RegisterSP := (RegisterSP + 4) and $ffff;""",
    )
    if prologue:
        program = program.replace("entry := $efde", "entry := $efd6")
        program = program.replace("RegisterBP := $eff4", "RegisterBP := $6789")
        program = program.replace(
            "RegisterSP := (RegisterSP + 4) and $ffff;",
            "RegisterSP := (RegisterSP + 12) and $ffff;",
        )
        program = program.replace(
            "inputArgument := input[0]; inputLookup := input[1];",
            """if (Word(arena[$640e - $5800]) +
      Word(arena[$640f - $5800]) * 256) > $ede0 then Halt(6);
    inputArgument := input[0]; inputLookup := input[1];""",
        )
    return composed, program


def run(
    root: pathlib.Path,
    output: pathlib.Path,
    predecessor: pathlib.Path,
    *,
    prologue: bool = False,
) -> dict:
    """Oracle: frozen original caller-slice differential, one terminal, no model/training promotion."""
    contract = caller_contract(root, prologue=prologue)
    previous = trial.validate_artifacts(root, predecessor, historical=True)
    if previous["routines"]["FUN_24dd_48e1"]["interpretation"]["status"] != "passed":
        raise ValueError("caller composition requires checked interpretation")
    body = trial.lower_interpretation(
        previous["routines"]["FUN_24dd_48e1"]["interpretation"]["selected"]
    )
    source, host = program(trial.compose_residual(body), prologue=prologue)
    output.mkdir(parents=True, exist_ok=False)
    trial.pilot.save(
        output / "freeze.json",
        {
            "contract": contract,
            "method_sha256": trial.pilot.digest(pathlib.Path(__file__)),
            "predecessor_artifacts_sha256": trial.pilot.digest(
                predecessor / "artifacts.json"
            ),
            "corpora": {
                s: hashlib.sha256(b"".join(cases(s, prologue=prologue))).hexdigest()
                for s in ("training", "terminal")
            },
            "candidate_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "budget": "One mechanical candidate, no repairs, terminal once after training; zero model requests.",
            "disclosure": "Previously known callee terminal evidence is disclosed; new caller corpus is scoped composition, not unseen discovery.",
            "prologue": prologue,
            "external_frame": (
                "Harness far bridge saves return IP/CS out of SS stack, near CALLs05eb, "
                "then restores its far return. External MOV SP,BP/POP BP/RET2 after062e "
                "unwinds only the measured slice; not original caller epilogue."
                if prologue
                else "External RETF after062e returns injected slice frame."
            ),
        },
    )
    candidate = output / "candidate"
    candidate.mkdir()
    (candidate / "candidate.inc").write_text(source)
    (candidate / "probe.pas").write_text(host)
    methods = output / "methods"
    methods.mkdir()
    for path in (root / name for name in METHODS):
        shutil.copy2(path, methods / path.name)
    frozen = json.loads((output / "freeze.json").read_text())
    frozen["method_hashes"] = {
        str(p.relative_to(root)): trial.pilot.digest(p)
        for p in (root / name for name in METHODS)
    }
    frozen["host_program_sha256"] = hashlib.sha256(host.encode()).hexdigest()
    frozen["harness_sha256"] = hashlib.sha256(
        harness(prologue=prologue).encode()
    ).hexdigest()
    frozen["predecessor_path"] = str(predecessor.resolve())
    trial.pilot.save(output / "freeze.json", frozen)
    build = subprocess.run(
        ["fpc", "-Mtp", "-Cr", f"-Fu{root / 'targets/liero/src'}", "-FU.", "probe.pas"],
        cwd=candidate,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (candidate / "compile.log").write_bytes(build.stdout + build.stderr)
    if build.returncode:
        raise ValueError("caller candidate compilation failed; see compile.log")
    result = {}
    for suite in ("training", "terminal"):
        inputs = cases(suite, prologue=prologue)
        original = output / f"original-{suite}"
        original.mkdir()
        (original / "harness.S").write_text(harness(prologue=prologue))
        image = trial.assemble_probe(original / "harness.S", original)
        if len(image) + 0x100 >= BASE:
            raise ValueError("caller harness overlaps arena")
        if image.count(CALLER) != 1 or image.count(trial.INTERPRETATION_BYTES) != 1:
            raise ValueError("original caller/callee bytes missing or duplicated")
        if prologue and (
            image.count(PROLOGUE + CALLER) != 1 or image.count(STACK_CHECK) != 1
        ):
            raise ValueError(
                "original prologue/stack-check bytes missing or duplicated"
            )
        (original / "PROBE.COM").write_bytes(image)
        (original / "CASES.BIN").write_bytes(b"".join(inputs))
        trial.run_dosbox(original)
        native = compare(
            inputs,
            (original / "TRACE.BIN").read_bytes(),
            native=True,
            prologue=prologue,
        )
        if native["status"] != "passed":
            trial.pilot.save(original / "failure.json", native)
            raise ValueError("original caller contradicts derived contract")
        host_dir = output / f"host-{suite}"
        host_dir.mkdir()
        shutil.copy2(candidate / "probe", host_dir / "probe")
        (host_dir / "CASES.BIN").write_bytes(b"".join(inputs))
        execution = subprocess.run(
            [str(host_dir / "probe")],
            cwd=host_dir,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (host_dir / "runtime.log").write_bytes(execution.stdout + execution.stderr)
        if execution.returncode:
            raise ValueError("caller host execution failed")
        result[suite] = compare(
            inputs,
            (host_dir / "PASCAL.BIN").read_bytes(),
            native=False,
            prologue=prologue,
        )
        trial.pilot.save(output / "selection.json", result)
        if result[suite]["status"] != "passed":
            break
    result.update(
        model_requests=0,
        weights_changed=False,
        source_installed=False,
        scope="Original caller slice under owned DS/SS premises; not whole caller or native ABI acceptance.",
    )
    if any(
        trial.pilot.digest(root / p) != identity
        for p, identity in frozen["method_hashes"].items()
    ):
        raise ValueError("caller methods changed during evaluation")
    trial.pilot.save(output / "result.json", result)
    seal_archive(output)
    return result


def replay(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: immutable evidence and full original/host trace replay, no execution."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    prologue = frozen.get("prologue", False)
    if frozen["contract"] != caller_contract(root, prologue=prologue):
        raise ValueError("caller byte contract changed")
    if (
        hashlib.sha256(archive["candidate/candidate.inc"]).hexdigest()
        != frozen["candidate_sha256"]
    ):
        raise ValueError("caller selected source identity differs")
    if (
        "host_program_sha256" in frozen
        and hashlib.sha256(archive["candidate/probe.pas"]).hexdigest()
        != frozen["host_program_sha256"]
    ):
        raise ValueError("caller host program identity differs")
    for name, identity in frozen.get("method_hashes", {}).items():
        if (
            hashlib.sha256(archive["methods/" + pathlib.Path(name).name]).hexdigest()
            != identity
        ):
            raise ValueError("caller method snapshot changed")
    if "predecessor_path" in frozen:
        predecessor = pathlib.Path(frozen["predecessor_path"])
        if (
            trial.pilot.digest(predecessor / "artifacts.json")
            != frozen["predecessor_artifacts_sha256"]
        ):
            raise ValueError("caller predecessor changed")
        trial.validate_artifacts(root, predecessor, historical=True)
    result = json.loads(archive["result.json"])
    for suite in ("training", "terminal"):
        if suite not in result:
            if suite == "terminal" and result["training"]["status"] != "passed":
                continue
            raise ValueError("caller selected candidate has missing terminal result")
        inputs = cases(suite, prologue=prologue)
        payload = b"".join(inputs)
        if hashlib.sha256(payload).hexdigest() != frozen["corpora"][suite]:
            raise ValueError("caller frozen corpus differs")
        original = f"original-{suite}"
        host = f"host-{suite}"
        if (
            "harness_sha256" in frozen
            and hashlib.sha256(archive[f"{original}/harness.S"]).hexdigest()
            != frozen["harness_sha256"]
        ):
            raise ValueError("caller harness identity differs")
        if (
            archive[f"{original}/CASES.BIN"] != payload
            or archive[f"{host}/CASES.BIN"] != payload
        ):
            raise ValueError("caller input payload differs")
        if (
            compare(
                inputs,
                archive[f"{original}/TRACE.BIN"],
                native=True,
                prologue=prologue,
            )["status"]
            != "passed"
        ):
            raise ValueError("original caller replay failed")
        assessment = compare(
            inputs, archive[f"{host}/PASCAL.BIN"], native=False, prologue=prologue
        )
        if any(assessment[key] != value for key, value in result[suite].items()):
            raise ValueError("host caller replay differs")
    return result


def main() -> None:
    """Oracle: explicit bounded BYOD caller execution."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    parser.add_argument("--from", dest="predecessor", type=pathlib.Path)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--prologue", action="store_true")
    parser.add_argument("--packed", action="store_true")
    args = parser.parse_args()
    if args.packed and args.prologue:
        parser.error("--packed has a distinct caller; --prologue unsupported")
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        print(json.dumps({"status": "skipped", "reason": "BYOD unavailable"}))
        return
    if not args.replay and args.predecessor is None:
        parser.error("--from is required for a new caller trial")
    if args.packed:
        result = (
            replay_packed(ROOT, args.output.resolve())
            if args.replay
            else run_packed(ROOT, args.output.resolve(), args.predecessor.resolve())
        )
        print(json.dumps(result, indent=2))
        return
    result = (
        replay(ROOT, args.output.resolve())
        if args.replay
        else run(
            ROOT,
            args.output.resolve(),
            args.predecessor.resolve(),
            prologue=args.prologue,
        )
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
