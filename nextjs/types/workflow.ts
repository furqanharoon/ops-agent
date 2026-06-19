export type WorkflowStatus =
  | "running"
  | "waiting_approval"
  | "completed"
  | "manual_review"
  | "rejected"
  | "approved"
  | "unknown";

export interface StartWorkflowRequest {
  case_id: string;
}

export interface ResumeRequest {
  thread_id: string;
  approval_status: "approved" | "rejected";
  rejection_reason?: string;
}

export interface Incident {
  case_id?: string | null;
  priority?: string | null;
  reporter?: string | null;
  issue_type?: string | null;
  short_description?: string | null;
  customer_satisfaction?: number | null;
  [key: string]: unknown;
}

export interface Facts {
  case_id?: string | null;
  priority?: string | null;
  reporter?: string | null;
  final_resolver?: string | null;
  customer_satisfaction?: number | null;
  resolution_duration_hours?: number | null;
  total_personnel?: number | null;
  number_of_handoffs?: number | null;
  support_levels_involved?: number | null;
  escalation_count?: number | null;
  error_message?: string | null;
}

export interface Analysis {
  severity?: string | null;
  summary?: string | null;
}

export interface TimelineEvent {
  id?: string | number;
  label?: string;
  actor?: string | null;
  timestamp?: string | null;
  description?: string | null;
  [key: string]: unknown;
}

export interface Interrupt {
  value?: unknown;
  resumable?: boolean;
  ns?: string[];
  when?: string;
  [key: string]: unknown;
}

export interface WorkflowState {
  thread_id?: string | null;
  incident?: Incident | null;
  duration?: Record<string, unknown> | null;
  facts?: Facts | null;
  analysis?: Analysis | null;
  report?: string | null;
  approval_status?: string | null;
  rejection_reason?: string | null;
  timeline?: TimelineEvent[] | null;
  __interrupt__?: Interrupt[] | null;
  [key: string]: unknown;
}

export interface Workflow {
  thread_id: string;
  workflow_id?: string | number;
  status: WorkflowStatus;
  started_at?: string | null;
  updated_at?: string | null;
  state?: WorkflowState | null;
  interrupt?: Interrupt[] | null;
}

export interface StartWorkflowResponse {
  thread_id: string;
  state: WorkflowState;
}

export interface ResumeWorkflowResponse {
  thread_id?: string;
  state: WorkflowState;
}
