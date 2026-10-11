"""Provenance gate: BYOD hash-gate + compiler ID via strings/magic. Disc-gated: SKIP in CI.

Non-destructive by design: hand-curated research above the AUTO marker is
preserved across runs; only the machine-generated hash block between the markers
is regenerated. Running the pipeline is idempotent and never erases findings.
"""
from __future__ import annotations
import argparse
import hashlib
import pathlib
import sys

SIGS = {b"Watcom": "watcom?", b"Borland": "borland?", b"DJGPP": "djgpp?",
        b"Microsoft": "msvc?", b"GCC:": "gcc?", b"psy-q": "psy-q?", b"MIPS": "mips?"}

BEGIN = "<!-- BEGIN AUTO (tools/provenance.py) -->"
END = "<!-- END AUTO -->"

def sha1(p: pathlib.Path) -> str:
    h = hashlib.sha1()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def compiler_id(blob: bytes) -> str:
    hits = [v for k, v in SIGS.items() if k.lower() in blob.lower()]
    return ",".join(hits) if hits else "unknown"

def provenance(target: str, byod: pathlib.Path) -> int:
    out = pathlib.Path(f"targets/{target}/docs/PROVENANCE.md")
    if not byod.exists():
        print(f"[provenance:{target}] SKIP no BYOD at {byod}")
        return 0
    files = [p for p in byod.rglob("*") if p.is_file()]
    auto = [BEGIN, f"- files: {len(files)}"]
    for p in files[:50]:
        blob = p.read_bytes()[:1 << 20]
        auto.append(f"- {p.name}: sha1={sha1(p)[:16]} compiler~{compiler_id(blob)}")
    auto.append(END)
    # Preserve curated research above the marker; regenerate only the AUTO block.
    head = f"# {target} provenance"
    if out.exists():
        existing = out.read_text()
        head = existing.split(BEGIN, 1)[0].rstrip("\n") if BEGIN in existing else existing.rstrip("\n")
        if not head.strip():
            head = f"# {target} provenance"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head + "\n\n" + "\n".join(auto) + "\n")
    print(f"[provenance:{target}] wrote {out} ({len(files)} files, research preserved)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--game", default=None, help="deprecated alias for --target")
    ap.add_argument("--byod", default=None)
    a = ap.parse_args()
    t = a.target or a.game
    sys.exit(provenance(t, pathlib.Path(a.byod or f"extracted/{t}")))
