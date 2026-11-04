"""Integrated SS-attribute arithmetic through the actual shortstring caller prefix.

Oracle: original 249c:0037..0060 and 249c:0013 bytes, installed Pascal,
complete owned arena/state differential. Remainder of0037 is unresolved.
"""

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
from tools import liero_source_trial as trial

ROOT = trial.ROOT
CALLER = bytes.fromhex(
    "c80a01008cd38ec38cdbfc8dbe00ffc57606acaa9130edf3a48edbc686fcfe07c686fbfe0055e8b3ff"
)
CALLER_TAIL = bytes.fromhex("c9ca0800")
CURSOR_BYTES = bytes.fromhex("5589e5b402b7008a76068a5608cd10c9ca0400")
ERROR_CHECK_BYTES = bytes.fromhex("833e1064007501cba11064e90dfc")
WRITE_WORD_BYTES = bytes.fromhex(
    "558becc45e06b80200be24648cdae858ff750a26837f1a007403e82d005dca0400"
)
BUFFER_WRITE_BYTES = bytes.fromhex(
    "833e106400754826817f02b2d77541268b4f04268b7f082bcf2bc1730403c833c01e06538eda26c45f0c03fbfcf3a42bfb5b071f26897f08263b7f04750d5052560653e88d005b075e5a580bc075c0c3c70610646900c3"
)
METHODS = (
    "engine/evidence_archive.py",
    "tools/liero_nibble_caller.py",
    "tools/liero_source_trial.py",
    "tools/liero_file_probe.py",
    "targets/liero/src/FUN_249c_0013.inc",
    "targets/liero/src/LieroRuntime.pas",
)


def cursor_contract(root: pathlib.Path) -> dict:
    """Oracle: original19-byte BIOS adapter and actual0037 PUSH/CALL argument origins."""
    target = root / "targets/liero"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    start = header + (0x249C - base) * 16
    caller = bytes.fromhex("8a460c508a460a500ee87dff")
    if (
        binary[start : start + len(CURSOR_BYTES)] != CURSOR_BYTES
        or binary[start + 0x77 : start + 0x83] != caller
    ):
        raise ValueError("cursor original routine/caller bytes differ")
    if any(
        start - 1 <= p < start + len(CURSOR_BYTES)
        for p in _mz_relocation_locations(binary, header)
    ):
        raise ValueError("cursor original routine relocation differs")
    return {
        "binary_sha256": identity,
        "bytes": CURSOR_BYTES.hex(),
        "entry": "249c:0000",
        "caller_slice": "249c:0077..0083",
        "caller_bytes": caller.hex(),
        "arguments": "two16-bit stack words; last pushed row atcalleeBP+6, column atBP+8; only low bytes used",
        "service": "INT10/AH02, BH0 display page, DH=row, DL=column",
        "return": "LEAVE/RETF4 balances saved BP, far return and4argument bytes; native calleeSP+8",
        "scope": "Logical cursor position input/page0 and bounded DOSBox BIOS-state observation only",
        "unknown": [
            "BIOS-specific register/flags clobbers and external device effects",
            "Video mode/page validity and normal reachability",
            "Native TP7 ABI/type identity",
            "Other caller state",
        ],
        "whole_routine_accepted": False,
    }


