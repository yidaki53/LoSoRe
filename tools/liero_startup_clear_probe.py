"""Frozen startup clear/Pascal projections and original-only heap/service observations."""

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
from engine.evidence_archive import read_archive, seal_archive
from tools.liero_file_probe import run_dosbox
from tools.liero_four_routine_pilot import (
    run_prefix_transfer,
    save,
    validate_partial_memory_source,
    write_partial_memory_source,
)
from tools.liero_startup_clear_contract import (
    startup_clear_contract,
    startup_heap_contract,
    startup_vector_boundary_contract,
)

SEEDS = (0xA5, 0x5A, 0xFF)
WINDOW = (0x6000, 0x8000)
APPEND_OFFSET = 0x21800
SERVICE_WINDOW = (0x63D8, 0x7B52)
SERVICE_REGISTERS = (
    "AX",
    "BX",
    "CX",
    "DX",
    "SI",
    "DI",
    "BP",
    "DS",
    "ES",
    "SS",
    "SP",
    "FLAGS",
    "PSP_END",
    "VECTOR0_OFF",
    "VECTOR0_SEG",
    "IVT21_OFF",
    "IVT21_SEG",
)
SECOND_SERVICE_REGISTERS = SERVICE_REGISTERS + ("VECTOR2_OFF", "VECTOR2_SEG")
THIRD_SERVICE_REGISTERS = SECOND_SERVICE_REGISTERS + ("VECTOR1B_OFF", "VECTOR1B_SEG")
VECTOR_NUMBERS = bytes.fromhex("00021b2123243435363738393a3b3c3d3e3f75")
BATCH_REGISTERS = SERVICE_REGISTERS + tuple(
    f"VECTOR{number:02X}_{part}"
    for number in VECTOR_NUMBERS[1:]
    for part in ("OFF", "SEG")
)


def service_instrumentation_source(
    contract: dict,
    *,
    bridge: bool = False,
    second: bool = False,
    third: bool = False,
    vector_batch: bool = False,
) -> str:
    """Oracle: disclosed first-call/bridge or second-call snapshots, not universal DOS ABI."""
    if third and (bridge or second):
        raise ValueError("third service cannot combine with bridge or second")
    if vector_batch and (bridge or second or third):
        raise ValueError("vector batch cannot combine with per-call modes")
    record_registers = (
        BATCH_REGISTERS
        if vector_batch
        else THIRD_SERVICE_REGISTERS
        if third
        else SECOND_SERVICE_REGISTERS
        if second
        else SERVICE_REGISTERS
    )
    relative_cs = contract["startup"]["relocated_cs"] - contract["load_segment"]
    original_cs = contract["mz"]["initial_cs"] - contract["load_segment"]
    original_ip = contract["mz"]["initial_ip"]
    size = SERVICE_WINDOW[1] - SERVICE_WINDOW[0]
    snapshots = []
    for label in ("before", "after"):
        vector2 = (
            f"""
    mov %es:8, %ax
    mov %ax, %cs:{label}_VECTOR2_OFF
    mov %es:10, %ax
    mov %ax, %cs:{label}_VECTOR2_SEG
"""
            if second or third
            else ""
        )
        vector1b = (
            f"""
    mov %es:0x6c, %ax
    mov %ax, %cs:{label}_VECTOR1B_OFF
    mov %es:0x6e, %ax
    mov %ax, %cs:{label}_VECTOR1B_SEG
"""
            if third
            else ""
        )
        if vector_batch:
            vector1b = "\n".join(
                f"    mov %es:{4 * number + delta}, %ax\n"
                f"    mov %ax, %cs:{label}_VECTOR{number:02X}_{part}"
                for number in VECTOR_NUMBERS[1:]
                for delta, part in ((0, "OFF"), (2, "SEG"))
            )
        registers = "\n".join(
            f"    mov %{reg.lower()}, %cs:{label}_{reg}"
            for reg in SERVICE_REGISTERS[:11]
        )
        snapshots.append(f"""
{registers}
    pushf
    popw %cs:{label}_FLAGS
    pushf
    push %ax
    push %cx
    push %si
    push %di
    push %es
    mov %cs:initial_es, %ax
    mov %ax, %es
    mov %es:2, %ax
    mov %ax, %cs:{label}_PSP_END
    xor %ax, %ax
    mov %ax, %es
    mov %es:0, %ax
    mov %ax, %cs:{label}_VECTOR0_OFF
    mov %es:2, %ax
    mov %ax, %cs:{label}_VECTOR0_SEG
    mov %es:0x84, %ax
    mov %ax, %cs:{label}_IVT21_OFF
    mov %es:0x86, %ax
    mov %ax, %cs:{label}_IVT21_SEG
{vector2}
{vector1b}
    push %cs
    pop %es
    mov ${SERVICE_WINDOW[0]}, %si
    mov ${label}_memory, %di
    mov ${size}, %cx
    cld
    rep movsb
    pop %es
    pop %di
    pop %si
    pop %cx
    pop %ax
    popf
""")
    record = "\n".join(
        f"{label}_{reg}: .word 0"
        for label in ("before", "after")
        for reg in record_registers
    )
    path = (
        f"""
    pushf
    cmp $19, %cx
    je first_query
    popf
{snapshots[1]}
    jmp output
first_query:
    popf
    jmp 0x56
collector:
{snapshots[0]}
    .byte 0x89, 0x1d, 0x8c, 0x45, 0x02
    jmp 0x5f
output:
"""
        if bridge
        else f"""
{snapshots[0]}
    jmp 0x56
collector:
{snapshots[1]}
"""
    )
    if second or third:
        path = f"""
    pushf
    cmp ${17 if third else 18}, %cx
    jne run_query
    popf
{snapshots[0]}
    jmp 0x56
run_query:
    popf
    jmp 0x56
collector:
    pushf
    cmp ${17 if third else 19}, %cx
    {"jne" if third else "je"} save_first_pointer
    popf
{snapshots[1]}
    jmp output
save_first_pointer:
    popf
    .byte 0x89, 0x1d, 0x8c, 0x45, 0x02
    jmp 0x5f
output:
"""
    if bridge and second:
        path = f"""
    pushf
    cmp $17, %cx
    je third_input
    popf
    jmp 0x56
third_input:
    popf
{snapshots[1]}
    jmp output
collector:
    pushf
    cmp $18, %cx
    je second_return
    popf
    jmp save_pointer
second_return:
    popf
{snapshots[0]}
save_pointer:
    .byte 0x89, 0x1d, 0x8c, 0x45, 0x02
    jmp 0x5f
output:
"""
    if vector_batch:
        path = f"""
    pushf
    cmp $19, %cx
    jne batch_query
    popf
{snapshots[0]}
    jmp 0x56
batch_query:
    popf
    jmp 0x56
collector:
{snapshots[1]}
"""
    return f"""
.code16
.global _start, collector, before_service
_start:
    mov %ss, %cs:initial_ss
    mov %sp, %cs:initial_sp
    mov %es, %cs:initial_es
    pushf
    push %ax
    mov %cs, %ax
    sub ${relative_cs - original_cs}, %ax
    mov %ax, %cs:entry_pointer+2
    pop %ax
    popf
    ljmp *%cs:entry_pointer
before_service:
    .byte 0xfc, 0x2e, 0xac
{path}
    push %cs
    pop %ds
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, %bx
    mov $record, %dx
    mov ${6 + 4 * len(record_registers) + 2 * size}, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp ${6 + 4 * len(record_registers) + 2 * size}, %ax
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
entry_pointer: .word {original_ip}, 0
record:
initial_ss: .word 0
initial_sp: .word 0
initial_es: .word 0
{record}
before_memory: .space {size}
after_memory: .space {size}
"""


def sha(data: bytes) -> str:
    """Oracle: immutable artifact identity."""
    return hashlib.sha256(data).hexdigest()


def instrumentation_source(contract: dict, seed: int, *, heap: bool = False) -> str:
    """Oracle: disclosed bootstrap/collector, outside the measured original path."""
    if seed not in SEEDS:
        raise ValueError("seed outside frozen three-case budget")
    startup_segment = contract["startup"]["relocated_cs"] - contract["load_segment"]
    data_segment = contract["startup"]["relocated_ds"] - contract["load_segment"]
    original_cs = contract["mz"]["initial_cs"] - contract["load_segment"]
    original_ip = contract["mz"]["initial_ip"]
    dirty_setup = (
        f"""
    mov $0x6000, %di
    mov $0x2000, %cx
    mov ${seed}, %al
    cld
    rep stosb
"""
        if not heap
        else ""
    )
    psp_capture = (
        """
    mov %es:2, %ax
    mov %ax, %cs:psp_end
"""
        if heap
        else ""
    )
    record_size = 18 if heap else 16
    return f"""
.code16
.global _start, collector
_start:
    mov %ss, %cs:initial_ss
    mov %sp, %cs:initial_sp
    mov %es, %cs:initial_es
    pushf
    push %ax
    push %cx
    push %di
    push %es
    mov %cs, %ax
    sub ${startup_segment - original_cs}, %ax
    mov %ax, %cs:entry_pointer+2
    add ${data_segment - original_cs}, %ax
    mov %ax, %es
{dirty_setup}
    pop %es
    pop %di
    pop %cx
    pop %ax
    popf
    ljmp *%cs:entry_pointer
collector:
    mov %cs, %cs:observed_cs
    mov %ds, %cs:observed_ds
    mov %es, %cs:observed_es
    mov %ss, %cs:observed_ss
    mov %sp, %cs:observed_sp
{psp_capture}
    push %ds
    push %cs
    pop %ds
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    pop %ds
    jc failed
    mov %ax, %bx
    mov $0x6000, %dx
    mov $0x2000, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $0x2000, %ax
    jne failed
    push %ds
    push %cs
    pop %ds
    mov $record, %dx
    mov ${record_size}, %cx
    mov $0x4000, %ax
    int $0x21
    pop %ds
    jc failed
    cmp ${record_size}, %ax
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
entry_pointer: .word {original_ip}, 0
record:
initial_ss: .word 0
initial_sp: .word 0
initial_es: .word 0
observed_cs: .word 0
observed_ds: .word 0
observed_es: .word 0
observed_ss: .word 0
observed_sp: .word 0
{"psp_end: .word 0" if heap else ""}
"""


