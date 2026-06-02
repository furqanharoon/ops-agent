from app.schemas.investigation_facts import InvestigationFacts
from datetime import datetime

def build_investigation_facts(incident:dict,duration:dict,timeline:list):
  if "error" in incident or "error" in duration:
    return InvestigationFacts(
      error_message="Incident not found"
    )
  final_resolver = ""
  total_personnel = []
  total_esclations = []
  levels = set()
  handoffs_count = 0

  opened = datetime.fromisoformat(
    duration["opened_at"]
  )
  closed = datetime.fromisoformat(
    duration["closed_at"]
  )
  resolution_duration_hours = (closed - opened).total_seconds() / 3600
  loop_count = 0
  active_resolver = ""
  for event in reversed(timeline):
    if "solved" in event['event_type'].lower():
      final_resolver=event['resolver'].lower()
    if event['resolver'] and event['resolver'] not in total_personnel:
      total_personnel.append(event['resolver'])
    if "escalate" in event['event_type'].lower():
      total_esclations.append("escalate")
    if "level 1" in event['event_type'].lower():
      levels.add(1)
    if "level 2" in event['event_type'].lower():
      levels.add(2)
    if "level 3" in event['event_type'].lower():
      levels.add(3)
    if event['resolver'] and event['resolver']!= active_resolver and loop_count>0:
      handoffs_count+=1
    
    if event['resolver']:
      loop_count+=1
      active_resolver = event['resolver']
      
  return InvestigationFacts(
    case_id=incident['case_id'],
    priority=incident['priority'],
    reporter=incident['reporter'],
    customer_satisfaction=incident['customer_satisfaction'],
    final_resolver=final_resolver,
    resolution_duration_hours=resolution_duration_hours,
    total_personnel=len(total_personnel),
    number_of_handoffs=handoffs_count,
    support_levels_involved=len(levels),
    escalation_count=len(total_esclations),
    error_message=""
  )
