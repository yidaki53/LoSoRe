import hashlib
import json
import pathlib
import struct

import pytest

from engine.routine_contract import load_contract
from tools import liero_startup_clear_contract as contracts
from tools.liero_startup_clear_contract import (
    startup_clear_contract,
    write_startup_clear_contract,
)

CPU_BYTES = bytes.fromhex(
    "33c09c5b80e70f539d9c5980e5f080fdf0740e4080cff0539d9c5980e5f0740140a22064c3"
)


@pytest.fixture
def cpu_binary():
    """Oracle: read-only actual BYOD, not exported decompiler classification."""
    root = pathlib.Path(__file__).resolve().parents[1]
    path = root / "extracted/liero/LIERO.EXE"
    if not path.is_file():
        pytest.skip("Liero BYOD unavailable")
    return path.read_bytes()


def test_cpu_all_control_paths_balance_stack_without_assuming_cpu_class(
    cpu_binary, tmp_path
):
    """Oracle: complete original bytes and three independently reviewed path shapes."""
    report = contracts.startup_cpu_contract(cpu_binary, load_segment=0x1000)
    cpu = report["cpu"]
    assert cpu["file_offset"] == 91633
    assert cpu["reviewed_bytes_hex"] == CPU_BYTES.hex()
    assert cpu["near_return_ip"] == 0x11
    assert cpu["store_ds_offset"] == 0x6420
    assert cpu["entry_sp"] == 0xFFEA
    assert cpu["lowest_sp"] == 0xFFE8
    assert cpu["return_sp"] == 0xFFEC
    assert cpu["preserved"] == ["DX", "SI", "DI", "BP", "DS", "ES", "SS"]
    assert cpu["stack_write_module_range"] == [201304, 201306]
    assert cpu["store_module_range"] == [129840, 129841]
    assert cpu["source_recovered"] is False
    assert cpu["original_execution_cases"] == 0
    # This table covers every instruction and both branch edges, not a CPU emulator.
    instructions = (
        (0xB1, "33c0", 0),
        (0xB3, "9c", -2),
        (0xB4, "5b", 2),
        (0xB5, "80e70f", 0),
        (0xB8, "53", -2),
        (0xB9, "9d", 2),
        (0xBA, "9c", -2),
        (0xBB, "59", 2),
        (0xBC, "80e5f0", 0),
        (0xBF, "80fdf0", 0),
        (0xC2, "740e", 0),
        (0xC4, "40", 0),
        (0xC5, "80cff0", 0),
        (0xC8, "53", -2),
        (0xC9, "9d", 2),
        (0xCA, "9c", -2),
        (0xCB, "59", 2),
        (0xCC, "80e5f0", 0),
        (0xCF, "7401", 0),
        (0xD1, "40", 0),
        (0xD2, "a22064", 0),
        (0xD5, "c3", 2),
    )
    assert b"".join(bytes.fromhex(raw) for _, raw, _ in instructions) == CPU_BYTES
    for pc, displacement in ((0xC2, 0x0E), (0xCF, 1)):
        assert pc + 2 + displacement == 0xD2
    expected_paths = [
        [pc for pc, _, _ in instructions if pc <= 0xC2 or pc >= 0xD2],
        [pc for pc, _, _ in instructions if pc != 0xD1],
        [pc for pc, _, _ in instructions],
    ]
    assert [p["instruction_offsets"] for p in cpu["paths"]] == expected_paths
    deltas = {pc: delta for pc, _, delta in instructions}
    for classification, path in enumerate(expected_paths):
        sp = 0xFFEA
        low = sp
        for pc in path:
            sp += deltas[pc]
            low = min(low, sp)
        assert (sp, low) == (0xFFEC, 0xFFE8)
        assert sum(pc in (0xC4, 0xD1) for pc in path) == classification
        assert cpu["paths"][classification]["stored_al"] == classification
    assert "TF=0" in " ".join(cpu["assumptions"])
    assert "TF=0" in " ".join(report["assumptions"])
    assert "not CPU-family identification" in " ".join(cpu["limitations"])
    assert "not Pascal parity" in " ".join(cpu["limitations"])
    assert report["clear"]["ds_range"] == [0x6426, 0x7B52]
    root = pathlib.Path(__file__).resolve().parents[1]
    contract = load_contract(root / "targets/liero", "FUN_24dd_00b1")
    assert contract["reviewed_bytes_hex"] == cpu["reviewed_bytes_hex"]
    assert contract["file_offset"] == cpu["file_offset"]
    assert contract["binary_sha256"] == report["binary_sha256"]
    assert contract["return_projection"]["preserved"] == cpu["preserved"]
    assert contract["return_projection"]["stored_al_by_path"] == [0, 1, 2]
    assert contract["return_projection"]["store_ds_offset"] == cpu["store_ds_offset"]
    paths = (
        root / "tools/liero_startup_clear_contract.py",
        pathlib.Path(__file__),
        root / "engine/alternate_streams.py",
        root / "engine/instruction_facts.py",
        root / "targets/liero/config/routine_contracts.json",
        root / "targets/liero/src/FUN_24dd_00b1.inc",
        root / "targets/liero/asm/FUN_24dd_00b1.s",
        root / "targets/liero/recovery.json",
    )
    report["evidence_hashes"] = {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
    }
    for path in paths:
        destination = tmp_path / "sources" / path.relative_to(root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(path.read_bytes())
    (tmp_path / "cpu.bin").write_bytes(CPU_BYTES)
    (tmp_path / "result.json").write_text(json.dumps(report, indent=2) + "\n")


@pytest.mark.parametrize("offset", range(37))
def test_cpu_contract_rejects_every_instruction_byte_mutant(cpu_binary, offset):
    """Oracle: changing even a skipped branch/store byte invalidates this exact review."""
    binary = bytearray(cpu_binary)
    binary[91633 + offset] ^= 1
    with pytest.raises(ValueError, match="CPU leaf"):
        contracts.startup_cpu_contract(bytes(binary), load_segment=0x1000)


def test_cpu_contract_rejects_call_target_and_relocated_leaf(cpu_binary):
    """Oracle: unmodified listing text cannot hide changed call/loader semantics."""
    binary = bytearray(cpu_binary)
    binary[91456 + 0xF] ^= 1
    with pytest.raises(ValueError, match="CPU call"):
        contracts.startup_cpu_contract(bytes(binary), load_segment=0x1000)
    binary = bytearray(cpu_binary)
    table = struct.unpack_from("<H", binary, 24)[0]
    count = struct.unpack_from("<H", binary, 6)[0]
    locations = []
    for index in range(count):
        offset, segment = struct.unpack_from("<HH", binary, table + index * 4)
        locations.append((segment * 16 + offset, index))
    # Replace an unrelated relocation rather than duplicating a required one.
    _, index = next((loc, i) for loc, i in locations if loc > 100000)
    struct.pack_into("<HH", binary, table + index * 4, 0xB5, 0x14DD)
    with pytest.raises(ValueError, match="relocated CPU"):
        contracts.startup_cpu_contract(bytes(binary), load_segment=0x1000)


def test_cpu_store_must_not_alias_live_return_stack(cpu_binary):
    """Oracle: a segment-preserving store can still invalidate a near-return premise."""
    binary = bytearray(cpu_binary)
    # Shift the loader stack so DS:6420 aliases the call's stacked return IP.
    struct.pack_into("<HH", binary, 14, 0x1962, 0x6516)
    with pytest.raises(ValueError, match="CPU store aliases"):
        contracts.startup_cpu_contract(bytes(binary), load_segment=0x1000)


def test_original_vector_boundary_stops_at_first_external_service(cpu_binary, tmp_path):
    """Oracle: original loop/table/relocations and conditional write arithmetic, no service run."""
    report = contracts.startup_vector_boundary_contract(cpu_binary, load_segment=0x1000)
    boundary = report["vector_boundary"]
    loop = bytes.fromhex("bff07abe3902b9130090fc2eacb435cd21891d8c450283c704e2ef")
    numbers = bytes.fromhex("00021b2123243435363738393a3b3c3d3e3f75")
    assert boundary["file_offset"] == 91529
    assert boundary["reviewed_bytes_hex"] == loop.hex()
    assert boundary["table_file_offset"] == 92025
    assert boundary["interrupt_numbers"] == list(numbers)
    assert boundary["stop_before_startup_offset"] == 0x58
    assert boundary["service_return_ip"] == 0x5A
    assert boundary["first_service_inputs"] == {
        "AX": 0x3500,
        "CX": 19,
        "SI": 0x23A,
        "DI": 0x7AF0,
        "DF": 0,
    }
    assert boundary["ivt_entry_physical_range"] == [0x84, 0x88]
    assert boundary["conditional_vector_save_ds_range"] == [0x7AF0, 0x7B3C]
    assert boundary["conditional_loop_return_offset"] == 0x64
    assert boundary["loop_target_offset"] == 0x53
    assert 0x64 + int.from_bytes(loop[-1:], "little", signed=True) == 0x53
    assert boundary["interrupt_frame_module_range"] == [201302, 201308]
    assert boundary["required_loop_preservation"] == [
        "DS",
        "SI",
        "DI",
        "CX",
        "SS",
        "SP",
    ]
    assert boundary["service_contract_established"] is False
    assert boundary["execution_cases"] == 0
    bridge = boundary["first_return_bridge"]
    assert bridge["return_offset"] == 0x5A
    assert bridge["store_bytes_hex"] == "891d8c4502"
    assert bridge["add_loop_bytes_hex"] == "83c704e2ef"
    assert bridge["conditional_first_store_ds_range"] == [0x7AF0, 0x7AF4]
    assert bridge["next_lodsb_table_file_offset"] == 92026
    assert bridge["next_service_inputs"] == {
        "AX": 0x3502,
        "CX": 18,
        "SI": 0x23B,
        "DI": 0x7AF4,
        "DF": 0,
    }
    assert bridge["execution_cases"] == 0
    assert bridge["second_service_contract_established"] is False
    second_bridge = boundary["second_return_bridge"]
    assert second_bridge["store_bytes_hex"] == bridge["store_bytes_hex"]
    assert second_bridge["add_loop_bytes_hex"] == bridge["add_loop_bytes_hex"]
    assert second_bridge["conditional_second_store_ds_range"] == [0x7AF4, 0x7AF8]
    assert second_bridge["next_lodsb_table_file_offset"] == 92027
    assert second_bridge["next_service_inputs"] == {
        "AX": 0x351B,
        "CX": 17,
        "SI": 0x23C,
        "DI": 0x7AF8,
        "DF": 0,
    }
    assert second_bridge["third_service_contract_established"] is False
    assert second_bridge["execution_cases"] == 0
    # The returned pointer is stored, not dereferenced. Each later CLD resets DF.
    assert loop[0x53 - 0x49 : 0x56 - 0x49] == bytes.fromhex("fc2eac")
    assert loop[0x5A - 0x49 : 0x5F - 0x49] == bytes.fromhex("891d8c4502")
    slots = [0x7AF0 + 4 * index for index in range(len(numbers))]
    assert slots[-1] == 0x7B38
    assert slots[-1] + 4 == 0x7B3C
    assert len(set(slots)) == 19
    assert boundary["conditional_slot_offsets"] == slots
    assert "not a service preservation guarantee" in " ".join(boundary["limitations"])
    root = pathlib.Path(__file__).resolve().parents[1]
    allocator = load_contract(root / "targets/liero", "FUN_24dd_0353")
    evidence = allocator["startup_heap_evidence"]["next_external_boundary"]
    for field in (
        "file_offset",
        "reviewed_bytes_hex",
        "interrupt_numbers",
        "conditional_vector_save_ds_range",
        "service_contract_established",
    ):
        assert evidence[field] == boundary[field]
    paths = (
        root / "tools/liero_startup_clear_contract.py",
        pathlib.Path(__file__),
        root / "targets/liero/config/routine_contracts.json",
        root / "targets/liero/recovery.json",
        root / "engine/alternate_streams.py",
        root / "engine/instruction_facts.py",
    )
    report["evidence_hashes"] = {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
    }
    for path in paths:
        destination = tmp_path / "sources" / path.relative_to(root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(path.read_bytes())
    (tmp_path / "vector-loop.bin").write_bytes(loop)
    (tmp_path / "vector-numbers.bin").write_bytes(numbers)
    (tmp_path / "result.json").write_text(json.dumps(report, indent=2) + "\n")


@pytest.mark.parametrize("offset", [*range(0x49, 0x64), *range(0x239, 0x24C)])
def test_vector_boundary_rejects_all_loop_and_table_mutants(cpu_binary, offset):
    """Oracle: no opcode, vector ID or branch mutation hides behind a valid heap prefix."""
    binary = bytearray(cpu_binary)
    binary[91456 + offset] ^= 1
    with pytest.raises(ValueError, match="vector"):
        contracts.startup_vector_boundary_contract(bytes(binary), load_segment=0x1000)


@pytest.mark.parametrize("offset", [0x48, 0x49, 0x58, 0x63, 0x238, 0x239, 0x24B])
def test_vector_boundary_rejects_overlapping_loader_relocations(cpu_binary, offset):
    """Oracle: loader words starting just before a reviewed range also invalidate it."""
    binary = bytearray(cpu_binary)
    table = struct.unpack_from("<H", binary, 24)[0]
    count = struct.unpack_from("<H", binary, 6)[0]
    locations = []
    for index in range(count):
        relative_offset, segment = struct.unpack_from("<HH", binary, table + index * 4)
        locations.append((segment * 16 + relative_offset, index))
    _, index = next(
        (location, index) for location, index in locations if location > 100000
    )
    struct.pack_into("<HH", binary, table + index * 4, offset, 0x14DD)
    with pytest.raises(ValueError, match="relocat"):
        contracts.startup_vector_boundary_contract(bytes(binary), load_segment=0x1000)


def mz_fixture() -> bytearray:
    """Oracle: synthetic exact-shape MZ with known code/data/stack intervals."""
    binary = bytearray(48 + 512)
    struct.pack_into(
        "<14H",
        binary,
        0,
        0x5A4D,
        48,
        2,
        2,
        3,
        0x40,
        0xFFFF,
        0x40,
        0x100,
        0,
        0x10,
        0,
        28,
        0,
    )
    struct.pack_into("<4H", binary, 28, 0x13, 0, 1, 0x10)
    binary[48 + 0x10 : 48 + 0x15] = bytes.fromhex("9a00001000")
    binary[48 + 0x100 : 48 + 0x10E] = bytes.fromhex("ba30008eda8c06000033ede83200")
    binary[48 + 0x140 : 48 + 0x152] = bytes.fromhex(
        "bf10001e07b920002bcfd1e933c0fcf3abc3"
    )
    return binary


def test_derives_loader_ranges_near_return_and_preserves_generic_residue():
    """Oracle: exact independent synthetic arithmetic, not compilation."""
    report = startup_clear_contract(bytes(mz_fixture()), load_segment=0x1000)
    assert report["mz"]["minimum_allocation_bytes"] == 1536
    assert report["startup"]["relocated_ds"] == 0x1030
    assert report["startup"]["relocated_cs"] == 0x1010
    assert report["startup"]["near_return_ip"] == 14
    assert report["clear"]["ds_range"] == [16, 32]
    assert report["clear"]["word_count"] == 8
    assert report["module_relative_ranges"]["clear_memory"] == [784, 800]
    assert report["module_relative_ranges"]["active_stack"] == [1272, 1280]
    assert report["stack"] == {
        "at_startup": 252,
        "at_clear_entry": 250,
        "lowest_during_clear": 248,
        "after_clear": 252,
    }
    assert report["clear"]["supported_prefix"]["residue"]["offset"] == 17
    assert report["clear"]["supported_prefix"]["residue"]["bytes_hex"] == "c3"
    assert report["routine_recovered"] is False


@pytest.mark.parametrize(
    ("offset", "value", "reason"),
    [
        (0, 0, "MZ bytes"),
        (2, 47, "MZ size"),
        (10, 0, "guaranteed MZ allocation"),
        (14, 0x22, "aliases"),
        (17, 0, "initial stack"),
        (28, 0x12, "exclusively relocated"),
        (32, 0, "startup DS/store"),
        (48 + 0x10, 0xEA, "far call"),
        (48 + 0x11, 1, "startup entry offset"),
        (48 + 0x103, 0x8C, "startup DS/store"),
        (48 + 0x107, 0x10, "aliases clear_memory"),
        (48 + 0x10C, 0x31, "near-clear shape"),
        (48 + 0x146, 0x21, "even nonwrapping"),
        (48 + 0x151, 0xCB, "near-clear shape"),
    ],
)
def test_rejects_header_path_and_memory_mutants(offset, value, reason):
    """Oracle: one unsupported byte cannot be hidden behind a passing prefix."""
    binary = mz_fixture()
    binary[offset] = value
    with pytest.raises(ValueError, match=reason):
        startup_clear_contract(bytes(binary), load_segment=0x1000)


@pytest.mark.parametrize("relative_location", [0x13, 0x14, 0x141])
def test_rejects_duplicate_overlapping_or_clear_relocations(relative_location):
    """Oracle: loader applies every relocation, including duplicate/overlap hazards."""
    binary = mz_fixture()
    struct.pack_into("<H", binary, 6, 3)
    struct.pack_into("<2H", binary, 36, relative_location, 0)
    with pytest.raises(ValueError, match="relocat"):
        startup_clear_contract(bytes(binary), load_segment=0x1000)


@pytest.mark.parametrize(
    "offset",
    [0, 3, 4, 5, 6, 9, 10, 11],
)
def test_rejects_each_fixed_startup_opcode_mutant(offset):
    """Oracle: prefix instruction semantics require exact bytes, not a few anchors."""
    binary = mz_fixture()
    binary[48 + 0x100 + offset] ^= 1
    with pytest.raises(ValueError, match="startup DS/store"):
        startup_clear_contract(bytes(binary), load_segment=0x1000)


@pytest.mark.parametrize("offset", [0, 3, 4, 5, *range(8, 18)])
def test_rejects_each_fixed_clear_opcode_mutant(offset):
    """Oracle: no opcode, flag setup, loop or return mutation is accepted."""
    binary = mz_fixture()
    binary[48 + 0x140 + offset] ^= 1
    with pytest.raises(ValueError, match="near-clear shape"):
        startup_clear_contract(bytes(binary), load_segment=0x1000)


def test_varied_operands_are_derived_without_original_liero_constants():
    """Oracle: independent synthetic operand arithmetic at a different load base."""
    binary = mz_fixture()
    struct.pack_into("<H", binary, 48 + 0x101, 0x31)
    struct.pack_into("<H", binary, 48 + 0x141, 0x20)
    struct.pack_into("<H", binary, 48 + 0x146, 0x40)
    report = startup_clear_contract(bytes(binary), load_segment=0x1200)
    assert report["startup"]["relocated_ds"] == 0x1231
    assert report["clear"]["ds_range"] == [32, 64]
    assert report["clear"]["word_count"] == 16
    assert report["module_relative_ranges"]["clear_memory"] == [816, 848]


@pytest.mark.parametrize("base", [True, -1, 0, 65535, 0xFFF0])
def test_rejects_unsupported_loader_bases(base):
    """Oracle: logical addresses may not silently wrap physical/segment bounds."""
    with pytest.raises(ValueError):
        startup_clear_contract(bytes(mz_fixture()), load_segment=base)


def test_original_mz_entry_allocation_and_stack_are_bound():
    """Oracle: BYOD bytes and relocation table, not exported assembly text."""
    root = pathlib.Path(__file__).resolve().parents[1]
    binary_path = root / "extracted/liero/LIERO.EXE"
    if not binary_path.is_file():
        pytest.skip("Liero BYOD unavailable")
    binary = binary_path.read_bytes()
    assert hashlib.sha256(binary).hexdigest() == (
        "e45653ab0f915238f7394b2846b70288d0cc35a2595debc2a49502078398c7d1"
    )
    report = startup_clear_contract(binary, load_segment=0x1000)
    assert report["entry"]["file_offset"] == 64535
    assert report["entry"]["bytes_hex"] == "9a0000dd14"
    assert report["startup"]["file_offset"] == 91456
    assert report["startup"]["segment_relocation_file_offset"] == 91457
    assert report["startup"]["relocated_ds"] == 0x2971
    assert report["mz"]["minimum_allocation_bytes"] == 201312
    assert report["clear"]["file_offset"] == 110188
    assert report["clear"]["word_count"] == 2966
    assert report["module_relative_ranges"]["clear_memory"] == [129846, 135778]
    assert report["module_relative_ranges"]["active_stack"] == [201304, 201312]
    assert report["startup"]["near_return_ip"] == 14


def test_report_preserves_evidence_identity_and_refuses_overwrite(tmp_path):
    """Oracle: manifest authentication, immutable method snapshots and fresh output."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    output = tmp_path / "contract"
    report = write_startup_clear_contract(root, output)
    assert json.loads((output / "result.json").read_text()) == report
    for relative, expected in report["evidence_hashes"].items():
        assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected
        if relative.endswith(".py"):
            assert (output / pathlib.Path(relative).name).read_bytes() == (
                root / relative
            ).read_bytes()
    with pytest.raises(FileExistsError):
        write_startup_clear_contract(root, output)
