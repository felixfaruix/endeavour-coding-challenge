import json
import sys
from pathlib import Path

tests_directory = Path(__file__).parent
file_path = tests_directory.parent
api_samples = file_path .parent / "api_samples"
sys.path.insert(0, str(file_path ))

from src.transformers import transform_pokemon_moves 

def test():
    json_path = api_samples / "raw_pokemon.json"
    with open(json_path ) as f:
        raw = json.load(f)
    
    result = transform_pokemon_moves(raw)

    assert result.pokemon_name == "pikachu"
    assert result.total_moves > 50  # Pikachu has many moves
    assert len(result.moves) == result.total_moves

    print("All test passed")

if __name__ == "__main__":
    test()