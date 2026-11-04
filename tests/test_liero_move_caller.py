"""Owned caller-slice contract and complete typed composition regressions."""

import shutil
import struct
import subprocess

import pytest

from tools import liero_move_caller as caller
from tools import liero_source_trial as trial


def test_packed_retained_pointer_and_original_relocations(monkeypatch):
    """Oracle: exact retained4-byte argument, actual MZ relocations and original callees."""
    if not (trial.ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("BYOD unavailable")
    contract = caller.packed_caller_contract(trial.ROOT)
    assert contract["relocation_offsets"] == [10, 22]
    assert contract["source"] == "SS:[BP-0x50]"
    assert contract["destination"] == "SS:[BP-0x30]"
    assert contract["initializer"]["cleanup"] == 2
    assert contract["copier"]["cleanup"] == 10
    assert (
        "%es:0x92df" in caller.packed_harness()
        and "%es:0x92eb" in caller.packed_harness()
    )
    monkeypatch.setattr(caller, "PACKED_CALLER", b"\x90" + caller.PACKED_CALLER[1:])
    with pytest.raises(ValueError, match="bytes/relocations"):
        caller.packed_caller_contract(trial.ROOT)


@pytest.mark.parametrize("native", [False, True])
def test_packed_caller_full_state_mutants(native):
    """Oracle: entire frame/arena, initializer/source/destination/local, far-stack cleanup."""
    inputs = caller.packed_cases("training")
    trace = b"".join(
        caller.packed_expected(row, 0x2000, native=native) for row in inputs
    )
    assert caller.packed_compare(inputs, trace, native=native)["matches"] == 12
    assert inputs != caller.packed_cases("terminal")
    for offset in (0, 2, 8, 10, 14, 16, 32 + 0x3B0, 32 + 0x3D0, 32 + 0x3FC):
        mutant = bytearray(trace)
        mutant[offset] ^= 1
        assert (
            caller.packed_compare(inputs, bytes(mutant), native=native)["status"]
            == "failed"
        )
    with pytest.raises(ValueError, match="partial"):
        caller.packed_compare(inputs, trace[:-1], native=native)


@pytest.mark.parametrize("mutant", [False, True])
def test_packed_host_caller_binds_actual_pointers(tmp_path, mutant):
    """Oracle: supplied test interpretation compiles; original caller binding is not incoming SI."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    hypothesis = {
        "source_start": "high_byte",
        "destination_start": "zero",
        "count": "low_byte",
        "step": 1,
        "access_order": "copy_then_step",
        "zero_count": "no_access",
        "evidence": trial.PACKED_BINDINGS,
    }
    source = trial.compose_residual(
        trial.lower_packed_interpretation(hypothesis), "FUN_24dd_4141"
    )
    (tmp_path / "candidate.inc").write_text(source)
    program = caller.packed_program()
    if mutant:
        program = program.replace(
            "RegisterSI := input[0] - $50", "RegisterSI := input[1]"
        )
    (tmp_path / "probe.pas").write_text(program)
    compilation = subprocess.run(
        [
            "fpc",
            "-Mtp",
            "-Cr",
            f"-Fu{trial.ROOT / 'targets/liero/src'}",
            "-FU.",
            "probe.pas",
        ],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert compilation.returncode == 0, compilation.stdout + compilation.stderr
    inputs = caller.packed_cases("training")
    (tmp_path / "CASES.BIN").write_bytes(b"".join(inputs))
    execution = subprocess.run(
        [str(tmp_path / "probe")],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert execution.returncode == 0
    result = caller.packed_compare(
        inputs, (tmp_path / "PASCAL.BIN").read_bytes(), native=False
    )
    assert result["status"] == ("failed" if mutant else "passed")


@pytest.mark.parametrize("suite", ["training", "terminal"])
def test_caller_full_memory_and_register_contract(suite):
    """Oracle: independent original-row contract, full-state mutations fail."""
    inputs = caller.cases(suite)
    trace = b"".join(caller.expected(data, 0x2000, native=True) for data in inputs)
    assert caller.compare(inputs, trace, native=True)["matches"] == 12
    assert caller.cases("training") != caller.cases("terminal")
    for offset in (0, 2, 8, 10, 16, 32 + 0x26):
        mutant = bytearray(trace)
        mutant[offset] ^= 1
        assert caller.compare(inputs, bytes(mutant), native=True)["status"] == "failed"
    with pytest.raises(ValueError, match="partial"):
        caller.compare(inputs, trace[:-1], native=True)


def test_caller_relocation_and_argument_origins(monkeypatch):
    """Oracle: actual BYOD bytes, not listing CALLF text."""
    if not (trial.ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("BYOD unavailable")
    contract = caller.caller_contract(trial.ROOT)
    assert contract["relocation_offsets"] == [51]
    assert contract["count"] == 3
    assert "66d8" in contract["source"] and "5826" in contract["destination"]
    assert contract["call_target"] == "load+14dd:48e1"
    monkeypatch.setattr(caller, "CALLER", b"\x90" + caller.CALLER[1:])
    with pytest.raises(ValueError, match="caller bytes"):
        caller.caller_contract(trial.ROOT)


@pytest.mark.parametrize("mutant", [False, True])
def test_typed_caller_uses_actual_arguments_not_incoming_si_di(tmp_path, mutant):
    """Oracle: supplied checked memory actions and compiler execution of composed caller."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    hypothesis = {
        "condition": "source_lt_destination",
        "zero_count": "no_access",
        "forward_start": "zero",
        "backward_start": "count_minus_one",
        "forward_step": 1,
        "backward_step": -1,
        "access_order": "copy_then_step",
        "repeat": "count_times",
    }
    source, program = caller.program(
        trial.compose_residual(trial.lower_interpretation(hypothesis))
    )
    if mutant:
        source = source.replace(
            "sourceOffset := $66d8 + 3 * inputArgument; destinationOffset := $5826 + 3 * inputLookup;",
            "sourceOffset := RegisterSI; destinationOffset := RegisterDI;",
        )
    (tmp_path / "candidate.inc").write_text(source)
    (tmp_path / "probe.pas").write_text(program)
    build = subprocess.run(
        [
            "fpc",
            "-Mtp",
            "-Cr",
            f"-Fu{trial.ROOT / 'targets/liero/src'}",
            "-FU.",
            "probe.pas",
        ],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    inputs = caller.cases("training")
    (tmp_path / "CASES.BIN").write_bytes(b"".join(inputs))
    execution = subprocess.run(
        [str(tmp_path / "probe")],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert execution.returncode == 0, execution.stdout + execution.stderr
    assessment = caller.compare(
        inputs, (tmp_path / "PASCAL.BIN").read_bytes(), native=False
    )
    assert assessment["status"] == ("failed" if mutant else "passed")


def test_caller_scope_and_exact_relocated_harness():
    """Oracle: bounded input/protected ranges and unchanged original instruction payload."""
    data = bytearray(caller.cases("training")[0])
    struct.pack_into("<H", data, 0, 256)
    with pytest.raises(ValueError, match="outside frozen"):
        caller.expected(bytes(data), 0x2000, native=False)
    with pytest.raises(ValueError, match="record or segment"):
        caller.expected(bytes(data[:-1]), 0x2000, native=False)
    text = caller.harness()
    assert "lcall *caller_pointer" in text
    assert "mov %ax, %es:0x62c" in text
    assert "mov $0x1111, %si" in text and "mov $0x2222, %di" in text
    assert "mov $54, %cx" in text
    assert "sub $18, %ax" in text


def test_saved_caller_trace_replay_and_tamper_rejection(tmp_path):
    """Oracle: immutable saved synthetic rows; replay needs no original execution."""
    if not (trial.ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("BYOD unavailable")
    result = {}
    frozen = {"contract": caller.caller_contract(trial.ROOT), "corpora": {}}
    (tmp_path / "candidate").mkdir()
    (tmp_path / "candidate/candidate.inc").write_text("synthetic test source")
    frozen["candidate_sha256"] = trial.pilot.digest(
        tmp_path / "candidate/candidate.inc"
    )
    for suite in ("training", "terminal"):
        inputs = caller.cases(suite)
        payload = b"".join(inputs)
        frozen["corpora"][suite] = caller.hashlib.sha256(payload).hexdigest()
        for origin, native in (("original", True), ("host", False)):
            directory = tmp_path / f"{origin}-{suite}"
            directory.mkdir()
            (directory / "CASES.BIN").write_bytes(payload)
            trace = b"".join(
                caller.expected(row, 0x2000, native=native) for row in inputs
            )
            (directory / ("TRACE.BIN" if native else "PASCAL.BIN")).write_bytes(trace)
        result[suite] = caller.compare(
            inputs, (tmp_path / f"host-{suite}/PASCAL.BIN").read_bytes(), native=False
        )
    trial.pilot.save(tmp_path / "freeze.json", frozen)
    trial.pilot.save(tmp_path / "result.json", result)
    trial.pilot.save(
        tmp_path / "artifacts.json",
        {
            str(p.relative_to(tmp_path)): trial.pilot.digest(p)
            for p in tmp_path.rglob("*")
            if p.is_file()
        },
    )
    assert caller.replay(trial.ROOT, tmp_path) == result
    (tmp_path / "host-terminal/PASCAL.BIN").write_bytes(b"")
    with pytest.raises(ValueError, match="artifact changed"):
        caller.replay(trial.ROOT, tmp_path)


@pytest.mark.parametrize("prologue", [False, True])
def test_caller_runner_freezes_source_before_single_terminal(
    tmp_path, monkeypatch, prologue
):
    """Oracle: controlled original observations and actual FPC composition; no live recovery."""
    if (
        not shutil.which("fpc")
        or not (trial.ROOT / "extracted/liero/LIERO.EXE").is_file()
    ):
        pytest.skip("FPC/BYOD unavailable")
    predecessor = tmp_path / "prior"
    predecessor.mkdir()
    (predecessor / "artifacts.json").write_text("{}")
    hypothesis = {
        "condition": "source_lt_destination",
        "zero_count": "no_access",
        "forward_start": "zero",
        "backward_start": "count_minus_one",
        "forward_step": 1,
        "backward_step": -1,
        "access_order": "copy_then_step",
        "repeat": "count_times",
    }
    monkeypatch.setattr(
        trial,
        "validate_artifacts",
        lambda *a, **k: {
            "routines": {
                "FUN_24dd_48e1": {
                    "interpretation": {"status": "passed", "selected": hypothesis}
                }
            }
        },
    )
    suites = []
    output = tmp_path / "caller"

    def dosbox(directory):
        """Oracle: known original fixture rows; assert training-only selection before terminal."""
        suite = directory.name.removeprefix("original-")
        suites.append(suite)
        if suite == "terminal":
            saved = caller.json.loads((output / "selection.json").read_text())
            assert saved["training"]["status"] == "passed"
            assert "terminal" not in saved
        trace = b"".join(
            caller.expected(row, 0x2000, native=True, prologue=prologue)
            for row in caller.cases(suite, prologue=prologue)
        )
        (directory / "TRACE.BIN").write_bytes(trace)

    monkeypatch.setattr(trial, "run_dosbox", dosbox)
    result = caller.run(trial.ROOT, output, predecessor, prologue=prologue)
    assert suites == ["training", "terminal"]
    assert result["training"]["matches"] == result["terminal"]["matches"] == 12
    frozen = caller.json.loads((output / "freeze.json").read_text())
    assert frozen["method_hashes"]
    assert frozen["host_program_sha256"]
    assert caller.replay(trial.ROOT, output) == result


@pytest.mark.parametrize(
    "requested,sp,minimum,status,reason",
    [
        (6, 0xEFE4, 0xEDDE, "returns", None),
        (6, 0xEFE4, 0xEDDF, "error-dispatch", "below-minimum"),
        (0xFDFF, 0xFFFF, 0, "error-dispatch", "sub-no-borrow"),
        (0xFE00, 0xFFFF, 0, "error-dispatch", "add-carry"),
        (6, 0x206, 0, "error-dispatch", "sub-no-borrow"),
        (6, 0x207, 1, "returns", None),
    ],
)
def test_original_stack_check_unsigned_boundaries(
    requested, sp, minimum, status, reason
):
    """Oracle: original exact ADD/SUB/NEG/CMP constraints; dispatch is not accepted return."""
    result = caller.stack_check_contract(caller.STACK_CHECK, requested, sp, minimum)
    assert (result["status"], result["reason"]) == (status, reason)
    assert result["failure_target"] == "24dd:010f"
    assert result["failure_ax"] == 202
    with pytest.raises(ValueError, match="unsupported"):
        caller.stack_check_contract(
            b"\x90" + caller.STACK_CHECK[1:], requested, sp, minimum
        )


def test_prologue_composition_establishes_frame_not_injected_bp(tmp_path):
    """Oracle: actual FPC composition with checked stack-success premises and full-state rows."""
    if not shutil.which("fpc"):
        pytest.skip("FPC unavailable")
    contract = caller.caller_contract(trial.ROOT, prologue=True)
    assert contract["stack_check"]["status"] == "returns"
    assert contract["copy_entry_sp"] == 0xEFD6
    hypothesis = {
        "condition": "source_lt_destination",
        "zero_count": "no_access",
        "forward_start": "zero",
        "backward_start": "count_minus_one",
        "forward_step": 1,
        "backward_step": -1,
        "access_order": "copy_then_step",
        "repeat": "count_times",
    }
    source, program = caller.program(
        trial.compose_residual(trial.lower_interpretation(hypothesis)), prologue=True
    )
    (tmp_path / "candidate.inc").write_text(source)
    (tmp_path / "probe.pas").write_text(program)
    build = subprocess.run(
        [
            "fpc",
            "-Mtp",
            "-Cr",
            f"-Fu{trial.ROOT / 'targets/liero/src'}",
            "-FU.",
            "probe.pas",
        ],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    inputs = caller.cases("training", prologue=True)
    (tmp_path / "CASES.BIN").write_bytes(b"".join(inputs))
    execution = subprocess.run(
        [str(tmp_path / "probe")],
        cwd=tmp_path,
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert execution.returncode == 0
    assert (
        caller.compare(
            inputs, (tmp_path / "PASCAL.BIN").read_bytes(), native=False, prologue=True
        )["matches"]
        == 12
    )
    invalid = bytearray(inputs[0])
    struct.pack_into("<H", invalid, 8 + 0x640E - caller.BASE, 0xEDE1)
    with pytest.raises(ValueError, match="unresolved error"):
        caller.expected(bytes(invalid), 0x2000, native=False, prologue=True)
    text = caller.harness(prologue=True)
    assert "mov %ax, %es:0x5f4" in text
    assert "caller_pointer: .word 0x500" in text
    assert "mov $24, %cx" in text
    assert "sub $24, %ax" in text
    assert "0xe8,0xde,0x00" in text
    assert "0x89,0xec,0x5d,0xc2,0x02,0x00" in text
    assert text.index("mov $stack_bytes, %si") > text.index("mov $0x48e1, %di")
