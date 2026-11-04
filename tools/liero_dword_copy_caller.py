"""Bounded premise check for the original 1000:94D7 dword-copy call site."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.alternate_streams import _mz_relocation_locations, load_binary_evidence
from tools.liero_dword_copy_contract import checked_contract, digest
from tools.liero_four_routine_pilot import save


def caller_constraints(
    raw: bytes, relocation_offsets: set[int], *, load_segment: int
) -> dict:
    """Oracle: exact argument setup and actual relocation; unknown premises stay unknown."""
    expected = bytes.fromhex("e89ec9c43e84660657c43ed76506576850c39a0000c20e")
    if raw != expected or relocation_offsets != {21}:
        raise ValueError("unsupported caller bytes or relocation layout")
    if type(load_segment) is not int or not 0 <= load_segment <= 0xFFFF - 0x0EC2:
        raise ValueError("unsupported nonwrapping call relocation base")
    return {
        "oracle": "exact_original_callsite_constraints_not_caller_acceptance",
        "status": "blocked-on-caller-premises",
        "caller": "FUN_1000_929a",
        "slice_entry": "1000:94c5",
        "call_address": "1000:94d7",
        "bytes_hex": raw.hex(),
        "bytes_sha256": digest(raw),
        "predecessor_call": {
            "address": "1000:94c5",
            "target": "FUN_1000_5e66",
            "kind": "near",
            "relative_displacement": -13922,
            "obligation": "Establish post-call DF, DS, SS:SP and global pointer-cell effects before resolving this caller.",
        },
        "source_pointer": {
            "address_space": "post_predecessor_ds",
            "far_pointer_cell_offset": 0x6684,
        },
        "destination_pointer": {
            "address_space": "post_predecessor_ds",
            "far_pointer_cell_offset": 0x65D7,
        },
        "count_word": 50000,
        "copied_bytes_if_contract_holds": 50000,
        "call_target_relative_to_load": {"segment": 0x0EC2, "offset": 0},
        "call_target_relocated": {"segment": load_segment + 0x0EC2, "offset": 0},
        "call_argument_bytes": 10,
        "far_return_ip": 0x94DC,
        "stack_requirement": {
            "minimum_pre_argument_sp": 18,
            "lowest_relative_to_pre_argument_sp": -18,
            "post_return_sp_relative_to_pre_argument_sp": 0,
            "reason": "10 argument bytes + 4 far-return bytes + saved BP/DS; RETF10 restores pre-argument SP if valid.",
        },
        "conditional_bounds": {
            "maximum_initial_source_offset": 15536,
            "maximum_initial_destination_offset": 15536,
            "reason": "offset + 50000 <= 65536; readable/writable physical bounds and nonaliasing must also be established.",
        },
        "blockers": [
            "Unreviewed predecessor FUN_1000_5e66: no established post-call DF=0 or preserved DS/SS:SP contract.",
            "Pointer-cell values/provenance and 50000-byte readable/writable allocations are not established by LES.",
            "Source/destination physical disjointness and separation from stack/code remain unknown, even when segment words differ.",
            "Existing leaf execution corpus covers counts 0..257 and at most 256 copied bytes; it does not measure this 50000-byte call.",
            "Local bytes do not establish normal-program reachability of this caller slice.",
        ],
        "routine_recovered": False,
        "caller_eligible": False,
        "model_requests": 0,
        "execution_cases": 0,
        "source_promoted": False,
    }


def assess_caller(root: pathlib.Path, output: pathlib.Path) -> dict:
    """Oracle: authenticated original-image slice and persisted blocked assessment."""
    target = root / "targets/liero"
    manifest_path = target / "alternate_streams.json"
    binary, header, base, identity = load_binary_evidence(
        target, json.loads(manifest_path.read_text())
    )
    _, callee = checked_contract(root)
    if header != int.from_bytes(binary[8:10], "little") * 16 or base != 0x1000:
        raise ValueError(
            "caller assessment requires the existing 1000h logical mapping"
        )
    offset = header + 0x94C5
    relocations = {
        location - offset
        for location in _mz_relocation_locations(binary, header)
        if offset - 1 <= location < offset + 23
    }
    report = caller_constraints(
        binary[offset : offset + 23], relocations, load_segment=base
    )
    ledger_path = target / "recovery.json"
    ledger = json.loads(ledger_path.read_text())["functions"]
    report["ledger_status_snapshot"] = {
        name: ledger[name]["status"]
        for name in ("FUN_1000_929a", "FUN_1000_5e66", "FUN_1ec2_0000")
    }
    report.update(
        {"file_offset": offset, "binary_sha256": identity, "callee_contract": callee}
    )
    paths = (
        root / "tools/liero_dword_copy_caller.py",
        root / "tools/liero_dword_copy_contract.py",
        root / "engine/alternate_streams.py",
        root / "tools/liero_four_routine_pilot.py",
        manifest_path,
        ledger_path,
    )
    report["evidence_hashes"] = {
        str(path.relative_to(root)): digest(path.read_bytes()) for path in paths
    }
    output.mkdir(parents=True, exist_ok=False)
    (output / "methods").mkdir()
    for path in paths:
        shutil.copy2(path, output / "methods" / path.name)
    save(output / "result.json", report)
    return report


def main() -> None:
    """Oracle: fresh-directory static blocked report; missing disc input explicitly skips."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    if not (args.root / "extracted/liero/LIERO.EXE").is_file():
        print(json.dumps({"status": "skipped", "reason": "Liero BYOD unavailable"}))
        return
    print(
        json.dumps(assess_caller(args.root.resolve(), args.output.resolve()), indent=2)
    )


if __name__ == "__main__":
    main()
