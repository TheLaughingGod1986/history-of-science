#!/usr/bin/env tsx
/**
 * Write NEXT_EPISODE_BRIEF.md from YouTube growth metrics JSON.
 *
 * Usage:
 *   npm run brief:next -- --file content/samples/json/youtube_growth_metrics_sample.json
 *   npm run brief:next -- --file metrics.json --out ../docs/NEXT_EPISODE_BRIEF.md --topic "Moon Leaving Us"
 */
import fs from "fs";
import path from "path";
import { buildNextEpisodeBrief } from "../src/lib/analytics/next-episode-brief";
import type { YouTubeGrowthMetrics } from "../src/lib/analytics/youtube-growth";

function argValue(flag: string): string | undefined {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function main() {
  const file = argValue("--file") || argValue("-f");
  if (!file) {
    console.error(
      "Usage: npm run brief:next -- --file <metrics.json> [--out path] [--topic \"hint\"]",
    );
    process.exit(2);
  }
  const abs = path.resolve(file);
  const videos = JSON.parse(fs.readFileSync(abs, "utf8")) as YouTubeGrowthMetrics[];
  const brief = buildNextEpisodeBrief(videos, { nextTopicHint: argValue("--topic") });

  const out =
    argValue("--out") ||
    path.resolve(__dirname, "../../../docs/NEXT_EPISODE_BRIEF.md");
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, brief.markdown);
  console.log(`Wrote ${out}`);
  console.log(`Priorities: ${brief.priorities.length}`);
  for (const p of brief.priorities.slice(0, 5)) {
    console.log(`- [${p.category}] ${p.finding.slice(0, 100)}`);
  }
}

main();
