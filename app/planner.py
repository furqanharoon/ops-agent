from app.logger import log_event
from app.utils.pretty_print import print_llm_response
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
  thought:str = ""

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
  system_prompt = f"""
    You are a AI investigative agent.
    You may call ONE tool per response.
    Never request multiple tools at ONCE.
    Before choosing another TOOL, review the observations already gathered.
    After receiving an observation, decide the single next best tool.
    Do not CALL a tool if its result already exist in the observation.
    If you have enough information to answer the user's question, do not CALL any further tool and provide the final answer.
  """
  llm_response = await anthropic_client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    system=system_prompt,
    tools=TOOLS,
    messages=messages
  )
  llm_content = llm_response.content
  print_llm_response(llm_response)
  tool_use = None
  tool_uses = []
  thought = ""
  for block in llm_content:
    if block.type == 'text':
      thought+=block.text
    if block.type == 'tool_use':
      tool_use = block
      tool_uses.append(block)

  tool_names=[]
  for tool in tool_uses:
    tool_info = {
      "name": tool.name,
      "input": tool.input
    }
    tool_names.append(tool_info)

  if tool_uses:
    single_tool = tool_uses[0]
    return PlannerDecision(
      action="tool",
      thought=thought,
      tool_uses=[single_tool],
      input_tokens=llm_response.usage.input_tokens,
      output_tokens=llm_response.usage.output_tokens
    )
  else:
    text_response = llm_content[0].text
    return PlannerDecision(
      action="final",
      thought=thought,
      final_response=text_response,
      input_tokens=llm_response.usage.input_tokens,
      output_tokens=llm_response.usage.output_tokens
    )
