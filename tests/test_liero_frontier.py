"""Conservative whole-census original-byte dependency triage."""

import pytest

from tools import liero_frontier as frontier


def row(offset, raw, text):
    """Oracle: supplied original decoder row, not an assembly-listing instruction fact."""
    return {"offset": offset, "bytes": raw, "text": text}


def test_actual_relocation_not_exported_far_target():
    """Oracle: far target decoded from original bytes only with actual MZ relocation."""
    rows = [row(0x629, "9ae148dd14", "call 0x14dd:0x48e1")]
    edges, blockers = frontier.transfers(rows, 0x1000, 0x629, 5, {3})
    assert not blockers
    assert (edges[0]["segment"], edges[0]["offset"]) == (0x24DD, 0x48E1)
    assert frontier.transfers(rows, 0x1000, 0x629, 5, set())[1]


def test_indirect_external_and_tail_dependencies_are_not_leaves():
    """Oracle: exact control-transfer bytes; embedded/unknown transfers are conservative blockers."""
    edges, blockers = frontier.transfers(
        [
            row(0x100, "e80500", "call 0x108"),
            row(0x103, "ffd0", "call ax"),
            row(0x105, "cd21", "int 0x21"),
            row(0x107, "9b", "fwait"),
            row(0x108, "eb20", "jmp 0x12a"),
        ],
        0x24DD,
        0x100,
        10,
        set(),
    )
    assert len(edges) == 2
    assert len(blockers) == 3
    assert edges[1]["offset"] == 0x12A


def test_mutual_recursion_stays_one_dependency_group():
    """Oracle: graph SCC grouping, never bootstrap callee resolution from circular edges."""
    groups = frontier.dependency_groups(
        {"a": {"b"}, "b": {"a", "c"}, "c": set(), "d": {"d"}}
    )
    assert groups == [["a", "b"], ["c"], ["d"]]


def test_whole_census_triage_original_bytes_and_replay(tmp_path):
    """Oracle: real BYOD census/audit; triage does not execute or promote routines."""
    if not (frontier.ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("BYOD unavailable")
    result = frontier.triage(frontier.ROOT, tmp_path / "frontier")
    assert result["routines_total"] == 295
    assert sum(result["categories"].values()) == 295
    records = result["routines"]
    assert records["FUN_24dd_3117"]["category"] == "blocked-control-or-external"
    assert records["FUN_24dd_4141"]["category"] == "unresolved-leaf-ready-for-oracle"
    assert records["FUN_2971_65df"]["bytes_sha256"] is None
    assert records["FUN_1000_05eb"]["unresolved_dependencies"]
    assert all(row["execution_eligible"] is False for row in records.values())
    assert frontier.replay(frontier.ROOT, tmp_path / "frontier") == result
    (tmp_path / "frontier/bytes/FUN_24dd_4141.bin").write_bytes(b"\x90")
    with pytest.raises(ValueError, match="artifact changed"):
        frontier.replay(frontier.ROOT, tmp_path / "frontier")
