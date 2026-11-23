# .github/AGENTS.md

- CI runs `make lint`, `make typecheck`, pytest, then regenerates `"recovery_results.json"` and asserts no false source verification.
- `ACTIVE_FILES` in the Makefile is the enforced static gate scope. Extend it when new recovery/status code becomes stable; do not weaken checks with `|| true`.
- `dev` dependencies in `"pyproject.toml"` include `pytest`, `ruff` and `mypy`; keep CI aligned with them.
- Any change to verifier promotion rules must update `"tests/test_oracle.py"`, `"tests/test_recovery_integration.py"` and the CI status assertion together.
