"""Compare Liero's shared six-word copy entries with original bytes in DOSBox."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from collections.abc import Mapping

REPOSITORY = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from tools import liero_file_probe

ROUTINES = ("FUN_24dd_0582", "FUN_24dd_05e8")
ENTRY_OFFSETS = {ROUTINES[0]: 0x0582, ROUTINES[1]: 0x05E8}
SOURCE_OFFSETS = {ROUTINES[0]: 0x0576, ROUTINES[1]: 0x05DC}
EXPECTED_BYTES = {
    0x0576: bytes.fromhex("000000000000008001000000b87605eb64"),
    0x05DC: bytes.fromhex("000000000000000001c00000"),
    0x05E8: bytes.fromhex("b8dc051e8cc98ed996fcb90600f3a583ef0c961fc3"),
}
DESTINATIONS = (0x0200, 0xFFFA, 0x0000, 0x000C)
TRAINING_CASES = tuple(
    (routine, offset)
    for offset in DESTINATIONS[:2]
    for routine in ROUTINES
)
HELD_OUT_CASES = tuple(
    (routine, offset)
    for offset in DESTINATIONS[2:]
    for routine in ROUTINES
)
ALL_CASES = TRAINING_CASES + HELD_OUT_CASES
DEFINED_FLAG_MASK = 0x0441
RECORD = struct.Struct("<13H14B")
RECORD_SIZE = RECORD.size


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_binary(root: pathlib.Path) -> tuple[bytes, dict]:
    binary_path = root / "extracted/liero/LIERO.EXE"
    manifest = json.loads((root / "targets/liero/alternate_streams.json").read_text())
    binary = binary_path.read_bytes()
    expected_hash = manifest["binary"]["sha256"]
    if _sha256(binary) != expected_hash:
        raise ValueError("original executable changed after validation")
    header_bytes = manifest["image_mapping"]["header_bytes"]
    for offset, expected in EXPECTED_BYTES.items():
        file_offset = header_bytes + 0x24DD0 + offset - 0x10000
        if binary[file_offset : file_offset + len(expected)] != expected:
            raise ValueError(f"original executable bytes differ at 24DD:{offset:04X}")
    return binary, manifest


def _regions() -> list[dict[str, str]]:
    return [
        {
            "address": f"0x{0x24DD0 + offset:05x}",
            "bytes_hex": data.hex(),
        }
        for offset, data in EXPECTED_BYTES.items()
    ]


def _harness_source(cases: tuple[tuple[str, int], ...]) -> str:
    case_table = "\n".join(
        f"    .word 0x{ENTRY_OFFSETS[routine]:04x}, 0x{destination:04x}"
        for routine, destination in cases
    )
    return r""".code16
.section .text
.global _start

.set RECORD_SIZE, 40

_start:
    push %cs
    pop %ds
    mov $trace_name, %dx
    mov $0x3c00, %ax
    xor %cx, %cx
    int $0x21
    jc failed
    mov %ax, output_handle
    mov $case_table, %bp

next_case:
    movw 0(%bp), %bx
    cmpw $0xffff, %bx
    je finish
    movw 2(%bp), %di
    addw $4, %bp
    movw %di, di_input
    movw $0x2000, %ax
    movw %ax, %es
    movw $14, %cx
    movb $0xa5, %al
    cld
    rep stosb
    movw di_input, %di
    movw $0x3456, %si
    movw $0x1234, %cx
    movw $0xbeef, %ax
    movw %sp, trace_record+20
    std
    stc
    call *%bx

    movw %bx, trace_record+0
    movw %ax, trace_record+4
    movw di_input, %ax
    movw %ax, trace_record+2
    movw %cx, trace_record+6
    movw %si, trace_record+8
    movw %di, trace_record+10
    movw %cs, %ax
    movw %ax, trace_record+12
    movw %ds, %ax
    movw %ax, trace_record+14
    movw %es, %ax
    movw %ax, trace_record+16
    movw %ss, %ax
    movw %ax, trace_record+18
    movw %sp, %ax
    movw %ax, trace_record+22
    pushf
    popw %ax
    movw %ax, trace_record+24

    movw di_input, %si
    push %ds
    push %es
    movw %es, %ax
    movw %ax, %ds
    push %cs
    pop %es
    movw $trace_record+26, %di
    movw $14, %cx
    cld
    rep movsb
    pop %es
    pop %ds

    movw output_handle, %bx
    movw $trace_record, %dx
    movw $RECORD_SIZE, %cx
    movw $0x4000, %ax
    int $0x21
    jc failed
    cmpw $RECORD_SIZE, %ax
    jne failed
    jmp next_case

