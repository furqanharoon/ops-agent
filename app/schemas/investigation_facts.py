from pydantic import BaseModel


class InvestigationFacts(BaseModel):
  # Raw Facts
  
  case_id: str

  priority: str

  reporter: str

  final_resolver: str

  customer_satisfaction: int

  resolution_duration_hours: float
  # Derived Metrics

  total_personnel: int

  handoffs: int

  support_levels_involved: int

  escalation_count: int