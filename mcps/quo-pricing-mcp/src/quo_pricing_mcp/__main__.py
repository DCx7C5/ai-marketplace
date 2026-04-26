"""MCP Server for quo-pricing-mcp."""
import asyncio
from fastmcp import FastMCP

mcp = FastMCP(name="quo-pricing-mcp")

async def main():
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
