import hashlib
import json
from pathlib import Path

import pytest

from engine import improve_loop


def test_verify_returns_subprocess_exit_code(tmp_path, monkeypatch):
    monkeypatch.setattr(
        improve_loop,
        "_run",
        lambda command: (7, "", ""),
    )

    result = improve_loop._verify(
        "target",
        Path(tmp_path / "byod"),
        Path(tmp_path / "build"),
        oracle="dat-parity",
    )

    assert result == 7


def test_verified_function_count_ignores_format_oracle_paths():
    data = {
        "targets": {
            "liero": {
                "verified": {
                    "dat-parity": ["LIERO.DAT"],
                    "byte-exact": ["src/FUN_1000_01a1.inc"],
                }
            }
        }
    }

    assert improve_loop._verified_functions(
        data, "liero", "dat-parity", {"FUN_1000_01a1"}
    ) == set()
    assert improve_loop._verified_functions(
        data, "liero", "byte-exact", {"FUN_1000_01a1"}
    ) == {"FUN_1000_01a1"}


def test_draft_supports_targeted_retry_and_compile_feedback(monkeypatch):
    seen = {}

    def fake_run(command, cwd=None):
        seen["command"] = command
        return 0, "", ""

    monkeypatch.setattr(improve_loop, "_run", fake_run)

    result = improve_loop._draft(
        "liero",
        fn="FUN_0001",
        model="local-model",
        endpoint="http://localhost:11434/api/generate",
        retry_existing=True,
        repair_note="line 12: undeclared identifier",
        capture_dir=Path("attempt-capture"),
        temperature=0.25,
    )

    command = seen["command"]
    assert result == 0
    assert "--fn" in command and command[command.index("--fn") + 1] == "FUN_0001"
    assert "--retry-existing" in command
    assert "--repair-note" in command
    assert command[command.index("--repair-note") + 1] == (
        "line 12: undeclared identifier"
    )
    assert command[command.index("--capture-dir") + 1] == "attempt-capture"
    assert command[command.index("--temperature") + 1] == "0.25"


def test_draft_passes_localized_repair_mode(monkeypatch):
    seen = {}

    def fake_run(command, cwd=None):
        seen["command"] = command
        return 0, "", ""

    monkeypatch.setattr(improve_loop, "_run", fake_run)

    result = improve_loop._draft(
        "liero",
        fn="FUN_24dd_3f86",
        retry_existing=True,
        repair_note="ORIGINAL-ORACLE FAILURE:\nequal mismatch",
        function_only=True,
        localized_repair=True,
    )

    assert result == 0
    assert "--localized-repair" in seen["command"]


@pytest.mark.parametrize(
    ("function_oracle", "max_attempts"),
    [(None, 2), ("liero-compare-routine-probe", 3)],
)
def test_localized_repair_requires_routine_oracle_and_two_attempt_cap(
    function_oracle, max_attempts
):
    with pytest.raises(ValueError, match="localized repair requires"):
        improve_loop.improve(
            "liero",
            function_oracle=function_oracle,
            max_attempts_per_function=max_attempts,
            localized_repair=True,
        )


def test_generation_evidence_records_prompt_and_previous_candidate_hashes(
    tmp_path,
):
    root = tmp_path / "targets" / "liero"
    capture_dir = root / "runs" / "trial.generations" / "routine" / "attempt-2"
    capture_root = capture_dir / "FUN_0001"
    capture_root.mkdir(parents=True)
    prompt = "retry prompt with compiler diagnostics and prior source"
    completion = "procedure FUN_0001; begin end;"
    previous_candidate = b"previous candidate"
    (capture_root / "prompt.txt").write_text(prompt)
    (capture_root / "completion.txt").write_text(completion)
    (capture_root / "capture.json").write_text(
        json.dumps(
            {
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "completion_sha256": hashlib.sha256(completion.encode()).hexdigest(),
                "candidate_sha256": hashlib.sha256(
                    b"sanitized candidate"
                ).hexdigest(),
            }
        )
    )

    evidence = improve_loop._generation_evidence(
        root,
        capture_dir,
        "FUN_0001",
        previous_candidate,
        "local-model",
        0.25,
    )

    assert evidence["status"] == "captured"
    assert evidence["prompt_sha256"] == hashlib.sha256(prompt.encode()).hexdigest()
    assert evidence["previous_candidate_sha256"] == hashlib.sha256(
        previous_candidate
    ).hexdigest()
    assert evidence["prompt_chars"] == len(prompt)


