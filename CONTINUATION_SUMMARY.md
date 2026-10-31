# LoSoRe recovery handoff

## Current checkpoint: 2026-10-31

Objective: recover evidence-accounted Pascal source from Liero's original
binary, not a clone. The latest batch is complete: shared segment/global
rules, original-memory measurements and documentation passed validation.
There is no active model run or newly installed candidate.

Read these sources first:

- [Recovery TODOs](docs/RECOVERY_TODO.md): completed milestones, ordered
  suggestions, acceptance checks and stop conditions.
- [Recovery method](docs/RECOVERY_METHOD.md): reusable evidence rules.
- [Liero reconstruction](targets/liero/docs/RECONSTRUCTION.md): commands,
  experiment history, hashes, scopes and failures.
- [Oracle contracts](docs/ORACLES.md): what each check establishes.
- [Executable census](targets/liero/docs/BINARY_CENSUS.md): historical
  inventory/coverage baseline, not complete code discovery.

### What changed in this session

- Separated compilation, routine review, binary-backed scoped comparisons
  and format checks. Rejected or unchanged model output cannot borrow a
  successful baseline build. Raw proposals, errors and source lineage are
  retained rather than diagnosing failures from a success-shaped summary.
- Built cross-project retrieval/local LoRA infrastructure, evidence-linked
  fact/constraint handling, isolated resumable trials and original-byte
  DOSBox probes. Infrastructure smoke tests do not demonstrate better
  recovery on real held-out projects.
- Established manual and composed file-input contracts before callers.
  Dirty states, delimiter/refill boundaries, sticky errors, retained
  arguments, indirect method slots and exact branch tails matter.
- Automatic close repair passed 8/8 training and 16/16 held-out calls.
  A fresh refill proposal passed 64/64 and 32/32. These are bounded
  developer-sketch PoCs, not unrestricted automatic decompilation.
- Constructor expansion failed: 17 compiled hypotheses, zero training
  passes. Byte-derived initialization constraints plus the existing
  length-prefix alternative subsequently passed 514/514 training and
  264/264 held-out cases. This changed strategy repairs a known slice;
  neither trial establishes model-weight overfitting or its absence.
- Frozen rules initially decoded 4/18 global-initializer bytes and stopped
  at `POP ES`. Shared rules now decode 15/18 without a data window, or
  17/18 with entry DS `[6000h,8000h)` explicitly writable/nonaliasing.
  They derive zeroing `[6426h,7B52h)` (2966 words / 5932 bytes).
- Three original-only COM runs seeded with A5h/5Ah/FFh match all 8192
  observed memory bytes each, including 2260 unchanged outside-range bytes.
  SP before/after is FFFEh. `RET` and full ABI/caller safety are unresolved.
  No Pascal candidate was compared by this latest memory test.

Latest validation: **184 focused tests**, Ruff, formatting, syntax and scoped
diff checks pass. Final static snapshots rederive; three distinct archived
measurements' hashes and traces replay. Four protected Pascal body hashes
are unchanged. No recent source attestation, training promotion or new
routine recovery is claimed.

Final evidence directories in the session workspace:

- `liero-global-range-492c-20261031-final/`
- `liero-global-clear-measurements-20261031-final/`

Final instruction-rule SHA-256:
`490ec7b9bdb952b7b3c860bcb1451c43fb924748020ed204e1c6de858e9e996e`.
Earlier frozen/development evidence remains separate; do not relabel it
with this identity. Session evidence is not committed BYOD data.

### Next bounded milestone

Establish the remaining return/caller contract for `FUN_24dd_492c` using
original evidence, then measure Pascal effects under those same explicit
preconditions. Do not mark `RET` supported solely to remove residue.
Freeze the resulting method before selecting one untouched-by-this-method
callee-free slice. Use the [TODO gates](docs/RECOVERY_TODO.md); larger runs,
toolchain migration, broad graph rebuilds and training sweeps are deferred.

## Historical CFG-normalization note (not current recovery acceptance)

The note below is retained as historical scoring/toolchain context, not a
freshly reproduced result. Its phrases "verified functions", "fully pinned",
"production-ready" and "complete" must not be interpreted as binary-backed
source recovery. FPC `-Mtp` is a compatibility build, not the historical
Borland TP7 compiler or a DOS ABI oracle. CFG similarity scores cannot
establish semantic equivalence, and the historical numbers below were not
rerun in the current milestone.

### LoSoRe CFG Normalization: historical summary

## Approach A: 16-bit Compiler (Turbo Pascal 7 / Free Pascal Cross-Compile)

### Status: ✅ Fully Pinched to TP7 — Already in Place

**Toolchain already pins to Turbo Pascal 7:**
- `targets/liero-dos/config/toolchain.yaml`: `compiler: turbo-pascal-7`, `compiler_confidence: high`
- Docker image: `rev:dos-tp7` (550MB, specifically for TP7 DOS development)
- Compilation flag: `fpc -Mtp` (Turbo Pascal mode)
- Pascal template: `{$MODE TP}` directive embedded in generated code
- LLM prompt: "You are reverse-engineering a **Turbo Pascal 7 DOS program** (Liero v1.33)"

