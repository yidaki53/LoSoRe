# targets/liero/AGENTS.md

- Quote every path. Treat `"extracted/liero/"` and all `"vendor/"` material as read-only; do not modify or copy evidence into memory stores.
- `"targets/liero/functions.json"` is the 295-function inventory; `"targets/liero/asm/"` and `"targets/liero/decomp/"` are references, not acceptance evidence.
- `"targets/liero/docs/RECONSTRUCTION.md"` is the evidence ledger; `"targets/liero/recovery.json"` tracks review state. Neither is oracle verification.
- `"targets/liero/src/liero.pas"` still ends in an entry stub; do not claim a complete program until callees are attested.
- Only oracle-backed relpaths in `"knowledge/knowledge.json"` count as verified source. `source_recovered` in `recovery.json` is review state only.
- Scoped routine or bytes/visual parity probes promote functions; DAT format round-trip and constructor probes never do. `FUN_24dd_48e1`, `FUN_24dd_4141`, `FUN_24dd_3d68`, `FUN_24dd_455e`, `FUN_249c_0013` and `FUN_24dd_40d6` were promoted only under `routine-trace-parity` after compile, 56/56 training and 56/56 terminal matches each.
- Record unresolved callees, blockers and failed assumptions in target docs before changing strategy.
