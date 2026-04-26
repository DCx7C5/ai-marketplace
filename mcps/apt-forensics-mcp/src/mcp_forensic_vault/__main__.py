"""
Forensic Vault MCP Server Entry Point

Run with: python -m mcp_forensic_vault
"""

import asyncio
import logging
import sys
from typing import Any, NoReturn

from fastmcp import FastMCP

from mcp_csscore import ScopeLevel, get_scope_context

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP(name="forensic-vault", description="Forensic investigation tools for APT analysis, IOC extraction, and case management")


@mcp.tool()
async def placeholder_tool() -> dict[str, Any]:
    """Placeholder tool for forensic-vault."""
    scope = await get_scope_context(ScopeLevel.RUNTIME, "runtime-001", "/tmp")
    return {"status": "ok", "scope": scope.scope_level.value}


async def main() -> NoReturn:
    """Main entry point for Forensic Vault MCP server."""
    try:
        logger.info("Starting Forensic Vault MCP Server")
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
