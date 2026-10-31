"""Execute hash-bound original Liero file routines in a controlled DOSBox COM harness.

This is original-byte execution, not normal LIERO.EXE startup or Pascal parity.
No recovery ledger or knowledge-store entries are promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import struct
import subprocess
import sys

REPOSITORY = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from engine.object_identity import load_verified_object_identities
from engine.object_setup import load_verified_object_setups

RECORD_SIZE = 532
FIXUP_OFFSETS = (0x3663, 0x4241, 0x425C, 0x4272, 0x4291)
FIXTURES = {
    "two_lines": (b"ALPHA", b"BETA", [(5, 13), (7, 13), (11, 13), (13, 13)]),
    "cr_at_refill_boundary": (
        b"A" * 127,
        b"BETA",
        [(127, 128), (1, 7), (5, 7), (7, 7)],
    ),
}


def _sha256(data: bytes) -> str:
    """Oracle: explicit SHA-256 binding of input and generated runtime artifacts."""
    return hashlib.sha256(data).hexdigest()


def _checked_regions(root: pathlib.Path) -> tuple[dict, list[dict]]:
    """Oracle: existing binary-bound identity/setup validators, not new static claims."""
    target = root / "targets" / "liero"
    load_verified_object_identities(target)
    (setup,) = load_verified_object_setups(target)
    manifest = json.loads((target / "alternate_streams.json").read_text())
    (chain,) = manifest["object_identity_chains"]
    (protocol,) = manifest["object_setup_protocols"]
    mapped_fixups = tuple(
        entry["file_offset"]
        - manifest["image_mapping"]["header_bytes"]
        + 0x10000
        - 0x24DD0
        for entry in setup["relocated_segment_words"]
    )
    if mapped_fixups != FIXUP_OFFSETS:
        raise ValueError("probe loader fixups disagree with checked original code")
    regions = [
        *protocol["regions"].values(),
        *protocol["input_lifecycle_regions"].values(),
        *(
            region
            for name, region in chain["regions"].items()
            # Only these paths execute in the successful-allocation COM fixture.
            if name in ("error_check", "allocation_helper", "reader", "skip")
        ),
        *(
            region
            for name, region in chain["loop_regions"].items()
            if name != "caller_tail"
        ),
    ]
    return manifest, regions


def _build_image(
    harness: bytes, binary: bytes, manifest: dict, regions: list[dict]
) -> bytes:
    """Oracle: only byte-matched original regions; no overwritten harness or code."""
    image = bytearray(0x6500 - 0x100)
    if not harness or len(harness) >= 0x3500:
        raise ValueError("probe harness is empty or overlaps original routines")
    image[: len(harness)] = harness
    occupied = set(range(0x100, 0x100 + len(harness)))
    header = manifest["image_mapping"]["header_bytes"]
    for region in regions:
        address = int(region["address"], 16)
        offset = address - 0x24DD0
        data = bytes.fromhex(region["bytes_hex"])
        file_offset = header + address - 0x10000
        if binary[file_offset : file_offset + len(data)] != data:
            raise ValueError("probe original-code region does not match executable")
        if not 0x100 <= offset < offset + len(data) <= 0x6500:
            raise ValueError("probe code region is outside the reserved image")
        for index, value in enumerate(data):
            position = offset + index
            if position in occupied and image[position - 0x100] != value:
                raise ValueError("probe code regions overlap with different bytes")
            image[position - 0x100] = value
            occupied.add(position)
    return bytes(image)


def decode_trace(data: bytes, *, expected_count: int = 10) -> list[dict]:
    """Oracle: exact requested snapshot count; reject partial or unexpected traces."""
    if len(data) != RECORD_SIZE * expected_count:
        expected = "ten" if expected_count == 10 else str(expected_count)
        raise ValueError(
            f"probe produced {len(data)} bytes; expected {expected} complete snapshots"
        )
    records = []
    for index in range(expected_count):
        record = data[index * RECORD_SIZE : (index + 1) * RECORD_SIZE]
        fields = struct.unpack("<10H", record[:20])
        stage, cs, ds, ss, bp, sp, flags, status, object_offset, destination_offset = (
            fields
        )
        if stage != index + 1:
            raise ValueError("probe snapshot stage ordering disagrees")
        records.append(
            {
                "stage": stage,
                "cs": cs,
                "ds": ds,
                "ss": ss,
                "bp": bp,
                "sp": sp,
                "flags": flags,
                "status": status,
                "object_offset": object_offset,
                "destination_offset": destination_offset,
                "object": record[20:276],
                "destination": record[276:532],
            }
        )
    return records


def _word(data: bytes, offset: int) -> int:
    """Oracle: captured little-endian 16-bit object field."""
    return struct.unpack_from("<H", data, offset)[0]


def validate_trace(data: bytes, fixture: str) -> list[dict]:
    """Oracle: fixed fixture outputs, actual stack handoff and normalized method slots."""
    records = decode_trace(data)
    first, second, consumed = FIXTURES[fixture]
    strings = [b"", b"", first, first, second, second, second, first, first, first]
    positions = [(0, 0), (0, 0), *consumed, (0, 0), *consumed[:2], consumed[1]]
    baseline = records[0]
    snapshots = []
    for index, record in enumerate(records):
        obj = record["object"]
        segment = record["cs"]
        expected_mode = 0xD7B0 if index in {0, 9} else 0xD7B1
        base_sp = (record["bp"] - 0x206) & 0xFFFF
        expected_sp = base_sp - (4 if index in {2, 4, 7} else 0)
        if (
            record["status"] != 0
            or (record["cs"], record["ds"], record["ss"]) != (segment,) * 3
            or record["bp"] != baseline["bp"]
            or record["cs"] != baseline["cs"]
            or record["sp"] != expected_sp
            or record["object_offset"] != record["bp"] - 0x104
            or record["destination_offset"] != record["bp"] - 0x204
        ):
            raise ValueError(
                f"probe register/status/argument-stack mismatch at stage {index + 1}"
            )
        if _word(obj, 2) != expected_mode or _word(obj, 4) != 128:
            raise ValueError(f"probe mode/buffer-size mismatch at stage {index + 1}")
        methods = {
            offset: (_word(obj, offset), _word(obj, offset + 2))
            for offset in (0x10, 0x14, 0x18, 0x1C)
        }
        expected_methods = {
            0x10: (0x420C, segment),
            0x14: (0, 0) if index == 0 else (0x375E, segment),
            0x18: (0, 0),
            0x1C: (0, 0) if index == 0 else (0x37D3, segment),
        }
        if methods != expected_methods:
            raise ValueError(f"probe method slots mismatch at stage {index + 1}")
        if (_word(obj, 12), _word(obj, 14)) != (record["object_offset"] + 128, segment):
            raise ValueError("probe internal-buffer pointer mismatch")
        actual_position = (_word(obj, 8), _word(obj, 10))
        if actual_position != positions[index]:
            raise ValueError(f"probe buffer position mismatch at stage {index + 1}")
        destination = record["destination"]
        string = destination[1 : 1 + destination[0]]
        if string != strings[index]:
            raise ValueError(f"probe string mismatch at stage {index + 1}")
        snapshots.append(
            {
                **{
                    key: value
                    for key, value in record.items()
                    if key not in {"object", "destination"}
                },
                "mode": expected_mode,
                "method_slots": {
                    f"0x{key:x}": list(value) for key, value in methods.items()
                },
                "buffer_position": list(actual_position),
                "string_hex": string.hex(),
            }
        )
    return snapshots


def assemble_probe(assembly: pathlib.Path, output: pathlib.Path) -> bytes:
    """Oracle: GNU 16-bit harness assembly, linked at DOS COM offset 0x100."""
    subprocess.run(
        ["as", "--32", "-o", str(output / "probe.o"), str(assembly)],
        check=True,
        capture_output=True,
        timeout=30,
    )
    subprocess.run(
        [
            "ld",
            "-m",
            "elf_i386",
            "-Ttext",
            "0x100",
            "--oformat",
            "binary",
            "-o",
            str(output / "harness.bin"),
            str(output / "probe.o"),
        ],
        check=True,
        capture_output=True,
        timeout=30,
    )
    return (output / "harness.bin").read_bytes()


def run_dosbox(directory: pathlib.Path) -> list[str]:
    """Oracle: bounded local DOS execution; trace validation is the caller's duty."""
    directory = directory.resolve()
    config = directory / "probe.conf"
    config.write_text(
        "[sdl]\noutput=surface\n[dosbox]\nmemsize=16\n"
        "[mixer]\nnosound=true\n[midi]\nmpu401=none\n"
        "[sblaster]\nsbtype=none\n[gus]\ngus=false\n"
        "[speaker]\npcspeaker=false\ntandy=off\n[cpu]\ncycles=fixed 10000\n"
    )
    command = [
        "dosbox",
        "-conf",
        str(config),
        "-noautoexec",
        "-c",
        "mount c .",
        "-c",
        "c:",
        "-c",
        "probe.com",
        "-c",
        "exit",
    ]
    environment = {**os.environ, "SDL_VIDEODRIVER": "dummy", "SDL_AUDIODRIVER": "dummy"}
    completed = subprocess.run(
        command,
        check=False,
        cwd=directory,
        env=environment,
        capture_output=True,
        timeout=30,
    )
    (directory / "dosbox.log").write_bytes(completed.stdout + completed.stderr)
    completed.check_returncode()
    return command


