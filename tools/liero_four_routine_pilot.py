"""Bounded local-model pilot using four existing Liero binary-backed probes."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import re
import shutil
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine import knowledge
from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.instruction_facts import (
    allocator_empty_list_contract,
    bounded_byte_fill_contract,
    bounded_shortstring_contract,
    initialization_prefix,
)
from engine.recovery import audit_target
from tools import liero_compare_routine_probe as compare
from tools import liero_constructor_probe as constructor
from tools import liero_file_probe as file_probe
from tools import liero_read_handler_probe as handler

PANEL = {
    "constructor": ("FUN_24dd_3639", 0x3639, 83),
    "comparator": ("FUN_24dd_3f86", 0x3F86, 43),
    "read": ("FUN_24dd_375e", 0x375E, 48),
    "close": ("FUN_24dd_37d3", 0x37D3, 25),
}
LEAF_PANEL = {
    "FUN_24dd_4905": (0x4905, 20),
    "FUN_24dd_3b22": (0x3B22, 59),
}
FILL_SKETCH_SCHEMA = {
    "type": "object",
    "properties": {
        "loop_kind": {"type": "string", "enum": ["for", "while"]},
        "guard_zero": {"type": "boolean"},
        "first_index": {"type": "integer", "enum": [0, 1]},
        "end_expression": {"type": "string", "enum": ["count_minus_one", "count"]},
        "stored_value": {"type": "string", "enum": ["value", "zero"]},
    },
    "required": [
        "loop_kind",
        "guard_zero",
        "first_index",
        "end_expression",
        "stored_value",
    ],
    "additionalProperties": False,
}
STRING_SKETCH_SCHEMA = {
    "type": "object",
    "properties": {
        "loop_kind": {"type": "string", "enum": ["for", "while"]},
        "prefix": {"type": "string", "enum": ["byte_contract", "zero_all"]},
        "maximum_text_bytes": {"type": "integer", "enum": [79, 80, 255]},
        "text_destination_offset": {"type": "integer", "enum": [48, 0]},
        "source_text_offset": {"type": "integer", "enum": [1, 0]},
        "stop_at_nul": {"type": "boolean"},
    },
    "required": [
        "loop_kind",
        "prefix",
        "maximum_text_bytes",
        "text_destination_offset",
        "source_text_offset",
        "stop_at_nul",
    ],
    "additionalProperties": False,
}
DRAW_SKETCH_SCHEMA = {
    "type": "object",
    "properties": {
        "guard_style": {"type": "string", "enum": ["early_exit", "nested"]},
        "skip_zero": {"type": "boolean"},
        "stride": {"type": "integer", "enum": [158, 320]},
        "coordinate_order": {"type": "string", "enum": ["row_column", "column_row"]},
        "maximum_coordinate": {"type": "integer", "enum": [157, 158]},
    },
    "required": [
        "guard_style",
        "skip_zero",
        "stride",
        "coordinate_order",
        "maximum_coordinate",
    ],
    "additionalProperties": False,
}


def render_draw_sketch(sketch: dict, original: bytes) -> str:
    """Oracle: known62-byte shape plus supplied nonwrapping memory topology, not recovery."""
    if original != bytes.fromhex(
        "5589e5804e0a0074318b5e0c8b4e0e83f9007c2681f99d007f2083fb007c1b"
        "81fb9d007f15c47e06c1e30601dfc1e30201df01cf8a460a268805c9ca0a00"
    ):
        raise ValueError("drawing original-byte shape differs")
    if (
        not isinstance(sketch, dict)
        or set(sketch) != set(DRAW_SKETCH_SCHEMA["required"])
        or sketch["guard_style"] not in ("early_exit", "nested")
        or type(sketch["skip_zero"]) is not bool
        or sketch["skip_zero"] is not True
        or type(sketch["stride"]) is not int
        or sketch["stride"] != 320
        or sketch["coordinate_order"] != "row_column"
        or type(sketch["maximum_coordinate"]) is not int
        or sketch["maximum_coordinate"] != 157
    ):
        raise ValueError(
            "drawing sketch conflicts with closed vocabulary/byte contract"
        )
    lines = [
        "{ Oracle: supplied nonwrapping drawing projection; scoped parity required. }",
        "procedure FUN_1ec2_0dc8(param_1: Longint; param_2: Char; param_3, param_4: Integer);",
        "var pixelAddress: Longint;",
        "begin",
    ]
    if sketch["guard_style"] == "early_exit":
        lines += [
            "  if (param_2 = #0) or (param_3 < 0) or (param_3 > 157) or",
            "     (param_4 < 0) or (param_4 > 157) then Exit;",
        ]
        indent = "  "
    else:
        lines += [
            "  if (param_2 <> #0) and (param_3 >= 0) and (param_3 <= 157) and",
            "     (param_4 >= 0) and (param_4 <= 157) then",
            "  begin",
        ]
        indent = "    "
    lines += [
        f"{indent}pixelAddress := param_1 + Longint(param_3) * 320 + param_4;",
        f"{indent}RealModeMemory[pixelAddress] := Byte(param_2);",
    ]
    if sketch["guard_style"] == "nested":
        lines.append("  end;")
    return "\n".join([*lines, "end;", ""])


def validate_draw_candidate(source: str, sketch: dict, original: bytes) -> None:
    """Oracle: execute only exact closed-renderer output under caller-proven arena bounds.

    This is not a safety checker for arbitrary Pascal or unknown input pointers.
    """
    if source != render_draw_sketch(sketch, original):
        raise ValueError("drawing candidate differs from exact rendered source")


def render_shortstring_sketch(sketch: dict, routine: str, contract: dict) -> str:
    """Oracle: supplied typed composition; semantics must agree with exact original bytes."""
    if (
        routine != "FUN_24dd_3b22"
        or not isinstance(sketch, dict)
        or set(sketch) != set(STRING_SKETCH_SCHEMA["required"])
        or any(
            type(sketch[name]) is not int or sketch[name] not in spec["enum"]
            for name, spec in STRING_SKETCH_SCHEMA["properties"].items()
            if spec["type"] == "integer"
        )
        or type(sketch["stop_at_nul"]) is not bool
        or sketch["loop_kind"] not in ("for", "while")
        or sketch["prefix"] not in ("byte_contract", "zero_all")
    ):
        raise ValueError("invalid typed shortstring sketch")
    if (
        contract
        != bounded_shortstring_contract(bytes.fromhex(contract["routine_bytes_hex"]))
        or sketch["prefix"] != "byte_contract"
        or not sketch["stop_at_nul"]
        or any(
            sketch[name] != contract[name]
            for name in (
                "maximum_text_bytes",
                "text_destination_offset",
                "source_text_offset",
            )
        )
    ):
        raise ValueError("shortstring sketch conflicts with exact byte contract")
    lines = [
        "{ Oracle: supplied typed composition; scoped original-memory comparison required. }",
        leaf_interface(routine),
        "var index, count, copied: LongInt;",
        "begin",
    ]
    for write in contract["prefix_writes"]:
        begin = write["byte_offset"]
        count = write["word_count"]
        value = write["value"]["amount"]
        if count == 1:
            lines += [
                f"  destination^[{begin}] := {value & 255};",
                f"  destination^[{begin + 1}] := {value >> 8};",
            ]
        elif count:
            lines += [
                f"  for index := 0 to {count - 1} do",
                "  begin",
                f"    destination^[{begin} + index * 2] := {value & 255};",
                f"    destination^[{begin + 1} + index * 2] := {value >> 8};",
                "  end;",
            ]
    limit = contract["maximum_text_bytes"]
    destination = contract["text_destination_offset"]
    source = contract["source_text_offset"]
    lines += [
        "  count := source^[0];",
        f"  if count > {limit} then count := {limit};",
        "  copied := 0;",
    ]
    if sketch["loop_kind"] == "for":
        lines += ["  for index := 0 to count - 1 do", "  begin"]
    else:
        lines += ["  index := 0;", "  while index < count do", "  begin"]
    lines += [
        f"    if source^[{source} + index] = 0 then Break;",
        f"    destination^[{destination} + index] := source^[{source} + index];",
        "    Inc(copied);",
    ]
    if sketch["loop_kind"] == "while":
        lines.append("    Inc(index);")
    return "\n".join(
        [*lines, "  end;", f"  destination^[{destination} + copied] := 0;", "end;", ""]
    )


def render_fill_sketch(sketch: dict, routine: str) -> str:
    """Oracle: typed supplied loop topology, not a model-authored Pascal source body."""
    if not re.fullmatch(r"FUN_[0-9a-f]{4}_[0-9a-f]{4}", routine):
        raise ValueError("invalid fill sketch routine name")
    if (
        not isinstance(sketch, dict)
        or set(sketch) != set(FILL_SKETCH_SCHEMA["required"])
        or type(sketch["guard_zero"]) is not bool
        or type(sketch["first_index"]) is not int
        or sketch["first_index"] not in (0, 1)
        or any(
            sketch[field] not in FILL_SKETCH_SCHEMA["properties"][field]["enum"]
            for field in ("loop_kind", "end_expression", "stored_value")
        )
    ):
        raise ValueError("invalid fill sketch fields or vocabulary")
    limit = (
        "LongInt(count) - 1"
        if sketch["end_expression"] == "count_minus_one"
        else "LongInt(count)"
    )
    value = "value" if sketch["stored_value"] == "value" else "0"
    lines = [
        "{ Oracle: model-selected typed fill sketch; scoped memory parity required. }",
        f"procedure {routine}(destination: PBlock; count: Word; value: Byte);",
        "var index: LongInt;",
        "begin",
    ]
    indent = "  "
    if sketch["guard_zero"]:
        lines.extend(["  if count > 0 then", "  begin"])
        indent = "    "
    if sketch["loop_kind"] == "for":
        lines.extend(
            [
                f"{indent}for index := {sketch['first_index']} to {limit} do",
                f"{indent}  destination^[index] := {value};",
            ]
        )
    else:
        lines.extend(
            [
                f"{indent}index := {sketch['first_index']};",
                f"{indent}while index <= {limit} do",
                f"{indent}begin",
                f"{indent}  destination^[index] := {value};",
                f"{indent}  Inc(index);",
                f"{indent}end;",
            ]
        )
    if sketch["guard_zero"]:
        lines.append("  end;")
    return "\n".join([*lines, "end;", ""])


def validate_fill_sketch_contract(sketch: dict, contract: dict) -> None:
    """Oracle: exact REP STOSB argument bindings reject contradicting memory hypotheses."""
    if (
        contract.get("oracle") != "exact_byte_shape_under_scoped_far_call_preconditions"
        or contract.get("destination_far_pointer_slot") != 8
        or contract.get("count_word_slot") != 6
        or contract.get("value_low_byte_slot") != 4
        or sketch["first_index"] != 0
        or sketch["end_expression"] != "count_minus_one"
        or sketch["stored_value"] != "value"
    ):
        raise ValueError(
            "fill sketch conflicts with the exact byte contract/host interface"
        )


class LeafCandidateExecutionError(RuntimeError):
    """Oracle: a compiled candidate failed bounded training execution, never a pass."""


def leaf_cases(routine: str, suite: str) -> list[tuple[str, bytes]]:
    """Oracle: frozen disjoint dirty-memory corpora; no model-dependent cases."""
    if routine not in LEAF_PANEL or suite not in {"training", "heldout"}:
        raise ValueError("unknown leaf routine or corpus")
    seeds = (0, 255) if suite == "training" else (165,)
    cases = []
    for seed in seeds:
        for length in range(257 if routine == "FUN_24dd_4905" else 256):
            data = bytearray([seed] * 544)
            if routine == "FUN_24dd_4905":
                struct.pack_into("<HB", data, 0, length, (length * 37 + seed) & 255)
            else:
                data[:256] = bytes([length]) + bytes(65 + i % 26 for i in range(255))
            cases.append((f"seed-{seed}-length-{length}", bytes(data)))
    if routine == "FUN_24dd_3b22" and suite == "heldout":
        for position in (0, 1, 2, 77, 78, 79, 80, 254):
            data = bytearray(cases[-1][1])
            data[position + 1] = 0
            cases.append((f"nul-{position}", bytes(data)))
    return cases


def leaf_stress_cases(spec: dict) -> list[tuple[str, bytes]]:
    """Oracle: frozen seeded training inputs; heldout payloads excluded without outcome feedback."""
    if (
        set(spec) != {"seed", "batch", "count"}
        or any(type(spec[key]) is not int for key in spec)
        or not 0 <= spec["seed"] < 2**32
        or not 0 <= spec["batch"] < 10000
        or not 1 <= spec["count"] <= 4096
    ):
        raise ValueError("invalid stress corpus descriptor")
    routine = "FUN_24dd_3b22"
    excluded = {data for _, data in leaf_cases(routine, "heldout")}
    generator = random.Random((spec["seed"] << 32) + spec["batch"])
    cases = []
    for index in range(spec["count"]):
        data = bytearray(generator.randbytes(544))
        data[0] = index % 256
        # Systematically exercise terminator before/at/after the 79-byte clamp.
        position = (0, 1, 77, 78, 79, 254, None)[(index // 256 + spec["batch"]) % 7]
        data[1:256] = bytes(generator.randrange(1, 256) for _ in range(255))
        if position is not None:
            data[1 + position] = 0
        struct.pack_into("<II", data, 536, spec["batch"], index)
        if bytes(data) in excluded:
            raise ValueError("stress training input overlaps frozen heldout payload")
        cases.append((f"stress-{spec['batch']}-{index}", bytes(data)))
    return cases


def leaf_expected(routine: str, data: bytes) -> bytes:
    """Oracle: independently specified memory contract; not supplied as model source."""
    if routine not in LEAF_PANEL or len(data) != 544:
        raise ValueError("invalid leaf routine/input")
    result = bytearray(data)
    if routine == "FUN_24dd_4905":
        count = int.from_bytes(data[:2], "little")
        if count > 256:
            raise ValueError("leaf fill count exceeds bounded object")
        result[272 : 272 + count] = bytes([data[2]]) * count
    else:
        result[272:320] = b"\0\0\xb0\xd7" + bytes(44)
        text = data[1 : 1 + min(data[0], 79)].split(b"\0", 1)[0]
        result[320 : 321 + len(text)] = text + b"\0"
    return bytes(result)


def leaf_interface(routine: str) -> str:
    """Oracle: declared scoped host interface, not original TP7 ABI equivalence."""
    if routine == "FUN_24dd_4905":
        return f"procedure {routine}(destination: PBlock; count: Word; value: Byte);"
    if routine == "FUN_24dd_3b22":
        return f"procedure {routine}(source, destination: PBlock);"
    raise ValueError("unknown leaf routine")


def leaf_control_source(routine: str) -> str:
    """Oracle: disclosed manually known control; never used as generated candidate/seed."""
    if routine == "FUN_24dd_4905":
        body = (
            "var i: LongInt;\nbegin\n"
            "  if count > 0 then for i := 0 to count - 1 do destination^[i] := value;\n"
            "end;\n"
        )
    elif routine == "FUN_24dd_3b22":
        body = (
            "var i, count: LongInt;\nbegin\n"
            "  for i := 0 to 47 do destination^[i] := 0;\n"
            "  destination^[2] := $B0; destination^[3] := $D7;\n"
            "  count := source^[0]; if count > 79 then count := 79;\n"
            "  i := 0;\n"
            "  while i < count do begin\n"
            "    if source^[i + 1] = 0 then break;\n"
            "    destination^[48 + i] := source^[i + 1]; Inc(i);\n"
            "  end;\n"
            "  destination^[48 + i] := 0;\nend;\n"
        )
    else:
        raise ValueError("unknown leaf routine")
    return leaf_interface(routine) + "\n" + body


def _leaf_harness(routine: str) -> str:
    """Oracle: full original leaf bytes, fixed disjoint input/object, observed RETF 8."""
    offset = LEAF_PANEL[routine][0]
    arguments = (
        "    push %cs\n    push $0x6910\n"
        "    pushw 0x6800\n    xor %ax,%ax\n    movb 0x6802,%al\n    push %ax\n"
        if routine == "FUN_24dd_4905"
        else "    push %cs\n    push $0x6910\n    push %cs\n    push $0x6800\n"
    )
    return f""".code16
.global _start
_start:
    push %cs
    pop %ds
    mov $input_name,%dx
    mov $0x3d00,%ax
    int $0x21
    jc failed
    mov %ax,input_handle
    mov $output_name,%dx
    xor %cx,%cx
    mov $0x3c00,%ax
    int $0x21
    jc failed
    mov %ax,output_handle
next_case:
    mov input_handle,%bx
    mov $0x6800,%dx
    mov $544,%cx
    mov $0x3f00,%ax
    int $0x21
    jc failed
    or %ax,%ax
    jz finish
    cmp $544,%ax
    jne failed
    mov %sp,0x67fc
{arguments}    push %cs
    call 0x{offset:04x}
    mov %sp,%cs:0x67fe
    mov %ds,%ax
    mov %ax,%cs:0x67f8
    mov %ss,%ax
    mov %ax,%cs:0x67fa
    push %cs
    pop %ds
    mov %cs,%ax
    mov %ax,0x67f6
    mov case_index,%ax
    mov %ax,0x67f4
    incw case_index
    mov output_handle,%bx
    mov $0x67f4,%dx
    mov $556,%cx
    mov $0x4000,%ax
    int $0x21
    jc failed
    cmp $556,%ax
    jne failed
    jmp next_case
finish:
    mov input_handle,%bx
    mov $0x3e00,%ax
    int $0x21
    jc failed
    mov output_handle,%bx
    mov $0x3e00,%ax
    int $0x21
    jc failed
    mov $0x4c00,%ax
    int $0x21
failed:
    mov $0x4c01,%ax
    int $0x21
input_handle: .word 0
output_handle: .word 0
case_index: .word 0
input_name: .asciz "CASES.BIN"
output_name: .asciz "TRACE.BIN"
"""


def _leaf_program(routine: str) -> str:
    """Oracle: compile supplied include unchanged; copy/compare the complete input arena."""
    call = (
        f"{routine}(@data[272], data[0] + 256 * Word(data[1]), data[2]);"
        if routine == "FUN_24dd_4905"
        else f"{routine}(@data[0], @data[272]);"
    )
    return f"""program LeafProbe;
type TBlock = array[0..255] of Byte; PBlock = ^TBlock;
{{$I candidate.inc}}
var data: array[0..543] of Byte; inputFile, outputFile: file; count: LongInt;
begin
  Assign(inputFile, ParamStr(1)); Reset(inputFile, 1);
  Assign(outputFile, ParamStr(2)); Rewrite(outputFile, 1);
  while not Eof(inputFile) do begin
    BlockRead(inputFile, data, 544, count);
    if count <> 544 then Halt(1);
    {call}
    BlockWrite(outputFile, data, 544, count);
    if count <> 544 then Halt(1);
  end;
  Close(inputFile); Close(outputFile);
