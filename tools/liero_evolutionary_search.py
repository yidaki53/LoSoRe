from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import time
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from engine import draft
from tools import liero_compare_routine_probe as probe

TARGET_NAME = "liero"
ROUTINE_NAME = probe.ROUTINE_NAME
POPULATION_SIZE = 8
MAX_GENERATIONS = 4
MAX_EVALUATIONS_PER_ARM = 32
MAX_PROPOSALS_PER_ARM = 64
MAX_MUTATION_TOKENS = 192
RANDOM_SEED = 20261030
DEFAULT_MODEL = "qwen2.5-coder:14b-instruct-q4_K_M"
DEFAULT_ENDPOINT = "http://localhost:11434"
OPERATORS = (
    "assignment-expression",
    "comparison-operator",
    "counter-guard-order",
    "flag-exit-toggle",
    "adjacent-assignment-swap",
    "branch-crossover",
)


class MutationRejectedError(ValueError):
    pass


@dataclass(frozen=True, order=True)
class Fitness:
    target_build: int
    oracle_safety: int
    passing_cases: int
    matching_flag_bits: int
    negative_region_bytes: int

    @property
    def training_pass(self) -> bool:
        return (
            self.target_build == 1
            and self.oracle_safety == 1
            and self.passing_cases == len(probe.fixture_cases())
        )


@dataclass
class Individual:
    source: str
    generation: int
    parents: tuple[str, ...]
    operator: str
    source_sha256: str = ""
    fitness: Fitness | None = None
    report_path: str | None = None
    prompt_sha256: str | None = None
    completion_sha256: str | None = None
    diagnostics: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.source_sha256 = _sha256(self.source.encode("utf-8"))


@dataclass(frozen=True)
class MutationProposal:
    source: str
    operator: str
    prompt: str | None = None
    completion: str | None = None


