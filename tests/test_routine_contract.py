import json
from pathlib import Path

import pytest

from engine import draft, routine_contract

ROOT = Path(__file__).resolve().parents[1]
ROUTINE = "FUN_24dd_3f86"


def test_checked_liero_contract_overrides_decompiler_pointer_guess():
    target_root = ROOT / "targets" / "liero"
    declaration = routine_contract.load_contract(target_root, ROUTINE)["declaration"]

    assert declaration == (
        "procedure FUN_24dd_3f86(param_1, param_2: Longint);"
    )
    assert draft._decl_for(target_root, ROUTINE) == declaration
    candidate = draft._force_decl(
        "procedure FUN_24dd_3f86(param_1, param_2: Pointer);\n"
        "begin\n  { candidate body }\nend;",
        declaration,
    )
    assert candidate.splitlines()[0] == declaration


def test_checked_liero_contract_is_injected_into_prompt():
    target_root = ROOT / "targets" / "liero"
    declaration = draft._decl_for(target_root, ROUTINE)
    prompt = draft._build_pascal_prompt(
        target_root,
        "liero",
        ROUTINE,
        "0000:0000  RET",
        "void FUN_24dd_3f86(byte *param_1, byte *param_2);",
        "Ghidra",
        declaration,
        set(),
    )

    assert "packed far pointer" in prompt
    assert "do not cast either argument to a host Pointer" in prompt
    assert declaration in prompt
    assert "RealModeMemory[address]" in prompt
    assert "Do NOT declare or use `Pointer`, `^Byte`, `PChar`, `Ptr`" in prompt
    assert "Raw/absolute memory: declare typed pointer variables" not in prompt
    assert "For pointers use local declarations" not in prompt
    assert "RegisterZeroFlag" in prompt
    assert "RegisterCarryFlag" in prompt
    assert "2000:8D70" in prompt
    assert "JZ 8D7A" in prompt
    assert "JNZ 8D7C" in prompt
    assert "source byte < destination byte" in prompt
    assert "sourceLen < destLen" in prompt
    for outcome in (
        "both-empty=0x0040",
        "equal=0x0040",
        "dest-less=0x0000",
        "dest-greater=0x0001",
        "source-shorter=0x0001",
        "dest-shorter=0x0000",
        "embedded-zero=0x0000",
        "equal-maximum-length=0x0040",
        "late-mismatch=0x0000",
    ):
        assert outcome in prompt


def test_checked_liero_retry_prompt_contains_diagnostics_and_previous_candidate():
    target_root = ROOT / "targets" / "liero"
    declaration = draft._decl_for(target_root, ROUTINE)
    previous_candidate = (
        "procedure FUN_24dd_3f86(param_1, param_2: Longint);\n"
        "begin\n  destPtr := ^Byte(param_1);\nend;"
    )
    prompt = draft._build_pascal_prompt(
        target_root,
        "liero",
        ROUTINE,
        "0000:0000  RET",
        "",
        "Ghidra",
        declaration,
        set(),
        repair_note="Incompatible types: got Char expected ^Byte",
        previous_attempt=previous_candidate,
    )

    assert "Incompatible types: got Char expected ^Byte" in prompt
    assert previous_candidate in prompt
    assert "Do NOT declare or use `Pointer`, `^Byte`, `PChar`, `Ptr`" in prompt
    assert "RealModeMemory[address]" in prompt


def test_localized_repair_prompt_requests_only_the_checked_region():
    target_root = ROOT / "targets" / "liero"
    declaration = draft._decl_for(target_root, ROUTINE)
    prompt = draft._build_pascal_prompt(
        target_root,
        "liero",
        ROUTINE,
        "24DD:3F9A  CMP CL,AH",
        "",
        "Ghidra",
        declaration,
        set(),
        repair_note=(
            "ORIGINAL-ORACLE FAILURE:\nequal: expected flags 0x0040, got 0x0000"
        ),
        previous_attempt="procedure FUN_24dd_3f86;\nbegin\n  Compare;\nend;",
        localized_repair_region="if srcLen <= destLen then\n  ...\nend;",
    )

    assert "Return only replacement Pascal statements for the selected region" in prompt
    assert "Do not output a procedure/function header" in prompt
    assert "equal: expected flags 0x0040, got 0x0000" in prompt
    assert "Exact selected region:\nif srcLen <= destLen then" in prompt
    assert "Previous complete candidate:" in prompt


def test_localized_region_helpers_preserve_code_outside_unique_anchors():
    source = (
        "procedure FUN_24dd_3f86;\n"
        "begin\n"
        "  DecodePointers;\n"
        "  if srcLen <= destLen then\n"
        "    CompareBytes;\n"
        "  RegisterCarryFlag := (srcLen < destLen);\n"
        "  RestoreState;\n"
        "end;\n"
    )
    region = {
        "start": "if srcLen <= destLen then",
        "end": "RegisterCarryFlag := (srcLen < destLen);",
    }

    prefix, selected, suffix = draft._split_localized_region(source, region)
    replacement = "  CompareAndSetFlags;"
    patched = draft._replace_localized_region(source, region, replacement)

    assert selected == (
        "  if srcLen <= destLen then\n"
        "    CompareBytes;\n"
        "  RegisterCarryFlag := (srcLen < destLen);\n"
    )
    assert patched == prefix + replacement + "\n" + suffix
    assert patched.startswith(prefix)
    assert patched.endswith(suffix)
    assert "DecodePointers;" in patched
    assert "RestoreState;" in patched


