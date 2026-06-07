from langgraph.workflow import graph

result = graph.invoke(
  {
    "facts": None,
    "analysis": None,
    "report": None
  },
  config={
    "configurable": {
      "thread_id": "workflow-1"
    }
  }
)

print(result)
