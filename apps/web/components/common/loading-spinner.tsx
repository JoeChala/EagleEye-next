import { Loader2 } from "lucide-react";

import { cn } from "@/lib/utils/cn";

type LoadingSpinnerProps = {
  className?: string;
};

export function LoadingSpinner({ className }: LoadingSpinnerProps) {
  return <Loader2 className={cn("h-5 w-5 animate-spin", className)} aria-hidden="true" />;
}

