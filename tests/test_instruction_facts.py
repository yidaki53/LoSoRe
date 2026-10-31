import hashlib
import json
import pathlib
import shutil
import struct

import pytest

from engine.instruction_facts import initialization_prefix
from tools.liero_file_probe import assemble_probe, run_dosbox
from tools.liero_four_routine_pilot import prefix_transfer_report


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
    """Oracle: original bytes execute in DOSBox; predicted writes match the entire guarded window."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox")
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
    artifacts = {
        name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()
        for name in (
            "TRACE.BIN",
            "PROBE.COM",
            "original.bin",
            "harness.S",
            "harness.bin",
            "probe.conf",
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
                "artifact_hashes": artifacts,
                "limitations": "Finite original-only COM contexts; no Pascal, full ABI or source promotion.",
            },
            indent=2,
        )
    )
