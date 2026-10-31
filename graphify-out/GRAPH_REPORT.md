# Graph Report - /home/robin/OneDrive/University and such/LoSoRe  (2026-10-27)

## Corpus Check
- 75 files · ~54,587 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1037 nodes · 1507 edges · 40 communities (33 shown, 7 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 106 edges (avg confidence: 0.81)
- Token cost: 30,897 input · 3,749 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Verified Example Knowledge|Verified Example Knowledge]]
- [[_COMMUNITY_DAT and Runtime Verification|DAT and Runtime Verification]]
- [[_COMMUNITY_Pascal Draft Generation|Pascal Draft Generation]]
- [[_COMMUNITY_Decompiler Matching|Decompiler Matching]]
- [[_COMMUNITY_Oracle Verification|Oracle Verification]]
- [[_COMMUNITY_Pascal Decompilation Matching|Pascal Decompilation Matching]]
- [[_COMMUNITY_Assembly CFG Analysis|Assembly CFG Analysis]]
- [[_COMMUNITY_Overnight Experiment Suite 2|Overnight Experiment Suite 2]]
- [[_COMMUNITY_Overnight Experiment Suite|Overnight Experiment Suite]]
- [[_COMMUNITY_Semantic Auditing|Semantic Auditing]]
- [[_COMMUNITY_Decompilation Fine-Tuning|Decompilation Fine-Tuning]]
- [[_COMMUNITY_Failure-Driven Improvement|Failure-Driven Improvement]]
- [[_COMMUNITY_Diff Oracles and Scheduling|Diff Oracles and Scheduling]]
- [[_COMMUNITY_Cross-Project Training Corpus|Cross-Project Training Corpus]]
- [[_COMMUNITY_Dual-Judge Auditing|Dual-Judge Auditing]]
- [[_COMMUNITY_Model Training and Distillation|Model Training and Distillation]]
- [[_COMMUNITY_Project Workflow and Oracles|Project Workflow and Oracles]]
- [[_COMMUNITY_Prompt Sanitization Tests|Prompt Sanitization Tests]]
- [[_COMMUNITY_Assembly Baseline|Assembly Baseline]]
- [[_COMMUNITY_Compile-Gated Iteration|Compile-Gated Iteration]]
- [[_COMMUNITY_Learning Regression Tests|Learning Regression Tests]]
- [[_COMMUNITY_Progress and Reconstruction Reports|Progress and Reconstruction Reports]]
- [[_COMMUNITY_Skeleton Drop Diagnostics|Skeleton Drop Diagnostics]]
- [[_COMMUNITY_Signed Result Helpers|Signed Result Helpers]]
- [[_COMMUNITY_Memory Copy Routines|Memory Copy Routines]]
- [[_COMMUNITY_Ghidra Export Integration|Ghidra Export Integration]]
- [[_COMMUNITY_Provenance Evidence|Provenance Evidence]]
- [[_COMMUNITY_Ghidra Ingestion|Ghidra Ingestion]]
- [[_COMMUNITY_Liero Reconstruction Documentation|Liero Reconstruction Documentation]]
- [[_COMMUNITY_Logical Global State|Logical Global State]]
- [[_COMMUNITY_Stack Copy Operations|Stack Copy Operations]]
- [[_COMMUNITY_Target Scaffolding|Target Scaffolding]]
- [[_COMMUNITY_Fallback Oracle Guidance|Fallback Oracle Guidance]]
- [[_COMMUNITY_Liero Program Entry|Liero Program Entry]]

