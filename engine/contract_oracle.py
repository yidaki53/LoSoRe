"""Decomp/contract-derived original-trace oracle for safe Liero routines."""

from __future__ import annotations

import hashlib
import json
import pathlib
import random
import re
import shutil
import struct
import subprocess
from typing import Any

from engine import target_packet
from tools import liero_four_routine_pilot as pilot
from tools import liero_source_trial as trial
from tools.liero_file_probe import assemble_probe, run_dosbox

ARENA = 4096
CASE_BYTES = 8 + ARENA
RECORD_BYTES = 32 + ARENA
_UNSAFE = re.compile(
    r"\b(CALLF?|INT|INTO|IN|OUT|J[A-Z]{1,5}|LOOP\w*|JCXZ|JECXZ|IRET)\b", re.I
)
_ABSOLUTE = re.compile(r"\[(?:0x)?[0-9a-f]{4,}\]", re.I)
_RET = re.compile(r"\b(RETF|RET)(?:\s+(?:0x)?([0-9a-f]+))?\b", re.I)
_DECL = re.compile(
    r"^(procedure|function)\s+(\w+)"
    r"(?:\s*\((.*)\))?"
    r"\s*(?::\s*([\w^]+))?\s*;$",
    re.I,
)
_SIZES = {
    "byte": 2,
    "char": 2,
    "integer": 2,
    "word": 2,
    "boolean": 2,
    "longint": 4,
    "pointer": 2,
    "pbyte": 2,
}
_POINTERS = {"pointer", "pbyte"}


def _contract(root: pathlib.Path, target: str, routine: str) -> dict[str, Any]:
    if target != "liero":
        raise ValueError("contract oracle supports only liero")
    path = root / "targets" / target / "config" / "routine_contracts.json"
    data = json.loads(path.read_text())
    contract = data.get("functions", {}).get(routine)
    if not isinstance(contract, dict):
        raise ValueError(f"no checked contract for routine: {routine}")
    return contract


def _declaration(root: pathlib.Path, target: str, routine: str) -> str:
    contract = _contract(root, target, routine)
    declaration = contract.get("declaration")
    if not isinstance(declaration, str):
        raise ValueError(f"contract declaration missing for routine: {routine}")
    if not _DECL.fullmatch(declaration.strip()):
        raise ValueError(f"unsupported contract declaration: {declaration}")
    path = root / "targets" / target / "decomp" / f"{routine}.c"
    decomp = path.read_text(errors="replace")
    if routine not in decomp:
        raise ValueError(f"decompilation does not contain routine: {routine}")
    return declaration.strip()


def _parse_declaration(declaration: str) -> dict[str, Any]:
    match = _DECL.fullmatch(declaration.strip())
    if match is None:
        raise ValueError(f"unsupported contract declaration: {declaration}")
    kind, name, params_text, return_text = match.groups()
    params = []
    if params_text and params_text.strip():
        for group in params_text.split(";"):
            names_text, type_text = (part.strip() for part in group.split(":", 1))
            type_name = type_text.lower().strip()
            if type_name not in _SIZES:
                raise ValueError(f"unsupported contract parameter type: {type_text}")
            for param_name in (part.strip() for part in names_text.split(",")):
                if not re.fullmatch(r"\w+", param_name):
                    raise ValueError(f"unsupported contract parameter name: {param_name}")
                params.append({"name": param_name, "type": type_name})
    return_type = None
    if kind.lower() == "function":
        return_type = (return_text or "").lower().strip() or "word"
        if return_type not in _SIZES:
            raise ValueError(f"unsupported contract return type: {return_text}")
    return {
        "kind": kind.lower(),
        "name": name,
        "params": params,
        "return_type": return_type,
    }


