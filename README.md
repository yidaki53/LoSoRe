# Lost-Source Revival Factory
BYOD binary -> detect -> disasm -> evidence-linked same-language source recovery -> verification.
Any program with lost source: games, applications, firmware, drivers. Compilation and source recovery are tracked separately from behavioral verification.

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

The latest shared-rule milestone passes **184 focused tests**, lint and
syntax checks. This is not a fresh whole-repository test count. No generated
candidate was installed, attested or promoted by these recent trials.
Earlier local LoRA training/inference smoke tests validate infrastructure,
not improved real Pascal recovery. Continual model improvement still needs
qualified cross-project data and a frozen binary-backed evaluation.

**Next:** establish the remaining return/caller contract for `FUN_24dd_492c`
under explicit segment and aliasing assumptions, then freeze the method
before one untouched-by-this-method callee-free slice. Reuse the existing
runner, probes, ledger and fact graph; do not start a larger run, model sweep
or graph rebuild merely because known-slice repair passed.

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
make train-export TARGET=liero              # write training_data/liero.jsonl
make train-now TARGET=liero                 # train immediately (requires >=2 targets)
LSR_TRAIN_THRESHOLD=32 make train TARGET=liero
```

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
