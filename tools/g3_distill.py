"""Night-3 torch worker: distill judge-verified clean C into 1.5B + corpus.

Night-2's F3 verdict: training on Ghidra pseudocode teaches the small model
to mimic junk SHAPE. Tonight's fix: train asm -> judge-verified clean C
(both judges agreed >=4). Then generate the full 294-fn corpus with the
distilled model (only compiling outputs are written; G4 backfills failures
from G1 candidates).

Steps:
  1. dataset = (asm prompt, agreed-real clean C target) for fns whose
     G2 verdict == real, EXCLUDING panel + night-1 stems (eval never train).
  2. LoRA r=16, 5 epochs, seq 1024 (night-1 proven memory profile).
  3. eval on the 60-fn panel -> reports/overnight3/g3/results.json
  4. generate all 294 fns with the distilled model, compile-gate,
     write compiling outputs -> reports/overnight3/g4/results.json
     (rows carry generator="distilled-g3")

Run: /tmp/ftvenv/bin/python tools/g3_distill.py --budget-s N
     --exclude-file PATH --panel a,b,c
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import asm_baseline as ab                      # noqa: E402
from f2_train import load_base, encode, pad_batch, train as f2train  # noqa

OUT = ROOT / "reports" / "overnight3"
TARGET = ROOT / "targets" / "liero-dos"
BASE_MODEL = "Qwen/Qwen2.5-Coder-1.5B"
CFG = dict(lora_epochs=5, lr=2e-4, r=16, alpha=32)


def say(msg: str) -> None:
    print(f"[g3 {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_json(path: pathlib.Path, default):
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def save_json(path: pathlib.Path, rows: list) -> None:
    path.write_text(json.dumps(rows, indent=2))


def build_pairs(tok, exclude: set[str]) -> list[dict]:
    """asm -> agreed-real clean C. Target text = the JUDGED candidate."""
    real = load_json(OUT / "g2" / "real_pairs.json", [])
    g1 = {f'{r["model"]}|{r["fn"]}': r
          for r in load_json(OUT / "g1" / "results.json", [])}
    pairs = []
    for rp in real:
        f = rp["fn"]
        if f in exclude:
            continue
        cand = g1.get(f'{rp.get("model")}|{f}')
        if not cand or not cand.get("code"):
            continue
        pairs.append({
            "prompt": ab.ASM_TO_C_PROMPT.format(
                asm=(TARGET / "asm" / f"{f}.s").read_text()[:ab.ASM_CAP]),
            "target": cand["code"].strip() + tok.eos_token,
            "stem": f})
    say(f"distill dataset: {len(pairs)} verified pairs "
        f"({len(real)} real total, {len(exclude)} stems excluded)")
    return pairs


def generate(model, tok, prompt: str) -> str:
    ids = tok(prompt, return_tensors="pt",
              add_special_tokens=False).input_ids.to(model.device)
    out_ids = model.generate(ids, max_new_tokens=1024, do_sample=False,
                             pad_token_id=tok.pad_token_id)
    return tok.decode(out_ids[0][ids.shape[1]:], skip_special_tokens=True)


@__import__("torch").no_grad()
def run_eval(model, tok, fns: list[str], tag: str, rows: list,
             out_path: pathlib.Path, eval_set: str) -> None:
    have = {(r.get("fn")) for r in rows}
    model.eval()
    for f in fns:
        if f in have:
            continue
        prompt = ab.ASM_TO_C_PROMPT.format(
            asm=(TARGET / "asm" / f"{f}.s").read_text()[:ab.ASM_CAP])
        t0 = time.time()
        text = generate(model, tok, prompt)
        code = ab.extract_c(text)
        gdir = OUT / "gen_distilled"
        gdir.mkdir(parents=True, exist_ok=True)
        status, err = ab.compile_c(code, gdir, f)
        rows.append({"fn": f, "eval_set": eval_set, "compile": status,
                     "bucket": ab.bucket(err), "error": err[:200],
                     "seconds": round(time.time() - t0, 1),
                     "generator": "distilled-g3",
                     "raw": text, "code": code})
        save_json(out_path, rows)
        say(f"  [{tag}] {f}: {status}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget-s", type=float, default=5400)
    ap.add_argument("--exclude-file", required=True)
    ap.add_argument("--panel", default="")
    a = ap.parse_args()
    t0 = time.time()
    (OUT / "g3").mkdir(parents=True, exist_ok=True)
    (OUT / "g4").mkdir(parents=True, exist_ok=True)
    exclude = set(pathlib.Path(a.exclude_file).read_text().split())
    panel = [x for x in a.panel.split(",") if x]
    all_fns = sorted(p.stem for p in (TARGET / "asm").glob("FUN_*.s")
                     if (TARGET / "decomp" / f"{p.stem}.c").exists())

    from peft import PeftModel
    from transformers import AutoTokenizer
    say(f"variant=distill cfg={CFG}")
    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    tok.pad_token = tok.eos_token or tok.pad_token
    tok.padding_side = "right"

    model = load_base()
    pairs = build_pairs(tok, exclude)
    if not pairs:
        say("FATAL: no distill pairs")
        return 1
    adapter = OUT / "g3" / "lora_distilled"
    f2train(model, tok, pairs, CFG, a.budget_s, t0, adapter)
    del model
    __import__("torch").cuda.empty_cache()

    em = load_base()
    em = PeftModel.from_pretrained(em, str(adapter))

    # 60-fn panel eval (hypothesis test vs night-2 F3 junk rate)
    g3_path = OUT / "g3" / "results.json"
    g3_rows = load_json(g3_path, [])
    if panel:
        run_eval(em, tok, panel, "panel", g3_rows, g3_path, "panel")
    ok = sum(r["compile"] != "fail" for r in g3_rows)
    st = sum(r["compile"] == "strict" for r in g3_rows)
    (OUT / "g3" / "summary.md").write_text(
        f"# g3 distilled (r=16, {CFG['lora_epochs']}ep, verified targets)\n"
        f"- panel: strict {st}/{len(g3_rows)}, "
        f"any-compile {ok}/{len(g3_rows)}\n"
        f"- dataset: {len(pairs)} judge-verified pairs\n")

    # full 294-fn corpus (compiling outputs only; G4 backfills the rest)
    g4_path = OUT / "g4" / "results.json"
    g4_rows = load_json(g4_path, [])
    for f in all_fns:
        if time.time() - t0 > a.budget_s * 0.95:
            say("corpus budget guard hit")
            break
        run_eval(em, tok, [f], "corpus", g4_rows, g4_path, "corpus")
    del em
    __import__("torch").cuda.empty_cache()
    say(f"corpus: {len(g4_rows)} compiling distilled outputs")
    say("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())

