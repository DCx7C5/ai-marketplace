"""canvas-mcp MCP server entrypoint."""

from fastmcp import FastMCP

mcp = FastMCP("canvas-mcp")


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
