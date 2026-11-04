import json
import pathlib
import shutil
import struct
import subprocess

import pytest

from tools import liero_cleanup_port_probe as probe

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture
def contract():
    """Oracle: original bytes and actual relocations, not listing call aliases."""
    if not (ROOT / "extracted/liero/LIERO.EXE").is_file():
        pytest.skip("Liero BYOD unavailable")
    return probe.checked_contract(ROOT)


def test_real_callback_dependencies(contract):
    """Oracle: signed original near displacements and segment-relative module targets."""
    calls = contract["calls"]
    assert calls["callback"] == [0x13A1D, 0x138EE]
    assert calls["stop"] == [0x135C0] * 3
    assert calls["finish"] == [0x148DA, 0x135F6]
    assert calls["reset"] == [0x14B83, 0x135DA]
    assert calls["interrupt"] == [0x14D44]
    assert contract["source_recovered"] is False
    assert contract["actual_device_verified"] is False
    assert contract["ready_only"] is True
    assert len(probe.CASES) == len(set(probe.CASES)) == 512
    assert probe.REGIONS["write"][1][-3:] == bytes.fromhex("c20200")


@pytest.mark.parametrize("name", probe.REGIONS)
def test_changed_dependency_rejected(contract, monkeypatch, name):
    """Oracle: every reviewed region is authenticated, even unexecuted service leaves."""
    binary, allocator, extra = probe.pilot.allocator_deduction_inputs(ROOT)
    mutant = bytearray(binary)
    header = int.from_bytes(binary[8:10], "little") * 16
    mutant[header + probe.REGIONS[name][0]] ^= 1
    monkeypatch.setattr(
        probe.pilot,
        "allocator_deduction_inputs",
        lambda root: (bytes(mutant), allocator, extra),
    )
    with pytest.raises(ValueError, match="bytes/relocations"):
        probe.checked_contract(ROOT)


@pytest.mark.parametrize("mutation", ["missing", "extra"])
def test_actual_relocation_mismatch_rejected(contract, monkeypatch, mutation):
    """Oracle: actual loader relocations, not segment constants inferred from listings."""
    binary, _, _ = probe.pilot.allocator_deduction_inputs(ROOT)
    header = int.from_bytes(binary[8:10], "little") * 16
    relocations = set(probe._mz_relocation_locations(binary, header))
    if mutation == "missing":
        relocations.remove(header + 0x135F6 + 16)
    else:
        relocations.add(header + 0x135C0 + 1)
    monkeypatch.setattr(
        probe, "_mz_relocation_locations", lambda binary, header: relocations
    )
    with pytest.raises(ValueError, match="bytes/relocations"):
        probe.checked_contract(ROOT)


def test_original_leaf_harness_assembles(contract, tmp_path):
    """Oracle: original IN/OUT bytes, no I/O substitutions or guessed hardware helper."""
    assembly = probe.harness(probe.CASES[:32])
    (tmp_path / "harness.S").write_text(assembly)
    raw = probe.assemble_probe(tmp_path / "harness.S", tmp_path)
    assert probe.build_image(raw)[0x1F00:0x1F1A] == probe.REGIONS["write"][1]
    mutant = bytearray(raw)
    mutant[0x1F07] ^= 1
    with pytest.raises(ValueError):
        probe.build_image(bytes(mutant))


def synthetic_record(case):
    """Oracle: synthetic expected snapshot, never guest execution evidence."""
    status, command = case
    seed = 0xA5 if status == 0 else 0x5A
    memory = bytearray([seed] * 64)
    struct.pack_into("<H", memory, 0x14, 0x21)
    return (
        struct.pack(
            "<14H",
            status,
            seed * 256 + command,
            0x2000,
            0x2000,
            0x2000,
            0xEFF0,
            0x2468,
            seed * 256 + command,
            0x21,
            0x46,
            0x1357,
            0x2468,
            command,
            0x21,
        )
        + memory
    )


