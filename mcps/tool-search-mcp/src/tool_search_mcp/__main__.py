"""MCP Server for tool-search-mcp."""
import asyncio
from fastmcp import FastMCP

mcp = FastMCP(name="tool-search-mcp")

async def main():
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
