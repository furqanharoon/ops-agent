from app.tools import (get_cpu_usage, restart_service)

tool_registry = {
  "get_cpu_usage": get_cpu_usage,
  "restart_service": restart_service
}