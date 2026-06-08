from langgraph.workflow import graph
from langgraph.types import Command
import asyncio
from app.runtime import run_agent_execution_debug

query="Investigate INC24493"
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

# resume_result = graph.invoke(
#   Command(
#     resume={
#       "approval_status": "approved"
#     }
#   ),
#   config = {
#     "configurable": {
#       "thread_id": "workflow-1"
#     }
#   }
# )
resume_result = graph.invoke(
  Command(
    resume={
      "approval_status": "rejected",
      "rejection_reason": "This case needs to be discussed in Weekly Customer Support Review meeting."
    }
  ),
  config = {
    "configurable": {
      "thread_id": "workflow-1"
    }
  }
)

print(resume_result)
