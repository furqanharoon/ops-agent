from fastapi import FastAPI
from pydantic import BaseModel

from app.tools import get_cpu_usage

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

  if "cpu" in query:
    tool_result = await get_cpu_usage(server_name="web-1")
    return {
      "query": request.query,
      "tool_used": "get_cpu_usage",
      "tool_result": tool_result
    }
  return {
    "message": "No matching tool found."
  }
