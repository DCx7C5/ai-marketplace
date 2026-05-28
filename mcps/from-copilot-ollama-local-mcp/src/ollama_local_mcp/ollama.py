"""Ollama client helpers and MCP tool implementations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

import httpx

from .config import FALLBACK_MODEL, OLLAMA_BASE_URL, PRIMARY_MODEL, REQUEST_TIMEOUT_SECONDS

AssistOperation = Literal["summarize", "rewrite", "extract", "classify"]


class OllamaError(RuntimeError):
    """Raised when Ollama API requests fail."""


@dataclass(slots=True)
class OllamaClient:
    """Small async wrapper for Ollama local API."""

    base_url: str = OLLAMA_BASE_URL
    timeout_seconds: float = REQUEST_TIMEOUT_SECONDS
    transport: httpx.AsyncBaseTransport | None = None

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout_seconds, transport=self.transport)

    async def list_models(self) -> dict[str, Any]:
        async with self._client() as client:
            response = await client.get("/api/tags")
            response.raise_for_status()
            payload = response.json()

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

        async with self._client() as client:
            response = await client.post("/api/generate", json=payload)
            if response.status_code >= 400:
                raise OllamaError(response.text)
            data = response.json()

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

        chunks: list[str] = []
        event_count = 0
        final_model = model
        done = False
        done_reason: str | None = None

        async with self._client() as client:
            async with client.stream("POST", "/api/generate", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    event_count += 1
                    event = httpx.Response(200, text=line).json()
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
        async with self._client() as client:
            embed_response = await client.post("/api/embed", json={"model": model, "input": text})
            if embed_response.status_code < 400:
                payload = embed_response.json()
                embeddings = payload.get("embeddings", [])
                vector = embeddings[0] if embeddings else []
                return {"model": model, "embedding": vector, "dimensions": len(vector), "raw": payload}

            legacy_response = await client.post("/api/embeddings", json={"model": model, "prompt": text})
            if legacy_response.status_code >= 400:
                raise OllamaError(legacy_response.text)
            legacy_payload = legacy_response.json()

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
