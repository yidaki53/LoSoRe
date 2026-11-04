"""Local inference with an activated PEFT adapter."""

from __future__ import annotations

import gc
import pathlib
from typing import Any

_CACHE: dict[tuple[str, str, bool], tuple[Any, Any, Any]] = {}


def generate_with_adapter(
    prompt: str,
    base_model_path: str,
    adapter_path: str,
    max_new_tokens: int = 768,
    temperature: float = 0.0,
    *,
    quantized: bool = False,
) -> str:
    key = (
        str(pathlib.Path(base_model_path).resolve()),
        str(pathlib.Path(adapter_path).resolve()) if adapter_path else "",
        quantized,
    )
    if key not in _CACHE:
        try:
            import torch
            from peft import PeftModel
            from transformers import (
                AutoModelForCausalLM,
                AutoTokenizer,
                BitsAndBytesConfig,
            )
        except ImportError as exc:
            raise RuntimeError(
                "using the trained adapter requires the optional [training] extra"
            ) from exc
        if quantized and _CACHE:
            _CACHE.clear()
            gc.collect()
            torch.cuda.empty_cache()

        tokenizer = AutoTokenizer.from_pretrained(key[0], local_files_only=True)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        options = {}
        if quantized:
            if not torch.cuda.is_available():
                raise RuntimeError("quantized adapter inference requires CUDA")
            options = {
                "device_map": {"": 0},
                "quantization_config": BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_compute_dtype=torch.bfloat16,
                ),
            }
        model = AutoModelForCausalLM.from_pretrained(
            key[0], local_files_only=True, **options
        )
        if adapter_path:
            model = PeftModel.from_pretrained(model, key[1], local_files_only=True)
        model.eval()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if not quantized:
            model.to(device)
        _CACHE[key] = (model, tokenizer, torch)

    model, tokenizer, torch = _CACHE[key]
    device = next(model.parameters()).device
    if quantized:
        prompt = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=False,
            add_generation_prompt=True,
        )
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    if (
        inputs["input_ids"].shape[1] + max_new_tokens
        > model.config.max_position_embeddings
    ):
        raise ValueError("prompt and output budget exceed model context")
    generation_options = {
        "max_new_tokens": max_new_tokens,
        "do_sample": temperature > 0.0,
        "pad_token_id": tokenizer.pad_token_id or tokenizer.eos_token_id,
    }
    if temperature > 0.0:
        generation_options["temperature"] = temperature
    with torch.inference_mode():
        generated = model.generate(**inputs, **generation_options)
    prompt_tokens = inputs["input_ids"].shape[1]
    completion = generated[0][prompt_tokens:]
    if (
        len(completion) >= max_new_tokens
        and int(completion[-1]) != tokenizer.eos_token_id
    ):
        raise ValueError(
            "model output exhausted token budget without EOS; raw completion:\n"
            + tokenizer.decode(completion, skip_special_tokens=True)
        )
    return tokenizer.decode(completion, skip_special_tokens=True)
