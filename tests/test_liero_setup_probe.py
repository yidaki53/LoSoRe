import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_read_handler_probe as probe


def test_setup_skips_missing_original(tmp_path):
    """Oracle: absent BYOD skips without creating setup evidence."""
    assert (
        probe.run_probe(tmp_path / "run", tmp_path, handler="setup")["status"]
        == "skipped"
    )
    assert not (tmp_path / "run").exists()


def test_input_setup_original_pascal_errors_and_mutants(tmp_path):
    """Oracle: actual original input setup versus scoped Pascal and host open service."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    if not all(shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")):
        pytest.skip("DOSBox/assembler/FPC unavailable")
    output = tmp_path / "setup"
    result = probe.run_probe(output, root, handler="setup")
    assert result["status"] == "passed"
    assert result["call_count"] == 32
    assert probe.validate_saved_report(output, root) == result
    for name, status in (
        ("setup-existing", 0),
        ("setup-empty-name", 0),
        ("setup-missing-file", 2),
        ("setup-missing-directory", 2),
    ):
        assert [
            row["expected_return"] for row in result["fixtures"][name]["calls"]
        ] == [status] * 8
    for name, (kind, _) in probe.fixtures("setup").items():
        fixture = output / name
        trace = (fixture / "TRACE.BIN").read_bytes()
        candidate = (fixture / "PASCAL.BIN").read_bytes()
        for offset in (0, 2, 6, 10, 22, 30, 50, 130, 513):
            changed = bytearray(candidate)
            changed[offset] ^= 1
            assert (
                probe.compare_setup(trace, bytes(changed), kind)["status"] == "failed"
            )
        changed = bytearray(trace)
        changed[2 * 532 + 10] ^= 1
        with pytest.raises(ValueError):
            probe.compare_setup(bytes(changed), candidate, kind)
        with pytest.raises(ValueError, match="Pascal setup records"):
            probe.compare_setup(trace, candidate[:-1], kind)
    directory = output / "candidate"
    source = directory / "FUN_24dd_420c.inc"
    original = source.read_text()
    for name, old, new, fixture_name in (
        (
            "clear-position",
            "objectWords^ := 0;",
            "objectWords^ := 0; PWord(PByte(objectPointer) + 8)^ := 0;",
            "setup-existing",
        ),
        (
            "error-is-success",
            "if status <> 0 then",
            "if False then",
            "setup-missing-file",
        ),
    ):
        assert old in original
        source.write_text(original.replace(old, new, 1))
        executable = probe.compile_candidate(directory, handler="setup")
        fixture = output / fixture_name
        kind, _ = probe.fixtures("setup")[fixture_name]
        mutant = output / (name + ".BIN")
        subprocess.run(
            [
                str(executable),
                str(fixture / "STATE.BIN"),
                str(fixture / "INPUT.TXT"),
                str(mutant),
                str(kind),
            ],
            check=True,
            capture_output=True,
            timeout=30,
        )
        assert (
            probe.compare_setup(
                (fixture / "TRACE.BIN").read_bytes(), mutant.read_bytes(), kind
            )["status"]
            == "failed"
        )
    with pytest.raises(ValueError, match="artifact"):
        probe.validate_saved_report(output, root)
    source.write_text(original)
    executable = probe.compile_candidate(directory, handler="setup")
    fixture = output / "setup-existing"
    state = bytearray((fixture / "STATE.BIN").read_bytes())
    struct.pack_into("<H", state, 2, 0xD7B2)
    invalid = output / "OUTPUT-MODE.BIN"
    invalid.write_bytes(state)
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
