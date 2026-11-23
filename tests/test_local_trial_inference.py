"""Oracle: controlled HTTP transport and evidence checks, not model recovery."""

import hashlib
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from engine.local_trial_inference import (
    InferenceFailure,
    TrialInference,
    generation_budget,
    replay_response,
)


@pytest.fixture
def endpoint():
    state = {
        "response": {"response": '{"source":"procedure Test; begin end;"}',
                     "done": True, "done_reason": "stop", "eval_count": 8},
        "requests": [], "delay": 0,
    }

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            body = {"models": [{"name": "test", "digest": "fixed", "details": {}}]}
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())

        def do_POST(self):
            payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            state["requests"].append((self.path, payload))
            time.sleep(state["delay"])
            self.send_response(200)
            self.end_headers()
            try:
                self.wfile.write(json.dumps(state["response"]).encode())
            except BrokenPipeError:
                pass

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("localhost", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://localhost:{server.server_port}", state
    server.shutdown()
    server.server_close()
    thread.join()


def client(tmp_path, endpoint, **changes):
    config = {
        "backend": "ollama", "endpoint": endpoint, "model": "test",
        "identity": {"digest": "fixed"}, "max_tokens": 128,
        "context_tokens": 4096, "timeout_seconds": 5, "reasoning": "off",
    }
    config.update(changes)
    path = tmp_path / "inference.json"
    path.write_text(json.dumps(config))
    return TrialInference.from_file(path)


def test_ollama_strict_prompt_mode_preserves_raw_response_and_identity(
    tmp_path, endpoint
):
    url, state = endpoint
    inference = client(tmp_path, url)
    assert inference.identity()["digest"] == "fixed"
    directory = tmp_path / "request"
    result = inference.request("same Pascal task", directory)
    assert json.loads(result)["response"] == state["response"]["response"]
    route, payload = state["requests"][0]
    assert route == "/api/generate"
    assert payload["options"]["num_predict"] == 128
    assert payload["options"]["num_ctx"] == 4096
    assert "format" not in payload
    assert payload["think"] is False
    assert json.loads((directory / "response.raw").read_bytes()) == state["response"]
    assert replay_response(directory) == result


@pytest.mark.parametrize("content,reason", [
    ("not json", "format"),
    ('{"source":"a","extra":1}', "format"),
    ('{"source":null}', "format"),
    ('{"source":"a","source":"b"}', "format"),
])
def test_invalid_proposal_preserved_without_silent_repair(
    tmp_path, endpoint, content, reason
):
    url, state = endpoint
    state["response"]["response"] = content
    directory = tmp_path / "request"
    with pytest.raises(InferenceFailure) as error:
        client(tmp_path, url).request("task", directory)
    assert error.value.kind == reason
    assert len(state["requests"]) == 1
    assert content == json.loads((directory / "response.raw").read_bytes())["response"]
    assert json.loads((directory / "metadata.json").read_text())["status"] == "format"


def test_truncation_is_rejected_even_when_json_is_complete(tmp_path, endpoint):
    url, state = endpoint
    state["response"]["done_reason"] = "length"
    with pytest.raises(InferenceFailure, match="length"):
        client(tmp_path, url).request("task", tmp_path / "request")


def test_absolute_deadline_retains_unknown_outcome_and_never_retries(
    tmp_path, endpoint
):
    url, state = endpoint
    state["delay"] = 1
    directory = tmp_path / "request"
    start = time.monotonic()
    with pytest.raises(InferenceFailure) as error:
        client(tmp_path, url, timeout_seconds=0.2).request("task", directory)
    assert error.value.kind == "timeout"
    assert time.monotonic() - start < 0.9
    assert json.loads((directory / "metadata.json").read_text())["server_outcome"] == (
        "unknown-do-not-retry"
    )


def test_identity_change_rejects_before_generation(tmp_path, endpoint):
    url, state = endpoint
    with pytest.raises(InferenceFailure, match="identity"):
        client(tmp_path, url, identity={"digest": "different"}).identity()
    assert state["requests"] == []


def test_no_remote_or_credentialed_endpoint(tmp_path):
    for url in ("https://example.com", "http://user:password@localhost:8000"):
        with pytest.raises(ValueError, match="loopback"):
            client(tmp_path, url)


def test_openai_response_mapping_has_no_ollama_or_reasoning_flags(tmp_path, endpoint):
    url, state = endpoint
    state["response"] = {
        "model": "test", "choices": [{"finish_reason": "stop", "message": {
            "content": '{"source":"procedure Test; begin end;"}',
            "reasoning_content": "separate reasoning",
        }}], "usage": {"completion_tokens": 12},
    }
    inference = client(tmp_path, url + "/v1", backend="openai", reasoning="default")
    inference.request("same Pascal task", tmp_path / "request")
    path, payload = state["requests"][0]
    assert path == "/v1/chat/completions"
    assert payload["messages"] == [{"role": "user", "content": "same Pascal task"}]
    assert "format" not in payload and "response_format" not in payload
    assert "think" not in payload and "enable_thinking" not in payload
    metadata = json.loads((tmp_path / "request/metadata.json").read_text())
    assert metadata["reasoning"] == "separate reasoning"


def test_archive_replay_detects_response_tampering(tmp_path, endpoint):
    url, _ = endpoint
    directory = tmp_path / "request"
    client(tmp_path, url).request("task", directory)
    (directory / "response.raw").write_text("{}")
    with pytest.raises(ValueError):
        replay_response(directory)


def test_manifest_weight_and_process_identity(tmp_path, endpoint):
    url, _ = endpoint
    weights = tmp_path / "weights"
    weights.write_bytes(b"fixed weights")
    identity = {"files": [{
        "path": str(weights), "sha256": hashlib.sha256(weights.read_bytes()).hexdigest(),
    }], "processes": []}
    inference = client(
        tmp_path, url, backend="openai", identity=identity, reasoning="default"
    )
    with pytest.raises(InferenceFailure, match="process"):
        inference.identity()


@pytest.mark.parametrize("timeout", [False, True])
def test_profile_trial_preserves_failed_evidence_and_replays_without_network(
    tmp_path, endpoint, monkeypatch, timeout
):
    from tools import liero_source_trial as trial

    url, state = endpoint
    state["response"]["response"] = "invalid JSON"
    state["delay"] = 1 if timeout else 0
    inference = client(
        tmp_path, url, timeout_seconds=0.2 if timeout else 5, context_tokens=8192
    )
    routine = "FUN_24dd_48e1"

    def original(root, output, fn, inputs):
        assert output.name == "original-training"
        output.mkdir(parents=True)
        (output / "CASES.BIN").write_bytes(b"".join(inputs))
        (output / "TRACE.BIN").write_bytes(
            b"".join(trial.expected(fn, row, 0x2000) for row in inputs)
        )

    def forbidden(*args, **kwargs):
        pytest.fail("profile trial used legacy transport, compiler or candidate execution")

    monkeypatch.setattr(trial, "original", original)
    monkeypatch.setattr(trial, "compile_candidate", forbidden)
    monkeypatch.setattr(trial, "run_candidate", forbidden)
    monkeypatch.setattr(trial.pilot, "request", forbidden)
    monkeypatch.setattr(trial.pilot, "leaf_model_identity", forbidden)
    output = tmp_path / "trial"
    result = trial.run(
        trial.ROOT, output, "test", url, routines=(routine,),
        enforce_outputs=True, inference=inference,
    )
    assert result["model_requests"] == (1 if timeout else 2)
    assert result["routines"][routine]["terminal"] is None
    assert result["accepted_source_recoveries"] == 0
    monkeypatch.setattr(TrialInference, "identity", forbidden)
    assert trial.validate_artifacts(trial.ROOT, output) == result


def test_profile_rejects_different_scope_before_reading_binary(tmp_path, endpoint):
    from tools import liero_source_trial as trial

    url, _ = endpoint
    with pytest.raises(ValueError, match="direct-source48e1"):
        trial.freeze(
            tmp_path, tmp_path / "out", "test", url,
            routines=("FUN_249c_0013",), enforce_outputs=True,
            inference=client(tmp_path, url),
        )
    assert not (tmp_path / "out").exists()


def test_shared_budget_is_durable_and_unknown_prior_request_is_not_retried(tmp_path):
    path = tmp_path / "budget.json"
    path.write_text(json.dumps({
        "limit_seconds": 43200, "spent_seconds": 43199, "active": None,
    }))
    with generation_budget(path, 7200) as remaining:
        assert 0 < remaining <= 1
        assert json.loads(path.read_text())["active"] is not None
    state = json.loads(path.read_text())
    assert state["spent_seconds"] >= 43199 and state["active"] is None
    state["active"] = {"pid": 123, "outcome": "unknown"}
    path.write_text(json.dumps(state))
    with pytest.raises(InferenceFailure, match="unknown"), generation_budget(path, 7200):
        pytest.fail("unknown generation was retried")


def test_context_guard_refuses_before_http_without_truncating_prompt(tmp_path, endpoint):
    url, state = endpoint
    directory = tmp_path / "request"
    with pytest.raises(InferenceFailure) as error:
        client(tmp_path, url).request("long input " * 500, directory)
    assert error.value.kind == "context"
    assert state["requests"] == []
    assert json.loads((directory / "metadata.json").read_text())["status"] == "context"


def test_raw_source_response_is_normalized_and_replayable(tmp_path, endpoint):
    url, state = endpoint
    state["response"]["response"] = "```\nprocedure Test; begin end;\n```"
    inference = client(tmp_path, url, response_format="raw-source")
    directory = tmp_path / "request"
    result = inference.request("task", directory)
    assert json.loads(json.loads(result)["response"]) == {
        "source": "procedure Test; begin end;"
    }
    metadata = json.loads((directory / "metadata.json").read_text())
    assert metadata["response_format"] == "raw-source"
    assert replay_response(directory) == result


def test_unknown_response_format_is_rejected_before_http(tmp_path, endpoint):
    url, state = endpoint
    with pytest.raises(ValueError, match="response format"):
        client(tmp_path, url, response_format="unknown")
    assert state["requests"] == []
