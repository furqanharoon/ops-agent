import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function EvaluationsPage() {
  return (
    <div className="mx-auto max-w-6xl">
      <Card>
        <CardHeader>
          <CardTitle>Evaluations</CardTitle>
          <CardDescription>Evaluation run history can be connected here when an API endpoint is available.</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">No evaluation endpoint is exposed by the backend yet.</p>
        </CardContent>
      </Card>
    </div>
  );
}
