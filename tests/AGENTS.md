# tests/AGENTS.md

- Tests pin safety gates: no vacuous PASS, no source promotion from `dat-parity`, and truthful `recovery_results.json`.
- Use `tmp_path`, `monkeypatch`, and in-memory dicts; never copy BYOD bytes, disassembly dumps, traces or candidate bodies into tests.
- When changing verifier return codes, keep `"verify.verify()"` compatibility: only a real oracle failure returns non-zero.
- `"tests/test_recovery_integration.py"` covers Matrix ordering, real Q updates, status promotion policy and empty-frontier behavior. Extend it rather than adding a parallel harness.
- `"tests/test_bootstrap.py"` pins automatic bootstrap promotion gating, stale unverified source replacement with preserved previous body, verified-source conflict refusal, no terminal run after training failure, training-only evaluator scope, closed normalization classifications/renderers and non-promoting oracle refusal.
- Run `python3 -m pytest tests/ -q`; the focused recovery gate is `python3 -m pytest tests/test_recovery_integration.py tests/test_bootstrap.py tests/test_learning.py tests/test_local_trial_inference.py tests/test_oracle.py -q`.
- Local baseline after the 2026-11-22 RTL bridge, routine-oracle promotion, packed-copy bridge and bootstrap-produced routine: `42 failed, 1991 passed, 47 skipped, 1 xfailed`. The failures are pre-existing BYOD/source-tree probes (missing `FUN_24dd_*.inc`, stale sign-source records, legacy sanitizer), not the Matrix/verifier gates; use the focused gate when iterating.
