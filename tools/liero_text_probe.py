"""Original full text execution versus installed Pascal, with explicit service/ABI limits."""

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
from tools import liero_nibble_caller as nibble
from tools import liero_write_handler_probe as write
from tools.liero_file_probe import assemble_probe, run_dosbox

ROOT = write.ROOT
ENTRIES = {"writer": 0, "crlf": 1, "text": 2}
SERVICES = {"file": 0, "injected": 1, "console": 2, "scroll": 3}
CASE_BYTES, NATIVE_BYTES, HOST_BYTES = 536, 5568, 5544
TEXT_BYTES = bytes.fromhex(
    "c80a01008cd38ec38cdbfc8dbe00ffc57606acaa9130edf3a48edbc686fcfe07c686fbfe0055e8b3ff"
    "8a460c30e48bd08a460a30e46bc05003c2d1e08986f8fe8a460c508a460a500ee87dffc686fffe00"
    "8a8600ff8886f7feb0013a86f7fe7603e993008886fafeeb04fe86fafe8a86fafe30e48bf88a8300ff"
    "8886fefe8a86fffe3c00753880befefe007507c686fffe01eb288a96fefeb800b8508bbef8fe07268815"
    "ff86f8fe8a96fdfeb800b8508bbef8fe07268815ff86f8feeb2c3c017513c686fffe028a86fefe8886fcfe"
    "55e809ffeb153c027511c686fffe008a86fefe8886fbfe55e8f2fe8a86fafe3a86f7fe7403e973ff"
    "8a8600ff30e48bd08a460c30e403c2508a460a500ee8bafebff0791e579a3039dd149af404dd14c9ca0800"
)
SOURCES = (
    "tools/liero_text_probe.py",
    "tools/liero_text_probe.S",
    "tools/liero_file_probe.py",
    "tools/liero_nibble_caller.py",
    "tools/liero_write_handler_probe.py",
    "engine/alternate_streams.py",
    "engine/evidence_archive.py",
    *(
        f"targets/liero/src/{name}"
        for name in (
            "LieroRuntime.pas",
            "FUN_24dd_374d.inc",
            "FUN_24dd_375e.inc",
            "FUN_24dd_37b3.inc",
            "FUN_24dd_396c.inc",
            "FUN_24dd_397a.inc",
            "FUN_24dd_3899.inc",
            "FUN_24dd_3930.inc",
            "FUN_24dd_04f4.inc",
            "FUN_24dd_010f.inc",
            "FUN_24dd_3711.inc",
            "FUN_24dd_0232.inc",
            "FUN_24dd_020a.inc",
            "FUN_24dd_01fe.inc",
            "FUN_24dd_022a.inc",
            "FUN_24dd_021f.inc",
            "FUN_24dd_0218.inc",
            "FUN_24dd_01f0.inc",
            "FUN_249c_0000.inc",
            "FUN_249c_0013.inc",
            "FUN_249c_0037.inc",
        )
    ),
    "targets/liero/tests/probe_liero_text.pas",
)
LEGACY_SOURCES = tuple(
    name
    for name in SOURCES
    if pathlib.Path(name).name
    not in {
        "FUN_24dd_010f.inc",
        "FUN_24dd_3711.inc",
        "FUN_24dd_0232.inc",
        "FUN_24dd_020a.inc",
        "FUN_24dd_01fe.inc",
        "FUN_24dd_022a.inc",
        "FUN_24dd_021f.inc",
        "FUN_24dd_0218.inc",
        "FUN_24dd_01f0.inc",
    }
)


