| arm | model | input | out | n | strict | any-compile/sanitize | struct |
|---|---|---|---|---|---|---|---|
| A | llm4decompile-6.7b | asm | C | 12 | 6/12 | 6/12 (50%) | 9/12 |
| B | qwen2.5-coder:14b | asm | C | 12 | 4/12 | 5/12 (41%) | 6/12 |
| C | qwen2.5-coder:14b | decomp-C | C | 12 | 9/12 | 9/12 (75%) | 10/12 |
| D | qwen2.5-coder:14b | asm+decomp-C | Pascal | 12 | — | 6/12 (50%) | 6/12 |

**failure buckets (C arms)**

undeclared-ident=6, other=5, syntax=5

**median seconds/call**

A=3, B=24, C=9, D=9
