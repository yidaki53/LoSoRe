"""Scoped original/Pascal parity for input leaves, setup and dispatch.

Original open establishes fixture identity. Host service adapters cover only
the recorded input read/open/close outcomes, not complete DOS emulation.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import struct
import subprocess
import sys

REPOSITORY = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from tools.liero_file_probe import (
    _build_image,
    _checked_regions,
    _sha256,
    _word,
    assemble_probe,
    decode_trace,
    run_dosbox,
)

FUNCTION = "FUN_24dd_375e"
CANDIDATE_RECORD_SIZE = 514
CONTRACT = {
    "function": FUNCTION,
    "oracle": "isolated_original_vs_host_pascal_read_adapter",
    "layout": "file probe CS=DS=SS, object=BP-104h, destination=BP-204h",
    "checks": [
        "Original open/setup seeds all 512 object/destination bytes; no normalization.",
        "Seven valid refill calls, then invalid handle FFFF; RETF 4 restores SP.",
        "Position and available count are dirtied before every refill.",
        "All 512 bytes and returned AX are checked against Pascal and a file contract.",
        "Capacity 0/1/7/128; short/full reads, repeated EOF, unchanged buffer tails.",
    ],
    "limitations": [
        "Finite fixed corpus and nonaliasing layout, not universal equivalence.",
        "Host DOS adapter, not TP7 ABI or complete DOS error semantics.",
        "No open/setup Pascal parity, normal startup, source or training promotion.",
        "Successful read preserves the incoming object handle; no handle masking.",
    ],
}
CLOSE_CONTRACT = {
    "function": "FUN_24dd_37d3",
    "oracle": "isolated_original_vs_host_pascal_close_adapter",
    "layout": CONTRACT["layout"],
    "checks": [
        "Original open/setup seeds object identity; no pointer/handle normalization.",
        "Handles 0..4 return zero without calling the host DOS adapter.",
        "Close the original live handle, close it again, then close FFFF.",
        "Dirty position/count, buffer A5 and destination 5A before the baseline snapshot.",
        "All 512 bytes remain unchanged except the harness-selected handle.",
        "Returned AX, preserved DS/SS and original RETF 4 stack cleanup.",
    ],
    "limitations": [
        "Finite fixed corpus and nonaliasing layout, not universal equivalence.",
        "Host DOS adapter, not TP7 ABI or complete DOS error semantics.",
        "No open/setup Pascal parity, normal startup, source or training promotion.",
        "Adapter call count is host-only instrumentation, not an original DOS trace.",
    ],
}
DISPATCH_CONTRACT = {
    "function": "FUN_24dd_374d",
    "oracle": "isolated_original_vs_host_pascal_dispatch_composition",
    "layout": CONTRACT["layout"],
    "checks": [
        "Original open fixture; slot 18 replaced with a labeled synthetic far callback.",
        "Read, close, repeated close, reserved close, invalid read, three synthetic calls.",
        "Global status starts 55AA; zero returns preserve it; nonzero returns replace it.",
        "Synthetic returns 1234/0/FFFF increment object+6 and clobber ES:DI.",
        "All 512 bytes, returned AX, restored ES:DI, ZF and balanced original near RET.",
    ],
    "limitations": [
        "Finite fixed corpus and nonaliasing layout, not universal equivalence.",
        "Host register mirrors/callback resolver, not original TP7 code generation.",
        "Synthetic callback is not recovered Liero behavior or a setup-method contract.",
        "No open/setup Pascal parity, normal startup, source or training promotion.",
        "Original flags other than ZF and other register clobbers are not compared.",
    ],
}


SETUP_CONTRACT = {
    "function": "FUN_24dd_420c",
    "oracle": "isolated_original_vs_host_pascal_input_setup",
    "layout": CONTRACT["layout"],
    "checks": [
        "Input mode D7B1 only; original open fixture supplies segment and reusable DOS handle.",
        "Existing, missing file, missing directory and empty filename; eight calls each.",
        "Each call starts with BEEF handle, dirty position/count and A5 method slots.",
        "Error clears handle to zero, leaves dirty method slots and returns observed DOSBox 2.",
        "Success installs read/null/close slots; empty name keeps handle zero without DOS open.",
        "Full 512-byte states, returned AX, preserved DS/SS and RETF 4 stack balance.",
    ],
    "limitations": [
        "Input-mode subset, not complete setup routine; output modes abort in Pascal.",
        "Successful host opens use captured fixture handle identity, not DOS allocation parity.",
        "Open-call count is probe instrumentation, not an original interrupt trace.",
        "Host maps missing file/path to observed DOSBox 2, not universal DOS semantics.",
        "Unexpected host I/O errors abort.",
        "No normal startup, universal equivalence, TP7 ABI or source/training promotion.",
    ],
}


OPEN_CONTRACT = {
    "function": "FUN_24dd_36c4",
    "oracle": "isolated_original_vs_host_pascal_input_open_composition",
    "layout": CONTRACT["layout"],
    "checks": [
        "Actual input entry/common open/close wrapper, dispatcher and setup/close leaves.",
        "Reopen, reopen after close error, failed setup, closed-to-open, failed close.",
        "Already-closed close, invalid open mode, empty-name open.",
        "Sticky status, exact mode/handle/position/count/slots, all 512 bytes and RETF 4.",
        "Harness invalidates live handles outside the wrappers to force close error 6.",
    ],
    "limitations": [
        "Input-only composition; output current/requested modes abort in Pascal.",
        "Host pointers resolve objects; logical ES:DI supplied by the bounded caller.",
        "Successful host opens reuse fixture DOS handle; not allocator or TP7 ABI parity.",
        "Missing file maps to observed DOSBox error 2; unexpected host errors abort.",
        "Wrapper register returns are not compared, only global error and memory.",
        "No normal startup, universal equivalence, source or training promotion.",
    ],
}


CALLBACKS_CONTRACT = {
    "function": "FUN_24dd_39ab",
    "oracle": "isolated_original_vs_host_pascal_line_callbacks",
    "layout": CONTRACT["layout"],
    "checks": [
        "Original open/refill supplies nonempty buffer; alternating read/skip callbacks.",
        "Read counts 0/1/7/255; count wrap, CR/1A, LF/NUL and full buffer boundaries.",
        "Exact AX continuation, relative SI/DI, remaining CX and all 512 memory bytes.",
        "Original near RET balances stack; DS/SS preserved; input untouched.",
    ],
    "limitations": [
        "Callbacks only, not string reader, line skip wrapper or refill composition.",
        "DF clear, nonempty contiguous source, offset zero, nonaliasing destination.",
        "Relative offsets are explicitly instrumented, not TP7 ABI or flag parity.",
        "No normal startup, universal equivalence, source or training promotion.",
        "3923 is only a returned continuation token; its next phase is not recovered.",
    ],
}


BUFFER_CONTRACT = {
    "function": "FUN_24dd_37ec",
    "oracle": "isolated_original_vs_host_pascal_buffer_dispatch",
    "layout": CONTRACT["layout"],
    "checks": [
        "Actual 37EC, 396C, 375E, 39AB, 390E and 3923 bodies compose.",
        "Six alternating prefix-read/skip operations, then sticky error and invalid mode.",
        "Full 512 bytes, status, AX callback continuation, SI/DI/CX and ZF.",
        "Read limits 7/111/1; CR at byte127 and LF/non-LF after actual refill.",
        "Empty input, repeated EOF, multi-refill skip, invalid read handle6.",
    ],
    "limitations": [
        "Input read method375E only, bound host buffers and service adapter, not TP7 ABI.",
        "SI/DI are instrumented buffer-relative offsets; other registers/flags not compared.",
        "Object+32..41 are harness-only SI/DI/CX/AX/ZF instrumentation.",
        "Nonaliasing 128-byte buffers, nonwrapping destination, fixed call sequence.",
        "Unknown callback/method or malformed buffer state aborts, never succeeds silently.",
        "Reader/skip wrappers and retained far-object argument remain unproved.",
        "No normal startup, universal equivalence, source or training promotion.",
    ],
}

WRAPPER_CONTRACT = {
    "function": "FUN_24dd_3988",
    "oracle": "isolated_original_vs_host_pascal_reader_skip_wrappers",
    "layout": CONTRACT["layout"],
    "calls_per_fixture": 4,
    "checks": [
        "Actual reader3988 and skip wrapper38F0 compose the buffer dependency group.",
        "Four alternating wrapper calls; read leaves the same logical far object argument for skip.",
        "All512 object/destination bytes and global status after each wrapper.",
        "Logical retained object offset/segment and active lifetime are checked.",
        "Validated optional-method pointer, zero/error return and sticky-error bypass.",
        "Original reader RETF6 and skip RETF4 stack snapshots remain part of the oracle.",
    ],
    "limitations": [
        "Host wrapper APIs use Pointer parameters, not TP7 far-call ABI.",
        "Four-byte retained stack argument is modeled by an explicit host logical stack record.",
        "Optional method callback is synthetic and only validates a bounded resolver.",
        "Input mode, nonaliasing object/destination and the fixed two-line sequence only.",
        "No open/reopen wrapper integration, normal startup, universal equivalence or promotion.",
    ],
}


def handler_contract(handler: str) -> dict:
    """Oracle: explicit selection; unknown handlers never fall back to another oracle."""
    if handler == "read":
        return CONTRACT
    if handler == "close":
        return CLOSE_CONTRACT
    if handler == "dispatch":
        return DISPATCH_CONTRACT
    if handler == "setup":
        return SETUP_CONTRACT
    if handler == "open":
        return OPEN_CONTRACT
    if handler == "callbacks":
        return CALLBACKS_CONTRACT
    if handler == "buffer":
        return BUFFER_CONTRACT
    if handler == "wrappers":
        return WRAPPER_CONTRACT
    raise ValueError(f"unknown file handler: {handler}")


def candidate_name(handler: str) -> str:
    """Oracle: select the corresponding actual Pascal driver, not substitute logic."""
    handler_contract(handler)
    return f"probe_liero_{'setup' if handler == 'open' else handler}_handler"


def harness_source(root: pathlib.Path, handler: str, capacity: int) -> bytes:
    """Oracle: snapshotted common COM harness with exactly one selected leaf branch."""
    handler_contract(handler)
    definitions = (
        f".set {handler.upper()}_HANDLER_PROBE, 1\n.set READ_CAPACITY, {capacity}\n"
    )
    if handler == "close" and capacity == 129:
        definitions += ".set CLOSE_BOUNDARY_PROBE, 1\n"
    if handler == "wrappers":
        definitions += (
            ".set WRAPPER_METHOD_RETURN, 0x1234\n"
            if capacity
            else ".set WRAPPER_METHOD_RETURN, 0\n"
        )
    return definitions.encode() + (root / "tools/liero_file_probe.S").read_bytes()


def fixtures(
    handler: str = "read", suite: str = "all"
) -> dict[str, tuple[int, bytes]]:
    """Oracle: fixed binary payloads around the 128-byte refill boundary."""
    handler_contract(handler)
    if suite == "heldout-v2":
        if handler != "close":
            raise ValueError("heldout-v2 is limited to close")
        return {
            **fixtures(handler, "heldout"),
            "heldout-close-boundaries": (129, b"BOUNDARY\x00\xff"),
        }
    if suite not in ("all", "training", "heldout"):
        raise ValueError(f"unknown file-handler suite: {suite}")
    if suite != "all":
        if handler == "close":
            return (
                fixtures(handler) if suite == "training"
                else {"heldout-close-binary": (128, bytes(range(256)))}
            )
        if handler != "read":
            raise ValueError(f"split suites are unavailable for {handler}")
        heldout = {"length-127", "length-129", "length-257", "capacity-seven"}
        return {
            name: value for name, value in fixtures(handler).items()
            if (name in heldout) == (suite == "heldout")
        }
    if handler == "buffer":
        return {
            "buffer-empty": (0, b""),
            "buffer-short": (0, b"ABC\r\nDEF\r\n"),
            "buffer-cr-boundary": (0, b"A" * 127 + b"\r\nBETA\r\nC\r\n"),
            "buffer-nonlf-boundary": (0, b"A" * 127 + b"\rBETA\r\nC\r\n"),
            "buffer-cr-eof": (0, b"A" * 127 + b"\r"),
            "buffer-long-skip": (0, b"A" * 390 + b"\r\nB\r\n"),
            "buffer-long-read": (0, b"A\r\n" + b"B" * 180 + b"\r\nC\r\n"),
            "buffer-read-boundary": (
                0,
                b"A" * 100 + b"\r\n" + b"B" * 160 + b"\r\nC\r\n",
            ),
            "buffer-control-z": (0, b"ABC\x1aTAIL\r\n"),
            "buffer-lf-nul": (0, b"\x00\n\xffABC\r\nNEXT\n\r\n"),
            "buffer-invalid-read": (1, b"ABC\r\n"),
        }
    if handler == "wrappers":
        return {
            "wrapper-zero": (0, b"A" * 127 + b"\r\nBETA\r\nNEXT\r\nEND"),
            "wrapper-error": (1, b"A" * 127 + b"\r\nBETA\r\nNEXT\r\nEND"),
        }
    if handler == "callbacks":
        return {
            "line-byte": (128, b"A"),
            "line-crlf": (128, b"ABC\r\nNEXT"),
            "line-cr-other": (128, b"ABC\rX"),
            "line-cr-end": (128, b"ABC\r"),
            "line-cr-first": (128, b"\r\n"),
            "line-cr-only": (128, b"\r"),
            "line-cr-at-limit": (128, b"A" * 7 + b"\r\n"),
            "line-size-at-limit": (128, b"A" * 7),
            "line-cr-cr": (128, b"\r\r\n"),
            "line-eof": (128, b"ABC\x1aTAIL"),
            "line-eof-first": (128, b"\x1a"),
            "line-binary": (128, b"\x00\n\xffBINARY"),
            "line-full": (128, b"A" * 128),
            "line-cr-last": (128, b"A" * 127 + b"\r"),
        }
    if handler == "close":
        return {"handle-lifecycle": (128, b"\x00\r\n\xffCLOSE")}
    if handler == "dispatch":
        return {
            "dispatch-empty": (128, b""),
            "dispatch-short": (128, b"\x00\r\n\xffDISPATCH"),
            "dispatch-full": (128, bytes(range(256))),
        }
    if handler == "setup":
        return {
            "setup-existing": (128, b"\x00\r\n\xffSETUP"),
            "setup-empty-name": (0, b"UNCHANGED"),
            "setup-missing-file": (1, b"UNCHANGED"),
            "setup-missing-directory": (2, b"UNCHANGED"),
        }
    if handler == "open":
        return {
            "open-empty": (128, b""),
            "open-short": (128, b"\x00\r\n\xffOPEN"),
            "open-full": (128, bytes(range(256))),
        }
    result = {
        f"length-{length}": (
            128,
            bytes((index * 37 + 13) % 256 for index in range(length)),
        )
        for length in (0, 1, 127, 128, 129, 255, 256, 257, 769)
    }
    result["capacity-zero"] = (0, b"UNCHANGED")
    result["capacity-one"] = (1, b"\x00\r\n\xff")
    result["capacity-seven"] = (7, bytes(range(17)))
    return result


def compare(trace: bytes, candidate: bytes, capacity: int, payload: bytes) -> dict:
    """Oracle: independent refill contract plus complete original/Pascal memory parity."""
    if not 0 <= capacity <= 128:
        raise ValueError("read capacity exceeds the reserved buffer")
    if len(candidate) != 8 * CANDIDATE_RECORD_SIZE:
        raise ValueError("missing, partial or extra Pascal refill records")
    records = checked_records(trace)
    baseline = records[1]
    obj = baseline["object"]
    expected = bytearray(obj + baseline["destination"])
    struct.pack_into("<H", expected, 4, capacity)
    position = 0
    results = []
    for index, record in enumerate(records[2:]):
        invalid = index == 7
        if invalid:
            struct.pack_into("<H", expected, 0, 0xFFFF)
        chunk = b"" if invalid else payload[position : position + capacity]
        position += len(chunk)
        struct.pack_into("<HH", expected, 8, 0, len(chunk))
        expected[128 : 128 + len(chunk)] = chunk
        status = 6 if invalid else 0
        host = candidate[
            index * CANDIDATE_RECORD_SIZE : (index + 1) * CANDIDATE_RECORD_SIZE
        ]
        original = record["object"] + record["destination"]
        differences = [
            offset
            for offset, (wanted, dos, pascal) in enumerate(
                zip(expected, original, host[2:], strict=True)
            )
            if dos != wanted or pascal != wanted
        ]
        passed = (
            not differences and record["status"] == status and _word(host, 0) == status
        )
        results.append(
            {
                "stage": index + 3,
                "status": "passed" if passed else "failed",
                "expected_return": status,
                "original_return": record["status"],
                "pascal_return": _word(host, 0),
                "bytes_read": len(chunk),
                "memory_differences": differences,
            }
        )
    return {
        "status": "passed"
        if all(case["status"] == "passed" for case in results)
        else "failed",
        "calls": results,
    }


def checked_records(
    trace: bytes, *, retained_reader_stages: bool = False
) -> list[dict]:
    """Oracle: shared open state, object layout and operation-specific stack checks."""
    records = decode_trace(trace, expected_count=6 if retained_reader_stages else 10)
    baseline = records[1]
    obj = baseline["object"]
    segment = baseline["cs"]
    if (
        records[0]["status"] != 0
        or baseline["status"] != 0
        or _word(obj, 2) != 0xD7B1
        or _word(obj, 4) != 128
        or _word(obj, 0) <= 4
        or _word(obj, 0) == 0xFFFF
        or (_word(obj, 12), _word(obj, 14))
        != (baseline["object_offset"] + 128, segment)
        or tuple(_word(obj, offset) for offset in (16, 18, 20, 22, 28, 30))
        != (0x420C, segment, 0x375E, segment, 0x37D3, segment)
    ):
        raise ValueError("original input-open preconditions disagree")
    for index, record in enumerate(records):
        expected_sp = 0xFDF4 if retained_reader_stages and index in (2, 4) else 0xFDF8
        if (
            not segment
            or (record["cs"], record["ds"], record["ss"]) != (segment,) * 3
            or record["bp"] != 0xFFFE
            or record["sp"] != expected_sp
            or record["object_offset"] != 0xFEFA
            or record["destination_offset"] != 0xFDFA
        ):
            raise ValueError("file-handler register/layout/RETF 4 contract disagrees")
    return records


def compare_close(trace: bytes, candidate: bytes, *, boundaries: bool = False) -> dict:
    """Oracle: exact no-write close contract, return status and host adapter call count."""
    record_size = 516
    if len(candidate) != 8 * record_size:
        raise ValueError("missing, partial or extra Pascal close records")
    records = checked_records(trace)
    baseline = records[1]
    expected = bytearray(baseline["object"] + baseline["destination"])
    opened_handle = _word(expected, 0)
    results = []
    for index, record in enumerate(records[2:]):
        prefix = (6, 7, 255, 0x8000, 0xFFFE) if boundaries else tuple(range(5))
        if boundaries and opened_handle in prefix:
            raise ValueError("boundary fixture handle collides with the live DOS handle")
        handle = prefix[index] if index < 5 else opened_handle if index < 7 else 0xFFFF
        struct.pack_into("<H", expected, 0, handle)
        status = 6 if boundaries and index < 5 else 0 if index < 6 else 6
        adapter_calls = index + 1 if boundaries else max(0, index - 4)
        host = candidate[index * record_size : (index + 1) * record_size]
        original = record["object"] + record["destination"]
        differences = [
            offset
            for offset, (wanted, dos, pascal) in enumerate(
                zip(expected, original, host[4:], strict=True)
            )
            if dos != wanted or pascal != wanted
        ]
        passed = (
            not differences
            and record["status"] == status
            and _word(host, 0) == status
            and _word(host, 2) == adapter_calls
        )
        results.append(
            {
                "stage": index + 3,
                "status": "passed" if passed else "failed",
                "expected_return": status,
                "original_return": record["status"],
                "pascal_return": _word(host, 0),
                "handle": handle,
                "adapter_calls": _word(host, 2),
                "memory_differences": differences,
            }
        )
    return {
        "status": "passed"
        if all(case["status"] == "passed" for case in results)
        else "failed",
        "calls": results,
    }


def compare_dispatch(trace: bytes, candidate: bytes, payload: bytes) -> dict:
    """Oracle: composed leaf effects, sticky status and synthetic pointer restoration."""
    record_size = 514
    if len(candidate) != 8 * record_size:
        raise ValueError("missing, partial or extra Pascal dispatch records")
    records = checked_records(trace)
    baseline = records[1]
    segment = baseline["cs"]
    expected = bytearray(baseline["object"] + baseline["destination"])
    if (_word(expected, 24), _word(expected, 26)) != (0x400, segment):
        raise ValueError("dispatch synthetic method slot disagrees")
    status = 0x55AA
    results = []
    returns = (0, 0, 6, 0, 6, 0x1234, 0, 0xFFFF)
    for index, record in enumerate(records[2:]):
        returned = returns[index]
        if index == 0:
            chunk = payload[:128]
            struct.pack_into("<HH", expected, 8, 0, len(chunk))
            expected[128 : 128 + len(chunk)] = chunk
        elif index == 3:
            struct.pack_into("<H", expected, 0, 4)
        elif index == 4:
            struct.pack_into("<H", expected, 0, 0xFFFF)
            struct.pack_into("<HH", expected, 8, 0, 0)
        elif index >= 5:
            struct.pack_into("<H", expected, 6, (_word(expected, 6) + 1) & 0xFFFF)
        if returned:
            status = returned
        struct.pack_into(
            "<4H", expected, 256, returned, segment, 0xFEFA, int(returned == 0)
        )
        host = candidate[index * record_size : (index + 1) * record_size]
        original = record["object"] + record["destination"]
        differences = [
            offset
            for offset, (wanted, dos, pascal) in enumerate(
                zip(expected, original, host[2:], strict=True)
            )
            if dos != wanted or pascal != wanted
        ]
        passed = (
            not differences and record["status"] == status and _word(host, 0) == status
        )
        results.append(
            {
                "stage": index + 3,
                "status": "passed" if passed else "failed",
                "method_kind": (
                    "read",
                    "close",
                    "close",
                    "close",
                    "read",
                    "synthetic",
                    "synthetic",
                    "synthetic",
                )[index],
                "expected_return": returned,
                "expected_status": status,
                "original_status": record["status"],
                "pascal_status": _word(host, 0),
                "memory_differences": differences,
            }
        )
    return {
        "status": "passed"
        if all(row["status"] == "passed" for row in results)
        else "failed",
        "calls": results,
    }


def compare_setup(trace: bytes, candidate: bytes, kind: int) -> dict:
    """Oracle: input-only setup writes, preserved error slots and empty-name bypass."""
    names = {128: b"INPUT.TXT", 0: b"", 1: b"MISSING.TXT", 2: b"NO_DIR/INPUT.TXT"}
    if kind not in names:
        raise ValueError("unrecognized setup input fixture")
    record_size = 514
    if len(candidate) != 8 * record_size:
        raise ValueError("missing, partial or extra Pascal setup records")
    records = checked_records(trace)
    baseline = records[1]
    obj = baseline["object"]
    segment = baseline["cs"]
    if obj[48:128] != names[kind] + bytes(80 - len(names[kind])):
        raise ValueError("setup fixture filename disagrees")
    status = {128: 0, 0: 0, 1: 2, 2: 2}[kind]
    results = []
    for index, record in enumerate(records[2:]):
        expected = bytearray(obj + baseline["destination"])
        struct.pack_into("<H", expected, 0, 0)
        struct.pack_into("<HH", expected, 8, 0x55AA, 0xFFFF)
        expected[20:32] = b"\xa5" * 12
        if status == 0:
            handle = 0 if kind == 0 else _word(obj, 0)
            struct.pack_into("<H", expected, 0, handle)
            struct.pack_into(
                "<6H", expected, 20, 0x375E, segment, 0, 0, 0x37D3, segment
            )
        struct.pack_into("<H", expected, 256, 0 if kind == 0 else index + 1)
        original = record["object"] + record["destination"]
        host = candidate[index * record_size : (index + 1) * record_size]
        differences = [
            offset
            for offset, (wanted, dos, pascal) in enumerate(
                zip(expected, original, host[2:], strict=True)
            )
            if dos != wanted or pascal != wanted
        ]
        passed = (
            not differences and record["status"] == status and _word(host, 0) == status
        )
        results.append(
            {
                "stage": index + 3,
                "status": "passed" if passed else "failed",
                "expected_return": status,
                "original_return": record["status"],
                "pascal_return": _word(host, 0),
                "expected_handle": _word(expected, 0),
                "memory_differences": differences,
            }
        )
    return {
        "status": "passed"
        if all(row["status"] == "passed" for row in results)
        else "failed",
        "calls": results,
    }


def compare_open(trace: bytes, candidate: bytes) -> dict:
    """Oracle: independently specified input lifecycle and sticky global-status sequence."""
    record_size = 514
    if len(candidate) != 8 * record_size:
        raise ValueError("missing, partial or extra Pascal open records")
    records = checked_records(trace)
    baseline = records[1]
    obj = baseline["object"]
    expected = bytearray(obj + baseline["destination"])
    handle = _word(obj, 0)
    statuses = (0x55AA, 6, 2, 2, 6, 0x67, 0x66, 0x66)
    modes = (0xD7B1, 0xD7B1, 0xD7B0, 0xD7B1, 0xD7B0, 0xD7B0, 0x1234, 0xD7B1)
    handles = (handle, handle, 0, handle, 0xFFFF, 0xFFFF, 0xFFFF, 0)
    names = (
        b"INPUT.TXT",
        b"INPUT.TXT",
        b"MISSING.TXT",
        b"INPUT.TXT",
        b"INPUT.TXT",
        b"INPUT.TXT",
        b"INPUT.TXT",
        b"",
    )
    results = []
    for index, record in enumerate(records[2:]):
        struct.pack_into("<HH", expected, 0, handles[index], modes[index])
        struct.pack_into(
            "<HH",
            expected,
            8,
            0x55AA if index in (4, 5, 6) else 0,
            0xFFFF if index in (4, 5, 6) else 0,
        )
        expected[48:128] = names[index] + bytes(80 - len(names[index]))
        original = record["object"] + record["destination"]
        host = candidate[index * record_size : (index + 1) * record_size]
        differences = [
            offset
            for offset, (wanted, dos, pascal) in enumerate(
                zip(expected, original, host[2:], strict=True)
            )
            if dos != wanted or pascal != wanted
        ]
        passed = (
            not differences
            and record["status"] == statuses[index]
            and _word(host, 0) == statuses[index]
        )
        results.append(
            {
                "stage": index + 3,
                "status": "passed" if passed else "failed",
                "expected_status": statuses[index],
                "expected_mode": modes[index],
                "original_status": record["status"],
                "pascal_status": _word(host, 0),
                "memory_differences": differences,
            }
        )
    return {
        "status": "passed"
        if all(row["status"] == "passed" for row in results)
        else "failed",
        "calls": results,
    }


def compare_callbacks(trace: bytes, candidate: bytes, payload: bytes) -> dict:
    """Oracle: independent string-prefix/terminator contract, not callback execution."""
    if len(candidate) != 8 * CANDIDATE_RECORD_SIZE:
        raise ValueError("missing, partial or extra Pascal callback records")
    if not 1 <= len(payload) <= 128:
        raise ValueError("callback fixture must be a nonempty single buffer")
    records = checked_records(trace)
    baseline = records[1]
    if (
        _word(baseline["object"], 8) != 0
        or _word(baseline["object"], 10) != len(payload)
        or baseline["object"][128 : 128 + len(payload)] != payload
    ):
        raise ValueError("callback baseline refill disagrees with payload")
    stops = [payload.find(bytes([value])) for value in (13, 26)]
    first_stop = min((value for value in stops if value >= 0), default=len(payload))
    results = []
    for index, record in enumerate(records[2:]):
        limit = (0, 1, 7, 255)[index // 2]
        expected = bytearray(baseline["object"] + b"\xa5" * 256)
        if index % 2 == 0:
            copied = min(first_stop, limit or 65536)
            remaining = (limit - copied) & 0xFFFF
            returned = 0 if first_stop < len(payload) or remaining == 0 else 0x39AB
            consumed = copied
            expected[256 : 256 + copied] = payload[:copied]
        else:
            copied, remaining = 0, limit
            consumed = first_stop
            if first_stop == len(payload):
                returned = 0x390E
            else:
                returned = 0
                if payload[first_stop] == 13:
                    consumed += 1
                    returned = 0x3923
                    if consumed < len(payload):
                        consumed += int(payload[consumed] == 10)
                        returned = 0
        struct.pack_into("<4H", expected, 504, consumed, copied, remaining, returned)
        host = candidate[index * 514 : (index + 1) * 514]
        original = record["object"] + record["destination"]
        differences = [
            offset
            for offset, (wanted, dos, pascal) in enumerate(
                zip(expected, original, host[2:], strict=True)
            )
            if dos != wanted or pascal != wanted
        ]
        passed = (
            not differences
            and record["status"] == returned
            and _word(host, 0) == returned
        )
        results.append(
            {
                "stage": index + 3,
                "callback": "read" if index % 2 == 0 else "skip",
                "status": "passed" if passed else "failed",
                "expected_return": returned,
                "original_return": record["status"],
                "pascal_return": _word(host, 0),
                "consumed": consumed,
                "copied": copied,
                "remaining": remaining,
                "memory_differences": differences,
            }
        )
    return {
        "status": "passed"
        if all(row["status"] == "passed" for row in results)
        else "failed",
        "calls": results,
    }


def compare_buffer(trace: bytes, candidate: bytes, kind: int, payload: bytes) -> dict:
    """Oracle: independent chunk/prefix contract with exact captured register effects."""
    if len(candidate) != 8 * CANDIDATE_RECORD_SIZE:
        raise ValueError("missing, partial or extra Pascal buffer records")
    if kind not in (0, 1):
        raise ValueError("unknown buffer fixture kind")
    records = checked_records(trace)
    baseline = records[1]
    expected = bytearray(baseline["object"] + baseline["destination"])
    if (_word(expected, 8), _word(expected, 10)) != (0, 0):
        raise ValueError("buffer dispatcher must start before first refill")
    file_cursor, status = 0, 0
    results = []
    for index, record in enumerate(records[2:]):
        expected[256:] = b"\xa5" * 256
        token = 0x39AB if index % 2 == 0 else 0x390E
        remaining = (7, 111, 1, 111)[index // 2]
        consumed, copied, zero = 0xBEEF, 0, False
        if kind == 1 and index == 0:
            struct.pack_into("<H", expected, 0, 0xFFFF)
        if index == 6:
            status = 0x55AA
        if index == 7:
            status = 0
            struct.pack_into("<H", expected, 2, 0x1212)
        if status == 0 and _word(expected, 2) != 0xD7B1:
            status = 0x68
        elif status == 0:
            while True:
                consumed, end = _word(expected, 8), _word(expected, 10)
                if consumed != end:
                    window = bytes(expected[128 + consumed : 128 + end])
                    if token == 0x3923:
                        consumed += int(window.startswith(b"\n"))
                        token = 0
                    else:
                        stop = min(
                            (
                                value
                                for value in (window.find(b"\r"), window.find(b"\x1a"))
                                if value >= 0
                            ),
                            default=len(window),
                        )
                        if token == 0x39AB:
                            length = min(stop, remaining)
                            expected[256 + copied : 256 + copied + length] = window[
                                :length
                            ]
                            copied += length
                            remaining -= length
                            consumed += length
                            if remaining == 0 or stop < len(window):
                                token = 0
                        else:
                            consumed += stop
                            if stop < len(window):
                                token = 0
                                if window[stop] == 13:
                                    consumed += 1
                                    if consumed == end:
                                        token = 0x3923
                                    else:
                                        consumed += int(expected[128 + consumed] == 10)
                    struct.pack_into("<H", expected, 8, consumed)
                    zero = token == 0
                    if zero:
                        break
                chunk = payload[file_cursor : file_cursor + 128]
                if _word(expected, 0) == 0xFFFF:
                    chunk, status = b"", 6
                else:
                    file_cursor += len(chunk)
                struct.pack_into("<HH", expected, 8, 0, len(chunk))
                expected[128 : 128 + len(chunk)] = chunk
                consumed = 0
                zero = len(chunk) == 0
                if zero:
                    break
        struct.pack_into(
            "<5H", expected, 32, consumed, copied, remaining, token, int(zero)
        )
        host = candidate[index * 514 : (index + 1) * 514]
        original = record["object"] + record["destination"]
        differences = [
            offset
            for offset, (wanted, dos, pascal) in enumerate(
                zip(expected, original, host[2:], strict=True)
            )
            if dos != wanted or pascal != wanted
        ]
        passed = (
            not differences and record["status"] == status and _word(host, 0) == status
        )
        results.append(
            {
                "stage": index + 3,
                "status": "passed" if passed else "failed",
                "expected_status": status,
                "original_status": record["status"],
                "pascal_status": _word(host, 0),
                "callback_return": token,
                "position": _word(expected, 8),
                "available": _word(expected, 10),
                "memory_differences": differences,
            }
        )
    return {
        "status": "passed"
        if all(row["status"] == "passed" for row in results)
        else "failed",
        "calls": results,
    }


def compare_wrappers(trace: bytes, candidate: bytes) -> dict:
    """Oracle: compare actual wrapper calls and explicit retained-argument lifetime."""
    record_size = 520
    if len(candidate) != 4 * record_size:
        raise ValueError("missing, partial or extra Pascal wrapper records")
    records = checked_records(trace, retained_reader_stages=True)
    baseline = records[1]
    results = []
    for index, record in enumerate(records[2:6]):
        host = candidate[index * record_size : (index + 1) * record_size]
        original = record["object"] + record["destination"]
        differences = [
            offset
            for offset, (dos, pascal) in enumerate(
                zip(original, host[2:514], strict=True)
            )
            if dos != pascal
        ]
        retained = struct.unpack_from("<3H", host, 514)
        expected = [
            baseline["object_offset"],
            baseline["cs"],
            index % 2 == 0,
        ]
        passed = (
            not differences
            and _word(host, 0) == record["status"]
            and retained == tuple(expected)
        )
        results.append(
            {
                "stage": index + 3,
                "wrapper": "reader" if index % 2 == 0 else "skip",
                "status": "passed" if passed else "failed",
                "original_status": record["status"],
                "pascal_status": _word(host, 0),
                "retained_object_offset": retained[0],
                "retained_object_segment": retained[1],
                "retained_active": retained[2],
                "expected_retained": expected,
                "memory_differences": differences,
            }
        )
    return {
        "status": "passed"
        if all(row["status"] == "passed" for row in results)
        else "failed",
        "calls": results,
    }


def compare_handler(
    handler: str, trace: bytes, candidate: bytes, capacity: int, payload: bytes
) -> dict:
    """Oracle: route each selected mode to its own independently checked contract."""
    handler_contract(handler)
    if handler == "read":
        return compare(trace, candidate, capacity, payload)
    if handler == "close":
        return compare_close(trace, candidate, boundaries=capacity == 129)
    if handler == "setup":
        return compare_setup(trace, candidate, capacity)
    if handler == "open":
        return compare_open(trace, candidate)
    if handler == "callbacks":
        return compare_callbacks(trace, candidate, payload)
    if handler == "buffer":
        return compare_buffer(trace, candidate, capacity, payload)
    if handler == "wrappers":
        return compare_wrappers(trace, candidate)
    return compare_dispatch(trace, candidate, payload)


def candidate_sources(root: pathlib.Path, handler: str) -> list[pathlib.Path]:
    """Oracle: all actual candidate/include/runtime dependencies are snapshotted."""
    sources = []
    if handler == "wrappers":
        sources.extend(
            root / "targets/liero/src" / name
            for name in (
                "LieroRuntime.pas",
                "FUN_24dd_374d.inc",
                "FUN_24dd_375e.inc",
                "FUN_24dd_37ec.inc",
                "FUN_24dd_38f0.inc",
                "FUN_24dd_390e.inc",
                "FUN_24dd_3923.inc",
                "FUN_24dd_396c.inc",
                "FUN_24dd_397a.inc",
                "FUN_24dd_3988.inc",
                "FUN_24dd_39ab.inc",
            )
        )
    if handler == "buffer":
        sources.extend(
            root / "targets/liero/src" / name
            for name in (
                "LieroRuntime.pas",
                "FUN_24dd_375e.inc",
                "FUN_24dd_39ab.inc",
                "FUN_24dd_390e.inc",
                "FUN_24dd_3923.inc",
                "FUN_24dd_396c.inc",
            )
        )
    if handler == "callbacks":
        sources.append(root / "targets/liero/src/FUN_24dd_390e.inc")
    if handler in ("dispatch", "open"):
        sources.extend(
            root / path
            for path in (
                "targets/liero/src/LieroRuntime.pas",
                "targets/liero/src/FUN_24dd_37d3.inc",
            )
        )
    if handler == "dispatch":
        sources.append(root / "targets/liero/src/FUN_24dd_375e.inc")
    if handler == "open":
        sources.extend(
            root / path
            for path in (
                "targets/liero/src/FUN_24dd_420c.inc",
                "targets/liero/src/FUN_24dd_374d.inc",
                "targets/liero/src/FUN_24dd_3711.inc",
                "targets/liero/src/FUN_24dd_36b7.inc",
                "targets/liero/src/FUN_24dd_36bc.inc",
                "targets/liero/src/_forward.inc",
            )
        )
    sources.extend(
        (
            root
            / "targets/liero/src"
            / (handler_contract(handler)["function"] + ".inc"),
            root / "targets/liero/tests" / (candidate_name(handler) + ".pas"),
        )
    )
    return sources


def source_paths(root: pathlib.Path, handler: str = "read") -> list[pathlib.Path]:
    """Oracle: bind comparator, original region validators and candidate dependencies."""
    return [
        root / "tools/liero_read_handler_probe.py",
        root / "tools/liero_file_probe.py",
        root / "tools/liero_file_probe.S",
        root / "tools/asmcfg.py",
        root / "targets/liero/alternate_streams.json",
        *(
            root / "engine" / name
            for name in (
                "object_identity.py",
                "object_setup.py",
                "object_lifecycle.py",
                "object_loops.py",
                "alternate_streams.py",
                "callbacks.py",
            )
        ),
        *candidate_sources(root, handler),
        *([root / "targets/liero/src/liero.pas"] if handler == "buffer" else []),
        *([root / "targets/liero/src/liero.pas"] if handler == "wrappers" else []),
    ]


def compile_candidate(directory: pathlib.Path, handler: str = "read") -> pathlib.Path:
    """Oracle: compile the snapshotted candidate, retaining command and compiler errors."""
    executable = directory / candidate_name(handler)
    command = [
        "fpc",
        "-Mtp",
        f"-Fu{directory}",
        f"-Fi{directory}",
        f"-FU{directory}",
        f"-o{executable}",
        str(directory / (candidate_name(handler) + ".pas")),
    ]
    if handler == "open":
        command.insert(1, "-dOPEN_WRAPPER_PROBE")
    result = subprocess.run(command, check=False, capture_output=True, timeout=30)
    (directory / "compile.log").write_bytes(result.stdout + result.stderr)
    (directory / "compile-command.json").write_text(
        json.dumps(command, indent=2) + "\n"
    )
    result.check_returncode()
    return executable


def run_probe(
    output: pathlib.Path, root: pathlib.Path = REPOSITORY, *, handler: str = "read",
    suite: str = "all",
) -> dict:
    """Oracle: fresh DOS service calls against the compiled Pascal leaf; no promotion."""
    contract = handler_contract(handler)
    cases = fixtures(handler, suite)
    root, output = root.resolve(), output.resolve()
    binary_path = root / "extracted/liero/LIERO.EXE"
    if not binary_path.is_file():
        return {"status": "skipped", "reason": "Liero BYOD executable unavailable"}
    tools = {}
    for name in ("as", "ld", "dosbox", "fpc"):
        path = shutil.which(name)
        if path is None:
            raise FileNotFoundError(f"refill probe requires installed tool: {name}")
        tools[name] = path
    manifest, regions = _checked_regions(root)
    binary = binary_path.read_bytes()
    if _sha256(binary) != manifest["binary"]["sha256"]:
        raise ValueError("original executable changed after validation")
    contents = {path: path.read_bytes() for path in source_paths(root, handler)}
    output.mkdir(parents=True, exist_ok=False)
    candidate_dir = output / "candidate"
    candidate_dir.mkdir()
    for source in candidate_sources(root, handler):
        (candidate_dir / source.name).write_bytes(contents[source])
    executable = compile_candidate(candidate_dir, handler)
    results = {}
    for name, (capacity, payload) in cases.items():
        directory = output / name
        directory.mkdir()
        assembly = directory / "harness.S"
        assembly.write_bytes(harness_source(root, handler, capacity))
        harness = assemble_probe(assembly, directory)
        image = _build_image(harness, binary, manifest, regions)
        (directory / "PROBE.COM").write_bytes(image)
        (directory / "INPUT.TXT").write_bytes(payload)
        command = run_dosbox(directory)
        trace = (directory / "TRACE.BIN").read_bytes()
        opened = decode_trace(trace, expected_count=6 if handler == "wrappers" else 10)[
            1
        ]
        (directory / "STATE.BIN").write_bytes(opened["object"] + opened["destination"])
        subprocess.run(
            [
                str(executable),
                str(directory / "STATE.BIN"),
                str(directory / "INPUT.TXT"),
                str(directory / "PASCAL.BIN"),
                str(capacity),
            ],
            check=True,
            capture_output=True,
            timeout=30,
        )
        candidate = (directory / "PASCAL.BIN").read_bytes()
        comparison = compare_handler(handler, trace, candidate, capacity, payload)
        results[name] = {
            **comparison,
            "emulator_command": command,
        }
        if (directory / "INPUT.TXT").read_bytes() != payload:
            raise ValueError("read-only probe changed its input")
    if any(path.read_bytes() != data for path, data in contents.items()):
        raise ValueError("refill source/evidence changed during execution")
    if binary_path.read_bytes() != binary:
        raise ValueError("refill executable changed during execution")
    report = {
        "schema_version": 1,
        "suite": suite,
        "status": "passed"
        if all(row["status"] == "passed" for row in results.values())
        else "failed",
        "contract": contract,
        "binary_sha256": _sha256(binary),
        "source_hashes": {
            str(path.relative_to(root)): _sha256(data)
            for path, data in contents.items()
        },
        "tool_hashes": {
            name: _sha256(pathlib.Path(path).read_bytes())
            for name, path in tools.items()
        },
        "artifact_hashes": {
            str(path.relative_to(output)): _sha256(path.read_bytes())
            for path in sorted(output.rglob("*"))
            if path.is_file()
        },
        "fixtures": results,
        "call_count": contract.get("calls_per_fixture", 8) * len(results),
    }
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def validate_saved_report(
    output: pathlib.Path, root: pathlib.Path = REPOSITORY
) -> dict:
    """Oracle: replay fixed inputs and reject stale/partial saved refill evidence."""
    root, output = root.resolve(), output.resolve()
    report = json.loads((output / "result.json").read_text())
    if report.get("schema_version") != 1 or report.get("contract") not in (
        CONTRACT,
        CLOSE_CONTRACT,
        DISPATCH_CONTRACT,
        SETUP_CONTRACT,
        OPEN_CONTRACT,
        CALLBACKS_CONTRACT,
        BUFFER_CONTRACT,
        WRAPPER_CONTRACT,
    ):
        raise ValueError("unrecognized file-handler contract")
    handler = next(
        name
        for name in (
            "read",
            "close",
            "dispatch",
            "setup",
            "open",
            "callbacks",
            "buffer",
            "wrappers",
        )
        if report["contract"] == handler_contract(name)
    )
    cases = fixtures(handler, report.get("suite", "all"))
    current = {
        str(path.relative_to(root)): _sha256(path.read_bytes())
        for path in source_paths(root, handler)
    }
    if report.get("source_hashes") != current:
        raise ValueError("stale refill source/evidence")
    binary = (root / "extracted/liero/LIERO.EXE").read_bytes()
    if report.get("binary_sha256") != _sha256(binary):
        raise ValueError("stale refill original executable")
    artifacts = report.get("artifact_hashes")
    if not isinstance(artifacts, dict) or not artifacts:
        raise ValueError("missing refill artifact bindings")
    present = {
        str(path.relative_to(output))
        for path in output.rglob("*")
        if path.is_file() and path != output / "result.json"
    }
    required = {
        f"candidate/{candidate_name(handler)}",
        f"candidate/{candidate_name(handler)}.pas",
        f"candidate/{handler_contract(handler)['function']}.inc",
        *(f"candidate/{source.name}" for source in candidate_sources(root, handler)),
        "candidate/compile-command.json",
        *(
            f"{name}/{filename}"
            for name in cases
            for filename in (
                "INPUT.TXT",
                "STATE.BIN",
                "TRACE.BIN",
                "PASCAL.BIN",
                "PROBE.COM",
                "harness.S",
                "harness.bin",
                "probe.conf",
            )
        ),
    }
    if set(artifacts) != present or not required <= present:
        raise ValueError("missing refill artifact bindings")
    for relative, digest in artifacts.items():
        if _sha256((output / relative).read_bytes()) != digest:
            raise ValueError(f"stale refill artifact: {relative}")
    for source in candidate_sources(root, handler):
        if (output / "candidate" / source.name).read_bytes() != source.read_bytes():
            raise ValueError("refill candidate snapshot disagrees with source")
    manifest, regions = _checked_regions(root)
    rows = report.get("fixtures")
    if not isinstance(rows, dict) or set(rows) != set(cases):
        raise ValueError("refill fixture corpus disagrees")
    for name, (capacity, payload) in cases.items():
        directory = output / name
        trace = (directory / "TRACE.BIN").read_bytes()
        opened = decode_trace(trace, expected_count=6 if handler == "wrappers" else 10)[
            1
        ]
        assembly = harness_source(root, handler, capacity)
        if (
            (directory / "INPUT.TXT").read_bytes() != payload
            or (directory / "STATE.BIN").read_bytes()
            != opened["object"] + opened["destination"]
            or (directory / "harness.S").read_bytes() != assembly
            or (directory / "PROBE.COM").read_bytes()
            != _build_image(
                (directory / "harness.bin").read_bytes(), binary, manifest, regions
            )
        ):
            raise ValueError("saved refill input/image disagrees")
        candidate = (directory / "PASCAL.BIN").read_bytes()
        replay = compare_handler(handler, trace, candidate, capacity, payload)
        if not isinstance(rows[name], dict) or any(
            rows[name].get(key) != value for key, value in replay.items()
        ):
            raise ValueError("stored refill comparison disagrees with replay")
    status = (
        "passed"
        if all(row["status"] == "passed" for row in rows.values())
        else "failed"
    )
    expected_calls = report["contract"].get("calls_per_fixture", 8) * len(rows)
    if report.get("status") != status or report.get("call_count") != expected_calls:
        raise ValueError("stored refill summary disagrees with replay")
    return report


def main() -> int:
    """Oracle: standalone scoped execution, explicit skip/failure and persistent report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    parser.add_argument(
        "--handler",
        choices=(
            "read",
            "close",
            "dispatch",
            "setup",
            "open",
            "callbacks",
            "buffer",
            "wrappers",
        ),
        default="read",
    )
    parser.add_argument(
        "--suite", choices=("all", "training", "heldout", "heldout-v2"), default="all",
    )
    args = parser.parse_args()
    if args.suite != "all" and args.handler not in ("read", "close"):
        parser.error("split suites are limited to read and close")
    if args.suite == "heldout-v2" and args.handler != "close":
        parser.error("heldout-v2 is limited to close")
    result = run_probe(args.output, handler=args.handler, suite=args.suite)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"passed", "skipped"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
