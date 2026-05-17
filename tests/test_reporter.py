"""Tests for BenchmarkReporter – formatting and summary output."""

from __future__ import annotations

import csv
import io
import json

import pytest

from benchmark.metrics import BenchmarkResult, TimingMetrics, TokenMetrics
from benchmark.reporter import BenchmarkReporter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _result(
    prompt="test prompt",
    model="gpt-4o",
    elapsed=0.5,
    prompt_tokens=10,
    completion_tokens=20,
    response_text="",
):
    timing = TimingMetrics(start_time=0.0, end_time=elapsed)
    tokens = TokenMetrics(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)
    return BenchmarkResult(
        prompt=prompt,
        model=model,
        timing=timing,
        tokens=tokens,
        response_text=response_text,
    )


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

class TestToJson:
    def test_returns_valid_json(self):
        reporter = BenchmarkReporter()
        raw = reporter.to_json(_result())
        parsed = json.loads(raw)  # must not raise
        assert isinstance(parsed, dict)

    def test_contains_all_keys(self):
        reporter = BenchmarkReporter()
        parsed = json.loads(reporter.to_json(_result()))
        for key in ("prompt", "model", "elapsed_seconds", "elapsed_ms",
                    "prompt_tokens", "completion_tokens", "total_tokens"):
            assert key in parsed, f"Missing key: {key}"

    def test_token_values_correct(self):
        reporter = BenchmarkReporter()
        parsed = json.loads(reporter.to_json(_result(prompt_tokens=7, completion_tokens=13)))
        assert parsed["prompt_tokens"] == 7
        assert parsed["completion_tokens"] == 13
        assert parsed["total_tokens"] == 20

    def test_elapsed_value_correct(self):
        reporter = BenchmarkReporter()
        parsed = json.loads(reporter.to_json(_result(elapsed=2.0)))
        assert parsed["elapsed_seconds"] == pytest.approx(2.0)
        assert parsed["elapsed_ms"] == pytest.approx(2000.0)


# ---------------------------------------------------------------------------
# JSON-lines output
# ---------------------------------------------------------------------------

class TestToJsonLines:
    def test_one_line_per_result(self):
        reporter = BenchmarkReporter()
        results = [_result(), _result(elapsed=1.0)]
        output = reporter.to_json_lines(results)
        lines = output.strip().splitlines()
        assert len(lines) == 2

    def test_each_line_is_valid_json(self):
        reporter = BenchmarkReporter()
        results = [_result(prompt_tokens=i, completion_tokens=i) for i in range(5)]
        output = reporter.to_json_lines(results)
        for line in output.splitlines():
            json.loads(line)  # must not raise

    def test_empty_list(self):
        reporter = BenchmarkReporter()
        output = reporter.to_json_lines([])
        assert output == ""


# ---------------------------------------------------------------------------
# CSV output
# ---------------------------------------------------------------------------

class TestToCsv:
    def _parse_csv(self, text: str):
        reader = csv.DictReader(io.StringIO(text))
        return list(reader)

    def test_returns_header_row(self):
        reporter = BenchmarkReporter()
        output = reporter.to_csv([_result()])
        assert "prompt_tokens" in output
        assert "completion_tokens" in output
        assert "total_tokens" in output
        assert "elapsed_ms" in output

    def test_one_data_row_per_result(self):
        reporter = BenchmarkReporter()
        rows = self._parse_csv(reporter.to_csv([_result(), _result()]))
        assert len(rows) == 2

    def test_token_values_in_csv(self):
        reporter = BenchmarkReporter()
        rows = self._parse_csv(
            reporter.to_csv([_result(prompt_tokens=11, completion_tokens=22)])
        )
        assert rows[0]["prompt_tokens"] == "11"
        assert rows[0]["completion_tokens"] == "22"
        assert rows[0]["total_tokens"] == "33"

    def test_empty_list_returns_empty_string(self):
        reporter = BenchmarkReporter()
        assert reporter.to_csv([]) == ""


# ---------------------------------------------------------------------------
# Text output
# ---------------------------------------------------------------------------

class TestToText:
    def test_contains_model(self):
        reporter = BenchmarkReporter()
        text = reporter.to_text(_result(model="gpt-4o-mini"))
        assert "gpt-4o-mini" in text

    def test_contains_token_counts(self):
        reporter = BenchmarkReporter()
        text = reporter.to_text(_result(prompt_tokens=5, completion_tokens=15))
        assert "5" in text
        assert "15" in text
        assert "20" in text

    def test_contains_elapsed_ms(self):
        reporter = BenchmarkReporter()
        text = reporter.to_text(_result(elapsed=0.1))
        assert "100.0" in text


# ---------------------------------------------------------------------------
# Summary statistics
# ---------------------------------------------------------------------------

class TestSummarise:
    def test_empty_list(self):
        reporter = BenchmarkReporter()
        summary = reporter.summarise([])
        assert summary["count"] == 0
        assert summary["total_tokens_mean"] == 0.0
        assert summary["elapsed_ms_mean"] == 0.0

    def test_count(self):
        reporter = BenchmarkReporter()
        results = [_result() for _ in range(3)]
        assert reporter.summarise(results)["count"] == 3

    def test_total_tokens_mean(self):
        reporter = BenchmarkReporter()
        # 30 tokens each (10+20), 3 results → mean = 30
        results = [_result(prompt_tokens=10, completion_tokens=20) for _ in range(3)]
        assert reporter.summarise(results)["total_tokens_mean"] == pytest.approx(30.0)

    def test_elapsed_ms_mean(self):
        reporter = BenchmarkReporter()
        results = [
            _result(elapsed=0.1),
            _result(elapsed=0.3),
        ]
        # 100 ms, 300 ms → mean = 200 ms
        assert reporter.summarise(results)["elapsed_ms_mean"] == pytest.approx(200.0)

    def test_prompt_tokens_total(self):
        reporter = BenchmarkReporter()
        results = [_result(prompt_tokens=10) for _ in range(4)]
        assert reporter.summarise(results)["prompt_tokens_total"] == 40

    def test_completion_tokens_total(self):
        reporter = BenchmarkReporter()
        results = [_result(completion_tokens=5) for _ in range(6)]
        assert reporter.summarise(results)["completion_tokens_total"] == 30

    def test_single_result(self):
        reporter = BenchmarkReporter()
        summary = reporter.summarise([_result(elapsed=0.25, prompt_tokens=8, completion_tokens=12)])
        assert summary["count"] == 1
        assert summary["total_tokens_mean"] == pytest.approx(20.0)
        assert summary["elapsed_ms_mean"] == pytest.approx(250.0)
