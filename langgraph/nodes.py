from langgraph.state import WorkflowState
from app.schemas.investigation_facts import InvestigationFacts
from app.services.analyzer import analyze_incident

def analysis_node(state: WorkflowState):
  print("\n Running Analysis Node \n")
  state['analysis'] = analyze_incident(state['facts'])
  return state

def facts_node(state: WorkflowState):
  print("\n Running Facts Node \n")
  state['facts'] = InvestigationFacts(
    case_id="INC24493",
    priority="Low",
    reporter="John",
    final_resolver="Sarah",
    customer_satisfaction=1,
    resolution_duration_hours=52.3,
    total_personnel=7,
    number_of_handoffs=9,
    support_levels_involved=3,
    escalation_count=3
  )
  return state

def report_node(state: WorkflowState):
  print("\n Running Reports Node \n")
  state['report'] = f"""
    Report generated from:
    {state['analysis']}
  """
  return state

def approval_node(state: WorkflowState):
  print("\n Running Approval Node \n")
  return state
  
def route_after_analysis(state: WorkflowState):
  if state["analysis"].severity == "high":
    return "approval"
  return "report"
