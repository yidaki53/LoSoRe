"""Oracle: archive integrity and immutable replay inputs, not recovery acceptance."""

import hashlib
import json
import operator
import os
import subprocess

import pytest

from engine.evidence_archive import ArchiveError, read_archive, seal_archive
from tools import liero_move_caller as move
from tools import liero_nibble_caller as nibble
from tools import liero_source_trial as trial


def _digest(payload):
    """Oracle: exact fixture byte identity."""
    return hashlib.sha256(payload).hexdigest()


def _index(root, manifest):
    """Oracle: legacy index fixture without trial execution."""
    (root / "artifacts.json").write_text(json.dumps(manifest))


@pytest.mark.parametrize("mutation", ["setitem"])
def test_legacy_index_and_immutable_snapshot(tmp_path, monkeypatch, mutation):
    """Oracle: original format and retained bytes, never validate then reopen."""
    (tmp_path / "nested").mkdir()
    payload = b"\x00\xfforiginal"
    (tmp_path / "nested/TRACE.BIN").write_bytes(payload)
    seal_archive(tmp_path)
    expected = {"nested/TRACE.BIN": _digest(payload)}
    assert (tmp_path / "artifacts.json").read_text() == (
        json.dumps(expected, indent=2, sort_keys=True) + "\n"
    )
    snapshot = read_archive(tmp_path)
    (tmp_path / "nested/TRACE.BIN").write_bytes(b"changed")
    (tmp_path / "artifacts.json").unlink()

    def forbidden(*args, **kwargs):
        """Oracle: snapshot access must not perform additional filesystem reads."""
        pytest.fail("reopened archive")

    monkeypatch.setattr(os, "open", forbidden)
    assert snapshot["nested/TRACE.BIN"] == payload
    assert snapshot.get("nested/TRACE.BIN") == payload
    assert snapshot.get("unlisted") is None
    assert snapshot.get("unlisted", b"default") == b"default"
    sentinel = object()
    assert snapshot.get("unlisted", sentinel) is sentinel
    assert json.loads(snapshot["artifacts.json"]) == expected
    with pytest.raises(TypeError):
        getattr(operator, mutation)(snapshot, "nested/TRACE.BIN", b"other")
    with pytest.raises(ArchiveError, match="missing"):
        snapshot["unlisted"]


@pytest.mark.parametrize(
    "name",
    [
        "/absolute",
        "../outside",
        "nested/../../outside",
        "./alias",
        "nested/../alias",
        "nested//alias",
        "nested/./alias",
        "nested/",
        "",
        r"nested\alias",
        "C:/outside",
        "nul\0name",
    ],
)
def test_noncanonical_paths_rejected(tmp_path, name):
    """Oracle: no escaping, platform aliases or normalized path duplicates."""
    _index(tmp_path, {name: "0" * 64})
    with pytest.raises(ArchiveError, match="unsafe"):
        read_archive(tmp_path)


@pytest.mark.parametrize(
    "digest", [True, False, None, 1, [], {}, "", "a" * 63, "A" * 64, "z" * 64]
)
def test_digest_format_rejected(tmp_path, digest):
    """Oracle: only canonical lowercase SHA256 strings are identities."""
    (tmp_path / "member").write_bytes(b"data")
    _index(tmp_path, {"member": digest})
    with pytest.raises(ArchiveError, match="SHA256"):
        read_archive(tmp_path)


@pytest.mark.parametrize("index", [b"{", b"\xff", b"[]", b"null", b"true", b"{}"])
def test_malformed_or_empty_index_rejected(tmp_path, index):
    """Oracle: malformed, non-object and empty archives have no validated inputs."""
    (tmp_path / "artifacts.json").write_bytes(index)
    with pytest.raises(ArchiveError):
        read_archive(tmp_path)


def test_duplicate_manifest_keys_and_self_reference(tmp_path):
    """Oracle: index ambiguity or circular index identity is rejected."""
    digest = "0" * 64
    (tmp_path / "artifacts.json").write_text(
        f'{{"member":"{digest}","member":"{digest}"}}'
    )
    with pytest.raises(ArchiveError, match="duplicate"):
        read_archive(tmp_path)
    _index(tmp_path, {"artifacts.json": digest})
    with pytest.raises(ArchiveError, match="itself"):
        read_archive(tmp_path)


