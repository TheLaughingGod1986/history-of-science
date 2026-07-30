export type MetricLike = {
  views?: number | null;
  likes?: number | null;
  comments?: number | null;
  shares?: number | null;
  saves?: number | null;
  subscribersGained?: number | null;
  followersGained?: number | null;
  completionRate?: number | null;
  averageWatchTime?: number | null;
};

export function engagementRate(m: MetricLike): number | null {
  const views = m.views ?? 0;
  if (!views) return null;
  const eng = (m.likes ?? 0) + (m.comments ?? 0) + (m.shares ?? 0) + (m.saves ?? 0);
  return eng / views;
}

export function viewsPerFollower(views: number | null | undefined, followers: number): number | null {
  if (!views || !followers) return null;
  return views / followers;
}

export function perThousand(numerator: number | null | undefined, views: number | null | undefined): number | null {
  if (numerator == null || !views) return null;
  return (numerator / views) * 1000;
}

export type InsightRow = {
  platform?: string | null;
  topic?: string | null;
  hookCategory?: string | null;
  durationSeconds?: number | null;
  scheduledHour?: number | null;
  scheduledDay?: string | null;
  metrics: MetricLike;
};

export type GeneratedInsight = {
  type: string;
  topic?: string;
  platform?: string;
  finding: string;
  evidence: string;
  confidence: number;
  recommendedAction: string;
  sampleSize: number;
};

const MIN_SAMPLES = 5;

export function generateInsights(rows: InsightRow[]): {
  insights: GeneratedInsight[];
  lowDataMessage?: string;
} {
  if (rows.length < MIN_SAMPLES) {
    return {
      insights: [],
      lowDataMessage:
        "More performance data is needed before this recommendation is reliable.",
    };
  }

  const insights: GeneratedInsight[] = [];

  // Hook category completion
  const byHook = group(rows.filter((r) => r.hookCategory), (r) => r.hookCategory!);
  const hookStats = Object.entries(byHook)
    .map(([hook, list]) => ({
      hook,
      n: list.length,
      avgCompletion: avg(list.map((r) => r.metrics.completionRate)),
    }))
    .filter((h) => h.n >= 3 && h.avgCompletion != null)
    .sort((a, b) => (b.avgCompletion ?? 0) - (a.avgCompletion ?? 0));

    if (hookStats.length >= 2 && hookStats[0].avgCompletion != null && hookStats[1].avgCompletion != null) {
    const best = hookStats[0];
    const bestCompletion = best.avgCompletion as number;
    const restAvg =
      hookStats.slice(1).reduce((s, h) => s + (h.avgCompletion ?? 0), 0) /
      (hookStats.length - 1);
    if (restAvg > 0) {
      const lift = ((bestCompletion - restAvg) / restAvg) * 100;
      if (lift >= 10) {
        insights.push({
          type: "hook_performance",
          finding: `${labelHook(best.hook)} hooks are generating ${Math.round(lift)}% higher completion rates.`,
          evidence: `Based on ${best.n} posts vs other categories (n=${rows.length}).`,
          confidence: Math.min(0.9, 0.5 + best.n * 0.05),
          recommendedAction: `Prioritise ${labelHook(best.hook)} openings in the next Shorts cluster.`,
          sampleSize: best.n,
        });
      }
    }
  }

  // Duration buckets
  const mid = rows.filter(
    (r) => (r.durationSeconds ?? 0) >= 31 && (r.durationSeconds ?? 0) <= 42,
  );
  const other = rows.filter(
    (r) =>
      r.durationSeconds != null &&
      ((r.durationSeconds ?? 0) < 31 || (r.durationSeconds ?? 0) > 42),
  );
  if (mid.length >= 3 && other.length >= 3) {
    const midEng = avg(mid.map((r) => engagementRate(r.metrics)));
    const otherEng = avg(other.map((r) => engagementRate(r.metrics)));
    if (midEng != null && otherEng != null && otherEng > 0 && midEng > otherEng) {
      insights.push({
        type: "duration",
        finding: "Clips between 31 and 42 seconds outperform longer or shorter clips.",
        evidence: `Engagement ${midEng.toFixed(3)} (n=${mid.length}) vs ${otherEng.toFixed(3)} (n=${other.length}).`,
        confidence: 0.6,
        recommendedAction: "Target 31–42s when trimming approved clips.",
        sampleSize: mid.length + other.length,
      });
    }
  }

  // Platform hour
  const byPlatformHour = group(
    rows.filter((r) => r.platform && r.scheduledHour != null),
    (r) => `${r.platform}|${r.scheduledHour}`,
  );
  const hourStats = Object.entries(byPlatformHour)
    .map(([key, list]) => {
      const [platform, hour] = key.split("|");
      return {
        platform,
        hour: Number(hour),
        n: list.length,
        eng: avg(list.map((r) => engagementRate(r.metrics))),
      };
    })
    .filter((h) => h.n >= 3 && h.eng != null)
    .sort((a, b) => (b.eng ?? 0) - (a.eng ?? 0));

  if (hourStats[0]) {
    const best = hourStats[0];
    insights.push({
      type: "posting_time",
      platform: best.platform,
      finding: `${best.platform} posts around ${best.hour}:00 show the strongest engagement in the current dataset.`,
      evidence: `n=${best.n}, avg engagement ${(best.eng ?? 0).toFixed(3)}.`,
      confidence: Math.min(0.85, 0.45 + best.n * 0.05),
      recommendedAction: "Bias the next schedule block toward this hour window.",
      sampleSize: best.n,
    });
  }

  if (!insights.length) {
    return {
      insights: [],
      lowDataMessage:
        "More performance data is needed before this recommendation is reliable.",
    };
  }

  return { insights };
}

function group<T>(items: T[], keyFn: (t: T) => string): Record<string, T[]> {
  return items.reduce<Record<string, T[]>>((acc, item) => {
    const k = keyFn(item);
    (acc[k] ||= []).push(item);
    return acc;
  }, {});
}

function avg(nums: (number | null | undefined)[]): number | null {
  const vals = nums.filter((n): n is number => n != null && !Number.isNaN(n));
  if (!vals.length) return null;
  return vals.reduce((a, b) => a + b, 0) / vals.length;
}

function labelHook(hook: string): string {
  return hook.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}
