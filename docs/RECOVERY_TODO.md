# Recovery TODOs

Checkpoint: 2026-10-31. This is the persistent recovery backlog, not an
instruction to execute every future task. Session SQL tracks execution;
these IDs and acceptance gates make the next batch understandable without
that session. See [current handoff](../CONTINUATION_SUMMARY.md),
[method](RECOVERY_METHOD.md) and
[target measurements](../targets/liero/docs/RECONSTRUCTION.md).

## Completed evidence milestones

| Status | Milestone | Evidence and qualification |
| --- | --- | --- |
| Done | Retrieval and local adapter infrastructure | Cross-project/task labels and local training/inference smoke tests; no demonstrated real-project recovery gain |
| Done | Isolated, resumable candidate evaluation | Preserve raw output, sanitizer/build/oracle failures and hashes; baseline compilation is separate |
| Done | Binary census and alternate-entry accounting | Byte/relocation-bound streams and call provenance; coverage/decoded destinations are not source recovery |
| Done | Manual/composed file-input contracts | Original-byte probes, actual callees, dirty objects, callback/refill and stack checks; scoped, not full-program parity |
| Done | Automatic close/refill PoC | Close 8/8 training, 16/16 holdout; refill 64/64, 32/32; supplied sketches |
| Done | Constructor failure analysis | 17 compiled hypotheses, zero training passes; 0/1 slice yield stopped expansion |
| Done | Byte-constrained constructor repair | 514/514 training, 264/264 holdout; known-slice changed-strategy pass |
| Done | Frozen transfer assessment | 4/18 bytes at 492c, no writes; historical failure preserved |
| Done | `global-transfer`, `global-measure`, `global-record` | Shared segment/global rules; explicit DS window; three 8192-byte original-only checks; 184 focused tests |

None of the recent generated trials installed source, changed recovery
attestations, promoted examples or demonstrated continual weight learning.
Repeated replay is integrity validation, not additional independent support.

## Suggested next batches, in dependency order

### 1. `next-global-contract` — resolve the 492c contract gap

**Status:** pending. **Slice:** `FUN_24dd_492c` and the direct call sites
needed to establish its entry/return conditions.

- Blocking question: which caller segment, writable/nonaliasing range and
  near-return/stack obligations are actually supported by original evidence?
- Reuse original-byte/MZ binding, existing call inventory, ledger and probe.
  Distinguish the probe's DS=CS layout from original-program entry DS.
  A caller window is a precondition until evidenced, not an allocation fact.
- Acceptance: publish a hash-bound scoped contract with exact supporting
  call/instruction references and explicit unknown ABI effects. If support
  is insufficient, record the concrete blocker instead of enabling `RET`
  as a blanket success.
- Stop: after that one contract question is settled or a missing original
  observation prevents it. No model calls or larger frontier.

### 2. `next-global-parity` — compare Pascal under the checked contract

**Status:** pending. **Prerequisite:** `next-global-contract`.

- Blocking question: does Pascal reproduce the supported 492c memory
  contract, rather than merely agree with another hand-written expectation?
- Reuse the archived original-byte harness and existing Pascal comparison
  patterns. Check dirty memory, the full guarded window and stated effects;
  preserve original-only, host-Pascal and ABI measurements separately.
- Acceptance: replayable original/Pascal comparisons with all 8192 bytes
  checked per applicable case, unchanged outside-range guards, source/rule/
  input hashes and any ABI limitations. Review existing manual source
  independently; do not feed it as a hidden model answer.
- Stop: fixed cases under the established contract; unknown layouts remain
  unknown. A finite pass is not whole-routine attestation or corpus promotion.

### 3. `next-frozen-transfer` — measure portability before expansion

**Status:** pending. **Prerequisite:** `next-global-parity`.

- Choose one callee-free slice untouched by the evaluated method. If it was
  manually reconstructed earlier, label that fact; it is not blind source.
- Freeze rule/source hashes, input contract, oracle cases, developer-supplied
  topology, repair operators and budget before the result. Do not add an
  answer-shaped sketch after seeing it.
- Acceptance: report static coverage, candidate compilation, training
  selection and one held-out outcome separately. Compare concrete
  discrepancies with original bytes, not just CFG similarity.
- Stop: the existing bounded runner budget (at most four model requests
  where applicable), no held-out feedback, no duplicate oracle work.
  If slice yield is below 25%, stop expansion and report the shared blocker.
  Static coverage alone is not the yield denominator or a recovery pass.

### 4. `next-assisted-package` — package only the measured path

**Status:** pending. **Prerequisite:** `next-frozen-transfer`.

- Reuse the current runner; document a reproducible entry point for the
  measured slices, explicit dependencies, skip/failure states, provenance,
  fixed budgets, controls and replay.
- Acceptance: another invocation reproduces the stated bounded workflow
  without operator semantic intervention; unknowns and developer-supplied
  hypotheses remain visible. A failed portability test may still be
  packaged honestly, but cannot justify a larger recovery run.
- Stop: no second orchestration/graph/probe framework, playable rewrite,
  broad model sweep or automatic source installation.

### 5. `next-contract-propagation` — unlock one connected neighbor

**Status:** pending. **Prerequisite:** `next-frozen-transfer`.

- Publish an established field/ABI/effect constraint through an evidenced
  caller/callee or shared-data relationship using the existing fact graph.
- Acceptance: name one downstream ambiguity removed or one contradiction
  exposed, retaining dependencies, scope and stale-evidence invalidation.
  Compose actual checked callees; a guessed callee cannot unblock a caller.
- Stop: one connected neighbor/dependency group, not a whole-program solver
  or graph rebuild. Consistency is not independent correctness evidence.

## Deferred: `later-model-improvement`

Do not start a new training/model sweep from the current scoped probes.
First obtain independently reviewable, eligible Pascal examples across
projects and fix a held-out-project binary-backed benchmark. Keep legacy
decompiler-C supervision separate from verified Pascal, deduplicate evidence
and retain compiler/platform/contract provenance.

Measure retrieval/constraint benefits separately from adapter gains against
the same base model, tasks and budgets. Report language-model validation
loss separately from accepted recovery outcomes. Only the applicable corpus,
oracle and review gates permit promotion; a tiny training smoke test or a
successful known-slice repair does not establish the requested continual
model improvement.
