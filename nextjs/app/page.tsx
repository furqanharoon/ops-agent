"use client";

import { FormEvent, useMemo, useState } from "react";
import { CheckCircle2, GitBranch, Play, RefreshCw, ShieldAlert, Timer } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Spinner } from "@/components/ui/spinner";
import { WorkflowTable } from "@/components/workflows/workflow-table";
import { useDeleteWorkflow, useStartWorkflow, useWorkflows } from "@/hooks/use-workflows";
import { getApiErrorMessage } from "@/lib/api";

export default function DashboardPage() {
  const [caseId, setCaseId] = useState("INC24493");
  const workflows = useWorkflows();
  const startWorkflow = useStartWorkflow();
  const deleteWorkflow = useDeleteWorkflow();

  const sortedWorkflows = useMemo(
    () => [...(workflows.data ?? [])].sort((a, b) => Date.parse(b.started_at ?? "") - Date.parse(a.started_at ?? "")),
    [workflows.data]
  );
  const statusCounts = useMemo(() => {
    const runs = workflows.data ?? [];
    return {
      total: runs.length,
      running: runs.filter((workflow) => workflow.status === "running").length,
      approvals: runs.filter((workflow) => workflow.status === "waiting_approval" || workflow.status === "manual_review").length,
      completed: runs.filter((workflow) => workflow.status === "completed" || workflow.status === "approved").length
    };
  }, [workflows.data]);

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    startWorkflow.mutate({ case_id: caseId.trim() });
  };

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6">
      <section className="rounded-lg border border-border bg-card/70 p-5 shadow-[0_18px_50px_rgba(0,0,0,0.18)]">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="mb-2 text-xs font-medium uppercase tracking-[0.18em] text-sky-300">Operations console</p>
            <h1 className="text-2xl font-semibold tracking-normal">Incident Workflow Dashboard</h1>
            <p className="mt-1 text-sm text-muted-foreground">Start investigations, monitor workflow state, and route human approvals.</p>
          </div>
          <div className="rounded-md border border-emerald-400/25 bg-emerald-400/10 px-3 py-2 text-xs text-emerald-200">
            Workflow API configured
          </div>
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-4">
        {[
          { label: "Total Runs", value: statusCounts.total, icon: GitBranch, tone: "text-sky-300" },
          { label: "Running", value: statusCounts.running, icon: Timer, tone: "text-blue-300" },
          { label: "Needs Review", value: statusCounts.approvals, icon: ShieldAlert, tone: "text-amber-300" },
          { label: "Completed", value: statusCounts.completed, icon: CheckCircle2, tone: "text-emerald-300" }
        ].map((item) => (
          <Card key={item.label} className="bg-card/80">
            <CardContent className="flex items-center justify-between p-4">
              <div>
                <p className="text-xs text-muted-foreground">{item.label}</p>
                <p className="mt-1 text-2xl font-semibold">{item.value}</p>
              </div>
              <item.icon className={`h-5 w-5 ${item.tone}`} />
            </CardContent>
          </Card>
        ))}
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Start Investigation</CardTitle>
          <CardDescription>Submit a case ID to start the LangGraph workflow.</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="flex flex-col gap-3 sm:flex-row" onSubmit={onSubmit}>
            <Input
              aria-label="Case ID"
              value={caseId}
              onChange={(event) => setCaseId(event.target.value)}
              placeholder="Enter CaseID"
              disabled={startWorkflow.isPending}
            />
            <Button className="sm:w-44" disabled={startWorkflow.isPending || caseId.trim().length === 0}>
              {startWorkflow.isPending ? <Spinner /> : <Play className="h-4 w-4" />}
              Start Workflow
            </Button>
          </form>
          {startWorkflow.isError ? <p className="mt-3 text-sm text-red-200">{getApiErrorMessage(startWorkflow.error)}</p> : null}
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex-row items-center justify-between space-y-0">
          <div>
            <CardTitle>Recent Workflows</CardTitle>
            <CardDescription>Runs returned by the workflow API.</CardDescription>
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
              workflows={sortedWorkflows}
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
