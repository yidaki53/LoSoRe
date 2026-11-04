"""Oracle: archive byte integrity only, never execution or semantic acceptance.

The legacy artifacts.json format is retained exactly. Unlisted files are allowed
for historical post-seal reviews, but are not returned or trusted. Listed members
and the index are read through no-follow directory descriptors and returned as an
immutable snapshot. The archive root's parent location is caller-selected.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import stat
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from types import MappingProxyType
from typing import TypeVar, overload

INDEX = "artifacts.json"
_Default = TypeVar("_Default")


class ArchiveError(ValueError):
    """Oracle: explicit invalid, unsafe, changed or incomplete archive."""


@dataclass(frozen=True)
class _Members(Mapping[str, bytes]):
    """Oracle: privately owned immutable validated bytes."""

    _members: Mapping[str, bytes]

    def __getitem__(self, name: str) -> bytes:
        """Oracle: absent semantic inputs cannot fall back to unlisted paths."""
        try:
            return self._members[name]
        except KeyError as exc:
            raise ArchiveError("archive member missing: " + name) from exc

    def __iter__(self) -> Iterator[str]:
        """Oracle: immutable snapshot member names."""
        return iter(self._members)

    def __len__(self) -> int:
        """Oracle: immutable snapshot member count."""
        return len(self._members)

    def __contains__(self, name: object) -> bool:
        """Oracle: membership queries do not read paths or require missing bytes."""
        return name in self._members

    @overload
    def get(self, name: str) -> bytes | None:
        """Oracle: an absent optional member returns None."""

    @overload
    def get(self, name: str, default: bytes) -> bytes:
        """Oracle: a byte default preserves the member value type."""

    @overload
    def get(self, name: str, default: _Default) -> bytes | _Default:
        """Oracle: an absent optional member preserves the supplied default."""

    def get(
        self, name: str, default: _Default | None = None
    ) -> bytes | _Default | None:
        """Oracle: optional metadata lookup retains normal mapping behavior."""
        return self._members.get(name, default)


def _parts(name: str) -> tuple[str, ...]:
    """Oracle: canonical relative POSIX paths, without traversal or aliases."""
    if (
        not isinstance(name, str)
        or not name
        or "\\" in name
        or ":" in name
        or "\0" in name
        or any(part in {"", ".", ".."} for part in name.split("/"))
    ):
        raise ArchiveError(f"unsafe archive path: {name!r}")
    return tuple(name.split("/"))


@contextmanager
def _directory(path: pathlib.Path):
    """Oracle: pin caller-selected root, rejecting a symlink or non-directory."""
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        yield fd
    finally:
        os.close(fd)


def _read_member(root_fd: int, name: str) -> bytes:
    """Oracle: no-follow descriptor traversal and regular-file byte snapshot."""
    parts = _parts(name)
    directory = os.dup(root_fd)
    try:
        for part in parts[:-1]:
            child = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory
            )
            os.close(directory)
            directory = child
        fd = os.open(
            parts[-1],
            os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
            dir_fd=directory,
        )
        with os.fdopen(fd, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise ArchiveError("archive member is not regular: " + name)
            return stream.read()
    finally:
        os.close(directory)


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    """Oracle: duplicate JSON keys cannot hide a conflicting member identity."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ArchiveError("duplicate archive manifest key: " + key)
        result[key] = value
    return result


def read_archive(root: pathlib.Path) -> Mapping[str, bytes]:
    """Oracle: immutable hash-validated listed bytes plus exact index bytes.

    Unlisted historical additions remain outside this snapshot and must have
    separate routine-owned review checks. No executable is imported or run.
    """
    try:
        with _directory(root) as fd:
            index = _read_member(fd, INDEX)
            manifest = json.loads(index, object_pairs_hook=_unique_object)
            if not isinstance(manifest, dict) or not manifest:
                raise ArchiveError("archive manifest must be a nonempty object")
            members = {INDEX: index}
            for name, digest in manifest.items():
                _parts(name)
                if name == INDEX:
                    raise ArchiveError("archive manifest references itself")
                if not isinstance(digest, str) or not re.fullmatch(
                    r"[0-9a-f]{64}", digest
                ):
                    raise ArchiveError("malformed archive SHA256: " + name)
                payload = _read_member(fd, name)
                if hashlib.sha256(payload).hexdigest() != digest:
                    raise ArchiveError("archive artifact changed: " + name)
                members[name] = payload
            return _Members(MappingProxyType(members))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ArchiveError(f"cannot read archive {root}: {exc}") from exc


def _file_names(fd: int, prefix: str = "") -> Iterator[str]:
    """Oracle: seal all regular files, rejecting symlinks and special files."""
    with os.scandir(fd) as entries:
        for entry in entries:
            name = prefix + entry.name
            _parts(name)
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                child = os.open(
                    entry.name,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=fd,
                )
                try:
                    yield from _file_names(child, name + "/")
                finally:
                    os.close(child)
            elif stat.S_ISREG(mode):
                yield name
            else:
                raise ArchiveError("archive member is not regular: " + name)


def seal_archive(root: pathlib.Path) -> None:
    """Oracle: one-time legacy index creation; no acceptance or resealing.

    Callers must finish writes before sealing. A concurrent mutation may make
    an archive fail subsequent reading; it can never change returned snapshots.
    """
    try:
        with _directory(root) as fd:
            if INDEX in os.listdir(fd):
                raise ArchiveError("archive already sealed")
            names = sorted(_file_names(fd))
            if not names:
                raise ArchiveError("cannot seal empty archive")
            manifest = {
                name: hashlib.sha256(_read_member(fd, name)).hexdigest()
                for name in names
            }
            payload = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
            index_fd = os.open(
                INDEX,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o666,
                dir_fd=fd,
            )
            with os.fdopen(index_fd, "wb") as stream:
                stream.write(payload)
    except OSError as exc:
        raise ArchiveError(f"cannot seal archive {root}: {exc}") from exc
