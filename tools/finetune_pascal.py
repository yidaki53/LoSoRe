#!/usr/bin/env python3
"""Fine-tune Qwen2.5-Coder-1.5B on the Pascal corpus using QLoRA."""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

OUT = ROOT / "reports" / "pascal_finetune"
OUT.mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
log = logging.getLogger("pascal_ft")

import torch  # noqa: E402
from transformers import (  # noqa: E402
    AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig,
    TrainingArguments, Trainer, DataCollatorForLanguageModeling,
)
from peft import (  # noqa: E402
    LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType,
)
from datasets import Dataset  # noqa: E402

BASE_MODEL = "Qwen/Qwen2.5-Coder-1.5B"
CORPUS_DIR = ROOT / "corpus" / "pure" / "turbo-pascal"


def build_prompt(example: dict) -> str:
    parts = []
    if example.get("instruction"):
        parts.append(f"### Instruction:\n{example['instruction']}")
    if example.get("input", "").strip():
        parts.append(f"### Input:\n{example['input']}")
    parts.append(f"### Response:\n{example['output']}")
    return "\n\n".join(parts)


def load_examples(jsonl_path: Path) -> list[dict]:
    examples = []
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                examples.append(json.loads(line))
    return examples


def tokenize_function(examples, tokenizer, max_len: int = 1024):
    # examples is a dict of lists when batched=True
    n = len(examples["instruction"])
    texts = []
    for i in range(n):
        ex = {k: examples[k][i] for k in examples}
        texts.append(build_prompt(ex))
    return tokenizer(
        texts, truncation=True, max_length=max_len,
        padding="max_length", return_tensors="pt",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune Qwen on Pascal corpus")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--max-len", type=int, default=1024)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--load-in-4bit", action="store_true", default=False)
    parser.add_argument("--smoke", action="store_true", help="Smoke test")
    args = parser.parse_args()

    log.info(f"Loading tokenizer from {BASE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    log.info(f"Loading model {BASE_MODEL}")
    model_kwargs = {"trust_remote_code": True,
                    "device_map": "auto" if torch.cuda.is_available() else None}

    if args.load_in_4bit:
        model_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True,
        )

    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, **model_kwargs)

    if args.load_in_4bit:
        model = prepare_model_for_kbit_training(model)

    log.info(f"Applying LoRA (r={args.lora_r}, alpha={args.lora_alpha})")
    lora_config = LoraConfig(
        r=args.lora_r, lora_alpha=args.lora_alpha,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        task_type=TaskType.CAUSAL_LM, lora_dropout=0.05, bias="none",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    log.info("Loading data...")
    train_path = CORPUS_DIR / "train.jsonl"
    val_path = CORPUS_DIR / "val.jsonl"
    test_path = CORPUS_DIR / "test.jsonl"

    train_examples = load_examples(train_path)
    val_examples = load_examples(val_path)

    if args.smoke:
        train_examples = train_examples[:20]
        val_examples = val_examples[:5]
        log.info(f"Smoke test: train={len(train_examples)}, val={len(val_examples)}")

    log.info(f"Train examples: {len(train_examples)}, Val examples: {len(val_examples)}")

    def preprocess(examples):
        return tokenize_function(examples, tokenizer, args.max_len)

    train_dataset = Dataset.from_list(train_examples)
    val_dataset = Dataset.from_list(val_examples)

    train_dataset = train_dataset.map(
        preprocess, batched=True, remove_columns=train_dataset.column_names,
    )
    val_dataset = val_dataset.map(
        preprocess, batched=True, remove_columns=val_dataset.column_names,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )

    train_kwargs = {}
    if hasattr(TrainingArguments, "evaluation_strategy"):
        train_kwargs["evaluation_strategy"] = "steps"
    else:
        train_kwargs["eval_strategy"] = "steps"

    training_args = TrainingArguments(
        output_dir=str(OUT / "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        fp16=torch.cuda.is_available(),
        bf16=False,
        logging_steps=10,
        eval_steps=50,
        save_steps=50,
        warmup_steps=10,
        save_strategy="steps",
        load_best_model_at_end=True,
        report_to="none",
        remove_unused_columns=False,
        push_to_hub=False,
        **train_kwargs,
    )

    trainer = Trainer(
        model=model, args=training_args,
        train_dataset=train_dataset, eval_dataset=val_dataset,
        data_collator=data_collator, processing_class=tokenizer,
    )

    log.info("Starting training...")
    start = time.time()
    trainer.train()
    elapsed = time.time() - start
    log.info(f"Training completed in {elapsed:.1f}s")

    adapter_dir = OUT / "lora_adapter"
    model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(adapter_dir)
    log.info(f"Adapter saved to {adapter_dir}")

    test_examples = load_examples(test_path)
    if args.smoke:
        test_examples = test_examples[:5]
    log.info(f"Test examples: {len(test_examples)}")

    model.eval()
    for i, ex in enumerate(test_examples[:3]):
        prompt = build_prompt({k: v for k, v in ex.items() if k != "output"})
        inputs = tokenizer(prompt, return_tensors="pt",
                           truncation=True, max_length=args.max_len)
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        with torch.no_grad():
            outputs = model.generate(
                **inputs, max_new_tokens=200,
                temperature=0.7, do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
            )
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        log.info(f"\n--- Sample {i+1} ---")
        log.info(f"Prompt: {prompt[:200]}...")
        log.info(f"Generated: {generated[-200:]}")

    log.info("Done!")


if __name__ == "__main__":
    main()