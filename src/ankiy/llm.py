"""A small OpenAI-compatible chat client.

Ollama exposes this protocol locally at http://localhost:11434/v1, so no cloud key
is needed for the default setup. Hosted compatible providers work by changing .env.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


class LLMError(RuntimeError):
    """An actionable failure to reach or parse the configured chat model."""


@dataclass(frozen=True, slots=True)
class LLMClient:
    base_url: str
    model: str
    api_key: str | None = None
    timeout_seconds: float = 90.0

    def chat(self, system_prompt: str, messages: list[dict[str, str]]) -> str:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}, *messages],
            "temperature": 0.85,
            "max_tokens": 500,
        }
        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except httpx.TimeoutException as error:
            raise LLMError("The chat model took too long to reply. Please try again.") from error
        except httpx.RequestError as error:
            raise LLMError(
                f"Could not reach the chat model at {self.base_url}. "
                "If you are using Ollama, start it and run `ollama pull llama3.2`."
            ) from error
        except httpx.HTTPStatusError as error:
            detail = _error_detail(error.response)
            raise LLMError(
                f"The chat model returned HTTP {error.response.status_code}: {detail}"
            ) from error

        try:
            body = response.json()
            content = body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise LLMError("The chat model returned an unexpected response format.") from error
        text = _content_to_text(content).strip()
        if not text:
            raise LLMError("The chat model returned an empty response. Please try again.")
        return text


def _content_to_text(content: Any) -> str:
    """Handle both ordinary OpenAI strings and a few content-part variants."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        chunks: list[str] = []
        for part in content:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                chunks.append(part["text"])
        return "".join(chunks)
    return ""


def _error_detail(response: httpx.Response) -> str:
    try:
        body = response.json()
        if isinstance(body, dict):
            error = body.get("error", body)
            if isinstance(error, dict) and error.get("message"):
                return str(error["message"])
    except ValueError:
        pass
    return response.text[:300] or "no error details returned"
