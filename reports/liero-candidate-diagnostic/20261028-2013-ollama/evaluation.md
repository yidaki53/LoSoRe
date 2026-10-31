# Liero pilot candidate evaluation

Date: 2026-10-28  
Routine: `FUN_24dd_0582`  
Model: `qwen2.5-coder:14b-instruct-q4_K_M`  
Prompt profile: `base-prompt`; temperature `0.0`; maximum completion `768` tokens  
Oracle: none; this is a candidate/sanitizer review only.

## Captured result

The raw completion is preserved in `completion.txt`, the full request prompt in
`prompt.txt`, and the Ollama response envelope in `response.json`. The sanitizer
returned `unsupported-assembly-artifact`; its decision and hashes are in
`capture.json`. The completion is a Pascal wrapper containing inline assembly:

```pascal
procedure FUN_24dd_0582;
begin
  asm
    MOV AX, 0x576
    JMP 0x2000:53bb
  end;
end;
```

The candidate was captured with `--diagnostic-only`; no target source was
written or compiled.

## Initial review

The staged listing is five bytes and contains exactly two instructions:

```text
24dd:0582  MOV AX,0x576
24dd:0585  JMP 0x2000:53bb
```

At this stage, the target did not appear as a separate entry in
`functions.json`, so its behavior was unresolved. The decompiler's
six-word-copy description and the previous Pascal implementation were not
enough to explain the listed transfer.

## Raw-binary resolution

The executable hash matches the census baseline. Using the census's inferred
load segment `0x1000`, `FUN_24dd_0582` maps to image offset `0x15352` and file
offset `0x16ac2`. GNU `objdump` in 16-bit mode decodes the bytes there as
`MOV AX,0x0576; JMP short 0x253bb` (raw bytes `b8 76 05 eb 64`).

The target address maps to image offset `0x153bb`, which is three bytes into
the known `FUN_24dd_05e8` entry at image offset `0x153b8`. That function loads
`AX=0x05dc` and falls through to the same body. The body saves DS, loads DS
from CS, exchanges AX/SI, copies six words with `REP MOVSW`, subtracts 12 from
DI to restore it, exchanges AX/SI back, restores DS, and returns. Therefore
the `$0576` thunk is a shared-code-entry variant, not a missing function or an
unclassified-range destination.

The host models for `FUN_24dd_0582` and `FUN_24dd_05e8` now share a
code-segment-to-ES copy helper. Focused assertions cover memory, preserved
registers, CX, direction flag, and the modeled carry/zero effects. Processor
flags beyond those represented by the harness and execution against the
original binary remain unverified; both recovery ledger entries stay
`in_progress`.

The sanitizer decision remains correct: the captured candidate is still an
inline-assembly wrapper, not a recovered Pascal implementation. The diagnosis
now supplies a safe behavior model without weakening the sanitizer.

## Endpoint note

Two initial CLI attempts omitted `--endpoint` and returned an empty completion:
without an endpoint, `draft.py` fell through to the optional `llm` CLI, which
is not installed here. Supplying the local Ollama endpoint produced the
captured completion. `engine/draft.py` now resolves an omitted endpoint from
`LSR_LLM_ENDPOINT` or defaults to `http://localhost:11434`, matching the
documented local-first behavior.
