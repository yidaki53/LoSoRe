"""Observe one actual64000-byte caller across original startup/028a; no full-routine acceptance."""

from __future__ import annotations

import argparse
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
from tools.liero_file_probe import run_dosbox
from tools.liero_startup_clear_contract import startup_heap_contract
from tools.liero_startup_clear_probe import APPEND_OFFSET, SERVICE_WINDOW, sha

REGISTERS = ("AX", "BX", "CX", "DX", "SI", "DI", "BP", "DS", "ES", "SS", "SP", "FLAGS")
SNAPSHOT_BYTES = len(REGISTERS) * 2 + 12 + SERVICE_WINDOW[1] - SERVICE_WINDOW[0]
TRACE_BYTES = 8 + 2 * SNAPSHOT_BYTES
MAIN_CALL = bytes.fromhex("6800fa9a8a02dd14a3846689168666")
WRAPPER = bytes.fromhex("558bec8b4606e8c0005d7203ca0200b8cb00e970fe")


def entry_contract(root: pathlib.Path) -> tuple[bytes, dict, str]:
    """Oracle: actual original call/prologue/store bytes and exclusive MZ relocation words."""
    binary, _, allocator = pilot.allocator_deduction_inputs(root)
    startup = startup_heap_contract(binary, load_segment=0x1000)
    header = startup["mz"]["header_bytes"]
    relative_cs = startup["startup"]["relocated_cs"] - startup["load_segment"]
    relocations = _mz_relocation_locations(binary, header)
    for offset, raw, expected in (
        (0xE50B, MAIN_CALL, {6}),
        (relative_cs * 16 + 0x28A, WRAPPER, set()),
        (0xE51A, bytes.fromhex("6840c99a8a02dd14"), {6}),
    ):
        start = header + offset
        if (
            binary[start : start + len(raw)] != raw
            or {r - start for r in relocations if start - 1 <= r < start + len(raw)}
            != expected
        ):
            raise ValueError("allocator actual caller/hook bytes or relocations differ")
    facts = {key: value for key, value in allocator.items() if key != "binary_sha256"}
    contract = {
        "oracle": "instrumented_actual_028a_64000_caller_vs_frozen_pascal_projection",
        "binary_sha256": allocator["binary_sha256"],
        "startup": startup,
        "allocator": allocator,
        "request": 64000,
        "return_ip": 0xE513,
        "stop_ip": 0xE51A,
        "globals": list(SERVICE_WINDOW),
        "instrumentation": [
            "MZ entry redirects to appended bootstrap; original startup and main call/store bytes stay intact.",
            "028a PUSH BP/MOV BP,SP replaced by same-CS near JMP; gateway restores flags/registers and executes displaced prologue.",
            "Only return e513 with original main CS is observed; other028a calls continue through displaced prologue unchanged.",
            "At e51a next PUSH replaced by three NOPs and next CALL becomes far JMP, reusing its unchanged MZ segment relocation.",
            "No dirty globals, supplied pointers, mocked services or callback replacement; collector terminates instrumented guest.",
            "Bootstrap scratch10, dispatch6, snapshot14 transient bytes; observed stack restricted to last4096 guaranteed bytes, payload below it.",
        ],
        "unresolved": [
            "one instrumented DOSBox context, not all environments or unmodified normal execution",
            "interrupt effects outside captured memory and all earlier initialization routines",
            "arbitrary free lists, nondefault callbacks/retry and010f failure transfer",
            "later allocation lifetime, full register/flag ABI and whole routine source acceptance",
        ],
    }
    return binary, contract, pilot.render_allocator_empty_source(facts)


