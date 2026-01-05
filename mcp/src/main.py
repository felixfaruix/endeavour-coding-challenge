"""
Main entry point for the server.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from .client import pokeapi_client
from .tools import mcp

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    It manages the application lifecycle    
    """
    print("Server starting")
    async with mcp.session_manager.run():
        yield
    print("Server stopping")
    await pokeapi_client.stop()

app = FastAPI(title="MCP Server for PokeAPI", description="MCP server providing Pokemon data from PokeAPI",
              version="1.0.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "MCP Server running", "mcp_endpoint": "/mcp"}

app.mount("", mcp.streamable_http_app())