"""
Transformers keeps extraction logic separate from HTTP logic and
each transformer takes raw PokeAPI data and etracts relevant fields into a clean Pydantic model.
"""

from .models import (PokemonInfo, PokemonBasic, PokemonMoveList,
                    Move, TypeEffectiveness, Ability)

def transform_pokemon_info(raw: dict) -> PokemonInfo:
    """
    It transforms raw pokemon info into a PokemonInfo model.
    """

    types = [t["type"]["name"] for t in raw["types"]]
    abilities = [a["ability"]["name"] for a in raw["abilities"]]
    stats_dict = {stat["stat"]["name"]: stat["base_stat"] for stat in raw["stats"]}
    
    stats = PokemonBasic(hp=stats_dict["hp"], attack=stats_dict["attack"],
                         defense=stats_dict["defense"],
                         special_attack=stats_dict["special-attack"],
                         special_defense=stats_dict["special-defense"],
                         speed=stats_dict["speed"])

    return PokemonInfo(name=raw["name"], id=raw["id"], types=types, abilities=abilities,
                       height_meters=raw["height"] / 10, weight_kg=raw["weight"] / 10, stats=stats)

def transform_pokemon_moves(raw: dict) -> PokemonMoveList:
    """
    It transforms the info of a pokemon to PokemonMoveList, collecting only the moves.
    Also, it cuts out different versions of the moves.
    """
    moves = [m["move"]["name"] for m in raw["moves"]]
    return PokemonMoveList(pokemon_name=raw["name"], total_moves=len(moves),moves=moves) 

def transform_move_info(raw: dict) -> Move:
    """
    It transforms info of a move into a Move object.
    """
    effect = "No description available."
    for entry in raw.get("effect_entries", []):
        if entry["language"]["name"] == "en":
            effect = entry.get("effect", effect)  # We are using only the full effect 
            break
    
    return Move(name=raw["name"], type=raw["type"]["name"], power=raw["power"],
                accuracy=raw["accuracy"], pp=raw["pp"],damage_class=raw["damage_class"]["name"], effect=effect)

def transform_type_effectiveness(raw: dict) -> TypeEffectiveness:
    """
    It takes all the damage relations and trasnforms the response into a TypeEffectivness object.
    """
    relations = raw["damage_relations"]
    return TypeEffectiveness(name=raw["name"],
                             double_damage_to=[t["name"] for t in relations["double_damage_to"]],
                             half_damage_to=[t["name"] for t in relations["half_damage_to"]], no_damage_to=[t["name"] for t in relations["no_damage_to"]],
                             double_damage_from=[t["name"] for t in relations["double_damage_from"]],
                             half_damage_from=[t["name"] for t in relations["half_damage_from"]],
                             no_damage_from=[t["name"] for t in relations["no_damage_from"]])

def transform_ability_info(raw: dict) -> Ability:
    """
    It takes an ability response from the endpoint and 
    gives out an Ability object with its name, the effect descriptions and a list of Pokemon that have it.
    """

    effect = "No description available."
    for entry in raw.get("effect_entries", []):
        if entry["language"]["name"] == "en":
            effect = entry.get("effect", effect) # We are skipping the short effect
            break

    pokemon_list = [pokemon["pokemon"]["name"] for pokemon in raw.get("pokemon", [])[:10]]
    return Ability(name=raw["name"], effect=effect, pokemon_with_ability=pokemon_list)