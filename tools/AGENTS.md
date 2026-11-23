# tools/AGENTS.md

- CLI wrappers stay thin: parse arguments, call an engine function, print JSON. Put logic in `"engine/"`.
- `"tools/run_full_pipeline.py"` validates the frozen `"targets/liero/config/build.sha1"` gate; never auto-generate or append hashes to it.
- `"tools/rl_recover.py"` is the RL entry point: it defaults to `routine-trace-parity`, accepts `--root` for disposable roots, and never prints success from a skip. Legacy model endpoints remain available only through the non-autonomous draft path.
- `"tools/build_codebase_graph.py"` generates `"graphify/codebase.json"`. The installed `/home/robin/.local/bin/graphify` is job-search-specific and must not be used for this repo.
- Do not touch `"extracted/"` or `"vendor/"`. BYOD paths are read-only evidence inputs; disc-gated checks degrade to skip.
- `python3 -m py_compile` all touched Python files before running a pipeline; several legacy scripts still contain syntax errors.
- Use `"tools/benchmark_matrix_models.py --output <new-dir>"` for the pinned 22B-vs-1.5B Matrix leaf comparison; it reuses the frozen direct-source48e1 prompt, training corpus and terminal holdout. Never reuse or overwrite an evaluated archive.
- Use `"--profile raw-source --representation-only"` for a frozen plain-Pascal format gate; normalization accepts only raw/fenced text, never salvage, and cannot promote source.
- Profiles `rtl-template`, `rtl-template-v2`, `rtl-template-v3`, `bootstrap-move-forward-v1` and `bootstrap-move-forward-v2` classify one RTL operation and let `"engine/rtl_template.py"` render Pascal; a new renderer requires a new frozen method id and comparison archive.
- Profiles `packed-copy-v1` and `packed-copy-v2` classify one `FUN_24dd_4141` packed byte-transfer layout and render Pascal from `"engine/rtl_template.py"`; v2 freezes the byte-backed declaration after v1's stale-skeleton declaration failed compile. Each method id requires a fresh archive.
- Use `"tools/evaluate_frozen_source.py --source <rendered.inc> --output <new-dir>"` for one-shot training-then-single-terminal evaluation; the evaluator never promotes source automatically. Promotion is a separate provenance-bearing decision after the matched oracle passes.
- Pass `--routine <FUNCTION>` to the evaluator for non-`FUN_24dd_48e1` leaves; keep training-first and single-terminal ordering unchanged.
- Use `"tools/run_bootstrap.py --target <target> --routine <FN> --output <new-dir>"` for bounded self-bootstrapping: one frozen request per method/model, training-only selection, terminal once per training pass and promotion only after routine oracle parity.
- Profiles `bootstrap-normalize-v1` and `bootstrap-normalize-v2` use closed oracle-backed normalization alternatives for `FUN_24dd_455e`; preserve every failed classification archive. The deterministic `oracle-normalize-v1` archive is provenance for local lowering, not an additional model attempt.
- Use `"tools/build_target_packet.py --target <target> --output <new-dir>"` to turn a target subfolder into a binary-derived evidence packet. Without `--routine`, it selects the first Matrix-unblocked routine that also passes the static binary-evidence gate; the prompt contains no verified source examples, candidate bodies, decompiler output, arbitrary labels or online-agent seeds.
- Quote file paths in commands and docs.
