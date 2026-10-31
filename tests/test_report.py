import json
import pathlib
import subprocess
import sys

from engine import recovery
from tools.report import _drafted, _generated, _recovery_summary, _verified


def test_generated_counts_function_files_but_not_program_includes(tmp_path):
    target = tmp_path / "stickman"
    (target / "asm").mkdir(parents=True)
    (target / "src").mkdir()
    (target / "asm" / "FUN_1234.s").write_text("ret\n")
    (target / "src" / "FUN_1234.inc").write_text(
        "procedure FUN_1234;\nbegin\n  { TODO: translate from asm }\nend;\n"
    )
    (target / "src" / "_forward.inc").write_text("declarations\n")
    (target / "src" / "entry.inc").write_text("program entry\n")

    assert _generated(tmp_path, "stickman") == 1
    assert _drafted(tmp_path, "stickman") == 0


def test_drafted_counts_implemented_bodies_not_scaffolds(tmp_path):
    target = tmp_path / "liero"
    (target / "asm").mkdir(parents=True)
    (target / "src").mkdir()
    (target / "asm" / "FUN_1234.s").write_text("ret\n")
    source = target / "src" / "FUN_1234.inc"
    source.write_text(
        "{ generated comment }\nprocedure FUN_1234;\n"
        "begin\n  { placeholder }\nend;\n"
    )

    assert _drafted(tmp_path, "liero") == 0

    source.write_text(
        "{ documented behavior }\nprocedure FUN_1234;\n"
        "begin\n  Inc(A);\nend;\n"
    )
    assert _drafted(tmp_path, "liero") == 1


def test_verified_excludes_dat_oracle_artifacts(tmp_path):
    asm = tmp_path / "stickman" / "asm"
    asm.mkdir(parents=True)
    (asm / "FUN_1234.s").write_text("ret\n")
    target_data = {
        "verified": {
            "dat-parity": ["LIERO.DAT"],
            "byte-exact": ["src/FUN_1234.inc"],
        }
    }

    assert _verified(tmp_path, "stickman", target_data) == 1
    assert _verified(
        tmp_path, "stickman", {"verified": {"dat-parity": ["LIERO.DAT"]}}
    ) == 0


def test_report_marks_missing_recovery_ledger_explicitly(tmp_path):
    result = _recovery_summary(tmp_path, "liero")

    assert result == {
        "recovery_ledger": "missing",
        "source_recovered": None,
        "evidence_accounted_percent": None,
        "stale_source_recoveries": None,
    }


def test_report_uses_recovery_ledger_without_counting_body_presence(tmp_path):
    target = tmp_path / "liero"
    (target / "asm").mkdir(parents=True)
    (target / "src").mkdir()
    (target / "functions.json").write_text(
        '{"num_functions": 1, "functions": [{"name": "FUN_1"}]}'
    )
    (target / "asm" / "FUN_1.s").write_text("0000:0000  RET\n")
    (target / "src" / "FUN_1.inc").write_text(
        "procedure FUN_1;\nbegin\n  Inc(Value);\nend;\n"
    )
    recovery.initialize_ledger(target)

    result = _recovery_summary(tmp_path, "liero")

    assert result["recovery_ledger"] == "present"
    assert result["source_recovered"] == 0
    assert result["evidence_accounted_percent"] == 0


def test_report_cli_imports_recovery_from_outside_repository(tmp_path):
    """Oracle: actual CLI must report scoped checks without relying on pytest imports."""
    target = tmp_path / "targets/liero"
    (target / "asm").mkdir(parents=True)
    (target / "src").mkdir()
    (target / "functions.json").write_text(
        '{"num_functions": 1, "functions": [{"name": "FUN_1"}]}'
    )
    (target / "asm/FUN_1.s").write_text("0000:0000  RET\n")
    recovery.initialize_ledger(target)
    script = pathlib.Path(__file__).resolve().parents[1] / "tools/report.py"
    subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        capture_output=True,
        check=True,
        timeout=30,
    )
    result = json.loads((tmp_path / "reports/progress.json").read_text())
    assert result["targets"]["liero"]["source_recovered"] == 0
    assert result["targets"]["liero"]["scoped_differential_routines_passed"] == 0
    assert result["targets"]["liero"]["scoped_differential_reports_invalid"] == 0
