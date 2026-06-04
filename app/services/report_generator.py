from app.schemas.investigation_facts import InvestigationFacts
from app.schemas.incident_analysis import IncidentAnalysis

#  FACTSSSSSS case_id='INC24493' priority='Low' reporter='John' final_resolver='sarah' customer_satisfaction=1 resolution_duration_hours=56.31666666666667 total_personnel=7 number_of_handoffs=9 support_levels_involved=3 escalation_count=3 error_message=''


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