import hashlib
import json
import pathlib
import shutil
import struct

import pytest

from tools import liero_startup_clear_probe as probe
from tools.liero_startup_clear_contract import startup_clear_contract
from tools.liero_startup_clear_probe import (
    APPEND_OFFSET,
    build_instrumented_mz,
    compare_trace,
    instrumentation_source,
    run_layout_probe,
)


def test_full_startup_actual_return_and_default_objects(
    tmp_path, original, monkeypatch
):
    """Oracle: original entire startup returned; fixed identities, not Pascal startup parity."""
    if not all(shutil.which(tool) for tool in ("dosbox", "as", "ld")):
        pytest.skip("original startup toolchain unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "full-return"
    result = probe.run_startup_return(root, output)
    assert result["default_objects"]["79f0"]["handle"] == 1
    assert result["default_objects"]["79f0"]["flush"] == [
        0x37B3,
        result["code_segment"],
    ]
    assert result["source_recovered"] is False
    assert result["normal_unmodified_game"] is False
    monkeypatch.setattr(
        probe, "run_dosbox", lambda *_: pytest.fail("replay executed DOS")
    )
    assert probe.replay_startup_return(root, output) == result
    binary, _ = original
    patched = (output / "PROBE.COM").read_bytes()
    freeze = json.loads((output / "freeze.json").read_text())
    contract = freeze["contract"]
    start = contract["startup"]["file_offset"]
    assert patched[start : start + 0xB1] == binary[start : start + 0xB1]
    assert patched[6:8] == binary[6:8]
    trace = (output / "TRACE.BIN").read_bytes()
    for offset in (
        0x40C,
        0x410,
        0x18F0,
        0x18F2,
        0x19F0,
        0x19FC,
        0x1A04,
        0x1A08,
        0x1A0C,
        *range(8192, 8210, 2),
    ):
        mutant = bytearray(trace)
        mutant[offset] ^= 1
        with pytest.raises(ValueError):
            probe.compare_startup_return(bytes(mutant), contract)
    with pytest.raises(ValueError):
        probe.compare_startup_return(trace[:-1], contract)


@pytest.fixture
def original():
    """Oracle: actual read-only BYOD and already tested exact loader contract."""
    root = pathlib.Path(__file__).resolve().parents[1]
    path = root / "extracted/liero/LIERO.EXE"
    if not path.is_file():
        pytest.skip("Liero BYOD unavailable")
    binary = path.read_bytes()
    return binary, startup_clear_contract(binary, load_segment=0x1000)


def memory_fixture():
    """Oracle: independent synthetic trace, explicit loader/clear/startup arithmetic."""
    contract = {
        "load_segment": 0x1000,
        "mz": {"initial_ss": 0x3127, "initial_sp": 0xFFF0},
        "startup": {"relocated_cs": 0x24DD, "relocated_ds": 0x2971},
        "clear": {"ds_range": [0x6426, 0x7B52]},
        "module_relative_ranges": {"saved_entry_es": [129820, 129822]},
    }
    seed = 0xA5
    pascal = bytearray([seed] * 8192)
    pascal[0x426:0x1B52] = bytes(5932)
    trace = bytearray(pascal)
    base = 0x800
    trace[0x40C:0x40E] = struct.pack("<H", base - 16)
    trace.extend(
        struct.pack(
            "<8H",
            base + 0x2127,
            0xFFF0,
            base - 16,
            base + 0x14DD,
            base + 0x1971,
            base + 0x1971,
            base + 0x2127,
            0xFFEC,
        )
    )
    return bytes(trace), bytes(pascal), contract


def test_full_trace_checks_every_byte_and_explicit_startup_word():
    """Oracle: no masking except independently validated startup ES-store composition."""
    trace, pascal, contract = memory_fixture()
    report = compare_trace(trace, pascal, contract, 0xA5)
    assert report["bytes_checked"] == 8192
    assert report["guards_checked"] == 2258
    assert report["startup_only_saved_es"] == {"window_offset": 0x40C, "value": 0x7F0}
    assert report["observed_load_segment"] == 0x800
    assert report["original_only_sp_after_clear"] == 0xFFEC


@pytest.mark.parametrize(
    "offset", [0, 0x40C, 0x40D, 0x426, 0x1B51, 0x1B52, 8191, *range(8192, 8208)]
)
def test_original_memory_or_abi_mutant_fails(offset):
    """Oracle: guards, clear boundaries, startup word and each recorded register are checked."""
    trace, pascal, contract = memory_fixture()
    mutated = bytearray(trace)
    mutated[offset] ^= 1
    with pytest.raises(ValueError):
        compare_trace(bytes(mutated), pascal, contract, 0xA5)


@pytest.mark.parametrize("offset", [0, 0x40C, 0x40D, 0x426, 0x1B51, 0x1B52, 8191])
def test_pascal_mutant_fails_without_silently_normalizing(offset):
    """Oracle: Pascal startup-only bytes must still hold the dirty seed."""
    trace, pascal, contract = memory_fixture()
    mutated = bytearray(pascal)
    mutated[offset] ^= 1
    with pytest.raises(ValueError):
        compare_trace(trace, bytes(mutated), contract, 0xA5)


@pytest.mark.parametrize(
    "trace_length,pascal_length", [(0, 8192), (8207, 8192), (8209, 8192), (8208, 8191)]
)
def test_truncated_or_extended_outputs_fail(trace_length, pascal_length):
    """Oracle: output shapes are exact; absent results cannot count as success."""
    with pytest.raises(ValueError, match="length"):
        compare_trace(bytes(trace_length), bytes(pascal_length), {}, 0xA5)


def test_mz_patch_inventory_preserves_original_path_and_allocation(original):
    """Oracle: independent byte diff and MZ allocation arithmetic."""
    binary, contract = original
    boot = APPEND_OFFSET - 0x14DD * 16
    patched, report = build_instrumented_mz(binary, contract, bytes(300), boot + 50)
    header = contract["mz"]["header_bytes"]
    assert (len(patched) - header + 15) // 16 * 16 + struct.unpack_from(
        "<H", patched, 10
    )[0] * 16 == 201312
    assert (len(patched) - header + 15) // 16 + struct.unpack_from("<H", patched, 12)[
        0
    ] == (len(binary) - header + 15) // 16 + struct.unpack_from("<H", binary, 12)[0]
    assert struct.unpack_from("<HH", patched, 20) == (boot, 0x14DD)
    for section, size in (("entry", 5), ("startup", 14), ("clear", 18)):
        start = contract[section]["file_offset"]
        assert patched[start : start + size] == binary[start : start + size]
    assert patched[28:6000] == binary[28:6000]
    assert report["original_byte_changes"] == [
        {"file_offset": index, "original": before, "instrumented": after}
        for index, (before, after) in enumerate(zip(binary, patched))
        if before != after
    ]


