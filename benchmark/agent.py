"""Custom benchmarking agent that measures time and token usage for LLM prompts."""

from __future__ import annotations

import time
from typing import Any, Optional

from benchmark.metrics import BenchmarkResult, TimingMetrics, TokenMetrics


class BenchmarkAgent:
    """Agent that wraps an LLM client and records timing and token metrics.

    Parameters
    ----------
    client:
        An OpenAI-compatible client object that exposes
        ``client.chat.completions.create(model=..., messages=[...])``.
    model:
        Default model name to use when none is supplied per-call.
    """

    def __init__(self, client: Any, model: str = "gpt-4o") -> None:
        self._client = client
        self.model = model

    def run(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        extra_params: Optional[dict] = None,
    ) -> BenchmarkResult:
        """Run a single prompt and return a :class:`BenchmarkResult`.

        Parameters
        ----------
        prompt:
            User message to send.
        model:
            Override the agent's default model for this call.
        system_prompt:
            Optional system message prepended before the user message.
        extra_params:
            Additional keyword arguments forwarded to the API call (e.g.
            ``temperature``, ``max_tokens``).

        Returns
        -------
        BenchmarkResult
            Contains timing, token usage, and the first response message.

        Raises
        ------
        ValueError
            If *prompt* is empty.
        """
        if not prompt or not prompt.strip():
            raise ValueError("prompt must not be empty.")

        target_model = model or self.model
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        params = dict(extra_params or {})

        start = time.perf_counter()
        response = self._client.chat.completions.create(
            model=target_model, messages=messages, **params
        )
        end = time.perf_counter()

        timing = TimingMetrics(start_time=start, end_time=end)
        tokens = TokenMetrics.from_response(response)

        if isinstance(response, dict):
            choices = response.get("choices", [])
        else:
            choices = getattr(response, "choices", []) or []
        response_text = ""
        if choices:
            first = choices[0]
            if isinstance(first, dict):
                response_text = first.get("message", {}).get("content", "")
            else:
                response_text = getattr(
                    getattr(first, "message", None), "content", ""
                ) or ""

        return BenchmarkResult(
            prompt=prompt,
            model=target_model,
            timing=timing,
            tokens=tokens,
            response_text=response_text,
        )