def instrumentation_source(contract: dict) -> str:
    """Oracle: state-preserving original-entry gateway and endpoint capture, not Pascal ABI."""
    startup = contract["startup"]
    relative_cs = startup["startup"]["relocated_cs"] - startup["load_segment"]
    snapshots = []
    for stage in ("before", "after"):
        registers = "\n".join(
            f"    mov %{reg.lower()}, %cs:{stage}_{reg}" for reg in REGISTERS[:-1]
        )
        snapshots.append(f"""
{registers}
    pushf
    popw %cs:{stage}_FLAGS
    pushf
    push %ax
    push %cx
    push %si
    push %di
    push %es
    mov %sp, %si
    add $12, %si
    push %cs
    pop %es
    mov ${stage}_stack, %di
    mov $12, %cx
    cld
    ss rep movsb
    mov ${SERVICE_WINDOW[0]}, %si
    mov ${stage}_memory, %di
    mov ${SERVICE_WINDOW[1] - SERVICE_WINDOW[0]}, %cx
    rep movsb
    pop %es
    pop %di
    pop %si
    pop %cx
    pop %ax
    popf
""")
    records = "\n".join(
        "\n".join(f"{stage}_{reg}: .word 0" for reg in REGISTERS)
        + f"\n{stage}_stack: .space 12\n{stage}_memory: .space {SERVICE_WINDOW[1] - SERVICE_WINDOW[0]}"
        for stage in ("before", "after")
    )
    return f""".code16
.global _start, before_entry, collector
_start:
    mov %ss, %cs:initial_ss
    mov %sp, %cs:initial_sp
    mov %es, %cs:initial_es
    pushf
    push %ax
    push %cx
    push %di
    push %es
    mov %es:2, %ax
    mov %ax, %cs:psp_end
    mov %cs, %ax
    sub ${relative_cs}, %ax
    mov %ax, %cs:entry_pointer+2
    pop %es
    pop %di
    pop %cx
    pop %ax
    popf
    ljmp *%cs:entry_pointer
before_entry:
    pushf
    push %bp
    push %ax
    mov %sp, %bp
    cmpw $0xe513, %ss:6(%bp)
    jne bypass
    mov %cs:entry_pointer+2, %ax
    cmp %ss:8(%bp), %ax
    jne bypass
    pop %ax
    pop %bp
    popf
{snapshots[0]}
    jmp displaced
bypass:
    pop %ax
    pop %bp
    popf
displaced:
    push %bp
    mov %sp, %bp
    jmp 0x28d
collector:
{snapshots[1]}
    push %cs
    pop %ds
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
entry_pointer: .word {startup["mz"]["initial_ip"]}, 0
record:
initial_ss: .word 0
initial_sp: .word 0
initial_es: .word 0
psp_end: .word 0
{records}
"""


