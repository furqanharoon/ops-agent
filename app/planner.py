from app.logger import log_event

def decide_tool(query:str):
  query = query.lower()
  if "cpu" in query:
    decision = {
      "tool": "get_cpu_usage",
      "arguments": {
        "server_name": "web-1"
      }
    }
    log_event("planner_decision", decision)
    return decision
  if "restart" in query:
    decision = {
      "tool_name": "restart_service",
      "arguments": {
        "service_name": "nginx"
      }
    }
    log_event("planner_decision", decision)
    return decision
  return None
