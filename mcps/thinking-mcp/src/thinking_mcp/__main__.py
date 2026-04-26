"""MCP Server for thinking-mcp."""
import asyncio
from fastmcp import FastMCP

mcp = FastMCP(name="thinking-mcp")

async def main():
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
