from pathlib import Path

from engine import knowledge, oracle_gate, target_packet

REPO = Path(__file__).resolve().parents[1]


def test_promote_refuses_missing_gate(tmp_path):
    result = oracle_gate.promote(
        tmp_path,
        "demo",
        "FUN_1000_0000",
        "generic-capability-ir",
        tmp_path / "candidate.inc",
        tmp_path / "eval",
        str(tmp_path / "arm.json"),
        oracle="routine-trace-parity",
    )

    assert result["status"] == "refused"
    assert "explicit oracle gate decision" in result["reason"]
    assert not (tmp_path / "targets" / "demo" / "src" / "FUN_1000_0000.inc").exists()


def test_routine_trace_blocker_reports_fixture_failure(monkeypatch, tmp_path):
    def fail(*_args, **_kwargs):
        raise ValueError("unsupported control flow")

    monkeypatch.setattr(oracle_gate.contract_oracle, "fixture", fail)

    assert oracle_gate.routine_trace_blocker(
        "demo", "FUN_1000_0000", tmp_path
    ) == "ValueError: unsupported control flow"


def test_composed_evidence_is_gated_after_rewrite(monkeypatch):
    original = target_packet._evidence_gate
    calls = []

    def capture(record, assembly, facts):
        result = original(record, assembly, facts)
        calls.append((record, assembly, facts, result))
        return result

    monkeypatch.setattr(target_packet, "_evidence_gate", capture)
    evidence = target_packet.evidence_for_routine(
        REPO, "liero", "FUN_24dd_4654"
    )

    assert calls
    composed = calls[-1]
    assert composed[2]["method"] == "composed_instruction_prefix"
    assert "residue" in composed[2]
    assert evidence["static_evidence"]["gate"] == composed[3]
    assert evidence["static_evidence"]["raw_byte_facts"]["method"] == (
        "composed_instruction_prefix"
    )


def test_dl_status_never_changes_weights():
    data = knowledge.load(REPO / "knowledge" / "knowledge.json")
    status = oracle_gate.dl_status(REPO, "liero", data=data)
    readiness = status["readiness"]

    assert status["oracle_gated"] is True
    assert status["status"] == (
        "eligible" if not readiness["pascal_corpus_blockers"] else "blocked"
    )
    assert readiness["source_review_revalidated"] is False
    assert readiness["behavioral_improvement_established"] is False
    assert readiness["changes_weights"] is False


def test_non_promoting_oracle_never_unblocks_dl():
    decision = {
        "status": "verified",
        "promotion_eligible": True,
        "oracle": "dat-parity",
    }

    assert oracle_gate.decide("dat-parity", decision)["status"] == "scoped"
    assert oracle_gate.decide("dat-parity", decision)["promotion_eligible"] is False
    assert oracle_gate.decide("constructor-parity", decision)["status"] == "scoped"