finish:
    movw output_handle, %bx
    movw $0x3e00, %ax
    int $0x21
    jc failed
    movw $0x4c00, %ax
    int $0x21

failed:
    movw $0x4c01, %ax
    int $0x21

trace_name:
    .asciz "TRACE.BIN"

.align 2
output_handle:
    .word 0
di_input:
    .word 0
trace_record:
    .space RECORD_SIZE
case_table:
__CASE_TABLE__
    .word 0xffff, 0
""".replace("__CASE_TABLE__", case_table)


def _candidate_program(
    cases: tuple[tuple[str, int], ...], source_bytes: Mapping[int, bytes]
) -> str:
    entry_values = ", ".join(f"${ENTRY_OFFSETS[name]:04X}" for name, _ in cases)
    destinations = ", ".join(f"${offset:04X}" for _, offset in cases)
    initialize_code = "\n".join(
        f"  CodeMemory[${offset + index:04X}] := ${value:02X};"
        for offset, data in source_bytes.items()
        for index, value in enumerate(data)
    )
    return f"""program LieroCopyCandidate;
{{$MODE TP}}
uses LieroRuntime;
{{$I {ROUTINES[0]}.inc}}
{{$I {ROUTINES[1]}.inc}}

type
  TOracleRecord = packed record
    EntryPoint, DIInput, AXValue, CXValue, SIValue, DIValue: Word;
    CSValue, DSValue, ESValue, SSValue, SPBefore, SPAfter, FlagsValue: Word;
    Memory: array[0..13] of Byte;
  end;
  TWordArray = array[0..{len(cases) - 1}] of Word;

const
  EntryPoints: TWordArray = ({entry_values});
  DestinationOffsets: TWordArray = ({destinations});

var
  outputFile: file;
  outputRecord: TOracleRecord;
  caseIndex, byteIndex: Integer;
  destinationAddress, wrappedOffset: Longint;

begin
  Assign(outputFile, ParamStr(1));
  Rewrite(outputFile, 1);
  for caseIndex := 0 to {len(cases) - 1} do
  begin
    FillChar(CodeMemory, SizeOf(CodeMemory), 0);
    FillChar(RealModeMemory, SizeOf(RealModeMemory), 0);
{initialize_code}
    RegisterDS := $1111;
    RegisterES := $2000;
    RegisterSS := $2222;
    RegisterSP := $D000;
    RegisterSI := $3456;
    RegisterDI := DestinationOffsets[caseIndex];
    RegisterAX := $BEEF;
    RegisterCX := $1234;
    RegisterZeroFlag := True;
    RegisterCarryFlag := True;
    RegisterDirectionFlag := True;
    for byteIndex := 0 to 13 do
    begin
      wrappedOffset := (Longint(RegisterDI) + byteIndex) and $FFFF;
      destinationAddress :=
        ((Longint(RegisterES) * 16) + wrappedOffset) and $FFFFF;
      RealModeMemory[destinationAddress] := $A5;
    end;
    outputRecord.SPBefore := RegisterSP;
    if EntryPoints[caseIndex] = $0582 then
      FUN_24dd_0582
    else
      FUN_24dd_05e8;
    outputRecord.EntryPoint := EntryPoints[caseIndex];
    outputRecord.DIInput := DestinationOffsets[caseIndex];
    outputRecord.AXValue := RegisterAX;
    outputRecord.CXValue := RegisterCX;
    outputRecord.SIValue := RegisterSI;
    outputRecord.DIValue := RegisterDI;
    outputRecord.CSValue := 0;
    outputRecord.DSValue := RegisterDS;
    outputRecord.ESValue := RegisterES;
    outputRecord.SSValue := RegisterSS;
    outputRecord.SPAfter := RegisterSP;
    outputRecord.FlagsValue := 0;
    if RegisterCarryFlag then
      outputRecord.FlagsValue := outputRecord.FlagsValue or $0001;
    if RegisterZeroFlag then
      outputRecord.FlagsValue := outputRecord.FlagsValue or $0040;
    if RegisterDirectionFlag then
      outputRecord.FlagsValue := outputRecord.FlagsValue or $0400;
    for byteIndex := 0 to 13 do
    begin
      wrappedOffset := (Longint(RegisterDI) + byteIndex) and $FFFF;
      destinationAddress :=
        ((Longint(RegisterES) * 16) + wrappedOffset) and $FFFFF;
      outputRecord.Memory[byteIndex] := RealModeMemory[destinationAddress];
    end;
    BlockWrite(outputFile, outputRecord, SizeOf(outputRecord));
  end;
  Close(outputFile);
