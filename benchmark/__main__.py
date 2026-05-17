"""Command-line interface for running a benchmark against GitHub Copilot.

Usage::

    GITHUB_TOKEN=<token> python -m benchmark "Your prompt here"
    GITHUB_TOKEN=<token> python -m benchmark "Your prompt" --model gpt-4o --format json

The ``GITHUB_TOKEN`` environment variable must be set to a GitHub personal-
access token (or the token injected automatically in GitHub Actions / Copilot
coding-agent environments) that has permission to use GitHub Models.
"""

from __future__ import annotations

import argparse
import os
import sys

from benchmark.agent import BenchmarkAgent
from benchmark.copilot_client import CopilotClient
from benchmark.reporter import BenchmarkReporter


def main(argv: list[str] | None = None) -> int:
    """Entry point for ``python -m benchmark``.

    Returns
    -------
    int
        Exit code: 0 on success, non-zero on error.
    """
    parser = argparse.ArgumentParser(
        prog="python -m benchmark",
        description=(
            "Benchmark a prompt against GitHub Copilot / GitHub Models and "
            "report token usage and latency."
        ),
    )
    parser.add_argument("prompt", help="Prompt text to evaluate.")
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Model name to use (default: gpt-4o-mini).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text).",
    )
    args = parser.parse_args(argv)

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print(
            "Error: GITHUB_TOKEN environment variable is not set.\n"
            "Set it to a GitHub token with GitHub Models access before running.",
            file=sys.stderr,
        )
        return 1

    client = CopilotClient(github_token)
    agent = BenchmarkAgent(client, model=args.model)

    try:
        result = agent.run(args.prompt)
    except RuntimeError as exc:
        print(f"Error calling GitHub Models API: {exc}", file=sys.stderr)
        return 1

    reporter = BenchmarkReporter()
    if args.format == "json":
        print(reporter.to_json(result))
    else:
        print(reporter.to_text(result))

    return 0


if __name__ == "__main__":
    sys.exit(main())
