"""Disc-gated tests: green WITH or WITHOUT BYOD present (the Liero standard).

The pipeline's central contract is graceful disc-gating: every stage
(provenance/ingest/draft/verify) must exit 0 and SKIP when its gated input is
absent, AND do real work when it is present. `extracted/` is gitignored, so CI
runs with no BYOD while a developer machine may have extracted/liero/ populated.
These tests therefore pin BOTH branches against explicit temp paths, decoupled
from the ambient state of extracted/liero/, so the suite is deterministic on any
machine. No pass on an oracle == not decompiled (docs/ORACLES.md).
"""
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent


def _run(script: str, *args: str, cwd: pathlib.Path | None = None) -> subprocess.CompletedProcess:
    """Invoke a repo entry-point with absolute paths so results never depend on CWD."""
    return subprocess.run(
        [sys.executable, str(REPO / script), *args],
        capture_output=True, text=True, cwd=str(cwd or REPO),
    )


# --- gated SKIP branch: forced absent BYOD, regardless of extracted/liero/ ---

def test_verify_skips_without_byod(tmp_path):
    r = _run("engine/verify.py", "--target", "liero", "--byod", str(tmp_path / "absent"))
    assert r.returncode == 0 and "SKIP" in r.stdout


def test_provenance_skips_without_byod(tmp_path):
    r = _run("tools/provenance.py", "--target", "liero", "--byod", str(tmp_path / "absent"))
    assert r.returncode == 0 and "SKIP" in r.stdout


def test_draft_skips_without_asm(tmp_path):
    # draft gates on targets/<slug>/asm/*.s; a slug with no asm/ always SKIPs.
    r = _run("engine/draft.py", "--target", "no-such-target")
    assert r.returncode == 0 and "SKIP" in r.stdout


def test_ingest_skips_without_ghidra(tmp_path):
    # analyzeHeadless is not installed in CI -> SKIP even if BYOD is present.
    r = _run("engine/ingest.py", "--target", "liero")
    assert r.returncode == 0 and "SKIP" in r.stdout


# --- ungated branch: real work happens when the gated input IS present ---

def test_provenance_runs_with_byod(tmp_path):
    byod = tmp_path / "byod"
    byod.mkdir()
    (byod / "FAKE.EXE").write_bytes(b"MZ\x90\x00" + b"Portions Copyright (c) 1983,92 Borland\x00" * 2)
    work = tmp_path / "repo"
    (work / "targets" / "faketgt" / "docs").mkdir(parents=True)
    r = _run("tools/provenance.py", "--target", "faketgt", "--byod", str(byod), cwd=work)
    assert r.returncode == 0 and "SKIP" not in r.stdout
    prov = work / "targets" / "faketgt" / "docs" / "PROVENANCE.md"
    assert prov.exists() and "borland" in prov.read_text().lower()


def test_verify_passes_on_byte_match(tmp_path):
    byod = tmp_path / "byod"
    byod.mkdir()
    build = tmp_path / "build"
    build.mkdir()
    payload = b"MZ" + bytes(range(64))
    (byod / "LIERO.EXE").write_bytes(payload)
    (build / "LIERO.EXE").write_bytes(payload)
    work = tmp_path / "repo"
    cfg = work / "targets" / "faketgt" / "config"
    cfg.mkdir(parents=True)
    (cfg / "build.sha1").write_text("514511ffcdbefa6f LIERO.EXE\n")
    r = _run("engine/verify.py", "--target", "faketgt", "--byod", str(byod),
             "--build", str(build), "--oracle", "byte-exact", cwd=work)
    assert r.returncode == 0 and "PASS" in r.stdout


def test_verify_fails_on_byte_mismatch(tmp_path):
    byod = tmp_path / "byod"
    byod.mkdir()
    build = tmp_path / "build"
    build.mkdir()
    (byod / "LIERO.EXE").write_bytes(b"MZ" + bytes(range(64)))
    (build / "LIERO.EXE").write_bytes(b"MZ" + bytes(range(64)) + b"\xff")  # differs
    work = tmp_path / "repo"
    cfg = work / "targets" / "faketgt" / "config"
    cfg.mkdir(parents=True)
    (cfg / "build.sha1").write_text("514511ffcdbefa6f LIERO.EXE\n")
    r = _run("engine/verify.py", "--target", "faketgt", "--byod", str(byod),
             "--build", str(build), "--oracle", "byte-exact", cwd=work)
    assert r.returncode == 1 and "FAIL" in r.stdout


# --- pure unit backends ---

def test_diff_backends(tmp_path):
    sys.path.insert(0, str(REPO / "engine"))
    from diff import byte_exact, relocation_aware
    a = tmp_path / "a.bin"
    b = tmp_path / "b.bin"
    a.write_bytes(b"\x01\x02\x03")
    b.write_bytes(b"\x01\x02\x03")
    assert byte_exact(a, b) and relocation_aware(a, b)
    b.write_bytes(b"\x01\x02\x04")
    assert not byte_exact(a, b)


def test_scheduler_routes():
    sys.path.insert(0, str(REPO / "engine"))
    from scheduler import route
    assert route(100, 10) == "human-residue"
    assert route(100, 40) == "agent-fanout-high-effort"
    assert route(100, 80) == "agent-fanout"


def test_new_target_scaffold(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sys.path.insert(0, str(REPO / "tools"))  # absolute: survives the chdir above
    import new_target
    new_target.new_target("demo-fw", "firmware")
    assert (tmp_path / "targets/demo-fw/src/main.c").exists()
    assert "firmware" in (tmp_path / "targets/demo-fw/config/target.yaml").read_text()

