"""
It connects to the MCP server and calls the various tools.
"""
import httpx

class MCPClient:
    """
    Calls the MCP server and it gets the list of available tools
    Then, it executes the tools when LLM requests them.
    """
    def __init__(self, mcp_server_url: str = "http://localhost:8000"):
        self.mcp_server_url = mcp_server_url
        self.http_client = httpx.AsyncClient(timeout=20.0)
    
    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()
    
    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """
        Ths function calls a tool on the MCP server. 
        If there is an errror it returns it instead. 
        """
        # JSON-RPC 2.0 protocol
        request = {"jsonrpc": "2.0",
                   "id": 1,
                   "method": "tools/call",
                   "params": {"name": tool_name,
                              "arguments": arguments
                              }
                    }
        response = await self.http_client.post(f"{self.mcp_server_url}/mcp", json=request)
        data = response.json()

        if "error" in data:
            return {"error": data["error"]}
        return data.get("result", {})
    
mcp_client = MCPClient()