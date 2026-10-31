from __future__ import annotations

import json
import shutil
import urllib.request
from pathlib import Path
from typing import Self

import pytest

from tools import liero_copy_routine_probe as probe


def _record(
    routine: str,
    destination: int,
    *,
    original: bool,
    ax: int | None = None,
    memory: bytes | None = None,
) -> dict:
    source_offset = probe.SOURCE_OFFSETS[routine]
    source_data = probe.EXPECTED_BYTES[source_offset][:12]
    expected_flags = (1 if destination == 0xFFFA else 0) | (
        0x40 if destination == 0 else 0
    )
    return {
        "entry": probe.ENTRY_OFFSETS[routine],
        "di_input": destination,
        "ax": (source_offset + 12) & 0xFFFF if ax is None else ax,
        "cx": 0,
        "si": 0x3456,
        "di": destination,
        "cs": 0x0191 if original else 0,
        "ds": 0x0191 if original else 0x1111,
        "es": 0x2000,
        "ss": 0x0191 if original else 0x2222,
        "sp_before": 0xFFFE if original else 0xD000,
        "sp_after": 0xFFFE if original else 0xD000,
        "flags": expected_flags,
        "memory": source_data + b"\xA5\xA5" if memory is None else memory,
    }


def _records(cases, *, original: bool) -> list[dict]:
    return [
        _record(routine, destination, original=original)
        for routine, destination in cases
    ]


def test_training_and_heldout_fixtures_are_distinct_and_bounded() -> None:
    assert len(probe.TRAINING_CASES) == len(probe.HELD_OUT_CASES) == 4
    assert set(probe.TRAINING_CASES).isdisjoint(probe.HELD_OUT_CASES)
    assert probe.ALL_CASES == probe.TRAINING_CASES + probe.HELD_OUT_CASES
    assert probe._suite_cases("training") == probe.TRAINING_CASES
    assert probe._suite_cases("heldout") == probe.HELD_OUT_CASES
    with pytest.raises(ValueError, match="unsupported"):
        probe._suite_cases("other")


def test_assembly_derived_pascal_positive_control_is_accepted() -> None:
    sources = probe._positive_control_sources()

    for routine in probe.ROUTINES:
        assert probe._validate_candidate_source(routine, sources[routine])

    unsafe_source = sources[probe.ROUTINES[0]].replace(
        "CopyCodeWordsToESDI;", "Halt(1);"
    )
    with pytest.raises(ValueError, match="exactly"):
        probe._validate_candidate_source(probe.ROUTINES[0], unsafe_source)


def test_pair_comparison_accepts_semantics_and_rejects_mutated_ax_and_memory() -> None:
    original = _records(probe.TRAINING_CASES, original=True)
    candidate = _records(probe.TRAINING_CASES, original=False)
    passed = probe._compare(original, candidate, probe.TRAINING_CASES)

    assert all(result["status"] == "passed" for result in passed)

    candidate[0]["ax"] ^= 1
    candidate[1]["memory"] = bytes([candidate[1]["memory"][0] ^ 1]) + candidate[1][
        "memory"
    ][1:]
    failed = probe._compare(original, candidate, probe.TRAINING_CASES)

    assert failed[0]["checks"]["ax"] is False
    assert failed[1]["checks"]["memory"] is False


def test_trace_decoder_rejects_empty_or_partial_records() -> None:
    with pytest.raises(ValueError, match="empty or has a partial"):
        probe._decode_records(b"")
    with pytest.raises(ValueError, match="empty or has a partial"):
        probe._decode_records(bytes(probe.RECORD_SIZE + 1))


@pytest.mark.parametrize(
    ("field", "changed"),
    [("case_count", 999), ("oracle", "unbound"), ("suite", "heldout")],
)
def test_replay_rejects_changed_scope_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, field: str, changed: object
) -> None:
    """Oracle: a replay must agree on both measured results and evidence scope."""
    candidate = tmp_path / "candidate-source"
    candidate.mkdir()
    sources = probe._positive_control_sources()
    for routine, source in sources.items():
        (candidate / f"{routine}.inc").write_text(source)
    runtime = "unit LieroRuntime;"
    (candidate / "LieroRuntime.pas").write_text(runtime)
    replay = {
        "status": "passed",
        "oracle": "isolated_original_bytes_dosbox_vs_pascal_host_model",
        "suite": "training",
        "case_count": 4,
        "binary_sha256": "binary",
        "harness_source_sha256": "harness",
        "harness_binary_sha256": "assembled",
        "probe_com_sha256": "com",
        "candidate_source_sha256": {
            routine: probe._sha256(source.encode())
            for routine, source in sources.items()
        },
        "candidate_runtime_sha256": probe._sha256(runtime.encode()),
        "results": [],
    }
    (tmp_path / "result.json").write_text(json.dumps({**replay, field: changed}))
    monkeypatch.setattr(probe, "run_probe", lambda *_args, **_kwargs: replay)

    with pytest.raises(ValueError, match="disagrees with original-byte replay"):
        probe.validate_saved_report(tmp_path)