def test_changed_binary_and_invalid_payload_fail(original):
    """Oracle: stale inputs and out-of-segment instrumentation cannot be patched."""
    binary, contract = original
    with pytest.raises(ValueError, match="binary differs"):
        build_instrumented_mz(binary + b"x", contract, bytes(300), 52000)
    with pytest.raises(ValueError, match="instrumentation"):
        build_instrumented_mz(binary, contract, b"", 52000)
    with pytest.raises(ValueError, match="instrumentation"):
        build_instrumented_mz(binary, contract, bytes(20000), 52000)


def test_dirty_window_cannot_alias_original_code(original):
    """Oracle: bootstrap initialization must not corrupt measured instructions."""
    binary, contract = original
    contract["module_relative_ranges"]["entry_code"] = [129000, 129005]
    with pytest.raises(ValueError, match="dirty window aliases entry_code"):
        build_instrumented_mz(binary, contract, bytes(300), 52000)


def test_dirty_window_cannot_exceed_original_allocation(original):
    """Oracle: guard setup also requires allocated writable memory, not just the clear."""
    binary, contract = original
    contract["mz"]["minimum_allocation_bytes"] = 130000
    with pytest.raises(ValueError, match="dirty window exceeds"):
        build_instrumented_mz(binary, contract, bytes(300), 52000)


def test_unfrozen_seed_fails(original):
    """Oracle: no implicit extension of the three-case budget."""
    _, contract = original
    with pytest.raises(ValueError, match="budget"):
        instrumentation_source(contract, 0)


