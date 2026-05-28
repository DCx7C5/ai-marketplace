"""Entrypoint for ollama-local-mcp."""

from __future__ import annotations

import asyncio
import logging
import sys

from .server import run


def main() -> None:
    """Run MCP server process."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr,
    )
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