def text_dependency_contracts(root: pathlib.Path) -> dict:
    """Oracle: exact static callee/path facts; unresolved dispatch/error paths never count as resolution."""
    target = root / "targets/liero"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    for offset, raw in (
        (0x04F4, ERROR_CHECK_BYTES),
        (0x3930, WRITE_WORD_BYTES),
        (0x3899, BUFFER_WRITE_BYTES),
    ):
        start = header + (0x24DD - base) * 16 + offset
        if binary[start : start + len(raw)] != raw or any(
            start - 1 <= p < start + len(raw)
            for p in _mz_relocation_locations(binary, header)
        ):
            raise ValueError("text dependency original bytes/relocations differ")
    return {
        "binary_sha256": identity,
        "FUN_24dd_04f4": {
            "bytes": ERROR_CHECK_BYTES.hex(),
            "conditional_return": "DS:[6410]=0: CMPword0 thenRETF, no non-stack writes, CF0/ZF1, AXpreserved,SPentry+4",
            "error_path": "DS:[6410]nonzero: AX=stickyerror, nearJMP010f inherits existing farreturn frame, never a guessed return",
            "blockers": [
                "010f error service/dispatch/return contract",
                "Proven DS global provenance and disjoint active stack",
            ],
            "whole_routine_resolved": False,
        },
        "FUN_24dd_3899": {
            "bytes": BUFFER_WRITE_BYTES.hex(),
            "conditional_return": "Sticky DS:[6410]nonzero: nearRET preserves inputs except CMPflags. Invalid ES:BX modeword+2 !=D7B2 with zero sticky: stores105 toDS6410 andRET.",
            "write_path": "ModeD7B2: copies AXbytes fromDX:SI toobjectfarbuffer+used, updatesword+8. Capacityword+4-used; full buffer calls396c and may repeat. SourceDS=DX only inside savedsegment block; restoresDS/ES/BX beforeobjectwrite.",
            "blockers": [
                "Writable/nonaliasing object,buffer,source,global and active-stack bounds",
                "Output-mode396c method atobject+20, not existing input-method375e projection",
                "Callback return/error/progress obligations to avoid infinite loop",
            ],
            "whole_routine_resolved": False,
        },
        "FUN_24dd_3930": {
            "bytes": WRITE_WORD_BYTES.hex(),
            "operations": "LESBX fromonefarargument, AX2,SI6424,DXentryDS; nearCALL3899; ifZF andobjectword+26nonzero nearCALL397a; POPBP/RETF4",
            "blockers": [
                "3899 outputwrite/fullbuffer contract",
                "397a optionalmethod target/slot26word and callbackeffects",
                "ProvenDS6424 two-byte source and originalobject provenance",
            ],
            "whole_routine_resolved": False,
        },
        "caller": "FUN_249c_0037",
        "scope": "Static original-byte contracts and conditional paths only; no source acceptance, service/whole-caller parity or model learning.",
    }


def cursor_harness() -> str:
    """Oracle: unchanged original BIOS bytes plus query/BDA observation; unrelated registers not used as parity."""
    text = trial.harness("FUN_249c_0013")
    # The shared assembler text spaces its byte list.
    old = ", ".join(
        "0x" + trial.routine_spec("FUN_249c_0013")["bytes"][i : i + 2]
        for i in range(0, 72, 2)
    )
    query = """
    mov $0x0300, %ax
    xor %bx, %bx
    int $0x10
    mov %dx, 0x8000
    push %es
    mov $0x40, %ax
    mov %ax, %es
    mov %es:0x50, %ax
    mov %ax, 0x8002
    mov %es:0x49, %ax
    mov %ax, 0x8004
    mov %es:0x4a, %ax
    mov %ax, 0x8006
    pop %es
"""
    for before, after in (
        (old, ", ".join(hex(b) for b in CURSOR_BYTES)),
        ("    pushw input\n", "    pushw input+2\n    pushw input\n"),
        ("sub $2, %ax", "sub $4, %ax"),
        ("    call original", "    push %cs\n    call original"),
        ("    cld\n    mov $0x8000, %si", query + "    cld\n    mov $0x8000, %si"),
    ):
        if text.count(before) != 1:
            raise ValueError(
                "cursor base harness binding missing or ambiguous: " + before
            )
        text = text.replace(before, after, 1)
    return text


