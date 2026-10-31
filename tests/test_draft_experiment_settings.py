import json
import urllib.request

from engine import draft


def test_sanitizer_reports_rejection_reason():
    assert draft._sanitize_pascal_with_reason("") == ("", "empty-completion")
    assert draft._sanitize_pascal_with_reason(
        "No Pascal body here"
    ) == ("", "missing-routine-declaration")
    assert draft._sanitize_pascal_with_reason(
        "procedure FUN_0001;\nbegin\n  Inc(Value);"
    ) == ("", "incomplete-routine")


def test_run_llm_passes_experiment_settings_to_chat_endpoint(monkeypatch):
    seen = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return json.dumps({
                "choices": [{"message": {"content": "procedure FUN_0001;"} }]
            }).encode()

    def fake_urlopen(request, timeout):
        seen["payload"] = json.loads(request.data)
        seen["timeout"] = timeout
        return Response()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    result = draft.run_llm(
        "prompt",
        "local-model",
        "http://localhost:11434",
        temperature=0.3,
        max_tokens=1024,
    )

    assert result == "procedure FUN_0001;"
    assert seen["payload"]["temperature"] == 0.3
    assert seen["payload"]["max_tokens"] == 1024
    assert seen["timeout"] == 300


def test_run_llm_defaults_to_configured_local_ollama(monkeypatch):
    seen = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return json.dumps({
                "choices": [{"message": {"content": "local response"}}]
            }).encode()

    def fake_urlopen(request, timeout):
        seen["url"] = request.full_url
        return Response()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(draft.shutil, "which", lambda _name: None)
    monkeypatch.delenv("LSR_LLM_ENDPOINT", raising=False)

    result = draft.run_llm("prompt", "local-model", None)

    assert result == "local response"
    assert seen["url"] == "http://localhost:11434/v1/chat/completions"


def test_fewshot_context_can_disable_learned_examples(monkeypatch):
    monkeypatch.setattr(draft.knowledge, "load", dict)

    assert draft.fewshot_context(
        "liero",
        "turbo-pascal-7",
        "dos",
        include_learned_context=False,
    ) == ""


def test_generation_capture_records_sanitizer_reason(tmp_path):
    draft._write_generation_capture(
        tmp_path,
        "FUN_0001",
        "prompt",
        "raw completion",
        "",
        "missing-routine-declaration",
    )

    metadata = json.loads((tmp_path / "capture.json").read_text())

    assert metadata["sanitizer_accepted"] is False
    assert metadata["rejection_reason"] == "missing-routine-declaration"
    assert metadata["prompt_sha256"]
    assert (tmp_path / "completion.txt").read_text() == "raw completion"
