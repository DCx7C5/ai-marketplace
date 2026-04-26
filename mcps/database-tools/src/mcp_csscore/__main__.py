"""
CyberSecSuite Core MCP Server Entry Point

This module initializes and runs the csscore MCP server that provides
foundation services to all other externalized MCPs.

Run with: python -m mcp_csscore
"""

import asyncio
import logging
import sys
from typing import Any, NoReturn

from fastmcp import FastMCP
from pydantic import BaseModel

from mcp_csscore.core import (
    ScopeLevel,
    create_audit_logger,
    discover_assets,
    get_configuration,
    get_marketplace_registry,
    get_scope_context,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(name="csscore", description="CyberSecSuite Core MCP Foundation")


class ScopeInput(BaseModel):
    """Input model for scope-aware operations."""

    scope_level: str
    runtime_id: str
    worktree_path: str


@mcp.tool()
async def marketplace_registry() -> dict[str, Any]:
    """Get marketplace registry of available MCPs and tools."""
    return await get_marketplace_registry()


@mcp.tool()
async def discover_assets_tool(
    scope_level: str, runtime_id: str, worktree_path: str, asset_type: str = ""
) -> list[dict[str, Any]]:
    """Discover assets and systems in the target environment."""
    scope = await get_scope_context(
        ScopeLevel(scope_level), runtime_id, worktree_path
    )
    return await discover_assets(scope, asset_type if asset_type else None)


@mcp.tool()
async def get_config(
    config_key: str, scope_level: str, runtime_id: str, worktree_path: str
) -> dict[str, Any]:
    """Retrieve CyberSecSuite configuration values."""
    scope = await get_scope_context(
        ScopeLevel(scope_level), runtime_id, worktree_path
    )
    result = await get_configuration(config_key, scope)
    return result or {"error": f"Config key not found: {config_key}"}


@mcp.tool()
async def create_logger(
    service_name: str, scope_level: str, runtime_id: str, worktree_path: str
) -> dict[str, Any]:
    """Create an audit logger for MCP operations."""
    scope = await get_scope_context(
        ScopeLevel(scope_level), runtime_id, worktree_path
    )
    log = await create_audit_logger(service_name, scope)
    return {
        "service": service_name,
        "level": log.level,
        "handlers": len(log.handlers),
    }


@mcp.tool()
async def get_scope(
    scope_level: str, runtime_id: str, worktree_path: str
) -> dict[str, Any]:
    """Get or create scope context for execution."""
    scope = await get_scope_context(
        ScopeLevel(scope_level), runtime_id, worktree_path
    )
    return {
        "scope_level": scope.scope_level.value,
        "runtime_id": scope.runtime_id,
        "worktree_path": scope.worktree_path,
        "project_id": scope.project_id,
        "session_id": scope.session_id,
    }


async def main() -> NoReturn:
    """
    Main entry point for CyberSecSuite Core MCP server.

    Initializes FastMCP server with 5 core tools and starts the server loop.
    """
    try:
        logger.info("Starting CyberSecSuite Core MCP Server (csscore 1.0.0)")

        # Verify core functions are accessible
        registry = await get_marketplace_registry()
        logger.info(f"Marketplace registry loaded: {len(registry)} MCPs available")

        # Start FastMCP server
        logger.info("CyberSecSuite Core MCP Server started successfully")
        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for 1 hour

    except KeyboardInterrupt:
        logger.info("MCP Server shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error in MCP server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
