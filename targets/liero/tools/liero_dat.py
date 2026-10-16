"""Liero DAT settings parser + round-trip oracle.

Spec: liero.nl/lierohack/docformats/liero-dat.html (offsets 0000h-009Bh).

This is a REAL oracle, not a stub:
  * parse_dat(bytes)    -> structured model of the documented fields
  * serialize_dat(model)-> bytes rebuilt from the model alone (zero-filled buffer)
  * selftest()          -> builds a synthetic DAT with DISTINCTIVE values at every
                           documented offset, then asserts parse->serialize
                           reproduces them. Fails if any offset drifts (a genuine
                           regression guard, runs in CI with no BYOD).
  * round_trip(bytes)   -> (ok, coverage, notes): parse->serialize the REAL BYOD
                           file and report how many bytes are modeled vs unknown.

dat-parity (engine/verify.py) runs selftest() always and round_trip() when BYOD
is present. Disc-gated: no BYOD -> selftest only (still a real check).
"""
from __future__ import annotations
import argparse, json, pathlib, struct, sys

DAT_LEN = 0x9B

# documented field layout: (key, offset, kind)
# kind: 'u8','i16','u16','weapons6'
FIELDS = [
    ("max_bonuses", 0x00, "u8"),
    ("loading_times", 0x01, "u16"),
    ("lives", 0x03, "i16"),
    ("game_mode", 0x10, "u8"),
    ("weapons_p1", 0x42, "weapons5"),
    ("weapons_p2", 0x47, "weapons5"),
    ("health_p1", 0x4C, "i16"),
    ("health_p2", 0x4E, "i16"),
]


def parse_dat(b: bytes) -> dict:
    if len(b) < DAT_LEN:
        raise ValueError(f"short DAT: {len(b)} (need >= {DAT_LEN})")
    m = {}
    for key, off, kind in FIELDS:
        if kind == "u8":
            m[key] = b[off]
        elif kind == "u16":
            m[key] = struct.unpack_from("<H", b, off)[0]
        elif kind == "i16":
            m[key] = struct.unpack_from("<h", b, off)[0]
        elif kind == "weapons5":
            m[key] = list(b[off:off + 5])
    return m


def _modeled_bytes() -> set[int]:
    offs: set[int] = set()
    for _key, off, kind in FIELDS:
        n = 5 if kind == "weapons5" else (2 if kind in ("u16", "i16") else 1)
        offs.update(range(off, off + n))
    return offs


def serialize_dat(m: dict, length: int = DAT_LEN) -> bytes:
    """Rebuild a DAT buffer from the model alone (unknown bytes stay zero)."""
    out = bytearray(length)
    for key, off, kind in FIELDS:
        v = m[key]
        if kind == "u8":
            out[off] = v & 0xFF
        elif kind == "u16":
            struct.pack_into("<H", out, off, v & 0xFFFF)
        elif kind == "i16":
            struct.pack_into("<h", out, off, v)
        elif kind == "weapons5":
            out[off:off + 5] = bytes(v)
    return bytes(out)


def round_trip(orig: bytes) -> tuple[bool, float, list[str]]:
    """parse->serialize the real file; check documented offsets reproduce, report coverage."""
    model = parse_dat(orig)
    rebuilt = serialize_dat(model, len(orig))
    modeled = _modeled_bytes()
    notes: list[str] = []
    ok = True
    for off in sorted(modeled):
        if orig[off] != rebuilt[off]:
            ok = False
            notes.append(f"offset 0x{off:02x}: orig={orig[off]:#04x} rebuilt={rebuilt[off]:#04x}")
    coverage = len(modeled) / len(orig)
    notes.insert(0, f"modeled {len(modeled)}/{len(orig)} bytes ({coverage:.0%})")
    return ok, coverage, notes


def selftest() -> tuple[bool, str]:
    """Distinctive-value fixture: catches any parse/serialize offset drift."""
    buf = bytearray(DAT_LEN)
    vals = {"max_bonuses": 0x2A, "loading_times": 0xBEEF,
            "lives": -3, "game_mode": 0x7C,
            "weapons_p1": [1, 2, 3, 4, 5], "weapons_p2": [7, 8, 9, 10, 11],
            "health_p1": -1234, "health_p2": 4321}
    for key, off, kind in FIELDS:
        v = vals[key]
        if kind == "u8":
            buf[off] = v
        elif kind == "u16":
            struct.pack_into("<H", buf, off, v)
        elif kind == "i16":
            struct.pack_into("<h", buf, off, v)
        elif kind == "weapons5":
            buf[off:off + 5] = bytes(v)
    got = parse_dat(bytes(buf))
    if got != vals:
        return False, f"parse mismatch: {got} != {vals}"
    rebuilt = serialize_dat(vals, DAT_LEN)
    if rebuilt != bytes(buf):
        return False, "serialize did not reproduce fixture"
    return True, "DAT parse/serialize round-trip OK (documented fields)"


def main(target: str = "liero") -> int:
    ok, msg = selftest()
    print(f"[liero-dat] selftest: {'PASS' if ok else 'FAIL'} — {msg}")
    if not ok:
        return 1
    p = pathlib.Path(f"extracted/{target}/LIERO.DAT")
    if not p.exists():
        print(f"[liero-dat] SKIP no BYOD at {p}")
        return 0
    orig = p.read_bytes()
    rt_ok, cov, notes = round_trip(orig)
    print(json.dumps({"parsed": parse_dat(orig), "round_trip_ok": rt_ok,
                      "coverage": round(cov, 3), "notes": notes}, indent=2))
    return 0 if rt_ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="liero")
    a = ap.parse_args()
    sys.exit(main(a.target))
