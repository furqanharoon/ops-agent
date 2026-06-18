"use client";

import { useParams } from "next/navigation";
import { RefreshCw } from "lucide-react";
import { AnalysisCard } from "@/components/workflows/analysis-card";
import { ApprovalDialog } from "@/components/workflows/approval-dialog";
import { FactsCard } from "@/components/workflows/facts-card";
import { IncidentCard } from "@/components/workflows/incident-card";
import { ReportCard } from "@/components/workflows/report-card";
import { StatusBadge } from "@/components/workflows/status-badge";
import { buildWorkflowSteps, WorkflowTimeline } from "@/components/workflows/workflow-timeline";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { useWorkflow } from "@/hooks/use-workflows";
import { getApiErrorMessage } from "@/lib/api";
import { deriveWorkflowStatus } from "@/lib/workflow-utils";

export default function WorkflowDetailPage() {
  const params = useParams<{ thread_id: string }>();
  const threadId = params.thread_id;
  const workflow = useWorkflow(threadId);
  const state = workflow.data?.state;
  const status = workflow.data?.status ?? deriveWorkflowStatus(state);
  const waitingForApproval = status === "waiting_approval";

  if (workflow.isLoading) {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Spinner />
        Loading workflow
      </div>
    );
  }

  if (workflow.isError) {
    return (
      <div className="mx-auto max-w-3xl rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-700">
        <p>{getApiErrorMessage(workflow.error)}</p>
        <Button className="mt-3" variant="outline" size="sm" onClick={() => workflow.refetch()}>
          Retry
        </Button>
      </div>
    );
  }

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6">
      <section className="flex flex-col gap-4 rounded-lg border border-border bg-card/70 p-5 shadow-[0_18px_50px_rgba(0,0,0,0.18)] md:flex-row md:items-start md:justify-between">
        <div>
          <p className="mb-2 text-xs font-medium uppercase tracking-[0.18em] text-sky-300">Workflow trace</p>
          <h1 className="text-2xl font-semibold tracking-normal">Workflow Details</h1>
          <p className="mt-1 break-all font-mono text-sm text-muted-foreground">{threadId}</p>
        </div>
        <div className="flex items-center gap-2">
          <StatusBadge status={status} />
          <Button variant="outline" size="sm" onClick={() => workflow.refetch()} disabled={workflow.isFetching}>
            {workflow.isFetching ? <Spinner /> : <RefreshCw className="h-3.5 w-3.5" />}
            Refresh
          </Button>
        </div>
      </section>

      {waitingForApproval ? <ApprovalDialog threadId={threadId} /> : null}

      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_340px]">
        <div className="flex flex-col gap-6">
          <IncidentCard incident={state?.incident} />
          <FactsCard facts={state?.facts} />
          <AnalysisCard analysis={state?.analysis} />
          <Card>
            <CardHeader>
              <CardTitle>Approval State</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p>
                <span className="text-muted-foreground">Status: </span>
                {state?.approval_status ?? "Not requested"}
              </p>
              {state?.rejection_reason ? (
                <p>
                  <span className="text-muted-foreground">Rejection reason: </span>
                  {state.rejection_reason}
                </p>
              ) : null}
            </CardContent>
          </Card>
          <ReportCard report={state?.report} />
        </div>

        <div className="flex flex-col gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <WorkflowTimeline steps={buildWorkflowSteps(state)} />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Workflow State</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="max-h-[440px] overflow-auto rounded-md border border-border bg-background/45 p-3 text-xs leading-5">
                {JSON.stringify(state ?? { thread_id: threadId }, null, 2)}
              </pre>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
