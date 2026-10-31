"""Local inference with an activated PEFT adapter."""

from __future__ import annotations

import pathlib
from typing import Any

_CACHE: dict[tuple[str, str], tuple[Any, Any, Any]] = {}


def generate_with_adapter(
    prompt: str,
    base_model_path: str,
    adapter_path: str,
    max_new_tokens: int = 768,
    temperature: float = 0.0,
) -> str:
    key = (str(pathlib.Path(base_model_path).resolve()),
           str(pathlib.Path(adapter_path).resolve()))
    if key not in _CACHE:
        try:
            import torch
            from peft import PeftModel
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "using the trained adapter requires the optional [training] extra"
            ) from exc

        tokenizer = AutoTokenizer.from_pretrained(
            key[0], local_files_only=True
        )
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        model = AutoModelForCausalLM.from_pretrained(
            key[0], local_files_only=True
        )
        model = PeftModel.from_pretrained(
            model, key[1], local_files_only=True
        )
        model.eval()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        _CACHE[key] = (model, tokenizer, torch)

    model, tokenizer, torch = _CACHE[key]
    device = next(model.parameters()).device
    inputs = tokenizer(
        prompt, return_tensors="pt", truncation=True, max_length=4096
    ).to(device)
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
    return tokenizer.decode(generated[0][prompt_tokens:], skip_special_tokens=True)
