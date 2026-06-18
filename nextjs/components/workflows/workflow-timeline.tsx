import { CheckCircle2, Circle, CircleDot } from "lucide-react";
import { cn } from "@/lib/utils";
import type { WorkflowState } from "@/types/workflow";

export interface TimelineStep {
  id: string;
  label: string;
  complete?: boolean;
  active?: boolean;
}

export function buildWorkflowSteps(state?: WorkflowState | null): TimelineStep[] {
  const hasFacts = Boolean(state?.facts);
  const hasAnalysis = Boolean(state?.analysis);
  const needsApproval = Boolean(state?.__interrupt__?.length || state?.approval_status);
  const hasApprovalDecision = Boolean(state?.approval_status);
  const hasReport = Boolean(state?.report);
  const rejected = state?.approval_status === "rejected";

  return [
    { id: "facts", label: "Facts", complete: hasFacts, active: !hasFacts },
    { id: "analysis", label: "Analysis", complete: hasAnalysis, active: hasFacts && !hasAnalysis },
    ...(needsApproval
      ? [
          {
            id: "approval",
            label: "Approval",
            complete: hasApprovalDecision,
            active: hasAnalysis && !hasApprovalDecision
          }
        ]
      : []),
    {
      id: rejected ? "manual_review" : "report",
      label: rejected ? "Manual Review" : "Report",
      complete: hasReport || rejected,
      active: hasAnalysis && !hasReport && (!needsApproval || hasApprovalDecision)
    }
  ];
}

export function WorkflowTimeline({ steps }: { steps: TimelineStep[] }) {
  return (
    <ol className="space-y-4">
      {steps.map((step, index) => {
        const Icon = step.complete ? CheckCircle2 : step.active ? CircleDot : Circle;
        return (
          <li key={step.id} className="flex gap-3">
            <div className="flex flex-col items-center">
              <Icon
                className={cn(
                  "h-5 w-5",
                  step.complete ? "text-emerald-300" : step.active ? "text-sky-300" : "text-muted-foreground"
                )}
              />
              {index < steps.length - 1 ? <div className="mt-2 h-7 w-px bg-border" /> : null}
            </div>
            <div>
              <p className={cn("text-sm font-medium", step.active && "text-sky-200")}>{step.label}</p>
              <p className="text-xs text-muted-foreground">{step.complete ? "Complete" : step.active ? "Current step" : "Pending"}</p>
            </div>
          </li>
        );
      })}
    </ol>
  );
}
