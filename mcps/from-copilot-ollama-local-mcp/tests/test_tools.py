"""Tests for ollama-local-mcp core behavior."""

from __future__ import annotations

import json

import httpx
import pytest

from ollama_local_mcp.config import FALLBACK_MODEL, PRIMARY_MODEL
from ollama_local_mcp.ollama import OllamaClient, assist, build_assist_prompt, chat, embeddings, health


@pytest.mark.asyncio
async def test_list_models_and_health_ok() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tags":
            return httpx.Response(
                200,
                json={
                    "models": [
                        {"name": PRIMARY_MODEL},
                        {"name": FALLBACK_MODEL},
                    ]
                },
            )
        raise AssertionError(f"unexpected route: {request.url.path}")

    client = OllamaClient(transport=httpx.MockTransport(handler))
    models = await client.list_models()
    assert models["count"] == 2
    assert PRIMARY_MODEL in models["model_names"]

    status = await health(client)
    assert status["ok"] is True
    assert status["primary_available"] is True
    assert status["fallback_available"] is True


@pytest.mark.asyncio
async def test_chat_uses_fallback_on_missing_model() -> None:
    call_count = {"generate": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/generate":
            call_count["generate"] += 1
            payload = json.loads(request.content.decode("utf-8"))
            if payload["model"] == PRIMARY_MODEL:
                return httpx.Response(404, text="model not found, please pull")
            if payload["model"] == FALLBACK_MODEL:
                return httpx.Response(200, json={"model": FALLBACK_MODEL, "response": "ok", "done": True})
        raise AssertionError(f"unexpected request: {request.url.path}")

    client = OllamaClient(transport=httpx.MockTransport(handler))
    result = await chat(prompt="hello", client=client)

    assert result["model"] == FALLBACK_MODEL
    assert result["fallback_used"] is True
    assert call_count["generate"] == 2


@pytest.mark.asyncio
async def test_embeddings_new_and_legacy_endpoints() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/embed":
            return httpx.Response(404, text="not found")
        if request.url.path == "/api/embeddings":
            return httpx.Response(200, json={"embedding": [0.1, 0.2, 0.3]})
        raise AssertionError(f"unexpected request: {request.url.path}")

    client = OllamaClient(transport=httpx.MockTransport(handler))
    result = await embeddings(text="abc", client=client)
    assert result["dimensions"] == 3
    assert result["embedding"] == [0.1, 0.2, 0.3]


@pytest.mark.asyncio
async def test_assist_classify_constrained_output_shape() -> None:
    captured_prompt: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/generate":
            payload = json.loads(request.content.decode("utf-8"))
            captured_prompt["prompt"] = payload["prompt"]
            return httpx.Response(200, json={"model": PRIMARY_MODEL, "response": "bug", "done": True})
        raise AssertionError(f"unexpected route: {request.url.path}")

    client = OllamaClient(transport=httpx.MockTransport(handler))
    result = await assist(
        operation="classify",
        text="Null pointer exception in parser",
        labels=["bug", "feature", "question"],
        client=client,
    )

    assert result["operation"] == "classify"
    assert result["output"] == "bug"
    assert "Return only the chosen label" in captured_prompt["prompt"]


def test_build_assist_prompt_validation() -> None:
    with pytest.raises(ValueError):
        build_assist_prompt("classify", "x", labels=[])
