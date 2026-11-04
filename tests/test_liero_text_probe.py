"""Oracle: connected original text execution, installed bodies and explicit unsupported paths."""

import pathlib
import shutil
import struct
import subprocess

import pytest

from engine.evidence_archive import read_archive
from tools import liero_text_probe as probe


def available():
    """Oracle: BYOD/toolchain gate, never fabricated original observations."""
    return (probe.ROOT / "extracted/liero/LIERO.EXE").is_file() and all(
        shutil.which(name) for name in ("as", "ld", "dosbox", "fpc")
    )


def test_text_panel_and_original_contract(monkeypatch):
    """Oracle: complete original body/relocation facts and distinct deterministic panels."""
    for entry in probe.ENTRIES:
        for service in probe.SERVICES:
            if service in ("console", "scroll") and entry != "text":
                with pytest.raises(ValueError, match="console panel"):
                    probe.cases(entry, service)
                continue
            panel = probe.cases(entry, service)
            assert panel == probe.cases(entry, service)
            assert len(set(panel)) == len(panel)
            assert all(len(row) == probe.CASE_BYTES for row in panel)
            if entry == "text":
                assert all(
                    row[280] + struct.unpack_from("<H", row, 4)[0] < 80 for row in panel
                )
    if not available():
        pytest.skip("text original dependencies unavailable")
    checked, regions = probe.original(probe.ROOT)
    assert checked["text_relocations"] == [0x14E, 0x153]
    assert regions[0x1000][0x37:] == probe.TEXT_BYTES
    monkeypatch.setattr(probe, "TEXT_BYTES", b"\x90" + probe.TEXT_BYTES[1:])
    with pytest.raises(ValueError, match="text original"):
        probe.original(probe.ROOT)


@pytest.mark.parametrize(
    "entry,service",
    [
        ("writer", "file"),
        ("writer", "injected"),
        ("crlf", "file"),
        ("crlf", "injected"),
        ("text", "file"),
        ("text", "console"),
        ("text", "scroll"),
    ],
)
def test_original_text_chain_installed_source_and_immutable_replay(
    tmp_path, monkeypatch, entry, service
):
    """Oracle: whole declared output state, original frame and no-execution replay; not whole ABI."""
    if not available():
        pytest.skip("text original dependencies unavailable")
    output = tmp_path / "run"
    result = probe.run(probe.ROOT, output, entry, service)
    assert result["status"] == "passed"
    assert result["matches"] == len(probe.cases(entry, service))
    assert not result["whole_routine_accepted"] and result["source_promotions"] == 0
    assert probe.replay(probe.ROOT, output) == result
    archive = read_archive(output)
    args = (
        archive["CASES.BIN"],
        archive["TRACE.BIN"],
        archive["host/PASCAL.BIN"],
        archive["OUTPUT.BIN"],
        archive["host/OUTPUT.BIN"],
        entry,
        service,
    )
    for offset in (
        0,
        2,
        6,
        8,
        10,
        14,
        16,
        18,
        20,
        24,
        26,
        28,
        32 + 8,
        32 + 128,
        32 + 256,
        32 + 512,
        4544,
        5056,
    ):
        mutant = bytearray(args[1])
        mutant[offset] ^= 0x40 if offset == 14 else 1
        assert probe.compare(args[0], bytes(mutant), *args[2:])["status"] == "failed"
    for offset in (0, 2, 4, 6, 8, 8 + 128, 8 + 256, 8 + 512, 4520, 5032):
        mutant = bytearray(args[2])
        mutant[offset] ^= 1
        assert probe.compare(*args[:2], bytes(mutant), *args[3:])["status"] == "failed"
    with pytest.raises(ValueError, match="incomplete"):
        probe.compare(args[0], args[1][:-1], *args[2:])
    if args[3]:
        with pytest.raises(ValueError, match="emitted"):
            probe.compare(*args[:3], b"", *args[4:])

    def forbidden(*_args, **_kwargs):
        """Oracle: replay must not execute a process."""
        raise AssertionError("text replay attempted execution")

    monkeypatch.setattr(probe.subprocess, "run", forbidden)
    assert probe.replay(probe.ROOT, output) == result
    (output / "TRACE.BIN").write_bytes(b"partial")
    with pytest.raises(ValueError, match="changed"):
        probe.replay(probe.ROOT, output)


def compile_host(directory: pathlib.Path):
    """Oracle: mutant or rejection driver still compiles actual installed includes."""
    subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fi.", "-Fu.", "-FU.", "probe_liero_text.pas"],
        cwd=directory,
        capture_output=True,
        timeout=30,
        check=True,
    )


