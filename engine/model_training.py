"""Labeled cross-project corpus export and local PEFT/LoRA fine-tuning."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import sys
from datetime import UTC, datetime
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import knowledge

DEFAULT_THRESHOLD = 64
STATE_PATH = pathlib.Path(".lsr/training_state.json")
ADAPTER_ROOT = pathlib.Path(".lsr/adapters")


def _read_yaml_value(path: pathlib.Path, key: str, default: str = "unknown") -> str:
    if not path.exists():
        return default
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip() or default
    return default


def toolchain_for_target(target: str) -> tuple[str, str, str]:
    config = pathlib.Path("targets") / target / "config"
    compiler = _read_yaml_value(
        config / "toolchain.yaml", "compiler",
        _read_yaml_value(config / "target.yaml", "compiler"),
    )
    platform = _read_yaml_value(
        config / "toolchain.yaml", "platform",
        _read_yaml_value(config / "target.yaml", "platform"),
    )
    language = _read_yaml_value(
        config / "toolchain.yaml", "language",
        _read_yaml_value(config / "target.yaml", "language"),
    ).lower()
    return knowledge.compiler_key(compiler, platform), compiler, language


def pair_fingerprint(example: dict[str, Any]) -> str:
    content = "\0".join(
        (example.get("asm", ""), example.get("pascal", ""))
    )
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def eligible_examples(
    data: dict[str, Any], toolchain: str
) -> list[dict[str, Any]]:
    """Return unique, verified Pascal pairs; reject legacy and placeholder data."""
    examples = []
    seen_pairs: set[str] = set()
    for example in data.get("verified_pascal_examples", {}).get(toolchain, []):
        pascal = example.get("pascal", "")
        if (example.get("verification_status") != "verified"
                or example.get("language") != "pascal"
                or not example.get("oracle")
                or not example.get("target")
                or not example.get("asm")
                or not re.search(
                    r"(?im)^\s*(procedure|function)\s+[A-Za-z_]\w*", pascal
                )
                or re.search(r"\bTODO\b|UNMATCHED", pascal, re.IGNORECASE)):
            continue
        fingerprint = pair_fingerprint(example)
        if fingerprint in seen_pairs:
            continue
        seen_pairs.add(fingerprint)
        examples.append({
            **example,
            "task": "assembly_to_pascal",
            "completion": pascal,
            "trust_status": "oracle-verified",
            "source_type": "verified-pascal",
            "pair_fingerprint": fingerprint,
        })
    return sorted(examples, key=lambda item: (
        item.get("target", ""), item.get("fn", "")
    ))


def _is_legacy_c_pair(fn: str, asm: str, completion: str) -> bool:
    if len(asm.strip()) < 20 or len(completion.strip()) < 60:
        return False
    if re.search(
        r"halt_baddata|bad instruction|truncating control flow",
        completion,
        re.IGNORECASE,
    ):
        return False
    return (
        re.search(rf"\b{re.escape(fn)}\s*\(", completion) is not None
        and "{" in completion
        and "}" in completion
    )


def legacy_assembly_examples(
    data: dict[str, Any],
    toolchain: str,
    targets_root: pathlib.Path = pathlib.Path("targets"),
    max_per_target: int = 32,
) -> list[dict[str, Any]]:
    """Collect noisy assembly-to-C pairs without treating them as verified source."""
    candidates: dict[tuple[str, str], dict[str, Any]] = {}
    for example in data.get("examples", {}).get(toolchain, []):
        target = example.get("target", "")
        fn = example.get("fn", "")
        asm = example.get("asm") or example.get("asm_head", "")
        completion = example.get("c", "")
        if (target and fn and
                _is_legacy_c_pair(fn, asm, completion)):
            candidates[(target, fn)] = {
                "target": target,
                "fn": fn,
                "compiler": example.get("compiler", toolchain),
                "platform": example.get("platform", "dos"),
                "asm": asm,
                "completion": completion.strip(),
                "oracle": None,
                "task": "assembly_to_c",
                "trust_status": "legacy-unverified",
                "source_type": "legacy-knowledge",
            }

    for target_root in targets_root.iterdir() if targets_root.exists() else []:
        if not target_root.is_dir():
            continue
        config = target_root / "config"
        compiler = _read_yaml_value(
            config / "toolchain.yaml",
            "compiler",
            _read_yaml_value(config / "target.yaml", "compiler"),
        )
        platform = _read_yaml_value(
            config / "toolchain.yaml",
            "platform",
            _read_yaml_value(config / "target.yaml", "platform"),
        )
        if knowledge.compiler_key(compiler, platform) != toolchain:
            continue
        asm_dir = target_root / "asm"
        decomp_dir = target_root / "decomp"
        if not asm_dir.is_dir() or not decomp_dir.is_dir():
            continue
        for asm_path in asm_dir.glob("*.s"):
            decomp_path = decomp_dir / f"{asm_path.stem}.c"
            if not decomp_path.is_file():
                continue
            asm = asm_path.read_text(errors="replace")
            completion = decomp_path.read_text(errors="replace").strip()
            if not _is_legacy_c_pair(asm_path.stem, asm, completion):
                continue
            previous = candidates.get((target_root.name, asm_path.stem))
            sources = ["ghidra-decompiler"]
            if previous:
                sources.insert(0, previous["source_type"])
            candidates[(target_root.name, asm_path.stem)] = {
                "target": target_root.name,
                "fn": asm_path.stem,
                "compiler": compiler,
                "platform": platform,
                "asm": asm,
                "completion": completion,
                "oracle": None,
                "task": "assembly_to_c",
                "trust_status": "legacy-unverified",
                "source_type": "+".join(sources),
            }

    unique_pairs: dict[str, dict[str, Any]] = {}
    for example in sorted(
        candidates.values(), key=lambda item: (item["target"], item["fn"])
    ):
        fingerprint = hashlib.sha256(
            (example["asm"] + "\0" + example["completion"]).encode("utf-8")
        ).hexdigest()
        example["pair_fingerprint"] = fingerprint
        unique_pairs.setdefault(fingerprint, example)

    by_target: dict[str, list[dict[str, Any]]] = {}
    for example in unique_pairs.values():
        by_target.setdefault(example["target"], []).append(example)

    selected = []
    for target, examples in sorted(by_target.items()):
        examples.sort(key=lambda item: (
            0 if "legacy-knowledge" in item["source_type"] else 1,
            item["pair_fingerprint"],
        ))
        selected.extend(examples[:max_per_target])
    return selected


def training_examples(
    data: dict[str, Any],
    toolchain: str,
    targets_root: pathlib.Path = pathlib.Path("targets"),
    max_legacy_per_target: int = 32,
) -> list[dict[str, Any]]:
    """Combine oracle-verified Pascal with separately labeled legacy C pairs."""
    return (
        eligible_examples(data, toolchain)
        + legacy_assembly_examples(
            data, toolchain, targets_root, max_per_target=max_legacy_per_target
        )
    )


def format_training_prompt(example: dict[str, Any]) -> str:
    if example.get("task") == "assembly_to_c":
        return (
            "Reconstruct a Ghidra-style C pseudocode interpretation of this "
            "16-bit DOS assembly routine. This is noisy, unverified legacy "
            "decompiler supervision, not ground-truth original source. "
            "Preserve the visible control flow and avoid inventing behavior. "
            "Output only the C function.\n"
            f"Toolchain: {example.get('compiler', 'unknown')} / "
            f"{example.get('platform', 'unknown')}\n"
            f"Function: {example.get('fn', 'unknown')}\n"
            f"Raw assembly:\n{example['asm']}\n"
        )
    decomp = example.get("decomp_c", "").strip()
    optional_decomp = (
        f"\nDecompiler pseudocode (lossy reference, not ground truth):\n{decomp}\n"
        if decomp else ""
    )
    return (
        "Reconstruct this verified original Turbo Pascal function. "
        "Treat raw assembly as authoritative; use decompiler pseudocode only "
        "as a potentially lossy clue. Preserve 16-bit arithmetic, control "
        "flow, calling convention, and memory semantics. Output only the "
        "single Turbo Pascal routine.\n"
        f"Toolchain: {example.get('compiler', 'unknown')} / "
        f"{example.get('platform', 'unknown')}\n"
        f"Calling convention: {example.get('calling_convention') or 'unknown'}\n"
        f"Function: {example.get('fn', 'unknown')}\n"
        f"Raw assembly:\n{example['asm']}\n"
        f"{optional_decomp}"
        "Verified with oracle: " + example["oracle"] + "\n"
    )


def training_record(example: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": example.get("example_id") or example.get("pair_fingerprint")
        or hashlib.sha256(
            (example.get("asm", "") + "\0" + example.get("completion", "")).encode(
                "utf-8"
            )
        ).hexdigest(),
        "target": example["target"],
        "toolchain": example.get("compiler", "unknown"),
        "task": example.get("task", "assembly_to_pascal"),
        "source_type": example.get("source_type", "verified-pascal"),
        "trust_status": example.get("trust_status", "oracle-verified"),
        "oracle": example.get("oracle"),
        "prompt": format_training_prompt(example),
        "completion": example.get("completion", example.get("pascal", "")),
    }


def export_dataset(
    data: dict[str, Any],
    toolchain: str,
    output_path: pathlib.Path,
    targets_root: pathlib.Path = pathlib.Path("targets"),
) -> int:
    examples = training_examples(data, toolchain, targets_root)
    if not examples:
        raise ValueError(f"no eligible reverse-engineering examples for {toolchain}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as output:
        for example in examples:
            output.write(json.dumps(training_record(example), ensure_ascii=False))
            output.write("\n")
    temporary_path.replace(output_path)
    return len(examples)


def split_by_target(
    examples: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    targets = sorted({example["target"] for example in examples})
    if len(targets) < 2:
        raise ValueError("fine-tuning requires examples from at least 2 targets")
    validation_target = targets[-1]
    training = [item for item in examples if item["target"] != validation_target]
    validation = [item for item in examples if item["target"] == validation_target]
    if not training or not validation:
        raise ValueError("target-level split produced an empty train or validation set")
    return training, validation, validation_target


def _load_state(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        state = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid model training state at {path}: {exc}") from exc
    if not isinstance(state, dict):
        raise TypeError(f"model training state at {path} must be a JSON object")
    return state


def _save_state(path: pathlib.Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    temporary_path.replace(path)


def active_adapter_for(
    toolchain: str,
    state_path: pathlib.Path = STATE_PATH,
    task: str = "assembly_to_pascal",
) -> dict[str, str] | None:
    record = _load_state(state_path).get("toolchains", {}).get(toolchain)
    if not record:
        return None
    if task not in record.get("trained_tasks", []):
        return None
    adapter_path = pathlib.Path(record.get("adapter_path", ""))
    base_model_path = pathlib.Path(record.get("base_model_path", ""))
    if not adapter_path.is_dir() or not base_model_path.is_dir():
        return None
    return {
        "adapter_path": str(adapter_path),
        "base_model_path": str(base_model_path),
    }


class _PairedDataset:
    """Lazy torch Dataset to keep ordinary installs free of ML dependencies."""

    def __new__(cls, examples, tokenizer, torch, max_length):
        class Dataset(torch.utils.data.Dataset):
            def __len__(self):
                return len(examples)

            def __getitem__(self, index):
                example = examples[index]
                prompt_ids = tokenizer(
                    format_training_prompt(example),
                    add_special_tokens=True,
                    truncation=True,
                    max_length=max_length // 2,
                )["input_ids"]
                completion_ids = tokenizer(
                    example.get("completion", example.get("pascal", "")),
                    add_special_tokens=False,
                )["input_ids"]
                if tokenizer.eos_token_id is not None:
                    completion_ids.append(tokenizer.eos_token_id)
                completion_ids = completion_ids[:max_length - len(prompt_ids)]
                input_ids = prompt_ids + completion_ids
                labels = [-100] * len(prompt_ids) + completion_ids
                return {
                    "input_ids": input_ids,
                    "attention_mask": [1] * len(input_ids),
                    "labels": labels,
                }

        return Dataset()


def train_adapter(
    examples: list[dict[str, Any]],
    base_model_path: pathlib.Path,
    toolchain: str,
    output_root: pathlib.Path = ADAPTER_ROOT,
    max_length: int = 2048,
) -> dict[str, Any]:
    training, validation, validation_target = split_by_target(examples)
    if not base_model_path.is_dir():
        raise ValueError(f"base model path must be a local directory: {base_model_path}")

    try:
        import torch
        from peft import LoraConfig, TaskType, get_peft_model
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            DataCollatorForSeq2Seq,
            Trainer,
            TrainingArguments,
        )
    except ImportError as exc:
        raise RuntimeError(
            "local training requires the optional training dependencies; "
            "install the project's [training] extra"
        ) from exc

    tokenizer = AutoTokenizer.from_pretrained(
        str(base_model_path), local_files_only=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    if tokenizer.pad_token is None:
        raise ValueError("the configured tokenizer must define an EOS or pad token")

    use_bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()
    model = AutoModelForCausalLM.from_pretrained(
        str(base_model_path),
        local_files_only=True,
        **({"torch_dtype": torch.bfloat16} if use_bf16 else {}),
    )
    model.config.pad_token_id = tokenizer.pad_token_id
    if torch.cuda.is_available():
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()
    model = get_peft_model(model, LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules="all-linear",
    ))

    run_name = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = output_root / toolchain / run_name
    output_dir.mkdir(parents=True, exist_ok=False)
    args = TrainingArguments(
        output_dir=str(output_dir / "checkpoints"),
        num_train_epochs=3,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        bf16=use_bf16,
        gradient_checkpointing=torch.cuda.is_available(),
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        logging_steps=10,
        report_to="none",
        remove_unused_columns=False,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=_PairedDataset(training, tokenizer, torch, max_length),
        eval_dataset=_PairedDataset(validation, tokenizer, torch, max_length),
        data_collator=DataCollatorForSeq2Seq(
            tokenizer, model=model, label_pad_token_id=-100
        ),
    )
    baseline = trainer.evaluate(metric_key_prefix="baseline")
    trainer.train()
    final = trainer.evaluate(metric_key_prefix="final")
    adapter_dir = output_dir / "adapter"
    trainer.model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(adapter_dir)
    metrics = {
        "baseline_eval_loss": baseline.get("baseline_loss"),
        "final_eval_loss": final.get("final_loss"),
        "eval_target": validation_target,
        "training_pairs": len(training),
        "validation_pairs": len(validation),
        "task_counts": {
            task: sum(item.get("task") == task for item in examples)
            for task in sorted({item.get("task", "assembly_to_pascal")
                                for item in examples})
        },
    }
    improved = (
        metrics["baseline_eval_loss"] is not None
        and metrics["final_eval_loss"] is not None
        and metrics["final_eval_loss"] < metrics["baseline_eval_loss"]
    )
    manifest = {
        "toolchain": toolchain,
        "base_model_path": str(base_model_path.resolve()),
        "adapter_path": str(adapter_dir.resolve()),
        "created_at": datetime.now(UTC).isoformat(),
        "trained_tasks": sorted({
            item.get("task", "assembly_to_pascal") for item in examples
        }),
        "trust_counts": {
            trust: sum(item.get("trust_status") == trust for item in examples)
            for trust in sorted({item.get("trust_status", "oracle-verified")
                                 for item in examples})
        },
        "metrics": metrics,
        "validation_loss_improved": improved,
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    if not improved:
        raise RuntimeError(
            "adapter was saved but not activated: held-out target loss did not improve"
        )
    return manifest


def train_for_target(
    target: str,
    model_path: str | None,
    threshold: int,
    automatic: bool,
    store_path: pathlib.Path = knowledge.STORE,
    state_path: pathlib.Path = STATE_PATH,
    output_root: pathlib.Path = ADAPTER_ROOT,
) -> int:
    toolchain, compiler, language = toolchain_for_target(target)
    if language != "pascal":
        print(f"[train:{target}] SKIP language is {language}, not Pascal")
        return 0
    if not model_path:
        print(f"[train:{target}] SKIP set LSR_TRAIN_MODEL to a local model directory")
        return 0
    base_model_path = pathlib.Path(model_path).expanduser()
    if not base_model_path.is_dir():
        print(f"[train:{target}] SKIP local model directory not found: {base_model_path}")
        return 0

    data = knowledge.load(store_path)
    examples = training_examples(data, toolchain)
    if not examples:
        print(f"[train:{target}] SKIP no eligible reverse-engineering examples "
              f"for {toolchain}")
        return 0

    if len({item["target"] for item in examples}) < 2:
        print(f"[train:{target}] SKIP target-level validation needs examples "
              "from at least 2 projects")
        return 0

    state = _load_state(state_path)
    toolchain_state = state.get("toolchains", {}).get(toolchain, {})
    attempted = set(toolchain_state.get("attempted_pair_fingerprints", []))
    new_examples = [
        item for item in examples if item["pair_fingerprint"] not in attempted
    ]
    if automatic and len(new_examples) < threshold:
        print(f"[train:{target}] SKIP {len(new_examples)}/{threshold} new "
              "unique training pairs since the previous training attempt")
        return 0

    try:
        manifest = train_adapter(
            examples, base_model_path, toolchain, output_root=output_root
        )
    except (RuntimeError, ValueError) as exc:
        if automatic and "did not improve" in str(exc):
            state.setdefault("toolchains", {}).setdefault(toolchain, {})[
                "attempted_pair_fingerprints"
            ] = sorted(attempted | {item["pair_fingerprint"] for item in new_examples})
            _save_state(state_path, state)
        raise

    record = state.setdefault("toolchains", {}).setdefault(toolchain, {})
    record.update({
        "base_model_path": manifest["base_model_path"],
        "adapter_path": manifest["adapter_path"],
        "trained_tasks": manifest["trained_tasks"],
        "attempted_pair_fingerprints": sorted(
            attempted | {item["pair_fingerprint"] for item in examples}
        ),
        "trained_pair_fingerprints": sorted(
            item["pair_fingerprint"] for item in examples
        ),
        "manifest_path": str(
            pathlib.Path(manifest["adapter_path"]).parent / "manifest.json"
        ),
    })
    _save_state(state_path, state)
    print(f"[train:{target}] saved LoRA adapter for {compiler} "
          f"(tasks: {', '.join(manifest['trained_tasks'])}; "
          f"{len(examples)} pairs; held-out eval loss "
          f"{manifest['metrics']['final_eval_loss']:.4f})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export labeled reverse-engineering pairs or fine-tune a local LoRA adapter"
    )
    parser.add_argument("--target", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--auto", action="store_true",
                      help="fine-tune after the new-pair threshold is reached")
    mode.add_argument("--train", action="store_true",
                      help="fine-tune all eligible examples now")
    mode.add_argument("--export", type=pathlib.Path,
                      help="export labeled training pairs to JSONL")
    parser.add_argument("--model-path", default=os.environ.get("LSR_TRAIN_MODEL"))
    parser.add_argument("--threshold", type=int,
                        default=int(os.environ.get(
                            "LSR_TRAIN_THRESHOLD", DEFAULT_THRESHOLD
                        )))
    parser.add_argument("--store", type=pathlib.Path, default=knowledge.STORE)
    parser.add_argument("--state", type=pathlib.Path, default=STATE_PATH)
    parser.add_argument("--output-root", type=pathlib.Path, default=ADAPTER_ROOT)
    args = parser.parse_args(argv)
    if args.threshold < 1:
        parser.error("--threshold must be positive")

    if args.export:
        toolchain, _, language = toolchain_for_target(args.target)
        if language != "pascal":
            parser.error(f"target {args.target} is not configured as Pascal")
        count = export_dataset(
            knowledge.load(args.store), toolchain, args.export
        )
        print(f"[train:{args.target}] exported {count} labeled pairs to {args.export}")
        return 0

    return train_for_target(
        args.target, args.model_path, args.threshold,
        automatic=args.auto, store_path=args.store,
        state_path=args.state, output_root=args.output_root,
    )


if __name__ == "__main__":
    sys.exit(main())