def fixture(root: pathlib.Path, target: str, routine: str) -> dict[str, Any]:
    declaration = _declaration(root, target, routine)
    parsed = _parse_declaration(declaration)
    asm_path = root / "targets" / target / "asm" / f"{routine}.s"
    asm = asm_path.read_text(errors="replace")
    if _UNSAFE.search(asm) or _ABSOLUTE.search(asm):
        raise ValueError(f"routine is not a safe contract-oracle leaf: {routine}")
    returns = _RET.findall(asm)
    if len(returns) != 1 or len(re.findall(r"\bRET(?:F)?\b", asm, re.I)) != 1:
        raise ValueError(f"contract oracle requires one return: {routine}")
    near = returns[0][0].upper() == "RET"
    cleanup = int(returns[0][1], 16) if returns[0][1] else 0
    evidence = target_packet.evidence_for_routine(root, target, routine)
    raw = bytes.fromhex(evidence["bytes"]["hex"])
    if not raw:
        raise ValueError(f"contract oracle routine has no bytes: {routine}")
    args_bytes = sum(_SIZES[item["type"]] for item in parsed["params"])
    return {
        "target": target,
        "routine": routine,
        "declaration": declaration,
        "kind": parsed["kind"],
        "name": parsed["name"],
        "params": parsed["params"],
        "return_type": parsed["return_type"],
        "args_bytes": args_bytes,
        "bytes": raw.hex(),
        "bytes_sha256": hashlib.sha256(raw).hexdigest(),
        "near": near,
        "cleanup": cleanup,
    }


def supported(root: pathlib.Path, target: str, routine: str) -> bool:
    try:
        fixture(root, target, routine)
    except Exception:
        return False
    return True


def cases(fixture_data: dict[str, Any], suite: str) -> list[bytes]:
    if suite not in {"training", "terminal"}:
        raise ValueError(f"unknown suite: {suite}")
    rng = random.Random(20261123 + (suite == "terminal"))
    result: list[bytes] = []
    for _ in range(56):
        words = [rng.randrange(65536) for _ in range(4)]
        for arg in fixture_data["params"]:
            if arg["type"] in _POINTERS:
                index = len(result) % 4
                words[index] = 0x8200 + rng.randrange(128)
        flags = rng.randrange(65536)
        arena = bytearray(flags.to_bytes(2, "little")) + bytearray(rng.randbytes(ARENA - 2))
        result.append(struct.pack("<4H", *words) + bytes(arena))
    return result


def corpus_hash(fixture_data: dict[str, Any], suite: str) -> str:
    return hashlib.sha256(b"".join(cases(fixture_data, suite))).hexdigest()


def _word_at(data: bytes, index: int) -> int:
    if index < 4:
        return struct.unpack_from("<H", data, index * 2)[0]
    offset = 8 + (index - 4) * 2
    if offset + 2 > len(data):
        raise ValueError("contract case has too few argument words")
    return struct.unpack_from("<H", data, offset)[0]


def _argument_values(fixture_data: dict[str, Any], data: bytes) -> list[tuple[int, str]]:
    values = []
    index = 0
    for arg in fixture_data["params"]:
        type_name = arg["type"]
        if type_name == "longint":
            low = _word_at(data, index)
            high = _word_at(data, index + 1)
            index += 2
            values.append((low | (high << 16), type_name))
            continue
        value = _word_at(data, index)
        index += 1
        if type_name in _POINTERS:
            if not 0x8000 <= value <= 0x9000 - 32:
                raise ValueError("contract pointer argument outside owned arena")
        values.append((value, type_name))
    return values


def _push_args(values: list[tuple[int, str]]) -> str:
    lines = []
    for value, type_name in reversed(values):
        if type_name in _POINTERS:
            lines.append("push %cs")
            lines.append(f"pushw ${value}")
        elif type_name == "longint":
            lines.append(f"pushw ${(value >> 16) & 0xffff}")
            lines.append(f"pushw ${value & 0xffff}")
        else:
            lines.append(f"pushw ${value & 0xffff}")
    return "\n    ".join(lines)


def _call_arg(value: int, type_name: str) -> str:
    if type_name in _POINTERS:
        return f"@arena[{value} - $8000]"
    if type_name == "longint":
        return f"LongInt({value})"
    if type_name == "byte":
        return f"Byte({value} and $ff)"
    if type_name == "char":
        return f"Chr({value} and $ff)"
    return f"Word({value} and $ffff)"


