# Oracles — strongest first
1. byte-exact: rebuilt bytes == original (reccmp/asm-differ).
2. relocation-aware: equal modulo addresses/relocs.
3. round-trip: .bin->src->.bin identical with original compiler (pathologic_re pattern).
4. trace-parity: Frida draw/call traces equal (openrecet pattern).
Every function record stores which oracle passed. No pass = not decompiled.

Only a passing oracle entry that maps to a real `asm/<function>.s` and
`src/<function>.inc` pair can promote Pascal into cross-project memory. A
format-level check such as `dat-parity` verifies the format implementation,
not unrelated function bodies, and must not seed Pascal retrieval or training.
The LoRA trainer additionally holds out complete targets during evaluation.

## Current evidence boundary

The recent automatic close/refill trials establish a narrow assisted-recovery
PoC under developer-supplied sketches. Constructor repair is a changed-strategy
known-slice result. The latest global-clear check executes original bytes
only; no Pascal candidate, complete ABI or normal-program equivalence is
certified by its 8192-byte guarded-memory comparisons.

Keep compilation, CFG similarity, static prefix coverage, scoped parity,
review attestations and language-model validation loss separate. None permits
unconditional promotion from these experiments. The explicit DS window is
a caller precondition; `RET` remains unsupported. See
[current target evidence](../targets/liero/docs/RECONSTRUCTION.md) and
[next-step gates](RECOVERY_TODO.md).

## Oracle-gated drafting for the checked string comparator

The improve loop can use the original-executable routine probe as a strict
feedback gate for the checked `FUN_24dd_3f86` contract:

```sh
uv run python engine/improve_loop.py \
  --target liero \
  --fn FUN_24dd_3f86 \
  --function-oracle liero-compare-routine-probe \
  --oracle none \
  --localized-repair \
  --max-iterations 5 \
  --max-attempts-per-function 2 \
  --temperature 0
```

`FUN_24dd_3f86` is currently marked source-recovered in the main worktree, so
this command there will skip it. Live generation trials must use a disposable
copy with only this routine reset to an unreviewed skeleton; never reset the
checked repository source to make a model trial eligible. The bounded
comparator trial recorded in `targets/liero/docs/RECONSTRUCTION.md` did not
meet its PoC success bar. Later close/refill sketch trials are separate
bounded PoC results, not a successful comparator run or an MVP claim.

With `--localized-repair`, the first attempt is a normal candidate draft. After
an original-oracle failure, the retry asks for replacement statements only
inside the unique start/end anchors in that routine's checked contract. The
surrounding candidate source is preserved, and malformed full-routine output
is rejected. The option is restricted to this routine oracle and a maximum of
two attempts; ambiguous or missing anchors block the repair rather than
expanding the patch or guessing a region.

Each draft is generated and built in an isolated target copy. Only the selected
include is eligible for installation, and only after the saved comparator
report is validated as `passed` and the installed target still builds. A
`failed` comparison is retained with per-case mismatch feedback for a bounded
retry. A skipped, missing or invalid report blocks the run; it is never treated
as a pass. In routine-oracle runs, a repeated candidate hash is recorded and
stops the run instead of spending the remaining attempts on identical output.
`--oracle none` avoids running the unrelated target-format oracle.
For routine-oracle runs, prompts, completions and sanitizer candidates are
captured under `targets/liero/runs/<run-id>.generations/`; the run record stores
their hashes, model, temperature, and the previous candidate hash. This makes
retry diversity and delivery of repair context auditable without relying on
terminal logs.

The run summary reports `functions_scoped_oracle_passed` separately from
`functions_verified`. These nine fixtures cover only the checked ZF/CF,
far-call stack-balance and tested-memory non-mutation observations. A scoped
pass does not establish universal routine equivalence, attest source recovery,
or promote a knowledge/training example.

## Scoped original-versus-Pascal checks

`constructor-parity` is a deliberately narrower oracle for
`FUN_24dd_3639`. Run:

