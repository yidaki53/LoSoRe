"""Oracle recommender: suggest which oracle to use for a new target.

Based on what worked for similar targets (same compiler/platform/toolchain)
in the knowledge base. Reduces manual setup when onboarding new projects.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import knowledge  # noqa: E402

ORACLES = ["byte-exact", "relocation-aware", "round-trip", "trace-parity", "dat-parity"]


def recommend_oracle(target: str, compiler: str, platform: str,
                     data: dict | None = None) -> str:
    """Recommend an oracle type for `target`.

    Heuristic:
      1. If another target with the same toolchain succeeded with a specific
         oracle, recommend that one.
      2. If the target has LIERO.DAT in BYOD and a tools/liero_dat.py exists,
         recommend dat-parity.
      3. Default to byte-exact.
    """
    if data is None:
        data = knowledge.load()
    key = knowledge.compiler_key(compiler, platform)
    tc = data.get("compilers", {}).get(key, {})

    # Look at verified oracles used by prior targets with same toolchain
    verified_oracles: dict[str, int] = {}
    for tname, trec in data.get("targets", {}).items():
        if trec.get("toolchain") != key:
            continue
        for oracle, relpaths in trec.get("verified", {}).items():
            if relpaths:
                verified_oracles[oracle] = verified_oracles.get(oracle, 0) + 1

    if verified_oracles:
        # Return the most-used successful oracle
        best = max(verified_oracles.items(), key=lambda kv: kv[1])[0]
        return best

    # Check if this target has a DAT oracle available
    root = pathlib.Path(f"targets/{target}")
    dat_oracle = root / "tools" / "liero_dat.py"
    if dat_oracle.exists():
        return "dat-parity"

    return "byte-exact"


def suggest_build_sha1_entries(target: str, oracle: str) -> list[str]:
    """Suggest build.sha1 entries for a target based on its asm files.

    Returns lines like '<sha1> <relpath>' for each asm function file.
    The actual sha1 values are placeholders — the user fills them in
    after the first successful build.
    """
    root = pathlib.Path(f"targets/{target}")
    asm_dir = root / "asm"
    if not asm_dir.exists():
        return []
    entries = []
    for asm_file in sorted(asm_dir.glob("*.s")):
        fn = asm_file.stem
        # relpath where the built function binary would go
        rel = f"build/{fn}"
        entries.append(f"0000000000000000000000000000000000000000 {rel}")
    return entries