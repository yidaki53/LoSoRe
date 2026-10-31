from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from engine.alternate_streams import _mz_relocation_locations, _repository_file
from engine.routine_contract import load_contract, pascal_declaration
from tools.asmcfg import parse_ghidra_asm, resolve_branch_target
from tools.liero_file_probe import (
    _build_image,
    _checked_regions,
    _sha256,
    assemble_probe,
    run_dosbox,
)

TARGET_NAME = "liero"
ROUTINE_NAME = "FUN_24dd_3f86"
ROUTINE_SEGMENT = 0x24DD
ROUTINE_OFFSET = 0x3F86
ROUTINE_ADDRESS = ROUTINE_SEGMENT * 16 + ROUTINE_OFFSET
ROUTINE_BYTES = bytes.fromhex(
    "fc 8b dc 8c da 36 c5 77 08 36 c4 7f 04 ac 26 8a 25 47 8a c8 "
    "3a cc 76 02 8a cc 0a c9 74 06 32 ed f3 a6 75 02 3a c4 8e da "
    "ca 08 00"
)
INSTRUCTION_SIZES = (
    1,
    2,
    2,
    4,
    4,
    1,
    3,
    1,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    2,
    3,
)
INSTRUCTIONS = (
    "CLD",
    "MOV BX,SP",
    "MOV DX,DS",
    "LDS SI,SS:[BX + 0X8]",
    "LES DI,SS:[BX + 0X4]",
    "LODSB SI",
    "MOV AH,BYTE PTR ES:[DI]",
    "INC DI",
    "MOV CL,AL",
    "CMP CL,AH",
    "JBE 0X2000:8D70",
    "MOV CL,AH",
    "OR CL,CL",
    "JZ 0X2000:8D7A",
    "XOR CH,CH",
    "CMPSB.REPE ES:DI,SI",
    "JNZ 0X2000:8D7C",
    "CMP AL,AH",
    "MOV DX,DS",
    "RETF 0X8",
)

DEST_OFFSET = 0x5000
SOURCE_OFFSET = 0x5400
STRING_SIZE = 256
CASE_RECORD_SIZE = 4 + STRING_SIZE * 2
ORIGINAL_RECORD_SIZE = 20 + STRING_SIZE * 2
CANDIDATE_RECORD_SIZE = 2 + STRING_SIZE * 2
DEFINED_FLAG_MASK = 0x0041


@dataclass(frozen=True)
class CompareCase:
    name: str
    dest: bytes
    source: bytes
    dest_offset: int = DEST_OFFSET
    source_offset: int = SOURCE_OFFSET

    def __post_init__(self) -> None:
        if len(self.dest) != STRING_SIZE or len(self.source) != STRING_SIZE:
            raise ValueError("each length-prefixed string must occupy 256 bytes")
        if self.dest[0] > 255 or self.source[0] > 255:
            raise ValueError("string length must fit in one byte")


def _encoded_string(value: bytes) -> bytes:
    if len(value) > 255:
        raise ValueError("Pascal string payload cannot exceed 255 bytes")
    return bytes((len(value),)) + value + bytes(255 - len(value))


def fixture_cases() -> list[CompareCase]:
    return [
        CompareCase("both-empty", _encoded_string(b""), _encoded_string(b"")),
        CompareCase("equal", _encoded_string(b"LIERO"), _encoded_string(b"LIERO")),
        CompareCase("dest-less", _encoded_string(b"ABC"), _encoded_string(b"ABD")),
        CompareCase("dest-greater", _encoded_string(b"ABD"), _encoded_string(b"ABC")),
        CompareCase("source-shorter", _encoded_string(b"ABCD"), _encoded_string(b"AB")),
        CompareCase("dest-shorter", _encoded_string(b"AB"), _encoded_string(b"ABCD")),
        CompareCase(
            "embedded-zero", _encoded_string(b"A\x00C"), _encoded_string(b"A\x00D")
        ),
        CompareCase(
            "equal-maximum-length",
            _encoded_string(bytes(range(255))),
            _encoded_string(bytes(range(255))),
        ),
        CompareCase(
            "late-mismatch",
            _encoded_string(bytes(range(254)) + b"\x10"),
            _encoded_string(bytes(range(254)) + b"\x20"),
        ),
    ]


