import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_read_handler_probe as probe


def test_open_skips_missing_original(tmp_path):
    """Oracle: BYOD gate precedes artifacts, not successful-looking wrapper evidence."""
    assert (
        probe.run_probe(tmp_path / "run", tmp_path, handler="open")["status"]
        == "skipped"
    )
    assert not (tmp_path / "run").exists()


def test_input_open_reopen_close_composition_and_mutants(tmp_path):
    """Oracle: actual wrapper/dispatcher/leaf bodies, full state and supported error paths."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    if not all(shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")):
        pytest.skip("DOSBox/assembler/FPC unavailable")
    output = tmp_path / "open"
    forward = (root / "targets/liero/src/_forward.inc").read_text()
    driver = (root / "targets/liero/tests/probe_liero_setup_handler.pas").read_text()
    for function in ("36b7", "36bc", "36c4", "3711"):
        declaration = f"procedure FUN_24dd_{function}(objectPointer: Pointer); forward;"
        assert declaration in forward
        assert declaration in driver
    result = probe.run_probe(output, root, handler="open")
    assert result["status"] == "passed"
    assert result["call_count"] == 24
    assert probe.validate_saved_report(output, root) == result
    for row in result["fixtures"].values():
        assert [call["expected_status"] for call in row["calls"]] == [
            0x55AA,
            6,
            2,
            2,
            6,
            0x67,
            0x66,
            0x66,
        ]
        assert [call["expected_mode"] for call in row["calls"]] == [
            0xD7B1,
            0xD7B1,
            0xD7B0,
            0xD7B1,
            0xD7B0,
            0xD7B0,
            0x1234,
            0xD7B1,
        ]
    fixture = output / "open-short"
    trace = (fixture / "TRACE.BIN").read_bytes()
    candidate = (fixture / "PASCAL.BIN").read_bytes()
    for offset in (0, 2, 4, 10, 12, 22, 32, 132, 258, 513):
        changed = bytearray(candidate)
        changed[offset] ^= 1
        assert probe.compare_open(trace, bytes(changed))["status"] == "failed"
    changed = bytearray(trace)
    changed[2 * 532 + 10] ^= 1
    with pytest.raises(ValueError):
        probe.compare_open(bytes(changed), candidate)
    with pytest.raises(ValueError, match="Pascal open records"):
        probe.compare_open(trace, candidate[:-1])
    directory = output / "candidate"
    for file, old, new in (
        (
            "FUN_24dd_36c4.inc",
            "if not RegisterZeroFlag then",
            "if GlobalWord6410 <> 0 then",
        ),
        (
            "FUN_24dd_36c4.inc",
            "FUN_24dd_3711(objectPointer)\n  else",
            "begin FUN_24dd_3711(objectPointer); if GlobalWord6410 <> 0 then Exit; end\n  else",
        ),
        (
            "FUN_24dd_3711.inc",
            "modePointer^ := $D7B0;",
            "if RegisterZeroFlag then modePointer^ := $D7B0;",
        ),
    ):
        source = directory / file
        original = source.read_text()
        assert old in original
        source.write_text(original.replace(old, new))
        executable = probe.compile_candidate(directory, handler="open")
        mutant = output / "MUTANT.BIN"
        execution = subprocess.run(
            [
                str(executable),
                str(fixture / "STATE.BIN"),
                str(fixture / "INPUT.TXT"),
                str(mutant),
                "128",
            ],
            check=False,
            capture_output=True,
            timeout=30,
        )
        if execution.returncode == 0:
            assert probe.compare_open(trace, mutant.read_bytes())["status"] == "failed"
        else:
            assert execution.returncode in (7, 8)
        source.write_text(original)
    state = bytearray((fixture / "STATE.BIN").read_bytes())
    struct.pack_into("<H", state, 2, 0xD7B2)
    invalid = output / "OUTPUT.BIN"
    invalid.write_bytes(state)
    executable = probe.compile_candidate(directory, handler="open")
    rejected = subprocess.run(
        [
            str(executable),
            str(invalid),
            str(fixture / "INPUT.TXT"),
            str(output / "REJECTED.BIN"),
            "128",
        ],
        check=False,
        capture_output=True,
        timeout=30,
    )
    assert rejected.returncode == 211
    driver_path = directory / "probe_liero_setup_handler.pas"
    original_driver = driver_path.read_text()
    invocation = "FUN_24dd_36b7(@State.ObjectData[0]);"
    assert invocation in original_driver
    driver_path.write_text(
        original_driver.replace(invocation, "FUN_24dd_36bc(@State.ObjectData[0]);")
    )
    executable = probe.compile_candidate(directory, handler="open")
    rejected = subprocess.run(
        [
            str(executable),
            str(fixture / "STATE.BIN"),
            str(fixture / "INPUT.TXT"),
            str(output / "OUTPUT-REQUEST.BIN"),
            "128",
        ],
        check=False,
        capture_output=True,
        timeout=30,
    )
    assert rejected.returncode == 211