def build_image(
    binary: bytes, contract: dict, payload: bytes, labels: dict
) -> tuple[bytes, dict]:
    """Oracle: unchanged allocation/relocations and exact two-hook inventory; no original service patch."""
    startup = contract["startup"]
    header = startup["mz"]["header_bytes"]
    relative_cs = startup["startup"]["relocated_cs"] - startup["load_segment"]
    boot = APPEND_OFFSET - relative_cs * 16
    end = APPEND_OFFSET + len(payload)
    if (
        sha(binary) != contract["binary_sha256"]
        or labels["_start"] != boot
        or not boot
        < labels["before_entry"]
        < labels["collector"]
        < boot + len(payload)
        <= 65536
        or APPEND_OFFSET < startup["mz"]["image_bytes"]
        or end >= startup["mz"]["minimum_allocation_bytes"] - 4096
    ):
        raise ValueError("allocator entry payload/binary/stack bounds invalid")
    added = (end + 15) // 16 - (startup["mz"]["image_bytes"] + 15) // 16
    minimum, maximum = struct.unpack_from("<HH", binary, 10)
    if not payload or not 0 <= added <= min(minimum, maximum):
        raise ValueError("allocator entry payload cannot preserve MZ allocation")
    image = bytearray(binary)
    image.extend(bytes(header + APPEND_OFFSET - len(binary)))
    image.extend(payload)
    struct.pack_into("<HH", image, 2, len(image) % 512, (len(image) + 511) // 512)
    struct.pack_into("<HH", image, 10, minimum - added, maximum - added)
    struct.pack_into("<HH", image, 20, boot, relative_cs)
    wrapper = header + relative_cs * 16 + 0x28A
    struct.pack_into(
        "<BH", image, wrapper, 0xE9, (labels["before_entry"] - 0x28D) & 65535
    )
    stop = header + 0xE51A
    image[stop : stop + 8] = b"\x90\x90\x90\xea" + struct.pack(
        "<HH", labels["collector"], relative_cs
    )
    allowed = {
        *range(2, 6),
        *range(10, 14),
        *range(20, 24),
        *range(wrapper, wrapper + 3),
        *range(stop, stop + 6),
    }
    changed = [
        {"file_offset": i, "original": old, "instrumented": new}
        for i, (old, new) in enumerate(zip(binary, image))
        if old != new
    ]
    if any(change["file_offset"] not in allowed for change in changed):
        raise ValueError("allocator entry undisclosed original-byte patch")
    for position in _mz_relocation_locations(binary, header):
        if binary[position : position + 2] != image[position : position + 2]:
            raise ValueError("allocator entry changed an original relocation word")
    return bytes(image), {
        "changed_original_bytes": changed,
        "appended_module_range": [APPEND_OFFSET, end],
    }


def compare_trace(trace: bytes, contract: dict) -> dict:
    """Oracle: one actual entry/return/global projection, explicit capacity and disjointness gates."""
    if len(trace) != TRACE_BYTES:
        raise ValueError("allocator entry trace must contain both complete endpoints")
    initial_ss, initial_sp, psp, psp_end = struct.unpack_from("<4H", trace)
    base = psp + 16
    startup = contract["startup"]
    relative_cs = startup["startup"]["relocated_cs"] - startup["load_segment"]
    relative_ds = startup["startup"]["relocated_ds"] - startup["load_segment"]
    rows = []
    for begin in (8, 8 + SNAPSHOT_BYTES):
        registers = dict(
            zip(REGISTERS, struct.unpack_from("<12H", trace, begin), strict=True)
        )
        stack = list(struct.unpack_from("<6H", trace, begin + 24))
        memory = trace[begin + 36 : begin + SNAPSHOT_BYTES]
        rows.append((registers, stack, memory))
    before, after = rows

    def word(memory: bytes, cell: int) -> int:
        """Oracle: bounded captured DS word."""
        return struct.unpack_from("<H", memory, cell - SERVICE_WINDOW[0])[0]

    pre, post = before[2], after[2]
    start = [word(pre, 0x63EE), word(pre, 0x63F0)]
    limit = [word(pre, 0x63F2), word(pre, 0x63F4)]
    physical = start[1] * 16 + start[0]
    heap_end = physical + contract["request"]
    frontier = [start[0], start[1] + contract["request"] // 16]
    memory_end = base * 16 + startup["mz"]["minimum_allocation_bytes"]
    if (
        not 0 < base <= 0xFFFF - relative_ds
        or initial_ss != base + startup["mz"]["initial_ss"] - startup["load_segment"]
        or initial_sp != startup["mz"]["initial_sp"]
        or not 0 < psp_end <= 0xFFFF
        or limit != [0, psp_end]
        or not 0 <= start[0] < 16
        or [word(pre, 0x63F6), word(pre, 0x63F8)] != start
        or [word(pre, 0x63FE), word(pre, 0x6400)] != [0xD6, base + relative_cs]
        or not memory_end <= physical < heap_end <= psp_end * 16 <= 0x100000
    ):
        raise ValueError(
            "allocator actual entry empty-list/callback/capacity premises fail"
        )
    for registers, _, _ in rows:
        low = registers["SS"] * 16 + registers["SP"] - 14
        high = registers["SS"] * 16 + registers["SP"] + 12
        if (
            registers["DS"] != base + relative_ds
            or registers["SS"] != initial_ss
            or not 14 <= registers["SP"] <= initial_sp
            or not memory_end - 4096 <= low < high <= memory_end
        ):
            raise ValueError("allocator entry observed DS/stack bounds fail")
    if (
        before[1][:3] != [contract["return_ip"], base, contract["request"]]
        or after[0]["SP"] != before[0]["SP"] + 6
        or after[0]["BP"] != before[0]["BP"]
        or after[0]["FLAGS"] & 1
        or [after[0]["AX"], after[0]["DX"]] != start
        or [word(post, 0x6684), word(post, 0x6686)] != start
    ):
        raise ValueError("allocator original far-call/return/result contract differs")
    expected = bytearray(pre)
    for cell, value in (
        (0x63EE, frontier[0]),
        (0x63F0, frontier[1]),
        (0x63F6, frontier[0]),
        (0x63F8, frontier[1]),
        (0x6684, start[0]),
        (0x6686, start[1]),
        (0x7B3C, contract["request"]),
    ):
        struct.pack_into("<H", expected, cell - SERVICE_WINDOW[0], value)
    if bytes(expected) != post:
        raise ValueError(
            "allocator original global projection/unchanged residue differs"
        )
    return {
        "load_segment": base,
        "before_registers": before[0],
        "after_registers": after[0],
        "entry_stack": before[1],
        "result_pointer": start,
        "next_frontier": frontier,
        "limit": limit,
        "allocation_physical": [physical, heap_end],
        "callback": [0xD6, base + relative_cs],
        "protected_global_bytes": len(pre),
        "pascal_case": [contract["request"], *start, *limit],
        "expected_pascal_row": [*start, 0, *frontier, *frontier, contract["request"]],
    }


def freeze_method(root: pathlib.Path, contract: dict, source: str) -> dict:
    """Oracle: pre-execution observation budget, deterministic source and immutable method identities."""
    paths = (
        "tools/liero_allocator_entry_probe.py",
        "tools/liero_startup_clear_contract.py",
        "tools/liero_startup_clear_probe.py",
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
        "source_sha256": sha(source.encode()),
        "method_hashes": {name: pilot.digest(root / name) for name in paths},
        "budget": {
            "original_executions": 1,
            "candidate_executions": 1,
            "model_requests": 0,
            "repairs": 0,
            "heldout_evaluations": 0,
        },
        "scope": "one instrumented real caller; input observed, method/source fixed before execution; not unseen recovery",
    }


def assemble(output: pathlib.Path, contract: dict) -> dict:
    """Oracle: existing GNU tools, startup-CS-linked payload and saved symbol table."""
    startup = contract["startup"]
    boot = (
        APPEND_OFFSET
        - (startup["startup"]["relocated_cs"] - startup["load_segment"]) * 16
    )
    for command in (
        ["as", "--32", "-o", "probe.o", "instrumentation.S"],
        ["ld", "-m", "elf_i386", "-Ttext", hex(boot), "-o", "probe.elf", "probe.o"],
        [
            "ld",
            "-m",
            "elf_i386",
            "-Ttext",
            hex(boot),
            "--oformat",
            "binary",
            "-o",
            "payload.bin",
            "probe.o",
        ],
    ):
        completed = subprocess.run(
            command, cwd=output, capture_output=True, timeout=30, check=False
        )
        with (output / "build.log").open("ab") as log:
            log.write(completed.stdout + completed.stderr)
        completed.check_returncode()
    symbols = subprocess.run(
        ["nm", "probe.elf"],
        cwd=output,
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    ).stdout
    (output / "symbols.txt").write_text(symbols)
    return {line.split()[-1]: int(line.split()[0], 16) for line in symbols.splitlines()}


def run(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: one actual caller observation and one frozen Pascal projection, no repair/retry."""
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "Liero BYOD unavailable"}
    binary, contract, source = entry_contract(root)
    freeze = freeze_method(root, contract, source)
    output.mkdir(parents=True, exist_ok=False)
    pilot.save(output / "freeze.json", freeze)
    (output / "candidate.inc").write_text(source)
    (output / "methods").mkdir()
    for name in freeze["method_hashes"]:
        shutil.copy2(root / name, output / "methods" / pathlib.Path(name).name)
    result = {
        "status": "failed",
        "oracle": contract["oracle"],
        "model_requests": 0,
        "original_executions": 0,
        "candidate_executions": 0,
        "heldout_evaluations": 0,
        "routine_recovered": False,
        "source_promoted": False,
        "unresolved": contract["unresolved"],
    }

    def validate_frozen() -> None:
        """Oracle: reject method/source/premise drift both before and after original/Pascal execution."""
        _, current, current_source = entry_contract(root)
        if (
            freeze_method(root, current, current_source) != freeze
            or json.loads((output / "freeze.json").read_text()) != freeze
            or (output / "candidate.inc").read_text() != source
        ):
            raise ValueError("allocator entry freeze/premises/source changed")

    try:
        validate_frozen()
        (output / "instrumentation.S").write_text(instrumentation_source(contract))
        labels = assemble(output, contract)
        image, patches = build_image(
            binary, contract, (output / "payload.bin").read_bytes(), labels
        )
        (output / "PROBE.COM").write_bytes(image)
        pilot.save(output / "patches.json", patches)
        result["original_executions"] = 1
        run_dosbox(output)
        validate_frozen()
        measured = compare_trace((output / "TRACE.BIN").read_bytes(), contract)
        result["measurement"] = measured
        result["candidate_executions"] = 1
        rows = pilot.allocator_candidate(
            output / "pascal", source, [tuple(measured["pascal_case"])]
        )
        validate_frozen()
        if rows != [measured["expected_pascal_row"]]:
            raise ValueError("allocator observed caller vs frozen Pascal differs")
        result.update(
            status="passed", stop_reason="one-instrumented-caller-context-validated"
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
    """Oracle: replay observed inputs, original image and complete result against current frozen source/method."""
    binary, contract, source = entry_contract(root)
    freeze = freeze_method(root, contract, source)
    report = json.loads((output / "result.json").read_text())
    if (
        json.loads((output / "freeze.json").read_text()) != freeze
        or report["freeze_sha256"] != pilot.digest(output / "freeze.json")
        or report["status"] != "passed"
        or report["oracle"] != contract["oracle"]
        or report["unresolved"] != contract["unresolved"]
        or report["original_executions"] != 1
        or report["candidate_executions"] != 1
        or report["model_requests"] != 0
        or report["heldout_evaluations"] != 0
        or report["routine_recovered"] is not False
        or report["source_promoted"] is not False
        or (output / "candidate.inc").read_text() != source
        or (output / "instrumentation.S").read_text()
        != instrumentation_source(contract)
    ):
        raise ValueError("allocator entry report/source/freeze invalid")
    labels = {
        line.split()[-1]: int(line.split()[0], 16)
        for line in (output / "symbols.txt").read_text().splitlines()
    }
    image, patches = build_image(
        binary, contract, (output / "payload.bin").read_bytes(), labels
    )
    if image != (output / "PROBE.COM").read_bytes() or patches != json.loads(
        (output / "patches.json").read_text()
    ):
        raise ValueError("allocator entry saved original image/patches differ")
    measured = compare_trace((output / "TRACE.BIN").read_bytes(), contract)
    if (
        report["measurement"] != measured
        or (output / "pascal/candidate.inc").read_text() != source
        or (output / "pascal/probe.pas").read_text()
        != pilot.allocator_candidate_program([tuple(measured["pascal_case"])])
        or (output / "pascal/PASCAL.BIN").read_bytes()
        != struct.pack("<8H", *measured["expected_pascal_row"])
    ):
        raise ValueError("allocator entry saved observed/Pascal projection differs")
    required = {
        "freeze.json",
        "candidate.inc",
        "instrumentation.S",
        "symbols.txt",
        "payload.bin",
        "PROBE.COM",
        "patches.json",
        "TRACE.BIN",
        "build.log",
        "dosbox.log",
        "pascal/candidate.inc",
        "pascal/probe.pas",
        "pascal/probe",
        "pascal/compile.log",
        "pascal/execution.log",
        "pascal/PASCAL.BIN",
    }
    for name, identity in freeze["method_hashes"].items():
        saved = f"methods/{pathlib.Path(name).name}"
        required.add(saved)
        if pilot.digest(output / saved) != identity:
            raise ValueError("allocator entry saved method differs")
    if not required <= report["artifact_hashes"].keys():
        raise ValueError("allocator entry required artifact hashes missing")
    for name, identity in report["artifact_hashes"].items():
        path = (output / name).resolve()
        if not path.is_relative_to(output.resolve()) or pilot.digest(path) != identity:
            raise ValueError("allocator entry artifact changed")
    return report


def main() -> int:
    """Oracle: scoped pass/failure/skip CLI; replay does not execute original or Pascal."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    report = validate_report(ROOT, output) if args.replay else run(ROOT, output)
    print(
        json.dumps(
            {key: value for key, value in report.items() if key != "artifact_hashes"},
            indent=2,
        )
    )
    return 0 if report["status"] in {"passed", "skipped"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