```sh
uv run python engine/verify.py --target liero --oracle constructor-parity
```

It executes checked original bytes under DOSBox and the actual reconstructed
constructor under host FPC over 778 fixed guarded-memory cases. Results,
inputs, traces, candidate source snapshots and tool hashes are retained in a
new `targets/liero/build/constructor-parity/<run-id>/` directory.
The comparator checks all input/object/guard bytes, original argument
cleanup, and one explicitly normalized relocated method-segment word.

Successful checks are reported separately as scoped differential evidence.
They do **not** enter the knowledge store, promote training examples, attest
recovered source, or increment the whole-routine original-binary count.
The result does not establish normal-program startup, universal equivalence
or host-versus-original ABI parity. Missing tools fail explicitly; missing
BYOD inputs skip explicitly.

Recovery audits replay the saved byte comparison and check current input,
source and artifact hashes. Changed or incomplete evidence is reported as
invalid, not reused as a pass. Raw bytes without the recognized scoped
contract cannot certify a candidate. The conventional build directory is
the discovery location; custom output roots must be validated explicitly.

The verifier also emits `constraints.json`, demonstrating conditional
propagation of the constructor's checked buffer-capacity field to the
same-object input-open entry. Derived constraints remain scoped and do not
certify the receiving routine. See [the whole-program recovery
method](RECOVERY_METHOD.md) for hypotheses, confidence and conflict handling.

### Shared six-word copy entries

The bounded copy probe compares `FUN_24dd_0582` and `FUN_24dd_05e8`
against hash-bound original bytes under DOSBox, using host FPC for the
current Pascal includes and shared runtime. Its fixed training and held-out
suites each contain four cases across the two entries. Reports retain
source snapshots, original/candidate traces, source hashes and per-case
memory/register/defined CF/ZF/DF checks.

Recovery audits discover reports at
`targets/liero/build/copy-parity/*/result.json`. They replay each report and
require both current includes and the shared runtime to match the saved
candidate hashes. Historical candidates, modified scope metadata and changed
sources cannot count as current passes. Missing BYOD inputs explicitly skip;
invalid evidence is reported with a reason. Cases are counted per routine,
and invalid multi-routine reports are counted once per report.

To run the current sources without another model request, use a new output
directory for each suite:

```python
from pathlib import Path
from tools.liero_copy_routine_probe import run_probe, validate_saved_report

for suite in ("training", "heldout"):
    output = Path("targets/liero/build/copy-parity") / f"new-run-{suite}"
    run_probe(output, suite=suite)
    validate_saved_report(output)
```

These are scoped differential passes only: they do not attest routine-wide
source recovery, increment whole-routine original-binary verification, or
promote retrieval/training examples. Controlled COM segment/register state
is not normal-program startup evidence.

### Four-routine model pilot

```sh
uv run python tools/liero_four_routine_pilot.py --output <new-empty-directory>
```

This fixed constructor/comparator/refill/close panel uses the existing
binary-backed probes, disjoint training/held-out fixtures, and separate
control/candidate source snapshots. Reviewed controls must pass first.
Each routine has at most four model requests; duplicate candidates stop.
Only training diagnostics feed retries, and a training-passing candidate is
selected once for held-out evaluation. All raw responses and rejected
compiler outputs are retained; actual compiler diagnostics feed the next
prompt. Model service errors explicitly block rather than count as passes.

The measured first panel yielded zero passes: all five unique candidates
submitted to FPC failed compilation. No candidate reached behavioral or
held-out testing. It therefore hit the 25% stop floor and does not authorize
a larger run. See the target reconstruction notes for exact counts,
output/interface failures, the measured feedback limitation and subsequent
tested hardening. No source/ledger/training promotion occurs.

An optional **single close-routine** follow-up reuses manually recovered
same-target examples:

```sh
uv run python tools/liero_four_routine_pilot.py \
  --routine close --recovered-examples --output <new-empty-directory>
```

