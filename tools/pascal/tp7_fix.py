"""LLM-based Turbo Pascal 7 syntax fixer for decompiled Pascal source.

Runs automatically when fpc -Mtp compilation fails.
Preserves function signature and semantics, outputs the routine
with 'begin...end;'.
"""
import urllib.request
import json
import subprocess
import tempfile
import os

OLLAMA = "http://localhost:11434"


def _extract_compile_errors(stderr_text: str) -> list:
    """Extract FPC error messages from compilation output."""
    if not stderr_text:
        return []
    errors = []
    for line in stderr_text.split('\n'):
        line = line.strip()
        if 'Fatal:' in line or 'Error:' in line:
            errors.append(line)
    return errors

def ollama_gen(model: str, prompt: str, npx: int = 1024, timeout: int = 300) -> str:
    data = json.dumps({"model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": 0.0, "num_ctx": 8192, "num_predict": npx}}).encode()
    req = urllib.request.Request(OLLAMA + "/api/generate", data=data,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()).get("response", "")

def fix_pascal_tp7(pas_content: str, fn: str) -> str:
    """Use LLM to make decompiled Pascal code TP7-compatible.

    Transforms decompiled code snippets into TP7-compatible syntax:
    - Adds missing function/procedure declaration header
    - Adds missing `var` section for undeclared variables
    - Replaces `//` comments with `{ }` comments (TP7-compatible)
    - Fixes type casts to TP7-compatible syntax
    - Preserves Mem[base], MemW[base], and/or operators (already TP7-compatible)
    - Outputs the routine with 'begin...end;'

    Does NOT produce standalone-compilable code — inter-function references
    (FUN_XXXX_YYYY calls) remain as-is since they require full program context.
    """
    prompt = f"""You are making a Turbo Pascal 7 (TP7) routine TP7-compatible for Liero v1.33.

The input is a decompiled Pascal code SNIPPET (a function body without declarations).
Transform it into TP7-compatible syntax. Do NOT try to make it standalone-compilable
(inter-function references like FUN_XXXX_YYYY cannot be resolved without full program context).

Required changes:
1. Add a function/procedure declaration header at the top: `function {fn}: <return_type>;` or `procedure {fn};`
   - If the code assigns to `{fn}` (e.g. `{fn} := value`), it's a function — guess return type (Integer, Boolean, Byte, etc.)
   - Otherwise it's a procedure
2. Add a `var` section declaring ALL variables used but not declared (param_*, local_*, cond_*, base, old_val, rnd, carry, etc.)
   - Use TP7 types: Byte, Char, Word, Integer, Longint, Boolean, Pointer
   - Guess types from usage: `Mem[...]` → Byte, `MemW[...]` → Word, `FUN_...()` → Integer
3. Replace ALL `//` comments with `{{ }}` comments (TP7 does not support `//`)
4. Fix type casts to TP7 syntax: `Word(x)`, `Byte(x)`, `Pointer(x)`, `Integer(x)` are fine in TP7
5. Keep `Mem[base]`, `MemW[base]`, `and`, `or`, `$` hex literals, `@` address-of — all TP7-compatible
6. Output the routine with `begin...end;`

TP7-compatible types only: Byte, Char, Word, Integer, Longint, Boolean, Pointer.
No `Result` variable. No `goto`. No `Exit(v)`. No `asm` blocks.

Function name: {fn}
Original code:
{pas_content}"""

    try:
        result = ollama_gen("qwen2.5-coder:14b-instruct-q4_K_M", prompt, timeout=300)
    except Exception:
        result = ollama_gen("qwen2.5-coder:14b-instruct", prompt, timeout=300)

    # Extract the TP7-compatible routine from LLM output
    # Look for function/procedure declaration through end;
    start_markers = ['function ', 'procedure ']
    start_idx_extract = -1
    for marker in start_markers:
        idx = result.lower().find(marker)
        if idx >= 0:
            start_idx_extract = idx
            break

    if start_idx_extract >= 0:
        end_idx_extract = result.rfind('end;')
        if end_idx_extract > start_idx_extract:
            result = result[start_idx_extract:end_idx_extract + 4].strip()

    return result.strip()

def auto_tp7_fix(pas_content: str, fn: str, max_iterations: int = 3) -> dict:
    """Iterative TP7 fixer with compilation feedback loop.

    Runs the LLM fixer, compiles with fpc -Mtp, and if compilation fails,
    passes the errors back to the LLM for correction. Repeats up to
    max_iterations times.

    Returns dict with keys:
      - 'fixed': the best fixed code found
      - 'compile_ok': whether it compiled successfully
      - 'error': compilation error message if failed
      - 'iterations': number of iterations attempted
    """
    fixed = fix_pascal_tp7(pas_content, fn)
    iterations = 0
    best_fixed = fixed

    for iteration in range(max_iterations):
        iterations = iteration + 1

        # Try compiling with fpc -Mtp
        with tempfile.NamedTemporaryFile(suffix='.pas', mode='w', delete=False) as tf:
            tf.write(fixed)
            tf.flush()
            tmp_path = tf.name

        result = subprocess.run(
            ['fpc', '-Mtp', tmp_path],
            capture_output=True, text=True, timeout=30
        )
        os.unlink(tmp_path)

        if result.returncode == 0:
            return {
                'fixed': fixed,
                'compile_ok': True,
                'error': None,
                'iterations': iterations
            }

        # Compilation failed - extract errors
        error_output = result.stdout + result.stderr
        errors = _extract_compile_errors(error_output)
        error_msg = error_output[:500]

        if not errors:
            error_msg = "Compilation failed (no specific error extracted)"

        # Pass errors back to LLM for correction
        prompt = f"""You are fixing a Turbo Pascal 7 (TP7) routine for Liero v1.33.

The previous attempt FAILED to compile with fpc -Mtp. Please fix the following compilation errors:

{error_msg}

Function: {fn}
Previous (failed) code:
{fixed}

Fix the syntax errors so it compiles with fpc -Mtp (Turbo Pascal mode).
Preserve the first line (function/procedure declaration) exactly.
Output the routine with 'begin...end;'. No C, no C++ idioms.
Use TP7 Pascal syntax: 'begin', 'end;', no braces, no type casts like (Word).
Types allowed: Byte, Char, Word, Integer, Longint, Boolean, Pointer only.
No 'Result' variable. No 'goto'. No 'Exit(v)'.
A procedure call is a STATEMENT (not ':='). A function call returns a value.
Mem[base] and MemW[base] for memory access (already TP7-compatible).
All 'and'/'or' operators stay as-is (they are TP7-compatible).

Output only the fixed routine with 'begin...end;', no explanations."""

        try:
            result = ollama_gen("qwen2.5-coder:14b-instruct-q4_K_M", prompt, timeout=300)
        except Exception:
            result = ollama_gen("qwen2.5-coder:14b-instruct", prompt, timeout=300)

        if "begin" in result.lower() and "end;" in result.lower():
            begin_idx = result.lower().find("begin")
            end_idx = result.rfind("end;")
            if begin_idx >= 0 and end_idx > begin_idx:
                fixed = result[begin_idx:end_idx + 4].strip()
            else:
                fixed = result.strip()
        else:
            fixed = result.strip()

        if iteration == 0:
            best_fixed = fixed

    return {
        'fixed': best_fixed,
        'compile_ok': False,
        'error': error_msg,
        'iterations': iterations
    }
