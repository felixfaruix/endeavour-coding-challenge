import json
import sys
from pathlib import Path

tests_directory = Path(__file__).parent
file_path = tests_directory.parent
api_samples = file_path .parent / "api_samples"
sys.path.insert(0, str(file_path ))

from src.transformers import transform_move_info

def test():

    json_path = api_samples / "raw_move.json"
    with open(json_path ) as f:
        raw = json.load(f)
    
    result = transform_move_info(raw)

    assert result.name == "thunderbolt"
    assert result.type == "electric"
    assert result.power == 90
    assert result.accuracy == 100

    print("All test passed")

if __name__ == "__main__":
    test()