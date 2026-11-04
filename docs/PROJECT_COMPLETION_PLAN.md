# Completion plan: proof-carrying Pascal recovery

## Product, not another laboratory

LoSoRe should deliver Pascal source accompanied by evidence that states exactly
what it recovers, where it is usable, and what remains unknown. Liero is the
first proving ground. The product is neither a playable clone nor an assertion
that compilable generated routines are original source.

The most useful change in perspective is to ship **connected, proof-carrying
source bundles**, not compete on the number of isolated routines passing small
tests. A bundle contains source, original-byte/relocation identities, applicable
callee contracts, observed caller behavior, review, and unresolved obligations.
Use the existing trial/export and recovery ledger mechanisms; do not build a
second graph, orchestration framework, or acceptance database.

## Architecture decision

RFC: [#1](https://github.com/yidaki53/LoSoRe/issues/1).

Deepen shared archive integrity rather than move files into fashionable layers.
The shared archive boundary seals existing evidence and returns immutable,
hash-checked member bytes. Routine tools keep the meaning of those bytes.
Archive integrity is not behavioral correctness or source acceptance.

| Owner | Responsibility | Must not own |
| --- | --- | --- |
| Shared evidence archive | Safe membership, hashes, sealing, verified read snapshots | Oracle execution, source restoration, model selection, promotion |
| Existing source/caller experiment tools | Frozen method, original and host execution, routine-specific comparisons, replay, export | Duplicated generic archive validation |
| Instruction facts and routine contracts | Original bytes/relocations, provenance, bounds, applicable dependencies | Guessed segment origins or universal callback effects |
| Mutable run state | Interrupted-attempt persistence and restoration | Immutable historical replay |
| Recovery ledger | Source/review identity and explicit acceptance decisions | Automatically promoting finite corpus passes |
| Model adapter and training | Generation and provenance-accounted weight experiments | Deciding correctness from output, loss, retrieval or compilation |
| Pascal target/runtime | Supported recovered bodies and declared projections | Silently implementing unknown DOS/BIOS behavior |

Keep per-routine Pascal includes: their one-to-one original routine mapping is
useful provenance, not gratuitous fragmentation. Extract shared runtime behavior
only when actual routines share a checked contract. Keep target-specific probes
outside the generic engine; absorb repeated infrastructure, not target semantics.

### Implemented architecture milestone

The shared [evidence archive](../engine/evidence_archive.py) now exposes
`seal_archive(directory)` and `read_archive(directory)`. The latter returns a
read-only mapping of validated member bytes, used as `archive["TRACE.BIN"]`.
It imports no compiler, model, target or promotion machinery.

Nibble/cursor, move and source/calibration runners use the shared boundary for
sealing and generic integrity checks; their migrated replay evidence is consumed
from immutable bytes. New method freezes include the shared module, while
historical runs retain their original method sets. Existing CLI/output shapes
and artifact-index serialization remain compatible.

The index must be a nonempty canonical relative-name/SHA256 mapping. Listed
members must be regular files; escaping names, aliases, symlinks, special files,
duplicate keys, invalid digests, missing or modified files and resealing fail
explicitly. Scope-specific required evidence remains the routine validator's
responsibility: a valid generic archive is not a complete experiment.

Unlisted historical additions are allowed but are **not returned as verified
evidence**. Separately attached reviews and predecessor links retain their own
bindings. Export/export validation remain in the existing source-trial tool;
their format and separate path-based checks were not redesigned. The filesystem
boundary targets the current POSIX environment; ancestors above the selected
archive root are not constrained. Do not claim signed authenticity, adversarial
concurrent filesystem guarantees or complete elimination of cross-script imports.

Verification:49 shared-boundary tests;548 connected tests passed with3 existing
expected failures. Historical arithmetic/cursor/packed caller, source success,
source failure and scoped export replays passed without new execution. Full
Pascal target compiled; the unrelated runtime Halt97 remains. The frozen live
Qwen3 arithmetic regression used one request and passed56/56training plus
56/56terminal; no source/example promotion or weight improvement.
Final Pylance caught an incompatible `Mapping.get` override; typed overloads
fixed it without changing runtime semantics. The227 directly connected tests
and historical replays were rerun, and a fresh frozen one-request56+56 live
regression passed with the corrected module. Earlier results were retained.
Core Pylance diagnostics are empty.

The architecture implementation is delivered. The recovery/learning sequence
below remains evidence-gated future work, not work falsely marked complete by
this refactor.

### Testing the boundary

Filesystem tests use temporary directories, not mocks of the implementation.
Shared tests cover corruption, missing members, unsafe names, symlinks, incomplete
archives and immutable reads. Replace duplicate generic seam checks only after
the same invariant is covered there. Preserve original-byte/MZ checks, source
review bindings, stack/guard mutations, selection/terminal restrictions and
routine-specific semantic tests.

Compiler/DOSBox/model adapters may be substituted in orchestration tests.
Those tests do not replace real original-binary execution, compiled Pascal
comparisons or bounded live-model performance measurements.

## Finish lines and current evidence

| Deliverable | Acceptance | Current position |
| --- | --- | --- |
| Dependable scoped recovery tool | Frozen generation, checked source, original/host comparisons, read-only replay and reviewable export | Existing supported pipeline; shared archive refactor addresses duplicated integrity ownership |
| Clean supported panel | One frozen supported-method run, reported without substituting older passes or retrying terminal failures | Clean panel2/3; earlier individual passes do not change that |
| Connected Pascal text subsystem | Applicable callee contracts, installed bodies, composed original/host behavior, source review and explicit ABI/service limits | Complete supported0037 return path:44realconsole+44file,88scroll;28 closed-error,40 open-cleanup and3 full text-error cases. Empty descriptor/callback chains, checked default objects/ports. Actual callbacks, Pascal startup and native ABI remain unresolved |
| Native whole-source acceptance | Every relevant path/ABI/data/service obligation justified independently of finite tests | Whole-review ledger28/295; host mirrors and assembly residue are not native recovery |
| Cross-project improving weights | Reviewed lawful training data, project-held-out evaluation, equal-budget baseline/retrieval/adapter arms | Infrastructure exists; no demonstrated cross-project weight gain |

Read [current TODOs](RECOVERY_TODO.md) and
[target evidence](../targets/liero/docs/RECONSTRUCTION.md) before each batch.
Historical run success is not current source acceptance.

### Connected execution milestone delivered

Follow-on limits work includes row24 scrolling and nonreturning010f with empty
chains and checked closed/open default objects.3711 composes374d/37b3 flush
then37d3 close even after flush failure:40/40 original/Pascal cases. The full
0037 nonzero04f4 continuation agrees3/3, including original0155:textCS return
(correcting unmeasured0157), both writes, close, diagnostics and termination.
One full-text case uses actual invalid-handle6; two inject mechanism outcomes.
Video/input snapshot is before diagnostics, not final diagnostic console state.
The method resolver and vector/termination services are explicit host ports,
not native/universal recovery.

Original startup also executes through its actual far return and supplies
default-object provenance. This remains original-only, not recovered Pascal
startup. The next blocking group is actual descriptor/callback provenance,
writable bounds and hardware-dependent leaves. Relative135c:1345 ultimately
depends on send0000/receive001a polling without software timeouts; a ready-port
fixture is not evidence of real device progress. Do not fake that edge to
declare the subsystem universally complete.

1192 connected tests pass,3 existing xfail; full range-checked target builds
with40 warnings; final open/text-error and historical archives replay.
One liveQwen3 request56training+56terminal and identical replay; known assisted
regression only. No whole-source count, clean-panel result or weight claim changes.

The device write leaf, both output dispatchers, buffered3899,CRLF3930 and
complete0037 supported returning body are installed. The original full text
routine and Pascal agree in44 real-console plus44 file-output cases, including
all4000video/256object-buffer/256input bytes, cursor/status and exact attempted
service bytes/counts. Separate writer/error panels pass75+78 and27+28 cases;
injected outcomes remain mechanism evidence. Console CRLF cursor movement is
explicitly observed/projected, not inferred from file output.

567 connected tests pass,3 expected failures; full target builds. Frozen
liveQwen3 regression passes56+56 with one request, unchanged assisted corpus,
no weight gain. Source/method review and sealed no-execution replay are recorded
in the target evidence/current handoff.

This delivers supported returning and checked terminating text execution, not
step4's all-path/native claim. Nonzero04f4 now composes010f only within the
declared checked cleanup scope; unsupported chains/devices still reject.
Invalid coordinates, redirected378e, source startup and native ABI remain
separate obligations; do not count provisional source as training data.

## Execution sequence

### 1. Finish one infrastructure change, then stop restructuring

Implement and migrate the selected shared archive boundary. Keep existing CLI
and archive formats compatible. Verify historical arithmetic/cursor/copy and
source-trial archives without generation or terminal reexecution. Run focused
tests, connected suites, the Pascal target build and the existing bounded live
model regression. Record integrity, compilation and model outcomes separately.

**Stop condition:** the migrated tools share archive policy and preserve their
behavior. Do not follow this with a provider rewrite, toolchain migration,
graph rebuild or new dashboard. The next recovery batch must attempt an actual
unresolved routine, not another preparation milestone.

### 2. Recover the default-output write leaf

**Slice:** original24dd:37b3. **Question:** what does its DOS write boundary
guarantee, including count0, success, short writes and service errors?

Original linkage conditionally selects37b3 for device output and378e for
nondevice output; both clear the object's used count before DOS21/AH40.
37b3 clearsAX on success without comparing returnedcount;378e returns101 for
a successful short write. Do not repair that difference into a redesigned API.

Reuse existing DOS-service probes. Bind actual DS:79f0 object, source segment,
buffer, active stack and actual relocations; freeze readable/writable ownership
and nonaliasing bounds. Compare original observable memory, return and required
register/flag effects with the installed Pascal/service projection.
Real DOS execution establishes measured service behavior; injected errors or
short writes test the declared adapter mechanism and are labeled separately.

**Acceptance:** reviewed complete leaf under an explicit service contract,
with unsupported outcomes and native ABI limits retained. **Stop:** if a real
service premise cannot be established, name that premise and defer dependent
callers; do not count a returning stub.

### 3. Close the output dispatch and buffered writer

**Order:**396c and397a dispatch scopes, then3899, then3930.

Prove exact method identities and compatible return/error/progress behavior.
Do not use the current396c input375e implementation as output support.
Device output can use37b3 for both flush and optional method; redirected output
requires the distinct378e scope and zero optional slot. Reuse shared helpers
only after those contracts establish what is genuinely common.

For3899 cover zero bytes, partial capacity, exact fill, multiple fills,
sticky error, invalid mode, overlap/alias exclusions and callback failure.
Establish progress on refill/flush loops; testing one non-full buffer cannot
resolve a callback-dependent routine.3930 then composes the two-byte CRLF
source at provenDS:6424 and its optional callback.

**Acceptance:** original/host composed checks plus source/path review for each
claimed scope. **Stop:** unresolved callback effects or changed object/source
contracts invalidate dependent conclusions; re-resolve the affected group only.

### 4. Resolve the error boundary before finishing the caller

**Order:** applicable010f error/cleanup services, then04f4, finally249c:0037.

04f4 returns only on zero sticky error; nonzero tail-jumps010f with the existing
far-return frame. A successful zero fixture cannot certify the error path.
Retain unknown errors as obligations rather than silently defaulting to success.

For0037 compose actual shortstring setup, all0013 calls, both cursor calls,
video writes, output3930 and error04f4. Establish video segment provenance and
owned/nonaliasing bounds; column+length may leave valid text coordinates, so
do not generalize the16valid BIOS cursor observations to every input.

**Acceptance:** one installed connected subsystem with source review and
original/host caller checks covering declared supported paths. Separate scoped
service projections from native ABI and normal-program reachability. A clean
build is necessary, not sufficient. **Stop:** any unresolved direct callee or
service scope blocks the full caller claim.

### 5. Deliver and challenge the prototype

Use the existing CLI, not another interface layer:

```sh
uv run python -m tools.liero_source_trial --prototype \
  --routine FUN_249c_0013 --output /path/to/fresh-private-run
uv run python -m tools.liero_source_trial \
  --output /path/to/fresh-private-run --export /path/to/private-export
uv run python -m tools.liero_source_trial \
  --validate-export --output /path/to/private-export
```

An export without the applicable review is explicitly pending. Retain raw
proposals, failures, source/method hashes and unknowns. BYOD executable and
compiled images stay private and outside exported source bundles.

Run the supported panel under a predeclared method, compatible model/options,
fixed budget and one terminal evaluation per selected candidate. Disclose all
prior measured behavior. Do not replace a failed run with a historical pass.
Choose one transfer task before supplying target-specific source/action answers;
reuse applicable contracts, not answer-encoded guesses.

**Acceptance:** independently reviewable bundle plus honest panel and transfer
results. **Stop:** below25percent yield, stop frontier expansion and identify
the missing capability or one evidence-justified strategy change.

### 6. Measure learning, not just better prompts

Only independently reviewed, hash-bound and appropriately scoped lawful pairs
enter training. Exclude failed candidates, unknown stubs, stale reviews,
terminal families and assessed responses. Label synthetic compiler pairs and
human/model/mechanical assistance distinctly.

Freeze project-level train/development/terminal exclusions, source deduplication,
base identity, one adapter configuration, resource/request budgets and selection
rule before evaluation. Compare base-only, retrieval-only and adapted inference
on the same interface and equal budgets. Development selects; one held-out
evaluation of the selected adapter ends the experiment.

Report syntax, static constraints, original/host behavior, whole-source review
and forgetting separately. Lower loss or faster generation is not recovery
gain. If no eligible data or compatible local resources exist, record that
blocker and skip training rather than train on provisional labels.

**Acceptance:** measured project-held-out behavioral gain without leakage or
regression on declared preservation tasks. **Stop:** a failed adapter is a
preserved experiment, not permission to tune against terminal feedback.

## Operational discipline

Track four separate outputs for each delivery:

1. **Source gained:** exact installed/reviewed bodies and applicable scopes.
2. **Behavior established:** original observations and composed Pascal checks,
   with service premises and unexplored paths.
3. **Tool reliability gained:** replay, integrity, failure handling and build
   behavior; do not add this to recovered-source totals.
4. **Model gain measured:** fixed-budget live results and, separately, genuine
   project-held-out weight comparisons.

Make the existing export the handoff between recovery and review. A reviewer
should be able to reject a source claim without discarding the useful byte
facts or successful narrower scope. Failed hypotheses remain useful negative
evidence; they are not training gold. This keeps forward progress possible
without lowering acceptance gates or repeatedly starting from scratch.

After each coherent improvement, freeze and run one bounded live local-model
regression using the existing runner. Replayed known seeds measure reproducibility,
not new support. Keep failures and assistance visible.

Do not make the pre-existing runtime Halt97 disappear as part of this
architecture change. Its stale/unresolved behavior must be separately recovered
if it blocks a required delivery gate. Do not infer that all runtime tests pass
merely because the mixed-source target compiles.

The finish line advances through verified connected source and measured
transfer. Infrastructure completion alone cannot close the project.