def _sha256(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def _load_region(root: Path) -> dict[str, str]:
    contract_path = root / "targets/liero/config/routine_contracts.json"
    payload = json.loads(contract_path.read_text(encoding="utf-8"))
    contract = payload["functions"][ROUTINE_NAME]
    region = contract.get("localized_repair_region")
    if not isinstance(region, dict):
        raise TypeError(f"{ROUTINE_NAME}: localized repair region is missing")
    if not all(
        isinstance(region.get(key), str) and region[key] for key in ("start", "end")
    ):
        raise ValueError(f"{ROUTINE_NAME}: localized repair anchors are malformed")
    return region


def _region_boundaries(source: str, region: dict[str, str]) -> tuple[str, str]:
    prefix, _, suffix = draft._split_localized_region(source, region)
    return prefix, suffix


def _split(
    source: str,
    region: dict[str, str],
    boundaries: tuple[str, str] | None = None,
) -> tuple[str, str, str]:
    if boundaries is None:
        return draft._split_localized_region(source, region)
    prefix, suffix = boundaries
    if not source.startswith(prefix) or not source.endswith(suffix):
        raise ValueError("candidate changed code outside the selected region")
    suffix_start = len(source) - len(suffix) if suffix else len(source)
    if suffix_start < len(prefix):
        raise ValueError("candidate is shorter than its selected-region boundaries")
    return prefix, source[len(prefix) : suffix_start], suffix


def _replace_region(
    source: str,
    region: dict[str, str],
    replacement: str,
    boundaries: tuple[str, str] | None = None,
) -> str:
    cleaned, reason = draft._sanitize_pascal_region_with_reason(replacement)
    if not cleaned:
        raise ValueError(f"invalid localized mutation: {reason}")
    if boundaries is None:
        return draft._replace_localized_region(source, region, cleaned)
    prefix, selected, suffix = _split(source, region, boundaries)
    newline = "\r\n" if "\r\n" in selected else "\n"
    cleaned = cleaned.strip("\r\n")
    if not cleaned.endswith(("\n", "\r")):
        cleaned += newline
    return prefix + cleaned + suffix


def _fitness_from_report(
    report: dict,
    target_build: bool,
    region_bytes: int,
) -> Fitness:
    cases = report.get("cases", [])
    safe = bool(cases) and all(
        case.get("identity_valid") is True
        and case.get("stack_balanced") is True
        and case.get("original_flags") == case.get("expected_flags")
        and case.get("original_memory_changed") is False
        and case.get("candidate_memory_changed") is False
        for case in cases
    )
    passing = sum(case.get("status") == "passed" for case in cases)
    matching_bits = sum(
        (
            probe.DEFINED_FLAG_MASK
            & ~(case.get("expected_flags", 0) ^ case.get("candidate_flags", 0))
        ).bit_count()
        for case in cases
    )
    return Fitness(
        int(target_build),
        int(safe),
        passing,
        matching_bits,
        -region_bytes,
    )


def _fitness_record(fitness: Fitness | None) -> dict | None:
    if fitness is None:
        return None
    return {
        "target_build": bool(fitness.target_build),
        "oracle_safety": bool(fitness.oracle_safety),
        "passing_cases": fitness.passing_cases,
        "matching_flag_bits": fitness.matching_flag_bits,
        "negative_region_bytes": fitness.negative_region_bytes,
        "training_pass": fitness.training_pass,
    }


def _assignment_mutation(
    region_text: str,
    rng: random.Random,
    seed_regions: list[str],
) -> str | None:
    assignment_pattern = re.compile(
        r"(?m)^(?P<indent>\s*)(?P<name>[A-Za-z_]\w*)\s*:=\s*"
        r"(?P<value>[^;\n]+);(?P<tail>\s*)$"
    )
    matches = list(assignment_pattern.finditer(region_text))
    if not matches:
        return None
    match = rng.choice(matches)
    name = match.group("name")
    values = {
        other.group("value").strip()
        for seed in seed_regions
        for other in assignment_pattern.finditer(seed)
        if other.group("name") == name
    }
    if name == "RegisterZeroFlag":
        values.update({"True", "False", "destByte = srcByte", "srcLen = destLen"})
    elif name == "RegisterCarryFlag":
        values.update(
            {
                "True",
                "False",
                "(srcByte < destByte)",
                "(srcLen < destLen)",
                "(destLen < srcLen)",
            }
        )
    else:
        values.update({"0", "1", "srcLen", "destLen", "srcByte", "destByte"})
    values.discard(match.group("value").strip())
    if not values:
        return None
    replacement = rng.choice(sorted(values))
    return (
        region_text[: match.start("value")]
        + replacement
        + region_text[match.end("value") :]
    )


def _comparison_mutation(region_text: str, rng: random.Random) -> str | None:
    pattern = re.compile(
        r"(?P<lhs>\b[A-Za-z_]\w*\b)\s*(?P<op><=|>=|<>|=|<|>)\s*(?P<rhs>\b[A-Za-z_]\w*\b)"
    )
    matches = list(pattern.finditer(region_text))
    if not matches:
        return None
    match = rng.choice(matches)
    operators = [
        operator
        for operator in ("<", "<=", ">", ">=", "=", "<>")
        if operator != match.group("op")
    ]
    replacement = rng.choice(operators)
    return (
        region_text[: match.start("op")] + replacement + region_text[match.end("op") :]
    )


def _counter_guard_mutation(region_text: str, rng: random.Random) -> str | None:
    lines = region_text.splitlines(keepends=True)
    candidates = []
    for index in range(len(lines) - 2):
        guard = re.search(
            r"\bif\s+([A-Za-z_]\w*)\s*=\s*0\s+then\s*$", lines[index].strip()
        )
        if not guard or lines[index + 1].strip().lower() != "exit;":
            continue
        decrement = re.fullmatch(
            r"\s*Dec\(\s*([A-Za-z_]\w*)\s*\);\s*", lines[index + 2], re.IGNORECASE
        )
        if decrement and decrement.group(1).lower() == guard.group(1).lower():
            candidates.append(index)
    if not candidates:
        return None
    index = rng.choice(candidates)
    lines[index + 1], lines[index + 2] = lines[index + 2], lines[index + 1]
    return "".join(lines)


def _flag_exit_mutation(region_text: str, rng: random.Random) -> str | None:
    pattern = re.compile(
        r"(?P<zero>\s*RegisterZeroFlag\s*:=\s*[^;\n]+;)"
        r"(?P<carry>\s*RegisterCarryFlag\s*:=\s*[^;\n]+;)"
        r"(?P<exit>\s*Exit;)?",
        re.IGNORECASE,
    )
    matches = list(pattern.finditer(region_text))
    if not matches:
        return None
    match = rng.choice(matches)
    if match.group("exit"):
        replacement = match.group("zero") + match.group("carry")
    else:
        replacement = match.group("zero") + match.group("carry") + "\n    Exit;"
    return region_text[: match.start()] + replacement + region_text[match.end() :]


def _assignment_swap_mutation(region_text: str, rng: random.Random) -> str | None:
    lines = region_text.splitlines(keepends=True)
    pairs = []
    for index in range(len(lines) - 1):
        if (
            re.match(r"\s*[A-Za-z_]\w*\s*:=", lines[index])
            and re.match(r"\s*[A-Za-z_]\w*\s*:=", lines[index + 1])
            and lines[index][: len(lines[index]) - len(lines[index].lstrip())]
            == lines[index + 1][
                : len(lines[index + 1]) - len(lines[index + 1].lstrip())
            ]
        ):
            pairs.append(index)
    if not pairs:
        return None
    index = rng.choice(pairs)
    lines[index], lines[index + 1] = lines[index + 1], lines[index]
    return "".join(lines)


def _top_level_blocks(region_text: str) -> list[tuple[int, int]]:
    lines = region_text.splitlines(keepends=True)
    depth = 0
    start = None
    blocks = []
    for index, line in enumerate(lines):
        tokens = re.findall(r"\b(begin|end)\b", line, re.IGNORECASE)
        for token in tokens:
            if token.lower() == "begin":
                if depth == 0:
                    start = index
                depth += 1
            else:
                depth -= 1
                if depth < 0:
                    return []
                if depth == 0 and start is not None:
                    blocks.append((start, index + 1))
                    start = None
    return blocks if depth == 0 else []


def _branch_crossover(
    first_region: str, second_region: str, rng: random.Random
) -> str | None:
    first_blocks = _top_level_blocks(first_region)
    second_blocks = _top_level_blocks(second_region)
    if len(first_blocks) != len(second_blocks) or len(first_blocks) < 2:
        return None
    first_lines = first_region.splitlines(keepends=True)
    second_lines = second_region.splitlines(keepends=True)
    block_index = rng.randrange(2)
    first_start, first_end = first_blocks[block_index]
    second_start, second_end = second_blocks[block_index]
    return "".join(
        first_lines[:first_start]
        + second_lines[second_start:second_end]
        + first_lines[first_end:]
    )


def _apply_line_patch(region_text: str, patch: dict) -> str:
    old_line = patch.get("old_line")
    new_line = patch.get("new_line")
    if not isinstance(old_line, str) or not old_line.strip():
        raise MutationRejectedError("LLM patch has no old_line")
    if not isinstance(new_line, str) or not new_line.strip():
        raise MutationRejectedError("LLM patch has no new_line")
    cleaned, reason = draft._sanitize_pascal_region_with_reason(new_line)
    if not cleaned or "\n" in cleaned or "\r" in cleaned:
        raise MutationRejectedError(f"LLM patch line rejected: {reason or 'multiline'}")
    lines = region_text.splitlines(keepends=True)
    matches = [
        index for index, line in enumerate(lines) if line.strip() == old_line.strip()
    ]
    if len(matches) != 1:
        raise MutationRejectedError(
            f"LLM old_line must match exactly one selected-region line; found {len(matches)}"
        )
    index = matches[0]
    original_line = lines[index]
    indentation = original_line[: len(original_line) - len(original_line.lstrip())]
    line_ending = "\r\n" if original_line.endswith("\r\n") else "\n"
    lines[index] = indentation + cleaned + line_ending
    patched_region = "".join(lines)
    if patched_region == region_text:
        raise MutationRejectedError("LLM patch does not change the selected region")
    return patched_region


def _deterministic_proposal(
    first: Individual,
    second: Individual,
    rng: random.Random,
    region: dict[str, str],
    seed_regions: list[str],
    boundaries: tuple[str, str],
) -> MutationProposal | None:
    _, first_region, _ = _split(first.source, region, boundaries)
    _, second_region, _ = _split(second.source, region, boundaries)
    operator = rng.choice(OPERATORS)
    if operator == "branch-crossover":
        changed = _branch_crossover(first_region, second_region, rng)
    else:
        mutators: dict[str, Callable[[], str | None]] = {
            "assignment-expression": lambda: _assignment_mutation(
                first_region, rng, seed_regions
            ),
            "comparison-operator": lambda: _comparison_mutation(first_region, rng),
            "counter-guard-order": lambda: _counter_guard_mutation(first_region, rng),
            "flag-exit-toggle": lambda: _flag_exit_mutation(first_region, rng),
            "adjacent-assignment-swap": lambda: _assignment_swap_mutation(
                first_region, rng
            ),
        }
        changed = mutators[operator]()
    if changed is None or changed == first_region:
        return None
    try:
        source = _replace_region(first.source, region, changed, boundaries)
    except ValueError:
        return None
    return MutationProposal(source, operator)


def _ollama_mutation(
    parent: Individual,
    region: dict[str, str],
    boundaries: tuple[str, str],
    *,
    model: str,
    endpoint: str,
    temperature: float,
) -> MutationProposal:
    _, selected_region, _ = _split(parent.source, region, boundaries)
    diagnostics = parent.diagnostics or ["no training evaluation feedback"]
    prompt = (
        "You are proposing one evolutionary mutation to a Pascal function "
        "candidate. Return one JSON object with string fields old_line and "
        "new_line. Each field must contain one complete Pascal source line "
        "without indentation or line breaks. old_line must exactly match one "
        "existing line in the selected region; new_line replaces only that "
        "line. Do not output Markdown, declarations, or a procedure header. "
        "Preserve the checked Longint ABI, use RealModeMemory, and do not "
        "change code outside the selected region. Use the training comparator "
        "feedback to improve behavior. The held-out suite and its outcomes "
        "are unavailable and must not be inferred.\n\n"
        f"Assembly-derived checked contract:\n"
        f"{parent_context(parent)}\n\n"
        "Training feedback:\n"
        + "\n".join(diagnostics)
        + "\n\nCurrent selected region:\n"
        + selected_region
    )
    url = endpoint.rstrip("/")
    if not url.endswith("/api/generate"):
        url += "/api/generate"
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": MAX_MUTATION_TOKENS,
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        body = json.loads(response.read().decode("utf-8"))
    completion = body.get("response")
    if not isinstance(completion, str) or not completion.strip():
        raise MutationRejectedError("local model returned an empty mutation proposal")
    try:
        patch = json.loads(completion)
    except json.JSONDecodeError as exc:
        raise MutationRejectedError("LLM mutation was not valid JSON") from exc
    if not isinstance(patch, dict):
        raise MutationRejectedError("LLM mutation JSON must be an object")
    patched_region = _apply_line_patch(selected_region, patch)
    try:
        source = _replace_region(parent.source, region, patched_region, boundaries)
    except ValueError as exc:
        raise MutationRejectedError(f"local model mutation rejected: {exc}") from exc
    return MutationProposal(source, "llm-mutation", prompt, completion)


def parent_context(parent: Individual) -> str:
    return (
        f"Routine: {ROUTINE_NAME}\n"
        "Arguments: packed 16:16 destination and source far pointers.\n"
        "Observed outputs: ZF and CF, far-call stack balance, tested-memory "
        "non-mutation.\n"
        "The original compares bytes through the shorter length; a mismatch "
        "leaves flags from source-minus-destination, otherwise flags reflect "
        "source length minus destination length.\n"
        f"Current candidate SHA-256: {parent.source_sha256}"
    )


def _select_parent(
    population: list[Individual], rng: random.Random, count: int = 3
) -> Individual:
    contestants = rng.sample(population, min(count, len(population)))
    return max(contestants, key=lambda member: member.fitness or Fitness(0, 0, 0, 0, 0))


def _evaluate_source(
    root: Path,
    source: str,
    output_dir: Path,
    *,
    suite_id: str = probe.TRAINING_SUITE,
    boundaries: tuple[str, str] | None = None,
) -> tuple[Fitness, dict | None, list[str]]:
    target_root = root / "targets/liero"
    include = target_root / "src" / f"{ROUTINE_NAME}.inc"
    include.write_text(source, encoding="utf-8")
    compile_errors, compile_diagnostics = draft._compile_errors(target_root)
    _, region_text, _ = _split(source, _load_region(root), boundaries)
    region_bytes = len(region_text.encode("utf-8"))
    if compile_errors:
        return Fitness(0, 0, 0, 0, -region_bytes), None, compile_diagnostics
    try:
        report = probe.run_probe(root, output_dir, suite_id)
    except RuntimeError as exc:
        if not str(exc).startswith("Free Pascal compilation failed:"):
            raise
        return Fitness(0, 0, 0, 0, -region_bytes), None, [str(exc)]
    return (
        _fitness_from_report(report, True, region_bytes),
        report,
        compile_diagnostics,
    )


def _generate_child(
    arm: str,
    first: Individual,
    second: Individual,
    rng: random.Random,
    region: dict[str, str],
    seed_regions: list[str],
    boundaries: tuple[str, str],
    *,
    model: str,
    endpoint: str,
    temperature: float,
) -> MutationProposal | None:
    if arm == "deterministic":
        return _deterministic_proposal(
            first, second, rng, region, seed_regions, boundaries
        )
    if arm != "llm-assisted":
        raise ValueError(f"unknown evolutionary search arm: {arm}")
    return _ollama_mutation(
        first,
        region,
        boundaries,
        model=model,
        endpoint=endpoint,
        temperature=temperature,
    )


def _individual_record(member: Individual) -> dict:
    return {
        "source_sha256": member.source_sha256,
        "generation": member.generation,
        "parents": list(member.parents),
        "operator": member.operator,
        "fitness": _fitness_record(member.fitness),
        "report_path": member.report_path,
        "prompt_sha256": member.prompt_sha256,
        "completion_sha256": member.completion_sha256,
        "diagnostics": member.diagnostics,
    }


def _run_arm(
    root: Path,
    output_dir: Path,
    arm: str,
    seed_sources: list[str],
    region: dict[str, str],
    boundaries: tuple[str, str],
    *,
    model: str,
    endpoint: str,
    temperature: float,
) -> dict:
    rng = random.Random(RANDOM_SEED)
    seed_regions = [_split(source, region, boundaries)[1] for source in seed_sources]
    evaluated: dict[str, Individual] = {}
    population: list[Individual] = []
    proposal_count = 0
    evaluation_count = 0
    generation_records: list[dict] = []
    rejected_proposals: list[str] = []

    def evaluate(member: Individual) -> Individual:
        nonlocal evaluation_count
        evaluation_count += 1
        candidate_path = output_dir / "candidates" / arm / f"{member.source_sha256}.inc"
        candidate_path.parent.mkdir(parents=True, exist_ok=True)
        candidate_path.write_text(member.source, encoding="utf-8")
        attempt_dir = (
            output_dir
            / "evaluations"
            / arm
            / f"{evaluation_count:03d}-{member.source_sha256}"
        )
        fitness, report, diagnostics = _evaluate_source(
            root, member.source, attempt_dir, boundaries=boundaries
        )
        member.fitness = fitness
        member.diagnostics = diagnostics
        if report is not None:
            member.report_path = attempt_dir.relative_to(root).as_posix()
            member.diagnostics = [
                f"{case['name']}: expected {case['expected_flags']:#06x}, "
                f"got {case['candidate_flags']:#06x}"
                for case in report["cases"]
                if case["status"] != "passed"
            ]
        evaluated[member.source_sha256] = member
        return member

    for index, source in enumerate(seed_sources):
        member = Individual(source, 0, (), f"seed-{index + 1}")
        if member.source_sha256 not in evaluated:
            population.append(evaluate(member))
            if member.fitness and member.fitness.training_pass:
                break

    while (
        len(population) < POPULATION_SIZE
        and evaluation_count < MAX_EVALUATIONS_PER_ARM
        and proposal_count < MAX_PROPOSALS_PER_ARM
        and not any(
            member.fitness and member.fitness.training_pass for member in population
        )
    ):
        proposal_count += 1
        parent = _select_parent(population, rng)
        other = _select_parent(population, rng)
        try:
            proposal = _generate_child(
                arm,
                parent,
                other,
                rng,
                region,
                seed_regions,
                boundaries,
                model=model,
                endpoint=endpoint,
                temperature=temperature,
            )
        except MutationRejectedError as exc:
            rejected_proposals.append(str(exc))
            continue
        if proposal is None or _sha256(proposal.source.encode()) in evaluated:
            continue
        member = Individual(
            proposal.source,
            0,
            (parent.source_sha256, other.source_sha256),
            proposal.operator,
        )
        if proposal.prompt is not None and proposal.completion is not None:
            capture = (
                output_dir / "generations" / arm / f"proposal-{proposal_count:03d}"
            )
            capture.mkdir(parents=True, exist_ok=True)
            (capture / "prompt.txt").write_text(proposal.prompt, encoding="utf-8")
            (capture / "completion.txt").write_text(
                proposal.completion, encoding="utf-8"
            )
            member.prompt_sha256 = _sha256(proposal.prompt.encode())
            member.completion_sha256 = _sha256(proposal.completion.encode())
        population.append(evaluate(member))
        if member.fitness and member.fitness.training_pass:
            break

    for generation in range(1, MAX_GENERATIONS + 1):
        if not population:
            break
        population.sort(
            key=lambda member: member.fitness or Fitness(0, 0, 0, 0, 0), reverse=True
        )
        best = population[0]
        generation_records.append(
            {
                "generation": generation - 1,
                "evaluations": evaluation_count,
                "best_fitness": _fitness_record(best.fitness),
                "best_sha256": best.source_sha256,
                "population_sha256": [member.source_sha256 for member in population],
            }
        )
        if best.fitness and best.fitness.training_pass:
            break
        if (
            generation == MAX_GENERATIONS
            or evaluation_count >= MAX_EVALUATIONS_PER_ARM
            or proposal_count >= MAX_PROPOSALS_PER_ARM
        ):
            break

        elites = population[:2]
        next_population = list(elites)
        while (
            len(next_population) < POPULATION_SIZE
            and evaluation_count < MAX_EVALUATIONS_PER_ARM
            and proposal_count < MAX_PROPOSALS_PER_ARM
        ):
            proposal_count += 1
            first = _select_parent(population, rng)
            second = _select_parent(population, rng)
            try:
                proposal = _generate_child(
                    arm,
                    first,
                    second,
                    rng,
                    region,
                    seed_regions,
                    boundaries,
                    model=model,
                    endpoint=endpoint,
                    temperature=temperature,
                )
            except MutationRejectedError as exc:
                rejected_proposals.append(str(exc))
                continue
            if proposal is None:
                continue
            candidate_hash = _sha256(proposal.source.encode("utf-8"))
            if candidate_hash in evaluated:
                continue
            member = Individual(
                proposal.source,
                generation,
                (first.source_sha256, second.source_sha256),
                proposal.operator,
            )
            if proposal.prompt is not None and proposal.completion is not None:
                capture = (
                    output_dir / "generations" / arm / f"proposal-{proposal_count:03d}"
                )
                capture.mkdir(parents=True, exist_ok=True)
                (capture / "prompt.txt").write_text(proposal.prompt, encoding="utf-8")
                (capture / "completion.txt").write_text(
                    proposal.completion, encoding="utf-8"
                )
                member.prompt_sha256 = _sha256(proposal.prompt.encode())
                member.completion_sha256 = _sha256(proposal.completion.encode())
            next_population.append(evaluate(member))
            if member.fitness and member.fitness.training_pass:
                break
        population = next_population

    population.sort(
        key=lambda member: member.fitness or Fitness(0, 0, 0, 0, 0), reverse=True
    )
    best = population[0] if population else None
    return {
        "arm": arm,
        "model": model if arm == "llm-assisted" else None,
        "temperature": temperature if arm == "llm-assisted" else None,
        "rng_seed": RANDOM_SEED,
        "population_size": POPULATION_SIZE,
        "max_generations": MAX_GENERATIONS,
        "max_evaluations": MAX_EVALUATIONS_PER_ARM,
        "max_proposals": MAX_PROPOSALS_PER_ARM,
        "evaluations": evaluation_count,
        "proposals": proposal_count,
        "rejected_proposals": rejected_proposals,
        "best": _individual_record(best) if best else None,
        "generations": generation_records,
        "individuals": [
            _individual_record(member)
            for member in sorted(
                evaluated.values(),
                key=lambda item: (
                    item.fitness or Fitness(0, 0, 0, 0, 0),
                    item.source_sha256,
                ),
                reverse=True,
            )
        ],
    }


def _validate_report_set(root: Path, output_dirs: list[Path], include: Path) -> None:
    original = include.read_bytes()
    try:
        for output_dir in output_dirs:
            candidate = output_dir / "candidate" / f"{ROUTINE_NAME}.inc"
            include.write_bytes(candidate.read_bytes())
            probe.validate_saved_report(output_dir, root)
    finally:
        include.write_bytes(original)


def _run_search_in_workspace(
    root: Path,
    control_source: Path,
    seed_candidate_paths: list[Path],
    output_dir: Path,
    *,
    model: str = DEFAULT_MODEL,
    endpoint: str = DEFAULT_ENDPOINT,
    temperature: float = 0.0,
) -> dict:
    if len(seed_candidate_paths) != 2:
        raise ValueError("the search requires exactly two failed candidate seeds")
    if not 0.0 <= temperature <= 2.0:
        raise ValueError("temperature must be between 0.0 and 2.0")
    root = root.resolve()
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    output_dir = output_dir.resolve()
    if output_dir.exists():
        raise FileExistsError(f"search output already exists: {output_dir}")
    try:
        output_dir.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            "search output must be inside the disposable target workspace"
        ) from exc
    control_source = (
        control_source if control_source.is_absolute() else root / control_source
    ).resolve()
    seed_candidate_paths = [
        (path if path.is_absolute() else root / path).resolve()
        for path in seed_candidate_paths
    ]
    target_root = root / "targets/liero"
    include = target_root / "src" / f"{ROUTINE_NAME}.inc"
    original_source = include.read_bytes()
    region = _load_region(root)
    seed_sources = [path.read_text(encoding="utf-8") for path in seed_candidate_paths]
    seed_parts = [_split(source, region) for source in seed_sources]
    if seed_parts[0][0] != seed_parts[1][0] or seed_parts[0][2] != seed_parts[1][2]:
        raise ValueError("seed candidates differ outside the localized repair region")
    boundaries = (seed_parts[0][0], seed_parts[0][2])

    output_dir.mkdir(parents=True)
    control_dir = output_dir / "controls"
    control_dir.mkdir()
    control_text = control_source.read_text(encoding="utf-8")
    control_reports = []
    try:
        include.write_text(control_text, encoding="utf-8")
        build_errors, build_diagnostics = draft._compile_errors(target_root)
        if build_errors:
            raise RuntimeError(
                "checked implementation failed its full-target positive-control "
                f"build: {'; '.join(build_diagnostics)}"
            )
        for suite_id in (probe.TRAINING_SUITE, probe.HELD_OUT_SUITE):
            report_dir = control_dir / suite_id
            report = probe.run_probe(root, report_dir, suite_id)
            if report["status"] != "passed":
                raise RuntimeError(
                    f"checked implementation failed positive-control suite {suite_id}"
                )
            control_reports.append(report_dir)
    finally:
        include.write_bytes(original_source)

    deterministic = _run_arm(
        root,
        output_dir,
        "deterministic",
        seed_sources,
        region,
        boundaries,
        model=model,
        endpoint=endpoint,
        temperature=temperature,
    )
    llm_assisted = _run_arm(
        root,
        output_dir,
        "llm-assisted",
        seed_sources,
        region,
        boundaries,
        model=model,
        endpoint=endpoint,
        temperature=temperature,
    )

    heldout_reports = []
    for arm_record in (deterministic, llm_assisted):
        best = arm_record["best"]
        if not best or not best["fitness"]["training_pass"]:
            arm_record["heldout"] = None
            continue
        candidate_path = (
            output_dir
            / "candidates"
            / arm_record["arm"]
            / f"{best['source_sha256']}.inc"
        )
        include.write_bytes(candidate_path.read_bytes())
        holdout_dir = output_dir / "heldout" / arm_record["arm"]
        report = probe.run_probe(root, holdout_dir, probe.HELD_OUT_SUITE)
        arm_record["heldout"] = {
            "status": report["status"],
            "case_count": report["case_count"],
            "passed_cases": sum(case["status"] == "passed" for case in report["cases"]),
            "report_path": holdout_dir.relative_to(root).as_posix(),
        }
        heldout_reports.append(holdout_dir)
    include.write_bytes(original_source)

    all_report_dirs = control_reports + heldout_reports
    for arm_record in (deterministic, llm_assisted):
        all_report_dirs.extend(
            root / member["report_path"]
            for member in arm_record["individuals"]
            if member["report_path"]
        )
    _validate_report_set(root, all_report_dirs, include)

    report = {
        "schema_version": 1,
        "target": TARGET_NAME,
        "routine": ROUTINE_NAME,
        "training_suite": {
            "id": probe.TRAINING_SUITE,
            "sha256": probe.fixture_suite_sha256(probe.TRAINING_SUITE),
            "cases": len(probe.fixture_suite(probe.TRAINING_SUITE)),
        },
        "heldout_suite": {
            "id": probe.HELD_OUT_SUITE,
            "sha256": probe.fixture_suite_sha256(probe.HELD_OUT_SUITE),
            "cases": len(probe.fixture_suite(probe.HELD_OUT_SUITE)),
        },
        "limits": {
            "population_size_per_arm": POPULATION_SIZE,
            "generations_per_arm": MAX_GENERATIONS,
            "unique_evaluations_per_arm": MAX_EVALUATIONS_PER_ARM,
            "proposals_per_arm": MAX_PROPOSALS_PER_ARM,
            "rng_seed": RANDOM_SEED,
        },
        "controls": [
            {
                "suite_id": report.get("fixture_suite"),
                "status": report.get("status"),
                "case_count": report.get("case_count"),
                "report_path": path.relative_to(root).as_posix(),
            }
            for report, path in zip(
                [
                    json.loads((path / "result.json").read_text(encoding="utf-8"))
                    for path in control_reports
                ],
                control_reports,
                strict=True,
            )
        ],
        "arms": {
            "deterministic": deterministic,
            "llm-assisted": llm_assisted,
        },
        "heldout_reports": [
            {
                "suite_id": probe.HELD_OUT_SUITE,
                "status": json.loads(
                    (path / "result.json").read_text(encoding="utf-8")
                )["status"],
                "report_path": path.relative_to(root).as_posix(),
            }
            for path in heldout_reports
        ],
        "control_source_sha256": _sha256(control_source.read_bytes()),
        "seed_candidates": [
            {"path": str(path), "sha256": _sha256(path.read_bytes())}
            for path in seed_candidate_paths
        ],
        "evolution_tool_sha256": _sha256(Path(__file__).read_bytes()),
        "contract_sha256": _sha256(
            (target_root / "config/routine_contracts.json").read_bytes()
        ),
        "completed_at_epoch": time.time(),
    }
    report_path = output_dir / "summary.json"
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return report


def run_search(
    root: Path,
    control_source: Path,
    seed_candidate_paths: list[Path],
    output_dir: Path,
    *,
    model: str = DEFAULT_MODEL,
    endpoint: str = DEFAULT_ENDPOINT,
    temperature: float = 0.0,
) -> dict:
    root = root.resolve()
    include = root / "targets/liero/src" / f"{ROUTINE_NAME}.inc"
    original_source = include.read_bytes()
    try:
        return _run_search_in_workspace(
            root,
            control_source,
            seed_candidate_paths,
            output_dir,
            model=model,
            endpoint=endpoint,
            temperature=temperature,
        )
    finally:
        include.write_bytes(original_source)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--control-source", type=Path, required=True)
    parser.add_argument("--seed-candidate", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--temperature", type=float, default=0.0)
    args = parser.parse_args()
    report = run_search(
        args.root,
        args.control_source,
        args.seed_candidate,
        args.output,
        model=args.model,
        endpoint=args.endpoint,
        temperature=args.temperature,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
