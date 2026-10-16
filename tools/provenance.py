"""Provenance gate: BYOD hash-gate + evidence-backed compiler/language detection.

Detection is now the GATE for same-language drafting: it writes a machine-readable
config/toolchain.yaml (compiler, compiler_confidence, language, platform, evidence)
that engine/draft.py and engine/learn.py consume. A target may not be drafted until
its language is known (see draft.py). Disc-gated: SKIP in CI (no BYOD).

Non-destructive by design: hand-curated research above the AUTO marker in
PROVENANCE.md is preserved across runs; only the machine-generated hash block
between the markers is regenerated. Running the pipeline is idempotent.
"""
from __future__ import annotations
import argparse
import datetime as _dt
import hashlib
import pathlib
import sys

BEGIN = "<!-- BEGIN AUTO (tools/provenance.py) -->"
END = "<!-- END AUTO -->"

# signature -> (compiler_label, language or None, strength)
# strength 'strong' defines the language; 'medium' only hints a compiler family.
SIGS = {
    b"Portions Copyright (c) 1983,92 Borland": ("turbo-pascal-7", "pascal", "strong"),
    b"Turbo Pascal": ("turbo-pascal", "pascal", "strong"),
    b"Runtime error": ("borland-rtl", "pascal", "strong"),
    b"Borland": ("borland", None, "medium"),
    b"Open Watcom": ("open-watcom", "c", "strong"),
    b"Watcom": ("watcom", "c", "medium"),
    b"DJGPP": ("djgpp", "c", "strong"),
    b"go32": ("djgpp", "c", "medium"),
    b"MSVCRT": ("msvc", "c", "medium"),
    b"Microsoft Visual": ("msvc", "c", "strong"),
    b"GCC: ": ("gcc", "c", "strong"),
    b"psy-q": ("psy-q", "c", "strong"),
    b"Psy-Q": ("psy-q", "c", "strong"),
}


def sha1(p: pathlib.Path) -> str:
    h = hashlib.sha1()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def compiler_id(blob: bytes) -> str:
    """Legacy per-file label (kept for the PROVENANCE.md AUTO block / existing tests)."""
    hits = []
    for k, (label, _lang, strength) in SIGS.items():
        if k.lower() in blob.lower():
            hits.append(label + ("?" if strength == "medium" else ""))
    # dedupe preserving order
    seen, out = set(), []
    for h in hits:
        if h not in seen:
            seen.add(h); out.append(h)
    return ",".join(out) if out else "unknown"


def detect_toolchain(byod: pathlib.Path) -> dict:
    """Scan BYOD executables/text for compiler + language signatures.

    Returns dict: compiler, compiler_confidence, language, platform, evidence[list].
    Confidence: high = a language-defining (strong) signature; medium = only a
    compiler-family (medium) signature; low = nothing definitive.
    """
    files = [p for p in byod.rglob("*") if p.is_file()]
    evidence: list[str] = []
    strong_langs: dict[str, int] = {}   # language -> count of strong hits
    strong_comps: dict[str, int] = {}
    medium_comps: dict[str, int] = {}
    saw_mz = False

    for p in files[:200]:
        try:
            blob = p.read_bytes()[:1 << 20]
        except OSError:
            continue
        if blob[:2] == b"MZ":
            saw_mz = True
        low = blob.lower()
        for k, (label, lang, strength) in SIGS.items():
            if k.lower() in low:
                snippet = k.decode("ascii", "replace")
                evidence.append(f'{p.name}: "{snippet}" ({strength})')
                if strength == "strong":
                    if lang:
                        strong_langs[lang] = strong_langs.get(lang, 0) + 1
                    strong_comps[label] = strong_comps.get(label, 0) + 1
                else:
                    medium_comps[label] = medium_comps.get(label, 0) + 1

    # compiler choice: prefer a strong label; refine generic borland->tp7 when RTL present
    compiler = "unknown"
    if strong_comps:
        compiler = max(strong_comps, key=strong_comps.get)
    elif medium_comps:
        compiler = max(medium_comps, key=medium_comps.get)
    # 'borland-rtl'/'borland' with an MZ binary strongly implies TP7
    if compiler in ("borland", "borland-rtl") and (saw_mz or "borland-rtl" in strong_comps):
        compiler = "turbo-pascal-7"

    language = "unknown"
    if strong_langs:
        language = max(strong_langs, key=strong_langs.get)
    elif strong_comps:
        # infer from the compiler label's canonical language if known
        for k, (label, lang, _s) in SIGS.items():
            if label == compiler and lang:
                language = lang
                break

    if strong_langs or (compiler != "unknown" and strong_comps):
        confidence = "high"
    elif medium_comps or compiler != "unknown":
        confidence = "medium"
    else:
        confidence = "low"

    platform = "dos" if saw_mz else "unknown"
    if saw_mz:
        evidence.append("(format) MZ executable (DOS real-mode)")
    return {"compiler": compiler, "compiler_confidence": confidence,
            "language": language, "platform": platform, "evidence": evidence}


def _write_toolchain_yaml(target: str, tc: dict, platform_override: str | None) -> pathlib.Path:
    out = pathlib.Path(f"targets/{target}/config/toolchain.yaml")
    out.parent.mkdir(parents=True, exist_ok=True)
    platform = platform_override or tc["platform"]
    lines = [
        f"slug: {target}",
        f"compiler: {tc['compiler']}",
        f"compiler_confidence: {tc['compiler_confidence']}",
        f"language: {tc['language']}",
        f"platform: {platform}",
        f"detected: {_dt.date.today().isoformat()}",
    ]
    if tc["evidence"]:
        lines.append("evidence:")
        lines += [f"  - {e}" for e in tc["evidence"]]
    out.write_text("\n".join(lines) + "\n")
    return out


def provenance(target: str, byod: pathlib.Path, platform: str | None = None) -> int:
    out = pathlib.Path(f"targets/{target}/docs/PROVENANCE.md")
    if not byod.exists():
        print(f"[provenance:{target}] SKIP no BYOD at {byod}")
        return 0
    files = [p for p in byod.rglob("*") if p.is_file()]
    tc = detect_toolchain(byod)
    tcyaml = _write_toolchain_yaml(target, tc, platform)

    auto = [BEGIN, f"- files: {len(files)}",
            f"- detected toolchain: {tc['compiler']} ({tc['compiler_confidence']}), "
            f"language={tc['language']}, platform={platform or tc['platform']}"]
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
    print(f"[provenance:{target}] {tc['compiler']} ({tc['compiler_confidence']}), "
          f"language={tc['language']} -> {tcyaml}; wrote {out} "
          f"({len(files)} files, research preserved)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--byod", default=None)
    ap.add_argument("--platform", default=None)
    a = ap.parse_args()
    t = a.target
    sys.exit(provenance(t, pathlib.Path(a.byod or f"extracted/{t}"), a.platform))
