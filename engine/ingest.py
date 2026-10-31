"""Ingest: Ghidra headless export -> targets/<slug>/asm/ (+ decomp/, functions.json).

Runs the Java post-script tools/ghidra/ExportFuncs.java which writes, per target:
  targets/<slug>/asm/<func>.s      raw instruction listing
  targets/<slug>/decomp/<func>.c   best-effort decompiler output (draft seed)
  targets/<slug>/functions.json    metadata (name, entry, size, cc, ...)

Disc-gated: SKIP (pass) without extracted/<target>/ or without analyzeHeadless.

Env knobs:
  LSR_GHIDRA         path to ghidra install dir (default: auto-detect ~/tools/ghidra_*)
  LSR_GHIDRA_PROJ    writable scratch root (default: <tempdir>/lsr_proj_<target>;
                     generated project paths must not contain spaces)
  LSR_PROCESSOR      force processor spec (else auto-detect by loader)
"""
from __future__ import annotations

import argparse
import datetime
import glob
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile


def find_ghidra() -> str | None:
    """Locate a Ghidra install dir (contains support/analyzeHeadless)."""
    env = os.environ.get("LSR_GHIDRA")
    cands = [env] if env else []
    cands += sorted(glob.glob(os.path.expanduser("~/tools/ghidra_*_PUBLIC")), reverse=True)
    cands += sorted(glob.glob("/opt/ghidra*"), reverse=True)
    cands += sorted(glob.glob("/usr/share/ghidra*"), reverse=True)
    for c in cands:
        if c and os.path.exists(os.path.join(c, "support", "analyzeHeadless")):
            return c
    # fall back to PATH
    return None  # analyzeHeadless on PATH handled by caller


def pick_binary(src: pathlib.Path) -> pathlib.Path | None:
    """Choose the main executable to analyze: prefer *.EXE (largest), else *.exe."""
    exes = sorted(src.glob("*.EXE")) + sorted(src.glob("*.exe"))
    if not exes:
        exes = []
        for path in src.iterdir():
            if not path.is_file():
                continue
            with path.open("rb") as stream:
                if stream.read(2) in (b"MZ", b"\x7fE"):
                    exes.append(path)
    if not exes:
        return None
    return max(exes, key=lambda p: p.stat().st_size)


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _ghidra_version(analyze_headless: str, ghidra: str | None) -> str | None:
    home = pathlib.Path(ghidra).resolve() if ghidra else pathlib.Path(
        analyze_headless
    ).resolve().parent.parent
    properties = home / "Ghidra" / "application.properties"
    if not properties.is_file():
        return None
    for line in properties.read_text(errors="replace").splitlines():
        if line.startswith("application.version="):
            return line.partition("=")[2].strip() or None
    return None


