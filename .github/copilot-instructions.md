# GitHub Copilot Instructions

## Development environment

The Copilot agent environment is pre-configured with:

- **Python 3.12**
- **pytest** (via `requirements-dev.txt`) – run tests with `python -m pytest tests/ -v`

## Available tools and packages

### `benchmark` package

A custom benchmarking agent (`benchmark/`) for measuring the time and token usage of LLM prompts via any OpenAI-compatible API.

| Module | Description |
|--------|-------------|
| `benchmark.agent.BenchmarkAgent` | Wraps an OpenAI-compatible client; records wall-clock timing around each `chat.completions.create` call and returns a `BenchmarkResult` |
| `benchmark.metrics.TimingMetrics` | Stores `start_time` / `end_time` (from `time.perf_counter`) and exposes `elapsed_seconds` / `elapsed_ms` |
| `benchmark.metrics.TokenMetrics` | Stores `prompt_tokens` / `completion_tokens` and `total_tokens`; constructed via `TokenMetrics.from_response(response)` which supports both dict-style and object-style API responses |
| `benchmark.metrics.BenchmarkResult` | Combines `TimingMetrics`, `TokenMetrics`, prompt, model, and response text into a serialisable result; `result.to_dict()` returns a flat dictionary |
| `benchmark.reporter.BenchmarkReporter` | Formats results as JSON (`.to_json`), JSON-Lines (`.to_json_lines`), CSV (`.to_csv`), plain text (`.to_text`), or aggregate summary statistics (`.summarise`) |

### Running the benchmark tests

```bash
python -m pytest tests/ -v
```

Expected output: 63 tests passing.

## Repository layout

```
benchmark/          # Benchmarking package (agent, metrics, reporter)
tests/              # pytest test suite (test_agent, test_metrics, test_reporter)
requirements.txt         # Runtime deps (none – stdlib only)
requirements-dev.txt     # Dev deps (pytest>=8.0)
.github/
  workflows/
    copilot-setup-steps.yml   # Pre-installs Python and pytest for agent sessions
```
