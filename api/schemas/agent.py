from pydantic import BaseModel

class AgentRequest(BaseModel):
  query: str
