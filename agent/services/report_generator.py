from app.schemas.investigation_facts import InvestigationFacts
from app.schemas.incident_analysis import IncidentAnalysis

def generate_report(facts: InvestigationFacts, analysis:IncidentAnalysis) -> str:
  return f"""
    Case ID: {facts.case_id}
    Priority: {facts.priority}
    Reporter: {facts.reporter}
    Final Resolver: {facts.final_resolver}
    Customer Satisfaction: {facts.customer_satisfaction}
    Total Personnel: {facts.total_personnel}
    Total Handoffs: {facts.number_of_handoffs}
    Escalation Count: {facts.escalation_count}
    Analyse Severity: {analysis.severity}
    Analyse Summary: {analysis.summary}
  """
