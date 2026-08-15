import Link from "next/link";
import { getAffiliateDashboardSummary } from "@/lib/affiliate/analytics";

export const dynamic = "force-dynamic";

function StatCard({
  label,
  value,
  hint,
}: {
  label: string;
  value: string | number;
  hint?: string;
}) {
  return (
    <div className="card-panel p-5">
      <div className="text-xs uppercase tracking-[0.18em] text-[#5A6E82]">{label}</div>
      <div className="mt-3 font-[family-name:var(--font-orbit-display)] text-3xl text-[#F5E8D2]">
        {value}
      </div>
      {hint ? <div className="mt-2 text-xs text-[#F5E8D2]/45">{hint}</div> : null}
    </div>
  );
}

export default async function AffiliateDashboardPage() {
  const data = await getAffiliateDashboardSummary();
  const warnings: string[] = [];
  if (data.warnings.videosMissingLinks > 0) {
    warnings.push(
      `${data.warnings.videosMissingLinks} published/high-view video(s) still missing affiliate links.`,
    );
  }
  if (data.warnings.inactiveProductInDescriptions > 0) {
    warnings.push(
      `${data.warnings.inactiveProductInDescriptions} inactive product(s) still appear in descriptions.`,
    );
  }
  if (data.warnings.brokenUrls > 0) {
    warnings.push(`${data.warnings.brokenUrls} broken affiliate URL(s) detected.`);
  }
  if (data.warnings.highClickZeroConversions > 0) {
    warnings.push(
      `${data.warnings.highClickZeroConversions} high-click product(s) with zero conversions.`,
    );
  }
  if (data.warnings.programmesNeedingReports > 0) {
    warnings.push(
      `${data.warnings.programmesNeedingReports} active programme(s) still need reporting data.`,
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.28em] text-[#FF7A24]">Monetisation</p>
          <h1 className="mt-2 font-[family-name:var(--font-orbit-display)] text-3xl text-[#F5E8D2]">
            Affiliate
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-[#F5E8D2]/55">
            Relevance before revenue. Only recommend products Orbit would still endorse with no
            commission.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link
            href="/affiliate/products"
            className="rounded-full border border-white/15 px-4 py-2 text-sm"
          >
            Products
          </Link>
          <Link
            href="/affiliate/programs"
            className="rounded-full border border-white/15 px-4 py-2 text-sm"
          >
            Programmes
          </Link>
          <Link
            href="/affiliate/opportunities"
            className="rounded-full bg-[#FF7A24] px-4 py-2 text-sm text-[#0A0C12]"
          >
            Opportunities
          </Link>
          <Link
            href="/affiliate/import"
            className="rounded-full border border-white/15 px-4 py-2 text-sm"
          >
            CSV import
          </Link>
        </div>
      </div>

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Active programmes" value={data.activePrograms} />
        <StatCard label="Active products" value={data.activeProducts} />
        <StatCard label="Videos with links" value={data.videosWithLinks} />
        <StatCard label="Clicks (all time)" value={data.clicksTotal} />
        <StatCard label="Clicks (month)" value={data.clicksMonth} />
        <StatCard label="Est. conversions" value={data.conversionsEstimated} />
        <StatCard
          label="Revenue (month)"
          value={`£${data.revenueMonth.toFixed(2)}`}
        />
        <StatCard
          label="Revenue (all time)"
          value={`£${data.revenueTotal.toFixed(2)}`}
        />
        <StatCard
          label="Top product"
          value={data.highestPerformingProduct || "—"}
        />
        <StatCard
          label="Top affiliate video"
          value={data.highestPerformingVideo || "—"}
        />
      </section>

      <section className="card-panel space-y-4 p-5">
        <div>
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
            Clicks & revenue by source
          </h2>
          <p className="mt-1 text-sm text-[#F5E8D2]/55">
            youtube · threads · instagram · facebook (from /go/ utm_source). Revenue attributed by
            click share per product when CSV conversions have no click id.
          </p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[420px] text-left text-sm">
            <thead>
              <tr className="border-b border-white/10 text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                <th className="py-2 pr-4 font-normal">Source</th>
                <th className="py-2 pr-4 font-normal">Clicks</th>
                <th className="py-2 font-normal">Est. revenue</th>
              </tr>
            </thead>
            <tbody>
              {data.bySource.map((row) => (
                <tr key={row.source} className="border-b border-white/5 text-[#F5E8D2]/85">
                  <td className="py-2.5 pr-4 capitalize">{row.source}</td>
                  <td className="py-2.5 pr-4">{row.clicks}</td>
                  <td className="py-2.5">£{row.revenue.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {warnings.length ? (
        <section className="card-panel space-y-3 p-5">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
            Warnings
          </h2>
          <ul className="space-y-2">
            {warnings.map((w) => (
              <li
                key={w}
                className="rounded-xl border border-[#FFC85A]/25 bg-[#FFC85A]/10 px-4 py-3 text-sm text-[#F5E8D2]"
              >
                {w}
              </li>
            ))}
          </ul>
        </section>
      ) : (
        <section className="card-panel p-5 text-sm text-[#F5E8D2]/55">
          No monetisation warnings right now.
        </section>
      )}
    </div>
  );
}
