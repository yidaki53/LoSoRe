# Liero candidate experiment

A candidate build is attempted only for a sanitizer-accepted draft that
changes the original routine. Build passes do not establish semantic
equivalence or source recovery.

- Baseline build passed: **True**
- Functions: FUN_1000_05a4
- Candidate generations: 1

| Model | Prompt profile | Temperature | Accepted | Changed | Build attempted | Candidate build pass | Both |
|---|---|---:|---:|---:|---:|---:|---:|
| qwen2.5-coder:14b-instruct-q4_K_M | base-prompt | 0.3 | 1/1 | 1/1 | 1/1 | 0/1 | 0/1 |

## Provisional per-function shortlist

- `FUN_1000_05a4`: `qwen2.5-coder:14b-instruct-q4_K_M`, base-prompt, temperature 0.3; accepted=True, candidate_build_status=failed, MLflow run `c3ed44199b3d47cb8b113353ea781a02`.

A shortlist is not a recovery attestation. Review each candidate against
its assembly, ABI, calls, state effects, and data references.
