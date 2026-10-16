# Lost-Source Revival Factory
BYOD binary -> detect -> disasm -> same-language drafts -> verify loop -> compilable `targets/<slug>/`.
Any program with lost source: games, applications, firmware, drivers. Nothing counts as decompiled until an oracle passes.

## Same-language policy
The rebuild is **always written in the language the original was written in** (Turbo Pascal 7 for the Liero pilot). Detection (`tools/provenance.py` -> `config/toolchain.yaml`, with confidence) is the gate: `engine/draft.py` refuses to emit until the language is known, then emits that language. Porting verified source to a modern, more maintainable language is a **separate, later project** that consumes this project's output — it is explicitly out of scope here.

## Playable-parity MVP
`make build TARGET=liero` compiles the same-language Pascal program (Free Pascal `-Mtp` proxy in the `rev:dos-tp7` Docker image; DOSBox available for behavioral runs). `make verify TARGET=liero --oracle dat-parity` runs a **real** format oracle (DAT parse->serialize round-trip + fixture selftest). An empty oracle gate reports **NOT verified**, never a vacuous PASS.

Own code: MIT (see LICENSE). No vendor bytes committed. `extracted/` gitignored.
Disc-gated tests skip-and-pass in CI.

## Quickstart
```sh
make init && make test        # green with no target data
python3 tools/new_target.py --slug liero --kind game  # scaffold targets/liero
# drop a legally-owned copy in extracted/liero/, then:
make pipeline TARGET=liero    # provenance -> ingest -> learn -> draft -> verify(dat-parity)
make build TARGET=liero       # compile the same-language program (Docker FPC proxy)
make report                   # per-target + learning stats
```
`make pipeline` = `provenance` (detect compiler/language/confidence) -> `ingest`
(Ghidra headless -> asm/+decomp/) -> `learn` (mine toolchain recipe + few-shot
examples into `knowledge/`) -> `draft` (emit the detected language; Pascal for
Liero, decompiler C kept as `//` reference) -> `verify` (dat-parity oracle).

## Learning (target-over-target)
`engine/knowledge.py` + `engine/learn.py` keep a committed store
`knowledge/knowledge.json`. Each learned target adds, per (compiler, platform)
toolchain: calling conventions, image base, instruction idioms, and verified
asm->C **few-shot examples** (gated on detection confidence). The NEXT target
with the same toolchain inherits them (draft.py injects them into LLM prompts;
verify.py records oracle passes). So the factory gets better at a given compiler
over time instead of starting cold.

## Layout
`targets/<slug>/{src,include,asm,config,tools,docs}/ engine/ compilers/ reports/ tests/ knowledge/`

## Oracles (strongest first)
byte-exact > relocation-aware > round-trip .bin->src->.bin > format/trace parity.
`dat-parity` (real today): DAT parse->serialize round-trip + fixture selftest.
See `engine/verify.py` and `docs/ORACLES.md`.

## Canon
sm64, isledecomp/isle (MSVC4.2+ReproBit), adonis-singh/re4, sm64ds crackloop, open-spyro+maspsx, Francesco149/openrecet, pathologic_re. Full citations: ../EPIC3_ABANDONWARE_REVIVAL_PLAN.md
