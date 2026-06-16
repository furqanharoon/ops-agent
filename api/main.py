from fastapi import FastAPI
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import asyncio
import time

from agent.planner import decide_tool
from agent.logger import log_event
from agent.runtime import run_agent_execution_debug

# app = FastAPI()
# class AgentRequest(BaseModel):
#   query: str

# @app.get("/health")
# async def health_check():
#   await asyncio.sleep(5)
#   return {
#     "status": "ok"
#   }

# @app.post("/agent/run")
# async def run_agent(request: AgentRequest):
#   query = request.query
#   result = await run_agent_execution_debug(query)
#   return result

# # SSE ENDPOINT
# # @app.get("/agent/stream")
# # async def stream_agent(query: str):
# #   return EventSourceResponse(
# #     run_agent_execution(query)
# #   )


app = FastAPI()

app.include_router(health.router)
app.include_router(agent.router)
app.include_router(workflow.router)