from langgraph.graph import StateGraph,START,END

from langgraph.state import WorkflowState
from langgraph.nodes import analysis_node, report_node, approval_node, route_after_analysis, facts_node

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
  "approval",
  approval_node
)

graph_builder.add_edge(
  START,
  "facts"
) # This adds and Edge that says START and goto analysis node

# graph_builder.add_edge(
#   "analysis",
#   "report"
# )
graph_builder.add_edge(
  "facts",
  "analysis"
)
graph_builder.add_conditional_edges(
  "analysis",
  route_after_analysis
)

graph_builder.add_edge(
  "approval",
  "report"
)

graph_builder.add_edge(
  "report",
  END
) # This add axnother Edge that says from Analysis node, goto END of Graph.

graph = graph_builder.compile() # This run the whole graph and make it executable
