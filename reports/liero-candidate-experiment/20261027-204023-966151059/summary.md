# Liero candidate experiment

Candidates are ranked only by sanitizer acceptance and a full-target
compile. Neither result establishes semantic equivalence or source recovery.

- Baseline build passed: **True**
- Functions: FUN_24dd_0582
- Candidate generations: 48

| Model | Prompt profile | Temperature | Accepted | Build pass | Both |
|---|---|---:|---:|---:|---:|
| deepseek-coder-v2:16b | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| deepseek-coder-v2:16b | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| deepseek-coder-v2:16b | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| deepseek-coder-v2:16b | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| deepseek-coder:6.7b | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| deepseek-coder:6.7b | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| deepseek-coder:6.7b | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| deepseek-coder:6.7b | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| hf.co/mradermacher/llm4decompile-6.7b-GGUF:Q4_K_M | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| hf.co/mradermacher/llm4decompile-6.7b-GGUF:Q4_K_M | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| hf.co/mradermacher/llm4decompile-6.7b-GGUF:Q4_K_M | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| hf.co/mradermacher/llm4decompile-6.7b-GGUF:Q4_K_M | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| hf.co/mradermacher/llm4decompile-9b-v2-GGUF:Q4_K_M | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| hf.co/mradermacher/llm4decompile-9b-v2-GGUF:Q4_K_M | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| hf.co/mradermacher/llm4decompile-9b-v2-GGUF:Q4_K_M | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| hf.co/mradermacher/llm4decompile-9b-v2-GGUF:Q4_K_M | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| llama3.2-vision:11b | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| llama3.2-vision:11b | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| llama3.2-vision:11b | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| llama3.2-vision:11b | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| llava:latest | base-prompt | 0.0 | 1/1 | 0/1 | 0/1 |
| llava:latest | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| llava:latest | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| llava:latest | learned-context | 0.3 | 1/1 | 0/1 | 0/1 |
| minicpm-v:latest | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| minicpm-v:latest | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| minicpm-v:latest | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| minicpm-v:latest | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| moondream:latest | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| moondream:latest | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| moondream:latest | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| moondream:latest | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| phi4:14b | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| phi4:14b | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| phi4:14b | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| phi4:14b | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| qwen2.5-coder-14b-32k:latest | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| qwen2.5-coder-14b-32k:latest | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| qwen2.5-coder-14b-32k:latest | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| qwen2.5-coder-14b-32k:latest | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| qwen2.5-coder:14b-instruct-q4_K_M | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| qwen2.5-coder:14b-instruct-q4_K_M | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| qwen2.5-coder:14b-instruct-q4_K_M | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| qwen2.5-coder:14b-instruct-q4_K_M | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |
| qwen3:14b | base-prompt | 0.0 | 0/1 | 1/1 | 0/1 |
| qwen3:14b | base-prompt | 0.3 | 0/1 | 1/1 | 0/1 |
| qwen3:14b | learned-context | 0.0 | 0/1 | 1/1 | 0/1 |
| qwen3:14b | learned-context | 0.3 | 0/1 | 1/1 | 0/1 |

## Provisional per-function shortlist

- `FUN_24dd_0582`: `llava:latest`, learned-context, temperature 0.3; accepted=True, build_passed=False, MLflow run `061f128b3fbf4426b728093c1146a924`.

A shortlist is not a recovery attestation. Review each candidate against
its assembly, ABI, calls, state effects, and data references.
