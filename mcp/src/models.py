"""
These models define the clean data we return to the LLM.
The raw PokeAPI responses get transformed into these.
We divide the models per type of information we cn get form the API """

from pydantic import BaseModel

class PokemonBasic(BaseModel):
    """
    The six basic stats every Pokemon has.
    """
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

class PokemonInfo(BaseModel):
    """
    All relevant Pokemon information we can get from a single request.
    """
    name: str
    id: int
    types: list[str]
    abilities: list[str]
    height_meters: float
    weight_kg: float
    stats: PokemonBasic

class PokemonMoveList(BaseModel):
    """
    List of moves a Pokemon can learn.
    """
    pokemon_name: str
    total_moves: int
    moves: list[str]

class Move(BaseModel):
    """
    Information about a specific move.
    """
    name: str
    type: str
    power: int | None
    accuracy: int | None
    pp: int
    damage_class: str
    effect: str

class TypeEffectiveness(BaseModel):
    """
    Type matchup information.
    """
    name: str
    double_damage_to: list[str]
    half_damage_to: list[str]
    no_damage_to: list[str]
    double_damage_from: list[str]
    half_damage_from: list[str]
    no_damage_from: list[str]

class Ability(BaseModel):
    """
    Information about an ability.
    """
    name: str
    effect: str
    pokemon_with_ability: list[str]