def test_binary_verified_count_excludes_format_oracles():
    data = {
        "targets": {
            "liero": {
                "verified": {
                    "dat-parity": ["LIERO.DAT"],
                    "byte-exact": ["src/FUN_0001.inc"],
                }
            }
        }
    }

    assert improve_loop._binary_verified_functions(
        data, "liero", {"FUN_0001"}
    ) == {"FUN_0001"}


def test_candidate_selection_skips_empty_assembly_and_invalid_decomp(tmp_path):
    target = tmp_path / "target"
    asm = target / "asm"
    decomp = target / "decomp"
    asm.mkdir(parents=True)
    decomp.mkdir()
    (asm / "FUN_EMPTY.s").write_text("; FUN_EMPTY entry=0000:0000 size=1\n")
    (decomp / "FUN_EMPTY.c").write_text("halt_baddata();\n")
    (asm / "FUN_BAD_DECOMP.s").write_text("0000:0000  RET\n")
    (decomp / "FUN_BAD_DECOMP.c").write_text("halt_baddata();\n")
    (asm / "FUN_VALID.s").write_text("0000:0000  RET\n")
    (decomp / "FUN_VALID.c").write_text("void FUN_VALID(void) { return; }\n")

    assert improve_loop._select_candidates(
        target,
        {"FUN_EMPTY", "FUN_BAD_DECOMP", "FUN_VALID"},
        attempted=improve_loop.Counter(),
        failed=set(),
        max_attempts_per_function=1,
        limit=3,
    ) == ["FUN_VALID", "FUN_BAD_DECOMP"]
    assert improve_loop.draft.read_decomp_seed(target, "FUN_BAD_DECOMP") is None


def test_candidate_workspace_ignores_numeric_core_dumps(tmp_path):
    target_root = tmp_path / "targets" / "liero"
    target_root.mkdir(parents=True)
    (target_root / "core.1").write_bytes(b"diagnostic dump")

    with improve_loop._candidate_workspace(
        target_root,
        "liero",
        tmp_path / "missing-byod",
    ) as (workspace, candidate_target):
        assert workspace.is_dir()
        assert not (candidate_target / "core.1").exists()


def _make_dependency_target(tmp_path):
    target = tmp_path / "targets" / "liero"
    for directory in ("asm", "src", "config"):
        (target / directory).mkdir(parents=True, exist_ok=True)
    (target / "config" / "toolchain.yaml").write_text(
        "language: pascal\ncompiler: turbo-pascal-7\n"
    )
    (target / "asm" / "FUN_LEAF.s").write_text(
        "; FUN_LEAF entry=0000:0100 size=1\n0000:0100  RET\n"
    )
    (target / "asm" / "FUN_CALLER.s").write_text(
        "; FUN_CALLER entry=0000:0200 size=2\n"
        "0000:0200  CALLF 0x0000:0100\n0000:0205  RET\n"
    )
    (target / "src" / "FUN_LEAF.inc").write_text(
        "procedure FUN_LEAF;\nbegin\n  { TODO: translate from asm }\nend;\n"
    )
    (target / "src" / "FUN_CALLER.inc").write_text(
        "procedure FUN_CALLER;\nbegin\n  { TODO: translate from asm }\nend;\n"
    )
    return target


def test_candidate_selection_resolves_callees_before_callers(tmp_path):
    target = _make_dependency_target(tmp_path)
    function_names = {"FUN_LEAF", "FUN_CALLER"}

    assert improve_loop._direct_call_dependencies(
        target, function_names
    ) == {"FUN_LEAF": set(), "FUN_CALLER": {"FUN_LEAF"}}
    assert improve_loop._select_candidates(
        target,
        function_names,
        attempted=improve_loop.Counter(),
        failed=set(),
        max_attempts_per_function=1,
        limit=2,
    ) == ["FUN_LEAF"]

    improve_loop.recovery.initialize_ledger(target)
    (target / "src" / "FUN_LEAF.inc").write_text(
        "procedure FUN_LEAF;\nbegin\n  Value := 1;\nend;\n"
    )
    (target / "src" / "FUN_CALLER.inc").write_text(
        "procedure FUN_CALLER;\nbegin\n  Value := 2;\nend;\n"
    )
    assert improve_loop._select_candidates(
        target,
        function_names,
        attempted=improve_loop.Counter(),
        failed=set(),
        max_attempts_per_function=1,
        limit=2,
    ) == []
    assert improve_loop._has_dependency_blocked_candidates(
        target, function_names, improve_loop.Counter(), 1
    )
    (target / "src" / "FUN_CALLER.inc").write_text(
        "procedure FUN_CALLER;\nbegin\n  { TODO: translate from asm }\nend;\n"
    )

    improve_loop.recovery.attest_source(
        target,
        "FUN_LEAF",
        "test",
        "Leaf body is independently implemented for dependency scheduling.",
        {
            field: [f"asm/FUN_LEAF.s ({field})"]
            for field in improve_loop.recovery.EVIDENCE_FIELDS
        },
    )

    assert improve_loop._select_candidates(
        target,
        function_names,
        attempted=improve_loop.Counter(),
        failed=set(),
        max_attempts_per_function=1,
        limit=2,
    ) == ["FUN_CALLER"]


