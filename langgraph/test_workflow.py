from langgraph.workflow import graph
import asyncio
from app.runtime import run_agent_execution_debug

query="Investigate INC0012"
response = asyncio.run(
  run_agent_execution_debug(query)
)

result = graph.invoke(
  {
    "incident": response['incident'],
    "duration": response['duration'],
    "timeline": response['timeline'],
    "facts": None,
    "analysis": None,
    "report": None,
    "approval_status": None,
    "rejection_status": None
  },
  config={
    "configurable": {
      "thread_id": "workflow-1"
    }
  }
)

print(result)
