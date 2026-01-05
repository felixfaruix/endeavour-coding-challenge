from anthropic.types import ToolParam

tools_schemas: list[ToolParam] = [
    {
        "name": "get_pokemon",
        "description": "Get basic info about a Pokemon including types, stats, height, weight.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Pokemon name, e.g. 'pikachu', 'charizard'"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "get_pokemon_moves",
        "description": "Get the list of moves a Pokemon can learn.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Pokemon name"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "get_move",
        "description": "Get details about a specific move including power, accuracy, type.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Move name, e.g. 'thunderbolt', 'fire-blast'"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "get_type",
        "description": "Get type effectiveness - what a type is strong/weak against.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Type name, e.g. 'electric', 'fire', 'water'"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "get_ability",
        "description": "Get information about a Pokemon ability.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Ability name, e.g. 'static', 'levitate'"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "list_pokemon",
        "description": "Get a list of Pokemon names.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "How many Pokemon to return (default 20)"
                }
            },
            "required": []
        }
    }
]