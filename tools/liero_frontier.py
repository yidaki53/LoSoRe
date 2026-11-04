"""Conservative original-byte routine triage using the existing recovery audit."""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import shutil
import subprocess

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from engine.recovery import audit_target
from engine.routine_contract import load_contracts
from tools import liero_four_routine_pilot as pilot

ROOT = pilot.ROOT


def decode(path: pathlib.Path, offset: int) -> list[dict]:
    """Oracle: GNU i8086 decoding of original bytes, conservative linear-sweep reference."""
    command = [
        "objdump",
        "-D",
        "-b",
        "binary",
        "-m",
        "i8086",
        "-M",
        "intel",
        "--insn-width=16",
        f"--adjust-vma={offset}",
        str(path),
    ]
    result = subprocess.run(
        command, capture_output=True, text=True, timeout=30, check=False
    )
    if result.returncode:
        raise ValueError("original-byte decoder failed: " + result.stderr)
    rows = []
    for line in result.stdout.splitlines():
        match = re.match(r"\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} )+)\s+(.+)", line)
        if match:
            raw = bytes.fromhex(match[2])
            rows.append(
                {
                    "offset": int(match[1], 16),
                    "bytes": raw.hex(),
                    "text": match[3].strip(),
                }
            )
    if not rows:
        raise ValueError("decoder returned no instructions")
    return rows


def transfers(
    rows: list[dict], segment: int, start: int, size: int, relocation_offsets: set[int]
) -> tuple[list[dict], list[str]]:
    """Oracle: direct instruction bytes and actual relocations; unknown calls stay blockers."""
    edges, blockers = [], []
    consumed = 0
    for row in rows:
        raw = bytes.fromhex(row["bytes"])
        consumed += len(raw)
        offset = row["offset"]
        text = row["text"]
        mnemonic = text.split()[0]
        if "(bad)" in text or mnemonic in {"(bad)", ".byte"}:
            blockers.append(f"undecoded bytes at {offset:04x}")
        if mnemonic.startswith(("call", "jmp", "j", "loop")):
            target = None
            if raw[0] in (0x9A, 0xEA) and len(raw) == 5:
                if offset - start + 3 not in relocation_offsets:
                    blockers.append(f"unrelocated far target at {offset:04x}")
                else:
                    target = (
                        0x1000 + int.from_bytes(raw[3:5], "little"),
                        int.from_bytes(raw[1:3], "little"),
                    )
            elif raw[0] in (0xE8, 0xE9) and len(raw) == 3:
                target = (
                    segment,
                    (offset + 3 + int.from_bytes(raw[1:], "little", signed=True))
                    & 65535,
                )
            elif (
                raw[0] == 0xEB or 0x70 <= raw[0] <= 0x7F or 0xE0 <= raw[0] <= 0xE3
            ) and len(raw) == 2:
                target = (
                    segment,
                    (offset + 2 + int.from_bytes(raw[1:], "little", signed=True))
                    & 65535,
                )
            if target is None:
                blockers.append(
                    f"indirect/unsupported transfer at {offset:04x}: {text}"
                )
            elif mnemonic.startswith("call") or not (
                target[0] == segment and start <= target[1] < start + size
            ):
                edges.append(
                    {
                        "site": f"{segment:04x}:{offset:04x}",
                        "kind": mnemonic,
                        "segment": target[0],
                        "offset": target[1],
                    }
                )
        if mnemonic.startswith("f") or mnemonic in {
            "int",
            "int3",
            "into",
            "iret",
            "in",
            "out",
            "ins",
            "outs",
            "hlt",
        }:
            blockers.append(f"external/interrupt effect at {offset:04x}: {text}")
    if consumed != size:
        blockers.append("linear decoder coverage differs from inventory byte size")
    return edges, blockers


def dependency_groups(graph: dict[str, set[str]]) -> list[list[str]]:
    """Oracle: strongly connected dependency groups, no circular resolution claims."""
    remaining = set(graph)
    groups = []

    def reachable(start: str) -> set[str]:
        """Oracle: finite graph reachability for SCC membership."""
        seen, pending = set(), [start]
        while pending:
            node = pending.pop()
            if node in seen:
                continue
            seen.add(node)
            pending.extend(graph.get(node, set()) - seen)
        return seen

    reach = {name: reachable(name) for name in graph}
    while remaining:
        name = min(remaining)
        group = sorted(
            other
            for other in remaining
            if other in reach[name] and name in reach[other]
        )
        groups.append(group)
        remaining.difference_update(group)
    return groups


