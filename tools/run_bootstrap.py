"""CLI for bounded oracle-backed bootstrap experiments."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import bootstrap


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--routine", required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--methods", nargs="+", choices=tuple(bootstrap.METHODS))
    parser.add_argument("--models", nargs="+", default=["qwen2.5-coder:1.5b"])
    args = parser.parse_args()
    result = bootstrap.run_bootstrap(
        pathlib.Path(bootstrap.BASE),
        args.target,
        args.routine,
        args.output.resolve(),
        methods=args.methods,
        models=args.models,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