**Verification:**
- The `e6_match.py` compilation flow at line 1020 runs:
  ```
  docker run --rm -v {wdir}:/src -w /src rev:dos-tp7 fpc -Mtp /src/{fn}_cand.pas
  ```
- Type system constrained to TP7-compatible types: Byte/Char/Word/Integer/Longint/Boolean/Pointer
- No Result var, no goto, no Exit(v), no asm blocks (TP7 rules)

**Limitation**: Decompiled `.pas` files in `targets/liero-dos/pascal/` use some modern syntax, but the output pipeline is constrained to TP7.

### Approach B: CFG + Mnemonic Normalization (Implemented)

### Status: ✅ Fully Implemented and Tested

### Results on 12 verified functions — +3.4 pp avg improvement (5.1% relative):

| Function | Raw match_pct | Norm match_pct | Δ |
|---|---|---|---|
| FUN_24dd_3ed3 | 67.5% | 72.0% | +4.5% |
| FUN_249c_0180 | 68.3% | 72.4% | +4.1% |
| FUN_24dd_2e94 | 65.0% | 69.1% | +4.1% |
| FUN_24dd_3360 | 66.2% | 70.1% | +3.9% |
| FUN_1ec2_0d5d | 67.7% | 71.4% | +3.7% |
| FUN_1e7d_018a | 58.6% | 61.7% | +3.1% |
| FUN_24dd_4905 | 69.4% | 69.5% | +0.1% |
| FUN_1000_5e66 | 73.2% | 75.1% | +1.9% |
| FUN_1ec2_00d0 | 69.8% | 72.3% | +2.5% |
| FUN_24dd_3711 | 63.4% | 67.8% | +4.4% |
| FUN_2971_65df | 61.2% | 64.9% | +3.7% |
| FUN_24dd_0548 | 68.7% | 71.2% | +2.5% |

### Summary Statistics (all 12 functions):
- **Raw avg match_pct: 67.3%**
- **Norm avg match_pct: 70.7%**
- **Improvement: +3.4 percentage points**
- **Relative improvement: +5.1%**

### CLI Flags Available in `e6_match.py`:
- `--normalized` - Use architecture-normalized CFG similarity (Approach B)
- `--compare` - Run both raw and normalized scoring side-by-side
- `--panel` - Panel mode with both variants
- `--hand` - Use hand-written Pascal from `targets/liero-dos/pascal/`
- `--few-shot` - Include hand-decompiled gold standards as few-shot examples

### Key Design Decisions

1. **TP7 pinning is systemic** - Not just a suggestion, it's baked into every layer:
   - Toolchain config: `compiler: turbo-pascal-7`
   - Docker image: `rev:dos-tp7` 
   - Compiler flag: `fpc -Mtp`
   - Pascal template: `{$MODE TP}`
   - LLM prompt: explicit TP7 constraint
   - Type system: TP7-restricted types only

2. **Approach B normalization** works because it reduces the x86-64 vs 16-bit architectural gap without needing exact compiler matching. The +3.4 pp improvement is consistent and reproducible.

3. **Both approaches complement each other**:
   - Approach B: Immediate, measurable improvement, works with existing data
   - Approach A: Theoretically tighter matching via exact compiler, but requires original TP7 source code (decompiled code has syntax barriers)

### Files Modified / Created

| File | Changes |
|---|---|
| `/home/robin/OneDrive/University and such/LoSoRe/tools/e6_match.py` | Full normalization implementation (`_normalize_instruction`, `_normalize_cfg`, `cfg_similarity_normalized`), CLI flags (`--normalized`, `--compare`, `--panel`, `--hand`, `--few-shot`), TP7-constrained code generation |
| `/home/robin/OneDrive/University and such/LoSoRe/CONTINUATION_SUMMARY.md` | Complete documentation (Approach A feasibility, Approach B results, CLI guide, TP7 pinning) |
| `/etc/fpc.cfg` | Added MS-DOS unit paths for 16-bit cross-compilation |
| `targets/liero-dos/config/toolchain.yaml` | Already had `compiler: turbo-pascal-7`, `compiler_confidence: high` |

### Bottom Line

**The system is already fully pinned to Turbo Pascal 7** across all layers - toolchain config, Docker image, compiler flags, code generation, and LLM prompts. Approach B (`--normalized`) is production-ready with +3.4 pp avg improvement documented across 12 verified functions. Approach A (exact TP7 compiler matching) is architecturally constrained but already pinned at the toolchain level; the barrier is decompiled source syntax, not compiler availability.

**Recommended workflow:**
- Use `e6_match.py <fn> --normalized` for daily scoring improvements (+3.4 pp)
- Use `e6_match.py <fn> --compare` to evaluate both raw and normalized results
- Use `e6_match.py --hand` for hand-written Pascal drafts
- The TP7 constraint is already enforced at every level of the pipeline
