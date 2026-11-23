"""Oracle: local transport identity/integrity only; never semantic acceptance."""

from __future__ import annotations

import fcntl
import hashlib
import ipaddress
import json
import os
import pathlib
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass


class InferenceFailure(ValueError):
    """Oracle: classified failed or unknown proposal; no implicit retries."""

    def __init__(self, kind: str, message: str):
        self.kind = kind
        super().__init__(message)


def digest(path: pathlib.Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(16 << 20), b""):
            result.update(block)
    return result.hexdigest()


def save(path: pathlib.Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def loads(value):
    return json.loads(value, object_pairs_hook=_unique_object)


def local_base(endpoint: str) -> str:
    url = urllib.parse.urlsplit(endpoint)
    host = url.hostname
    try:
        local = host == "localhost" or ipaddress.ip_address(host or "").is_loopback
    except ValueError:
        local = False
    if (
        url.scheme != "http" or not local or url.username or url.password
        or url.query or url.fragment or url.path.rstrip("/") not in ("", "/v1")
    ):
        raise ValueError("trial inference requires a credential-free loopback HTTP endpoint")
    return urllib.parse.urlunsplit((url.scheme, url.netloc, "", "", ""))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise InferenceFailure("transport", "local inference redirects are refused")


def opener():
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())


def _worker(request_path: pathlib.Path) -> int:
    """Oracle: isolated bounded HTTP read; killed on parent absolute deadline."""
    request = loads(request_path.read_bytes())
    directory = request_path.parent
    local_base(request["base"])
    body = json.dumps(request["payload"], allow_nan=False).encode()
    (directory / "request.body").write_bytes(body)
    req = urllib.request.Request(
        request["base"] + request["route"],
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with opener().open(req, timeout=request["timeout_seconds"]) as response:
            save(directory / "http.json", {
                "status": response.status, "headers": dict(response.headers),
            })
            size = 0
            with (directory / "response.raw").open("wb") as stream:
                while block := response.read(65536):
                    size += len(block)
                    if size > 64 << 20:
                        raise ValueError("response exceeds 64 MiB limit")
                    stream.write(block)
                    stream.flush()
    except urllib.error.HTTPError as error:
        (directory / "response.raw").write_bytes(error.read(64 << 20))
        save(directory / "http.json", {"status": error.code})
        return 1
    return 0


def decode_response(
    raw: bytes, backend: str, response_format: str = "source-json"
) -> tuple[str, dict]:
    """Oracle: preserve exact content; never salvage JSON or truncated output."""
    if response_format not in ("source-json", "raw-source"):
        raise ValueError("unsupported response format")
    try:
        response = loads(raw)
        if backend == "ollama":
            content = response["response"]
            reason = response.get("done_reason")
            if response.get("done") is not True or reason != "stop":
                raise InferenceFailure("truncation", f"incomplete completion: {reason}")
            metadata = {
                "finish_reason": reason, "reasoning": response.get("thinking"),
                "usage": {key: response.get(key) for key in (
                    "prompt_eval_count", "eval_count", "total_duration",
                    "load_duration", "prompt_eval_duration", "eval_duration",
                )},
                "response_format": response_format,
            }
        else:
            if len(response["choices"]) != 1:
                raise ValueError("expected exactly one completion")
            choice = response["choices"][0]
            reason = choice["finish_reason"]
            if reason != "stop":
                raise InferenceFailure("truncation", f"incomplete completion: {reason}")
            content = choice["message"]["content"]
            metadata = {
                "finish_reason": reason,
                "reasoning": choice["message"].get("reasoning_content"),
                "usage": response.get("usage"),
                "response_format": response_format,
            }
        if not isinstance(content, str) or not content.strip():
            raise ValueError("empty or non-text completion")
        if response_format == "source-json":
            proposal = loads(content)
            if (
                not isinstance(proposal, dict) or set(proposal) != {"source"}
                or not isinstance(proposal["source"], str) or not proposal["source"].strip()
            ):
                raise ValueError("proposal must contain exactly one nonempty source string")
            normalized = content
        else:
            source = content.strip()
            if source.startswith("```"):
                lines = source.splitlines()
                if len(lines) < 3 or lines[-1].strip() != "```":
                    raise ValueError("unterminated markdown fence")
                source = "\n".join(lines[1:-1]).strip()
            if not source:
                raise ValueError("empty source completion")
            normalized = json.dumps({"source": source})
    except InferenceFailure:
        raise
    except (ValueError, KeyError, TypeError, IndexError) as error:
        raise InferenceFailure("format", str(error)) from error
    return json.dumps({"response": normalized}), metadata


def replay_response(directory: pathlib.Path) -> str:
    """Oracle: read-only transport replay; no endpoint/model/process access."""
    metadata = loads((directory / "metadata.json").read_bytes())
    if metadata["status"] != "complete":
        raise ValueError("request has no complete response")
    if digest(directory / "response.raw") != metadata["response_sha256"]:
        raise ValueError("raw response identity changed")
    if digest(directory / "request.json") != metadata["request_sha256"]:
        raise ValueError("request identity changed")
    normalized, _ = decode_response(
        (directory / "response.raw").read_bytes(),
        metadata["backend"],
        metadata.get("response_format", "source-json"),
    )
    return normalized


@contextmanager
def generation_budget(path: pathlib.Path | None, ceiling: float):
    """Oracle: durable serial shared budget; unknown prior requests fail closed."""
    if path is None:
        yield ceiling
        return
    with path.open("r+") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = loads(stream.read())
        if state.get("active") is not None:
            raise InferenceFailure("budget", "prior generation outcome unknown; do not retry")
        remaining = min(ceiling, state["limit_seconds"] - state["spent_seconds"])
        if remaining <= 0:
            raise InferenceFailure("budget", "aggregate generation budget exhausted")
        started = time.monotonic()
        state["active"] = {"pid": os.getpid(), "started_at": time.time()}

        def write():
            stream.seek(0)
            json.dump(state, stream)
            stream.truncate()
            stream.flush()
            os.fsync(stream.fileno())

        write()
        try:
            yield remaining
        finally:
            state["spent_seconds"] += time.monotonic() - started
            state["active"] = None
            write()


@dataclass
class TrialInference:
    config: dict
    config_sha256: str

    @classmethod
    def from_file(cls, path: pathlib.Path) -> TrialInference:
        config = loads(path.read_bytes())
        required = {
            "backend", "endpoint", "model", "identity", "max_tokens",
            "context_tokens", "timeout_seconds", "reasoning",
        }
        if not required <= set(config) or set(config) - required - {
            "generation_budget_file", "comparison_sha256", "notes",
            "response_format",
        }:
            raise ValueError("unknown or missing inference configuration fields")
        if config.get("response_format", "source-json") not in (
            "source-json", "raw-source"
        ):
            raise ValueError("unsupported response format")
        if config["backend"] not in ("ollama", "openai"):
            raise ValueError("unsupported inference backend")
        local_base(config["endpoint"])
        for key, maximum in (("max_tokens", 8192), ("context_tokens", 16384)):
            if type(config[key]) is not int or not 0 < config[key] <= maximum:
                raise ValueError("invalid " + key)
        if not 0 < config["timeout_seconds"] <= 7200:
            raise ValueError("invalid absolute request deadline")
        if config["max_tokens"] >= config["context_tokens"]:
            raise ValueError("output budget must leave room for the prompt")
        if config["reasoning"] not in ("off", "on", "default"):
            raise ValueError("unsupported reasoning setting")
        if config["backend"] == "openai" and config["reasoning"] != "default":
            raise ValueError("OpenAI reasoning controls need explicit engine support")
        return cls(config, digest(path))

    def identity(self) -> dict:
        """Oracle: content hashes and controlled process, not a mutable model id."""
        config = self.config
        expected = config["identity"]
        if config["backend"] == "ollama":
            with opener().open(local_base(config["endpoint"]) + "/api/tags", timeout=30) as r:
                matches = [
                    item for item in loads(r.read())["models"]
                    if item["name"] == config["model"]
                ]
            if len(matches) != 1 or matches[0]["digest"] != expected.get("digest"):
                raise InferenceFailure("identity", "Ollama model identity changed")
            return {key: matches[0].get(key) for key in ("name", "digest", "details")}
        if not expected.get("files") or not expected.get("processes"):
            raise InferenceFailure("identity", "OpenAI model needs file and process identities")
        for item in expected["files"]:
            path = pathlib.Path(item["path"])
            if not path.is_absolute() or digest(path) != item["sha256"]:
                raise InferenceFailure("identity", "local model/engine file identity changed")
        for item in expected["processes"]:
            proc = pathlib.Path("/proc") / str(item["pid"])
            try:
                start = (proc / "stat").read_text().rsplit(")", 1)[1].split()[19]
                executable = str((proc / "exe").resolve(strict=True))
                argv = (proc / "cmdline").read_bytes().split(b"\0")[:-1]
                if (
                    start != str(item["start_ticks"]) or executable != item["executable"]
                    or [arg.decode() for arg in argv] != item["argv"]
                ):
                    raise ValueError("process changed")
            except (OSError, ValueError) as error:
                raise InferenceFailure("identity", "controlled engine process changed") from error
        return {"name": config["model"], "manifest": expected}

    def payload(self, prompt: str) -> tuple[str, dict]:
        config = self.config
        if config["backend"] == "openai":
            return "/v1/chat/completions", {
                "model": config["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0, "max_tokens": config["max_tokens"], "stream": False,
            }
        payload = {
            "model": config["model"], "prompt": prompt, "stream": False,
            "keep_alive": 0,
            "options": {"temperature": 0, "num_predict": config["max_tokens"],
                        "num_ctx": config["context_tokens"]},
        }
        if config["reasoning"] != "default":
            payload["think"] = config["reasoning"] == "on"
        return "/api/generate", payload

    def request(self, prompt: str, directory: pathlib.Path) -> str:
        """Oracle: one request, exact bytes, absolute deadline, no fallback."""
        directory.mkdir(parents=True, exist_ok=False)
        route, payload = self.payload(prompt)
        request_path = directory / "request.json"
        request = {
            "base": local_base(self.config["endpoint"]), "route": route,
            "payload": payload, "timeout_seconds": self.config["timeout_seconds"],
        }
        save(request_path, request)
        metadata = {
            "backend": self.config["backend"], "status": "started",
            "config_sha256": self.config_sha256, "started_at": time.time(),
            "request_sha256": digest(request_path), "first_token_seconds": None,
            "response_format": self.config.get("response_format", "source-json"),
        }
        save(directory / "metadata.json", metadata)
        started = time.monotonic()
        budget_path = self.config.get("generation_budget_file")
        try:
            # UTF-8 byte count plus fixed-template headroom is a conservative
            # token bound; refuse rather than let the server truncate input.
            if (
                len(prompt.encode()) + self.config["max_tokens"] + 512
                > self.config["context_tokens"]
            ):
                raise InferenceFailure("context", "conservative prompt/output context bound exceeded")
            with generation_budget(
                pathlib.Path(budget_path) if budget_path else None,
                self.config["timeout_seconds"],
            ) as timeout:
                with (directory / "worker.log").open("wb") as log:
                    process = subprocess.Popen(
                        [sys.executable, str(pathlib.Path(__file__).resolve()),
                         "--worker", str(request_path.resolve())],
                        stdout=log, stderr=log, start_new_session=True,
                    )
                    try:
                        code = process.wait(timeout=timeout)
                    except BaseException:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                        raise
                if code:
                    raise InferenceFailure("transport", f"HTTP worker failed: exit {code}")
                normalized, details = decode_response(
                    (directory / "response.raw").read_bytes(),
                    self.config["backend"],
                    self.config.get("response_format", "source-json"),
                )
                metadata.update(details)
                metadata["status"] = "complete"
                return normalized
        except subprocess.TimeoutExpired as error:
            metadata.update(status="timeout", server_outcome="unknown-do-not-retry")
            raise InferenceFailure("timeout", "absolute generation deadline exceeded") from error
        except InferenceFailure as error:
            metadata["status"] = error.kind
            raise
        except BaseException:
            metadata.update(status="interrupted", server_outcome="unknown-do-not-retry")
            raise
        finally:
            metadata["elapsed_seconds"] = time.monotonic() - started
            raw_path = directory / "response.raw"
            metadata["response_sha256"] = digest(raw_path) if raw_path.exists() else None
            save(directory / "metadata.json", metadata)


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--worker":
        raise SystemExit("internal HTTP worker only")
    raise SystemExit(_worker(pathlib.Path(sys.argv[2])))
