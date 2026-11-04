"""Oracle: original37B3 write boundary, installed source and deliberately scoped service mechanisms."""

import shutil
import struct
import subprocess

import pytest

from engine.evidence_archive import read_archive
from engine.routine_contract import load_contract
from tools import liero_write_handler_probe as probe


def test_write_corpus_freezes_count_outcomes_and_segment_origins():
    """Oracle: deterministic inputs distinguish real services and injected shortwrite/error paths."""
    for mode in probe.MODES:
        rows = probe.cases(mode)
        assert rows == probe.cases(mode)
        assert len(set(rows)) == len(rows)
        assert {struct.unpack_from("<H", row)[0] for row in rows} == {
            0,
            1,
            2,
            7,
            31,
            64,
            127,
            128,
        }
        assert {struct.unpack_from("<H", row, 6)[0] for row in rows} == {0, 0x100}
        assert all(len(row) == probe.CASE_BYTES for row in rows)
        assert all(
            struct.unpack_from("<H", row)[0] == struct.unpack_from("<H", row, 16)[0]
            for row in rows
        )
    scripted = probe.cases("injected")
    assert {struct.unpack_from("<2H", row, 2) for row in scripted} >= {
        (1, 5),
        (1, 65535),
        (0, 64),
    }
    with pytest.raises(ValueError, match="unknown"):
        probe.cases("guessed-service")


def test_original_write_leaf_installed_pascal_outputs_and_replay(tmp_path, monkeypatch):
    """Oracle: real file/NUL/invalidhandle plus separate synthetic INT21 returns, never whole ABI."""
    if not (probe.ROOT / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(name) for name in ("as", "ld", "fpc", "dosbox")
    ):
        pytest.skip("write original/host dependencies unavailable")
    output = tmp_path / "write"
    result = probe.run(probe.ROOT, output)
    assert result["status"] == "passed"
    assert [row["matches"] for row in result["modes"].values()] == [8, 8, 8, 32]
    assert result["modes"]["file"]["output_bytes"] == 360
    assert not result["whole_routine_accepted"] and result["source_promotions"] == 0
    assert result["modes"]["injected"]["oracle"] == "injected-service-mechanism"
    assert probe.replay(probe.ROOT, output) == result
    checked = load_contract(probe.ROOT / "targets/liero", "FUN_24dd_37b3")
    assert checked is not None and checked["reviewed_bytes_hex"] == probe.RAW.hex()
    assert checked["file_offset"] == probe.contract(probe.ROOT)["file_offset"]
    archive = read_archive(output)
    for mode in probe.MODES:
        payload = archive[f"{mode}/CASES.BIN"]
        native = archive[f"{mode}/TRACE.BIN"]
        host = archive[f"{mode}/host/PASCAL.BIN"]
        native_output = archive[f"{mode}/OUTPUT.BIN"] if mode == "file" else b""
        host_output = archive[f"{mode}/host/OUTPUT.BIN"] if mode == "file" else b""
        for offset in (
            0,
            12,
            14,
            16,
            18,
            20,
            22,
            26,
            28,
            32 + 8,
            32 + 256,
            4128,
            4132,
            4134,
            4136,
            4138,
        ):
            mutant = bytearray(native)
            mutant[offset] ^= 1
            assert (
                probe.compare(
                    mode, payload, bytes(mutant), host, native_output, host_output
                )["status"]
                == "failed"
            )
        for offset in (30, 4130):
            mutant = bytearray(native)
            mutant[offset] ^= 1
            with pytest.raises(ValueError, match="binding"):
                probe.compare(
                    mode, payload, bytes(mutant), host, native_output, host_output
                )
        for offset in (0, 2, 4, 6, 8, 12 + 8, 12 + 256):
            mutant = bytearray(host)
            mutant[offset] ^= 1
            assert (
                probe.compare(
                    mode, payload, native, bytes(mutant), native_output, host_output
                )["status"]
                == "failed"
            )
        with pytest.raises(ValueError, match="incomplete"):
            probe.compare(mode, payload, native[:-1], host, native_output, host_output)
    with pytest.raises(ValueError, match="emitted"):
        probe.compare(
            "file",
            archive["file/CASES.BIN"],
            archive["file/TRACE.BIN"],
            archive["file/host/PASCAL.BIN"],
            b"",
            archive["file/host/OUTPUT.BIN"],
        )

    def forbidden(*_args, **_kwargs):
        """Oracle: replay must not execute a process or assembler."""
        raise AssertionError("replay attempted execution")

    monkeypatch.setattr(probe, "run_dosbox", forbidden)
    monkeypatch.setattr(probe, "assemble_probe", forbidden)
    monkeypatch.setattr(probe.subprocess, "run", forbidden)
    assert probe.replay(probe.ROOT, output) == result
    (output / "file/TRACE.BIN").write_bytes(b"partial")
    with pytest.raises(ValueError, match="changed"):
        probe.replay(probe.ROOT, output)