def build_instrumented_mz(
    binary: bytes,
    contract: dict,
    payload: bytes,
    collector: int,
    *,
    heap: bool = False,
    service_entry: int | None = None,
    bridge: bool = False,
    second: bool = False,
    third: bool = False,
    vector_batch: bool = False,
) -> tuple[bytes, dict]:
    """Oracle: exact patch inventory; original entry/prefix/clear and allocation preserved."""
    if sha(binary) != contract["binary_sha256"]:
        raise ValueError("binary differs from checked contract")
    if third and (bridge or second):
        raise ValueError("third service cannot combine with bridge or second")
    if vector_batch and (
        bridge or second or third or service_entry is None or not heap
    ):
        raise ValueError("vector batch requires exclusive service entry and heap mode")
    displaced_stores = bridge or second or third
    if displaced_stores and service_entry is None:
        raise ValueError("bridge requires service snapshot entry")
    header = contract["mz"]["header_bytes"]
    startup_segment = contract["startup"]["relocated_cs"] - contract["load_segment"]
    boot_ip = APPEND_OFFSET - startup_segment * 16
    if not payload or not boot_ip < collector < boot_ip + len(payload) <= 65536:
        raise ValueError(
            "instrumentation exceeds startup segment or collector is invalid"
        )
    data_segment = contract["startup"]["relocated_ds"] - contract["load_segment"]
    window_start, window_end = (data_segment * 16 + offset for offset in WINDOW)
    if not 0 <= window_start < window_end <= contract["mz"]["minimum_allocation_bytes"]:
        raise ValueError("dirty window exceeds original guaranteed allocation")
    for name in ("entry_code", "startup_prefix", "clear_code", "active_stack"):
        start, stop = contract["module_relative_ranges"][name]
        if window_start < stop and start < window_end:
            raise ValueError(f"dirty window aliases {name}")
    if APPEND_OFFSET < window_end:
        raise ValueError("instrumentation aliases measured DS window")
    end = APPEND_OFFSET + len(payload)
    if end > contract["module_relative_ranges"]["active_stack"][0] - 32:
        raise ValueError("instrumentation aliases active/bootstrap stack")
    original_paragraphs = (contract["mz"]["image_bytes"] + 15) // 16
    added_paragraphs = (end + 15) // 16 - original_paragraphs
    minimum, maximum = struct.unpack_from("<HH", binary, 10)
    if minimum < added_paragraphs or maximum < added_paragraphs:
        raise ValueError("instrumentation cannot preserve original allocation")
    instrumented = bytearray(binary)
    instrumented.extend(bytes(header + APPEND_OFFSET - len(binary)))
    instrumented.extend(payload)
    struct.pack_into(
        "<HH",
        instrumented,
        2,
        len(instrumented) % 512,
        (len(instrumented) + 511) // 512,
    )
    struct.pack_into(
        "<HH", instrumented, 10, minimum - added_paragraphs, maximum - added_paragraphs
    )
    struct.pack_into("<HH", instrumented, 20, boot_ip, startup_segment)
    stop = (
        0x64
        if vector_batch
        else 0x5A
        if service_entry is not None
        else (0x49 if heap else 14)
    )
    continuation = contract["startup"]["file_offset"] + stop
    struct.pack_into(
        "<BH", instrumented, continuation, 0xE9, (collector - stop - 3) & 65535
    )
    if service_entry is not None:
        if not heap or not boot_ip < service_entry < boot_ip + len(payload):
            raise ValueError("invalid service snapshot entry")
        struct.pack_into(
            "<BH",
            instrumented,
            contract["startup"]["file_offset"] + 0x53,
            0xE9,
            (service_entry - 0x56) & 65535,
        )
        if displaced_stores:
            instrumented[continuation + 3 : continuation + 5] = b"\x90\x90"
    sections = [
        ("entry", 5),
        ("startup", 0x53 if service_entry is not None else stop),
        ("clear", 18),
    ]
    if heap:
        sections.append(("cpu", 37))
    for section, size in sections:
        offset = contract[section]["file_offset"]
        if instrumented[offset : offset + size] != binary[offset : offset + size]:
            raise ValueError(f"instrumentation altered original {section}")
    if service_entry is not None:
        location = contract["startup"]["file_offset"]
        if (
            vector_batch
            and instrumented[location + 0x56 : location + 0x64]
            != binary[location + 0x56 : location + 0x64]
        ):
            raise ValueError("instrumentation altered original vector loop body")
        if (
            instrumented[location + 0x56 : location + 0x5A]
            != binary[location + 0x56 : location + 0x5A]
        ):
            raise ValueError("instrumentation altered original AH35/INT21")
        if (
            displaced_stores
            and instrumented[location + 0x5F : location + 0x64]
            != binary[location + 0x5F : location + 0x64]
        ):
            raise ValueError("instrumentation altered original ADD/LOOP")
    changed = [
        {"file_offset": index, "original": before, "instrumented": after}
        for index, (before, after) in enumerate(zip(binary, instrumented))
        if before != after
    ]
    allowed = {
        *range(2, 6),
        *range(10, 14),
        *range(20, 24),
        *range(continuation, continuation + (5 if displaced_stores else 3)),
        *(
            range(
                contract["startup"]["file_offset"] + 0x53,
                contract["startup"]["file_offset"] + 0x56,
            )
            if service_entry is not None
            else ()
        ),
    }
    if any(change["file_offset"] not in allowed for change in changed):
        raise ValueError("undisclosed original-byte patch")
    return bytes(instrumented), {
        "original_sha256": sha(binary),
        "instrumented_sha256": sha(instrumented),
        "original_byte_changes": changed,
        "appended_module_offset": APPEND_OFFSET,
        "payload_sha256": sha(payload),
        "padding_bytes": header + APPEND_OFFSET - len(binary),
        "boot_ip": boot_ip,
        "collector_ip": collector,
        "stop_before_startup_offset": 0x56 if bridge else stop,
        "snapshot_return_offset": stop,
        "allocation_bytes_preserved": contract["mz"]["minimum_allocation_bytes"],
        "dirty_window_module_relative": [window_start, window_end],
        "window_dirtied": not heap,
        "service_snapshot_entry": service_entry,
        "disclosure": [
            *(
                [
                    "Batch snapshots before first query and at0064 after all19 original calls/stores/ADD/LOOP. Only0053 prefix displaced; no per-call return interception. Stops before installation. Endpoint checks only, no universal ABI/Pascal/lifetime acceptance."
                ]
                if vector_batch
                else []
            ),
            "Header entry redirects to appended bootstrap, then far-jumps to unchanged original entry.",
            "Heap mode leaves original file-backed data intact; clear mode dirties DS window."
            if heap
            else "Bootstrap dirties the fixed DS window before original entry.",
            "Original first far call, startup bytes through near CALL, relocation table and all clear bytes are unchanged.",
            f"Startup +{stop} is patched to jump to appended collector; subsequent execution is limited to the disclosed bridge."
            if displaced_stores
            else f"Startup +{stop} is patched to jump to appended collector; no later original instructions execute.",
            "Header file size and extra-paragraph counts change to preserve original minimum and maximum allocation totals.",
            "This is instrumented MZ execution, not normal unmodified startup.",
            "Service bootstrap temporarily uses four stack bytes and restores flags/AX/SP before original entry."
            if service_entry is not None
            else "Bootstrap temporarily uses ten stack bytes and restores flags, AX/CX/DI/ES and SP before original entry.",
            "DOSBox executes the MZ image named PROBE.COM using the existing probe runner.",
            *(
                [
                    "Startup0053..0055 CLD/CS:LODSB moves unchanged to the disclosed pre-service gateway in the same CS; returns to0056.",
                    "All19 original AH35/INT21, pointer stores and ADD/LOOP execute in place; stop0064 before installation."
                    if vector_batch
                    else "Original0056 MOV AH,35 and0058 INT21 execute unchanged three times; first two pointer stores displaced unchanged; third return exits before stores."
                    if third
                    else "Original0056 MOV AH,35 and0058 INT21 execute unchanged twice; both returned pointers saved by displaced stores; third input collected before its MOV AH35/INT21."
                    if bridge and second
                    else "Original0056 MOV AH,35 and0058 INT21 execute unchanged twice; first returned pointer saved by displaced stores; second return collected before its stores."
                    if second
                    else "Original0056 MOV AH,35 and0058 INT21 execute unchanged once; jump005a collects before original pointer stores/remaining loop.",
                    "Pre/post snapshots copy DS[63d8,7b52), record registers/FLAGS/PSP:2/IVT0/IVT21 before collector DOS calls. Snapshot scratch uses fourteen stack bytes including PUSH CS, within checked minimum allocation and disjoint from protected data/code; handler-internal stack and far-return contents are not checked.",
                ]
                if service_entry is not None
                else []
            ),
        ],
        "bridge_disclosure": [
            "At first return005a snapshot before, then displaced original005a..005e MOV[DI],BX/MOV[DI+2],ES execute unchanged in same-CS gateway.",
            "005a..005e patched JMP plus two NOPs; original005f ADD DI,4 and0062 LOOP0053 remain intact.",
            "Gateway executes displaced CLD/CS:LODSB each iteration; PUSHF/CMP CX,19/POPF dispatch restores flags. First query returns0056; next query snapshots after and exits before second MOV AH,35/INT21.",
            "Before/after record means first-service-return/next-query-input, NOT first service pre/post. No claim about first service endpoint equality in this case.",
        ]
        if bridge and not second
        else [],
        "second_service_disclosure": [
            "Snapshots enclose second AH35/AL2 only; first AH35/AL0 and displaced first stores/ADD/LOOP establish its context without pre/post measurement.",
            "005a..005e JMP plus two NOPs; original first pointer stores execute unchanged at gateway, original ADD/LOOP intact.",
            "Before-query dispatch PUSHF/CMP CX,18/POPF and return dispatch PUSHF/CMP CX,19/POPF preserve flags; second return exits before stores/remaining17 queries.",
            "Record adds IVT2 words from physical8..11 to each snapshot; exact12102 bytes, no Pascal or normalization.",
        ]
        if second and not bridge
        else [],
        "second_bridge_disclosure": [
            "Snapshots enclose second-return to third-input bridge, NOT a service pre/post check; first call/save and second call establish baseline.",
            "005a..005e JMP plus two NOPs; unchanged displaced pointer stores execute twice in same CS; original ADD/LOOP intact.",
            "CLD/CS:LODSB relocated unchanged; PUSHF/CMP CX,17/POPF query dispatch and PUSHF/CMP CX,18/POPF return dispatch restore flags. Third input exits before0056.",
            "Record includes IVT0/2/21, PSP:2 and both protected windows; exact12102 bytes. Only second slot predicted to change; no third service or whole-loop acceptance.",
        ]
        if bridge and second
        else [],
        "third_service_disclosure": [
            "First two calls/stores establish input; only third AH35/AL1b pre/post measured, stop third005a before its stores/remaining16 queries.",
            "Original005a..005e stores execute unchanged twice in same CS; original ADD/LOOP and AH35/INT21 intact. Prefix CLD/CS:LODSB relocated unchanged.",
            "Query and return dispatch PUSHF/CMP CX,17/POPF restore flags; no assumed beforeAH, returnedAX/DX/BP/FLAGS preservation.",
            "Each snapshot adds IVT1B from physical6c..6f; exact12110 bytes; PSP:2/IVT0/2/1b/21 and DS[63d8,7b52) captured.",
        ]
        if third
        else [],
    }


