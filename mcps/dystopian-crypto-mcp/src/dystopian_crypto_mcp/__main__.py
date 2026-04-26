"""
dystopian-crypto-mcp MCP Server

Run with: python -m dystopian_crypto_mcp
"""

import asyncio
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="dystopian-crypto-mcp", description="dystopian-crypto-mcp - Real implementations")

async def main():
    """Main entry point."""
    logger.info(f"Starting {mcp.name} server")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown")
