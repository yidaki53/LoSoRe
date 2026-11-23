# Implementation Plan

## Overview

This plan addresses the comprehensive

## Types

### Data Structures

1. **FunctionMetadata** (from `targets/liero/functions.json`)
   - `name`: str - function name (e.g., "FUN_1000_01a1")
   - `entry_point`: str - hex entry point
   - `size`: int - function size in bytes
   - `calling_convention`: str - Pascal/cdecl/etc.
   - `subsystem`: str - movement/shooting/physics/etc.

2. **VerificationResult**
   - `fn`: str - function name
   - `oracle`: str - oracle used (byte-exact, relocation-aware, round-trip, dat-parity, constructor-parity)
   - `passed`: bool - whether all checks passed
   - `passed_relpaths`: list[str] - relative paths that matched
   - `failed_relpaths`: list[str] - relative paths that differed

3. **BuildSha1Entry**
   - `sha1`: str - SHA1 hash
   - `relpath`: str - relative path in build directory

4. **KnowledgeRecord**
   - `targets`: dict - per-target state {target: {verified: {oracle: [fn names]}}}
   - `verified_pascal_examples`: dict - {toolchain: [example records]}
   - `compilers`: dict - {compiler_key: {compiler_confidence, language, platform, targets, examples, etc.}}
   - `example_quality`: dict - quality tracking per toolchain


## Files

### New Files

1. **`/home/robin/OneDrive/University and such/LoSoRe/engine/oracle_gate.py`** - New module for build.sha1 gate management
   - `populate_build_sha1(target: str) -> int` - Automatically generate build.sha1 from BYOD files
   - `check_oracle_gate(target: str) -> dict` - Check gate status (open/closed/pending)
   - `validate_build_sha1(target: str) -> bool` - Validate build.sha1 format and content

2. **`/home/robin/OneDrive/University and such/LoSoRe/engine/verification_loop.py`** - Systematic verification loop
   - `verify_priority_functions(target: str, priority_fns: list[str], oracle: str = "dat-parity") -> dict`
   - `record_verification_results(target: str, results: dict) -> None`
   - `compute_coverage(data: dict) -> float`

3. **`/home/robin/OneDrive/University and such/LoSoRe/engine/verified_examples.py`** - Verified Pascal examples management
   - `record_verified_pascal(target: str, fn: str, pascal_body: str, oracle: str) -> str`
   - `get_verified_examples(target: str, compiler: str, platform: str, limit: int = 3) -> list[dict]`
   - `update_example_quality(example_id: str, success: bool) -> None`

### Existing Files to Modify

1. **`/home/robin/OneDrive/University and such/LoSoRe/engine/verify.py`**
   - Integrate `oracle_gate.check_oracle_gate()` at the start of verify()
   - Add `record_verification_result()` call after successful verification
   - Enhance `_promote_verified_pascal()` to record to verified_pascal_examples
   - Add coverage tracking metrics

2. **`/home/robin/OneDrive/University and such/LoSoRe/engine/knowledge.py`**
   - Enhance `record_verified()` to also update verified_pascal_examples
   - Add coverage computation functions
   - Enhance `stats()` to include verification coverage

3. **`/home/robin/OneDrive/University and such/LoSoRe/engine/recovery_module.py`**
   - Integrate oracle_gate and verification_loop
   - Connect Q-table action selection with verified example retrieval
   - Add coverage tracking to RL stats

4. **`/home/robin/OneDrive/University and such/LoSoRe/tools/run_full_pipeline.py`**
   - Ensure `populate_build_sha1()` is called automatically when BYOD is present
   - Connect pipeline steps to engine verification loop
   - Add coverage reporting at end

5. **`/home/robin/OneDrive/University and such/LoSoRe/engine/recovery_loop.py`**
   - Integrate with new verification_loop module
   - Add coverage metric tracking
   - Improve idle detection with coverage awareness


### Configuration Updates

1. **`/home/robin/OneDrive/University and such/LoSoRe/targets/liero/config/toolchain.yaml`** - Already configured, verify compiler_confidence settings
2. **`/home/robin/OneDrive/University and such/LoSoRe/pyproject.toml`** - May add optional dependencies if needed

### Optional Enhancements
1. **LLM integration packages** (already in training extras): `transformers`, `torch`, `peft`, `bitsandbytes`
2. No new external dependencies needed for core functionality

## Dependencies

### No New Packages Required

The implementation uses only stdlib and existing project dependencies:
- `json` - for knowledge base operations
- `pathlib` - for path operations
- `hashlib` - for example ID generation
- `datetime` - for timestamp tracking
- Existing: `pytest`, `ruff` (dev deps)

### Existing Dependencies to Enhance
1. **`engine/knowledge.json`** - No new deps, just enhanced schema usage
2. **`tools/liero_dat.py`** - Already exists for dat-parity oracle
3. **`targets/liero/functions.json`** - Already has 295 functions with metadata

