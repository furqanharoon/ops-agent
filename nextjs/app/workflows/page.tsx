"use client";

import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { WorkflowTable } from "@/components/workflows/workflow-table";
import { useDeleteWorkflow, useWorkflows } from "@/hooks/use-workflows";
import { getApiErrorMessage } from "@/lib/api";

export default function WorkflowsPage() {
  const workflows = useWorkflows();
  const deleteWorkflow = useDeleteWorkflow();

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6">
      <section className="rounded-lg border border-border bg-card/70 p-5 shadow-[0_18px_50px_rgba(0,0,0,0.18)]">
        <p className="mb-2 text-xs font-medium uppercase tracking-[0.18em] text-sky-300">Run registry</p>
        <h1 className="text-2xl font-semibold tracking-normal">Workflows</h1>
        <p className="mt-1 text-sm text-muted-foreground">Inspect incident investigation workflow runs and operational state.</p>
      </section>

      <Card>
        <CardHeader className="flex-row items-center justify-between space-y-0">
          <div>
            <CardTitle>All Workflows</CardTitle>
            <CardDescription>Backed by the workflow list endpoint when available.</CardDescription>
          </div>
          <Button variant="outline" size="sm" onClick={() => workflows.refetch()} disabled={workflows.isFetching}>
            {workflows.isFetching ? <Spinner /> : <RefreshCw className="h-3.5 w-3.5" />}
            Refresh
          </Button>
        </CardHeader>
        <CardContent>
          {workflows.isError ? (
            <div className="rounded-md border border-red-400/35 bg-red-400/10 p-4 text-sm text-red-200">
              <p>{getApiErrorMessage(workflows.error)}</p>
              <Button className="mt-3" variant="outline" size="sm" onClick={() => workflows.refetch()}>
                Retry
              </Button>
            </div>
          ) : (
            <WorkflowTable
              workflows={workflows.data ?? []}
              isLoading={workflows.isLoading}
              onRetry={() => workflows.refetch()}
              onDelete={(threadId) => deleteWorkflow.mutate(threadId)}
              deletingThreadId={deleteWorkflow.variables ?? null}
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