def original(root: pathlib.Path) -> tuple[dict, dict[int, bytes]]:
    """Oracle: original bytes and actual MZ relocations, never decompiler text."""
    target = root / "targets/liero"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    regions = {
        0x37B3: write.RAW,
        0x3899: nibble.BUFFER_WRITE_BYTES,
        0x3930: nibble.WRITE_WORD_BYTES,
        0x396C: write.DISPATCH_RAW["flush"] + write.DISPATCH_RAW["optional"],
        0x04F4: nibble.ERROR_CHECK_BYTES,
    }
    relocations = _mz_relocation_locations(binary, header)
    for offset, raw in regions.items():
        location = header + (0x24DD - base) * 16 + offset
        if binary[location : location + len(raw)] != raw or any(
            location - 1 <= pos < location + len(raw) for pos in relocations
        ):
            raise ValueError("text runtime original bytes/relocations differ")
    start = header + (0x249C - base) * 16
    text = binary[start : start + 0x159]
    if (
        text[:0x13] != nibble.CURSOR_BYTES
        or text[0x13:0x37].hex() != nibble.trial.routine_spec("FUN_249c_0013")["bytes"]
        or text[0x37:] != TEXT_BYTES
        or {pos - start for pos in relocations if start - 1 <= pos < start + len(text)}
        != {0x14E, 0x153}
        or text[0x14E:0x150] != bytes.fromhex("dd14")
        or text[0x153:0x155] != bytes.fromhex("dd14")
    ):
        raise ValueError("complete text original bytes/relocations differ")
    data_start = header + (0x2971 - base) * 16 + 0x6424
    if binary[data_start : data_start + 2] != b"\r\n":
        raise ValueError("original CRLF source differs")
    regions[0x1000] = text
    regions[0x6424] = b"\r\n"
    return {
        "binary_sha256": identity,
        "regions": {f"{offset:04x}": raw.hex() for offset, raw in regions.items()},
        "text_relocations": [0x14E, 0x153],
        "scope": "Complete0037 return path under mode3, valid cursor coordinates and checked37b3. Full4000video+256object/buffer+256input, sticky/calls/exact servicecount sequence/cursor; original frame/DS/SS separately. Not full stack scratch, native ABI, normal startup or010f error behavior.",
        "layout": "CS data/globals, object79f0 with internalbuffer7a70, source8200, SSstackdb00..dff3; textcode(CS+100):0..158; runtime original offsets. Source segment for buffer alternatesCS/CS+100 with equivalent physical7a70.",
        "external": "Real DOS file writes or consolehandle1; injectedCF/AX separately labeled. Original BIOS02/03/BDAmode and B800 textvideo; host logicalcursor/video plus consoleCR/LF-without-scroll projection. Console startsused0; emitted payload and every servicecount captured exactly. Unsupported010f traps and exits99, never returns fabricated success.",
        "whole_routine_accepted": False,
    }, regions


def cases(entry: str, service: str) -> list[bytes]:
    """Oracle: deterministic known-body panel, not model training or held-out recovery."""
    if entry not in ENTRIES or service not in SERVICES:
        raise ValueError("unknown text entry/service")
    if service in ("console", "scroll") and entry != "text":
        raise ValueError("console panel supports complete text entry only")
    rng = random.Random(2026110417 + ENTRIES[entry])
    rows = []

    def add(
        count=2,
        capacity=128,
        used=0,
        sticky=0,
        mode=0xD7B2,
        optional=1,
        payload=None,
        invalid=0,
        carry=0,
        returned=0,
    ):
        """Oracle: explicitly bounded owned fixture and scripted outcome labels."""
        index = len(rows)
        obj = rng.randbytes(256)
        source = bytearray(rng.randbytes(256))
        if payload is not None:
            source[: len(payload) + 1] = bytes([len(payload)]) + payload
        rows.append(
            struct.pack(
                "<12H",
                count,
                index % 20,
                index % 3,
                capacity,
                used,
                sticky,
                mode,
                optional,
                (index % 2) * 0x100,
                carry,
                returned,
                invalid,
            )
            + obj
            + source
        )

    if entry == "writer":
        for capacity in (1, 2, 7, 128):
            for used in (0, capacity - 1, capacity):
                for count in (0, 1, 2, 7, 128, 255):
                    add(count, capacity, used)
        for sticky, mode in ((0x55AA, 0xD7B2), (0, 0xD7B1)):
            add(255, 7, 7, sticky=sticky, mode=mode)
        if service == "file":
            add(255, 7, 6, invalid=1)
        else:
            for carry, returned in ((0, 0), (0, 1), (1, 5), (1, 0xFFFF)):
                add(255, 7, 6, carry=carry, returned=returned)
    elif entry == "crlf":
        for capacity in (1, 2, 7, 128):
            for used in (0, capacity - 1, capacity):
                for optional in (0, 1):
                    add(capacity=capacity, used=used, optional=optional)
        add(sticky=0x55AA)
        add(mode=0xD7B1)
        if service == "file":
            add(capacity=1, invalid=1)
        else:
            add(capacity=1, carry=1, returned=5)
            add(capacity=128, carry=1, returned=0xFFFF)
    else:
        bodies = (
            b"",
            b"A",
            b"Hello, Liero!",
            b"\0",
            b"\0\x0f",
            b"\0\x0f\x04",
            b"A\0\x02\x03B",
            b"\0\xff\xffZ",
            b"A\0\0\0B\0\x08\x0eC",
            b"\0\x01\x02\0\x03\x04Z",
            b"X" * 76,
        )
        for capacity in (1, 2, 7, 128):
            for index, body in enumerate(bodies):
                add(
                    capacity=capacity,
                    used=0 if service == "console" else (index % (capacity + 1)),
                    payload=body,
                )
        if service == "scroll":
            rows = []
            for capacity in (1, 2, 7, 128):
                for row in (23, 24):
                    for body in bodies:
                        add(capacity=capacity, used=0, payload=body)
                        modified = bytearray(rows[-1])
                        struct.pack_into("<H", modified, 2, row)
                        rows[-1] = bytes(modified)
    return rows


