
from fastapi import APIRouter
from api.schemas.agent import AgentRequest
from agent.runtime import run_agent_execution_debug

router = APIRouter()

@router.post("/agent/run")
async def run_agent(request: AgentRequest):
  query = request.query
  result = await run_agent_execution_debug(query)
  return result
