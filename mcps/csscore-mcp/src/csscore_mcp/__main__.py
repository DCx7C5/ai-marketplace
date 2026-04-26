"""MCP Server for csscore-mcp."""
import asyncio
from fastmcp import FastMCP

mcp = FastMCP(name="csscore-mcp")

async def main():
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
