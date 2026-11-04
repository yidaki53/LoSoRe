import json
import pathlib

import pytest

from tools.liero_dword_copy_caller import assess_caller, caller_constraints
from tools.liero_dword_copy_contract import digest

RAW = bytes.fromhex("e89ec9c43e84660657c43ed76506576850c39a0000c20e")


def test_conditional_origins_count_bounds_and_blockers():
    """Oracle: independent caller stack arithmetic and original immediate/pointer slots."""
    result = caller_constraints(RAW, {21}, load_segment=0x1000)
    assert result["count_word"] == 50000
    assert result["source_pointer"]["far_pointer_cell_offset"] == 0x6684
    assert result["destination_pointer"]["far_pointer_cell_offset"] == 0x65D7
    assert result["predecessor_call"]["relative_displacement"] == int.from_bytes(
        RAW[1:3], "little", signed=True
    )
    assert (
        0x94C8 + result["predecessor_call"]["relative_displacement"]
    ) & 65535 == 0x5E66
    assert result["call_target_relocated"] == {"segment": 0x1EC2, "offset": 0}
    assert result["stack_requirement"]["minimum_pre_argument_sp"] == 18
    assert (
        65536 - result["count_word"]
        == result["conditional_bounds"]["maximum_initial_source_offset"]
    )
    assert result["caller_eligible"] is False
    assert result["execution_cases"] == 0
    assert len(result["blockers"]) == 5


@pytest.mark.parametrize("offset", range(23))
def test_every_slice_byte_mutant_fails(offset):
    """Oracle: predecessor, pointer direction, immediate and call target must match."""
    mutated = bytearray(RAW)
    mutated[offset] ^= 1
    with pytest.raises(ValueError, match="caller bytes"):
        caller_constraints(bytes(mutated), {21}, load_segment=0x1000)


@pytest.mark.parametrize("locations", [set(), {20}, {22}, {21, -1}, {3, 21}])
def test_actual_exclusive_segment_relocation_is_required(locations):
    """Oracle: unrelocated or overlapping instruction evidence cannot bind this target."""
    with pytest.raises(ValueError, match="relocation"):
        caller_constraints(RAW, locations, load_segment=0x1000)


@pytest.mark.parametrize("base", [True, -1, 65535])
def test_nonwrapping_relocation_base_required(base):
    """Oracle: caller-target arithmetic must not silently wrap."""
    with pytest.raises(ValueError, match="base"):
        caller_constraints(RAW, {21}, load_segment=base)


def test_original_slice_persists_blockers_and_does_not_change_ledger(tmp_path):
    """Oracle: actual original bytes/MZ relocation and persisted method/evidence identities."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    ledger = root / "targets/liero/recovery.json"
    before = ledger.read_bytes()
    output = tmp_path / "caller"
    result = assess_caller(root, output)
    assert result["file_offset"] == 44085
    assert result["status"] == "blocked-on-caller-premises"
    assert result["ledger_status_snapshot"]["FUN_1000_5e66"] == "unreviewed"
    assert ledger.read_bytes() == before
    assert json.loads((output / "result.json").read_text()) == result
    for relative, expected in result["evidence_hashes"].items():
        assert digest((root / relative).read_bytes()) == expected
        assert (
            digest((output / "methods" / pathlib.Path(relative).name).read_bytes())
            == expected
        )
    with pytest.raises(FileExistsError):
        assess_caller(root, output)
