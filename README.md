# Pokemon AI Agent with MCP Server

AI-powered Pokemon assistant using Claude AI and MCP protocol.

## Architecture

```
User → Agent API → Claude AI → MCP Server → PokeAPI
            ↓
          Redis (conversation memory)
```

## Run locally

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

pip install -r mcp/requirements.txt
pip install -r agent-api/requirements.txt
```

### Start Services

Terminal 1:
```bash
cd mcp
uvicorn src.main:app --port 8000
```

Terminal 2:
```bash
cd agent-api
uvicorn src.main:app --port 8001
```

### Test

Open http://localhost:8001/docs

---

## Docker Compose (uses Azure MCP)

### Run

```bash
docker-compose up --build
```

Open http://localhost:8001/docs

---

## API Usage

**New conversation:**
```json
POST /pokemon_request
{"message": "Tell me about Pikachu"}
```

**Continue conversation:**
```json
POST /pokemon_request
{"message": "What are its weaknesses?", "conversation_id": "from-previous-response"}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_pokemon` | Pokemon info (types, stats, abilities) |
| `get_pokemon_moves` | List of moves a Pokemon can learn |
| `get_move` | Move details (power, accuracy, type) |
| `get_type` | Type effectiveness |
| `get_ability` | Ability description |
| `list_pokemon` | List Pokemon names |
