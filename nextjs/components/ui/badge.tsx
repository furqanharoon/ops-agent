import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva("inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium", {
  variants: {
    variant: {
      default: "border-transparent bg-primary text-primary-foreground",
      secondary: "border-transparent bg-muted text-muted-foreground",
      outline: "text-foreground",
      success: "border-emerald-400/30 bg-emerald-400/12 text-emerald-200",
      warning: "border-amber-400/30 bg-amber-400/12 text-amber-200",
      danger: "border-red-400/35 bg-red-400/12 text-red-200",
      info: "border-sky-400/30 bg-sky-400/12 text-sky-200"
    }
  },
  defaultVariants: {
    variant: "default"
  }
});

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement>, VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}
