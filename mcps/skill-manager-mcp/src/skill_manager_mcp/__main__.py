"""MCP Server for skill-manager-mcp."""
import asyncio
from fastmcp import FastMCP

mcp = FastMCP(name="skill-manager-mcp")

async def main():
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
