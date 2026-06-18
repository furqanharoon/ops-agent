import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function ReportCard({ report }: { report?: string | null }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Generated Report</CardTitle>
      </CardHeader>
      <CardContent>
        {report ? (
          <pre className="whitespace-pre-wrap rounded-md border border-border bg-background/45 p-4 text-sm leading-6 text-foreground">{report}</pre>
        ) : (
          <p className="text-sm text-muted-foreground">No report has been generated yet.</p>
        )}
      </CardContent>
    </Card>
  );
}