def test_native_or_environment_failure_is_recorded_without_retry(
    tmp_path, original, monkeypatch
):
    """Oracle: a missing/failed DOS result ends the frozen experiment immediately."""
    if not all(shutil.which(tool) for tool in ("as", "ld", "nm", "dosbox", "fpc")):
        pytest.skip("probe build tools unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "failed"
    calls = []

    def fail(directory):
        """Oracle: explicit injected environment failure, not a recovery measurement."""
        calls.append(directory)
        raise RuntimeError("injected DOS worker failure")

    monkeypatch.setattr(probe, "run_dosbox", fail)
    with pytest.raises(RuntimeError, match="injected DOS"):
        run_layout_probe(root, output)
    failure = json.loads((output / "failure.json").read_text())
    assert failure["completed_cases"] == 0
    assert failure["retry_allowed"] is False
    assert len(calls) == 1
    assert (output / "freeze.json").is_file()
    assert not (output / "result.json").exists()
    assert not (output / "seed-5a").exists()


def test_instrumented_original_loader_layout_vs_pascal(tmp_path, original):
    """Oracle: real DOS MZ loading/original path and compiled Pascal, three fixed contexts."""
    if not all(shutil.which(tool) for tool in ("as", "ld", "nm", "dosbox", "fpc")):
        pytest.skip("DOS/Pascal probe tools unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "layout"
    result = run_layout_probe(root, output)
    assert result["status"] == "scoped-memory-pass"
    assert result["bytes_checked"] == 24576
    assert [case["seed"] for case in result["cases"]] == [0xA5, 0x5A, 0xFF]
    assert not (output / "failure.json").exists()
    assert result["routine_recovered"] is False
    freeze = json.loads((output / "freeze.json").read_text())
    for relative, expected in freeze["method_hashes"].items():
        assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected
    for case in result["cases"]:
        directory = output / f"seed-{case['seed']:02x}"
        for name, expected in case["artifact_hashes"].items():
            assert (
                hashlib.sha256((directory / name).read_bytes()).hexdigest() == expected
            )
    with pytest.raises(FileExistsError):
        run_layout_probe(root, output)


def heap_trace_fixture():
    """Oracle: independent synthetic original-only heap/PSP trace, not execution."""
    root = pathlib.Path(__file__).resolve().parents[1]
    path = root / "extracted/liero/LIERO.EXE"
    if not path.is_file():
        pytest.skip("Liero BYOD unavailable")
    binary = path.read_bytes()
    contract = probe.startup_heap_contract(binary, load_segment=0x1000)
    base = 0x800
    ss, ds, cs, psp = base + 0x2127, base + 0x1971, base + 0x14DD, base - 16
    heap, limit = ss + 0xFFF, 0x9FFF
    data = bytearray(8192)
    for cell in (0x63DE, 0x63E0, 0x63E2, 0x63EC, 0x63F0, 0x63F8):
        struct.pack_into("<H", data, cell - 0x6000, heap)
    for cell, value in ((0x63F4, limit), (0x63FE, 0xD6), (0x6400, cs), (0x640C, psp)):
        struct.pack_into("<H", data, cell - 0x6000, value)
    data[0x420] = 2
    data.extend(struct.pack("<9H", ss, 0xFFF0, psp, cs, ds, psp, ss, 0xFFEC, limit))
    return bytes(data), contract


def test_heap_observation_records_capacity_without_pascal_or_allocation_claim():
    """Oracle: exact synthetic shape, independently calculated heap and PSP fields."""
    trace, contract = heap_trace_fixture()
    result = probe.compare_heap_trace(trace, contract)
    assert result["observed_load_segment"] == 0x800
    assert result["heap_start_segment"] == 0x3926
    assert result["allocation_end_segment"] == 0x9FFF
    assert result["spare_heap_bytes"] == (0x9FFF - 0x3926) * 16
    assert result["cleared_bytes_checked"] == 5932
    assert result["observed_cpu_class"] == 2
    assert result["allocation_success_established"] is False
    assert result["pascal_parity"] is False


@pytest.mark.parametrize(
    "offset",
    [
        0x3D8,
        0x3DE,
        0x3E0,
        0x3E2,
        0x3EC,
        0x3EE,
        0x3F0,
        0x3F2,
        0x3F4,
        0x3F6,
        0x3F8,
        0x3FE,
        0x400,
        0x40C,
        0x426,
        0x1B3C,
        0x1B51,
        *range(8192, 8210),
    ],
)
def test_heap_state_and_record_mutations_fail(offset):
    """Oracle: initialized cells, clear and every loader/PSP record byte are checked."""
    trace, contract = heap_trace_fixture()
    mutated = bytearray(trace)
    mutated[offset] ^= 1
    with pytest.raises(ValueError):
        probe.compare_heap_trace(bytes(mutated), contract)


@pytest.mark.parametrize("size", [0, 8208, 8209, 8211])
def test_heap_trace_shape_is_exact(size):
    """Oracle: clear-only trace cannot be mistaken for heap/PSP observation."""
    with pytest.raises(ValueError, match="length"):
        probe.compare_heap_trace(bytes(size), {})


def test_heap_probe_preserves_original_data_and_measured_path(original):
    """Oracle: independent patch inventory; no dirty bootstrap before heap observation."""
    binary, _ = original
    contract = probe.startup_heap_contract(binary, load_segment=0x1000)
    source = instrumentation_source(contract, 0xA5, heap=True)
    assert "rep stosb" not in source
    assert "mov %es:2, %ax" in source
    assert source.index("mov %es:2, %ax") < source.index("int $0x21")
    boot = APPEND_OFFSET - 0x14DD * 16
    patched, report = build_instrumented_mz(
        binary, contract, bytes(300), boot + 50, heap=True
    )
    start = contract["startup"]["file_offset"]
    assert patched[start : start + 0x49] == binary[start : start + 0x49]
    assert patched[start + 0xB1 : start + 0xDB] == binary[start + 0xB1 : start + 0xDB]
    assert patched[28:6000] == binary[28:6000]
    assert report["stop_before_startup_offset"] == 0x49
    allowed = {
        *range(2, 6),
        *range(10, 14),
        *range(20, 24),
        *range(start + 0x49, start + 0x4C),
    }
    assert all(c["file_offset"] in allowed for c in report["original_byte_changes"])


@pytest.mark.parametrize("offset", range(56))
def test_heap_contract_rejects_each_initializer_mutant(original, offset):
    """Oracle: every measured initializer byte is authenticated before execution."""
    binary, _ = original
    mutated = bytearray(binary)
    mutated[91473 + offset] ^= 1
    with pytest.raises(ValueError, match="heap initializer"):
        probe.startup_heap_contract(bytes(mutated), load_segment=0x1000)


@pytest.mark.parametrize("cell", [0x63D8, 0x63EE, 0x63F2, 0x63F6])
def test_heap_contract_rejects_changed_initial_zero_state(original, cell):
    """Oracle: no invented initial data may be normalized into a passing heap fixture."""
    binary, _ = original
    mutated = bytearray(binary)
    mutated[6000 + 0x1971 * 16 + cell] = 1
    with pytest.raises(ValueError, match="heap initial zero word"):
        probe.startup_heap_contract(bytes(mutated), load_segment=0x1000)


@pytest.mark.parametrize(
    "mode", ["heap", "service", "bridge", "second", "second-bridge", "third"]
)
def test_heap_environment_failure_stops_without_retry(
    tmp_path, original, monkeypatch, mode
):
    """Oracle: explicit worker failure cannot fall back to clear/Pascal success."""
    if not all(shutil.which(tool) for tool in ("as", "ld", "nm", "dosbox")):
        pytest.skip("probe build tools unavailable")
    calls = []

    def fail(directory):
        """Oracle: injected environment failure, not original execution."""
        calls.append(directory)
        raise RuntimeError("injected heap worker failure")

    monkeypatch.setattr(probe, "run_dosbox", fail)
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "heap-failed"
    with pytest.raises(RuntimeError, match="injected heap worker"):
        options = (
            {"second": True, "bridge": True}
            if mode == "second-bridge"
            else {mode: True}
        )
        run_layout_probe(root, output, **options)
    assert len(calls) == 1
    assert not (output / "result.json").exists()
    assert not (output / "partial").exists()
    failure = json.loads((output / "failure.json").read_text())
    assert failure["completed_cases"] == 0
    assert failure["retry_allowed"] is False


def test_instrumented_heap_observation(tmp_path, original):
    """Oracle: one disclosed original-only DOSBox heap/PSP observation, no retries."""
    if not all(shutil.which(tool) for tool in ("as", "ld", "nm", "dosbox")):
        pytest.skip("DOS probe tools unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "heap"
    result = run_layout_probe(root, output, heap=True)
    assert result["status"] == "scoped-heap-observation-pass"
    assert result["oracle"] == "instrumented_original_mz_heap_initialization"
    assert len(result["cases"]) == 1
    assert not (output / "partial").exists()
    assert not (output / "seed-a5/PASCAL.BIN").exists()
    assert result["routine_recovered"] is False
    freeze = json.loads((output / "freeze.json").read_text())
    assert freeze["budget"].startswith("one original-only execution")
    for name, expected in freeze["method_hashes"].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected


def service_trace_fixture():
    """Oracle: independently composed synthetic pre/post record and protected memory."""
    heap_trace, _ = heap_trace_fixture()
    root = pathlib.Path(__file__).resolve().parents[1]
    original = root / "extracted/liero/LIERO.EXE"
    if not original.is_file():
        pytest.skip("Liero BYOD unavailable")
    contract = probe.startup_vector_boundary_contract(
        original.read_bytes(), load_segment=0x1000
    )
    before = dict(
        zip(
            probe.SERVICE_REGISTERS,
            (
                0x9F00,
                0x1234,
                19,
                0x4567,
                0x23A,
                0x7AF0,
                0,
                0x2171,
                0x7F0,
                0x2927,
                0xFFEC,
                0x202,
                0x9FFF,
                0x1234,
                0xF000,
                0x5678,
                0xF001,
            ),
            strict=True,
        )
    )
    after = {**before, "AX": 0x3500, "BX": 0x1234, "ES": 0xF000}
    memory = heap_trace[0x3D8:0x1B52]
    trace = struct.pack("<3H", 0x2927, 0xFFF0, 0x7F0)
    for record in (before, after):
        trace += struct.pack(
            "<17H", *(record[name] for name in probe.SERVICE_REGISTERS)
        )
    return trace + memory + memory, contract


def test_service_trace_checks_scoped_registers_result_and_memory():
    """Oracle: exact synthetic trace; successful measurement must not accept service ABI."""
    trace, contract = service_trace_fixture()
    result = probe.compare_service_trace(trace, contract)
    assert result["trace_bytes"] == 12094
    assert result["protected_bytes_unchanged"] == 6010
    assert result["vector0_result"] == [0xF000, 0x1234]
    assert result["handler21_observed"] == [0xF001, 0x5678]
    assert result["service_contract_established"] is False
    assert result["pascal_parity"] is False


@pytest.mark.parametrize(
    "offset",
    [
        0,
        2,
        4,
        6,
        10,
        14,
        16,
        20,
        24,
        26,
        29,
        30,
        32,
        34,
        36,
        38,
        42,
        44,
        48,
        50,
        54,
        58,
        60,
        64,
        66,
        68,
        70,
        72,
        74,
        74 + 0x426 - 0x3D8,
        6083,
        6084,
        12093,
    ],
)
def test_service_trace_mutations_fail(offset):
    """Oracle: changed bindings, IVT/result, baseline and protected memory cannot pass."""
    trace, contract = service_trace_fixture()
    trace = bytearray(trace)
    trace[offset] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract)


@pytest.mark.parametrize("size", [0, 8210, 12093, 12095])
def test_service_trace_requires_exact_shape(size):
    """Oracle: older heap trace cannot be mistaken for a pre/post service measurement."""
    with pytest.raises(ValueError, match="length"):
        probe.compare_service_trace(bytes(size), {})


@pytest.mark.parametrize(
    "cell",
    [
        0x63D8,
        0x63DE,
        0x63E0,
        0x63E2,
        0x63EC,
        0x63EE,
        0x63F0,
        0x63F2,
        0x63F4,
        0x63F6,
        0x63F8,
        0x63FE,
        0x6400,
        0x640C,
        0x6426,
        0x7B51,
    ],
)
def test_service_unchanged_but_invalid_baseline_rejected(cell):
    """Oracle: pre/post equality cannot hide an invalid initial heap or clear state."""
    trace, contract = service_trace_fixture()
    trace = bytearray(trace)
    for start in (74, 6084):
        trace[start + cell - probe.SERVICE_WINDOW[0]] ^= 1
    with pytest.raises(ValueError, match="pre-call"):
        probe.compare_service_trace(bytes(trace), contract)


def test_service_patch_inventory_preserves_original_int(original):
    """Oracle: original AH35/INT21 intact; relocated prefix and both jumps disclosed."""
    binary, _ = original
    contract = probe.startup_vector_boundary_contract(binary, load_segment=0x1000)
    source = probe.service_instrumentation_source(contract)
    assert "rep stosb" not in source
    assert source.index("before_service:") < source.index("collector:")
    assert ".byte 0xfc, 0x2e, 0xac" in source
    boot = APPEND_OFFSET - 0x14DD * 16
    patched, report = build_instrumented_mz(
        binary,
        contract,
        bytes(13000),
        boot + 500,
        heap=True,
        service_entry=boot + 100,
    )
    start = contract["startup"]["file_offset"]
    assert patched[start : start + 0x53] == binary[start : start + 0x53]
    assert patched[start + 0x56 : start + 0x5A] == bytes.fromhex("b435cd21")
    assert report["stop_before_startup_offset"] == 0x5A
    allowed = {
        *range(2, 6),
        *range(10, 14),
        *range(20, 24),
        *range(start + 0x53, start + 0x56),
        *range(start + 0x5A, start + 0x5D),
    }
    assert all(c["file_offset"] in allowed for c in report["original_byte_changes"])


def test_instrumented_first_service_observation(tmp_path, original):
    """Oracle: one frozen original AH35/AL0 execution, no repair/holdout/source promotion."""
    if not all(shutil.which(tool) for tool in ("as", "ld", "nm", "dosbox")):
        pytest.skip("DOS probe tools unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "service"
    result = run_layout_probe(root, output, service=True)
    assert result["status"] == "scoped-first-vector-service-observation-pass"
    assert result["bytes_checked"] == 6010
    assert len(result["cases"]) == 1
    assert result["cases"][0]["service_contract_established"] is False
    assert not (output / "partial").exists()
    freeze = json.loads((output / "freeze.json").read_text())
    for name, expected in freeze["method_hashes"].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected


def bridge_trace_fixture():
    """Oracle: synthetic first-service-return to next-query state, not DOS execution."""
    trace, contract = service_trace_fixture()
    before = list(struct.unpack_from("<17H", trace, 40))
    after = before.copy()
    for reg, value in {
        "AX": 0x3502,
        "CX": 18,
        "SI": 0x23B,
        "DI": 0x7AF4,
        "FLAGS": before[11] & ~0xCD5,
    }.items():
        after[probe.SERVICE_REGISTERS.index(reg)] = value
    before_memory = trace[74:6084]
    after_memory = bytearray(before_memory)
    struct.pack_into(
        "<HH", after_memory, 0x7AF0 - probe.SERVICE_WINDOW[0], before[1], before[8]
    )
    return (
        trace[:6]
        + struct.pack("<17H", *before)
        + struct.pack("<17H", *after)
        + before_memory
        + after_memory
    ), contract


def test_bridge_trace_exact_slot_next_input_and_flags():
    """Oracle: full window including slot, register/flag transitions; no second service."""
    trace, contract = bridge_trace_fixture()
    result = probe.compare_service_trace(trace, contract, bridge=True)
    assert result["trace_bytes"] == 12094
    assert result["memory_bytes_checked"] == 6010
    assert result["protected_bytes_unchanged"] == 6006
    assert result["next_service_ax"] == 0x3502
    assert result["second_service_executed"] is False
    assert result["service_contract_established"] is False


@pytest.mark.parametrize("reg", probe.SERVICE_REGISTERS)
def test_bridge_rejects_each_changed_next_register(reg):
    """Oracle: no unaccounted next-binding or flag change is accepted."""
    trace, contract = bridge_trace_fixture()
    trace = bytearray(trace)
    trace[40 + 2 * probe.SERVICE_REGISTERS.index(reg)] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract, bridge=True)


@pytest.mark.parametrize(
    "cell",
    [
        0x63D8,
        0x63FE,
        0x6400,
        0x6426,
        0x7AEF,
        0x7AF0,
        0x7AF1,
        0x7AF2,
        0x7AF3,
        0x7AF4,
        0x7B3C,
        0x7B51,
    ],
)
def test_bridge_rejects_wrong_store_or_other_memory(cell):
    """Oracle: pointer order/segment and both slot boundaries are checked, not masked."""
    trace, contract = bridge_trace_fixture()
    trace = bytearray(trace)
    trace[6084 + cell - probe.SERVICE_WINDOW[0]] ^= 1
    with pytest.raises(ValueError, match="memory"):
        probe.compare_service_trace(bytes(trace), contract, bridge=True)


@pytest.mark.parametrize("flags", [0x202, 0xED7, 0x7202, 0x7ED7])
def test_bridge_accepts_service_df_and_defined_add_flag_changes(flags):
    """Oracle: service DF may be set; ADD and next CLD establish defined next flags."""
    trace, contract = bridge_trace_fixture()
    trace = bytearray(trace)
    struct.pack_into("<H", trace, 28, flags)
    struct.pack_into("<H", trace, 62, flags & ~0xCD5)
    probe.compare_service_trace(bytes(trace), contract, bridge=True)


def test_bridge_patch_preserves_add_loop_and_discloses_stores(original):
    """Oracle: first INT and ADD/LOOP intact, five-byte displaced store and dispatch disclosed."""
    binary, _ = original
    contract = probe.startup_vector_boundary_contract(binary, load_segment=0x1000)
    source = probe.service_instrumentation_source(contract, bridge=True)
    assert ".byte 0x89, 0x1d, 0x8c, 0x45, 0x02" in source
    assert "jmp 0x5f" in source
    assert "cmp $19, %cx" in source
    boot = APPEND_OFFSET - 0x14DD * 16
    patched, report = build_instrumented_mz(
        binary,
        contract,
        bytes(13000),
        boot + 500,
        heap=True,
        service_entry=boot + 100,
        bridge=True,
    )
    start = contract["startup"]["file_offset"]
    assert patched[start : start + 0x53] == binary[start : start + 0x53]
    assert patched[start + 0x56 : start + 0x5A] == bytes.fromhex("b435cd21")
    assert patched[start + 0x5D : start + 0x5F] == b"\x90\x90"
    assert patched[start + 0x5F : start + 0x64] == bytes.fromhex("83c704e2ef")
    assert report["stop_before_startup_offset"] == 0x56
    assert len(report["bridge_disclosure"]) == 4
    allowed = {
        *range(2, 6),
        *range(10, 14),
        *range(20, 24),
        *range(start + 0x53, start + 0x56),
        *range(start + 0x5A, start + 0x5F),
    }
    assert all(c["file_offset"] in allowed for c in report["original_byte_changes"])


def test_instrumented_first_vector_bridge(tmp_path, original):
    """Oracle: one distinct frozen original bridge case, stop before second service, no retry."""
    if not all(shutil.which(tool) for tool in ("as", "ld", "nm", "dosbox")):
        pytest.skip("DOS probe tools unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "bridge"
    result = run_layout_probe(root, output, bridge=True)
    assert result["status"] == "scoped-first-vector-save-bridge-pass"
    assert result["bytes_checked"] == 6010
    assert len(result["cases"]) == 1
    assert result["cases"][0]["next_service_ax"] == 0x3502
    assert result["cases"][0]["second_service_executed"] is False
    assert not (output / "partial").exists()
    freeze = json.loads((output / "freeze.json").read_text())
    for name, expected in freeze["method_hashes"].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected


def second_service_trace_fixture():
    """Oracle: synthetic distinct IVT0/IVT2 pointers and second-call pre/post memory."""
    bridge, contract = bridge_trace_fixture()
    before = list(struct.unpack_from("<17H", bridge, 40)) + [0x4321, 0xE000]
    after = before.copy()
    after[1], after[8] = 0x4321, 0xE000
    memory = bridge[6084:]
    return (
        bridge[:6]
        + struct.pack("<19H", *before)
        + struct.pack("<19H", *after)
        + memory
        + memory
    ), contract


def test_second_service_checks_ivt2_and_preserves_first_slot():
    """Oracle: result must use IVT2, not IVT0; all6010 bytes including first slot checked."""
    trace, contract = second_service_trace_fixture()
    result = probe.compare_service_trace(trace, contract, second=True)
    assert result["trace_bytes"] == 12102
    assert result["protected_bytes_unchanged"] == 6010
    assert result["vector0_result"] == [0xF000, 0x1234]
    assert result["vector2_result"] == [0xE000, 0x4321]
    assert result["first_slot_bytes_checked"] == 4
    assert result["second_service_executed"] is True
    assert result["second_pointer_store_executed"] is False
    assert result["service_contract_established"] is False
    assert result["pascal_parity"] is False


@pytest.mark.parametrize(
    "reg",
    [
        "CX",
        "SI",
        "DI",
        "DS",
        "ES",
        "SS",
        "SP",
        "BX",
        "PSP_END",
        "VECTOR0_OFF",
        "VECTOR0_SEG",
        "IVT21_OFF",
        "IVT21_SEG",
        "VECTOR2_OFF",
        "VECTOR2_SEG",
    ],
)
def test_second_service_rejects_bad_return_register_or_ivt(reg):
    """Oracle: incorrect result/preserved registers or changed measured IVT cannot pass."""
    trace, contract = second_service_trace_fixture()
    trace = bytearray(trace)
    trace[44 + 2 * probe.SECOND_SERVICE_REGISTERS.index(reg)] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract, second=True)


@pytest.mark.parametrize("reg", ["AX", "BX", "CX", "SI", "DI", "DS", "ES", "SS", "SP"])
def test_second_service_rejects_bad_input_binding(reg):
    """Oracle: second-call preconditions must not silently use the first-call context."""
    trace, contract = second_service_trace_fixture()
    trace = bytearray(trace)
    trace[6 + 2 * probe.SECOND_SERVICE_REGISTERS.index(reg)] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract, second=True)


@pytest.mark.parametrize(
    "cell",
    [
        0x63D8,
        0x63FE,
        0x6400,
        0x6426,
        0x7AEF,
        0x7AF0,
        0x7AF1,
        0x7AF2,
        0x7AF3,
        0x7AF4,
        0x7B3C,
        0x7B51,
    ],
)
@pytest.mark.parametrize("both", [False, True])
def test_second_service_rejects_changed_or_invalid_unchanged_memory(cell, both):
    """Oracle: all protected writes rejected, including corruption equal at both endpoints."""
    trace, contract = second_service_trace_fixture()
    trace = bytearray(trace)
    starts = (82, 6092) if both else (6092,)
    for start in starts:
        trace[start + cell - probe.SERVICE_WINDOW[0]] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract, second=True)