def compare_trace(trace: bytes, pascal: bytes, contract: dict, seed: int) -> dict:
    """Oracle: full guarded memory plus original-only loader segment/stack observations."""
    if len(trace) != 8208 or len(pascal) != 8192:
        raise ValueError("original/Pascal trace has incorrect length")
    initial_ss, initial_sp, initial_es, cs, ds, es, ss, sp = struct.unpack(
        "<8H", trace[8192:]
    )
    relative_ss = contract["mz"]["initial_ss"] - contract["load_segment"]
    base = initial_ss - relative_ss
    if not 16 <= base <= 65535:
        raise ValueError("observed load base is unsupported")
    if (
        initial_sp != contract["mz"]["initial_sp"]
        or ss != initial_ss
        or sp != initial_sp - 4
        or initial_es != base - 16
        or cs != base + contract["startup"]["relocated_cs"] - contract["load_segment"]
        or ds != base + contract["startup"]["relocated_ds"] - contract["load_segment"]
        or es != ds
    ):
        raise ValueError(
            "original loader/segment/near-return stack observation differs"
        )
    original = trace[:8192]
    begin, end = contract["clear"]["ds_range"]
    expected = bytearray([seed] * 8192)
    expected[begin - WINDOW[0] : end - WINDOW[0]] = bytes(end - begin)
    # Startup saves entry ES before the clear; the memory-only Pascal projection does not.
    saved_es = contract["module_relative_ranges"]["saved_entry_es"][0]
    data_origin = (contract["startup"]["relocated_ds"] - contract["load_segment"]) * 16
    saved_offset = saved_es - data_origin - WINDOW[0]
    expected[saved_offset : saved_offset + 2] = initial_es.to_bytes(2, "little")
    if original != expected:
        raise ValueError(
            "original full-window memory differs from independently checked contract"
        )
    projected = bytearray(pascal)
    if projected[saved_offset : saved_offset + 2] != bytes([seed, seed]):
        raise ValueError("Pascal changed startup-only saved-ES bytes")
    projected[saved_offset : saved_offset + 2] = initial_es.to_bytes(2, "little")
    if original != projected:
        raise ValueError(
            "Pascal memory projection differs from original after explicit startup composition"
        )
    return {
        "seed": seed,
        "bytes_checked": 8192,
        "cleared_bytes": end - begin,
        "guards_checked": 8192 - (end - begin) - 2,
        "startup_only_saved_es": {"window_offset": saved_offset, "value": initial_es},
        "pascal_startup_composition": "Inject only independently observed/contract-checked startup ES store; all other 8190 bytes compared unchanged.",
        "observed_load_segment": base,
        "original_only_ss": ss,
        "original_only_sp_before_entry": initial_sp,
        "original_only_sp_after_clear": sp,
        "original_only_cs": cs,
        "original_only_ds": ds,
        "original_only_es": es,
        "trace_sha256": sha(trace),
        "pascal_sha256": sha(pascal),
        "status": "passed",
    }


def compare_heap_trace(trace: bytes, contract: dict) -> dict:
    """Oracle: original-only startup cells and PSP observation, not Pascal/allocation parity."""
    if len(trace) != 8210:
        raise ValueError("heap trace has incorrect length")
    initial_ss, initial_sp, initial_es, cs, ds, es, ss, sp, limit = struct.unpack(
        "<9H", trace[8192:]
    )
    relative_ss = contract["mz"]["initial_ss"] - contract["load_segment"]
    base = initial_ss - relative_ss
    if (
        not 16 <= base <= 65535
        or initial_sp != contract["mz"]["initial_sp"]
        or ss != initial_ss
        or sp != initial_sp - 4
        or initial_es != base - 16
        or es != initial_es
        or cs != base + contract["startup"]["relocated_cs"] - contract["load_segment"]
        or ds != base + contract["startup"]["relocated_ds"] - contract["load_segment"]
    ):
        raise ValueError("heap loader/segment/stack observation differs")
    if sp + 0x13 > 65535:
        raise ValueError("unsupported heap stack rounding wrap")
    heap_segment = ss + ((sp + 0x13) >> 4)
    if not heap_segment <= limit <= 0xA000:
        raise ValueError(
            "PSP allocation end is outside supported conventional-memory bounds"
        )
    begin, end = contract["clear"]["ds_range"]
    if trace[begin - WINDOW[0] : end - WINDOW[0]] != bytes(end - begin):
        raise ValueError("heap startup clear bytes differ")
    words = {
        **{cell: 0 for cell in contract["heap"]["initial_zero_words"]},
        **{cell: heap_segment for cell in contract["heap"]["heap_segment_stores"]},
        0x63F4: limit,
        0x63FE: 0xD6,
        0x6400: cs,
        0x640C: initial_es,
    }
    for cell, expected in words.items():
        actual = struct.unpack_from("<H", trace, cell - WINDOW[0])[0]
        if actual != expected:
            raise ValueError(f"heap startup word DS:{cell:04x} differs")
    cpu_class = trace[0x6420 - WINDOW[0]]
    if cpu_class not in (0, 1, 2):
        raise ValueError("CPU classification is outside reviewed path outputs")
    return {
        "status": "passed",
        "observed_load_segment": base,
        "observed_psp_segment": initial_es,
        "observed_cpu_class": cpu_class,
        "original_only_cs": cs,
        "original_only_ds": ds,
        "original_only_es": es,
        "original_only_ss": ss,
        "original_only_sp": sp,
        "heap_start_segment": heap_segment,
        "allocation_end_segment": limit,
        "spare_heap_bytes": (limit - heap_segment) * 16,
        "checked_words": {f"{cell:04x}": value for cell, value in words.items()},
        "cleared_bytes_checked": end - begin,
        "trace_bytes": len(trace),
        "trace_sha256": sha(trace),
        "allocation_success_established": False,
        "pascal_parity": False,
    }


