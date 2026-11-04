# Lost-Source Revival Factory
BYOD binary -> detect -> disasm -> evidence-linked same-language source recovery -> verification.
Any program with lost source: games, applications, firmware, drivers. Compilation and source recovery are tracked separately from behavioral verification.

## Scoped recovery prototype

### Connected text execution

The complete supported `FUN_249c_0037` path now executes, not just its
initialization prefix: shortstring copy, attribute escape state machine,
B800 text writes, both BIOS cursor calls, CRLF through the buffered writer/
dispatch/DOS chain, and the zero-error return.

Original execution and installed Pascal agree in44 real-console and44
file-output cases on all4000 screen bytes,256 object/buffer bytes,256 input
bytes, cursor/sticky status and the exact attempted service byte/count sequence.
Console CRLF advances the cursor to next row,column0; file output does not.
Buffered/CRLF panels separately check sticky/mode errors, repeated flushes,
zero counts and continuation after flush errors. Injected outcomes stay labeled
as mechanism tests, not observed DOS errors or short writes.

```sh
uv run python -m tools.liero_text_probe --entry text --service console --output /path/to/private-text-run
uv run python -m tools.liero_text_probe --replay --output /path/to/private-text-run
uv run python -m tools.liero_text_probe --entry writer --output /path/to/private-writer-run
```

Requires BYOD Liero, FPC, GNU assembler/linker and DOSBox. Use fresh output
directories. Runs seal source/method/image/corpus/trace snapshots; replay uses
immutable archived bytes without compilation, DOS or model execution.

**Extended limits work:**88 additional full-text console cases now check
row23/24 scrolling against the original, including every screen byte and
bottom-row spaces/attribute07. The CR/LF adapter lives in the installed runtime,
not only the test driver.

Nonzero04f4 now enters a checked **nonreturning**010f error scope: empty
descriptor/callback chains and closed input/output objects.28 original/Pascal
cases check error address/diagnostic bytes, all19 vector restorations and exit
request; host process exit status is checked independently. Unsupported cleanup
still rejects. Fixed an original fall-through omitted by the prior hex-word
draft: error addresses require four digits, not two.

The original MZ startup also executes through its real RETF to main. An
explicit post-return collector observes default output handle1, DS79f0 with
bufferDS7a70 and both37b3 slots. This is **original-only instrumented startup**,
not recovered Pascal startup or unmodified game execution.

```sh
uv run python -m tools.liero_text_probe --entry text --service scroll --output /path/to/private-scroll-run
uv run python -m tools.liero_cleanup_dispatch_probe --terminating --output /path/to/private-error-run
uv run python -m tools.liero_cleanup_dispatch_probe --terminating --replay --output /path/to/private-error-run
uv run python -m tools.liero_startup_clear_probe --full-return --output /path/to/private-startup-run
uv run python -m tools.liero_startup_clear_probe --full-return --replay --output /path/to/private-startup-run
```

**Open-output error continuation is now connected:**3711 flushes through
checked374d/37b3, then closes through37d3 even when the flush fails.40 original/
Pascal cases cover actual file success, actual invalid-handle6 and separately
injected write5/close6 outcomes. Three full0037-to-nonzero04f4-to010f cases
also agree, including both writes, close, diagnostic and termination. One uses
actual invalid-handle6; two are injected mechanisms. The original reports
`0300:0155`, correcting an earlier unmeasured0157 assumption.

```sh
uv run python -m tools.liero_cleanup_dispatch_probe --terminating --open-output --output /path/to/private-open-error-run
uv run python -m tools.liero_cleanup_dispatch_probe --terminating --open-output --text-error --output /path/to/private-text-error-run
uv run python -m tools.liero_cleanup_dispatch_probe --terminating --open-output --text-error --replay --output /path/to/private-text-error-run
```

These runs require empty descriptor/callback chains and checked default objects
with explicit method/vector/termination ports. The text-error screen/input
snapshot is taken at the first write, before diagnostics, not after them.
**Remaining:** actual descriptor/callback provenance and hardware progress,
redirected378e, arbitrary console/device effects, recovered Pascal startup and
native ABI. Real sound send/receive polling has no proven termination; a ready
port fixture does not discharge it. These have not been relabeled as complete.
1192 connected tests pass,3 expected failures; full Pascal target builds with40
warnings.
Post-change liveQwen3 regression passes56training+56terminal with one request;
same known assisted corpus, no demonstrated model-weight improvement.

### Earlier recovery and architecture milestones

