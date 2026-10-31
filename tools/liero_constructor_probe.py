"""Compare original FUN_24dd_3639 execution with its actual Pascal reconstruction.

The oracle is scoped to the recorded input corpus and nonaliasing COM layout.
It does not attest historical source, normal startup or full TP7 ABI equivalence.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass

REPOSITORY = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from tools.liero_file_probe import (
    _build_image,
    _checked_regions,
    _sha256,
    assemble_probe,
    run_dosbox,
)

FUNCTION = "FUN_24dd_3639"
CASE_SIZE = 544
TRACE_SIZE = 564
OBJECT_OFFSET = 0x6910
CONTRACT = {
    "version": 1,
    "function": FUNCTION,
    "oracle": "isolated_original_vs_host_pascal",
    "input": "256-byte short-string storage plus 16/256/16-byte guarded object",
    "layout": {"name_offset": 0x6800, "object_offset": OBJECT_OFFSET},
    "preconditions": [
        "CS=DS=SS, SP=FFFE; object and input are disjoint, valid and nonwrapping.",
        "Constructor code segment immediate is relocated to actual COM CS.",
        "Host RegisterES is original CS and RegisterDI is original object offset.",
    ],
    "comparison": [
        "All 544 bytes, including unchanged name, guards and object tail.",
        "Only method segment at object+18 is mapped between CS and logical 24DD.",
        "Original DS/SS preserved and RETF 8 restores SP for every case.",
    ],
    "limitations": [
        "Finite corpus, fixed nonaliasing layout, not universal equivalence.",
        "Host FPC checks Pascal memory effects, not original TP7 code generation.",
        "Original-only register/ABI observations do not verify host ABI parity.",
        "No ledger, source attestation or training-example promotion.",
    ],
}


@dataclass(frozen=True)
class ConstructorCase:
    name: str
    data: bytes


def constructor_cases(suite: str = "all") -> list[ConstructorCase]:
    """Oracle: fixed lengths 0..255, dirty states, embedded NUL and prior fixtures."""
    names = bytes(65 + index % 26 for index in range(255))
    cases = []
    for seed, arena in (
        ("zero", bytes(288)),
        ("ones", b"\xff" * 288),
        ("pattern", bytes((index * 37 + 19) % 256 for index in range(288))),
    ):
        for length in range(256):
            cases.append(
                ConstructorCase(
                    f"{seed}-length-{length}", bytes([length]) + names + arena
                )
            )
    for fixture in ("two_lines", "cr_at_refill_boundary"):
        cases.append(
            ConstructorCase(fixture, b"\x09INPUT.TXT" + bytes(246) + bytes(288))
        )
    for position in (0, 1, 2, 77, 78, 79, 80, 254):
        source = bytearray(b"\xff" + names)
        source[position + 1] = 0
        cases.append(
            ConstructorCase(f"nul-at-{position}", bytes(source) + b"\xa5" * 288)
        )
    if suite == "all":
        return cases
    if suite == "training":
        return [case for case in cases if not case.name.startswith(("pattern-", "nul-"))]
    if suite == "heldout":
        return [case for case in cases if case.name.startswith(("pattern-", "nul-"))]
    raise ValueError(f"unknown constructor suite: {suite}")


def expected_case(data: bytes, segment: int) -> bytes:
    """Oracle: constructor write contract; unchanged bytes remain independently checked."""
    if len(data) != CASE_SIZE or not 0 < segment <= 0xFFFF:
        raise ValueError("invalid constructor input size or segment")
    result = bytearray(data)
    obj = 256 + 16
    struct.pack_into(
        "<10H",
        result,
        obj,
        0,
        0xD7B0,
        128,
        0,
        0,
        0,
        OBJECT_OFFSET + 128,
        segment,
        0x420C,
        0x24DD,
    )
    result[obj + 20 : obj + 48] = bytes(28)
    name = data[1 : 1 + min(data[0], 79)].split(b"\0", 1)[0]
    result[obj + 48 : obj + 49 + len(name)] = name + b"\0"
    return bytes(result)


def decode_original(trace: bytes, count: int) -> tuple[int, list[bytes]]:
    """Oracle: exact ordered snapshots, relocated constructor and observed RETF 8."""
    if count < 1 or len(trace) != count * TRACE_SIZE:
        raise ValueError("constructor trace missing, partial or has extra records")
    results = []
    segment = None
    for index in range(count):
        record = trace[index * TRACE_SIZE : (index + 1) * TRACE_SIZE]
        stage, cs, ds, ss, before, after, es, di, obj, name = struct.unpack(
            "<10H", record[:20]
        )
        if (
            stage != index
            or cs == 0
            or cs != ds
            or cs != ss
            or cs != es
            or before != after
            or before != 0xFFFE
            or obj != OBJECT_OFFSET
            or name != 0x6800
            or not OBJECT_OFFSET + 49 <= di <= OBJECT_OFFSET + 128
            or (segment is not None and cs != segment)
        ):
            raise ValueError(f"constructor ABI/identity mismatch at case {index}")
        segment = cs
        data = bytearray(record[20:])
        if struct.unpack_from("<H", data, 256 + 16 + 18)[0] != cs:
            raise ValueError(
                f"constructor relocated method segment mismatch at case {index}"
            )
        struct.pack_into("<H", data, 256 + 16 + 18, 0x24DD)
        results.append(bytes(data))
    if segment is None:
        raise ValueError("constructor trace has no segment")
    return segment, results


def compare_cases(cases: list[ConstructorCase], trace: bytes, candidate: bytes) -> dict:
    """Oracle: three-way original/candidate/write-contract match, no broad masking."""
    segment, original = decode_original(trace, len(cases))
    if len(candidate) != CASE_SIZE * len(cases):
        raise ValueError("Pascal output missing, partial or has extra records")
    rows = []
    for index, case in enumerate(cases):
        actual = candidate[index * CASE_SIZE : (index + 1) * CASE_SIZE]
        expected = expected_case(case.data, segment)
        differences = [
            {
                "offset": offset,
                "original": left,
                "pascal": right,
                "contract": expected[offset],
            }
            for offset, (left, right) in enumerate(zip(original[index], actual))
            if left != right or left != expected[offset]
        ]
        rows.append(
            {
                "case": case.name,
                "status": "failed" if differences else "passed",
                "differences": differences,
            }
        )
    return {
        "status": "passed"
        if all(row["status"] == "passed" for row in rows)
        else "failed",
        "segment": segment,
        "cases": rows,
    }


def _compile_candidate(output: pathlib.Path) -> pathlib.Path:
    """Oracle: compile the snapshotted actual source and runtime, never substitute logic."""
    executable = output / "probe_liero_constructor"
    command = [
        "fpc",
        "-Mtp",
        f"-Fu{output}",
        f"-Fi{output}",
        f"-FU{output}",
        f"-o{executable}",
        str(output / "probe_liero_constructor.pas"),
    ]
    completed = subprocess.run(command, capture_output=True, check=False, timeout=30)
    (output / "compile.log").write_bytes(completed.stdout + completed.stderr)
    (output / "compile-command.json").write_text(json.dumps(command, indent=2) + "\n")
    completed.check_returncode()
    return executable


def source_paths(root: pathlib.Path) -> list[pathlib.Path]:
    """Oracle: explicit source and evidence dependencies of this scoped comparator."""
    return [
        root / "tools/liero_constructor_probe.S",
        root / "tools/liero_constructor_probe.py",
        root / "tools/liero_file_probe.py",
        root / "tools/asmcfg.py",
        root / "targets/liero/alternate_streams.json",
        root / "targets/liero/asm" / f"{FUNCTION}.s",
        *(
            root / "engine" / name
            for name in (
                "object_identity.py",
                "object_setup.py",
                "object_loops.py",
                "object_lifecycle.py",
                "alternate_streams.py",
                "callbacks.py",
                "scoped_verification.py",
                "fact_graph.py",
            )
        ),
        root / "targets/liero/src" / f"{FUNCTION}.inc",
        root / "targets/liero/src/LieroRuntime.pas",
        root / "targets/liero/tests/probe_liero_constructor.pas",
    ]


def run_probe(
    output: pathlib.Path, root: pathlib.Path = REPOSITORY, *, suite: str = "all"
) -> dict:
    """Oracle: fresh hash-bound original/Pascal execution, never automatic promotion."""
    cases = constructor_cases(suite)
    root, output = root.resolve(), output.resolve()
    binary_path = root / "extracted/liero/LIERO.EXE"
    if not binary_path.is_file():
        return {"status": "skipped", "reason": "Liero BYOD executable unavailable"}
    missing = [
        tool for tool in ("as", "ld", "dosbox", "fpc") if shutil.which(tool) is None
    ]
    if missing:
        raise FileNotFoundError("constructor probe requires: " + ", ".join(missing))
    manifest, regions = _checked_regions(root)
    binary = binary_path.read_bytes()
    if _sha256(binary) != manifest["binary"]["sha256"]:
        raise ValueError("constructor binary changed after validation")
    sources = source_paths(root)
    contents = {path: path.read_bytes() for path in sources}
    fingerprints = {
        str(path.relative_to(root)): _sha256(contents[path]) for path in sources
    }
    output.mkdir(parents=True, exist_ok=False)
    candidate_dir = output / "candidate"
    candidate_dir.mkdir()
    for source in sources[-3:]:
        (candidate_dir / source.name).write_bytes(contents[source])
    assembly = output / "harness.S"
    assembly.write_bytes(contents[sources[0]])
    harness = assemble_probe(assembly, output)
    image = _build_image(harness, binary, manifest, regions)
    (output / "PROBE.COM").write_bytes(image)
    payload = b"".join(case.data for case in cases)
    (output / "CASES.BIN").write_bytes(payload)
    command = run_dosbox(output)
    trace = (output / "TRACE.BIN").read_bytes()
    segment, _ = decode_original(trace, len(cases))
    executable = _compile_candidate(candidate_dir)
    subprocess.run(
        [
            str(executable),
            str(output / "CASES.BIN"),
            str(output / "PASCAL.BIN"),
            str(segment),
        ],
        check=True,
        capture_output=True,
        timeout=30,
    )
    candidate = (output / "PASCAL.BIN").read_bytes()
    report = compare_cases(cases, trace, candidate)
    if (output / "CASES.BIN").read_bytes() != payload:
        raise ValueError("constructor probe changed its input corpus")
    if any(
        _sha256(path.read_bytes()) != fingerprints[str(path.relative_to(root))]
        for path in sources
    ):
        raise ValueError("constructor probe source/evidence changed during execution")
    if _sha256(binary_path.read_bytes()) != _sha256(binary):
        raise ValueError("constructor original executable changed during execution")
    report.update(
        {
            "schema_version": 1,
            "suite": suite,
            "function": FUNCTION,
            "oracle": CONTRACT["oracle"],
            "contract": CONTRACT,
            "contract_sha256": _sha256(json.dumps(CONTRACT, sort_keys=True).encode()),
            "binary_sha256": _sha256(binary),
            "source_hashes": fingerprints,
            "artifact_hashes": {
                "CASES.BIN": _sha256(payload),
                "TRACE.BIN": _sha256(trace),
                "PASCAL.BIN": _sha256(candidate),
                "PROBE.COM": _sha256(image),
                "harness.bin": _sha256(harness),
                "candidate/probe_liero_constructor": _sha256(executable.read_bytes()),
                "candidate/FUN_24dd_3639.inc": fingerprints[
                    "targets/liero/src/FUN_24dd_3639.inc"
                ],
                "candidate/LieroRuntime.pas": fingerprints[
                    "targets/liero/src/LieroRuntime.pas"
                ],
                "candidate/probe_liero_constructor.pas": fingerprints[
                    "targets/liero/tests/probe_liero_constructor.pas"
                ],
                "harness.S": _sha256(assembly.read_bytes()),
                "probe.conf": _sha256((output / "probe.conf").read_bytes()),
                "candidate/compile-command.json": _sha256(
                    (candidate_dir / "compile-command.json").read_bytes()
                ),
            },
            "tool_hashes": {
                tool: _sha256(pathlib.Path(shutil.which(tool)).read_bytes())
                for tool in ("as", "ld", "dosbox", "fpc")
            },
            "emulator_command": command,
            "case_count": len(cases),
        }
    )
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def validate_saved_report(
    output: pathlib.Path, root: pathlib.Path = REPOSITORY
) -> dict:
    """Oracle: recheck current inputs and recompute results; stored status is not proof."""
    report = json.loads((output / "result.json").read_text())
    if (
        report.get("schema_version") != 1
        or report.get("function") != FUNCTION
        or report.get("oracle") != CONTRACT["oracle"]
        or report.get("contract") != CONTRACT
        or report.get("contract_sha256")
        != _sha256(json.dumps(CONTRACT, sort_keys=True).encode())
    ):
        raise ValueError("unrecognized constructor differential contract")
    current = {
        str(path.relative_to(root)): _sha256(path.read_bytes())
        for path in source_paths(root)
    }
    if report.get("source_hashes") != current:
        raise ValueError("stale constructor source/evidence")
    binary = (root / "extracted/liero/LIERO.EXE").read_bytes()
    if report.get("binary_sha256") != _sha256(binary):
        raise ValueError("stale constructor original executable")
    required = {
        "CASES.BIN",
        "TRACE.BIN",
        "PASCAL.BIN",
        "PROBE.COM",
        "harness.bin",
        "candidate/probe_liero_constructor",
        "candidate/FUN_24dd_3639.inc",
        "candidate/LieroRuntime.pas",
        "candidate/probe_liero_constructor.pas",
        "harness.S",
        "probe.conf",
        "candidate/compile-command.json",
    }
    hashes = report.get("artifact_hashes")
    if not isinstance(hashes, dict) or set(hashes) != required:
        raise ValueError("missing constructor artifact bindings")
    for relative in required:
        if _sha256((output / relative).read_bytes()) != hashes[relative]:
            raise ValueError(f"stale constructor artifact: {relative}")
    cases = constructor_cases(report.get("suite", "all"))
    if (output / "CASES.BIN").read_bytes() != b"".join(
        case.data for case in cases
    ) or report.get("case_count") != len(cases):
        raise ValueError("constructor corpus changed")
    manifest, regions = _checked_regions(root)
    if (
        _build_image((output / "harness.bin").read_bytes(), binary, manifest, regions)
        != (output / "PROBE.COM").read_bytes()
    ):
        raise ValueError("constructor COM no longer matches bound original regions")
    result = compare_cases(
        cases, (output / "TRACE.BIN").read_bytes(), (output / "PASCAL.BIN").read_bytes()
    )
    if any(report.get(key) != value for key, value in result.items()):
        raise ValueError("stored constructor status disagrees with replayed comparison")
    return report


def main() -> int:
    """Oracle: nonzero CLI status on any recorded differential mismatch."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    report = run_probe(args.output)
    print(
        json.dumps(
            {key: value for key, value in report.items() if key != "cases"}, indent=2
        )
    )
    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
