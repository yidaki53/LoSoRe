import hashlib
import json
from pathlib import Path

import pytest

from engine import object_lifecycle, object_setup, recovery


@pytest.fixture
def setup_target(tmp_path):
    root = tmp_path / "targets" / "test"
    root.mkdir(parents=True)
    binary = bytearray(0x20000)
    binary[:2] = b"MZ"
    binary[6:8] = (5).to_bytes(2, "little")
    binary[8:10] = (4).to_bytes(2, "little")
    binary[0x18:0x1A] = (0x1C).to_bytes(2, "little")
    regions = {}
    starts = {"constructor": 0x28409, "setup": 0x28FDC, "helper": 0x29069}
    for name, tokens in object_setup._REVIEWED_STREAMS.items():
        data = bytes.fromhex("".join(tokens.split()))
        address = starts[name]
        offset = 0x40 + address - 0x10000
        binary[offset : offset + len(data)] = data
        regions[name] = {"address": hex(address), "bytes_hex": data.hex()}
    relocation_sites = [0x28433, 0x29011, 0x2902C, 0x29042, 0x29061]
    for index, address in enumerate(relocation_sites):
        entry = 0x1C + 4 * index
        segment, offset = divmod(address - 0x10000, 16)
        binary[entry : entry + 2] = offset.to_bytes(2, "little")
        binary[entry + 2 : entry + 4] = segment.to_bytes(2, "little")
    binary_path = tmp_path / "program.exe"
    binary_path.write_bytes(binary)
    manifest = {
        "schema_version": 1,
        "binary": {"path": "program.exe", "sha256": hashlib.sha256(binary).hexdigest()},
        "image_mapping": {"load_segment": "0x1000", "header_bytes": 64},
        "object_setup_protocols": [
            {
                "kind": "liero_file_object_v1",
                "regions": regions,
            }
        ],
    }
    (root / "alternate_streams.json").write_text(json.dumps(manifest))
    return root


def test_setup_validates_complete_streams_and_conditional_slots(setup_target):
    (protocol,) = object_setup.load_verified_object_setups(setup_target)

    assert protocol["resolves_call_sites"] is False
    assert len(protocol["streams"]) == 3
    assert protocol["streams"]["setup"]["byte_count"] == 141
    assert protocol["streams"]["helper"]["byte_count"] == 90
    assert protocol["streams"]["setup"]["near_calls"] == [
        {"address": 0x2903B, "target": 0x29069}
    ]
    assert len(protocol["relocated_segment_words"]) == 5
    assert protocol["constructor_method_slots"] == {
        "0x10": "0x24dd:420c",
        "0x14": "0x0000:0000",
        "0x18": "0x0000:0000",
        "0x1c": "0x0000:0000",
    }
    input_outcomes = protocol["mode_outcomes"]["0xd7b1"]
    assert len(input_outcomes) == 2
    assert len(protocol["mode_outcomes"]["0xd7b2"]) == 3
    assert len(protocol["mode_outcomes"]["0xd7b3"]) == 3
    assert {tuple(row["method_slots"].items()) for row in input_outcomes} == {
        (),
        (("0x14", "0x24dd:375e"), ("0x18", "0x0000:0000"), ("0x1c", "0x24dd:37d3")),
    }
    assert all(not row["helper_called"] for row in input_outcomes)
    assert all(row["resulting_mode"] == "0xd7b1" for row in input_outcomes)
    assert any(row["method_slots"] == {} for row in input_outcomes)
    output = protocol["mode_outcomes"]["0xd7b3"]
    assert any(row["helper_called"] for row in output)
    assert all(
        row["resulting_mode"] == ("0xd7b2" if row["writes_methods"] else "0xd7b3")
        for row in output
    )
    assert any(
        row["method_slots"].get("0x14") == "0x24dd:37b3"
        and row["method_slots"].get("0x18") == "0x24dd:37b3"
        for row in output
    )
    assert {
        (
            row["method_slots"].get("0x14"),
            row["method_slots"].get("0x18"),
            row["helper_called"],
        )
        for row in protocol["mode_outcomes"]["0xd7b2"]
    } == {
        (None, None, False),
        ("0x24dd:378e", "0x0000:0000", False),
        ("0x24dd:37b3", "0x24dd:37b3", False),
    }
    assert {
        (
            row["method_slots"].get("0x14"),
            row["method_slots"].get("0x18"),
            row["helper_called"],
        )
        for row in output
    } == {
        (None, None, False),
        ("0x24dd:378e", "0x0000:0000", True),
        ("0x24dd:37b3", "0x24dd:37b3", False),
    }
    assert protocol["remaining_obligations"]
    assert len(protocol["streams"]["setup"]["dos_interrupt_sites"]) == 2
    assert len(protocol["streams"]["helper"]["dos_interrupt_sites"]) == 5
    assert protocol["streams"]["helper"]["return_sites"] == [0x290C2]


