import json
import sys
from pathlib import Path

tests_directory = Path(__file__).parent
file_path = tests_directory.parent
api_samples = file_path .parent / "api_samples"
sys.path.insert(0, str(file_path ))

from src.transformers import transform_pokemon_info

def test():

    json_path = api_samples / "raw_pokemon.json"
    with open(json_path) as f:
        raw = json.load(f)

    result = transform_pokemon_info(raw)

    assert result.name == "pikachu", f"Expected pikachu, got {result.name}"
    assert result.id == 25, f"Expected 25, got {result.id}"
    assert "electric" in result.types, f"Expected electric in types"
    assert result.stats.hp == 35, f"Expected HP 35, got {result.stats.hp}"

    print("All test passed")

if __name__ == "__main__":
    test()