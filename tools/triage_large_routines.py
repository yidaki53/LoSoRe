"""CLI for generic large-routine blocker triage."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import large_routine_plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--min-group-count", type=int, default=2)
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()
    result = large_routine_plan.analyze(
        args.root.resolve(), args.target, min_group_count=args.min_group_count
    )
    if args.limit >= 0:
        result["routines"] = result["routines"][:args.limit]
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
