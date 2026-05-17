"""Metrics data classes for collecting time and token usage."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TimingMetrics:
    """Wall-clock timing for a single LLM request."""

    start_time: float
    end_time: float

    @property
    def elapsed_seconds(self) -> float:
        """Total elapsed time in seconds."""
        return self.end_time - self.start_time

    @property
    def elapsed_ms(self) -> float:
        """Total elapsed time in milliseconds."""
        return self.elapsed_seconds * 1000.0


@dataclass
class TokenMetrics:
    """Token usage reported by the LLM API."""

    prompt_tokens: int
    completion_tokens: int

    @property
    def total_tokens(self) -> int:
        """Sum of prompt and completion tokens."""
        return self.prompt_tokens + self.completion_tokens

    @classmethod
    def from_response(cls, response: Any) -> "TokenMetrics":
        """Extract token metrics from an OpenAI-compatible API response.

        Supports both object-style (``response.usage.prompt_tokens``) and
        dict-style (``response["usage"]["prompt_tokens"]``) responses.

        Raises:
            ValueError: if usage information is missing from the response.
        """
        if response is None:
            raise ValueError("Response is None; cannot extract token metrics.")

        # Dict-style response
        if isinstance(response, dict):
            usage = response.get("usage")
            if usage is None:
                raise ValueError("Response dict has no 'usage' key.")
            prompt = usage.get("prompt_tokens")
            completion = usage.get("completion_tokens")
        else:
            # Object-style response (e.g. openai.types.chat.ChatCompletion)
            usage = getattr(response, "usage", None)
            if usage is None:
                raise ValueError("Response object has no 'usage' attribute.")
            prompt = getattr(usage, "prompt_tokens", None)
            completion = getattr(usage, "completion_tokens", None)

        if prompt is None or completion is None:
            raise ValueError(
                "Token metrics incomplete: prompt_tokens or completion_tokens missing."
            )

        return cls(prompt_tokens=int(prompt), completion_tokens=int(completion))


@dataclass
class BenchmarkResult:
    """Combined benchmark result for a single prompt run."""

    prompt: str
    model: str
    timing: TimingMetrics
    tokens: TokenMetrics
    response_text: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialise the result to a plain dictionary."""
        return {
            "prompt": self.prompt,
            "model": self.model,
            "elapsed_seconds": self.timing.elapsed_seconds,
            "elapsed_ms": self.timing.elapsed_ms,
            "prompt_tokens": self.tokens.prompt_tokens,
            "completion_tokens": self.tokens.completion_tokens,
            "total_tokens": self.tokens.total_tokens,
            "response_text": self.response_text,
            "metadata": self.metadata,
        }
