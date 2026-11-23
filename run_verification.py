#!/usr/bin/env python3
"""Write an authoritative, non-inflated recovery status report."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "engine"))

from engine import knowledge, matrix, verify


def build_report(target: str, oracle: str, byod: pathlib.Path,
                 build: pathlib.Path) -> dict:
    data = knowledge.load()
    rows = matrix.build(target, data)
    target_data = data.get("targets", {}).get(target, {})
    verified: set[str] = set()
    for names in target_data.get("verified", {}).values():
        verified.update(names)
    candidates = target_data.get("candidates", {})

    verified_functions = verified & {row["name"] for row in rows}
    functions = []
    counts: dict[str, int] = {}
    for row in rows:
        fn = row["name"]
        if fn in verified_functions:
            status = "oracle_verified"
        elif candidates.get(fn, {}).get("status") in {"compiled", "verified"}:
            status = "compiled_candidate"
        elif row["status"] == "source_recovered":
            status = "reviewed_unattested"
        elif row["status"] == "partially_recoverable":
            status = "partial"
        else:
            status = "unrecovered"
        counts[status] = counts.get(status, 0) + 1
        functions.append({
            "name": fn,
            "status": status,
            "attempts": row["attempts"],
            "unverified_callees": row["unverified_callees"],
        })

    result = verify.verify_status(target, byod, build, oracle)
    return {
        "schema_version": 2,
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(),
        "target": target,
        "oracle": oracle,
        "counts": counts,
        "total": len(rows),
        "verified_functions": sorted(verified_functions),
        "verification": result,
        "promotion_policy": (
            "dat-parity and constructor-parity are scoped checks and never promote source"
            if oracle in verify.ORACLES and oracle in {"dat-parity", "constructor-parity"}
            else "only matching oracle relpaths promote source"
        ),
        "functions": functions,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="liero")
    parser.add_argument("--oracle", default="dat-parity")
    parser.add_argument("--byod", default=None)
    parser.add_argument("--build", default=None)
    parser.add_argument("--output", default="recovery_results.json")
    args = parser.parse_args()

    report = build_report(
        args.target,
        args.oracle,
        pathlib.Path(args.byod or f"extracted/{args.target}"),
        pathlib.Path(args.build or f"targets/{args.target}/build"),
    )
    path = pathlib.Path(args.output)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"wrote {path}: {report['counts']}")


if __name__ == "__main__":
    main()
