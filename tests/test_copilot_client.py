"""Tests for CopilotClient and the ``python -m benchmark`` CLI."""

from __future__ import annotations

import io
import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from benchmark.copilot_client import GITHUB_COPILOT_BASE_URL, GITHUB_MODELS_BASE_URL, CopilotClient


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_response_body(
    prompt_tokens: int = 10,
    completion_tokens: int = 20,
    content: str = "Hello!",
    model: str = "gpt-4o",
) -> bytes:
    payload = {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "model": model,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}}],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }
    return json.dumps(payload).encode()


def _mock_urlopen(body: bytes, status: int = 200):
    """Return a context-manager mock for urllib.request.urlopen."""
    resp = MagicMock()
    resp.read.return_value = body
    resp.__enter__ = lambda s: s
    resp.__exit__ = MagicMock(return_value=False)
    return resp


# ---------------------------------------------------------------------------
# CopilotClient construction
# ---------------------------------------------------------------------------

class TestCopilotClientConstruction:
    def test_default_base_url(self):
        client = CopilotClient("token123")
        assert client._base_url == GITHUB_COPILOT_BASE_URL.rstrip("/")

    def test_custom_base_url(self):
        client = CopilotClient("token123", base_url="https://example.com/")
        assert client._base_url == "https://example.com"

    def test_empty_token_raises(self):
        with pytest.raises(ValueError, match="github_token"):
            CopilotClient("")

    def test_chat_completions_accessible(self):
        client = CopilotClient("token123")
        assert hasattr(client.chat, "completions")
        assert hasattr(client.chat.completions, "create")


# ---------------------------------------------------------------------------
# _post: request construction
# ---------------------------------------------------------------------------

class TestCopilotClientPost:
    def test_sends_correct_url(self):
        client = CopilotClient("token123", base_url="https://example.com")
        mock_resp = _mock_urlopen(_make_response_body())

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
            client._post("/chat/completions", {"model": "gpt-4o", "messages": []})

        req = mock_open.call_args[0][0]
        assert req.full_url == "https://example.com/chat/completions"

    def test_sends_bearer_auth_header(self):
        client = CopilotClient("mytoken", base_url="https://example.com")
        mock_resp = _mock_urlopen(_make_response_body())

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
            client._post("/chat/completions", {})

        req = mock_open.call_args[0][0]
        assert req.get_header("Authorization") == "Bearer mytoken"

    def test_sends_json_content_type(self):
        client = CopilotClient("token123", base_url="https://example.com")
        mock_resp = _mock_urlopen(_make_response_body())

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
            client._post("/chat/completions", {})

        req = mock_open.call_args[0][0]
        assert req.get_header("Content-type") == "application/json"

    def test_body_serialised_as_json(self):
        client = CopilotClient("token123", base_url="https://example.com")
        mock_resp = _mock_urlopen(_make_response_body())
        payload = {"model": "gpt-4o", "messages": [{"role": "user", "content": "hi"}]}

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
            client._post("/chat/completions", payload)

        req = mock_open.call_args[0][0]
        assert json.loads(req.data) == payload

    def test_returns_parsed_dict(self):
        client = CopilotClient("token123", base_url="https://example.com")
        body = _make_response_body(prompt_tokens=5, completion_tokens=15)
        mock_resp = _mock_urlopen(body)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = client._post("/chat/completions", {})

        assert result["usage"]["prompt_tokens"] == 5
        assert result["usage"]["completion_tokens"] == 15


# ---------------------------------------------------------------------------
# _post: error handling
# ---------------------------------------------------------------------------

class TestCopilotClientErrors:
    def test_http_error_raises_runtime_error(self):
        import urllib.error

        client = CopilotClient("token123", base_url="https://example.com")
        http_err = urllib.error.HTTPError(
            url="https://example.com/chat/completions",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=io.BytesIO(b"bad token"),
        )

        with patch("urllib.request.urlopen", side_effect=http_err):
            with pytest.raises(RuntimeError, match="401"):
                client._post("/chat/completions", {})

    def test_http_error_message_includes_body(self):
        import urllib.error

        client = CopilotClient("token123", base_url="https://example.com")
        http_err = urllib.error.HTTPError(
            url="https://example.com/chat/completions",
            code=429,
            msg="Too Many Requests",
            hdrs=None,
            fp=io.BytesIO(b"rate limit exceeded"),
        )

        with patch("urllib.request.urlopen", side_effect=http_err):
            with pytest.raises(RuntimeError, match="rate limit exceeded"):
                client._post("/chat/completions", {})


# ---------------------------------------------------------------------------
# chat.completions.create
# ---------------------------------------------------------------------------

