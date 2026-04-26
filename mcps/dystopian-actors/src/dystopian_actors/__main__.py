"""
dystopian-actors MCP Server Entry Point

Run with: python -m dystopian_actors
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

mcp = FastMCP(name="dystopian-actors", description="dystopian-actors MCP")


async def main() -> NoReturn:
    """Main entry point for dystopian-actors server."""
    try:
        logger.info("Starting dystopian-actors Server")
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
