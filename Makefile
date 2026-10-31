.PHONY: init test verify new-target lint report provenance preflight ingest draft learn build pipeline improve recovery-audit binary-census train train-now train-export
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
	ruff check . || true
report:
	python3 tools/report.py