end.
"""


def run_leaf_probe(
    root: pathlib.Path,
    output: pathlib.Path,
    routine: str,
    source: str,
    suite: str,
    *,
    stress: dict | None = None,
) -> dict:
    """Oracle: finite original/actual Pascal/independent contract check; no installation."""
    if stress is not None and (routine != "FUN_24dd_3b22" or suite != "training"):
        raise ValueError("stress corpus only supports 3b22 training, never heldout")
    cases = leaf_cases(routine, suite) if stress is None else leaf_stress_cases(stress)
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "BYOD unavailable"}
    missing = [tool for tool in ("as", "ld", "dosbox", "fpc") if not shutil.which(tool)]
    if missing:
        raise FileNotFoundError("leaf probe requires: " + ", ".join(missing))
    prefix = prefix_transfer_report(root, routine)
    manifest = json.loads((root / "targets/liero/alternate_streams.json").read_text())
    binary = (root / "extracted/liero/LIERO.EXE").read_bytes()
    start, size = prefix["file_offset"], prefix["routine_size"]
    if any(
        start - 1 <= location < start + size
        for location in _mz_relocation_locations(
            binary, manifest["image_mapping"]["header_bytes"]
        )
    ):
        raise ValueError("leaf probe does not support relocated routine operands")
    output.mkdir(parents=True, exist_ok=False)
    (output / "candidate.inc").write_text(source)
    (output / "probe.pas").write_text(_leaf_program(routine))
    assembly = output / "harness.S"
    assembly.write_text(_leaf_harness(routine))
    harness = file_probe.assemble_probe(assembly, output)
    image = file_probe._build_image(
        harness,
        binary,
        manifest,
        [
            {
                "address": hex(0x24DD0 + LEAF_PANEL[routine][0]),
                "bytes_hex": prefix["routine_bytes_hex"],
            }
        ],
    )
    (output / "PROBE.COM").write_bytes(image)
    payload = b"".join(data for _, data in cases)
    (output / "CASES.BIN").write_bytes(payload)
    file_probe.run_dosbox(output)
    trace = (output / "TRACE.BIN").read_bytes()
    if len(trace) != 556 * len(cases):
        raise ValueError("leaf trace missing, partial or extra records")
    command = [
        "fpc",
        "-Mtp",
        "-Cr",
        f"-Fi{output}",
        f"-FU{output}",
        f"-o{output / 'probe'}",
        str(output / "probe.pas"),
    ]
    compiled = subprocess.run(command, capture_output=True, check=False, timeout=30)
    (output / "compile.log").write_bytes(compiled.stdout + compiled.stderr)
    compiled.check_returncode()
    runtime_command = [
        str(output / "probe"),
        str(output / "CASES.BIN"),
        str(output / "PASCAL.BIN"),
    ]
    try:
        runtime = subprocess.run(
            runtime_command, capture_output=True, timeout=30, check=False
        )
    except subprocess.TimeoutExpired as exc:
        save(
            output / "runtime.json",
            {
                "status": "failed",
                "reason": "candidate-timeout",
                "command": runtime_command,
            },
        )
        raise LeafCandidateExecutionError(
            "candidate exceeded its 30-second execution budget"
        ) from exc
    runtime_record = {
        "status": "passed" if runtime.returncode == 0 else "failed",
        "command": runtime_command,
        "returncode": runtime.returncode,
        "stdout": runtime.stdout.decode(errors="replace"),
        "stderr": runtime.stderr.decode(errors="replace"),
    }
    save(output / "runtime.json", runtime_record)
    if runtime.returncode:
        raise LeafCandidateExecutionError(
            "candidate runtime failure: " + json.dumps(runtime_record)
        )
    pascal = (output / "PASCAL.BIN").read_bytes()
    if len(pascal) != len(payload):
        raise ValueError("leaf Pascal output missing, partial or extra records")
    rows = _compare_leaf(routine, cases, trace, pascal)
    report = {
        "schema_version": 1,
        "function": routine,
        "suite": suite,
        "stress_corpus": stress,
        "status": "passed"
        if all(row["status"] == "passed" for row in rows)
        else "failed",
        "oracle": "isolated_original_vs_host_pascal_leaf_memory",
        "case_count": len(cases),
        "cases": rows,
        "binary_sha256": prefix["binary_sha256"],
        "routine_sha256": prefix["routine_sha256"],
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "probe_sha256": digest(root / "tools/liero_four_routine_pilot.py"),
        "evidence_hashes": _leaf_evidence_hashes(root, routine),
        "artifact_hashes": {
            str(path.relative_to(output)): digest(path)
            for path in output.iterdir()
            if path.is_file()
        },
        "limitations": [
            "Finite nonaliasing COM arena; not universal/source or normal-program acceptance.",
            "DS/SS/SP are original-only observations, not host TP7 ABI parity.",
            "Register/flag outputs are outside this memory contract.",
            "Manual control/reference topology disclosed; no training promotion.",
        ],
    }
    save(output / "result.json", report)
    return report


def _compare_leaf(
    routine: str, cases: list[tuple[str, bytes]], trace: bytes, pascal: bytes
) -> list[dict]:
    """Oracle: rederive all ordered memory differences and original-only ABI checks."""
    if len(trace) != 556 * len(cases) or len(pascal) != 544 * len(cases):
        raise ValueError("leaf outputs missing, partial or extra records")
    rows = []
    segment = None
    for index, (name, data) in enumerate(cases):
        record = trace[index * 556 : (index + 1) * 556]
        stage, cs, ds, ss, before, after = struct.unpack("<6H", record[:12])
        if (
            stage != index
            or not cs
            or cs != ds
            or cs != ss
            or before != after
            or before != 0xFFFE
            or segment is not None
            and cs != segment
        ):
            raise ValueError(f"leaf original ABI mismatch at {name}")
        segment = cs
        original = record[12:]
        candidate = pascal[index * 544 : (index + 1) * 544]
        expected = leaf_expected(routine, data)
        differences = [
            {
                "offset": pos,
                "original": left,
                "pascal": right,
                "contract": expected[pos],
            }
            for pos, (left, right) in enumerate(zip(original, candidate))
            if left != right or left != expected[pos]
        ]
        rows.append(
            {
                "case": name,
                "status": "failed" if differences else "passed",
                "differences": differences,
            }
        )
    return rows


def validate_leaf_probe(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: replay exact original/Pascal corpus under unchanged byte/probe identities."""
    report = json.loads((output / "result.json").read_text())
    prefix = prefix_transfer_report(root, report["function"])
    if (
        report["probe_sha256"] != digest(root / "tools/liero_four_routine_pilot.py")
        or report["binary_sha256"] != prefix["binary_sha256"]
        or report["routine_sha256"] != prefix["routine_sha256"]
        or report["source_sha256"] != digest(output / "candidate.inc")
        or report["evidence_hashes"] != _leaf_evidence_hashes(root, report["function"])
    ):
        raise ValueError("stale leaf probe source/binary/method")
    for name, identity in report["artifact_hashes"].items():
        path = (output / name).resolve()
        if not path.is_relative_to(output.resolve()) or digest(path) != identity:
            raise ValueError("leaf probe artifact changed")
    required = {
        "CASES.BIN",
        "TRACE.BIN",
        "PASCAL.BIN",
        "PROBE.COM",
        "harness.bin",
        "harness.S",
        "probe.pas",
        "candidate.inc",
        "probe",
        "probe.conf",
    }
    if not required <= report["artifact_hashes"].keys():
        raise ValueError("leaf probe artifact identities incomplete")
    if (
        report["oracle"] != "isolated_original_vs_host_pascal_leaf_memory"
        or report["schema_version"] != 1
        or (output / "harness.S").read_text() != _leaf_harness(report["function"])
        or (output / "probe.pas").read_text() != _leaf_program(report["function"])
    ):
        raise ValueError("leaf probe contract/harness changed")
    stress = report.get("stress_corpus")
    if stress is not None and (
        report["function"] != "FUN_24dd_3b22" or report["suite"] != "training"
    ):
        raise ValueError("invalid stress corpus scope")
    cases = (
        leaf_cases(report["function"], report["suite"])
        if stress is None
        else leaf_stress_cases(stress)
    )
    if (output / "CASES.BIN").read_bytes() != b"".join(data for _, data in cases):
        raise ValueError("leaf probe corpus changed")
    rows = _compare_leaf(
        report["function"],
        cases,
        (output / "TRACE.BIN").read_bytes(),
        (output / "PASCAL.BIN").read_bytes(),
    )
    status = "passed" if all(row["status"] == "passed" for row in rows) else "failed"
    if (
        report["cases"] != rows
        or report["case_count"] != len(cases)
        or report["status"] != status
    ):
        raise ValueError("leaf probe saved outcome disagrees with replay")
    return report


def _leaf_evidence_hashes(root: pathlib.Path, routine: str) -> dict[str, str]:
    """Oracle: immutable shared byte/mapping/probe inputs for the active leaf contract."""
    return {
        name: digest(root / name)
        for name in (
            "engine/instruction_facts.py",
            "engine/alternate_streams.py",
            "tools/liero_file_probe.py",
            "targets/liero/alternate_streams.json",
            f"targets/liero/asm/{routine}.s",
        )
    }


def run_leaf_optimisation(
    root: pathlib.Path,
    output: pathlib.Path,
    first: pathlib.Path,
    sketch: dict,
    freeze: dict,
) -> dict:
    """Oracle: fixed typed neighborhood, matched training, one terminal selected holdout.

    The loop flip is supplied search topology, not another live model proposal.
    Shortest source is only a reproducible search tie-break, not historical truth.
    """
    routine = "FUN_24dd_3b22"
    contract = freeze["routines"][routine]["deductive_constraints"]
    options = freeze["stress_training"]
    started = time.monotonic()
    candidates = [
        {
            "directory": str(first.relative_to(output)),
            "source_sha256": digest(first / "candidate.inc"),
            "status": "eligible",
            "training_cases": len(leaf_cases(routine, "training")),
        }
    ]
    if freeze["optimise"]:
        neighbor = dict(sketch)
        neighbor["loop_kind"] = "while" if sketch["loop_kind"] == "for" else "for"
        directory = output / routine / "neighbors" / "loop-flip"
        directory.mkdir(parents=True)
        save(directory / "sketch.json", neighbor)
        source = render_shortstring_sketch(neighbor, routine, contract)
        (directory / "candidate.inc").write_text(source)
        try:
            result = run_leaf_probe(
                root, directory / "training", routine, source, "training"
            )
        except LeafCandidateExecutionError as exc:
            candidates.append(
                {
                    "directory": str(directory.relative_to(output)),
                    "source_sha256": digest(directory / "candidate.inc"),
                    "status": "runtime-rejected",
                    "reason": str(exc),
                    "training_cases": 0,
                }
            )
        else:
            validate_leaf_probe(root, directory / "training")
            candidates.append(
                {
                    "directory": str(directory.relative_to(output)),
                    "source_sha256": digest(directory / "candidate.inc"),
                    "status": "eligible"
                    if result["status"] == "passed"
                    else "training-rejected",
                    "training_cases": result["case_count"],
                }
            )
    search = {
        "status": "running",
        "candidates": candidates,
        "batches_completed": 0,
        "unique_stress_inputs": 0,
        "comparison_cases": 0,
        "artifact_bytes": 0,
        "ranking": "All checked training cases pass; then source bytes ascending, SHA256 ascending.",
        "source_recovered": 0,
        "examples_promoted": 0,
    }
    log = output / "search.json"
    artifact_bytes = sum(
        path.stat().st_size for path in output.rglob("*") if path.is_file()
    )
    stop = "coverage-budget-complete"
    for batch in range(options["maximum_batches"]):
        validate_leaf_freeze(root, output, freeze)
        if time.monotonic() - started >= options["maximum_seconds"]:
            stop = "time-budget-exhausted"
            break
        if (
            artifact_bytes >= options["maximum_artifact_bytes"]
            or shutil.disk_usage(output).free < 2 * 1024**3
        ):
            search.update(status="blocked", stop_reason="disk-budget-exhausted")
            save(log, search)
            return {"status": "failed", "selected_source": None, "search": search}
        spec = {
            "seed": options["seed"],
            "batch": batch,
            "count": options["cases_per_batch"],
        }
        corpus_sha256 = hashlib.sha256(
            b"".join(data for _, data in leaf_stress_cases(spec))
        ).hexdigest()
        eligible = [row for row in candidates if row["status"] == "eligible"]
        if not eligible:
            stop = "no-passing-candidate"
            break
        for candidate in eligible:
            directory = output / candidate["directory"]
            if digest(directory / "candidate.inc") != candidate["source_sha256"]:
                raise ValueError("optimisation candidate changed after freeze")
            destination = directory / "stress" / f"batch-{batch:05d}"
            save(
                output / "progress.json",
                {
                    "status": "running",
                    "stage": "matched-stress-training",
                    "batch": batch,
                    "candidate": candidate["source_sha256"],
                    "unique_stress_inputs": search["unique_stress_inputs"],
                    "comparison_cases": search["comparison_cases"],
                    "elapsed_seconds": round(time.monotonic() - started, 1),
                },
            )
            try:
                result = run_leaf_probe(
                    root,
                    destination,
                    routine,
                    (directory / "candidate.inc").read_text(),
                    "training",
                    stress=spec,
                )
            except LeafCandidateExecutionError as exc:
                candidate.update(
                    status="runtime-rejected",
                    reason=str(exc),
                    rejection_reference=str(destination),
                )
            else:
                validate_leaf_probe(root, destination)
                if digest(destination / "CASES.BIN") != corpus_sha256:
                    raise ValueError(
                        "optimisation candidates did not use matched training inputs"
                    )
                candidate["training_cases"] += result["case_count"]
                candidate["last_training_reference"] = str(destination)
                if result["status"] != "passed":
                    candidate.update(
                        status="stress-rejected", rejection_reference=str(destination)
                    )
                search["comparison_cases"] += result["case_count"]
            artifact_bytes += sum(
                path.stat().st_size for path in destination.rglob("*") if path.is_file()
            )
        search.update(
            batches_completed=batch + 1,
            unique_stress_inputs=(batch + 1) * spec["count"],
            artifact_bytes=artifact_bytes,
        )
        save(log, search)
        if batch % 10 == 0:
            print(
                json.dumps(
                    {
                        "event": "stress-progress",
                        "batch": batch + 1,
                        "unique_stress_inputs": search["unique_stress_inputs"],
                        "comparison_cases": search["comparison_cases"],
                        "elapsed_seconds": round(time.monotonic() - started, 1),
                    }
                ),
                flush=True,
            )
    eligible = [row for row in candidates if row["status"] == "eligible"]
    if not eligible or not search["batches_completed"]:
        search.update(
            status="failed",
            stop_reason=stop if not eligible else "no-stress-measurement",
        )
        save(log, search)
        return {"status": "failed", "selected_source": None, "search": search}
    selected = min(
        eligible,
        key=lambda row: (
            (output / row["directory"] / "candidate.inc").stat().st_size,
            row["source_sha256"],
        ),
    )
    directory = output / selected["directory"]
    # Freeze the selection before touching the single heldout.
    search.update(
        status="selected", stop_reason=stop, selected=selected["source_sha256"]
    )
    save(log, search)
    validate_leaf_freeze(root, output, freeze)
    save(
        output / "progress.json",
        {"status": "running", "stage": "terminal-heldout", "search": str(log)},
    )
    try:
        heldout = run_leaf_probe(
            root,
            directory / "heldout",
            routine,
            (directory / "candidate.inc").read_text(),
            "heldout",
        )
    except LeafCandidateExecutionError as exc:
        search.update(status="failed", heldout_runtime_failure=str(exc))
        save(log, search)
        return {
            "status": "failed",
            "selected_source": str((directory / "candidate.inc").relative_to(output)),
            "search": search,
        }
    validate_leaf_probe(root, directory / "heldout")
    search.update(status=heldout["status"], heldout_cases=heldout["case_count"])
    save(log, search)
    return {
        "status": heldout["status"],
        "selected_source": str((directory / "candidate.inc").relative_to(output)),
        "source_sha256": selected["source_sha256"],
        "training_cases": selected["training_cases"],
        "heldout_cases": heldout["case_count"],
        "reference": str(directory / "heldout"),
        "search": search,
    }


def leaf_deductive_constraints(routine: str, raw: bytes) -> dict:
    """Oracle: complete supported leaf shapes, not model/manual-source explanations."""
    if routine == "FUN_24dd_4905":
        return bounded_byte_fill_contract(raw)
    if routine == "FUN_24dd_3b22":
        return bounded_shortstring_contract(raw)
    raise ValueError("unknown leaf constraint routine")