def test_missing_changed_and_partial_members(tmp_path):
    """Oracle: index and every listed member must exist and match completely."""
    with pytest.raises(ArchiveError, match="cannot read"):
        read_archive(tmp_path)
    _index(tmp_path, {"member": _digest(b"complete")})
    with pytest.raises(ArchiveError, match="cannot read"):
        read_archive(tmp_path)
    for payload in (b"complet", b"changed!"):
        (tmp_path / "member").write_bytes(payload)
        with pytest.raises(ArchiveError, match="artifact changed"):
            read_archive(tmp_path)


@pytest.mark.parametrize("kind", ["file", "directory", "index", "root"])
def test_symlink_members_and_roots_rejected(tmp_path, kind):
    """Oracle: no-follow traversal rejects internal aliases as well as escapes."""
    archive = tmp_path / "archive"
    archive.mkdir()
    real = tmp_path / "real"
    real.mkdir()
    (real / "member").write_bytes(b"data")
    if kind == "file":
        (archive / "member").symlink_to(real / "member")
        _index(archive, {"member": _digest(b"data")})
    elif kind == "directory":
        (archive / "nested").symlink_to(real, target_is_directory=True)
        _index(archive, {"nested/member": _digest(b"data")})
    elif kind == "index":
        _index(real, {"member": _digest(b"data")})
        (archive / "artifacts.json").symlink_to(real / "artifacts.json")
    else:
        (archive / "member").write_bytes(b"data")
        seal_archive(archive)
        alias = tmp_path / "alias"
        alias.symlink_to(archive, target_is_directory=True)
        with pytest.raises(ArchiveError):
            read_archive(alias)
        with pytest.raises(ArchiveError):
            seal_archive(alias)
        return
    with pytest.raises(ArchiveError):
        read_archive(archive)


@pytest.mark.parametrize("kind", ["file", "directory", "fifo"])
def test_seal_refuses_symlinks_and_special_files(tmp_path, kind):
    """Oracle: seal must not follow symlinks or block on a FIFO."""
    if kind == "fifo":
        os.mkfifo(tmp_path / "member")
    else:
        (tmp_path / "real").mkdir()
        (tmp_path / "real/member").write_bytes(b"data")
        target = tmp_path / ("real" if kind == "directory" else "real/member")
        (tmp_path / "alias").symlink_to(target, target_is_directory=kind == "directory")
    with pytest.raises(ArchiveError, match="not regular"):
        seal_archive(tmp_path)
    assert not (tmp_path / "artifacts.json").exists()


def test_listed_special_file_rejected_without_blocking(tmp_path):
    """Oracle: malformed archives cannot cause a FIFO read to block."""
    os.mkfifo(tmp_path / "member")
    _index(tmp_path, {"member": _digest(b"")})
    with pytest.raises(ArchiveError, match="not regular"):
        read_archive(tmp_path)


def test_reseal_and_empty_archive_refused(tmp_path):
    """Oracle: sealing cannot repair or overwrite historical identities."""
    with pytest.raises(ArchiveError, match="empty"):
        seal_archive(tmp_path)
    (tmp_path / "member").write_bytes(b"first")
    seal_archive(tmp_path)
    original_index = (tmp_path / "artifacts.json").read_bytes()
    (tmp_path / "member").write_bytes(b"second")
    with pytest.raises(ArchiveError, match="already sealed"):
        seal_archive(tmp_path)
    assert (tmp_path / "artifacts.json").read_bytes() == original_index


def test_historical_unlisted_reviews_are_not_archive_evidence(tmp_path):
    """Oracle: historical post-seal review additions require separate bindings."""
    (tmp_path / "result.json").write_text('{"status":"failed"}')
    seal_archive(tmp_path)
    index = (tmp_path / "artifacts.json").read_bytes()
    (tmp_path / "review.json").write_text('{"status":"reviewed"}')
    snapshot = read_archive(tmp_path)
    assert snapshot["artifacts.json"] == index
    assert json.loads(snapshot["result.json"])["status"] == "failed"
    assert "review.json" not in snapshot
    with pytest.raises(ArchiveError, match="missing"):
        snapshot["review.json"]