def test_dependency_blockers_name_callee_call_site_and_evidence(tmp_path):
    target = _make_dependency_target(tmp_path)

    blockers = improve_loop._dependency_blockers(
        target,
        {"FUN_LEAF", "FUN_CALLER"},
        improve_loop.Counter(),
        max_attempts_per_function=1,
    )

    assert blockers == [
        {
            "function": "FUN_CALLER",
            "callee": "FUN_LEAF",
            "component": ["FUN_CALLER"],
            "call_site": "call:liero:FUN_CALLER:00200",
            "evidence_refs": ["asm:FUN_CALLER:0x200"],
        }
    ]


def test_candidate_selection_groups_mutually_recursive_routines(tmp_path):
    target = tmp_path / "targets" / "liero"
    (target / "asm").mkdir(parents=True)
    (target / "src").mkdir()
    (target / "asm" / "FUN_FIRST.s").write_text(
        "; FUN_FIRST entry=0000:0100 size=2\n"
        "0000:0100  CALLF 0x0000:0200\n0000:0105  RET\n"
    )
    (target / "asm" / "FUN_SECOND.s").write_text(
        "; FUN_SECOND entry=0000:0200 size=2\n"
        "0000:0200  CALLF 0x0000:0100\n0000:0205  RET\n"
    )
    for fn in ("FUN_FIRST", "FUN_SECOND"):
        (target / "src" / f"{fn}.inc").write_text(
            f"procedure {fn};\nbegin\n  {{ TODO: translate from asm }}\nend;\n"
        )

    assert improve_loop._select_candidates(
        target,
        {"FUN_FIRST", "FUN_SECOND"},
        attempted=improve_loop.Counter(),
        failed=set(),
        max_attempts_per_function=1,
        limit=2,
    ) == ["FUN_FIRST", "FUN_SECOND"]


def test_callers_wait_for_every_member_of_a_recursive_group(tmp_path):
    target = tmp_path / "targets" / "liero"
    (target / "asm").mkdir(parents=True)
    (target / "src").mkdir()
    (target / "config").mkdir()
    (target / "config" / "toolchain.yaml").write_text(
        "language: pascal\ncompiler: turbo-pascal-7\n"
    )
    (target / "asm" / "FUN_FIRST.s").write_text(
        "; FUN_FIRST entry=0000:0100 size=2\n"
        "0000:0100  CALLF 0x0000:0200\n0000:0105  RET\n"
    )
    (target / "asm" / "FUN_SECOND.s").write_text(
        "; FUN_SECOND entry=0000:0200 size=2\n"
        "0000:0200  CALLF 0x0000:0100\n0000:0205  RET\n"
    )
    (target / "asm" / "FUN_CALLER.s").write_text(
        "; FUN_CALLER entry=0000:0300 size=2\n"
        "0000:0300  CALLF 0x0000:0100\n0000:0305  RET\n"
    )
    for fn in ("FUN_FIRST", "FUN_SECOND", "FUN_CALLER"):
        (target / "src" / f"{fn}.inc").write_text(
            f"procedure {fn};\nbegin\n  {{ TODO: translate from asm }}\nend;\n"
        )
    function_names = {"FUN_FIRST", "FUN_SECOND", "FUN_CALLER"}
    improve_loop.recovery.initialize_ledger(target)

    def attest(function_name):
        source = target / "src" / f"{function_name}.inc"
        source.write_text(
            f"procedure {function_name};\nbegin\n  Value := 1;\nend;\n"
        )
        improve_loop.recovery.attest_source(
            target,
            function_name,
            "test",
            "Routine is independently reviewed for this scheduling test.",
            {
                field: [f"asm/{function_name}.s ({field})"]
                for field in improve_loop.recovery.EVIDENCE_FIELDS
            },
        )

    attest("FUN_FIRST")
    assert improve_loop._select_candidates(
        target,
        function_names,
        attempted=improve_loop.Counter(),
        failed=set(),
        max_attempts_per_function=1,
        limit=3,
    ) == ["FUN_SECOND"]

    attest("FUN_SECOND")
    assert improve_loop._select_candidates(
        target,
        function_names,
        attempted=improve_loop.Counter(),
        failed=set(),
        max_attempts_per_function=1,
        limit=3,
    ) == ["FUN_CALLER"]


