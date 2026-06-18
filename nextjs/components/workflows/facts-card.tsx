import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { KeyValueList } from "@/components/workflows/key-value-list";
import type { Facts } from "@/types/workflow";

export function FactsCard({ facts }: { facts?: Facts | null }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Facts</CardTitle>
      </CardHeader>
      <CardContent>
        <KeyValueList data={facts} />
      </CardContent>
    </Card>
  );
}
