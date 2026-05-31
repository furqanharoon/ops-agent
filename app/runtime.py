import asyncio
import time
import uuid
from pydantic import BaseModel
from app.tools.tools_registry import tools_registry
from app.planner import decide_tool
from app.logger import log_event

MAX_ITERATIONS = 5
class AgentState(BaseModel):
  user_query: str
  trace_id: str = str(uuid.uuid4())
  current_iteration: int = 0
  tool_history: list = []
  observations: list = []
  final_response: str | None = None
  llm_calls: int = 0
  total_input_tokens: int = 0
  total_output_tokens: int = 0
  total_tokens: int = 0

async def run_agent_execution(query):
  state = AgentState(
    user_query=query,
    trace_id=str(uuid.uuid4())
  )
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
      "data": {
        "iteration": state.current_iteration
      }
    }
    tool_response = await decide_tool(messages)
    tool_decider = tool_response['tool_use']
    state.total_input_tokens+=tool_response['input_tokens']
    state.total_output_tokens+=tool_response['output_tokens']
    state.total_tokens=state.total_tokens+(state.total_input_tokens+state.total_output_tokens)
    state.llm_calls+=1

    if not tool_decider:
      state.final_response = "No action required"
      yield {
        "event": "final_response",
        "data": {
          "message": "No action required"
        }
      }

    tool_name = tool_decider.name
    tool_arguments = tool_decider.input
    yield {
      "event": "tool_selected",
      "data": {
        "tool_name": tool_name,
        "tool_arguments": tool_arguments
      }
    }
    tool = tools_registry[tool_name]
    yield {
      "event": "tool_exection",
      "data":
      {
        "tool_name": tool_name,
        "tool_arguments": tool_arguments
      }
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
      "observation": tool_result
    })
    yield {
      "event": "observation",
      "data": {
        "tool_name": tool_name,
        "tool_result": tool_result
      }
    }
    messages.append({
      "role": "assistant",
      "content": f"I used tool {tool_name}"
    })
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

async def run_agent_execution_debug(query):
  state = AgentState(user_query=query,trace_id=str(uuid.uuid4()))
  messages = [
    {
      "role": "user",
      "content": query
    }
  ]
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
        tool_results.append(
          {
            "tool_name":tool_name,
            "result": tool_result
          }
        )
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
    messages.append({
      "role": "assistant",
      "content": f"I used tools {tool_names}"
    })
    messages.append({
      "role": "user",
      "content": f"Tool Results: {tool_results} "
    })
    state.current_iteration+=1
  
  return {
    "trace_id": state.trace_id,
    "query": query,
    "final_response": state.final_response,
    "state": state
  }