def harness(fixture_data: dict[str, Any]) -> str:
    sample = cases(fixture_data, "training")[0]
    raw = ", ".join(
        "0x" + fixture_data["bytes"][index:index + 2]
        for index in range(0, len(fixture_data["bytes"]), 2)
    )
    return_bytes = 2 if fixture_data["near"] else 4
    call_prefix = "" if fixture_data["near"] else "push %cs"
    caller_cleanup = 0 if fixture_data["cleanup"] else fixture_data["args_bytes"]
    return f""".code16
.global _start
_start:
    push %cs
    pop %ds
    push %cs
    pop %es
    cli
    push %cs
    pop %ss
    mov $0xeff0, %sp
    sti
    cld
    mov $input_name, %dx
    mov $0x3d00, %ax
    int $0x21
    jc failed
    mov %ax, input_handle
    mov $output_name, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, output_handle
next_case:
    cld
    mov $0xeff0, %sp
    mov input_handle, %bx
    mov $input, %dx
    mov ${CASE_BYTES}, %cx
    mov $0x3f00, %ax
    int $0x21
    jc failed
    or %ax, %ax
    jz finished
    cmp ${CASE_BYTES}, %ax
    jne failed
    mov $input+8, %si
    mov $0x8000, %di
    mov ${ARENA}, %cx
    rep movsb
    movw $0x1357, %ss:0xeff0
    movw $0x2468, %ss:0xeff2
{_push_args(_argument_values(fixture_data, sample))}
    mov %sp, %ax
    sub ${return_bytes}, %ax
    mov %ax, snapshot+14
    mov $0x6789, %bp
    mov input+2, %bx
    mov input+4, %cx
    mov input+6, %dx
    mov input+2, %si
    mov input+4, %di
    mov input+8, %ax
    or $0x202, %ax
    push %ax
    popf
    mov input, %ax
    {call_prefix}
    call original
    add ${caller_cleanup}, %sp
    mov %ax, snapshot
    mov %bx, snapshot+2
    mov %cx, snapshot+4
    mov %dx, snapshot+6
    mov %si, snapshot+8
    mov %di, snapshot+10
    mov %bp, snapshot+12
    mov %sp, snapshot+16
    mov %ds, snapshot+18
    mov %es, snapshot+20
    mov %ss, snapshot+22
    pushf
    popw snapshot+24
    mov %ss:0xeff0, %ax
    mov %ax, snapshot+26
    mov %ss:0xeff2, %ax
    mov %ax, snapshot+28
    mov %cs, %ax
    mov %ax, snapshot+30
    cld
    mov $0x8000, %si
    mov $snapshot+32, %di
    mov ${ARENA}, %cx
    rep movsb
    mov output_handle, %bx
    mov $snapshot, %dx
    mov ${RECORD_BYTES}, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp ${RECORD_BYTES}, %ax
    jne failed
    jmp next_case
finished:
    mov output_handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21
input_name: .asciz "CASES.BIN"
output_name: .asciz "TRACE.BIN"
input_handle: .word 0
output_handle: .word 0
original: .byte {raw}
input: .space {CASE_BYTES}
snapshot: .space {RECORD_BYTES}
"""


