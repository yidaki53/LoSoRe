"""Evidence-first overnight analysis of unresolved Liero control-flow targets.

The run disassembles each file-backed direct target from the original MZ image,
then asks a local Ollama model for a hypothesis and a separate critique. It
only writes resumable reports; it never edits assembly, source, or recovery
attestations.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.recovery import audit_target  # noqa: E402
from tools.asmcfg import parse_ghidra_asm  # noqa: E402
from tools.binary_census import build_census  # noqa: E402

DEFAULT_MODEL = "qwen2.5-coder:14b-instruct-q4_K_M"
DEFAULT_ENDPOINT = "http://localhost:11434"
ANALYSIS_VERSION = 2
TARGET_PRIORITY = {
    0x1398B: 0,
}


def _hex(value: int) -> str:
    return f"0x{value:05x}"


def _log(message: str) -> None:
    print(f"[overnight7 {time.strftime('%Y-%m-%d %H:%M:%S')}] {message}", flush=True)


def _save_json(path: pathlib.Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def _file_backed_targets(
    target_root: pathlib.Path, audit: dict, census: dict
) -> tuple[list[dict], int, int, str]:
    load_segment = int(census["summary"]["analysis_load_segment"], 16)
    header_bytes = census["binary"]["header_bytes"]
    binary_bytes = census["binary"]["actual_file_bytes"]
    image_start = load_segment * 16
    image_end = image_start + census["binary"]["load_image_bytes"]
    target_groups: dict[int, list[dict]] = defaultdict(list)

    for routine in audit["routines"]:
        asm_path = target_root / "asm" / f"{routine['name']}.s"
        if not asm_path.is_file():
            continue
        parsed = parse_ghidra_asm(asm_path.read_text(errors="replace"))
        for transfer in routine["unresolved_control_transfers"]:
            if transfer["target"] is None:
                continue
            destination = int(transfer["target"], 16)
            if not image_start <= destination < image_end:
                continue
            source_address = int(transfer["address"], 16)
            index = parsed["addrs"].index(source_address)
            start = max(0, index - 8)
            end = min(len(parsed["insts"]), index + 9)
            target_groups[destination].append(
                {
                    "caller": routine["name"],
                    "source_address": transfer["address"],
                    "instruction": transfer["instruction"],
                    "context": [
                        {
                            "address": _hex(parsed["addrs"][item]),
                            "instruction": parsed["insts"][item],
                        }
                        for item in range(start, end)
                    ],
                    "assembly_sha256": hashlib.sha256(
                        asm_path.read_bytes()
                    ).hexdigest(),
                }
            )

    targets = []
    for destination, callers in target_groups.items():
        file_offset = header_bytes + destination - image_start
        if not 0 <= file_offset < binary_bytes:
            continue
        targets.append(
            {
                "address": _hex(destination),
                "file_offset": _hex(file_offset),
                "callers": callers,
            }
        )
    targets.sort(
        key=lambda target: (
            TARGET_PRIORITY.get(int(target["address"], 16), 100),
            int(target["address"], 16),
        )
    )
    return targets, image_start, image_end, census["binary"]["sha256"]


def _disassemble(
    binary_path: pathlib.Path,
    target: dict,
    file_vma: int,
    file_size: int,
    max_bytes: int,
) -> str:
    address = int(target["address"], 16)
    stop_address = min(address + max_bytes, file_vma + file_size)
    result = subprocess.run(
        [
            "objdump",
            "-D",
            "-b",
            "binary",
            "-m",
            "i8086",
            "-M",
            "intel",
            f"--adjust-vma={_hex(file_vma)}",
            f"--start-address={_hex(address)}",
            f"--stop-address={_hex(stop_address)}",
            str(binary_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(
            f"objdump failed for {target['address']}: {result.stderr.strip()}"
        )
    lines = result.stdout.splitlines()
    instruction_lines = [
        line for line in lines if re.match(r"^\s*[0-9a-fA-F]+:", line)
    ]
    if not instruction_lines:
        raise RuntimeError(f"objdump produced no instructions at {target['address']}")
    return "\n".join(instruction_lines)


def _ollama_chat(
    endpoint: str,
    model: str,
    prompt: str,
    timeout_seconds: int,
) -> str:
    request_data = json.dumps(
        {
            "model": model,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are analyzing 16-bit x86 control flow. Distinguish "
                        "observed bytes from hypotheses. Never invent instructions."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "options": {"temperature": 0.1, "num_ctx": 8192, "num_predict": 1024},
        }
    ).encode()
    request = urllib.request.Request(
        f"{endpoint.rstrip('/')}/api/chat",
        data=request_data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"local Ollama request failed: {error}") from error
    content = payload.get("message", {}).get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("local Ollama returned no message content")
    return content.strip()


def _analysis_prompt(target: dict, disassembly: str) -> str:
    callers = json.dumps(target["callers"], indent=2)
    return (
        "Analyze this candidate alternate entry using only the supplied evidence.\n"
        "Return concise bullets for: (1) instruction boundaries starting at the "
        "target, (2) direct branch/call targets and returns visible in the "
        "listing, (3) which control-flow exits are not established by this "
        "window, and (4) the single best next static check. Do not assign Pascal "
        "semantics or claim the entry is correct. Mark all conclusions as "
        "hypotheses requiring human review.\n\n"
        f"Candidate target: {target['address']}\n"
        f"Mapped file offset: {target['file_offset']}\n"
        f"Caller evidence:\n{callers}\n"
        f"Raw executable disassembly:\n{disassembly}\n"
    )


def _critique_prompt(
    target: dict, disassembly: str, hypothesis: str
) -> str:
    return (
        "Critique the proposed control-flow notes against the raw disassembly. "
        "List only specific claims that are unsupported, contradicted, or "
        "missing important visible branches/returns. If none, say so. Do not "
        "add semantic interpretations or replace evidence with guesses.\n\n"
        f"Candidate target: {target['address']}\n"
        f"Raw executable disassembly:\n{disassembly}\n"
        f"Proposed notes:\n{hypothesis}\n"
    )


def _load_results(path: pathlib.Path, binary_sha256: str) -> dict:
    if not path.is_file():
        return {"binary_sha256": binary_sha256, "targets": {}}
    existing = json.loads(path.read_text())
    if existing.get("binary_sha256") != binary_sha256:
        raise ValueError(
            f"{path} belongs to a different binary; choose a fresh --output-dir"
        )
    if existing.get("analysis_version") not in {None, ANALYSIS_VERSION}:
        raise ValueError(
            f"{path} uses analysis version {existing['analysis_version']}; "
            "choose a fresh --output-dir"
        )
    existing["analysis_version"] = ANALYSIS_VERSION
    return existing


def _write_report(path: pathlib.Path, results: dict) -> None:
    lines = [
        "# Overnight alternate-entry analysis",
        "",
        f"- Binary SHA-256: `{results['binary_sha256']}`",
        f"- Default model: `{results['model']}` via local Ollama",
        "- Status: model notes are hypotheses only; no recovery gate or source "
        "attestation was changed.",
        "",
    ]
    for address, item in sorted(results["targets"].items()):
        lines.extend(
            [
                f"## {address}",
                "",
                f"- File offset: `{item['file_offset']}`",
                f"- Status: `{item['status']}`",
                f"- Analysis model: `{item.get('model', results['model'])}`",
                "- Callers: "
                + ", ".join(
                    f"`{caller['caller']}:{caller['source_address']}`"
                    for caller in item["callers"]
                ),
                "",
                "### Independent disassembly",
                "",
                "```asm",
                item.get("disassembly", "not available"),
                "```",
                "",
                "### Model hypothesis (unverified)",
                "",
                item.get("hypothesis", "Not generated."),
                "",
                "### Model critique (unverified)",
                "",
                item.get("critique", "Not generated."),
                "",
            ]
        )
    path.write_text("\n".join(lines))


def run(args: argparse.Namespace) -> int:
    target_root = ROOT / "targets" / args.target
    binary_path = args.binary or ROOT / "extracted" / args.target / "LIERO.EXE"
    out_dir = args.output_dir or ROOT / "reports" / "overnight7"
    out_dir.mkdir(parents=True, exist_ok=True)

    audit = audit_target(target_root)
    census = build_census(target_root, binary_path)
    candidates, image_start, image_end, binary_sha256 = _file_backed_targets(
        target_root, audit, census
    )
    results_path = out_dir / "analysis.json"
    results = _load_results(results_path, binary_sha256)
    results["analysis_version"] = ANALYSIS_VERSION
    results["model"] = args.model
    results["target"] = args.target
    results["candidates_total"] = len(candidates)
    results["started_at"] = results.get("started_at", time.strftime("%Y-%m-%dT%H:%M:%S%z"))
    file_vma = image_start - census["binary"]["header_bytes"]
    _log(
        f"{len(candidates)} file-backed direct targets; "
        f"binary={binary_sha256[:12]}; output={out_dir}"
    )
    started = time.monotonic()
    remaining = candidates[: args.max_targets] if args.max_targets else candidates
    for index, candidate in enumerate(remaining, 1):
        if time.monotonic() - started >= args.budget_hours * 3600:
            _log("time budget reached; preserving completed results")
            break
        address = candidate["address"]
        previous = results["targets"].get(address, {})
        if (
            previous.get("status") == "complete"
            and previous.get("analysis_version") == ANALYSIS_VERSION
            and previous.get("max_bytes") == args.max_bytes
        ):
            _log(f"[{index}/{len(remaining)}] {address} already complete; skipping")
            continue
        item = {
            **candidate,
            "status": "running",
            "analysis_version": ANALYSIS_VERSION,
            "max_bytes": args.max_bytes,
            "model": args.model,
        }
        results["targets"][address] = item
        _save_json(results_path, results)
        try:
            item["disassembly"] = _disassemble(
                binary_path,
                candidate,
                file_vma,
                census["binary"]["actual_file_bytes"],
                args.max_bytes,
            )
            item["hypothesis"] = _ollama_chat(
                args.endpoint,
                args.model,
                _analysis_prompt(candidate, item["disassembly"]),
                args.timeout_seconds,
            )
            _save_json(results_path, results)
            item["critique"] = _ollama_chat(
                args.endpoint,
                args.model,
                _critique_prompt(
                    candidate, item["disassembly"], item["hypothesis"]
                ),
                args.timeout_seconds,
            )
            item["status"] = "complete"
            item["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            _log(
                f"[{index}/{len(remaining)}] {address} complete "
                f"({len(candidate['callers'])} caller(s))"
            )
        except (OSError, RuntimeError, ValueError) as error:
            item["status"] = "failed"
            item["error"] = str(error)
            _log(f"[{index}/{len(remaining)}] {address} failed: {error}")
        _save_json(results_path, results)
        _write_report(out_dir / "CONTROL_FLOW_REVIEW.md", results)

    results["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    results["remaining_file_backed_targets"] = [
        candidate["address"]
        for candidate in candidates
        if results["targets"].get(candidate["address"], {}).get("status")
        != "complete"
    ]
    _save_json(results_path, results)
    _write_report(out_dir / "CONTROL_FLOW_REVIEW.md", results)
    _log(
        f"finished; {len(candidates) - len(results['remaining_file_backed_targets'])}"
        f"/{len(candidates)} target(s) complete; image="
        f"{_hex(image_start)}..{_hex(image_end)}"
    )
    has_failed_targets = any(
        item["status"] == "failed" for item in results["targets"].values()
    )
    return 1 if has_failed_targets else 0


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="liero")
    parser.add_argument("--binary", type=pathlib.Path)
    parser.add_argument("--output-dir", type=pathlib.Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--budget-hours", type=float, default=8)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--max-bytes", type=int, default=384)
    parser.add_argument("--max-targets", type=int)
    return parser.parse_args(argv)


if __name__ == "__main__":
    try:
        raise SystemExit(run(_parse_args()))
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        _log(f"fatal: {error}")
        raise SystemExit(2) from error
