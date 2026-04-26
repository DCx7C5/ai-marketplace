# Network Layers MCP

**Version:** 1.0.0  
**Status:** Phase 2 MCP Extraction  
**Dependencies:** csscore==1.0.0

## Overview

This MCP provides specialized tools for network layers.

## Installation

```bash
uv pip install mcp-network-layers
```

## Dependencies

- csscore==1.0.0 (core MCP foundation)
- fastmcp>=3.1.0
- pydantic>=2.0

## Development

```bash
cd /home/daen/Projects/ai-marketplace/mcps/network-layers
uv sync
uv run pytest tests/ -v
uv run ruff check src/
uv run mypy src/ --strict
```
