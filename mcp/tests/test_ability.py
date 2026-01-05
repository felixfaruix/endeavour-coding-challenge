import json
from pathlib import Path
import sys

tests_directory = Path(__file__).parent
file_path = tests_directory.parent
api_samples = file_path .parent / "api_samples"
sys.path.insert(0, str(file_path ))

from src.transformers import transform_ability_info

def test():
    json_path = api_samples / "raw_ability.json"
    with open(json_path) as f:
        raw = json.load(f)
    
    result = transform_ability_info(raw)

    assert result.name == "static"
    assert len(result.effect) > 0
    assert len(result.pokemon_with_ability) <= 10

    print("All test passed")

if __name__ == "__main__":
    test()