def assembly(source: bytes, entry: str, service: str) -> bytes:
    """Oracle: explicit original entry and real/injected service, no modified bodies."""
    return (
        f".set TEXT_ENTRY, {ENTRIES[entry]}\n.set INJECTED, {int(service == 'injected')}\n.set CONSOLE, {int(service in ('console', 'scroll'))}\n".encode()
        + source
    )


def image(harness: bytes, regions: dict[int, bytes]) -> bytes:
    """Oracle: original-offset placement; only actual MZ segment operands relocated at runtime."""
    if not harness or len(harness) + 0x100 > 0x1000:
        raise ValueError("text harness overlaps original text code")
    result = bytearray(0x6500 - 0x100)
    result[: len(harness)] = harness
    for offset, raw in regions.items():
        if any(result[offset - 0x100 : offset - 0x100 + len(raw)]):
            raise ValueError("text harness overlaps original runtime")
        result[offset - 0x100 : offset - 0x100 + len(raw)] = raw
    return bytes(result)


def expected(data: bytes, entry: str, service: str, segment: int, handle: int) -> tuple:
    """Oracle: independent source-level specification, including original error continuation."""
    (
        count,
        row,
        column,
        capacity,
        used,
        sticky,
        mode,
        optional,
        bias,
        carry,
        returned,
        invalid,
    ) = struct.unpack_from("<12H", data)
    obj = bytearray(data[24:280])
    source = data[280:]
    handle = 0xFFFF if invalid else handle
    struct.pack_into("<3H", obj, 0, handle, mode, capacity)
    struct.pack_into("<H", obj, 8, used)
    struct.pack_into("<2H", obj, 12, 0x7A70 - bias * 16, segment + bias)
    struct.pack_into(
        "<4H", obj, 20, 0x37B3, segment, 0x37B3, segment if optional else 0
    )
    video = bytearray(b"\x2e\x4f" * 2000)
    output = bytearray()
    calls = 0
    service_counts = []
    attempted = bytearray()
    cursor = 0
    status = (
        returned
        if service == "injected" and carry
        else 6
        if service == "file" and invalid
        else 0
    )

    def flush():
        """Oracle: leaf reset before service; unsuccessful writes still discard used."""
        nonlocal used, sticky, calls
        service_counts.append(used)
        attempted.extend(obj[128 : 128 + used])
        if service == "file" and not invalid:
            output.extend(obj[128 : 128 + used])
        used = 0
        calls += 1
        if status:
            sticky = status

    if entry == "text":
        state, low, high, position = 0, 7, 0, (row * 80 + column) * 2
        for value in source[1 : source[0] + 1]:
            if state == 0:
                if value == 0:
                    state = 1
                else:
                    video[position : position + 2] = bytes(
                        (value, (high * 16 + low) & 255)
                    )
                    position += 2
            elif state == 1:
                low, state = value, 2
            else:
                high, state = value, 0
        cursor = row * 256 + column + source[0]
    payload = source[:count] if entry == "writer" else b"\r\n"
    zero = sticky == 0
    if not sticky:
        zero = mode == 0xD7B2
        if not zero:
            sticky = 105
        else:
            remaining = payload
            while True:
                chunk = min(capacity - used, len(remaining))
                obj[128 + used : 128 + used + chunk] = remaining[:chunk]
                remaining = remaining[chunk:]
                used += chunk
                if used == capacity:
                    flush()
                if not remaining:
                    break
            zero = True
    if entry != "writer" and zero:
        if optional:
            flush()
            zero = status == 0
        else:
            zero = True
    if entry == "text":
        if sticky:
            raise ValueError("full text panel reached unsupported010f")
        zero = True
        if service in ("console", "scroll"):
            cursor = min(row + 1, 24) * 256
            if row == 24:
                video[:3840] = video[160:4000]
                video[3840:] = b"\x20\x07" * 80
    struct.pack_into("<H", obj, 8, used)
    if len(service_counts) > 256:
        raise ValueError("text service count log exceeds owned fixture")
    log = struct.pack(
        "<256H", *(service_counts + [0xFFFF] * (256 - len(service_counts)))
    )
    if len(attempted) > 512:
        raise ValueError("text service byte log exceeds owned fixture")
    log += bytes(attempted) + b"\xff" * (512 - len(attempted))
    return sticky, calls, cursor, zero, bytes(obj) + source + video + log, bytes(output)


