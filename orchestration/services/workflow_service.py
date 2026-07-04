import asyncio
import uuid
from orchestration.workflow import get_graph
from langgraph.types import Command
from agent.runtime import run_agent_execution_debug
from langgraph.checkpoint.postgres import PostgresSaver
from orchestration.repositories.workflow_repository import create_workflow_run, update_workflow_status, get_all_workflows, get_workflow

DB_URI = "postgresql://postgres@localhost/incident_management"

async def start_workflow(case_id: str):
  query = f"Investigate {case_id}"

  response = await run_agent_execution_debug(query)
  
  result = None

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

  return {
    "thread_id": thread_id,
    "state": result
  }

async def resume_workflow(
  thread_id:str,
  approval_status:str | None = None,
  rejection_reason:str | None = None
):
  resume_payload = {
    "approval_status": approval_status
  }
  if rejection_reason:
    resume_payload["rejection_reason"] = rejection_reason
  update_workflow_status(thread_id, approval_status)
  with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    graph = get_graph(checkpointer)
    resume_result = graph.invoke(
      Command(
        resume=resume_payload
      ),
      config = {
        "configurable": {
          "thread_id": thread_id
        }
      }
    )
    print(resume_result)
  
  return {
    "state": resume_result
  }

async def list_workflows():
  workflows = get_all_workflows()
  return {
    "workflows": workflows
  }

async def get_workflow_details(thread_id):
  row = get_workflow(thread_id)

  if not row:
    return None

  id_, thread_id_db, status, created_at, updated_at = row

  state = None
  with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    graph = get_graph(checkpointer)
    snapshot = graph.get_state({"configurable": {"thread_id": thread_id}})
    if snapshot:
      state = snapshot.values

  return {
    "id": id_,
    "thread_id": thread_id_db,
    "status": status,
    "created_at": created_at.isoformat() if created_at else None,
    "updated_at": updated_at.isoformat() if updated_at else None,
    "state": state
  }