def program(fixture_data: dict[str, Any]) -> str:
    values = _argument_values(fixture_data, cases(fixture_data, "training")[0])
    args = ", ".join(_call_arg(value, type_name) for value, type_name in values)
    call = f"{fixture_data['name']}({args});" if args else f"{fixture_data['name']};"
    if fixture_data["kind"] == "function":
        call = f"contractResult := LongInt({fixture_data['name']}({args}));"
    return_bytes = 2 if fixture_data["near"] else 4
    return f"""program ContractTrial;
uses LieroRuntime;
{{$I candidate.inc}}
var arena: array[0..4095] of Byte;
    input: array[0..3] of Word; row: array[0..15] of Word;
    inputFile, outputFile: file; transferred: LongInt;
    entry: Word; contractResult: LongInt; flagsWord: Word;
begin
  if SizeOf(Integer) <> 2 then Halt(1);
  Assign(inputFile, 'CASES.BIN'); Reset(inputFile, 1);
  Assign(outputFile, 'PASCAL.BIN'); Rewrite(outputFile, 1);
  while not Eof(inputFile) do
  begin
    BlockRead(inputFile, input, 8, transferred);
    if transferred <> 8 then Halt(2);
    BlockRead(inputFile, arena, 4096, transferred);
    if transferred <> 4096 then Halt(3);
    entry := $eff0 - {fixture_data['args_bytes']} - {return_bytes};
    RegisterAX := input[0]; RegisterBX := input[1];
    RegisterCX := input[2]; RegisterDX := input[3];
    RegisterSI := input[1]; RegisterDI := input[2];
    RegisterSP := entry; RegisterBP := $6789;
    RegisterDS := $2000; RegisterES := $2000; RegisterSS := $2000;
    flagsWord := Word(arena[0]) or (Word(arena[1]) shl 8);
    RegisterCarryFlag := (flagsWord and 1) <> 0;
    RegisterZeroFlag := (flagsWord and $40) <> 0;
    RegisterDirectionFlag := (flagsWord and $400) <> 0;
    {call}
    row[0] := RegisterAX; row[1] := RegisterBX; row[2] := RegisterCX;
    row[3] := RegisterDX; row[4] := RegisterSI; row[5] := RegisterDI;
    row[6] := RegisterBP; row[7] := entry; row[8] := RegisterSP;
    row[9] := RegisterDS; row[10] := RegisterES; row[11] := RegisterSS;
    row[12] := Word(RegisterCarryFlag) + Word(RegisterZeroFlag) * $40 +
      Word(RegisterDirectionFlag) * $400;
    row[13] := $1357; row[14] := $2468; row[15] := $2000;
    BlockWrite(outputFile, row, 32, transferred);
    if transferred <> 32 then Halt(4);
    BlockWrite(outputFile, arena, 4096, transferred);
    if transferred <> 4096 then Halt(5);
  end;
  Close(inputFile); Close(outputFile);
end.
"""


def compile_candidate(
    root: pathlib.Path,
    output: pathlib.Path,
    fixture_data: dict[str, Any],
    source: str,
) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    (output / "candidate.inc").write_text(source)
    (output / "probe.pas").write_text(program(fixture_data))
    command = [
        "fpc",
        "-Mtp",
        "-Cr",
        f"-Fu{root.resolve() / 'targets/liero/src'}",
        "-FU.",
        "probe.pas",
    ]
    result = subprocess.run(
        command, cwd=output, capture_output=True, timeout=30, check=False
    )
    (output / "compile.log").write_bytes(result.stdout + result.stderr)
    return {
        "status": "passed" if result.returncode == 0 else "compile-failed",
        "returncode": result.returncode,
    }


def original(
    output: pathlib.Path,
    fixture_data: dict[str, Any],
    inputs: list[bytes],
) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    (output / "harness.S").write_text(harness(fixture_data))
    image = assemble_probe(output / "harness.S", output)
    raw = bytes.fromhex(fixture_data["bytes"])
    if image.count(raw) != 1:
        raise ValueError("contract-original routine bytes missing or duplicated")
    if len(image) + 0x100 >= 0x6000:
        raise ValueError("contract-original harness overlaps protected arena")
    (output / "PROBE.COM").write_bytes(image)
    (output / "CASES.BIN").write_bytes(b"".join(inputs))
    run_dosbox(output)
    trace = (output / "TRACE.BIN").read_bytes()
    if len(trace) != len(inputs) * RECORD_BYTES:
        raise ValueError("contract-original trace has wrong length")
    result = {"status": "passed", "cases": len(inputs)}
    pilot.save(output / "result.json", result)
    return result


