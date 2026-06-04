import asyncio
import time
import uuid
from pydantic import BaseModel,Field
from app.tools.tools_registry import tools_registry
from app.planner import decide_tool
from app.logger import log_event
from app.utils.fetch_tool_result import get_tool_result

MAX_ITERATIONS = 5
class AgentState(BaseModel):
  user_query: str
  trace_id: str = str(uuid.uuid4())
  current_iteration: int = 0
  final_response: str | None = None
  llm_calls: int = 0
  total_input_tokens: int = 0
  total_output_tokens: int = 0
  total_tokens: int = 0
  tool_history: list = Field(default_factory=list)
  observations: list = Field(default_factory=list)
  messages: list = Field(default_factory=list)
  memory: dict = Field(default_factory=dict)

async def run_agent_execution_debug(query):
  state = AgentState(user_query=query,trace_id=str(uuid.uuid4()))
  messages = [
    {
      "role": "user",
      "content": query
    }
  ]
  state.messages.append({
    "role": "user",
    "content": query
  })
  while state.current_iteration < MAX_ITERATIONS:
    log_event("iteration_started",{"iteration": state.current_iteration})
    tool_response = await decide_tool(messages)
    state.total_input_tokens+=tool_response.input_tokens
    state.total_output_tokens+=tool_response.output_tokens
    state.total_tokens=(state.total_input_tokens+state.total_output_tokens)
    state.llm_calls+=1
    if tool_response.action == "final":
      state.final_response = tool_response.final_response
      break
    # Start of LOOP
    tool_results = []
    tool_names = []
    for tool_use in tool_response.tool_uses:
      # tool_name = tool_response.tool_name
      # tool_arguments = tool_response.tool_arguments
      tool_name = tool_use.name
      tool_names.append(tool_name)
      tool = tools_registry[tool_name]
      tool_arguments = tool_use.input
      start_time = time.perf_counter()
      try:
        tool_result = await tool(**tool_arguments)
        if tool_name == 'get_incident':
          state.memory['incident'] = tool_result
        if tool_name == "get_incident_duration":
          state.memory['duration'] = tool_result
        if tool_name == 'get_incident_timeline':
          state.memory['timeline'] = tool_result

        print("\n MEMORY", tool_name)
        print("="*80)
        print(state.memory)

        tool_result_dict = {
          "tool_name":tool_name,
          "result": tool_result
        }
        tool_results.append(
          tool_result_dict
        )
        state.messages.append(
          {
            "role": "user",
            "content": f"Observation : {tool_result_dict}"
          }
        )
        messages.append({
          "role": "user",
          "content": f"Observation : {tool_result_dict}"
        })
      except Exception as e:
        log_event("tool_failure",{
          "trace_id": state.trace_id,
          "tool_name": tool_name,
          "arguments": tool_arguments,
          "current_iteration": state.current_iteration,
          "status": "Failed",
          "error": str(e)
        })
        state.tool_history.append({
          "tool": tool_name,
          "arguments": tool_arguments,
          "current_iteration": state.current_iteration,
          "failure_reason": str(e),
        })
        state.observations.append({
          "tool": tool_name,
          "status": "Tool Failed",
          "error": str(e)
        })
        tool_results.append({
          "status": "failed",
          "tool_name":tool_name,
          "error": str(e)
        })
      execution_time = time.perf_counter()-start_time
      log_event(
        "tool_execution",
        {
          "trace_id": state.trace_id,
          "tool_name": tool_name,
          "arguments": tool_arguments,
          "tool_result": tool_result,
          "execution_time_in_ms": execution_time
        }
      )
      state.tool_history.append({
        "tool": tool_name,
        "arguments": tool_arguments,
        "tool_result": tool_result
      })
      state.observations.append({
        "tool": tool_name,
        "observation": tool_result
      })
    ### END OF LOOP
    incident = get_tool_result(tool_results, "get_incident")
    duration = get_tool_result(tool_results, "get_incident_duration")
    timeline = get_tool_result(tool_results, "get_incident_timeline")
    state.current_iteration+=1
  
  return {
    "trace_id": state.trace_id,
    "query": query,
    "final_response": state.final_response,
    "state": state,
    "incident": incident,
    "duration": duration,
    "timeline": timeline
  }
