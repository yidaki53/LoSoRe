import hashlib
import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.routine_contract import load_contract
from tools.liero_file_probe import assemble_probe, run_dosbox

RAW = bytes.fromhex(
    "c8020000837e06007d07c746feffffeb12837e06007e07c746fe0100eb05"
    "31c08946fe8b46fec9c20400"
)


def test_sign_caller_step_contract_and_remaining_callees(tmp_path):
    """Oracle: original caller bytes propagate signed steps only; unresolved callees block recovery."""
    root = pathlib.Path(__file__).resolve().parents[1]
    target = root / "targets/liero"
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    manifest_path = target / "alternate_streams.json"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads(manifest_path.read_text())
    )
    offset = header + (0x1EC2 - base) * 16 + 0x0895
    raw = binary[offset : offset + 296]
    assert raw[:54].hex() == (
        "c80e00008b46108946fe8b460e8946fc8b460c2b46108946f8"
        "8b460a2b460e8946f6ff76f855e8adff8946f4ff76f655e8a3ff8946f2"
    )
    relocations = _mz_relocation_locations(binary, header)
    assert not any(offset - 1 <= location < offset + 54 for location in relocations)
    for call_offset in (38, 48):
        assert raw[call_offset] == 0xE8
        assert (
            0x0895
            + call_offset
            + 3
            + int.from_bytes(
                raw[call_offset + 1 : call_offset + 3], "little", signed=True
            )
        ) & 65535 == 0x086B
    far_calls, drawing_calls = [], []
    for index in range(len(raw) - 4):
        if raw[index] == 0x9A and offset + index + 3 in relocations:
            target_offset, relative_segment = struct.unpack_from("<HH", raw, index + 1)
            assert (relative_segment + base, target_offset) == (0x24DD, 0x4654)
            far_calls.append(index)
        if raw[index : index + 2] == b"\x0e\xe8":
            destination = (
                0x0895
                + index
                + 4
                + int.from_bytes(raw[index + 2 : index + 4], "little", signed=True)
            ) & 65535
            assert destination == 0x0DC8
            drawing_calls.append(index + 1)
    assert far_calls == [150, 167, 255, 272]
    assert drawing_calls == [182, 287]
    for call_offset, bound in ((150, 5), (167, 2), (255, 5), (272, 2)):
        assert raw[call_offset - 2 : call_offset] == bytes((0x6A, bound))
    for call_offset in (167, 272):
        assert raw[call_offset - 8 : call_offset - 2] == b"\xff\x76\xfe\xff\x76\xfc"
        assert raw[call_offset + 5 : call_offset + 9] == b"\x05\x53\x00\x50"
        assert raw[call_offset + 9 : call_offset + 15] == b"\xc4\x7e\x06\x06\x57\x0e"
    for call_offset in (150, 255):
        assert raw[call_offset + 5 : call_offset + 9] == b"\x09\xc0\x75\x1a"
    ledger_path = target / "recovery.json"
    ledger = json.loads(ledger_path.read_text())["functions"]
    assert ledger["FUN_1ec2_086b"]["status"] == "source_recovered"
    assert ledger["FUN_24dd_4654"]["status"] != "source_recovered"
    assert ledger["FUN_1ec2_0dc8"]["status"] != "source_recovered"
    report = {
        "status": "blocked-on-other-callees",
        "caller": "FUN_1ec2_0895",
        "binary_sha256": identity,
        "file_offset": offset,
        "routine_bytes_hex": raw.hex(),
        "caller_sha256": hashlib.sha256(raw).hexdigest(),
        "resolved_dependency": "FUN_1ec2_086b",
        "propagated_constraint": {
            "x_step_bp_minus_12": "sign16(wrap16(frame_word_12 - frame_word_16))",
            "y_step_bp_minus_14": "sign16(wrap16(frame_word_10 - frame_word_14))",
            "range": [65535, 0, 1],
            "ignored_argument": "PUSH BP is the unread first argument, not an output pointer.",
            "premises": "Valid writable nonaliasing caller frame/stack/code and entry at original first instruction.",
        },
        "remaining_dependencies": ["FUN_24dd_4654", "FUN_1ec2_0dc8"],
        "conditional_random_constraint": {
            "premises": "46b1 state contract requires proven writable nonaliasing DS6412..6415 and original CS constant8405h; actual caller provenance still unknown.",
            "bound5_return": "0..4; only zero takes draw path",
            "conditional_bound2_return": "0..1; adding53h yields low color byte83 or84",
            "state_effect": "advance08088405h LCG once for each executed random call",
            "draw_arguments": "PUSH column(BP-2), row(BP-4), color83/84, segment, offset; caller allocation/offset premises remain unknown",
        },
        "blockers": [
            "Random state/return projection is scoped; actual caller DS seed window and drawing buffer/offset provenance remain unproved.",
            "Wrapping coordinate arithmetic, signed absolute -32768 path and loop termination require separate caller review.",
            "This prefix is not a recovered caller, observed caller execution or normal-program reachability.",
        ],
        "next_dependency": "Resolve028a->0353 allocation and parent5e66 DS/pointer continuity; then revisit0895 seed, buffer and loop obligations",
        "ledger_sha256_at_assessment": hashlib.sha256(
            ledger_path.read_bytes()
        ).hexdigest(),
    }
    (tmp_path / "result.json").write_text(json.dumps(report, indent=2) + "\n")