def _make_liero_candidate(tmp_path):
    target = tmp_path / "targets" / "liero"
    (target / "asm").mkdir(parents=True)
    (target / "src").mkdir()
    (target / "config").mkdir()
    (target / "config" / "toolchain.yaml").write_text(
        "language: pascal\ncompiler: turbo-pascal-7\n"
    )
    (target / "asm" / "FUN_0001.s").write_text("0000:0000  RET\n")
    candidate = target / "src" / "FUN_0001.inc"
    candidate.write_text(
        "{ unmatched skeleton }\n"
        "procedure FUN_0001;\nbegin\n  { TODO: translate from asm }\nend;\n"
    )
    return target, candidate


def test_improve_counts_only_compiled_meaningful_candidates(tmp_path, monkeypatch):
    target_root, candidate = _make_liero_candidate(tmp_path)
    improve_loop.recovery.initialize_ledger(target_root)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(improve_loop, "_compile_status", lambda root: (set(), []))
    monkeypatch.setattr(improve_loop, "_verify", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        improve_loop.knowledge,
        "load",
        lambda: {"targets": {"liero": {"verified": {"dat-parity": ["LIERO.DAT"]}}}},
    )
    calls = []

    def fake_draft(target, **kwargs):
        calls.append(kwargs)
        candidate.write_text(
            "procedure FUN_0001;\nbegin\n  Inc(Value);\nend;\n"
        )
        return 0

    monkeypatch.setattr(improve_loop, "_draft", fake_draft)

    summary = improve_loop.improve(
        "liero", max_iterations=3, saturation_window=2
    )

    assert calls[0]["fn"] == "FUN_0001"
    assert calls[0]["retry_existing"] is True
    assert summary["functions_meaningful"] == 1
    assert summary["functions_compilable"] == 1
    assert summary["whole_target_build_passed"] is True
    assert summary["functions_binary_verified"] == 0
    assert summary["functions_verified"] == 0
    assert summary["functions_source_recovered"] == 0
    assert summary["evidence_accounted_percent"] == 0
    assert summary["source_recovery_ledger"] == "present"
    assert summary["dependency_blockers"] == []
    assert summary["unresolved_call_targets"] == []
    assert summary["saturated"] is False
    assert target_root.is_dir()
    run_state = json.loads(
        (target_root / "runs" / f"{summary['run_id']}.json").read_text()
    )
    assert run_state["routines"]["FUN_0001"]["attempts"][0]["status"] == (
        "candidate-compiled"
    )


def test_failed_candidate_is_rolled_back_and_retried_with_diagnostics(
    tmp_path, monkeypatch
):
    _, candidate = _make_liero_candidate(tmp_path)
    original = candidate.read_text()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        improve_loop,
        "_compile_status",
        lambda root: (
            ({"FUN_0001"}, ["FUN_0001.inc(3,1) Error: syntax error"])
            if "INVALID" in candidate.read_text()
            else (set(), [])
        ),
    )
    monkeypatch.setattr(improve_loop, "_verify", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        improve_loop.knowledge,
        "load",
        lambda: {"targets": {"liero": {"verified": {}}}},
    )
    calls = []

    def fake_draft(target, **kwargs):
        calls.append(kwargs)
        candidate.write_text(
            "procedure FUN_0001;\nbegin\n  INVALID;\nend;\n"
        )
        return 0

    monkeypatch.setattr(improve_loop, "_draft", fake_draft)

    summary = improve_loop.improve(
        "liero",
        max_iterations=2,
        saturation_window=2,
        max_attempts_per_function=3,
    )

    assert candidate.read_text() == original
    assert calls[0]["repair_note"] == ""
    assert "syntax error" in calls[1]["repair_note"]
    assert summary["functions_meaningful"] == 0
    assert summary["functions_compilable"] == 0
    assert summary["saturated"] is True
    assert summary["candidate_failures"] == 2


