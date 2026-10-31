"""Census DOS MZ image coverage against a target's exported routines."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import struct
from collections import Counter

from tools.asmcfg import (
    build_blocks,
    cfg_stats,
    is_call,
    parse_ghidra_asm,
    resolve_branch_target,
)

SCHEMA_VERSION = 1
MZ_HEADER = struct.Struct("<14H")


def _address(value: str) -> tuple[int, int]:
    segment, offset = value.split(":", maxsplit=1)
    return int(segment, 16), int(offset, 16)


def _hex(value: int) -> str:
    return f"0x{value:05x}"


def _union_ranges(
    ranges: list[tuple[int, int, str]], image_bytes: int
) -> tuple[list[dict], list[dict]]:
    ordered = sorted(ranges)
    merged: list[list] = []
    overlaps = []
    for start, end, name in ordered:
        if not merged or start >= merged[-1][1]:
            merged.append([start, end, [name]])
            continue
        previous_end = merged[-1][1]
        overlaps.append(
            {
                "start": _hex(start),
                "end": _hex(min(previous_end, end)),
                "bytes": min(previous_end, end) - start,
                "functions": [merged[-1][2][-1], name],
            }
        )
        merged[-1][1] = max(previous_end, end)
        merged[-1][2].append(name)

    gaps = []
    cursor = 0
    for start, end, _ in merged:
        if start > cursor:
            gaps.append(
                {"start": _hex(cursor), "end": _hex(start), "bytes": start - cursor}
            )
        cursor = max(cursor, end)
    if cursor < image_bytes:
        gaps.append(
            {
                "start": _hex(cursor),
                "end": _hex(image_bytes),
                "bytes": image_bytes - cursor,
            }
        )
    return (
        [
            {"start": _hex(start), "end": _hex(end), "bytes": end - start,
             "functions": names}
            for start, end, names in merged
        ],
        gaps,
    )


def _parse_mz(data: bytes) -> dict:
    if len(data) < MZ_HEADER.size:
        raise ValueError("binary is too short to contain a DOS MZ header")
    values = MZ_HEADER.unpack_from(data)
    (
        signature,
        last_page_bytes,
        pages,
        relocation_count,
        header_paragraphs,
        minimum_extra_paragraphs,
        maximum_extra_paragraphs,
        initial_ss,
        initial_sp,
        checksum,
        initial_ip,
        initial_cs,
        relocation_table_offset,
        overlay_number,
    ) = values
    if signature != 0x5A4D:
        raise ValueError("binary does not have an MZ signature")
    if pages == 0 or last_page_bytes > 511:
        raise ValueError("MZ header has an invalid declared file size")

    declared_file_bytes = (
        (pages - 1) * 512 + last_page_bytes
        if last_page_bytes
        else pages * 512
    )
    header_bytes = header_paragraphs * 16
    if header_bytes < MZ_HEADER.size:
        raise ValueError("MZ header size is smaller than the header structure")
    if header_bytes > declared_file_bytes:
        raise ValueError("MZ header size exceeds the declared file size")
    relocation_table_end = relocation_table_offset + relocation_count * 4
    if relocation_count and (
        relocation_table_end > header_bytes or relocation_table_end > len(data)
    ):
        raise ValueError("MZ relocation table extends beyond the declared header")
    if declared_file_bytes > len(data):
        raise ValueError("MZ declared file size exceeds the actual file size")

    image_bytes = declared_file_bytes - header_bytes
    relocations = []
    for index in range(relocation_count):
        offset, segment = struct.unpack_from(
            "<HH", data, relocation_table_offset + index * 4
        )
        module_offset = segment * 16 + offset
        relocations.append(
            {
                "segment": f"{segment:04x}",
                "offset": f"{offset:04x}",
                "module_offset": _hex(module_offset),
                "within_file_backed_image": module_offset + 2 <= image_bytes,
            }
        )

    return {
        "declared_file_bytes": declared_file_bytes,
        "header_bytes": header_bytes,
        "load_image_bytes": image_bytes,
        "minimum_extra_allocation_bytes": minimum_extra_paragraphs * 16,
        "maximum_extra_allocation_bytes": (
            None if maximum_extra_paragraphs == 0xFFFF
            else maximum_extra_paragraphs * 16
        ),
        "minimum_total_memory_bytes": (
            image_bytes + minimum_extra_paragraphs * 16
        ),
        "initial_stack": f"{initial_ss:04x}:{initial_sp:04x}",
        "initial_entry": f"{initial_cs:04x}:{initial_ip:04x}",
        "checksum": f"0x{checksum:04x}",
        "relocation_count": relocation_count,
        "relocation_table_offset": _hex(relocation_table_offset),
        "relocations_within_file_backed_image": sum(
            item["within_file_backed_image"] for item in relocations
        ),
        "relocations_outside_file_backed_image": sum(
            not item["within_file_backed_image"] for item in relocations
        ),
        "overlay_number": overlay_number,
        "relocations": relocations,
    }


def build_census(target_root: pathlib.Path, binary_path: pathlib.Path) -> dict:
    """Measure MZ layout and evidence-backed routine ranges for a target."""
    data = binary_path.read_bytes()
    mz = _parse_mz(data)

    metadata_path = target_root / "functions.json"
    metadata = json.loads(metadata_path.read_text(errors="replace"))
    functions = metadata.get("functions")
    if not isinstance(functions, list):
        raise TypeError(f"functions must be an array in {metadata_path}")

    entry_functions = [
        item for item in functions
        if isinstance(item, dict) and item.get("name") == "entry"
    ]
    load_segment = None
    entry_mapping_valid = False
    if len(entry_functions) == 1:
        exported_segment, exported_offset = _address(entry_functions[0]["entry"])
        mz_cs, mz_ip = _address(mz["initial_entry"])
        if exported_offset == mz_ip:
            load_segment = exported_segment - mz_cs
            entry_mapping_valid = load_segment >= 0
    if not entry_mapping_valid:
        load_segment = None

    asm_dir = target_root / "asm"
    asm_paths = {
        path.stem: path for path in asm_dir.glob("*.s")
    } if asm_dir.is_dir() else {}
    decomp_dir = target_root / "decomp"
    decomp_names = {
        path.stem for path in decomp_dir.glob("*.c")
    } if decomp_dir.is_dir() else set()

    ledger_path = target_root / "recovery.json"
    ledger_records = {}
    if ledger_path.is_file():
        ledger = json.loads(ledger_path.read_text(errors="replace"))
        raw_records = ledger.get("functions", {})
        if isinstance(raw_records, dict):
            ledger_records = raw_records

    routine_ranges = []
    routines = []
    direct_call_edges = []
    metadata_names = []
    actual_instruction_total = 0
    mismatched_instruction_counts = []
    entry_listing_mismatches = []
    entry_names_by_address: dict[int, list[str]] = {}
    for item in functions:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            continue
        try:
            segment, offset = _address(item.get("entry", ""))
        except (AttributeError, TypeError, ValueError):
            continue
        entry_names_by_address.setdefault(
            segment * 16 + offset, []
        ).append(item["name"])
    for item in functions:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            continue
        name = item["name"]
        metadata_names.append(name)
        entry_text = item.get("entry", "")
        size = item.get("size", 0)
        if not isinstance(size, int) or size < 0:
            raise ValueError(f"{name}: size must be a non-negative integer")

        asm_path = asm_paths.get(name)
        parsed = parse_ghidra_asm(
            asm_path.read_text(errors="replace") if asm_path else ""
        )
        parsed_count = len(parsed["insts"]) if asm_path else None
        cfg = cfg_stats(
            build_blocks(parsed["addrs"], parsed["insts"], parsed["segments"])
        )
        direct_calls = []
        absolute_memory_operands = set()
        for instruction_address, instruction, source_segment in zip(
            parsed["addrs"],
            parsed["insts"],
            parsed["segments"],
            strict=True,
        ):
            for match in re.finditer(
                r"\[\s*0X([0-9A-F]{1,4})\s*\]", instruction
            ):
                absolute_memory_operands.add(
                    f"0x{int(match.group(1), 16):04x}"
                )
            if not is_call(instruction):
                continue
            target_address = resolve_branch_target(instruction, source_segment)
            resolved_targets = (
                entry_names_by_address.get(target_address, [])
                if target_address is not None
                else []
            )
            edge = {
                "instruction_address": _hex(instruction_address),
                "target_flat_address": (
                    _hex(target_address) if target_address is not None else None
                ),
                "target_functions": resolved_targets,
                "direct_target_resolved": bool(resolved_targets),
            }
            direct_calls.append(edge)
            if target_address is not None:
                direct_call_edges.append(
                    {"caller": name, **edge}
                )
        actual_instruction_total += parsed_count or 0
        expected_count = item.get("num_instructions")
        count_matches = (
            parsed_count == expected_count
            if isinstance(expected_count, int) and parsed_count is not None
            else None
        )
        if count_matches is False:
            mismatched_instruction_counts.append(
                {
                    "name": name,
                    "metadata": expected_count,
                    "assembly_listing": parsed_count,
                }
            )

        try:
            segment, offset = _address(entry_text)
        except (AttributeError, TypeError, ValueError):
            segment, offset = None, None
        image_offset = None
        range_class = "unmapped"
        if segment is not None and load_segment is not None:
            image_offset = (segment - load_segment) * 16 + offset
            end_offset = image_offset + size
            if image_offset < 0:
                range_class = "before_load_image"
            elif end_offset <= mz["load_image_bytes"]:
                range_class = "file_backed_image"
            elif end_offset <= mz["minimum_total_memory_bytes"]:
                range_class = "minimum_allocated_uninitialized_tail"
            else:
                range_class = "beyond_minimum_allocated_memory"

        entry_matches_listing = None
        assembly_first_address = None
        if parsed["addrs"] and segment is not None:
            assembly_first_address = parsed["raw"][0].split(maxsplit=1)[0]
            entry_matches_listing = (
                parsed["addrs"][0] == segment * 16 + offset
            )
            if not entry_matches_listing:
                entry_listing_mismatches.append(
                    {
                        "name": name,
                        "metadata_entry": entry_text,
                        "assembly_first_instruction": assembly_first_address,
                    }
                )

        contributes_to_coverage = (
            range_class == "file_backed_image"
            and parsed_count is not None
            and parsed_count > 0
            and entry_matches_listing is True
            and size > 0
        )
        if contributes_to_coverage:
            routine_ranges.append(
                (image_offset, image_offset + size, name)
            )

        record = ledger_records.get(name, {})
        routines.append(
            {
                "name": name,
                "entry": entry_text,
                "size_bytes_from_metadata": size,
                "image_offset": (
                    _hex(image_offset) if image_offset is not None else None
                ),
                "range_class": range_class,
                "metadata_instruction_count": expected_count,
                "assembly_instruction_count": parsed_count,
                "instruction_count_matches": count_matches,
                "entry_matches_listing": entry_matches_listing,
                "assembly_first_address": assembly_first_address,
                "cfg": cfg,
                "direct_calls": direct_calls,
                "absolute_memory_operands": sorted(absolute_memory_operands),
                "decompiler_file_present": name in decomp_names,
                "recovery_status": record.get("status", "no_ledger_record"),
                "included_in_file_backed_coverage": contributes_to_coverage,
            }
        )

    merged_ranges, gaps = _union_ranges(
        routine_ranges, mz["load_image_bytes"]
    )
    overlapping_ranges = _overlaps(routine_ranges)
    covered_bytes = sum(item["bytes"] for item in merged_ranges)
    image_bytes = mz["load_image_bytes"]
    assembly_names = set(asm_paths)
    metadata_name_set = set(metadata_names)
    recovery_counts = Counter(
        item["recovery_status"] for item in routines
    )
    range_counts = Counter(item["range_class"] for item in routines)
    summary = {
        "metadata_function_count": len(metadata_names),
        "inventory_declared_count": metadata.get("num_functions"),
        "declared_count_matches_metadata": (
            metadata.get("num_functions") is None
            or metadata.get("num_functions") == len(metadata_names)
        ),
        "assembly_file_count": len(assembly_names),
        "metadata_functions_missing_assembly": sorted(
            metadata_name_set - assembly_names
        ),
        "assembly_files_missing_metadata": sorted(
            assembly_names - metadata_name_set
        ),
        "metadata_instruction_count_total": sum(
            item.get("num_instructions", 0)
            for item in functions
            if isinstance(item, dict)
            and isinstance(item.get("num_instructions", 0), int)
        ),
        "assembly_instruction_count_total": actual_instruction_total,
        "instruction_count_mismatch_count": len(mismatched_instruction_counts),
        "entry_listing_mismatch_count": len(entry_listing_mismatches),
        "functions_by_range_class": dict(sorted(range_counts.items())),
        "empty_assembly_exports": sorted(
            item["name"] for item in routines
            if item["assembly_instruction_count"] == 0
        ),
        "file_backed_function_range_count": sum(
            item["included_in_file_backed_coverage"] for item in routines
        ),
        "file_backed_function_union_bytes": covered_bytes,
        "file_backed_function_union_percent": (
            round(covered_bytes * 100 / image_bytes, 2) if image_bytes else 0
        ),
        "unclassified_file_backed_bytes": image_bytes - covered_bytes,
        "unclassified_file_backed_percent": (
            round((image_bytes - covered_bytes) * 100 / image_bytes, 2)
            if image_bytes else 0
        ),
        "unclassified_range_count": len(gaps),
        "function_range_overlap_count": len(overlapping_ranges),
        "recovery_status_counts": dict(sorted(recovery_counts.items())),
        "direct_call_edge_count": len(direct_call_edges),
        "direct_calls_to_exported_entries": sum(
            edge["direct_target_resolved"] for edge in direct_call_edges
        ),
        "calls_without_static_target_count": sum(
            call["target_flat_address"] is None
            for routine in routines
            for call in routine["direct_calls"]
        ),
        "entry_mapping_valid": entry_mapping_valid,
        "analysis_load_segment": (
            f"{load_segment:04x}" if load_segment is not None else None
        ),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "target": target_root.name,
        "binary": {
            "path": str(binary_path),
            "sha256": hashlib.sha256(data).hexdigest(),
            "actual_file_bytes": len(data),
            "declared_file_bytes": mz["declared_file_bytes"],
            "declared_file_size_matches": (
                len(data) == mz["declared_file_bytes"]
            ),
            **mz,
        },
        "address_mapping": {
            "load_segment_inferred_from_entry": summary["analysis_load_segment"],
            "entry_mapping_valid": entry_mapping_valid,
            "method": (
                "MZ initial entry offset is matched to the exported entry; "
                "its segment is adjusted by the MZ initial CS."
            ),
        },
        "summary": summary,
        "unclassified_file_backed_ranges": gaps,
        "overlapping_function_ranges": overlapping_ranges,
        "instruction_count_mismatches": mismatched_instruction_counts,
        "entry_listing_mismatches": entry_listing_mismatches,
        "direct_call_edges": direct_call_edges,
        "merged_function_ranges": merged_ranges,
        "routines": routines,
        "census_limitations": [
            (
                "The function sizes are Ghidra metadata spans, not "
                "independently decoded byte lengths."
            ),
            (
                "Complement ranges are unclassified, not presumed to be code "
                "or data; they require disassembly/reference analysis."
            ),
            (
                "Uninitialized MZ allocation may contain runtime-generated "
                "code or data, but has no corresponding file-backed bytes."
            ),
            (
                "This census does not prove that the Ghidra function export is "
                "complete or that every function boundary is correct."
            ),
            (
                "Indirect or non-literal call targets are not statically "
                "resolved; per-routine call records retain them with a null "
                "target."
            ),
        ],
    }


def _overlaps(ranges: list[tuple[int, int, str]]) -> list[dict]:
    ordered = sorted(ranges)
    result = []
    active: list[tuple[int, int, str]] = []
    for start, end, name in ordered:
        active = [item for item in active if item[1] > start]
        for other_start, other_end, other_name in active:
            result.append(
                {
                    "functions": [other_name, name],
                    "start": _hex(max(start, other_start)),
                    "end": _hex(min(end, other_end)),
                    "bytes": min(end, other_end) - max(start, other_start),
                }
            )
        active.append((start, end, name))
    return result


def _summary_text(report: dict) -> str:
    summary = report["summary"]
    binary = report["binary"]
    return (
        f"{report['target']}: MZ {binary['actual_file_bytes']} bytes "
        f"(load image {binary['load_image_bytes']} bytes), "
        f"{summary['metadata_function_count']} metadata routines, "
        f"{summary['file_backed_function_range_count']} nonempty routine "
        f"ranges cover {summary['file_backed_function_union_bytes']} bytes "
        f"({summary['file_backed_function_union_percent']}%); "
        f"{summary['unclassified_file_backed_bytes']} file-backed bytes in "
        f"{summary['unclassified_range_count']} unclassified ranges."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="target slug")
    parser.add_argument(
        "--binary",
        type=pathlib.Path,
        help="binary path (default: extracted/<target>/<program name>)",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="write the full census JSON to this path",
    )
    args = parser.parse_args(argv)
    target_root = pathlib.Path("targets") / args.target
    metadata = json.loads(
        (target_root / "functions.json").read_text(errors="replace")
    )
    binary_path = args.binary
    if binary_path is None:
        program_name = metadata.get("program")
        if not isinstance(program_name, str) or not program_name:
            parser.error("functions.json must name the program or pass --binary")
        binary_path = pathlib.Path("extracted") / args.target / program_name
    report = build_census(target_root, binary_path)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
        print(f"Wrote {args.output}")
        print(_summary_text(report))
    else:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
