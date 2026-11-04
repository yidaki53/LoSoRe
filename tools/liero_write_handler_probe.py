"""Original37B3 DOS-write boundary versus installed Pascal; no native/source promotion."""

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
from tools.liero_file_probe import assemble_probe, run_dosbox

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = bytes.fromhex("8bdc1e36c47f0426c5550c33c926874d08268b1db440cd21720233c01fca0400")
CASE_BYTES = 4104
NATIVE_BYTES = 4140
HOST_BYTES = 4108
MODES = {"file": 0, "nul": 1, "invalid": 2, "injected": 3}
DISPATCHES = {"leaf": 0, "flush": 1, "optional": 2}
DISPATCH_RAW = {
    "flush": bytes.fromhex("065326ff5f140bc07403a31064c3"),
    "optional": bytes.fromhex("065326ff5f180bc07403a31064c3"),
}
SOURCES = (
    "tools/liero_write_handler_probe.py",
    "tools/liero_write_handler_probe.S",
    "tools/liero_file_probe.py",
    "engine/alternate_streams.py",
    "engine/evidence_archive.py",
    "targets/liero/src/FUN_24dd_37b3.inc",
    "targets/liero/src/FUN_24dd_374d.inc",
    "targets/liero/src/FUN_24dd_375e.inc",
    "targets/liero/src/FUN_24dd_396c.inc",
    "targets/liero/src/FUN_24dd_397a.inc",
    "targets/liero/src/LieroRuntime.pas",
    "targets/liero/tests/probe_liero_write_handler.pas",
)


def contract(root: pathlib.Path, dispatch: str = "leaf") -> dict:
    """Oracle: original complete alternate-entry bytes and actual relocation absence."""
    target = root / "targets/liero"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    start = header + (0x24DD - base) * 16 + 0x37B3
    if binary[start : start + len(RAW)] != RAW or any(
        start - 1 <= pos < start + len(RAW)
        for pos in _mz_relocation_locations(binary, header)
    ):
        raise ValueError("37b3 original bytes/relocations differ")
    checked = {
        "function": "FUN_24dd_37b3",
        "binary_sha256": identity,
        "file_offset": start,
        "bytes": RAW.hex(),
        "relocations": [],
        "service": "ES:DI object; LDS DX fromfarbuffer+12; CX=used+8 viaXCHGzero; BX=handle; DOS21/AH40; CFclear=>AX0 else preserveerror; POPDS/RETF4",
        "bounds": "Object8000..80ff, physicalsourceCS:8100..817f, ownedarena8000..8fff; SSstackefe8..eff3 disjoint. EntryDS=SS=CS; serviceDS=CS orCS+100 withoffset8100 or7100. Count0..128.",
        "scope": "Full4096arena, serviceinputs/resetorder, AXstatus and emittedfilebytes. OriginalDS/SS/SP/BP/guards separately checked, not host/native ABI parity.",
        "unknown": [
            "Other external DOS register/flag/deviceeffects",
            "Normal-program reachability/native TP7 types and ABI",
            "Redirected378e shortwrite contract and caller/error composition",
        ],
        "injection": "INT21 shim onlyforAH40, fixed returnedCF/AX; no actual shortwrite/error claim for those cases. All other DOSservices chained; vector restored before tracewrite.",
        "whole_routine_accepted": False,
    }
    if dispatch not in DISPATCHES:
        raise ValueError("unknown write dispatch")
    if dispatch != "leaf":
        entry = 0x396C if dispatch == "flush" else 0x397A
        location = header + (0x24DD - base) * 16 + entry
        raw = DISPATCH_RAW[dispatch]
        if binary[location : location + len(raw)] != raw or any(
            location - 1 <= pos < location + len(raw)
            for pos in _mz_relocation_locations(binary, header)
        ):
            raise ValueError("output dispatch original bytes/relocations differ")
        checked["dispatch"] = {
            "entry": entry,
            "file_offset": location,
            "bytes": raw.hex(),
            "relocations": [],
            "semantics": "PUSH ES/BX argument; farcall exactslot20/24 to original37b3; ORAX setsZF; nonzero storesDS6410; nearRET. No BX restore.",
            "bindings": "Fixture code offset explicitly resolves original37b3. Host slot is logical37b3; snapshot restores fixture encoding only after checked invocation. Not pointer-bit/native ABI parity.",
            "scope": "Full leaf comparison plus stickyDS6410, originalZF/BX/DI, balanced nearRET; sourceDS alternates. DOS preservesBX/DI/ES in this scoped service panel; other external clobbers unknown.",
        }
    return checked


