import Link from "next/link";

const NAV = [
  { href: "/", label: "Overview" },
  { href: "/pipeline", label: "Pipeline" },
  { href: "/videos", label: "Long-form" },
  { href: "/calendar", label: "Calendar" },
  { href: "/analytics", label: "Analytics" },
  { href: "/affiliate", label: "Affiliate" },
  { href: "/settings/connections", label: "Connections" },
  { href: "/settings", label: "Settings" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b border-white/5 bg-[#0a0c12]/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4">
          <Link href="/" className="group flex items-baseline gap-3">
            <span className="font-[family-name:var(--font-orbit-display)] text-2xl tracking-tight text-[#F5E8D2]">
              ORBIT
            </span>
            <span className="text-xs uppercase tracking-[0.22em] text-[#FF7A24]">
              Content Ops
            </span>
          </Link>
          <nav className="flex flex-wrap items-center gap-1 text-sm text-[#F5E8D2]/75">
            {NAV.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-full px-3 py-1.5 transition hover:bg-white/5 hover:text-[#F5E8D2]"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-6 py-8">{children}</main>
    </div>
  );
}
