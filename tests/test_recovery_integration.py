"""Tests for the integrated Matrix/recovery/verification path."""

from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "engine"))

from engine import matrix, recovery_loop, rl_engine, rtl_template, verify


def test_matrix_frontier_prefers_callee_first(tmp_path, monkeypatch):
    target = tmp_path / "targets" / "sample"
    (target / "asm").mkdir(parents=True)
    (target / "functions.json").write_text(json.dumps({
        "functions": [
            {"name": "LEAF", "entry": "1000:0010", "size": 4, "num_instructions": 1},
            {"name": "TOP", "entry": "1000:0020", "size": 4, "num_instructions": 1},
        ],
        "num_functions": 2,
    }))
    (target / "asm" / "LEAF.s").write_text("1000:0010  RET\n")
    (target / "asm" / "TOP.s").write_text(
        "1000:0020  CALLF 0x1000:0010\n1000:0023  RET\n")
    monkeypatch.setattr(matrix, "BASE", tmp_path)

    rows = matrix.build("sample", {})
    by_name = {row["name"]: row for row in rows}
    assert by_name["TOP"]["callees"] == ["LEAF"]
    assert by_name["TOP"]["unverified_callees"] == ["LEAF"]
    assert matrix.select_frontier("sample", {}, limit=1)[0]["name"] == "LEAF"


def test_q_update_is_real():
    data = {"current_target": "sample"}
    state = "s0"
    action = "model|0.4|3"
    rl_engine.record_recovery_outcome(
        data, "pascal|turbo-pascal-7", "FUN_1", "verified", 1.0, True,
        action, state=state, next_state="s1",
    )
    assert data["q_table"]["pascal|turbo-pascal-7"][state][action] > 0
    assert data["experience_buffer"]["pascal|turbo-pascal-7"][0]["action"] == action
    assert data["total_attempts"] == 1
    assert data["total_verified"] == 1


def test_dat_selftest_is_not_source_promotion(tmp_path, monkeypatch):
    class FakeOracle:
        @staticmethod
        def selftest():
            return True, "fixture ok"

    monkeypatch.setattr(verify, "_load_dat_oracle", lambda target: FakeOracle)
    result = verify.verify_status("liero", None, None, "dat-parity")
    assert result["status"] == "scoped"
    assert result["checked"] == 1
    assert "no source promotion" in result["reason"]


def test_dat_round_trip_does_not_write_knowledge(tmp_path, monkeypatch):
    class FakeOracle:
        @staticmethod
        def selftest():
            return True, "fixture ok"

        @staticmethod
        def round_trip(data):
            assert data == b"dat"
            return True, 0.5, "ok"

    monkeypatch.setattr(verify, "_load_dat_oracle", lambda target: FakeOracle)
    monkeypatch.chdir(tmp_path)
    byod = tmp_path / "byod"
    byod.mkdir()
    (byod / "LIERO.DAT").write_bytes(b"dat")

    result = verify.verify_status("liero", byod, None, "dat-parity")

    assert result["status"] == "scoped"
    assert not (tmp_path / "knowledge" / "knowledge.json").exists()


def test_authoritative_status_reflects_only_oracle_backed_promotion():
    report = json.loads((REPO / "recovery_results.json").read_text())
    assert report["schema_version"] == 2
    assert set(report["verified_functions"]) == {
        "FUN_24dd_3d68",
        "FUN_24dd_4141",
        "FUN_24dd_455e",
        "FUN_249c_0013",
        "FUN_24dd_40d6",
        "FUN_24dd_48e1",
        "FUN_24dd_04dc",
    }
    assert report["counts"]["oracle_verified"] == 7
    assert report["total"] == 295
    assert "no source promotion" in report["verification"]["reason"]