def cases(mode: str) -> list[bytes]:
    """Oracle: frozen owned-memory panel; scripted outcomes are mechanism tests only."""
    if mode not in MODES:
        raise ValueError("unknown write mode")
    rng = random.Random(2026110411 + MODES[mode])
    result = []
    for count in (0, 1, 2, 7, 31, 64, 127, 128):
        outcomes = (
            ((0, count), (0, count // 2), (1, 5), (1, 0xFFFF))
            if mode == "injected"
            else ((0, 0),)
        )
        for carry, returned in outcomes:
            arena = bytearray(rng.randbytes(4096))
            struct.pack_into("<H", arena, 8, count)
            result.append(
                struct.pack("<4H", count, carry, returned, (len(result) % 2) * 0x100)
                + arena
            )
    return result


def assembly(source: bytes, mode: str, dispatch: str = "leaf") -> bytes:
    """Oracle: checked original byte inclusion with explicit real/injected service mode."""
    if mode not in MODES:
        raise ValueError("unknown write mode")
    if dispatch not in DISPATCHES:
        raise ValueError("unknown write dispatch")
    prefix = f".set WRITE_MODE, {MODES[mode]}\n"
    if dispatch != "leaf":
        prefix += f".set DISPATCH_KIND, {DISPATCHES[dispatch]}\n"
    return prefix.encode() + source


def compare(
    mode: str,
    inputs: bytes,
    native: bytes,
    host: bytes,
    native_output: bytes,
    host_output: bytes,
    dispatch: str = "leaf",
    method_offset: int = 0,
) -> dict:
    """Oracle: independent expected arena/status/serviceinputs and actual emitted bytes."""
    count = len(cases(mode))
    if dispatch not in DISPATCHES:
        raise ValueError("unknown write dispatch")
    record_bytes = NATIVE_BYTES + (2 if dispatch != "leaf" else 0)
    if dispatch != "leaf" and not 0x100 <= method_offset < 0x6000:
        raise ValueError("write dispatch method binding missing")
    if (
        inputs != b"".join(cases(mode))
        or len(native) != count * record_bytes
        or len(host) != count * HOST_BYTES
    ):
        raise ValueError("write corpus/trace incomplete or changed")
    failures = []
    expected_output = bytearray()
    identities = set()
    for index in range(count):
        data = inputs[index * CASE_BYTES : (index + 1) * CASE_BYTES]
        requested, carry, returned, segment_bias = struct.unpack_from("<4H", data)
        row = native[index * record_bytes : (index + 1) * record_bytes]
        regs = struct.unpack_from("<16H", row)
        calls_seen, handle, service_count, offset, segment, used = struct.unpack_from(
            "<6H", row, 4128
        )
        status = (
            6 if mode == "invalid" else returned if mode == "injected" and carry else 0
        )
        object_segment = regs[15]
        identities.add((handle, object_segment))
        arena = bytearray(data[8:])
        struct.pack_into("<H", arena, 0, handle)
        struct.pack_into("<H", arena, 8, 0)
        source_offset = 0x8100 - (segment_bias << 4)
        struct.pack_into("<2H", arena, 12, source_offset, segment)
        sticky = 0
        if dispatch != "leaf":
            sticky = status if status else 0x55AA if segment_bias else 0
            struct.pack_into(
                "<4H",
                arena,
                20,
                method_offset,
                object_segment,
                method_offset,
                object_segment,
            )
        candidate = host[index * HOST_BYTES : (index + 1) * HOST_BYTES]
        expected_host = (
            struct.pack("<6H", status, 1, handle, requested, 0, sticky) + arena
        )
        valid_handle = (
            handle == 0xFFFF if mode in ("invalid", "injected") else 4 < handle < 0xFFFF
        )
        if (
            not valid_handle
            or not segment
            or regs[0] != status
            or regs[6:10]
            != (
                0x6789,
                0xEFE8 if dispatch == "leaf" else 0xEFEE,
                0xEFF0,
                object_segment,
            )
            or regs[10:12] != (object_segment, object_segment)
            or regs[13:16] != (0x1357, 0x2468, object_segment)
            or segment != object_segment + segment_bias
            or (calls_seen, service_count, offset, used)
            != (1, requested, source_offset, 0)
            or row[32:4128] != arena
            or candidate != expected_host
            or (
                dispatch != "leaf"
                and (
                    struct.unpack_from("<H", row, 4140)[0] != sticky
                    or bool(regs[12] & 0x40) != (status == 0)
                    or regs[1] != handle
                    or regs[5] != 0x8000
                )
            )
        ):
            failures.append(index)
        if mode == "file":
            expected_output.extend(data[8 + 256 : 8 + 256 + requested])
    if len(identities) != 1:
        raise ValueError("write fixture handle/segment binding changed")
    if native_output != bytes(expected_output) or host_output != bytes(expected_output):
        raise ValueError("write emitted bytes differ")
    return {
        "status": "failed" if failures else "passed",
        "cases": count,
        "matches": count - len(failures),
        "failures": failures,
        "fixture_handle": next(iter(identities))[0],
        "fixture_segment": next(iter(identities))[1],
        "output_bytes": len(expected_output),
        "oracle": "injected-service-mechanism"
        if mode == "injected"
        else "actual-DOS-service/host-projection",
    }


def run(root: pathlib.Path, output: pathlib.Path, dispatch: str = "leaf") -> dict:
    """Oracle: frozen complete leaf, real DOS outputs and separately labeled injected outcomes."""
    checked = contract(root, dispatch)
    missing = [name for name in ("as", "ld", "fpc", "dosbox") if not shutil.which(name)]
    if missing:
        raise FileNotFoundError("write probe requires: " + ", ".join(missing))
    sources = {name: (root / name).read_bytes() for name in SOURCES}
    output.mkdir()
    methods = output / "methods"
    for name, content in sources.items():
        path = methods / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    freeze = {
        "dispatch": dispatch,
        "contract": checked,
        "methods": {
            name: hashlib.sha256(value).hexdigest() for name, value in sources.items()
        },
        "corpora": {
            mode: hashlib.sha256(b"".join(cases(mode))).hexdigest() for mode in MODES
        },
        "policy": "No model generation/selection/holdout; finite reviewed known-byte leaf. Actual DOS and injected mechanism results separate; no source/training promotion.",
    }
    (output / "freeze.json").write_text(json.dumps(freeze, indent=2) + "\n")
    rows = {}
    for mode, mode_value in MODES.items():
        directory = output / mode
        directory.mkdir()
        payload = b"".join(cases(mode))
        (directory / "CASES.BIN").write_bytes(payload)
        source = assembly(sources["tools/liero_write_handler_probe.S"], mode, dispatch)
        (directory / "harness.S").write_bytes(source)
        image = assemble_probe(directory / "harness.S", directory)
        if (
            image.count(RAW) != 1
            or len(image) + 0x100 >= 0x6000
            or (dispatch != "leaf" and image.count(DISPATCH_RAW[dispatch]) != 1)
        ):
            raise ValueError(
                "write harness original bytes missing or code/data overlap"
            )
        (directory / "PROBE.COM").write_bytes(image)
        run_dosbox(directory)
        native = (directory / "TRACE.BIN").read_bytes()
        if len(native) != (NATIVE_BYTES + (2 if dispatch != "leaf" else 0)) * len(
            cases(mode)
        ):
            raise ValueError("write original trace partial")
        _, handle, _, _, segment, _ = struct.unpack_from("<6H", native, 4128)
        candidate = directory / "host"
        candidate.mkdir()
        for name in SOURCES:
            if not name.startswith("targets/liero/"):
                continue
            (candidate / pathlib.Path(name).name).write_bytes(sources[name])
        (candidate / "CASES.BIN").write_bytes(payload)
        build = subprocess.run(
            [
                "fpc",
                "-Mtp",
                "-Cr",
                "-Fu.",
                "-Fi.",
                "-FU.",
                "probe_liero_write_handler.pas",
            ],
            cwd=candidate,
            capture_output=True,
            check=False,
            timeout=30,
        )
        (candidate / "compile.log").write_bytes(build.stdout + build.stderr)
        build.check_returncode()
        execution = subprocess.run(
            [
                str(candidate / "probe_liero_write_handler"),
                str(mode_value),
                str(handle),
                str(segment),
                str(DISPATCHES[dispatch]),
                str(image.index(RAW) + 0x100),
            ],
            cwd=candidate,
            capture_output=True,
            check=False,
            timeout=30,
        )
        (candidate / "execution.log").write_bytes(execution.stdout + execution.stderr)
        execution.check_returncode()
        rows[mode] = compare(
            mode,
            payload,
            native,
            (candidate / "PASCAL.BIN").read_bytes(),
            (directory / "OUTPUT.BIN").read_bytes() if mode == "file" else b"",
            (candidate / "OUTPUT.BIN").read_bytes() if mode == "file" else b"",
            dispatch,
            image.index(RAW) + 0x100,
        )
    if any((root / name).read_bytes() != content for name, content in sources.items()):
        raise ValueError("write source/method changed during execution")
    if contract(root, dispatch) != checked:
        raise ValueError("write original executable changed during execution")
    result = {
        "status": "passed"
        if all(row["status"] == "passed" for row in rows.values())
        else "failed",
        "modes": rows,
        "whole_routine_accepted": False,
        "model_requests": 0,
        "source_promotions": 0,
    }
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    seal_archive(output)
    return result


def replay(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: immutable archived bytes, recheck scoped comparisons without executing services."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    dispatch = frozen.get("dispatch", "leaf")
    if frozen["contract"] != contract(root, dispatch):
        raise ValueError("write original contract changed")
    for name, digest in frozen["methods"].items():
        if (
            name not in SOURCES
            or hashlib.sha256(archive["methods/" + name]).hexdigest() != digest
        ):
            raise ValueError("write frozen method differs")
    expected_sources = set(SOURCES)
    if "dispatch" not in frozen:
        expected_sources -= {
            "targets/liero/src/FUN_24dd_374d.inc",
            "targets/liero/src/FUN_24dd_375e.inc",
            "targets/liero/src/FUN_24dd_396c.inc",
            "targets/liero/src/FUN_24dd_397a.inc",
            "targets/liero/src/LieroRuntime.pas",
        }
    if set(frozen["methods"]) != expected_sources:
        raise ValueError("write method snapshot missing")
    result = json.loads(archive["result.json"])
    rows = {}
    for mode in MODES:
        for name in frozen["methods"]:
            if not name.startswith("targets/liero/"):
                continue
            if (
                archive[f"{mode}/host/{pathlib.Path(name).name}"]
                != archive["methods/" + name]
            ):
                raise ValueError("write candidate source snapshot differs")
        if archive[f"{mode}/harness.S"] != assembly(
            archive["methods/tools/liero_write_handler_probe.S"], mode, dispatch
        ):
            raise ValueError("write assembly method differs")
        image = archive[f"{mode}/PROBE.COM"]
        if (
            image != archive[f"{mode}/harness.bin"]
            or image.count(RAW) != 1
            or len(image) + 0x100 >= 0x6000
            or (dispatch != "leaf" and image.count(DISPATCH_RAW[dispatch]) != 1)
        ):
            raise ValueError("write original image differs")
        payload = archive[f"{mode}/CASES.BIN"]
        if hashlib.sha256(payload).hexdigest() != frozen["corpora"][mode]:
            raise ValueError("write corpus hash differs")
        if archive[f"{mode}/host/CASES.BIN"] != payload:
            raise ValueError("write host corpus differs")
        rows[mode] = compare(
            mode,
            payload,
            archive[f"{mode}/TRACE.BIN"],
            archive[f"{mode}/host/PASCAL.BIN"],
            archive[f"{mode}/OUTPUT.BIN"] if mode == "file" else b"",
            archive[f"{mode}/host/OUTPUT.BIN"] if mode == "file" else b"",
            dispatch,
            image.index(RAW) + 0x100,
        )
    expected = {
        "status": "passed"
        if all(row["status"] == "passed" for row in rows.values())
        else "failed",
        "modes": rows,
        "whole_routine_accepted": False,
        "model_requests": 0,
        "source_promotions": 0,
    }
    if result != expected:
        raise ValueError("write saved result differs from replay")
    return result


def main() -> None:
    """Oracle: fresh scoped write experiment or no-execution replay; BYOD absence skips."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--dispatch", choices=DISPATCHES, default="leaf")
    args = parser.parse_args()
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        print(json.dumps({"status": "skipped", "reason": "BYOD unavailable"}))
        return
    result = (
        replay(ROOT, args.output.resolve())
        if args.replay
        else run(ROOT, args.output.resolve(), args.dispatch)
    )
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
