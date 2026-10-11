# Lost-Source Revival Factory
BYOD binary -> disasm -> AI C drafts -> verify loop -> compilable `targets/<slug>/`.
Any program with lost source: games, applications, firmware, drivers. Nothing counts as decompiled until an oracle passes.

Own code: MIT (see LICENSE). No vendor bytes committed. `extracted/` gitignored.
Disc-gated tests skip-and-pass in CI.

## Quickstart
```sh
make init && make test        # green with no target data
python3 tools/new_target.py --slug liero --kind game  # scaffold targets/liero
make verify TARGET=liero      # recompile + diff (needs BYOD in extracted/liero/)
```

## Layout
`targets/<slug>/{src,include,asm,config,tools,docs}/ engine/ compilers/ reports/ tests/`

`games/` is a compat symlink -> `targets/` and will be removed; use `targets/` + `TARGET=` going forward.

## Oracles (strongest first)
byte-exact > relocation-aware > round-trip .bin->src->.bin > Frida trace parity.
See `engine/verify.py` and `docs/ORACLES.md`.

## Canon
sm64, isledecomp/isle (MSVC4.2+ReproBit), adonis-singh/re4, sm64ds crackloop, open-spyro+maspsx, Francesco149/openrecet, pathologic_re. Full citations: ../EPIC3_ABANDONWARE_REVIVAL_PLAN.md
