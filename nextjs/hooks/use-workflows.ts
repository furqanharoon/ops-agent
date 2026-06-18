"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createStartedWorkflow, deleteWorkflow, getWorkflow, getWorkflows, resumeWorkflow, startWorkflow } from "@/services/workflow";
import type { ResumeRequest, StartWorkflowRequest, Workflow } from "@/types/workflow";

export const workflowKeys = {
  all: ["workflows"] as const,
  detail: (threadId: string) => ["workflows", threadId] as const
};

export function useWorkflows() {
  return useQuery({
    queryKey: workflowKeys.all,
    queryFn: getWorkflows
  });
}

export function useWorkflow(threadId: string) {
  return useQuery({
    queryKey: workflowKeys.detail(threadId),
    queryFn: () => getWorkflow(threadId),
    enabled: threadId.length > 0
  });
}

export function useStartWorkflow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: StartWorkflowRequest) => startWorkflow(request),
    onSuccess: (response) => {
      const workflow = createStartedWorkflow(response);
      queryClient.setQueryData<Workflow[]>(workflowKeys.all, (current) => [workflow, ...(current ?? [])]);
      queryClient.setQueryData(workflowKeys.detail(response.thread_id), workflow);
    }
  });
}

export function useResumeWorkflow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: ResumeRequest) => resumeWorkflow(request),
    onSuccess: (response, request) => {
      const threadId = response.thread_id ?? request.thread_id;
      queryClient.invalidateQueries({ queryKey: workflowKeys.detail(threadId) });
      queryClient.invalidateQueries({ queryKey: workflowKeys.all });
    }
  });
}

export function useDeleteWorkflow() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (threadId: string) => deleteWorkflow(threadId),
    onSuccess: (_response, threadId) => {
      queryClient.setQueryData<Workflow[]>(workflowKeys.all, (current) => current?.filter((workflow) => workflow.thread_id !== threadId) ?? []);
      queryClient.removeQueries({ queryKey: workflowKeys.detail(threadId) });
    }
  });
}
