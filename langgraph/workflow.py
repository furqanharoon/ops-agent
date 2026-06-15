from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.state import WorkflowState
from langgraph.nodes import analysis_node, report_node, require_approval_node, route_after_analysis, facts_node, route_after_required_approval, manual_review_node
from langgraph.checkpoint.postgres import PostgresSaver


def get_graph(checkpointer):
  graph_builder = StateGraph(WorkflowState) # Creates an empty graph

  graph_builder.add_node(
    "facts",
    facts_node
  )
  graph_builder.add_node(
    "analysis",
    analysis_node
  ) # this creates a node to the graph

  graph_builder.add_node(
    "report",
    report_node
  )
  graph_builder.add_node(
    "required_approval",
    require_approval_node
  )

  graph_builder.add_node(
    "manual_review",
    manual_review_node
  )


  graph_builder.add_edge(
    START,
    "facts"
  ) # This adds and Edge that says START and goto analysis node

  graph_builder.add_edge(
    "facts",
    "analysis"
  )
  graph_builder.add_conditional_edges(
    "analysis",
    route_after_analysis
  )

  graph_builder.add_conditional_edges(
    "required_approval",
    route_after_required_approval
  )

  graph_builder.add_edge(
    "manual_review",
    END
  )

  graph_builder.add_edge(
    "report",
    END
  ) # This add axnother Edge that says from Analysis node, goto END of Graph.

  graph = graph_builder.compile(checkpointer=checkpointer) # This run the whole graph and make it executable
  return graph