def test_improve_resume_continues_failed_routine_attempt_history(tmp_path, monkeypatch):
    target_root, candidate = _make_liero_candidate(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        improve_loop,
        "_compile_status",
        lambda root: (
            ({"FUN_0001"}, ["FUN_0001.inc(3,1) Error: syntax error"])
            if "INVALID" in candidate.read_text()
            else (set(), [])
        ),
    )
    monkeypatch.setattr(improve_loop, "_verify", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        improve_loop.knowledge,
        "load",
        lambda: {"targets": {"liero": {"verified": {}}}},
    )
    draft_calls = 0

    def fake_draft(target, **kwargs):
        nonlocal draft_calls
        draft_calls += 1
        body = "INVALID;" if draft_calls == 1 else "Inc(Value);"
        candidate.write_text(f"procedure FUN_0001;\nbegin\n  {body}\nend;\n")
        return 0

    monkeypatch.setattr(improve_loop, "_draft", fake_draft)

    first = improve_loop.improve(
        "liero", max_iterations=1, max_attempts_per_function=3
    )
    resumed = improve_loop.improve(
        "liero",
        max_iterations=1,
        max_attempts_per_function=3,
        resume_run_id=first["run_id"],
    )

    persisted_run = json.loads(
        (target_root / "runs" / f"{first['run_id']}.json").read_text()
    )
    attempts = persisted_run["routines"]["FUN_0001"]["attempts"]
    assert [attempt["status"] for attempt in attempts] == [
        "candidate-rejected",
        "candidate-compiled",
    ]
    assert resumed["run_id"] == first["run_id"]
    assert resumed["functions_meaningful"] == 1
    assert resumed["candidate_failures"] == 1


def test_improve_resume_rejects_changed_assembly_inputs(tmp_path, monkeypatch):
    target_root, _ = _make_liero_candidate(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(improve_loop, "_compile_status", lambda root: (set(), []))
    monkeypatch.setattr(improve_loop, "_verify", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        improve_loop.knowledge,
        "load",
        lambda: {"targets": {"liero": {"verified": {}}}},
    )
    monkeypatch.setattr(improve_loop, "_draft", lambda *args, **kwargs: 0)
    first = improve_loop.improve("liero", max_iterations=1)
    (target_root / "asm" / "FUN_0001.s").write_text("INT 21h\n")

    with pytest.raises(ValueError, match="input files changed"):
        improve_loop.improve(
            "liero", max_iterations=1, resume_run_id=first["run_id"]
        )


def test_improve_resume_restores_sources_after_interrupted_generation(
    tmp_path, monkeypatch
):
    target_root, candidate = _make_liero_candidate(tmp_path)
    original = candidate.read_bytes()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(improve_loop, "_compile_status", lambda root: (set(), []))
    monkeypatch.setattr(improve_loop, "_verify", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        improve_loop.knowledge,
        "load",
        lambda: {"targets": {"liero": {"verified": {}}}},
    )
    draft_calls = 0

    def interrupt_first_draft(target, **kwargs):
        nonlocal draft_calls
        draft_calls += 1
        if draft_calls == 1:
            candidate.write_text("partial candidate\n")
            raise KeyboardInterrupt
        candidate.write_text(
            "procedure FUN_0001;\nbegin\n  Inc(Value);\nend;\n"
        )
        return 0

    monkeypatch.setattr(improve_loop, "_draft", interrupt_first_draft)

    with pytest.raises(KeyboardInterrupt):
        improve_loop.improve("liero", max_iterations=1)

    interrupted_run = next((target_root / "runs").glob("*.json"))
    run_id = interrupted_run.stem
    assert candidate.read_text() == "partial candidate\n"

    resumed = improve_loop.improve(
        "liero", max_iterations=1, resume_run_id=run_id
    )

    persisted_run = json.loads(interrupted_run.read_text())
    attempts = persisted_run["routines"]["FUN_0001"]["attempts"]
    assert [attempt["status"] for attempt in attempts] == [
        "interrupted-restored",
        "candidate-compiled",
    ]
    assert attempts[0]["source_sha256"] is None
    assert candidate.read_bytes() != original
    assert resumed["run_id"] == run_id
    assert resumed["functions_meaningful"] == 1


def _make_checked_routine_target(tmp_path):
    target = tmp_path / "targets" / "liero"
    for directory in ("asm", "src", "config"):
        (target / directory).mkdir(parents=True, exist_ok=True)
    (target / "config" / "toolchain.yaml").write_text(
        "language: pascal\ncompiler: turbo-pascal-7\ncompiler_confidence: high\n"
    )
    (target / "config" / "routine_contracts.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "functions": {
                    "FUN_24dd_3f86": {
                        "declaration": (
                            "procedure FUN_24dd_3f86("
                            "param_1, param_2: Longint);"
                        ),
                        "oracle": "liero-compare-routine-probe",
                        "arguments": [
                            {
                                "name": "param_1",
                                "role": "destination",
                                "representation": "packed far pointer",
                            },
                            {
                                "name": "param_2",
                                "role": "source",
                                "representation": "packed far pointer",
                            },
                        ],
                        "memory_model": "RealModeMemory",
                        "observed_outputs": ["ZF", "CF"],
                        "prompt": "Use checked far-pointer semantics.",
                    }
                },
            }
        )
    )
    (target / "asm" / "FUN_24dd_3f86.s").write_text(
        "; FUN_24dd_3f86 entry=24DD:3F86 size=1\n24DD:3F86  RET\n"
    )
    candidate = target / "src" / "FUN_24dd_3f86.inc"
    candidate.write_text(
        "procedure FUN_24dd_3f86(param_1, param_2: Longint);\n"
        "begin\n  { TODO: translate from asm }\nend;\n"
    )
    sibling = target / "src" / "LieroRuntime.pas"
    sibling.write_text("unit LieroRuntime; { shared declarations }\n")
    (target / "src" / "_forward.inc").write_text(
        "procedure SharedRoutine; forward;\n"
    )
    return target, candidate, sibling


