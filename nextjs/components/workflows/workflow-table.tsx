"use client";

import Link from "next/link";
import { ExternalLink, RefreshCw, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { StatusBadge } from "@/components/workflows/status-badge";
import { getCaseId } from "@/lib/workflow-utils";
import type { Workflow } from "@/types/workflow";

export function WorkflowTable({
  workflows,
  isLoading,
  onRetry,
  onDelete,
  deletingThreadId
}: {
  workflows: Workflow[];
  isLoading?: boolean;
  onRetry?: () => void;
  onDelete?: (threadId: string) => void;
  deletingThreadId?: string | null;
}) {
  if (isLoading) {
    return (
      <div className="flex items-center gap-2 rounded-md border border-border bg-background/35 p-4 text-sm text-muted-foreground">
        <Spinner />
        Loading workflows
      </div>
    );
  }

  if (workflows.length === 0) {
    return (
      <div className="rounded-md border border-dashed border-border bg-background/30 p-6 text-sm text-muted-foreground">
        No workflows found. Start an investigation to create the first run.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-border bg-[#111a28] text-xs uppercase text-muted-foreground">
          <tr>
            <th className="px-4 py-3 font-medium">Thread ID</th>
            <th className="px-4 py-3 font-medium">Status</th>
            <th className="px-4 py-3 font-medium">Started At</th>
            <th className="px-4 py-3 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border bg-card">
          {workflows.map((workflow) => (
            <tr key={workflow.thread_id} className="hover:bg-sky-400/[0.06]">
              <td className="px-4 py-3">
                <Link href={`/workflows/${workflow.thread_id}`} className="font-mono text-xs font-medium text-sky-300 hover:underline">
                  {workflow.thread_id}
                </Link>
                {getCaseId(workflow.state) ? <div className="mt-1 text-xs text-muted-foreground">{getCaseId(workflow.state)}</div> : null}
              </td>
              <td className="px-4 py-3">
                <StatusBadge status={workflow.status} />
              </td>
              <td className="px-4 py-3 text-muted-foreground">
                {workflow.started_at ? new Date(workflow.started_at).toLocaleString() : "Not available"}
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-2">
                  <Button asChild variant="outline" size="sm">
                    <Link href={`/workflows/${workflow.thread_id}`}>
                      <ExternalLink className="h-3.5 w-3.5" />
                      Open
                    </Link>
                  </Button>
                  {onDelete ? (
                    <Button
                      variant="ghost"
                      size="icon"
                      title="Delete workflow"
                      disabled={deletingThreadId === workflow.thread_id}
                      onClick={() => onDelete(workflow.thread_id)}
                    >
                      {deletingThreadId === workflow.thread_id ? <Spinner /> : <Trash2 className="h-4 w-4" />}
                    </Button>
                  ) : null}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {onRetry ? (
        <div className="flex justify-end border-t border-border bg-background/30 p-3">
          <Button variant="outline" size="sm" onClick={onRetry}>
            <RefreshCw className="h-3.5 w-3.5" />
            Refresh
          </Button>
        </div>
      ) : null}
    </div>
  );
}