def test_request_proposal_uses_json_schema(monkeypatch: pytest.MonkeyPatch) -> None:
    completion = json.dumps(probe._positive_control_sources())

    class Response:
        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps({"response": completion}).encode()

    def fake_urlopen(request: urllib.request.Request, timeout: int) -> Response:
        payload = json.loads(request.data)
        assert timeout == 300
        assert payload["stream"] is False
        assert payload["format"]["type"] == "object"
        assert set(payload["format"]["required"]) == set(probe.ROUTINES)
        assert payload["format"]["additionalProperties"] is False
        return Response()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    result, raw_response, error = probe._request_proposal(
        "prompt", model="local-model", endpoint="http://localhost:11434"
    )

    assert error is None
    assert result == completion
    assert json.loads(raw_response)["response"] == completion


def test_trial_does_not_run_candidate_heldout_before_training_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[str, str]] = []

    def fake_run_probe(
        output: Path,
        _root: Path,
        *,
        suite: str,
        candidate_sources=None,
        candidate_runtime_source=None,
    ) -> dict:
        calls.append((output.name, suite))
        return {
            "status": "passed",
            "case_count": 4,
            "results": [],
        }

    completion = json.dumps(probe._positive_control_sources())
    monkeypatch.setattr(probe, "run_probe", fake_run_probe)
    monkeypatch.setattr(probe, "validate_saved_report", lambda *_args: {})
    monkeypatch.setattr(
        probe,
        "_request_proposal",
        lambda *_args, **_kwargs: (
            completion,
            json.dumps({"response": completion}),
            None,
        ),
    )

    result = probe.run_trial(
        tmp_path / "trial",
        root=tmp_path,
        model="local-model",
        max_proposals=1,
    )

    assert result["status"] == "passed"
    assert result["training_hit_rate"] == result["scoped_pass_rate"] == 1.0
    response_path = tmp_path / "trial" / result["proposals"][0]["raw_response_path"]
    assert response_path.is_file()
    assert calls == [
        ("repository-baseline-training", "training"),
        ("control-training", "training"),
        ("candidate-001-training", "training"),
        ("control-heldout", "heldout"),
        ("candidate-001-heldout", "heldout"),
    ]


def test_trial_persists_malformed_raw_completion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake_run_probe(
        _output: Path,
        _root: Path,
        *,
        suite: str,
        candidate_sources=None,
        candidate_runtime_source=None,
    ) -> dict:
        return {
            "status": "passed",
            "case_count": 4,
            "results": [],
        }

    malformed_completion = '{"FUN_24dd_0582":'
    monkeypatch.setattr(probe, "run_probe", fake_run_probe)
    monkeypatch.setattr(probe, "validate_saved_report", lambda *_args: {})
    monkeypatch.setattr(
        probe,
        "_request_proposal",
        lambda *_args, **_kwargs: (
            malformed_completion,
            json.dumps({"response": malformed_completion}),
            None,
        ),
    )

    output = tmp_path / "trial"
    result = probe.run_trial(
        output,
        root=tmp_path,
        model="local-model",
        max_proposals=1,
    )

    proposal = output / "proposals/001"
    assert result["status"] == "failed"
    assert result["unique_candidates_evaluated"] == 0
    assert (proposal / "completion.txt").read_text() == malformed_completion
    assert (proposal / "raw-response.txt").is_file()
    rejection = json.loads((proposal / "rejection.json").read_text())
    assert "valid JSON" in rejection["reason"]


@pytest.mark.skipif(
    not (Path(__file__).resolve().parents[1] / "extracted/liero/LIERO.EXE").is_file()
    or any(shutil.which(tool) is None for tool in ("as", "ld", "dosbox", "fpc")),
    reason="Liero executable or original-byte probe tools are unavailable",
)
def test_original_byte_control_passes_and_replays(tmp_path: Path) -> None:
    candidate_sources = probe._positive_control_sources()
    for suite in ("training", "heldout"):
        output = tmp_path / suite
        report = probe.run_probe(
            output,
            suite=suite,
            candidate_sources=candidate_sources,
        )
        replay = probe.validate_saved_report(output)

        assert report["status"] == "passed"
        assert report["case_count"] == 4
        assert replay["results"] == report["results"]


@pytest.mark.skipif(
    not (Path(__file__).resolve().parents[1] / "extracted/liero/LIERO.EXE").is_file()
    or any(shutil.which(tool) is None for tool in ("as", "ld", "dosbox", "fpc")),
    reason="Liero executable or original-byte probe tools are unavailable",
)
def test_checked_in_copy_includes_pass_both_scoped_suites(tmp_path: Path) -> None:
    from engine.scoped_verification import load_scoped_checks

    root = Path(__file__).resolve().parents[1]
    target = tmp_path / "targets/liero"
    (target / "build/copy-parity").mkdir(parents=True)
    (target / "src").symlink_to(root / "targets/liero/src", target_is_directory=True)
    (target / "alternate_streams.json").symlink_to(
        root / "targets/liero/alternate_streams.json"
    )
    (tmp_path / "extracted").symlink_to(root / "extracted", target_is_directory=True)
    for suite in ("training", "heldout"):
        report = probe.run_probe(target / "build/copy-parity" / suite, suite=suite)

        assert report["status"] == "passed"
        assert report["case_count"] == 4

    checks = load_scoped_checks(target)
    assert len(checks) == 4
    assert all(check["status"] == "passed" for check in checks)
    assert all(check["case_count"] == 2 for check in checks)
    assert {check["suite"] for check in checks} == {"training", "heldout"}
