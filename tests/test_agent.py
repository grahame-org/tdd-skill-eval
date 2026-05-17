"""Tests for BenchmarkAgent – validates time and token collection via mocked API."""

from __future__ import annotations

import time
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from benchmark.agent import BenchmarkAgent
from benchmark.metrics import BenchmarkResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_client(prompt_tokens=10, completion_tokens=20, content="Test response"):
    """Build a mock OpenAI-compatible client."""
    usage = SimpleNamespace(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
    message = SimpleNamespace(content=content)
    choice = SimpleNamespace(message=message)
    response = SimpleNamespace(usage=usage, choices=[choice])

    client = MagicMock()
    client.chat.completions.create.return_value = response
    return client


# ---------------------------------------------------------------------------
# Basic functionality
# ---------------------------------------------------------------------------

class TestBenchmarkAgentRun:
    def test_returns_benchmark_result(self):
        agent = BenchmarkAgent(_make_client())
        result = agent.run("Hello world")
        assert isinstance(result, BenchmarkResult)

    def test_prompt_stored_in_result(self):
        agent = BenchmarkAgent(_make_client())
        result = agent.run("My test prompt")
        assert result.prompt == "My test prompt"

    def test_default_model_used(self):
        client = _make_client()
        agent = BenchmarkAgent(client, model="gpt-4o")
        agent.run("prompt")
        _, kwargs = client.chat.completions.create.call_args
        assert kwargs["model"] == "gpt-4o"

    def test_per_call_model_override(self):
        client = _make_client()
        agent = BenchmarkAgent(client, model="gpt-4o")
        agent.run("prompt", model="gpt-3.5-turbo")
        _, kwargs = client.chat.completions.create.call_args
        assert kwargs["model"] == "gpt-3.5-turbo"

    def test_model_stored_in_result(self):
        agent = BenchmarkAgent(_make_client(), model="gpt-4o-mini")
        result = agent.run("prompt")
        assert result.model == "gpt-4o-mini"

    def test_response_text_captured(self):
        agent = BenchmarkAgent(_make_client(content="The answer is 42"))
        result = agent.run("What is 6 * 7?")
        assert result.response_text == "The answer is 42"


# ---------------------------------------------------------------------------
# Token collection
# ---------------------------------------------------------------------------

class TestTokenCollection:
    def test_prompt_tokens_collected(self):
        agent = BenchmarkAgent(_make_client(prompt_tokens=50))
        result = agent.run("prompt")
        assert result.tokens.prompt_tokens == 50

    def test_completion_tokens_collected(self):
        agent = BenchmarkAgent(_make_client(completion_tokens=75))
        result = agent.run("prompt")
        assert result.tokens.completion_tokens == 75

    def test_total_tokens_correct(self):
        agent = BenchmarkAgent(_make_client(prompt_tokens=30, completion_tokens=70))
        result = agent.run("prompt")
        assert result.tokens.total_tokens == 100

    def test_zero_completion_tokens(self):
        agent = BenchmarkAgent(_make_client(prompt_tokens=5, completion_tokens=0))
        result = agent.run("prompt")
        assert result.tokens.total_tokens == 5


# ---------------------------------------------------------------------------
# Timing collection
# ---------------------------------------------------------------------------

class TestTimingCollection:
    def test_elapsed_seconds_positive(self):
        agent = BenchmarkAgent(_make_client())
        result = agent.run("prompt")
        assert result.timing.elapsed_seconds >= 0.0

    def test_elapsed_ms_positive(self):
        agent = BenchmarkAgent(_make_client())
        result = agent.run("prompt")
        assert result.timing.elapsed_ms >= 0.0

    def test_timing_captures_api_delay(self):
        """Verify the timer actually spans the API call."""
        client = MagicMock()
        usage = SimpleNamespace(prompt_tokens=5, completion_tokens=5)
        message = SimpleNamespace(content="ok")
        choice = SimpleNamespace(message=message)
        response = SimpleNamespace(usage=usage, choices=[choice])

        FAKE_DELAY = 0.05  # 50 ms simulated latency

        def slow_create(**kwargs):
            time.sleep(FAKE_DELAY)
            return response

        client.chat.completions.create.side_effect = slow_create

        agent = BenchmarkAgent(client)
        result = agent.run("prompt")
        assert result.timing.elapsed_seconds >= FAKE_DELAY

    def test_start_before_end(self):
        agent = BenchmarkAgent(_make_client())
        result = agent.run("prompt")
        assert result.timing.start_time <= result.timing.end_time


# ---------------------------------------------------------------------------
# Message construction
# ---------------------------------------------------------------------------

class TestMessageConstruction:
    def test_user_message_sent(self):
        client = _make_client()
        agent = BenchmarkAgent(client)
        agent.run("Tell me a joke")
        _, kwargs = client.chat.completions.create.call_args
        messages = kwargs["messages"]
        assert any(m["role"] == "user" and m["content"] == "Tell me a joke"
                   for m in messages)

    def test_system_prompt_prepended(self):
        client = _make_client()
        agent = BenchmarkAgent(client)
        agent.run("Hi", system_prompt="You are helpful.")
        _, kwargs = client.chat.completions.create.call_args
        messages = kwargs["messages"]
        assert messages[0] == {"role": "system", "content": "You are helpful."}
        assert messages[1]["role"] == "user"

    def test_no_system_prompt_by_default(self):
        client = _make_client()
        agent = BenchmarkAgent(client)
        agent.run("Hi")
        _, kwargs = client.chat.completions.create.call_args
        roles = [m["role"] for m in kwargs["messages"]]
        assert "system" not in roles

    def test_extra_params_forwarded(self):
        client = _make_client()
        agent = BenchmarkAgent(client)
        agent.run("prompt", extra_params={"temperature": 0.0, "max_tokens": 128})
        _, kwargs = client.chat.completions.create.call_args
        assert kwargs["temperature"] == 0.0
        assert kwargs["max_tokens"] == 128


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class TestInputValidation:
    def test_empty_prompt_raises(self):
        agent = BenchmarkAgent(_make_client())
        with pytest.raises(ValueError, match="empty"):
            agent.run("")

    def test_whitespace_only_prompt_raises(self):
        agent = BenchmarkAgent(_make_client())
        with pytest.raises(ValueError, match="empty"):
            agent.run("   ")
