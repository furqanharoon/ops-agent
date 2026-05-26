import random

async def get_cpu_usage(server_name:str):
  return {
    "server_name": server_name,
    "cpu_percent": random.randint(50,100)
  }