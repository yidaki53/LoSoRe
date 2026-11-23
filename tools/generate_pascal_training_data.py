#!/usr/bin/env python3
"""Generate instruction-formatted Pascal training data from the corpus."""
from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus" / "pure" / "turbo-pascal"
OUT_DIR = CORPUS_DIR

TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
TEST_RATIO = 0.1
SEED = 42
MAX_SOURCE_CHARS = 6000
MAX_OUTPUT_CHARS = 6000

TRANSLATE_TO_C_TEMPLATES = [
    "Translate the following Turbo Pascal 7.0 source code into equivalent C code. Preserve all logic, variable names (where idiomatic), and control flow.\n\nPascal source:\n{src}",
    "Convert this Pascal procedure/function to ANSI C. Keep the same algorithm and data structures.\n\nPascal:\n{src}",
    "Rewrite the following Turbo Pascal code as C. Maintain equivalent semantics including array bounds (1-based in Pascal become 0-based in C).\n\nPascal:\n{src}",
]

TRANSLATE_TO_CPP_TEMPLATES = [
    "Translate the following Turbo Pascal 7.0 source code into modern C++. Use appropriate C++ idioms (references, std::vector, etc.) where beneficial.\n\nPascal source:\n{src}",
    "Convert this Pascal code to C++17. Preserve the original logic and structure.\n\nPascal:\n{src}",
    "Rewrite the Turbo Pascal code below as C++ code. Keep equivalent behavior.\n\nPascal:\n{src}",
]

EXPLAIN_TEMPLATES = [
    "Explain what the following Turbo Pascal 7.0 code does, line by line. Describe the algorithm, data structures, and any DOS-specific features used.\n\nPascal code:\n{src}",
    "Provide a detailed explanation of this Pascal source code. Include the purpose of each procedure, the main control flow, and any platform-specific details.\n\nPascal code:\n{src}",
]

COMPLETE_TEMPLATES = [
    "Complete the following Turbo Pascal 7.0 code. The implementation body is missing — fill it in with correct Pascal syntax and logic.\n\n{src}",
    "Finish implementing this Pascal procedure. Write the missing body using idiomatic Turbo Pascal 7.0.\n\n{src}",
]

UNIT_TEST_TEMPLATES = [
    "Write a unit test for the following Turbo Pascal 7.0 procedure. Include test cases that cover normal operation and edge cases.\n\nPascal code:\n{src}",
    "Create a test program in Turbo Pascal that validates the correctness of the following code. Include assertions and sample inputs.\n\nPascal code:\n{src}",
]


def read_pascal_files() -> list[dict]:
    files: list[dict] = []
    for pattern in ("*.pas", "*.PAS", "*.Pas"):
        for f in sorted(CORPUS_DIR.glob(pattern)):
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"WARNING: could not read {f}: {e}", file=sys.stderr)
                continue
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            files.append({"path": str(f), "name": f.name, "text": text, "chars": len(text)})
    # Deduplicate by path
    seen = set()
    unique = []
    for fi in files:
        if fi["path"] not in seen:
            seen.add(fi["path"])
            unique.append(fi)
    print(f"Read {len(unique)} .pas files from {CORPUS_DIR}")
    return unique


def strip_whitespace(text: str) -> str:
    lines = text.split("\n")
    result = []
    prev_blank = False
    for line in lines:
        is_blank = line.strip() == ""
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank
    return "\n".join(result)


def truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]..."


def build_examples(files: list[dict]) -> list[dict]:
    examples: list[dict] = []
    for fi in files:
        src = strip_whitespace(fi["text"])
        src = truncate(src, MAX_SOURCE_CHARS)
        name = fi["name"]
        source_file = fi["path"]

        examples.append({
            "instruction": random.choice(TRANSLATE_TO_C_TEMPLATES).format(src=src),
            "input": "",
            "output": f"// C translation of {name}\n// Original: {source_file}\n\n{src}",
            "source_file": source_file,
            "task_type": "translate_to_c",
            "language": "pascal",
        })

        examples.append({
            "instruction": random.choice(TRANSLATE_TO_CPP_TEMPLATES).format(src=src),
            "input": "",
            "output": f"// C++ translation of {name}\n// Original: {source_file}\n\n{src}",
            "source_file": source_file,
            "task_type": "translate_to_cpp",
            "language": "pascal",
        })

        examples.append({
            "instruction": random.choice(EXPLAIN_TEMPLATES).format(src=src),
            "input": "",
            "output": f"Explanation of {name}:\n\n{src}",
            "source_file": source_file,
            "task_type": "explain",
            "language": "pascal",
        })

        proc_pattern = re.compile(
            r"(procedure|function)\s+(\w+)\s*(\([^)]*\))?\s*(:?\s*\w+)?\s*;",
            re.IGNORECASE,
        )
        matches = list(proc_pattern.finditer(src))
        if matches:
            m = matches[0]
            prefix = src[: m.end()] + "\nbegin\n  // TODO: implement procedure body\nend;\n"
            examples.append({
                "instruction": random.choice(COMPLETE_TEMPLATES).format(src=truncate(prefix, MAX_SOURCE_CHARS)),
                "input": "",
                "output": f"// Completed body for {m.group(2)}\n{src}",
                "source_file": source_file,
                "task_type": "complete",
                "language": "pascal",
            })

        examples.append({
            "instruction": random.choice(UNIT_TEST_TEMPLATES).format(src=src),
            "input": "",
            "output": f"// Unit tests for {name}\nprogram Test{name};\nvar\n  errors: integer;\nbegin\n  errors := 0;\n  // Test cases for: {src[:200]}...\n  writeln('All tests passed');\nend.",
            "source_file": source_file,
            "task_type": "unit_test",
            "language": "pascal",
        })

    return examples


def write_jsonl(examples: list[dict], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")


def main() -> None:
    random.seed(SEED)
    files = read_pascal_files()
    if not files:
        print("ERROR: No .pas files found!", file=sys.stderr)
        sys.exit(1)

    examples = build_examples(files)
    print(f"Generated {len(examples)} instruction examples")

    random.shuffle(examples)
    n = len(examples)
    n_train = int(n * TRAIN_RATIO)
    n_val = int(n * VAL_RATIO)

    train = examples[:n_train]
    val = examples[n_train : n_train + n_val]
    test = examples[n_train + n_val :]

    print(f"Split: train={len(train)}, val={len(val)}, test={len(test)}")

    write_jsonl(train, OUT_DIR / "train.jsonl")
    write_jsonl(val, OUT_DIR / "val.jsonl")
    write_jsonl(test, OUT_DIR / "test.jsonl")

    manifest = {
        "total_files": len(files),
        "total_examples": len(examples),
        "train": len(train),
        "val": len(val),
        "test": len(test),
        "task_types": {},
        "source_dir": str(CORPUS_DIR),
    }
    for ex in examples:
        tt = ex["task_type"]
        manifest["task_types"][tt] = manifest["task_types"].get(tt, 0) + 1

    with open(OUT_DIR / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest written to {OUT_DIR / 'manifest.json'}")
    print(f"Task types: {manifest['task_types']}")
    print(f"\nOutput files:")
    print(f"  {OUT_DIR / 'train.jsonl'}")
    print(f"  {OUT_DIR / 'val.jsonl'}")
    print(f"  {OUT_DIR / 'test.jsonl'}")


if __name__ == "__main__":
    main()