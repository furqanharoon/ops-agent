import json
import time

def log_event(event_type:str, payload: dict):
  event_log = {
    "timestamp": time.time(),
    "event_type":event_type,
    "payload": payload
  }
  print(json.dumps(event_log, indent=2))
