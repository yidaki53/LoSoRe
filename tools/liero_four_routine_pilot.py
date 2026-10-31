"""Bounded local-model pilot using four existing Liero binary-backed probes."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from collections.abc import Callable

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine import knowledge
from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.instruction_facts import initialization_prefix
from engine.recovery import audit_target
from tools import liero_compare_routine_probe as compare
from tools import liero_constructor_probe as constructor
from tools import liero_read_handler_probe as handler

PANEL = {
    "constructor": ("FUN_24dd_3639", 0x3639, 83),
    "comparator": ("FUN_24dd_3f86", 0x3F86, 43),
    "read": ("FUN_24dd_375e", 0x375E, 48),
    "close": ("FUN_24dd_37d3", 0x37D3, 25),
}
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
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


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


def request(
    prompt: str, model: str, endpoint: str, *, schema: dict | None = None
) -> str:
    """Oracle: local structured proposal only; binary probes decide acceptance."""
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
        "options": {"temperature": 0.0, "num_predict": 2048},
    }
    message = urllib.request.Request(
        endpoint.rstrip("/") + "/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(message, timeout=600) as response:
        return response.read().decode("utf-8")


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


def main() -> int:
    """Oracle: report completed measurements without claiming recovery success."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--model", default="qwen2.5-coder:14b-instruct")
    parser.add_argument("--routine", choices=tuple(PANEL))
    parser.add_argument("--recovered-examples", action="store_true")
    parser.add_argument("--constrained-close", action="store_true")
    parser.add_argument("--automatic-close-repair", action="store_true")
    parser.add_argument("--automatic-read-repair", action="store_true")
    parser.add_argument("--automatic-constructor-repair", action="store_true")
    parser.add_argument("--constructor-instruction-constraints", action="store_true")
    parser.add_argument("--prefix-transfer-routine")
    parser.add_argument(
        "--prefix-data-window", nargs=2, type=lambda value: int(value, 0)
    )
    parser.add_argument("--branch-repair-seed", type=pathlib.Path)
    args = parser.parse_args()
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
