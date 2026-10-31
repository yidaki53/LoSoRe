import hashlib
import json
import pathlib
import subprocess


def _target(tmp_path):
    target_root = tmp_path / "targets" / "demo"
    target_root.mkdir(parents=True)
    byod = tmp_path / "extracted" / "demo"
    byod.mkdir(parents=True)
    binary = byod / "DEMO.EXE"
    binary.write_bytes(b"MZ\x00\x01demo")
    return target_root, binary


def test_ingest_rejects_target_paths_outside_targets(tmp_path, monkeypatch, capsys):
    from engine import ingest

    monkeypatch.chdir(tmp_path)

    assert ingest.ingest("../outside") == 1
    assert "invalid target slug" in capsys.readouterr().out
    assert not (tmp_path / "outside").exists()


def test_failed_extraction_preserves_last_staged_assembly(tmp_path, monkeypatch):
    from engine import ingest

    target_root, _ = _target(tmp_path)
    (target_root / "asm").mkdir(parents=True)
    (target_root / "decomp").mkdir()
    (target_root / "asm" / "FUN_OLD.s").write_text("; known good export\n")
    (target_root / "functions.json").write_text('{"functions":[]}\n')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LSR_GHIDRA_PROJ", str(tmp_path / "scratch"))
    monkeypatch.setattr(ingest, "find_ghidra", lambda: None)
    monkeypatch.setattr(ingest.shutil, "which", lambda _: "/usr/bin/python3")
    monkeypatch.setattr(
        ingest.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0], returncode=7, stdout="", stderr="Ghidra failed"
        ),
    )

    assert ingest.ingest("demo") == 1
    assert (target_root / "asm" / "FUN_OLD.s").read_text() == "; known good export\n"
    json_file = target_root / "functions.json"
    assert json_file.read_text() == '{"functions":[]}\n'


def test_successful_extraction_replaces_exports_and_records_provenance(
    tmp_path, monkeypatch
):
    from engine import ingest

    target_root, binary = _target(tmp_path)
    (target_root / "asm").mkdir(parents=True)
    (target_root / "asm" / "FUN_OLD.s").write_text("; stale\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LSR_GHIDRA_PROJ", str(tmp_path / "scratch"))
    monkeypatch.setattr(ingest, "find_ghidra", lambda: None)
    monkeypatch.setattr(ingest.shutil, "which", lambda _: "/usr/bin/python3")

    def export_functions(command, **kwargs):
        if command[-1] == "-version":
            return subprocess.CompletedProcess(
                command,
                returncode=0,
                stdout="",
                stderr='openjdk version "test"',
            )
        out = pathlib.Path(kwargs["env"]["LSR_OUTDIR"])
        (out / "asm").mkdir(parents=True)
        (out / "decomp").mkdir()
        (out / "asm" / "FUN_NEW.s").write_text(
            "; entry=1000:0000\nMOV AX, BX\n"
        )
        (out / "decomp" / "FUN_NEW.c").write_text("void FUN_NEW(void) {}\n")
        (out / "functions.json").write_text(
            json.dumps({"functions": [{"name": "FUN_NEW"}], "num_functions": 1})
        )
        return subprocess.CompletedProcess(
            command, returncode=0, stdout="[ExportFuncs] wrote 1 functions", stderr=""
        )

    monkeypatch.setattr(ingest.subprocess, "run", export_functions)

    assert ingest.ingest("demo") == 0
    assert not (target_root / "asm" / "FUN_OLD.s").exists()
    assert (target_root / "asm" / "FUN_NEW.s").is_file()
    assert (target_root / "decomp" / "FUN_NEW.c").is_file()
    manifests = list((target_root / "ingest-runs").glob("*.json"))
    assert len(manifests) == 1
    manifest = json.loads(manifests[0].read_text())
    assert manifest["status"] == "ready"
    assert manifest["binary"]["sha256"] == hashlib.sha256(binary.read_bytes()).hexdigest()
    assert manifest["exports"] == {"functions": 1, "assembly": 1, "decompiler": 1}
    assert manifest["tools"]["java_version"] == 'openjdk version "test"'


def test_empty_ghidra_export_is_failure_and_keeps_previous_assembly(
    tmp_path, monkeypatch
):
    from engine import ingest

    target_root, _ = _target(tmp_path)
    (target_root / "asm").mkdir()
    previous = target_root / "asm" / "FUN_OLD.s"
    previous.write_text("; known good export\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LSR_GHIDRA_PROJ", str(tmp_path / "scratch"))
    monkeypatch.setattr(ingest, "find_ghidra", lambda: None)
    monkeypatch.setattr(ingest.shutil, "which", lambda _: "/usr/bin/python3")

    def export_no_functions(command, **kwargs):
        if command[-1] == "-version":
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="java test")
        out = pathlib.Path(kwargs["env"]["LSR_OUTDIR"])
        (out / "asm").mkdir(parents=True)
        (out / "decomp").mkdir()
        (out / "functions.json").write_text(
            json.dumps({"functions": [], "num_functions": 0})
        )
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(ingest.subprocess, "run", export_no_functions)

    assert ingest.ingest("demo") == 1
    assert previous.read_text() == "; known good export\n"
    manifest_path = next((target_root / "ingest-runs").glob("*.json"))
    manifest = json.loads(manifest_path.read_text())
    assert manifest["status"] == "failed"
    assert "contains no functions" in manifest["error"]