Examples must pass the current recovery audit's source/hash and recorded
behavior gates. Every pilot routine is excluded to avoid self-example
leakage. The existing structural retriever ranks at most three examples;
their hashes and exact prompt content are retained. This is an ephemeral
retrieval view, not promotion to the cross-project verified corpus. Examples
are labeled with their actual static-review/host-test scope, not as binary
equivalence. The generated close callback/interface is checked before FPC.
The measured follow-up still rejected all four proposals for inline assembly;
no compilation or candidate held-out evaluation occurred. Reuse is supported,
but a measurable benefit from it has not yet been established.

Add `--constrained-close` to that single-routine command to use a strict JSON
conditional sketch instead of free-form Pascal. The model selects the loaded
word offset, comparison, threshold and branch returns; a deterministic renderer
fixes syntax and callback wiring, **not** the chosen behavior. The human-supplied
single-word-load/conditional topology limits the hypothesis space and must
not be presented as general decompilation. Invalid values are rejected, not
silently corrected. The schema, raw responses, sketch and rendered source are
retained with the existing binary-backed reports.

The measured constrained trial compiled one unique candidate but failed all
eight training calls because the branch returns were reversed. Its retry
duplicated that sketch despite training counterexamples, so the run stopped
after two requests without candidate held-out testing. Compilation success
is a resolved output blocker only; no recovery or training promotion follows.

The subsequent `--routine close --branch-repair-seed <failed-proposal-directory>`
mode tests exactly the unchanged sketch and the same sketch with swapped
return expressions. The seed must have a replay-validated failed close report
and matching original executable, raw model response, sketch and measured
source. Fresh separate snapshots supply training evidence for both hypotheses;
only a training pass gates held-out execution. No model calls or source
installation occur.

Measured branch-swap result: unchanged failed 8/8 training calls; swapped
passed 8/8 training and 8/8 held-out calls. This is human-localized scoped
repair, not a new autonomous model success or a larger-run readiness claim.
The same handle lifecycle is reused in held-out, with changed payload only.
Reports remain outside automatic source/knowledge/training promotion.

The later `--routine close --automatic-close-repair` mode automatically
consumes a fresh failed sketch, replay-checks its training evidence and tests
the branch swap without repeating the seed oracle. It uses `heldout-v2`:
the original lifecycle plus invalid 6/7/255/32768/65534 handles followed by
live/repeated/FFFF close. Legacy `heldout` remains payload-only, preserving
its original scope. The first training-passing selection ends the run after
one held-out suite, including on failure; no held-out-guided retry is allowed.
The standalone probe also exposes the stronger suite via
`uv run python tools/liero_read_handler_probe.py --handler close --suite heldout-v2 --output <new-empty-directory>`.

`--routine read --automatic-read-repair` applies the same replay/selection
loop to a constrained one-read/state-update sketch. It permits five one-field
alternatives (error clearing, successful count value, return value), leaving
the four model-selected word offsets unchanged. Invalid sketch values are
rejected. Oversized reads abort at the host adapter's reserved-buffer boundary.
Four model requests per routine and source-hash deduplication bound both
modes. Raw proposals, rendered sources, lineage and all oracle reports are
retained; no recovery, retrieval, training or model-weight promotion occurs.

