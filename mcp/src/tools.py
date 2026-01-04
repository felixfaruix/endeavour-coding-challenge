from mcp.server.fastmcp import FastMCP
from .client import pokeapi_client
from .transformers import (transform_pokemon_info, transform_pokemon_moves,
                           transform_move_info, transform_type_effectiveness,
                           transform_ability_info)

mcp = FastMCP("MCP Server for PokeAPI")

@mcp.tool()
async def get_pokemon(name: str) -> dict:
    """
    It takes as input a Pokemon name and it gets its basic info.
    """
    try:
        raw = await pokeapi_client.get_pokemon_raw(name)
        info = transform_pokemon_info(raw)
        return info.model_dump()
    except ValueError as e:
        return {"error": str(e)}

@mcp.tool()
async def get_pokemon_moves(name: str) -> dict:
    """
    It gets the list of moves a Pokemon can learn and it returns the Pokemon name along with the list of all move names.
    We are separating it from get_pokemon because move lists are quite large.
    """
    try:
        raw = await pokeapi_client.get_pokemon_raw(name)
        moves = transform_pokemon_moves(raw)
        return moves.model_dump()
    except ValueError as e:
        return {"error": str(e)}

@mcp.tool()
async def get_move(name: str) -> dict:
    """
    This tool gets all the info about a specific move.
    """
    try:
        raw = await pokeapi_client.get_move_raw(name)
        info = transform_move_info(raw)
        return info.model_dump()
    except ValueError as e:
        return {"error": str(e)}

@mcp.tool()
async def get_type(name: str) -> dict:
    """
    This tool returns type effectiveness data with all damage relations.
    """
    try:
        raw = await pokeapi_client.get_type_raw(name)
        info = transform_type_effectiveness(raw)
        return info.model_dump()
    except ValueError as e:
        return {"error": str(e)}

@mcp.tool()
async def get_ability(name: str) -> dict:
    """
    This tool returns all the info about a certain ability.
    """
    try:
        raw = await pokeapi_client.get_ability_raw(name)
        info = transform_ability_info(raw)
        return info.model_dump()
    except ValueError as e:
        return {"error": str(e)}

@mcp.tool()
async def list_pokemon(limit: int = 20, offset: int = 0) -> dict:
    """Get a list of Pokemon names."""
    try:
        data = await pokeapi_client.list_pokemon(limit, offset)
        return {"pokemon": [item["name"] for item in data["results"]]}
    except ValueError as e:
        return {"error": str(e)}