def test_generic_recovery_uses_one_gate_for_promotion_rl_and_dl(tmp_path, monkeypatch):
    from engine import draft, frozen_source_eval, oracle_gate, target_packet

    target = tmp_path / "targets" / "sample"
    (target / "asm").mkdir(parents=True)
    (target / "config").mkdir()
    (tmp_path / "knowledge").mkdir()
    (target / "functions.json").write_text(json.dumps({
        "functions": [
            {"name": "LEAF", "entry": "1000:0010", "size": 4,
             "num_instructions": 1},
        ],
        "num_functions": 1,
    }))
    (target / "recovery.json").write_text(json.dumps({"functions": {}}))
    (target / "asm" / "LEAF.s").write_text("1000:0010  RET\n")
    (target / "config" / "toolchain.yaml").write_text(
        "compiler: turbo-pascal-7\nplatform: dos\n"
    )

    evidence = {
        "schema_version": 3,
        "target": "sample",
        "routine": "LEAF",
        "binary": {"sha256": "binary-sha256"},
        "bytes": {"sha256": "bytes-sha256"},
        "assembly_sha256": "assembly-sha256",
        "static_evidence": {
            "assembly": {"instructions": [
                "MOV BX,SP", "MOV DX,DS", "LDS SI,SS:[BX + 0xa]",
                "LES DI,SS:[BX + 0x6]",
                "MOV CX,word ptr SS:[BX + 0x4]", "CLD",
                "MOVSB.REP ES:DI,SI", "MOV DX,DS", "RETF 0xa",
            ]},
            "gate": {"passed": True, "reasons": []},
        },
        "source_policy": {"binary_derived_evidence_only": True},
    }
    monkeypatch.setattr(oracle_gate, "routine_trace_supported", lambda *_a, **_k: True)
    monkeypatch.setattr(
        target_packet, "evidence_for_routine",
        lambda root, target_name, routine: evidence,
    )
    monkeypatch.setattr(
        frozen_source_eval, "run_training",
        lambda root, output, source, routine: {
            "compile": {"status": "passed"},
            "suites": {"training": {"original": {"status": "passed"},
                                    "candidate": {"status": "passed"}}},
        },
    )

    def fake_run(root, output, source, routine, suites=("training", "terminal")):
        output.mkdir(parents=True, exist_ok=True)
        return {
            "compile": {"status": "passed"},
            "suites": {"terminal": {"original": {"status": "passed"},
                                    "candidate": {"status": "passed"}}},
        }

    monkeypatch.setattr(frozen_source_eval, "run", fake_run)
    called = []
    monkeypatch.setattr(draft, "draft", lambda *args, **kwargs: called.append(args))

    result = recovery_loop.run_recovery(
        "sample", max_iterations=1, root=tmp_path
    )

    assert called == []
    assert result["outcomes"] == {"verified": 1}
    assert result["dl_status"]["oracle_gated"] is True
    assert (target / "src" / "LEAF.inc").is_file()
    store = tmp_path / "knowledge" / "knowledge.json"
    data = json.loads(store.read_text())
    assert "LEAF" in data["targets"]["sample"]["verified"]["routine-trace-parity"]
    replay = data["experience_buffer"]["pascal|turbo-pascal-7"]
    assert replay[-1]["reward"] == 1.0
    assert replay[-1]["gate_outcome"]["gate_status"] == "verified"
    assert replay[-1]["gate_outcome"]["promotion_eligible"] is True


def test_recovery_skips_routines_without_oracle_fixture(tmp_path, monkeypatch):
    from engine import matrix, oracle_gate, target_packet

    (tmp_path / "knowledge").mkdir()
    monkeypatch.setattr(matrix, "load_inventory", lambda *_: {"num_functions": 1})
    monkeypatch.setattr(matrix, "select_frontier", lambda *_a, **_k: [{
        "name": "NO_FIXTURE", "instructions": 1, "unverified_callees": [],
    }])
    monkeypatch.setattr(oracle_gate, "routine_trace_supported", lambda *_a, **_k: False)

    def forbidden(*_args, **_kwargs):
        raise AssertionError("unfixtured routine reached synthesis or evaluation")

    monkeypatch.setattr(target_packet, "evidence_for_routine", forbidden)
    monkeypatch.setattr(verify, "verify_routine_status", forbidden)

    result = recovery_loop.run_recovery("sample", max_iterations=1, root=tmp_path)

    assert result["outcomes"] == {"skipped": 1}
    replay = json.loads(
        (tmp_path / "knowledge" / "knowledge.json").read_text()
    )["experience_buffer"]["pascal|turbo-pascal-7"]
    assert replay[-1]["reward"] == 0.0
    assert replay[-1]["gate_outcome"]["gate_status"] == "skipped"
    assert replay[-1]["gate_outcome"]["promotion_eligible"] is False