def compare_service_trace(
    trace: bytes,
    contract: dict,
    *,
    bridge: bool = False,
    second: bool = False,
    third: bool = False,
) -> dict:
    """Oracle: one finite pre/post register/IVT/memory observation, not universal service ABI."""
    if third and (bridge or second):
        raise ValueError("third service cannot combine with bridge or second")
    registers = (
        THIRD_SERVICE_REGISTERS
        if third
        else SECOND_SERVICE_REGISTERS
        if second
        else SERVICE_REGISTERS
    )
    size = SERVICE_WINDOW[1] - SERVICE_WINDOW[0]
    record_bytes = 6 + 4 * len(registers)
    if len(trace) != record_bytes + 2 * size:
        raise ValueError("service trace has incorrect length")
    initial_ss, initial_sp, initial_es = struct.unpack_from("<3H", trace)
    before = dict(
        zip(registers, struct.unpack_from(f"<{len(registers)}H", trace, 6), strict=True)
    )
    after = dict(
        zip(
            registers,
            struct.unpack_from(f"<{len(registers)}H", trace, 6 + 2 * len(registers)),
            strict=True,
        )
    )
    base = initial_ss - (contract["mz"]["initial_ss"] - contract["load_segment"])
    expected_ds = base + contract["startup"]["relocated_ds"] - contract["load_segment"]
    expected_cs = base + contract["startup"]["relocated_cs"] - contract["load_segment"]
    if (
        not 16 <= base <= 65535
        or initial_es != base - 16
        or initial_sp != contract["mz"]["initial_sp"]
        or before["SS"] != initial_ss
        or before["SP"] != initial_sp - 4
        or before["DS"] != expected_ds
        or (not bridge and not second and not third and before["ES"] != initial_es)
        or before["CX"] != (17 if third else 18 if second else 19)
        or before["SI"] != (0x23C if third else 0x23B if second else 0x23A)
        or before["DI"] != (0x7AF8 if third else 0x7AF4 if second else 0x7AF0)
        or (
            not bridge
            and not second
            and not third
            and before["AX"] != before["PSP_END"] & 0xFF00
        )
        or (second and not bridge and before["AX"] & 0xFF != 2)
        or (third and before["AX"] & 0xFF != 0x1B)
        or before["FLAGS"] & (0x100 if bridge else 0x500)
    ):
        raise ValueError("service pre-call loader/register premises differ")
    for reg in (
        "DS",
        "SS",
        "SP",
        "PSP_END",
        "VECTOR0_OFF",
        "VECTOR0_SEG",
        "IVT21_OFF",
        "IVT21_SEG",
    ):
        if after[reg] != before[reg]:
            raise ValueError(f"service changed required {reg}")
    if second or third:
        for reg in ("VECTOR2_OFF", "VECTOR2_SEG"):
            if after[reg] != before[reg]:
                raise ValueError(f"service changed required {reg}")
        if (
            not bridge
            and not third
            and (
                before["BX"] != before["VECTOR0_OFF"]
                or before["ES"] != before["VECTOR0_SEG"]
            )
        ):
            raise ValueError("second service input differs from first vector0 result")
    if third:
        for reg in ("VECTOR1B_OFF", "VECTOR1B_SEG"):
            if after[reg] != before[reg]:
                raise ValueError(f"service changed required {reg}")
        if (
            before["BX"] != before["VECTOR2_OFF"]
            or before["ES"] != before["VECTOR2_SEG"]
        ):
            raise ValueError("third service input differs from second vector2 result")
    result = before if bridge else after
    vector = "VECTOR1B" if third else "VECTOR2" if second else "VECTOR0"
    if (
        result["BX"] != before[f"{vector}_OFF"]
        or result["ES"] != before[f"{vector}_SEG"]
    ):
        raise ValueError(f"AH35 result differs from pre-call {vector.lower()}")
    if bridge:
        expected = {
            "SI": 0x23C if second else 0x23B,
            "DI": 0x7AF8 if second else 0x7AF4,
            "CX": 17 if second else 18,
            "AX": (before["AX"] & 0xFF00) | (0x1B if second else 2),
            "FLAGS": before["FLAGS"] & ~0xCD5,
            **{reg: before[reg] for reg in ("BX", "ES", "DX", "BP")},
        }
        for reg, value in expected.items():
            if after[reg] != value:
                raise ValueError(f"bridge next input {reg} differs")
    elif any(after[reg] != before[reg] for reg in ("SI", "DI", "CX")):
        raise ValueError("service changed required loop registers")
    before_memory = trace[record_bytes : record_bytes + size]
    after_memory = trace[record_bytes + size :]
    expected_memory = bytearray(before_memory)
    if bridge:
        struct.pack_into(
            "<HH",
            expected_memory,
            (0x7AF4 if second else 0x7AF0) - SERVICE_WINDOW[0],
            before["BX"],
            before["ES"],
        )
    if expected_memory != after_memory:
        raise ValueError("service changed protected memory window")
    sp = before["SP"]
    if sp + 0x13 > 65535:
        raise ValueError("unsupported service heap rounding wrap")
    heap_segment = initial_ss + ((sp + 0x13) >> 4)
    if not heap_segment <= before["PSP_END"] <= 0xA000:
        raise ValueError("unsupported service PSP allocation end")
    cells = {
        **{cell: 0 for cell in contract["heap"]["initial_zero_words"]},
        **{cell: heap_segment for cell in contract["heap"]["heap_segment_stores"]},
        0x63F4: before["PSP_END"],
        0x63FE: 0xD6,
        0x6400: expected_cs,
        0x640C: initial_es,
    }
    for cell, value in cells.items():
        if (
            struct.unpack_from("<H", before_memory, cell - SERVICE_WINDOW[0])[0]
            != value
        ):
            raise ValueError(f"service pre-call heap cell {cell:04x} differs")
    begin, end = contract["clear"]["ds_range"]
    expected_clear = bytearray(end - begin)
    if second or third:
        struct.pack_into(
            "<HH",
            expected_clear,
            0x7AF0 - begin,
            before["VECTOR0_OFF"],
            before["VECTOR0_SEG"],
        )
    if third:
        struct.pack_into(
            "<HH",
            expected_clear,
            0x7AF4 - begin,
            before["VECTOR2_OFF"],
            before["VECTOR2_SEG"],
        )
    if (
        before_memory[begin - SERVICE_WINDOW[0] : end - SERVICE_WINDOW[0]]
        != expected_clear
    ):
        raise ValueError("service pre-call clear differs")
    if before_memory[0x6420 - SERVICE_WINDOW[0]] not in (0, 1, 2):
        raise ValueError("service pre-call CPU class differs")
    measurement = {
        "status": "passed",
        "before": before,
        "after": after,
        "observed_load_segment": base,
        "protected_ds_range": list(SERVICE_WINDOW),
        "protected_bytes_unchanged": size - (4 if bridge else 0),
        "memory_bytes_checked": size,
        "protected_memory_sha256": sha(before_memory),
        "trace_sha256": sha(trace),
        "trace_bytes": len(trace),
        "handler21_observed": [before["IVT21_SEG"], before["IVT21_OFF"]],
        "vector0_result": [before["VECTOR0_SEG"], before["VECTOR0_OFF"]],
        "bridge_observed": bridge,
        "next_service_ax": (0x351B if second else 0x3502) if bridge else None,
        "second_service_executed": second,
        "service_contract_established": False,
        "allocation_success_established": False,
        "pascal_parity": False,
    }
    if second:
        measurement["vector2_result"] = [result["ES"], result["BX"]]
        measurement["first_slot_bytes_checked"] = 4
        measurement["second_pointer_store_executed"] = bridge
        if bridge:
            measurement["third_service_executed"] = False
    if third:
        measurement.update(
            vector2_result=[before["VECTOR2_SEG"], before["VECTOR2_OFF"]],
            vector1b_result=[after["ES"], after["BX"]],
            saved_slot_bytes_checked=8,
            second_service_executed=True,
            second_pointer_store_executed=True,
            third_service_executed=True,
            third_pointer_store_executed=False,
        )
    return measurement


