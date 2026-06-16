from pydantic import BaseModel

class InvestigationFacts(BaseModel):
  # Raw Facts

  case_id: str | None = None

  priority: str | None = None

  reporter: str | None = None

  final_resolver: str | None = None

  customer_satisfaction: int | None = None

  resolution_duration_hours: float | None = None
  
  # Derived Metrics

  total_personnel: int | None = None

  number_of_handoffs: int | None = None

  support_levels_involved: int | None = None

  escalation_count: int | None = None

  error_message: str | None = None
