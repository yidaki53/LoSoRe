"""draft + compile-gate -> oracle verify, with honest reporting.

Closes the learning loop: each target is drafted (optionally via the local LLM),
the compile gate reverts anything that breaks the whole-program build, and then
engine/verify.py's oracle checks the rebuild against BYOD. The result is recorded
into knowledge/knowledge.json so progress counts are oracle-backed, never just
fn totals.

The verify oracle is configured per target in config/build.sha1 as
    <sha1> <relpath>
and (for dat-parity) targets/<slug>/tools/liero_dat.py. When build.sha1 carries
no entries, verify.py prints a WARN and returns 0 with NOT VERIFIED (no pass
on an empty/unchosen oracle).
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "engine"))

import draft  # noqa: E402
from verify import verify  # noqa: E402


def _run_draft(target: str, use_llm: bool, model: str | None, endpoint: str | None,
               limit: int | None, recon_dir: str | None, recon_verdicts: str) -> None:
    draft.draft(target, oracle="none", use_llm=use_llm, model=model,
                endpoint=endpoint, limit=limit,
                recon_dir=recon_dir, recon_verdicts=recon_verdicts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", required=True)
    ap.add_argument("--byod", default=None,
                    help="BYOD tree (extracted/<target>); absent => disc-gated")
    ap.add_argument("--build", default=None, help="build dir (default targets/<t>/build)")
    ap.add_argument("--oracle", default="byte-exact", choices=[
        "byte-exact", "relocation-aware", "round-trip", "trace-parity", "dat-parity"])
    ap.add_argument("--llm", action="store_true", help="invoke the local LLM")
    ap.add_argument("--model", default=None)
    ap.add_argument("--endpoint", default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--recon-dir", default=None)
    ap.add_argument("--recon-verdicts", default="real")
    a = ap.parse_args()

    root = pathlib.Path(f"targets/{a.target}")
    build = pathlib.Path(a.build or f"targets/{a.target}/build")
    byod = pathlib.Path(a.byod or f"extracted/{a.target}")

    print(f"[draft-verify:{a.target}] drafting...")
    _run_draft(a.target, a.llm, a.model, a.endpoint, a.limit, a.recon_dir,
               a.recon_verdicts)

    print(f"[draft-verify:{a.target}] compile-gate...")
    draft._compile_gate(root, a.target, a.recon_dir, {v.strip() for v in a.recon_verdicts.split(",") if v.strip()})

    print(f"[draft-verify:{a.target}] verifying ({a.oracle})...")
    rc = verify(a.target, byod, build, a.oracle)

    print(f"[draft-verify:{a.target}] done (rc={rc})")
    return rc


if __name__ == "__main__":
    sys.exit(main())