def run_layout_probe(
    root: pathlib.Path,
    output: pathlib.Path,
    *,
    heap: bool = False,
    service: bool = False,
    bridge: bool = False,
    second: bool = False,
    third: bool = False,
) -> dict:
    """Oracle: frozen finite instrumented original-vs-Pascal run; no retry or promotion."""
    if third and (bridge or second):
        raise ValueError("third service cannot combine with bridge or second")
    manifest_path = root / "targets/liero/alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    binary, _, base, _ = load_binary_evidence(root / "targets/liero", manifest)
    service = service or bridge or second or third
    heap = heap or service
    contract = (
        startup_vector_boundary_contract(binary, load_segment=base)
        if service
        else (
            startup_heap_contract(binary, load_segment=base)
            if heap
            else startup_clear_contract(binary, load_segment=base)
        )
    )
    tools = (
        ("as", "ld", "nm", "dosbox") if heap else ("as", "ld", "nm", "dosbox", "fpc")
    )
    for tool in tools:
        if shutil.which(tool) is None:
            raise FileNotFoundError(f"caller-layout probe requires {tool}")
    output.mkdir(parents=True, exist_ok=False)
    paths = (
        pathlib.Path(__file__),
        root / "tools/liero_startup_clear_contract.py",
        root / "tools/liero_four_routine_pilot.py",
        root / "tools/liero_file_probe.py",
        root / "engine/instruction_facts.py",
        root / "engine/alternate_streams.py",
        manifest_path,
        root / "tests/test_liero_startup_clear_probe.py",
    )
    seeds = (SEEDS[0],) if heap else SEEDS
    freeze = {
        "contract": contract,
        "seeds": list(seeds),
        "window": list(WINDOW),
        "method_hashes": {
            str(path.relative_to(root)): sha(path.read_bytes()) for path in paths
        },
        "budget": "one original-only execution; no dirty seed, subprocesses <=30s; first error ends run; no retries"
        if heap
        else "one execution per seed, three cases; each subprocess <=30s; first error ends run; no retries",
        "scope": "original-only instrumented heap/PSP initialization, no Pascal/allocation/source acceptance"
        if heap
        else "known-slice instrumented MZ/host-Pascal memory only, no heldout/model/ABI/source promotion",
        "startup_composition": "Original-only heap/PSP trace; no Pascal projection or memory normalization."
        if heap
        else "Compare startup saved entry ES separately; inject exactly that word into Pascal output before whole-window equality.",
    }
    if service:
        freeze["scope"] = (
            "One original AH35/AL0 INT21 with disclosed pre/post snapshots, stop005a; no later loop, universal service ABI or Pascal parity."
        )
        freeze["service_window"] = list(SERVICE_WINDOW)
        freeze["service_registers"] = list(SERVICE_REGISTERS)
        freeze["startup_composition"] = (
            "Original-only pre/post service snapshots, no Pascal or normalization. "
            "Before snapshot follows displaced CLD/CS:LODSB; AX retains PSP-end high byte. "
            "Unchanged MOV AH,35 at0056 establishes AX3500 before original INT21 at0058."
        )
    if bridge:
        freeze["scope"] = (
            "One original first AH35/AL0 call then first pointer-save/next-input bridge; stop before second MOV AH35/INT21. No retries."
        )
        freeze["startup_composition"] = (
            "Snapshots at first return005a and next input after CLD/CS:LODSB. "
            "Displaced005a..005e stores execute unchanged in same CS; original ADD/LOOP intact. "
            "Expected four-byte first pointer store, other6006 bytes unchanged; nextCX18/SI023b/DI7af4/AL2/DF0. "
            "ADD7af0+4 sets CF/PF/AF/ZF/SF/OF0; CLD clearsDF. "
            "Not a pre/post first-service check; before state must satisfy explicit post-service heap/register premises."
        )
    if second:
        freeze["scope"] = (
            "One distinct original-only startup case: first AH35/AL0 establishes first saved slot, pre/post second AH35/AL2 snapshots, stop second return005a before its stores. No retries."
        )
        freeze["service_registers"] = list(SECOND_SERVICE_REGISTERS)
        freeze["startup_composition"] = (
            "First stores relocated unchanged; ADD/LOOP intact; flags-preserving CX dispatch. "
            "Snapshots before second MOV AH35 (AL2, AH not assumed) and after second INT21. "
            "Check ES:BX against pre-IVT2, required loop registers, IVT0/2/21, PSP:2 and all6010 bytes unchanged. "
            "First slot must match IVT0, remaining clear region zero; no second stores or later query executes. "
            "Exact12102-byte trace; scratch14/bootstrap4/dispatch2 bytes, disjoint tracked data/code/payload; handler-internal stack/live return contents unknown."
        )
    if bridge and second:
        freeze["scope"] = (
            "One distinct original-only startup case: first two calls establish context, "
            "second return005a to third-input snapshots; stop before third MOV AH35/INT21. No retries."
        )
        freeze["startup_composition"] = (
            "Before is second returned state, NOT service input. First saved slot must match IVT0; "
            "returned ES:BX must match IVT2. Displaced pointer stores execute unchanged twice, ADD/LOOP intact. "
            "After third CLD/CS:LODSB, expect only second slotDS7af4..7af7 changed; other6006 bytes unchanged. "
            "Next CX17/SI023c/DI7af8/AL1b/DF0; original MOV AH35 would establishAX351b but does not execute. "
            "ADD7af4+4 clears CF/PF/AF/ZF/SF/OF, CLD clearsDF; other flags/registers and PSP:2/IVT0/2/21 preserved. "
            "Exact12102-byte trace, snapshot14/bootstrap4/dispatch2 scratch; no third service/other-memory/live-return proof or Pascal acceptance."
        )
    if third:
        freeze["scope"] = (
            "One distinct original-only startup case, first two calls/stores setup, pre/post third AH35/AL1b, stop third005a before stores; no retries."
        )
        freeze["service_registers"] = list(THIRD_SERVICE_REGISTERS)
        freeze["startup_composition"] = (
            "Snapshots before third MOV AH35 (AL1b required, AH not assumed) and after third INT21. "
            "First two saved pointers must match IVT0/2, remaining clear region zero; heap/class/callback baseline checked. "
            "ES:BX must match pre-IVT1B; loopDS/SI/DI/CX/SS/SP, PSP:2/IVT0/2/1b/21 and all6010 bytes unchanged. "
            "Original AH35/INT21 three times, displaced stores/prefix unchanged, ADD/LOOP intact, flags-restoring CX17 dispatch. "
            "Exact12110-byte record; bootstrap4/snapshot14/dispatch2 scratch disjoint from tracked code/data/payload. "
            "First two calls setup only; stop before third stores/remaining16 queries; no universal ABI/Pascal/allocator/other-memory/live-return proof."
        )
    save(output / "freeze.json", freeze)
    snapshots = output / "methods"
    snapshots.mkdir()
    for path in paths:
        shutil.copy2(path, snapshots / path.name)
    measurements = []
    try:
        partial = output / "partial"
        if not heap:
            run_prefix_transfer(root, partial, "FUN_24dd_492c", data_window=WINDOW)
            write_partial_memory_source(root, partial)
        for seed in seeds:
            case = output / f"seed-{seed:02x}"
            case.mkdir()
            source = case / "instrumentation.S"
            source.write_text(
                service_instrumentation_source(
                    contract, bridge=bridge, second=second, third=third
                )
                if service
                else instrumentation_source(contract, seed, heap=heap)
            )
            startup_segment = contract["startup"]["relocated_cs"] - base
            boot_ip = APPEND_OFFSET - startup_segment * 16
            commands = [
                ["as", "--32", "-o", str(case / "probe.o"), str(source)],
                [
                    "ld",
                    "-m",
                    "elf_i386",
                    "-Ttext",
                    hex(boot_ip),
                    "-o",
                    str(case / "probe.elf"),
                    str(case / "probe.o"),
                ],
                [
                    "ld",
                    "-m",
                    "elf_i386",
                    "-Ttext",
                    hex(boot_ip),
                    "--oformat",
                    "binary",
                    "-o",
                    str(case / "payload.bin"),
                    str(case / "probe.o"),
                ],
            ]
            for index, command in enumerate(commands):
                completed = subprocess.run(
                    command, check=False, capture_output=True, timeout=30
                )
                (case / f"build-{index}.log").write_bytes(
                    completed.stdout + completed.stderr
                )
                completed.check_returncode()
            symbols = subprocess.run(
                ["nm", str(case / "probe.elf")],
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            ).stdout
            (case / "symbols.txt").write_text(symbols)
            collector = next(
                int(line.split()[0], 16)
                for line in symbols.splitlines()
                if line.split()[-1] == "collector"
            )
            instrumented, patches = build_instrumented_mz(
                binary,
                contract,
                (case / "payload.bin").read_bytes(),
                collector,
                heap=heap,
                service_entry=next(
                    int(line.split()[0], 16)
                    for line in symbols.splitlines()
                    if line.split()[-1] == "before_service"
                )
                if service
                else None,
                bridge=bridge,
                second=second,
                third=third,
            )
            (case / "PROBE.COM").write_bytes(instrumented)
            save(case / "patches.json", patches)
            run_dosbox(case)
            if heap:
                compare = compare_service_trace if service else compare_heap_trace
                measurement = (
                    compare(
                        (case / "TRACE.BIN").read_bytes(),
                        contract,
                        bridge=bridge,
                        second=second,
                        third=third,
                    )
                    if service
                    else compare((case / "TRACE.BIN").read_bytes(), contract)
                )
                measurement["artifact_hashes"] = {
                    path.name: sha(path.read_bytes())
                    for path in case.iterdir()
                    if path.is_file()
                }
                save(case / "result.json", measurement)
                measurements.append(measurement)
                continue
            program = case / "projection.pas"
            program.write_text(f"""program Projection;
{{$I partial-memory.inc}}
var data: TEntryData; outputFile: file; written: LongInt;
begin
  FillChar(data, SizeOf(data), {seed});
  ApplyPartialMemoryEffects(data);
  Assign(outputFile, 'PASCAL.BIN');
  Rewrite(outputFile, 1);
  BlockWrite(outputFile, data[$6000], $2000, written);
  Close(outputFile);
  if written <> $2000 then Halt(1);
end.
""")
            compiled = subprocess.run(
                ["fpc", "-Mtp", "-Cr", f"-Fi{partial}", str(program)],
                check=False,
                cwd=case,
                capture_output=True,
                timeout=30,
            )
            (case / "fpc.log").write_bytes(compiled.stdout + compiled.stderr)
            compiled.check_returncode()
            executed = subprocess.run(
                [str(case / "projection")],
                check=False,
                cwd=case,
                capture_output=True,
                timeout=30,
            )
            (case / "pascal.log").write_bytes(executed.stdout + executed.stderr)
            executed.check_returncode()
            measurement = compare_trace(
                (case / "TRACE.BIN").read_bytes(),
                (case / "PASCAL.BIN").read_bytes(),
                contract,
                seed,
            )
            measurement["artifact_hashes"] = {
                path.name: sha(path.read_bytes())
                for path in case.iterdir()
                if path.is_file()
            }
            save(case / "result.json", measurement)
            measurements.append(measurement)
        if not heap:
            validate_partial_memory_source(root, partial)
        for relative, expected in freeze["method_hashes"].items():
            if sha((root / relative).read_bytes()) != expected:
                raise ValueError("method/input changed during frozen run")
    except (
        OSError,
        ValueError,
        RuntimeError,
        subprocess.SubprocessError,
        StopIteration,
    ) as error:
        save(
            output / "failure.json",
            {
                "status": "failed",
                "error_type": type(error).__name__,
                "error": str(error),
                "completed_cases": len(measurements),
                "retry_allowed": False,
            },
        )
        raise
    result = {
        "status": "scoped-heap-observation-pass" if heap else "scoped-memory-pass",
        "cases": measurements,
        "bytes_checked": sum(
            case["memory_bytes_checked"]
            if service
            else case["cleared_bytes_checked"] + 2 * len(case["checked_words"]) + 1
            for case in measurements
        )
        if heap
        else len(measurements) * 8192,
        "oracle": "instrumented_original_mz_heap_initialization"
        if heap
        else "instrumented_mz_vs_host_pascal_memory_projection",
        "freeze_sha256": sha((output / "freeze.json").read_bytes()),
        "routine_recovered": False,
        "source_promoted": False,
        "limitations": [
            "One disclosed DOSBox instrumented original-only startup observation, not an unmodified normal run.",
            "No dirty initialization; preserves original file-backed heap cells, original entry/clear/CPU/heap instructions and relocation table.",
            "Stops before0049; collector records PSP:2 before its own DOS calls. Later startup/heap/callback lifetime is unproved.",
            "Observed spare capacity is not successful allocation, Pascal parity, full ABI or a new routine recovery.",
        ]
        if heap
        else [
            "Three finite developer-specified dirty-memory contexts; no unseen routine or learned generalization.",
            "Instrumented MZ bootstrap and post-return collector, not unmodified normal-program execution.",
            "Two startup-only saved-ES bytes composed explicitly; Pascal implements only clear memory effects.",
            "Segment/stack observations are original-only; full registers/flags/return ABI is not translated.",
        ],
    }
    if service:
        result.update(
            status="scoped-first-vector-service-observation-pass",
            oracle="instrumented_original_first_ah35_vector0",
            limitations=[
                "One DOSBox AH35/AL0 execution; not all nineteen queries or an installed-handler source/ABI proof.",
                "Only DS[63d8,7b52), recorded registers/PSP:2/IVT0/IVT21 checked; other memory, transient writes and handler-internal stack are unobserved.",
                "Original AH35/INT21 bytes intact; disclosed relocation of CLD/CS:LODSB plus pre/post snapshot code changes execution context.",
                "Original instructions stop005a before pointer saves/remaining loop; no allocator success, Pascal parity, normal-program or later state-lifetime acceptance.",
            ],
        )
    if bridge:
        result.update(
            status="scoped-first-vector-save-bridge-pass",
            oracle="instrumented_original_first_vector_save_bridge",
            limitations=[
                "One first AH35/AL0 call followed by first pointer save and next input; second service never executes.",
                "Original pointer stores relocated unchanged; ADD/LOOP intact; gateway dispatch restores flags. Instrumented context, not normal-program proof.",
                "Snapshots check6010 bytes: four first-slot pointer bytes, other6006 unchanged. Other memory, code/table, live return contents and transient mutations unobserved.",
                "First-return baseline validated, not first-service pre/post preservation; no universal DOS ABI, Pascal parity, allocator success or whole-loop acceptance.",
            ],
        )
    if second:
        result.update(
            status="scoped-second-vector-service-observation-pass",
            oracle="instrumented_original_second_ah35_vector2",
            limitations=[
                "One distinct startup context, first AH35/AL0 and first save establish input; only second AH35/AL2 pre/post measured.",
                "All6010 protected bytes, first slot, required loop registers, PSP:2/IVT0/IVT2/IVT21 checked. No transient or other-memory/code/table/live-return integrity proof.",
                "Original AH35/INT21 twice, ADD/LOOP intact; disclosed same-CS stores/prefix relocation and flags-preserving dispatch. Not unmodified normal execution.",
                "Stops second return005a before its stores and remaining17 queries. No universal service ABI, Pascal parity, allocator success, later lifetime or source acceptance.",
            ],
        )
    if bridge and second:
        result.update(
            status="scoped-second-vector-save-bridge-pass",
            oracle="instrumented_original_second_vector_save_bridge",
            limitations=[
                "One distinct startup context; first two calls establish baseline, only second-return/third-input bridge measured.",
                "All6010 protected bytes checked: four predicted second-slot bytes and other6006 unchanged, including first slot; recorded registers/PSP:2/IVT0/2/21 checked.",
                "Displaced pointer stores/CLD-CSLODSB unchanged, original ADD/LOOP intact; flags-restoring dispatch disclosed. Not an unmodified normal run.",
                "Stops before third MOV AH35/INT21, remaining17 queries unexecuted. No service pre/post, transient/other-memory/code/table/live-return integrity, universal ABI, Pascal parity, allocator lifetime or source acceptance.",
            ],
        )
    if third:
        result.update(
            status="scoped-third-vector-service-observation-pass",
            oracle="instrumented_original_third_ah35_vector1b",
            limitations=[
                "One distinct startup context, first two calls/stores setup; only third AH35/AL1b measured pre/post.",
                "All6010 bytes including both saved slots, loop-required registers, PSP:2/IVT0/2/1b/21 checked; endpoint equality not transient/other-memory/code/table/live-return integrity.",
                "Original AH35/INT21 three times, ADD/LOOP intact; unchanged same-CS displaced prefix/stores and flags-restoring dispatch disclosed. Not an unmodified normal run.",
                "Stops third005a before stores/remaining16 queries. No universal service ABI, Pascal parity, allocator lifetime/success, source acceptance or learning claim.",
            ],
        )
    save(output / "result.json", result)
    return result