@pytest.mark.parametrize("case", [(0, 0), (0, 255), (127, 128), (127, 255)])
def test_snapshot_comparison_checks_globals_stack_io_and_if(case):
    """Oracle: full recorded state, allowing only declared segment and undefined flags."""
    data = synthetic_record(case)
    expected = probe.projection(data, [case])
    assert expected == struct.pack(
        "<3H", case[1], (0xA5 if case[0] == 0 else 0x5A) * 256 + case[1], 0xEFF0
    )
    for offset in range(len(data)):
        if offset in (4, 5, 6, 7, 8, 9, 18, 19):
            continue
        mutant = bytearray(data)
        mutant[offset] ^= 1
        with pytest.raises(ValueError):
            probe.projection(bytes(mutant), [case])
    for flag in (0x200, 1, 0x80, 0x800, 0x400):
        mutant = bytearray(data)
        struct.pack_into("<H", mutant, 18, 0x46 ^ flag)
        with pytest.raises(ValueError):
            probe.projection(bytes(mutant), [case])
    with pytest.raises(ValueError):
        probe.projection(data[:-1], [case])


def test_missing_byod_skips_without_artifacts(tmp_path):
    """Oracle: disc-gated input, not a pass."""
    assert probe.run(tmp_path, tmp_path / "out")["status"] == "skipped"
    assert not (tmp_path / "out").exists()


def test_timeout_stops_without_retry(contract, tmp_path, monkeypatch):
    """Oracle: injected timeout is a failed experiment, not terminal feedback for repair."""
    calls = []

    def timeout(directory):
        """Oracle: mechanism failure injection, no original execution."""
        calls.append(directory)
        raise subprocess.TimeoutExpired(["dosbox"], 30)

    monkeypatch.setattr(probe, "run_dosbox", timeout)
    result = probe.run(ROOT, tmp_path / "out")
    assert result["status"] == "failed"
    assert len(calls) == 1
    assert not (tmp_path / "out/compile.log").exists()


@pytest.mark.parametrize(
    "mutation",
    ["none", "trace", "image", "source", "method", "metadata", "missing", "escape"],
)
def test_saved_replay_rejects_rehashed_mutations(contract, tmp_path, mutation):
    """Oracle: saved-image/method/whole-record replay; no new original executions."""
    saved = ROOT / "targets/liero/build/cleanup-port/pic-ready-v1"
    if not (saved / "result.json").is_file():
        pytest.skip("saved port fixture unavailable")
    output = tmp_path / "copy"
    shutil.copytree(saved, output)
    report = json.loads((output / "result.json").read_text())
    paths = {
        "trace": "batch-0/TRACE.BIN",
        "image": "batch-0/PROBE.COM",
        "source": "probe.pas",
        "method": "methods/liero_cleanup_port_probe.py",
    }
    if mutation in paths:
        path = output / paths[mutation]
        data = bytearray(path.read_bytes())
        data[-1] ^= 1
        path.write_bytes(data)
        report["artifact_hashes"][paths[mutation]] = probe.pilot.digest(path)
    elif mutation == "metadata":
        report["actual_device_verified"] = True
    elif mutation == "missing":
        report["artifact_hashes"].pop("batch-0/TRACE.BIN")
    elif mutation == "escape":
        report["artifact_hashes"]["../outside"] = "0" * 64
    probe.pilot.save(output / "result.json", report)
    if mutation == "none":
        assert probe.validate_report(ROOT, output)["cases"] == 512
    else:
        with pytest.raises(ValueError):
            probe.validate_report(ROOT, output)


