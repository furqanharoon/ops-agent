from fastapi import FastAPI
from pydantic import BaseModel
from see_starlette.sse import EventSourceResponse
from runtime import run_agent_execution
import asyncio
import time

from app.registry import tool_registry
from app.planner import decide_tool
from app.logger import log_event

app = FastAPI()
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
  print("\nSTART\n")
  await time.sleep(5)
  print("THIS IS AFTER SLEEP\n")
  return {
    "status": "ok"
  }

@app.post("/agent/run")
async def run_agent(request: AgentRequest):
  return {
    "message": "Use /agent/stream end-point for streaming runtime"
  }

# SSE ENDPOINT
@app.get("/agent/stream")
async def stream_agent(query: str):
  return EventSourceResponse(
    run_agent_execution(query)
  )
