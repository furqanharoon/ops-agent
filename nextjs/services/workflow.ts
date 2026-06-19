import { api } from "@/lib/api";
import { deriveWorkflowStatus, getWorkflowFromStart, normalizeStatus } from "@/lib/workflow-utils";
import { isRecord } from "@/lib/utils";
import type {
  ResumeRequest,
  ResumeWorkflowResponse,
  StartWorkflowRequest,
  StartWorkflowResponse,
  Workflow,
  WorkflowState
} from "@/types/workflow";

function toWorkflowState(value: unknown): WorkflowState {
  return isRecord(value) ? (value as WorkflowState) : {};
}

function toWorkflow(value: unknown): Workflow | null {
  if (!isRecord(value)) {
    return null;
  }

  const threadId = typeof value.thread_id === "string" ? value.thread_id : null;
  if (!threadId) {
    return null;
  }

  const state = toWorkflowState(value.state);
  const status = deriveWorkflowStatus(state, typeof value.status === "string" ? value.status : null);
  const workflowId = typeof value.workflow_id === "string" || typeof value.workflow_id === "number" ? value.workflow_id : value.id;
  const startedAt =
    typeof value.started_at === "string"
      ? value.started_at
      : typeof value.created_at === "string"
        ? value.created_at
        : null;

  return {
    thread_id: threadId,
    workflow_id: typeof workflowId === "string" || typeof workflowId === "number" ? workflowId : undefined,
    started_at: startedAt,
    updated_at: typeof value.updated_at === "string" ? value.updated_at : null,
    status,
    state,
    interrupt: state.__interrupt__ ?? null
  };
}

export async function startWorkflow(request: StartWorkflowRequest): Promise<StartWorkflowResponse> {
  const response = await api.post<unknown>("/workflows/start", request);

  if (!isRecord(response.data) || typeof response.data.thread_id !== "string") {
    throw new Error("The workflow API did not return a thread ID.");
  }

  return {
    thread_id: response.data.thread_id,
    state: toWorkflowState(response.data.state)
  };
}

export async function resumeWorkflow(request: ResumeRequest): Promise<ResumeWorkflowResponse> {
  const response = await api.post<unknown>("/workflows/resume", request);

  if (!isRecord(response.data)) {
    throw new Error("The workflow API returned an unexpected response.");
  }

  return {
    thread_id: typeof response.data.thread_id === "string" ? response.data.thread_id : request.thread_id,
    state: toWorkflowState(response.data.state)
  };
}

export async function getWorkflows(): Promise<Workflow[]> {
  const response = await api.get<unknown>("/workflows");

  if (Array.isArray(response.data)) {
    return response.data.map(toWorkflow).filter((workflow): workflow is Workflow => workflow !== null);
  }

  if (isRecord(response.data) && Array.isArray(response.data.workflows)) {
    return response.data.workflows.map(toWorkflow).filter((workflow): workflow is Workflow => workflow !== null);
  }

  return [];
}

export async function getWorkflow(threadId: string): Promise<Workflow | null> {
  const response = await api.get<unknown>(`/workflows/${threadId}`);

  if (typeof response.data === "string" && response.data.length === 0) {
    return null;
  }

  const workflow = toWorkflow(response.data);
  if (workflow) {
    return workflow;
  }

  if (isRecord(response.data)) {
    const state = toWorkflowState(response.data.state ?? response.data);
    return {
      thread_id: threadId,
      status: deriveWorkflowStatus(state, isRecord(response.data) && typeof response.data.status === "string" ? response.data.status : null),
      started_at: typeof response.data.started_at === "string" ? response.data.started_at : null,
      state,
      interrupt: state.__interrupt__ ?? null
    };
  }

  return {
    thread_id: threadId,
    status: normalizeStatus(null),
    state: null,
    interrupt: null
  };
}

export async function deleteWorkflow(threadId: string): Promise<void> {
  await api.delete(`/workflows/${threadId}`);
}

export function createStartedWorkflow(response: StartWorkflowResponse): Workflow {
  return getWorkflowFromStart(response.thread_id, response.state);
}
