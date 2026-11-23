#!/usr/bin/env python3
"""RL-guided recovery loop for Liero Pascal source recovery.

Single system: one algorithm, one state, one loop.

Uses the unified RL agent (engine/recovery_loop.py) to:

  1. Load the single state file (knowledge base + Q-tables + experience buffer)
  2. Select the next function to solve (callee-first priority)
  3. Select the recovery action (model | temperature | few_shot) via epsilon-greedy Q-learning
  4. Draft the function body
  5. Verify against the oracle
  6. Learn from the outcome (Q-table update + experience replay)

Pascal isolation: Q-tables are keyed by language|toolchain so Pascal never
shares experience with C or any other language.

Usage:
    uv run python tools/rl_recover.py --target liero --max-iterations 10
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "engine"))

from engine.recovery_loop import run_recovery  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="RL-guided Liero Pascal source recovery")
    ap.add_argument("--target", default="liero", help="Target slug")
    ap.add_argument("--max-iterations", type=int, default=10, help="Maximum recovery iterations")
    ap.add_argument("--byod", default=None, help="Path to BYOD executable")
    ap.add_argument("--build", default=None, help="Build directory")
    ap.add_argument(
        "--oracle", default="routine-trace-parity",
        choices=["dat-parity", "byte-exact", "relocation-aware", "round-trip",
                 "trace-parity", "routine-trace-parity", "constructor-parity"],
    )
    ap.add_argument("--models", default=None, help="Comma-separated list of available models")
    ap.add_argument("--endpoint", default=None, help="OpenAI-compatible endpoint (Colibri/Ollama)")
    ap.add_argument("--max-tokens", type=int, default=768)
    ap.add_argument("--root", default=None)
    args = ap.parse_args()

    available_models = None
    if args.models:
        available_models = [m.strip() for m in args.models.split(",")]

    print(json.dumps(run_recovery(
        target=args.target,
        max_iterations=args.max_iterations,
        byod=pathlib.Path(args.byod) if args.byod else None,
        build=pathlib.Path(args.build) if args.build else None,
        oracle=args.oracle,
        available_models=available_models,
        endpoint=args.endpoint,
        max_tokens=args.max_tokens,
        root=pathlib.Path(args.root) if args.root else None,
    ), indent=2))


if __name__ == "__main__":
    main()