@pytest.fixture
def lifecycle_target(setup_target):
    """Oracle: synthetic binary with the independently reviewed input lifecycle."""
    manifest_path = setup_target / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    binary_path = setup_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    regions = {}
    for name, (entry, template) in object_lifecycle._INPUT_STREAMS.items():
        address = 0x24DD0 + entry
        data = bytes.fromhex("".join(template.split()))
        offset = 64 + address - 0x10000
        binary[offset : offset + len(data)] = data
        regions[name] = {"address": hex(address), "bytes_hex": data.hex()}
    manifest["object_setup_protocols"][0]["input_lifecycle_regions"] = regions
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    manifest_path.write_text(json.dumps(manifest))
    return setup_target


def test_input_open_and_reopen_keep_failure_paths(lifecycle_target):
    """Oracle: exact wrapper paths composed with checked setup outcomes."""
    (protocol,) = object_setup.load_verified_object_setups(lifecycle_target)
    lifecycle = protocol["input_lifecycle"]
    fresh = lifecycle["open_from_closed"]
    assert len(fresh) == 2
    (success,) = [row for row in fresh if row["mode"] == "0xd7b1"]
    (failure,) = [row for row in fresh if row["mode"] == "0xd7b0"]
    assert success["method_slots"]["0x14"] == "0x24dd:375e"
    assert success["status"] == "incoming"
    assert failure["method_slots"]["0x14"] == "0x0000:0000"
    assert failure["status"] == "setup_error"
    assert all(row["buffer_resets"] == ["0x8", "0xa"] for row in fresh)
    reopened = lifecycle["reopen_from_input"]
    assert len(reopened) == 4
    assert {tuple(row["method_returns"]) for row in reopened} == {
        (f"close:{close}", f"setup:{setup}")
        for close in ("zero", "nonzero")
        for setup in ("zero", "nonzero")
    }
    assert all(row["calls"] == ["close:0x1c", "setup:0x10"] for row in reopened)
    assert all(row["method_slots"]["0x14"] == "0x24dd:375e" for row in reopened)
    assert {row["status"] for row in reopened if row["mode"] == "0xd7b1"} == {
        "incoming",
        "close_error",
    }
    assert all(
        row["status"] == "setup_error" for row in reopened if row["mode"] == "0xd7b0"
    )
    assert all(row["mode"] == "0xd7b0" for row in lifecycle["close_from_input"])
    assert {row["status"] for row in lifecycle["close_from_input"]} == {
        "incoming",
        "close_error",
    }
    assert lifecycle["resolves_call_sites"] is False
    assert lifecycle["input_handler_method_slots_preserved"] is True
    assert lifecycle["open_cleanup_bytes"] == lifecycle["close_cleanup_bytes"] == 4
    (invalid,) = lifecycle["open_from_invalid_mode"]
    assert invalid["mode"] == "0xd7b3" and invalid["status"] == "0x0066"
    assert invalid["calls"] == invalid["buffer_resets"] == []
    (already_closed,) = lifecycle["close_from_closed"]
    assert already_closed["mode"] == "0xd7b0" and already_closed["status"] == "0x0067"
    assert already_closed["calls"] == []
    assert lifecycle["remaining_obligations"]


