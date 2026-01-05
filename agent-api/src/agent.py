import json
from anthropic import AsyncAnthropic
from .mcp_client import mcp_client
from .tools_schemas import tools_schemas
from .memory import memory


class Agent:
    """
    It takes  the user messages and sends it to Claude with the available tools.
    It then executes tool calls via MCP server and teturns the final response.
    """
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
    
    async def process_query(self, conversation_id: str, user_message: str) -> str:
        """
        It returns the assistant's text response.
        """
        messages = memory.get_messages(conversation_id)
        messages.append({"role": "user", "content": user_message})

        while True:
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system="You are a Pokemon assistant fetching information from 4 different endpoints, which narrow the " \
                "data you have available. You need to remind the user about it, if it asks different stuff." \
                "The following endpoints are: " \
                "- pokemon/{name} - Pokemon data" \
                "- move/{name} - moves data" \
                "- type/{name} - type effectiveness data" \
                "- ability/{name} - ability descriptions data" \
                "- pokemon - list of all Pokemons. " \
                "Do not answer questions unrelated to Pokemon. " \
                "Reply to the user briefly with only the information required. Nothing else.",
                tools=tools_schemas,
                messages=messages)
            
            if response.content[0].type == "text" and len(response.content) == 1:
                assistant_text = response.content[0].text
                assistant_message = {
                    "role": "assistant",
                    "content": assistant_text
                }
                memory.save_messages(conversation_id, messages)
                return assistant_text
            
            assistant_message = {
                "role": "assistant",
                "content": response.to_dict()["content"]
            }
            messages.append(assistant_message)
            
            for content in response.content:
                if content.type == "tool_use":
                    tool_name = content.name
                    tool_args = content.input
                    tool_use_id = content.id
                    
                    print(f"Calling tool: {tool_name} with args: {tool_args}")
                    
                    # Calling the MCP server
                    result = await mcp_client.call_tool(tool_name, tool_args)

                    print(f"Tool {tool_name} result: {result}")
                    
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(result)
                        }]
                    })
            memory.save_messages(conversation_id, messages)