Measured automatic close: one failed model proposal, automatic swap, 8/8
training and 16/16 held-out calls passed. Independent refill: one fresh model
proposal passed 64/64 training and 32/32 held-out calls without needing repair.
A deliberate refill error-clear mutant separately exercises automatic repair
in integration tests; it is not counted as another model success. These are
developer-defined sketch searches, not unrestricted decompilation or a
population-based evolutionary algorithm. See
[the scoped PoC results](../targets/liero/docs/RECONSTRUCTION.md#automatic-bounded-recovery-poc-close-and-refill)
for commands, evidence identities and unresolved limitations.

The next bounded expansion adds
`--routine constructor --automatic-constructor-repair`. It reuses the existing
514/264 guarded constructor corpus without changing acceptance checks.
Its supplied initialization/copy topology leaves ten semantic fields to the
model; at most four one-field name-cap/prefix/NUL alternatives follow a
replay-validated training failure. Constants are not silently corrected.
The prompt explicitly accounts for the logical setup-segment mapping.
Constructor feedback preserves valid JSON with representative byte
differences and explicit omitted counts.

Measured expansion: both controls passed, but four model proposals and
thirteen repair alternatives all failed training. All nineteen reports
replayed; no generated candidate reached held-out or promotion.
The **0/1** slice yield stops expansion below the 25% floor. A deliberately
off-by-one integration fixture verifies the mechanism but is not counted
as a model recovery. See
[the constructor expansion record](../targets/liero/docs/RECONSTRUCTION.md#bounded-constructor-expansion-no-new-automatic-pass).

A changed-strategy constructor mode,
`--routine constructor --constructor-instruction-constraints`, derives seven
initialization fields from supported original-byte transfer rules and actual
MZ fixups. It restricts those fields in the model schema and rejects raw
contradictions unchanged. The supported prefix, exact bytes, relative
provenance and unknown suffix are saved in `instruction-facts.json`;
`validate_constructor_instruction_facts(path, root)` re-derives rather than
trusting stored claims. The remaining name cap/prefix/NUL choices still
require the existing oracle, and the four repair alternatives are unchanged.

Measured: one fresh proposal passed 2/514 training cases; the existing
length-prefix toggle passed 514/514 training and 264/264 held-out cases.
All eight oracle reports and both instruction-fact reports replayed.
This is a scoped changed-strategy result on the already-investigated routine,
**not** untouched-routine generalization or proof that over-specialization
has disappeared. See
[the instruction-constrained results](../targets/liero/docs/RECONSTRUCTION.md#constructor-instruction-constraints-changed-strategy-scoped-pass).

The evidence-only `--prefix-transfer-routine <exported-routine>` mode freezes
the current prefix rules and records original bytes, rule/listing snapshots,
provenance and unsupported residue without generating a candidate.
`validate_prefix_transfer(root, output)` re-derives and checks all three
snapshots. Unknown suffixes return a nonzero CLI exit; even a fully decoded
prefix is not a routine recovery. Entry object/source assumptions must not
be transferred to a different routine without supporting evidence.

The first distinct-routine check, callee-free `FUN_24dd_492c`, decodes
4/18 bytes and stops at `POP ES`. It establishes no write facts and no new
routine pass. No rule change or bespoke mutation was made within that
frozen evaluation.
This is an explicit static-method portability limitation, not end-to-end
generalization. See
[the frozen transfer record](../targets/liero/docs/RECONSTRUCTION.md#frozen-prefix-transfer-distinct-global-initializer-remains-unsupported).

The subsequent shared-rule repair supports segment push/pop provenance,
unsigned word subtraction/shift and bounded global stores. The optional
`--prefix-data-window START END` is available only with prefix-transfer
mode and accepts decimal or `0x` offsets. It supplies a nonempty half-open
entry-DS writable, nonaliasing range within `[0,65536)`, not a discovered
allocation. Reports retain the range; replay rejects invalid or changed
bounds. Unknown segments, stack bindings, store direction or out-of-window
writes stop analysis.

On `FUN_24dd_492c`, the new rules stop before stores at 15/18 bytes without
a window. With `--prefix-data-window 0x6000 0x8000` they derive 2966 zero
words at `[6426h,7B52h)` and stop at `RET` at 17/18 bytes, still returning
a nonzero exit and no routine recovery. Three original-byte DOSBox COM
contexts match all 8192 guarded memory bytes and observed SP balance.
The tests save hash-bound traces and measurement reports; these finite
original-only observations do not establish Pascal parity or full ABI.
See [the shared-rule measurement](../targets/liero/docs/RECONSTRUCTION.md#shared-segmentglobal-rules-bounded-original-memory-check).

### Input refill leaf

The next connected leaf, `FUN_24dd_375e` (original entry `24DD:375E`), has
a standalone bounded comparator:

```sh
uv run python tools/liero_read_handler_probe.py \
  --output targets/liero/build/read-handler-parity/<new-run-id>
```

It reuses the original file probe's constructor/open/setup code, then calls
the original refill handler seven times with a valid DOS handle and once with
handle `FFFF`. Twelve fixtures produce 96 compared calls: binary file lengths
0, 1, 127, 128, 129, 255, 256, 257 and 769, plus capacities 0, 1 and 7.
Incoming position/count fields are deliberately dirtied before each call.
The comparator checks returned AX and all 512 object/destination bytes against
both the actual Pascal include and an independent file/memory contract.
There is no pointer or handle normalization.

The Pascal body accepts an explicit DOS-read adapter and a resolved buffer
pointer. The host adapter implements valid host file reads and DOS error 6 for
the deliberately invalid handle; unexpected host I/O errors abort. This tests
the refill algorithm, not a reconstruction of DOS, the original register
interface, arbitrary far-pointer layouts or every DOS error.

Saved reports retain source snapshots, tools, images, traces and hashes.
`tools.liero_read_handler_probe.validate_saved_report()` checks current
dependencies and replays the comparisons; a stored pass alone is not evidence.
This leaf is absent from the existing 295-entry inventory and remains a
standalone candidate: it does not yet enter the verifier's scoped counters,
replace the unresolved open wrapper, or promote source/training/ledger state.

### Input close leaf

The same runner now compares `FUN_24dd_37d3` (original entry `24DD:37D3`):

```sh
uv run python tools/liero_read_handler_probe.py --handler close \
  --output targets/liero/build/close-handler-parity/<new-run-id>
```

After original constructor/open/setup, the harness dirties the position/count
words, fills the 128-byte buffer with `A5` and the separate destination with
`5A`, and snapshots that state. It then tests handles 0 through 4, closes the
live file handle, repeats that close, and tests `FFFF`: eight calls in total.
Original and Pascal returns must be 0 for the first six calls and DOS error 6
for the last two. The entire 512-byte state must stay unchanged except for
the harness-selected handle, and original `RETF 4` must restore SP.

The Pascal candidate takes an explicit DOS-close adapter. The host runner
maps one actual open file to the captured DOS handle, closes it on the first
service call, and returns error 6 for its closed or unmapped handles.
Unexpected host close errors abort. Host-only call counts check that reserved
handles 0..4 never invoke the adapter; these counts are not an original
interrupt trace. The byte-checked original stream independently contains the
unsigned `handle <= 4` guard.

A compiled candidate changing that guard to `handle <= 3` is rejected.
Both handler modes use the same snapshot/build/replay infrastructure. Updating
shared sources invalidates older saved results; regenerate rather than
relabeling them as current. Both leaves remain standalone, outside the
295-entry inventory and automatic scoped counters, with no ledger/training
promotion or claim of complete caller/DOS/TP7 ABI parity.

### Indexed method dispatcher

The same runner now checks the actual `FUN_24dd_374d` Pascal body:

```sh
uv run python tools/liero_read_handler_probe.py --handler dispatch \
  --output targets/liero/build/dispatch-parity/<new-run-id>
```

Three fixed fixtures (empty, binary short, 256-byte input) each execute eight
dispatches: read, close, repeated close, reserved-handle close, invalid read,
and three synthetic callback calls. Read and close use original leaf bytes on
the DOS side and the actual checked Pascal leaf includes on the host side.
Setup/open remain original-only fixtures.

The global error starts at `55AA`. Returned AX values are
`0,0,6,0,6,1234,0,FFFF`; the expected global errors are
`55AA,55AA,6,6,6,1234,1234,FFFF`. A zero method result must not clear an
earlier error. Return AX, zero flag, restored `ES:DI`, balanced original near
return and all 512 object/destination bytes are checked. The harness stores
AX/ES/DI/ZF in the first eight destination bytes solely as instrumentation.

The synthetic callback is installed in otherwise-null slot `18h` for this
probe only. It increments object word `+06`, clobbers `ES:DI`, and returns
`1234`, `0`, then `FFFF`. It is not a recovered game method. The real dispatch
instructions remain unchanged; the synthetic callback resides at harness
offset `0400`, below the checked original helper at `04F4`.

The existing parameterless Pascal entry and forward declaration remain
compatible. A host resolver callback supplies the explicit method/argument
mapping; an unset resolver raises runtime error 211, and the bounded probe
resolver rejects unknown slots, segments and method offsets. No setup,
output-mode or arbitrary far method is given a guessed successful return.
Compiled mutants clearing sticky status or failing either pointer restoration
are rejected. This is scoped composition, not full register/flag/TP7 ABI,
normal startup, source-attestation or training promotion. Unlike the two leaf
entries, this dispatcher is already inventoried, but its standalone report is
not yet integrated into automatic scoped-audit counters.

### Input-only setup

The same runner now checks the input-mode subset of `FUN_24dd_420c`:

```sh
uv run python tools/liero_read_handler_probe.py --handler setup \
  --output targets/liero/build/setup-parity/<new-run-id>
```

Four fixtures each make eight calls: an existing binary file, empty filename,
missing file, and missing directory (`NO_DIR/INPUT.TXT`). An original open
first establishes the fixture's segment and reusable DOS handle, then the
harness closes it before running setup. Each call starts with handle `BEEF`,
position/count `55AA/FFFF` and method-slot bytes `A5`. Successful handles are
closed between calls by probe instrumentation.

The candidate is explicitly input-mode-only (`D7B1`). Output modes raise
runtime error 211 instead of receiving guessed implementations. Input setup
clears the handle before attempting open. On error it returns the service
error and leaves prior method slots intact. On success it installs read
`375E`, null slot `18h`, and close `37D3` using the captured code segment.
It does not reset buffer position/count or mode; those are wrapper effects.
An empty filename skips open **and the subsequent handle store**, leaving
handle zero while still installing the input method slots.

The recorded DOSBox build returns error **2** for both missing fixtures.
The host adapter checks the actual filesystem and maps these two outcomes
to that observed value, not a universal DOS error rule. Successful host
read-only opens use the captured reusable DOS handle as their logical
identity; this is not a test of DOS handle allocation. Unknown host I/O
errors abort. A probe-only counter in the first destination word checks the
empty-name bypass; it is not an interrupt trace.

All 32 calls compare full 512-byte states, returned AX, original preserved
DS/SS and `RETF 4` balance. Compiled mutants spuriously clearing position or
turning an open failure into success are rejected. The initial hypothesis
that empty names store `3D00` was rejected by original execution; the corrected
candidate stores zero. A missing-directory error of 3 was likewise not observed
on this backend. Both failed assumptions remain documented, not normalized
away. Setup is outside the current inventory/scoped counters and no whole
routine, source, training or normal-startup promotion occurs.

### Input open/reopen/close composition

The shared runner's `open` mode composes actual Pascal bodies for the input
entry `36B7`, common open `36C4`, close wrapper `3711`, dispatcher `374D`,
input setup `420C` and close leaf `37D3`:

```sh
uv run python tools/liero_read_handler_probe.py --handler open \
  --output targets/liero/build/open-parity/<new-run-id>
```

Three fixtures (empty, binary short, 256-byte input) each exercise eight
transitions: reopen a live input, reopen after forced close error, reopen to
a missing file, open from closed after failure, forced failing close, close
an already-closed object, invalid-mode open, and empty-name open from closed.
Harness-only cleanup closes live resources before installing invalid handles;
these forced failures are not normal-game observations.

Full 512-byte states and global statuses are compared independently against
the expected transitions. Expected global errors are
`55AA,6,2,2,6,67,66,66`; modes are
`D7B1,D7B1,D7B0,D7B1,D7B0,D7B0,1234,D7B1`. Position/count are dirtied before
every operation and reset only by accepted open attempts. Original DS/SS and
`RETF 4` balance remain checked; wrapper register return values are not compared.

Successful setup leaves earlier errors untouched. Common open decides its
final mode from the dispatcher's zero flag, not whether global status is zero.
Reopen attempts setup even after a close error. Close marks input closed even
when the close leaf returns an error. Empty-name setup succeeds with handle
zero and installs input methods, but does not erase the earlier error.

The host setup driver is reused with a compile-time wrapper-composition mode;
its resolver invokes actual setup/close bodies and rejects unknown methods.
Host object parameters now use `Pointer` rather than the decompiler's guessed
`Longint` or parameterless signatures. Corresponding forward declarations and
the output-entry binding were updated together and compile-checked. Logical
`RegisterES:DI` must identify that resolved host object; this is not TP7 ABI
parity. Current/requested output modes raise runtime error 211 before wrapper
side effects. The output entry forwards its object and requests `D7B2`, so it
reaches that explicit unsupported-mode gate rather than a guessed output path.

Three compiled mutants are rejected: testing old global status instead of
the current zero flag, stopping reopen after close error, and retaining input
mode after failed close. Rejection can be a differential mismatch or an
explicit resource-lifecycle assertion in the host adapter, never a partial
successful report. No ledger/training/scoped-counter promotion follows.

### String-read and line-skip buffer callbacks

```sh
uv run python tools/liero_read_handler_probe.py --handler callbacks --output targets/liero/build/line-callbacks-parity/RUN_ID
```

Oracle: `isolated_original_vs_host_pascal_line_callbacks`. The existing
byte-bound COM runner invokes original near callbacks `24DD:39AB` (copy a
string prefix) and `24DD:390E` (skip a line prefix), alternating eight calls
per fixture. Actual Pascal bodies use explicit logical buffer offsets, not
guessed decompiler signatures. Original open/refill supplies the buffer;
neither is replaced with a host implementation in this mode.

The fixed 14-fixture corpus covers one-byte and 128-byte buffers, counts
`0/1/7/255`, CR alone/first/last, CRLF, CR followed by a non-LF, repeated CR,
`1A` first/interior, embedded NUL/LF/FF, and count/terminator boundary ties.
Every call starts at buffer offset zero with a fresh A5 destination.
All 512 object/destination bytes, returned AX, remaining CX, relative SI/DI,
original near-return stack balance and DS/SS are compared. The destination's
last eight bytes are labeled harness instrumentation for SI/DI/CX/AX;
relative offsets are computed explicitly, not blanket pointer masking.

Count zero wraps to FFFF after the first ordinary copied byte. Count
exhaustion consumes the last copied byte and returns zero; CR/1A stops the
reader without consuming the delimiter. Bare LF and NUL are ordinary bytes.
Skip leaves `1A` unconsumed and returns zero. Skip consumes CR and an optional
following LF; a non-LF remains unconsumed. A CR at buffer end returns `3923`;
buffer exhaustion without a terminator returns `390E` for skip or `39AB`
for read. These are continuation tokens, not terminal EOF classifications.

The initial source/model hypotheses incorrectly backed up SI on count
exhaustion and consumed `1A` in skip. Original execution rejected both;
the exact short-branch targets distinguish a shared XOR/RET from a preceding
DEC SI. Three compiled mutants challenge delimiter rewind, optional LF and
zero-count wrap. Partial/tampered outputs and stored comparison changes fail
saved-report replay.

Scope is **nonempty, contiguous, nonaliasing buffers with DF clear**, supplied
host memory and starting offset zero. Empty/nil source inputs fail explicitly
in the candidate instead of inventing an empty-buffer result. Flags and
other register clobbers, arbitrary far-pointer layouts, `3923`'s next phase
and whole-program behavior remain unproved. New include bodies are
probe-compiled candidates, not additions to the 295-routine inventory or
whole-program recovery ledger. No training or automatic scoped-counter
promotion follows.

### Input buffer dispatcher and refill continuation

```sh
uv run python tools/liero_read_handler_probe.py --handler buffer --output targets/liero/build/buffer-parity/RUN_ID
```

Oracle: `isolated_original_vs_host_pascal_buffer_dispatch`. Actual Pascal
`37EC` composes actual refill bridge `396C`, read leaf `375E`, read callback
`39AB`, skip callback `390E` and continuation `3923`. The latter's bytes were
already covered by the checked skip region: it reads one byte, consumes LF,
backs up for any other byte and returns zero. This phase is invoked only
after a successful refill following CR at the preceding buffer's end.

Eleven fixed fixtures produce 88 original/Pascal calls: six alternating
read/skip operations (read limits 7/111/1), a sticky-error no-op, then
invalid-mode error `68`. Fixtures cover empty/repeated EOF, CR at byte127
followed by LF/non-LF/EOF, multiple refills during skip, read continuation
across refill, 1A, embedded NUL/LF/FF and forced invalid read handle6.
Full 512-byte states, sticky status, callback AX, remaining CX, relative
SI/DI and ZF are checked. Object bytes32..41 are explicitly reserved
harness instrumentation for SI/DI/CX/AX/ZF, not candidate object writes.
Original DS/SS and near-RET balance are also required.

The refill bridge calls the actual read leaf, not a copied read summary.
The host adapter performs real reads and maps only the deliberate invalid
handle to DOS6; unexpected I/O aborts. The dispatcher preserves the current
callback AX and remaining CX/DI across refill, including a transition from
390E to3923. Sticky errors bypass mode/buffer work; an invalid input mode
sets68. Refill failure empties the buffer, retains its bytes and leaves the
callback token in AX, with ZF set from the final position/count comparison.
Thus AX can remain nonzero at EOF or read failure while ZF is true.

Host object/source/destination pointers must resolve the original logical
far addresses and are bound explicitly by the probe. SI/DI mirrors are
buffer-relative, not native far addresses. The read slot must be375E with
the exact captured code segment; unknown callbacks, unknown method segments,
nil source, malformed counts or absent service adapters abort with runtime211.
Three compiled mutants break optional LF handling, callback preservation or
sticky-error gating; all are rejected. Replay also rejects changed comparison
fields, truncated outputs and broken original stack snapshots.

The main target include order now supplies the actual dependency bodies
before37EC, preserving existing parameterless forwards for37EC/396C.
The whole target compiles without running it; unresolved draft/result and
unbound-adapter warnings remain explicit. Compilation is not executable
recovery.

### Reader and line-skip wrappers

```sh
uv run python tools/liero_read_handler_probe.py --handler wrappers --output targets/liero/build/wrapper-parity/RUN_ID
```

Oracle: `isolated_original_vs_host_pascal_reader_skip_wrappers`. Two fixed
fixtures run the original reader `3988` and skip wrapper `38F0` twice each
(eight calls), including CR/LF split across the 128-byte refill boundary.
All512 object/destination bytes and global status are compared after each
call. Reader return leaves SP at `FDF4` from baseline `FDF8`; skip consumes
the retained far object argument and restores SP to `FDF8`.

The host probe records that retained argument logically; it does not claim
TP7 ABI parity. The optional `+18` method path is exercised with a synthetic
far method returning zero or `1234`; only the fixture's exact `0400:CS`
method and object address are accepted. `1234` becomes sticky global status
on skip and is preserved by following calls. Remaining buffered bytes model
the original ZF-clear branch only for this measured wrapper sequence; no
general dispatcher-flag equivalence follows.

Replay hashes the harness, code and inputs and recomputes each comparison.
Malformed or tampered output, a compiled reader mutant and an unsupported
method slot are rejected. This is bounded input-mode composition over the
already checked dispatcher/refill group, not arbitrary far-call support,
normal startup, universal wrapper equivalence or whole-routine recovery.
No recovery-count, ledger or training promotion follows.
