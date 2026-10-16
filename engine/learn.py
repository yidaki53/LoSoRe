"""Learn: mine an ingested target into knowledge/knowledge.json (the "learning" step).

Reads (produced by ingest):
  targets/<slug>/functions.json   Ghidra metadata (compiler, language, fns)
  targets/<slug>/asm/<fn>.s       per-function instruction listing
  targets/<slug>/decomp/<fn>.c    decompiler output (few-shot "answer")

And config/target.yaml for compiler/platform/language.

Extracts, per (compiler, platform) toolchain:
  * calling conventions + image base (recipe)
  * instruction-idiom frequency (top prologues/bodies) — guides future drafts
  * few-shot examples: (asm head -> decomp C) for representative functions

Disc-gated: SKIP (pass) without functions.json. Idempotent: re-running merges
rather than duplicating. This is what makes the factory improve target-over-target.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import knowledge  # noqa: E402

# capture the mnemonic (first token after the address) from an asm line
_ADDR_MNEMONIC = re.compile(r"^\s*[0-9a-fA-F:]+\s+([A-Za-z][A-Za-z0-9]*)")
MAX_EXAMPLES_PER_TOOLCHAIN = 6
MAX_ASM_HEAD_LINES = 24


def _yaml_kv(path: pathlib.Path, key: str, default: str = "unknown") -> str:
    if not path.exists():
        return default
    for line in path.read_text().splitlines():
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip() or default
    return default


def _mnemonics(asm_text: str) -> list[str]:
    out = []
    for line in asm_text.splitlines():
        if line.startswith(";"):
            continue
        m = _ADDR_MNEMONIC.match(line)
        if m:
            out.append(m.group(1).upper())
    return out


def _asm_head(asm_text: str, n: int = MAX_ASM_HEAD_LINES) -> str:
    lines = [l for l in asm_text.splitlines() if l.strip()][:n]
    return "\n".join(lines)


def learn(target: str, store_path: pathlib.Path = knowledge.STORE) -> int:
    root = pathlib.Path("targets") / target
    fns_json = root / "functions.json"
    if not fns_json.exists():
        print(f"[learn:{target}] SKIP no functions.json (run ingest first)")
        return 0

    meta = json.loads(fns_json.read_text())
    yaml = root / "config" / "target.yaml"
    tcyaml = root / "config" / "toolchain.yaml"
    # Prefer the evidence-backed toolchain.yaml (written by provenance/detection);
    # fall back to target.yaml, then Ghidra metadata.
    compiler = _yaml_kv(tcyaml, "compiler", _yaml_kv(yaml, "compiler",
                 meta.get("compiler") or "unknown"))
    platform = _yaml_kv(tcyaml, "platform", _yaml_kv(yaml, "platform", "unknown"))
    language = _yaml_kv(tcyaml, "language", _yaml_kv(yaml, "language", "unknown"))
    confidence = _yaml_kv(tcyaml, "compiler_confidence", "low")
    key = knowledge.compiler_key(compiler, platform)

    data = knowledge.load(store_path)

    # --- recipe: calling conventions + image base (accumulate counts) ---
    cc = Counter()
    mnem = Counter()
    bigram = Counter()
    nfns = 0
    for f in meta.get("functions", []):
        nfns += 1
        if f.get("calling_convention"):
            cc[f["calling_convention"]] += 1
        asm_file = root / "asm" / (f["name"] + ".s")
        if not asm_file.exists():
            matches = list((root / "asm").glob(f["name"] + ".s"))
            asm_file = matches[0] if matches else None
        if asm_file and asm_file.exists():
            ms = _mnemonics(asm_file.read_text(errors="replace"))
            mnem.update(ms)
            bigram.update(" ".join(bg) for bg in zip(ms, ms[1:]))

    recipe = data["compilers"].setdefault(key, {
        "compiler": compiler, "platform": platform, "language": language,
        "compiler_confidence": confidence,
        "targets": [], "image_bases": [], "calling_conventions": {},
        "top_mnemonics": {}, "top_bigrams": {}, "functions_seen": 0,
    })
    recipe["language"] = language
    # keep the strongest confidence we've ever seen for this toolchain
    if knowledge._CONF_RANK.get(confidence, 0) > knowledge._CONF_RANK.get(
            recipe.get("compiler_confidence", "low"), 0):
        recipe["compiler_confidence"] = confidence
    if meta.get("image_base") and meta["image_base"] not in recipe["image_bases"]:
        recipe["image_bases"].append(meta["image_base"])
    for c, n in cc.items():
        recipe["calling_conventions"][c] = recipe["calling_conventions"].get(c, 0) + n
    recipe["top_mnemonics"] = dict(
        (Counter(recipe["top_mnemonics"]) + mnem).most_common(20))
    recipe["top_bigrams"] = dict(
        (Counter(recipe["top_bigrams"]) + bigram).most_common(20))
    recipe["functions_seen"] += nfns
    if target not in recipe["targets"]:
        recipe["targets"].append(target)

    # --- few-shot examples: representative fns with decompiled output ---
    # Gate: only high/medium-confidence toolchains contribute few-shot examples,
    # so a mis-detected toolchain can't leak wrong translations to other targets.
    may_seed_examples = knowledge.confidence_ok(
        {"compiler_confidence": recipe.get("compiler_confidence", "low")}, "medium")
    pool = [f for f in meta.get("functions", []) if f.get("decompiled")]
    pool.sort(key=lambda f: f.get("num_instructions", 0))
    chosen: list[dict] = []
    if pool:
        idxs = sorted(set([0, len(pool) // 3, len(pool) // 2,
                           (2 * len(pool)) // 3, len(pool) - 1]))
        chosen = [pool[i] for i in idxs]
    ex_key = data["examples"].setdefault(key, [])
    have = {(e["asm_head"][:60]) for e in ex_key}
    for f in chosen[:MAX_EXAMPLES_PER_TOOLCHAIN]:
        if not may_seed_examples:
            break
        asm_file = root / "asm" / (f["name"] + ".s")
        dec_file = root / "decomp" / (f["name"] + ".c")
        if not (asm_file.exists() and dec_file.exists()):
            continue
        asm_head = _asm_head(asm_file.read_text(errors="replace"))
        if asm_head[:60] in have:
            continue
        ex_key.append({
            "fn": f["name"], "target": target,
            "calling_convention": f.get("calling_convention"),
            "asm_head": asm_head,
            "c": dec_file.read_text(errors="replace")[:4000],
        })
    data["examples"][key] = data["examples"][key][-MAX_EXAMPLES_PER_TOOLCHAIN:]

    # --- per-target record ---
    data["targets"][target] = {
        "compiler": compiler, "platform": platform, "language": language,
        "compiler_confidence": recipe.get("compiler_confidence", "low"),
        "functions": nfns, "toolchain": key,
        "examples_added": (min(len(chosen), MAX_EXAMPLES_PER_TOOLCHAIN)
                           if may_seed_examples else 0),
    }

    knowledge.save(data, store_path)
    st = knowledge.stats(data)
    print(f"[learn:{target}] toolchain={key} fns={nfns} "
          f"examples={len(data['examples'][key])} "
          f"(store: {st['targets_seen']} targets, {st['toolchains_seen']} toolchains, "
          f"{st['examples_total']} examples)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--store", default=None)
    a = ap.parse_args()
    sys.exit(learn(a.target,
                   pathlib.Path(a.store) if a.store else knowledge.STORE))