def compare(
    payload: bytes,
    native: bytes,
    host: bytes,
    native_output: bytes,
    host_output: bytes,
    entry: str,
    service: str,
) -> dict:
    """Oracle: original and host independently checked against full declared state/output."""
    panel = cases(entry, service)
    if (
        payload != b"".join(panel)
        or len(native) != len(panel) * NATIVE_BYTES
        or len(host) != len(panel) * HOST_BYTES
    ):
        raise ValueError("text corpus/trace incomplete or changed")
    failures, identities = [], set()
    emitted = bytearray()
    for index, data in enumerate(panel):
        n = native[index * NATIVE_BYTES : (index + 1) * NATIVE_BYTES]
        h = host[index * HOST_BYTES : (index + 1) * HOST_BYTES]
        regs = struct.unpack_from("<16H", n)
        segment = regs[11]
        handle = struct.unpack_from("<H", n, 32)[0]
        if not struct.unpack_from("<H", data, 22)[0]:
            identities.add((segment, handle))
        valid_handle = (
            handle == 1
            if service in ("console", "scroll")
            else handle == 0xFFFF or 4 < handle < 0xFFFF
        )
        if not segment or not valid_handle:
            raise ValueError("text fixture identity invalid")
        sticky, calls, cursor, zero, memory, output = expected(
            data, entry, service, segment, handle
        )
        emitted.extend(output)
        if (
            regs[0] != sticky
            or regs[1] != segment
            or regs[3] != segment
            or regs[4:6] != (0x6789, 0xDFF0)
            or regs[8:10] != (0x1357, 0x2468)
            or regs[10] != calls
            or regs[12] != cursor
            or regs[13] != 3
            or regs[14:] != (0, 0)
            or bool(regs[7] & 0x40) != zero
            or n[32:] != memory
            or h != struct.pack("<4H", sticky, calls, cursor, int(zero)) + memory
        ):
            failures.append(index)
    if len(identities) != 1:
        raise ValueError("text fixture identity changed")
    if native_output != bytes(emitted) or host_output != bytes(emitted):
        raise ValueError("text emitted bytes differ")
    return {
        "status": "failed" if failures else "passed",
        "entry": entry,
        "service": service,
        "cases": len(panel),
        "matches": len(panel) - len(failures),
        "failures": failures,
        "output_bytes": len(emitted),
        "fixture_segment": next(iter(identities))[0],
        "fixture_handle": next(iter(identities))[1],
        "execution_scope": "complete-supported0037-return-path"
        if entry == "text"
        else "buffered-writer-service-projection",
        "service_evidence": "injected-mechanism"
        if service == "injected"
        else "actual-DOS-console-and-BIOS"
        if service in ("console", "scroll")
        else "actual-DOS-file-service",
        "whole_routine_accepted": False,
        "source_promotions": 0,
    }


