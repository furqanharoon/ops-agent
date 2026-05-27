from fastapi import FastAPI
from pydantic import BaseModel
import time

from app.registry import tool_registry
from app.planner import decide_tool
from app.logger import log_event

app = FastAPI()
MAX_ITERATIONS = 5


class AgentRequest(BaseModel):
  query: str

class AgentState(BaseModel):
  user_query: str
  current_iteration: int = 0
  tool_history: list = []
  observations: list = []
  final_response: str | None = None

@app.get("/health")
async def health_check():
  return {
    "status": "ok"
  }

@app.post("/agent/run")
async def run_agent(request: AgentRequest):
  query = request.query.lower()
  state = AgentState(user_query = query)
  messages = [
    {
      "role": "user",
      "content": query,
    }
  ]

  while state.current_iteration < MAX_ITERATIONS:
    log_event("iteration_started",{"iteration": state.current_iteration})
    tool_decider = await decide_tool(messages)
    print("\n tool_decider \n", tool_decider)
    if tool_decider:
      print("Tool decider details", tool_decider.name)
      tool_name = tool_decider.name
      tool_arguments = tool_decider.input
      tool = tool_registry[tool_name]
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
      messages.append({
        "role": "user",
        "content": f"Tool Result: {tool_result} "
      })
      state.current_iteration+=1
      return {
        "query": request.query,
        "decision": tool_decider,
        "tool_result": tool_result
      }
    else:
      state.final_response = "No action required"
      return {
        "message": "No Matching Tool was found."
      }