@pytest.mark.parametrize("size", [0, 12094, 12101, 12103])
def test_second_service_requires_its_exact_trace_shape(size):
    """Oracle: first-call/bridge traces cannot masquerade as an IVT2 observation."""
    with pytest.raises(ValueError, match="length"):
        probe.compare_service_trace(bytes(size), {}, second=True)


def test_second_service_does_not_assume_ax_dx_bp_or_flags_preservation():
    """Oracle: only loop-required result/preservation gates, no invented DOS residue ABI."""
    trace, contract = second_service_trace_fixture()
    trace = bytearray(trace)
    struct.pack_into("<H", trace, 6, 0xAB02)
    for reg, value in {
        "AX": 0x4567,
        "DX": 0x1234,
        "BP": 0x9876,
        "FLAGS": 0x602,
    }.items():
        struct.pack_into(
            "<H", trace, 44 + 2 * probe.SECOND_SERVICE_REGISTERS.index(reg), value
        )
    probe.compare_service_trace(bytes(trace), contract, second=True)


def test_second_bridge_rejects_missing_or_old_shape():
    """Oracle: newly supported combination requires its full nineteen-word snapshots."""
    for size in (0, 12094, 12101, 12103):
        with pytest.raises(ValueError, match="length"):
            probe.compare_service_trace(bytes(size), {}, bridge=True, second=True)


