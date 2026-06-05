from langgraph.workflow import graph

result = graph.invoke(
  {
    "facts": None,
    "analysis": None,
    "report": None
  }
)

print(result)
