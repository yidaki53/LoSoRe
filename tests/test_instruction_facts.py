import hashlib
import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from engine.instruction_facts import (
    bounded_byte_fill_contract,
    bounded_shortstring_contract,
    initialization_prefix,
)
from tools.liero_file_probe import assemble_probe, run_dosbox
from tools.liero_four_routine_pilot import (
    leaf_cases,
    leaf_control_source,
    prefix_transfer_report,
    run_leaf_probe,
    run_prefix_transfer,
    validate_partial_memory_source,
    write_partial_memory_source,
)

SHORTSTRING_BYTES = bytes.fromhex(
    "33d28bdc1e36c47f0836c57704fc33c0abb8b0d7ab33c0b91600f3ab"
    "b94f000bd27509ac3ac876048ac8e308ac0ac07403aae2f832c0aa1fca0800"
)


@pytest.mark.parametrize(
    "source_slot, word_count, constant, limit",
    [(4, 22, 0xD7B0, 79), (4, 0, 0x1234, 1), (4, 3, 0xFEFF, 255)],
)
def test_shortstring_contract_derives_parameters_not_routine_name(
    source_slot, word_count, constant, limit
):
    """Oracle: varied stack bindings, initialization words and unsigned string bounds."""
    raw = bytearray(SHORTSTRING_BYTES)
    raw[8], raw[12] = source_slot + 4, source_slot
    raw[18:20] = constant.to_bytes(2, "little")
    raw[24:26] = word_count.to_bytes(2, "little")
    raw[29:31] = limit.to_bytes(2, "little")
    raw[57:59] = (source_slot + 4).to_bytes(2, "little")
    contract = bounded_shortstring_contract(bytes(raw))
    assert contract["source_far_pointer_slot"] == source_slot
    assert contract["text_destination_offset"] == 4 + 2 * word_count
    assert contract["maximum_text_bytes"] == limit
    assert contract["prefix_writes"][1]["value"]["amount"] == constant
    assert contract["unreachable_branch"]["offset"] == 33
    assert contract["far_return_cleanup_bytes"] == source_slot + 4
    assert contract["limitations"].startswith("Scoped memory contract")


@pytest.mark.parametrize(
    "offset", [i for i in range(59) if i not in {8, 12, 18, 19, 24, 25, 29, 30, 57, 58}]
)
def test_shortstring_contract_rejects_every_opcode_branch_and_mode_mutation(offset):
    """Oracle: branch destinations, unsigned comparison, entry DX and DS restoration are exact."""
    raw = bytearray(SHORTSTRING_BYTES)
    raw[offset] ^= 1
    with pytest.raises(ValueError, match="shape"):
        bounded_shortstring_contract(bytes(raw))


@pytest.mark.parametrize(
    "offset, value", [(8, 10), (12, 3), (29, 0), (30, 1), (25, 255), (57, 0)]
)
def test_shortstring_contract_rejects_invalid_bounds_and_argument_layout(offset, value):
    """Oracle: do not widen CL limits, wrap destination writes or alias argument cells."""
    raw = bytearray(SHORTSTRING_BYTES)
    raw[offset] = value
    with pytest.raises(ValueError, match="bounds"):
        bounded_shortstring_contract(bytes(raw))