def test_second_service_patch_inventory_and_snapshot_source(original):
    """Oracle: original calls/ADD/LOOP intact; first stores relocated; IVT2 recorded."""
    binary, _ = original
    contract = probe.startup_vector_boundary_contract(binary, load_segment=0x1000)
    source = probe.service_instrumentation_source(contract, second=True)
    assert "cmp $18, %cx" in source and "cmp $19, %cx" in source
    assert ".byte 0x89, 0x1d, 0x8c, 0x45, 0x02" in source
    assert "mov %es:8, %ax" in source and "mov %es:10, %ax" in source
    assert "mov $12102, %cx" in source
    boot = APPEND_OFFSET - 0x14DD * 16
    patched, report = build_instrumented_mz(
        binary,
        contract,
        bytes(13000),
        boot + 500,
        heap=True,
        service_entry=boot + 100,
        second=True,
    )
    start = contract["startup"]["file_offset"]
    assert patched[start : start + 0x53] == binary[start : start + 0x53]
    assert patched[start + 0x56 : start + 0x5A] == bytes.fromhex("b435cd21")
    assert patched[start + 0x5D : start + 0x5F] == b"\x90\x90"
    assert patched[start + 0x5F : start + 0x64] == bytes.fromhex("83c704e2ef")
    assert patched[28:6000] == binary[28:6000]
    assert report["stop_before_startup_offset"] == 0x5A
    assert len(report["second_service_disclosure"]) == 4
    assert not report["bridge_disclosure"]
    assert any("twice" in text for text in report["disclosure"])
    allowed = {
        *range(2, 6),
        *range(10, 14),
        *range(20, 24),
        *range(start + 0x53, start + 0x56),
        *range(start + 0x5A, start + 0x5F),
    }
    assert all(c["file_offset"] in allowed for c in report["original_byte_changes"])


