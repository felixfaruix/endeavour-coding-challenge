"""
It connects to the MCP server and calls the various tools.
"""
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

class MCPClient:
    """
    Calls the MCP server and it gets the list of available tools
    Then, it executes the tools when LLM requests them.
    """

    def __init__(self):
        self.mcp_server_url = os.getenv("mcp_server_url", "http://localhost:8000")
        print(f"MCP loading url: {self.mcp_server_url}")
        self.http_client = httpx.AsyncClient(timeout=20.0)
        self.session_id = None
    
    async def close(self):
        """
        it closes the HTTP client.
        """
        await self.http_client.aclose()
    
    async def _ensure_session(self):
        """
        Initialize session if not exists
        """
        if self.session_id:
            return
        
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-01-01",
                "capabilities": {},
                "clientInfo": {"name": "pokemon-agent", "version": "1.0.0"}
            }
        }
        
        headers = {"Accept": "application/json, text/event-stream"}
        response = await self.http_client.post(f"{self.mcp_server_url}/mcp", json=init_request, headers=headers)
        
        self.session_id = response.headers.get("mcp-session-id")
        print(f"MCP Session Id: {self.session_id}")

        if not self.session_id:
            print(f"Session init failed. Status: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            raise Exception("Failed to initialize MCP session")
    
    async def call_tool(self, tool_name: str, arguments: dict) -> dict: # type: ignore
        """
        Ths function calls a tool on the MCP server. 
        If there is an errror it returns it instead. 
        """
        await self._ensure_session()

        request = {"jsonrpc": "2.0",
                   "id": 1,
                   "method": "tools/call",
                   "params": {"name": tool_name,
                              "arguments": arguments
                              }
                    }
        headers = {
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": self.session_id
        }
        
        response = await self.http_client.post(f"{self.mcp_server_url}/mcp", json=request, headers=headers)
        import json
        text = response.text

        for line in text.split("\n"):
            if line.startswith("data: "):
                data = json.loads(line[6:])
                if "error" in data:
                    return {"error": data["error"]}

                result = data.get("result", {})
                if "content" in result and len(result["content"]) > 0:
                    content = result["content"][0]
                    if content.get("type") == "text":
                        return json.loads(content["text"])
                return result
    
        return {"error": "No valid response"}
    
mcp_client = MCPClient()