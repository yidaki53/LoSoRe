import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_cleanup_dispatch_probe as probe

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture
def contract():
    """Oracle: actual original29-byte dispatch, not a guessed callback contract."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    return probe.checked_contract(ROOT)


def test_dispatch_static_contract(contract):
    """Oracle: null branch, clear-before-transfer and016e far continuation."""
    assert len(probe.RAW) == 29
    assert contract["null_target"] == 0x18B
    assert 0x176 + 2 + int.from_bytes(probe.RAW[9:10], "little", signed=True) == 0x18B
    assert probe.RAW[-8:] == bytes.fromhex("b86e010e500653cb")
    assert contract["source_recovered"] is False
    assert len(probe.CASES) == len(set(probe.CASES)) == 8
    assert probe.target(2, 0x2000) == (0, 0x2300)
    with pytest.raises(ValueError):
        probe.target(4, 0x2000)


def test_terminating_contract_and_closed_cleanup(contract):
    """Oracle: actual original nonreturning tail, exact MZ fixup and known fixture bounds."""
    checked, regions = probe.exit_contract(ROOT)
    assert checked["mz_DS_fixup"] == 0x11B
    assert regions[0x4F4][-3:] == bytes.fromhex("e90dfc")
    assert checked["whole_routine_accepted"] is False
    assert len(probe.EXIT_CASES) == len(set(probe.EXIT_CASES)) == 28
    with pytest.raises(ValueError):
        probe.exit_assembly(b"", (0, 0, 0))
    with pytest.raises(ValueError):
        probe.exit_expected(b"", probe.EXIT_CASES[0])


def test_actual_terminating_error_path(tmp_path, contract, monkeypatch):
    """Oracle: all original/Pascal endpoints, actual vector restoration and nonreturning exit."""
    if not all(shutil.which(tool) for tool in ("dosbox", "as", "ld", "fpc")):
        pytest.skip("original execution toolchain unavailable")
    output = tmp_path / "exit"
    result = probe.run_exit(ROOT, output)
    assert result["matches"] == result["cases"] == 28
    monkeypatch.setattr(
        probe, "run_dosbox", lambda *_: pytest.fail("replay executed original")
    )
    assert probe.replay_exit(ROOT, output) == result
    case = probe.EXIT_CASES[2]
    trace = (output / "case-2/TRACE.BIN").read_bytes()
    for index in (2, 4, 8, 10, 12, 14, 16, 74, 662, 681, 757, 884):
        mutant = bytearray(trace)
        mutant[index] ^= 1
        with pytest.raises(ValueError):
            probe.exit_expected(bytes(mutant), case)

    host = output / "host"
    segment = struct.unpack_from("<H", trace)[0]
    for mode in range(1, 7):
        rejected = subprocess.run(
            [
                str(host / "probe_liero_error_exit"),
                str(segment),
                *map(str, case),
                str(mode),
            ],
            cwd=host,
            capture_output=True,
            check=False,
        )
        assert rejected.returncode == 211
    original = (host / "FUN_24dd_0218.inc").read_text()
    (host / "FUN_24dd_0218.inc").write_text(
        original.replace(
            "  RegisterAX := originalAX;\n  FUN_24dd_021f;",
            "  RegisterAX := originalAX;",
        )
    )
    build = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fi.", "-Fu.", "-FU.", "probe_liero_error_exit.pas"],
        cwd=host,
        capture_output=True,
        check=True,
    )
    assert build.returncode == 0
    (host / "VECTORS.BIN").write_bytes(trace[586:662])
    execution = subprocess.run(
        [str(host / "probe_liero_error_exit"), str(segment), *map(str, case)],
        cwd=host,
        capture_output=True,
        check=False,
    )
    assert execution.returncode == case[0]
    assert (host / "PASCAL.BIN").read_bytes() != trace


@pytest.mark.parametrize("text_error", [False, True])
def test_open_cleanup_and_text_error_original_parity(
    tmp_path, contract, monkeypatch, text_error
):
    """Oracle: actual flush/close composition and caller error frame, not full-program recovery."""
    if not all(shutil.which(tool) for tool in ("dosbox", "as", "ld", "fpc")):
        pytest.skip("original execution toolchain unavailable")
    output = tmp_path / "open-error"
    result = probe.run_exit(ROOT, output, open_output=True, text_error=text_error)
    panel = probe.TEXT_EXIT_CASES if text_error else probe.OPEN_EXIT_CASES
    assert result["matches"] == len(panel)
    monkeypatch.setattr(
        probe, "run_dosbox", lambda *_: pytest.fail("replay executed DOS")
    )
    assert (
        probe.replay_exit(ROOT, output, open_output=True, text_error=text_error)
        == result
    )
    trace = (output / "case-0/TRACE.BIN").read_bytes()
    for offset in (
        2,
        8,
        10,
        62,
        64,
        72,
        76,
        332,
        338,
        458,
        662,
        757,
        *range(885, 909, 2),
        909,
        len(trace) - 1,
    ):
        mutant = bytearray(trace)
        mutant[offset] ^= 1
        with pytest.raises(ValueError):
            probe.exit_expected(bytes(mutant), panel[0])
    host = output / "host"
    if text_error:
        path = host / "FUN_249c_0037.inc"
        original = path.read_text()
        assert "$0155" in original
        path.write_text(original.replace("$0155", "$0157"))
    else:
        segment = struct.unpack_from("<H", trace)[0]
        handle = struct.unpack_from("<H", trace, 885)[0]
        for mode in range(1, 9):
            rejected = subprocess.run(
                [
                    str(host / "probe_liero_error_exit"),
                    str(segment),
                    *map(str, panel[0]),
                    str(handle),
                    str(mode),
                ],
                cwd=host,
                capture_output=True,
                check=False,
            )
            assert rejected.returncode == 211
        path = host / "FUN_24dd_3711.inc"
        original = path.read_text()
        path.write_text(
            original.replace(
                "    FUN_24dd_374d;\n  end;",
                "    FUN_24dd_374d;\n    if RegisterAX <> 0 then Exit;\n  end;",
            )
        )
    subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fi.", "-Fu.", "-FU.", "probe_liero_error_exit.pas"],
        cwd=host,
        capture_output=True,
        check=True,
    )
    index = 0 if text_error else 4
    case = panel[index]
    original_trace = (output / f"case-{index}/TRACE.BIN").read_bytes()
    segment = struct.unpack_from("<H", original_trace)[0]
    handle = struct.unpack_from("<H", original_trace, 885)[0]
    (host / "VECTORS.BIN").write_bytes(original_trace[586:662])
    execution = subprocess.run(
        [
            str(host / "probe_liero_error_exit"),
            str(segment),
            *map(str, case),
            str(handle),
        ],
        cwd=host,
        capture_output=True,
        check=False,
    )
    assert execution.returncode == case[0]
    assert (host / "PASCAL.BIN").read_bytes() != original_trace


@pytest.mark.parametrize("mode", range(4))
def test_disjoint_original_harness_assembles(tmp_path, contract, mode):
    """Oracle: real assembler with owned code hole/target aliases, not original execution."""
    (tmp_path / "harness.S").write_text(probe.harness(0xA5, mode))
    raw = probe.assemble_probe(tmp_path / "harness.S", tmp_path)
    symbols = subprocess.run(
        ["nm", str(tmp_path / "probe.o")], capture_output=True, text=True, check=True
    ).stdout
    labels = {
        line.split()[-1]: int(line.split()[0], 16) + 0x100
        for line in symbols.splitlines()
    }
    image = probe.build_image(raw, labels["collector"])
    assert image[0x6E : 0x6E + 29] == probe.RAW
    assert image[0x8B] == 0xE9
    assert len(image) + 0x100 < 0x6000
    mutant = bytearray(raw)
    mutant[0x6E] = 1
    with pytest.raises(ValueError):
        probe.build_image(bytes(mutant), labels["collector"])


def synthetic_trace(case):
    """Oracle: synthetic endpoint mechanism only, no claim of DOS evidence."""
    seed, mode = case
    segment = 0x2000
    _, target_segment = probe.target(mode, segment)
    globals_ = bytearray([seed] * 58)
    for cell in (0x6402, 0x6404, 0x6410) if mode else (0x6402, 0x6404):
        struct.pack_into("<H", globals_, cell - 0x63D8, 0)
    first = (
        struct.pack("<6H", target_segment, segment, 0xEFEC, segment, 0x16E, segment)
        + globals_
        if mode
        else bytes([seed] * probe.SNAPSHOT)
    )
    last = (
        struct.pack("<6H", segment, segment, 0xEFF0, segment, 0x1357, 0x2468) + globals_
    )
    return struct.pack("<4H", segment, mode, seed, int(mode != 0)) + first + last


@pytest.mark.parametrize("case", probe.CASES)
def test_full_trace_global_stack_and_null_selection(case):
    """Oracle: each captured byte is bound to disclosed fixture semantics."""
    trace = synthetic_trace(case)
    row = probe.projection(trace, case)
    assert row[0] == int(case[1] != 0)
    assert row[2] == 0xEFF0
    for index in range(len(trace)):
        mutant = bytearray(trace)
        mutant[index] ^= 1
        with pytest.raises(ValueError):
            probe.projection(bytes(mutant), case)
    with pytest.raises(ValueError):
        probe.projection(trace[:-1], case)


def test_missing_original_skips(tmp_path):
    """Oracle: BYOD gating does not create success-shaped artifacts."""
    assert probe.run(tmp_path, tmp_path / "run")["status"] == "skipped"
    assert not (tmp_path / "run").exists()


def test_first_failure_no_retry(contract, tmp_path, monkeypatch):
    """Oracle: injected DOS timeout cannot trigger another case or Pascal execution."""
    calls = []

    def failing(directory):
        """Oracle: synthetic timeout, no guest execution."""
        calls.append(directory)
        raise subprocess.TimeoutExpired(["dosbox"], 30)

    monkeypatch.setattr(probe, "run_dosbox", failing)
    report = probe.run(ROOT, tmp_path / "run")
    assert report["status"] == "failed"
    assert len(calls) == 1
    assert report["actual_callback_recovered"] is False
    assert not (tmp_path / "run/compile.log").exists()


@pytest.mark.parametrize(
    "mutation",
    ["none", "trace", "image", "Pascal", "method", "metadata", "missing", "escape"],
)
def test_saved_replay_rehashed_tamper_rejected(tmp_path, mutation):
    """Oracle: saved synthetic mechanism, no original/candidate rerun."""
    saved = ROOT / "targets/liero/build/cleanup-dispatch/mechanism-v1"
    if (
        not (saved / "result.json").is_file()
        or not (ROOT / "extracted/liero/LIERO.EXE").is_file()
    ):
        pytest.skip("saved mechanism/BYOD unavailable")
    copied = tmp_path / "copy"
    shutil.copytree(saved, copied)
    report = json.loads((copied / "result.json").read_text())
    paths = {
        "trace": "case-1/TRACE.BIN",
        "image": "case-1/PROBE.COM",
        "Pascal": "PASCAL.BIN",
        "method": "methods/liero_cleanup_dispatch_probe.py",
    }
    if mutation in paths:
        path = copied / paths[mutation]
        data = bytearray(path.read_bytes())
        data[-1] ^= 1
        path.write_bytes(data)
        report["artifact_hashes"][paths[mutation]] = probe.pilot.digest(path)
    elif mutation == "metadata":
        report["actual_callback_recovered"] = True
    elif mutation == "missing":
        report["artifact_hashes"].pop("case-1/TRACE.BIN")
    elif mutation == "escape":
        report["artifact_hashes"]["../outside"] = "0" * 64
    probe.pilot.save(copied / "result.json", report)
    if mutation == "none":
        assert probe.validate_report(ROOT, copied)["cases"] == 8
        from engine.scoped_verification import cleanup_dispatch_contract_graph

        graph = cleanup_dispatch_contract_graph(ROOT / "targets/liero", copied)
        assert (
            graph.facts["allocator.cleanup-dispatch.mechanism"].value[
                "synthetic_callback"
            ]
            is True
        )
        assert (
            graph.facts["allocator.cleanup-dispatch.actual_callback_contract"].status
            == "unknown"
        )
        assert graph.facts["allocator.cleanup-dispatch.write-sites"].value[
            "installed_target_relative_to_load"
        ] == {"offset": 0x1345, "segment": 0x135C}
        assert not graph.conflicts()
        assert not graph.propagate_same_value()
    else:
        with pytest.raises(ValueError):
            probe.validate_report(ROOT, copied)


def test_scoped_audit_preserves_synthetic_label(contract):
    """Oracle: audit mechanism must not masquerade as real callback behavior."""
    from engine.scoped_verification import load_scoped_checks

    saved = ROOT / "targets/liero/build/cleanup-dispatch/mechanism-v1/result.json"
    if not saved.is_file():
        pytest.skip("saved mechanism unavailable")
    checks = [
        item
        for item in load_scoped_checks(ROOT / "targets/liero")
        if item["scope"] == "cleanup_dispatch_synthetic_callback_mechanism"
    ]
    assert checks[0]["case_count"] == 8
    assert checks[0]["synthetic_callback"] is True
    assert checks[0]["actual_callback_recovered"] is False
    assert checks[0]["source_recovered"] is False
