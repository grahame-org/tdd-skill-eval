"""Tests for benchmark.metrics – timing and token data collection."""

import pytest

from benchmark.metrics import BenchmarkResult, TimingMetrics, TokenMetrics


# ---------------------------------------------------------------------------
# TimingMetrics
# ---------------------------------------------------------------------------

class TestTimingMetrics:
    def test_elapsed_seconds(self):
        t = TimingMetrics(start_time=100.0, end_time=101.5)
        assert t.elapsed_seconds == pytest.approx(1.5)

    def test_elapsed_ms(self):
        t = TimingMetrics(start_time=0.0, end_time=0.25)
        assert t.elapsed_ms == pytest.approx(250.0)

    def test_zero_elapsed(self):
        t = TimingMetrics(start_time=5.0, end_time=5.0)
        assert t.elapsed_seconds == pytest.approx(0.0)
        assert t.elapsed_ms == pytest.approx(0.0)

    def test_sub_millisecond(self):
        t = TimingMetrics(start_time=0.0, end_time=0.0001)
        assert t.elapsed_ms == pytest.approx(0.1)


# ---------------------------------------------------------------------------
# TokenMetrics – dict-style response
# ---------------------------------------------------------------------------

class TestTokenMetricsFromDict:
    def _make_response(self, prompt_tokens, completion_tokens):
        return {
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            }
        }

    def test_total_tokens(self):
        m = TokenMetrics.from_response(self._make_response(10, 20))
        assert m.total_tokens == 30

    def test_prompt_tokens(self):
        m = TokenMetrics.from_response(self._make_response(7, 3))
        assert m.prompt_tokens == 7

    def test_completion_tokens(self):
        m = TokenMetrics.from_response(self._make_response(7, 3))
        assert m.completion_tokens == 3

    def test_zero_completion_tokens(self):
        m = TokenMetrics.from_response(self._make_response(5, 0))
        assert m.total_tokens == 5
        assert m.completion_tokens == 0

    def test_large_token_counts(self):
        m = TokenMetrics.from_response(self._make_response(8192, 4096))
        assert m.total_tokens == 12288

    def test_missing_usage_key_raises(self):
        with pytest.raises(ValueError, match="usage"):
            TokenMetrics.from_response({"choices": []})

    def test_none_response_raises(self):
        with pytest.raises(ValueError, match="None"):
            TokenMetrics.from_response(None)

    def test_missing_prompt_tokens_raises(self):
        with pytest.raises(ValueError, match="incomplete"):
            TokenMetrics.from_response({"usage": {"completion_tokens": 5}})

    def test_missing_completion_tokens_raises(self):
        with pytest.raises(ValueError, match="incomplete"):
            TokenMetrics.from_response({"usage": {"prompt_tokens": 5}})


# ---------------------------------------------------------------------------
# TokenMetrics – object-style response
# ---------------------------------------------------------------------------

class _Usage:
    def __init__(self, prompt_tokens, completion_tokens):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens


class _Response:
    def __init__(self, prompt_tokens, completion_tokens):
        self.usage = _Usage(prompt_tokens, completion_tokens)


class TestTokenMetricsFromObject:
    def test_total_tokens(self):
        m = TokenMetrics.from_response(_Response(15, 25))
        assert m.total_tokens == 40

    def test_prompt_and_completion(self):
        m = TokenMetrics.from_response(_Response(8, 12))
        assert m.prompt_tokens == 8
        assert m.completion_tokens == 12

    def test_no_usage_attribute_raises(self):
        class NoUsage:
            pass

        with pytest.raises(ValueError, match="usage"):
            TokenMetrics.from_response(NoUsage())

    def test_missing_prompt_tokens_raises(self):
        class BadUsage:
            completion_tokens = 5

        class BadResponse:
            usage = BadUsage()

        with pytest.raises(ValueError, match="incomplete"):
            TokenMetrics.from_response(BadResponse())


# ---------------------------------------------------------------------------
# BenchmarkResult
# ---------------------------------------------------------------------------

class TestBenchmarkResult:
    def _make_result(self, prompt="hello", model="gpt-4o", elapsed=0.5,
                     prompt_tokens=10, completion_tokens=20):
        timing = TimingMetrics(start_time=0.0, end_time=elapsed)
        tokens = TokenMetrics(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
        return BenchmarkResult(prompt=prompt, model=model, timing=timing, tokens=tokens)

    def test_to_dict_keys(self):
        r = self._make_result()
        d = r.to_dict()
        expected_keys = {
            "prompt", "model", "elapsed_seconds", "elapsed_ms",
            "prompt_tokens", "completion_tokens", "total_tokens",
            "response_text", "metadata",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_values(self):
        r = self._make_result(elapsed=1.0, prompt_tokens=5, completion_tokens=15)
        d = r.to_dict()
        assert d["elapsed_seconds"] == pytest.approx(1.0)
        assert d["elapsed_ms"] == pytest.approx(1000.0)
        assert d["prompt_tokens"] == 5
        assert d["completion_tokens"] == 15
        assert d["total_tokens"] == 20

    def test_default_response_text_empty(self):
        r = self._make_result()
        assert r.response_text == ""

    def test_response_text_preserved(self):
        timing = TimingMetrics(0.0, 0.1)
        tokens = TokenMetrics(1, 1)
        r = BenchmarkResult("hi", "m", timing, tokens, response_text="hello!")
        assert r.to_dict()["response_text"] == "hello!"

    def test_metadata_preserved(self):
        timing = TimingMetrics(0.0, 0.1)
        tokens = TokenMetrics(1, 1)
        r = BenchmarkResult("hi", "m", timing, tokens, metadata={"run_id": 42})
        assert r.to_dict()["metadata"] == {"run_id": 42}