def test_instrumented_second_service_observation(tmp_path, original):
    """Oracle: one frozen second AH35/AL2 call, no second pointer save or retry."""
    if not all(shutil.which(tool) for tool in ("as", "ld", "nm", "dosbox")):
        pytest.skip("DOS probe tools unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "second"
    result = run_layout_probe(root, output, second=True)
    assert result["status"] == "scoped-second-vector-service-observation-pass"
    assert result["bytes_checked"] == 6010
    assert len(result["cases"]) == 1
    assert result["cases"][0]["second_service_executed"] is True
    assert result["cases"][0]["second_pointer_store_executed"] is False
    assert result["cases"][0]["trace_bytes"] == 12102
    assert not (output / "partial").exists()
    freeze = json.loads((output / "freeze.json").read_text())
    assert "pre/post second AH35/AL2" in freeze["scope"]
    assert "IVT2" in freeze["startup_composition"]
    assert freeze["service_registers"] == list(probe.SECOND_SERVICE_REGISTERS)
    for name, expected in freeze["method_hashes"].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected


def second_bridge_trace_fixture():
    """Oracle: independently composed second returned state/third input and second slot."""
    trace, contract = second_service_trace_fixture()
    before = list(struct.unpack_from("<19H", trace, 44))
    after = before.copy()
    for reg, value in {
        "AX": 0x351B,
        "CX": 17,
        "SI": 0x23C,
        "DI": 0x7AF8,
        "FLAGS": before[11] & ~0xCD5,
    }.items():
        after[probe.SECOND_SERVICE_REGISTERS.index(reg)] = value
    before_memory = trace[82:6092]
    after_memory = bytearray(before_memory)
    struct.pack_into(
        "<HH", after_memory, 0x7AF4 - probe.SERVICE_WINDOW[0], before[1], before[8]
    )
    return (
        trace[:6]
        + struct.pack("<19H", *before)
        + struct.pack("<19H", *after)
        + before_memory
        + after_memory
    ), contract


def test_second_bridge_checks_slot_and_third_input():
    """Oracle: complete endpoint shape, second result/slot and exact next bindings."""
    trace, contract = second_bridge_trace_fixture()
    result = probe.compare_service_trace(trace, contract, bridge=True, second=True)
    assert result["trace_bytes"] == 12102
    assert result["memory_bytes_checked"] == 6010
    assert result["protected_bytes_unchanged"] == 6006
    assert result["vector0_result"] == [0xF000, 0x1234]
    assert result["vector2_result"] == [0xE000, 0x4321]
    assert result["next_service_ax"] == 0x351B
    assert result["second_pointer_store_executed"] is True
    assert result["third_service_executed"] is False
    assert result["service_contract_established"] is False


@pytest.mark.parametrize("reg", probe.SECOND_SERVICE_REGISTERS)
def test_second_bridge_rejects_each_changed_next_register(reg):
    """Oracle: no unexplained next-register, IVT or FLAGS change accepted."""
    trace, contract = second_bridge_trace_fixture()
    trace = bytearray(trace)
    trace[44 + 2 * probe.SECOND_SERVICE_REGISTERS.index(reg)] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract, bridge=True, second=True)


@pytest.mark.parametrize(
    "cell",
    [
        0x63D8,
        0x63FE,
        0x6400,
        0x6426,
        0x7AF0,
        0x7AF3,
        0x7AF4,
        0x7AF5,
        0x7AF6,
        0x7AF7,
        0x7AF8,
        0x7B3C,
        0x7B51,
    ],
)
@pytest.mark.parametrize("both", [False, True])
def test_second_bridge_rejects_bad_slot_or_protected_state(cell, both):
    """Oracle: second slot cannot mask other changes or identical invalid baseline."""
    trace, contract = second_bridge_trace_fixture()
    trace = bytearray(trace)
    for start in (82, 6092) if both else (6092,):
        trace[start + cell - probe.SERVICE_WINDOW[0]] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract, bridge=True, second=True)


@pytest.mark.parametrize("flags", [0x202, 0xED7, 0x7202, 0x7ED7])
def test_second_bridge_accounts_for_add_flags_and_service_df(flags):
    """Oracle: no incoming DF/condition-code preservation assumption across second service."""
    trace, contract = second_bridge_trace_fixture()
    trace = bytearray(trace)
    struct.pack_into("<H", trace, 28, flags)
    struct.pack_into("<H", trace, 66, flags & ~0xCD5)
    probe.compare_service_trace(bytes(trace), contract, bridge=True, second=True)


def test_second_bridge_does_not_require_returned_ax_low_byte():
    """Oracle: second returned AX is unconstrained; next LODSB replaces AL only."""
    trace, contract = second_bridge_trace_fixture()
    trace = bytearray(trace)
    struct.pack_into("<H", trace, 6, 0xABCD)
    struct.pack_into("<H", trace, 44, 0xAB1B)
    probe.compare_service_trace(bytes(trace), contract, bridge=True, second=True)


def test_second_bridge_patch_and_source_preserve_original_loop(original):
    """Oracle: original calls/ADD/LOOP intact, both displaced stores disclosed, third stop."""
    binary, _ = original
    contract = probe.startup_vector_boundary_contract(binary, load_segment=0x1000)
    source = probe.service_instrumentation_source(contract, bridge=True, second=True)
    assert "cmp $17, %cx" in source and "cmp $18, %cx" in source
    assert source.count(".byte 0x89, 0x1d, 0x8c, 0x45, 0x02") == 1
    assert "third_input:" in source and "second_return:" in source
    assert "jmp 0x5f" in source
    boot = APPEND_OFFSET - 0x14DD * 16
    patched, report = build_instrumented_mz(
        binary,
        contract,
        bytes(13000),
        boot + 500,
        heap=True,
        service_entry=boot + 100,
        bridge=True,
        second=True,
    )
    start = contract["startup"]["file_offset"]
    assert patched[start : start + 0x53] == binary[start : start + 0x53]
    assert patched[start + 0x56 : start + 0x5A] == bytes.fromhex("b435cd21")
    assert patched[start + 0x5D : start + 0x5F] == b"\x90\x90"
    assert patched[start + 0x5F : start + 0x64] == bytes.fromhex("83c704e2ef")
    assert patched[28:6000] == binary[28:6000]
    assert report["stop_before_startup_offset"] == 0x56
    assert not report["second_service_disclosure"] and not report["bridge_disclosure"]
    assert len(report["second_bridge_disclosure"]) == 4
    allowed = {
        *range(2, 6),
        *range(10, 14),
        *range(20, 24),
        *range(start + 0x53, start + 0x56),
        *range(start + 0x5A, start + 0x5F),
    }
    assert all(c["file_offset"] in allowed for c in report["original_byte_changes"])


