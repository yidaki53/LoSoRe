.PHONY: init test verify new-target lint report provenance ingest draft
init:
	uv sync --extra dev || pip install -e .[dev]
test:
	python3 -m pytest tests/ -q
verify:
	python3 engine/verify.py --target $(TARGET) --oracle $(or $(ORACLE),byte-exact)
provenance:
	python3 tools/provenance.py --target $(TARGET)
ingest:
	python3 engine/ingest.py --target $(TARGET)
draft:
	python3 engine/draft.py --target $(TARGET) $(if $(FN),--fn $(FN)) $(if $(LLM),--llm --endpoint $(LLM))
new-target:
	python3 tools/new_target.py --slug $(SLUG) --kind $(or $(KIND),game)
# compat (deprecated, will be removed): GAME= -> TARGET=
new-game:
	python3 tools/new_target.py --slug $(SLUG) --kind game
lint:
	ruff check . || true
report:
	python3 tools/report.py