def test_full_text_source_mutants_and_unsupported_error_reject(tmp_path):
    """Oracle: compiled source mutations fail; nonzero010f transfer is not a successful no-op."""
    if not available():
        pytest.skip("text original dependencies unavailable")
    output = tmp_path / "text"
    result = probe.run(probe.ROOT, output, "text", "file")
    archive = read_archive(output)
    host = tmp_path / "mutants"
    shutil.copytree(output / "host", host)
    command = [
        str(host / "probe_liero_text"),
        "2",
        "0",
        str(result["fixture_segment"]),
        str(result["fixture_handle"]),
    ]
    for name, old, new in (
        ("FUN_249c_0037.inc", "state := 1 else", "state := 2 else"),
        ("FUN_249c_0037.inc", "Word(param_3) + length", "Word(param_3)"),
        ("FUN_24dd_3930.inc", "RegisterAX := 2;", "RegisterAX := 1;"),
    ):
        source = host / name
        original = source.read_text()
        assert old in original
        source.write_text(original.replace(old, new))
        compile_host(host)
        changed = subprocess.run(
            command, cwd=host, capture_output=True, timeout=30, check=False
        )
        if changed.returncode == 0:
            try:
                comparison = probe.compare(
                    archive["CASES.BIN"],
                    archive["TRACE.BIN"],
                    (host / "PASCAL.BIN").read_bytes(),
                    archive["OUTPUT.BIN"],
                    (host / "OUTPUT.BIN").read_bytes(),
                    "text",
                    "file",
                )
                assert comparison["status"] == "failed"
            except ValueError as exc:
                assert "emitted" in str(exc)
        source.write_text(original)
    compile_host(host)
    first = bytearray(probe.cases("text", "file")[0])
    for offset, value in (
        (10, 0x55AA),
        (12, 0xD7B1),
        (22, 1),
        (2, 25),
        (4, 80),
        (6, 0),
        (8, 129),
    ):
        invalid = bytearray(first)
        struct.pack_into("<H", invalid, offset, value)
        (host / "CASES.BIN").write_bytes(invalid)
        rejected = subprocess.run(
            command, cwd=host, capture_output=True, timeout=30, check=False
        )
        assert rejected.returncode == 211, (offset, rejected.stderr)


def test_buffered_flush_error_continuation_and_alias_rejection(tmp_path):
    """Oracle: original continues after failure; unsupported aliases are rejected before writes."""
    if not available():
        pytest.skip("text original dependencies unavailable")
    output = tmp_path / "writer"
    result = probe.run(probe.ROOT, output, "writer", "injected")
    archive = read_archive(output)
    host = tmp_path / "writer-mutant"
    shutil.copytree(output / "host", host)
    command = [
        str(host / "probe_liero_text"),
        "0",
        "1",
        str(result["fixture_segment"]),
        str(result["fixture_handle"]),
    ]
    source = host / "FUN_24dd_3899.inc"
    original = source.read_text()
    assert "FUN_24dd_396c;" in original
    source.write_text(
        original.replace(
            "FUN_24dd_396c;", "FUN_24dd_396c;\n      if GlobalWord6410 <> 0 then Exit;"
        )
    )
    compile_host(host)
    changed = subprocess.run(
        command, cwd=host, capture_output=True, timeout=30, check=False
    )
    assert changed.returncode == 0
    assert (
        probe.compare(
            archive["CASES.BIN"],
            archive["TRACE.BIN"],
            (host / "PASCAL.BIN").read_bytes(),
            archive["OUTPUT.BIN"],
            (host / "OUTPUT.BIN").read_bytes(),
            "writer",
            "injected",
        )["status"]
        == "failed"
    )
    source.write_text(original)
    driver = host / "probe_liero_text.pas"
    baseline = driver.read_text()
    (host / "CASES.BIN").write_bytes(probe.cases("writer", "injected")[1])
    for setup in (
        "LieroBufferSource := nil;",
        "LieroBufferObject := nil;",
        "RegisterSI := $7A70; RegisterAX := 1;",
        "RegisterSI := $79F0; RegisterAX := 1;",
        "RegisterSI := $6410; RegisterAX := 1;",
        "RegisterSI := $FFFF; RegisterAX := 2;",
        "LieroBufferSource := @RealModeMemory[0];",
        "LieroTextDataSegment := 0;",
        "RegisterDX := $FFFF; RegisterAX := 2;",
    ):
        driver.write_text(baseline.replace("calls := 0;", setup + "\n    calls := 0;"))
        compile_host(host)
        rejected = subprocess.run(
            command, cwd=host, capture_output=True, timeout=30, check=False
        )
        assert rejected.returncode == 211, (setup, rejected.stderr)
