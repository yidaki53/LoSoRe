"""Tests for generic large-routine blocker triage."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from engine import large_routine_plan, recovery_loop


def _make_target(tmp_path: pathlib.Path) -> pathlib.Path:
    target = tmp_path / "targets" / "sample"
    (target / "asm").mkdir(parents=True)
    (target / "functions.json").write_text(json.dumps({
        "functions": [
            {"name": "LEAF", "entry": "1000:0010", "size": 2,
             "num_instructions": 1},
            {"name": "HELPER", "entry": "1000:0020", "size": 10,
             "num_instructions": 2},
            {"name": "TOP", "entry": "1000:0030", "size": 4,
             "num_instructions": 2},
            {"name": "TAIL", "entry": "1000:0040", "size": 2,
             "num_instructions": 1},
        ],
        "num_functions": 4,
    }))
    (target / "asm" / "LEAF.s").write_text("1000:0010  RET\n")
    (target / "asm" / "HELPER.s").write_text(
        "1000:0020  LES DI,[BP+0x6]\n1000:0024  RETF 0x4\n")
    (target / "asm" / "TOP.s").write_text(
        "1000:0030  CALLF 0x1000:0020\n1000:0034  RET\n")
    (target / "asm" / "TAIL.s").write_text(
        "1000:0040  JMPF 0x1000:0020\n")
    return tmp_path


def test_triage_groups_blockers_and_ranks_leverage(tmp_path):
    root = _make_target(tmp_path)
    report = large_routine_plan.analyze(root, "sample", {})
    by_name = {routine["name"]: routine for routine in report["routines"]}
    groups = {group["capability"]: group for group in report["groups"]}

    assert by_name["HELPER"]["direct_callers"] == ["TAIL", "TOP"]
    assert by_name["HELPER"]["unlockable_callers"] == ["TOP"]
    assert "far-pointer-load" in by_name["HELPER"]["blockers"]
    assert "far-transfer" in by_name["HELPER"]["blockers"]
    assert "return-immediate" in by_name["HELPER"]["blockers"]
    assert groups["far-transfer"]["routine_count"] == 2
    assert report["priority"]["HELPER"] > report["priority"]["TOP"]
    assert report["next_capability"] == "far-transfer"
    assert report["stop"] is False


def test_triage_resolves_entries_across_segment_lengths(tmp_path):
    target = tmp_path / "targets" / "sample"
    (target / "asm").mkdir(parents=True)
    (target / "functions.json").write_text(json.dumps({
        "functions": [
            {"name": "LEAF", "entry": "2000:abcd", "size": 2,
             "num_instructions": 1},
            {"name": "CALLER", "entry": "1234:4321", "size": 4,
             "num_instructions": 2},
        ],
        "num_functions": 2,
    }))
    (target / "asm" / "LEAF.s").write_text("2000:ABCD  RET\n")
    (target / "asm" / "CALLER.s").write_text(
        "1234:4321  CALLF 0x2000:ABCD\n1234:4325  RET\n")

    report = large_routine_plan.analyze(tmp_path, "sample", {})
    by_name = {routine["name"]: routine for routine in report["routines"]}
    assert by_name["LEAF"]["direct_callers"] == ["CALLER"]
    assert by_name["LEAF"]["unlockable_callers"] == ["CALLER"]


def test_triage_stops_at_yield_floor(tmp_path):
    root = _make_target(tmp_path)
    report = large_routine_plan.analyze(
        root, "sample", {"total_attempts": 20, "total_verified": 1})
    assert report["stop"] is True
    assert report["priority"] == {}
    assert report["next_capability"] is None


def test_triage_priority_merges_with_capability_priority():
    merged = recovery_loop._merge_priorities(
        {"A": 1.5, "B": 2.0}, {"B": 0.5, "C": 3.0})
    assert merged == {"A": 1.5, "B": 2.5, "C": 3.0}


def test_focus_priority_boosts_next_capability_group(tmp_path):
    root = _make_target(tmp_path)
    report = large_routine_plan.analyze(root, "sample", {})
    focused = large_routine_plan.focus_priority(report)
    assert focused["HELPER"] == (
        report["priority"]["HELPER"] + large_routine_plan.FOCUS_PRIORITY_BONUS)
    assert focused["LEAF"] == report["priority"]["LEAF"]


def test_supported_frontier_prefers_oracle_supported_rows():
    class Gate:
        @staticmethod
        def routine_trace_supported(target, routine, root=None):
            return routine == "SUPPORTED"

    candidates = [{"name": "UNSUPPORTED"}, {"name": "SUPPORTED"}]
    selected = recovery_loop._supported_frontier(
        candidates, "sample", pathlib.Path("."), Gate, 1, "routine-trace-parity")
    assert selected == [{"name": "SUPPORTED"}]


def test_triage_cli_emits_json(tmp_path):
    root = _make_target(tmp_path)
    result = subprocess.run(
        [sys.executable, str(REPO / "tools" / "triage_large_routines.py"),
         "--target", "sample", "--root", str(root), "--limit", "1"],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    assert report["target"] == "sample"
    assert len(report["routines"]) == 1
    assert report["next_capability"] == "far-transfer"