def _write_fake_generation_capture(kwargs, function_name, generated_candidate):
    workspace_candidate = (
        kwargs["cwd"]
        / "targets"
        / "liero"
        / "src"
        / f"{function_name}.inc"
    )
    previous_candidate = (
        workspace_candidate.read_text() if workspace_candidate.is_file() else ""
    )
    prompt = (
        f"repair_note:\n{kwargs.get('repair_note', '')}\n"
        f"previous_candidate:\n{previous_candidate}"
    )
    completion = generated_candidate
    capture_root = kwargs["capture_dir"] / function_name
    capture_root.mkdir(parents=True, exist_ok=True)
    (capture_root / "prompt.txt").write_text(prompt)
    (capture_root / "completion.txt").write_text(completion)
    (capture_root / "candidate.pas").write_text(generated_candidate)
    (capture_root / "capture.json").write_text(
        json.dumps(
            {
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "completion_sha256": hashlib.sha256(completion.encode()).hexdigest(),
                "candidate_sha256": hashlib.sha256(
                    generated_candidate.encode()
                ).hexdigest(),
            }
        )
    )


def test_function_oracle_mismatch_is_retried_and_scoped_pass_is_not_promotion(
    tmp_path, monkeypatch
):
    target_root, candidate, sibling = _make_checked_routine_target(tmp_path)
    improve_loop.recovery.initialize_ledger(target_root)
    original_candidate = candidate.read_bytes()
    original_sibling = sibling.read_bytes()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(improve_loop, "_compile_status", lambda root: (set(), []))
    monkeypatch.setattr(
        improve_loop,
        "_verify",
        lambda *args, **kwargs: pytest.fail("the unrelated final oracle must be skipped"),
    )
    monkeypatch.setattr(
        improve_loop.knowledge,
        "load",
        lambda: {"targets": {"liero": {"verified": {}}}},
    )
    drafted = []
    generated_candidates = [
        (
            "procedure FUN_24dd_3f86(param_1, param_2: Longint);\n"
            "begin\n  CompareStrings;\nend;\n"
        ),
        (
            "procedure FUN_24dd_3f86(param_1, param_2: Longint);\n"
            "begin\n  CompareStringsWithFlags;\nend;\n"
        ),
    ]

    def fake_draft(target, **kwargs):
        drafted.append(kwargs)
        candidate_in_workspace = (
            kwargs["cwd"] / "targets" / "liero" / "src" / candidate.name
        )
        generated_candidate = generated_candidates[len(drafted) - 1]
        _write_fake_generation_capture(
            kwargs, "FUN_24dd_3f86", generated_candidate
        )
        candidate_in_workspace.write_text(generated_candidate)
        return 0

    reports = [
        {
            "status": "failed",
            "case_count": 1,
            "cases": [
                {
                    "name": "equal",
                    "status": "failed",
                    "expected_flags": 0x40,
                    "candidate_flags": 0,
                    "stack_balanced": True,
                    "candidate_memory_changed": False,
                }
            ],
        },
        {
            "status": "passed",
            "case_count": 1,
            "cases": [
                {
                    "name": "equal",
                    "status": "passed",
                    "expected_flags": 0x40,
                    "candidate_flags": 0x40,
                    "stack_balanced": True,
                    "candidate_memory_changed": False,
                }
            ],
        },
    ]

    def fake_oracle(name, workspace, output):
        assert name == "liero-compare-routine-probe"
        assert output.is_absolute()
        report = reports.pop(0)
        output.mkdir(parents=True)
        (output / "result.json").write_text(json.dumps(report))
        return report

    monkeypatch.setattr(improve_loop, "_draft", fake_draft)
    monkeypatch.setattr(improve_loop, "_run_function_oracle", fake_oracle)

    summary = improve_loop.improve(
        "liero",
        oracle=None,
        function_oracle="liero-compare-routine-probe",
        only_functions={"FUN_24dd_3f86"},
        max_iterations=2,
        max_attempts_per_function=2,
        localized_repair=True,
    )

    assert len(drafted) == 2
    assert all(call["function_only"] for call in drafted)
    assert [call["localized_repair"] for call in drafted] == [False, True]
    assert "ORIGINAL-ORACLE FAILURE" in drafted[1]["repair_note"]
    assert "expected flags 0x0040, got 0x0000" in drafted[1]["repair_note"]
    assert candidate.read_bytes() != original_candidate
    assert sibling.read_bytes() == original_sibling
    assert summary["functions_scoped_oracle_passed"] == 1
    assert summary["functions_verified"] == 0
    assert summary["functions_source_recovered"] == 0
    assert summary["whole_target_build_passed"] is True
    run_state = json.loads(
        (target_root / "runs" / f"{summary['run_id']}.json").read_text()
    )
    attempts = run_state["routines"]["FUN_24dd_3f86"]["attempts"]
    assert [attempt["status"] for attempt in attempts] == [
        "candidate-oracle-rejected",
        "candidate-scoped-pass",
    ]
    assert attempts[0]["evidence"]["function_oracle"]["status"] == "failed"
    assert attempts[1]["evidence"]["function_oracle"]["status"] == "passed"
    assert attempts[1]["evidence"]["function_oracle"]["report_sha256"]
    assert attempts[1]["evidence"]["generation"]["status"] == "captured"
    prompt_capture = (
        target_root
        / attempts[1]["evidence"]["generation"]["capture_path"]
        / "prompt.txt"
    ).read_text()
    assert "ORIGINAL-ORACLE FAILURE" in prompt_capture
    assert "CompareStrings" in prompt_capture


