"""MCP Server for canvas-mcp."""
import asyncio
from fastmcp import FastMCP

mcp = FastMCP(name="canvas-mcp")

async def main():
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
