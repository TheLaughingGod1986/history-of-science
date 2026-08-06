/**
 * Orbit Growth System v2 — YouTube analytics diagnostics & recommendations.
 */

import type { GeneratedInsight } from "@/lib/analytics/insights";

export type YouTubeGrowthMetrics = {
  title?: string | null;
  topic?: string | null;
  hookCategory?: string | null;
  isShort?: boolean | null;
  durationSeconds?: number | null;
  views?: number | null;
  impressions?: number | null;
  ctr?: number | null; // 0–100
  averageViewDurationSeconds?: number | null;
  averagePercentageViewed?: number | null;
  retention30s?: number | null; // 0–100
  retentionDropAtSeconds?: number | null;
  retentionDropDepth?: number | null; // % points lost
  returningViewers?: number | null;
  newViewers?: number | null;
  subscribersGained?: number | null;
  browsePercent?: number | null;
  suggestedPercent?: number | null;
  searchPercent?: number | null;
  endScreenCtr?: number | null;
  cardsCtr?: number | null;
  averageSessionSeconds?: number | null;
};

export type GrowthRecommendation = GeneratedInsight & {
  videoTitle?: string;
  category:
    | "weak_opening"
    | "retention_drop"
    | "poor_title"
    | "weak_thumbnail"
    | "needs_update"
    | "traffic_mix"
    | "funnel"
    | "top_performer"
    | "runtime";
};

const TARGETS = {
  ctrMin: 4,
  retention30Min: 60,
  apvLongMin: 35,
  apvShortMin: 70,
  browseSuggestedMin: 25,
  endScreenCtrMin: 2,
};

export function computeCtr(impressions?: number | null, views?: number | null): number | null {
  if (!impressions || impressions <= 0 || views == null) return null;
  return (views / impressions) * 100;
}

export function diagnoseVideo(m: YouTubeGrowthMetrics): GrowthRecommendation[] {
  const out: GrowthRecommendation[] = [];
  const title = m.title ?? "Untitled";
  const ctr = m.ctr ?? computeCtr(m.impressions, m.views);
  const apv = m.averagePercentageViewed;
  const isShort = Boolean(m.isShort);

  if (m.retention30s != null && m.retention30s < TARGETS.retention30Min) {
    out.push({
      type: "weak_opening",
      category: "weak_opening",
      videoTitle: title,
      topic: m.topic ?? undefined,
      finding: `${title}: weak opening — 30s retention ${m.retention30s.toFixed(1)}% (target ≥${TARGETS.retention30Min}%).`,
      evidence: `Cold-open clock failed or explanation-before-story.`,
      confidence: 0.8,
      recommendedAction:
        "Rewrite cold open: curiosity by 5s, stakes by 15s, journey by 30s. Cut definition/history opens. Put Orbit in danger/experience immediately.",
      sampleSize: 1,
    });
  }

  if (
    m.retentionDropAtSeconds != null &&
    m.retentionDropDepth != null &&
    m.retentionDropDepth >= 8
  ) {
    out.push({
      type: "retention_drop",
      category: "retention_drop",
      videoTitle: title,
      finding: `${title}: retention drop ~${m.retentionDropDepth.toFixed(0)} pts near ${Math.round(m.retentionDropAtSeconds)}s.`,
      evidence: `Curve cliff at ${m.retentionDropAtSeconds}s.`,
      confidence: 0.75,
      recommendedAction:
        "Insert curiosity reset (new question / Orbit beat / number) before that timestamp. Avoid explain-dumps without story motion.",
      sampleSize: 1,
    });
  }

  if (ctr != null && m.impressions != null && m.impressions >= 500 && ctr < TARGETS.ctrMin) {
    const packaging =
      ctr < 2.5
        ? ({
            category: "weak_thumbnail" as const,
            action:
              "Thumbnail likely underperforming — one object, one emotion, minimal text, same promise as title. Run thumb ABC.",
          })
        : ({
            category: "poor_title" as const,
            action:
              "Title underperforming — one promise, prefer ≤60 chars, no series suffix. Re-test title ABC with vidIQ ≥90.",
          });
    out.push({
      type: packaging.category,
      category: packaging.category,
      videoTitle: title,
      finding: `${title}: CTR ${ctr.toFixed(2)}% on ${m.impressions} impressions (target ≥${TARGETS.ctrMin}%).`,
      evidence: `CTR signal with meaningful impressions.`,
      confidence: 0.7,
      recommendedAction: packaging.action,
      sampleSize: 1,
    });
  }

  const apvFloor = isShort ? TARGETS.apvShortMin : TARGETS.apvLongMin;
  if (apv != null && apv < apvFloor && (m.views ?? 0) >= 100) {
    out.push({
      type: "needs_update",
      category: "needs_update",
      videoTitle: title,
      finding: `${title}: APV ${apv.toFixed(1)}% below ${apvFloor}% floor.`,
      evidence: `Average percentage viewed under target.`,
      confidence: 0.65,
      recommendedAction: isShort
        ? "Tighten to 22–30s, punch-first fact, curiosity-gap ending into Related long."
        : "Consider trim to 8–12 min trust window, strengthen mid-film escalation, ensure Orbit agency every act.",
      sampleSize: 1,
    });
  }

  if (
    !isShort &&
    m.durationSeconds != null &&
    m.durationSeconds > 16 * 60 &&
    apv != null &&
    apv < 40
  ) {
    out.push({
      type: "runtime",
      category: "runtime",
      videoTitle: title,
      finding: `${title}: long runtime (${Math.round(m.durationSeconds / 60)} min) with APV ${apv.toFixed(1)}%.`,
      evidence: `Trust-building window prefers 8–12 min.`,
      confidence: 0.6,
      recommendedAction: "Next videos: target 8–12 min until returning viewers and APV rise.",
      sampleSize: 1,
    });
  }

  const browse = m.browsePercent ?? 0;
  const suggested = m.suggestedPercent ?? 0;
  const search = m.searchPercent ?? 0;
  if ((m.views ?? 0) >= 200 && browse + suggested + search > 0) {
    if (browse + suggested < TARGETS.browseSuggestedMin && search >= 50) {
      out.push({
        type: "traffic_mix",
        category: "traffic_mix",
        videoTitle: title,
        finding: `${title}: Search-heavy traffic (Search ${search.toFixed(0)}% · Browse+Suggested ${(browse + suggested).toFixed(0)}%).`,
        evidence: `Distribution still not recommending broadly.`,
        confidence: 0.55,
        recommendedAction:
          "Improve session bridges (end screen/cards/pin to sibling docs) and Shorts Related funnel; strengthen hook retention so Browse/Suggested can trust the video.",
        sampleSize: 1,
      });
    }
  }

  if (!isShort && (m.endScreenCtr == null || m.endScreenCtr < TARGETS.endScreenCtrMin)) {
    if ((m.views ?? 0) >= 100) {
      out.push({
        type: "funnel",
        category: "funnel",
        videoTitle: title,
        finding: `${title}: end-screen CTR weak or missing.`,
        evidence: m.endScreenCtr != null ? `End screen CTR ${m.endScreenCtr}%` : "No end-screen CTR imported",
        confidence: 0.5,
        recommendedAction:
          "Configure end screen + cards to another Orbit documentary. Never leave a dead end.",
        sampleSize: 1,
      });
    }
  }

  return out;
}

