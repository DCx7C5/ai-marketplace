"""MCP Server for web-search-mcp."""
import asyncio
from fastmcp import FastMCP

mcp = FastMCP(name="web-search-mcp")

async def main():
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
