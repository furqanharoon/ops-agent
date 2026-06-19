from fastapi import APIRouter
from orchestration.services.workflow_service import start_workflow, resume_workflow, list_workflows, get_workflow
from api.schemas.agent import AgentRequest
from api.schemas.workflow import ResumeWorkflowRequest, WorkflowResponse, StartWorkflowRequest
router = APIRouter()

@router.post("/workflows/start")
async def start_new_workflow(request: StartWorkflowRequest):
  return await start_workflow(request.case_id)

@router.post("/workflows/resume")
async def resume_existing_workflow(request: ResumeWorkflowRequest):
  return await resume_workflow(request.thread_id, request.approval_status, request.rejection_reason)

@router.get("/workflows/{thread_id}")
async def get_workflow(thread_id: str):
  return ""

@router.get("/workflows")
async def list_workflows():
  return await list_workflows()

@router.delete("/workflows/{thread_id}")
async def delete_workflow(thread_id: str):
  return ""