def test_read_does_not_execute_or_promote(tmp_path, monkeypatch):
    """Oracle: reading a failed archive never executes its archived programs."""
    (tmp_path / "program.py").write_text("raise RuntimeError('executed')")
    (tmp_path / "result.json").write_text('{"status":"failed"}')
    seal_archive(tmp_path)

    def forbidden(*args, **kwargs):
        """Oracle: no external program execution during archive reading."""
        pytest.fail("executed archive")

    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(os, "system", forbidden)
    assert json.loads(read_archive(tmp_path)["result.json"])["status"] == "failed"


@pytest.mark.parametrize("replay", ["nibble", "cursor", "move", "packed", "source"])
def test_missing_frozen_shared_method_rejected(tmp_path, monkeypatch, replay):
    """Oracle: new shared-method claims must bind an archived implementation."""
    frozen = {
        "contract": {},
        "method_hashes": {"engine/evidence_archive.py": "0" * 64},
        "candidate_sha256": _digest(b"candidate"),
        "binary_sha256": "binary",
        "regions": {},
        "source_hashes": {"engine/evidence_archive.py": "0" * 64},
    }
    (tmp_path / "candidate").mkdir()
    (tmp_path / "candidate/candidate.inc").write_bytes(b"candidate")
    trial.pilot.save(tmp_path / "freeze.json", frozen)
    seal_archive(tmp_path)
    monkeypatch.setattr(nibble, "contract", lambda root: {})
    monkeypatch.setattr(nibble, "cursor_contract", lambda root: {})
    monkeypatch.setattr(move, "caller_contract", lambda root, **kwargs: {})
    monkeypatch.setattr(move, "packed_caller_contract", lambda root: {})
    monkeypatch.setattr(trial.pilot, "digest", lambda path: "binary")
    functions = {
        "nibble": nibble.replay,
        "cursor": nibble.replay_cursor,
        "move": move.replay,
        "packed": move.replay_packed,
        "source": trial.validate_artifacts,
    }
    with pytest.raises(ArchiveError, match="evidence_archive.py"):
        functions[replay](trial.ROOT, tmp_path)


def test_historical_source_method_set_and_failed_status_retained(tmp_path, monkeypatch):
    """Oracle: old frozen method sets remain valid, without inferred new evidence."""
    frozen = {
        "binary_sha256": "binary",
        "regions": {},
        "source_hashes": {},
    }
    result = {"routines": {}, "status": "failed", "whole_routine_accepted": False}
    trial.pilot.save(tmp_path / "freeze.json", frozen)
    trial.pilot.save(tmp_path / "result.json", result)
    seal_archive(tmp_path)
    monkeypatch.setattr(trial.pilot, "digest", lambda path: "binary")
    assert trial.validate_artifacts(trial.ROOT, tmp_path, historical=True) == result


def test_source_replay_uses_validated_snapshot_after_disk_changes(
    tmp_path, monkeypatch
):
    """Oracle: replay consumes exact checked JSON/method bytes, not reopened paths."""
    method = b"frozen shared method"
    (tmp_path / "sources").mkdir()
    (tmp_path / "sources/evidence_archive.py").write_bytes(method)
    frozen = {
        "binary_sha256": "binary",
        "regions": {},
        "source_hashes": {"engine/evidence_archive.py": _digest(method)},
    }
    result = {"routines": {}, "status": "failed"}
    trial.pilot.save(tmp_path / "freeze.json", frozen)
    trial.pilot.save(tmp_path / "result.json", result)
    seal_archive(tmp_path)

    def read_then_change(path):
        """Oracle: disk mutation after validation cannot supply replay inputs."""
        snapshot = read_archive(path)
        (path / "freeze.json").write_text("malformed")
        (path / "result.json").write_text('{"status":"passed"}')
        (path / "sources/evidence_archive.py").write_bytes(b"changed")
        return snapshot

    def original_digest(path):
        """Oracle: only the routine-owned original binary remains path-based."""
        assert path == trial.ROOT / "extracted/liero/LIERO.EXE"
        return "binary"

    monkeypatch.setattr(trial, "read_archive", read_then_change)
    monkeypatch.setattr(trial.pilot, "digest", original_digest)
    assert trial.validate_artifacts(trial.ROOT, tmp_path, historical=True) == result
