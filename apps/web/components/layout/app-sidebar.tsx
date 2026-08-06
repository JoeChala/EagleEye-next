import Link from "next/link";

import { APP_NAME } from "@/lib/utils/constants";

const navigation = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/students", label: "Students" },
  { href: "/attendance", label: "Attendance" },
  { href: "/reports", label: "Reports" },
  { href: "/settings", label: "Settings" },
];

export function AppSidebar() {
  return (
    <aside className="flex h-full w-64 flex-col border-r bg-background px-4 py-6">
      <div className="mb-8">
        <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">App</p>
        <h2 className="mt-2 text-xl font-semibold">{APP_NAME}</h2>
      </div>

      <nav className="space-y-1">
        {navigation.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="block rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}

