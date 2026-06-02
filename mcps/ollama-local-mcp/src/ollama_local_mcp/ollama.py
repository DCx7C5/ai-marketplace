"""Ollama client helpers and MCP tool implementations."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
import json
from typing import Any, Literal

import aiohttp

from .config import FALLBACK_MODEL, OLLAMA_BASE_URL, PRIMARY_MODEL, REQUEST_TIMEOUT_SECONDS

AssistOperation = Literal["summarize", "rewrite", "extract", "classify"]


class OllamaError(RuntimeError):
    """Raised when Ollama API requests fail."""


@dataclass(slots=True)
class MockTransportResponse:
    """Lightweight test response payload for injected transport handlers."""

    status: int
    json_data: dict[str, Any] | None = None
    text: str = ""
    lines: list[str] | None = None


TransportHandler = Callable[
    [str, str, dict[str, Any] | None],
    Awaitable[MockTransportResponse] | MockTransportResponse,
]


@dataclass(slots=True)
class OllamaClient:
    """Small async wrapper for Ollama local API."""

    base_url: str = OLLAMA_BASE_URL
    timeout_seconds: float = REQUEST_TIMEOUT_SECONDS
    transport: TransportHandler | None = None

    async def _transport_response(
        self,
        *,
        method: str,
        path: str,
        payload: dict[str, Any] | None,
    ) -> MockTransportResponse | None:
        if self.transport is None:
            return None

        result = self.transport(method, path, payload)
        if hasattr(result, "__await__"):
            result = await result
        return result

    async def _request(
        self,
        *,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> tuple[int, str, dict[str, Any]]:
        mocked = await self._transport_response(method=method, path=path, payload=payload)
        if mocked is not None:
            data = mocked.json_data or {}
            text = mocked.text or (json.dumps(data) if data else "")
            return mocked.status, text, data

        timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
        async with aiohttp.ClientSession(base_url=self.base_url, timeout=timeout) as client:
            async with client.request(method, path, json=payload) as response:
                text = await response.text()
                status = response.status

        data: dict[str, Any] = {}
        if text:
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict):
                    data = parsed
            except json.JSONDecodeError:
                data = {}

        return status, text, data

    async def _stream_generate(
        self,
        *,
        payload: dict[str, Any],
    ) -> tuple[int, str, list[dict[str, Any]]]:
        mocked = await self._transport_response(method="POST", path="/api/generate", payload=payload)
        if mocked is not None:
            lines = mocked.lines or ([mocked.text] if mocked.text else [])
            events: list[dict[str, Any]] = []
            for line in lines:
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(event, dict):
                    events.append(event)
            return mocked.status, mocked.text, events

        timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
        events: list[dict[str, Any]] = []
        async with aiohttp.ClientSession(base_url=self.base_url, timeout=timeout) as client:
            async with client.post("/api/generate", json=payload) as response:
                if response.status >= 400:
                    return response.status, await response.text(), []

                async for raw_line in response.content:
                    line = raw_line.decode("utf-8").strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(event, dict):
                        events.append(event)

                return response.status, "", events

    async def list_models(self) -> dict[str, Any]:
        status, text, payload = await self._request(method="GET", path="/api/tags")
        if status >= 400:
            raise OllamaError(text)

        models = payload.get("models", [])
        names = [m.get("name", "") for m in models if m.get("name")]
        return {"models": models, "model_names": names, "count": len(names)}

    async def generate(
        self,
        *,
        prompt: str,
        model: str,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system:
            payload["system"] = system
        if max_tokens is not None:
            payload["options"]["num_predict"] = max_tokens

        status, text, data = await self._request(method="POST", path="/api/generate", payload=payload)
        if status >= 400:
            raise OllamaError(text)

        return {
            "model": data.get("model", model),
            "response": data.get("response", ""),
            "done": bool(data.get("done", True)),
            "done_reason": data.get("done_reason"),
            "raw": data,
        }

    async def generate_stream(
        self,
        *,
        prompt: str,
        model: str,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": temperature},
        }
        if system:
            payload["system"] = system
        if max_tokens is not None:
            payload["options"]["num_predict"] = max_tokens

        status, text, events = await self._stream_generate(payload=payload)
        if status >= 400:
            raise OllamaError(text)

        chunks: list[str] = []
        event_count = 0
        final_model = model
        done = False
        done_reason: str | None = None

        for event in events:
            event_count += 1
            piece = event.get("response", "")
            if piece:
                chunks.append(piece)
            final_model = event.get("model", final_model)
            done = bool(event.get("done", done))
            if "done_reason" in event:
                done_reason = event.get("done_reason")

        return {
            "model": final_model,
            "chunks": chunks,
            "response": "".join(chunks),
            "done": done,
            "done_reason": done_reason,
            "events": event_count,
        }

    async def embeddings(self, *, text: str, model: str) -> dict[str, Any]:
        status, first_text, payload = await self._request(
            method="POST",
            path="/api/embed",
            payload={"model": model, "input": text},
        )
        if status < 400:
            embeddings_data = payload.get("embeddings", [])
            vector = embeddings_data[0] if embeddings_data else []
            return {"model": model, "embedding": vector, "dimensions": len(vector), "raw": payload}

        legacy_status, legacy_text, legacy_payload = await self._request(
            method="POST",
            path="/api/embeddings",
            payload={"model": model, "prompt": text},
        )
        if legacy_status >= 400:
            raise OllamaError(legacy_text or first_text)

        vector = legacy_payload.get("embedding", [])
        return {"model": model, "embedding": vector, "dimensions": len(vector), "raw": legacy_payload}


async def list_models(client: OllamaClient | None = None) -> dict[str, Any]:
    target = client or OllamaClient()
    return await target.list_models()


async def health(client: OllamaClient | None = None) -> dict[str, Any]:
    target = client or OllamaClient()
    try:
        model_info = await target.list_models()
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "reachable": False,
            "base_url": target.base_url,
            "primary_model": PRIMARY_MODEL,
            "fallback_model": FALLBACK_MODEL,
            "error": str(exc),
        }

    names = set(model_info["model_names"])
    primary_available = PRIMARY_MODEL in names
    fallback_available = FALLBACK_MODEL in names
    return {
        "ok": primary_available or fallback_available,
        "reachable": True,
        "base_url": target.base_url,
        "primary_model": PRIMARY_MODEL,
        "fallback_model": FALLBACK_MODEL,
        "primary_available": primary_available,
        "fallback_available": fallback_available,
        "model_count": model_info["count"],
        "models": model_info["model_names"],
    }


def _looks_like_missing_model(error: str) -> bool:
    message = error.lower()
    return "not found" in message or "model" in message and "pull" in message


def _bounded_text(value: str, limit: int = 8000) -> str:
    return value.strip()[:limit]


def build_assist_prompt(
    operation: AssistOperation,
    text: str,
    *,
    instructions: str | None = None,
    labels: list[str] | None = None,
) -> str:
    cleaned = _bounded_text(text)
    if not cleaned:
        raise ValueError("text is required")

    if operation == "summarize":
        extra = _bounded_text(instructions or "")
        suffix = f" Additional constraint: {extra}" if extra else ""
        return (
            "Summarize the text in at most 80 words. Keep key facts only. "
            "Return plain text only."
            f"{suffix}\n\nText:\n{cleaned}"
        )

    if operation == "rewrite":
        style = _bounded_text(instructions or "clear and concise")
        return (
            f"Rewrite the text to be {style}. Preserve meaning. "
            "Return only the rewritten text.\n\n"
            f"Text:\n{cleaned}"
        )

    if operation == "extract":
        schema = _bounded_text(instructions or "keywords")
        return (
            "Extract structured items from the text. "
            "Return strict JSON only in this shape: {\"items\": [\"...\"]}. "
            f"Extraction focus: {schema}.\n\n"
            f"Text:\n{cleaned}"
        )

    if operation == "classify":
        if not labels:
            raise ValueError("labels are required for classify")
        clean_labels = [_bounded_text(label, limit=128) for label in labels if label.strip()]
        if not clean_labels:
            raise ValueError("labels are required for classify")
        return (
            "Classify the text into exactly one label from this list: "
            + ", ".join(clean_labels)
            + ". Return only the chosen label.\n\nText:\n"
            + cleaned
        )

    raise ValueError(f"Unsupported operation: {operation}")


async def chat(
    *,
    prompt: str,
    model: str | None = None,
    system: str | None = None,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    client: OllamaClient | None = None,
) -> dict[str, Any]:
    selected_model = model or PRIMARY_MODEL
    target = client or OllamaClient()
    cleaned_prompt = _bounded_text(prompt)
    if not cleaned_prompt:
        raise ValueError("prompt is required")

    try:
        return await target.generate(
            prompt=cleaned_prompt,
            model=selected_model,
            system=_bounded_text(system or "", 1000) or None,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except OllamaError as exc:
        if selected_model != FALLBACK_MODEL and _looks_like_missing_model(str(exc)):
            result = await target.generate(
                prompt=cleaned_prompt,
                model=FALLBACK_MODEL,
                system=_bounded_text(system or "", 1000) or None,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result["fallback_used"] = True
            result["requested_model"] = selected_model
            return result
        raise


async def chat_stream(
    *,
    prompt: str,
    model: str | None = None,
    system: str | None = None,
    temperature: float = 0.0,
    max_tokens: int | None = None,
    client: OllamaClient | None = None,
) -> dict[str, Any]:
    target = client or OllamaClient()
    cleaned_prompt = _bounded_text(prompt)
    if not cleaned_prompt:
        raise ValueError("prompt is required")
    return await target.generate_stream(
        prompt=cleaned_prompt,
        model=model or PRIMARY_MODEL,
        system=_bounded_text(system or "", 1000) or None,
        temperature=temperature,
        max_tokens=max_tokens,
    )


async def embeddings(*, text: str, model: str | None = None, client: OllamaClient | None = None) -> dict[str, Any]:
    target = client or OllamaClient()
    cleaned_text = _bounded_text(text)
    if not cleaned_text:
        raise ValueError("text is required")
    return await target.embeddings(text=cleaned_text, model=model or PRIMARY_MODEL)


async def assist(
    *,
    operation: AssistOperation,
    text: str,
    instructions: str | None = None,
    labels: list[str] | None = None,
    model: str | None = None,
    client: OllamaClient | None = None,
) -> dict[str, Any]:
    prompt = build_assist_prompt(operation, text, instructions=instructions, labels=labels)
    result = await chat(
        prompt=prompt,
        model=model,
        system="You are a lightweight local assistant. Follow instructions exactly.",
        temperature=0.0,
        max_tokens=256,
        client=client,
    )
    return {
        "operation": operation,
        "model": result.get("model"),
        "output": result.get("response", "").strip(),
        "fallback_used": bool(result.get("fallback_used", False)),
    }