def run_candidate(
    output: pathlib.Path,
    fixture_data: dict[str, Any],
    inputs: list[bytes],
    original_trace: bytes,
) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    (output / "CASES.BIN").write_bytes(b"".join(inputs))
    try:
        result = subprocess.run(
            [str(output / "probe")],
            cwd=output,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        (output / "runtime.log").write_bytes((error.stdout or b"") + (error.stderr or b""))
        return {"status": "runtime-timeout"}
    (output / "runtime.log").write_bytes(result.stdout + result.stderr)
    if result.returncode:
        return {"status": "runtime-failed", "returncode": result.returncode}
    trace = (output / "PASCAL.BIN").read_bytes()
    return compare(original_trace, trace)


def compare(original_trace: bytes, candidate_trace: bytes) -> dict:
    if len(original_trace) != len(candidate_trace) or len(original_trace) % RECORD_BYTES:
        raise ValueError("partial or extra contract-oracle output")
    checked = (0, 2, 4, 6, 8, 10, 12, 14, 24, 26, 28)
    failures = []
    count = len(original_trace) // RECORD_BYTES
    for index in range(count):
        start = index * RECORD_BYTES
        original = bytearray(original_trace[start:start + RECORD_BYTES])
        candidate = bytearray(candidate_trace[start:start + RECORD_BYTES])
        differences = []
        for offset in checked:
            if offset == 24:
                mask = 0x441
                left = struct.unpack_from("<H", original, offset)[0] & mask
                right = struct.unpack_from("<H", candidate, offset)[0] & mask
                if left != right:
                    differences.append(offset)
            elif original[offset:offset + 2] != candidate[offset:offset + 2]:
                differences.append(offset)
        if original[14:16] != candidate[16:18]:
            differences.append(16)
        if original[32:] != candidate[32:]:
            differences.append(32)
        if differences:
            failures.append({"case": index, "first_different_bytes": differences[:12]})
    return {
        "status": "failed" if failures else "passed",
        "cases": count,
        "matches": count - len(failures),
        "failures": failures,
    }


def run(
    root: pathlib.Path,
    output: pathlib.Path,
    source_path: pathlib.Path,
    routine: str,
    suites: tuple[str, ...] = ("training", "terminal"),
) -> dict:
    root_path = pathlib.Path(root)
    source = pathlib.Path(source_path).read_text()
    fixture_data = fixture(root_path, "liero", routine)
    output = pathlib.Path(output)
    output.mkdir(parents=True, exist_ok=False)
    result: dict[str, Any] = {
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "source_path": str(pathlib.Path(source_path).resolve()),
        "compile": {"status": "pending"},
        "suites": {},
    }
    pilot.save(output / "freeze.json", {
        "routine": routine,
        "source_sha256": result["source_sha256"],
        "fixture_sha256": fixture_data["bytes_sha256"],
        "corpora": {suite: corpus_hash(fixture_data, suite) for suite in suites},
        "policy": "training first, terminal once only if training passes",
        "budget": "no model requests, no repair, no source promotion",
    })
    pilot.save(output / "result.json", result)
    result["compile"] = compile_candidate(
        root_path, output / "candidate", fixture_data, source
    )
    pilot.save(output / "result.json", result)
    if result["compile"]["status"] != "passed":
        return result
    for suite in suites:
        inputs = cases(fixture_data, suite)
        original_dir = output / f"original-{suite}"
        original_result = original(original_dir, fixture_data, inputs)
        original_trace = (original_dir / "TRACE.BIN").read_bytes()
        candidate_dir = output / f"candidate-{suite}"
        candidate_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output / "candidate" / "probe", candidate_dir / "probe")
        candidate_result = run_candidate(
            candidate_dir, fixture_data, inputs, original_trace
        )
        result["suites"][suite] = {
            "original": original_result,
            "candidate": candidate_result,
        }
        pilot.save(output / "result.json", result)
        if suite == "training" and candidate_result["status"] != "passed":
            break
    return result


def run_training(
    root: pathlib.Path,
    output: pathlib.Path,
    source_path: pathlib.Path,
    routine: str,
) -> dict:
    return run(root, output, source_path, routine, suites=("training",))