def test_original_caller_inputs_bind_conditional_buffer_bounds(tmp_path):
    """Oracle: original slices/MZ relocations and exhaustive offset arithmetic, not execution."""
    root = pathlib.Path(__file__).resolve().parents[1]
    target = root / "targets/liero"
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    manifest_path = target / "alternate_streams.json"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads(manifest_path.read_text())
    )
    contract = load_contract(target, "FUN_1ec2_0895")
    assert contract["binary_sha256"] == identity
    assert contract["oracle"] == "static-original-callsite-constraints"
    assert contract["scope"] == "conditional-input-and-callee-facts-not-caller-recovery"
    assert contract["callee_contracts"] == ["FUN_24dd_4654", "FUN_1ec2_0dc8"]
    relocations = _mz_relocation_locations(binary, header)
    for slice_, address, size, target_address in zip(
        contract["reviewed_slices"],
        (0x7E3C, 0x8411, 0xE50B),
        (70, 74, 15),
        ((0x0895, 0x0EC2), (0x0895, 0x0EC2), (0x028A, 0x14DD)),
        strict=True,
    ):
        offset = header + address
        raw = binary[offset : offset + size]
        assert slice_["file_offset"] == offset
        assert slice_["entry"] == f"1000:{address:04x}"
        assert bytes.fromhex(slice_["bytes_hex"]) == raw
        assert {
            r - offset for r in relocations if offset - 1 <= r < offset + size
        } == set(slice_["relocation_offsets"])
        call = slice_["far_call_offset"]
        assert raw[call] == 0x9A
        assert struct.unpack_from("<HH", raw, call + 1) == target_address
        assert slice_["relocation_offsets"] == [call + 3]
        if address == 0xE50B:
            assert raw[:3] == b"\x68\x00\xfa"
            assert slice_["requested_size_word"] == int.from_bytes(raw[1:3], "little")
            assert raw[8:] == b"\xa3\x84\x66\x89\x16\x86\x66"
            continue
        assert raw[:7] == b"\xc4\xbe\xc8\xfe\x26\x8b\x05"
        assert raw[7:11] == (
            b"\x2b\x06\xb0\x67" if address == 0x7E3C else b"\x2b\x06\xb2\x67"
        )
        assert raw[20:24] == b"\x26\x8b\x45\x02"
        assert raw[24:28] == (
            b"\x2b\x06\xb4\x67" if address == 0x7E3C else b"\x2b\x06\xb6\x67"
        )
        assert raw[37:59].hex() == "ffb6d0feffb6ccfe8b46fa050700508b46f805040050"
        assert raw[59:63] == b"\xc4\x3e\x84\x66"
        assert raw[call - 2 : call] == b"\x06\x57"
        adjustment = 0 if address == 0x7E3C else 160
        assert slice_["destination_offset_adjustment"] == adjustment
        if adjustment:
            assert raw[63:67] == b"\x81\xc7\xa0\x00"

    wrapper_offset = header + (0x24DD - base) * 16 + 0x028A
    wrapper = binary[wrapper_offset : wrapper_offset + 21]
    assert wrapper.hex() == "558bec8b4606e8c0005d7203ca0200b8cb00e970fe"
    assert not any(
        wrapper_offset - 1 <= r < wrapper_offset + len(wrapper) for r in relocations
    )
    assert wrapper[6] == 0xE8
    assert 0x028A + 9 + int.from_bytes(wrapper[7:9], "little", signed=True) == 0x0353
    bounds = contract["conditional_bounds"]
    displacement = 157 * 320 + 157
    assert bounds["maximum_draw_displacement"] == displacement == 50397
    assert bounds["maximum_view_offset"] == 65535 - displacement
    assert bounds["maximum_displacement_both_views"] == displacement + 160
    assert bounds["required_writable_bytes_from_base"] == displacement + 161
    accepted_offsets = [
        offset
        for offset in range(65536)
        if offset + 160 <= 65535
        and offset + displacement <= 65535
        and ((offset + 160) & 65535) + displacement <= 65535
    ]
    assert accepted_offsets == list(range(14979))
    assert bounds["maximum_base_offset_both_views"] == max(accepted_offsets)
    assert bounds["required_writable_bytes_from_base"] <= 64000
    assert 15000 + displacement <= 65535
    assert 15000 + 160 + displacement == 65557
    assert (15000 + 160 + displacement) & 65535 == 21
    ledger_path = target / "recovery.json"
    ledger = json.loads(ledger_path.read_text())["functions"]
    assert all(
        ledger[name]["status"] == "unreviewed"
        for name in (
            "FUN_1000_5e66",
            "FUN_1ec2_0895",
            "FUN_24dd_028a",
            "FUN_24dd_0353",
        )
    )
    report = {
        "status": "blocked-on-producer-contracts",
        "oracle": "static-original-callsite-constraints",
        "contract": contract,
        "binary_sha256": identity,
        "logical_load_segment": base,
        "unresolved_allocation_wrapper": {
            "entry": "24dd:028a",
            "bytes_hex": wrapper.hex(),
            "near_callee": "FUN_24dd_0353",
            "file_offset": wrapper_offset,
        },
        "normal_program_ds": "unknown; local slice DS is not assumed to be source DS",
        "premises": "Valid disjoint SS frame/stack/code and input cells; aliasing stores or changed SS/SP invalidate argument bindings.",
        "supported_base_offsets_if_all_premises_hold": len(accepted_offsets),
        "excluded_offset_arithmetic": {
            "base": 15000,
            "left_final_offset": 65397,
            "right_linear_offset": 65557,
            "right_wrapped_offset": 21,
        },
        "blockers": [
            "Allocator028a near-calls0353; neither has a checked allocation/DS/ABI contract.",
            "Parent5e66 is unresolved; DS continuity and pointer lifetime/aliasing are unknown.",
            "Caller seed initialization, buffer allocation and actual offset remain unknown.",
            "Caller wrapped arithmetic/loop and full host ABI remain unreviewed.",
        ],
        "execution_cases": 0,
        "source_promoted": False,
        "model_requests": 0,
        "evidence_hashes": {
            str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (
                manifest_path,
                ledger_path,
                target / "config/routine_contracts.json",
                target / "asm/FUN_1000_5e66.s",
                target / "asm/entry.s",
                target / "asm/FUN_24dd_028a.s",
                target / "asm/FUN_24dd_0353.s",
                pathlib.Path(__file__),
            )
        },
    }
    (tmp_path / "result.json").write_text(json.dumps(report, indent=2) + "\n")