## God Nodes (most connected - your core abstractions)
1. `draft()` - 17 edges
2. `_repair_stem()` - 15 edges
3. `_load()` - 15 edges
4. `phase_e1()` - 12 edges
5. `_decl_for()` - 11 edges
6. `Verification Flow` - 11 edges
7. `log()` - 10 edges
8. `phase_p1()` - 10 edges
9. `_revert_to_skeleton()` - 9 edges
10. `_run()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `test_drafted_counts_implemented_bodies_not_scaffolds()` --calls--> `_drafted()`  [INFERRED]
  tests/test_report.py → tools/report.py
- `test_diff_backends()` --calls--> `byte_exact()`  [INFERRED]
  tests/test_gated.py → engine/diff.py
- `test_diff_backends()` --calls--> `relocation_aware()`  [INFERRED]
  tests/test_gated.py → engine/diff.py
- `test_scheduler_routes()` --calls--> `route()`  [INFERRED]
  tests/test_gated.py → engine/scheduler.py
- `main()` --calls--> `verify()`  [INFERRED]
  tools/draft_verify.py → engine/verify.py

## Communities (40 total, 7 thin omitted)

### Community 1 - "Verified Example Knowledge"
Cohesion: 0.06
Nodes (50): _fn_key(), get_weighted_examples(), Example quality tracking for few-shot examples.  Each verified example in knowle, Prefer stable pair IDs while preserving legacy function-name keys., Increment success count for an example and recompute its rate., Increment failure count for an example and recompute its rate., Compute success_rate from an entry dict., Return up to `limit` examples sorted by success_rate desc, then recency.      Fi (+42 more)

### Community 2 - "DAT and Runtime Verification"
Cohesion: 0.05
Nodes (29): LIERO.CHR graphics format (from liero.nl/lierohack + openliero tctool — clean-room reference, verify against BYOD), LIERO.DAT settings format: the file is 155 bytes (0000h-009Ah; 009Bh is, LIERO.SND format: raw samples + index; lierolibre provides replacements; original SND stays BYOD-only, preservation only, not that those opaque bytes' semantics are understood., the exclusive end offset). The current parser models 20 documented bytes;, the remaining 135 bytes are preserved opaquely. Byte-exact round-trip proves, Register Management, Verification Flow (+21 more)

### Community 3 - "Pascal Draft Generation"
Cohesion: 0.09
Nodes (45): _assembly_evidence(), _build_pascal_prompt(), _c_ref_block(), _compile_errors(), _compile_gate(), _decl_for(), detect_language(), draft() (+37 more)

### Community 4 - "Decompiler Matching"
Cohesion: 0.08
Nodes (37): Code Generation and Conversion, Semantic Fixing, _branch_target(), build_and_diff(), _c_to_pascal(), cfg_from_ghidra_asm(), _cfg_from_lists(), cfg_from_objdump() (+29 more)

### Community 5 - "Oracle Verification"
Cohesion: 0.07
Nodes (32): Ghidra ingest (2026-10-11), liero provenance (P0 findings 2026-10-10, BYOD confirmed 2026-10-11), Two archives are byte-identical (2026-10-11), Oracle recommender: suggest which oracle to use for a new target.  Based on what, Recommend an oracle type for `target`.      Heuristic:       1. If another targe, Suggest build.sha1 entries for a target based on its asm files.      Returns lin, recommend_oracle(), suggest_build_sha1_entries() (+24 more)

### Community 6 - "Pascal Decompilation Matching"
Cohesion: 0.08
Nodes (27): LLM-based Fixer, _branch_target(), _c_to_pascal(), cfg_from_ghidra_asm(), _cfg_from_lists(), cfg_from_objdump(), cfg_similarity(), hist() (+19 more)

### Community 7 - "Assembly CFG Analysis"
Cohesion: 0.09
Nodes (33): branch_target(), build_blocks(), cfg_stats(), _contiguous_runs(), dominators(), find_loops(), is_branch(), is_call() (+25 more)

### Community 8 - "Overnight Experiment Suite 2"
Cohesion: 0.14
Nodes (33): c_call(), dual_verdict(), elapsed(), f3_finish(), f3_summarize(), f4_prompts(), f4_summarize(), f5_summarize() (+25 more)

### Community 9 - "Overnight Experiment Suite"
Cohesion: 0.16
Nodes (33): base_prompt(), c_call(), daytime(), e1_summarize(), e2_summarize(), e3_summarize(), e5_summarize(), fix_prompt() (+25 more)

### Community 10 - "Semantic Auditing"
Cohesion: 0.12
Nodes (31): Semantic Audit, budget_left(), _build_ok(), capped_c_call(), _decomp_lines(), elapsed(), heartbeat(), load_json() (+23 more)

### Community 11 - "Decompilation Fine-Tuning"
Cohesion: 0.12
Nodes (28): LLM Decomilation, LoRA Fine-Tuning, batchify(), build_dataset(), encode(), eval_model(), main(), pad_batch() (+20 more)

### Community 12 - "Failure-Driven Improvement"
Cohesion: 0.09
Nodes (27): classify_failure(), _default(), get_anti_patterns(), _parse_classification(), Failure analysis via a specialised LLM.  Classifies why a decompiled function fa, Classify why function `fn` failed verification., Append a failure to the per-toolchain failures catalogue., Return the most common failure categories as anti-patterns. (+19 more)

### Community 13 - "Diff Oracles and Scheduling"
Cohesion: 0.11
Nodes (18): byte_exact(), _norm(), Oracle diff backends (stdlib only; asm-differ/reccmp/frida optional adapters). b, relocation_aware(), Scheduler: auto-templates -> agent fan-out with hit-rate monitor -> human residu, route(), Disc-gated tests: green WITH or WITHOUT BYOD present (the Liero standard).  The, Invoke a repo entry-point with absolute paths so results never depend on CWD. (+10 more)

### Community 14 - "Cross-Project Training Corpus"
Cohesion: 0.15
Nodes (23): active_adapter_for(), eligible_examples(), export_dataset(), format_training_prompt(), _is_legacy_c_pair(), legacy_assembly_examples(), _load_state(), main() (+15 more)

### Community 15 - "Dual-Judge Auditing"
Cohesion: 0.21
Nodes (23): Dual-Judge Semantic Audit, best_candidate(), best_corpus_rows(), budget_left(), cand_prompt(), elapsed(), g2_finish(), heartbeat() (+15 more)

### Community 16 - "Model Training and Distillation"
Cohesion: 0.18
Nodes (20): LLM Training, build_pairs(), encode(), evaluate(), load_base(), main(), pad_batch(), Night-2 torch worker: two finetune variants, seq 2048.    f1 = cfgA-long: reload (+12 more)

### Community 17 - "Project Workflow and Oracles"
Cohesion: 0.10
Nodes (18): Oracles — strongest first, agents.md — orchestration (adapted from openrecet AGENT-WORKFLOW.md), Canon, code:sh (make init && make test        # green with no target data), code:sh (uv sync --extra dev --extra training), code:sh (make train-export TARGET=liero              # write training), Layout, Learning (target-over-target) (+10 more)

### Community 18 - "Prompt Sanitization Tests"
Cohesion: 0.22
Nodes (16): _load(), Regression tests for tools/e6_match.py prompt/sanitize pipeline.  Pins the three, test_declare_undeclared_adds_missing_locals(), test_declare_undeclared_ignores_fun_and_known(), test_expand_ptr_stmts_derefs_and_increments(), test_fix_arity_truncates_surplus_args(), test_fix_arity_zero_param_function(), test_fix_types_leaves_identifiers_alone() (+8 more)

### Community 19 - "Assembly Baseline"
Cohesion: 0.19
Nodes (16): asm_to_ops(), bucket(), compile_c(), extract_c(), find_llm4_model(), main(), ollama_generate(), ollama_unload() (+8 more)

### Community 20 - "Compile-Gated Iteration"
Cohesion: 0.20
Nodes (16): Compile Gate, LoRA Finetuning, Overnight Experiment Suite, batchify(), build_dataset(), encode(), eval_model(), main() (+8 more)

### Community 21 - "Learning Regression Tests"
Cohesion: 0.21
Nodes (11): _make_target(), Tests for the learning component: knowledge store + learn stage.  The central cl, _run(), test_draft_emits_same_language_pascal(), test_draft_gated_on_low_confidence(), test_learn_creates_toolchain_recipe(), test_learn_skips_without_functions_json(), test_learning_transfers_to_second_target() (+3 more)

### Community 22 - "Progress and Reconstruction Reports"
Cohesion: 0.24
Nodes (12): Decompilation Report, test_drafted_counts_implemented_bodies_not_scaffolds(), test_generated_counts_function_files_but_not_program_includes(), test_verified_excludes_dat_oracle_artifacts(), _drafted(), _fn_count(), _function_names(), _generated() (+4 more)

### Community 23 - "Skeleton Drop Diagnostics"
Cohesion: 0.24
Nodes (12): analyze(), classify(), gate_sim(), main(), online_census(), _print(), _print_gate(), diagnose silent drops: why functions end up as skeletons in src/.\n\nTwo modes, (+4 more)

### Community 26 - "Ghidra Export Integration"
Cohesion: 0.31
Nodes (3): ExportFuncs, GhidraScript, Ghidra Integration

### Community 27 - "Provenance Evidence"
Cohesion: 0.33
Nodes (8): compiler_id(), detect_toolchain(), provenance(), Provenance gate: BYOD hash-gate + evidence-backed compiler/language detection., Legacy per-file label (kept for the PROVENANCE.md AUTO block / existing tests)., Scan BYOD executables/text for compiler + language signatures.      Returns dict, sha1(), _write_toolchain_yaml()

### Community 28 - "Ghidra Ingestion"
Cohesion: 0.38
Nodes (6): find_ghidra(), ingest(), pick_binary(), Ingest: Ghidra headless export -> targets/<slug>/asm/ (+ decomp/, functions.json, Locate a Ghidra install dir (contains support/analyzeHeadless)., Choose the main executable to analyze: prefer *.EXE (largest), else *.exe.

### Community 29 - "Liero Reconstruction Documentation"
Cohesion: 0.40
Nodes (4): DAT file coverage, Implemented assembly-derived routines, Liero source reconstruction status, Remaining work

## Knowledge Gaps
- **23 isolated node(s):** `Same-language policy`, `Playable-parity MVP`, `code:sh (make init && make test        # green with no target data)`, `code:sh (uv sync --extra dev --extra training)`, `code:sh (make train-export TARGET=liero              # write training)` (+18 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Verification Flow` connect `DAT and Runtime Verification` to `Oracle Verification`, `Diff Oracles and Scheduling`, `Prompt Sanitization Tests`, `Learning Regression Tests`, `Progress and Reconstruction Reports`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `Oracle Verification` connect `Project Workflow and Oracles` to `Diff Oracles and Scheduling`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **What connects `Same-language policy`, `Playable-parity MVP`, `code:sh (make init && make test        # green with no target data)` to the rest of the system?**
  _190 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Liero Routine Interface` be split into smaller, more focused modules?**
  _Cohesion score 0.006756756756756757 - nodes in this community are weakly interconnected._
- **Should `Verified Example Knowledge` be split into smaller, more focused modules?**
  _Cohesion score 0.05520614954577219 - nodes in this community are weakly interconnected._
- **Should `DAT and Runtime Verification` be split into smaller, more focused modules?**
  _Cohesion score 0.05442176870748299 - nodes in this community are weakly interconnected._
- **Should `Pascal Draft Generation` be split into smaller, more focused modules?**
  _Cohesion score 0.08695652173913043 - nodes in this community are weakly interconnected._