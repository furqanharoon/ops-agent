def get_tool_result(tool_results, tool_name):
  for tool_result in tool_results:
    if tool_result["tool_name"] == tool_name:
      return tool_result["result"]
  return None
