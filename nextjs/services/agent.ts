import { api } from "@/lib/api";
import type { AgentRequest, AgentResponse } from "@/types/agent";

export async function runAgent(request: AgentRequest): Promise<AgentResponse> {
  const response = await api.post<AgentResponse>("/agent/run", request);
  return response.data;
}
