/**
 * Build NEXT_EPISODE_BRIEF.md from YouTube growth diagnostics.
 */

import {
  diagnoseCatalog,
  summarizeGrowthDashboard,
  type GrowthRecommendation,
  type YouTubeGrowthMetrics,
} from "./youtube-growth";

export type NextEpisodeBrief = {
  generatedAt: string;
  summary: ReturnType<typeof summarizeGrowthDashboard>;
  priorities: GrowthRecommendation[];
  leaders: ReturnType<typeof diagnoseCatalog>["leaders"];
  markdown: string;
};

const PRIORITY_ORDER: GrowthRecommendation["category"][] = [
  "weak_opening",
  "runtime",
  "retention_drop",
  "poor_title",
  "weak_thumbnail",
  "needs_update",
  "traffic_mix",
  "funnel",
];

function categoryRank(c: GrowthRecommendation["category"]): number {
  const i = PRIORITY_ORDER.indexOf(c);
  return i === -1 ? 99 : i;
}

export function buildNextEpisodeBrief(
  videos: YouTubeGrowthMetrics[],
  opts?: { nextTopicHint?: string },
): NextEpisodeBrief {
  const summary = summarizeGrowthDashboard(videos);
  const { recommendations, leaders } = diagnoseCatalog(videos);
  const priorities = [...recommendations]
    .filter((r) => r.category !== "top_performer")
    .sort((a, b) => categoryRank(a.category) - categoryRank(b.category) || b.confidence - a.confidence)
    .slice(0, 8);

  const generatedAt = new Date().toISOString();
  const topicLine = opts?.nextTopicHint
    ? `**Candidate next topic:** ${opts.nextTopicHint}`
    : "**Candidate next topic:** _(fill from TOPIC_OPPORTUNITY_SCORE / ideas backlog)_";

  const md = [
    "# Next episode brief — Growth System v2",
    "",
    `Generated: ${generatedAt}`,
    "",
    topicLine,
    "",
    "## Channel snapshot (imported metrics)",
    "",
    `| Metric | Value |`,
    `|---|---|`,
    `| Videos in sample | ${summary.videoCount} |`,
    `| Impressions | ${summary.impressions} |`,
    `| Views | ${summary.views} |`,
    `| Avg CTR | ${summary.avgCtr != null ? summary.avgCtr.toFixed(2) + "%" : "—"} |`,
    `| Avg APV | ${summary.avgApv != null ? summary.avgApv.toFixed(1) + "%" : "—"} |`,
    `| Avg AVD (s) | ${summary.avgAvdSeconds != null ? summary.avgAvdSeconds.toFixed(0) : "—"} |`,
    `| Subs gained | ${summary.subscribersGained} |`,
    `| Returning / new | ${summary.returningViewers} / ${summary.newViewers} |`,
    "",
    "## Priorities for the next build",
    "",
    "Apply these before writing the next cold open / packaging:",
    "",
    ...priorities.map(
      (p, i) =>
        `${i + 1}. **[${p.category}]** ${p.finding}\n   - Action: ${p.recommendedAction}`,
    ),
    priorities.length ? "" : "_No critical flags — still run Growth System v2 gate._",
    "",
    "## What is working (keep)",
    "",
    leaders.topHooks.length
      ? `- Top hooks: ${leaders.topHooks.map((h) => `${h.hook} (APV ${h.avgApv.toFixed(1)}%)`).join("; ")}`
      : "- Top hooks: _(need more labelled Shorts)_",
    leaders.topTopics.length
      ? `- Top topics: ${leaders.topTopics.map((t) => `${t.topic} (CTR ${t.avgCtr.toFixed(2)}%)`).join("; ")}`
      : "- Top topics: _(need more data)_",
    leaders.topShorts.length
      ? `- Top Shorts: ${leaders.topShorts.map((s) => `${s.title} (${s.apv.toFixed(1)}% APV)`).join("; ")}`
      : "- Top Shorts: _(need more data)_",
    "",
    "## Next episode locked defaults",
    "",
    "- Runtime **8–12 min** · cold open 5s / 15s / 30s",
    "- Orbit **experiences** the science · 4–6 acts",
    "- CG: **Gemini Veo** · VO: **ElevenLabs** Ben Orbit Narrator",
    "- 3–5 Shorts · curiosity-gap ends · Related → long",
    "- Thumbs ABC + social mirror schedule after YouTube lock",
    "",
    "## Gate before VO / Veo",
    "",
    "```bash",
    "cd 07_Content-Ops",
    "npm run gate:episode -- --project ../02_Video-Projects/<NNN_Slug>",
    "```",
    "",
  ].join("\n");

  return { generatedAt, summary, priorities, leaders, markdown: md };
}
