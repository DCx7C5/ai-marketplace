"""
encoding-analysis MCP Server Entry Point

Run with: python -m encoding_analysis
"""

import asyncio
import logging
import sys
from typing import NoReturn

from fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="encoding-analysis", description="encoding-analysis MCP")


async def main() -> NoReturn:
    """Main entry point for encoding-analysis server."""
    try:
        logger.info("Starting encoding-analysis Server")
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        sys.exit(0)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
