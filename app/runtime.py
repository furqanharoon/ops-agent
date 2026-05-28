import asyncio
import time
from pydantic import BaseModel

from app.registry import tool_registry
from app.planner import decide_tool
from app.logger import log_event

MAX_ITERATIONS = 5

class AgentState(BaseModel):
  user_query: str
  current_iteration: int = 0
  tool_history: list = []
  observations: list = []
  final_response: str | None = None

async def run_agent_execution(query):
  state = AgentState(user_query=query)
  messages = [
    {
      "role": "user",
      "content": query
    }
  ]
  yield {
    "event": "status",
    "data": "Agent execution started"
  }
  while state.current_iteration < MAX_ITERATIONS:
    log_event("iteration_started",{"iteration": state.current_iteration})
    yield {
      "event": "iteration",
      "data": f"iteration count: {state.current_iteration}"
    }
    yield {
      "event": "planner",
      "data": "Planning next action"
    }
    tool_decider = await decide_tool(messages)
    if tool_decider:
      tool_name = tool_decider.name
      tool_arguments = tool_decider.input
      yield {
        "event": "tool_selected",
        "data": f"Selected Tool: {tool_name}"
      }
      tool = tool_registry[tool_name]
      yield {
        "event": "tool_exection",
        "data": f"Executing {tool_name}"
      }
      start_time = time.perf_counter()
      tool_result = await tool(**tool_arguments)
      execution_time = time.perf_counter()-start_time
      log_event(
        "tool_execution",
        {
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
        "observe": tool_result
      })
      yield {
        "event": "observation",
        "data": f"Observation {tool_result}"
      }
      messages.append({
        "role": "user",
        "content": f"Tool Result: {tool_result} "
      })
      state.current_iteration+=1
      yield {
        "event": "completed",
        "data": {
          "iterations": state.current_iteration,
          "query": query,
          "tool_history": state.tool_history,
          "observations": state.observations
        }
      }
      return {
        "query": query,
        "decision": tool_decider,
        "tool_result": tool_result
      }
    else:
      state.final_response = "No action required"
      return {
        "message": "No Matching Tool was found."
      }