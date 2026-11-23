"""CLI for binary-only evidence packets for a target subfolder."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import target_packet


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--routine")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    output = args.output.resolve()
    if args.routine:
        result = target_packet.build_packet(ROOT, args.target, args.routine, output)
    else:
        result = target_packet.build_frontier_packet(
            ROOT, args.target, output, limit=args.limit
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
