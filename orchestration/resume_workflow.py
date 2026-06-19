from orchestration.workflow import get_graph
from langgraph.types import Command
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://postgres@localhost/incident_management"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
  graph = get_graph(checkpointer)
  resume_result = graph.invoke(
    Command(
      resume={
        "approval_status": "approved"
      }
    ),
    config = {
      "configurable": {
        "thread_id": "workflow-1"
      }
    }
  )
  print(resume_result)
  