.PHONY: init test verify new-target lint typecheck report provenance preflight ingest draft learn build pipeline improve recovery-audit binary-census train train-now train-export autonomous
ACTIVE_FILES = engine/recovery_loop.py engine/matrix.py engine/rl_engine.py engine/verify.py engine/knowledge.py engine/model_training.py engine/local_trial_inference.py engine/rtl_template.py engine/frozen_source_eval.py engine/oracle_gate.py engine/contract_oracle.py engine/generic_synthesizer.py engine/capability_registry.py engine/capability_learner.py engine/capability_dsl.py engine/capability_proposer.py engine/large_routine_plan.py engine/asm_emulator.py engine/bootstrap.py engine/target_packet.py engine/improve_loop.py tools/run_full_pipeline.py tools/rl_recover.py tools/benchmark_matrix_models.py tools/evaluate_frozen_source.py tools/run_bootstrap.py tools/build_target_packet.py tools/triage_large_routines.py run_verification.py tools/build_codebase_graph.py tests/test_recovery_integration.py tests/test_bootstrap.py tests/test_target_packet.py tests/test_generic_synthesizer.py tests/test_contract_oracle.py tests/test_capability_registry.py tests/test_capability_dsl.py tests/test_local_trial_inference.py tests/test_learning.py tests/test_large_routine_plan.py tests/test_canonical_state.py tests/test_gate_hardening.py
IMPROVE_ARGS = \
	$(if $(MODEL),--model $(MODEL)) \
	$(if $(LLM),--endpoint $(LLM)) \
	$(if $(MAX_ITERATIONS),--max-iterations $(MAX_ITERATIONS)) \
	$(if $(SATURATION_WINDOW),--saturation-window $(SATURATION_WINDOW)) \
	$(if $(FUNCTIONS_PER_ITERATION),--functions-per-iteration $(FUNCTIONS_PER_ITERATION)) \
	$(if $(MAX_ATTEMPTS_PER_FUNCTION),--max-attempts-per-function $(MAX_ATTEMPTS_PER_FUNCTION)) \
	$(if $(RESUME_RUN),--resume-run $(RESUME_RUN))
init:
	uv sync --extra dev || pip install -e .[dev]
test:
	python3 -m pytest tests/ -q
verify:
	python3 engine/verify.py --target $(TARGET) --oracle $(or $(ORACLE),dat-parity)
provenance:
	python3 tools/provenance.py --target $(TARGET)
preflight:
	python3 engine/preflight.py --target $(TARGET)
ingest:
	python3 engine/ingest.py --target $(TARGET)
draft:
	python3 engine/draft.py --target $(TARGET) $(if $(FN),--fn $(FN)) --llm $(if $(LLM),--endpoint $(LLM)) $(if $(MODEL),--model $(MODEL))
learn:
	python3 engine/learn.py --target $(TARGET)
build:
	@echo "build handled by per-target Makefile"
improve:
	python3 engine/improve_loop.py --target $(TARGET) --oracle $(or $(ORACLE),dat-parity) $(IMPROVE_ARGS)
autonomous:
	python3 tools/rl_recover.py --target $(or $(TARGET),liero) --oracle $(or $(ORACLE),routine-trace-parity) --max-iterations $(or $(MAX_ITERATIONS),10)
recovery-audit:
	python3 -m engine.recovery --target $(TARGET) --init --summary-only
binary-census:
	python3 -m tools.binary_census --target $(TARGET) --output reports/$(TARGET)-binary-census.json
train:
	python3 engine/model_training.py --target $(TARGET) --auto
train-now:
	python3 engine/model_training.py --target $(TARGET) --train
train-export:
	python3 engine/model_training.py --target $(TARGET) --export $(or $(OUT),training_data/$(TARGET).jsonl)
# full run: ingest -> learn (update knowledge) -> draft (few-shot) -> verify -> improve (self-improving loop)
pipeline:
	python3 engine/preflight.py --target $(TARGET)
	python3 tools/provenance.py --target $(TARGET)
	python3 engine/ingest.py --target $(TARGET)
	python3 engine/learn.py --target $(TARGET)
	python3 engine/draft.py --target $(TARGET) $(if $(FN),--fn $(FN)) $(if $(LIMIT),--limit $(LIMIT)) --llm $(if $(MODEL),--model $(MODEL)) $(if $(LLM),--endpoint $(LLM))
	python3 engine/verify.py --target $(TARGET) --oracle $(or $(ORACLE),dat-parity)
	python3 engine/improve_loop.py --target $(TARGET) --oracle $(or $(ORACLE),dat-parity) $(IMPROVE_ARGS)
	python3 -m engine.recovery --target $(TARGET) --init --summary-only
	python3 engine/model_training.py --target $(TARGET) --auto
new-target:
	python3 tools/new_target.py --slug $(SLUG) --kind $(or $(KIND),game)
lint:
	python3 -m ruff check --select E9,F63,F7,F82 $(ACTIVE_FILES)
typecheck:
	python3 -m mypy --ignore-missing-imports --follow-imports=skip $(ACTIVE_FILES)
report:
	python3 tools/report.py
