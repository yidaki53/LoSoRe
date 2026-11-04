"""One exact MZ-loader/startup/492c contract; no generic RET acceptance."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pathlib
import shutil
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.instruction_facts import initialization_prefix


def startup_clear_contract(binary: bytes, *, load_segment: int) -> dict:
    """Oracle: exact DOS-MZ entry/startup/near-clear path under successful loader semantics.

    This scopes one entry path; it does not extend the generic prefix RET gate
    or attest historical Pascal source, interrupts or host ABI equivalence.
    """
    if (
        len(binary) < 28
        or binary[:2] != b"MZ"
        or type(load_segment) is not int
        or not 16 <= load_segment <= 65535
    ):
        raise ValueError(
            "startup contract requires MZ bytes and a valid PSP/load segment"
        )
    words = struct.unpack_from("<14H", binary)
    (
        _,
        last_page,
        pages,
        _,
        header_paragraphs,
        minimum,
        maximum,
        ss,
        sp,
        _,
        ip,
        cs,
        _,
        overlay,
    ) = words
    header = header_paragraphs * 16
    declared = pages * 512 - (512 - last_page if last_page else 0)
    if (
        not pages
        or last_page >= 512
        or declared != len(binary)
        or not 28 <= header < len(binary)
        or overlay
        or maximum < minimum
        or not 8 <= sp <= 65535
    ):
        raise ValueError("unsupported MZ size, overlay, allocation or initial stack")
    image_size = len(binary) - header
    minimum_size = ((image_size + 15) // 16 + minimum) * 16
    if (load_segment << 4) + minimum_size > 0x100000 or load_segment + ss > 65535:
        raise ValueError(
            "loader allocation or stack would wrap the supported address space"
        )
    relocations = _mz_relocation_locations(binary, header)
    ordered_relocations = sorted(relocations)
    if len(relocations) != words[3] or any(
        right - left < 2 for left, right in itertools.pairwise(ordered_relocations)
    ):
        raise ValueError("duplicate or overlapping MZ relocation words")
    entry = header + cs * 16 + ip
    if entry < header or entry + 5 > len(binary) or ip + 5 > 65536:
        raise ValueError("MZ entry lies outside complete file-backed far call")
    call = binary[entry : entry + 5]
    if call[0] != 0x9A or {
        location - entry
        for location in relocations
        if entry - 1 <= location < entry + 5
    } != {3}:
        raise ValueError(
            "first MZ instruction is not an exclusively relocated direct far call"
        )
    startup_ip, startup_cs = struct.unpack_from("<HH", call, 1)
    if startup_ip != 0 or load_segment + startup_cs > 65535:
        raise ValueError("unsupported startup entry offset or relocated CS wrap")
    startup = header + startup_cs * 16
    prefix = binary[startup : startup + 14]
    if (
        len(prefix) != 14
        or prefix[0] != 0xBA
        or prefix[3:7] != bytes.fromhex("8eda8c06")
        or prefix[9:12] != bytes.fromhex("33ede8")
        or {
            location - startup
            for location in relocations
            if startup - 1 <= location < startup + 14
        }
        != {1}
    ):
        raise ValueError("unsupported exact startup DS/store/BP/near-call prefix")
    data_segment = int.from_bytes(prefix[1:3], "little")
    saved_es_offset = int.from_bytes(prefix[7:9], "little")
    if load_segment + data_segment > 65535 or saved_es_offset > 65534:
        raise ValueError("startup data segment/store wraps")
    displacement = int.from_bytes(prefix[12:14], "little", signed=True)
    clear_ip = (14 + displacement) & 65535
    clear = header + startup_cs * 16 + clear_ip
    raw = binary[clear : clear + 18]
    if (
        len(raw) != 18
        or clear_ip + 18 > 65536
        or raw[:1] != b"\xbf"
        or raw[3:6] != bytes.fromhex("1e07b9")
        or raw[8:] != bytes.fromhex("2bcfd1e933c0fcf3abc3")
        or any(clear - 1 <= location < clear + 18 for location in relocations)
    ):
        raise ValueError("unsupported complete near-clear shape or relocated operands")
    begin = int.from_bytes(raw[1:3], "little")
    end = int.from_bytes(raw[6:8], "little")
    if not begin < end or (end - begin) % 2:
        raise ValueError("startup clear requires nonempty even nonwrapping range")
    facts = initialization_prefix(raw, data_window=(begin, end))
    if facts["residue"]["offset"] != 17 or len(facts["writes"]) != 1:
        raise ValueError("startup clear memory facts not established")
    ranges = {
        "entry_code": [entry - header, entry - header + 5],
        "startup_prefix": [startup - header, startup - header + 14],
        "clear_code": [clear - header, clear - header + 18],
        "saved_entry_es": [
            data_segment * 16 + saved_es_offset,
            data_segment * 16 + saved_es_offset + 2,
        ],
        "clear_memory": [data_segment * 16 + begin, data_segment * 16 + end],
        "active_stack": [ss * 16 + sp - 8, ss * 16 + sp],
    }
    if any(not 0 <= start < stop <= minimum_size for start, stop in ranges.values()):
        raise ValueError("code/data/stack lies outside guaranteed MZ allocation")
    for name in ("saved_entry_es", "clear_memory", "active_stack"):
        start, stop = ranges[name]
        for other, (left, right) in ranges.items():
            if other != name and start < right and left < stop:
                raise ValueError(f"startup write/stack aliases {other}")
    return {
        "oracle": "exact_mz_loader_startup_near_clear_contract",
        "status": "scoped-contract-established",
        "binary_sha256": hashlib.sha256(binary).hexdigest(),
        "load_segment": load_segment,
        "mz": {
            "header_bytes": header,
            "image_bytes": image_size,
            "minimum_extra_paragraphs": minimum,
            "minimum_allocation_bytes": minimum_size,
            "initial_cs": load_segment + cs,
            "initial_ip": ip,
            "initial_ss": load_segment + ss,
            "initial_sp": sp,
        },
        "entry": {
            "file_offset": entry,
            "bytes_hex": call.hex(),
            "segment_relocation_file_offset": entry + 3,
        },
        "startup": {
            "file_offset": startup,
            "bytes_hex": prefix.hex(),
            "segment_relocation_file_offset": startup + 1,
            "relocated_cs": load_segment + startup_cs,
            "relocated_ds": load_segment + data_segment,
            "near_call_offset": 11,
            "near_return_ip": 14,
        },
        "clear": {
            "file_offset": clear,
            "bytes_hex": raw.hex(),
            "offset": clear_ip,
            "word_count": (end - begin) // 2,
            "ds_range": [begin, end],
            "supported_prefix": facts,
            "return_opcode": "c3",
            "near_return_contract": "RET pops the original near-call IP; balanced PUSH DS/POP ES; no destination/stack alias.",
        },
        "module_relative_ranges": ranges,
        "stack": {
            "at_startup": sp - 4,
            "at_clear_entry": sp - 6,
            "lowest_during_clear": sp - 8,
            "after_clear": sp - 4,
        },
        "assumptions": [
            "Successful ordinary DOS MZ loading at the stated base, including header relocation and minimum allocation.",
            "Original entry is executed first; loaded code and header are not modified before this path.",
            "Allocated program memory is writable conventional RAM; no asynchronous interrupt/external memory mutation is modeled.",
        ],
        "limitations": [
            "Static loader/path contract, not an observed normal-program run or full TP7/host ABI parity.",
            "Only the first startup near call is covered; later startup calls and return to main remain unresolved.",
            "Generic initialization_prefix still retains C3 residue; no blanket RET acceptance or source promotion.",
        ],
        "routine_recovered": False,
        "model_requests": 0,
        "examples_promoted": 0,
    }


def startup_cpu_contract(binary: bytes, *, load_segment: int) -> dict:
    """Oracle: exact original CPU-leaf paths composed with the existing loader/clear gate."""
    report = startup_clear_contract(binary, load_segment=load_segment)
    startup = report["startup"]["file_offset"]
    if binary[startup + 14 : startup + 17] != bytes.fromhex("e8a000"):
        raise ValueError("unsupported exact startup CPU call")
    offset = 17 + int.from_bytes(
        binary[startup + 15 : startup + 17], "little", signed=True
    )
    leaf = startup + offset
    raw = binary[leaf : leaf + 37]
    if raw != bytes.fromhex(
        "33c09c5b80e70f539d9c5980e5f080fdf0740e4080cff0539d9c5980e5f0740140a22064c3"
    ):
        raise ValueError("unsupported complete CPU leaf")
    header = report["mz"]["header_bytes"]
    relocations = _mz_relocation_locations(binary, header)
    if any(startup + 13 <= r < startup + 17 for r in relocations) or any(
        leaf - 1 <= r < leaf + len(raw) for r in relocations
    ):
        raise ValueError("relocated CPU call or leaf")
    data_segment = report["startup"]["relocated_ds"] - load_segment
    store = int.from_bytes(raw[-3:-1], "little")
    store_range = [data_segment * 16 + store, data_segment * 16 + store + 1]
    code_range = [leaf - header, leaf - header + len(raw)]
    minimum_size = report["mz"]["minimum_allocation_bytes"]
    if not all(
        0 <= start < stop <= minimum_size for start, stop in (store_range, code_range)
    ):
        raise ValueError("CPU code/store exceeds guaranteed MZ allocation")
    for name, (left, right) in {
        **report["module_relative_ranges"],
        "cpu_code": code_range,
    }.items():
        if store_range[0] < right and left < store_range[1]:
            raise ValueError(f"CPU store aliases {name}")
    for name in ("saved_entry_es", "clear_memory", "active_stack"):
        left, right = report["module_relative_ranges"][name]
        if code_range[0] < right and left < code_range[1]:
            raise ValueError(f"CPU code aliases {name}")
    entry_sp = report["stack"]["after_clear"] - 2
    # Every PUSHF/PUSH BX is paired with POP BX/POPF/POP CX before either branch.
    prefix = [0xB1, 0xB3, 0xB4, 0xB5, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBF, 0xC2]
    second = [0xC4, 0xC5, 0xC8, 0xC9, 0xCA, 0xCB, 0xCC, 0xCF]
    suffix = [0xD2, 0xD5]
    report["oracle"] = "exact_mz_loader_startup_cpu_return_projection"
    report["cpu"] = {
        "oracle": "static_complete_original_cpu_leaf_paths",
        "scope": "return-segment-stack-and-write-footprint-not-cpu-family-parity",
        "file_offset": leaf,
        "reviewed_bytes_hex": raw.hex(),
        "offset": offset,
        "near_return_ip": 17,
        "entry_sp": entry_sp,
        "lowest_sp": entry_sp - 2,
        "return_sp": entry_sp + 2,
        "stack_write_module_range": [
            (report["mz"]["initial_ss"] - load_segment) * 16 + entry_sp - 2,
            (report["mz"]["initial_ss"] - load_segment) * 16 + entry_sp,
        ],
        "store_ds_offset": store,
        "store_module_range": store_range,
        "preserved": ["DX", "SI", "DI", "BP", "DS", "ES", "SS"],
        "clobbered": ["AX", "BX", "CX", "status flags"],
        "paths": [
            {
                "condition": "First PUSHF readback high nibble equals Fh",
                "instruction_offsets": prefix + suffix,
                "stored_al": 0,
            },
            {
                "condition": "First readback high nibble differs from Fh; second equals0",
                "instruction_offsets": prefix + second + suffix,
                "stored_al": 1,
            },
            {
                "condition": "First readback high nibble differs from Fh; second differs from0",
                "instruction_offsets": prefix + second + [0xD1] + suffix,
                "stored_al": 2,
            },
        ],
        "assumptions": [
            "Existing successful ordinary MZ loader/clear premises; unchanged original call and leaf.",
            "Ordinary real-mode x86 execution, TF=0, no faults, traps or asynchronous interrupt/external mutation in the scoped path.",
            "Documented PUSHF/POPF, PUSH/POP and near CALL/RET word-stack semantics apply; upper FLAGS readback is left hardware-dependent.",
            "Valid writable disjoint stack and DS store; checked minimum allocation and nonaliasing bounds apply.",
        ],
        "limitations": [
            "All three path effects are reviewed, not CPU-family identification or execution coverage of hardware-dependent branches.",
            "Historical constant2 Pascal body omits observable0/1 paths; not Pascal parity or source recovery.",
            "Later startup calls/interrupts, heap/handler lifetime and actual PSP allocation capacity remain unproved.",
        ],
        "source_recovered": False,
        "original_execution_cases": 0,
    }
    report["limitations"][1] = (
        "Only startup through the CPU leaf return to0011 is covered; later startup calls, interrupts and return to main remain unresolved."
    )
    report["assumptions"].extend(report["cpu"]["assumptions"][1:])
    report["limitations"].extend(report["cpu"]["limitations"])
    return report


def startup_heap_contract(binary: bytes, *, load_segment: int) -> dict:
    """Oracle: exact original heap initialization composed with checked CPU/loader path."""
    report = startup_cpu_contract(binary, load_segment=load_segment)
    start = report["startup"]["file_offset"] + 17
    raw = binary[start : start + 56]
    if raw != bytes.fromhex(
        "8bc4051300b104d3e88cd203c2a3de63a3e0630306d863a3e263a3ec63"
        "a3f063a3f8638e060c6426a10200a3f463c706fe63d6008c0e0064"
    ):
        raise ValueError("unsupported exact startup heap initializer")
    relocations = _mz_relocation_locations(binary, report["mz"]["header_bytes"])
    if any(start - 1 <= r < start + len(raw) for r in relocations):
        raise ValueError("relocated heap initializer")
    relative_ds = report["startup"]["relocated_ds"] - load_segment
    cells = (0x63D8, 0x63EE, 0x63F2, 0x63F6)
    code = [
        start - report["mz"]["header_bytes"],
        start - report["mz"]["header_bytes"] + 56,
    ]
    minimum_size = report["mz"]["minimum_allocation_bytes"]
    heap_stores = (0x63DE, 0x63E0, 0x63E2, 0x63EC, 0x63F0, 0x63F8)
    for cell in (*cells, *heap_stores, 0x63F4, 0x63FE, 0x6400, 0x640C):
        bounds = [relative_ds * 16 + cell, relative_ds * 16 + cell + 2]
        if not 0 <= bounds[0] < bounds[1] <= minimum_size:
            raise ValueError("heap state exceeds guaranteed MZ allocation")
        for name, (left, right) in {
            "heap_code": code,
            "cpu_code": [
                report["cpu"]["file_offset"] - report["mz"]["header_bytes"],
                report["cpu"]["file_offset"] - report["mz"]["header_bytes"] + 37,
            ],
            **{
                key: value
                for key, value in report["module_relative_ranges"].items()
                if key in ("entry_code", "startup_prefix", "clear_code", "active_stack")
            },
        }.items():
            if bounds[0] < right and left < bounds[1]:
                raise ValueError(f"heap state aliases {name}")
    for cell in cells:
        location = report["mz"]["header_bytes"] + relative_ds * 16 + cell
        if binary[location : location + 2] != b"\x00\x00" or any(
            location - 1 <= r < location + 2 for r in relocations
        ):
            raise ValueError("heap initial zero word is changed or relocated")
    report["heap"] = {
        "oracle": "static_exact_original_heap_initialization",
        "file_offset": start,
        "reviewed_bytes_hex": raw.hex(),
        "stop_before_startup_offset": 0x49,
        "initial_zero_words": list(cells),
        "heap_segment_stores": list(heap_stores),
        "default_callback_offset": 0xD6,
        "minimum_guaranteed_spare_heap_bytes": 0,
    }
    report["limitations"].append(
        "Heap initialization requires valid DOS PSP at saved entryES; PSP:2 and later heap/callback lifetime are not established by static bytes."
    )
    return report


def startup_vector_boundary_contract(binary: bytes, *, load_segment: int) -> dict:
    """Oracle: original vector-save prefix; stop before unreviewed external INT21 effects."""
    report = startup_heap_contract(binary, load_segment=load_segment)
    startup = report["startup"]["file_offset"]
    start = startup + 0x49
    raw = binary[start : startup + 0x64]
    if raw != bytes.fromhex("bff07abe3902b9130090fc2eacb435cd21891d8c450283c704e2ef"):
        raise ValueError("unsupported exact startup vector loop")
    table_offset = int.from_bytes(raw[4:6], "little")
    count = int.from_bytes(raw[7:9], "little")
    table = startup + table_offset
    numbers = binary[table : table + count]
    if numbers != bytes.fromhex("00021b2123243435363738393a3b3c3d3e3f75"):
        raise ValueError("unsupported exact startup vector table")
    header = report["mz"]["header_bytes"]
    relocations = _mz_relocation_locations(binary, header)
    if any(start - 1 <= r < start + len(raw) for r in relocations) or any(
        table - 1 <= r < table + count for r in relocations
    ):
        raise ValueError("relocated vector loop or table")
    destination = int.from_bytes(raw[1:3], "little")
    end = destination + count * 4
    if end > 65536 or table_offset + count > 65536:
        raise ValueError("vector table or destination wraps segment")
    data_segment = report["startup"]["relocated_ds"] - load_segment
    data_range = [data_segment * 16 + destination, data_segment * 16 + end]
    sp = report["cpu"]["return_sp"]
    stack_origin = (report["mz"]["initial_ss"] - load_segment) * 16
    interrupt_frame = [stack_origin + sp - 6, stack_origin + sp]
    protected = {
        "startup_code": [startup - header, startup - header + 0x64],
        "cpu_code": [
            report["cpu"]["file_offset"] - header,
            report["cpu"]["file_offset"] - header + 37,
        ],
        "clear_code": report["module_relative_ranges"]["clear_code"],
        "vector_numbers": [table - header, table - header + count],
        "live_return_stack": [stack_origin + sp, stack_origin + sp + 4],
        "heap_and_callback": [data_segment * 16 + 0x63D8, data_segment * 16 + 0x6426],
        "saved_request": [data_segment * 16 + 0x7B3C, data_segment * 16 + 0x7B3E],
    }
    if sp < 6 or any(
        not 0 <= left < right <= report["mz"]["minimum_allocation_bytes"]
        for left, right in (data_range, interrupt_frame, *protected.values())
    ):
        raise ValueError(
            "vector state/code/interrupt frame outside guaranteed allocation"
        )
    for name, (left, right) in protected.items():
        for kind, (begin, end_range) in (
            ("vector-save destination", data_range),
            ("interrupt frame", interrupt_frame),
        ):
            if begin < right and left < end_range:
                raise ValueError(f"{kind} aliases {name}")
    if data_range[0] < interrupt_frame[1] and interrupt_frame[0] < data_range[1]:
        raise ValueError("vector-save destination aliases interrupt frame")
    report["oracle"] = "static_original_startup_first_external_service_boundary"
    report["vector_boundary"] = {
        "oracle": "static_exact_original_vector_loop_and_table",
        "file_offset": start,
        "reviewed_bytes_hex": raw.hex(),
        "table_file_offset": table,
        "table_bytes_hex": numbers.hex(),
        "interrupt_numbers": list(numbers),
        "stop_before_startup_offset": 0x58,
        "service_return_ip": 0x5A,
        "first_service_inputs": {
            "AX": 0x3500 | numbers[0],
            "CX": count,
            "SI": table_offset + 1,
            "DI": destination,
            "DF": 0,
        },
        "ivt_entry_physical_range": [0x21 * 4, 0x21 * 4 + 4],
        "interrupt_frame_module_range": interrupt_frame,
        "conditional_vector_save_ds_range": [destination, end],
        "conditional_vector_save_module_range": data_range,
        "conditional_slot_offsets": [destination + 4 * index for index in range(count)],
        "loop_target_offset": 0x64 + int.from_bytes(raw[-1:], "little", signed=True),
        "conditional_loop_return_offset": 0x64,
        "required_loop_preservation": ["DS", "SI", "DI", "CX", "SS", "SP"],
        "service_reference": "https://fd.lod.bz/rbil/interrup/dos_kernel/2135.html",
        "service_reference_scope": "AH35h/AL interrupt number returns current handler in ES:BX; not proof of actual IVT21 handler, register/stack preservation or side effects.",
        "limitations": [
            "First unresolved external transfer is INT21 at0058, not a direct original allocator call. IVT21 handler bytes and DOS-internal stack/effects are not reviewed.",
            "DOS service result convention is not a service preservation guarantee. Required DS/SI/DI/CX and SS/SP/return behavior remain premises, not proven facts.",
            "Conditional19-iteration footprint requires preserved loop bindings, no mutation of original code/table and no service/external writes to protected heap/PSP/callback cells.",
            "CLD executes before every CS:LODSB; no DF preservation is required across service calls for this loop. Returned ES:BX is stored, not dereferenced or validated as callable.",
            "Real-mode INT pushes FLAGS/CS/IP using six caller-stack bytes; handler additional stack and external effects are unknown.",
            "No new execution, Pascal parity, source recovery, allocator success or later startup lifetime acceptance.",
        ],
        "service_contract_established": False,
        "execution_cases": 0,
        "first_return_bridge": {
            "oracle": "static_exact_original_pointer_save_and_next_input",
            "return_offset": 0x5A,
            "store_bytes_hex": raw[0x5A - 0x49 : 0x5F - 0x49].hex(),
            "add_loop_bytes_hex": raw[0x5F - 0x49 :].hex(),
            "conditional_first_store_ds_range": [destination, destination + 4],
            "next_lodsb_table_file_offset": table + 1,
            "next_service_inputs": {
                "AX": 0x3500 | numbers[1],
                "CX": count - 1,
                "SI": table_offset + 2,
                "DI": destination + 4,
                "DF": 0,
            },
            "premises": "First service returns to005a with checked DS/SS/SP, CX19/SI023a/DI7af0 and returned ES:BX; original code/table intact and writable nonaliasing first slot. MOV stores pointer words without dereference; ADD DI,4 then LOOP decrementsCX and branches0053; CLD/CS:LODSB loads vector2 before MOV AH35.",
            "second_service_contract_established": False,
            "execution_cases": 0,
        },
        "second_return_bridge": {
            "oracle": "static_exact_original_second_pointer_save_and_third_input",
            "return_offset": 0x5A,
            "store_bytes_hex": raw[0x5A - 0x49 : 0x5F - 0x49].hex(),
            "add_loop_bytes_hex": raw[0x5F - 0x49 :].hex(),
            "conditional_second_store_ds_range": [destination + 4, destination + 8],
            "next_lodsb_table_file_offset": table + 2,
            "next_service_inputs": {
                "AX": 0x3500 | numbers[2],
                "CX": count - 2,
                "SI": table_offset + 3,
                "DI": destination + 8,
                "DF": 0,
            },
            "premises": "Second service returns005a with checked DS/SS/SP, CX18/SI023b/DI7af4 and returned ES:BX; first saved slot intact, original code/table intact, second slot writable nonaliasing. MOV stores offset/segment without dereference; ADD DI,4 then LOOP decrementsCX and branches0053. CLD/CS:LODSB loads vector1b; MOV AH35 would establishAX351b. Returned AX and DF need not be preserved by service. This is a conditional static projection, not third service effects.",
            "third_service_contract_established": False,
            "execution_cases": 0,
        },
    }
    report["limitations"][1] = (
        "Original startup prefix reaches the first INT21 at0058 under existing loader/path premises; no external-service return/effects or subsequent original execution are established."
    )
    report["limitations"].extend(report["vector_boundary"]["limitations"])
    return report


def write_startup_clear_contract(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: persistent original-MZ contract bound to current mapping/method identities."""
    manifest_path = root / "targets/liero/alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    binary, header, segment, _ = load_binary_evidence(root / "targets/liero", manifest)
    report = startup_clear_contract(binary, load_segment=segment)
    if report["mz"]["header_bytes"] != header:
        raise ValueError("manifest header disagrees with MZ header")
    sources = (
        manifest_path,
        root / "tools/liero_startup_clear_contract.py",
        root / "engine/instruction_facts.py",
        root / "engine/alternate_streams.py",
    )
    report["evidence_hashes"] = {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sources
    }
    output.mkdir(parents=True, exist_ok=False)
    for path in sources[1:]:
        shutil.copy2(path, output / path.name)
    (output / "result.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    return report


def main() -> None:
    """Oracle: explicit CLI failure; fresh report directory only, no target mutation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    result = write_startup_clear_contract(args.root, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
