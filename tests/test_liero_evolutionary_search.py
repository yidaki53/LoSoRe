from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Self

import pytest

from tools import liero_compare_routine_probe as probe
from tools import liero_evolutionary_search as search

ROOT = Path(__file__).resolve().parents[1]


def _seed_sources() -> tuple[dict[str, str], list[str]]:
    region = search._load_region(ROOT)
    source = """procedure FUN_24dd_3f86(param_1, param_2: Longint);
begin
  if srcLen <= destLen then
  begin
    if srcLen = 0 then
      Exit;
    Dec(srcLen);
    RegisterZeroFlag := False;
    RegisterCarryFlag := (srcByte < destByte);
  end
  else
  begin
    srcLen := destLen;
    if srcLen = 0 then
      Exit;
    Dec(srcLen);
    RegisterZeroFlag := False;
    RegisterCarryFlag := (srcByte < destByte);
  end;
  RegisterZeroFlag := (srcLen = destLen);
  RegisterCarryFlag := (srcLen < destLen);
end;
"""
    _, selected_region, _ = search._split(source, region)
    alternate_region = selected_region.replace(
        "RegisterCarryFlag := (srcByte < destByte);",
        "RegisterCarryFlag := False;",
        1,
    )
    return region, [
        source,
        search._replace_region(source, region, alternate_region),
    ]


def test_fitness_counts_matching_flag_bits_per_case() -> None:
    report = {
        "cases": [
            {
                "status": "passed",
                "expected_flags": 0,
                "candidate_flags": 0,
                "identity_valid": True,
                "stack_balanced": True,
                "original_flags": 0,
                "original_memory_changed": False,
                "candidate_memory_changed": False,
            },
            {
                "status": "failed",
                "expected_flags": 0,
                "candidate_flags": 1,
                "identity_valid": True,
                "stack_balanced": True,
                "original_flags": 0,
                "original_memory_changed": False,
                "candidate_memory_changed": False,
            },
        ]
    }

    fitness = search._fitness_from_report(report, True, 128)

    assert fitness.passing_cases == 1
    assert fitness.matching_flag_bits == 3
    assert fitness.oracle_safety == 1
    assert not fitness.training_pass


def test_fitness_rejects_build_and_oracle_safety_failures() -> None:
    report = {
        "cases": [
            {
                "status": "passed",
                "expected_flags": 0,
                "candidate_flags": 0,
                "identity_valid": True,
                "stack_balanced": True,
                "original_flags": 0,
                "original_memory_changed": False,
                "candidate_memory_changed": True,
            }
            for _ in probe.fixture_cases()
        ]
    }

    fitness = search._fitness_from_report(report, False, 128)

    assert fitness.target_build == 0
    assert fitness.oracle_safety == 0
    assert fitness.passing_cases == len(probe.fixture_cases())
    assert not fitness.training_pass


def test_fitness_is_lexicographic_with_safety_before_case_count() -> None:
    safe_but_fewer_passes = search.Fitness(1, 1, 1, 0, -500)
    unsafe_with_more_passes = search.Fitness(1, 0, 9, 18, -1)
    more_matching_bits = search.Fitness(1, 1, 1, 2, -500)
    smaller_region = search.Fitness(1, 1, 1, 2, -100)

    assert safe_but_fewer_passes > unsafe_with_more_passes
    assert more_matching_bits > safe_but_fewer_passes
    assert smaller_region > more_matching_bits


def test_deterministic_mutations_stay_inside_anchored_region() -> None:
    region, seeds = _seed_sources()
    prefix, selected_region, suffix = search._split(seeds[0], region)
    boundaries = (prefix, suffix)
    first = search.Individual(seeds[0], 0, (), "seed")
    second = search.Individual(seeds[1], 0, (), "seed")

    proposals = [
        search._deterministic_proposal(
            first,
            second,
            random.Random(seed),
            region,
            [search._split(source, region, boundaries)[1] for source in seeds],
            boundaries,
        )
        for seed in range(50)
    ]
    proposal = next(item for item in proposals if item is not None)
    proposal_prefix, proposal_region, proposal_suffix = search._split(
        proposal.source, region, boundaries
    )

    assert (proposal_prefix, proposal_suffix) == (prefix, suffix)
    assert proposal_region != selected_region


def test_mutated_anchor_lines_keep_region_boundaries_stable() -> None:
    region, seeds = _seed_sources()
    boundaries = search._region_boundaries(seeds[0], region)
    _, selected_region, _ = search._split(seeds[0], region, boundaries)
    replacement = selected_region.replace(
        "if srcLen <= destLen then", "if srcLen > destLen then"
    ).replace(
        "RegisterCarryFlag := (srcLen < destLen);",
        "RegisterCarryFlag := False;",
    )

    candidate = search._replace_region(seeds[0], region, replacement, boundaries)
    _, candidate_region, _ = search._split(candidate, region, boundaries)

    assert "if srcLen > destLen then" in candidate_region
    assert "RegisterCarryFlag := False;" in candidate_region


def test_llm_line_patch_rejects_missing_or_ambiguous_source_lines() -> None:
    with pytest.raises(search.MutationRejectedError, match="found 0"):
        search._apply_line_patch(
            "  First := True;\n",
            {
                "old_line": "Missing := True;",
                "new_line": "Missing := False;",
            },
        )

    with pytest.raises(search.MutationRejectedError, match="found 2"):
        search._apply_line_patch(
            "  First := True;\n  First := True;\n",
            {
                "old_line": "First := True;",
                "new_line": "First := False;",
            },
        )


