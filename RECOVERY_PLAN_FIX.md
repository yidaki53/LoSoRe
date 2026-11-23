# Liero Source Code Recovery - Fix Plan
## Glaring Error: DL Code Doesn't Recover Lost Source Code

**Report Date**: Current
**Reported By**: System Design Review
**Severity**: Critical - System fails core objective

---

## 1. THE PROBLEM

### What's Broken
The Deep Learning model generates Pascal code that passes the `dat-parity` format oracle but has **no connection to what Liero functions actually do**. The Reinforcement Learning component that should produce game-semantic code was never properly implemented.

** symptoms**:
- 295/295 functions pass format oracle (dat-parity) ✅
- 297 Pascal bodies stored ✅
- DL model generates format-correct Pascal ✅
- **But**: Code has no game semantics ❌
- **RL component for game-semantic code: NOT implemented** ❌
- **System does not recover lost source code** ❌

### Root Cause
The RL component that produces code based on Liero game semantics was never implemented. The system started with format oracle verification (which works) but never completed the RL component that would produce actual functional code.

### Impact
- System recovers format, not source code
- DL generates format-correct but semantically-neutral code
- Continuous loop adds examples that don't improve game semantics
- Core objective (recover lost source code) is NOT met

---

## 2. WHAT NEEDS TO BE FIXED

### 1. RL Component Implementation
Produce Pascal code based on Liero game semantics:
- **Function semantics**: What each function controls (movement, shooting, physics, etc.)
- **State transitions**: How function state changes during gameplay
- **Action-effect patterns**: Cause-effect relationships in Liero gameplay
- **Use verified examples as guidance**: 295+ existing examples constrain the search space

### 2. RL→DL Pipeline Integration
Connect RL output as input to DL improvement:
- RL produces draft code based on game semantics
- DL improves the code quality and format correctness
- Format oracle verifies the improved output
- Record verified examples back to knowledge base
- Retrain both RL and DL on improved data

### 2. Success Metrics
**Before (Current)**:
- Format oracle: 295/295 pass ✅
- Code with game semantics: NOT MET ❌

**After (Target)**:
- Format oracle: 295/295 pass ✅
- Code with game semantics: 295/295 pass ✅ (new target)
- DL improvement over raw RL: Measurable quality gain
- Continuous loop adds meaningful examples

### 3. Implementation Plan

#### Phase 1: RL Component (Weeks 1-2)
- [ ] Analyze 295 verified examples to extract game-semantic patterns
- [ ] Implement RL function that produces Pascal code based on:
  - Function type (movement, shooting, physics, etc.)
  - Expected behavior patterns from verified examples
  - Constraint rules from the oracle guidelines
- [ ] Test RL output against verified examples for semantic similarity
- [ ] Document RL patterns and constraints

#### Phase 2: RL→DL Pipeline (Weeks 3-4)
- [ ] Modify `generate_prompted()` to accept RL-generated code as input
- [ ] Implement RL→DL pipeline: RL produces draft → DL improves
- [ ] Set up verification: RL→DL output → dat-parity oracle
- [ ] Record passing examples to knowledge base
- [ ] Retrain DL model on improved dataset

#### Phase 3: Pipeline Validation (Weeks 5-6)
- [ ] Test RL→DL pipeline on 10 functions
- [ ] Measure: format oracle pass rate, semantic similarity to verified examples
- [ ] Retrain both RL and DL on passing examples
- [ ] Expand to full 295 functions
- [ ] Document results and plan next iterations

#### Phase 4: Ongoing Continuous Loop
- [ ] Implement automatic RL→DL→verify→record→retrain loop
- [ ] Set up metrics tracking per iteration
- [ ] Plan for adding new functions/subsystems
- [ ] Document findings and plan next phases

### 4. Data Structures Needed

**RL Guidance Database** (enhanced from current verified examples):
```json
{
  "function_type": "movement|shooting|physics|ai|etc",
  "expected_behavior": "description of what the function does in gameplay",
  "constraints": ["oracle guidelines", "known patterns"],
  "examples": [list of similar verified function names],
  "success_rate": float from previous iterations
}
```

**DL Training Data** (enhanced):
```json
{
  "source": "RL_output or original_verified",
  "improved_by": "DL_few_shot_prompting",
  "oracle_result": "dat-parity result",
  "semantic_similarity": float to original verified example,
  "improvement_quality": float measure
}
```

### 5. Implementation Tasks

| Task | Owner | Priority | Status |
|------|-------|----------|--------|
| Analyze 295 verified examples for game-semantic patterns | System | High | Not started |
| Implement RL function for code production | System | High | Not started |
| Connect RL output to DL improvement step | System | High | Not started |
| Set up RL→DL→verify metrics | System | High | Not started |
| Test on subset of 10 functions | System | Medium | Pending |
| Expand to full 295 functions | System | Medium | Pending |
| Document architecture and findings | System | Medium | Pending |
| Set up ongoing continuous loop | System | Ongoing | Pending |

### 6. Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| RL produces nonsensical code | Start with constrained patterns from verified examples; use oracle to reject failing outputs |
| DL degrades RL output | Use DL only for format improvement, not semantic changes; verify each improvement |
| Loop doesn't improve over time | Track metrics per iteration; only retain examples that improve or maintain success rate |
| RL overfits to limited 295 examples | Use data augmentation; periodically add new functions; periodically reevaluate pattern space |
| Oracle doesn't catch semantic errors | This is the fundamental limitation; eventual gameplay testing required (beyond current scope) |

### 6. Timeline

**Week 1**: Analyze verified examples for semantic patterns
**Week 2**: Implement RL function prototype
**Week 3**: Connect RL→DL pipeline
**Week 4**: Set up verification and recording
**Week 5**: Test on subset of functions
**Week 6**: Expand to full functions, document results
**Ongoing**: Continuous loop with metric tracking

### 7. Success Criteria

**Minimum Viable Success**:
- [ ] RL produces code that passes dat-parity oracle for ≥50% of tested functions
- [ ] DL improves RL output format correctness (maintains or improves pass rate)
- [ ] 20+ new verified examples added through RL→DL loop
- [ ] Metrics tracked and documented per iteration

**Full Success**:
- [ ] RL produces code passing dat-parity for ≥90% of 295 functions
- [ ] DL improves code quality (fewer patterns, smoother syntax) while maintaining pass rate
- [ ] 100+ new verified examples added through RL→DL loop
- [ ] Full architecture documented with clear path for ongoing improvement
- [ ] System demonstrably recovers lost source code semantics (not just format)

### 8. Conclusion

The current system has a critical gap: format recovery without source code recovery. The RL component was never implemented, and the DL model generates format-correct but semantically-neutral code. 

**This plan fixes that by**:
1. Implementing the RL component based on verified example patterns
2. Connecting RL→DL as a proper improvement pipeline
3. Setting up measurable success criteria
4. Creating a continuous learning loop that actually recovers lost source code semantics

**Without this fix**, the system continues to recover format but not source code — missing the core objective entirely.

**With this fix**, the system recovers lost Liero source code through the integrated RL→DL→verify loop, adding verified examples continuously and improving both format correctness and game-semantic accuracy.

---

**Plan Created**: Current Date  
**Next Review**: After Phase 1 completion  
**Owner**: System Architecture  
**Priority**: Critical — Core objective not met  
**Dependencies**: Verified examples (295), DL model (trained), Oracle (dat-parity 295/295 pass)  
**Tags**: #rl+dl #source-code-recovery #game-semantics #continuous-learning #plan  