end.
"""


def _decode_records(data: bytes) -> list[dict]:
    if not data or len(data) % RECORD_SIZE:
        raise ValueError("oracle output is empty or has a partial record")
    names = (
        "entry",
        "di_input",
        "ax",
        "cx",
        "si",
        "di",
        "cs",
        "ds",
        "es",
        "ss",
        "sp_before",
        "sp_after",
        "flags",
    )
    records = []
    for offset in range(0, len(data), RECORD_SIZE):
        values = RECORD.unpack_from(data, offset)
        records.append(
            {
                **dict(zip(names, values[:13], strict=True)),
                "memory": bytes(values[13:]),
            }
        )
    return records


def _suite_cases(suite: str) -> tuple[tuple[str, int], ...]:
    if suite == "training":
        return TRAINING_CASES
    if suite == "heldout":
        return HELD_OUT_CASES
    raise ValueError(f"unsupported copy-routine suite: {suite}")


def _compare(
    original: list[dict],
    candidate: list[dict],
    cases: tuple[tuple[str, int], ...],
) -> list[dict]:
    if len(original) != len(cases) or len(candidate) != len(cases):
        raise ValueError("original or Pascal record count disagrees with suite")
    original_by_case = {
        (record["entry"], record["di_input"]): record for record in original
    }
    results = []
    for index, (routine, destination) in enumerate(cases):
        entry = ENTRY_OFFSETS[routine]
        original_record = original_by_case[(entry, destination)]
        candidate_record = candidate[index]
        checks = {
            field: original_record[field] == candidate_record[field]
            for field in ("entry", "di_input", "ax", "cx", "si", "di", "memory")
        }
        checks["original_ds_preserved"] = (
            original_record["ds"] == original_record["cs"]
        )
        checks["candidate_ds_preserved"] = candidate_record["ds"] == 0x1111
        checks["original_es_preserved"] = original_record["es"] == 0x2000
        checks["candidate_es_preserved"] = candidate_record["es"] == 0x2000
        checks["original_ss_preserved"] = (
            original_record["ss"] == original_record["cs"]
        )
        checks["candidate_ss_preserved"] = candidate_record["ss"] == 0x2222
        checks["original_stack_balanced"] = (
            original_record["sp_before"] == original_record["sp_after"]
        )
        checks["candidate_stack_balanced"] = (
            candidate_record["sp_before"] == candidate_record["sp_after"]
        )
        checks["defined_flags"] = (
            original_record["flags"] & DEFINED_FLAG_MASK
        ) == (candidate_record["flags"] & DEFINED_FLAG_MASK)
        results.append(
            {
                "routine": routine,
                "destination": destination,
                "status": "passed" if all(checks.values()) else "failed",
                "checks": checks,
                "original": {
                    **{key: value for key, value in original_record.items() if key != "memory"},
                    "memory_hex": original_record["memory"].hex(),
                },
                "candidate": {
                    **{key: value for key, value in candidate_record.items() if key != "memory"},
                    "memory_hex": candidate_record["memory"].hex(),
                },
            }
        )
    return results


def _compile_candidate(
    directory: pathlib.Path,
    cases: tuple[tuple[str, int], ...],
    source_bytes: Mapping[int, bytes],
) -> pathlib.Path:
    executable = directory / "candidate"
    source = directory / "candidate.pas"
    source.write_text(_candidate_program(cases, source_bytes), encoding="utf-8")
    command = [
        "fpc",
        "-Mtp",
        f"-Fu{directory}",
        f"-Fi{directory}",
        f"-FU{directory}",
        f"-FE{directory}",
        f"-o{executable}",
        str(source),
    ]
    result = subprocess.run(
        command, cwd=directory, check=False, capture_output=True, timeout=60
    )
    (directory / "compile.log").write_bytes(result.stdout + result.stderr)
    (directory / "compile-command.json").write_text(json.dumps(command, indent=2) + "\n")
    result.check_returncode()
    return executable


def run_probe(
    output: pathlib.Path,
    root: pathlib.Path = REPOSITORY,
    *,
    suite: str = "training",
    candidate_sources: Mapping[str, str] | None = None,
    candidate_runtime_source: str | None = None,
) -> dict:
    """Run a bounded original-byte comparison; this does not promote recovery."""
    root, output = root.resolve(), output.resolve()
    cases = _suite_cases(suite)
    tools = ("as", "ld", "dosbox", "fpc")
    missing = [tool for tool in tools if shutil.which(tool) is None]
    if missing:
        raise FileNotFoundError("copy-routine probe requires: " + ", ".join(missing))
    binary, manifest = _read_binary(root)
    output.mkdir(parents=True, exist_ok=False)

    harness_path = output / "harness.S"
    harness_path.write_text(_harness_source(cases), encoding="utf-8")
    harness = liero_file_probe.assemble_probe(harness_path, output)
    image = liero_file_probe._build_image(
        harness, binary, manifest, _regions()
    )
    if len(harness) >= 0x0576 - 0x0100:
        raise ValueError("copy-routine harness overlaps original source bytes")
    (output / "PROBE.COM").write_bytes(image)
    liero_file_probe.run_dosbox(output)
    original_trace = (output / "TRACE.BIN").read_bytes()
    original_records = _decode_records(original_trace)
    if len(original_records) != len(cases):
        raise ValueError("original execution did not produce all requested cases")

    candidate_dir = output / "candidate-source"
    candidate_dir.mkdir()
    source_hashes = {}
    for routine in ROUTINES:
        source_text = (
            candidate_sources[routine]
            if candidate_sources is not None
            else (root / "targets/liero/src" / f"{routine}.inc").read_text()
        )
        source_bytes_file = source_text.encode("utf-8")
        (candidate_dir / f"{routine}.inc").write_bytes(source_bytes_file)
        source_hashes[routine] = _sha256(source_bytes_file)
    runtime = root / "targets/liero/src/LieroRuntime.pas"
    runtime_content = (
        candidate_runtime_source
        if candidate_runtime_source is not None
        else runtime.read_text(encoding="utf-8")
    )
    runtime_bytes = runtime_content.encode("utf-8")
    (candidate_dir / runtime.name).write_bytes(runtime_bytes)
    source_bytes = {
        offset: binary[
            manifest["image_mapping"]["header_bytes"] + 0x24DD0 + offset - 0x10000 :
            manifest["image_mapping"]["header_bytes"] + 0x24DD0 + offset - 0x10000 + len(data)
        ]
        for offset, data in EXPECTED_BYTES.items()
    }
    executable = _compile_candidate(candidate_dir, cases, source_bytes)
    candidate_output = output / "PASCAL.BIN"
    completed = subprocess.run(
        [str(executable), str(candidate_output)],
        cwd=candidate_dir,
        check=False,
        capture_output=True,
        timeout=30,
    )
    (output / "candidate-run.log").write_bytes(completed.stdout + completed.stderr)
    completed.check_returncode()
    candidate_trace = candidate_output.read_bytes()
    candidate_records = _decode_records(candidate_trace)
    results = _compare(original_records, candidate_records, cases)
    report = {
        "status": "passed" if all(item["status"] == "passed" for item in results) else "failed",
        "oracle": "isolated_original_bytes_dosbox_vs_pascal_host_model",
        "suite": suite,
        "case_count": len(cases),
        "binary_sha256": _sha256(binary),
        "harness_source_sha256": _sha256(harness_path.read_bytes()),
        "harness_binary_sha256": _sha256(harness),
        "probe_com_sha256": _sha256(image),
        "original_trace_sha256": _sha256(original_trace),
        "candidate_trace_sha256": _sha256(candidate_trace),
        "candidate_source_sha256": source_hashes,
        "candidate_runtime_sha256": _sha256(runtime_bytes),
        "results": results,
        "limitations": [
            "The original routines execute in a controlled COM image, not normal LIERO.EXE startup.",
            "Only the fixed six-word copy entries, selected segment/register state, and defined CF/ZF/DF bits are compared.",
            "This scoped pass is not universal routine equivalence or source-recovery attestation.",
        ],
    }
    (output / "result.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


def validate_saved_report(output: pathlib.Path, root: pathlib.Path = REPOSITORY) -> dict:
    """Re-run the saved candidate against original bytes and compare its evidence."""
    output, root = output.resolve(), root.resolve()
    report = json.loads((output / "result.json").read_text(encoding="utf-8"))
    candidate_sources = {}
    for routine, expected_hash in report["candidate_source_sha256"].items():
        source = output / "candidate-source" / f"{routine}.inc"
        content = source.read_text(encoding="utf-8")
        if _sha256(content.encode("utf-8")) != expected_hash:
            raise ValueError(f"saved candidate source hash disagrees: {routine}")
        candidate_sources[routine] = content
    runtime_path = output / "candidate-source" / "LieroRuntime.pas"
    runtime_source = runtime_path.read_text(encoding="utf-8")
    if _sha256(runtime_source.encode("utf-8")) != report["candidate_runtime_sha256"]:
        raise ValueError("saved candidate runtime hash disagrees")
    with tempfile.TemporaryDirectory(
        prefix="liero-copy-replay-", dir=output.parent
    ) as temporary:
        replay = run_probe(
            pathlib.Path(temporary) / "replay",
            root,
            suite=report["suite"],
            candidate_sources=candidate_sources,
            candidate_runtime_source=runtime_source,
        )
    replay_keys = (
        "status",
        "oracle",
        "suite",
        "case_count",
        "binary_sha256",
        "harness_source_sha256",
        "harness_binary_sha256",
        "probe_com_sha256",
        "candidate_source_sha256",
        "candidate_runtime_sha256",
        "results",
    )
    if any(replay[key] != report[key] for key in replay_keys):
        raise ValueError("saved copy-routine report disagrees with original-byte replay")
    return report


def _validate_candidate_source(routine: str, source: str) -> str:
    pattern = re.compile(
        rf"\s*procedure\s+{re.escape(routine)}\s*;\s*"
        r"begin\s*RegisterAX\s*:=\s*\$[0-9A-Fa-f]{1,4}\s*;\s*"
        r"CopyCodeWordsToESDI\s*;\s*"
        r"RegisterAX\s*:=\s*\(\s*RegisterAX\s*\+\s*12\s*\)\s*"
        r"and\s*\$FFFF\s*;\s*end\s*;\s*",
        re.IGNORECASE,
    )
    if not pattern.fullmatch(source):
        raise ValueError(
            f"{routine} candidate must contain exactly the AX source assignment, "
            "checked CopyCodeWordsToESDI call, and AX source-end adjustment"
        )
    return source


def _model_prompt(feedback: list[str]) -> str:
    failures = "\n".join(feedback) if feedback else "No candidate feedback yet."
    return (
        "Implement two Turbo Pascal procedure includes from the original x86 "
        "instructions. Return only the required JSON object. Each value must "
        "be one complete procedure include with exactly three statements: set "
        "RegisterAX to the source offset, call CopyCodeWordsToESDI, then set "
        "RegisterAX to (RegisterAX + 12) and $FFFF. Do not add declarations, "
        "comments, directives, helper implementations, or other statements.\n\n"
        "Assembly facts:\n"
        "FUN_24dd_0582 at 24DD:0582 loads AX=$0576 then jumps to 24DD:05EB.\n"
        "FUN_24dd_05e8 at 24DD:05E8 loads AX=$05DC and enters the shared body.\n"
        "The shared body saves DS, loads CS then DS into CX, exchanges AX/SI, "
        "clears DF, sets CX=6, executes REP MOVSW from DS:SI to ES:DI, subtracts "
        "$000C from DI, exchanges AX/SI back, restores DS, and returns.\n"
        "The available runtime helper CopyCodeWordsToESDI models the shared "
        "six-word copy and the defined resulting CX, DF, CF, and ZF effects. "
        "It leaves RegisterAX unchanged and preserves RegisterSI, RegisterDI, "
        "RegisterDS, and RegisterES. In the original shared body, REP MOVSW "
        "advances SI by 12 before the final XCHG, so the returned AX is the "
        "source offset plus 12 modulo 16 bits.\n\n"
        "Training comparison failures (held-out outcomes are unavailable):\n"
        f"{failures}"
    )


def _request_proposal(
    prompt: str,
    *,
    model: str,
    endpoint: str,
) -> tuple[str | None, str, str | None]:
    schema = {
        "type": "object",
        "properties": {
            routine: {"type": "string", "minLength": 1} for routine in ROUTINES
        },
        "required": list(ROUTINES),
        "additionalProperties": False,
    }
    url = endpoint.rstrip("/")
    if not url.endswith("/api/generate"):
        url += "/api/generate"
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": schema,
            "options": {"temperature": 0.0, "num_predict": 256},
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        response_body = response.read().decode("utf-8")
    try:
        body = json.loads(response_body)
    except json.JSONDecodeError:
        return None, response_body, "local model returned an invalid response envelope"
    if not isinstance(body, dict):
        return None, response_body, "local model response envelope must be an object"
    completion = body.get("response")
    if not isinstance(completion, str):
        return None, response_body, "local model response has no string completion"
    return completion, response_body, None


def _positive_control_sources() -> dict[str, str]:
    return {
        routine: (
            f"procedure {routine};\n"
            "begin\n"
            f"  RegisterAX := ${SOURCE_OFFSETS[routine]:04X};\n"
            "  CopyCodeWordsToESDI;\n"
            "  RegisterAX := (RegisterAX + 12) and $FFFF;\n"
            "end;\n"
        )
        for routine in ROUTINES
    }


def run_trial(
    output: pathlib.Path,
    root: pathlib.Path = REPOSITORY,
    *,
    model: str,
    endpoint: str = "http://localhost:11434",
    max_proposals: int = 4,
) -> dict:
    """Run a four-proposal structured-output trial; candidates are never promoted."""
    if not 1 <= max_proposals <= 4:
        raise ValueError("max_proposals must be between 1 and 4")
    root, output = root.resolve(), output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    baseline = run_probe(
        output / "repository-baseline-training", root, suite="training"
    )
    positive_sources = _positive_control_sources()
    training_control = run_probe(
        output / "control-training",
        root,
        suite="training",
        candidate_sources=positive_sources,
    )
    controls = {"training": training_control}
    if training_control["status"] != "passed":
        result = {
            "status": "blocked",
            "stop_reason": "assembly-derived positive control failed training",
            "repository_baseline": {
                "status": baseline["status"],
                "report_path": "repository-baseline-training/result.json",
            },
            "controls": controls,
            "proposals": [],
        }
        (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
        return result
    validate_saved_report(output / "control-training", root)

    proposal_records = []
    baseline_failures = [
        "Repository baseline mismatches: "
        + "; ".join(
            f"{item['routine']} DI={item['destination']:#06x} "
            f"({', '.join(key for key, passed in item['checks'].items() if not passed)})"
            for item in baseline["results"]
            if item["status"] != "passed"
        )
    ]
    failures = [item for item in baseline_failures if item.split(": ", 1)[-1]]
    seen_sources: set[str] = set()
    best_candidate: dict | None = None
    for attempt in range(1, max_proposals + 1):
        prompt = _model_prompt(failures)
        proposal_dir = output / "proposals" / f"{attempt:03d}"
        proposal_dir.mkdir(parents=True)
        prompt_bytes = prompt.encode("utf-8")
        (proposal_dir / "prompt.txt").write_bytes(prompt_bytes)
        try:
            completion, response_body, response_error = _request_proposal(
                prompt, model=model, endpoint=endpoint
            )
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, TypeError) as exc:
            record = {
                "attempt": attempt,
                "status": "rejected",
                "reason": str(exc),
                "prompt_sha256": _sha256(prompt_bytes),
            }
            if isinstance(exc, urllib.error.HTTPError):
                error_body = exc.read().decode("utf-8", errors="replace")
                (proposal_dir / "http-error.txt").write_text(error_body, encoding="utf-8")
                record["http_status"] = exc.code
                record["http_error_path"] = (
                    proposal_dir / "http-error.txt"
                ).relative_to(output).as_posix()
            (proposal_dir / "rejection.json").write_text(
                json.dumps(record, indent=2) + "\n"
            )
            proposal_records.append(record)
            result = {
                "status": "blocked",
                "stop_reason": "model-request-failed",
                "model": model,
                "proposal_budget": max_proposals,
                "unique_candidates_evaluated": len(seen_sources),
                "training_hit_rate": None,
                "scoped_pass_rate": None,
                "repository_baseline": {
                    "status": baseline["status"],
                    "report_path": "repository-baseline-training/result.json",
                },
                "controls": {
                    suite: {
                        "status": control["status"],
                        "report_path": f"control-{suite}/result.json",
                    }
                    for suite, control in controls.items()
                },
                "proposals": proposal_records,
            }
            (output / "result.json").write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n"
            )
            return result
        if response_error is not None or completion is None:
            response_path = proposal_dir / "raw-response.txt"
            response_path.write_text(response_body, encoding="utf-8")
            record = {
                "attempt": attempt,
                "status": "rejected",
                "reason": response_error or "local model returned no completion",
                "prompt_sha256": _sha256(prompt_bytes),
                "response_path": response_path.relative_to(output).as_posix(),
            }
            (proposal_dir / "rejection.json").write_text(
                json.dumps(record, indent=2) + "\n"
            )
            proposal_records.append(record)
            failures.append(record["reason"])
            continue
        completion_bytes = completion.encode("utf-8")
        (proposal_dir / "completion.txt").write_bytes(completion_bytes)
        raw_response_path = proposal_dir / "raw-response.txt"
        raw_response_path.write_text(
            response_body, encoding="utf-8"
        )
        raw_response_relative = raw_response_path.relative_to(output).as_posix()
        try:
            try:
                proposal = json.loads(completion)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "local model completion is not valid JSON"
                ) from exc
            if not isinstance(proposal, dict):
                raise TypeError("local model completion must be a JSON object")
            if set(proposal) != set(ROUTINES):
                raise ValueError(
                    "local model completion must contain exactly the required routine keys"
                )
            sources = {
                routine: _validate_candidate_source(routine, proposal[routine])
                for routine in ROUTINES
            }
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            record = {
                "attempt": attempt,
                "status": "rejected",
                "reason": str(exc),
                "prompt_sha256": _sha256(prompt_bytes),
                "completion_sha256": _sha256(completion_bytes),
                "completion_path": (proposal_dir / "completion.txt").relative_to(output).as_posix(),
                "raw_response_path": raw_response_relative,
            }
            (proposal_dir / "rejection.json").write_text(
                json.dumps(record, indent=2) + "\n"
            )
            proposal_records.append(record)
            failures.append(str(exc))
            continue
        identity = _sha256(
            "\n".join(sources[routine] for routine in ROUTINES).encode("utf-8")
        )
        if identity in seen_sources:
            record = {
                "attempt": attempt,
                "status": "rejected",
                "reason": "duplicate candidate source",
                "prompt_sha256": _sha256(prompt_bytes),
                "completion_sha256": _sha256(completion_bytes),
                "candidate_sha256": identity,
                "completion_path": (proposal_dir / "completion.txt").relative_to(output).as_posix(),
                "raw_response_path": raw_response_relative,
            }
            (proposal_dir / "rejection.json").write_text(
                json.dumps(record, indent=2) + "\n"
            )
            proposal_records.append(record)
            failures.append("previous candidate source was duplicated")
            continue
        seen_sources.add(identity)
        try:
            candidate_report = run_probe(
                output / f"candidate-{attempt:03d}-training",
                root,
                suite="training",
                candidate_sources=sources,
            )
        except subprocess.CalledProcessError as exc:
            record = {
                "attempt": attempt,
                "status": "rejected",
                "reason": "candidate failed to compile or execute",
                "candidate_sha256": identity,
                "prompt_sha256": _sha256(prompt_bytes),
                "completion_sha256": _sha256(completion_bytes),
                "completion_path": (proposal_dir / "completion.txt").relative_to(output).as_posix(),
                "raw_response_path": raw_response_relative,
                "return_code": exc.returncode,
                "candidate_directory": f"candidate-{attempt:03d}-training",
            }
            (proposal_dir / "rejection.json").write_text(
                json.dumps(record, indent=2) + "\n"
            )
            proposal_records.append(record)
            failures.append(record["reason"])
            continue
        candidate_record = {
            "attempt": attempt,
            "status": candidate_report["status"],
            "training_status": candidate_report["status"],
            "candidate_sha256": identity,
            "prompt_sha256": _sha256(prompt_bytes),
            "completion_sha256": _sha256(completion_bytes),
            "completion_path": (proposal_dir / "completion.txt").relative_to(output).as_posix(),
            "raw_response_path": raw_response_relative,
            "training_report_path": f"candidate-{attempt:03d}-training/result.json",
        }
        if candidate_report["status"] == "passed":
            validate_saved_report(
                output / f"candidate-{attempt:03d}-training", root
            )
            if "heldout" not in controls:
                heldout_control = run_probe(
                    output / "control-heldout",
                    root,
                    suite="heldout",
                    candidate_sources=positive_sources,
                )
                controls["heldout"] = heldout_control
                if heldout_control["status"] != "passed":
                    candidate_record["status"] = "heldout-control-failed"
                    candidate_record["heldout_control_status"] = "failed"
                    proposal_records.append(candidate_record)
                    result = {
                        "status": "blocked",
                        "stop_reason": "assembly-derived positive control failed heldout",
                        "model": model,
                        "repository_baseline": {
                            "status": baseline["status"],
                            "report_path": "repository-baseline-training/result.json",
                        },
                        "controls": {
                            suite: {
                                "status": control["status"],
                                "case_count": control["case_count"],
                                "report_path": f"control-{suite}/result.json",
                            }
                            for suite, control in controls.items()
                        },
                        "proposals": proposal_records,
                    }
                    (output / "result.json").write_text(
                        json.dumps(result, indent=2, sort_keys=True) + "\n"
                    )
                    return result
                validate_saved_report(output / "control-heldout", root)
            heldout_report = run_probe(
                output / f"candidate-{attempt:03d}-heldout",
                root,
                suite="heldout",
                candidate_sources=sources,
            )
            candidate_record["heldout_status"] = heldout_report["status"]
            candidate_record["heldout_report_path"] = (
                f"candidate-{attempt:03d}-heldout/result.json"
            )
            if heldout_report["status"] == "passed":
                validate_saved_report(
                    output / f"candidate-{attempt:03d}-heldout", root
                )
                best_candidate = candidate_record
                candidate_record["status"] = "passed"
                proposal_records.append(candidate_record)
                break
            candidate_record["status"] = "heldout-failed"
        else:
            failures = [
                f"{item['routine']} DI={item['destination']:#06x}: "
                + ", ".join(
                    key for key, passed in item["checks"].items() if not passed
                )
                for item in candidate_report["results"]
                if item["status"] != "passed"
            ]
        proposal_records.append(candidate_record)

    training_passes = sum(
        record.get("training_status") == "passed" for record in proposal_records
    )
    training_hit_rate = (
        training_passes / len(seen_sources) if seen_sources else None
    )
    scoped_passes = sum(record.get("status") == "passed" for record in proposal_records)
    scoped_pass_rate = scoped_passes / len(seen_sources) if seen_sources else None
    stop_reason = (
        "scoped-pass"
        if best_candidate
        else "yield-below-25-percent-floor"
        if training_hit_rate is not None and training_hit_rate < 0.25
        else "proposal-budget-exhausted"
    )
    result = {
        "status": "passed" if best_candidate else "failed",
        "stop_reason": stop_reason,
        "model": model,
        "proposal_budget": max_proposals,
        "unique_candidates_evaluated": len(seen_sources),
        "training_hit_rate": training_hit_rate,
        "scoped_pass_rate": scoped_pass_rate,
        "repository_baseline": {
            "status": baseline["status"],
            "report_path": "repository-baseline-training/result.json",
        },
        "controls": {
            suite: {
                "status": report["status"],
                "case_count": report["case_count"],
                "report_path": f"control-{suite}/result.json",
            }
            for suite, report in controls.items()
        },
        "proposals": proposal_records,
        "best_candidate": best_candidate,
        "limitations": [
            "No candidate is promoted to the recovery ledger or knowledge store.",
            "Results cover only the fixed six-word copy fixtures, not universal routine behavior.",
        ],
    }
    (output / "result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--model", default="deepseek-coder:6.7b")
    parser.add_argument("--endpoint", default="http://localhost:11434")
    parser.add_argument("--max-proposals", type=int, default=4)
    arguments = parser.parse_args()
    result = run_trial(
        arguments.output,
        model=arguments.model,
        endpoint=arguments.endpoint,
        max_proposals=arguments.max_proposals,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