def test_repeated_candidate_hash_stops_bounded_repair(
    tmp_path, monkeypatch
):
    target_root, candidate, sibling = _make_checked_routine_target(tmp_path)
    improve_loop.recovery.initialize_ledger(target_root)
    original_candidate = candidate.read_bytes()
    original_sibling = sibling.read_bytes()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(improve_loop, "_compile_status", lambda root: (set(), []))
    monkeypatch.setattr(
        improve_loop.knowledge,
        "load",
        lambda: {"targets": {"liero": {"verified": {}}}},
    )
    generated_candidate = (
        "procedure FUN_24dd_3f86(param_1, param_2: Longint);\n"
        "begin\n  CompareStrings;\nend;\n"
    )

    def fake_draft(target, **kwargs):
        candidate_in_workspace = (
            kwargs["cwd"] / "targets" / "liero" / "src" / candidate.name
        )
        _write_fake_generation_capture(
            kwargs, "FUN_24dd_3f86", generated_candidate
        )
        candidate_in_workspace.write_text(generated_candidate)
        return 0

    oracle_calls = []

    def fake_oracle(name, workspace, output):
        oracle_calls.append(name)
        report = {
            "status": "failed",
            "case_count": 1,
            "cases": [
                {
                    "name": "equal",
                    "status": "failed",
                    "expected_flags": 0x40,
                    "candidate_flags": 0,
                    "stack_balanced": True,
                    "candidate_memory_changed": False,
                }
            ],
        }
        output.mkdir(parents=True)
        (output / "result.json").write_text(json.dumps(report))
        return report

    monkeypatch.setattr(improve_loop, "_draft", fake_draft)
    monkeypatch.setattr(improve_loop, "_run_function_oracle", fake_oracle)

    summary = improve_loop.improve(
        "liero",
        oracle=None,
        function_oracle="liero-compare-routine-probe",
        only_functions={"FUN_24dd_3f86"},
        max_iterations=5,
        max_attempts_per_function=5,
    )

    assert summary["stop_reason"] == "duplicate-candidate"
    assert len(oracle_calls) == 1
    assert candidate.read_bytes() == original_candidate
    assert sibling.read_bytes() == original_sibling
    attempts = json.loads(
        (target_root / "runs" / f"{summary['run_id']}.json").read_text()
    )["routines"]["FUN_24dd_3f86"]["attempts"]
    assert [attempt["status"] for attempt in attempts] == [
        "candidate-oracle-rejected",
        "candidate-duplicate",
    ]
    assert attempts[1]["evidence"]["candidate_sha256"] == hashlib.sha256(
        generated_candidate.encode()
    ).hexdigest()
    assert attempts[1]["evidence"]["duplicate_of_attempt"] == 1
    resumed_summary = improve_loop.improve(
        "liero",
        oracle=None,
        function_oracle="liero-compare-routine-probe",
        only_functions={"FUN_24dd_3f86"},
        max_iterations=5,
        max_attempts_per_function=5,
        resume_run_id=summary["run_id"],
    )
    assert resumed_summary == summary
    assert len(oracle_calls) == 1


