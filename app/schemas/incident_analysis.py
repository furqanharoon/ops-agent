from pydantic import BaseModel

class IncidentAnalysis(BaseModel):
  severity: str | None = None
  summary: str | None = None
