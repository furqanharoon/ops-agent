import { toDisplayValue } from "@/lib/workflow-utils";
import { toTitleCase } from "@/lib/utils";

export function KeyValueList({ data }: { data?: object | null }) {
  if (!data || Object.keys(data).length === 0) {
    return <p className="text-sm text-muted-foreground">No data available yet.</p>;
  }

  return (
    <dl className="grid gap-3 sm:grid-cols-2">
      {Object.entries(data).map(([key, value]) => (
        <div key={key} className="rounded-md border border-border bg-background/35 px-3 py-2">
          <dt className="text-xs font-medium text-muted-foreground">{toTitleCase(key)}</dt>
          <dd className="mt-1 whitespace-pre-wrap break-words text-sm">{toDisplayValue(value)}</dd>
        </div>
      ))}
    </dl>
  );
}
