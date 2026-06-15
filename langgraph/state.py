from typing import TypedDict
from app.schemas.incident_analysis import IncidentAnalysis
from app.schemas.investigation_facts import InvestigationFacts

class WorkflowState(TypedDict):
  thread_id: str | None
  facts: InvestigationFacts | None
  analysis: IncidentAnalysis | None
  report: str | None
  approval_status: str | None
  rejection_reason: str | None
  incident: dict | None
  duration: dict | None
  timeline: list | None
  