@pytest.mark.parametrize(
    "name",
    ["input_entry", "open", "close", "dispatch", "read_handler", "close_handler"],
)
def test_lifecycle_rejects_rewritten_stream(lifecycle_target, name):
    """Oracle: a changed call/store/cleanup cannot inherit the reviewed summary."""
    path = lifecycle_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    region = manifest["object_setup_protocols"][0]["input_lifecycle_regions"][name]
    data = bytearray.fromhex(region["bytes_hex"])
    data[-1] ^= 1
    region["bytes_hex"] = data.hex()
    binary_path = lifecycle_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    offset = 64 + int(region["address"], 16) - 0x10000
    binary[offset : offset + len(data)] = data
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="reviewed input lifecycle"):
        object_setup.load_verified_object_setups(lifecycle_target)


def test_lifecycle_rejects_missing_region(lifecycle_target):
    """Oracle: all reached input wrapper and method summaries need byte evidence."""
    path = lifecycle_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    del manifest["object_setup_protocols"][0]["input_lifecycle_regions"]["dispatch"]
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="requires all"):
        object_setup.load_verified_object_setups(lifecycle_target)


@pytest.mark.parametrize(
    ("name", "before", "after"),
    [
        ("read_handler", "2689450a", "26894514"),
        ("dispatch", "26ff19", "3eff19"),
        ("open", "e82500", "e82400"),
        ("open", "7412", "7411"),
        ("close", "26c74502b0d7", "26c74514b0d7"),
    ],
)
def test_lifecycle_rejects_slot_or_control_flow_changes(
    lifecycle_target, name, before, after
):
    """Oracle: same-hash fixture updates cannot authorize unreviewed state effects."""
    path = lifecycle_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    region = manifest["object_setup_protocols"][0]["input_lifecycle_regions"][name]
    original = region["bytes_hex"]
    assert before in original
    region["bytes_hex"] = original.replace(before, after, 1)
    binary_path = lifecycle_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    data = bytes.fromhex(region["bytes_hex"])
    offset = 64 + int(region["address"], 16) - 0x10000
    binary[offset : offset + len(data)] = data
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="reviewed input lifecycle"):
        object_setup.load_verified_object_setups(lifecycle_target)


def test_lifecycle_rejects_unexpected_fixup(lifecycle_target):
    """Oracle: a relocation cannot rewrite an otherwise matching slot instruction."""
    path = lifecycle_target / "alternate_streams.json"
    manifest = json.loads(path.read_text())
    binary_path = lifecycle_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    binary[6:8] = (6).to_bytes(2, "little")
    segment, offset = divmod(0x28520 - 0x10000, 16)
    binary[0x30:0x32] = offset.to_bytes(2, "little")
    binary[0x32:0x34] = segment.to_bytes(2, "little")
    binary_path.write_bytes(binary)
    manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="unexpected relocation"):
        object_setup.load_verified_object_setups(lifecycle_target)


