import Link from "next/link";
import { Activity, BarChart3, GitBranch, LayoutDashboard, Settings } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/workflows", label: "Workflows", icon: GitBranch },
  { href: "/evaluations", label: "Evaluations", icon: BarChart3 },
  { href: "/settings", label: "Settings", icon: Settings }
];

export function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 border-r border-border bg-[#0b111b] md:block">
      <div className="flex h-14 items-center gap-2 border-b border-border px-5">
        <div className="flex h-8 w-8 items-center justify-center rounded-md border border-sky-400/25 bg-sky-400/10">
          <Activity className="h-4 w-4 text-sky-300" />
        </div>
        <div>
          <span className="block text-sm font-semibold">Ops-Agent</span>
          <span className="block text-[11px] text-muted-foreground">Workflow console</span>
        </div>
      </div>
      <nav className="space-y-1 p-3">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground",
              item.href === "/" && "border border-sky-400/20 bg-sky-400/10 text-sky-100"
            )}
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
