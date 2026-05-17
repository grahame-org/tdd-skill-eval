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
| `benchmark.copilot_client.CopilotClient` | Minimal OpenAI-compatible client backed by the **GitHub Copilot API** (`https://api.individual.githubcopilot.com`). Authenticates with a `GITHUB_TOKEN`; no third-party libraries required. Pass directly to `BenchmarkAgent`. |
| `benchmark.metrics.TimingMetrics` | Stores `start_time` / `end_time` (from `time.perf_counter`) and exposes `elapsed_seconds` / `elapsed_ms` |
| `benchmark.metrics.TokenMetrics` | Stores `prompt_tokens` / `completion_tokens` and `total_tokens`; constructed via `TokenMetrics.from_response(response)` which supports both dict-style and object-style API responses |
| `benchmark.metrics.BenchmarkResult` | Combines `TimingMetrics`, `TokenMetrics`, prompt, model, and response text into a serializable result; `result.to_dict()` returns a flat dictionary |
| `benchmark.reporter.BenchmarkReporter` | Formats results as JSON (`.to_json`), JSON-Lines (`.to_json_lines`), CSV (`.to_csv`), plain text (`.to_text`), or aggregate summary statistics (`.summarise`) |

### Benchmarking GitHub Copilot from the agent environment

The `GITHUB_TOKEN` secret is available in the Copilot coding-agent environment and has GitHub Copilot access. Use it to benchmark prompts directly:

```bash
# Plain-text output (default)
python -m benchmark "Explain the halting problem in one sentence."

# JSON output, custom model
python -m benchmark "What is 2+2?" --model gpt-4.1 --format json
```

Or call the API from Python:

```python
import os
from benchmark import BenchmarkAgent, CopilotClient
from benchmark.reporter import BenchmarkReporter

client  = CopilotClient(github_token=os.environ["GITHUB_TOKEN"])
agent   = BenchmarkAgent(client, model="gpt-4o-mini")
result  = agent.run("Explain the halting problem in one sentence.")

reporter = BenchmarkReporter()
print(reporter.to_text(result))
# Model         : gpt-4o-mini
# Prompt tokens : 12
# Completion    : 30
# Total tokens  : 42
# Elapsed       : 823.4 ms
```

### Running the benchmark tests

```bash
python -m pytest tests/ -v
```

Expected output: 86 tests passing.

## Repository layout

```
benchmark/                   # Benchmarking package
  agent.py                   # BenchmarkAgent – timing wrapper
  copilot_client.py          # CopilotClient – GitHub Models HTTP client
  metrics.py                 # TimingMetrics / TokenMetrics / BenchmarkResult
  reporter.py                # BenchmarkReporter – JSON/CSV/text/summary output
  __main__.py                # CLI: python -m benchmark "prompt"
tests/                       # pytest test suite
  test_agent.py
  test_copilot_client.py
  test_metrics.py
  test_reporter.py
requirements.txt             # Runtime deps (none – stdlib only)
requirements-dev.txt         # Dev deps (pytest>=8.0)
.github/
  workflows/
    copilot-setup-steps.yml  # Pre-installs Python and pytest for agent sessions
```