TRAINING_SUITE = "liero-compare-train-v1"
HELD_OUT_SUITE = "liero-compare-heldout-v1-seed-20261030"
HELD_OUT_CASE_COUNT = 64


def held_out_fixture_cases() -> list[CompareCase]:
    """Create a stable challenge suite with lengths and mismatch positions."""
    rng = random.Random(0x20261030)
    length_pairs = (
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (254, 255),
        (255, 254),
        (255, 255),
        (254, 254),
        (127, 128),
        (128, 127),
        (128, 128),
        (3, 255),
        (255, 3),
    )
    cases = []
    for index in range(HELD_OUT_CASE_COUNT):
        destination_length, source_length = length_pairs[index % len(length_pairs)]
        common_length = min(destination_length, source_length)
        destination = bytearray(rng.randrange(256) for _ in range(destination_length))
        source = bytearray(destination[:common_length])
        source.extend(rng.randrange(256) for _ in range(source_length - common_length))

        mode = (index // len(length_pairs)) % 4
        if common_length and mode:
            mismatch_position = {
                1: 0,
                2: common_length // 2,
                3: common_length - 1,
            }[mode]
            destination_byte = destination[mismatch_position]
            source[mismatch_position] = (
                destination_byte + 1 if destination_byte < 255 else destination_byte - 1
            )
        if common_length > 1 and index % 5 == 0:
            embedded_zero = common_length // 2
            if mode == 2 and embedded_zero == common_length // 2:
                embedded_zero = max(0, embedded_zero - 1)
            is_mismatch_position = (
                common_length > 0 and mode > 0 and embedded_zero == mismatch_position
            )
            if not is_mismatch_position:
                destination[embedded_zero] = 0
                source[embedded_zero] = 0

        cases.append(
            CompareCase(
                f"heldout-{index:02d}",
                _encoded_string(bytes(destination)),
                _encoded_string(bytes(source)),
            )
        )
    return cases


def fixture_suite(suite_id: str) -> list[CompareCase]:
    if suite_id == TRAINING_SUITE:
        return fixture_cases()
    if suite_id == HELD_OUT_SUITE:
        return held_out_fixture_cases()
    raise ValueError(f"unknown comparator fixture suite: {suite_id}")


def fixture_suite_sha256(suite_id: str) -> str:
    return hashlib.sha256(encode_cases(fixture_suite(suite_id))).hexdigest()


def encode_cases(cases: list[CompareCase]) -> bytes:
    encoded = bytearray()
    for case in cases:
        encoded.extend(struct.pack("<HH", case.dest_offset, case.source_offset))
        encoded.extend(case.dest)
        encoded.extend(case.source)
    return bytes(encoded)


def expected_flag_mask(case: CompareCase) -> int:
    dest_len, source_len = case.dest[0], case.source[0]
    common = min(dest_len, source_len)
    for index in range(common):
        dest_byte = case.dest[index + 1]
        source_byte = case.source[index + 1]
        if dest_byte != source_byte:
            return 0x0001 if source_byte < dest_byte else 0
    if dest_len == source_len:
        return 0x0040
    return 0x0001 if source_len < dest_len else 0


def decode_original_trace(data: bytes, cases: list[CompareCase]) -> list[dict]:
    expected_size = len(cases) * ORIGINAL_RECORD_SIZE
    if len(data) != expected_size:
        raise ValueError(f"trace size is {len(data)} bytes; expected {expected_size}")

    records: list[dict] = []
    for index, case in enumerate(cases):
        start = index * ORIGINAL_RECORD_SIZE
        header = struct.unpack_from("<10H", data, start)
        stage, cs, ds, es, ss, sp_before, sp_after, flags, dest, source = header
        data_start = start + 20
        records.append(
            {
                "stage": stage,
                "cs": cs,
                "ds": ds,
                "es": es,
                "ss": ss,
                "sp_before": sp_before,
                "sp_after": sp_after,
                "flags": flags & DEFINED_FLAG_MASK,
                "dest_offset": dest,
                "source_offset": source,
                "dest": data[data_start : data_start + STRING_SIZE],
                "source": data[data_start + STRING_SIZE : data_start + 2 * STRING_SIZE],
                "identity_valid": (
                    stage == index + 1
                    and cs != 0
                    and cs == ds == es == ss
                    and dest == case.dest_offset
                    and source == case.source_offset
                ),
                "stack_balanced": sp_before == sp_after,
            }
        )
    return records


def _decode_candidate_output(data: bytes, cases: list[CompareCase]) -> list[dict]:
    expected_size = len(cases) * CANDIDATE_RECORD_SIZE
    if len(data) != expected_size:
        raise ValueError(
            f"candidate output size is {len(data)} bytes; expected {expected_size}"
        )

    records: list[dict] = []
    for index in range(len(cases)):
        start = index * CANDIDATE_RECORD_SIZE
        flags = struct.unpack_from("<H", data, start)[0] & DEFINED_FLAG_MASK
        data_start = start + 2
        records.append(
            {
                "flags": flags,
                "dest": data[data_start : data_start + STRING_SIZE],
                "source": data[data_start + STRING_SIZE : data_start + 2 * STRING_SIZE],
            }
        )
    return records


def compare_cases(
    cases: list[CompareCase], original_trace: bytes, candidate_output: bytes
) -> dict:
    originals = decode_original_trace(original_trace, cases)
    candidates = _decode_candidate_output(candidate_output, cases)
    results = []
    for case, original, candidate in zip(cases, originals, candidates, strict=True):
        expected_flags = expected_flag_mask(case)
        original_memory_changed = (
            original["dest"] != case.dest or original["source"] != case.source
        )
        candidate_memory_changed = (
            candidate["dest"] != case.dest or candidate["source"] != case.source
        )
        passed = (
            original["identity_valid"]
            and original["stack_balanced"]
            and original["flags"] == expected_flags
            and candidate["flags"] == original["flags"]
            and not original_memory_changed
            and not candidate_memory_changed
        )
        results.append(
            {
                "name": case.name,
                "status": "passed" if passed else "failed",
                "expected_flags": expected_flags,
                "original_flags": original["flags"],
                "candidate_flags": candidate["flags"],
                "identity_valid": original["identity_valid"],
                "stack_balanced": original["stack_balanced"],
                "original_memory_changed": original_memory_changed,
                "candidate_memory_changed": candidate_memory_changed,
            }
        )
    return {
        "status": "passed"
        if all(row["status"] == "passed" for row in results)
        else "failed",
        "case_count": len(results),
        "cases": results,
    }


def _validate_artifact_hashes(output_dir: Path, expected_hashes: dict) -> None:
    if not isinstance(expected_hashes, dict):
        raise TypeError("comparator artifact bindings must be a mapping")
    expected_paths = set(expected_hashes)
    if not expected_paths:
        raise ValueError("missing comparator artifact bindings")
    for relative in expected_paths:
        relative_path = Path(relative)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"invalid comparator artifact path: {relative}")
    actual_paths = {
        str(path.relative_to(output_dir))
        for path in output_dir.rglob("*")
        if path.is_file() and path.name != "result.json"
    }
    if actual_paths != expected_paths:
        raise ValueError("missing or unexpected comparator artifacts")
    for relative, expected_hash in expected_hashes.items():
        path = output_dir / relative
        if _sha256(path.read_bytes()) != expected_hash:
            raise ValueError(f"stale comparator artifact: {relative}")


