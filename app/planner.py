from app.logger import log_event
from anthropic import AsyncAnthropic

anthropic_client = AsyncAnthropic()

TOOLS=[
  {
    "name":"get_cpu_usage",
    "description": "Get CPU Usage for a server",
    "input_schema": {
      "type": "object",
      "properties": {
        "server_name": {
          "type": "string"
        }
      },
      "required": ["server_name"]
    }
  },
  {
    "name": "restart_service",
    "description": "Restart the given AWS service",
    "input_schema": {
      "type": "object",
      "properties": {
        "service_name": {
          "type":"string"
        }
      },
      "required": ["service_name"]
    }
  }
]

async def decide_tool(messages:list):
  llm_response = await anthropic_client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    system="You are a helpful AI assistant. You job is to ONLY use the tool at your disposal. Pleae make sure to not use anyother external or hallucinate anyother requirements. If you don't find anything using the GIVEN tools just reply 'I wasn't able to find anything using the provided tools'",
    tools=TOOLS,
    messages=messages
  )
  llm_content = llm_response.content

  print("\n\n LLM CONTENT \n\n", llm_content)
  
  tool_use = None

  for block in llm_content:
    if block.type == 'tool_use':
      tool_use = block
      break
  return tool_use
