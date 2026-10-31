# Evidence-backed, whole-program recovery

## Objective

Recover as much source-level structure and behavior as the original Pascal
binary and lawful supporting evidence permit. Liero is the first case, not
a request for another Liero clone. Preserve original routine structure,
calling conventions, layouts and effects where supported. Historical names,
comments and exact source text cannot generally be recovered uniquely.

## The crossword model

An unsolved routine is not an isolated translation problem. Its callers,
callees, shared records and globals constrain its possible meanings. Each
checked solution supplies more constraints on the remaining puzzle:

1. Establish a scoped routine contract from original evidence.
2. Record preconditions, effects, hashes and supporting references.
3. Propagate applicable constraints across evidenced relationships.
4. Detect contradictions and retain unresolved alternatives.
5. Select the next routine or experiment that can remove an important
   ambiguity.
6. Generate, execute and compare candidates; feed counterexamples back into
   the same connected system.

A constructor's checked buffer-capacity field can constrain a refill
routine. A callee's stack cleanup constrains argument interpretation at a
call site; a caller's use of the return value constrains the callee. Shared
field layouts tie otherwise distant routines together.

Use the existing [fact graph](../engine/fact_graph.py), not an unrelated
graph framework. It already distinguishes observed, oracle-verified,
hypothetical, derived, contradicted and unknown facts, supports evidenced
same-value propagation and detects conflicts. That does **not** mean it
already implements a general whole-program constraint solver.

## Competing hypotheses and confidence

Keep multiple candidate signatures, layouts, targets or behaviors when the
evidence permits them. Each hypothesis needs:

- A stable identity, subject and explicit claim.
- Scope and assumptions, including path/input conditions.
- Supporting and contradicting evidence, with original/source hashes.
- Dependencies on other hypotheses or checked contracts.
- A score with its meaning stated: model ranking is not a calibrated
  probability of correctness.
- A discriminator: what observation or check could reject it.

Test compatible combinations against the already checked parts of the
program. Reject only what the evidence actually contradicts; a missing
trace is not a contradiction. Keep alternatives when tests cannot
distinguish them. Shared dependencies and recursive groups must be checked
together when relevant, rather than choosing an unsupported local guess.

Do not treat mutually supporting guesses as independent evidence. Reusing
one trace through several graph paths must not increase certainty. Model
confidence cannot turn a hypothesis into an observed fact. When support
changes or becomes stale, invalidate affected conclusions and reconsider
the alternatives.

Bound the search. Do not enumerate every combination across the entire
binary. Start with the active connected slice, prune using checked hard
constraints, retain a bounded set of alternatives, and record any
budget-pruned alternatives separately from disproven ones.

## ML/DL's role

Use learned models to propose Pascal bodies, recognize compiler patterns,
rank hypotheses and select useful experiments. Retain validated patterns
for retrieval and, once suitable data and holdouts exist, local training.
Acceptance still needs independently checked binary-backed evidence.

Do not ask a model to rediscover constants or pointer-origin arithmetic that
supported byte transfer rules can establish. Publish those rules' entry
assumptions, exact instruction/relocation support and unknown residue; reject
contradictory proposals without silently editing them into successful ones.
A straight-line prefix cannot certify a later branch or loop: keep those
fields unresolved and let independent execution test proposed behavior.
Changing the method after a known failure is debugging, not an untouched
generalization evaluation. Freeze the method and holdouts before evaluating
new routines; count developer-supplied sketches separately from recovered
behavior and do not infer weight learning from successful repair.

For global-memory effects, distinguish a constant offset from an
object-relative pointer and require established segment provenance.
Unsigned word arithmetic wraps before later shifts; validate the entire
nonwrapping write span against an explicit writable/nonaliasing caller
window. Segment or stack changes must invalidate dependent bindings.
Preserve a frozen failure when adding shared rules afterward, then record
the changed rule identity separately. Guarded original-only execution can
check predicted writes and observed stack balance; it cannot stand in for
Pascal parity, full ABI or normal-program evidence, nor resolve an
unsupported return or justify source promotion.