def run(root: pathlib.Path, output: pathlib.Path, entry: str, service: str) -> dict:
    """Oracle: freeze before execution; sealed full-body original/installed-source observations."""
    checked, regions = original(root)
    sources = {name: (root / name).read_bytes() for name in SOURCES}
    payload = b"".join(cases(entry, service))
    for tool in ("as", "ld", "dosbox", "fpc"):
        if not shutil.which(tool):
            raise FileNotFoundError(f"text probe requires {tool}")
    output.mkdir()
    for name, content in sources.items():
        path = output / "methods" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    frozen = {
        "contract": checked,
        "entry": entry,
        "service": service,
        "methods": {
            name: hashlib.sha256(value).hexdigest() for name, value in sources.items()
        },
        "corpus_sha256": hashlib.sha256(payload).hexdigest(),
        "policy": "Human known-byte recovery, no model selection/holdout/source promotion. Complete supported execution is not all-path/native/program acceptance.",
    }
    (output / "freeze.json").write_text(json.dumps(frozen, indent=2) + "\n")
    (output / "CASES.BIN").write_bytes(payload)
    (output / "harness.S").write_bytes(
        assembly(sources["tools/liero_text_probe.S"], entry, service)
    )
    harness = assemble_probe(output / "harness.S", output)
    (output / "PROBE.COM").write_bytes(image(harness, regions))
    run_dosbox(output)
    native = (output / "TRACE.BIN").read_bytes()
    if len(native) != len(cases(entry, service)) * NATIVE_BYTES:
        raise ValueError(
            "text original trace partial; unsupported error or fixture failure"
        )
    segment = struct.unpack_from("<H", native, 22)[0]
    handle = struct.unpack_from("<H", native, 32)[0]
    candidate = output / "host"
    candidate.mkdir()
    for name, content in sources.items():
        if name.startswith("targets/"):
            (candidate / pathlib.Path(name).name).write_bytes(content)
    (candidate / "CASES.BIN").write_bytes(payload)
    build = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fi.", "-Fu.", "-FU.", "probe_liero_text.pas"],
        cwd=candidate,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (candidate / "compile.log").write_bytes(build.stdout + build.stderr)
    build.check_returncode()
    execution = subprocess.run(
        [
            str(candidate / "probe_liero_text"),
            str(ENTRIES[entry]),
            str(SERVICES[service]),
            str(segment),
            str(handle),
        ],
        cwd=candidate,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (candidate / "execution.log").write_bytes(execution.stdout + execution.stderr)
    execution.check_returncode()
    result = compare(
        payload,
        native,
        (candidate / "PASCAL.BIN").read_bytes(),
        (output / "OUTPUT.BIN").read_bytes(),
        (candidate / "OUTPUT.BIN").read_bytes(),
        entry,
        service,
    )
    if original(root)[0] != checked or any(
        (root / name).read_bytes() != content for name, content in sources.items()
    ):
        raise ValueError("text original/source method changed during execution")
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    seal_archive(output)
    return result


def replay(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: immutable no-execution replay; bind original images and candidate snapshots."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    checked, regions = original(root)
    if frozen["contract"] != checked or set(frozen["methods"]) not in (
        set(SOURCES),
        set(LEGACY_SOURCES),
    ):
        raise ValueError("text original/method contract differs")
    for name, digest in frozen["methods"].items():
        content = archive["methods/" + name]
        if hashlib.sha256(content).hexdigest() != digest:
            raise ValueError("text frozen source hash differs")
        if (
            name.startswith("targets/")
            and archive["host/" + pathlib.Path(name).name] != content
        ):
            raise ValueError("text candidate source differs")
    entry, service = frozen["entry"], frozen["service"]
    if archive["harness.S"] != assembly(
        archive["methods/tools/liero_text_probe.S"], entry, service
    ):
        raise ValueError("text harness method differs")
    if archive["PROBE.COM"] != image(archive["harness.bin"], regions):
        raise ValueError("text original image differs")
    payload = archive["CASES.BIN"]
    if (
        archive["host/CASES.BIN"] != payload
        or hashlib.sha256(payload).hexdigest() != frozen["corpus_sha256"]
    ):
        raise ValueError("text corpus differs")
    result = compare(
        payload,
        archive["TRACE.BIN"],
        archive["host/PASCAL.BIN"],
        archive["OUTPUT.BIN"],
        archive["host/OUTPUT.BIN"],
        entry,
        service,
    )
    if result != json.loads(archive["result.json"]):
        raise ValueError("text saved result differs")
    return result


def main() -> None:
    """Oracle: explicit BYOD gate and bounded full-body run or no-execution replay."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--entry", choices=ENTRIES, default="text")
    parser.add_argument("--service", choices=SERVICES, default="file")
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        print(json.dumps({"status": "skipped", "reason": "BYOD unavailable"}))
        return
    result = (
        replay(ROOT, args.output.resolve())
        if args.replay
        else run(
            ROOT,
            args.output.resolve(),
            args.entry,
            args.service,
        )
    )
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
