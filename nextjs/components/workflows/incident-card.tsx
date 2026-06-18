import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { KeyValueList } from "@/components/workflows/key-value-list";
import type { Incident } from "@/types/workflow";

export function IncidentCard({ incident }: { incident?: Incident | null }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Incident</CardTitle>
      </CardHeader>
      <CardContent>
        <KeyValueList data={incident} />
      </CardContent>
    </Card>
  );
}