def _routine_region(root: Path, binary: bytes, manifest: dict) -> dict:
    mapping = manifest["image_mapping"]
    load_value = mapping["load_segment"]
    load_segment = (
        int(load_value, 0) if isinstance(load_value, str) else int(load_value)
    )
    header_bytes = int(mapping["header_bytes"])
    expected_segment = (load_segment + 0x14DD) & 0xFFFF
    if expected_segment != ROUTINE_SEGMENT:
        raise ValueError("comparator address does not match the manifest load mapping")

    file_offset = header_bytes + ROUTINE_ADDRESS - load_segment * 16
    file_end = file_offset + len(ROUTINE_BYTES)
    if file_offset < header_bytes or file_end > len(binary):
        raise ValueError("comparator code lies outside the verified executable")
    if binary[file_offset:file_end] != ROUTINE_BYTES:
        raise ValueError("comparator bytes differ from the pinned original bytes")
    if any(
        file_offset <= offset < file_end
        for offset in _mz_relocation_locations(binary, header_bytes)
    ):
        raise ValueError("comparator bytes overlap a relocated MZ operand")

    asm_path = root / "targets/liero/asm/FUN_24dd_3f86.s"
    parsed = parse_ghidra_asm(asm_path.read_text(encoding="utf-8"))
    boundaries = []
    cursor = ROUTINE_ADDRESS
    for size in INSTRUCTION_SIZES:
        boundaries.append(cursor)
        cursor += size
    if cursor != ROUTINE_ADDRESS + len(ROUTINE_BYTES):
        raise ValueError("instruction sizes do not cover the pinned routine bytes")
    if parsed["addrs"] != boundaries:
        raise ValueError(
            "assembly instruction boundaries differ from the pinned routine"
        )
    if parsed["segments"] != [ROUTINE_SEGMENT] * len(boundaries):
        raise ValueError("assembly segment differs from the original routine segment")
    if parsed["insts"] != list(INSTRUCTIONS):
        raise ValueError(
            "assembly instructions differ from the reviewed routine listing"
        )

    boundary_set = set(boundaries)
    for instruction in parsed["insts"]:
        mnemonic = instruction.split(maxsplit=1)[0].split(".", maxsplit=1)[0]
        if mnemonic in {"JMP", "JBE", "JB", "JAE", "JA", "JZ", "JNZ", "LOOP"}:
            target = resolve_branch_target(instruction, ROUTINE_SEGMENT)
            if target not in boundary_set:
                raise ValueError(
                    f"branch target is not an instruction boundary: {instruction}"
                )

    return {
        "name": ROUTINE_NAME,
        "address": f"0x{ROUTINE_ADDRESS:X}",
        "location": f"{ROUTINE_SEGMENT:04X}:{ROUTINE_OFFSET:04X}",
        "file_offset": file_offset,
        "size": len(ROUTINE_BYTES),
        "bytes_hex": ROUTINE_BYTES.hex(),
        "sha256": hashlib.sha256(ROUTINE_BYTES).hexdigest(),
    }


