#!/usr/bin/env python3
"""
Fully automated end-to-end Liero reverse engineering pipeline.

Steps:
  1. Validate the frozen build.sha1 oracle gate against BYOD
  2. Run RL-guided recovery for all functions  
  3. Verify each draft against oracle
  4. Generate final report

Usage:
    python3 tools/run_full_pipeline.py --target liero --max-iterations 295
    
Model selection:
  --model ollama      Use Ollama models via RL agent (default)
  --model 1.5b        Use fine-tuned Qwen2.5-Coder-1.5B model
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import subprocess

import shutil

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from engine import recovery_loop, knowledge, rl_engine

BASE = pathlib.Path(__file__).resolve().parent.parent


def populate_build_sha1(target: str) -> int:
    """Validate the frozen oracle gate against BYOD; never rewrite it."""
    byod = BASE / "extracted" / target
    sha1_path = BASE / "targets" / target / "config" / "build.sha1"
    if not sha1_path.is_file():
        print(f"[pipeline] frozen oracle gate missing at {sha1_path}")
        return 1
    lines = [
        line.strip()
        for line in sha1_path.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not lines:
        print(f"[pipeline] frozen oracle gate has no entries at {sha1_path}")
        return 1
    mismatches = []
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            mismatches.append(line)
            continue
        expected, rel = parts
        source = byod / rel
        if not source.is_file():
            mismatches.append(rel)
        elif hashlib.sha1(source.read_bytes()).hexdigest() != expected:
            mismatches.append(rel)
    if mismatches:
        print(f"[pipeline] oracle gate mismatch: {mismatches[:5]}")
        return 1
    print(f"[pipeline] frozen oracle gate validated ({len(lines)} entries)")
    return 0


def _create_wrapper_pascal(target: str) -> pathlib.Path:
    """Create a wrapper Pascal program that includes all .inc function drafts."""
    src_dir = BASE / "targets" / target / "src"
    build_dir = BASE / "targets" / target / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all .inc files and .pas files from src directory
    inc_files = sorted(src_dir.glob("*.inc"))
    pas_files = sorted(src_dir.glob("*.pas"))
    
    # Copy .inc files to build directory so FPC can find them via #include
    for f in inc_files:
        shutil.copy(f, build_dir / f.name)
    
    # Build the includes list - use relative paths from build directory
    includes = []
    for f in inc_files + pas_files:
        rel = f.relative_to(src_dir).as_posix()
        # Use the copy in build directory
        includes.append("{" + "$INCLUDE " + f.name + "}")
    
    # Create wrapper program structure
    wrapper_content = "{$MODE TP}\n{$ASMMODE INTEL}\nprogram liero_recovery;\nuses LieroDat, LieroRuntime;\n"
    wrapper_content += "\n".join(includes)
    wrapper_content += "\n\nbegin\n  { recovery program entry point }\n  writeln('Liero function recovery');\nend.\n"
    
    wrapper_path = build_dir / "recovery_wrapper.pas"
    wrapper_path.write_text(wrapper_content)
    return wrapper_path


def compile_drafts(target: str) -> int:
    """Compile the drafted Pascal tree without mutating the oracle gate."""
    build_dir = BASE / "targets" / target / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    for compiler in ["fpc", "ppc386", "tpc7", "ppcx64"]:
        try:
            probe = subprocess.run(
                [compiler, "-iV"], capture_output=True, text=True, timeout=5,
                cwd=BASE,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
        if probe.returncode != 0:
            continue
        print(f"[pipeline] Found Pascal compiler: {compiler}")
        wrapper_path = _create_wrapper_pascal(target)
        out = build_dir / "recovery_wrapper.o"
        result = subprocess.run(
            [compiler, "-Mtp", f"-o{out}", str(wrapper_path)],
            capture_output=True, text=True, timeout=120, cwd=BASE,
        )
        compiled = result.returncode == 0 or out.exists()
        print(f"[pipeline] compile status={compiled} compiler={compiler}")
        if not compiled:
            print(result.stderr[-2000:])
            return 1
        return 0
    print("[pipeline] No Pascal compiler found — compilation unavailable")
    return 0


def run_recovery(target: str, max_iterations: int, models: list[str] | None = None,
                 oracle: str = "routine-trace-parity", endpoint: str | None = None,
                 byod: pathlib.Path | None = None,
                 build: pathlib.Path | None = None) -> dict:
    """Step 3: Run RL-guided recovery loop."""
    print(f"\n{'='*60}")
    print(f"Step 3: RL-Guided Recovery for {target}")
    print(f"{'='*60}\n")

    return recovery_loop.run_recovery(
        target=target,
        max_iterations=max_iterations,
        oracle=oracle,
        available_models=models or ["losore-llm4decompile-22b-v2:Q4_K_M"],
        endpoint=endpoint,
        byod=byod,
        build=build,
    )


def generate_report(target: str, results: dict) -> None:
    """Step 4: Generate final report."""
    report_path = BASE / "targets" / target / "pipeline_report.json"

    outcomes = results.get("outcomes", {})

    report = {
        "target": target,
        "total_functions": results.get("frontier", {}).get("total", 295),
        "verified": results.get("total_verified", 0),
        "attempts": results.get("total_attempts", 0),
        "reward": results.get("cumulative_reward", 0.0),
        "outcomes": dict(outcomes),
        "coverage": results.get("coverage", 0.0),
        "oracle": results.get("oracle", "routine-trace-parity"),
        "pascal_isolation": rl_engine.verify_pascal_isolation(knowledge.load()),
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")

    print(f"\n{'='*60}")
    print(f"PIPELINE REPORT: {target}")
    print(f"{'='*60}")
    print(f"Total functions:   {report['total_functions']}")
    print(f"Verified:          {report['verified']}")
    print(f"Attempts:          {report['attempts']}")
    print(f"Reward:            {report['reward']:.2f}")
    print(f"Pascal isolation:  {report['pascal_isolation']}")
    print("\nOutcomes:")
    for oc, count in sorted(outcomes.items(), key=lambda item: -item[1]):
        print(f"  {oc}: {count}")
    print(f"\nReport saved to: {report_path}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Fully automated Liero reverse engineering pipeline")
    ap.add_argument("--target", default="liero", help="Target slug")
    ap.add_argument("--max-iterations", type=int, default=295, help="Max recovery iterations")
    ap.add_argument("--model", action="append", default=None, help="Model id; repeat for a panel")
    ap.add_argument(
        "--oracle", default="routine-trace-parity",
        choices=["dat-parity", "byte-exact", "relocation-aware", "round-trip",
                 "trace-parity", "routine-trace-parity", "constructor-parity"],
    )
    ap.add_argument("--endpoint", default=None)
    ap.add_argument("--byod", default=None)
    ap.add_argument("--build", default=None)
    args = ap.parse_args()

    print(f"{'='*60}")
    print(f"AUTOMATED PIPELINE: {args.target}")
    print(f"{'='*60}\n")

    print("[Step 1/4] Validating frozen oracle gate...")
    if populate_build_sha1(args.target) != 0:
        print("[pipeline] abort: oracle gate is invalid")
        return 1

    print("\n[Step 2/4] Compiling drafted Pascal...")
    if compile_drafts(args.target) != 0:
        print("[pipeline] abort: draft compilation failed")
        return 1

    print("\n[Step 3/4] Running RL-guided recovery...")
    results = run_recovery(
        args.target, args.max_iterations, args.model, args.oracle, args.endpoint,
        pathlib.Path(args.byod) if args.byod else None,
        pathlib.Path(args.build) if args.build else None,
    )

    # Step 4: Generate report
    print("\n[Step 4/4] Generating report...")
    generate_report(args.target, results)

    print(f"\n{'='*60}")
    print("PIPELINE COMPLETE")
    print(f"{'='*60}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