@pytest.mark.parametrize("entry", [0x086B, 0x09BD], ids=["086b", "09bd"])
def test_actual_signed_word_leaf_all_inputs(tmp_path, entry):
    """Oracle: complete original-byte/static branch review plus exhaustive actual-source returns.

    BP/SP/DF/DS/SS observations remain original-only, not host ABI equivalence.
    Historical manual source is explicitly used; no model/generalization claim.
    """
    root = pathlib.Path(__file__).resolve().parents[1]
    target = root / "targets/liero"
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD/probe tools unavailable")
    manifest_path = target / "alternate_streams.json"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads(manifest_path.read_text())
    )
    assert header == int.from_bytes(binary[8:10], "little") * 16
    routine = f"FUN_1ec2_{entry:04x}"
    offset = header + (0x1EC2 - base) * 16 + entry
    assert binary[offset : offset + 42] == RAW
    assert not any(
        offset - 1 <= location < offset + 42
        for location in _mz_relocation_locations(binary, header)
    )
    # Each relative branch lands on the start of a checked instruction.
    assert {
        position: position + 2 + RAW[position + 1] for position in (8, 15, 21, 28)
    } == {
        8: 17,
        15: 35,
        21: 30,
        28: 35,
    }
    source_files = (
        target / "src" / f"{routine}.inc",
        target / "src/LieroRuntime.pas",
        root / "tools/liero_file_probe.py",
        root / "engine/alternate_streams.py",
        pathlib.Path(__file__),
        manifest_path,
    )
    fingerprints = {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in source_files
    }
    freeze = {
        "function": routine,
        "binary_sha256": identity,
        "file_offset": offset,
        "routine_bytes_hex": RAW.hex(),
        "source_hashes": fingerprints,
        "cases": "All 65536 signed-word bit patterns in ascending unsigned order.",
        "ignored_argument": "input bits XOR AAAAh; static body never reads BP+4.",
        "direction_flag": "alternates by input bit0; no direction-changing opcode in original leaf.",
        "budget": "one original execution, one actual-source compilation/execution; subprocess limits30s; no model/holdout/retry",
        "preconditions": "Valid nonaliasing SS stack/frame/arguments and unmodified code; no asynchronous mutation.",
        "limitations": "Exhaustive return-value domain, not exhaustive machine states or normal-program reachability. Host ABI/flags are not compared.",
    }
    (tmp_path / "freeze.json").write_text(json.dumps(freeze, indent=2) + "\n")
    (tmp_path / "sources").mkdir()
    for path in source_files:
        shutil.copy2(path, tmp_path / "sources" / path.name)
    (tmp_path / "original.bin").write_bytes(RAW)
    assembly = tmp_path / "harness.S"
    assembly.write_text(f"""
.code16
.global _start
_start:
    push %cs
    pop %ds
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, handle
next_case:
    mov $0x1234, %bp
    mov %sp, before_sp
    mov counter, %ax
    push %ax
    xor $0xaaaa, %ax
    push %ax
    cld
    testw $1, counter
    jz invoke
    std
invoke:
    call original
    pushf
    pop %dx
    mov used, %di
    mov %ax, buffer(%di)
    mov %bp, buffer+2(%di)
    mov before_sp, %ax
    mov %ax, buffer+4(%di)
    mov %sp, buffer+6(%di)
    and $0x400, %dx
    mov %dx, buffer+8(%di)
    mov %ds, buffer+10(%di)
    mov %ss, buffer+12(%di)
    mov counter, %ax
    xor $0xaaaa, %ax
    mov %ax, buffer+14(%di)
    add $16, %di
    mov %di, used
    cmp $4096, %di
    jne advance
    cld
    mov handle, %bx
    mov $buffer, %dx
    mov $4096, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $4096, %ax
    jne failed
    movw $0, used
advance:
    incw counter
    jnz next_case
    mov handle, %bx
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    cld
    mov $0x4c01, %ax
    int $0x21
original:
.incbin "{tmp_path / "original.bin"}"
filename: .asciz "TRACE.BIN"
handle: .word 0
counter: .word 0
used: .word 0
before_sp: .word 0
buffer: .space 4096
""")
    (tmp_path / "PROBE.COM").write_bytes(assemble_probe(assembly, tmp_path))
    run_dosbox(tmp_path)
    program = tmp_path / "actual_sign.pas"
    program.write_text(
        """program ActualSign;
uses LieroRuntime;
{$I FUN_1ec2_086b.inc}
var bits: LongInt; signedValue: Integer; resultWord: Word;
    outputFile: file; written: LongInt;
begin
  if SizeOf(Integer) <> 2 then Halt(1);
  Assign(outputFile, 'PASCAL.BIN'); Rewrite(outputFile, 1);
  for bits := 0 to 65535 do
  begin
    if bits < 32768 then signedValue := bits else signedValue := bits - 65536;
    resultWord := FUN_1ec2_086b(Word(bits) xor $AAAA, signedValue);
    BlockWrite(outputFile, resultWord, 2, written);
    if written <> 2 then Halt(1);
  end;
  Close(outputFile);
end.
""".replace("FUN_1ec2_086b", routine)
    )
    compiled = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fusources", "-Fisources", "-FU.", "actual_sign.pas"],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (tmp_path / "fpc.log").write_bytes(compiled.stdout + compiled.stderr)
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    executed = subprocess.run(
        [str(tmp_path / "actual_sign")],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (tmp_path / "runtime.log").write_bytes(executed.stdout + executed.stderr)
    assert executed.returncode == 0, executed.stdout + executed.stderr
    trace = (tmp_path / "TRACE.BIN").read_bytes()
    pascal = (tmp_path / "PASCAL.BIN").read_bytes()
    assert len(trace) == 65536 * 16
    assert len(pascal) == 65536 * 2
    segment = struct.unpack_from("<H", trace, 10)[0]
    for bits in range(65536):
        ax, bp, before, after, df, ds, ss, ignored = struct.unpack_from(
            "<8H", trace, bits * 16
        )
        expected = 0xFFFF if bits >= 32768 else int(bits > 0)
        assert ax == expected == struct.unpack_from("<H", pascal, bits * 2)[0], bits
        assert bp == 0x1234 and before == after == 0xFFFE, bits
        assert df == (bits & 1) * 0x400, bits
        assert ds == ss == segment, bits
        assert ignored == bits ^ 0xAAAA, bits
    for relative, expected_hash in fingerprints.items():
        assert (
            hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected_hash
        )
    result = {
        "status": "exhaustive-signed-word-return-pass",
        "cases": 65536,
        "actual_target_source": True,
        "source_hashes": fingerprints,
        "original_only": "BP/SP/DF/DS/SS checked; not host ABI equivalence.",
        "static_review": "All42 original bytes/three signed return paths covered; BP+4 unused; only valid frame writes, no globals/calls.",
        "limitations": freeze["limitations"],
        "artifact_hashes": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in tmp_path.iterdir()
            if path.is_file()
        },
    }
    (tmp_path / "result.json").write_text(json.dumps(result, indent=2) + "\n")
