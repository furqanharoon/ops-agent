import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { KeyValueList } from "@/components/workflows/key-value-list";
import type { Analysis } from "@/types/workflow";

export function AnalysisCard({ analysis }: { analysis?: Analysis | null }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <KeyValueList data={analysis} />
      </CardContent>
    </Card>
  );
}