def compare_vector_batch(trace: bytes, contract: dict) -> dict:
    """Oracle: finite whole-loop endpoints, not individual service preservation or lifetime."""
    size = SERVICE_WINDOW[1] - SERVICE_WINDOW[0]
    count = len(BATCH_REGISTERS)
    record_bytes = 6 + 4 * count
    if len(trace) != record_bytes + 2 * size:
        raise ValueError("vector batch trace has incorrect length")
    ss, sp, psp = struct.unpack_from("<3H", trace)
    before, after = (
        dict(
            zip(
                BATCH_REGISTERS,
                struct.unpack_from(f"<{count}H", trace, offset),
                strict=True,
            )
        )
        for offset in (6, 6 + 2 * count)
    )
    base = ss - (contract["mz"]["initial_ss"] - contract["load_segment"])
    ds = base + contract["startup"]["relocated_ds"] - contract["load_segment"]
    cs = base + contract["startup"]["relocated_cs"] - contract["load_segment"]
    if (
        list(VECTOR_NUMBERS) != contract["vector_boundary"]["interrupt_numbers"]
        or not 16 <= base <= 65535
        or psp != base - 16
        or sp != contract["mz"]["initial_sp"]
        or before["SS"] != ss
        or before["SP"] != sp - 4
        or before["DS"] != ds
        or before["ES"] != psp
        or before["CX"] != 19
        or before["SI"] != 0x23A
        or before["DI"] != 0x7AF0
        or before["AX"] != before["PSP_END"] & 0xFF00
        or before["FLAGS"] & 0x500
    ):
        raise ValueError("vector batch entry premises differ")
    for reg in ("DS", "SS", "SP", "PSP_END", *BATCH_REGISTERS[13:]):
        if before[reg] != after[reg]:
            raise ValueError(f"vector batch changed required {reg}")
    if (after["CX"], after["SI"], after["DI"]) != (0, 0x24C, 0x7B3C):
        raise ValueError("vector batch loop endpoint differs")
    memory = trace[record_bytes : record_bytes + size]
    final = trace[record_bytes + size :]
    heap = ss + ((sp - 4 + 0x13) >> 4)
    if sp - 4 + 0x13 > 65535 or not heap <= before["PSP_END"] <= 0xA000:
        raise ValueError("vector batch heap bounds differ")
    cells = {
        **{cell: 0 for cell in contract["heap"]["initial_zero_words"]},
        **{cell: heap for cell in contract["heap"]["heap_segment_stores"]},
        0x63F4: before["PSP_END"],
        0x63FE: 0xD6,
        0x6400: cs,
        0x640C: psp,
    }
    for cell, value in cells.items():
        if struct.unpack_from("<H", memory, cell - SERVICE_WINDOW[0])[0] != value:
            raise ValueError(f"vector batch baseline heap cell {cell:04x} differs")
    begin, end = contract["clear"]["ds_range"]
    if memory[begin - SERVICE_WINDOW[0] : end - SERVICE_WINDOW[0]] != bytes(
        end - begin
    ):
        raise ValueError("vector batch initial clear differs")
    if memory[0x6420 - SERVICE_WINDOW[0]] not in (0, 1, 2):
        raise ValueError("vector batch CPU class differs")
    expected = bytearray(memory)
    pointers = []
    for index, number in enumerate(VECTOR_NUMBERS):
        prefix = "VECTOR0" if number == 0 else f"VECTOR{number:02X}"
        pointer = [before[f"{prefix}_OFF"], before[f"{prefix}_SEG"]]
        struct.pack_into(
            "<HH", expected, 0x7AF0 + 4 * index - SERVICE_WINDOW[0], *pointer
        )
        pointers.append({"interrupt": number, "offset_segment": pointer})
    if final != expected:
        raise ValueError("vector batch pointer saves or protected memory differ")
    if [after["BX"], after["ES"]] != pointers[-1]["offset_segment"]:
        raise ValueError("vector batch final pointer differs")
    return {
        "status": "passed",
        "oracle": "instrumented_original_vector_loop_endpoints",
        "queries_checked": 19,
        "saved_pointer_bytes": 76,
        "other_protected_bytes_unchanged": size - 76,
        "before": before,
        "after": after,
        "pointers": pointers,
        "trace_bytes": len(trace),
        "trace_sha256": sha(trace),
        "service_contract_established": False,
        "pascal_parity": False,
        "allocator_entry_state_established": False,
        "source_promoted": False,
    }