def test_instrumented_second_vector_bridge(tmp_path, original):
    """Oracle: one frozen second pointer-save bridge, stop before third service, no retry."""
    if not all(shutil.which(tool) for tool in ("as", "ld", "nm", "dosbox")):
        pytest.skip("DOS probe tools unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "second-bridge"
    result = run_layout_probe(root, output, bridge=True, second=True)
    assert result["status"] == "scoped-second-vector-save-bridge-pass"
    assert result["bytes_checked"] == 6010
    assert len(result["cases"]) == 1
    case = result["cases"][0]
    assert case["next_service_ax"] == 0x351B
    assert case["third_service_executed"] is False
    assert case["second_pointer_store_executed"] is True
    assert case["trace_bytes"] == 12102
    assert case["protected_bytes_unchanged"] == 6006
    freeze = json.loads((output / "freeze.json").read_text())
    assert "second return005a to third-input" in freeze["scope"]
    assert "NOT service input" in freeze["startup_composition"]
    assert freeze["service_registers"] == list(probe.SECOND_SERVICE_REGISTERS)
    assert not (output / "partial").exists()
    for name, expected in freeze["method_hashes"].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected


def third_service_trace_fixture():
    """Oracle: independent third-input/return record with three distinct vector pointers."""
    trace, contract = second_bridge_trace_fixture()
    before = list(struct.unpack_from("<19H", trace, 44)) + [0x6543, 0xD000]
    after = before.copy()
    after[1], after[8] = 0x6543, 0xD000
    memory = trace[6092:]
    return (
        trace[:6]
        + struct.pack("<21H", *before)
        + struct.pack("<21H", *after)
        + memory
        + memory
    ), contract


def test_third_service_checks_ivt1b_and_both_slots():
    """Oracle: third result matches IVT1B, not earlier vectors; full window unchanged."""
    trace, contract = third_service_trace_fixture()
    result = probe.compare_service_trace(trace, contract, third=True)
    assert result["trace_bytes"] == 12110
    assert result["protected_bytes_unchanged"] == 6010
    assert result["vector1b_result"] == [0xD000, 0x6543]
    assert result["vector2_result"] == [0xE000, 0x4321]
    assert result["saved_slot_bytes_checked"] == 8
    assert result["third_service_executed"] is True
    assert result["third_pointer_store_executed"] is False
    assert result["service_contract_established"] is False


@pytest.mark.parametrize(
    "reg",
    [
        "CX",
        "SI",
        "DI",
        "DS",
        "ES",
        "SS",
        "SP",
        "BX",
        "PSP_END",
        "VECTOR0_OFF",
        "VECTOR0_SEG",
        "VECTOR2_OFF",
        "VECTOR2_SEG",
        "IVT21_OFF",
        "IVT21_SEG",
        "VECTOR1B_OFF",
        "VECTOR1B_SEG",
    ],
)
def test_third_service_rejects_bad_return_register_or_ivt(reg):
    """Oracle: wrong vector result or changed loop/IVT bindings must fail."""
    trace, contract = third_service_trace_fixture()
    trace = bytearray(trace)
    trace[48 + 2 * probe.THIRD_SERVICE_REGISTERS.index(reg)] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract, third=True)


@pytest.mark.parametrize("reg", ["AX", "BX", "CX", "SI", "DI", "DS", "ES", "SS", "SP"])
def test_third_service_rejects_bad_input_binding(reg):
    """Oracle: earlier-call context cannot substitute for third call inputs."""
    trace, contract = third_service_trace_fixture()
    trace = bytearray(trace)
    trace[6 + 2 * probe.THIRD_SERVICE_REGISTERS.index(reg)] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract, third=True)


@pytest.mark.parametrize(
    "cell",
    [
        0x63D8,
        0x63FE,
        0x6400,
        0x6426,
        0x7AEF,
        0x7AF0,
        0x7AF3,
        0x7AF4,
        0x7AF5,
        0x7AF6,
        0x7AF7,
        0x7AF8,
        0x7B3C,
        0x7B51,
    ],
)
@pytest.mark.parametrize("both", [False, True])
def test_third_service_rejects_changed_or_invalid_unchanged_memory(cell, both):
    """Oracle: both saved slots and untouched third slot/bounds validated, no masking."""
    trace, contract = third_service_trace_fixture()
    trace = bytearray(trace)
    for start in (90, 6100) if both else (6100,):
        trace[start + cell - probe.SERVICE_WINDOW[0]] ^= 1
    with pytest.raises(ValueError):
        probe.compare_service_trace(bytes(trace), contract, third=True)


@pytest.mark.parametrize("size", [0, 12094, 12102, 12109, 12111])
def test_third_service_requires_exact_record(size):
    """Oracle: earlier snapshots cannot masquerade as IVT1B measurement."""
    with pytest.raises(ValueError, match="length"):
        probe.compare_service_trace(bytes(size), {}, third=True)


def test_third_service_does_not_invent_residue_preservation():
    """Oracle: beforeAH and returnedAX/DX/BP/FLAGS are reported, not required preserved."""
    trace, contract = third_service_trace_fixture()
    trace = bytearray(trace)
    struct.pack_into("<H", trace, 6, 0xAB1B)
    for reg, value in {
        "AX": 0x9876,
        "DX": 0x5432,
        "BP": 0x1234,
        "FLAGS": 0x602,
    }.items():
        struct.pack_into(
            "<H", trace, 48 + 2 * probe.THIRD_SERVICE_REGISTERS.index(reg), value
        )
    probe.compare_service_trace(bytes(trace), contract, third=True)


@pytest.mark.parametrize("other", ["bridge", "second"])
def test_third_service_conflicts_fail_before_output(tmp_path, other):
    """Oracle: unsupported third-bridge/second combinations are explicit errors."""
    options = {"third": True, other: True}
    with pytest.raises(ValueError, match="cannot combine"):
        run_layout_probe(tmp_path, tmp_path / "out", **options)
    assert not (tmp_path / "out").exists()
    with pytest.raises(ValueError, match="cannot combine"):
        probe.service_instrumentation_source({}, **options)
    with pytest.raises(ValueError, match="cannot combine"):
        probe.compare_service_trace(b"", {}, **options)


