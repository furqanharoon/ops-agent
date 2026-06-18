import { Server } from "lucide-react";

export function Navbar() {
  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-background/80 px-4 backdrop-blur md:px-6">
      <div>
        <p className="text-sm font-medium text-foreground">AI workflow orchestration</p>
        <p className="text-xs text-muted-foreground">Incident investigation runs and approval gates</p>
      </div>
      <div className="flex items-center gap-2 rounded-md border border-emerald-400/25 bg-emerald-400/10 px-2.5 py-1.5 text-xs text-emerald-200">
        <Server className="h-3.5 w-3.5" />
        FastAPI
      </div>
    </header>
  );
}