def test_shortstring_composition_predicts_original_dirty_memory_and_nul_training(
    tmp_path, monkeypatch
):
    """Oracle: actual complete original bytes; manual Pascal is only a disclosed control."""
    from tools import liero_four_routine_pilot as pilot

    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("BYOD or original leaf tools unavailable")
    routine = "FUN_24dd_3b22"
    report = prefix_transfer_report(root, routine)
    raw = bytes.fromhex(report["routine_bytes_hex"])
    assert raw == SHORTSTRING_BYTES
    contract = bounded_shortstring_contract(raw)
    cases = leaf_cases(routine, "training")
    for seed in (0, 255):
        for length in (0, 1, 78, 79, 80, 255):
            for position in (0, 1, 77, 78, 79, 254):
                data = bytearray([seed] * 544)
                data[:256] = bytes([length]) + b"A" * 255
                data[position + 1] = 0
                cases.append((f"train-nul-{seed}-{length}-{position}", bytes(data)))
    monkeypatch.setattr(pilot, "leaf_cases", lambda fn, suite: cases)
    output = tmp_path / "composition"
    result = run_leaf_probe(
        root, output, routine, leaf_control_source(routine), "training"
    )
    assert result["status"] == "passed"
    trace = (output / "TRACE.BIN").read_bytes()
    for index, (_, data) in enumerate(cases):
        expected = bytearray(data)
        for write in contract["prefix_writes"]:
            begin = 272 + write["byte_offset"]
            value = write["value"]["amount"].to_bytes(2, "little")
            expected[begin : begin + 2 * write["word_count"]] = (
                value * write["word_count"]
            )
        length = min(
            data[contract["source_length_offset"]], contract["maximum_text_bytes"]
        )
        text = data[
            contract["source_text_offset"] : contract["source_text_offset"] + length
        ]
        text = text.split(b"\0", 1)[0]
        begin = 272 + contract["text_destination_offset"]
        expected[begin : begin + len(text) + 1] = text + b"\0"
        assert trace[index * 556 + 12 : (index + 1) * 556] == expected
    assert len(cases) == 584


@pytest.mark.parametrize("slots,cleanup", [((8, 6, 4), 8), ((12, 10, 8), 12)])
def test_byte_fill_contract_derives_argument_slots_without_routine_identity(
    slots, cleanup
):
    """Oracle: varied exact stack operands, unsigned byte-repeat memory shape only."""
    destination, count, value = slots
    raw = (
        bytes.fromhex("8bdc36c47f")
        + bytes([destination])
        + bytes.fromhex("368b4f")
        + bytes([count])
        + bytes.fromhex("368a47")
        + bytes([value])
        + bytes.fromhex("fcf3aaca")
        + cleanup.to_bytes(2, "little")
    )
    contract = bounded_byte_fill_contract(raw)
    assert contract["destination_far_pointer_slot"] == destination
    assert contract["count_word_slot"] == count
    assert contract["value_low_byte_slot"] == value
    assert contract["far_return_cleanup_bytes"] == cleanup


@pytest.mark.parametrize(
    "index,value",
    [(0, 0x90), (14, 0xFD), (16, 0xAB), (17, 0xC3), (5, 7), (9, 4), (18, 0)],
)
def test_byte_fill_contract_rejects_opcode_direction_layout_and_return_mutants(
    index, value
):
    """Oracle: no permissive byte-fill or blanket RET acceptance after a shape change."""
    raw = bytearray.fromhex("8bdc36c47f08368b4f06368a4704fcf3aaca0800")
    raw[index] = value
    with pytest.raises(ValueError):
        bounded_byte_fill_contract(bytes(raw))


@pytest.mark.parametrize(("start", "end"), [(0, 8), (0x6426, 0x7B52), (0xFFF0, 0xFFFE)])
def test_global_word_clear_derives_range_and_segment(start, end):
    """Oracle: varied raw immediates determine the range without a routine identifier."""
    raw = (
        b"\xbf"
        + start.to_bytes(2, "little")
        + b"\x1e\x07\xb9"
        + end.to_bytes(2, "little")
        + bytes.fromhex("2bcfd1e933c0fcf3abc3")
    )
    facts = initialization_prefix(raw, data_window=(0, 65536))
    assert facts["residue"]["offset"] == len(raw) - 1
    assert facts["residue"]["bytes_hex"] == "c3"
    write = facts["writes"][0]
    assert write["address_space"] == "entry_ds"
    assert write["byte_offset"] == start
    assert write["word_count"] == (end - start) // 2
    assert write["value"]["amount"] == 0
    assert write["segment"]["kind"] == "entry_ds"
    assert facts["registers"]["cx"]["amount"] == 0
    assert facts["registers"]["di"]["amount"] == end
    assert {0, 3, 4, 5, 8, 10, 12, 14, 15} <= set(write["support"])


