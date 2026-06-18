import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/workflows/status-badge";
import { getCaseId } from "@/lib/workflow-utils";
import type { Workflow } from "@/types/workflow";

export function WorkflowCard({ workflow }: { workflow: Workflow }) {
  return (
    <Link href={`/workflows/${workflow.thread_id}`}>
      <Card className="transition-colors hover:bg-sky-400/[0.06]">
        <CardHeader>
          <div className="flex items-center justify-between gap-3">
            <CardTitle className="font-mono text-sm">{workflow.thread_id}</CardTitle>
            <StatusBadge status={workflow.status} />
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">Case: {getCaseId(workflow.state) ?? "Not available"}</p>
        </CardContent>
      </Card>
    </Link>
  );
}
