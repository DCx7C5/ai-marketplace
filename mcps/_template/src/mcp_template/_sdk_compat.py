"""SDK/Stdio compatibility layer for FastMCP template.

This module provides a unified interface for running the FastMCP server in both:
  - SDK mode: In-process operation where the server is instantiated and used directly
  - Stdio mode: Out-of-process JSON-RPC communication over stdin/stdout

The module handles:
  - Automatic mode detection via MCP_SDK_MODE environment variable
  - FastMCP server initialization with tool registration
  - Async event loop management
  - Proper error handling and logging
"""

import asyncio
import logging
import os
import sys
from typing import Optional

from fastmcp import FastMCP

# Module-level logger
logger = logging.getLogger(__name__)

# Global FastMCP server instance (SDK mode)
_mcp_server: Optional[FastMCP] = None


async def initialize_mcp() -> FastMCP:
    """Initialize and configure the FastMCP server instance.

    This function creates a new FastMCP server with the standard configuration,
    loads all tool definitions from the tools module, and registers them with
    the server. It uses a module-level cache to ensure only one server instance
    is created.

    Returns:
        FastMCP: The initialized FastMCP server instance.

    Raises:
        ImportError: If the tools module cannot be imported or tools registration fails.
        RuntimeError: If server initialization encounters an error.

    Example:
        >>> server = await initialize_mcp()
        >>> isinstance(server, FastMCP)
        True
    """
    global _mcp_server

    if _mcp_server is not None:
        return _mcp_server

    try:
        logger.debug("Initializing FastMCP server instance")

        # Create FastMCP server with standard configuration
        _mcp_server = FastMCP(
            name="mcp-template",
            instructions="MCP template for CyberSecSuite",
        )

        logger.debug("FastMCP instance created: %s", _mcp_server.name)

        # Import tools module to trigger tool registration via @mcp.tool() decorators
        # This must happen after the server is created so decorators can register with it
        try:
            from . import tools as _  # noqa: F401
            logger.debug("Tools module imported and registered")
        except ImportError as e:
            logger.error("Failed to import tools module: %s", e)
            raise ImportError(f"Could not import tools module: {e}") from e

        logger.info("FastMCP server initialized successfully")
        return _mcp_server

    except Exception as e:
        logger.error("Error during FastMCP initialization: %s", e)
        raise RuntimeError(f"Failed to initialize FastMCP server: {e}") from e


async def run_stdio_mode() -> None:
    """Run the FastMCP server in Stdio mode.

    In Stdio mode, the server communicates with a parent process via JSON-RPC
    protocol over stdin/stdout. This is the standard mode for MCP servers when
    invoked as a subprocess by an MCP client.

    The function:
    1. Initializes the FastMCP server
    2. Starts the JSON-RPC server on stdin/stdout
    3. Runs until the connection is closed or an error occurs

    Raises:
        RuntimeError: If server initialization or startup fails.
        EOFError: If stdin is closed unexpectedly.

    Note:
        This function is typically called from __main__.py and runs in the main
        asyncio event loop. It will block until the server shuts down.

    Example:
        >>> await run_stdio_mode()  # Runs until parent closes connection
    """
    logger.debug("Starting FastMCP in Stdio mode")

    try:
        # Initialize server (loads tools and configuration)
        server = await initialize_mcp()

        logger.info("Starting Stdio JSON-RPC server on stdin/stdout")

        # Run the server in stdio mode using the async stdio transport
        # The server reads JSON-RPC requests from stdin
        # and writes JSON-RPC responses to stdout
        await server.run_stdio_async(show_banner=False, stateless=False)

    except EOFError:
        logger.warning("Stdio connection closed by client")
        raise
    except KeyboardInterrupt:
        logger.info("Stdio mode interrupted by user")
        raise
    except Exception as e:
        logger.error("Error in Stdio mode: %s", e)
        raise RuntimeError(f"Stdio server error: {e}") from e


def get_mcp_server() -> FastMCP:
    """Get the FastMCP server instance (SDK mode).

    This function returns the module-level FastMCP server instance for use in
    SDK mode operations. The server must have been initialized via initialize_mcp()
    before calling this function.

    This is intended for use in SDK mode where the server is managed as a
    library component rather than as a subprocess.

    Returns:
        FastMCP: The module-level FastMCP server instance.

    Raises:
        RuntimeError: If the server has not been initialized via initialize_mcp().

    Example:
        >>> server = get_mcp_server()  # Raises RuntimeError if not initialized
        Traceback (most recent call last):
            ...
        RuntimeError: FastMCP not initialized. Call initialize_mcp() first.
    """
    if _mcp_server is None:
        error_msg = "FastMCP not initialized. Call initialize_mcp() first."
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    return _mcp_server


async def main() -> None:
    """Main entry point for the MCP server.

    This function serves as the primary entry point when the module is run
    directly (e.g., `python -m mcp_template`). It detects the execution mode
    via the MCP_SDK_MODE environment variable and dispatches to the appropriate
    handler.

    Execution modes:
      - sdk: Initialize server for in-process use and exit (SDK mode)
      - stdio (default): Run server listening on stdin/stdout (JSON-RPC mode)

    Environment Variables:
        MCP_SDK_MODE: Set to "sdk" for SDK mode, any other value (or unset)
                      defaults to stdio mode.

    Raises:
        RuntimeError: If server initialization fails in either mode.
        KeyboardInterrupt: If interrupted by user signal.

    Example:
        >>> # Stdio mode (default)
        >>> await main()  # Runs JSON-RPC server

        >>> # SDK mode
        >>> os.environ["MCP_SDK_MODE"] = "sdk"
        >>> await main()  # Initializes and returns
    """
    # Detect execution mode from environment variable
    mode: str = os.environ.get("MCP_SDK_MODE", "stdio").lower()

    logger.info("MCP template server starting in %s mode", mode)

    if mode == "sdk":
        # SDK mode: Initialize server for in-process use
        logger.info("Initializing in SDK mode (in-process)")
        await initialize_mcp()
        logger.info("FastMCP server initialized and ready for SDK use")
        # In SDK mode, the server is now available via get_mcp_server()
        # The caller is responsible for managing the server lifecycle

    else:
        # Stdio mode (default): Run server listening on stdin/stdout
        logger.info("Initializing in Stdio mode (JSON-RPC)")
        await run_stdio_mode()


if __name__ == "__main__":
    # Configure logging when module is run directly
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr,  # Log to stderr to avoid interfering with JSON-RPC on stdout
    )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception:
        logger.exception("Unhandled exception in main")
        sys.exit(1)