export function diagnoseCatalog(videos: YouTubeGrowthMetrics[]): {
  recommendations: GrowthRecommendation[];
  leaders: {
    topHooks: { hook: string; avgApv: number; n: number }[];
    topTopics: { topic: string; avgCtr: number; n: number }[];
    topShorts: { title: string; apv: number }[];
  };
} {
  const recommendations = videos.flatMap(diagnoseVideo);

  const byHook = new Map<string, number[]>();
  const byTopic = new Map<string, number[]>();
  for (const v of videos) {
    if (v.hookCategory && v.averagePercentageViewed != null) {
      const list = byHook.get(v.hookCategory) || [];
      list.push(v.averagePercentageViewed);
      byHook.set(v.hookCategory, list);
    }
    const ctr = v.ctr ?? computeCtr(v.impressions, v.views);
    if (v.topic && ctr != null) {
      const list = byTopic.get(v.topic) || [];
      list.push(ctr);
      byTopic.set(v.topic, list);
    }
  }

  const avg = (xs: number[]) => xs.reduce((a, b) => a + b, 0) / xs.length;

  const topHooks = [...byHook.entries()]
    .map(([hook, vals]) => ({ hook, avgApv: avg(vals), n: vals.length }))
    .filter((h) => h.n >= 2)
    .sort((a, b) => b.avgApv - a.avgApv)
    .slice(0, 5);

  const topTopics = [...byTopic.entries()]
    .map(([topic, vals]) => ({ topic, avgCtr: avg(vals), n: vals.length }))
    .filter((t) => t.n >= 2)
    .sort((a, b) => b.avgCtr - a.avgCtr)
    .slice(0, 5);

  const topShorts = videos
    .filter((v) => v.isShort && v.averagePercentageViewed != null && v.title)
    .map((v) => ({ title: v.title!, apv: v.averagePercentageViewed! }))
    .sort((a, b) => b.apv - a.apv)
    .slice(0, 5);

  // Highlight leaders as positive insights
  if (topHooks[0]) {
    recommendations.push({
      type: "top_performer",
      category: "top_performer",
      finding: `Top hook category: ${topHooks[0].hook} (avg APV ${topHooks[0].avgApv.toFixed(1)}%, n=${topHooks[0].n}).`,
      evidence: "Cross-video hook comparison",
      confidence: Math.min(0.85, 0.4 + topHooks[0].n * 0.1),
      recommendedAction: `Bias next Shorts cluster toward ${topHooks[0].hook} openings.`,
      sampleSize: topHooks[0].n,
    });
  }

  return { recommendations, leaders: { topHooks, topTopics, topShorts } };
}

export function summarizeGrowthDashboard(videos: YouTubeGrowthMetrics[]) {
  const withImpressions = videos.filter((v) => (v.impressions ?? 0) > 0);
  const ctrs = withImpressions
    .map((v) => v.ctr ?? computeCtr(v.impressions, v.views))
    .filter((n): n is number => n != null);
  const apvs = videos
    .map((v) => v.averagePercentageViewed)
    .filter((n): n is number => n != null);
  const avds = videos
    .map((v) => v.averageViewDurationSeconds)
    .filter((n): n is number => n != null);

  const mean = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);

  return {
    videoCount: videos.length,
    impressions: videos.reduce((s, v) => s + (v.impressions ?? 0), 0),
    views: videos.reduce((s, v) => s + (v.views ?? 0), 0),
    avgCtr: mean(ctrs),
    avgApv: mean(apvs),
    avgAvdSeconds: mean(avds),
    subscribersGained: videos.reduce((s, v) => s + (v.subscribersGained ?? 0), 0),
    returningViewers: videos.reduce((s, v) => s + (v.returningViewers ?? 0), 0),
    newViewers: videos.reduce((s, v) => s + (v.newViewers ?? 0), 0),
  };
}
