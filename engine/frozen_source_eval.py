"""One-shot frozen evaluation of a supplied source candidate."""

from __future__ import annotations

import hashlib
import pathlib

from tools import liero_four_routine_pilot as pilot
from tools import liero_source_trial as trial

ROUTINE = "FUN_24dd_48e1"
SUITES = ("training", "terminal")


def corpus_hash(suite: str, routine: str = ROUTINE) -> str:
    return hashlib.sha256(b"".join(trial.cases(routine, suite))).hexdigest()


def run(
    root: pathlib.Path,
    output: pathlib.Path,
    source_path: pathlib.Path,
    routine: str = ROUTINE,
    suites: tuple[str, ...] = SUITES,
) -> dict:
    source = source_path.read_text()
    output.mkdir(parents=True, exist_ok=False)
    suite_results: dict[str, dict] = {}
    result: dict[str, object] = {
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "source_path": str(source_path.resolve()),
        "compile": {"status": "pending"},
        "suites": suite_results,
    }
    pilot.save(
        output / "freeze.json",
        {
            "routine": routine,
            "source_sha256": result["source_sha256"],
            "corpora": {
                suite: corpus_hash(suite, routine) for suite in SUITES
            },
            "policy": (
                "one compile, training first, terminal once only if training passes"
                if tuple(suites) == SUITES else f"training-only: {', '.join(suites)}"
            ),
            "budget": "no model requests, no repair, no source promotion",
        },
    )
    pilot.save(output / "result.json", result)
    compile_result = trial.compile_candidate(
        root, output / "candidate", routine, source
    )
    result["compile"] = compile_result
    pilot.save(output / "result.json", result)
    if compile_result["status"] != "passed":
        return result

    for suite in suites:
        inputs = trial.cases(routine, suite)
        original = trial.original(
            root, output / f"original-{suite}", routine, inputs
        )
        candidate = trial.run_candidate(output / "candidate", routine, inputs)
        suite_results[suite] = {
            "original": original,
            "candidate": candidate,
        }
        pilot.save(output / "result.json", result)
        if suite == "training" and candidate["status"] != "passed":
            break
    return result


def run_training(
    root: pathlib.Path,
    output: pathlib.Path,
    source_path: pathlib.Path,
    routine: str = ROUTINE,
) -> dict:
    return run(root, output, source_path, routine, suites=("training",))