@pytest.mark.parametrize(
    ("change", "error"),
    [
        ("stale", "stale for binary"),
        ("wrong-bytes", "bytes do not match"),
        ("changed-helper-branch", "reviewed helper stream"),
        ("changed-setup-call", "reviewed setup stream"),
        ("changed-constructor", "reviewed constructor stream"),
        ("missing-helper", "requires constructor, setup and helper"),
        ("overlap", "regions overlap"),
        ("wrong-helper-placement", "setup call does not target helper"),
        ("missing-relocation", "segment word lacks MZ relocation"),
        ("extra-code-relocation", "unexpected MZ relocation"),
        ("missing-mz", "require an MZ binary"),
        ("bad-kind", "unsupported object setup protocol"),
        ("wrong-setup-placement", "constructor pointer does not target"),
        ("duplicate-relocation", "segment relocation must occur once"),
    ],
)
def test_setup_fails_closed_on_mutated_evidence(setup_target, change, error):
    manifest_path = setup_target / "alternate_streams.json"
    manifest = json.loads(manifest_path.read_text())
    protocol = manifest["object_setup_protocols"][0]
    regions = protocol["regions"]
    binary_path = setup_target.parent.parent / "program.exe"
    binary = bytearray(binary_path.read_bytes())
    if change == "stale":
        binary[-1] ^= 1
    elif change == "wrong-bytes":
        regions["helper"]["bytes_hex"] = "c3"
    elif change in {
        "changed-helper-branch",
        "changed-setup-call",
        "changed-constructor",
    }:
        name, relative = {
            "changed-helper-branch": ("helper", 0x11),
            "changed-setup-call": ("setup", 0x60),
            "changed-constructor": ("constructor", 0),
        }[change]
        data = bytearray.fromhex(regions[name]["bytes_hex"])
        data[relative] ^= 1
        offset = 64 + int(regions[name]["address"], 16) - 0x10000
        binary[offset : offset + len(data)] = data
        regions[name]["bytes_hex"] = data.hex()
    elif change == "missing-helper":
        del regions["helper"]
    elif change in {"overlap", "wrong-helper-placement"}:
        address = 0x29000 if change == "overlap" else 0x29100
        data = bytes.fromhex(regions["helper"]["bytes_hex"])
        offset = 64 + address - 0x10000
        binary[offset : offset + len(data)] = data
        regions["helper"]["address"] = hex(address)
    elif change == "missing-relocation":
        binary[0x1C:0x1E] = (0x300).to_bytes(2, "little")
    elif change == "extra-code-relocation":
        binary[0x1C:0x1E] = (0x28409 - 0x20000).to_bytes(2, "little")
        binary[0x1E:0x20] = (0x1000).to_bytes(2, "little")
    elif change == "missing-mz":
        binary[:2] = b"XX"
    elif change == "bad-kind":
        protocol["kind"] = "generic"
    elif change == "wrong-setup-placement":
        address = 0x29200
        data = bytes.fromhex(regions["setup"]["bytes_hex"])
        offset = 64 + address - 0x10000
        binary[offset : offset + len(data)] = data
        regions["setup"]["address"] = hex(address)
    elif change == "duplicate-relocation":
        binary[6:8] = (6).to_bytes(2, "little")
        binary[0x30:0x34] = binary[0x1C:0x20]
    binary_path.write_bytes(binary)
    if change != "stale":
        manifest["binary"]["sha256"] = hashlib.sha256(binary).hexdigest()
    manifest_path.write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match=error):
        object_setup.load_verified_object_setups(setup_target)


def test_setup_evidence_is_optional(tmp_path):
    assert object_setup.load_verified_object_setups(tmp_path) == []
    (tmp_path / "alternate_streams.json").write_text('{"object_setup_protocols": []}')
    assert object_setup.load_verified_object_setups(tmp_path) == []


def test_setup_rejects_invalid_container(tmp_path):
    (tmp_path / "alternate_streams.json").write_text('{"object_setup_protocols": {}}')
    with pytest.raises(TypeError, match="must be an array"):
        object_setup.load_verified_object_setups(tmp_path)


def test_liero_setup_streams_and_audit_when_byod_available():
    repository = Path(__file__).resolve().parents[1]
    if not (repository / "extracted" / "liero" / "LIERO.EXE").is_file():
        pytest.skip("Liero BYOD executable is not available")
    root = repository / "targets" / "liero"
    (protocol,) = object_setup.load_verified_object_setups(root)
    assert protocol["streams"]["setup"]["entry"] == 0x28FDC
    assert protocol["streams"]["helper"]["entry"] == 0x29069
    assert protocol["streams"]["setup"]["near_calls"] == [
        {"address": 0x2903B, "target": 0x29069}
    ]
    assert [row["file_offset"] for row in protocol["relocated_segment_words"]] == [
        0x19BA3,
        0x1A781,
        0x1A79C,
        0x1A7B2,
        0x1A7D1,
    ]
    report = recovery.audit_target(root)
    assert report["object_setup_protocols"] == [protocol]
    assert report["summary"]["unresolved_control_transfers"] == 13
    assert report["summary"]["source_recovered"] == 26
    assert report["summary"]["behavior_verified"] == 10
    assert report["summary"]["original_binary_verified"] == 0
