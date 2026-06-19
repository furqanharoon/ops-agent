from orchestration.state import WorkflowState
from langgraph.types import interrupt
from agent.schemas.investigation_facts import InvestigationFacts
from agent.services.analyzer import analyze_incident
from agent.services.facts_extractor import build_investigation_facts
from agent.services.report_generator import generate_report

def analysis_node(state: WorkflowState):
  state['analysis'] = analyze_incident(state['facts'])
  return state

def facts_node(state: WorkflowState):
  state['facts'] = build_investigation_facts(state['incident'], state['duration'], state['timeline'])
  return state

def report_node(state: WorkflowState):
  state['report'] = generate_report(state['facts'], state['analysis'])
  return state

def require_approval_node(state: WorkflowState):
  approval_response = interrupt(
    {
      "message": "Human approval required",
      "analysis": str(state['analysis'])
    }
  )
  state['approval_status'] = approval_response['approval_status']
  if approval_response['approval_status'] =='rejected':
    state['rejection_reason'] = approval_response["rejection_reason"]

  return state
  
def route_after_analysis(state: WorkflowState):
  if state["analysis"].severity == "high":
    return "required_approval"
  return "report"

def route_after_required_approval(state: WorkflowState):
  if state['approval_status'] == 'approved':
    return "report"
  return "manual_review"

def manual_review_node(state: WorkflowState):
  return state