def test_original_leaf_contract_rejects_changed_instruction(monkeypatch):
    """Oracle: authenticated complete32-byte entry and no MZ fixups, not assembly text."""
    if not (probe.ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("BYOD unavailable")
    checked = probe.contract(probe.ROOT)
    assert checked["relocations"] == []
    assert checked["scope"].startswith("Full4096arena")
    monkeypatch.setattr(probe, "RAW", b"\x90" + probe.RAW[1:])
    with pytest.raises(ValueError, match="original bytes"):
        probe.contract(probe.ROOT)


@pytest.mark.parametrize("dispatch", ["flush", "optional"])
def test_original_output_dispatch_composes_leaf_and_preserves_sticky_error(
    tmp_path, monkeypatch, dispatch
):
    """Oracle: actual396c/397a to37b3, explicit code resolver; DOS versus injected outcomes separate."""
    if not (probe.ROOT / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(name) for name in ("as", "ld", "fpc", "dosbox")
    ):
        pytest.skip("write original/host dependencies unavailable")
    output = tmp_path / dispatch
    result = probe.run(probe.ROOT, output, dispatch)
    assert result["status"] == "passed"
    assert [row["matches"] for row in result["modes"].values()] == [8, 8, 8, 32]
    archive = read_archive(output)
    assert probe.replay(probe.ROOT, output) == result
    checked = probe.contract(probe.ROOT, dispatch)["dispatch"]
    assert checked["bytes"] == probe.DISPATCH_RAW[dispatch].hex()
    assert checked["relocations"] == []
    routine = "FUN_24dd_396c" if dispatch == "flush" else "FUN_24dd_397a"
    published = load_contract(probe.ROOT / "targets/liero", routine)
    assert published is not None
    assert published["reviewed_bytes_hex"] == checked["bytes"]
    assert published["file_offset"] == checked["file_offset"]
    assert published["callee_contracts"] == ["FUN_24dd_37b3"]
    for mode in probe.MODES:
        image = archive[f"{mode}/PROBE.COM"]
        method_offset = image.index(probe.RAW) + 0x100
        args = (
            mode,
            archive[f"{mode}/CASES.BIN"],
            archive[f"{mode}/TRACE.BIN"],
            archive[f"{mode}/host/PASCAL.BIN"],
            archive[f"{mode}/OUTPUT.BIN"] if mode == "file" else b"",
            archive[f"{mode}/host/OUTPUT.BIN"] if mode == "file" else b"",
            dispatch,
            method_offset,
        )
        for offset in (2, 10, 14, 16, 24, 32 + 20, 32 + 22, 32 + 24, 32 + 26, 4140):
            mutant = bytearray(args[2])
            mutant[offset] ^= 0x40 if offset == 24 else 1
            assert (
                probe.compare(*args[:2], bytes(mutant), *args[3:])["status"] == "failed"
            )
        mutant = bytearray(args[3])
        mutant[10] ^= 1
        assert probe.compare(*args[:3], bytes(mutant), *args[4:])["status"] == "failed"

    host = tmp_path / "rejections"
    shutil.copytree(output / "file/host", host)
    image = archive["file/PROBE.COM"]
    command = [
        str(host / "probe_liero_write_handler"),
        "0",
        str(result["modes"]["file"]["fixture_handle"]),
        str(result["modes"]["file"]["fixture_segment"]),
        str(probe.DISPATCHES[dispatch]),
        str(image.index(probe.RAW) + 0x100),
    ]
    for fault in (
        "nil-object",
        "nil-source",
        "missing-write",
        "wrong-object",
        "wrong-object-segment",
        "wrong-source",
        "wrong-source-segment",
        "wrong-code-segment",
        "bad-count",
        "unknown-method",
    ):
        rejected = subprocess.run(
            command + [fault], cwd=host, capture_output=True, timeout=30, check=False
        )
        assert rejected.returncode == 211, (fault, rejected.stderr)

    source = host / (routine + ".inc")
    original = source.read_text()
    assert "if RegisterAX <> 0 then" in original
    source.write_text(original.replace("if RegisterAX <> 0 then", "if True then"))
    subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fu.", "-Fi.", "-FU.", "probe_liero_write_handler.pas"],
        cwd=host,
        capture_output=True,
        timeout=30,
        check=True,
    )
    subprocess.run(command, cwd=host, capture_output=True, timeout=30, check=True)
    assert (
        probe.compare(
            "file",
            archive["file/CASES.BIN"],
            archive["file/TRACE.BIN"],
            (host / "PASCAL.BIN").read_bytes(),
            archive["file/OUTPUT.BIN"],
            (host / "OUTPUT.BIN").read_bytes(),
            dispatch,
            image.index(probe.RAW) + 0x100,
        )["status"]
        == "failed"
    )

    def forbidden(*_args, **_kwargs):
        """Oracle: saved dispatch replay must not execute processes."""
        raise AssertionError("dispatch replay attempted execution")

    monkeypatch.setattr(probe.subprocess, "run", forbidden)
    assert probe.replay(probe.ROOT, output) == result
