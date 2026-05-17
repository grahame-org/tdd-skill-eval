"""Reporter utilities for formatting and outputting benchmark results."""

from __future__ import annotations

import csv
import io
import json
from typing import Iterable, List

from benchmark.metrics import BenchmarkResult


class BenchmarkReporter:
    """Formats and outputs :class:`BenchmarkResult` objects."""

    def to_json(self, result: BenchmarkResult, *, indent: int = 2) -> str:
        """Serialise a single result to a JSON string."""
        return json.dumps(result.to_dict(), indent=indent)

    def to_json_lines(self, results: Iterable[BenchmarkResult]) -> str:
        """Serialise multiple results as newline-delimited JSON."""
        lines = [json.dumps(r.to_dict()) for r in results]
        return "\n".join(lines)

    def to_csv(self, results: Iterable[BenchmarkResult]) -> str:
        """Serialise multiple results to a CSV string."""
        rows = [r.to_dict() for r in results]
        if not rows:
            return ""

        fieldnames = [
            "prompt",
            "model",
            "elapsed_seconds",
            "elapsed_ms",
            "prompt_tokens",
            "completion_tokens",
            "total_tokens",
            "response_text",
        ]

        buf = io.StringIO()
        writer = csv.DictWriter(
            buf, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
        return buf.getvalue()

    def to_text(self, result: BenchmarkResult) -> str:
        """Format a single result as a human-readable text block."""
        d = result.to_dict()
        lines = [
            f"Model         : {d['model']}",
            f"Prompt tokens : {d['prompt_tokens']}",
            f"Completion    : {d['completion_tokens']}",
            f"Total tokens  : {d['total_tokens']}",
            f"Elapsed       : {d['elapsed_ms']:.1f} ms",
        ]
        return "\n".join(lines)

    def summarise(self, results: List[BenchmarkResult]) -> dict:
        """Compute aggregate statistics over a list of results.

        Returns a dict with keys: ``count``, ``total_tokens_mean``,
        ``elapsed_ms_mean``, ``prompt_tokens_total``,
        ``completion_tokens_total``.

        When *results* is empty, ``count`` is ``0`` and all mean/total
        values are reported as ``0.0`` or ``0`` rather than being omitted
        or raising an error.
        """
        if not results:
            return {
                "count": 0,
                "total_tokens_mean": 0.0,
                "elapsed_ms_mean": 0.0,
                "prompt_tokens_total": 0,
                "completion_tokens_total": 0,
            }

        count = len(results)
        return {
            "count": count,
            "total_tokens_mean": sum(r.tokens.total_tokens for r in results) / count,
            "elapsed_ms_mean": sum(r.timing.elapsed_ms for r in results) / count,
            "prompt_tokens_total": sum(r.tokens.prompt_tokens for r in results),
            "completion_tokens_total": sum(r.tokens.completion_tokens for r in results),
        }
