"""E4: LoRA-finetune Qwen2.5-Coder-1.5B on OUR asm->Ghidra-C pairs.

Question: does target-specific finetuning beat the purpose-built
llm4decompile (arm A, 6/12) and the general qwen14b (arm B, 5/12) on the
SAME held-out 12 liero-dos functions, judged by the SAME compile gate?

Data: targets/{liero,liero-dos}/{asm,decomp} pairs. The 12 eval functions
(and any same-named pair in the other target) are EXCLUDED from training.
Prompt = asm_baseline.ASM_TO_C_PROMPT (byte-identical to daytime arm B);
target = Ghidra decomp C (loss masked on prompt tokens).

Two LoRA hyperparam configs ("hyperparametrisations"):
  cfgA: r=16  alpha=32  lr=2e-4  3 epochs   (light adapter)
  cfgB: r=64  alpha=128 lr=8e-5  2 epochs   (wide, gentler)

Eval order: base zero-shot -> cfgA -> cfgB, greedy decode, then
extract_c + compile_c, rows -> reports/overnight/e4/results.json.

Run via /tmp/ftvenv/bin/python tools/e4_finetune.py --budget-s N (phase e4).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import asm_baseline as ab  # noqa: E402

OUT = ROOT / "reports" / "overnight" / "e4"
OUT.mkdir(parents=True, exist_ok=True)

import torch  # noqa: E402
from transformers import (  # noqa: E402
    AutoModelForCausalLM, AutoTokenizer)

BASE_MODEL = "Qwen/Qwen2.5-Coder-1.5B"
EVAL_FNS = set(ab.stratified_pick(ROOT / "targets" / "liero-dos",
                                  1 if "--smoke" in sys.argv else 12))
MAX_LEN = 1024
CFG = {"cfgA": dict(r=16, alpha=32, lr=2e-4, epochs=3),
       "cfgB": dict(r=64, alpha=128, lr=8e-5, epochs=2)}


def say(msg: str) -> None:
    print(f"[e4 {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def build_dataset(tok) -> list[dict]:
    """(prompt, target) pairs, eval fns excluded from BOTH targets."""
    pairs = []
    for tgt in ("liero", "liero-dos"):
        root = ROOT / "targets" / tgt
        for s in sorted((root / "asm").glob("FUN_*.s")):
            stem = s.stem
            if stem in EVAL_FNS:            # leakage guard (both targets)
                continue
            cp = root / "decomp" / f"{stem}.c"
            if not cp.exists():
                continue
            prompt = ab.ASM_TO_C_PROMPT.format(asm=s.read_text()[:ab.ASM_CAP])
            target = cp.read_text().strip() + tok.eos_token
            pairs.append({"prompt": prompt, "target": target, "stem": stem,
                          "tgt": tgt})
    say(f"dataset: {len(pairs)} pairs (excluded {len(EVAL_FNS)} eval stems)")
    return pairs


def encode(tok, pair: dict) -> dict:
    p = tok(pair["prompt"], truncation=True, max_length=768,
            add_special_tokens=False)
    t = tok(pair["target"], truncation=True, max_length=256,
            add_special_tokens=False)
    ids = p["input_ids"] + t["input_ids"]
    labels = [-100] * len(p["input_ids"]) + list(t["input_ids"])
    return {"input_ids": ids, "labels": labels}


def batchify(items: list[dict], bs: int) -> list[list[dict]]:
    return [items[i:i + bs] for i in range(0, len(items), bs)]


def pad_batch(tok, batch: list[dict]) -> dict:
    ml = max(len(x["input_ids"]) for x in batch)
    for k in ("input_ids", "labels"):
        pad = tok.pad_token_id if k == "input_ids" else -100
        batch = [{**x, k: x[k] + [pad] * (ml - len(x[k]))} for x in batch]
    return {k: torch.tensor([x[k] for x in batch]) for k in ("input_ids", "labels")}


def train_cfg(name: str, cfg: dict, model, tok, pairs: list[dict],
              budget_s: float, t0: float) -> pathlib.Path | None:
    """One LoRA config; returns adapter dir or None if budget killed it early."""
    from peft import LoraConfig, get_peft_model
    lconf = LoraConfig(
        r=cfg["r"], lora_alpha=cfg["alpha"],
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05, bias="none", task_type="CAUSAL_LM")
    lmodel = get_peft_model(model, lconf)
    lmodel.print_trainable_parameters()
    opt = torch.optim.AdamW(
        [p for p in lmodel.parameters() if p.requires_grad], lr=cfg["lr"])
    items = [encode(tok, p) for p in pairs]
    steps_done = 0
    for epoch in range(cfg["epochs"]):
        order = torch.randperm(len(items))
        batches = batchify([items[i] for i in order], 1)
        for bi, batch in enumerate(batches):
            if time.time() - t0 > budget_s * 0.85:
                say(f"{name}: budget guard at epoch {epoch} step {bi}")
                break
            bt = {k: v.to(model.device)
                  for k, v in pad_batch(tok, batch).items()}
            out = lmodel(input_ids=bt["input_ids"], labels=bt["labels"])
            out.loss.backward()
            torch.nn.utils.clip_grad_norm_(
                [p for p in lmodel.parameters() if p.requires_grad], 1.0)
            opt.step(); opt.zero_grad()
            steps_done += 1
            if bi % 20 == 0:
                say(f"{name} e{epoch} b{bi}/{len(batches)} "
                    f"loss={out.loss.item():.3f}")
        else:
            continue
        break
    adir = OUT / f"lora_{name}"
    lmodel.save_pretrained(str(adir))
    say(f"{name}: saved adapter ({steps_done} steps) -> {adir}")
    return adir if steps_done else None


@torch.no_grad()
def eval_model(model, tag: str, rows: list, tok) -> None:
    """Greedy-decode the 12 eval fns; compile with the daytime gate."""
    have = {(r["cfg"], r["fn"]) for r in rows}
    model.eval()
    for f in sorted(EVAL_FNS):
        if (tag, f) in have:
            continue
        prompt = ab.ASM_TO_C_PROMPT.format(
            asm=(ROOT / "targets" / "liero-dos" / "asm" / f"{f}.s").read_text()
                 [:ab.ASM_CAP])
        t0 = time.time()
        ids = tok(prompt, return_tensors="pt",
                  add_special_tokens=False).input_ids.to(model.device)
        out_ids = model.generate(
            ids, max_new_tokens=1024, do_sample=False,
            pad_token_id=tok.pad_token_id)
        text = tok.decode(out_ids[0][ids.shape[1]:], skip_special_tokens=True)
        code = ab.extract_c(text)
        gdir = OUT / "gen" / tag
        gdir.mkdir(parents=True, exist_ok=True)  # compile_c writes here; no mkdir
        status, err = ab.compile_c(code, gdir, f)
        rows.append({"cfg": tag, "fn": f, "compile": status,
                     "bucket": ab.bucket(err), "error": err[:200],
                     "seconds": round(time.time() - t0, 1), "raw": text})
        (OUT / "results.json").write_text(json.dumps(rows, indent=2))
        say(f"  eval[{tag}] {f}: {status}")


def _rollup(rows: list, tag: str) -> str:
    rs = [r for r in rows if r["cfg"] == tag]
    if not rs:
        return ""
    ok = sum(r["compile"] != "fail" for r in rs)
    st = sum(r["compile"] == "strict" for r in rs)
    return (f"strict {st}/{len(rs)}, "
            f"any-compile {ok}/{len(rs)} ({100*ok//len(rs)}%)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget-s", type=float, default=90 * 60)
    a = ap.parse_args()
    t0 = time.time()
    say(f"loading {BASE_MODEL} (downloads on first run; bf16)...")
    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    tok.pad_token = tok.eos_token or tok.pad_token
    tok.padding_side = "right"
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL, torch_dtype=torch.bfloat16, device_map="cuda:0")
    model.config.use_cache = False
    model.gradient_checkpointing_enable(
        gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    rows_path = OUT / "results.json"
    rows = json.loads(rows_path.read_text()) if rows_path.exists() else []

    say("eval: base zero-shot (control)...")
    eval_model(model, "base", rows, tok)
    del model; torch.cuda.empty_cache()

    pairs = build_dataset(tok)
    from peft import PeftModel
    for name, cfg in CFG.items():
        if time.time() - t0 > a.budget_s * 0.7:
            say(f"budget too low to start {name}; skipping")
            break
        # fresh base per config so cfgB isn't warm-started from cfgA
        base = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL, torch_dtype=torch.bfloat16, device_map="cuda:0")
        base.config.use_cache = False
        base.gradient_checkpointing_enable(
            gradient_checkpointing_kwargs={"use_reentrant": False})
        base.enable_input_require_grads()
        adir = train_cfg(name, cfg, base, tok, pairs, a.budget_s, t0)
        del base; torch.cuda.empty_cache()
        if adir is None:
            say(f"{name}: no steps ran; skipping eval")
            continue
        em = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL, torch_dtype=torch.bfloat16, device_map="cuda:0")
        em = PeftModel.from_pretrained(em, str(adir))
        eval_model(em, name, rows, tok)
        del em; torch.cuda.empty_cache()

    md = ["# E4 LoRA finetune (Qwen2.5-Coder-1.5B -> asm->C)\n",
          "daytime reference: A (llm4decompile) any-compile 6/12, "
          "B (qwen14b) 5/12\n"]
    for tag in ("base", *CFG):
        r = _rollup(rows, tag)
        if r:
            md.append(f"- {tag}: {r}")
    (OUT / "summary.md").write_text("\n".join(md) + "\n")
    say("E4 done")
    return 0


if __name__ == "__main__":
    sys.exit(main())

