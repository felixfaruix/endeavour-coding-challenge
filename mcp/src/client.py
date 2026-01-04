"""
HTTP client for PokeAPI with connection pooling, multiple endpoint support and caching
(although the API uses HTTP auto-catching). 

Each endpoint type has its own cache for raw responses (get_pokemon, and get_pokemon_moves tools share the same cache).
We are also keeping track of when something was added to the cache in order to delete the oldest when/if it's full (arbibrary)

List of endpoints handled: 
    - pokemon/{name} - Pokemon data
    - move/{name} - moves data
    - type/{name} - type effectiveness data
    - ability/{name} - ability descriptions data
    - pokemon - list of all Pokemons
"""

from datetime import datetime
import httpx

class CacheEntry:
    """
    This is the cache entry with metadata for validation and stores 
    the actual API response and when it was fetched (to remove the oldest)
    """
    def __init__(self, data: dict):
        self.data = data
        self.fetched_at = datetime.now()

class PokeAPIClient:
    """
    HTTP client for PokeAPI. 
    """
    api_base = "https://pokeapi.co/api/v2"
    cache_max = 200

    def __init__(self):

        self.http_client = httpx.AsyncClient(base_url="https://pokeapi.co/api/v2", timeout=30.0)
        self.pokemon_cache: dict[str, CacheEntry] = {}
        self.move_cache: dict[str, CacheEntry] = {}
        self.type_cache: dict[str, CacheEntry] = {}
        self.ability_cache: dict[str, CacheEntry] = {}

    async def stop(self) -> None:
        """
        This function closes the HTTP client and clears the caches after.
        """
        await self.http_client.aclose()
        self._clear_all_caches()
    
    def _clear_all_caches(self) -> None:
        """
        Clearing all cachec for the new session to start.
        """
        self.pokemon_cache = {}
        self.move_cache = {}
        self.type_cache = {}
        self.ability_cache = {}

    def _add_to_cache(self, cache: dict[str, CacheEntry], key: str, data: dict) -> None:
        """
        Adding new information to cache and replacing if full.
        """
        # Removing oldest entries if cache is full
        if len(cache) >= self.cache_max:
            sorted_keys = sorted(cache.keys(), key=lambda k: cache[k].fetched_at)
            # We are removing the 20 percent of the cache if it reaching its max
            remove_count = max(1, len(sorted_keys) // 20)
            for k in sorted_keys[:remove_count]:
                del cache[k]
        cache[key] = CacheEntry(data)

    async def _fetch(self, endpoint: str, resource_type: str, name: str) -> dict:
        """
        This is a generic fetch method for any PokeAPI endpoint.
        It returns a raw JSON response as a dictionary.
        """
        url = f"{self.api_base}/{endpoint}"
        response = await self.http_client.get(url)
        
        if response.status_code == 404:
            raise ValueError(f"{resource_type} '{name}' not found")
        if response.status_code != 200:
            raise ValueError(f"PokeAPI error: {response.status_code}")

        return response.json()

    async def get_pokemon_raw(self, name: str) -> dict:
        """
        This function gets raw Pokemon data from /pokemon/{name}.
    
        This is a large response containing all info about a single pokemon.
        Then, it caches the response for future requests.
        """
        key: str = name.lower().strip()
        # Checking the cache for previous data first
        if key in self.pokemon_cache:
            return self.pokemon_cache[key].data
        # If missed then we fetch the data directly from API
        data = await self._fetch(f"pokemon/{key}", "Pokemon", key)
        self._add_to_cache(self.pokemon_cache, key, data)
        return data

    async def get_move_raw(self, name: str) -> dict:
        """
        This function gets raw move data from /move/{name}.
        It contains: power, accuracy, type, PP, damage class, effect description.
        """
        key = name.lower().strip().replace(" ", "-")

        if key in self.move_cache:
            return self.move_cache[key].data
        
        data = await self._fetch(f"move/{key}", "Move", key)
        self._add_to_cache(self.move_cache, key, data)
        return data

    async def get_type_raw(self, name: str) -> dict:
        """
        This function gets raw type data from /type/{name}.
        It contains: damage relations (what this type is strong/weak against).
        """
        key = name.lower().strip()

        if key in self.type_cache:
            return self.type_cache[key].data
        
        data = await self._fetch(f"type/{key}", "Type", key)
        self._add_to_cache(self.type_cache, key, data)
        return data

    async def get_ability_raw(self, name: str) -> dict:
        """
        This function gets raw ability data from /ability/{name}.
        It contains: effect description, which Pokemon have this ability.
        """
        key = name.lower().strip().replace(" ", "-")

        if key in self.ability_cache:
            return self.ability_cache[key].data
        
        data = await self._fetch(f"ability/{key}", "Ability", key)
        self._add_to_cache(self.ability_cache, key, data)
        return data

    async def list_pokemon(self, limit: int = 20, offset: int = 0) -> dict:
        """
        This function gets a list of Pokemon names from /pokemon.
        We are not caching it since it's just a list of names/URLs.
        We are also limiting the items displayed since the list seems pretty long.
        """
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        
        url = f"{self.api_base}/pokemon"
        params = {"limit": limit, "offset": offset}
        response = await self.http_client.get(url, params=params)

        if response.status_code != 200:
            raise ValueError(f"PokeAPI error: {response.status_code}")
        return response.json()

pokeapi_client = PokeAPIClient()