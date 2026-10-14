"""Night-2 torch worker: two finetune variants, seq 2048.

  f1 = cfgA-long: reload night-1's lora_cfgA (reports/overnight/e4/lora_cfgA,
      READ-ONLY), continue training 4 epochs at seq 2048. Tests whether
      night-1's seq-1024 truncation cost real accuracy.
  f2 = cfgC-wide: fresh LoRA r=32/alpha=64, lr 1e-4, 3 epochs, seq 1024.
      Width test at proven-safe memory (r=64/seq-2048 OOMs on 12GB).

Both: Qwen2.5-Coder-1.5B bf16, LoRA on all attn+mlp projections, batch 1,
non-reentrant checkpointing + enable_input_require_grads (night-1 OOM fix),
train pairs exclude BOTH eval sets from BOTH targets (anti-leakage).

Eval: greedy decode on night-1's 12 fns (continuity) + 60-fn panel, same
compile gate as daytime. Rows -> reports/overnight2/{variant}/results.json.

Run via /tmp/ftvenv/bin/python tools/f2_train.py --variant f1 --budget-s N
  --exclude-file PATH --eval-f1 a,b,c --eval-panel d,e,f
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

OUT = ROOT / "reports" / "overnight2"
NIGHT1_ADAPTER = ROOT / "reports" / "overnight" / "e4" / "lora_cfgA"

import torch  # noqa: E402
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402

BASE_MODEL = "Qwen/Qwen2.5-Coder-1.5B"
SEQ = 1024
PROMPT_CAP, TARGET_CAP = 768, 256

CFGS = {"f1": dict(lora_epochs=5, lr=2e-4, r=16, alpha=32),
        "f2": dict(lora_epochs=4, lr=1e-4, r=32, alpha=64)}


def say(msg: str) -> None:
    print(f"[f2 {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_base():
    m = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL, torch_dtype=torch.bfloat16, device_map="cuda:0")
    m.config.use_cache = False
    m.gradient_checkpointing_enable(
        gradient_checkpointing_kwargs={"use_reentrant": False})
    m.enable_input_require_grads()
    return m


def build_pairs(tok, exclude: set[str]) -> list[dict]:
    pairs = []
    for tgt in ("liero", "liero-dos"):
        root = ROOT / "targets" / tgt
        for s in sorted((root / "asm").glob("FUN_*.s")):
            if s.stem in exclude:
                continue
            cp = root / "decomp" / f"{s.stem}.c"
            if not cp.exists():
                continue
            pairs.append({
                "prompt": ab.ASM_TO_C_PROMPT.format(
                    asm=s.read_text()[:ab.ASM_CAP]),
                "target": cp.read_text().strip() + tok.eos_token,
                "stem": s.stem, "tgt": tgt})
    say(f"dataset: {len(pairs)} pairs ({len(exclude)} stems excluded)")
    return pairs


def encode(tok, pair: dict) -> dict:
    p = tok(pair["prompt"], truncation=True, max_length=PROMPT_CAP,
            add_special_tokens=False)
    t = tok(pair["target"], truncation=True, max_length=TARGET_CAP,
            add_special_tokens=False)
    ids = p["input_ids"] + t["input_ids"]
    labels = [-100] * len(p["input_ids"]) + list(t["input_ids"])
    return {"input_ids": ids, "labels": labels}


def pad_batch(tok, batch: list[dict]) -> dict:
    ml = max(len(x["input_ids"]) for x in batch)
    out = {}
    for k in ("input_ids", "labels"):
        pad = tok.pad_token_id if k == "input_ids" else -100
        out[k] = torch.tensor(
            [x[k] + [pad] * (ml - len(x[k])) for x in batch])
    return out


def train(model, tok, pairs: list[dict], cfg: dict, budget_s: float,
          t0: float, adapter_dir: pathlib.Path) -> int:
    from peft import LoraConfig, PeftModel, get_peft_model
    if not isinstance(model, PeftModel):
        lconf = LoraConfig(
            r=cfg["r"], lora_alpha=cfg["alpha"],
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                            "gate_proj", "up_proj", "down_proj"],
            lora_dropout=0.05, bias="none", task_type="CAUSAL_LM")
        model = get_peft_model(model, lconf)
    # peft freezes LoRA params on load: continuation (f1) needs grads back
    for n, prm in model.named_parameters():
        prm.requires_grad = "lora_" in n
    model.print_trainable_parameters()
    opt = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad], lr=cfg["lr"])
    items = [encode(tok, p) for p in pairs]
    steps = 0
    for epoch in range(cfg["lora_epochs"]):
        order = torch.randperm(len(items))
        batches = [items[i] for i in order]
        for bi in range(len(batches)):
            if time.time() - t0 > budget_s * 0.85:
                say(f"budget guard: epoch {epoch} step {bi}")
                break
            bt = {k: v.to(model.device)
                  for k, v in pad_batch(tok, [batches[bi]]).items()}
            loss = model(input_ids=bt["input_ids"],
                         labels=bt["labels"]).loss
            loss.backward()
            torch.nn.utils.clip_grad_norm_(
                [p for p in model.parameters() if p.requires_grad], 1.0)
            opt.step(); opt.zero_grad()
            steps += 1
            if bi % 40 == 0:
                say(f"e{epoch} b{bi}/{len(batches)} loss={loss.item():.3f}")
        else:
            continue
        break
    model.save_pretrained(str(adapter_dir))
    say(f"saved adapter ({steps} steps) -> {adapter_dir}")
    return steps


@torch.no_grad()
def evaluate(model, tag: str, fns: list[str], eval_set: str,
             rows: list, tok) -> None:
    have = {(r["cfg"], r["fn"]) for r in rows}
    model.eval()
    for f in fns:
        if (tag, f) in have:
            continue
        prompt = ab.ASM_TO_C_PROMPT.format(
            asm=(ROOT / "targets" / "liero-dos" / "asm"
                 / f"{f}.s").read_text()[:ab.ASM_CAP])
        t0 = time.time()
        ids = tok(prompt, return_tensors="pt",
                  add_special_tokens=False).input_ids.to(model.device)
        out_ids = model.generate(ids, max_new_tokens=1024, do_sample=False,
                                 pad_token_id=tok.pad_token_id)
        text = tok.decode(out_ids[0][ids.shape[1]:], skip_special_tokens=True)
        code = ab.extract_c(text)
        gdir = OUT / f"gen_{tag}"
        gdir.mkdir(parents=True, exist_ok=True)   # compile_c needs the dir
        status, err = ab.compile_c(code, gdir, f)
        rows.append({"cfg": tag, "fn": f, "eval_set": eval_set,
                     "compile": status, "bucket": ab.bucket(err),
                     "error": err[:200], "seconds": round(time.time()-t0, 1),
                     "raw": text, "code": code})
        (OUT / variant_dir / "results.json").write_text(json.dumps(rows, indent=2))
        say(f"  eval[{tag}/{eval_set}] {f}: {status}")


def rollup(rows: list, tag: str) -> list[str]:
    out = []
    for es in ("n1", "panel"):
        rs = [r for r in rows if r["cfg"] == tag and r["eval_set"] == es]
        if not rs:
            continue
        ok = sum(r["compile"] != "fail" for r in rs)
        st = sum(r["compile"] == "strict" for r in rs)
        out.append(f"- {tag}/{es}: strict {st}/{len(rs)}, "
                   f"any-compile {ok}/{len(rs)} ({100*ok//len(rs)}%)")
    return out


def main() -> int:
    global variant_dir
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True, choices=["f1", "f2"])
    ap.add_argument("--budget-s", type=float, default=9000)
    ap.add_argument("--exclude-file", required=True)
    ap.add_argument("--eval-f1", default="")
    ap.add_argument("--eval-panel", default="")
    a = ap.parse_args()
    t0 = time.time()
    variant_dir = a.variant
    (OUT / a.variant).mkdir(parents=True, exist_ok=True)
    exclude = set(a.exclude_file and
                  pathlib.Path(a.exclude_file).read_text().split()) or set()
    eval_n1 = [x for x in a.eval_f1.split(",") if x]
    eval_panel = [x for x in a.eval_panel.split(",") if x]
    cfg = CFGS[a.variant]

    say(f"variant={a.variant} cfg={cfg} seq={SEQ}")
    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    tok.pad_token = tok.eos_token or tok.pad_token
    tok.padding_side = "right"

    from peft import PeftModel
    model = load_base()
    if a.variant == "f1":
        say(f"reloading night-1 adapter {NIGHT1_ADAPTER}")
        model = PeftModel.from_pretrained(model, str(NIGHT1_ADAPTER))
    adapter_dir = OUT / a.variant / f"lora_{a.variant}"
    rows_path = OUT / a.variant / "results.json"
    rows = json.loads(rows_path.read_text()) if rows_path.exists() else []

    train(model, tok, build_pairs(tok, exclude), cfg, a.budget_s, t0,
          adapter_dir)
    del model; torch.cuda.empty_cache()

    em = load_base()
    em = PeftModel.from_pretrained(em, str(adapter_dir))
    tag = "cfgA2" if a.variant == "f1" else "cfgC"
    if eval_n1:
        evaluate(em, tag, eval_n1, "n1", rows, tok)
    if eval_panel:
        evaluate(em, tag, eval_panel, "panel", rows, tok)
    del em; torch.cuda.empty_cache()

    md = [f"# {a.variant} ({tag}) seq={SEQ} cfg={cfg}\n"] + rollup(rows, tag)
    (OUT / a.variant / "summary.md").write_text("\n".join(md) + "\n")
    say("done")
    return 0


variant_dir = "f1"

if __name__ == "__main__":
    sys.exit(main())