def test_recovery_loop_with_empty_frontier_makes_no_draft(tmp_path, monkeypatch):
    from engine import knowledge

    store = tmp_path / "knowledge.json"
    monkeypatch.setattr(knowledge, "STORE", store)
    monkeypatch.setattr(recovery_loop, "KNOWLEDGE", tmp_path)
    monkeypatch.setattr(matrix, "select_frontier", lambda *args, **kwargs: [])
    called = []
    from engine import draft
    monkeypatch.setattr(draft, "draft", lambda *args, **kwargs: called.append(args))

    result = recovery_loop.run_recovery("sample", max_iterations=2)
    assert result["iterations"] == 0
    assert result["outcomes"] == {}
    assert called == []


def test_rtl_classifier_and_renderer_are_strict():
    assert rtl_template.classify("Move\n") == "Move"
    assert rtl_template.classify("The answer is Move") == "UNKNOWN"
    assert rtl_template.classify("Move(Source, Dest, Count)") == "UNKNOWN"
    declaration = "procedure FUN_24dd_48e1(param_1: Integer; param_2, param_3: Pointer);"
    source = rtl_template.render("FUN_24dd_48e1", declaration, "Move")
    assert source is not None
    assert "Move(param_2^, param_3^, Word(param_1));" in source
    assert rtl_template.render("FUN_24dd_48e1", declaration, "FillChar") is None


def test_rtl_declaration_falls_back_to_draft_source(tmp_path):
    source_dir = tmp_path / "targets/liero/src"
    source_dir.mkdir(parents=True)
    (source_dir / "FUN_24dd_48e1.inc").write_text(
        "procedure FUN_24dd_48e1(param_1: Integer; param_2, param_3: Pointer);\n"
        "begin\nend;\n"
    )
    declaration = rtl_template.declaration_for(
        tmp_path, "FUN_24dd_48e1", "procedure FUN_24dd_48e1;"
    )
    assert "param_1" in declaration


def test_rtl_bridge_renderer_uses_byte_bound_effects():
    declaration = "procedure FUN_24dd_48e1(param_1: Integer; param_2, param_3: Pointer);"
    source = rtl_template.render_bridge("FUN_24dd_48e1", declaration, "Move")
    assert source is not None
    assert "Move(param_3^, param_2^, Word(count));" in source
    assert "RegisterSI := (sourceOffset - 1) and 65535;" in source
    assert "RegisterSP := (RegisterSP + 14) and 65535;" in source
    assert rtl_template.render_bridge("FUN_24dd_48e1", declaration, "FillChar") is None


def test_packed_copy_classifier_and_renderer_are_strict():
    label = "CopySkipHighCountLowForward"
    assert rtl_template.classify_packed(f"{label}\n") == label
    assert rtl_template.classify_packed("count is low byte") == "UNKNOWN"
    declaration = "procedure FUN_24dd_4141(param_1: Word; param_2, param_3: Pointer);"
    source = rtl_template.render_packed("FUN_24dd_4141", declaration, label)
    assert source is not None
    assert "count := param_1 and $ff; skip := param_1 shr 8;" in source
    assert "for i := 0 to count - 1 do dst[i] := src[skip + i];" in source
    assert "RegisterSP := (LongInt(RegisterSP) + 14) and $ffff;" in source
    assert (
        rtl_template.render_packed(
            "FUN_24dd_4141", declaration, "CopySkipHighCountLowBackward"
        )
        is None
    )