def test_graph_and_audit_keep_real_callback_and_device_unknown(contract):
    """Oracle: conditional leaf control cannot discharge real device/callback neighbors."""
    from engine.scoped_verification import (
        cleanup_port_contract_graph,
        load_scoped_checks,
    )

    output = ROOT / "targets/liero/build/cleanup-port/pic-ready-v1"
    if not (output / "result.json").is_file():
        pytest.skip("saved port fixture unavailable")
    graph = cleanup_port_contract_graph(ROOT / "targets/liero", output)
    assert len(graph.nodes) == 10
    assert len(graph.edges) == 12
    assert (
        graph.facts["allocator.cleanup-real.write.pic-ready"].status
        == "oracle-verified"
    )
    assert graph.facts["allocator.cleanup-real.callback.unresolved"].status == "unknown"
    assert graph.facts["allocator.cleanup-real.write.unresolved"].status == "unknown"
    initialization = graph.facts["allocator.cleanup-real.sound-init.static"].value
    assert initialization["base_argument"]["caller_cell"] == 0x65D2
    assert initialization["ports"] == {
        "reset": {"cell": 0x67D0, "base_delta": 6},
        "read": {"cell": 0x67D2, "base_delta": 10},
        "write": {"cell": 0x67D4, "base_delta": 12},
        "status": {"cell": 0x67D6, "base_delta": 14},
    }
    assert initialization["actual_base_value"] is None
    assert initialization["runtime_reachability"] == "unknown"
    assert graph.facts["allocator.cleanup-real.sound-init.runtime"].status == "unknown"
    edge = graph.edges["allocator.cleanup-real.callback.call-0"]
    assert edge.source == "allocator.cleanup-real.callback"
    assert edge.target == "allocator.cleanup-real.stop"
    assert all(
        node.attributes["source_recovered"] is False for node in graph.nodes.values()
    )
    assert all(edge.status == "observed" for edge in graph.edges.values())
    assert not graph.conflicts()
    assert not graph.propagate_same_value()
    checks = [
        item
        for item in load_scoped_checks(ROOT / "targets/liero")
        if item["scope"] == "original_port_leaf_ready_on_owned_pic_vs_pascal"
    ]
    assert len(checks) == 1
    assert checks[0]["case_count"] == 512
    assert checks[0]["ready_only"] is True
    assert checks[0]["actual_device_verified"] is False
    assert checks[0]["source_recovered"] is False


def test_audit_marks_missing_byod_then_invalid_report_explicitly(tmp_path, monkeypatch):
    """Oracle: absent original skips; invalid present report fails without hiding its reason."""
    from engine.scoped_verification import _load_cleanup_port_checks

    target = tmp_path / "targets/liero"
    output = target / "build/cleanup-port/broken"
    output.mkdir(parents=True)
    (output / "result.json").write_text("{}")
    assert _load_cleanup_port_checks(target)[0]["status"] == "skipped"
    original = tmp_path / "extracted/liero/LIERO.EXE"
    original.parent.mkdir(parents=True)
    original.write_bytes(b"synthetic missing-evidence marker")

    def invalid(root, output):
        """Oracle: injected integrity failure, not BYOD validation."""
        raise ValueError("injected stale evidence")

    monkeypatch.setattr(probe, "validate_report", invalid)
    result = _load_cleanup_port_checks(target)[0]
    assert result["status"] == "invalid"
    assert result["reason"] == "injected stale evidence"


@pytest.mark.parametrize("module_offset", [0x13646, 0x24E])
def test_sound_initializer_and_caller_require_original_bytes(
    contract, monkeypatch, module_offset
):
    """Oracle: actual original prefix/caller identity, not listing-only sound port guesses."""
    from engine.scoped_verification import cleanup_sound_initialization_constraints

    binary, allocator, extra = probe.pilot.allocator_deduction_inputs(ROOT)
    header = int.from_bytes(binary[8:10], "little") * 16
    mutant = bytearray(binary)
    mutant[header + module_offset] ^= 1
    monkeypatch.setattr(
        probe.pilot,
        "allocator_deduction_inputs",
        lambda root: (bytes(mutant), allocator, extra),
    )
    with pytest.raises(ValueError, match="initialization bytes/relocations"):
        cleanup_sound_initialization_constraints(ROOT)


def test_sound_initializer_requires_actual_far_segment_relocation(
    contract, monkeypatch
):
    """Oracle: the caller's far segment is a real loader relocation, not an absolute segment."""
    import engine.alternate_streams as streams
    from engine.scoped_verification import cleanup_sound_initialization_constraints

    binary, _, _ = probe.pilot.allocator_deduction_inputs(ROOT)
    header = int.from_bytes(binary[8:10], "little") * 16
    relocations = set(streams._mz_relocation_locations(binary, header))
    relocations.remove(header + 0x24E + 19)
    monkeypatch.setattr(
        streams, "_mz_relocation_locations", lambda binary, header: relocations
    )
    with pytest.raises(ValueError, match="initialization bytes/relocations"):
        cleanup_sound_initialization_constraints(ROOT)