def run_leaf_trials(
    root: pathlib.Path,
    output: pathlib.Path,
    model: str,
    endpoint: str,
    *,
    byte_constraints: bool = False,
    resume_trial: pathlib.Path | None = None,
    fill_sketch: bool = False,
    string_sketch: bool = False,
    stress_seconds: int = 0,
    optimise: bool = False,
) -> dict:
    """Oracle: frozen leaf controls, bounded training selection and one holdout each."""
    if (fill_sketch or string_sketch) and (
        not byte_constraints or resume_trial is not None
    ):
        raise ValueError(
            "fill sketch requires byte constraints and a fresh known-slice run"
        )
    if fill_sketch and string_sketch:
        raise ValueError("choose one typed sketch mode")
    if type(stress_seconds) is not int or not 0 <= stress_seconds <= 8 * 3600:
        raise ValueError("stress budget must be 0..28800 seconds")
    if stress_seconds and not string_sketch:
        raise ValueError("overnight stress requires a fresh typed string sketch")
    if optimise and (not string_sketch or not stress_seconds):
        raise ValueError(
            "optimisation requires typed string sketches and a stress budget"
        )
    routines = (
        ("FUN_24dd_4905",)
        if fill_sketch
        else ("FUN_24dd_3b22",)
        if string_sketch
        else tuple(LEAF_PANEL)
    )
    schema = (
        STRING_SKETCH_SCHEMA
        if string_sketch
        else FILL_SKETCH_SCHEMA
        if fill_sketch
        else None
    )
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "BYOD unavailable"}
    missing = [
        tool
        for tool in ("as", "ld", "dosbox", "fpc", "objdump")
        if not shutil.which(tool)
    ]
    if missing:
        raise FileNotFoundError("leaf trials require: " + ", ".join(missing))
    output.mkdir(parents=True, exist_ok=False)
    freeze = {
        "schema_version": 1,
        "model": model,
        "endpoint": endpoint,
        "model_identity": leaf_model_identity(model, endpoint),
        "generation_options": {"temperature": 0.0, "num_predict": 2048},
        "byte_constraints": byte_constraints,
        "fill_sketch": fill_sketch,
        "string_sketch": string_sketch,
        "optimise": optimise,
        "proposal_schema": schema,
        "stress_training": {
            "maximum_seconds": stress_seconds,
            "maximum_batches": 4096,
            "cases_per_batch": 512,
            "seed": 20261101,
            "maximum_artifact_bytes": 16 * 1024**3,
            "policy": "Compare fixed byte-compatible loop alternatives on identical serial seeded training batches; discard failures, select shortest fully passing source (SHA tie-break), one terminal holdout with no retry.",
        }
        if stress_seconds
        else None,
        "resume_trial": str(resume_trial.resolve()) if resume_trial else None,
        "method_sha256": digest(root / "tools/liero_four_routine_pilot.py"),
        "scheduler_sha256": digest(root / "engine/improve_loop.py"),
        "tool_hashes": {
            tool: digest(pathlib.Path(shutil.which(tool)))
            for tool in ("as", "ld", "dosbox", "fpc", "objdump")
        },
        "maximum_model_requests_per_routine": 4,
        "search_operators": ["flip-for-while"] if optimise else [],
        "maximum_unique_candidates": 2 if optimise else 1,
        "repair_alternatives": "new whole include using training/compiler feedback only",
        "holdout_policy": "one evaluation of first training-passing unique source; no retries",
        "source_provenance": "previously manual leaves; no manual target bodies read",
        "topology_disclosure": (
            "Known-slice typed prefix/string topology and loop-flip search supplied; "
            "exact bytes fix memory semantics, not model algorithm discovery."
            if string_sketch
            else "Known-slice typed fill-loop topology supplied; bytes fix memory semantics; "
            "model chooses equivalent Pascal loop syntax, not recovered algorithm."
            if fill_sketch or string_sketch
            else "host pointer interfaces, static byte/segment bounds and controls manually supplied"
        ),
        "routines": {},
    }
    for routine in routines:
        prefix = prefix_transfer_report(root, routine)
        constraints = (
            leaf_deductive_constraints(
                routine, bytes.fromhex(prefix["routine_bytes_hex"])
            )
            if byte_constraints
            else None
        )
        freeze["routines"][routine] = {
            "original_prefix_report": prefix,
            "evidence_hashes": _leaf_evidence_hashes(root, routine),
            "deductive_constraints": constraints,
            "control_source_sha256": hashlib.sha256(
                leaf_control_source(routine).encode()
            ).hexdigest(),
            "case_hashes": {
                suite: hashlib.sha256(
                    b"".join(data for _, data in leaf_cases(routine, suite))
                ).hexdigest()
                for suite in ("training", "heldout")
            },
            "contract": {
                "oracle": "isolated_original_vs_host_pascal_leaf_memory",
                "input": "544-byte arena at DS:6800, 256-byte source, 16/256/16 guarded destination at 6910",
                "bounds": "count 0..256 or short-string length 0..255; disjoint valid nonwrapping pointers",
                "memory": "all 544 bytes compared, unchanged source and guards",
                "abi": "original DS/SS and SP=FFFE preserved across RETF 8; no host ABI claim",
                "output_registers_flags": "outside contract",
            },
        }
    if resume_trial is not None:
        prior = json.loads((resume_trial / "freeze.json").read_text())
        if (
            prior["model_identity"] != freeze["model_identity"]
            or prior["byte_constraints"] != byte_constraints
            or list(resume_trial.glob("*/attempt-*/heldout"))
            or any(
                prior["routines"][fn]["case_hashes"]
                != freeze["routines"][fn]["case_hashes"]
                or prior["routines"][fn]["original_prefix_report"]
                != freeze["routines"][fn]["original_prefix_report"]
                for fn in routines
            )
        ):
            raise ValueError(
                "leaf resume requires unchanged inputs/model and no prior heldout evaluation"
            )
        replayed = {}
        for routine in routines:
            paths = sorted((resume_trial / routine).glob("attempt-*/raw-response.json"))
            if any(
                not (directory / "raw-response.json").is_file()
                for directory in (resume_trial / routine).glob("attempt-*")
                if directory.is_dir()
            ):
                raise ValueError(
                    "leaf resume cannot refund an attempt with unknown model request outcome"
                )
            expected = [
                resume_trial / routine / f"attempt-{i}/raw-response.json"
                for i in range(1, len(paths) + 1)
            ]
            if paths != expected or len(paths) > 4:
                raise ValueError(
                    "leaf resume request history is not a contiguous bounded prefix"
                )
            replayed.update(
                {str(path.relative_to(resume_trial)): digest(path) for path in paths}
            )
        freeze["replayed_response_hashes"] = replayed
        freeze["prior_freeze_sha256"] = digest(resume_trial / "freeze.json")
    save(output / "freeze.json", freeze)
    print(
        json.dumps(
            {
                "event": "trial-frozen",
                "output": str(output),
                "routines": list(routines),
                "maximum_model_requests": 4,
                "stress_training": freeze["stress_training"],
            }
        ),
        flush=True,
    )
    save(
        output / "progress.json",
        {"status": "running", "stage": "positive-controls", "model_requests": 0},
    )
    for relative, name in (
        ("tools/liero_four_routine_pilot.py", "pilot-method.py"),
        ("engine/instruction_facts.py", "instruction-facts-method.py"),
        ("engine/improve_loop.py", "scheduler-method.py"),
    ):
        shutil.copy2(root / relative, output / name)
    validate_leaf_freeze(root, output, freeze)
    for routine in routines:
        control = run_leaf_probe(
            root,
            output / routine / "control",
            routine,
            leaf_control_source(routine),
            "training",
        )
        if control["status"] != "passed":
            result = {
                "status": "blocked",
                "stop_reason": "positive-control-not-passed",
                "function": routine,
                "control_status": control["status"],
            }
            save(output / "result.json", result)
            return result
        validate_leaf_probe(root, output / routine / "control")
    outcomes = []

    def check_piece(routine: str) -> dict:
        """Oracle: bounded training selection followed by at most one terminal holdout."""
        original = freeze["routines"][routine]["original_prefix_report"]
        offset = LEAF_PANEL[routine][0]
        raw_path = output / routine / "original.bin"
        raw_path.write_bytes(bytes.fromhex(original["routine_bytes_hex"]))
        disassembly = subprocess.run(
            [
                "objdump",
                "-D",
                "-b",
                "binary",
                "-m",
                "i8086",
                f"--adjust-vma={offset}",
                str(raw_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        prompt = (
            "Recover Pascal memory behavior from these original 16-bit bytes. "
            "Return JSON with only source, a complete include, no directives/services. "
            "No exact historical identifiers/types claim; register/flag outputs are excluded. "
            "Available type TBlock=array[0..255] of Byte; PBlock=^TBlock. "
            "Implement this interface: "
            + leaf_interface(routine)
            + "\nInput source/destination are disjoint valid nonwrapping 256-byte blocks. "
            "Original far-call stack at entry: return IP/CS at +0/+2; "
            "for fill: value word at +4, count word at +6, destination offset/segment at +8/+10. "
            "For string: source offset/segment at +4/+6, destination at +8/+10. "
            "Fill count <=256. All unknowns must be reported, not invented. "
            "DS is saved/restored where shown; host pointer interface handles segment mapping. "
            "\nOriginal bytes:\n" + original["routine_bytes_hex"] + "\n" + disassembly
        )
        if byte_constraints:
            prompt += (
                "\nDeduction before induction/abduction: obey these checked byte-derived "
                "memory constraints; do not ask the model to guess constants they establish:\n"
                + json.dumps(freeze["routines"][routine]["deductive_constraints"])
                + "\nWrite actual high-level Pascal assignments and loops on source^[i] "
                "and destination^[i]. No inline assembly, no labels, no stub/placeholder "
                "and no assembly transcription in comments. No calls to other routines. "
                "The return/register instructions are outside the host memory interface. "
                "Byte writes must include low and high bytes of any fixed word. "
                "Only explain unresolved suffix behavior by a bounded candidate; "
                "original/Pascal training execution will reject wrong explanations."
            )
        if fill_sketch:
            prompt = (
                "Select a typed Pascal fill-loop sketch, JSON only with exactly these fields: "
                + json.dumps(FILL_SKETCH_SCHEMA)
                + "\nNo source text or inline assembly. This is a supplied syntax mechanism "
                "on a known slice, not algorithm discovery. Original byte-derived contract:\n"
                + json.dumps(freeze["routines"][routine]["deductive_constraints"])
                + "\nHost interface: "
                + leaf_interface(routine)
                + "\nCount is an unsigned Word, bounded 0..256. Byte contract starts at "
                "destination index 0, writes exactly count input-value bytes; zero count "
                "writes nothing. Therefore first_index=0, end_expression=count_minus_one, "
                "stored_value=value are hard constraints, not guesses. loop_kind may be "
                "for or while; guard_zero may be true or false. Renderer uses signed "
                "LongInt bounds to avoid unsigned zero-count subtraction wrap."
            )
        if string_sketch:
            prompt = (
                "Select a typed high-level Pascal shortstring composition sketch. JSON only, "
                "no source text. This is supplied topology on a known slice, not algorithm "
                "discovery. Exact schema:\n"
                + json.dumps(STRING_SKETCH_SCHEMA)
                + "\nChecked original-byte contract:\n"
                + json.dumps(freeze["routines"][routine]["deductive_constraints"])
                + "\nUse prefix=byte_contract, maximum_text_bytes=79, text_destination_offset=48, "
                "source_text_offset=1, stop_at_nul=true. These are hard byte-derived constraints. "
                "Choose equivalent loop_kind for or while; renderer supplies signed bounds, "
                "prefix assignments, length clamp and terminating NUL. All other memory stays unchanged."
            )
        feedback = ""
        seen = set()
        outcome = {
            "function": routine,
            "status": "failed",
            "attempts": [],
            "selected_source": None,
        }
        for attempt in range(1, 5):
            validate_leaf_freeze(root, output, freeze)
            save(
                output / "progress.json",
                {
                    "status": "running",
                    "stage": "model-request",
                    "routine": routine,
                    "model_requests": attempt,
                },
            )
            attempt_dir = output / routine / f"attempt-{attempt}"
            attempt_dir.mkdir()
            save(attempt_dir / "prompt.json", {"prompt": prompt + feedback})
            previous_raw = (
                resume_trial / routine / f"attempt-{attempt}/raw-response.json"
                if resume_trial is not None
                else None
            )
            replayed = previous_raw is not None and previous_raw.is_file()
            raw = (
                previous_raw.read_text()
                if replayed
                else (
                    request(prompt + feedback, model, endpoint, schema=schema)
                    if schema is not None
                    else request(prompt + feedback, model, endpoint)
                )
            )
            (attempt_dir / "raw-response.json").write_text(raw)
            save(
                attempt_dir / "request-provenance.json",
                {
                    "new_model_request": not replayed,
                    "previous_response": str(previous_raw) if replayed else None,
                },
            )
            try:
                if fill_sketch or string_sketch:
                    sketch = json.loads(json.loads(raw)["response"])
                    save(attempt_dir / "sketch.json", sketch)
                    contract = freeze["routines"][routine]["deductive_constraints"]
                    if string_sketch:
                        source = render_shortstring_sketch(sketch, routine, contract)
                    else:
                        source = render_fill_sketch(sketch, routine)
                        validate_fill_sketch_contract(sketch, contract)
                else:
                    source = candidate_source(json.loads(raw), routine)
            except (ValueError, TypeError, KeyError) as exc:
                feedback = "\nPrevious candidate rejected by sanitizer: " + str(exc)
                outcome["attempts"].append(
                    {
                        "attempt": attempt,
                        "status": "sanitizer-rejected",
                        "reason": str(exc),
                    }
                )
                continue
            identity = hashlib.sha256(source.encode()).hexdigest()
            (attempt_dir / "candidate.inc").write_text(source)
            if identity in seen:
                outcome["attempts"].append(
                    {
                        "attempt": attempt,
                        "status": "duplicate-source",
                        "source_sha256": identity,
                    }
                )
                break
            seen.add(identity)
            try:
                training = run_leaf_probe(
                    root, attempt_dir / "training", routine, source, "training"
                )
            except LeafCandidateExecutionError as exc:
                feedback = (
                    "\nPrevious candidate training runtime rejection:\n"
                    + str(exc)[-4000:]
                )
                outcome["attempts"].append(
                    {
                        "attempt": attempt,
                        "status": "runtime-rejected",
                        "reason": str(exc),
                        "source_sha256": identity,
                    }
                )
                continue
            except subprocess.CalledProcessError as exc:
                log = attempt_dir / "training/compile.log"
                if not log.is_file() or (attempt_dir / "training/probe").is_file():
                    raise
                feedback = (
                    "\nPrevious candidate compiler rejection:\n"
                    + log.read_text(errors="replace")[-4000:]
                )
                outcome["attempts"].append(
                    {
                        "attempt": attempt,
                        "status": "compile-rejected",
                        "reason": str(exc),
                        "source_sha256": identity,
                    }
                )
                continue
            validate_leaf_probe(root, attempt_dir / "training")
            outcome["attempts"].append(
                {
                    "attempt": attempt,
                    "status": "training-" + training["status"],
                    "source_sha256": identity,
                }
            )
            if training["status"] != "passed":
                bad = next(
                    row for row in training["cases"] if row["status"] == "failed"
                )
                feedback = (
                    "\nPrevious candidate training mismatch:\n" + json.dumps(bad)[:4000]
                )
                continue
            outcome["selected_source"] = str(
                (attempt_dir / "candidate.inc").relative_to(output)
            )
            if stress_seconds:
                search = run_leaf_optimisation(
                    root,
                    output,
                    attempt_dir,
                    sketch,
                    freeze,
                )
                outcome.update(search)
                break
            save(
                output / "progress.json",
                {"status": "running", "stage": "terminal-heldout", "routine": routine},
            )
            try:
                heldout = run_leaf_probe(
                    root, attempt_dir / "heldout", routine, source, "heldout"
                )
            except LeafCandidateExecutionError as exc:
                outcome.update(
                    status="failed",
                    training_cases=training["case_count"],
                    heldout_cases=len(leaf_cases(routine, "heldout")),
                    source_sha256=identity,
                    heldout_runtime_failure=str(exc),
                )
                break
            validate_leaf_probe(root, attempt_dir / "heldout")
            outcome.update(
                status=heldout["status"],
                training_cases=training["case_count"],
                heldout_cases=heldout["case_count"],
                source_sha256=identity,
                reference=str(attempt_dir / "heldout"),
            )
            break
        save(output / routine / "outcome.json", outcome)
        outcomes.append(outcome)
        return {
            "status": outcome["status"],
            "oracle": "isolated_original_vs_host_pascal_leaf_memory",
            "reference": outcome.get("reference"),
        }

    def frontier() -> dict[str, dict]:
        """Oracle: revalidated frozen premises/scoped outcomes, not resolved routine source."""
        pieces = {}
        for routine in routines:
            if (
                _leaf_evidence_hashes(root, routine)
                != freeze["routines"][routine]["evidence_hashes"]
            ):
                raise ValueError("leaf premises changed after freeze")
            outcome = next(
                (row for row in outcomes if row["function"] == routine), None
            )
            checked = outcome is not None and outcome["status"] == "passed"
            if checked:
                validate_leaf_probe(root, pathlib.Path(outcome["reference"]))
            pieces[routine] = {
                "premise_sha256": hashlib.sha256(
                    json.dumps(freeze["routines"][routine], sort_keys=True).encode()
                ).hexdigest(),
                "checked": checked,
                "blockers": [],
            }
            if outcome is not None and not checked:
                terminal_holdout = outcome["selected_source"] is not None
                exhausted = len(outcome["attempts"]) >= 4 or terminal_holdout
                pieces[routine].update(
                    blockers=[
                        "heldout evaluation is terminal; no retry feedback"
                        if terminal_holdout
                        else "candidate request budget exhausted"
                        if exhausted
                        else "duplicate candidate; no new hypothesis under frozen alternatives"
                    ],
                    blocker_kind="budget" if exhausted else "method",
                )
        return pieces

    from engine.improve_loop import run_puzzle_passes

    puzzle = run_puzzle_passes(
        frontier, check_piece, max_passes=3, milestone=len(routines)
    )
    validate_leaf_freeze(root, output, freeze)
    passes = sum(row["status"] == "passed" for row in outcomes)
    result = {
        "status": "passed" if passes == len(routines) else "failed",
        "new_scoped_routine_passes": 0 if fill_sketch or string_sketch else passes,
        "scoped_memory_comparison_passes": passes,
        "automatic_new_recoveries": 0,
        "known_slice_syntax_mechanism": fill_sketch or string_sketch,
        "functions_evaluated": len(routines),
        "routines": outcomes,
        "yield": passes / len(routines),
        "stop_reason": "milestone-reached"
        if passes == len(routines)
        else "low-yield"
        if passes / len(routines) < 0.25
        else "frozen-budget-complete",
        "puzzle_saturated": False,
        "expansion_allowed": False,
        "next_action": (
            "Review known-slice composition/search evidence; no frontier expansion or source promotion."
            if fill_sketch or string_sketch
            else "Review scoped results; honor the 25% yield floor before expanding."
        ),
        "source_recovered": 0,
        "examples_promoted": 0,
        "puzzle_passes": puzzle,
        "limitations": "Finite assisted leaf-memory experiment; no source/ABI acceptance, no blind-source or weight-learning claim.",
    }
    if stress_seconds and outcomes and "search" in outcomes[0]:
        result["stop_reason"] = outcomes[0]["search"]["stop_reason"]
    save(output / "result.json", result)
    save(
        output / "progress.json",
        {
            "status": result["status"],
            "stage": "finished",
            "result": str(output / "result.json"),
        },
    )
    if fill_sketch and result["status"] == "passed":
        return validate_fill_sketch_trial(root, output)
    return result


def validate_leaf_freeze(
    root: pathlib.Path, output: pathlib.Path, freeze: dict
) -> None:
    """Oracle: frozen corpora/method/model inputs stay unchanged throughout evaluation."""
    if (
        json.loads((output / "freeze.json").read_text()) != freeze
        or freeze["method_sha256"] != digest(root / "tools/liero_four_routine_pilot.py")
        or freeze["scheduler_sha256"] != digest(root / "engine/improve_loop.py")
        or freeze["model_identity"]
        != leaf_model_identity(freeze["model"], freeze["endpoint"])
    ):
        raise ValueError("leaf freeze/model/method changed during evaluation")
    for tool, identity in freeze["tool_hashes"].items():
        executable = shutil.which(tool)
        if executable is None or digest(pathlib.Path(executable)) != identity:
            raise ValueError("leaf frozen tool changed during evaluation")
    if freeze["resume_trial"] is not None:
        previous = pathlib.Path(freeze["resume_trial"])
        if digest(previous / "freeze.json") != freeze["prior_freeze_sha256"] or any(
            digest(previous / name) != identity
            for name, identity in freeze["replayed_response_hashes"].items()
        ):
            raise ValueError(
                "leaf previous request/freeze history changed during evaluation"
            )
    for routine, frozen in freeze["routines"].items():
        if (
            prefix_transfer_report(root, routine) != frozen["original_prefix_report"]
            or _leaf_evidence_hashes(root, routine) != frozen["evidence_hashes"]
            or frozen["deductive_constraints"]
            != (
                leaf_deductive_constraints(
                    routine,
                    bytes.fromhex(
                        frozen["original_prefix_report"]["routine_bytes_hex"]
                    ),
                )
                if freeze["byte_constraints"]
                else None
            )
            or any(
                hashlib.sha256(
                    b"".join(data for _, data in leaf_cases(routine, suite))
                ).hexdigest()
                != identity
                for suite, identity in frozen["case_hashes"].items()
            )
        ):
            raise ValueError("leaf frozen evidence/corpus changed during evaluation")


def validate_fill_sketch_trial(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: replay selected typed sketch and terminal original/Pascal comparison."""
    freeze = json.loads((output / "freeze.json").read_text())
    if (
        freeze.get("fill_sketch") is not True
        or freeze["proposal_schema"] != FILL_SKETCH_SCHEMA
        or set(freeze["routines"]) != {"FUN_24dd_4905"}
    ):
        raise ValueError("not a frozen one-slice fill sketch trial")
    validate_leaf_freeze(root, output, freeze)
    report = json.loads((output / "result.json").read_text())
    if report["status"] != "passed" or len(report["routines"]) != 1:
        raise ValueError("fill sketch trial has no passing selected candidate")
    routine = "FUN_24dd_4905"
    outcome = report["routines"][0]
    if outcome != json.loads((output / routine / "outcome.json").read_text()):
        raise ValueError("fill sketch outcome disagrees with saved trial")
    selected = (output / outcome["selected_source"]).resolve()
    if not selected.is_relative_to(output.resolve()):
        raise ValueError("fill sketch selected source escapes experiment")
    attempt = selected.parent
    proposal = json.loads(
        json.loads((attempt / "raw-response.json").read_text())["response"]
    )
    if json.loads((attempt / "sketch.json").read_text()) != proposal:
        raise ValueError("fill sketch differs from recorded model response")
    source = render_fill_sketch(proposal, routine)
    validate_fill_sketch_contract(
        proposal, freeze["routines"][routine]["deductive_constraints"]
    )
    identity = hashlib.sha256(source.encode()).hexdigest()
    if selected.read_text() != source or outcome["source_sha256"] != identity:
        raise ValueError("fill sketch source differs from rendering")
    training = validate_leaf_probe(root, attempt / "training")
    heldout = validate_leaf_probe(root, attempt / "heldout")
    if (
        training["status"] != "passed"
        or heldout["status"] != "passed"
        or training["suite"] != "training"
        or heldout["suite"] != "heldout"
        or training["source_sha256"] != identity
        or heldout["source_sha256"] != identity
        or len(list((output / routine).glob("attempt-*"))) != len(outcome["attempts"])
        or not 1 <= len(outcome["attempts"]) <= 4
        or len(list(output.glob("*/attempt-*/heldout"))) != 1
        or report["automatic_new_recoveries"] != 0
        or report["source_recovered"] != 0
        or report["examples_promoted"] != 0
        or not report["known_slice_syntax_mechanism"]
    ):
        raise ValueError("fill sketch trial gates or terminal selection disagree")
    return report


def leaf_model_identity(model: str, endpoint: str) -> dict:
    """Oracle: freeze the actual locally installed model digest, not a mutable tag alone."""
    with urllib.request.urlopen(
        endpoint.rstrip("/") + "/api/tags", timeout=30
    ) as response:
        models = json.load(response)["models"]
    for entry in models:
        if entry["name"] == model:
            return {
                "name": model,
                "digest": entry["digest"],
                "details": entry["details"],
            }
    raise ValueError("requested leaf model is not installed at the configured endpoint")


INTERFACES = {
    "constructor": (
        "procedure FUN_24dd_3639(param_1, param_2: Pointer); "
        "param_1 points at 256-byte Pascal short-string storage. param_2 is "
        "the object. PByte and WriteWordLE(pointer, byteOffset, wordValue) are "
        "available. RegisterDI/ES mirror the original object offset/segment."
    ),
    "comparator": (
        "procedure FUN_24dd_3f86(param_1, param_2: Longint); "
        "param_1 is packed destination segment:offset, param_2 is source. "
        "RealModeMemory[0..$FFFFF] is byte memory; RegisterZeroFlag and "
        "RegisterCarryFlag are Boolean output mirrors. Preserve all memory. "
        "Model 16-bit offset wrap separately from 20-bit physical address wrap."
    ),
    "read": (
        "Declare type TLieroDosRead = function(handle, count: Word; "
        "destination: Pointer; var bytesRead: Word): Word; then "
        "function FUN_24dd_375e(objectPointer, bufferPointer: Pointer; "
        "dosRead: TLieroDosRead): Word; "
        "bufferPointer resolves the original far buffer. dosRead models INT 21h "
        "AH=3F: returns zero on success, error code otherwise; bytesRead is AX "
        "on success. The object contains handle at +0, capacity at +4, "
        "position at +8, available count at +10. Do not implement the adapter."
    ),
    "close": (
        "Declare type TLieroDosClose = function(handle: Word): Word; then "
        "function FUN_24dd_37d3(objectPointer: Pointer; "
        "dosClose: TLieroDosClose): Word; "
        "Object word +0 is the handle. dosClose models INT 21h AH=3E, "
        "returning zero or a DOS error code. Do not implement the adapter."
    ),
}
CLOSE_INTERFACE = (
    "type\n"
    "  TLieroDosClose = function(handle: Word): Word;\n\n"
    "function FUN_24dd_37d3(objectPointer: Pointer; "
    "dosClose: TLieroDosClose): Word;\n"
)
CLOSE_SKETCH_SCHEMA = {
    "type": "object",
    "properties": {
        "handle_byte_offset": {"type": "integer", "minimum": 0, "maximum": 254},
        "operator": {"type": "string", "enum": ["<", "<=", "=", "<>", ">=", ">"]},
        "threshold": {"type": "integer", "minimum": 0, "maximum": 65535},
        "then_return": {
            "type": "string",
            "enum": ["zero", "handle", "dos_close_status"],
        },
        "else_return": {
            "type": "string",
            "enum": ["zero", "handle", "dos_close_status"],
        },
    },
    "required": [
        "handle_byte_offset",
        "operator",
        "threshold",
        "then_return",
        "else_return",
    ],
    "additionalProperties": False,
}
READ_SKETCH_SCHEMA = {
    "type": "object",
    "properties": {
        **{
            name: {"type": "integer", "minimum": 0, "maximum": 254}
            for name in (
                "handle_byte_offset",
                "capacity_byte_offset",
                "position_byte_offset",
                "available_byte_offset",
            )
        },
        "clear_on_error": {"type": "boolean"},
        "count_value": {
            "type": "string",
            "enum": ["bytes_read", "requested_count", "zero"],
        },
        "return_value": {
            "type": "string",
            "enum": ["dos_read_status", "bytes_read", "zero"],
        },
    },
    "required": [
        "handle_byte_offset",
        "capacity_byte_offset",
        "position_byte_offset",
        "available_byte_offset",
        "clear_on_error",
        "count_value",
        "return_value",
    ],
    "additionalProperties": False,
}
CONSTRUCTOR_SKETCH_SCHEMA = {
    "type": "object",
    "properties": {
        **{
            name: {"type": "integer", "minimum": 0, "maximum": maximum}
            for name, maximum in (
                ("mode_word", 65535),
                ("capacity_word", 65535),
                ("buffer_byte_offset", 255),
                ("setup_offset", 65535),
                ("setup_segment", 65535),
                ("zero_word_count", 118),
                ("name_byte_offset", 128),
                ("name_limit", 127),
            )
        },
        "stop_at_nul": {"type": "boolean"},
        "use_length_prefix": {"type": "boolean"},
    },
    "required": [
        "mode_word",
        "capacity_word",
        "buffer_byte_offset",
        "setup_offset",
        "setup_segment",
        "zero_word_count",
        "name_byte_offset",
        "name_limit",
        "stop_at_nul",
        "use_length_prefix",
    ],
    "additionalProperties": False,
}


def digest(path: pathlib.Path) -> str:
    """Oracle: immutable source/evidence identity."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: pathlib.Path, value: dict) -> None:
    """Oracle: persistent, explicit trial state, never recovery promotion."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def snapshot(root: pathlib.Path, output: pathlib.Path) -> pathlib.Path:
    """Oracle: isolated source copy; original BYOD is read-only input to probes."""
    output.mkdir(parents=True)
    ignore = shutil.ignore_patterns(
        "build", "runs", "__pycache__", "*.pyc", "*.o", "*.ppu", ".git"
    )
    for relative in (
        "engine",
        "tools",
        "targets/liero/asm",
        "targets/liero/decomp",
        "targets/liero/config",
        "targets/liero/src",
        "targets/liero/tests",
    ):
        shutil.copytree(root / relative, output / relative, ignore=ignore)
    for source in (root / "targets/liero").glob("*.json"):
        shutil.copy2(source, output / "targets/liero" / source.name)
    binary = output / "extracted/liero/LIERO.EXE"
    binary.parent.mkdir(parents=True)
    shutil.copy2(root / "extracted/liero/LIERO.EXE", binary)
    return output


def probe(root: pathlib.Path, output: pathlib.Path, kind: str, suite: str) -> dict:
    """Oracle: existing original/Pascal comparison plus saved-evidence replay."""
    if kind == "constructor":
        report = constructor.run_probe(output, root, suite=suite)
        replay = constructor.validate_saved_report(output, root)
    elif kind == "comparator":
        suite_id = (
            compare.TRAINING_SUITE if suite == "training" else compare.HELD_OUT_SUITE
        )
        report = compare.run_probe(root, output, suite_id)
        replay = compare.validate_saved_report(output, root)
    else:
        report = handler.run_probe(output, root, handler=kind, suite=suite)
        replay = handler.validate_saved_report(output, root)
    if report != replay:
        raise ValueError("probe report disagrees with saved-evidence replay")
    return report


def assembly(root: pathlib.Path, output: pathlib.Path, kind: str) -> str:
    """Oracle: original bytes independently decoded, not a recovered body."""
    _, offset, size = PANEL[kind]
    manifest = json.loads((root / "targets/liero/alternate_streams.json").read_text())
    binary = (root / "extracted/liero/LIERO.EXE").read_bytes()
    if hashlib.sha256(binary).hexdigest() != manifest["binary"]["sha256"]:
        raise ValueError("pilot executable differs from bound original")
    file_offset = manifest["image_mapping"]["header_bytes"] + 0x24DD0 + offset - 0x10000
    raw = output / "original-routine.bin"
    raw.write_bytes(binary[file_offset : file_offset + size])
    decoded = subprocess.run(
        [
            "objdump",
            "-D",
            "-b",
            "binary",
            "-m",
            "i8086",
            f"--adjust-vma={offset}",
            str(raw),
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    (output / "original-routine.asm").write_text(decoded)
    return decoded


def prefix_transfer_report(
    root: pathlib.Path,
    routine: str,
    *,
    data_window: tuple[int, int] | None = None,
) -> dict:
    """Oracle: frozen static transfer assessment, never a routine/source acceptance check."""
    if not re.fullmatch(r"FUN_[0-9a-f]{4}_[0-9a-f]{4}", routine):
        raise ValueError(
            "prefix transfer requires an exported segment:offset routine name"
        )
    target = root / "targets/liero"
    asm_path = target / "asm" / f"{routine}.s"
    listing = asm_path.read_text()
    header_line = re.fullmatch(
        rf"; {routine}  entry=([0-9a-f]{{4}}):([0-9a-f]{{4}}) size=(\d+)",
        listing.splitlines()[0],
    )
    if header_line is None:
        raise ValueError("prefix transfer requires an explicit exported entry/size")
    segment, offset = (int(header_line[index], 16) for index in (1, 2))
    size = int(header_line[3])
    if routine != f"FUN_{segment:04x}_{offset:04x}" or not 0 < size <= 65536 - offset:
        raise ValueError("prefix transfer entry/size disagrees with the routine")
    manifest_path = target / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    binary, header, load_segment, identity = load_binary_evidence(target, manifest)
    file_offset = header + segment * 16 + offset - load_segment * 16
    if file_offset < header or file_offset + size > len(binary):
        raise ValueError("prefix transfer routine lies outside the file-backed image")
    raw = binary[file_offset : file_offset + size]
    relocations = {
        location - file_offset
        for location in _mz_relocation_locations(binary, header)
        if file_offset - 1 <= location < file_offset + size
    }
    prefix = initialization_prefix(
        raw,
        relocation_offsets=relocations,
        load_segment=load_segment,
        data_window=data_window,
    )
    return {
        "schema_version": 1,
        "function": routine,
        "status": "unsupported" if prefix["residue"] is not None else "prefix-decoded",
        "oracle": "frozen_supported_prefix_transfer_only",
        "rules_sha256": digest(root / "engine/instruction_facts.py"),
        "binary_sha256": identity,
        "manifest_sha256": digest(manifest_path),
        "assembly_sha256": digest(asm_path),
        "file_offset": file_offset,
        "routine_bytes_hex": raw.hex(),
        "routine_sha256": hashlib.sha256(raw).hexdigest(),
        "decoded_prefix_bytes": sum(
            len(bytes.fromhex(row["bytes_hex"])) for row in prefix["instructions"]
        ),
        "routine_size": size,
        "prefix": prefix,
        "data_window": list(data_window) if data_window is not None else None,
        "model_requests": 0,
        "routine_recovered": False,
        "limitations": [
            "Previously manual routine, untouched by this frozen transfer method; not a blind-source benchmark.",
            "Entry object/source argument assumptions are conditional, not established for this routine.",
            "Static decoding/coverage only; no candidate synthesis, binary differential or whole-routine acceptance.",
            "No new rules, mutation choices, installation or source/training promotion after evaluation.",
            "Optional entry-DS writable window is an explicit caller precondition, not a discovered allocation.",
        ],
    }


def run_prefix_transfer(
    root: pathlib.Path,
    output: pathlib.Path,
    routine: str,
    *,
    data_window: tuple[int, int] | None = None,
) -> dict:
    """Oracle: immutable rule/input snapshots and replayable unsupported residue."""
    root, output = root.resolve(), output.resolve()
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "BYOD unavailable"}
    report = prefix_transfer_report(root, routine, data_window=data_window)
    output.mkdir(parents=True, exist_ok=False)
    (output / "original-routine.bin").write_bytes(
        bytes.fromhex(report["routine_bytes_hex"])
    )
    shutil.copy2(root / "engine/instruction_facts.py", output / "instruction_facts.py")
    shutil.copy2(
        root / "targets/liero/asm" / f"{routine}.s", output / "original-routine.s"
    )
    save(output / "result.json", report)
    return validate_prefix_transfer(root, output)


def validate_prefix_transfer(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: rederive against unchanged rules/binary; saved coverage is not proof."""
    stored = json.loads((output / "result.json").read_text())
    raw_window = stored.get("data_window")
    if raw_window is not None and (
        not isinstance(raw_window, list) or len(raw_window) != 2
    ):
        raise ValueError("saved prefix data window must be a two-element range")
    expected = prefix_transfer_report(
        root,
        stored["function"],
        data_window=tuple(raw_window) if raw_window is not None else None,
    )
    if stored != expected:
        raise ValueError(
            "saved prefix transfer disagrees with current rules/binary derivation"
        )
    if (
        digest(output / "instruction_facts.py") != expected["rules_sha256"]
        or digest(output / "original-routine.s") != expected["assembly_sha256"]
        or digest(output / "original-routine.bin") != expected["routine_sha256"]
    ):
        raise ValueError("saved prefix transfer snapshot disagrees")
    return expected


def render_partial_memory_source(writes: list[dict], window: tuple[int, int]) -> str:
    """Oracle: constant entry-DS write projection; excludes registers, flags and returns."""
    if not writes:
        raise ValueError("partial memory source has no supported writes")
    lower, upper = window
    if not 0 <= lower <= upper <= 65536:
        raise ValueError("partial memory source requires bounded constant writes")
    lines = [
        "{ Memory effects only; not the original routine or its unresolved return. }",
        "type TEntryData = array[0..65535] of Byte;",
        "procedure ApplyPartialMemoryEffects(var entryData: TEntryData);",
        "var index: LongInt;",
        "begin",
    ]
    for write in writes:
        offset, count = write.get("byte_offset"), write.get("word_count")
        value = write.get("value", {})
        amount = value.get("amount")
        if (
            write.get("address_space") != "entry_ds"
            or value.get("kind") != "constant"
            or any(type(number) is not int for number in (offset, count, amount))
            or not 0 <= amount <= 65535
            or count < 0
            or not lower <= offset <= offset + 2 * count <= upper
        ):
            raise ValueError("partial memory source requires bounded constant writes")
        if count:
            lines.extend(
                [
                    f"  for index := 0 to {count - 1} do",
                    "  begin",
                    f"    entryData[{offset} + 2 * index] := {amount & 255};",
                    f"    entryData[{offset} + 2 * index + 1] := {amount >> 8};",
                    "  end;",
                ]
            )
    return "\n".join([*lines, "end;", ""])


def _partial_memory_artifact(
    root: pathlib.Path, output: pathlib.Path
) -> tuple[str, dict]:
    """Oracle: current-bound prefix dependencies and exact retained suffix."""
    prefix = validate_prefix_transfer(root, output)
    window = prefix["data_window"]
    if window is None:
        raise ValueError("partial memory source requires an explicit entry-DS window")
    source = render_partial_memory_source(prefix["prefix"]["writes"], tuple(window))
    residue = prefix["prefix"]["residue"]
    return source, {
        "schema_version": 1,
        "function": prefix["function"],
        "oracle": "static_memory_projection_only",
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "renderer_sha256": digest(root / "tools/liero_four_routine_pilot.py"),
        "prefix_report_sha256": digest(output / "result.json"),
        "binary_sha256": prefix["binary_sha256"],
        "rules_sha256": prefix["rules_sha256"],
        "data_window": window,
        "memory_writes": prefix["prefix"]["writes"],
        "dependency_instruction_offsets": sorted(
            {
                offset
                for write in prefix["prefix"]["writes"]
                for offset in write["support"]
            }
        ),
        "unresolved_offset": residue["offset"] if residue else None,
        "unresolved_bytes_hex": residue["bytes_hex"] if residue else "",
        "routine_recovered": False,
        "whole_routine_execution": "blocked",
        "training_promotion": "blocked",
        "limitations": [
            "Host Pascal memory projection only; not exact historical source structure.",
            "Entry-DS window is conditional; no normal-program allocation established.",
            "Register, flag, segment-stack and return effects are not implemented.",
            "Original routine bytes/listing remain separate; no mixed-assembly execution.",
            "Static rendering is not a scoped differential pass or source attestation.",
        ],
    }


def write_partial_memory_source(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: disposable partial source, never installed into target/runtime/training."""
    source, report = _partial_memory_artifact(root, output)
    with (output / "partial-memory.inc").open("x") as stream:
        stream.write(source)
    with (output / "partial-memory.json").open("x") as stream:
        json.dump(report, stream, indent=2)
    return validate_partial_memory_source(root, output)


def validate_partial_memory_source(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: rederive partial source and dependencies; reject stale/tampered artifacts."""
    source, expected = _partial_memory_artifact(root, output)
    if (output / "partial-memory.inc").read_text() != source or json.loads(
        (output / "partial-memory.json").read_text()
    ) != expected:
        raise ValueError("saved partial memory artifact disagrees with derivation")
    return expected


def request(
    prompt: str,
    model: str,
    endpoint: str,
    *,
    schema: dict | None = None,
    max_generated_tokens: int = 2048,
    think: bool | None = None,
) -> str:
    """Oracle: local structured proposal only; binary probes decide acceptance."""
    if type(max_generated_tokens) is not int or max_generated_tokens <= 0:
        raise ValueError("generated token budget must be a positive integer")
    if think is not None and type(think) is not bool:
        raise ValueError("thinking setting must be boolean or unset")
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": schema
        if schema is not None
        else {
            "type": "object",
            "properties": {"source": {"type": "string"}},
            "required": ["source"],
            "additionalProperties": False,
        },
        "options": {"temperature": 0.0, "num_predict": max_generated_tokens},
    }
    if think is not None:
        payload["think"] = think
    message = urllib.request.Request(
        endpoint.rstrip("/") + "/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(message, timeout=600) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise ValueError(f"local model HTTP {error.code}: {detail}") from error


def candidate_source(response: dict, routine: str) -> str:
    """Oracle: complete include only; no compiler directives or service replacement."""
    proposal = json.loads(response["response"])
    if not isinstance(proposal, dict) or set(proposal) != {"source"}:
        raise ValueError("proposal must contain only source")
    source = proposal["source"]
    if not isinstance(source, str) or not re.search(
        rf"\b(?:procedure|function)\s+{routine}\b", source, re.IGNORECASE
    ):
        raise ValueError("proposal lacks the required routine")
    if re.search(
        r"\{\$|\(\*\$|\b(uses|program|unit|external|assembler|asm|"
        r"halt|assign|reset|rewrite|blockread|blockwrite|exec)\b",
        source,
        re.IGNORECASE,
    ):
        raise ValueError("proposal contains forbidden directives or services")
    return source


def render_close_sketch(response: dict) -> tuple[dict, str]:
    """Oracle: restricted conditional hypotheses, not an assumed recovered answer."""
    proposal = json.loads(response["response"])
    if not isinstance(proposal, dict) or set(proposal) != set(
        CLOSE_SKETCH_SCHEMA["required"]
    ):
        raise ValueError("close sketch must contain exactly the five required fields")
    for field, maximum in (("handle_byte_offset", 254), ("threshold", 65535)):
        value = proposal[field]
        if type(value) is not int or not 0 <= value <= maximum:
            raise ValueError(f"close sketch {field} must be an integer in 0..{maximum}")
    if proposal["handle_byte_offset"] % 2:
        raise ValueError("close sketch handle_byte_offset must be word-aligned")
    for field in ("operator", "then_return", "else_return"):
        if proposal[field] not in CLOSE_SKETCH_SCHEMA["properties"][field]["enum"]:
            raise ValueError(f"close sketch {field} is outside the allowed vocabulary")
    expressions = {
        "zero": "0",
        "handle": "handle",
        "dos_close_status": "dosClose(handle)",
    }
    source = (
        "{ Oracle: model-selected conditional sketch; scoped parity required. }\n"
        + CLOSE_INTERFACE
        + "var\n  objectWord: ^Word;\n  handle: Word;\nbegin\n"
        + "  objectWord := objectPointer;\n"
        + f"  Inc(objectWord, {proposal['handle_byte_offset'] // 2});\n"
        + "  handle := objectWord^;\n"
        + f"  if handle {proposal['operator']} {proposal['threshold']} then\n"
        + f"    FUN_24dd_37d3 := {expressions[proposal['then_return']]}\n"
        + "  else\n"
        + f"    FUN_24dd_37d3 := {expressions[proposal['else_return']]};\nend;\n"
    )
    return proposal, source


def render_read_sketch(response: dict) -> tuple[dict, str]:
    """Oracle: one DOS-read/state-update topology; all semantic fields remain hypotheses."""
    proposal = json.loads(response["response"])
    if not isinstance(proposal, dict) or set(proposal) != set(
        READ_SKETCH_SCHEMA["required"]
    ):
        raise ValueError("read sketch must contain exactly the seven required fields")
    for name in READ_SKETCH_SCHEMA["required"][:4]:
        value = proposal[name]
        if type(value) is not int or not 0 <= value <= 254 or value % 2:
            raise ValueError(f"read sketch {name} must be an even integer in 0..254")
    if type(proposal["clear_on_error"]) is not bool:
        raise ValueError("read sketch clear_on_error must be Boolean")
    for name in ("count_value", "return_value"):
        if proposal[name] not in READ_SKETCH_SCHEMA["properties"][name]["enum"]:
            raise ValueError(f"read sketch {name} is outside the allowed vocabulary")
    count = {"bytes_read": "received", "requested_count": "capacity", "zero": "0"}
    returns = {"dos_read_status": "status", "bytes_read": "received", "zero": "0"}
    guard = "" if proposal["clear_on_error"] else "  if status = 0 then\n"
    source = (
        "{ Oracle: model-selected read sketch; scoped adapter parity required. }\n"
        "type\n  TLieroDosRead = function(handle, count: Word; destination: Pointer;\n"
        "    var bytesRead: Word): Word;\n\n"
        "function FUN_24dd_375e(objectPointer, bufferPointer: Pointer;\n"
        "  dosRead: TLieroDosRead): Word;\n"
        "var\n  handle, capacity, received, status: Word;\n"
        "function ObjectWord(offset: Word): Word;\n"
        "var\n  p: ^Word;\nbegin\n  p := objectPointer;\n  Inc(p, offset div 2);\n"
        "  ObjectWord := p^;\nend;\n"
        "procedure SetObjectWord(offset, value: Word);\n"
        "var\n  p: ^Word;\nbegin\n  p := objectPointer;\n  Inc(p, offset div 2);\n"
        "  p^ := value;\nend;\n"
        "begin\n"
        f"  handle := ObjectWord({proposal['handle_byte_offset']});\n"
        f"  capacity := ObjectWord({proposal['capacity_byte_offset']});\n"
        "  received := 0;\n  status := dosRead(handle, capacity, bufferPointer, received);\n"
        + guard
        + "  begin\n"
        + f"    SetObjectWord({proposal['position_byte_offset']}, 0);\n"
        + "    if status = 0 then\n"
        + f"      SetObjectWord({proposal['available_byte_offset']}, {count[proposal['count_value']]})\n"
        + "    else\n"
        + f"      SetObjectWord({proposal['available_byte_offset']}, 0);\n"
        + "  end;\n"
        + f"  FUN_24dd_375e := {returns[proposal['return_value']]};\nend;\n"
    )
    return proposal, source


def render_constructor_sketch(response: dict) -> tuple[dict, str]:
    """Oracle: bounded sequential initialization/copy topology, not a recovered answer."""
    proposal = json.loads(response["response"])
    if not isinstance(proposal, dict) or set(proposal) != set(
        CONSTRUCTOR_SKETCH_SCHEMA["required"]
    ):
        raise ValueError("constructor sketch must contain exactly ten required fields")
    for name, rule in CONSTRUCTOR_SKETCH_SCHEMA["properties"].items():
        value = proposal[name]
        if rule["type"] == "boolean":
            if type(value) is not bool:
                raise ValueError(f"constructor sketch {name} must be Boolean")
        elif type(value) is not int or not 0 <= value <= rule["maximum"]:
            raise ValueError(f"constructor sketch {name} is outside its integer bounds")
    length = (
        "  if input^ < limit then\n    limit := input^;\n  Inc(input);\n"
        if proposal["use_length_prefix"]
        else ""
    )
    stop = " and (input^ <> 0)" if proposal["stop_at_nul"] else ""
    source = (
        "{ Oracle: model-selected constructor sketch; guarded binary parity required. }\n"
        "procedure FUN_24dd_3639(param_1, param_2: Pointer);\n"
        "var\n  input, output: PByte;\n  index, limit: Word;\nbegin\n"
        "  input := PByte(param_1);\n  output := PByte(param_2);\n"
        "  WriteWordLE(output, 0, 0);\n"
        f"  WriteWordLE(output, 2, {proposal['mode_word']});\n"
        f"  WriteWordLE(output, 4, {proposal['capacity_word']});\n"
        "  WriteWordLE(output, 6, 0);\n  WriteWordLE(output, 8, 0);\n"
        "  WriteWordLE(output, 10, 0);\n"
        f"  WriteWordLE(output, 12, (RegisterDI + {proposal['buffer_byte_offset']}) and $FFFF);\n"
        "  WriteWordLE(output, 14, RegisterES);\n"
        f"  WriteWordLE(output, 16, {proposal['setup_offset']});\n"
        f"  WriteWordLE(output, 18, {proposal['setup_segment']});\n"
        "  index := 0;\n"
        f"  while index < {proposal['zero_word_count']} do\n"
        "  begin\n    WriteWordLE(output, 20 + index * 2, 0);\n"
        "    Inc(index);\n  end;\n"
        f"  limit := {proposal['name_limit']};\n"
        + length
        + "  index := 0;\n"
        + f"  while (index < limit){stop} do\n"
        + "  begin\n"
        + f"    output[{proposal['name_byte_offset']} + index] := input^;\n"
        + "    Inc(input);\n    Inc(index);\n  end;\n"
        + f"  output[{proposal['name_byte_offset']} + index] := 0;\nend;\n"
    )
    return proposal, source


def constructor_instruction_facts(root: pathlib.Path) -> dict:
    """Oracle: binary/MZ-bound initialization constraints, not the unresolved copy loop."""
    target = root / "targets/liero"
    manifest = json.loads((target / "alternate_streams.json").read_text())
    binary, header, load_segment, identity = load_binary_evidence(target, manifest)
    _, offset, size = PANEL["constructor"]
    file_offset = header + (0x24DD - load_segment) * 16 + offset
    raw = binary[file_offset : file_offset + size]
    if len(raw) != size:
        raise ValueError("constructor instruction bytes are incomplete")
    relocations = {
        location - file_offset
        for location in _mz_relocation_locations(binary, header)
        if file_offset - 1 <= location < file_offset + size
    }
    facts = initialization_prefix(
        raw,
        relocation_offsets=relocations,
        load_segment=load_segment,
    )
    writes = facts["writes"]
    if (
        len(writes) != 11
        or any(
            row["byte_offset"] != index * 2 or row["word_count"] != 1
            for index, row in enumerate(writes[:10])
        )
        or writes[10]["byte_offset"] != 20
        or any(
            writes[index]["value"]["kind"] != "constant"
            or writes[index]["value"]["amount"] != 0
            for index in (0, 3, 4, 5, 10)
        )
        or writes[6]["value"]["kind"] != "object_offset"
        or writes[7]["value"]["kind"] != "object_segment"
        or facts["next_object_offset"] is None
    ):
        raise ValueError(
            "supported prefix does not establish constructor sketch topology"
        )
    fields = {
        "mode_word": (1, "constant"),
        "capacity_word": (2, "constant"),
        "buffer_byte_offset": (6, "object_offset"),
        "setup_offset": (8, "constant"),
        "setup_segment": (9, "constant"),
    }
    constraints = {}
    for field, (index, kind) in fields.items():
        row = writes[index]
        if row["value"]["kind"] != kind:
            raise ValueError(f"constructor {field} has an unknown expression")
        constraints[field] = {
            "value": row["value"]["amount"],
            "instruction_offsets": sorted(
                set(row["support"] + list(row["value"]["support"]))
            ),
        }
    segment_definition = writes[9]["value"]["support"][-1]
    if not any(
        row["offset"] == segment_definition and row["relocation_offset"] is not None
        for row in facts["instructions"]
    ):
        raise ValueError("constructor setup segment lacks an MZ relocation")
    constraints["zero_word_count"] = {
        "value": writes[10]["word_count"],
        "instruction_offsets": writes[10]["support"],
    }
    constraints["name_byte_offset"] = {
        "value": facts["next_object_offset"],
        "instruction_offsets": facts["registers"]["di"]["support"],
    }
    for field, claim in constraints.items():
        rule = CONSTRUCTOR_SKETCH_SCHEMA["properties"][field]
        if not 0 <= claim["value"] <= rule["maximum"]:
            raise ValueError(f"binary {field} is outside the supported sketch bounds")
    return {
        "function": PANEL["constructor"][0],
        "binary_sha256": identity,
        "manifest_sha256": digest(target / "alternate_streams.json"),
        "file_offset": file_offset,
        "bytes_hex": raw.hex(),
        "routine_sha256": hashlib.sha256(raw).hexdigest(),
        "prefix": facts,
        "constraints": constraints,
        "unresolved_fields": ["name_limit", "stop_at_nul", "use_length_prefix"],
        "limitations": [
            "Static supported-prefix facts under the recorded entry argument/layout contract.",
            "No branch or name-copy proof; raw CX alone is not a loop contract.",
            "No source attestation, universal equivalence or model generalization.",
        ],
    }


def constrain_constructor_schema(facts: dict) -> dict:
    """Oracle: known numeric fields are restricted, never guessed or silently replaced."""
    schema = json.loads(json.dumps(CONSTRUCTOR_SKETCH_SCHEMA))
    for field, claim in facts["constraints"].items():
        schema["properties"][field]["enum"] = [claim["value"]]
    return schema


def validate_constructor_instruction_facts(
    path: pathlib.Path, root: pathlib.Path
) -> dict:
    """Oracle: regenerate static facts from bound bytes; stored claims are not proof."""
    saved = json.loads(path.read_text())
    expected = constructor_instruction_facts(root)
    if saved != expected:
        raise ValueError(
            "saved constructor instruction facts disagree with current binary derivation"
        )
    return expected


def check_constructor_constraints(sketch: dict, facts: dict) -> None:
    """Oracle: contradiction rejects the model proposal without editing its semantic fields."""
    conflicts = {
        field: {"proposed": sketch[field], "binary": claim["value"]}
        for field, claim in facts["constraints"].items()
        if sketch[field] != claim["value"]
    }
    if conflicts:
        raise ValueError("constructor instruction conflicts: " + json.dumps(conflicts))


def sketch_renderer(kind: str) -> Callable[[dict], tuple[dict, str]]:
    """Oracle: explicit supported sketch routing; unknown routines are errors."""
    renderers = {
        "close": render_close_sketch,
        "read": render_read_sketch,
        "constructor": render_constructor_sketch,
    }
    if kind not in renderers:
        raise ValueError("sketch repair is limited to constructor, read and close")
    return renderers[kind]


def training_feedback(report: dict) -> str:
    """Oracle: valid, bounded constructor counterexamples; omitted evidence is explicit."""
    failures = [case for case in report.get("cases", []) if case["status"] != "passed"]
    if report.get("function") == PANEL["constructor"][0]:
        return json.dumps(
            {
                "status": report["status"],
                "failed_case_count": len(failures),
                "failed_cases": [
                    {
                        **case,
                        "differences": case["differences"][:8],
                        "difference_count": len(case["differences"]),
                    }
                    for case in failures[:8]
                ],
                "omitted_failed_cases": max(0, len(failures) - 8),
            }
        )
    return json.dumps(
        {
            "status": report["status"],
            "failed_cases": failures[:8],
            "fixtures": report.get("fixtures", {}),
        }
    )[:12000]


def repair_hypotheses(kind: str, sketch: dict) -> list[tuple[str, dict]]:
    """Oracle: bounded one-field alternatives, never chosen from held-out results."""
    sketch_renderer(kind)
    if kind == "constructor":
        return [
            (name, {**sketch, "name_limit": value})
            for name, value in (
                ("name-limit-minus-one", sketch["name_limit"] - 1),
                ("name-limit-plus-one", sketch["name_limit"] + 1),
            )
            if 0 <= value <= 127
        ] + [
            (f"toggle-{field}", {**sketch, field: not sketch[field]})
            for field in ("stop_at_nul", "use_length_prefix")
        ]
    if kind == "close":
        return (
            [
                (
                    "swapped",
                    {
                        **sketch,
                        "then_return": sketch["else_return"],
                        "else_return": sketch["then_return"],
                    },
                )
            ]
            if sketch["then_return"] != sketch["else_return"]
            else []
        )
    return [
        (
            "toggle-error-clear",
            {**sketch, "clear_on_error": not sketch["clear_on_error"]},
        ),
        *[
            (f"{field}-{value}", {**sketch, field: value})
            for field in ("count_value", "return_value")
            for value in READ_SKETCH_SCHEMA["properties"][field]["enum"]
            if value != sketch[field]
        ],
    ]


def recovered_examples(root: pathlib.Path, query_asm: str) -> list[dict]:
    """Oracle: current ledger review plus recorded host tests, not binary parity."""
    target = root / "targets/liero"
    audit = audit_target(target)
    ledger = json.loads((target / "recovery.json").read_text())
    excluded = {item[0] for item in PANEL.values()}
    examples = []
    for routine in audit["routines"]:
        name = routine["name"]
        if (
            name in excluded
            or not routine["source_recovered"]
            or not routine["behavior_verified"]
        ):
            continue
        record = ledger["functions"][name]
        source = target / record["source_file"]
        asm = target / "asm" / f"{name}.s"
        # Remove historical decompiler commentary, not the checked Pascal body.
        pascal = re.sub(
            r"\{.*?\}|\(\*.*?\*\)|//[^\n]*", "", source.read_text(), flags=re.DOTALL
        ).strip()
        examples.append(
            {
                "fn": name,
                "target": "liero",
                "language": "pascal",
                "verification_status": "verified",
                "oracle": "ledger static review and recorded host tests; NOT binary parity",
                "asm": asm.read_text(),
                "pascal": pascal,
                "source_sha256": digest(source),
                "assembly_sha256": digest(asm),
                "review_notes": record["review_notes"],
                "validation_notes": record["verification"]["notes"],
            }
        )
    key = knowledge.compiler_key("tp7", "dos")
    # This retrieval view is ephemeral: no corpus promotion or knowledge writes.
    return knowledge.verified_pascal_examples_for(
        {"verified_pascal_examples": {key: examples}},
        "tp7",
        "dos",
        query_asm,
        limit=3,
    )


def recovered_context(examples: list[dict]) -> str:
    """Oracle: examples teach syntax only; their scope never certifies the candidate."""
    if not examples:
        raise ValueError("no current recovered and host-tested examples are available")
    parts = [
        (
            "Recovered SAME-TARGET examples, excluding every pilot routine. "
            "These have current static source review and recorded host tests, "
            "not original-binary equivalence. Use their Pascal syntax and memory/"
            "register idioms, NOT their algorithms or undeclared helpers. "
            "Do not emit assembly mnemonics as Pascal calls."
        )
    ]
    for example in examples:
        parts.append(
            f"\nExample {example['fn']} ({example['oracle']}):\n"
            + example["asm"]
            + "\nPASCAL:\n"
            + example["pascal"]
        )
    return "\n".join(parts)


def run_routine(
    root: pathlib.Path,
    output: pathlib.Path,
    kind: str,
    model: str,
    endpoint: str,
    budget: int,
    *,
    use_recovered: bool = False,
    constrained_close: bool = False,
    automatic_close_repair: bool = False,
    automatic_read_repair: bool = False,
    automatic_constructor_repair: bool = False,
    constructor_instruction_constraints: bool = False,
) -> dict:
    """Oracle: controls precede generation; held-out results never feed repair."""
    if constrained_close and kind != "close":
        raise ValueError("conditional sketch is limited to the close routine")
    if automatic_close_repair and not constrained_close:
        raise ValueError("automatic close repair requires a constrained close sketch")
    if automatic_read_repair and (kind != "read" or constrained_close):
        raise ValueError("automatic read repair is limited to the read routine")
    if automatic_constructor_repair and (kind != "constructor" or constrained_close):
        raise ValueError("automatic constructor repair is limited to the constructor")
    if constructor_instruction_constraints and not automatic_constructor_repair:
        raise ValueError("instruction constraints require automatic constructor mode")
    automatic_repair = (
        automatic_close_repair or automatic_read_repair or automatic_constructor_repair
    )
    schema = (
        CONSTRUCTOR_SKETCH_SCHEMA
        if automatic_constructor_repair
        else READ_SKETCH_SCHEMA
        if automatic_read_repair
        else CLOSE_SKETCH_SCHEMA
    )
    renderer = (
        sketch_renderer(kind)
        if automatic_repair or constrained_close
        else render_close_sketch
    )
    if not 1 <= budget <= 4:
        raise ValueError("routine budget must be between 1 and 4")
    output.mkdir()
    workspace = snapshot(root, output / "control-workspace")
    routine = PANEL[kind][0]
    result = {"function": routine, "status": "blocked", "attempts": [], "controls": {}}
    result["model_request_budget"] = budget
    result["repair_budget_per_proposal"] = (
        4
        if automatic_constructor_repair
        else 5
        if automatic_read_repair
        else 1
        if automatic_close_repair
        else 0
    )
    if constrained_close:
        result["proposal_mode"] = "close-conditional-sketch-v1"
        result["search_scope"] = (
            "Human-supplied single word load and if/else topology; model selects "
            "offset, unsigned condition, threshold and return expressions. "
            "Not unrestricted source synthesis or evidence of generalization."
        )
        save(output / "proposal-schema.json", CLOSE_SKETCH_SCHEMA)
    if automatic_read_repair:
        result["proposal_mode"] = "read-state-sketch-v1"
        result["search_scope"] = (
            "Human-supplied one DOS-read call and position/count update topology. "
            "Model selects four word offsets, error clearing, count and return values. "
            "Five one-field repair alternatives; not unrestricted source synthesis."
        )
        save(output / "proposal-schema.json", READ_SKETCH_SCHEMA)
    if automatic_constructor_repair:
        result["proposal_mode"] = "constructor-init-copy-sketch-v1"
        result["search_scope"] = (
            "Human-supplied sequential word initialization and bounded byte-copy topology. "
            "Model selects constants, clear span, copy offset/cap and prefix/NUL behavior. "
            "Four one-field alternatives; fixed disjoint guarded layout, not full recovery."
        )
        save(output / "proposal-schema.json", CONSTRUCTOR_SKETCH_SCHEMA)
    instruction_facts = None
    if constructor_instruction_constraints:
        try:
            instruction_facts = constructor_instruction_facts(workspace)
        except (OSError, ValueError, TypeError) as exc:
            result["reason"] = f"instruction facts blocked: {exc}"
            save(output / "result.json", result)
            return result
        schema = constrain_constructor_schema(instruction_facts)
        save(output / "instruction-facts.json", instruction_facts)
        validate_constructor_instruction_facts(
            output / "instruction-facts.json", workspace
        )
        save(output / "proposal-schema.json", schema)
        result["instruction_facts_sha256"] = digest(output / "instruction-facts.json")
        result["known_fields"] = list(instruction_facts["constraints"])
        result["unresolved_fields"] = instruction_facts["unresolved_fields"]
        result["proposal_mode"] = "constructor-instruction-constrained-v1"
    heldout_suite = "heldout-v2" if automatic_close_repair else "heldout"
    for suite in ("training", heldout_suite):
        try:
            control = probe(workspace, output / f"control-{suite}", kind, suite)
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            result["reason"] = f"{suite} control error: {exc}"
            save(output / "result.json", result)
            return result
        result["controls"][suite] = control["status"]
        if control["status"] != "passed":
            result["reason"] = f"{suite} positive control failed"
            save(output / "result.json", result)
            return result
    instructions = assembly(workspace, output, kind)
    context = ""
    if use_recovered:
        query_asm = re.sub(
            r"(?m)^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2}\s+)+",
            r"24dd:\1  ",
            instructions,
        )
        examples = recovered_examples(root, query_asm)
        save(output / "recovered-examples.json", {"examples": examples})
        context = recovered_context(examples)
        result["recovered_examples"] = [example["fn"] for example in examples]
        if kind == "close" and not constrained_close:
            context += (
                "\nThe output source must start with this exact callback/interface "
                "declaration, followed by your var declarations and begin/end body:\n"
                + CLOSE_INTERFACE
                + "\nThe probe does NOT import LieroRuntime or define PWord. "
                "Use a locally declared ^Word pointer variable; assign "
                "objectPointer to it and dereference with ^. The only callable "
                "service is the passed dosClose callback. Do not copy helper calls "
                "or register mirrors from examples into this pointer-based interface."
            )
    seen = set()
    feedback = "No previous candidate."
    for attempt in range(1, budget + 1):
        directory = output / f"proposal-{attempt:02}"
        directory.mkdir()
        prompt = (
            "Recover a Pascal include from these original 16-bit x86 instructions. "
            "Return JSON with only a source field containing the complete include. "
            "Use {$MODE TP}-compatible Pascal, but do not emit compiler directives, "
            "uses, unit/program, inline assembler, file I/O or adapter implementations. "
            "Only the routine, local variables and required callback type are allowed. "
            "Your result is checked against the original binary, not a style example.\n"
            + INTERFACES[kind]
            + "\n"
            + context
            + "\nOriginal instructions:\n"
            + instructions
            + "\nTraining feedback only:\n"
            + feedback
        )
        if constrained_close:
            prompt = (
                "Infer the behavior of this original 16-bit close routine. "
                "Return only a JSON conditional sketch, NEVER Pascal or assembly. "
                "The supplied sketch reads one word from the object and branches "
                "on an unsigned comparison. Select handle_byte_offset (even byte "
                "offset 0..254), operator (<, <=, =, <>, >=, >), threshold (0..65535), "
                "then_return and else_return. Return choices are zero, handle, "
                "dos_close_status. dos_close_status means invoke the supplied "
                "DOS-close adapter once with the loaded handle and return its "
                "status; it replaces INT 21h AH=3E. Do not assume a branch is "
                "correct just because it fits this sketch; original execution "
                "decides acceptance. No other keys or text.\n"
                + context
                + "\nOriginal instructions:\n"
                + instructions
                + "\nTraining feedback only:\n"
                + feedback
            )
        if automatic_read_repair:
            prompt = (
                "Infer this original 16-bit refill routine. Return only a JSON sketch, "
                "never Pascal or assembly. Choose even byte offsets 0..254 for "
                "handle_byte_offset, capacity_byte_offset, position_byte_offset, "
                "available_byte_offset. The supplied topology calls dosRead once, "
                "then clears position and writes available count on success. "
                "clear_on_error selects whether both fields are also cleared on error. "
                "count_value is bytes_read, requested_count, or zero. return_value "
                "is dos_read_status, bytes_read, or zero. DOS adapter returns zero "
                "on success or error code; bytes_read is AX only on success. "
                "The adapter resolves the original far buffer, not an object-word field. "
                "Original execution, not the supplied topology, decides acceptance.\n"
                + INTERFACES[kind]
                + "\nOriginal instructions:\n"
                + instructions
                + "\nTraining feedback only:\n"
                + feedback
            )
        if automatic_constructor_repair:
            prompt = (
                "Infer this original 16-bit constructor. Return only a JSON sketch, "
                "never Pascal or assembly. The supplied topology writes ten object "
                "words: zero, mode_word, capacity_word, three zeros, "
                "object offset plus buffer_byte_offset, object segment, setup_offset, "
                "setup_segment. Then zero_word_count words starting at byte 20. "
                "Copy at most name_limit input bytes to name_byte_offset, then "
                "write one NUL. stop_at_nul chooses early termination; use_length_prefix "
                "chooses reading/skipping the initial Pascal length byte and clamping "
                "the limit to it. Select all fields from instructions. "
                "Word constants are 0..65535; buffer offset 0..255, clear count 0..118, "
                "name offset 0..128, name cap 0..127. Boolean fields must be booleans. "
                "No call is executed: the setup pointer is stored, not invoked. "
                "The probe uses logical code segments at image-relative segment plus "
                "$1000. For the stored setup segment immediate, add $1000 modulo "
                "$10000 to the raw disassembled immediate; this is explicit MZ/host "
                "address mapping, not an inferred semantic repair. Object buffer "
                "offset is relative to the initial object, not advanced DI. "
                "Original-byte execution and all guard bytes decide acceptance.\n"
                + INTERFACES[kind]
                + "\nOriginal instructions:\n"
                + instructions
                + "\nTraining feedback only:\n"
                + feedback
            )
        if instruction_facts is not None:
            prompt += (
                "\nStatic original-byte initialization constraints (not model guesses):\n"
                + json.dumps(instruction_facts["constraints"], sort_keys=True)
                + "\nThese fields MUST match exactly; contradictions are rejected, "
                "not corrected. Infer only name_limit, stop_at_nul and "
                "use_length_prefix from the remaining instructions. "
                "Initial CX is an observed register value, not a proven loop contract."
            )
        (directory / "prompt.txt").write_text(prompt)
        row = {"attempt": attempt, "status": "rejected"}
        result["attempts"].append(row)
        try:
            response_body = (
                request(prompt, model, endpoint, schema=schema)
                if constrained_close or automatic_repair
                else request(prompt, model, endpoint)
            )
        except (urllib.error.URLError, TimeoutError) as exc:
            row["reason"] = f"model request failed: {exc}"
            if isinstance(exc, urllib.error.HTTPError):
                (directory / "http-error.txt").write_bytes(exc.read())
            result["reason"] = row["reason"]
            save(output / "result.json", result)
            return result
        (directory / "raw-response.json").write_text(response_body)
        try:
            response = json.loads(response_body)
            if constrained_close or automatic_repair:
                proposal, source = renderer(response)
                save(directory / "sketch.json", proposal)
                row["sketch"] = proposal
                if instruction_facts is not None:
                    check_constructor_constraints(proposal, instruction_facts)
            else:
                source = candidate_source(response, routine)
            if use_recovered and kind == "close" and not constrained_close:
                compact_source = re.sub(r"\s+", "", source).casefold()
                compact_interface = re.sub(r"\s+", "", CLOSE_INTERFACE).casefold()
                if not compact_source.startswith(compact_interface):
                    raise ValueError(
                        "Missing or changed callback/interface declaration. Start "
                        "your source with:\n" + CLOSE_INTERFACE
                    )
        except (ValueError, KeyError, TypeError) as exc:
            feedback = str(exc)
            row["reason"] = feedback
            save(output / "result.json", result)
            continue
        (directory / f"{routine}.inc").write_text(source)
        identity = hashlib.sha256(source.encode()).hexdigest()
        row["source_sha256"] = identity
        if identity in seen:
            row["reason"] = "duplicate candidate"
            result["reason"] = row["reason"]
            break
        seen.add(identity)
        workspace = snapshot(root, directory / "workspace")
        source_path = workspace / "targets/liero/src" / f"{routine}.inc"
        source_path.write_text(source)
        try:
            training = probe(workspace, directory / "training", kind, "training")
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            feedback = f"Training compilation/execution rejected: {exc}"
            if isinstance(exc, subprocess.CalledProcessError):
                for content in (exc.stdout, exc.stderr):
                    if content:
                        feedback += "\n" + (
                            content.decode("utf-8", errors="replace")
                            if isinstance(content, bytes)
                            else content
                        )
            row["reason"] = feedback
            save(output / "result.json", result)
            continue
        row["training_status"] = training["status"]
        if training["status"] != "passed":
            row["status"] = "failed"
            feedback = training_feedback(training)
            save(output / "result.json", result)
            if automatic_repair and repair_hypotheses(kind, proposal):
                try:
                    repair = (
                        run_sketch_repair(
                            root,
                            directory / "repair",
                            directory,
                            kind=kind,
                            retest_seed=False,
                            seen_sources=seen,
                            **(
                                {"enforce_constructor_facts": True}
                                if constructor_instruction_constraints
                                else {}
                            ),
                        )
                        if automatic_read_repair or automatic_constructor_repair
                        else run_close_branch_repair(
                            root,
                            directory / "repair",
                            directory,
                            retest_seed=False,
                            seen_sources=seen,
                        )
                    )
                except (
                    OSError,
                    ValueError,
                    RuntimeError,
                    subprocess.SubprocessError,
                ) as exc:
                    result["status"] = "blocked"
                    result["reason"] = f"automatic repair validation error: {exc}"
                    save(output / "result.json", result)
                    return result
                row["repair"] = repair
                if any("heldout_status" in item for item in repair["hypotheses"]):
                    result["status"] = repair["status"]
                    result["selected_by"] = (
                        "deterministic-state-repair"
                        if automatic_read_repair or automatic_constructor_repair
                        else "deterministic-branch-repair"
                    )
                    if repair["status"] == "passed":
                        result["accepted_by"] = result["selected_by"]
                    result["reason"] = (
                        "training-selected repair evaluated once on heldout"
                    )
                    break
            continue
        try:
            heldout = probe(workspace, directory / "heldout", kind, heldout_suite)
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            result["status"] = "blocked"
            result["reason"] = f"heldout validation error: {exc}"
            save(output / "result.json", result)
            return result
        row["heldout_status"] = heldout["status"]
        row["status"] = heldout["status"]
        result["status"] = heldout["status"]
        result["selected_by"] = "model-proposal"
        if heldout["status"] == "passed":
            result["accepted_by"] = result["selected_by"]
        result["reason"] = "selected candidate evaluated once on heldout"
        break
    else:
        result["reason"] = "proposal budget exhausted"
    if result["status"] == "blocked" and result["attempts"]:
        result["status"] = "failed"
    result["unique_candidates"] = len(seen)
    result["model_requests"] = len(result["attempts"])
    if automatic_constructor_repair:
        result["scoped_pass_rate"] = 1.0 if result["status"] == "passed" else 0.0
        result["stop_reason"] = (
            "bounded-slice-complete"
            if result["status"] == "passed"
            else "below-25-percent-floor"
        )
    save(output / "result.json", result)
    return result


def run_pilot(
    root: pathlib.Path,
    output: pathlib.Path,
    *,
    model: str,
    endpoint: str = "http://localhost:11434",
    budget: int = 4,
) -> dict:
    """Oracle: fixed four-routine panel; below-floor yield forbids expansion."""
    if not 1 <= budget <= 4:
        raise ValueError("pilot budget must be between 1 and 4")
    root, output = root.resolve(), output.resolve()
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "BYOD unavailable"}
    for tool in ("as", "ld", "dosbox", "fpc", "objdump"):
        if shutil.which(tool) is None:
            raise FileNotFoundError(f"pilot requires {tool}")
    output.mkdir(parents=True, exist_ok=False)
    protected = [root / "targets/liero/recovery.json"] + [
        root / "targets/liero/src" / f"{item[0]}.inc" for item in PANEL.values()
    ]
    before = {str(path): digest(path) for path in protected}
    result = {
        "status": "running",
        "model": model,
        "candidate_budget_per_routine": budget,
        "routines": [],
        "limitations": [
            "Finite scoped fixtures, not universal recovery or model-weight learning.",
            "Read/close use host DOS adapters; original setup is fixture code only.",
            "Close heldout changes payload only, not the tested handle lifecycle.",
            "No candidate source, ledger, retrieval or training promotion.",
        ],
    }
    save(output / "result.json", result)
    for kind in PANEL:
        print(f"Starting {kind}", flush=True)
        row = run_routine(root, output / kind, kind, model, endpoint, budget)
        result["routines"].append(row)
        save(output / "result.json", result)
        print(f"{kind}: {row['status']}", flush=True)
    if {str(path): digest(path) for path in protected} != before:
        raise ValueError("protected repository source/ledger changed during pilot")
    passes = sum(row["status"] == "passed" for row in result["routines"])
    result.update(
        status="completed",
        scoped_passes=passes,
        panel_size=len(PANEL),
        scoped_pass_rate=passes / len(PANEL),
        stop_reason="below-25-percent-floor" if passes == 0 else "fixed-panel-complete",
        protected_hashes=before,
    )
    save(output / "result.json", result)
    return result


def run_close_branch_repair(
    root: pathlib.Path,
    output: pathlib.Path,
    seed: pathlib.Path,
    *,
    retest_seed: bool = True,
    seen_sources: set[str] | None = None,
) -> dict:
    """Oracle: two evidenced branch hypotheses, never model or source promotion."""
    return run_sketch_repair(
        root,
        output,
        seed,
        kind="close",
        retest_seed=retest_seed,
        seen_sources=seen_sources,
    )


def run_sketch_repair(
    root: pathlib.Path,
    output: pathlib.Path,
    seed: pathlib.Path,
    *,
    kind: str,
    retest_seed: bool = False,
    seen_sources: set[str] | None = None,
    enforce_constructor_facts: bool = False,
) -> dict:
    """Oracle: replay-bound bounded alternatives, with one held-out selection."""
    renderer = sketch_renderer(kind)
    if enforce_constructor_facts and kind != "constructor":
        raise ValueError("instruction constraints are limited to the constructor")
    routine = PANEL[kind][0]
    root, output, seed = root.resolve(), output.resolve(), seed.resolve()
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "BYOD unavailable"}
    validator = (
        constructor.validate_saved_report
        if kind == "constructor"
        else handler.validate_saved_report
    )
    contract = (
        constructor.CONTRACT
        if kind == "constructor"
        else handler.handler_contract(kind)
    )
    original = validator(seed / "training", seed / "workspace")
    if (
        original["contract"] != contract
        or original["status"] != "failed"
        or original.get("suite", "training") != "training"
    ):
        raise ValueError(
            "sketch repair requires a replay-validated failed training report"
        )
    if original["binary_sha256"] != digest(root / "extracted/liero/LIERO.EXE"):
        raise ValueError("seed report belongs to a different original executable")
    raw = json.loads((seed / "raw-response.json").read_text())
    sketch, source = renderer(raw)
    instruction_facts = (
        constructor_instruction_facts(root) if enforce_constructor_facts else None
    )
    if instruction_facts is not None:
        check_constructor_constraints(sketch, instruction_facts)
    if (
        sketch != json.loads((seed / "sketch.json").read_text())
        or source != (seed / "training/candidate" / f"{routine}.inc").read_text()
    ):
        raise ValueError("seed sketch disagrees with the measured candidate")
    alternatives = repair_hypotheses(kind, sketch)
    if not alternatives:
        raise ValueError("sketch supplies no competing hypothesis")
    protected = [root / "targets/liero/recovery.json"] + [
        root / "targets/liero/src" / f"{item[0]}.inc" for item in PANEL.values()
    ]
    before = {str(path): digest(path) for path in protected}
    output.mkdir(parents=True, exist_ok=False)
    result = {
        "status": "running",
        "method": f"single-field-{kind}-repair-v1"
        if kind != "close"
        else "swap-branch-returns-only-v1",
        "seed": str(seed),
        "seed_report_sha256": digest(seed / "training/result.json"),
        "model_requests": 0,
        "hypotheses": [],
        "protected_hashes": before,
        "limitations": [
            "Fixed single-field search space, not unrestricted semantic repair.",
            "Finite DOS-adapter fixtures, not universal equivalence or general decompilation.",
            (
                "Automatic close mode uses heldout-v2 unsigned invalid-handle boundaries."
                if kind == "close"
                else "Constructor heldout uses patterned arenas and embedded NUL cases."
                if kind == "constructor"
                else "Read heldout uses disjoint lengths 127/129/257 and capacity seven."
            ),
            "No installation, recovery attestation, knowledge or training promotion.",
        ],
    }
    save(output / "result.json", result)
    if instruction_facts is not None:
        save(output / "instruction-facts.json", instruction_facts)
        validate_constructor_instruction_facts(output / "instruction-facts.json", root)
        result["instruction_facts_sha256"] = digest(output / "instruction-facts.json")
    for name, hypothesis in [("unchanged", sketch), *alternatives]:
        if instruction_facts is not None:
            check_constructor_constraints(hypothesis, instruction_facts)
        _, rendered = renderer({"response": json.dumps(hypothesis)})
        identity = hashlib.sha256(rendered.encode()).hexdigest()
        if not retest_seed and name == "unchanged":
            result["hypotheses"].append(
                {
                    "hypothesis": name,
                    "source_sha256": identity,
                    "sketch": hypothesis,
                    "training_status": original["status"],
                    "training_report": str(seed / "training/result.json"),
                    "reused_seed_report": True,
                }
            )
            continue
        if seen_sources is not None:
            if identity in seen_sources:
                result["hypotheses"].append(
                    {
                        "hypothesis": name,
                        "source_sha256": identity,
                        "status": "skipped",
                        "reason": "duplicate candidate",
                    }
                )
                continue
            seen_sources.add(identity)
        directory = output / name
        directory.mkdir()
        workspace = snapshot(root, directory / "workspace")
        (workspace / "targets/liero/src" / f"{routine}.inc").write_text(rendered)
        save(directory / "sketch.json", hypothesis)
        training = probe(workspace, directory / "training", kind, "training")
        row = {
            "hypothesis": name,
            "sketch": hypothesis,
            "source_sha256": hashlib.sha256(rendered.encode()).hexdigest(),
            "training_status": training["status"],
            "training_report": f"{name}/training/result.json",
        }
        if kind == "constructor":
            row["training_cases_passed"] = sum(
                case["status"] == "passed" for case in training["cases"]
            )
        else:
            row["training_calls_passed"] = sum(
                call["status"] == "passed"
                for fixture in training["fixtures"].values()
                for call in fixture["calls"]
            )
        result["hypotheses"].append(row)
        if training["status"] == "passed":
            heldout = probe(
                workspace,
                directory / "heldout",
                kind,
                "heldout-v2" if kind == "close" and not retest_seed else "heldout",
            )
            row["heldout_status"] = heldout["status"]
            row["heldout_report"] = f"{name}/heldout/result.json"
        save(output / "result.json", result)
        if "heldout_status" in row:
            break
    if {str(path): digest(path) for path in protected} != before:
        raise ValueError("protected sources changed during sketch repair")
    result["status"] = (
        "passed"
        if any(row.get("heldout_status") == "passed" for row in result["hypotheses"])
        else "failed"
    )
    result["stop_reason"] = (
        "training-selected-candidate-evaluated-once"
        if any("heldout_status" in row for row in result["hypotheses"])
        else "fixed-hypothesis-budget-complete"
    )
    save(output / "result.json", result)
    return result


ALLOCATOR_INTERFACE = """procedure FUN_24dd_0353(requestSize, startOffset, startSegment,
  limitOffset, limitSegment: Word; var resultOffset, resultSegment,
  newOffset, newSegment, savedRequest: Word; var failed: Boolean);"""


def allocator_cases(suite: str) -> list[tuple[int, int, int, int, int]]:
    """Oracle: frozen empty-list contexts, not arbitrary free-list or startup reachability."""
    if suite not in ("training", "heldout"):
        raise ValueError("unknown allocator suite")
    requests = (
        (0, 1, 8, 9, 15, 16, 64000, 65535)
        if suite == "training"
        else (2, 7, 17, 255, 4095, 65528)
    )
    return [
        (request, offset, 0x800, limit_offset, 0x800 + capacity)
        for request in requests
        for offset in (0, 8)
        for capacity, limit_offset in ((0, 0), (1, 0), (0x1000, 0), (0, 8))
    ]


def allocator_harness(case_path: pathlib.Path, count: int) -> str:
    """Oracle: controlled disjoint COM data/code/stack with actual allocator/helper/callback."""
    return f"""
.code16
.global _start
_start:
    jmp start
.org 0x1000-0x100
start:
    push %cs
    pop %ds
    push %cs
    pop %ss
    mov $0xeff0, %sp
    mov %cs, %ax
    add $0x1000, %ax
    jc failed
    cmp 2, %ax
    ja failed
    movw $0xc033, %cs:0xd6
    movw $0x02ca, %cs:0xd8
    movb $0, %cs:0xda
    mov $cases, %si
    mov $records, %di
    mov ${count}, %cx
next_case:
    push %cx
    push %si
    push %di
    push %ds
    pop %es
    mov $0x63d8, %di
    mov $56, %cx
    mov $0xa5, %al
    cld
    rep stosb
    mov $0x8000, %di
    mov $128, %cx
    rep stosb
    movw $0xa5a5, 0x7b3c
    mov 2(%si), %ax
    mov %ax, 0x63ee
    mov %ax, 0x63f6
    mov %cs, %ax
    add 4(%si), %ax
    mov %ax, 0x63f0
    mov %ax, 0x63f8
    mov 6(%si), %ax
    mov %ax, 0x63f2
    mov %cs, %ax
    add 8(%si), %ax
    mov %ax, 0x63f4
    movw $0xd6, 0x63fe
    mov %cs, %ax
    mov %ax, 0x6400
    mov (%si), %ax
    mov %sp, %cs:call_sp
    call 0x353
    pushf
    popw %cs:result_flags
    cmp %cs:call_sp, %sp
    jne failed
    mov %cs, %bx
    mov %ds, %cx
    cmp %bx, %cx
    jne failed
    mov %ss, %cx
    cmp %bx, %cx
    jne failed
    test %dx, %dx
    jz normalized
    sub %bx, %dx
normalized:
    push %ds
    pop %es
    cld
    pop %di
    stosw
    mov %dx, %ax
    stosw
    mov %cs:result_flags, %ax
    and $1, %ax
    stosw
    mov 0x63ee, %ax
    stosw
    mov 0x63f0, %ax
    sub %bx, %ax
    stosw
    mov 0x63f6, %ax
    stosw
    mov 0x63f8, %ax
    sub %bx, %ax
    stosw
    mov 0x7b3c, %ax
    stosw
    mov $0x63d8, %si
    mov $56, %cx
    push %ds
    pop %es
    rep movsb
    mov $0x8000, %si
    mov $128, %cx
    rep movsb
    pop %si
    add $10, %si
    pop %cx
    dec %cx
    jz write_output
    jmp next_case
write_output:
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, %bx
    mov $records, %dx
    mov ${count * 200}, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp ${count * 200}, %ax
    jne failed
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21
call_sp: .word 0
result_flags: .word 0
filename: .asciz "TRACE.BIN"
.balign 2
cases: .incbin "{case_path}"
records: .space {count * 200}
"""


def allocator_original(
    root: pathlib.Path,
    output: pathlib.Path,
    cases: list[tuple],
    binary: bytes,
    contract: dict,
) -> list[list[int]]:
    """Oracle: original203-byte allocator, actual helper/default callback; controlled empty list only."""
    output.mkdir()
    (output / "CASES.BIN").write_bytes(
        b"".join(struct.pack("<5H", *case) for case in cases)
    )
    source = output / "harness.S"
    source.write_text(allocator_harness((output / "CASES.BIN").resolve(), len(cases)))
    harness = file_probe.assemble_probe(source, output)
    if len(harness) + 0x100 >= 0x6000:
        raise ValueError("allocator harness overlaps global cells")
    image = bytearray(harness)
    for offset, raw in (
        (0x353, bytes.fromhex(contract["reviewed_bytes_hex"])),
        (
            0x4DC,
            bytes.fromhex(
                json.loads(
                    (root / "targets/liero/config/routine_contracts.json").read_text()
                )["functions"]["FUN_24dd_04dc"]["reviewed_bytes_hex"]
            ),
        ),
        (0xD6, bytes.fromhex("33c0ca0200")),
    ):
        start = contract["file_offset"] + offset - 0x353
        if binary[start : start + len(raw)] != raw:
            raise ValueError("allocator dependency bytes differ")
        if offset < 0x100:
            # COM starts at0100; use the PSP scratch tail for the unchanged callback bytes.
            continue
        if any(image[offset - 0x100 : offset - 0x100 + len(raw)]):
            raise ValueError("allocator copied code overlaps harness")
        image[offset - 0x100 : offset - 0x100 + len(raw)] = raw
    (output / "PROBE.COM").write_bytes(image)
    file_probe.run_dosbox(output)
    return allocator_original_rows((output / "TRACE.BIN").read_bytes(), cases)


def allocator_original_rows(trace: bytes, cases: list[tuple]) -> list[list[int]]:
    """Oracle: complete original trace and explicit global/heap guards, not Pascal parity."""
    if len(trace) != 200 * len(cases):
        raise ValueError("allocator original trace shape differs")
    rows = []
    for index, case in enumerate(cases):
        record = trace[index * 200 : (index + 1) * 200]
        fields = list(struct.unpack_from("<8H", record))
        memory = record[16:72]
        code_segment = struct.unpack_from("<H", memory, 0x6400 - 0x63D8)[0]
        if (
            struct.unpack_from("<H", memory, 0x63F2 - 0x63D8)[0] != case[3]
            or struct.unpack_from("<H", memory, 0x63F4 - 0x63D8)[0]
            != code_segment + case[4]
            or struct.unpack_from("<H", memory, 0x63FE - 0x63D8)[0] != 0xD6
        ):
            raise ValueError("allocator changed limit/default callback")
        # All unrelated globals and guarded heap bytes must stay untouched.
        allowed = {*(range(0x63EE, 0x63FA)), *range(0x63FE, 0x6402)}
        if (
            any(
                value != 0xA5
                for cell, value in enumerate(memory, 0x63D8)
                if cell not in allowed
            )
            or record[72:] != bytes([0xA5]) * 128
        ):
            raise ValueError("allocator original changed guards/unrelated cells")
        if fields[2] not in (0, 1) or fields[5:7] != fields[3:5]:
            raise ValueError("allocator empty-list head/frontier invariant differs")
        if (
            fields[7] != (case[0] if case[0] else 0xA5A5)
            or any(
                struct.unpack_from("<H", memory, cell - 0x63D8)[0] != expected
                for cell, expected in (
                    (0x63EE, fields[3]),
                    (0x63F0, code_segment + fields[4]),
                    (0x63F6, fields[5]),
                    (0x63F8, code_segment + fields[6]),
                )
            )
            or ((not case[0] or fields[2]) and fields[3:5] != list(case[1:3]))
            or (not case[0] and fields[:3] != [0, 0, 0])
        ):
            raise ValueError("allocator original state/row projection differs")
        rows.append(fields)
    return rows


def render_allocator_empty_source(facts: dict) -> str:
    """Oracle: deterministic known-slice rendering; no model discovery or full ABI claim."""
    expected = allocator_empty_list_contract(
        bytes.fromhex(facts["routine_bytes_hex"]),
        bytes.fromhex(facts["helper_bytes_hex"]),
        bytes.fromhex(facts["callback_bytes_hex"]),
    )
    if facts != expected:
        raise ValueError("allocator obligations differ from instruction derivation")
    return (
        ALLOCATOR_INTERFACE
        + """
var rounded, off, seg: LongWord;
begin
  resultOffset := 0; resultSegment := 0; failed := false;
  if requestSize = 0 then Exit;
  savedRequest := requestSize;
  rounded := ((LongWord(requestSize) + 7) div 8) * 8;
  off := (LongWord(startOffset) + rounded mod 16) and $ffff;
  seg := (LongWord(startSegment) + rounded div 16) and $ffff;
  if (off and 255) >= 16 then seg := (seg + 1) and $ffff;
  off := off and $ff0f;
  if (seg > limitSegment) or ((seg = limitSegment) and (off > limitOffset)) then
  begin
    resultSegment := seg;
    failed := true
  end
  else begin
    resultOffset := startOffset; resultSegment := startSegment;
    newOffset := off; newSegment := seg;
  end;
end;
"""
    )


def allocator_deduction_inputs(root: pathlib.Path) -> tuple[bytes, dict, dict]:
    """Oracle: actual original bytes and MZ relocations, never assembly-listing facts."""
    from engine.routine_contract import load_contract

    target = root / "targets/liero"
    contract = load_contract(target, "FUN_24dd_0353")
    helper = load_contract(target, "FUN_24dd_04dc")
    binary, header, _, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    if identity != contract["binary_sha256"] or identity != helper["binary_sha256"]:
        raise ValueError("allocator dependency binary identity differs")
    start = contract["file_offset"]
    raw = binary[start : start + 203]
    helper_start = start + 0x4DC - 0x353
    callback_start = start + 0xD6 - 0x353
    helper_raw = binary[helper_start : helper_start + 17]
    callback = binary[callback_start : callback_start + 5]
    if (
        raw.hex() != contract["reviewed_bytes_hex"]
        or helper_raw.hex() != helper["reviewed_bytes_hex"]
        or any(
            begin - 1 <= relocation < begin + size
            for relocation in _mz_relocation_locations(binary, header)
            for begin, size in ((start, 203), (helper_start, 17), (callback_start, 5))
        )
    ):
        raise ValueError("allocator dependency bytes/relocations differ")
    return (
        binary,
        contract,
        {
            **allocator_empty_list_contract(raw, helper_raw, callback),
            "binary_sha256": identity,
        },
    )


def allocator_deduction_freeze(root: pathlib.Path, facts: dict) -> dict:
    """Oracle: deterministic strategy/corpus/premise identity, separate from old model trials."""
    paths = (
        "tools/liero_four_routine_pilot.py",
        "tools/liero_file_probe.py",
        "engine/instruction_facts.py",
        "engine/routine_contract.py",
        "engine/alternate_streams.py",
        "targets/liero/config/routine_contracts.json",
        "targets/liero/alternate_streams.json",
    )
    return {
        "strategy": "byte-deduction-empty-list-v1",
        "binary_sha256": facts["binary_sha256"],
        "method_hashes": {path: digest(root / path) for path in paths},
        "training": [list(case) for case in allocator_cases("training")],
        "heldout": [list(case) for case in allocator_cases("heldout")],
        "budget": {"candidates": 1, "model_requests": 0, "heldout_evaluations": 1},
        "known_scope": (
            "Developer-known empty-list/default-callback slice; supplied topology, "
            "historical corpus and control. Deductive mechanism check, not automatic "
            "unseen-routine generalization or normal-program allocator acceptance."
        ),
    }


def _allocator_suite_result(
    original: list[list[int]], candidate: list[list[int]], count: int
) -> dict:
    """Oracle: exact complete row counts; partial output never becomes a scored pass."""
    if any(
        len(rows) != count
        or any(
            len(row) != 8 or any(type(v) is not int or not 0 <= v <= 65535 for v in row)
            for row in rows
        )
        for rows in (original, candidate)
    ):
        raise ValueError("allocator comparison has incomplete or invalid trace shape")
    mismatches = [
        i
        for i, pair in enumerate(zip(original, candidate, strict=True))
        if pair[0] != pair[1]
    ]
    return {
        "cases": count,
        "passed": count - len(mismatches),
        "mismatch_indices": mismatches,
    }


def run_allocator_deduction(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: one deterministic candidate, complete training then one terminal validation."""
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "Liero BYOD unavailable"}
    binary, contract, facts = allocator_deduction_inputs(root)
    freeze = allocator_deduction_freeze(root, facts)
    semantic_facts = {
        key: value for key, value in facts.items() if key != "binary_sha256"
    }
    source = render_allocator_empty_source(semantic_facts)
    output.mkdir(parents=True, exist_ok=False)
    save(output / "freeze.json", freeze)
    save(output / "obligations.json", facts)
    (output / "candidate.inc").write_text(source)
    (output / "methods").mkdir()
    for path in freeze["method_hashes"]:
        shutil.copy2(root / path, output / "methods" / pathlib.Path(path).name)
    result = {
        "status": "failed",
        "function": "FUN_24dd_0353",
        "oracle": "controlled_original_empty_freelist_vs_deduced_pascal",
        "binary_sha256": facts["binary_sha256"],
        "scope": freeze["known_scope"],
        "model_requests": 0,
        "heldout_evaluations": 0,
        "source_promoted": False,
        "routine_recovered": False,
        "automatic_discovery": False,
        "expansion_allowed": False,
        "unresolved": facts["unresolved"],
    }

    def validate_frozen() -> None:
        """Oracle: current original bytes, methods, obligations and exact rendered source."""
        _, _, current = allocator_deduction_inputs(root)
        if (
            current != facts
            or json.loads((output / "freeze.json").read_text()) != freeze
            or allocator_deduction_freeze(root, current) != freeze
            or json.loads((output / "obligations.json").read_text()) != facts
            or (output / "candidate.inc").read_text() != source
        ):
            raise ValueError("allocator deduction freeze/method/premises changed")

    try:
        for suite in ("training", "heldout"):
            validate_frozen()
            cases = [tuple(case) for case in freeze[suite]]
            if suite == "heldout":
                result["heldout_evaluations"] = 1
            original = allocator_original(
                root, output / f"original-{suite}", cases, binary, contract
            )
            candidate = allocator_candidate(
                output / f"candidate-{suite}", source, cases
            )
            result[suite] = _allocator_suite_result(original, candidate, len(cases))
            validate_frozen()
            if result[suite]["mismatch_indices"]:
                result["stop_reason"] = f"{suite}-failure-no-retry"
                break
        else:
            result.update(status="passed", stop_reason="deductive-scope-validated")
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["stop_reason"] = "first-error-no-retry"
    save(
        output / "review.json",
        {
            "decision": "accept-controlled-projection"
            if result["status"] == "passed"
            else "reject-controlled-projection",
            "basis": "exact supported byte composition and complete scoped comparison",
            "source_installed": False,
            "routine_recovered": False,
            "unresolved": facts["unresolved"],
        },
    )
    result["freeze_sha256"] = digest(output / "freeze.json")
    result["artifact_hashes"] = {
        str(path.relative_to(output)): digest(path)
        for path in output.rglob("*")
        if path.is_file()
    }
    save(output / "result.json", result)
    return result


def validate_allocator_deduction(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: replay source-bound complete traces under current bytes/methods, no execution."""
    report = json.loads((output / "result.json").read_text())
    _, contract, facts = allocator_deduction_inputs(root)
    freeze = allocator_deduction_freeze(root, facts)
    source = render_allocator_empty_source(
        {key: value for key, value in facts.items() if key != "binary_sha256"}
    )
    if (
        json.loads((output / "freeze.json").read_text()) != freeze
        or report["freeze_sha256"] != digest(output / "freeze.json")
        or json.loads((output / "obligations.json").read_text()) != facts
        or (output / "candidate.inc").read_text() != source
        or report["oracle"] != "controlled_original_empty_freelist_vs_deduced_pascal"
        or report["function"] != "FUN_24dd_0353"
        or report["binary_sha256"] != facts["binary_sha256"]
        or report["scope"] != freeze["known_scope"]
        or report["status"] != "passed"
        or report["model_requests"] != 0
        or report["heldout_evaluations"] != 1
        or any(
            report[key] is not False
            for key in (
                "source_promoted",
                "routine_recovered",
                "automatic_discovery",
                "expansion_allowed",
            )
        )
        or report["unresolved"] != facts["unresolved"]
    ):
        raise ValueError(
            "allocator deduction report/premises/source changed or not passed"
        )
    required = {"freeze.json", "obligations.json", "candidate.inc", "review.json"}
    for path in freeze["method_hashes"]:
        name = f"methods/{pathlib.Path(path).name}"
        required.add(name)
        if digest(output / name) != freeze["method_hashes"][path]:
            raise ValueError("allocator saved method differs")
    for suite in ("training", "heldout"):
        cases = [tuple(case) for case in freeze[suite]]
        original_dir = output / f"original-{suite}"
        candidate_dir = output / f"candidate-{suite}"
        original_files = ("CASES.BIN", "harness.S", "PROBE.COM", "TRACE.BIN")
        candidate_files = (
            "candidate.inc",
            "probe.pas",
            "probe",
            "compile.log",
            "execution.log",
            "PASCAL.BIN",
        )
        required.update(f"original-{suite}/{name}" for name in original_files)
        required.update(f"candidate-{suite}/{name}" for name in candidate_files)
        if (
            (original_dir / "CASES.BIN").read_bytes()
            != b"".join(struct.pack("<5H", *case) for case in cases)
            or (original_dir / "harness.S").read_text()
            != allocator_harness((original_dir / "CASES.BIN").resolve(), len(cases))
            or (candidate_dir / "candidate.inc").read_text() != source
            or (candidate_dir / "probe.pas").read_text()
            != allocator_candidate_program(cases)
        ):
            raise ValueError("allocator saved corpus/harness/candidate differs")
        image = (original_dir / "PROBE.COM").read_bytes()
        for offset, raw in (
            (0x353, bytes.fromhex(contract["reviewed_bytes_hex"])),
            (0x4DC, bytes.fromhex(facts["helper_bytes_hex"])),
        ):
            if image[offset - 0x100 : offset - 0x100 + len(raw)] != raw:
                raise ValueError("allocator original image dependency changed")
        original = allocator_original_rows(
            (original_dir / "TRACE.BIN").read_bytes(), cases
        )
        trace = (candidate_dir / "PASCAL.BIN").read_bytes()
        if len(trace) != 16 * len(cases):
            raise ValueError("allocator saved Pascal trace shape differs")
        candidate = [list(row) for row in struct.iter_unpack("<8H", trace)]
        measured = _allocator_suite_result(original, candidate, len(cases))
        if measured != report[suite] or measured["passed"] != len(cases):
            raise ValueError("allocator replay comparison differs or failed")
    review = json.loads((output / "review.json").read_text())
    if review != {
        "decision": "accept-controlled-projection",
        "basis": "exact supported byte composition and complete scoped comparison",
        "source_installed": False,
        "routine_recovered": False,
        "unresolved": facts["unresolved"],
    }:
        raise ValueError("allocator scoped review changed")
    if not required <= report["artifact_hashes"].keys():
        raise ValueError("allocator artifact identities incomplete")
    for name, identity in report["artifact_hashes"].items():
        path = (output / name).resolve()
        if not path.is_relative_to(output.resolve()) or digest(path) != identity:
            raise ValueError("allocator deduction artifact changed")
    return report


def run_allocator_puzzle(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: one known-slice check in the existing scheduler; callers remain dependency-gated."""
    from engine.improve_loop import run_puzzle_passes
    from engine.scoped_verification import allocator_contract_graph, allocator_frontier

    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "Liero BYOD unavailable"}
    target = root / "targets/liero"
    comparisons = 0

    def frontier() -> dict:
        """Oracle: revalidate before every scheduler decision, including resumption."""
        return allocator_frontier(target, output)

    def check(piece: str) -> dict:
        """Oracle: only the declared deduction slice is executable in this tranche."""
        nonlocal comparisons
        if piece != "allocator.empty-list":
            raise ValueError("unsupported allocator puzzle piece")
        comparisons += 1
        result = run_allocator_deduction(root, output)
        return {
            "status": result["status"],
            "oracle": result["oracle"],
            "reference": str((output / "result.json").resolve()),
        }

    puzzle = run_puzzle_passes(frontier, check, max_passes=2)
    pieces = frontier()
    checked = pieces["allocator.empty-list"]["checked"]
    if checked:
        allocator_contract_graph(target, output).save(output / "contract-graph.json")
    result = {
        "status": "scoped-frontier-blocked" if checked else "failed",
        "known_scope_checked": checked,
        "new_comparisons": comparisons,
        "automatic_new_recoveries": 0,
        "source_recovered": 0,
        "expansion_allowed": False,
        "puzzle": puzzle,
    }
    if output.is_dir():
        save(output / "puzzle.json", result)
    return result


def allocator_candidate_program(cases: list[tuple]) -> str:
    """Oracle: exact host projection harness; not original DOS calling convention."""
    statements = "\n".join(f"  Run({', '.join(map(str, case))});" for case in cases)
    return f"""program AllocatorProjection;
{{$I candidate.inc}}
var f: file; row: array[0..7] of Word; n: LongInt;
procedure Run(requestSize, startOffset, startSegment, limitOffset, limitSegment: Word);
var resultOffset, resultSegment, newOffset, newSegment, savedRequest: Word; failed: Boolean;
begin
  resultOffset := 0; resultSegment := 0; newOffset := startOffset;
  newSegment := startSegment; savedRequest := $a5a5; failed := false;
  FUN_24dd_0353(requestSize, startOffset, startSegment, limitOffset, limitSegment,
    resultOffset, resultSegment, newOffset, newSegment, savedRequest, failed);
  row[0] := resultOffset; row[1] := resultSegment; row[2] := Ord(failed);
  row[3] := newOffset; row[4] := newSegment;
  row[5] := newOffset; row[6] := newSegment; row[7] := savedRequest;
  BlockWrite(f, row, SizeOf(row), n); if n <> SizeOf(row) then Halt(2);
end;
begin
  Assign(f, 'PASCAL.BIN'); Rewrite(f, 1);
{statements}
  Close(f);
end.
"""


def allocator_candidate(
    output: pathlib.Path, source: str, cases: list[tuple]
) -> list[list[int]]:
    """Oracle: compile/run exact generated Pascal include, never a restored baseline."""
    output.mkdir()
    (output / "candidate.inc").write_text(source)
    (output / "probe.pas").write_text(allocator_candidate_program(cases))
    compiled = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "probe.pas"],
        cwd=output,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (output / "compile.log").write_bytes(compiled.stdout + compiled.stderr)
    compiled.check_returncode()
    completed = subprocess.run(
        [str((output / "probe").resolve())],
        cwd=output,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (output / "execution.log").write_bytes(completed.stdout + completed.stderr)
    completed.check_returncode()
    data = (output / "PASCAL.BIN").read_bytes()
    if len(data) != 16 * len(cases):
        raise ValueError("allocator Pascal trace shape differs")
    return [list(row) for row in struct.iter_unpack("<8H", data)]


def run_allocator_trial(
    root: pathlib.Path,
    output: pathlib.Path,
    model: str,
    endpoint: str,
    *,
    scaffold_from: pathlib.Path | None = None,
) -> dict:
    """Oracle: one proposal, training-only selection, one heldout, explicit partial review gate."""
    target = root / "targets/liero"
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        return {"status": "skipped", "reason": "Liero BYOD unavailable"}
    from engine.routine_contract import load_contract
    from tools.liero_candidate_experiment import _local_api_root

    endpoint = _local_api_root(endpoint)
    previous = None
    if scaffold_from is not None:
        previous = json.loads((scaffold_from / "result.json").read_text())
        previous_freeze = json.loads((scaffold_from / "freeze.json").read_text())
        if (
            previous["status"] != "failed"
            or previous["heldout_evaluations"] != 0
            or previous.get("candidate_sha256") is not None
            or not previous.get("error", "").startswith("ValueError: proposal lacks")
            or previous["freeze_sha256"] != digest(scaffold_from / "freeze.json")
            or previous_freeze.get("proposal_mode", "source-json") != "source-json"
        ):
            raise ValueError(
                "format retry requires a rejected declaration and no evaluated candidate/holdout"
            )
    contract = load_contract(target, "FUN_24dd_0353")
    manifest = json.loads((target / "alternate_streams.json").read_text())
    binary, header, _, identity = load_binary_evidence(target, manifest)
    raw = bytes.fromhex(contract["reviewed_bytes_hex"])
    if (
        identity != contract["binary_sha256"]
        or binary[contract["file_offset"] : contract["file_offset"] + len(raw)] != raw
    ):
        raise ValueError("allocator binary identity differs")
    regions = (
        (contract["file_offset"], len(raw)),
        (contract["file_offset"] + 0x4DC - 0x353, 17),
        (contract["file_offset"] + 0xD6 - 0x353, 5),
    )
    if any(
        start - 1 <= r < start + size
        for r in _mz_relocation_locations(binary, header)
        for start, size in regions
    ):
        raise ValueError("allocator copied code has unsupported relocation")
    output.mkdir(parents=True, exist_ok=False)
    training, heldout = allocator_cases("training"), allocator_cases("heldout")
    paths = (
        pathlib.Path(__file__),
        root / "tools/liero_file_probe.py",
        root / "engine/alternate_streams.py",
        target / "config/routine_contracts.json",
    )
    (output / "methods").mkdir()
    for path in paths:
        shutil.copy2(path, output / "methods" / path.name)
    freeze = {
        "function": "FUN_24dd_0353",
        "binary_sha256": identity,
        "oracle": "controlled_original_empty_freelist_vs_generated_pascal",
        "model": leaf_model_identity(model, endpoint),
        "training": [list(case) for case in training],
        "heldout": [list(case) for case in heldout],
        "budget": "one proposal, zero repairs, one training and at most one heldout; original subprocess30s/model600s; no retries",
        "method_hashes": {str(p.relative_to(root)): digest(p) for p in paths},
        "known_scope": "Developer-supplied empty-free-list topology, host projection and a manually known preflight control body. Model sees byte-backed helper/callback/branch facts, not the control body. Not unseen-routine generalization.",
        "review_gate": "Finite pass never promotes routine. Static review must account for complete original paths before source acceptance; unknown branches remain residue.",
        "startup_dependencies": "NONE for controlled COM test. Explicit disjoint writable globals, code, stack and heap guard; authenticated default callback and resolved rounding helper. Actual allocator-entry heap/list/callback lifetime remains unproved.",
        "layout": "DOS COM, require PSP:2 covers64KiB atCS; DS=SS=CS, SP=eff0, code0353/04dc, harness1000..below6000, globals63d8..6410 plus7b3c, heap guard8000..807f. Authenticated callback copied to PSP command-tail scratchd6..da, callback pointer CS:d6. Limit segments are input bounds, not dereferenced. Capture AX/DX/CF/frontier/head/request and original-only global/128-byte heap guards; not all registers or memory.",
        "proposal_mode": "declaration-constrained-known-slice",
        "prior_rejected_freeze_sha256": previous["freeze_sha256"] if previous else None,
        "prior_rejected_result_sha256": digest(scaffold_from / "result.json")
        if scaffold_from
        else None,
    }
    save(output / "freeze.json", freeze)
    prompt = (
        "Recover only the empty-free-list behavior of the original Liero allocator as Pascal. "
        "Return JSON source, one complete procedure, no services/directives/assembler. /no_think\n"
        + ALLOCATOR_INTERFACE
        + "\nHost projection: segments are relative to harness CS; unsigned16-bit values. "
        "newOffset/newSegment initialized to start, savedRequest=$a5a5. "
        "resultOffset/resultSegment and failed must reflect original AX/DX and carry. "
        "Empty-list head equals frontier; branch036d goes03d2, bypasses free-list scan. "
        "Default callback authenticated XOR AX,AX; RETF2. "
        "Failure callback leaves computed DX intact; CMP AL,1 then JB03cd returns with CF1, not through XOR AX/CWD at03ce. "
        "Zero-size path03ce returns AX=DX=0, CF0 and no memory writes. "
        "Nonzero writes savedRequest then calls resolved rounding helper. "
        "Use widened arithmetic and explicit masks; FPC-Mtp-Cr enabled. "
        "Compute only memory/result projection, not register residue. "
        "Known topology supplied by developer, not unseen-routine recovery.\n"
        + json.loads((target / "config/routine_contracts.json").read_text())[
            "functions"
        ]["FUN_24dd_04dc"]["instruction_semantics"]
        + "\nAuthenticated allocator bytes: "
        + raw.hex()
        + "\nAssembly reference (some listing branch addresses use alternate mapping; bytes authoritative):\n"
        + (target / "asm/FUN_24dd_0353.s").read_text()
    )
    schema = {
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "minLength": 160,
                "pattern": "^procedure FUN_24dd_0353.*$",
            }
        },
        "required": ["source"],
        "additionalProperties": False,
    }
    prompt += (
        "\nOUTPUT CONTRACT: JSON object with one source string containing the COMPLETE "
        "Pascal procedure above: declaration, any local variables, begin, implementation, end;. "
        "The first characters inside source MUST be procedure FUN_24dd_0353. "
        "Do NOT return a language name, markdown, explanation or a stub. "
        "Implement zero, success and default-callback failure paths. This attempt changes only "
        "the output-format strategy; no training or heldout results are supplied."
    )
    save(output / "proposal-schema.json", schema)
    (output / "prompt.txt").write_text(prompt)
    freeze["prompt_sha256"] = digest(output / "prompt.txt")
    freeze["proposal_schema"] = schema
    save(output / "freeze.json", freeze)
    freeze_identity = digest(output / "freeze.json")

    def validate_frozen() -> None:
        """Oracle: reject input/method/model drift before exposing any next suite."""
        if (
            json.loads((output / "freeze.json").read_text()) != freeze
            or digest(output / "prompt.txt") != freeze["prompt_sha256"]
            or any(
                digest(path) != freeze["method_hashes"][str(path.relative_to(root))]
                for path in paths
            )
            or leaf_model_identity(model, endpoint) != freeze["model"]
        ):
            raise ValueError("allocator freeze/method/model changed")

    result = {
        "status": "failed",
        "function": "FUN_24dd_0353",
        "source_promoted": False,
        "routine_recovered": False,
        "model_requests": 1,
        "heldout_evaluations": 0,
        "proposal_mode": freeze["proposal_mode"],
        "scope": freeze["known_scope"],
        "unresolved": [
            "free-list exact-fit/split/traversal",
            "nondefault callback/retry",
            "normal-program heap provenance/lifetime",
            "full register/flag ABI",
        ],
    }
    try:
        response = request(prompt, model, endpoint, schema=schema)
        (output / "raw-response.json").write_text(response)
        source = candidate_source(json.loads(response), "FUN_24dd_0353")
        (output / "candidate.inc").write_text(source)
        result["candidate_sha256"] = hashlib.sha256(source.encode()).hexdigest()
        for suite, cases in (("training", training), ("heldout", heldout)):
            validate_frozen()
            if suite == "heldout":
                result["heldout_evaluations"] = 1
            original = allocator_original(
                root, output / f"original-{suite}", cases, binary, contract
            )
            candidate = allocator_candidate(
                output / f"candidate-{suite}", source, cases
            )
            mismatches = [
                i
                for i, pair in enumerate(zip(original, candidate, strict=True))
                if pair[0] != pair[1]
            ]
            result[suite] = {
                "cases": len(cases),
                "passed": len(cases) - len(mismatches),
                "mismatch_indices": mismatches,
            }
            if mismatches:
                result["stop_reason"] = (
                    "training-failure-no-repair-or-heldout"
                    if suite == "training"
                    else "heldout-failure-no-feedback-retry"
                )
                break
        else:
            result.update(
                status="scoped-pass-awaiting-review",
                stop_reason="frozen-budget-complete",
            )
        validate_frozen()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["stop_reason"] = "first-error-no-retry"
    result["freeze_sha256"] = freeze_identity
    result["artifact_hashes"] = {
        str(path.relative_to(output)): digest(path)
        for path in output.rglob("*")
        if path.is_file()
    }
    result["expansion_allowed"] = False
    save(output / "result.json", result)
    return result


def main() -> int:
    """Oracle: report completed measurements without claiming recovery success."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--model", default="qwen2.5-coder:14b-instruct")
    parser.add_argument("--allocator-trial", action="store_true")
    parser.add_argument("--allocator-scaffold-from", type=pathlib.Path)
    parser.add_argument("--allocator-deduction", action="store_true")
    parser.add_argument("--allocator-deduction-replay", action="store_true")
    parser.add_argument("--allocator-puzzle", action="store_true")
    parser.add_argument("--leaf-trials", action="store_true")
    parser.add_argument("--leaf-byte-constraints", action="store_true")
    parser.add_argument("--leaf-fill-sketch", action="store_true")
    parser.add_argument("--leaf-string-sketch", action="store_true")
    parser.add_argument("--optimise-loop-search", action="store_true")
    parser.add_argument("--overnight-hours", type=int, choices=range(1, 9), default=0)
    parser.add_argument("--resume-leaf-trial", type=pathlib.Path)
    parser.add_argument("--routine", choices=tuple(PANEL))
    parser.add_argument("--recovered-examples", action="store_true")
    parser.add_argument("--constrained-close", action="store_true")
    parser.add_argument("--automatic-close-repair", action="store_true")
    parser.add_argument("--automatic-read-repair", action="store_true")
    parser.add_argument("--automatic-constructor-repair", action="store_true")
    parser.add_argument("--constructor-instruction-constraints", action="store_true")
    parser.add_argument("--prefix-transfer-routine")
    parser.add_argument("--partial-memory-source", action="store_true")
    parser.add_argument(
        "--prefix-data-window", nargs=2, type=lambda value: int(value, 0)
    )
    parser.add_argument("--branch-repair-seed", type=pathlib.Path)
    args = parser.parse_args()
    if args.allocator_puzzle:
        if any(
            value
            for key, value in vars(args).items()
            if key not in {"output", "model", "allocator_puzzle"}
        ):
            parser.error("--allocator-puzzle excludes other experiment modes")
        result = run_allocator_puzzle(ROOT, args.output)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] in {"scoped-frontier-blocked", "skipped"} else 1
    if args.allocator_deduction:
        active = {
            key
            for key, value in vars(args).items()
            if value
            and key
            not in {
                "output",
                "model",
                "allocator_deduction",
                "allocator_deduction_replay",
            }
        }
        if active:
            parser.error("--allocator-deduction excludes other experiment modes")
        result = (
            validate_allocator_deduction(ROOT, args.output)
            if args.allocator_deduction_replay
            else run_allocator_deduction(ROOT, args.output)
        )
        print(json.dumps(result, indent=2))
        return 0 if result["status"] in {"passed", "skipped"} else 1
    if args.allocator_deduction_replay:
        parser.error("--allocator-deduction-replay requires --allocator-deduction")
    if args.allocator_trial:
        active = {
            key
            for key, value in vars(args).items()
            if value
            and key
            not in {"output", "model", "allocator_trial", "allocator_scaffold_from"}
        }
        if active:
            parser.error("--allocator-trial excludes other experiment modes")
        result = run_allocator_trial(
            ROOT,
            args.output,
            args.model,
            "http://localhost:11434",
            scaffold_from=args.allocator_scaffold_from,
        )
        print(json.dumps(result, indent=2))
        return (
            0 if result["status"] in {"scoped-pass-awaiting-review", "skipped"} else 1
        )
    if args.allocator_scaffold_from:
        parser.error("--allocator-scaffold-from requires --allocator-trial")
    if args.leaf_string_sketch and (
        not args.leaf_trials
        or not args.leaf_byte_constraints
        or args.resume_leaf_trial
        or args.leaf_fill_sketch
    ):
        parser.error(
            "--leaf-string-sketch requires fresh --leaf-trials --leaf-byte-constraints and excludes fill mode"
        )
    if args.overnight_hours and not args.leaf_string_sketch:
        parser.error("--overnight-hours requires --leaf-string-sketch")
    if args.optimise_loop_search and not args.overnight_hours:
        parser.error("--optimise-loop-search requires --overnight-hours")
    if args.leaf_fill_sketch and (
        not args.leaf_trials or not args.leaf_byte_constraints or args.resume_leaf_trial
    ):
        parser.error(
            "--leaf-fill-sketch requires fresh --leaf-trials --leaf-byte-constraints"
        )
    if args.leaf_trials:
        if any(
            (
                args.routine,
                args.recovered_examples,
                args.constrained_close,
                args.automatic_close_repair,
                args.automatic_read_repair,
                args.automatic_constructor_repair,
                args.constructor_instruction_constraints,
                args.prefix_transfer_routine,
                args.prefix_data_window,
                args.partial_memory_source,
                args.branch_repair_seed,
            )
        ):
            parser.error(
                "--leaf-trials cannot be combined with existing candidate/prefix modes"
            )
        output_existed = args.output.exists()
        try:
            result = run_leaf_trials(
                ROOT,
                args.output,
                args.model,
                "http://localhost:11434",
                byte_constraints=args.leaf_byte_constraints,
                resume_trial=args.resume_leaf_trial,
                fill_sketch=args.leaf_fill_sketch,
                string_sketch=args.leaf_string_sketch,
                stress_seconds=args.overnight_hours * 3600,
                optimise=args.optimise_loop_search,
            )
        except (
            OSError,
            ValueError,
            subprocess.SubprocessError,
            LeafCandidateExecutionError,
        ) as exc:
            if (
                not output_existed
                and (args.output / "freeze.json").is_file()
                and not (args.output / "result.json").exists()
            ):
                save(
                    args.output / "failure.json",
                    {
                        "status": "failed",
                        "error_type": type(exc).__name__,
                        "reason": str(exc),
                    },
                )
                save(
                    args.output / "progress.json",
                    {
                        "status": "failed",
                        "stage": "infrastructure-or-contract-failure",
                        "reason": str(exc),
                    },
                )
            raise
        print(json.dumps(result, indent=2))
        return 0 if result["status"] in {"passed", "skipped"} else 1
    if args.leaf_byte_constraints:
        parser.error("--leaf-byte-constraints requires --leaf-trials")
    if args.resume_leaf_trial:
        parser.error("--resume-leaf-trial requires --leaf-trials")
    if args.partial_memory_source and (
        not args.prefix_transfer_routine or args.prefix_data_window is None
    ):
        parser.error(
            "--partial-memory-source requires --prefix-transfer-routine and --prefix-data-window"
        )
    if args.prefix_transfer_routine:
        if (
            args.routine
            or args.recovered_examples
            or args.constrained_close
            or args.automatic_close_repair
            or args.automatic_read_repair
            or args.automatic_constructor_repair
            or args.constructor_instruction_constraints
            or args.branch_repair_seed
        ):
            parser.error(
                "--prefix-transfer-routine cannot be combined with candidate modes"
            )
        result = run_prefix_transfer(
            ROOT,
            args.output,
            args.prefix_transfer_routine,
            **(
                {"data_window": tuple(args.prefix_data_window)}
                if args.prefix_data_window is not None
                else {}
            ),
        )
        if args.partial_memory_source and result["status"] != "skipped":
            write_partial_memory_source(ROOT, args.output)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] in ("prefix-decoded", "skipped") else 1
    if args.prefix_data_window is not None:
        parser.error("--prefix-data-window requires --prefix-transfer-routine")
    if args.branch_repair_seed:
        if (
            args.routine != "close"
            or args.recovered_examples
            or args.constrained_close
            or args.automatic_close_repair
            or args.automatic_read_repair
            or args.automatic_constructor_repair
            or args.constructor_instruction_constraints
        ):
            parser.error("--branch-repair-seed requires only --routine close")
        result = run_close_branch_repair(ROOT, args.output, args.branch_repair_seed)
        print(json.dumps(result, indent=2))
        return 0 if result["status"] in ("passed", "skipped") else 1
    if args.constrained_close and args.routine != "close":
        parser.error("--constrained-close requires --routine close")
    if args.automatic_close_repair:
        if args.routine != "close":
            parser.error("--automatic-close-repair requires --routine close")
        args.constrained_close = True
    if args.automatic_read_repair and args.routine != "read":
        parser.error("--automatic-read-repair requires --routine read")
    if args.automatic_constructor_repair and args.routine != "constructor":
        parser.error("--automatic-constructor-repair requires --routine constructor")
    if args.constructor_instruction_constraints:
        if args.routine != "constructor":
            parser.error(
                "--constructor-instruction-constraints requires --routine constructor"
            )
        args.automatic_constructor_repair = True
    if args.recovered_examples and args.routine != "close":
        parser.error(
            "--recovered-examples is limited to the bounded --routine close trial"
        )
    if args.routine:
        if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
            print("SKIP: Liero BYOD executable unavailable")
            return 0
        args.output.parent.mkdir(parents=True, exist_ok=True)
        protected = [ROOT / "targets/liero/recovery.json"] + [
            ROOT / "targets/liero/src" / f"{item[0]}.inc" for item in PANEL.values()
        ]
        before = {str(path): digest(path) for path in protected}
        result = run_routine(
            ROOT,
            args.output.resolve(),
            args.routine,
            args.model,
            "http://localhost:11434",
            4,
            use_recovered=args.recovered_examples,
            constrained_close=args.constrained_close,
            automatic_close_repair=args.automatic_close_repair,
            automatic_read_repair=args.automatic_read_repair,
            automatic_constructor_repair=args.automatic_constructor_repair,
            constructor_instruction_constraints=args.constructor_instruction_constraints,
        )
        if {str(path): digest(path) for path in protected} != before:
            raise ValueError("protected repository source/ledger changed during trial")
        result["protected_hashes"] = before
        result["model"] = args.model
        save(args.output / "result.json", result)
    else:
        result = run_pilot(ROOT, args.output, model=args.model)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in ("completed", "passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
