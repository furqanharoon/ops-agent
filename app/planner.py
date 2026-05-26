from app.logger import log_event
from anthropic import Anthropic

anthropic_client = Anthropic()

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

def decide_tool(query:str):
  query = query.lower()
  llm_response = anthropic_client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    system="You are a helpful AI assistant. You job is to ONLY use the tool at your disposal. Pleae make sure to not use anyother external or hallucinate anyother requirements. If you don't find anything using the GIVEN tools just reply 'I wasn't able to find anything using the provided tools'",
    tools=TOOLS,
    messages=[
      {
        "role": "user",
        "content": query
      }
    ]
  )
  llm_content = llm_response.content

  print("\n\n LLM CONTENT \n\n", llm_content)
  
  tool_use = None

  for block in llm_content:
    if block.type == 'tool_use':
      tool_use = block
      break


  # for block in llm


  # if "cpu" in query:
  #   decision = {
  #     "tool": "get_cpu_usage",
  #     "arguments": {
  #       "server_name": "web-1"
  #     }
  #   }
  #   log_event("planner_decision", decision)
  #   return decision
  # if "restart" in query:
  #   decision = {
  #     "tool_name": "restart_service",
  #     "arguments": {
  #       "service_name": "nginx"
  #     }
  #   }
  #   log_event("planner_decision", decision)
  #   return decision
  # return None
