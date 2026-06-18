import { Badge } from "@/components/ui/badge";
import type { WorkflowStatus } from "@/types/workflow";

const labels: Record<WorkflowStatus, string> = {
  running: "Running",
  waiting_approval: "Waiting Approval",
  completed: "Completed",
  manual_review: "Manual Review",
  rejected: "Rejected",
  approved: "Approved",
  unknown: "Unknown"
};

export function StatusBadge({ status }: { status: WorkflowStatus }) {
  const variant =
    status === "completed" || status === "approved"
      ? "success"
      : status === "waiting_approval" || status === "manual_review"
        ? "warning"
        : status === "rejected"
          ? "danger"
          : status === "running"
            ? "info"
            : "secondary";

  return <Badge variant={variant}>{labels[status]}</Badge>;
}