@pytest.mark.parametrize(
    ("source", "expected_error"),
    [
        (
            "if srcLen <= destLen then\n  A;\nif srcLen <= destLen then\n  B;\n"
            + "RegisterCarryFlag := (srcLen < destLen);\n",
            "start anchor must occur exactly once",
        ),
        (
            "if srcLen <= destLen then\n  A;\nRegisterCarryFlag := (srcLen < destLen);\n"
            + "RegisterCarryFlag := (srcLen < destLen);\n",
            "end anchor must occur exactly once",
        ),
    ],
)
def test_localized_region_helpers_reject_ambiguous_anchors(source, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        draft._split_localized_region(
            source,
            {
                "start": "if srcLen <= destLen then",
                "end": "RegisterCarryFlag := (srcLen < destLen);",
            },
        )


def test_localized_region_sanitizer_rejects_full_routine_output():
    clean, reason = draft._sanitize_pascal_region_with_reason(
        "procedure FUN_24dd_3f86;\nbegin\n  Compare;\nend;"
    )

    assert clean == ""
    assert reason == "routine-declaration-in-region"


def _make_localized_draft_target(tmp_path):
    target_root = tmp_path / "targets" / "liero"
    for directory in ("asm", "src", "config"):
        (target_root / directory).mkdir(parents=True, exist_ok=True)
    (target_root / "asm" / f"{ROUTINE}.s").write_text(
        "24DD:3F9A  CMP CL,AH\n"
    )
    (target_root / "config" / "routine_contracts.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "functions": {
                    ROUTINE: {
                        "declaration": (
                            "procedure FUN_24dd_3f86(param_1, param_2: Longint);"
                        ),
                        "oracle": "liero-compare-routine-probe",
                        "prompt": "Use the checked comparison semantics.",
                        "localized_repair_region": {
                            "start": "if srcLen <= destLen then",
                            "end": (
                                "RegisterCarryFlag := (srcLen < destLen);"
                            ),
                        },
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    candidate = target_root / "src" / f"{ROUTINE}.inc"
    candidate.write_text(
        "procedure FUN_24dd_3f86(param_1, param_2: Longint);\n"
        "begin\n"
        "  DecodePointers;\n"
        "  if srcLen <= destLen then\n"
        "    CompareBytes;\n"
        "  RegisterCarryFlag := (srcLen < destLen);\n"
        "  RestoreState;\n"
        "end;\n"
    )
    return target_root, candidate


def _stub_localized_draft_dependencies(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(draft, "detect_language", lambda _: ("pascal", "high", "tp7"))
    monkeypatch.setattr(draft.knowledge, "confidence_ok", lambda *args: True)
    monkeypatch.setattr(draft.model_training, "active_adapter_for", lambda _: None)
    monkeypatch.setattr(draft, "fewshot_context", lambda *args, **kwargs: "")
    monkeypatch.setattr(draft, "_function_calling_convention", lambda *args: None)
    monkeypatch.setattr(
        draft,
        "_write_program",
        lambda *args, **kwargs: pytest.fail(
            "localized function-only repair rewrote the shared program"
        ),
    )


def test_localized_draft_applies_patch_without_changing_surrounding_source(
    tmp_path, monkeypatch
):
    _, candidate = _make_localized_draft_target(tmp_path)
    original = candidate.read_text()
    region = {
        "start": "if srcLen <= destLen then",
        "end": "RegisterCarryFlag := (srcLen < destLen);",
    }
    original_prefix, _, original_suffix = draft._split_localized_region(
        original, region
    )
    _stub_localized_draft_dependencies(monkeypatch, tmp_path)
    monkeypatch.setattr(
        draft,
        "run_llm",
        lambda prompt, *args, **kwargs: (
            "RegisterZeroFlag := (srcLen = destLen);\n"
            "RegisterCarryFlag := (srcLen < destLen);"
        ),
    )
    capture_dir = tmp_path / "captures"

    result = draft.draft(
        "liero",
        fn=ROUTINE,
        use_llm=True,
        retry_existing=True,
        repair_note=(
            "ORIGINAL-ORACLE FAILURE:\nequal: expected flags 0x0040, got 0x0000"
        ),
        run_compile_gate=False,
        function_only=True,
        localized_repair=True,
        capture_dir=capture_dir,
    )

    patched = candidate.read_text()
    assert result == 0
    assert patched.startswith(original_prefix)
    assert patched.endswith(original_suffix)
    metadata = json.loads(
        (capture_dir / ROUTINE / "capture.json").read_text()
    )
    assert metadata["repair_mode"] == "localized-region"
    assert metadata["sanitizer_accepted"] is True


def test_localized_draft_rejects_full_routine_and_preserves_candidate(
    tmp_path, monkeypatch
):
    _, candidate = _make_localized_draft_target(tmp_path)
    original = candidate.read_bytes()
    _stub_localized_draft_dependencies(monkeypatch, tmp_path)
    monkeypatch.setattr(
        draft,
        "run_llm",
        lambda *args, **kwargs: (
            "procedure FUN_24dd_3f86;\nbegin\n  Compare;\nend;"
        ),
    )
    capture_dir = tmp_path / "captures"

    result = draft.draft(
        "liero",
        fn=ROUTINE,
        use_llm=True,
        retry_existing=True,
        repair_note="ORIGINAL-ORACLE FAILURE:\nequal mismatch",
        run_compile_gate=False,
        function_only=True,
        localized_repair=True,
        capture_dir=capture_dir,
    )

    assert result == 2
    assert candidate.read_bytes() == original
    metadata = json.loads(
        (capture_dir / ROUTINE / "capture.json").read_text()
    )
    assert metadata["sanitizer_accepted"] is False
    assert metadata["rejection_reason"] == "routine-declaration-in-region"


def test_contract_rejects_declaration_for_another_function(tmp_path):
    contracts = tmp_path / "contracts.json"
    contracts.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "functions": {
                    ROUTINE: {
                        "declaration": "procedure FUN_OTHER;",
                        "oracle": "liero-compare-routine-probe",
                        "prompt": "checked contract",
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    try:
        routine_contract.load_contracts(contracts)
    except routine_contract.RoutineContractError as exc:
        assert ROUTINE in str(exc)
    else:
        raise AssertionError("a mismatched declaration must be rejected")


def test_function_only_draft_preserves_shared_target_files(tmp_path, monkeypatch):
    target_root = tmp_path / "targets" / "liero"
    for directory in ("asm", "src", "config"):
        (target_root / directory).mkdir(parents=True, exist_ok=True)
    (target_root / "asm" / "FUN_0001.s").write_text("0000:0000  RET\n")
    (target_root / "asm" / "FUN_0002.s").write_text("0000:0010  RET\n")
    candidate = target_root / "src" / "FUN_0001.inc"
    candidate.write_text(
        "procedure FUN_0001;\nbegin\n  { TODO: translate from asm }\nend;\n"
    )
    untouched = {
        target_root / "src" / "FUN_0002.inc": "sibling include\n",
        target_root / "src" / "_forward.inc": "forward declarations\n",
        target_root / "src" / "liero.pas": "program source\n",
        target_root / "src" / "obsolete.inc": "stale include\n",
    }
    for path, contents in untouched.items():
        path.write_text(contents)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(draft, "detect_language", lambda _: ("pascal", "high", "tp7"))
    monkeypatch.setattr(draft.knowledge, "confidence_ok", lambda *args: True)
    monkeypatch.setattr(draft.model_training, "active_adapter_for", lambda _: None)
    monkeypatch.setattr(draft, "fewshot_context", lambda *args, **kwargs: "")
    monkeypatch.setattr(draft, "_function_calling_convention", lambda *args: None)
    monkeypatch.setattr(
        draft,
        "run_llm",
        lambda *args, **kwargs: (
            "procedure FUN_0001;\nbegin\n  Value := 1;\nend;"
        ),
    )
    monkeypatch.setattr(
        draft,
        "_write_program",
        lambda *args, **kwargs: pytest.fail("function-only draft rewrote shared program"),
    )

    result = draft.draft(
        "liero",
        fn="FUN_0001",
        use_llm=True,
        retry_existing=True,
        run_compile_gate=False,
        function_only=True,
    )

    assert result == 0
    assert "Value := 1;" in candidate.read_text()
    assert {path: path.read_text() for path in untouched} == untouched


def test_contract_rejects_malformed_argument_contract(tmp_path):
    contracts = tmp_path / "contracts.json"
    contracts.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "functions": {
                    ROUTINE: {
                        "declaration": (
                            "procedure FUN_24dd_3f86(param_1, param_2: Longint);"
                        ),
                        "oracle": "liero-compare-routine-probe",
                        "prompt": "checked contract",
                        "arguments": [{"name": "param_1"}],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(routine_contract.RoutineContractError, match="argument"):
        routine_contract.load_contracts(contracts)


def test_contract_rejects_malformed_localized_repair_region(tmp_path):
    contracts = tmp_path / "contracts.json"
    contracts.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "functions": {
                    ROUTINE: {
                        "declaration": (
                            "procedure FUN_24dd_3f86(param_1, param_2: Longint);"
                        ),
                        "oracle": "liero-compare-routine-probe",
                        "prompt": "checked contract",
                        "localized_repair_region": {
                            "start": "if sourceLen <= destLen then",
                            "end": "",
                        },
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        routine_contract.RoutineContractError, match="localized repair region"
    ):
        routine_contract.load_contracts(contracts)
