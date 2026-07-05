from agent.schemas.investigation_facts import InvestigationFacts
from agent.schemas.incident_analysis import IncidentAnalysis

def analyze_incident(facts:InvestigationFacts)->IncidentAnalysis:
  severity = "low"
  if facts.escalation_count >2:
    severity="high"
  summary=(
    f"Incident {facts.case_id} "
    f"required {facts.escalation_count} escalations "
    f"and involved {facts.total_personnel} personnel"
  )
  return IncidentAnalysis(
    severity=severity,
    summary=summary
  )