def test_third_service_patch_and_snapshot_source(original):
    """Oracle: three original services, two displaced saves, IVT1B snapshots and third stop."""
    binary, _ = original
    contract = probe.startup_vector_boundary_contract(binary, load_segment=0x1000)
    source = probe.service_instrumentation_source(contract, third=True)
    assert source.count("cmp $17, %cx") == 2
    assert "mov %es:0x6c, %ax" in source and "mov %es:0x6e, %ax" in source
    assert "mov $12110, %cx" in source
    boot = APPEND_OFFSET - 0x14DD * 16
    patched, report = build_instrumented_mz(
        binary,
        contract,
        bytes(13000),
        boot + 500,
        heap=True,
        service_entry=boot + 100,
        third=True,
    )
    start = contract["startup"]["file_offset"]
    assert patched[start : start + 0x53] == binary[start : start + 0x53]
    assert patched[start + 0x56 : start + 0x5A] == bytes.fromhex("b435cd21")
    assert patched[start + 0x5D : start + 0x5F] == b"\x90\x90"
    assert patched[start + 0x5F : start + 0x64] == bytes.fromhex("83c704e2ef")
    assert patched[28:6000] == binary[28:6000]
    assert report["stop_before_startup_offset"] == 0x5A
    assert len(report["third_service_disclosure"]) == 4
    assert any("three times" in text for text in report["disclosure"])
    allowed = {
        *range(2, 6),
        *range(10, 14),
        *range(20, 24),
        *range(start + 0x53, start + 0x56),
        *range(start + 0x5A, start + 0x5F),
    }
    assert all(c["file_offset"] in allowed for c in report["original_byte_changes"])


def test_instrumented_third_service_observation(tmp_path, original):
    """Oracle: one frozen third AH35/AL1B case, no third pointer save or retry."""
    if not all(shutil.which(tool) for tool in ("as", "ld", "nm", "dosbox")):
        pytest.skip("DOS probe tools unavailable")
    root = pathlib.Path(__file__).resolve().parents[1]
    output = tmp_path / "third"
    result = run_layout_probe(root, output, third=True)
    assert result["status"] == "scoped-third-vector-service-observation-pass"
    assert result["bytes_checked"] == 6010
    assert len(result["cases"]) == 1
    assert result["cases"][0]["third_service_executed"] is True
    assert result["cases"][0]["third_pointer_store_executed"] is False
    assert result["cases"][0]["trace_bytes"] == 12110
    freeze = json.loads((output / "freeze.json").read_text())
    assert "pre/post third AH35/AL1b" in freeze["scope"]
    assert "IVT1B" in freeze["startup_composition"]
    assert freeze["service_registers"] == list(probe.THIRD_SERVICE_REGISTERS)
    assert not (output / "partial").exists()
    for name, expected in freeze["method_hashes"].items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected


def vector_batch_fixture():
    """Oracle: independent19 distinct pointers and complete predicted save footprint."""
    trace, contract = service_trace_fixture()
    before = dict(
        zip(probe.SERVICE_REGISTERS, struct.unpack_from("<17H", trace, 6), strict=True)
    )
    for number in probe.VECTOR_NUMBERS[1:]:
        before[f"VECTOR{number:02X}_OFF"] = 0x100 + number * 3
        before[f"VECTOR{number:02X}_SEG"] = 0xD000 + number
    after = {
        **before,
        "CX": 0,
        "SI": 0x24C,
        "DI": 0x7B3C,
        "BX": before["VECTOR75_OFF"],
        "ES": before["VECTOR75_SEG"],
    }
    memory = trace[74:6084]
    final = bytearray(memory)
    for index, number in enumerate(probe.VECTOR_NUMBERS):
        prefix = "VECTOR0" if number == 0 else f"VECTOR{number:02X}"
        struct.pack_into(
            "<HH",
            final,
            0x7AF0 + 4 * index - probe.SERVICE_WINDOW[0],
            before[f"{prefix}_OFF"],
            before[f"{prefix}_SEG"],
        )
    return (
        trace[:6]
        + b"".join(
            struct.pack(
                f"<{len(probe.BATCH_REGISTERS)}H",
                *(record[key] for key in probe.BATCH_REGISTERS),
            )
            for record in (before, after)
        )
        + memory
        + final
    ), contract


def test_vector_batch_all_slots_and_scope():
    """Oracle:19 saved pointers, no whole-program or allocator-entry promotion."""
    trace, contract = vector_batch_fixture()
    result = probe.compare_vector_batch(trace, contract)
    assert result["queries_checked"] == 19
    assert result["saved_pointer_bytes"] == 76
    assert result["other_protected_bytes_unchanged"] == 5934
    assert result["allocator_entry_state_established"] is False
    assert result["service_contract_established"] is False


@pytest.mark.parametrize("slot", range(19))
def test_vector_batch_rejects_each_wrong_save(slot):
    """Oracle: mutation of any saved slot fails, not just first/last."""
    trace, contract = vector_batch_fixture()
    trace = bytearray(trace)
    trace[
        6
        + 4 * len(probe.BATCH_REGISTERS)
        + 6010
        + 0x7AF0
        - probe.SERVICE_WINDOW[0]
        + slot * 4
    ] ^= 1
    with pytest.raises(ValueError, match="pointer saves"):
        probe.compare_vector_batch(bytes(trace), contract)


@pytest.mark.parametrize("offset", [0, 2, 4, 6, 10, 14, 16, 20, 24, 26, 40, -1])
def test_vector_batch_rejects_bad_endpoint(offset):
    """Oracle: loader, baseline, IVT and guard mutations fail."""
    trace, contract = vector_batch_fixture()
    trace = bytearray(trace)
    trace[offset] ^= 1
    with pytest.raises(ValueError):
        probe.compare_vector_batch(bytes(trace), contract)


@pytest.mark.parametrize("delta", [-1, 1])
def test_vector_batch_exact_shape(delta):
    """Oracle: partial and trailing records fail."""
    trace, contract = vector_batch_fixture()
    with pytest.raises(ValueError, match="length"):
        probe.compare_vector_batch(trace[:-1] if delta < 0 else trace + b"\0", contract)


def test_vector_batch_build_preserves_entire_loop(tmp_path, original, monkeypatch):
    """Oracle: intercepted worker; assembly/build reviewed without original execution."""
    binary, _ = original
    calls = []

    def blocked_worker(directory):
        """Oracle: no DOS execution during preflight."""
        calls.append(directory)
        raise RuntimeError("no original execution")

    monkeypatch.setattr(probe, "run_dosbox", blocked_worker)
    with pytest.raises(RuntimeError, match="no original execution"):
        probe.run_vector_batch(
            pathlib.Path(__file__).resolve().parents[1], tmp_path / "batch"
        )
    assert len(calls) == 1
    image = (tmp_path / "batch/PROBE.COM").read_bytes()
    contract = probe.startup_vector_boundary_contract(binary, load_segment=0x1000)
    start = contract["startup"]["file_offset"]
    assert image[start + 0x56 : start + 0x64] == binary[start + 0x56 : start + 0x64]
    patches = json.loads((tmp_path / "batch/patches.json").read_text())
    assert patches["stop_before_startup_offset"] == 0x64
    assert (tmp_path / "batch/freeze.json").is_file()


def test_vector_batch_missing_input_skips(tmp_path, monkeypatch):
    """Oracle: absent BYOD skips without creating an experiment."""
    monkeypatch.setattr(pathlib.Path, "is_file", lambda self: False)
    assert probe.run_vector_batch(tmp_path, tmp_path / "batch")["status"] == "skipped"
    assert not (tmp_path / "batch").exists()
