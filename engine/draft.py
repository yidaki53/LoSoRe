"""P1 agent-draft: m2c -> candidate C, optional LLM refine (llama.cpp/vLLM local; hosted opt-in).
Input: targets/<slug>/asm/<fn>.s ; Output: targets/<slug>/src/<fn>.c + oracle label.
Backends tried in order: m2c (if installed) -> template. --llm refines via local server or CLI.
Disc-gated: SKIP without asm/ (CI green). Hit-rate monitored by engine/scheduler.py."""
from __future__ import annotations
import argparse, pathlib, shutil, subprocess, sys

TEMPLATE = """/* {slug}::{fn} — {kind} candidate (oracle: {oracle}).
 * Drafted from asm/{fn}.s via {backend}; UNMATCHED until verify passes.
 * Original assembly retained in asm/{fn}.s (INCLUDE_ASM residue).
 */
{body}
"""

FALLBACK_BODY = "int {fn}(void) {{\n    return 0; /* TODO: match original semantics */\n}}\n"

def run_m2c(asm_file: pathlib.Path, target_yaml: pathlib.Path) -> str | None:
    m2c = shutil.which("m2c")
    if not m2c:
        return None
    try:
        r = subprocess.run([m2c, str(asm_file)], capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
    except Exception as e:
        print(f"[m2c] {e}")
    return None

def run_llm(prompt: str, model: str | None, endpoint: str | None) -> str | None:
    """Local-first: llama.cpp server (/completion) or `llm` CLI; hosted only if LSR_ALLOW_HOSTED=1."""
    import json, os, urllib.request
    if endpoint:  # e.g. http://localhost:8080 (llama.cpp) or vLLM OpenAI-compat
        try:
            data = json.dumps({"prompt": prompt, "n_predict": 512}).encode()
            req = urllib.request.Request(endpoint.rstrip("/") + "/completion", data=data,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read()).get("content")
        except Exception as e:
            print(f"[llm-endpoint] {e}")
            return None
    cli = shutil.which("llm")
    if cli and model:
        try:
            r = subprocess.run([cli, "-m", model, prompt], capture_output=True, text=True, timeout=300)
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout
        except Exception as e:
            print(f"[llm-cli] {e}")
    if os.environ.get("LSR_ALLOW_HOSTED") != "1":
        return None
    return None

def draft(target: str, fn: str | None = None, oracle: str = "none",
          use_llm: bool = False, model: str | None = None, endpoint: str | None = None) -> int:
    root = pathlib.Path(f"targets/{target}")
    asm = root / "asm"
    if not asm.exists() or not any(asm.glob("*.s")):
        print(f"[draft:{target}] SKIP no asm/ (run ingest with BYOD first)")
        return 0
    kind = "game"
    y = root / "config" / "target.yaml"
    if y.exists():
        for line in y.read_text().splitlines():
            if line.startswith("kind:"):
                kind = line.split(":", 1)[1].strip()
    fns = [fn] if fn else [p.stem for p in sorted(asm.glob("*.s"))]
    for f in fns:
        out = root / "src" / f"{f}.c"
        if out.exists():
            print(f"[draft:{target}] exists src/{f}.c — skipping")
            continue
        body, backend = FALLBACK_BODY.format(fn=f), "template"
        m2c_out = run_m2c(asm / f"{f}.s", y)
        if m2c_out:
            body, backend = m2c_out, "m2c"
        if use_llm:
            prompt = (f"Rewrite this decompiled C to match original {kind} function {f}, "
                      f"preserving semantics exactly:\n{body}\nAssembly in asm/{f}.s.")
            llm_out = run_llm(prompt, model, endpoint)
            if llm_out:
                body, backend = llm_out, f"m2c+llm({model or endpoint})"
        out.write_text(TEMPLATE.format(slug=target, fn=f, kind=kind, oracle=oracle,
                                       backend=backend, body=body))
        print(f"[draft:{target}] wrote src/{f}.c via {backend} (oracle: {oracle})")
    return 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--game", default=None, help="deprecated alias")
    ap.add_argument("--fn", default=None)
    ap.add_argument("--oracle", default="none")
    ap.add_argument("--llm", action="store_true", help="refine via local LLM")
    ap.add_argument("--model", default=None)
    ap.add_argument("--endpoint", default=None, help="llama.cpp/vLLM server URL")
    a = ap.parse_args()
    sys.exit(draft(a.target or a.game, a.fn, a.oracle, a.llm, a.model, a.endpoint))
