from pydantic import BaseModel

class StartWorkflowRequest(BaseModel):
  case_id: str

class ResumeWorkflowRequest(BaseModel):
  thread_id: str
  approval_status: str
  rejection_reason: str | None = None


class WorkflowResponse(BaseModel):
  workflow_id: str
  thread_id: str
  status: str
