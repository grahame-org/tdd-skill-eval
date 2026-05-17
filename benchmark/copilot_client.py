"""GitHub Copilot / GitHub Models client for use with BenchmarkAgent.

Uses the GitHub Models inference endpoint with a ``GITHUB_TOKEN`` for
authentication.  No third-party libraries are required; all HTTP calls are
made with the standard-library ``urllib`` package.

Typical usage::

    import os
    from benchmark.copilot_client import CopilotClient
    from benchmark import BenchmarkAgent

    client = CopilotClient(github_token=os.environ["GITHUB_TOKEN"])
    agent  = BenchmarkAgent(client, model="gpt-4o")
    result = agent.run("Explain the halting problem in one sentence.")
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

GITHUB_MODELS_BASE_URL = "https://models.inference.ai.azure.com"


class CopilotClient:
    """Minimal OpenAI-compatible client backed by the GitHub Models endpoint.

    The client exposes the same ``client.chat.completions.create(model, messages,
    **kwargs)`` interface that :class:`~benchmark.agent.BenchmarkAgent` expects,
    so it can be passed directly::

        agent = BenchmarkAgent(CopilotClient(token), model="gpt-4o")

    Parameters
    ----------
    github_token:
        A GitHub personal-access token (or the ``GITHUB_TOKEN`` secret
        available in GitHub Actions / Copilot coding-agent environments)
        that has permission to use GitHub Models.
    base_url:
        Override the default GitHub Models inference endpoint.  Useful for
        testing or when pointing at a compatible self-hosted endpoint.
    """

    def __init__(
        self,
        github_token: str,
        base_url: str = GITHUB_MODELS_BASE_URL,
    ) -> None:
        if not github_token:
            raise ValueError("github_token must not be empty.")
        self._token = github_token
        self._base_url = base_url.rstrip("/")
        self.chat = _ChatNamespace(self)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _post(self, path: str, body: dict) -> dict:
        """POST *body* as JSON to *path* and return the decoded response dict.

        Raises
        ------
        RuntimeError
            When the server returns a non-2xx HTTP status code.
        """
        url = f"{self._base_url}{path}"
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            raise RuntimeError(
                f"GitHub Models API returned HTTP {exc.code}: {detail}"
            ) from exc


class _ChatNamespace:
    def __init__(self, client: CopilotClient) -> None:
        self.completions = _CompletionsNamespace(client)


class _CompletionsNamespace:
    def __init__(self, client: CopilotClient) -> None:
        self._client = client

    def create(self, model: str, messages: list, **kwargs: Any) -> dict:
        """Send a chat-completions request and return the raw response dict.

        Parameters
        ----------
        model:
            Model identifier (e.g. ``"gpt-4o"``).
        messages:
            List of ``{"role": ..., "content": ...}`` dicts.
        **kwargs:
            Additional parameters forwarded to the API (e.g. ``temperature``,
            ``max_tokens``).

        Returns
        -------
        dict
            The raw JSON response from the GitHub Models API, which is
            compatible with both :class:`~benchmark.metrics.TokenMetrics` and
            the choices-extraction logic in
            :class:`~benchmark.agent.BenchmarkAgent`.
        """
        body: dict[str, Any] = {"model": model, "messages": messages, **kwargs}
        return self._client._post("/chat/completions", body)
