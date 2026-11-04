import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_allocator_entry_probe as probe

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture
def inputs():
    """Oracle: current BYOD bytes and actual MZ relocations, never exported listing addresses."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    return probe.entry_contract(ROOT)


def synthetic_trace(contract):
    """Oracle: synthetic mechanism fixture, not evidence of actual startup execution."""
    startup = contract["startup"]
    base = 0x2000
    ss = base + startup["mz"]["initial_ss"] - startup["load_segment"]
    ds = base + startup["startup"]["relocated_ds"] - startup["load_segment"]
    cs = base + startup["startup"]["relocated_cs"] - startup["load_segment"]
    initial_sp = startup["mz"]["initial_sp"]
    heap_segment = base + startup["mz"]["minimum_allocation_bytes"] // 16
    frontier = heap_segment + 4000
    psp_end = 0x9000
    memory = bytearray([0xA5] * (probe.SERVICE_WINDOW[1] - probe.SERVICE_WINDOW[0]))
    for cell, value in (
        (0x63EE, 0),
        (0x63F0, heap_segment),
        (0x63F6, 0),
        (0x63F8, heap_segment),
        (0x63F2, 0),
        (0x63F4, psp_end),
        (0x63FE, 0xD6),
        (0x6400, cs),
    ):
        struct.pack_into("<H", memory, cell - probe.SERVICE_WINDOW[0], value)
    after = bytearray(memory)
    for cell, value in (
        (0x63EE, 0),
        (0x63F0, frontier),
        (0x63F6, 0),
        (0x63F8, frontier),
        (0x6684, 0),
        (0x6686, heap_segment),
        (0x7B3C, 64000),
    ):
        struct.pack_into("<H", after, cell - probe.SERVICE_WINDOW[0], value)
    before_regs = dict.fromkeys(probe.REGISTERS, 0)
    before_regs.update(DS=ds, SS=ss, SP=initial_sp - 64, BP=initial_sp - 32)
    after_regs = {
        **before_regs,
        "SP": before_regs["SP"] + 6,
        "AX": 0,
        "DX": heap_segment,
    }
    trace = bytearray(struct.pack("<4H", ss, initial_sp, base - 16, psp_end))
    for registers, stack, data in (
        (before_regs, [0xE513, base, 64000, 0, 0, 0], memory),
        (after_regs, [0] * 6, after),
    ):
        trace.extend(
            struct.pack("<12H", *(registers[name] for name in probe.REGISTERS))
        )
        trace.extend(struct.pack("<6H", *stack))
        trace.extend(data)
    return bytes(trace)


def test_actual_caller_and_relocation_contract(inputs):
    """Oracle: request64000 unsigned, actual028a and original far-return e513."""
    _, contract, source = inputs
    assert contract["request"] == 64000
    assert contract["return_ip"] == 0xE513
    assert "LongWord(requestSize) + 7" in source
    assert contract["allocator"]["source_recovered"] is False
    assert "not all environments" in contract["unresolved"][0]


def test_mechanism_checks_complete_actual_entry_projection(inputs):
    """Oracle: synthetic successful callback/head/limit/stack/global mechanism only."""
    _, contract, _ = inputs
    measured = probe.compare_trace(synthetic_trace(contract), contract)
    assert measured["entry_stack"][:3] == [0xE513, 0x2000, 64000]
    assert measured["protected_global_bytes"] == 6010
    assert measured["expected_pascal_row"][2] == 0
    assert (
        measured["allocation_physical"][1] - measured["allocation_physical"][0] == 64000
    )


@pytest.mark.parametrize(
    "offset",
    [
        0,
        2,
        4,
        6,
        8 + 14,
        8 + 18,
        8 + 20,
        8 + 24,
        8 + 26,
        8 + 28,
        8 + 36 + 0x63F6 - 0x63D8,
        8 + 36 + 0x63FE - 0x63D8,
        8 + probe.SNAPSHOT_BYTES,
        8 + probe.SNAPSHOT_BYTES + 22,
        8 + probe.SNAPSHOT_BYTES + 36 + 0x6684 - 0x63D8,
        8 + probe.SNAPSHOT_BYTES + 36 + 0x6404 - 0x63D8,
    ],
)
def test_wrong_entry_callback_stack_or_global_residue_rejected(inputs, offset):
    """Oracle: explicit premise or complete residue rejection, not success-shaped fallback."""
    _, contract, _ = inputs
    trace = bytearray(synthetic_trace(contract))
    trace[offset] ^= 1
    with pytest.raises(ValueError):
        probe.compare_trace(bytes(trace), contract)


def test_partial_original_trace_rejected(inputs):
    """Oracle: no inference from a missing endpoint."""
    _, contract, _ = inputs
    with pytest.raises(ValueError, match="complete"):
        probe.compare_trace(synthetic_trace(contract)[:-1], contract)


def test_disclosed_patch_inventory_preserves_original_call_and_relocations(inputs):
    """Oracle: assembled state-preserving gateways; exact original caller call/stores are untouched."""
    binary, contract, _ = inputs
    startup = contract["startup"]
    relative_cs = startup["startup"]["relocated_cs"] - startup["load_segment"]
    boot = probe.APPEND_OFFSET - relative_cs * 16
    payload = bytes(512)
    labels = {"_start": boot, "before_entry": boot + 16, "collector": boot + 32}
    image, patches = probe.build_image(binary, contract, payload, labels)
    header = startup["mz"]["header_bytes"]
    assert image[header + 0xE50B : header + 0xE51A] == probe.MAIN_CALL
    assert image[header + 0xE51A : header + 0xE51E] == bytes.fromhex("909090ea")
    assert image[header + 0xE520 : header + 0xE522] == bytes.fromhex("dd14")
    assert patches["appended_module_range"] == [
        probe.APPEND_OFFSET,
        probe.APPEND_OFFSET + 512,
    ]
    assert (
        struct.unpack_from("<HH", image, 10)[0]
        < struct.unpack_from("<HH", binary, 10)[0]
    )
    with pytest.raises(ValueError):
        probe.build_image(binary, contract, bytes(64000), labels)


def test_actual_gateway_assembles_and_displaces_only_prologue(inputs, tmp_path):
    """Oracle: GNU assembly syntax/labels and exact patch shape, no DOS or original execution."""
    binary, contract, _ = inputs
    text = probe.instrumentation_source(contract)
    assert "ss rep movsb" in text
    assert "cmpw $0xe513" in text
    assert "jmp 0x28d" in text
    assert "    push %bp\n    mov %sp, %bp\n    jmp 0x28d" in text
    (tmp_path / "instrumentation.S").write_text(text)
    labels = probe.assemble(tmp_path, contract)
    image, _ = probe.build_image(
        binary, contract, (tmp_path / "payload.bin").read_bytes(), labels
    )
    assert len(image) > len(binary)


def test_missing_byod_skips_without_artifacts(tmp_path):
    """Oracle: missing original is a skip, never a successful observation."""
    assert probe.run(tmp_path, tmp_path / "run")["status"] == "skipped"
    assert not (tmp_path / "run").exists()


@pytest.mark.parametrize("failure", ["none", "original", "partial", "pascal", "drift"])
def test_one_original_one_candidate_no_retry(inputs, tmp_path, monkeypatch, failure):
    """Oracle: injected endpoint/candidate/execute failures, not measured original parity."""
    _, contract, _ = inputs
    calls = []

    def original(output):
        """Oracle: synthetic endpoint capture."""
        calls.append("original")
        if failure == "original":
            raise subprocess.TimeoutExpired(["dosbox"], 30)
        data = synthetic_trace(contract)
        (output / "TRACE.BIN").write_bytes(data[:-1] if failure == "partial" else data)

    def pascal(output, source, cases):
        """Oracle: injected projection with fixed output; no compiler."""
        calls.append("pascal")
        if failure == "drift":
            (output.parent / "freeze.json").write_text("{}")
        row = probe.compare_trace(synthetic_trace(contract), contract)[
            "expected_pascal_row"
        ]
        if failure == "pascal":
            row[0] = 1
        return [row]

    monkeypatch.setattr(probe, "run_dosbox", original)
    monkeypatch.setattr(probe.pilot, "allocator_candidate", pascal)
    output = tmp_path / "run"
    result = probe.run(ROOT, output)
    assert result["status"] == ("passed" if failure == "none" else "failed")
    assert calls.count("original") == 1
    assert calls.count("pascal") == int(failure in {"none", "pascal", "drift"})
    assert result["heldout_evaluations"] == 0
    assert result["source_promoted"] is False
    assert json.loads((output / "result.json").read_text()) == result


@pytest.mark.parametrize(
    "mutation",
    [
        "none",
        "trace",
        "stack",
        "Pascal",
        "image",
        "source",
        "method",
        "missing",
        "escape",
        "promotion",
    ],
)
def test_saved_actual_context_replay_and_rehashed_tampering(tmp_path, mutation):
    """Oracle: saved actual-context replay, no original/Pascal reexecution or repeated validation corpus."""
    saved = ROOT / "targets/liero/build/allocator-entry/actual-64000-v1"
    if (
        not (saved / "result.json").is_file()
        or not (ROOT / "extracted/liero/LIERO.EXE").is_file()
    ):
        pytest.skip("actual caller evidence/BYOD unavailable")
    copied = tmp_path / "copy"
    shutil.copytree(saved, copied)
    report = json.loads((copied / "result.json").read_text())
    paths = {
        "trace": ("TRACE.BIN", -1),
        "stack": ("TRACE.BIN", 8 + 24),
        "Pascal": ("pascal/PASCAL.BIN", -1),
        "image": ("PROBE.COM", -1),
        "source": ("candidate.inc", -1),
        "method": ("methods/liero_allocator_entry_probe.py", -1),
    }
    if mutation in paths:
        name, offset = paths[mutation]
        path = copied / name
        data = bytearray(path.read_bytes())
        data[offset] ^= 1
        path.write_bytes(data)
        report["artifact_hashes"][name] = probe.pilot.digest(path)
    elif mutation == "missing":
        report["artifact_hashes"].pop("TRACE.BIN")
    elif mutation == "escape":
        report["artifact_hashes"]["../outside"] = "0" * 64
    elif mutation == "promotion":
        report["routine_recovered"] = True
    probe.pilot.save(copied / "result.json", report)
    if mutation != "none":
        with pytest.raises(ValueError):
            probe.validate_report(ROOT, copied)
        return
    from engine.scoped_verification import allocator_entry_contract_graph

    assert probe.validate_report(ROOT, copied)["candidate_executions"] == 1
    graph = allocator_entry_contract_graph(ROOT / "targets/liero", copied)
    origin = graph.facts["allocator.buffer6684.origin"]
    assert origin.status == "oracle-verified"
    assert origin.value["valid_at_main_offset"] == 0xE51A
    assert origin.value["physical_bounds"] == [207984, 271984]
    assert (
        graph.facts["allocator.buffer6684.later_lifetime_and_aliasing"].status
        == "unknown"
    )
    assert (
        graph.facts["allocator.observed-entry.universal_entry_applicability"].status
        == "unknown"
    )
    assert (
        graph.facts["allocator.observed-entry.error_transfer010f"].status == "unknown"
    )
    assert not graph.propagate_same_value()
    assert not graph.conflicts()


def test_actual_context_graph_does_not_promote_universal_caller_contract(inputs):
    """Oracle: joined real context adds call-point evidence, not universal caller eligibility."""
    from engine.scoped_verification import allocator_contract_graph, load_scoped_checks

    empty = ROOT / "targets/liero/build/allocator-deduction/deductive-v1"
    actual = ROOT / "targets/liero/build/allocator-entry/actual-64000-v1"
    if not all((path / "result.json").is_file() for path in (empty, actual)):
        pytest.skip("combined frozen evidence unavailable")
    graph = allocator_contract_graph(ROOT / "targets/liero", empty)
    assert graph.facts["allocator.caller.applicability"].status == "unknown"
    assert (
        graph.facts["allocator.observed-entry.applicability"].status
        == "oracle-verified"
    )
    assert (
        graph.facts["allocator.buffer6684.later_lifetime_and_aliasing"].status
        == "unknown"
    )
    assert not graph.conflicts()
    checks = [
        entry
        for entry in load_scoped_checks(ROOT / "targets/liero")
        if entry["scope"] == "instrumented_actual_64000_caller_entry_return_projection"
    ]
    assert len(checks) == 1
    assert checks[0]["case_count"] == 1
    assert checks[0]["source_recovered"] is False
    assert checks[0]["automatic_discovery"] is False


@pytest.mark.parametrize("available", [True, False])
def test_entry_audit_invalid_or_missing_original_never_passes(
    tmp_path, monkeypatch, available
):
    """Oracle: audit distinguishes missing input from rejected/stale context evidence."""
    from engine.scoped_verification import _load_allocator_entry_checks

    target = tmp_path / "targets/liero"
    saved = target / "build/allocator-entry/saved"
    saved.mkdir(parents=True)
    (saved / "result.json").write_text("{}")
    if available:
        original = tmp_path / "extracted/liero/LIERO.EXE"
        original.parent.mkdir(parents=True)
        original.touch()

    def rejected(*args):
        """Oracle: injected replay rejection, not a bypassed byte check."""
        raise ValueError("changed method")

    monkeypatch.setattr(probe, "validate_report", rejected)
    checks = _load_allocator_entry_checks(target)
    assert checks[0]["status"] == ("invalid" if available else "skipped")


def test_error_prefix_preserves_caller_origin_and_correct_source_ds(inputs):
    """Oracle: actual010f jump bypasses CX/BX clearing and relocated MOV loads DS, not DX."""
    from engine.alternate_streams import _mz_relocation_locations
    from engine.scoped_verification import allocator_error_transfer_constraints

    binary, contract, _ = inputs
    startup = contract["startup"]
    begin = startup["startup"]["file_offset"] + 0x10F
    raw = binary[begin : begin + 26]
    relocations = {
        r - begin
        for r in _mz_relocation_locations(binary, startup["mz"]["header_bytes"])
        if begin - 1 <= r < begin + 26
    }
    facts = allocator_error_transfer_constraints(raw, relocations)
    assert facts["jump_target"] == 0x11A
    assert facts["jump_target"] != facts["skipped_entry"]["offset"]
    assert facts["source_ds"]["immediate_relative_to_load"] == 0x1971
    assert facts["writes"] == [
        {"ds_offset": 0x6406, "value": "entry AX (028a failure supplies203)"}
    ]
    assert facts["failure_path_executed"] is False
    assert facts["routine_recovered"] is False
    assembly = (ROOT / "targets/liero/asm/FUN_24dd_0116.s").read_text()
    assert binary[begin + 0x21 : begin + 0x23] == bytes.fromhex("8ec0")
    assert "24dd:011d  MOV DS,DX" in assembly
    assert "24dd:0130  MOV ES,AX" in assembly
    for offset in range(len(raw)):
        mutant = bytearray(raw)
        mutant[offset] ^= 1
        with pytest.raises(ValueError):
            allocator_error_transfer_constraints(bytes(mutant), relocations)
    for incorrect in (set(), {5}, {12, 14}):
        with pytest.raises(ValueError):
            allocator_error_transfer_constraints(raw, incorrect)
