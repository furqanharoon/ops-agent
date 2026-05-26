def decide_tool(query:str):
  query = query.lower()
  if "cpu" in query:
    return {
      "tool": "get_cpu_usage",
      "arguments": {
        "server_name": "web-1"
      }
    }
  if "restart" in query:
    return {
      "tool_name": "restart_service",
      "arguments": {
        "service_name": "nginx"
      }
    }
  return None