def run_vector_batch(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: one frozen full query/save loop, no retries or later startup."""
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "Liero BYOD unavailable"}
    manifest = json.loads((root / "targets/liero/alternate_streams.json").read_text())
    binary, _, base, _ = load_binary_evidence(root / "targets/liero", manifest)
    contract = startup_vector_boundary_contract(binary, load_segment=base)
    output.mkdir(parents=True, exist_ok=False)
    methods = output / "methods"
    methods.mkdir()
    paths = (
        pathlib.Path(__file__),
        root / "tools/liero_startup_clear_contract.py",
        root / "tools/liero_file_probe.py",
        root / "engine/alternate_streams.py",
        root / "engine/instruction_facts.py",
    )
    for path in paths:
        shutil.copy2(path, methods / path.name)
    save(
        output / "freeze.json",
        {
            "contract": contract,
            "method_hashes": {
                str(p.relative_to(root)): sha(p.read_bytes()) for p in paths
            },
            "budget": "one original execution; no retries; subprocess limits30s",
            "scope": "all19 query/save endpoints; stop0064 before installation; not individual service ABI or allocator-entry lifetime",
            "registers": list(BATCH_REGISTERS),
            "protected_ds_range": list(SERVICE_WINDOW),
        },
    )
    try:
        source = output / "instrumentation.S"
        source.write_text(service_instrumentation_source(contract, vector_batch=True))
        boot = APPEND_OFFSET - (contract["startup"]["relocated_cs"] - base) * 16
        for command in (
            ["as", "--32", "-o", str(output / "probe.o"), str(source)],
            [
                "ld",
                "-m",
                "elf_i386",
                "-Ttext",
                hex(boot),
                "-o",
                str(output / "probe.elf"),
                str(output / "probe.o"),
            ],
            [
                "ld",
                "-m",
                "elf_i386",
                "-Ttext",
                hex(boot),
                "--oformat",
                "binary",
                "-o",
                str(output / "payload.bin"),
                str(output / "probe.o"),
            ],
        ):
            completed = subprocess.run(
                command, check=False, capture_output=True, timeout=30
            )
            with (output / "build.log").open("ab") as log:
                log.write(completed.stdout + completed.stderr)
            completed.check_returncode()
        symbols = subprocess.run(
            ["nm", str(output / "probe.elf")],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        ).stdout
        (output / "symbols.txt").write_text(symbols)
        labels = {
            line.split()[-1]: int(line.split()[0], 16) for line in symbols.splitlines()
        }
        image, patches = build_instrumented_mz(
            binary,
            contract,
            (output / "payload.bin").read_bytes(),
            labels["collector"],
            heap=True,
            service_entry=labels["before_service"],
            vector_batch=True,
        )
        (output / "PROBE.COM").write_bytes(image)
        save(output / "patches.json", patches)
        run_dosbox(output)
        result = compare_vector_batch((output / "TRACE.BIN").read_bytes(), contract)
        result["freeze_sha256"] = sha((output / "freeze.json").read_bytes())
        result["artifact_hashes"] = {
            p.name: sha(p.read_bytes()) for p in output.iterdir() if p.is_file()
        }
        save(output / "result.json", result)
        return result
    except (
        OSError,
        ValueError,
        RuntimeError,
        subprocess.SubprocessError,
        KeyError,
    ) as exc:
        save(
            output / "failure.json",
            {"status": "failed", "error": str(exc), "retry_allowed": False},
        )
        raise


def main() -> None:
    """Oracle: fresh-directory bounded experiment with explicit failures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--full-return", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument(
        "--vector-batch",
        action="store_true",
        help="check all19 query/save endpoints once; stop0064",
    )
    parser.add_argument(
        "--heap",
        action="store_true",
        help="observe original heap/PSP state before0049, without Pascal comparison",
    )
    parser.add_argument(
        "--service",
        action="store_true",
        help="snapshot first original AH35/AL0 call, stop005a; implies original-only heap mode",
    )
    parser.add_argument(
        "--bridge",
        action="store_true",
        help="observe pointer-save bridge; combine with --second for second save/third input; implies service mode",
    )
    parser.add_argument(
        "--second",
        action="store_true",
        help="observe second AH35/AL2 call; with --bridge observe its save/third input instead; implies service mode",
    )
    parser.add_argument(
        "--third",
        action="store_true",
        help="observe third AH35/AL1b, stop before its stores; cannot combine with bridge/second",
    )
    args = parser.parse_args()
    if args.full_return:
        if (
            args.vector_batch
            or args.heap
            or args.service
            or args.bridge
            or args.second
            or args.third
        ):
            parser.error("--full-return excludes other startup modes")
        result = (
            replay_startup_return(args.root.resolve(), args.output.resolve())
            if args.replay
            else run_startup_return(args.root.resolve(), args.output.resolve())
        )
        print(json.dumps(result, indent=2))
        return
    if args.replay:
        parser.error("--replay requires --full-return")
    if args.vector_batch:
        if args.heap or args.service or args.bridge or args.second or args.third:
            parser.error("--vector-batch excludes per-call modes")
        print(
            json.dumps(
                run_vector_batch(args.root.resolve(), args.output.resolve()), indent=2
            )
        )
        return
    print(
        json.dumps(
            run_layout_probe(
                args.root.resolve(),
                args.output.resolve(),
                heap=args.heap,
                service=args.service,
                bridge=args.bridge,
                second=args.second,
                third=args.third,
            ),
            indent=2,
        )
    )


def startup_return_source(contract: dict) -> str:
    """Oracle: original entire startup/RETF; restore original saved vectors after snapshot."""
    source = instrumentation_source(contract, SEEDS[0], heap=True)
    source = source.replace(
        "    mov %es:2, %ax\n    mov %ax, %cs:psp_end",
        "    push %es\n    mov %cs:initial_es, %ax\n    mov %ax, %es\n"
        "    mov %es:2, %ax\n    mov %ax, %cs:psp_end\n    pop %es",
    )
    marker = "    push %ds\n    push %cs\n    pop %ds\n    mov $filename"
    restore = """
    mov $0x7af0, %di
    mov $0x239, %si
    mov $19, %cx
restore_vectors:
    cld
    lodsb %cs:(%si), %al
    mov $0x25, %ah
    push %ds
    lds (%di), %dx
    int $0x21
    pop %ds
    add $4, %di
    loop restore_vectors
"""
    if source.count(marker) != 1:
        raise ValueError("startup return collector method differs")
    return source.replace(marker, restore + marker)


