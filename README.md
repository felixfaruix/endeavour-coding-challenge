# Pokemon AI Agent with MCP Server

AI-powered Pokemon assistant using Claude AI and MCP protocol.

## Quick Start

### 1. Setup Environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r mcp/requirements.txt
pip install -r agent-api/requirements.txt
```

### 2. Configure

Create `agent-api/.env`:

```
api_key=your-anthropic-key
mcp_server_url=http://localhost:8000
redis_host=localhost
redis_port=6379
redis_password=
```

### 3. Start Redis

```bash
docker run -d -p 6379:6379 --name redis redis
```

### 4. Start Servers

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

### 5. Test

Open http://localhost:8001/docs

```json
{
  "message": "Tell me about Pikachu"
}
```

## Docker Compose (Alternative)

```bash
docker-compose up
```

## API

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

## Tools Available

- `get_pokemon` - Pokemon info
- `get_pokemon_moves` - Move list
- `get_move` - Move details
- `get_type` - Type effectiveness
- `get_ability` - Ability info
- `list_pokemon` - List Pokemon names