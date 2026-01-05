from .agent import Agent
from .mcp_client import mcp_client
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    await mcp_client.close()

app = FastAPI(title="Pokemon AIAgent API", lifespan=lifespan)
api_key = os.getenv("api_key")

if not api_key:
    raise ValueError("Key not valid")

agent = Agent(api_key=api_key)

@app.get("/")
async def root():
    return {"status": "Agent running"}

@app.post("/pokemon_request")
async def pokemon_request(request: dict):
    """
    It sends a message to the LLM.
    """
    try: 
        conversation_id = request.get("conversation_id") or str(uuid.uuid4())
        response = await agent.process_query(conversation_id, request["message"])
            
        return {
            "response": response,
            "conversation_id": conversation_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