def test_arm_is_seed_deterministic_and_obeys_evaluation_budget(
    tmp_path: Path, monkeypatch
) -> None:
    region, seeds = _seed_sources()
    boundaries = search._region_boundaries(seeds[0], region)
    monkeypatch.setattr(search, "POPULATION_SIZE", 3)
    monkeypatch.setattr(search, "MAX_GENERATIONS", 2)
    monkeypatch.setattr(search, "MAX_EVALUATIONS_PER_ARM", 4)
    monkeypatch.setattr(search, "MAX_PROPOSALS_PER_ARM", 20)
    monkeypatch.setattr(
        search,
        "_evaluate_source",
        lambda root, source, output_dir, **_kwargs: (
            search.Fitness(1, 1, 0, 0, -len(source)),
            None,
            [],
        ),
    )

    first = search._run_arm(
        ROOT,
        tmp_path / "run-a",
        "deterministic",
        seeds,
        region,
        boundaries,
        model="unused",
        endpoint="unused",
        temperature=0.0,
    )
    second = search._run_arm(
        ROOT,
        tmp_path / "run-b",
        "deterministic",
        seeds,
        region,
        boundaries,
        model="unused",
        endpoint="unused",
        temperature=0.0,
    )

    assert first["evaluations"] <= 4
    assert first["proposals"] <= 20
    assert (
        len({item["source_sha256"] for item in first["individuals"]})
        == first["evaluations"]
    )
    assert [item["source_sha256"] for item in first["individuals"]] == [
        item["source_sha256"] for item in second["individuals"]
    ]
    assert first["generations"] == second["generations"]


def test_arm_stops_evaluating_after_a_full_training_pass(
    tmp_path: Path, monkeypatch
) -> None:
    region, seeds = _seed_sources()
    boundaries = search._region_boundaries(seeds[0], region)
    evaluations = 0

    def evaluate(_root, _source, _output_dir, **_kwargs):
        nonlocal evaluations
        evaluations += 1
        passing_cases = 0 if evaluations < 3 else len(probe.fixture_cases())
        return (
            search.Fitness(1, 1, passing_cases, 0, -1),
            None,
            [],
        )

    monkeypatch.setattr(search, "_evaluate_source", evaluate)
    monkeypatch.setattr(search, "POPULATION_SIZE", 8)
    monkeypatch.setattr(search, "MAX_EVALUATIONS_PER_ARM", 32)
    monkeypatch.setattr(search, "MAX_PROPOSALS_PER_ARM", 64)

    result = search._run_arm(
        ROOT,
        tmp_path / "early-stop",
        "deterministic",
        seeds,
        region,
        boundaries,
        model="unused",
        endpoint="unused",
        temperature=0.0,
    )

    assert result["best"]["fitness"]["training_pass"]
    assert result["evaluations"] == 3


def test_failed_positive_control_blocks_arms_and_restores_include(
    tmp_path: Path, monkeypatch
) -> None:
    region, seeds = _seed_sources()
    root = tmp_path / "workspace"
    include = root / "targets/liero/src" / f"{search.ROUTINE_NAME}.inc"
    include.parent.mkdir(parents=True)
    original_include = b"disposable original source\n"
    include.write_bytes(original_include)
    control_source = tmp_path / "control.inc"
    control_source.write_text(seeds[0], encoding="utf-8")
    seed_paths = []
    for index, source in enumerate(seeds):
        seed_path = tmp_path / f"seed-{index}.inc"
        seed_path.write_text(source, encoding="utf-8")
        seed_paths.append(seed_path)

    monkeypatch.setattr(search, "_load_region", lambda _root: region)
    monkeypatch.setattr(search.draft, "_compile_errors", lambda _target: (False, []))
    monkeypatch.setattr(
        search.probe,
        "run_probe",
        lambda _root, _output, suite_id: {
            "fixture_suite": suite_id,
            "status": "failed",
        },
    )
    monkeypatch.setattr(
        search,
        "_run_arm",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("a search arm must not run after a failed positive control")
        ),
    )

    with pytest.raises(RuntimeError, match="failed positive-control suite"):
        search.run_search(
            root,
            control_source,
            seed_paths,
            Path("trial-output"),
            model="unused",
            endpoint="unused",
        )

    assert include.read_bytes() == original_include
    assert (root / "trial-output" / "controls").is_dir()


def test_llm_prompt_does_not_include_heldout_fixtures(
    monkeypatch,
) -> None:
    region, seeds = _seed_sources()
    boundaries = search._region_boundaries(seeds[0], region)
    member = search.Individual(seeds[0], 0, (), "seed")
    prompt_request: dict[str, str] = {}

    class Response:
        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(
                {
                    "response": json.dumps(
                        {
                            "old_line": "if srcLen <= destLen then",
                            "new_line": "if srcLen > destLen then",
                        }
                    )
                }
            ).encode()

    def fake_urlopen(request, timeout):
        prompt_request["body"] = request.data.decode("utf-8")
        prompt_request["timeout"] = str(timeout)
        return Response()

    monkeypatch.setattr(search.urllib.request, "urlopen", fake_urlopen)

    proposal = search._ollama_mutation(
        member,
        region,
        boundaries,
        model="local-test",
        endpoint="http://localhost:11434",
        temperature=0.0,
    )

    assert proposal.operator == "llm-mutation"
    assert "if srcLen > destLen then" in proposal.source
    assert "if srcLen <= destLen then" not in proposal.source
    request_payload = json.loads(prompt_request["body"])
    assert request_payload["options"]["num_predict"] == search.MAX_MUTATION_TOKENS
    assert (
        "held-out suite and its outcomes are unavailable" in request_payload["prompt"]
    )
    assert not any(
        case.name in request_payload["prompt"]
        for case in probe.held_out_fixture_cases()
    )
    assert prompt_request["timeout"] == "300"
