"""Failure analysis via a specialised LLM.

Classifies why a decompiled function failed byte-exact verification so the
improve loop can re-draft with targeted context. Separate from the drafting
LLM: a smaller local model can categorise failures while a larger model
does the Pascal re-drafting.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

CATEGORIES = [
    "calling_convention", "memory_segment", "loop_bound",
    "prologue_epilogue", "parameter_order", "register_usage",
    "stack_frame", "control_flow", "data_reference", "unknown",
]

CLASSIFY_PROMPT = """You are a failure-analysis classifier for a 16-bit DOS Turbo Pascal
reverse-engineering factory.

A decompiled function failed byte-exact verification. You are given:
  * the original 8086 assembly (Intel syntax)
  * the previous Pascal draft that failed
  * the verify result (expected vs actual bytes at the mismatch offset)

Classify the failure into EXACTLY one of these categories:
  calling_convention   - wrong calling convention / parameter passing
  memory_segment       - wrong segment:offset or segment register usage
  loop_bound           - off-by-one or wrong loop termination
  prologue_epilogue    - missing/wrong PUSH BP/MOV BP,SP or POP BP/RET
  parameter_order      - parameters in wrong order or wrong count
  register_usage       - wrong register (AX/BX/CX/DX/SI/DI/BP/SP)
  stack_frame          - wrong stack frame layout / local var offsets
  control_flow         - wrong jump/call target or control structure
  data_reference       - wrong data address / variable reference
  unknown              - cannot determine from available evidence

Respond with ONLY a JSON object:
{
  "category": "<one of the above>",
  "explanation": "<one sentence>",
  "suggested_fix": "<concrete change to make in the Pascal draft>",
  "confidence": 0.0-1.0
}

No markdown fences, just raw JSON.

Assembly:
{asm}

Previous Pascal draft:
{pascal}

Verify result:
{verify_result}
"""

def _run_llm(prompt: str, model: str | None, endpoint: str | None) -> str | None:
    """Call a local LLM endpoint. Returns raw text or None on failure."""
    import urllib.request

    url = endpoint or "http://localhost:11434/api/generate"
    payload = {
        "model": model or "phi4-mini:3.8b",
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        data = json.loads(body)
        return data.get("response", "")
    except Exception as e:
        print(f"[failure_analyzer] LLM call failed: {e}")
        return None


def _parse_classification(text: str | None) -> dict:
    """Parse the LLM JSON response into a validated classification dict."""
    if not text:
        return _default("no-llm-response")

    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return _default("json-parse-failed")
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError:
            return _default("json-parse-failed")

    cat = obj.get("category", "unknown")
    if cat not in CATEGORIES:
        cat = "unknown"
    return {
        "category": cat,
        "explanation": obj.get("explanation", "unparsed")[:500],
        "suggested_fix": obj.get("suggested_fix", "review draft manually")[:500],
        "confidence": float(obj.get("confidence", 0.5)),
    }


def _default(reason: str) -> dict:
    return {
        "category": "unknown",
        "explanation": "classification unavailable: " + reason,
        "suggested_fix": "re-draft from scratch with full context",
        "confidence": 0.0,
    }


def classify_failure(
    fn: str,
    asm_text: str,
    pascal_draft: str,
    expected_hex: str,
    actual_hex: str,
    mismatch_offset: int,
    model: str | None = None,
    endpoint: str | None = None,
) -> dict:
    """Classify why function `fn` failed verification."""
    verify_result = (
        f"Function {fn} failed byte-exact verification.\n"
        f"Expected bytes at offset {mismatch_offset:#x}: {expected_hex}\n"
        f"Actual   bytes at offset {mismatch_offset:#x}: {actual_hex}\n"
    )
    prompt = CLASSIFY_PROMPT.format(
        asm=asm_text[:3000],
        pascal=pascal_draft[:2000],
        verify_result=verify_result,
    )
    text = _run_llm(prompt, model, endpoint)
    return _parse_classification(text)


def record_failure(
    data: dict,
    toolchain: str,
    category: str,
    asm_snippet: str,
    fn: str,
    target: str,
    store: pathlib.Path,
) -> None:
    """Append a failure to the per-toolchain failures catalogue."""
    compilers = data.setdefault("compilers", {})
    tc = compilers.setdefault(toolchain, {})
    failures = tc.setdefault("failures", {})
    entry = failures.setdefault(
        category, {"count": 0, "examples": [], "last_seen": None}
    )
    entry["count"] += 1
    import datetime as _dt
    entry["last_seen"] = _dt.date.today().isoformat()
    if len(entry["examples"]) < 10:
        entry["examples"].append(
            {"fn": fn, "target": target, "asm": asm_snippet[:500]}
        )
    if len(entry["examples"]) > 10:
        entry["examples"] = entry["examples"][-10:]


def get_anti_patterns(data: dict, toolchain: str, limit: int = 8) -> list[dict]:
    """Return the most common failure categories as anti-patterns."""
    tc = data.get("compilers", {}).get(toolchain, {})
    failures = tc.get("failures", {})
    items = []
    for cat, entry in failures.items():
        items.append(
            {
                "category": cat,
                "count": entry.get("count", 0),
                "example_asm": (
                    entry["examples"][0]["asm"] if entry.get("examples") else ""
                ),
            }
        )
    items.sort(key=lambda x: -x["count"])
    return items[:limit]


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Classify a verify failure")
    ap.add_argument("--fn", required=True)
    ap.add_argument("--asm", required=True)
    ap.add_argument("--pascal", required=True)
    ap.add_argument("--expected", required=True)
    ap.add_argument("--actual", required=True)
    ap.add_argument("--offset", type=lambda x: int(x, 16), default=0)
    ap.add_argument("--model", default=None)
    ap.add_argument("--endpoint", default=None)
    a = ap.parse_args()
    asm = pathlib.Path(a.asm).read_text(errors="replace")
    pascal = pathlib.Path(a.pascal).read_text(errors="replace")
    result = classify_failure(
        a.fn, asm, pascal, a.expected, a.actual, a.offset, a.model, a.endpoint
    )
    print(json.dumps(result, indent=2))