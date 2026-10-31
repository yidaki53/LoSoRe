import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent


def test_preflight_blocks_when_required_byod_is_missing(tmp_path):
    target_config = tmp_path / "targets" / "demo" / "config"
    target_config.mkdir(parents=True)
    (target_config / "target.yaml").write_text(
        "slug: demo\nkind: game\nplatform: dos\nlanguage: pascal\n"
    )
    (target_config / "toolchain.yaml").write_text(
        "compiler: turbo-pascal-7\nlanguage: pascal\n"
    )

    result = subprocess.run(
        [
            sys.executable,
            str(REPO / "engine" / "preflight.py"),
            "--target",
            "demo",
            "--workspace",
            str(tmp_path),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    report = json.loads(result.stdout)
    assert result.returncode != 0
    assert report["status"] == "blocked"
    assert any("extracted/demo" in issue for issue in report["blockers"])


def test_full_pipeline_stops_before_provenance_when_preflight_is_blocked():
    result = subprocess.run(
        ["make", "pipeline", "TARGET=preflight-missing-target"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )

    output = result.stdout + result.stderr
    assert result.returncode != 0
    assert "[preflight:preflight-missing-target] BLOCKED" in output
    assert "[provenance:" not in output
