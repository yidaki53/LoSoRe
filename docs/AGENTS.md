# docs/AGENTS.md

- `"RECOVERY_STATUS.md"` summarizes the generated `"recovery_results.json"`; regenerate the JSON with `python3 run_verification.py` instead of hand-editing status.
- Never report DAT format parity as 295 verified functions. It checks one scoped format oracle and cannot promote source. The seven `routine-trace-parity` promotions (`FUN_24dd_48e1`, `FUN_24dd_4141`, `FUN_24dd_3d68`, `FUN_24dd_455e`, `FUN_249c_0013`, `FUN_24dd_40d6`, `FUN_24dd_04dc`) are routine-level only; do not inflate them to all inputs or full-game parity.
- Distinguish reviewed, partial, compiled-candidate, oracle-verified and in-progress states explicitly.
- Success is behavioral/visual parity under DOSBox plus scoped witnesses, not byte-exact cloning.
- Keep historical trials, failures and strategy changes in `"docs/RECOVERY_METHOD.md"` and `"targets/liero/docs/RECONSTRUCTION.md"` with dates and exact commands.
- Update docs after measured milestones, not after every file edit; preserve older failures when strategies change.