def run_cursor(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: original BIOS state observations over frozen bounded valid text coordinates."""
    checked = cursor_contract(root)
    output.mkdir()
    cursor_methods = ("tools/liero_nibble_caller.py", "engine/evidence_archive.py")
    (output / "methods").mkdir()
    for name in cursor_methods:
        shutil.copy2(root / name, output / "methods" / pathlib.Path(name).name)
    rng = random.Random(20261109)
    inputs = [
        struct.pack(
            "<4H", row | ((index & 255) << 8), column | (((index + 1) & 255) << 8), 0, 0
        )
        + rng.randbytes(trial.ARENA)
        for index, (row, column) in enumerate(
            (r, c) for r in (0, 1, 12, 24) for c in (0, 1, 40, 79)
        )
    ]
    (output / "harness.S").write_text(cursor_harness())
    image = trial.assemble_probe(output / "harness.S", output)
    if image.count(CURSOR_BYTES) != 1 or len(image) + 0x100 >= 0x6000:
        raise ValueError("cursor image overlaps owned arena or original bytes missing")
    (output / "PROBE.COM").write_bytes(image)
    (output / "CASES.BIN").write_bytes(b"".join(inputs))
    trial.pilot.save(
        output / "freeze.json",
        {
            "contract": checked,
            "method_hashes": {
                name: trial.pilot.digest(root / name) for name in cursor_methods
            },
            "corpus_sha256": hashlib.sha256(b"".join(inputs)).hexdigest(),
            "harness_sha256": hashlib.sha256(cursor_harness().encode()).hexdigest(),
            "policy": "Original BIOS service observation and separate logical Pascal cursor projection, not full ABI parity or statistical evaluation",
            "video_premise": "DOSBox default text mode3/80columns, verified from BDA40:49/4a for every case",
            "source_sha256": trial.pilot.digest(
                root / "targets/liero/src/FUN_249c_0000.inc"
            ),
            "runtime_sha256": trial.pilot.digest(
                root / "targets/liero/src/LieroRuntime.pas"
            ),
        },
    )
    trial.run_dosbox(output)
    trace = (output / "TRACE.BIN").read_bytes()
    if len(trace) != len(inputs) * trial.RECORD_BYTES:
        raise ValueError("cursor original observation partial")
    failures = []
    observations = []
    for index, data in enumerate(inputs):
        native = trace[index * trial.RECORD_BYTES : (index + 1) * trial.RECORD_BYTES]
        row, column = struct.unpack_from("<2H", data)
        desired = ((row & 255) << 8) | (column & 255)
        query, bda, mode_columns, columns = struct.unpack_from("<4H", native, 32)
        snapshot = struct.unpack_from("<16H", native)
        unchanged = native[40:] == data[16:]
        if (
            query != desired
            or bda != desired
            or mode_columns != 0x5003
            or columns != 80
            or snapshot[7] != 0xEFE8
            or snapshot[8] != 0xEFF0
            or snapshot[6] != 0x6789
            or snapshot[13:15] != (0x1357, 0x2468)
            or not unchanged
        ):
            failures.append(index)
        observations.append(
            {
                "case": index,
                "row": row & 255,
                "column": column & 255,
                "query_word": query,
                "bda_word": bda,
                "mode": mode_columns & 255,
                "columns": columns,
                "native_snapshot": list(snapshot),
            }
        )
    result = {
        "status": "failed" if failures else "passed",
        "cases": len(inputs),
        "matches": len(inputs) - len(failures),
        "failures": failures,
        "observations": observations,
        "model_requests": 0,
        "oracle": "original-BIOS-cursor-state-observation",
        "pascal_parity": False,
        "whole_routine_accepted": False,
    }
    candidate = output / "host"
    candidate.mkdir()
    shutil.copy2(
        root / "targets/liero/src/FUN_249c_0000.inc", candidate / "candidate.inc"
    )
    shutil.copy2(
        root / "targets/liero/src/LieroRuntime.pas", candidate / "LieroRuntime.pas"
    )
    frozen = json.loads((output / "freeze.json").read_text())
    if (
        trial.pilot.digest(candidate / "candidate.inc") != frozen["source_sha256"]
        or trial.pilot.digest(candidate / "LieroRuntime.pas")
        != frozen["runtime_sha256"]
    ):
        raise ValueError("cursor source/runtime changed during observation")
    (candidate / "probe.pas").write_text("""program CursorProjection;
uses LieroRuntime;
{$I candidate.inc}
var input: array[0..3] of Word; arena: array[0..4095] of Byte;
    observed: array[0..2] of Word; f,g:file; n,i:LongInt;
begin
  for i := 0 to 65535 do begin
    RegisterSP := $fff8;
    FUN_249c_0000(Word(i),Word(65535-i));
    if (BIOSCursorColumn<>(i and 255)) or
       (BIOSCursorRow<>((65535-i) and 255)) or (RegisterSP<>0) then Halt(4);
  end;
  Assign(f,'CASES.BIN'); Reset(f,1); Assign(g,'CURSOR.BIN'); Rewrite(g,1);
  while not Eof(f) do begin
    BlockRead(f,input,8,n); if n<>8 then Halt(1);
    BlockRead(f,arena,4096,n); if n<>4096 then Halt(2);
    RegisterSP := $efe8;
    FUN_249c_0000(input[1],input[0]);
    observed[0] := BIOSCursorRow; observed[1] := BIOSCursorColumn;
    observed[2] := RegisterSP;
    BlockWrite(g,observed,6,n); if n<>6 then Halt(3);
  end;
  Close(f);Close(g);
end.
""")
    build = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fu.", "-FU.", "probe.pas"],
        cwd=candidate,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (candidate / "compile.log").write_bytes(build.stdout + build.stderr)
    if build.returncode:
        raise ValueError("cursor logical projection compilation failed")
    shutil.copy2(output / "CASES.BIN", candidate / "CASES.BIN")
    execution = subprocess.run(
        [str(candidate / "probe")],
        cwd=candidate,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (candidate / "runtime.log").write_bytes(execution.stdout + execution.stderr)
    if execution.returncode:
        raise ValueError("cursor logical projection execution failed")
    host = (candidate / "CURSOR.BIN").read_bytes()
    if len(host) != 6 * len(inputs):
        raise ValueError("cursor logical projection partial records")
    host_matches = sum(
        struct.unpack_from("<3H", host, index * 6)
        == (item["row"], item["column"], 0xEFF0)
        for index, item in enumerate(observations)
    )
    result["logical_cursor_matches"] = host_matches
    result["logical_word_boundary_cases"] = 65536
    result["logical_cursor_projection"] = (
        "Only page0 row,column and declaredSP; no full register/flag/device parity"
    )
    if host_matches != len(inputs):
        raise ValueError(
            "cursor logical projection differs from original observed position"
        )
    trial.pilot.save(output / "result.json", result)
    if any(
        trial.pilot.digest(root / name) != digest
        for name, digest in frozen["method_hashes"].items()
    ):
        raise ValueError("cursor methods changed during evaluation")
    seal_archive(output)
    if failures:
        raise ValueError("original BIOS cursor observation contradicts input contract")
    return result


def replay_cursor(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: saved original BIOS query/BDA observations and installed logical projection, no execution."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    for name, digest in frozen.get("method_hashes", {}).items():
        if (
            hashlib.sha256(archive["methods/" + pathlib.Path(name).name]).hexdigest()
            != digest
        ):
            raise ValueError("cursor method snapshot changed")
    if (
        frozen["contract"] != cursor_contract(root)
        or hashlib.sha256(archive["host/candidate.inc"]).hexdigest()
        != frozen["source_sha256"]
        or hashlib.sha256(archive["host/LieroRuntime.pas"]).hexdigest()
        != frozen["runtime_sha256"]
        or hashlib.sha256(archive["harness.S"]).hexdigest() != frozen["harness_sha256"]
    ):
        raise ValueError("cursor contract/source changed")
    payload = archive["CASES.BIN"]
    if hashlib.sha256(payload).hexdigest() != frozen["corpus_sha256"]:
        raise ValueError("cursor corpus changed")
    result = json.loads(archive["result.json"])
    native = archive["TRACE.BIN"]
    host = archive["host/CURSOR.BIN"]
    if (
        len(native) != result["cases"] * trial.RECORD_BYTES
        or len(host) != result["cases"] * 6
        or len(payload) != result["cases"] * trial.CASE_BYTES
        or len(result["observations"]) != result["cases"]
    ):
        raise ValueError("cursor traces partial")
    for index, item in enumerate(result["observations"]):
        if item["case"] != index:
            raise ValueError("cursor observation order changed")
        row, column = struct.unpack_from("<2H", payload, index * trial.CASE_BYTES)
        native_word, bda_word, mode_columns, columns = struct.unpack_from(
            "<4H", native, index * trial.RECORD_BYTES + 32
        )
        expected_word = ((row & 255) << 8) | (column & 255)
        if (
            native_word != bda_word
            or native_word != expected_word
            or native_word != item["query_word"]
            or bda_word != item["bda_word"]
            or mode_columns != 0x5003
            or columns != 80
            or item["mode"] != 3
            or item["columns"] != 80
        ):
            raise ValueError("cursor original service state replay differs")
        snapshot = struct.unpack_from("<16H", native, index * trial.RECORD_BYTES)
        if (
            list(snapshot) != item["native_snapshot"]
            or snapshot[7:9] != (0xEFE8, 0xEFF0)
            or snapshot[6] != 0x6789
            or snapshot[13:15] != (0x1357, 0x2468)
            or native[
                index * trial.RECORD_BYTES + 40 : (index + 1) * trial.RECORD_BYTES
            ]
            != payload[index * trial.CASE_BYTES + 16 : (index + 1) * trial.CASE_BYTES]
        ):
            raise ValueError("cursor original stack/guard/arena replay differs")
        if struct.unpack_from("<3H", host, index * 6) != (
            row & 255,
            column & 255,
            0xEFF0,
        ):
            raise ValueError("cursor host projection replay differs")
    if (
        result["status"] != "passed"
        or result["failures"]
        or result["matches"] != result["cases"]
        or result["logical_cursor_matches"] != result["cases"]
        or result["pascal_parity"]
        or result["whole_routine_accepted"]
    ):
        raise ValueError("cursor saved scope/counts differ")
    return result


def contract(root: pathlib.Path) -> dict:
    """Oracle: original caller near-call displacement, segment directions and actual relocation absence."""
    target = root / "targets/liero"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    start = header + (0x249C - base) * 16 + 0x37
    callee = header + (0x249C - base) * 16 + 0x13
    raw = bytes.fromhex(trial.routine_spec("FUN_249c_0013")["bytes"])
    if (
        base != 0x1000
        or binary[start : start + len(CALLER)] != CALLER
        or binary[callee : callee + len(raw)] != raw
    ):
        raise ValueError("arithmetic original caller/callee bytes differ")
    if any(
        callee - 1 <= p < start + len(CALLER)
        for p in _mz_relocation_locations(binary, header)
    ):
        raise ValueError("arithmetic caller/callee unexpected relocation")
    if 0x60 + int.from_bytes(CALLER[-2:], "little", signed=True) != 0x13:
        raise ValueError("arithmetic near-call target differs")
    return {
        "binary_sha256": identity,
        "caller": "FUN_249c_0037",
        "slice": "249c:0037..0060",
        "caller_bytes": CALLER.hex(),
        "callee_bytes": raw.hex(),
        "call_site": "249c:005d",
        "callee_entry": "249c:0013",
        "relocations": [],
        "original_argument": "PUSH BP; one16-bit word; type name not recoverable",
        "caller_frame": "ENTER10a,0; ES=SS from8cd3/8ec3; BX preserves entryDS; LDS source at SS:[BP+6];8edb restoresDS",
        "operation": "copy length-prefixed string to SS:[BP-100], set frame cells(BP-104)=7,(BP-105)=0, call0013, yielding(BP-103)=7",
        "fixture": "SS=DS=CS owned arena8000..9000; SP8480, far entry8474, BP8472, localSP8368, calleeSP8364; source8200..82ff",
        "instrumentation": "Stop before0060: appended LEAVE/RETF8; interrupts disabled through capture, then restored before DOS. Capture PUSHF writes0002 at847e; not original caller completion.",
        "scope": "Actual shortstring/attribute initialization prefix only; source length0..255; disjoint source/local frame/return/code.",
        "obligations": [
            "0037 remainder calls0000,3930 and04f4: unresolved contracts; defer full caller",
            "Other0013 callers at0107/011e and their frame/control states",
            "Native TP7 argument types and ABI, normal-program reachability",
            "Different DS/SS aliases, active stack overwrite, asynchronous mutation",
            "User source review signoff",
        ],
        "whole_caller_accepted": False,
        "whole_routine_promoted": False,
    }


def cases(suite: str) -> list[bytes]:
    """Oracle: frozen corpus with all byte shortstring lengths, no terminal feedback."""
    if suite not in {"training", "terminal"}:
        raise ValueError("unknown arithmetic caller suite")
    rng = random.Random(20261107 if suite == "training" else 20261108)
    result = []
    for length in range(256):
        memory = bytearray(rng.randbytes(trial.ARENA))
        memory[0x200] = length
        result.append(struct.pack("<4H", 0, 0x8200, 0, (length % 2) * 0x441) + memory)
    return result


def expected(data: bytes, segment: int, *, native: bool) -> bytes:
    """Oracle: actual ENTER/shortstring/near callee frame, all writes and complete arena."""
    if len(data) != trial.CASE_BYTES or not 0x100 <= segment <= 0x9000:
        raise ValueError("invalid arithmetic caller input/segment")
    row, source, column, entry_flags = struct.unpack_from("<4H", data)
    if row or column or source != 0x8200 or entry_flags not in (0, 0x441):
        raise ValueError("arithmetic caller inputs outside frozen scope")
    memory = bytearray(data[8:])
    length = memory[0x200]
    memory[0x372 : 0x373 + length] = memory[0x200 : 0x201 + length]
    # Actual frames are inside captured arena; instrumentation return addresses
    # vary with assembled load placement and are accounted separately.
    for offset, value in (
        (0x480, 0x1357),
        (0x482, 0x2468),
        (0x472, 0x6789),
        (0x478, source),
        (0x47A, segment),
        (0x47C, 0),
        (0x47E, 2),
        (0x366, 0x8472),
        (0x362, 0x8472),
        (0x364, 0x0060),
    ):
        struct.pack_into("<H", memory, offset, value)
    memory[0x36D] = 0
    memory[0x36E] = 7
    memory[0x36F] = 7
    flags = 0
    return (
        struct.pack(
            "<16H",
            7,
            segment,
            0,
            7,
            source + length + 1,
            0x8472,
            0x6789,
            0x8474,
            0x8480,
            segment,
            segment,
            segment,
            flags,
            0x1357,
            0x2468,
            segment,
        )
        + memory
    )


def compare(
    inputs: list[bytes],
    trace: bytes,
    *,
    native: bool,
    return_offset: int,
    return_segment: int,
) -> dict:
    """Oracle: all caller state plus owned stack bytes, including explicit bridge return identity."""
    if len(trace) != len(inputs) * trial.RECORD_BYTES:
        raise ValueError("partial arithmetic caller trace")
    failures = []
    for index, data in enumerate(inputs):
        observed = bytearray(
            trace[index * trial.RECORD_BYTES : (index + 1) * trial.RECORD_BYTES]
        )
        segment = struct.unpack_from("<H", observed, 30)[0] if native else 0x2000
        want = bytearray(expected(data, segment, native=native))
        struct.pack_into("<HH", want, 32 + 0x474, return_offset, return_segment)
        struct.pack_into(
            "<H",
            observed,
            24,
            struct.unpack_from("<H", observed, 24)[0] & (0xCC5 if native else 0x441),
        )
        if observed != want:
            failures.append(
                {
                    "case": index,
                    "bytes": [
                        j
                        for j, (a, b) in enumerate(zip(observed, want, strict=True))
                        if a != b
                    ][:20],
                }
            )
    return {
        "status": "failed" if failures else "passed",
        "cases": len(inputs),
        "matches": len(inputs) - len(failures),
        "failures": failures,
    }


def harness() -> str:
    """Oracle: allocated original near-call segment, unchanged caller/callee plus explicit exit instrumentation."""
    text = trial.harness("FUN_249c_0013")
    setup = """
    mov $0x1000, %bx
    mov $0x4a00, %ax
    int $0x21
    jc failed
    mov $0x1000, %bx
    mov $0x4800, %ax
    int $0x21
    jc failed
    mov %ax, caller_pointer+2
    mov %ax, %es
    mov $original, %si
    mov $0x13, %di
    mov $36, %cx
    rep movsb
    mov $caller_bytes, %si
    mov $0x37, %di
    mov $45, %cx
    rep movsb
    push %cs
    pop %es
"""
    text = text.replace(
        "    mov $input_name, %dx", setup + "    mov $input_name, %dx", 1
    )
    text = text.replace(
        "    movw $0x1357, %ss:0xeff0",
        "    mov $0x8480, %sp\n    movw $0x1357, %ss:0x8480",
    )
    text = text.replace("%ss:0xeff2", "%ss:0x8482").replace("%ss:0xeff0", "%ss:0x8480")
    text = text.replace(
        "    pushw input\n",
        "    pushw input+4\n    pushw input\n    push %cs\n    pushw input+2\n",
        1,
    )
    text = text.replace("sub $2, %ax", "sub $4, %ax").replace(
        "    \n    call original", "    lcall *caller_pointer"
    )
    text = text.replace("    mov $0x1234, %ax", "    cli\n    mov $0x1234, %ax")
    text = text.replace(
        "    mov output_handle, %bx\n    mov $snapshot, %dx",
        "    sti\n    mov output_handle, %bx\n    mov $snapshot, %dx",
    )
    if "call original" in text:
        text = text.replace("call original", "lcall *caller_pointer")
    return text.replace(
        "input_name:",
        "caller_pointer: .word 0x37,0\ncaller_bytes: .byte "
        + ",".join(hex(b) for b in CALLER + CALLER_TAIL)
        + "\ninput_name:",
        1,
    )


def program(return_offset: int, return_segment: int) -> str:
    """Oracle: installed source through byte-bound original prefix; unknown remainder is not executed."""
    text = trial.program("FUN_249c_0013")
    start = text.index("    FUN_249c_0013(")
    end = text.index("\n    row[0]", start)
    body = f"""
    for copied := 0 to 4095 do RealModeMemory[$28000 + copied] := arena[copied];
    length := RealModeMemory[$28200];
    for copied := 0 to length do RealModeMemory[$28372 + copied] := RealModeMemory[$28200 + copied];
    WriteWordLE(@RealModeMemory[$28000], $480, $1357);
    WriteWordLE(@RealModeMemory[$28000], $482, $2468);
    WriteWordLE(@RealModeMemory[$28000], $472, $6789);
    WriteWordLE(@RealModeMemory[$28000], $474, {return_offset});
    WriteWordLE(@RealModeMemory[$28000], $476, {return_segment});
    WriteWordLE(@RealModeMemory[$28000], $478, input[1]);
    WriteWordLE(@RealModeMemory[$28000], $47a, $2000);
    WriteWordLE(@RealModeMemory[$28000], $47c, 0);
    WriteWordLE(@RealModeMemory[$28000], $47e, 2);
    WriteWordLE(@RealModeMemory[$28000], $366, $8472);
    WriteWordLE(@RealModeMemory[$28000], $362, $8472);
    WriteWordLE(@RealModeMemory[$28000], $364, $60);
    RealModeMemory[$2836d] := 0; RealModeMemory[$2836e] := 7;
    RegisterSP := $8364; RegisterBP := $8472;
    RegisterAX := $2468; RegisterBX := $2000; RegisterCX := 0;
    RegisterSI := input[1] + length + 1; RegisterDI := $8373 + length;
    RegisterDirectionFlag := False;
    FUN_249c_0013(Integer(RegisterBP));
    RegisterBP := $6789; RegisterSP := $8480;
    for copied := 0 to 4095 do arena[copied] := RealModeMemory[$28000 + copied];"""
    text = text[:start] + body + text[end:]
    text = text.replace("entry := $eff0 - 2 - 2", "entry := $8474")
    return text.replace(
        "inputFile, outputFile: file;",
        "copied, length: LongInt;\n    inputFile, outputFile: file;",
    )


def run(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: freeze installed source/caller before training; terminal once only after full pass."""
    checked_contract = contract(root)
    output.mkdir()
    original_dir = output / "original-training"
    original_dir.mkdir()
    (original_dir / "harness.S").write_text(harness())
    image = trial.assemble_probe(original_dir / "harness.S", original_dir)
    if len(image) + 0x100 >= 0x6000 or image.count(CALLER) != 1:
        raise ValueError("arithmetic image overlaps arena or original bytes absent")
    # GNU indirect far-call FF /3 is followed by the AX snapshot store.
    marker = bytes.fromhex("ff1e")
    call_at = image.index(marker)
    if image.count(marker) != 1:
        raise ValueError("arithmetic caller bridge return not unique")
    return_offset = call_at + 4 + 0x100
    frozen = {
        "contract": checked_contract,
        "return_offset": return_offset,
        "method_hashes": {n: trial.pilot.digest(root / n) for n in METHODS},
        "corpora": {
            s: hashlib.sha256(b"".join(cases(s))).hexdigest()
            for s in ("training", "terminal")
        },
        "harness_sha256": hashlib.sha256(harness().encode()).hexdigest(),
        "model_requests": 0,
    }
    methods = output / "methods"
    methods.mkdir()
    for name in METHODS:
        shutil.copy2(root / name, methods / pathlib.Path(name).name)
    trial.pilot.save(output / "freeze.json", frozen)
    result = {
        "model_requests": 0,
        "source_installed": True,
        "whole_caller_accepted": False,
        "scope": checked_contract["scope"],
        "examples_promoted": 0,
        "weights_changed": False,
    }
    for suite in ("training", "terminal"):
        directory = output / f"original-{suite}"
        directory.mkdir(exist_ok=True)
        (directory / "harness.S").write_text(harness())
        (directory / "PROBE.COM").write_bytes(image)
        inputs = cases(suite)
        (directory / "CASES.BIN").write_bytes(b"".join(inputs))
        trial.run_dosbox(directory)
        trace = (directory / "TRACE.BIN").read_bytes()
        fixture_segment = struct.unpack_from("<H", trace, 30)[0]
        allocated_segment = struct.unpack_from("<H", trace, 32 + 0x476)[0]
        if allocated_segment != fixture_segment:
            raise ValueError("arithmetic bridge returnCS differs from fixtureCS")
        native = compare(
            inputs,
            trace,
            native=True,
            return_offset=return_offset,
            return_segment=allocated_segment,
        )
        trial.pilot.save(directory / "result.json", native)
        if native["status"] != "passed":
            raise ValueError(
                "original arithmetic caller contradicts full-state contract"
            )
        candidate = output / f"host-{suite}"
        candidate.mkdir()
        shutil.copy2(
            root / "targets/liero/src/FUN_249c_0013.inc", candidate / "candidate.inc"
        )
        (candidate / "probe.pas").write_text(program(return_offset, 0x2000))
        build = subprocess.run(
            [
                "fpc",
                "-Mtp",
                "-Cr",
                f"-Fu{root / 'targets/liero/src'}",
                "-FU.",
                "probe.pas",
            ],
            cwd=candidate,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (candidate / "compile.log").write_bytes(build.stdout + build.stderr)
        if build.returncode:
            raise ValueError("installed arithmetic caller compilation failed")
        (candidate / "CASES.BIN").write_bytes(b"".join(inputs))
        executed = subprocess.run(
            [str(candidate / "probe")],
            cwd=candidate,
            capture_output=True,
            timeout=30,
            check=False,
        )
        (candidate / "runtime.log").write_bytes(executed.stdout + executed.stderr)
        if executed.returncode:
            raise ValueError("installed arithmetic caller execution failed")
        result[suite] = compare(
            inputs,
            (candidate / "PASCAL.BIN").read_bytes(),
            native=False,
            return_offset=return_offset,
            return_segment=0x2000,
        )
        result[f"{suite}_segments"] = {
            "fixture": fixture_segment,
            "code": allocated_segment,
        }
        if result[suite]["status"] != "passed":
            break
    if any(
        trial.pilot.digest(root / name) != digest
        for name, digest in frozen["method_hashes"].items()
    ):
        raise ValueError("arithmetic integration methods changed during evaluation")
    trial.pilot.save(output / "result.json", result)
    seal_archive(output)
    return result


def replay(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: frozen original/installed-Pascal caller state, no execution or new model requests."""
    archive = read_archive(output)
    frozen = json.loads(archive["freeze.json"])
    if frozen["contract"] != contract(root):
        raise ValueError("arithmetic original contract changed")
    for name, digest in frozen["method_hashes"].items():
        if (
            hashlib.sha256(archive["methods/" + pathlib.Path(name).name]).hexdigest()
            != digest
        ):
            raise ValueError("arithmetic method snapshot changed")
    result = json.loads(archive["result.json"])
    for suite in ("training", "terminal"):
        if suite not in result:
            if suite == "terminal" and result["training"]["status"] != "passed":
                continue
            raise ValueError("arithmetic caller suite missing")
        inputs = cases(suite)
        payload = b"".join(inputs)
        if hashlib.sha256(payload).hexdigest() != frozen["corpora"][suite]:
            raise ValueError("arithmetic frozen corpus differs")
        for prefix, native in (("original", True), ("host", False)):
            directory = f"{prefix}-{suite}"
            if archive[f"{directory}/CASES.BIN"] != payload:
                raise ValueError("arithmetic caller input differs")
            if (
                prefix == "host"
                and hashlib.sha256(archive[f"{directory}/candidate.inc"]).hexdigest()
                != frozen["method_hashes"]["targets/liero/src/FUN_249c_0013.inc"]
            ):
                raise ValueError("arithmetic installed candidate differs")
            checked = compare(
                inputs,
                archive[f"{directory}/" + ("TRACE.BIN" if native else "PASCAL.BIN")],
                native=native,
                return_offset=frozen["return_offset"],
                return_segment=result[f"{suite}_segments"]["code"]
                if native
                else 0x2000,
            )
            if (native and checked["status"] != "passed") or (
                not native and checked != result[suite]
            ):
                raise ValueError("arithmetic caller trace replay differs")
    return result


def main() -> None:
    """Oracle: explicit original caller integration, BYOD absence skips without source credit."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--cursor", action="store_true")
    args = parser.parse_args()
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        print(json.dumps({"status": "skipped", "reason": "BYOD unavailable"}))
        return
    if args.cursor:
        print(
            json.dumps(
                replay_cursor(ROOT, args.output.resolve())
                if args.replay
                else run_cursor(ROOT, args.output.resolve()),
                indent=2,
            )
        )
        return
    result = (
        replay(ROOT, args.output.resolve())
        if args.replay
        else run(ROOT, args.output.resolve())
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
