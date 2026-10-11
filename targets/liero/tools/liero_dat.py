"""Liero DAT settings parser (spec: liero.nl/lierohack/docformats/liero-dat.html).
Behavioral/format oracle material: parse BYOD LIERO.DAT -> JSON; parity vs spec offsets.
Disc-gated: SKIP without extracted/liero/LIERO.DAT."""
from __future__ import annotations
import argparse, json, pathlib, struct, sys

def parse_dat(p: pathlib.Path) -> dict:
    b = p.read_bytes()
    if len(b) < 0x9B:
        raise ValueError(f"short DAT: {len(b)}")
    return {
        "max_bonuses": b[0x00],
        "loading_times": struct.unpack_from("<H", b, 0x01)[0],
        "lives": struct.unpack_from("<h", b, 0x03)[0],
        "game_mode": b[0x10],
        "weapons_p1": list(b[0x42:0x47]),
        "weapons_p2": list(b[0x47:0x4C]),
        "health_p1": struct.unpack_from("<h", b, 0x4C)[0],
        "health_p2": struct.unpack_from("<h", b, 0x4E)[0],
    }

def main(target: str = "liero") -> int:
    p = pathlib.Path(f"extracted/{target}/LIERO.DAT")
    if not p.exists():
        print(f"[liero-dat] SKIP no BYOD at {p}")
        return 0
    print(json.dumps(parse_dat(p), indent=2))
    return 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="liero")
    a = ap.parse_args()
    sys.exit(main(a.target))
