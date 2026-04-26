"""MCP Server for memory-mcp."""
import asyncio
from fastmcp import FastMCP

mcp = FastMCP(name="memory-mcp")

async def main():
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
