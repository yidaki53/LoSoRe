import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_dword_copy_contract as copy

RAW = bytes.fromhex("5589e51ec5760cc47e088b4e06c1e90266f3a51fc9ca0a00")


def test_exact_contract_preserves_df_and_truncated_tail_obligations():
    """Oracle: explicit complete original-byte shape, not host compilation."""
    contract = copy.dword_copy_contract(RAW)
    assert contract["entry_sp_slots"] == {
        "source_far_pointer": 10,
        "destination_far_pointer": 6,
        "count_word": 4,
    }
    assert contract["far_return_cleanup_bytes"] == 10
    assert "does not clear DF" in contract["direction"]
    assert contract["copy_bytes"] == "4 * (unsigned_count_word // 4)"
    assert contract["routine_recovered"] is False


@pytest.mark.parametrize("offset", range(24))
def test_each_instruction_or_operand_byte_mutant_is_rejected(offset):
    """Oracle: no alternate count, pointer slot, prefix, direction or return is silently accepted."""
    mutated = bytearray(RAW)
    mutated[offset] ^= 1
    with pytest.raises(ValueError, match="shape"):
        copy.dword_copy_contract(bytes(mutated))


@pytest.mark.parametrize("raw", [b"", RAW[:-1], RAW + b"\x90"])
def test_incomplete_or_extra_bytes_fail(raw):
    """Oracle: complete entry shape only, no partial-trace routine promotion."""
    with pytest.raises(ValueError, match="shape"):
        copy.dword_copy_contract(raw)


def outputs():
    """Oracle: independent finite expected memory and separately tagged original-only observations."""
    inputs = copy.cases()
    original, pascal = bytearray(), bytearray()
    for _, count, arena in inputs:
        expected = bytearray(arena)
        n = count - count % 4
        expected[272 : 272 + n] = arena[:n]
        original.extend(expected + struct.pack("<4H", 0xFFFE, 0xFFFE, 0x2000, 0x2000))
        pascal.extend(expected)
    return bytes(original), bytes(pascal), inputs


def test_corpus_and_output_contract_cover_remainders_zero_and_guards():
    """Oracle: exact 774-case frozen shape, every arena byte compared."""
    original, pascal, inputs = outputs()
    assert len(inputs) == 774
    assert {count for _, count, _ in inputs} == set(range(258))
    result = copy.compare_outputs(original, pascal, inputs)
    assert result["cases"] == 774
    assert result["bytes_checked"] == 421056


@pytest.mark.parametrize(
    "offset", [0, 255, 256, 271, 272, 527, 528, 543, 544, 546, 548, 550]
)
def test_original_memory_or_sp_ds_mutants_fail(offset):
    """Oracle: copied/uncopied/guard/source bytes and original SP/DS must agree."""
    original, pascal, inputs = outputs()
    changed = bytearray(original)
    changed[offset] ^= 1
    with pytest.raises(ValueError):
        copy.compare_outputs(bytes(changed), pascal, inputs)


@pytest.mark.parametrize(
    "case_index,offset",
    [(0, 272), (1, 272), (3, 274), (4, 275), (257, 527), (257, 528)],
)
def test_pascal_tail_and_boundary_mutants_fail(case_index, offset):
    """Oracle: count remainders must not copy extra bytes or silently round upward."""
    original, pascal, inputs = outputs()
    changed = bytearray(pascal)
    changed[case_index * 544 + offset] ^= 1
    with pytest.raises(ValueError, match="memory"):
        copy.compare_outputs(original, bytes(changed), inputs)


def test_invalid_output_shapes_fail():
    """Oracle: missing/truncated output never passes."""
    original, pascal, inputs = outputs()
    with pytest.raises(ValueError, match="shape"):
        copy.compare_outputs(original[:-1], pascal, inputs)
    with pytest.raises(ValueError, match="shape"):
        copy.compare_outputs(original, pascal + b"x", inputs)


def test_empty_or_changed_corpus_cannot_pass():
    """Oracle: zero cases or changed inputs must not produce a success-shaped result."""
    with pytest.raises(ValueError, match="corpus"):
        copy.compare_outputs(b"", b"", [])
    original, pascal, inputs = outputs()
    changed = list(inputs)
    seed, count, arena = changed[0]
    changed[0] = (seed, count, bytes([arena[0] ^ 1]) + arena[1:])
    with pytest.raises(ValueError, match="corpus"):
        copy.compare_outputs(original, pascal, changed)


