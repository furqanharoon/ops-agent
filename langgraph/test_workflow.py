from langgraph.workflow import get_graph
from langgraph.types import Command
import asyncio
import uuid
from app.runtime import run_agent_execution_debug
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.workflow_runs import create_workflow_run


DB_URI = "postgresql://postgres@localhost/incident_management"

query="Investigate INC24493"
response = asyncio.run(
  run_agent_execution_debug(query)
)

thread_id = str(uuid.uuid4())
create_workflow_run(thread_id)
print(f"Thread ID: {thread_id}")

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
  graph = get_graph(checkpointer)


  result = graph.invoke(
    {
      "thread_id": thread_id,
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
        "thread_id": thread_id
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
  # resume_result = graph.invoke(
  #   Command(
  #     resume={
  #       "approval_status": "rejected",
  #       "rejection_reason": "This case needs to be discussed in Weekly Customer Support Review meeting."
  #     }
  #   ),
  #   config = {
  #     "configurable": {
  #       "thread_id": "workflow-1"
  #     }
  #   }
  # )

  # print(resume_result)
