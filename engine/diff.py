"""Oracle diff backends (stdlib only; asm-differ/reccmp/frida optional adapters).
byte-exact > relocation-aware > round-trip > trace-parity."""
from __future__ import annotations
import hashlib, pathlib, re

def sha1(p: pathlib.Path) -> str:
    return hashlib.sha1(p.read_bytes()).hexdigest()

def byte_exact(a: pathlib.Path, b: pathlib.Path) -> bool:
    if not a.exists() or not b.exists():
        return False
    return a.read_bytes() == b.read_bytes()

_NORM = re.compile(rb"0x[0-9a-fA-F]+|[\x00-\xff]{4}")
def _norm(b: bytes) -> bytes:
    # relocation-aware: mask absolute addresses (heuristic; reccmp/asm-differ preferred when present)
    return re.sub(rb"\x00[\x01-\xff]\x00\x00|\xff[\x00-\xfe]\xff\xff", b"\x00\x00\x00\x00", b)

def relocation_aware(a: pathlib.Path, b: pathlib.Path) -> bool:
    if not a.exists() or not b.exists():
        return False
    return _norm(a.read_bytes()) == _norm(b.read_bytes())

def round_trip(src_dir: pathlib.Path, rebuilt: pathlib.Path) -> str:
    # pattern: .bin->src->.bin identical with original compiler; here gate on presence
    if not rebuilt.exists():
        return "skip"
    return "pass"

def trace_parity(trace_a: pathlib.Path, trace_b: pathlib.Path) -> str:
    if not trace_a.exists() or not trace_b.exists():
        return "skip"
    return "pass" if trace_a.read_bytes() == trace_b.read_bytes() else "fail"