def test_global_writes_require_explicit_matching_window():
    """Oracle: known segment provenance alone does not establish valid writable memory."""
    raw = bytes.fromhex("bf10001e07b9020033c0fcf3ab")
    for window in (None, (17, 32), (0, 19)):
        facts = initialization_prefix(raw, data_window=window)
        assert facts["writes"] == []
        assert facts["residue"]["bytes_hex"] == "f3ab"
    assert (
        initialization_prefix(raw, data_window=(16, 20))["writes"][0]["word_count"] == 2
    )
    unknown_es = raw.replace(bytes.fromhex("1e07"), bytes.fromhex("0607"))
    assert initialization_prefix(unknown_es, data_window=(0, 65536))["writes"] == []


@pytest.mark.parametrize(
    "raw",
    [
        "07bf1000b9020033c0fcf3ab",
        "bf10001e07b9ffff33c0fcf3ab",
        "bf10001e07b9020033c0fdf3ab",
        "bf10001e07b902002bc533c0fcf3ab",
    ],
)
def test_global_unknown_stack_direction_or_operands_stop_before_writes(raw):
    """Oracle: unknown POP, operands and overflowing stores never become write facts."""
    facts = initialization_prefix(bytes.fromhex(raw), data_window=(0, 65536))
    assert not facts["writes"]
    assert facts["residue"] is not None


@pytest.mark.parametrize(
    "window", [(0, 65537), (-1, 32), (32, 32), (True, 32), [0, 32]]
)
def test_data_window_validation(window):
    """Oracle: invalid memory preconditions are explicit errors."""
    with pytest.raises(ValueError, match="window"):
        initialization_prefix(b"\xfc", data_window=window)


def test_subtraction_wrap_and_shift_are_unsigned_word_operations():
    """Oracle: SUB wraps first, then SHR halves; no signed-range shortcut."""
    facts = initialization_prefix(bytes.fromhex("b90100bf03002bcfd1e9"))
    assert facts["registers"]["cx"]["amount"] == 32767
    assert facts["residue"] is None


def test_source_segment_load_does_not_reuse_entry_ds_write_permission():
    """Oracle: LDS changes segment provenance; writable entry DS is not permission for source DS."""
    raw = bytes.fromhex("8bdc36c577041e07bf1000b9020033c0fcf3ab")
    facts = initialization_prefix(raw, data_window=(0, 65536))
    assert facts["writes"] == []
    assert facts["residue"]["bytes_hex"] == "f3ab"


@pytest.mark.parametrize("raw", ["8bdc1e8be307", "8bdc1e178be336c57704"])
def test_stack_pointer_or_segment_changes_invalidate_saved_stack_bindings(raw):
    """Oracle: resetting SP cannot recover a popped stack value or an entry-SS pointer."""
    facts = initialization_prefix(bytes.fromhex(raw), data_window=(0, 65536))
    assert facts["residue"] is not None
    assert not facts["writes"]


def test_object_store_can_invalidate_a_pending_segment_pop():
    """Oracle: object bounds do not establish disjointness from stack memory."""
    raw = bytes.fromhex("8bdc1e36c47f0833c0fcab07")
    facts = initialization_prefix(raw)
    assert len(facts["writes"]) == 1
    assert facts["residue"]["bytes_hex"] == "07"


def test_odd_range_and_segment_end_are_not_rounded_into_extra_writes():
    """Oracle: SHR truncates odd byte spans; DI wraps after the final nonwrapping word."""
    odd = initialization_prefix(
        bytes.fromhex("bf10001e07b915002bcfd1e933c0fcf3ab"),
        data_window=(16, 21),
    )
    assert odd["writes"][0]["word_count"] == 2
    assert odd["registers"]["di"]["amount"] == 20
    boundary = initialization_prefix(
        bytes.fromhex("bffeff1e07b9010033c0fcf3ab"),
        data_window=(65534, 65536),
    )
    assert boundary["writes"][0]["word_count"] == 1
    assert boundary["registers"]["di"]["amount"] == 0