def test_actual_binary_mapping_and_no_relocation_overlap():
    """Oracle: original image hash, actual bytes and MZ relocation table."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    raw, contract = copy.checked_contract(root)
    assert raw == RAW
    assert contract["file_offset"] == 66448
    assert (
        contract["binary_sha256"]
        == "e45653ab0f915238f7394b2846b70288d0cc35a2595debc2a49502078398c7d1"
    )


def test_original_bytes_vs_developer_pascal_projection(tmp_path):
    """Oracle: finite DOSBox original/compiled Pascal memory, not learned recovery."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD/probe tools unavailable")
    output = tmp_path / "copy"
    result = copy.run_contract_probe(root, output)
    assert result["cases"] == 774
    assert result["bytes_checked"] == 421056
    assert result["source_promoted"] is False
    assert not (output / "failure.json").exists()
    freeze = json.loads((output / "freeze.json").read_text())
    for name, identity in result["artifact_hashes"].items():
        assert copy.digest((output / name).read_bytes()) == identity
    for relative, identity in freeze["method_hashes"].items():
        assert copy.digest((root / relative).read_bytes()) == identity
        assert (
            copy.digest((output / "methods" / pathlib.Path(relative).name).read_bytes())
            == identity
        )
    target_source = root / "targets/liero/src"
    target_dir = output / "target-source"
    target_dir.mkdir()
    target_files = ("FUN_1ec2_0000.inc", "LieroRuntime.pas")
    target_hashes = {}
    for name in target_files:
        contents = (target_source / name).read_bytes()
        (target_dir / name).write_bytes(contents)
        target_hashes[name] = copy.digest(contents)
    target_program = copy.PASCAL_SOURCE.replace(
        "program DwordCopyProjection;",
        "program TargetCopy;\nuses LieroRuntime;\n{$I FUN_1ec2_0000.inc}",
    ).replace(
        "    if copied > 0 then\n"
        "      for i := 0 to copied - 1 do arena[272 + i] := arena[i];",
        "    FUN_1ec2_0000(count, @arena[272], @arena[0]);",
    )
    assert "for i :=" not in target_program
    (target_dir / "target_copy.pas").write_text(target_program)
    shutil.copy2(output / "CASES.BIN", target_dir / "CASES.BIN")
    target_freeze = {
        "source_hashes": target_hashes,
        "program_sha256": copy.digest(target_program.encode()),
        "original_trace_sha256": copy.digest((output / "TRACE.BIN").read_bytes()),
        "cases_sha256": freeze["case_bytes_sha256"],
        "scope": "Actual target source/helper, same 774 known-slice inputs; no new independent original cases.",
        "budget": "one compile and one host execution, 30 seconds each; no repair/retry",
    }
    (target_dir / "freeze.json").write_text(json.dumps(target_freeze, indent=2) + "\n")
    compiled = subprocess.run(
        ["fpc", "-Mtp", "-Cr", "-Fu.", "-Fi.", "-FU.", "target_copy.pas"],
        cwd=target_dir,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (target_dir / "fpc.log").write_bytes(compiled.stdout + compiled.stderr)
    assert compiled.returncode == 0, compiled.stdout + compiled.stderr
    executed = subprocess.run(
        [str(target_dir / "target_copy")],
        cwd=target_dir,
        capture_output=True,
        timeout=30,
        check=False,
    )
    (target_dir / "runtime.log").write_bytes(executed.stdout + executed.stderr)
    assert executed.returncode == 0, executed.stdout + executed.stderr
    target_result = copy.compare_outputs(
        (output / "TRACE.BIN").read_bytes(),
        (target_dir / "PASCAL.BIN").read_bytes(),
        copy.cases(),
    )
    target_result["actual_target_source"] = True
    target_result["source_hashes"] = target_hashes
    target_result["artifact_hashes"] = {
        path.name: copy.digest(path.read_bytes())
        for path in target_dir.iterdir()
        if path.is_file()
    }
    (target_dir / "result.json").write_text(json.dumps(target_result, indent=2) + "\n")
    assert target_result["cases"] == 774
    with pytest.raises(FileExistsError):
        copy.run_contract_probe(root, output)


def test_execution_failure_is_persisted_without_retry(tmp_path, monkeypatch):
    """Oracle: injected native failure ends the frozen run, never refunds it."""
    root = pathlib.Path(__file__).resolve().parents[1]
    if not (root / "extracted/liero/LIERO.EXE").is_file() or not all(
        shutil.which(tool) for tool in ("as", "ld", "dosbox", "fpc")
    ):
        pytest.skip("Liero BYOD/probe tools unavailable")
    calls = []

    def fail(directory):
        """Oracle: mechanism-only injected worker failure."""
        calls.append(directory)
        raise subprocess.CalledProcessError(-11, ["dosbox"])

    monkeypatch.setattr(copy, "run_dosbox", fail)
    output = tmp_path / "failure"
    with pytest.raises(subprocess.CalledProcessError):
        copy.run_contract_probe(root, output)
    failure = json.loads((output / "failure.json").read_text())
    assert failure["retry_allowed"] is False
    assert len(calls) == 1
    assert not (output / "result.json").exists()