def triage(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: full census triage, not semantic acceptance or graph rebuild."""
    target = root / "targets/liero"
    inventory = json.loads((target / "functions.json").read_text())["functions"]
    binary, header, base, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    if base != 0x1000:
        raise ValueError("frontier requires existing1000 logical mapping")
    audit = audit_target(target)
    reviewed = {row["name"]: row for row in audit["routines"]}
    contracts = load_contracts(target / "config/routine_contracts.json")
    entries = {}
    for item in inventory:
        segment, offset = (int(part, 16) for part in item["entry"].split(":"))
        entries.setdefault((segment, offset), []).append(item["name"])
    output.mkdir(parents=True, exist_ok=False)
    raw_dir = output / "bytes"
    raw_dir.mkdir()
    relocations = _mz_relocation_locations(binary, header)
    records = {}
    for item in inventory:
        name, size = item["name"], item["size"]
        segment, offset = (int(part, 16) for part in item["entry"].split(":"))
        file_offset = header + (segment - base) * 16 + offset
        raw = binary[file_offset : file_offset + size]
        if file_offset < header or len(raw) != size or size <= 0:
            status = reviewed[name]
            records[name] = {
                "entry": item["entry"],
                "size": size,
                "file_offset": file_offset,
                "bytes_sha256": None,
                "instructions": [],
                "transfers": [],
                "dependencies": [],
                "blockers": [
                    "inventory extent has no complete original-file bytes; possible non-file-backed pseudo-entry"
                ],
                "source_review_current": status["source_recovered"],
                "behavior_verified": status["behavior_verified"],
                "pascal_body_present": status["pascal_body_present"],
                "contract_available": name in contracts,
                "oracle": None,
            }
            continue
        path = raw_dir / (name + ".bin")
        path.write_bytes(raw)
        rows = decode(path, offset)
        edges, blockers = transfers(
            rows,
            segment,
            offset,
            size,
            {
                p - file_offset
                for p in relocations
                if file_offset - 1 <= p < file_offset + size
            },
        )
        dependencies = set()
        for edge in edges:
            matches = entries.get((edge["segment"], edge["offset"]), [])
            edge["targets"] = matches
            if len(matches) != 1:
                blockers.append("unknown/alternate target at " + edge["site"])
            else:
                dependencies.add(matches[0])
        status = reviewed[name]
        records[name] = {
            "entry": item["entry"],
            "size": size,
            "file_offset": file_offset,
            "bytes_sha256": pilot.digest(path),
            "instructions": rows,
            "transfers": edges,
            "dependencies": sorted(dependencies),
            "blockers": blockers,
            "source_review_current": status["source_recovered"],
            "behavior_verified": status["behavior_verified"],
            "pascal_body_present": status["pascal_body_present"],
            "contract_available": name in contracts,
            "oracle": contracts[name]["oracle"] if name in contracts else None,
        }
    groups = dependency_groups({n: set(r["dependencies"]) for n, r in records.items()})
    for name, row in records.items():
        resolved = lambda callee: (
            records[callee]["source_review_current"]
            and records[callee]["behavior_verified"]
            and records[callee]["contract_available"]
        )
        row["unresolved_dependencies"] = [
            n for n in row["dependencies"] if not resolved(n)
        ]
        row["dependency_group"] = next(group for group in groups if name in group)
        if row["source_review_current"]:
            category = "reviewed-source-reuse-scope"
        elif row["blockers"]:
            category = "blocked-control-or-external"
        elif row["unresolved_dependencies"]:
            category = "blocked-callee-contracts"
        elif row["pascal_body_present"]:
            category = "manual-body-needs-review"
        else:
            category = (
                "unresolved-leaf-ready-for-oracle"
                if not row["dependencies"]
                else "unresolved-ready-with-contracts"
            )
        row["category"] = category
        row["execution_eligible"] = False
        row["execution_obligation"] = (
            "Select and freeze byte-bound input/ABI/memory oracle before execution; leaf status alone is not safety."
        )
    candidates = sorted(
        (n for n, r in records.items() if r["category"].startswith("unresolved-")),
        key=lambda n: (records[n]["size"], n),
    )
    result = {
        "binary_sha256": identity,
        "routines_total": len(records),
        "categories": dict(
            collections.Counter(r["category"] for r in records.values())
        ),
        "candidate_order": candidates,
        "dependency_groups": groups,
        "routines": records,
        "policy": "Conservative linear decode: potential embedded data/unknown edges block rather than imply leaf. Scoped contracts are not full callee resolution.",
        "model_requests": 0,
        "accepted_recoveries": 0,
    }
    methods = output / "methods"
    methods.mkdir()
    paths = [
        pathlib.Path(__file__),
        root / "engine/recovery.py",
        target / "functions.json",
        target / "recovery.json",
        target / "config/routine_contracts.json",
    ]
    for path in paths:
        shutil.copy2(path, methods / path.name)
    result["method_hashes"] = {str(p.relative_to(root)): pilot.digest(p) for p in paths}
    pilot.save(output / "result.json", result)
    pilot.save(
        output / "artifacts.json",
        {
            str(p.relative_to(output)): pilot.digest(p)
            for p in output.rglob("*")
            if p.is_file()
        },
    )
    return result


def replay(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: frozen census identities and original byte extents; not semantic acceptance."""
    result = json.loads((output / "result.json").read_text())
    for name, identity in json.loads((output / "artifacts.json").read_text()).items():
        path = (output / name).resolve()
        if not path.is_relative_to(output.resolve()) or pilot.digest(path) != identity:
            raise ValueError("frontier artifact changed: " + name)
    target = root / "targets/liero"
    binary, _, _, identity = load_binary_evidence(
        target, json.loads((target / "alternate_streams.json").read_text())
    )
    if identity != result["binary_sha256"]:
        raise ValueError("frontier binary changed")
    for name, row in result["routines"].items():
        if row["bytes_sha256"] is None:
            continue
        raw = (output / "bytes" / (name + ".bin")).read_bytes()
        if binary[row["file_offset"] : row["file_offset"] + row["size"]] != raw:
            raise ValueError("frontier original routine bytes differ: " + name)
    return result


def main() -> None:
    """Oracle: read-only BYOD census; missing disc input degrades to explicit skip."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        print(json.dumps({"status": "skipped", "reason": "BYOD unavailable"}))
        return
    result = (
        replay(ROOT, args.output.resolve())
        if args.replay
        else triage(ROOT, args.output.resolve())
    )
    print(
        json.dumps(
            {k: result[k] for k in ("routines_total", "categories", "candidate_order")},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
