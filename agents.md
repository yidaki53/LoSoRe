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

## Recovery-first execution and revisable progress

- Each recovery milestone must target an unresolved implementation or a concrete contradiction in an existing one. Reuse current manual contracts within their scope; do not make revalidation of all old solutions a prerequisite for trying a new routine.
- Keep provisional candidates with explicit evidence, assumptions, dependencies and unresolved obligations. They may guide exploratory caller/callee hypotheses, but those conclusions remain conditional, not checked premises or verified recovery/training examples. Contradictions or changed dependencies trigger re-resolution of affected conclusions, not abandonment of the entire frontier.
- Match acceptance to the claim. Preserve required memory, return, control-flow and caller-observable ABI effects. Require additional register/flag mirrors where observed or required by a dependent contract; prove irrelevance before omitting them. Keep unproved liveness as an explicit obligation, not a silent exemption. Freeze any changed observation contract before candidate evaluation; never weaken it after seeing a failure or relabel an old failure as a pass.
- Allow at most one preparatory work batch per active blocker: state the failing check, smallest necessary fix and unresolved-routine experiment it unlocks. The next batch must attempt that experiment or explicitly escalate the blocker; do not start another calibration, fixture, audit or scaffolding milestone under a new name. Reopen preparation only for new execution evidence that identifies a concrete prerequisite.
- Repeated model failures on the same representation or semantic requirement call for a bounded strategy/capacity escalation, not further pointer-only examples or manual solutions credited to the model. Consider one stronger available model with an adequate output budget; freeze its identity, assistance and budget before comparison, preserve failed runs and do not use terminal outcomes as repair feedback. Do not download models, send project inputs to a new provider or start a model sweep implicitly.
- Below the yield floor, stop expanding the panel, not all reasoning about unresolved code. Select one evidence-justified change on the blocked routine, or report the exact capability/resource needed. Calibration and tooling are prerequisites, never the recovery deliverable; report actual source progress separately from preparation.

## Live model measurement after improvements

- After each coherent codebase improvement milestone, run a bounded live local-model performance trial before declaring it complete; unit tests, compilation, replay and hand-written controls do not substitute for model-generated proposals. Batch related edits into one milestone, not one request per file edit.
- Freeze the model identity, changed method, assistance, training inputs, request/token budgets, acceptance checks and stop condition before generation. Compare with the preserved baseline on the same permitted training scope; record transport/representation failures, compilation, exact-case agreement, source-review eligibility, request count and resource limits. Distinguish pipeline gains from changed model weights.
- Never consume an evaluated holdout as repair feedback. Reuse original training evidence only with authenticated hashes and explicit replay attribution; run terminal evaluation once after training selection. A known/retried routine measures assisted debugging, not unseen generalization. Keep correctness probability/sensitivity null without valid estimators.
- Preserve negative results and method snapshots, persist the comparison in target documentation and stop expansion below the existing25percent floor. A failed live trial completes the measurement, not the recovery. If no relevant safe oracle or required local model/BYOD is available, explicitly record the blocked measurement and exact prerequisite; do not invent a pass or widen scope just to benchmark.