class TestCopilotClientCreate:
    def test_create_passes_model_and_messages(self):
        client = CopilotClient("token123", base_url="https://example.com")
        body = _make_response_body()
        mock_resp = _mock_urlopen(body)

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
            client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "hi"}],
            )

        req = mock_open.call_args[0][0]
        sent = json.loads(req.data)
        assert sent["model"] == "gpt-4o"
        assert sent["messages"] == [{"role": "user", "content": "hi"}]

    def test_create_forwards_extra_kwargs(self):
        client = CopilotClient("token123", base_url="https://example.com")
        mock_resp = _mock_urlopen(_make_response_body())

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
            client.chat.completions.create(
                model="gpt-4o",
                messages=[],
                temperature=0.0,
                max_tokens=64,
            )

        sent = json.loads(mock_open.call_args[0][0].data)
        assert sent["temperature"] == 0.0
        assert sent["max_tokens"] == 64

    def test_create_returns_dict(self):
        client = CopilotClient("token123", base_url="https://example.com")
        mock_resp = _mock_urlopen(_make_response_body())

        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = client.chat.completions.create(model="gpt-4o", messages=[])

        assert isinstance(result, dict)
        assert "choices" in result
        assert "usage" in result


# ---------------------------------------------------------------------------
# Integration: BenchmarkAgent + CopilotClient
# ---------------------------------------------------------------------------

class TestCopilotClientWithBenchmarkAgent:
    def test_agent_collects_tokens_via_copilot_client(self):
        from benchmark import BenchmarkAgent

        client = CopilotClient("token123", base_url="https://example.com")
        mock_resp = _mock_urlopen(_make_response_body(prompt_tokens=7, completion_tokens=13))

        with patch("urllib.request.urlopen", return_value=mock_resp):
            agent = BenchmarkAgent(client, model="gpt-4o")
            result = agent.run("Hello")

        assert result.tokens.prompt_tokens == 7
        assert result.tokens.completion_tokens == 13
        assert result.tokens.total_tokens == 20

    def test_agent_captures_response_text_via_copilot_client(self):
        from benchmark import BenchmarkAgent

        client = CopilotClient("token123", base_url="https://example.com")
        mock_resp = _mock_urlopen(_make_response_body(content="42"))

        with patch("urllib.request.urlopen", return_value=mock_resp):
            agent = BenchmarkAgent(client, model="gpt-4o")
            result = agent.run("What is 6*7?")

        assert result.response_text == "42"

    def test_agent_timing_captured(self):
        from benchmark import BenchmarkAgent

        client = CopilotClient("token123", base_url="https://example.com")
        mock_resp = _mock_urlopen(_make_response_body())

        with patch("urllib.request.urlopen", return_value=mock_resp):
            agent = BenchmarkAgent(client, model="gpt-4o")
            result = agent.run("prompt")

        assert result.timing.elapsed_seconds >= 0.0


# ---------------------------------------------------------------------------
# CLI (__main__)
# ---------------------------------------------------------------------------

class TestCLI:
    def test_missing_github_token_exits_1(self, monkeypatch):
        from benchmark.__main__ import main

        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        assert main(["hello"]) == 1

    def test_text_output_on_success(self, monkeypatch):
        import io as _io

        from benchmark.__main__ import main

        monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
        mock_resp = _mock_urlopen(_make_response_body(prompt_tokens=3, completion_tokens=5))

        with patch("urllib.request.urlopen", return_value=mock_resp):
            with patch("sys.stdout", new_callable=_io.StringIO) as mock_out:
                code = main(["hello world"])

        assert code == 0
        output = mock_out.getvalue()
        assert "Prompt tokens" in output
        assert "Total tokens" in output

    def test_json_output_on_success(self, monkeypatch):
        import io as _io

        from benchmark.__main__ import main

        monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
        mock_resp = _mock_urlopen(_make_response_body())

        with patch("urllib.request.urlopen", return_value=mock_resp):
            with patch("sys.stdout", new_callable=_io.StringIO) as mock_out:
                code = main(["hello", "--format", "json"])

        assert code == 0
        data = json.loads(mock_out.getvalue())
        assert "prompt_tokens" in data
        assert "completion_tokens" in data

    def test_api_error_exits_1(self, monkeypatch):
        import urllib.error

        from benchmark.__main__ import main

        monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
        http_err = urllib.error.HTTPError(
            url="https://models.inference.ai.azure.com/chat/completions",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=io.BytesIO(b"bad credentials"),
        )

        with patch("urllib.request.urlopen", side_effect=http_err):
            code = main(["hello"])

        assert code == 1

    def test_default_model_is_gpt4o_mini(self, monkeypatch):
        from benchmark.__main__ import main

        monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
        mock_resp = _mock_urlopen(_make_response_body())

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
            main(["hello"])

        sent = json.loads(mock_open.call_args[0][0].data)
        assert sent["model"] == "gpt-4o-mini"

    def test_model_override(self, monkeypatch):
        from benchmark.__main__ import main

        monkeypatch.setenv("GITHUB_TOKEN", "fake-token")
        mock_resp = _mock_urlopen(_make_response_body())

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_open:
            main(["hello", "--model", "gpt-4.1"])

        sent = json.loads(mock_open.call_args[0][0].data)
        assert sent["model"] == "gpt-4.1"
