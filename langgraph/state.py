from typing import TypedDict
from app.schemas.incident_analysis import IncidentAnalysis
from app.schemas.investigation_facts import InvestigationFacts

class WorkflowState(TypedDict):
  facts: InvestigationFacts | None
  analysis: IncidentAnalysis | None
  report: str | None
