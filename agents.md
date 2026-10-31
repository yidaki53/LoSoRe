# agents.md — orchestration (adapted from openrecet AGENT-WORKFLOW.md)
Tiers: R3 orchestrator (decides targets, thresholds, proof) / R2 implementer (bounded) / R1 worker (grep/run/fixtures).
Rules: no recursive delegation; never touch vendor/ or extracted/; disc-gated inputs degrade to skip; INCLUDE_ASM residue always builds; every fn labeled with oracle type.
Scope: any lost-source program (games, apps, firmware). Target kinds: game, app, firmware, driver, tool.
Fan-out: independent fns in parallel; stop if hit-rate <25% -> raise effort or route to humans (sm64ds-decomp pattern).
Recovery order: resolve and review routines whose direct callees are already resolved before working on their callers. Defer callers with unresolved callees, then revisit them after the callee contracts and behavior are established; handle mutually recursive routines as one dependency group. Never treat compilation or a guessed callee contract as resolution.

## Recovery objective and method

- Recover evidence-accounted Pascal source and behavior from the binary, not a clone, playable rewrite or redesign. Liero is the first proving ground; other languages/platforms are future work.
- Treat routines, shared data and call sites as a constrained whole. Publish checked contracts and propagate applicable constraints in both caller/callee directions; use them to narrow the next unsolved routines, not just as more few-shot examples.
- Retain competing hypotheses with explicit scope, support, conflicts and confidence. Test compatible combinations against solved neighbors and original execution; consistency alone is not correctness. Do not inflate confidence through circular or repeated use of the same evidence.
- ML proposes/ranks candidates; binary-backed checks determine acceptance. Unknown paths remain unknown. Changing an input contract invalidates dependent conclusions.
- Separate compilation, static review, scoped differential results and normal-program observations. Never promote an entire routine from a partial trace or finite test corpus alone.
- See [the recovery method](docs/RECOVERY_METHOD.md) for evidence handling, hypothesis search and concrete lessons.

## Evidence and experiment guardrails

- Read [current recovery TODOs](docs/RECOVERY_TODO.md) and the relevant [Liero evidence](targets/liero/docs/RECONSTRUCTION.md) before choosing a new batch. Historical handoffs and aggregate reports are not current acceptance evidence.
- Use original bytes and actual MZ relocations for instruction facts; assembly listings/decompiler text are references, not a substitute. Derive supported constants and pointer origins before asking a model to guess them.
- Require proven segment provenance plus explicit writable/nonaliasing bounds for global writes. Entry DS is not source DS; changed SP/SS or potentially aliasing stores invalidate dependent stack bindings.
- Keep controls, sanitized candidates and candidate compilation separate. A restored skeleton/baseline build is not a generated-candidate pass; CFG similarity is ranking evidence, not semantic acceptance.
- Freeze method, budgets, repair alternatives and holdouts before evaluation. Deduplicate source hashes; replay already measured seeds. Select with training only; one held-out evaluation of the selected candidate ends the run, with no held-out retry feedback.
- Record developer-supplied sketch/topology and manually known bodies. Repairing a known slice is debugging, not unseen-routine generalization; an injected mutant is a mechanism test, not another live model recovery.
- Preserve earlier failures and rule snapshots after a strategy change. Replayed evidence is not independent new evidence, and instruction-byte coverage is not a routine recovery rate.
- Never interpret original-only guarded COM memory/SP checks as Pascal parity, full ABI or normal-program reachability. Unsupported returns, unknown paths and external-service outcomes remain explicit obligations.
- Do not infer model improvement from retrieval, anti-pattern feedback, static constraints, compilation or a tiny LoRA smoke test. Keep scoped experimental results out of source/training promotion until the applicable review and oracle gates are met.

## Preventing scope creep during long runs

- Before each work batch, name the exact routine/slice, blocking question, acceptance check and stop condition. Continue only work needed to answer that question or unblock the next measured recovery.
- Reuse existing probes, fact graph, recovery ledger and improvement loop. Do not add a second framework, broad audit, graph rebuild, model sweep or toolchain migration without a demonstrated blocker in the active slice.
- Complete and validate one bounded milestone before widening the frontier. If yield is below the existing 25% floor, stop expansion and report the concrete blocker or changed strategy.
- Do not lower evidence gates, chase playable behavior or count generated stubs to show progress. Preserve successful work and explicitly record unresolved residue.
- Persist important verified findings and failed assumptions in the relevant target documentation; keep general reusable rules in the recovery-method document. Distinguish measured results, hypotheses and future work; session chat is not the only memory.