@pytest.mark.parametrize("failure", ["skip", "error", "missing-report"])
def test_function_oracle_skip_error_or_missing_report_blocks_candidate(
    tmp_path, monkeypatch, failure
):
    target_root, candidate, _ = _make_checked_routine_target(tmp_path)
    improve_loop.recovery.initialize_ledger(target_root)
    original_candidate = candidate.read_bytes()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(improve_loop, "_compile_status", lambda root: (set(), []))
    monkeypatch.setattr(
        improve_loop.knowledge,
        "load",
        lambda: {"targets": {"liero": {"verified": {}}}},
    )

    def fake_draft(target, **kwargs):
        candidate_in_workspace = (
            kwargs["cwd"] / "targets" / "liero" / "src" / candidate.name
        )
        generated_candidate = (
            "procedure FUN_24dd_3f86(param_1, param_2: Longint);\n"
            "begin\n  CompareStrings;\nend;\n"
        )
        _write_fake_generation_capture(
            kwargs, "FUN_24dd_3f86", generated_candidate
        )
        candidate_in_workspace.write_text(generated_candidate)
        return 0

    def fake_oracle(name, workspace, output):
        if failure == "error":
            raise RuntimeError("comparator unavailable")
        if failure == "missing-report":
            return {"status": "passed", "case_count": 1, "cases": []}
        output.mkdir(parents=True)
        (output / "result.json").write_text("{}")
        return {"status": "skipped", "case_count": 0, "cases": []}

    monkeypatch.setattr(improve_loop, "_draft", fake_draft)
    monkeypatch.setattr(improve_loop, "_run_function_oracle", fake_oracle)

    summary = improve_loop.improve(
        "liero",
        oracle=None,
        function_oracle="liero-compare-routine-probe",
        only_functions={"FUN_24dd_3f86"},
        max_iterations=1,
    )

    assert summary["blocked"] is True
    assert summary["functions_scoped_oracle_passed"] == 0
    assert summary["functions_verified"] == 0
    assert candidate.read_bytes() == original_candidate
    attempts = json.loads(
        (target_root / "runs" / f"{summary['run_id']}.json").read_text()
    )["routines"]["FUN_24dd_3f86"]["attempts"]
    assert attempts[0]["status"] == "candidate-oracle-blocked"
    assert attempts[0]["evidence"]["function_oracle"]["status"] in {
        "error",
        "skipped",
        "passed",
    }
