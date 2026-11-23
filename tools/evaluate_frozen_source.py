"""Evaluate one frozen source candidate against the scoped routine oracle."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.frozen_source_eval import run


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--routine", default="FUN_24dd_48e1")
    args = parser.parse_args()
    result = run(
        ROOT, args.output.resolve(), args.source.resolve(), args.routine
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
