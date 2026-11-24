import json
from pathlib import Path

from engine import knowledge, oracle_gate, recovery

REPO = Path(__file__).resolve().parents[1]
TARGET = "liero"
PROMOTING = oracle_gate.PROMOTING_ORACLES


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def _verified_routines(data: dict) -> set[str]:
    verified: set[str] = set()
    for names in data.get("targets", {}).get(TARGET, {}).get("verified", {}).values():
        verified.update(names)
    return verified


def test_verified_pairs_are_canonical():
    data = knowledge.load(REPO / "knowledge" / "knowledge.json")
    verified = _verified_routines(data)
    examples = data.get("verified_pascal_examples", {}).get(
        oracle_gate._toolchain_key(REPO, TARGET), []
    )

    assert verified
    assert all(example.get("target") == TARGET for example in examples)
    assert all(example.get("fn") in verified for example in examples)
    assert all(example.get("oracle") in PROMOTING for example in examples)
    assert all(example.get("verification_status") == "verified" for example in examples)
    assert {example["fn"] for example in examples} == verified


def test_verified_routines_have_promoted_source_files():
    data = knowledge.load(REPO / "knowledge" / "knowledge.json")
    verified = _verified_routines(data)

    assert all((REPO / "targets" / TARGET / "src" / f"{name}.inc").is_file()
               for name in verified)


def test_original_binary_attestations_are_oracle_verified():
    data = knowledge.load(REPO / "knowledge" / "knowledge.json")
    verified = _verified_routines(data)
    ledger = _load(REPO / "targets" / TARGET / "recovery.json")
    original = {
        name for name, record in ledger["functions"].items()
        if record.get("verification", {}).get("original_binary_status") == "passed"
    }

    assert original <= verified


def test_audit_summary_matches_recovery_ledger():
    root = REPO / "targets" / TARGET
    ledger = _load(root / "recovery.json")
    records = ledger["functions"]
    inventory = _load(root / "functions.json")["functions"]
    summary = recovery.audit_target(root)["summary"]

    assert set(records) == {item["name"] for item in inventory}

    def behavior_verified(record: dict) -> bool:
        verification = record.get("verification", {})
        return (
            record.get("status") == "source_recovered"
            and verification.get("host_test_status") == "passed"
            and verification.get("has_external_effects") is not None
            and (
                verification.get("original_binary_status") == "passed"
                or (
                    verification.get("has_external_effects") is False
                    and verification.get("original_binary_status") == "not_required"
                )
            )
        )

    assert summary["function_count"] == len(records)
    assert summary["source_recovered"] == sum(
        record.get("status") == "source_recovered" for record in records.values()
    )
    assert summary["behavior_verified"] == sum(
        behavior_verified(record) for record in records.values()
    )
    assert summary["original_binary_verified"] == sum(
        record.get("verification", {}).get("original_binary_status") == "passed"
        for record in records.values()
    )