def validate_saved_report(output_dir: Path, root: Path) -> dict:
    output_dir, root = output_dir.resolve(), root.resolve()
    report = json.loads((output_dir / "result.json").read_text(encoding="utf-8"))
    if report.get("schema_version") != 1 or report.get("target") != TARGET_NAME:
        raise ValueError("unrecognized comparator evidence report")
    _validate_checked_contract(root)

    manifest_path = root / "targets/liero/alternate_streams.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    binary_path = _repository_file(root / "targets/liero", manifest["binary"]["path"])
    if binary_path is None:
        raise FileNotFoundError("the manifest-bound Liero executable is unavailable")
    binary = binary_path.read_bytes()
    if report.get("manifest_sha256") != _sha256(
        manifest_path.read_bytes()
    ) or report.get("original_binary_sha256") != _sha256(binary):
        raise ValueError("stale comparator original executable or manifest")

    current_sources = {
        str(path.relative_to(root)): _sha256(path.read_bytes())
        for path in _source_paths(root)
    }
    if report.get("source_sha256") != current_sources:
        raise ValueError("stale comparator source/evidence")
    if report.get("tool_sha256") != _tool_hashes():
        raise ValueError("stale comparator toolchain")
    _validate_artifact_hashes(output_dir, report.get("artifacts", {}))
    for source in candidate_source_paths(root):
        copied_source = output_dir / "candidate" / source.name
        if copied_source.read_bytes() != source.read_bytes():
            raise ValueError(f"stale Pascal candidate source: {source.name}")

    region = _routine_region(root, binary, manifest)
    if report.get("routine") != region:
        raise ValueError("stale comparator routine mapping")
    suite_id = report.get("fixture_suite")
    cases = fixture_suite(suite_id)
    if report.get("fixture_suite_sha256") != fixture_suite_sha256(suite_id):
        raise ValueError("comparator fixture suite identity changed")
    if (output_dir / "CASES.BIN").read_bytes() != encode_cases(cases):
        raise ValueError("comparator fixture corpus changed")
    expected_image = _build_image(
        (output_dir / "harness/harness.bin").read_bytes(),
        binary,
        manifest,
        [region],
    )
    if (output_dir / "PROBE.COM").read_bytes() != expected_image:
        raise ValueError("stale comparator DOS image")

    recomputed = compare_cases(
        cases,
        (output_dir / "TRACE.BIN").read_bytes(),
        (output_dir / "PASCAL.BIN").read_bytes(),
    )
    if (
        report.get("status") != recomputed["status"]
        or report.get("case_count") != recomputed["case_count"]
        or report.get("cases") != recomputed["cases"]
    ):
        raise ValueError("saved comparator result does not match captured evidence")
    return report


