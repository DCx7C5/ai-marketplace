# ollama-local-mcp

Local MCP server for Ollama at `http://127.0.0.1:11434`.

Default CPU-friendly models:
- primary: `phi4-mini:latest`
- fallback: `qwen3:0.6b`

## Tools

- `list_models` – list locally available Ollama models
- `health` – connectivity + default model diagnostics
- `chat` – single-turn non-streaming completion
- `chat_stream` – streaming completion passthrough
- `embeddings` – local embedding generation
- `assist` – constrained helper operations:
  - `summarize`
  - `rewrite`
  - `extract`
  - `classify`

`assist` intentionally stays lightweight and bounded for small local models.

## Setup

```bash
cd /home/daen/Projects/ai-marketplace/mcps/ollama-local-mcp
uv sync --group dev
```

## Run MCP server (stdio)

```bash
uv run ollama-local-mcp
```

## Quick examples

```python
# list_models
{"tool": "list_models"}

# health
{"tool": "health"}

# chat
{
  "tool": "chat",
  "arguments": {
    "prompt": "Give 3 secure coding tips.",
    "temperature": 0.0
  }
}

# chat_stream
{
  "tool": "chat_stream",
  "arguments": {
    "prompt": "Explain SQL injection in 2 short paragraphs."
  }
}

# embeddings
{
  "tool": "embeddings",
  "arguments": {
    "text": "MCP local embeddings test"
  }
}

# assist
{
  "tool": "assist",
  "arguments": {
    "operation": "classify",
    "text": "The API returns 500 on malformed JSON.",
    "labels": ["bug", "feature", "question"]
  }
}
```