def build_startup_return(
    binary: bytes, contract: dict, payload: bytes, collector: int
) -> tuple[bytes, dict]:
    """Oracle: unchanged full original startup; one relocated post-return collector jump."""
    image, _ = build_instrumented_mz(binary, contract, payload, collector, heap=True)
    image = bytearray(image)
    startup = contract["startup"]["file_offset"]
    image[startup + 0x49 : startup + 0x4C] = binary[startup + 0x49 : startup + 0x4C]
    continuation = contract["entry"]["file_offset"] + 5
    entry_segment = contract["mz"]["initial_cs"] - contract["load_segment"]
    segment = contract["startup"]["relocated_cs"] - contract["load_segment"]
    header = contract["mz"]["header_bytes"]
    relocations = _mz_relocation_locations(binary, header)
    if {
        location
        for location in relocations
        if continuation - 1 <= location < continuation + 5
    } != {continuation + 3}:
        raise ValueError(
            "startup return requires the original next far-call segment fixup"
        )
    ip = continuation - header - entry_segment * 16
    if not 0 <= ip <= 0xFFF9:
        raise ValueError("startup return jump segment wraps")
    struct.pack_into("<BHH", image, continuation, 0xEA, collector, segment)
    if image[startup : startup + 0xB1] != binary[startup : startup + 0xB1]:
        raise ValueError("startup return altered original startup")
    changes = [
        {"file_offset": index, "original": before, "instrumented": after}
        for index, (before, after) in enumerate(zip(binary, image))
        if before != after
    ]
    allowed = {
        *range(2, 6),
        *range(10, 14),
        *range(20, 24),
        *range(continuation, continuation + 5),
    }
    if any(change["file_offset"] not in allowed for change in changes):
        raise ValueError("undisclosed startup-return original patch")
    return bytes(image), {
        "original_changes": changes,
        "post_return_jump": continuation,
        "reused_original_MZ_relocation": [ip + 3, entry_segment],
        "original_startup_unchanged": True,
        "original_far_call_and_RETF_unchanged": True,
        "appended_module_offset": APPEND_OFFSET,
        "allocation_bytes_preserved": contract["mz"]["minimum_allocation_bytes"],
        "scope": "instrumented original MZ startup through real return; not unmodified normal game or Pascal parity",
    }


def compare_startup_return(trace: bytes, contract: dict) -> dict:
    """Oracle: startup return stack, loader DS provenance and complete default-object identities."""
    if len(trace) != 8192 + 18:
        raise ValueError("full startup return trace incomplete")
    initial_ss, initial_sp, initial_es, cs, ds, es, ss, sp, psp_end = (
        struct.unpack_from("<9H", trace, 8192)
    )
    actual_load = ds - (contract["startup"]["relocated_ds"] - contract["load_segment"])
    startup_cs = actual_load + (
        contract["startup"]["relocated_cs"] - contract["load_segment"]
    )
    if (
        (ss, sp) != (initial_ss, initial_sp)
        or cs != startup_cs
        or es != ds
        or initial_ss
        != actual_load + contract["mz"]["initial_ss"] - contract["load_segment"]
        or initial_sp != contract["mz"]["initial_sp"]
        or initial_es != actual_load - 16
        or not initial_ss < psp_end <= 0xA000
    ):
        raise ValueError("full startup loader/RETF segment/stack provenance differs")

    def word(offset: int) -> int:
        """Oracle: explicit unnormalized original DS-relative observation."""
        return struct.unpack_from("<H", trace, offset - 0x6000)[0]

    if (
        word(0x640C) != initial_es
        or word(0x6400) != cs
        or word(0x6410) != 0
        or word(0x63F4) != psp_end
    ):
        raise ValueError("full startup PSP/code/sticky globals differ")
    objects = {}
    for offset, mode in ((0x78F0, 0xD7B1), (0x79F0, 0xD7B2)):
        handle, observed_mode, capacity = (word(offset + n) for n in (0, 2, 4))
        buffer_offset, buffer_segment = (word(offset + n) for n in (12, 14))
        if (
            observed_mode != mode
            or capacity != 128
            or word(offset + 8) != 0
            or (buffer_offset, buffer_segment) != (offset + 128, ds)
        ):
            raise ValueError("full startup default object/buffer differs")
        objects[f"{offset:04x}"] = {
            "handle": handle,
            "mode": observed_mode,
            "capacity": capacity,
            "used": word(offset + 8),
            "buffer": [buffer_offset, buffer_segment],
            "flush": [word(offset + 20), word(offset + 22)],
            "optional": [word(offset + 24), word(offset + 26)],
            "close": [word(offset + 28), word(offset + 30)],
        }
    if objects["78f0"]["handle"] != 0 or objects["79f0"]["handle"] != 1:
        raise ValueError("full startup standard handles differ")
    if (
        objects["78f0"]["flush"] != [0x375E, cs]
        or objects["78f0"]["optional"] != [0, 0]
        or any(obj["close"] != [0x37D3, cs] for obj in objects.values())
    ):
        raise ValueError("full startup input/close method provenance differs")
    if objects["79f0"]["flush"] != [0x37B3, cs] or objects["79f0"]["optional"] != [
        0x37B3,
        cs,
    ]:
        raise ValueError("full startup default output methods differ")
    return {
        "status": "passed",
        "original_cases": 1,
        "actual_load_segment": actual_load,
        "data_segment": ds,
        "code_segment": cs,
        "returned_stack": [ss, sp],
        "default_objects": objects,
        "window_bytes_captured": 8192,
        "source_recovered": False,
        "normal_unmodified_game": False,
        "source_promotions": 0,
        "scope": "original MZ startup returned through unchanged00b0 RETF; disclosed collector at main continuation",
        "limitations": [
            "Original-only loader/startup/default objects; no installed Pascal startup parity.",
            "Default handles are this DOSBox console observation, not redirected files/devices.",
            "Game main, file loading, scrolling/error reachability and later object lifetime are not executed.",
        ],
    }


def run_startup_return(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: one frozen original full startup-return observation; bounded, no candidate."""
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "BYOD original unavailable"}
    manifest = json.loads((root / "targets/liero/alternate_streams.json").read_text())
    binary, _, base, _ = load_binary_evidence(root / "targets/liero", manifest)
    contract = startup_vector_boundary_contract(binary, load_segment=base)
    output.mkdir()
    paths = (
        root / "tools/liero_startup_clear_probe.py",
        root / "tools/liero_startup_clear_contract.py",
        root / "tools/liero_file_probe.py",
        root / "engine/alternate_streams.py",
    )
    methods = output / "methods"
    methods.mkdir()
    for path in paths:
        shutil.copy2(path, methods / path.name)
    save(
        output / "freeze.json",
        {
            "contract": contract,
            "sources": {
                str(path.relative_to(root)): sha(path.read_bytes()) for path in paths
            },
            "budget": "one original startup return observation, 30s subprocess limits; no model/holdout/source promotion",
        },
    )
    source = output / "instrumentation.S"
    source.write_text(startup_return_source(contract))
    boot = APPEND_OFFSET - (contract["startup"]["relocated_cs"] - base) * 16
    for command in (
        ["as", "--32", "-o", str(output / "probe.o"), str(source)],
        [
            "ld",
            "-m",
            "elf_i386",
            "-Ttext",
            hex(boot),
            "-o",
            str(output / "probe.elf"),
            str(output / "probe.o"),
        ],
        [
            "ld",
            "-m",
            "elf_i386",
            "-Ttext",
            hex(boot),
            "--oformat",
            "binary",
            "-o",
            str(output / "payload.bin"),
            str(output / "probe.o"),
        ],
    ):
        completed = subprocess.run(
            command, capture_output=True, timeout=30, check=False
        )
        with (output / "build.log").open("ab") as log:
            log.write(completed.stdout + completed.stderr)
        completed.check_returncode()
    symbols = subprocess.run(
        ["nm", str(output / "probe.elf")],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    ).stdout
    (output / "symbols.txt").write_text(symbols)
    labels = {
        line.split()[-1]: int(line.split()[0], 16) for line in symbols.splitlines()
    }
    image, patches = build_startup_return(
        binary, contract, (output / "payload.bin").read_bytes(), labels["collector"]
    )
    (output / "PROBE.COM").write_bytes(image)
    save(output / "patches.json", patches)
    run_dosbox(output)
    result = compare_startup_return((output / "TRACE.BIN").read_bytes(), contract)
    save(output / "result.json", result)
    seal_archive(output)
    return result


def replay_startup_return(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: immutable original-only no-execution replay and complete patch inventory."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    manifest = json.loads((root / "targets/liero/alternate_streams.json").read_text())
    binary, _, base, _ = load_binary_evidence(root / "targets/liero", manifest)
    contract = startup_vector_boundary_contract(binary, load_segment=base)
    if frozen["contract"] != contract:
        raise ValueError("startup return original contract differs")
    for name, identity in frozen["sources"].items():
        if sha(archive["methods/" + pathlib.Path(name).name]) != identity:
            raise ValueError("startup return saved method differs")
    if archive["instrumentation.S"].decode() != startup_return_source(contract):
        raise ValueError("startup return collector source differs")
    labels = {
        line.split()[-1]: int(line.split()[0], 16)
        for line in archive["symbols.txt"].decode().splitlines()
    }
    image, patches = build_startup_return(
        binary, contract, archive["payload.bin"], labels["collector"]
    )
    if archive["PROBE.COM"] != image or json.loads(archive["patches.json"]) != patches:
        raise ValueError("startup return saved image differs")
    result = compare_startup_return(archive["TRACE.BIN"], contract)
    if json.loads(archive["result.json"]) != result:
        raise ValueError("startup return result claims differ")
    return result


if __name__ == "__main__":
    main()
