# Liero candidate experiment

Candidates are ranked only by sanitizer acceptance and a full-target
compile. Neither result establishes semantic equivalence or source recovery.

- Baseline build passed: **True**
- Functions: FUN_24dd_0582, FUN_24dd_462e, FUN_1000_05a4, FUN_1000_10ec
- Candidate generations: 32

| Model | Prompt profile | Temperature | Accepted | Build pass | Both |
|---|---|---:|---:|---:|---:|
| qwen2.5-coder:14b-instruct-q4_K_M | base-prompt | 0.0 | 2/4 | 3/4 | 1/4 |
| qwen2.5-coder:14b-instruct-q4_K_M | base-prompt | 0.3 | 2/4 | 3/4 | 1/4 |
| qwen2.5-coder:14b-instruct-q4_K_M | learned-context | 0.0 | 2/4 | 3/4 | 1/4 |
| qwen2.5-coder:14b-instruct-q4_K_M | learned-context | 0.3 | 1/4 | 4/4 | 1/4 |
| qwen3:14b | base-prompt | 0.0 | 1/4 | 4/4 | 1/4 |
| qwen3:14b | base-prompt | 0.3 | 0/4 | 4/4 | 0/4 |
| qwen3:14b | learned-context | 0.0 | 0/4 | 4/4 | 0/4 |
| qwen3:14b | learned-context | 0.3 | 0/4 | 4/4 | 0/4 |

## Provisional per-function shortlist

- `FUN_24dd_0582`: `qwen2.5-coder:14b-instruct-q4_K_M`, base-prompt, temperature 0.0; accepted=False, build_passed=True, MLflow run `046dc408d76f4a4594f6a32bad7b1060`.
- `FUN_24dd_462e`: `qwen2.5-coder:14b-instruct-q4_K_M`, base-prompt, temperature 0.3; accepted=True, build_passed=True, MLflow run `791db00d19234e42806f36e8d877e3e0`.
- `FUN_1000_05a4`: `qwen2.5-coder:14b-instruct-q4_K_M`, base-prompt, temperature 0.3; accepted=True, build_passed=False, MLflow run `b297b08447194f1abaa598bda7804cc3`.
- `FUN_1000_10ec`: `qwen2.5-coder:14b-instruct-q4_K_M`, base-prompt, temperature 0.0; accepted=False, build_passed=True, MLflow run `f7a172f537f04207a40cebd049e212ef`.

A shortlist is not a recovery attestation. Review each candidate against
its assembly, ABI, calls, state effects, and data references.