def candidate_source_paths(root: Path) -> list[Path]:
    return [
        root / "targets/liero/src/FUN_24dd_3f86.inc",
        root / "targets/liero/src/LieroRuntime.pas",
        root / "tools/liero_compare_candidate.pas",
        root / "targets/liero/config/routine_contracts.json",
    ]


def compile_candidate(candidate_dir: Path) -> Path:
    executable = candidate_dir / "probe_liero_compare"
    command = [
        "fpc",
        "-B",
        "-Fu.",
        "-Fi.",
        "-FE.",
        "-FU.",
        "-oprobe_liero_compare",
        "liero_compare_candidate.pas",
    ]
    completed = subprocess.run(
        command,
        cwd=candidate_dir,
        check=False,
        capture_output=True,
        text=True,
    )
    compile_output = completed.stdout + completed.stderr
    (candidate_dir / "fpc.log").write_text(compile_output, encoding="utf-8")
    if completed.returncode:
        raise RuntimeError(f"Free Pascal compilation failed:\n{compile_output}")
    return executable


def run_candidate(
    executable: Path, case_path: Path, output_path: Path, segment: int
) -> None:
    working_directory = executable.parent
    completed = subprocess.run(
        [
            f"./{executable.name}",
            os.path.relpath(case_path, working_directory),
            os.path.relpath(output_path, working_directory),
            f"{segment:04X}",
        ],
        cwd=working_directory,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(
            f"Pascal candidate failed with exit code {completed.returncode}: "
            f"{completed.stdout}{completed.stderr}"
        )


def _source_paths(root: Path) -> list[Path]:
    return [
        root / "tools/liero_compare_routine_probe.py",
        root / "tools/liero_compare_routine_probe.S",
        root / "tools/liero_file_probe.py",
        root / "tools/liero_file_probe.S",
        root / "tools/asmcfg.py",
        root / "targets/liero/alternate_streams.json",
        root / "targets/liero/asm/FUN_24dd_3f86.s",
        root / "targets/liero/src/FUN_24dd_3f86.inc",
        root / "targets/liero/src/LieroRuntime.pas",
        root / "targets/liero/config/routine_contracts.json",
        root / "tools/liero_compare_candidate.pas",
        root / "engine/alternate_streams.py",
        root / "engine/callbacks.py",
        root / "engine/object_identity.py",
        root / "engine/object_setup.py",
        root / "engine/object_lifecycle.py",
        root / "engine/object_loops.py",
    ]


def _validate_checked_contract(root: Path) -> None:
    target = root / "targets/liero"
    contract = load_contract(target, ROUTINE_NAME)
    if contract is None:
        raise ValueError(f"{ROUTINE_NAME}: checked routine contract is missing")
    if contract["oracle"] != "liero-compare-routine-probe":
        raise ValueError(f"{ROUTINE_NAME}: unexpected routine oracle contract")
    source = target / "src/FUN_24dd_3f86.inc"
    declaration = pascal_declaration(source.read_text(encoding="utf-8"), ROUTINE_NAME)
    if declaration != contract["declaration"]:
        raise ValueError(
            f"{ROUTINE_NAME}: Pascal declaration does not match the checked contract"
        )


def _tool_hashes() -> dict:
    hashes = {}
    for name in ("as", "ld", "dosbox", "fpc"):
        executable = shutil.which(name)
        if executable is None:
            raise FileNotFoundError(f"required comparator tool is unavailable: {name}")
        hashes[name] = _sha256(Path(executable).read_bytes())
    return hashes


def run_probe(
    root: Path,
    output_dir: Path,
    suite_id: str = TRAINING_SUITE,
) -> dict:
    if output_dir.exists():
        raise FileExistsError(f"probe output directory already exists: {output_dir}")
    if shutil.which("as") is None or shutil.which("ld") is None:
        raise RuntimeError("GNU as and ld are required to assemble the original probe")
    if shutil.which("dosbox") is None:
        raise RuntimeError("DOSBox is required to execute the original probe")
    if shutil.which("fpc") is None:
        raise RuntimeError("Free Pascal is required to execute the Pascal candidate")

    target = root / "targets/liero"
    _validate_checked_contract(root)
    manifest_path = target / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    binary_path = _repository_file(target, manifest["binary"]["path"])
    if binary_path is None:
        raise FileNotFoundError("the manifest-bound Liero executable is unavailable")
    binary = binary_path.read_bytes()
    if _sha256(binary) != manifest["binary"]["sha256"]:
        raise ValueError("probe executable changed after evidence validation")
    manifest, _ = _checked_regions(root)
    region = _routine_region(root, binary, manifest)
    cases = fixture_suite(suite_id)
    output_dir.mkdir(parents=True)

    source_paths = _source_paths(root)
    source_hashes = {
        str(path.relative_to(root)): _sha256(path.read_bytes()) for path in source_paths
    }
    candidate_dir = output_dir / "candidate"
    candidate_dir.mkdir()
    for source in candidate_source_paths(root):
        shutil.copy2(source, candidate_dir / source.name)
    case_path = output_dir / "CASES.BIN"
    case_path.write_bytes(encode_cases(cases))
    harness_path = root / "tools/liero_compare_routine_probe.S"
    harness_dir = output_dir / "harness"
    harness_dir.mkdir()
    harness_binary = assemble_probe(harness_path, harness_dir)
    dos_image = _build_image(
        harness_binary,
        binary,
        manifest,
        [region],
    )
    (output_dir / "PROBE.COM").write_bytes(dos_image)
    original_trace_path = output_dir / "TRACE.BIN"
    run_dosbox(output_dir)

    executable = compile_candidate(candidate_dir)
    candidate_output = output_dir / "PASCAL.BIN"
    original_records = decode_original_trace(original_trace_path.read_bytes(), cases)
    segment = original_records[0]["cs"]
    run_candidate(executable, case_path, candidate_output, segment)
    result = compare_cases(
        cases,
        original_trace_path.read_bytes(),
        candidate_output.read_bytes(),
    )
    artifacts = sorted(
        path
        for path in output_dir.rglob("*")
        if path.is_file() and path.name != "result.json"
    )
    report = {
        "schema_version": 1,
        "target": TARGET_NAME,
        "fixture_suite": suite_id,
        "fixture_suite_sha256": fixture_suite_sha256(suite_id),
        "routine": region,
        "status": result["status"],
        "case_count": result["case_count"],
        "cases": result["cases"],
        "original_binary_sha256": _sha256(binary),
        "manifest_sha256": _sha256(manifest_path.read_bytes()),
        "source_sha256": source_hashes,
        "tool_sha256": _tool_hashes(),
        "artifacts": {
            str(path.relative_to(output_dir)): _sha256(path.read_bytes())
            for path in artifacts
        },
        "scope": [
            "defined ZF and CF outcomes for listed fixtures",
            "far-call stack balance for the captured calls",
            "non-mutation of each tested 256-byte string region",
        ],
        "limitations": [
            "unmeasured registers and flags are not claimed",
            "arbitrary pointer aliasing and wrapping are not covered",
            "fixtures do not establish behavior for all possible inputs",
        ],
    }
    (output_dir / "result.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    validate_saved_report(output_dir, root)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--suite",
        default=TRAINING_SUITE,
        choices=[TRAINING_SUITE, HELD_OUT_SUITE],
    )
    args = parser.parse_args()
    report = run_probe(args.root.resolve(), args.output.resolve(), args.suite)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
