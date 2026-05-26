import random

async def get_cpu_usage(server_name:str):
  return {
    "server_name": server_name,
    "cpu_percent": random.randint(50,100)
  }

async def restart_service(service_name:str):
  return {
    "service": service_name,
    "status": "restarted"
  }
