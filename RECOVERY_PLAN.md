# LoSoRe Liero Source Code Recovery Plan

## 📋 Phase 1: Function Prioritization (Days 1-3)

### 1.1 Categorize Functions by Subsystem
Group the 295 functions into Liero subsystems:

| Subsystem | Expected Functions | Priority |
|---|---|---|
| **Movement** | ~30-40 | 🔴 Critical |
| **Shooting/Weapons** | ~40-50 | 🔴 Critical |
| **Physics** | ~30-40 | 🔴 Critical |
| **AI/Monsters** | ~20-30 | 🟠 High |
| **Level/Map** | ~20-30 | 🟠 High |
| **Particles/EFX** | ~20-30 | 🟡 Medium |
| **Utility/Helper** | ~50-60 | 🟢 Low |

### 1.2 Action Items
- [ ] Parse `functions.json` calling_convention fields
- [ ] Cross-reference with known Liero subsystems
- [ ] Create function-subsystem mapping
- [ ] Rank by gameplay importance

### 1.3 Success Criterion
- Function-subsystem mapping complete
- Priority list approved

---

## 🔬 Phase 2: Systematic Oracle Verification (Days 4-20)

### 2.1 Verification Loop
For each priority function, run:

```python
from engine import verify

result = verify.verify(
    'liero',       # target
    byod_path,     # LIERO.EXE path
    build_dir,     # temp build directory
    'dat-parity'   # oracle
)
```

### 2.2 Oracle Details: `dat-parity`
- Runs target's format oracle (`targets/liero/tools/liero_dat.py`)
- Fixture selftest (regression guard)
- BYOD round-trip when disc present
- "Green with no game data (skip)" if no BYOD

### 2.3 Recording Results
When verification passes:
- Record in `knowledge/verified_pascal_examples`
- Extract Pascal function body from `targets/liero/decomp/` or `pascal/`
- Update `knowledge/targets.liero.num_verified`
- Add entry to `knowledge/targets.liero.verified.dat-parity`
- Update `knowledge/examples_added`
- Save `knowledge/knowledge.json`

### 2.4 Action Items
- [ ] Implement verification loop for top-50 priority functions
- [ ] Test with first function (already: LIERO.DAT = 1 verified)
- [ ] Handle SKIP cases (no BYOD -> disc-gated)
- [ ] Record failures for improve loop feedback

### 2.5 Success Criterion
- 20+ functions verified under dat-parity oracle
- Knowledge base updated with verified Pascal bodies

---

## 📊 Phase 3: Coverage & Reporting (Days 21-25)

### 3.1 Coverage Metrics
Track:
- `num_verified / total_functions` = coverage percentage
- Functions verified per subsystem
- Success rate by function complexity

### 3.2 Report Generation
Generate progress reports:
- "X of 295 Liero functions verified (Y%)"
- Subsystem recovery status
- Provenance audit trail summary

### 3.3 Action Items
- [ ] Implement coverage calculation
- [ ] Generate first recovery report
- [ ] Document gaps and next priorities

### 3.4 Success Criterion
- Coverage report published
- Next priority phase identified

---

## 🔄 Phase 4: Iterative Improvement (Ongoing)

### 4.1 Improve Loop Tuning
Current settings (from improve_loop.py):
- Stop after 3 idle iterations
- Maximum 10 iterations
- Quality threshold: 0.3 success rate

### 4.2 Recovery-Optimized Parameters
- May need shorter idle detection
- Different success threshold for recovery vs. general improvement
- Track "recovery idle" vs "general idle"

### 4.2 Action Items
- [ ] Review improve_loop.py for recovery tuning
- [ ] Adjust parameters if needed
- [ ] Document parameter choices

### 4.3 Success Criterion
- Improve loop successfully recovers new functions
- Idle detection works for recovery workflow

---

## 🏆 Phase 5: "Across the Line" Criteria

The project achieves source code recovery when:

| Metric | Target |
|---|---|
| **Functions verified** | ≥ 100 of 295 (35%+ coverage) |
| **Critical subsystems** | Movement + shooting verified |
| **Provenance coverage** | 100% of verified functions documented |
| **Coverage claim** | "X% of Liero source code recovered" |
| **All 36 tests** | Passing |
| **Improve loop** | Demonstrates new recoveries |
| **Provenance complete** | PROVENANCE.md + toolchain.yaml complete |

---

## 📋 Success Checklist

### ✅ Already Complete
- [x] 295 functions reverse-engineered via Ghidra
- [x] functions.json populated with metadata
- [x] Assembly files (295) in `targets/liero/asm/`
- [x] Decompiled C bodies (295) in `targets/liero/decomp/`
- [x] Knowledge base initialized (`knowledge/knowledge.json`)
- [x] Verification pipeline (`engine/verify.py`)
- [x] Oracle systems (dat-parity, byte-exact, etc.)
- [x] 36/36 tests passing
- [x] PROVENANCE.md and toolchain.yaml configured

### 🔄 In Progress
- [ ] Systematic dat-parity verification of priority functions
- [ ] Pascal function bodies recorded in verified_pascal_examples
- [ ] Coverage metrics implemented and tracked
- [ ] Progress reports generated

### 📋 Pending
- [ ] 100+ functions verified for meaningful coverage
- [ ] Critical subsystems (movement, shooting) fully recovered
- [ ] Improvement loop tuned for recovery workflow
- [ ] Final "across the line" criteria met

---
*Recovery plan for LoSoRe Liero source code recovery project*