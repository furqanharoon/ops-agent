"use client";

import { useState } from "react";
import { Check, XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Spinner } from "@/components/ui/spinner";
import { Textarea } from "@/components/ui/textarea";
import { useResumeWorkflow } from "@/hooks/use-workflows";
import { getApiErrorMessage } from "@/lib/api";

export function ApprovalDialog({ threadId }: { threadId: string }) {
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState("");
  const resume = useResumeWorkflow();

  const approve = () => {
    resume.mutate({ thread_id: threadId, approval_status: "approved" });
  };

  const reject = () => {
    resume.mutate(
      { thread_id: threadId, approval_status: "rejected", rejection_reason: reason },
      {
        onSuccess: () => {
          setOpen(false);
          setReason("");
        }
      }
    );
  };

  return (
    <div className="rounded-lg border border-amber-400/30 bg-amber-400/10 p-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-sm font-semibold text-amber-100">Human Approval Required</h2>
          <p className="mt-1 text-sm text-amber-200/80">Review the analysis before allowing this workflow to generate a report.</p>
        </div>
        <div className="flex gap-2">
          <Button disabled={resume.isPending} onClick={approve}>
            {resume.isPending ? <Spinner /> : <Check className="h-4 w-4" />}
            Approve
          </Button>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button variant="outline" disabled={resume.isPending}>
                <XCircle className="h-4 w-4" />
                Reject
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Reject Workflow</DialogTitle>
                <DialogDescription>Provide the reason this workflow needs manual review.</DialogDescription>
              </DialogHeader>
              <Textarea value={reason} onChange={(event) => setReason(event.target.value)} placeholder="Reason" />
              <DialogFooter>
                <Button variant="outline" onClick={() => setOpen(false)}>
                  Cancel
                </Button>
                <Button variant="destructive" disabled={resume.isPending || reason.trim().length === 0} onClick={reject}>
                  {resume.isPending ? <Spinner /> : null}
                  Submit
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>
      {resume.isError ? <p className="mt-3 text-sm text-red-200">{getApiErrorMessage(resume.error)}</p> : null}
    </div>
  );
}
