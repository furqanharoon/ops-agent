from app.schemas.investigation_facts import InvestigationFacts
from app.schemas.incident_analysis import IncidentAnalysis

def analyze_incident(facts:InvestigationFacts)->IncidentAnalysis:
  severity = "low"
  if facts.escalation_count >2:
    severity="high"
  summary=(
    f"Incident {facts.case_id} "
    f"required {facts.escalation_count} " 
    f"and involved {facts.total_personnel} "
  )
  return IncidentAnalysis(
    severity=severity,
    summary=summary
  )
