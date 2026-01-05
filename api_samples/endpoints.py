import httpx
import json

url = "https://pokeapi.co/api/v2"


def endpoint(endpoint: str, filename: str):
    """
    Fetch an endpoint and save the full response to a file.
    Also prints the top-level keys so you can see the structure.
    """

    response = httpx.get(f"{url}/{endpoint}")
    data = response.json()
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    endpoint("pokemon/pikachu", "raw_pokemon.json")
    endpoint("move/thunderbolt", "raw_move.json")
    endpoint("type/electric", "raw_type.json")
    endpoint("ability/static", "raw_ability.json")
    endpoint("pokemon?limit=5", "raw_list.json")

if __name__ == "__main__":
    main()