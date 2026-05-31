from app.logger import log_event
from pydantic import BaseModel
from anthropic import AsyncAnthropic
from typing import Any

anthropic_client = AsyncAnthropic()

class PlannerDecision(BaseModel):
  action:str
  tool_name:str | None = None
  tool_arguments:dict | None = None
  final_response:str | None = None
  tool_uses: list[Any] = []
  input_tokens:int = 0
  output_tokens:int = 0

TOOLS = [
  {
    "name": "get_incident",
    "description": "Get incident detail including case_id,priority,reporter,issue_type,short_description,customer_satisfaction for a specific case_id.",
    "input_schema": {
      "type":"object",
      "properties": {
        "case_id": {
          "type":"string",
          "description": "The case_id of specific Incident we want to investigate"
        }
      },
      "required":["case_id"]
    }
  },
  {
    "name": "get_incident_duration",
    "description": "Get incident duration, opened_at timestamp, closed_at timestamp and total duration.",
    "input_schema":{
      "type":"object",
      "properties": {
        "case_id":{
          "type":"string",
          "description": "The case_id of specific Incident we want to investigate"
        }
      },
      "required":["case_id"]
    }
  },
  {
    "name": "get_incident_timeline",
    "description": "Get chronological timeline of a Incidents which include event timestamp,resolver(Person who resolved the Incident) and event_type",
    "input_schema":{
      "type":"object",
      "properties": {
        "case_id":{
          "type":"string"
        },
      },
      "required":["case_id"]
    }
  }
]


async def decide_tool(messages:list):
  llm_response = await anthropic_client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    system="You are a helpful AI assistant. You job is to ONLY use the tool at your disposal. Pleae make sure to not use anyother external or hallucinate anyother requirements. If you don't find anything using the GIVEN tools just reply 'I wasn't able to find anything using the provided tools'",
    tools=TOOLS,
    messages=messages
  )
  llm_content = llm_response.content

  print("\n\n LLM RESPONSE \n\n", llm_response)
  
  tool_use = None
  tool_uses = []
  for block in llm_content:
    if block.type == 'tool_use':
      tool_use = block
      tool_uses.append(block)
      # break
  print("\n\ntool_uses\n\n", tool_uses)
  tool_names=[]
  for tool in tool_uses:
    tool_info = {
      "name": tool.name,
      "input": tool.input
    }
    tool_names.append(tool_info)

  print("\n\TOOL NAMES\n\n", tool_names)


  if tool_uses:
    return PlannerDecision(
      action="tool",
      # tool_name=tool_use.name,
      # tool_arguments=tool_use.input,
      tool_uses=tool_uses,
      input_tokens=llm_response.usage.input_tokens,
      output_tokens=llm_response.usage.output_tokens
    )
  else:
    text_response = llm_content[0].text
    return PlannerDecision(
      action="final",
      final_response=text_response,
      input_tokens=llm_response.usage.input_tokens,
      output_tokens=llm_response.usage.output_tokens
    )