### Optional Enhancements
- If LLM integration is desired: `transformers`, `torch`, `peft`, `bitsandbytes` (already in training extras)
- No new external dependencies needed for core functionality

## Implementation Order

### Phase 1: Foundation (Priority - establish base infrastructure)

1. **Create `engine/oracle_gate.py`** - build.sha1 gate management
   - Implement `populate_build_sha1()` and `check_oracle_gate()`
   - Test with existing build.sha1

2. **Enhance `engine/knowledge.py`** - Knowledge base schema enhancements
   - Add coverage computation
   - Enhance `record_verified()`
   - Add `verified_pascal_examples_for()` improvements

3. **Update `tools/run_full_pipeline.py`** - Pipeline integration
   - Ensure `populate_build_sha1()` auto-runs when BYOD present
   - Add coverage reporting

### Phase 2: Verification Loop (Priority - systematic function verification)

4. **Create `engine/verification_loop.py`** - Systematic verification loop
   - Implement `verify_priority_functions()`
   - Integrate with verify.py and knowledge base
   - Add coverage tracking

5. **Enhance `engine/verify.py`** - Verification integration
   - Add oracle gate check at start
   - Enhance result recording
   - Add verified Pascal example recording

### Phase 3: Example Management (Priority - few-shot learning integration)

6. **Create `engine/verified_examples.py`** - Verified examples management
   - Implement `record_verified_pascal()`
   - Implement `get_verified_examples()` for few-shot prompts
   - Add quality tracking

7. **Enhance `engine/recovery_module.RecoveryEngine`** - Q-table integration
   - Connect with verified examples retrieval
   - Add coverage-aware action selection
   - Enhance language_stats

### Phase 4: End-to-End Integration (Priority - complete workflow)

8. **Integrate all modules** - Ensure seamless flow
   - Pipeline → build.sha1 → oracle gate → verification → knowledge recording
   - Recovery loop with coverage-aware Q-table
   - Draft generation with few-shot from verified examples

9. **Create comprehensive test suite**
   - All 36 existing tests pass
   - New tests for each module
   - Integration test suite

10. **Documentation and reports**
    - Update RECOVERY_STATUS.md with new metrics
    - Create coverage report template
    - Document new workflows
## Success Criteria

After implementation, the following metrics should improve:

| Metric | Current | Target After Implementation |
|---|---|---|
| Functions verified | 1/295 (0.34%) | Configurable target (e.g., 50/295 = 17%) |
| Build.sha1 gate status | Manual, inconsistent | Automated, consistent |
| Verified Pascal examples | 0 entries | Auto-recorded per verification |
| Coverage metric | Not tracked | Computed and reported per run |
| Few-shot examples available | Empty | Grows with each verified function |
| Oracle gate consistency | Manual checking | Automated check before verification |
| 36 tests passing | 36/36 | 36/36 (regression) |

## Implementation Notes

### Key Integration Points

1. **build.sha1 → Oracle Gate**: The build.sha1 file is the gatekeeper. Without it, verification should WARN "not verified" never claim PASS. The `oracle_gate.check_oracle_gate()` should be called before any verification runs.

2. **Verification → Knowledge Recording**: When a function passes oracle verification, three things happen:
   - `knowledge.record_verified()` records the verified function
   - `verified_examples.record_verified_pascal()` records the Pascal body
   - `recovery_module.RecoveryEngine` Q-table is updated with success

3. **Q-table → Action Selection**: The RL Q-table should consider:
   - Which functions are already verified (avoid re-work)
   - Which subsystems have highest coverage gaps
   - Availability of few-shot examples for the current toolchain

4. **Few-Shot → Draft Generation**: When drafting a function, `draft.py` should retrieve verified examples from `verified_examples.get_verified_examples()` and use them as few-shot prompts.

### Edge Cases

- **Empty build.sha1**: Should WARN "not verified" - never claim PASS
- **No BYOD present**: SKIP verification, gate closed
- **All functions verified**: Coverage = 100%, system complete
- **Mixed success/failure**: Record both, learn from failures
- **Concurrent verification**: Ensure knowledge base saves atomically

### Creative Improvements

1. **Subsystem-aware prioritization**: Use the 7 subsystems from the recovery plan (movement, shooting, physics, AI, level, particles, utility) to prioritize which functions to verify first.
2. **Coverage-driven RL rewards**: Reward the RL agent not just for individual function verification, but for increasing overall coverage percentage.
3. **Automatic priority ranking**: Instead of user-specified priority functions, automatically rank by:
   - Gameplay importance (from community knowledge)
   - Subsystem criticality
   - Existing example availability (verify functions with most few-shot support first)
4. **Failure pattern learning**: When a function fails verification, record the failure pattern and use it to bias future attempts away from known bad patterns.
