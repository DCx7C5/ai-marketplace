"""FastMCP server wiring for ollama-local-mcp."""

from __future__ import annotations

from typing import Any, cast

from fastmcp import FastMCP

from .ollama import AssistOperation, assist, chat, chat_stream, embeddings, health, list_models

mcp = FastMCP(
    name="ollama-local-mcp",
    instructions=(
        "Local Ollama MCP server exposing lightweight local inference and helper tools. "
        "Optimized for small CPU-friendly models."
    ),
)


@mcp.tool(name="list_models", description="List locally available models from Ollama API")
async def list_models_tool() -> dict[str, Any]:
    return await list_models()


@mcp.tool(name="health", description="Connectivity and model availability diagnostics")
async def health_tool() -> dict[str, Any]:
    return await health()


@mcp.tool(name="chat", description="Single-turn non-streaming local completion")
async def chat_tool(
    prompt: str,
    model: str | None = None,
    system: str | None = None,
    temperature: float = 0.0,
    max_tokens: int | None = None,
) -> dict[str, Any]:
    return await chat(prompt=prompt, model=model, system=system, temperature=temperature, max_tokens=max_tokens)


@mcp.tool(name="chat_stream", description="Streaming completion passthrough")
async def chat_stream_tool(
    prompt: str,
    model: str | None = None,
    system: str | None = None,
    temperature: float = 0.0,
    max_tokens: int | None = None,
) -> dict[str, Any]:
    return await chat_stream(prompt=prompt, model=model, system=system, temperature=temperature, max_tokens=max_tokens)


@mcp.tool(name="embeddings", description="Local embedding generation")
async def embeddings_tool(text: str, model: str | None = None) -> dict[str, Any]:
    return await embeddings(text=text, model=model)


@mcp.tool(
    name="assist",
    description=(
        "Lightweight constrained helper for small models. "
        "Supported operations: summarize, rewrite, extract, classify"
    ),
)
async def assist_tool(
    operation: str,
    text: str,
    instructions: str | None = None,
    labels: list[str] | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    if operation not in {"summarize", "rewrite", "extract", "classify"}:
        raise ValueError("operation must be one of: summarize, rewrite, extract, classify")

    op = cast(AssistOperation, operation)
    return await assist(
        operation=op,
        text=text,
        instructions=instructions,
        labels=labels,
        model=model,
    )


async def run() -> None:
    """Run the MCP server over stdio."""
    await mcp.run_stdio_async(show_banner=False, stateless=False)
