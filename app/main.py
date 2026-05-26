from fastapi import FastAPI
from pydantic import BaseModel
import time

from app.registry import tool_registry
from app.planner import decide_tool
from app.logger import log_event

app = FastAPI()

class AgentRequest(BaseModel):
  query: str

@app.get("/health")
async def health_check():
  return {
    "status": "ok"
  }

@app.post("/agent/run")
async def run_agent(request: AgentRequest):
  query = request.query.lower()
  tool_decider = decide_tool(query)
  if tool_decider:
    tool_name = tool_decider["tool"]
    tool_arguments = tool_decider["arguments"]
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
    return {
      "query": request.query,
      "decision": tool_decider,
      "tool_result": tool_result
    }
  else:
    return {
      "message": "No Matching Tool was found."
    }
