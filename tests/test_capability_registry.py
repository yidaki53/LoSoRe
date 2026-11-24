import pathlib

from engine import capability_learner, capability_registry, generic_synthesizer


def _evidence(instructions, addresses=None, segments=None):
    assembly = {"instructions": list(instructions)}
    if addresses is not None:
        assembly["addresses"] = list(addresses)
    if segments is not None:
        assembly["segments"] = list(segments)
    return {
        "target": "synthetic",
        "routine": "FN",
        "static_evidence": {"assembly": assembly},
    }


def test_signature_classifies_bounded_branches():
    internal = _evidence(
        ["JZ 0x0000:0004", "NOP", "RET"],
        addresses=[0, 4, 8], segments=[0, 0, 0],
    )
    external = _evidence(["JZ 0x1234:0004", "NOP", "RET"])
    assert "control:branch-internal" in capability_registry.signature(internal)["tokens"]
    assert "control:branch-external" in capability_registry.signature(external)["tokens"]


def test_detect_uses_evidence_features_not_routine_identity():
    evidence = _evidence(
        ["MOV AX,word ptr SS:[BP + SI + 0x2]", "RET"]
    )
    assert capability_registry.detect(evidence) == [
        "arena-mapped-memory", "bp-index-address-normalization",
    ]


def test_verified_outcome_is_persisted_and_recalled_by_signature(tmp_path):
    evidence = _evidence(["JZ 0x1234:0004", "NOP", "RET"])
    capability_registry.record_outcome(
        tmp_path, "synthetic", "FN", ["future-capability"], "verified", evidence,
    )
    assert "future-capability" in capability_registry.select(tmp_path, evidence)
    data = capability_registry.load(tmp_path)
    assert data["capabilities"]["future-capability"]["status"] == "verified"
    assert data["capabilities"]["future-capability"]["outcomes"]["verified"] == 1


def test_unsupported_evidence_records_reusable_gap(tmp_path):
    evidence = _evidence(["CALL 0x0000:0008", "RET"])
    first = capability_registry.observe_unsupported(tmp_path, "synthetic", "FN", evidence)
    second = capability_registry.observe_unsupported(tmp_path, "synthetic", "FN2", evidence)
    assert first["hash"] == second["hash"]
    assert second["count"] == 2
    gap = capability_registry.load(tmp_path)["gaps"][first["hash"]]
    assert {item["routine"] for item in gap["examples"]} == {"FN", "FN2"}


def test_generic_synthesizer_exposes_detected_capabilities():
    evidence = _evidence(
        ["JZ 0x0000:0004", "NOP", "RET"],
        addresses=[0, 4, 8], segments=[0, 0, 0],
    )
    result = generic_synthesizer.synthesize(evidence)
    assert "bounded-internal-branches" in result["ir"]["capabilities"]


def test_repeated_gap_proposes_candidate_from_verified_base(tmp_path):
    evidence = _evidence(["JZ 0x1234:0004", "NOP", "RET"])
    capability_registry.record_outcome(
        tmp_path, "synthetic", "BASE", ["base-capability"], "verified", evidence,
    )
    capability_registry.observe_unsupported(tmp_path, "synthetic", "FN", evidence)
    capability_registry.observe_unsupported(tmp_path, "synthetic", "FN", evidence)
    proposals = capability_learner.propose(tmp_path, min_gap_count=2)
    assert len(proposals) == 1
    entry = capability_registry.load(tmp_path)["capabilities"][proposals[0]]
    assert entry["source"] == "gap-generalization"
    assert entry["renderer"] == "asm-emulation-v1"
    assert proposals[0] in capability_registry.select(tmp_path, evidence)


def test_capability_gap_prioritizes_affected_frontier_rows(tmp_path):
    evidence = _evidence(["CALL 0x0000:0008", "RET"])
    capability_registry.observe_unsupported(tmp_path, "synthetic", "FN", evidence)
    capability_registry.observe_unsupported(tmp_path, "synthetic", "FN", evidence)
    assert capability_learner.frontier_priority(tmp_path, "synthetic")["FN"] > 0
    assert capability_learner.frontier_priority(tmp_path, "other") == {}
