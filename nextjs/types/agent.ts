export interface AgentRequest {
  query: string;
}

export interface AgentResponse {
  trace_id?: string;
  final_answer?: string;
  incident?: Record<string, unknown>;
  duration?: Record<string, unknown>;
  timeline?: Record<string, unknown>[];
  [key: string]: unknown;
}
