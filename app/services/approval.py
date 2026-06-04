from app.schemas.incident_analysis import IncidentAnalysis

def requires_human_approval(analysis: IncidentAnalysis)->bool:
  return analysis.severity == "high"