Two foundational references motivate this design:

- [Recurrent Relational Networks](https://arxiv.org/abs/1711.08028) study
  repeated relational inference on graphs, including supervised Sudoku
  solving. This motivates iterative neighbor updates, not a claim that a
  Sudoku network can decompile Pascal.
- [DreamCoder](https://arxiv.org/abs/2006.08381) combines program search,
  reusable learned symbolic abstractions and neural search guidance. This
  motivates accumulating trusted Pascal/compiler knowledge, not rewriting
  recovered routines into a different design.

These are foundational sources, not a survey of the latest methods. Measure
benefits using fixed tasks, initial evidence and budgets with propagation
enabled versus disabled. Report downstream unlocks, candidate attempts,
counterexamples and new recoveries. More context can help, but improvement
is a measured hypothesis, not a guarantee.

## Acceptance and memory

Keep these evidence levels separate:

| Evidence | What it establishes |
| --- | --- |
| Compilation | Syntax/type compatibility with the actual compiler used |
| Static evidence accounting | Relationship of source to checked original control flow and effects |
| Original-only execution | Behavior observed under the probe's stated conditions |
| Original-versus-Pascal comparison | Matching defined outputs/effects for the recorded contract and cases |
| Normal-program observation | Reached contexts/behavior in an original executable run |

None alone proves universal equivalence. A format test does not certify
unrelated routines. Host FPC execution does not establish TP7 code generation
or real-mode ABI parity. A controlled COM harness does not establish normal
program segment layout.

Persist current contracts and experimental results with hashes and
replayable inputs. Put target-specific discoveries and counterexamples in
the target's reconstruction documentation. General rules belong here;
short operational guardrails belong in [agents.md](../agents.md).

## Lessons established by the current Liero probes

- A compiled baseline, restored skeleton or unchanged proposal cannot count
  as candidate compilation. Capture raw proposals and exact rejection
  reasons; incomplete feedback transport must be observed, not guessed.
- Similarity/CFG normalization and model confidence can rank hypotheses,
  not certify their semantics. A short thunk and lossy decompiler loop
  may describe different entry scopes; inspect the bound bytes first.
- More models/retries are not a remedy for the wrong contract or hypothesis
  space. The constructor's 17 compiled failures could not be repaired by
  copy-loop mutations when initialization constants/offsets were wrong.
  Deriving seven supported fields from bytes removed that ambiguity;
  later name-copy behavior still required independent testing.
- Developer-defined sketches can over-specialize the recovery method.
  That observation does not establish model-weight overfitting. Report
  known-slice repair, untouched-method evaluation and blind-source
  evaluation separately; preserve negative trials when strategy changes.
- Training selects the first passing candidate; the selected candidate gets
  one held-out evaluation and its failure ends the run. Retrying from
  held-out counterexamples turns that set into training. Deduplicate source
  hashes and replay already measured seeds rather than spend the budget
  again. Deliberate mutants test repair machinery, not fresh model success.
- JSON-native evidence records and exact input/rule/source hashes make
  replay meaningful. Formatting can change a rule-file hash without
  changing semantics; keep historical versions distinct rather than
  relabeling snapshots or counting replay as new independent observations.
- The 492c shared-rule repair derived 2966 zero words only under an explicit
  writable/nonaliasing DS window. Three dirty-pattern original runs checked
  the full guarded window and SP balance, but did not execute Pascal or
  establish complete return/flags/register or normal-program contracts.
- Local training/inference smoke tests prove the adapter path runs.
  Retrieval, constraints, anti-pattern feedback and held-out token-loss
  improvements are not measured binary-backed Pascal recovery gains.
  Continual learning needs qualified cross-project examples and a frozen
  project-level recovery benchmark, not automatic promotion of finite probes.
- Research citations motivate experiments; they are not acceptance evidence.
  Earlier Reddit access failed, so no Reddit-specific finding was established.
  Do not describe foundational papers or previous searches as a fresh survey.
- Original file-routine bytes can execute in a small hash-checked DOSBox
  harness with actual DOS file services. This is narrower than original
  executable startup.
- The string reader retains a four-byte object argument for line skip;
  byte-correct output without correct stack behavior would miss that fact.
- CR at the end of a 128-byte buffer and LF after refill is a meaningful
  boundary case; ordinary short lines do not exercise it.
- The constructor has a 79-byte filename cap and an embedded-NUL stop.
  Checking complete object bytes and dirty initial states also exposes
  unintended zeroing or overwritten object tails.
- Normalize only identified relocated pointer fields, checking their
  expected segment first. Do not mask arbitrary pointer differences.
- Do not transfer a finite harness observation to arbitrary caller addresses
  by assumption. A layout-independent field rule needs its own static or
  broader execution evidence; keep probe preconditions separate from the
  conditions under which that rule can propagate.
- When a leaf calls an operating-system service, separate the recovered
  routine from the host service adapter. State which service outcomes are
  implemented and tested; unexpected host errors must abort, not become
  successful-looking DOS results. Original-only caller setup is a fixture,
  not evidence that the caller's Pascal body is recovered.
- Keep leaf and caller effects distinct: Liero's close leaf leaves the handle,
  mode and method slots untouched even after closing the OS resource. Test a
  repeated call and dirty state; do not add a convenient field reset that only
  the caller performs.
- Compose checked neighbors using their actual bodies, not copied summaries
  inside a new candidate. Use labeled synthetic callbacks to challenge a
  dispatcher's error and argument-preservation contract, but never count
  those callbacks as recovered game methods. An unknown resolver is an
  explicit blocker, not a no-op success.
- Test short branches against their exact targets: an empty-name setup branch
  can skip both an OS call and the following store. A prepared register value
  is not evidence that it reaches memory. Record observed emulator error
  mappings as backend-specific instead of replacing them with textbook values.
- A sticky global error is not the current callee's return result. Compose
  wrappers with actual callees and test successful operations after an earlier
  error; preserve return flags separately. An error in close may still permit
  a subsequent setup attempt, so do not impose a new early-exit policy.
- Distinguish shared return tails by exact branch destinations, not visual
  proximity: Liero's read callback backs up SI for CR/1A but not for count
  exhaustion; its skip callback leaves 1A unconsumed. Compare consumed offsets
  and remaining counts alongside output bytes. A continuation token such as
  `3923` is not proof of terminal EOF or of the next callback phase.
- Verify continuation transitions across actual refills, including delimiter
  splitting, rather than replaying each callback only at offset zero. In
  Liero, `390E` switches to `3923` after a trailing CR; refill must preserve
  that new token, count and destination offset. At empty-buffer return,
  callback AX can stay nonzero while ZF is true. Do not equate return flags,
  sticky status and callback identity.
- Wrapper parity must include caller/callee stack effects, not only object
  bytes and return status. When a host language cannot reproduce the original
  ABI, capture the original stack and model retained arguments explicitly,
  with that limitation in the oracle contract.
- Synthetic far callbacks are useful controlled probes for optional methods
  and sticky errors. Validate the exact method slot and receiver address;
  never let a synthetic callback imply that a real method was recovered.

See [Liero reconstruction evidence](../targets/liero/docs/RECONSTRUCTION.md)
for exact scope, commands and current verification limits.

## Long-run scope control

Every batch needs a named routine/slice, one blocking question, a measurable
acceptance condition and a stop rule. Prefer existing infrastructure and the
smallest experiment that settles the question. Stop low-yield expansion at
the established hit-rate floor; report actionable residue rather than
relaxing gates or starting another broad framework project.

The [persistent recovery TODOs](RECOVERY_TODO.md) separate completed
measurements from suggested future batches. Resolve the active contract gap,
measure its Pascal counterpart, then freeze the method before widening
coverage. Keep generalizable rules here, operational guardrails in
[agents.md](../agents.md), and exact target counts/hashes in the target docs.