def _java_version(java: str | None) -> str | None:
    if not java:
        return None
    try:
        result = subprocess.run(
            [java, "-version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {exc}"
    output = (result.stdout + result.stderr).strip()
    if output:
        return output.splitlines()[0]
    return f"unavailable: java -version exited {result.returncode}"


def _safe_export_name(name: str) -> str:
    return "".join(
        char if char.isascii() and (char.isalnum() or char in "-_.") else "_"
        for char in name
    ) or "unnamed"


def _validate_export(outdir: pathlib.Path) -> tuple[dict, int, int]:
    metadata_path = outdir / "functions.json"
    try:
        metadata = json.loads(metadata_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid or missing functions.json: {exc}") from exc
    if not isinstance(metadata, dict):
        raise TypeError("functions.json must contain a JSON object")
    functions = metadata.get("functions")
    if not isinstance(functions, list) or not functions:
        raise ValueError("Ghidra export contains no functions")
    exported_count = metadata.get("num_functions")
    if (
        isinstance(exported_count, bool)
        or not isinstance(exported_count, int)
        or exported_count != len(functions)
    ):
        raise ValueError("functions.json num_functions does not match functions list")

    names = [entry.get("name") for entry in functions if isinstance(entry, dict)]
    if len(names) != len(functions) or any(
        not isinstance(name, str) or not name for name in names
    ):
        raise ValueError("every exported function must have a nonempty name")
    if len(set(names)) != len(names):
        raise ValueError("functions.json contains duplicate function names")
    expected_names = {_safe_export_name(name) + ".s" for name in names}
    if len(expected_names) != len(names):
        raise ValueError("function names collide after Ghidra filename sanitization")

    asm_dir = outdir / "asm"
    asm_files = list(asm_dir.glob("*.s")) if asm_dir.is_dir() else []
    actual_names = {path.name for path in asm_files}
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        unexpected = sorted(actual_names - expected_names)
        raise ValueError(
            f"assembly inventory mismatch; missing={missing}, unexpected={unexpected}"
        )
    if any(path.stat().st_size == 0 for path in asm_files):
        raise ValueError("Ghidra export contains an empty assembly file")
    decomp_dir = outdir / "decomp"
    decomp_count = len(list(decomp_dir.glob("*.c"))) if decomp_dir.is_dir() else 0
    return metadata, len(asm_files), decomp_count


def _publish_exports(stage: pathlib.Path, root: pathlib.Path) -> None:
    backup = stage / "backup"
    backup.mkdir()
    names = ("asm", "decomp", "functions.json")
    saved = []
    installed = []
    try:
        for name in names:
            destination = root / name
            if destination.exists():
                os.replace(destination, backup / name)
                saved.append(name)
        for name in names:
            os.replace(stage / name, root / name)
            installed.append(name)
    except OSError:
        for name in reversed(installed):
            destination = root / name
            if destination.is_dir():
                shutil.rmtree(destination)
            elif destination.exists():
                destination.unlink()
        for name in reversed(saved):
            os.replace(backup / name, root / name)
        raise


def _write_run_record(
    root: pathlib.Path,
    run_id: str,
    record: dict,
    log: str,
) -> pathlib.Path:
    run_dir = root / "ingest-runs"
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / f"{run_id}.log"
    log_path.write_text(log)
    record["log_file"] = str(log_path.relative_to(root))
    manifest_path = run_dir / f"{run_id}.json"
    temporary_path = manifest_path.with_suffix(".json.tmp")
    temporary_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    os.replace(temporary_path, manifest_path)
    return manifest_path


def ingest(target: str, processor: str | None = None, timeout: int = 1800) -> int:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", target):
        print(f"[ingest:{target}] FAIL invalid target slug")
        return 1
    root = pathlib.Path("targets") / target
    src = pathlib.Path("extracted") / target
    if not src.exists():
        print(f"[ingest:{target}] SKIP no BYOD (disc-gated) at {src}")
        return 0

    ghidra = find_ghidra()
    if ghidra:
        ah = os.path.join(ghidra, "support", "analyzeHeadless")
    else:
        ah = shutil.which("analyzeHeadless")
    if not ah or not os.path.exists(ah):
        print(f"[ingest:{target}] SKIP analyzeHeadless not installed "
              f"(set LSR_GHIDRA to your ghidra install)")
        return 0

    binary = pick_binary(src)
    if not binary:
        print(f"[ingest:{target}] SKIP no executable found in {src}")
        return 0

    root.mkdir(parents=True, exist_ok=True)
    scratch_root = pathlib.Path(
        os.environ.get("LSR_GHIDRA_PROJ")
        or pathlib.Path(tempfile.gettempdir()) / f"lsr_proj_{target}"
    ).expanduser()
    if " " in str(scratch_root):
        print(f"[ingest:{target}] FAIL scratch path contains spaces: {scratch_root}")
        return 1
    try:
        scratch_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"[ingest:{target}] FAIL cannot create scratch directory: {exc}")
        return 1

    started_at = datetime.datetime.now(datetime.UTC)
    run_id = started_at.strftime("%Y%m%dT%H%M%S.%fZ")
    proc = processor or os.environ.get("LSR_PROCESSOR")
    binary_hash = _sha256(binary)
    java = shutil.which("java")
    base_record = {
        "schema_version": 1,
        "run_id": run_id,
        "target": target,
        "started_at": started_at.isoformat(),
        "binary": {
            "path": str(binary.resolve()),
            "size_bytes": binary.stat().st_size,
            "sha256": binary_hash,
        },
        "tools": {
            "analyze_headless": str(pathlib.Path(ah).resolve()),
            "ghidra_home": ghidra,
            "ghidra_version": _ghidra_version(ah, ghidra),
            "java": java,
            "java_version": _java_version(java),
        },
        "processor": proc,
    }

    with tempfile.TemporaryDirectory(
        prefix=f"lsr_proj_{target}_", dir=scratch_root
    ) as project_dir, tempfile.TemporaryDirectory(
        prefix=".lsr-ingest-", dir=root
    ) as working_dir:
        outdir = pathlib.Path(working_dir) / "export"
        scripts = pathlib.Path(__file__).resolve().parent.parent / "tools" / "ghidra"
        env = dict(os.environ, LSR_OUTDIR=str(outdir))
        cmd = [
            ah,
            project_dir,
            target,
            "-import",
            str(binary.resolve()),
            "-overwrite",
            "-postScript",
            "ExportFuncs.java",
            "-scriptPath",
            str(scripts),
        ]
        if proc:
            cmd += ["-processor", proc]
        print(f"[ingest:{target}] {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
            )
            log = result.stdout + result.stderr
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            log = stdout + stderr
            base_record.update({
                "status": "failed",
                "error": f"analyzeHeadless timed out after {timeout}s",
                "command": cmd,
                "finished_at": datetime.datetime.now(datetime.UTC).isoformat(),
            })
            manifest = _write_run_record(root, run_id, base_record, log)
            print(f"[ingest:{target}] FAIL analyzeHeadless timed out; manifest={manifest}")
            return 1
        except OSError as exc:
            base_record.update({
                "status": "failed",
                "error": f"could not start analyzeHeadless: {exc}",
                "command": cmd,
                "finished_at": datetime.datetime.now(datetime.UTC).isoformat(),
            })
            manifest = _write_run_record(root, run_id, base_record, str(exc))
            print(f"[ingest:{target}] FAIL could not start analyzeHeadless; manifest={manifest}")
            return 1

        for line in log.splitlines():
            if "ExportFuncs" in line or "ERROR" in line or "Exception" in line:
                print("  " + line.strip())
        if result.returncode:
            error = f"analyzeHeadless returned {result.returncode}"
        else:
            error = None

        counts = None
        if error is None:
            try:
                metadata, n_asm, n_dec = _validate_export(outdir)
                stage = pathlib.Path(working_dir) / "staged"
                (stage / "asm").mkdir(parents=True)
                (stage / "decomp").mkdir()
                for source in (outdir / "asm").glob("*.s"):
                    shutil.copy2(source, stage / "asm" / source.name)
                if (outdir / "decomp").is_dir():
                    for source in (outdir / "decomp").glob("*.c"):
                        shutil.copy2(source, stage / "decomp" / source.name)
                shutil.copy2(outdir / "functions.json", stage / "functions.json")
                _publish_exports(stage, root)
                counts = {
                    "functions": len(metadata["functions"]),
                    "assembly": n_asm,
                    "decompiler": n_dec,
                }
            except (OSError, TypeError, ValueError) as exc:
                error = f"invalid Ghidra export: {exc}"

        base_record.update({
            "status": "failed" if error else "ready",
            "error": error,
            "command": cmd,
            "return_code": result.returncode,
            "finished_at": datetime.datetime.now(datetime.UTC).isoformat(),
            "exports": counts,
        })
        manifest = _write_run_record(root, run_id, base_record, log)
        if error:
            print(f"[ingest:{target}] FAIL {error}; manifest={manifest}")
            print("\n".join(log.splitlines()[-15:]))
            return 1

    print(
        f"[ingest:{target}] OK {counts['assembly']} asm, "
        f"{counts['decompiler']} decomp -> targets/{target}/{{asm,decomp}}; "
        f"manifest={manifest}"
    )
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--processor", default=None, help="e.g. 'x86:LE:16:Real Mode'")
    ap.add_argument("--timeout", type=int, default=1800)
    a = ap.parse_args()
    sys.exit(ingest(a.target, a.processor, a.timeout))
