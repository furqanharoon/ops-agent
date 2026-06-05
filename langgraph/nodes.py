from langgraph.state import WorkflowState

def analysis_node(state: WorkflowState):
  print("\n Running Analysis Node \n")
  state['analysis'] = "Analysis Done"
  return state

def report_node(state: WorkflowState):
  print("\n Running Reports Node \n")
  state['report'] = f"""
    Report generated from:
    {state['analysis']}
  """
  return state