See the [completion plan](docs/PROJECT_COMPLETION_PLAN.md) for the architecture
ownership boundaries and callee-first path to a connected Pascal subsystem,
then independently measured transfer and cross-project weight learning.
The selected archive refactor is tracked in
[RFC #1](https://github.com/yidaki53/LoSoRe/issues/1); it does not change source
acceptance or turn scoped observations into whole-program recovery.

Caller/source experiments now share immutable archive validation in
[`engine/evidence_archive.py`](engine/evidence_archive.py); historical formats
and routine-specific acceptance checks are preserved.567 connected tests pass
(3 existing expected failures), historical success/failure archives replay, and
the post-refactor live regression passes56/56training plus56/56terminal.
This is tool reliability, not additional recovered routines or changed weights.

Cursor dependency `FUN_249c_0000` now has an explicit column/row word interface
and logical page-zero cursor state. Original BIOS query/BDA observations and
the installed position projection agree16/16;65536 host word/SP-wrap cases pass.
This is not full BIOS/device/ABI parity. Reproduce the bounded observation:

```sh
uv run python -m tools.liero_nibble_caller --cursor --output /path/to/private-cursor-run
uv run python -m tools.liero_nibble_caller --cursor --replay --output /path/to/private-cursor-run
```

Original initialization now identifies conditional output callbacks: device
output uses37b3; redirected nondevice output uses378e with different short-write
handling. `FUN_24dd_37b3` now has installed Pascal for its buffer-reset and
DOS-write status behavior. Real DOS file/NUL/invalid-handle observations match
the scoped host projection in24cases;32 separately injected service cases check
successful short writes and errors. The service sees used=0 even on failure,
and successful short writes return zero, not378e's101. Each panel varies the
source segment independently of the object segment.

```sh
uv run python -m tools.liero_write_handler_probe --output /path/to/private-write-run
uv run python -m tools.liero_write_handler_probe --replay --output /path/to/private-write-run
```

Both output dispatchers now invoke the checked leaf: `396c` through slot20
and `397a` through slot24. Each passes24 real DOS and32 injected-service
cases, including sticky errors and the original leaf's change of BX to handle.
Input-refill and isolated synthetic-callback behavior remain separately tested.

```sh
uv run python -m tools.liero_write_handler_probe --dispatch flush --output /path/to/private-flush-run
uv run python -m tools.liero_write_handler_probe --dispatch optional --output /path/to/private-optional-run
uv run python -m tools.liero_write_handler_probe --replay --output /path/to/private-flush-run
```

These are human byte-backed service projections, not native ABI or whole-source
acceptance. Buffered writer3899, CRLF3930 and the supported full text path are
now composed above.
Redirected378e remains separate. Closed/open-object termination and the checked
integrated text-error scope are measured above, not universal error recovery.

Earlier integrated milestone: `FUN_249c_0013` now has installed SS-relative
Pascal in the existing target runtime, retaining its one-word interface.
The actual original shortstring-initialization caller prefix and installed body
match256/256 training and256/256 held-out full-state cases. All65536 byte pairs
also pass host arithmetic checks. Run/replay this bounded integration:

```sh
uv run python -m tools.liero_nibble_caller --output /path/to/private-caller-run
uv run python -m tools.liero_nibble_caller --replay --output /path/to/private-caller-run
```

Full target compiles; the existing runtime regression still has an unrelated
baseline Halt97 failure. Nonzero error handling, native ABI and normal-program
reachability remain unresolved. This installed body/real-prefix integration
is not full-Liero or cross-project model learning.

The existing runner now packages the supported **interpretation -> original-byte/
training checks -> typed Pascal lowering -> one terminal check -> review/export**
workflow. Supported leaves: packed copier `FUN_24dd_4141`, SS-byte arithmetic
`FUN_249c_0013`, register normalization `FUN_24dd_455e`.
It is an assisted recovery tool, not an autonomous whole-Liero reconstruction.

With BYOD Liero, FPC, GNU assembler/linker, DOSBox and installed local
Ollama `qwen3:14b`:

```sh
uv run python -m tools.liero_source_trial --prototype \
  --routine FUN_249c_0013 --output /path/to/private-arithmetic-run
uv run python -m tools.liero_source_trial \
  --output /path/to/private-arithmetic-run --export /path/to/private-export
uv run python -m tools.liero_source_trial \
  --validate-export --output /path/to/private-export
```

Use one fresh output directory per trial. Repeating `--prototype` with a complete
existing output **replays**, with no generation or terminal reexecution. Partial
archives are rejected and preserved. The preset selects Qwen3 and thinking/
8192tokens; the legacy CLI keeps its previous model/options.
Two interpretation requests maximum, three alternatives per request, no supplied
action tuple/body; static/original checks select the first complete training pass.
Failed interpretation exports remain failures, without compiled/generated stubs.

Exports contain exact Pascal, source/method/runtime/corpus hashes, raw proposals,
byte facts, full declared-state traces, assistance, review scope and outstanding
obligations. `source-review.json` can bind an explicit scoped review to the exact
candidate hash; missing review remains pending. Whole source, gold examples and
weights are never promoted by this workflow. Original executable/compiled
binaries are excluded; exports remain private BYOD evidence.

For the packed vertical slice, the existing caller tool now supports:

```sh
uv run python -m tools.liero_move_caller --packed \
  --from /path/to/passing-packed-run --output /path/to/private-caller-run
uv run python -m tools.liero_source_trial \
  --output /path/to/passing-packed-run --caller-from /path/to/private-caller-run \
  --export /path/to/private-packed-export
```

Measured state: three distinct earlier scoped candidates pass56/56 training and
56/56 terminal; actual packed caller composition passes12/12 and12/12.
The clean frozen preset demonstration passes **2/3**, with copier destination-
offset interpretation still failing before compilation; that failure is retained.
Earlier successful copying is not relabeled as a clean success. Static assistant
reviews are not user signoff. This is useful prototype infrastructure with an
explicit stability limit, not the proposed three-success clean acceptance gate.
No cross-project model-weight improvement or native/full-program acceptance.

## Same-language policy
The rebuild is **always written in the language the original was written in** (Turbo Pascal 7 for the Liero pilot). Detection (`tools/provenance.py` -> `config/toolchain.yaml`, with confidence) is the gate: `engine/draft.py` refuses to emit until the language is known, then emits that language. Porting verified source to a modern, more maintainable language is a **separate, later project** that consumes this project's output — it is explicitly out of scope here.

## Source recovery
The objective is to recover the original program's source structure from
available evidence, not to create a clone. A stripped binary cannot reveal
historical comments, formatting, original identifiers, or every source-level
type choice, so exact text recovery is not promised. Recovery status requires
reviewed evidence for each routine's ABI/signature, control flow, call targets,
state effects, and data references. Stubs, guessed behavior, and trivial
wrappers do not count as recovered logic.

For a target, initialize or synchronize its evidence ledger and inspect its
aggregate status:

```sh
make recovery-audit TARGET=liero
python3 -m engine.recovery --target liero --init \
  --output reports/liero-recovery.json
```

The per-routine ledger lives at `targets/<slug>/recovery.json`; edits to Pascal
source or assembly invalidate a source-recovery attestation until it is reviewed
again. The audit keeps source-recovered, evidence-accounted, body-present, and
assembly coverage separate. Compilation and behavioral verification remain
separate build/oracle results. The ledger's explicit reviewer attestations are
not a substitute for original-binary tests; they record the evidence and review
of reconstructed source.
The current Liero ledger covers known routine entries only; matching its 295
entries to the Ghidra export does not establish that every executable byte or
code/data boundary in the image has been found.

Full-census dependency triage now separates28 reviewed scopes,46 manual bodies,
130 callee-contract blockers,82 control/external blockers and9 unimplemented
leaves needing oracles. Run `uv run python -m tools.liero_frontier --output PATH`
to preserve original bytes, real relocation targets, dependency groups and
method hashes; add `--replay` to authenticate the archive. It does not promote
source or make all295 executable. The first frozen Qwen3:14b4141 trial used two
requests, produced no executable candidate and stopped at0/1 yield. See
[current recovery TODOs](docs/RECOVERY_TODO.md); no weight improvement is claimed.

The opt-in source trial `--typed-memory-guidance` (single4141 with
`--enforce-outputs`) freezes typed-pointer guidance and4096tokens. Same-model
live measurement produced complete JSON and copy loops but still no executable
candidate: forbidden unit wrappers and omitted observable state. Each coherent
improvement now requires a bounded live trial under [agents.md](agents.md), not
just unit tests; failures and baseline comparisons are preserved.

Single4141 also supports `--residual --interpretation-first`: competing model
memory hypotheses, original-byte/training checks and disclosed mechanical Pascal
lowering. Live Qwen3 and one installed coder14B comparison produced correct
training-memory actions but failed required citations, including one immutable
`--binding-from` completion each. No live Pascal/terminal acceptance followed.
The broader roadmap remains blocked, not completed; see
[explicit stage status](docs/RECOVERY_TODO.md).

Opt-in `--supplied-bindings` freezes human byte-backed citation facts for4141
interpretation-first trials without fixing behavioral choices. Its live trial
passed citation format but still proposed wrong memory actions. No recovery,
weight gain, second-project MVP or full reconstruction is claimed.

Subsequent `--thinking` trial (explicit local Ollama option,8192tokens) passed
4141 full-state training56/56 and terminal56/56 with a model interpretation and
disclosed mechanical Pascal; scoped review accepted, not native/whole source.
No separate reasoning trace returned or weight gain established.
Different-behavior near SS-byte leaf249c:0013 direct-source trial emitted forbidden
assembly and failed. Broader roadmap remains incomplete; these measurements do
not establish equal-method transfer or generalization.

Reviewed routine contracts can name explicit `callee_contracts` in
[the existing configuration](targets/liero/config/routine_contracts.json).
Drafting carries one hop of those scoped contracts into caller prompts,
including their premises and limitations, even without decompiler C.
Malformed/missing references fail explicitly; this does not resolve partial
callees, change the dependency scheduler or permit automatic source acceptance.

`make build TARGET=liero` compiles the same-language Pascal program (Free
Pascal `-Mtp` proxy in the `rev:dos-tp7` Docker image). `make verify TARGET=liero
ORACLE=dat-parity` runs the DAT parse->serialize round-trip and fixture selftest;
it does not verify function source. An empty oracle gate reports NOT verified,
never a vacuous PASS.

Own code: MIT (see LICENSE). No vendor bytes committed. `extracted/` gitignored.
Disc-gated tests skip-and-pass in CI.

## Current Liero recovery checkpoint

The project has a **bounded assisted-recovery PoC**, not automatic
whole-Liero recovery. See the [session handoff](CONTINUATION_SUMMARY.md),
[measured target evidence](targets/liero/docs/RECONSTRUCTION.md) and
[recovery TODOs](docs/RECOVERY_TODO.md) for current scope and next steps.

| Measured milestone | Outcome | Limit |
| --- | --- | --- |
| Automatic close repair | 8/8 training and 16/16 held-out calls | Developer-supplied branch sketch; scoped DOS adapter |
| Fresh refill proposal | 64/64 training and 32/32 held-out calls | Supplied topology; separate mutant repair is a software test |
| First constructor expansion | 17 compiled hypotheses, zero training passes | 0/1 slice yield; expansion stopped |
| Byte-constrained constructor repair | 514/514 training and 264/264 held-out cases | Known-slice debugging, not unseen-routine generalization |
| Frozen global initializer transfer | 4/18 bytes, no write facts | Preserved historical failure at `POP ES` |
| Shared segment/global rule repair | 17/18 bytes with explicit DS window; three original runs match 8192 bytes each | `RET` unresolved; original-only memory checks, not Pascal parity |
| Partial global memory projection | Generated Pascal matches all 8192 original bytes per existing dirty-memory context | Memory effects only; unresolved return/register/ABI obligations remain |
| Repeated puzzle passes | Changed premises reopen blocked pieces; unchanged failures are suppressed | Scoped frontier scheduling, not a whole-program solver or source acceptance |
| New controlled leaf trials (4905/3b22) | Controls pass 514/512 training cases; both raw and changed byte-constrained model strategies yield 0/2 | No held-out evaluation or promotion; 25% yield floor stops expansion |
| Restricted 4905 fill sketch | First request passes 514/514 training and 257/257 held-out memory cases | Byte-derived semantics and supplied loop topology; syntax mechanism only, zero new recoveries |
| 3b22 composition contract | Exact byte-derived prefix/string predictions match all 544 bytes in 584 training cases | Developer-authored known-slice shape; no model request/holdout or full ABI acceptance |
| 492c checked caller layout | Three instrumented MZ contexts agree with the Pascal clear projection across 8192 bytes each, with the startup ES store checked/composed separately | Original-only segment/stack observations; not unmodified startup, full ABI parity or new recovery |
| 1ec2:0000 dword-copy contract | 774 finite original/Pascal cases check all 544 arena bytes each, including truncated-count tails | Requires entry DF=0 and disjoint valid buffers; developer-authored known-manual-slice check, not learned recovery |
| 1ec2:086b signed-word source review | Complete 42-byte control-flow/source review plus all 65,536 signed-word return values matched | One additional reviewed source recovery; not full host/DOS ABI parity, normal-program reachability or learned recovery |
| 1ec2:0dc8 drawing source review | 53 nonwrapping arena cases; 74,892 grid writes agree with actual Pascal | Partial only; excluded far-offset-wrap control disagrees |
| Drawing engine retry | Two fixed local-model drafts: baseline compiles but has invalid host-pointer model; assisted fails Char-to-Byte typing | 0/2 eligible; no runtime/holdout pass, repair, promotion or verified improvement |
| Typed drawing mechanism | Fresh one-request sketch matches 46/46 training and 7/7 withheld-from-feedback development cases | Identical to supplied control; syntax mechanism only, no new recovery or learned improvement |
| Random-state source correction | Original-byte recurrence review and 1754 actual-source state/return cases pass after fixing the low-product increment | Both routines partial; actual caller DS/seed and full ABI remain unresolved, not learned recovery |
| Caller input/context propagation | Two original relocated calls bind DS:6684 buffer views; engine now carries scoped callee contracts into caller prompts | Allocation/DS/seed remain blocked; added context does not unlock generation or establish learned recovery |
| Allocator prerequisite | All65,536 size-helper inputs match original/Pascal; three exported segment-MOV directions corrected from original bytes | Existing accepted helper corroborated, not new recovery; allocator free-list/handler contracts remain blocked |
| Bounded nonempty allocator | One byte-derived Pascal model matches72/72 training and48/48 terminal original cases, all256 owned heap words each | Known one/two-node fixture; arbitrary topology, callbacks, real entry and full ABI remain unresolved; no model/weight improvement claim |
| Actual64000 allocator caller | Original startup/call/result stores match the unchanged Pascal projection in one observed context; all6010 protected globals checked | Instrumented endpoint only; actual empty/default premises and allocation origin established here, not later lifetime, failure cleanup or full ABI |
| Error-address translation | Byte-derived Pascal matches61/61 training and37/37 terminal original cases before016e;512 descriptor bytes and58 globals checked per case | Supplied bounded descriptor chains; real provenance, cleanup callbacks and failure termination remain unknown |
| Cleanup dispatch mechanism | 8 original/Pascal state cases check clear-before-transfer and far-return/reentry with a disclosed synthetic RETF callback | Not real callback recovery; exact installer/restorer prefixes identify the next target, whose callees/lifetime remain unresolved |
| Real cleanup port leaf | 512 fixed original/Pascal ready-path cases on an owned emulated PIC; nine exact-byte dependency regions and ten direct calls mapped | Not Liero sound-device parity or busy-path/callback recovery; actual device initialization and service outcomes remain unknown |
| Pending-error exchange source review | Complete seven-byte review plus all65,536 old-word inputs and repeated calls match actual target source after fixing mirrored AX/CF/ZF | One additional reviewed source body (28/295 total); sequential logical-global model, not native atomicity/full ABI or learned recovery |
| Whole-source model batch (40d6/3d68) | Raw and representation-constrained strategies both yield0/2;112 original training calls pass, but generated bodies fail or repeat invalid numeric-pointer emulation | No terminal evaluation, installation or weights;25% floor stops expansion. Existing manual drafts disclosed, not unseen-routine recovery |
| Known-source adapter calibration and assisted retry | Two supplied-body adapters each pass65536 scalar cases; assisted copy matches56/56 training memories but0/56 complete states; initializer fails | Still0/2 complete recoveries, no terminal test/weights; missing signature/clobber/RETF effects cannot be replaced by memory-only acceptance |
| Unimplemented move source assessment | Exact declaration/output gates and named training feedback added;48e1 original56/56 fixture states match, but two requests repeat one numeric-address proposal |0/1 accepted, no terminal evaluation/source/weights; manual28 current sources remain reusable within their checked contracts, not automated unknown recovery |
| Composed residual and7B QLoRA | One actual NF4 adapter job fits12GBVRAM; synthetic development improves to7/8 complete tasks,1920/2048 byte agreement |48e1 base/adapter still yield no accepted source; synthetic development is not untouched Liero transfer. Explicit experimental inference only; per-proposal fixture recall is not correctness probability |
| Heap initialization/callback | Original startup conditionally establishes equal free-list/sentinel; default callback is XOR AX,AX; RETF2 | MZ minimum guarantees no spare heap; later state preservation/capacity remain unresolved |
| CPU startup prerequisite | All three original00b1 paths preserve segments and balance stack under explicit real-mode/no-trap premises | Hardware class and constant2 Pascal parity remain unverified; later state/capacity still blocked |
| Instrumented initial heap | One original-only DOSBox run observes447360 spare bytes and the expected sentinel/limit/callback before0049 | Disclosed instrumentation, not normal-run allocation success, Pascal parity or later state lifetime |
| First original vector query | One frozen AH35/AL0 call returns F000:1060; required loop registers and6010 protected bytes unchanged | Finite instrumented endpoint only; remaining18 queries, universal service ABI and allocator lifetime unresolved |
| First vector-save bridge | One distinct frozen case stores F000:1060 and reaches vector2 input; four slot bytes plus6006 unchanged bytes checked | Stops before second query; startup-only finite evidence, not allocator or whole-loop acceptance |
| Second original vector query | One distinct frozen AH35/AL2 case returns0070:0008 matching IVT2; all6010 bytes including first saved slot unchanged | Stops before second pointer save; remaining17 queries, universal ABI and allocator lifetime unresolved |
| Second vector-save bridge | One frozen case stores0070:0008 and reaches vector1b input; all6010 bytes accounted, first slot intact | Stops before third service; no whole-loop, Pascal or allocator acceptance |
| Third original vector query | One frozen AH35/AL1b case returnsF000:1060 matching IVT1B; all6010 bytes including both saved slots unchanged | Stops before third save; remaining16 queries, universal ABI and allocator lifetime unresolved |

The composition-contract continuation passes **314 focused tests**, lint and
syntax checks. This is not a fresh whole-repository test count. No generated
candidate was installed, attested or promoted by these recent trials.
Earlier local LoRA training/inference smoke tests validate infrastructure,
not improved real Pascal recovery. Continual model improvement still needs
qualified cross-project data and a frozen binary-backed evaluation.

**Current follow-up:** typed 3b22 composition and bounded optimization were
implemented, but two native Python crashes interrupted the overnight trial.
All **2,037,760 completed stress comparisons** replay; the failed attempt remains
unknown, so the trial is **closed incomplete**, with no selection or holdout.
Four fixed diagnostic probes on the failing input passed; the intermittent
crash cause remains unresolved. **350 focused tests** pass.

**Latest bounded milestone:** the original MZ entry's first instruction calls
startup directly. A separate [startup clear contract](tools/liero_startup_clear_contract.py)
binds its relocated DS, near call/return, minimum loader allocation and
disjoint code/data/active-stack ranges for 492c. The clear writes 5932 bytes
inside the guaranteed 201,312-byte module allocation under explicit ordinary
DOS loader assumptions. **398 focused tests** pass. This is static path evidence,
not observed unmodified startup or full Pascal ABI parity; no recovery count,
source acceptance or promotion changes. Frozen trial methods remain unchanged.

**Latest execution check:** the [caller-layout probe](tools/liero_startup_clear_probe.py)
preserves the original entry, supported startup prefix and all clear bytes in
a disclosed instrumented MZ copy. Three fixed dirty seeds pass **24,576 bytes**
of guarded comparison. The two-byte startup ES save is independently checked
and explicitly composed into the Pascal result; the other 8190 bytes per case
are compared without normalization. Actual observed DS is not assumed to be CS.
**440 focused tests** pass. Traces, patches, method snapshots and a pre-execution
freeze are retained; replays are not additional independent evidence.

**New contract development:** [the dword-copy check](tools/liero_dword_copy_contract.py)
binds all 24 original bytes of `FUN_1ec2_0000`. Under explicit entry DF=0 it
copies `4 * (count div 4)` bytes, leaving the remainder untouched. Counts
0–257 and three dirty seeds pass **774 cases / 421,056 checked arena bytes**.
The historical manual body was not read or used, and remains unreviewed;
this is not blind-source transfer. **492 focused tests** pass. No shared frozen
rule or pilot was changed, and no source/example/ledger promotion occurred.

**Caller assessment:** [the exact call-site check](tools/liero_dword_copy_caller.py)
binds original `1000:94D7` and its MZ relocation. It passes count **50,000**
with source/destination pointers loaded from DS:6684h/65D7h, immediately after
the unreviewed `FUN_1000_5e66` call. DF=0, pointer allocations and nonaliasing
are therefore still **blocked**, not inferred from LES or the 256-byte leaf
corpus. **85 focused caller/leaf tests** pass; no new execution cases or
caller acceptance are claimed.

**Current recovery focus:** repetitive startup checks are now one batch,
not individual interrupt milestones. The known allocator slice now uses
byte-derived semantics rather than another unconstrained model proposal:

```sh
uv run python tools/liero_startup_clear_probe.py --vector-batch --output /absolute/fresh/batch
uv run python tools/liero_four_routine_pilot.py --allocator-puzzle \
  --output targets/liero/build/allocator-deduction/deductive-v1
uv run python tools/liero_four_routine_pilot.py --allocator-deduction \
  --allocator-deduction-replay \
  --output targets/liero/build/allocator-deduction/deductive-v1
```

The batch passed all19 original queries/saves, stopping before handler
installation. The deterministic allocator candidate passes **64/64 training
and48/48 terminal validation** against original execution under explicit
empty-free-list/default-callback premises. One candidate, zero model calls
or repairs. Source-bound replay does not rerun the terminal suite.
The existing puzzle engine checks this scoped piece and keeps actual caller
applicability, remaining list/callback paths and010f error-transfer ABI blocked.
This is a **known-slice mechanism**, not AI discovery, full allocator recovery
or normal-program acceptance. No candidate is installed/promoted.

Historically, the first live model returned only `"pascal"`; a separate format attempt
hit a backend schema error before generation. Both failures are preserved.
The corrected schema subsequently produced a complete candidate that compiled,
but **failed original-backed training**: incorrect allocator semantics and
runtime201 at case60. Saved partial output has8 matches/52 mismatches,
not a completed training pass; heldout never ran. Review rejects promotion.
The manually known four-case control is not model recovery.
**424 connected regressions pass**,10 historical original/frozen cases excluded.
Actual target proxy compilation passes with existing warnings; recovery
remains **27/295**. Next: nonempty-node ownership and callback contracts,
not repeated proposals, weight training or more per-query startup milestones.
See [the scoped evidence and blockers](targets/liero/docs/RECONSTRUCTION.md).

**Previous service check:** the [existing startup observer](tools/liero_startup_clear_probe.py)
supports `--third`: one frozen AH35/AL1b case returns **F000:1060**,
matching IVT1B, preserving required loop registers and all **6010 bytes**
including both saved slots. First two calls/stores are setup only; stop
before third save/remaining16 queries. **703 connected regressions pass**,
six frozen cases excluded; new case passed separately once. Scoped engine
context, no universal ABI/Pascal/allocator/source acceptance.
Recovery remains **27/295**. Next: third-save/fourth-input bridge, stopping
before the fourth service.
See [the scoped evidence](targets/liero/docs/RECONSTRUCTION.md).

**Previous bridge check:** the [existing startup observer](tools/liero_startup_clear_probe.py)
supports `--bridge --second`: one frozen case verifies the second pointer
save and reaches vector1b input without executing its service. All
**6010 bytes** accounted: four second-slot bytes predicted, other6006
unchanged, including the first slot. **638 connected regressions pass**,
five frozen observations excluded; new case passed separately once.
Recovery remains **27/295**. Next: thirdAH35/AL1b pre/post effects.
See [the scoped evidence](targets/liero/docs/RECONSTRUCTION.md).

**Previous service check:** the [existing startup observer](tools/liero_startup_clear_probe.py)
now measures the second AH35/AL2 call with the first saved slot intact.
One frozen case returns **0070:0008**, matching IVT2, and preserves required
loop registers and all **6010 protected bytes**. Stops before the second
pointer save and remaining17 queries. Engine context carries finite
startup-only evidence, not universal DOS ABI, Pascal parity or allocator
acceptance. **585 connected regressions pass**, with four frozen cases
excluded; the new case passed separately once. Recovery remains **27/295**.
Next: second pointer-save/third-input bridge, stopping before that service.
See [the scoped evidence](targets/liero/docs/RECONSTRUCTION.md).

**Previous bridge check:** the [existing startup observer](tools/liero_startup_clear_probe.py)
now verifies the first returned-pointer save and next-query input in one
distinct frozen case. All **6010 protected bytes** checked: four predicted
slot bytes, other6006 unchanged. Reaches AX3502/CX18/SI023b/DI7af4/DF0,
then stops before the second service. Engine context carries startup-only
finite evidence, not allocator or whole-loop acceptance. **528 connected
regressions pass**, with all three frozen observations excluded; the new
bridge case passed separately once. Recovery remains **27/295**. Next:
measure second AH35/AL2 effects, preserving the first saved slot.
See [the scoped evidence](targets/liero/docs/RECONSTRUCTION.md).

**Previous preservation gate:** the [existing startup observer](tools/liero_startup_clear_probe.py)
now measures the first original DOS AH35/AL0 call at0058 and stops005a,
before pointer saves. One frozen run returns F000:1060, preserves the
required loop registers and all **6010 protected bytes**. The engine
prompt carries this finite observation, not a universal service contract,
Pascal parity or allocator success. **492 connected regressions pass**,
with both frozen heap/service executions excluded; the new service case
passed separately once. Recovery remains **27/295**. Next: check the
first pointer save and next vector2 input, stopping at its service boundary.
See [the scoped evidence](targets/liero/docs/RECONSTRUCTION.md).

**Previous heap observation:** the existing instrumented probe now reaches
original heap initialization, stops before later interrupts and captures
PSP:2 before collector DOS calls. It observes **447360 spare bytes** and
the expected heap/callback state in one DOSBox context. This is initial
capacity—not successful allocation or later lifetime. Scoped measurements
reach the engine prompt. **383 connected tests pass**; source recovery
remains **27/295**. Next: trace the first later state-preservation blocker.
See [the scoped evidence](targets/liero/docs/RECONSTRUCTION.md).

**Previous startup follow-up:** all three CPU-detection paths preserve the
segments and stack needed by heap initialization, under explicit real-mode/
no-trap premises. The existing engine context now uses that checked
projection; hardware classification and the Pascal constant2 body remain
unverified. **280 connected tests pass**; source recovery remains **27/295**.
Next is an instrumented observation of the original heap/PSP state before
later interrupts—not a guessed allocation or another model run.
See [the scoped evidence](targets/liero/docs/RECONSTRUCTION.md).

**Previous heap follow-up:** original bytes identify the default callback
and conditional initial heap state; a fourth reversed exported segment move
was corrected. The MZ minimum allocation guarantees **zero spare heap**,
not capacity for the64000-byte request. These constraints now reach the
existing engine prompt. **240 connected tests pass**; source recovery
remains **27/295**. Next is the CPU/FLAGS-sensitive00b1 return/segment
contract, then actual allocation bounds and state preservation.
See [the scoped evidence](targets/liero/docs/RECONSTRUCTION.md).

**Previous allocator follow-up:** the already reviewed size helper matches
original execution for **all65,536 inputs**. A64000-byte request becomes
offset0 plus4000 paragraphs—not a proven allocation. Original bytes corrected
three reversed segment-register moves in the allocator listing. Scoped engine
contracts now state the first unresolved free-list and callback prerequisites.
**285 focused tests pass**; source recovery remains **27/295**. Next:
establish heap initialization and callback provenance before accepting buffers.

**Previous engine follow-up:** checked caller inputs now reach the existing
drafting engine alongside explicit scoped callee contracts. Two original calls
use DS:6684 buffer views, the second offset by160; both require a sufficient
common nonwrap base<=14978 plus valid allocation/nonaliasing bounds. Startup's
64000-byte request identifies the unresolved allocator028a->0353, not proof
of a safe buffer. The scheduler correctly keeps0895 blocked. **283 focused
tests pass**; source count stays **27/295**, four partial. No new model run or
learning claim. Next is the allocator contract, not another long search.

**Previous source follow-up:** reviewed the random generator before its scaling
wrapper and fixed the historical [Pascal body](targets/liero/src/FUN_24dd_46b1.inc)
incrementing the old seed instead of the low product. Original recurrence is
`(state * $08088405 + 1) mod 2^32`; the wrapper returns the unsigned product's
high32 bits. [Source-bound tests](tests/test_liero_random_source.py) pass
**1754 scoped cases**, including full32-bit rollover; archived old source
mismatches1681/1753. Actual caller bounds5/2 now constrain conditional color
to83/84. **238 focused tests pass** and full target compiles. Current audit:
**27/295 source recoveries(9.15%), four partial,34 host passes,0 full
original-binary passes**. No model learning or whole-routine promotion.
Next is actual caller DS/seed and buffer provenance, not another long run.

**Previous mechanism follow-up:** the existing pilot now renders a closed,
type-safe drawing sketch and rejects anything other than exact renderer output
before execution. A fresh single model proposal matched **46/46 training and
7/7 withheld-from-feedback cases**. It was identical to the pre-run developer
control, so its output was reused—not independent recovery evidence. The
offset-wrap limitation remains. **399 focused tests pass**, full target
compiles, and source counts remain **27/295, two partial**. This validates the
supplied syntax mechanism, not learned semantics. Next is the unresolved
random-state dependency and actual caller-buffer provenance, not a larger run.

**Previous follow-up:** the callee-free
[drawing leaf](targets/liero/src/FUN_1ec2_0dc8.inc) now has a checked
nonwrapping memory contract consumed by the existing drafting engine.
The [source-bound test](tests/test_liero_draw_source.py) checks all **3,474,256
arena bytes** in 53 scoped cases and preserves an excluded offset-wrap
counterexample. Current audit: **27/295 recovered (9.15%), two partial,
32 host passes**. **194 focused tests pass** and full target compiles.
The bounded two-draft engine retry yielded **no eligible candidate**, so no
verified performance improvement is claimed; original caller provenance and
full ABI remain blocked. See the [measured evidence](targets/liero/docs/RECONSTRUCTION.md)
for the frozen budgets, compiler failures and safety stop.

**Previous connected milestone:** original calls in `FUN_1ec2_0895` now bind
the reviewed sign contract to wrapped X/Y coordinate differences. Caller
recovery remains blocked by unreviewed random/drawing dependencies; no guessed
callee behavior was installed. The planned fallback independently reviewed
the actual [sign sibling](targets/liero/src/FUN_1ec2_09bd.inc), including its own
original bytes and all **65,536 return inputs**. Current audit: **27/295 source
recoveries (9.15%)**, one partial, 31 host passes. **136 focused tests** pass
and the full target compiles. This is manual source review, not learned transfer.
Next: resolve the caller's drawing leaf/dependencies before returning to it.

**Previous source milestone:** the existing
[signed-word leaf](targets/liero/src/FUN_1ec2_086b.inc) is now reviewed against
all 42 original bytes and all three signed return paths. Its actual Pascal
body/helper matches original returns for **all 65,536 signed-word inputs**;
the unused argument is statically unread. The ledger now has **26 valid
source recoveries / 295 entries (8.81%)**, plus the one partial copy routine.
This is explicit source review, not promotion from finite testing alone.
**134 focused tests** pass and the full target compiles. Full original-machine
ABI/reachability remains unverified; no training promotion or new model result.

**Earlier Pascal deliverable:** the existing target
[copy body](targets/liero/src/FUN_1ec2_0000.inc) and its real runtime helper now
pass the same **774 original-byte memory cases**, rather than testing only a
separate projection. The body has descriptive arguments and an explicit
DF=0/bounds oracle label; the ledger records **one partially recoverable
routine**, not a whole-routine attestation. Accepted source recoveries remain
**25/295 (8.47%) at that checkpoint**. **133 focused source/caller/ledger tests** pass and the full
target compiles. The broad Pascal runtime suite still stops before this leaf
at unrelated `Halt(97)` (or a pre-existing range error with `-Cr`); no full-suite
pass is claimed.

The frozen complete-byte vocabulary matches only the two already tested
routines among 294 exported routine files (the separate startup entry is not
in that denominator). No new eligible transfer was found. **Next:** establish
the preceding `FUN_1000_5e66` contract in callee-first order before revisiting
this caller's DF and pointer provenance. New contract
development above does not retroactively change the frozen transfer result. No more
unchanged overnight retries, manual-body seeds or relabeling new rules as
untouched transfer. Known-slice checks do not meet the expansion-yield gate.

To persist the static contract and supporting method snapshots in a fresh directory:

```sh
uv run python tools/liero_startup_clear_contract.py --output /path/to/new-contract
uv run python tools/liero_startup_clear_probe.py --output /path/to/new-layout-run
uv run python tools/liero_dword_copy_contract.py --output /path/to/new-copy-run
uv run python tools/liero_dword_copy_caller.py --output /path/to/new-caller-report
```

For bounded unattended **known-slice search**, the existing pilot supports:

```sh
uv run python -u tools/liero_four_routine_pilot.py --leaf-trials \
  --leaf-byte-constraints --leaf-string-sketch --optimise-loop-search \
  --overnight-hours 8 --model qwen2.5-coder:14b-instruct \
  --output targets/liero/build/overnight-composition
```

It compares a typed model sketch and its supplied `for`/`while` neighbor on
identical seeded original-byte training batches, selecting only a fully passing
candidate before one terminal holdout. `progress.json`, `search.json`, logs and
per-batch traces retain results and failures. It stops on fixed coverage,
time/resource budgets or no eligible candidates; no idle retries, target-source
installation, training promotion or frontier expansion. A passing known-slice
search does not prove original structure or unseen recovery.

An interrupted overnight stress run can be continued only after its original
process has stopped and no heldout was attempted:

```sh
uv run python -X faulthandler tools/liero_overnight_resume.py \
  --prior targets/liero/build/overnight-composition \
  --output targets/liero/build/overnight-composition-continued
```

This authenticates the unchanged frozen pilot and replays contiguous completed
comparisons, then isolates each new comparison in a short-lived worker.
It preserves consumed budgets and the candidate/ranking/one-holdout policy.
Unknown/incomplete outcomes, worker crashes and duplicate resumes fail visibly;
there is no automatic retry or source promotion. A frozen-method change needs
separate review, not bypassing the replay gate.

## Quickstart
```sh
make init && make test        # green with no target data
python3 tools/new_target.py --slug liero --kind game  # scaffold targets/liero
# drop a legally-owned copy in extracted/liero/, then:
make pipeline TARGET=liero    # provenance -> ingest -> learn -> draft -> verify -> improve -> optional train
make pipeline TARGET=stickman LIMIT=5  # cap the initial LLM translation batch
make build TARGET=liero       # compile the same-language program (Docker FPC proxy)
make report                   # per-target + learning stats
```
`make pipeline` first runs a strict `preflight` and stops before changing
staged files when a required input or tool is unavailable. Use
`make preflight TARGET=liero` to inspect readiness independently. Individual
disc-gated stages still report `SKIP` when their inputs are absent.
`LSR_GHIDRA_PROJ` selects a writable scratch root (otherwise
`$TMPDIR/lsr_proj_<target>` is used); generated Ghidra project paths must not
contain spaces. Each real ingest attempt records its binary hash, tool paths,
export counts, status, and captured log under
`targets/<target>/ingest-runs/`. New exports replace staged assembly only after
metadata and assembly inventories validate, so a failed extraction preserves
the last usable export. The manifest includes detected Ghidra/Java versions
when available.

`make pipeline` = `preflight` -> `provenance` (detect compiler/language/confidence) -> `ingest`
(Ghidra headless -> asm/+decomp/) -> `learn` (mine toolchain recipe + few-shot
examples into `knowledge/`) -> `draft` (emit the detected language; Pascal for
Liero, decompiler C kept as `//` reference) -> `verify` -> `improve` -> a
threshold-gated local model training check. Training is skipped unless a local
base model is configured and enough new eligible training pairs exist.
`LIMIT=N` bounds the initial LLM translation batch; other functions still get
compiling assembly-residue skeletons. This is useful for large targets before
committing to a full sequential drafting run.

The improvement loop retries a bounded batch of assembly-backed Pascal
functions, feeding compiler diagnostics and the previous candidate back into
the next draft. It changes one routine at a time, compiles the full target
after each change, and restores the previous source if the build regresses.
Use `make improve TARGET=liero` to run it directly. Optional bounds and model
selection can be passed as `MAX_ITERATIONS`, `SATURATION_WINDOW`,
`FUNCTIONS_PER_ITERATION`, `MAX_ATTEMPTS_PER_FUNCTION`, `MODEL`, and `LLM`
make variables. Without explicit model settings, it uses local Ollama at
`http://localhost:11434` with `qwen2.5-coder:14b-instruct-q4_K_M`; override
these defaults with `LSR_LLM_ENDPOINT` and `LSR_LLM_MODEL`. Its summary reports
generated files, meaningful Pascal bodies, compilable routines, whole-target
build status, and binary-verified functions separately. The FPC `-Mtp` build
is a compile check, not behavioral parity; `dat-parity` checks LIERO.DAT and
never counts as a verified function.

Each improve invocation stores hash-bound run state and per-routine attempts
in `targets/<target>/runs/<run-id>.json`. Resume a run with the same inputs
and settings using `make improve TARGET=liero RESUME_RUN=<run-id>` (or
`python3 engine/improve_loop.py --target liero --resume-run <run-id>`).
Resume rejects changed assembly, binary, configuration, or improve settings.
Completed candidates are checked against their recorded source hash, and
rejected attempts retain compiler diagnostics for the next draft. Each attempt
persists a pre-generation snapshot of the target Pascal sources. If generation
is interrupted, resuming restores that snapshot and records the interrupted
attempt before retrying.

## Learning (target-over-target)
`engine/knowledge.py` + `engine/learn.py` keep a committed store
`knowledge/knowledge.json`. Each learned target adds, per (compiler, platform)
toolchain: calling conventions, image base, and instruction idioms. Legacy
assembly-to-decompiler-C pairs can be used as a separately labeled,
lower-confidence training task. They are never treated as verified Pascal or
as evidence that reconstructed Pascal is correct.

Function-level oracle passes add a separate `verified_pascal_examples` corpus.
Each record keeps its assembly, optional decompiler pseudocode, Pascal body,
toolchain, target, and oracle provenance. Pascal drafting retrieves examples
from other targets using assembly anchors and calling-convention similarity;
the raw instructions remain authoritative when they conflict with the lossy
decompiler reference. File/format checks such as `dat-parity` do not certify
function drafts and therefore never add training examples.

`engine/fact_graph.py` provides a separate versioned graph for evidence-linked
partial facts. It extracts routine entries, basic blocks, branch/fall-through
edges, direct/indirect call observations, and evidence-linked BP-relative frame
operand observations from Ghidra assembly. Frame observations preserve the
signed displacement and exact instruction/operand text; they do not classify
slots as parameters or locals, or identify source variables. Each occurrence
has its own observation node, so routine reads/writes do not appear as
contradictory values for a shared slot. A limited set of unambiguous
instructions (including `MOV`, `LDS`, `LES`, `IN`, `OUT`, `CMP`, `TEST`, stack
operations, common read-modify-write instructions, and supported multiply/
divide forms) also receives derived read/write access facts linked to the raw
operand and assembly evidence. Direct register operands of the same supported
instructions are recorded independently; `LDS`/`LES` classify their explicit
operands but not the implicit `DS`/`ES` loads. `IN`/`OUT` classify explicit
port/data registers but not implicit flag effects. `SHLD`/`SHRD` classify the
destination as read/write and the other explicit operands as reads.
Register-indirect call targets are classified as reads, without assuming
caller/callee register-clobber conventions.
One-operand 8/16-bit `MUL`,
`IMUL`, `DIV`, and `IDIV` forms include documented implicit accumulator and
high-word register effects; multi-operand `IMUL` classifies only its explicit
destination and source operands. Unsupported operand widths and 32-bit
register aliases remain unclassified. 8/16-bit `MOVS`, `LODS`, `STOS`, `CMPS`,
`SCAS`, `INS`, and `OUTS` string forms model their index/data registers and,
for repeat-prefixed forms, `CX`. The `MOVSD` dword data form is supported when
the listing shows 16-bit `SI`/`DI` addressing; other 32-bit address-register
forms remain unmodeled. String direction-flag and condition effects also
remain unmodeled. Explicit x86-16 storage overlaps (for
example `AL` within `AX`) are represented as separate architecture-evidence
edges; those edges do not propagate access facts. Unsupported instructions
and frame-address calculations such as `LEA` remain unclassified. Supported
frame accesses produce block use-before-definition and definition summaries, then a
CFG fixed-point analysis records live-in/live-out slot sets across branches
and loops. The analysis is limited to the supported frame accesses and does
not claim source-level variable identities or lifetimes. The same analysis
tracks direct and explicitly modeled implicit register accesses as physical
storage bit ranges, respecting partial-register definitions and omitting
unmodeled implicit instruction and call effects. `JCXZ` reads `CX`; `JECXZ`
reads all 32 bits of `ECX`. `LOOP`, `LOOPE`/`LOOPZ`, and `LOOPNE`/`LOOPNZ`
read and update `CX`. The conditional `LOOP` forms also read `ZF`; these
effects participate in register and flag liveness. A separate condition-flag
analysis records flag reads for supported conditional branches and effects
for `CMP`, `TEST`, `ADD`, `ADC`, `SUB`, `SBB`, `NEG`, `AND`, `OR`, `XOR`,
`INC`, `DEC`, `CLC`/`STC`/`CMC`, and the `SAL`/`SAR`/`SHL`/`SHR` and
`RCL`/`RCR`/`ROL`/`ROR` families, then solves flag liveness across the CFG.
Known zero shift counts preserve flags; unknown counts are conservatively
modeled as possibly preserving each affected flag. `MUL`/`IMUL` define
`CF`/`OF` and leave the other status flags undefined; `DIV`/`IDIV` leave all
status flags undefined. Undefined results are tracked as clobbers, not as
source-level values. `CMPSB`/`CMPSW` and `SCASB`/`SCASW` define the status
flags when executed. Their supported `REP`/`REPE`/`REPZ`/`REPNE`/`REPNZ`
forms conservatively model each flag as read/write because a zero initial
count preserves prior flag values. `LAHF` and `SAHF` record evidence-linked
transfers between `CF`, `PF`, `AF`, `ZF`, `SF` and their corresponding bit
positions in `AH`; `SAHF` leaves `OF` untouched. Register and flag liveness
remain separate analyses, so these transfer facts do not imply cross-domain
liveness propagation.
`TEST` marks `AF` as clobbered rather than defined; unsupported instruction
flag effects remain unknown. Each result links to parsed block listings and
CFG evidence. The graph
reports conflicting facts and unresolved calls, and propagates facts only
across explicitly evidenced `same_value` edges. Derived facts retain their
evidence and support links but remain non-oracular, never `oracle-verified`.
The improvement scheduler uses the graph for its existing direct-call
dependency map and includes evidence-linked dependency blockers in its
summary. Unknown call targets are reported separately and do not
automatically block callers. The graph does not use hypotheses to unblock
callers, attest source, or train model weights.

### Optional local fine-tuning

The pipeline uses Hugging Face Transformers + PEFT/LoRA locally. Install the
optional dependencies and point to a local causal-language-model directory:

```sh
uv sync --extra dev --extra training
export LSR_TRAIN_MODEL=/path/to/local/model
export LSR_TRAIN_THRESHOLD=64  # optional; default is 64 new unique pairs
make pipeline TARGET=liero
```

The corpus combines function-level oracle-verified assembly-to-Pascal pairs with
legacy assembly-to-Ghidra-C pairs. Legacy pairs are collected from
`knowledge/knowledge.json` and matching `targets/*/asm/*.s` and
`targets/*/decomp/*.c` files (up to 32 per target); decompiler failures and
format-only records are excluded, and exact duplicate pairs are deduplicated.
Every exported JSONL record has explicit `task`, `source_type`, `trust_status`,
and `oracle` metadata. Legacy C supervision is labeled `legacy-unverified`;
only verified Pascal examples carry an oracle.

Corpus eligibility in the training implementation is not permission to
promote a new experiment. The latest scoped pilot/static reports do not
automatically enter that corpus; their unresolved ABI/caller obligations
remain explicit. Held-out-target language-model loss and binary-backed
recovery success are different metrics.

Automatic training triggers after the configured count of new, unique pairs
(verified Pascal plus legacy C) is reached. The corpus must include at least two
targets; a whole target is held out for validation to reduce project leakage.
Adapters are versioned under `.lsr/adapters/` and record their supported tasks.
Pascal drafting only activates an adapter trained for assembly-to-Pascal;
training on legacy C alone cannot certify or silently alter Pascal output.
The base model and adapter are loaded with local-only paths; no project data or
model weights are sent to a hosted service by this training path. Existing LLM
endpoints remain a fallback when no task-compatible adapter is activated.

Useful commands:

```sh
uv run python -m engine.model_training --target liero --readiness
make train-export TARGET=liero              # write training_data/liero.jsonl
make train-now TARGET=liero                 # train immediately (requires >=2 targets)
LSR_TRAIN_THRESHOLD=32 make train TARGET=liero
```

For explicitly bounded experiments, `engine.model_training.train_adapter`
also accepts `quantized=True`, `experimental=True`, an explicit
`development_target`, and `max_length`. This uses4-bit NF4 QLoRA on CUDA;
experimental manifests have `activation_allowed=False` even if loss improves.
`tools.liero_source_trial.synthetic_residual_dataset` creates separately labeled
compiler-backed FPC examples, not verified Liero or TP7 training pairs.

The source-trial CLI supports explicit quantized base/adapter comparisons:

```sh
uv run --extra training python -m tools.liero_source_trial \
  --routine FUN_24dd_48e1 --residual --enforce-outputs \
  --local-base /path/to/pinned/transformers/model \
  --local-adapter /path/to/experimental/adapter --output /path/to/new/frozen-run
```

Omit `--local-adapter` to test the same base. This explicit path never falls back
to Ollama on loading/inference failure. `--residual` supplies a scoped ABI wrapper
and requires a declaration-free model memory body; it currently supports48e1
only. Freeze comparisons before execution and retain source/runtime/model hashes.
Each evaluated proposal reports required-case recall; unexecuted proposals and
whole-routine correctness probability remain unmeasured.

For an interpretation-first Ollama trial on the same unresolved routine:

```sh
uv run python -m tools.liero_source_trial \
  --routine FUN_24dd_48e1 --residual --enforce-outputs \
  --interpretation-first --model qwen3:14b \
  --training-from /path/to/authenticated/unevaluated-training-run \
  --output /path/to/new/frozen-run
```

This freezes at most two interpretation requests with three competing hypotheses
per request, followed by at most two Pascal requests. Hypotheses enumerate memory
traversal alternatives and cite instruction addresses; this search vocabulary is
disclosed assistance. Exact-byte constraints and complete original training
records check them before code generation. Interpretations retain conflicts,
memory recall and counterexamples separately; matching memory does not excuse
missing instruction bindings. Terminal data never repairs interpretations.
This mode requires Ollama, residual48e1 and no calibration context. Saved runs
replay without model requests; use `--historical` after method changes.

If such an archive contains a memory-matching, action-compatible hypothesis
blocked only by citations, add `--binding-from /path/to/prior-interpretation-run`
and set `--training-from` to that same archive. This authenticates and freezes
the first eligible prior hypothesis, then makes exactly one evidence-only
request before at most two Pascal requests. The response cannot change memory
actions. This is disclosed citation completion, not a fresh semantic recovery;
the old trial remains blocked under its original rules. The citation checker
checks address presence, not the truth of model-written explanatory prose.
Already evaluated terminal outcomes and chains of completion retries are refused.

Alternatively, once a selected checked interpretation exists but model-written
Pascal is invalid, use `--lowering-from /path/to/checked-interpretation-run`
with `--residual --enforce-outputs --training-from` that same archive (omit
`--interpretation-first` and inference options). This supports only the checked
48e1 traversal: human-authored typed indexed loops and the existing scoped ABI
wrapper. It freezes one candidate, makes zero model requests and performs the
same complete-state training/single-terminal checks. Provenance explicitly says
mechanical lowering, not model-generated source or weight improvement.
Terminal-exposed predecessors and lowering-retry chains are rejected. A passing
fixture composition still requires source review and caller/ABI obligations;
it is never automatically installed or promoted to training.

The original three-byte move caller can be tested independently of fixture entry
SI/DI assumptions:

```sh
uv run python -m tools.liero_move_caller \
  --from /path/to/checked-lowering-run --output /path/to/new/caller-run
uv run python -m tools.liero_move_caller --replay --output /path/to/caller-run
```

This authenticates1000:05f9..062e and the actual MZ relocation at062c, then runs
unchanged caller/callee bytes in an allocated DOS code block. Source and
destination are derived from the caller's DS-relative arguments, not arbitrary
entrySI/DI. One typed composition,12 training cases and one12-case terminal
suite cover owned bounds, full arena and declared registers/flags/stack.
No model request or automatic source/training promotion occurs. Injected frame,
lookup and memory premises do not prove the preceding prologue or whole caller's
normal-program reachability. Replay is read-only and verifies saved identities.

Add `--prologue` for the separately seeded05eb-entry success-path composition.
It authenticates the original stack-check0530, both far-call MZ relocations,
and the caller's near `LEAVE; RET2` tail. An external bridge supplies a real
near-call frame; the original prologue establishes BP and locals. Minimum-stack
cell values include exact success equality. Failure dispatch010f is statically
identified but never treated as returning or accepted. The harness-only unwind
after062e is not the unexecuted caller remainder. `--replay` reads the mode from
the saved freeze; no new original run is performed.

`--readiness` is read-only and needs no model or ML dependencies. It reports
unique marked-verified Pascal pairs/projects separately from noisy C, discounts
previously attempted pairs, and lists source-review and behavioral-evaluation
requirements. It does not revalidate source attestations or change existing
training/activation behavior. Its Pascal threshold is an advisory corpus check,
not proof that 64 examples suffice for learning.
On2026-11-03 the current selector finds **0 verified Pascal pairs and81 noisy
C pairs**. The mixed-corpus automatic threshold can be met by noisy C alone;
this is not evidence that Pascal weights can improve. Token-loss validation
used to select the adapter is development evidence, not an untouched behavioral
test. Require equal-budget base/retrieval/adapted recovery comparisons on
project/family-disjoint terminal tasks and retention checks before claiming
or promoting a weight improvement.

Research-inspired design choices include assembly-aligned evidence rather than
pseudocode-only prompting, feedback-driven refinement, and target-level
validation. See [ASAP](https://arxiv.org/abs/2610.06900),
[AutoDecompiler](https://arxiv.org/abs/2606.16162),
[CodeInverter](https://arxiv.org/abs/2503.07215), and the
[PEFT LoRA guide](https://huggingface.co/docs/peft/main/developer_guides/lora).

## Layout
`targets/<slug>/{src,include,asm,config,tools,docs}/ engine/ compilers/ reports/ tests/ knowledge/`

## Oracles (strongest first)
byte-exact > relocation-aware > round-trip .bin->src->.bin > format/trace parity.
`dat-parity` (real today): DAT parse->serialize round-trip + fixture selftest.
See `engine/verify.py` and `docs/ORACLES.md`.

## Canon
sm64, isledecomp/isle (MSVC4.2+ReproBit), adonis-singh/re4, sm64ds crackloop, open-spyro+maspsx, Francesco149/openrecet, pathologic_re. Full citations: ../EPIC3_ABANDONWARE_REVIVAL_PLAN.md