def run_probe(output: pathlib.Path, root: pathlib.Path = REPOSITORY) -> dict:
    """Oracle: reproducible isolated original-byte execution with real DOS file services."""
    binary_path = root / "extracted" / "liero" / "LIERO.EXE"
    if not binary_path.is_file():
        return {"status": "skipped", "reason": "Liero BYOD executable unavailable"}
    required = ("dosbox", "as", "ld")
    missing = [name for name in required if shutil.which(name) is None]
    if missing:
        raise FileNotFoundError("probe requires installed tools: " + ", ".join(missing))
    manifest, regions = _checked_regions(root)
    binary = binary_path.read_bytes()
    if _sha256(binary) != manifest["binary"]["sha256"]:
        raise ValueError("probe executable changed after evidence validation")
    output.mkdir(parents=True, exist_ok=False)
    assembly = root / "tools" / "liero_file_probe.S"
    harness = assemble_probe(assembly, output)
    image = _build_image(harness, binary, manifest, regions)
    results = {}
    for name, (first, second, _) in FIXTURES.items():
        directory = output / name
        directory.mkdir()
        payload = first + b"\r\n" + second + b"\r\n"
        (directory / "INPUT.TXT").write_bytes(payload)
        (directory / "PROBE.COM").write_bytes(image)
        command = run_dosbox(directory)
        trace = (directory / "TRACE.BIN").read_bytes()
        snapshots = validate_trace(trace, name)
        if (directory / "INPUT.TXT").read_bytes() != payload:
            raise ValueError("read-only probe unexpectedly changed its input fixture")
        results[name] = {
            "input_sha256": _sha256(payload),
            "trace_sha256": _sha256(trace),
            "snapshots": snapshots,
            "emulator_command": command,
        }
    report = {
        "status": "passed",
        "oracle": "isolated_original_bytes_dosbox",
        "binary_sha256": _sha256(binary),
        "harness_source_sha256": _sha256(assembly.read_bytes()),
        "harness_binary_sha256": _sha256(harness),
        "probe_com_sha256": _sha256(image),
        "fixtures": results,
        "limitations": [
            "Original routines execute in a COM harness, not normal LIERO.EXE startup.",
            "CS/DS/SS and object layout are controlled by this harness, not observed in the game.",
            "Only two successful read/reopen/close fixtures; no exhaustive DOS/error-path coverage.",
            "No reconstructed Pascal comparison; no source or original-binary recovery promotion.",
        ],
    }
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main() -> int:
    """Oracle: explicit CLI result, never silent success on a failed or missing trace."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        required=True,
        help="new directory for probe artifacts",
    )
    arguments = parser.parse_args()
    report = run_probe(arguments.output.resolve())
    print(
        json.dumps(
            {key: value for key, value in report.items() if key != "fixtures"}, indent=2
        )
    )
    if report["status"] == "passed":
        print(f"Checked {len(report['fixtures'])} fixtures, ten snapshots each.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
