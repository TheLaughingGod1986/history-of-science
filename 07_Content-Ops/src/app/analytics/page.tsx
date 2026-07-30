import { prisma } from "@/lib/storage/prisma";
import { engagementRate, generateInsights, perThousand } from "@/lib/analytics/insights";
import { AnalyticsImportForm } from "@/components/AnalyticsImportForm";
import { PLATFORMS } from "@/config/platforms";

export const dynamic = "force-dynamic";

export default async function AnalyticsPage() {
  const posts = await prisma.platformPost.findMany({
    include: {
      metrics: { orderBy: { recordedAt: "desc" }, take: 1 },
      shortClip: { include: { longFormVideo: true } },
    },
  });

  const rows = posts
    .filter((p) => p.metrics[0])
    .map((p) => {
      const m = p.metrics[0];
      return {
        platform: p.platform,
        topic: p.shortClip.longFormVideo.topic,
        hookCategory: p.shortClip.hookCategory,
        durationSeconds: p.shortClip.targetDurationSeconds,
        scheduledHour: p.scheduledAt ? p.scheduledAt.getHours() : null,
        scheduledDay: p.scheduledAt
          ? p.scheduledAt.toLocaleDateString("en-GB", { weekday: "long", timeZone: "Europe/London" })
          : null,
        metrics: m,
        title: p.shortClip.workingTitle,
      };
    });

  const { insights, lowDataMessage } = generateInsights(
    rows.map((r) => ({
      platform: r.platform,
      topic: r.topic,
      hookCategory: r.hookCategory,
      durationSeconds: r.durationSeconds,
      scheduledHour: r.scheduledHour,
      scheduledDay: r.scheduledDay,
      metrics: r.metrics,
    })),
  );

  const byPlatform = Object.keys(PLATFORMS).map((platform) => {
    const list = rows.filter((r) => r.platform === platform);
    const views = list.reduce((s, r) => s + (r.metrics.views ?? 0), 0);
    const eng = list
      .map((r) => engagementRate(r.metrics))
      .filter((n): n is number => n != null);
    const avgEng = eng.length ? eng.reduce((a, b) => a + b, 0) / eng.length : null;
    const subs = list.reduce((s, r) => s + (r.metrics.subscribersGained ?? 0), 0);
    return { platform, views, avgEng, subs, n: list.length };
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-[family-name:var(--font-orbit-display)] text-3xl">Performance</h1>
        <p className="mt-2 text-[#F5E8D2]/60">
          Compare platforms, hooks, topics and posting times. Import CSV analytics for v1.
        </p>
      </div>

      <AnalyticsImportForm />

      <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {byPlatform.map((p) => (
          <div key={p.platform} className="card-panel p-4">
            <div
              className="text-xs uppercase tracking-[0.14em]"
              style={{ color: PLATFORMS[p.platform as keyof typeof PLATFORMS].color }}
            >
              {PLATFORMS[p.platform as keyof typeof PLATFORMS].label}
            </div>
            <div className="mt-3 text-2xl">{p.views} views</div>
            <div className="mt-1 text-sm text-[#F5E8D2]/55">
              n={p.n} · eng {p.avgEng != null ? (p.avgEng * 100).toFixed(1) + "%" : "—"} · subs{" "}
              {p.subs}
            </div>
          </div>
        ))}
      </section>

      <section className="card-panel p-5">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Recommendations</h2>
        {lowDataMessage ? (
          <p className="mt-4 rounded-xl border border-[#FFC85A]/30 bg-[#FFC85A]/10 px-4 py-3 text-sm text-[#FFC85A]">
            {lowDataMessage}
          </p>
        ) : null}
        <ul className="mt-4 space-y-3">
          {insights.map((insight) => (
            <li key={insight.finding} className="rounded-xl bg-white/3 p-4 text-sm">
              <div className="text-[#F5E8D2]">{insight.finding}</div>
              <div className="mt-1 text-[#F5E8D2]/50">{insight.evidence}</div>
              <div className="mt-2 text-[#FF7A24]">{insight.recommendedAction}</div>
            </li>
          ))}
        </ul>
      </section>

      <section className="card-panel overflow-x-auto p-5">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Clip comparison</h2>
        <table className="mt-4 w-full min-w-[720px] text-left text-sm">
          <thead className="text-xs uppercase tracking-[0.12em] text-[#5A6E82]">
            <tr>
              <th className="pb-2">Clip</th>
              <th className="pb-2">Platform</th>
              <th className="pb-2">Hook</th>
              <th className="pb-2">Views</th>
              <th className="pb-2">Engagement</th>
              <th className="pb-2">Subs/1k</th>
              <th className="pb-2">Completion</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={`${r.title}-${r.platform}-${i}`} className="border-t border-white/5">
                <td className="py-2">{r.title}</td>
                <td className="py-2">{r.platform}</td>
                <td className="py-2">{r.hookCategory}</td>
                <td className="py-2">{r.metrics.views ?? "—"}</td>
                <td className="py-2">
                  {engagementRate(r.metrics) != null
                    ? `${((engagementRate(r.metrics) as number) * 100).toFixed(1)}%`
                    : "—"}
                </td>
                <td className="py-2">
                  {perThousand(r.metrics.subscribersGained, r.metrics.views)?.toFixed(2) ?? "—"}
                </td>
                <td className="py-2">
                  {r.metrics.completionRate != null ? `${r.metrics.completionRate}%` : "—"}
                </td>
              </tr>
            ))}
            {!rows.length ? (
              <tr>
                <td colSpan={7} className="py-6 text-[#F5E8D2]/50">
                  No metrics imported yet.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </section>
    </div>
  );
}
