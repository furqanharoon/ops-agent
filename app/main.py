from fastapi import FastAPI
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from app.runtime import (run_agent_execution_debug)
import asyncio
import time

from app.planner import decide_tool
from app.logger import log_event

app = FastAPI()
class AgentRequest(BaseModel):
  query: str

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
  query = request.query
  result = await run_agent_execution_debug(query)
  return result

# SSE ENDPOINT
# @app.get("/agent/stream")
# async def stream_agent(query: str):
#   return EventSourceResponse(
#     run_agent_execution(query)
#   )
