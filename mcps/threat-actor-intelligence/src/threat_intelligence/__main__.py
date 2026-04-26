"""
threat-intelligence MCP Server Entry Point

Run with: python -m threat_intelligence
"""

import asyncio
import logging
import sys
from typing import Any, Dict, NoReturn

from fastmcp import FastMCP
from mcp_csscore import get_scope_context, ScopeLevel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="threat-intelligence", description="threat-intelligence MCP with 14 tools")


async def main() -> NoReturn:
    """Main entry point for threat-intelligence server."""
    try:
        logger.info("Starting threat-intelligence Server")
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