@pytest.mark.parametrize("seed", [0xA5, 0x5A, 0xFF])
def test_original_global_clear_matches_derived_range_with_guards(tmp_path, seed):
    """Oracle: original DOSBox memory equals generated Pascal; SP observations are original-only."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD or DOS probe tools unavailable")
    report = prefix_transfer_report(
        root,
        "FUN_24dd_492c",
        data_window=(0x6000, 0x8000),
    )
    original = tmp_path / "original.bin"
    original.write_bytes(bytes.fromhex(report["routine_bytes_hex"]))
    assembly = tmp_path / "harness.S"
    assembly.write_text(f"""
.code16
.global _start
_start:
    push %cs
    pop %ds
    push %cs
    pop %es
    cld
    mov $0x6000, %di
    mov $0x2000, %cx
    mov ${seed}, %al
    rep stosb
    mov %sp, stack_before
    call original_routine
    mov %sp, stack_after
    mov $filename, %dx
    xor %cx, %cx
    mov $0x3c00, %ax
    int $0x21
    jc failed
    mov %ax, %bx
    mov $0x6000, %dx
    mov $0x2000, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $0x2000, %ax
    jne failed
    mov $stack_before, %dx
    mov $4, %cx
    mov $0x4000, %ax
    int $0x21
    jc failed
    cmp $4, %ax
    jne failed
    mov $0x3e00, %ax
    int $0x21
    jc failed
    mov $0x4c00, %ax
    int $0x21
failed:
    mov $0x4c01, %ax
    int $0x21
filename: .asciz "TRACE.BIN"
stack_before: .word 0
stack_after: .word 0
.org 0x492c - 0x100
original_routine:
.incbin "{original}"
""")
    (tmp_path / "PROBE.COM").write_bytes(assemble_probe(assembly, tmp_path))
    run_dosbox(tmp_path)
    trace = (tmp_path / "TRACE.BIN").read_bytes()
    assert len(trace) == 8196
    expected = bytearray([seed] * 8192)
    for write in report["prefix"]["writes"]:
        assert write["address_space"] == "entry_ds"
        start = write["byte_offset"] - 0x6000
        expected[start : start + write["word_count"] * 2] = (
            write["value"]["amount"].to_bytes(2, "little") * write["word_count"]
        )
    assert trace[:8192] == expected
    before, after = struct.unpack("<HH", trace[8192:])
    assert before == after
    partial_dir = tmp_path / "partial"
    run_prefix_transfer(
        root, partial_dir, "FUN_24dd_492c", data_window=(0x6000, 0x8000)
    )
    partial = write_partial_memory_source(root, partial_dir)
    program = tmp_path / "memory_projection.pas"
    program.write_text(f"""
program MemoryProjection;
{{$I partial-memory.inc}}
var data: TEntryData; outputFile: file; written: LongInt;
begin
  FillChar(data, SizeOf(data), {seed});
  ApplyPartialMemoryEffects(data);
  Assign(outputFile, 'PASCAL.BIN');
  Rewrite(outputFile, 1);
  BlockWrite(outputFile, data[$6000], $2000, written);
  Close(outputFile);
  if written <> $2000 then Halt(1);
end.
""")
    compiled = subprocess.run(
        ["fpc", "-Mtp", "-Cr", f"-Fi{partial_dir}", str(program)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    subprocess.run([str(tmp_path / "memory_projection")], cwd=tmp_path, check=True)
    assert (tmp_path / "PASCAL.BIN").read_bytes() == trace[:8192]
    assert validate_partial_memory_source(root, partial_dir) == partial
    assert partial["whole_routine_execution"] == "blocked"
    artifacts = {
        name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()
        for name in (
            "TRACE.BIN",
            "PROBE.COM",
            "original.bin",
            "harness.S",
            "harness.bin",
            "probe.conf",
            "PASCAL.BIN",
            "memory_projection.pas",
            "memory_projection",
        )
    }
    (tmp_path / "measurement.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "seed": seed,
                "window": [0x6000, 0x8000],
                "bytes_checked": 8192,
                "stack_before": before,
                "stack_after": after,
                "static_report": report,
                "partial_memory_report": partial,
                "artifact_hashes": artifacts,
                "limitations": "Finite COM vs host Pascal memory projection; no full ABI, original-program reachability or source promotion.",
            },
            indent=2,
        )
    )
