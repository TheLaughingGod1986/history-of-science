#!/usr/bin/env tsx
/**
 * Diagnose YouTube growth metrics JSON (array of YouTubeGrowthMetrics).
 *
 * Usage:
 *   npm run diagnose:youtube -- --file metrics.json
 */
import fs from "fs";
import path from "path";
import {
  diagnoseCatalog,
  summarizeGrowthDashboard,
  type YouTubeGrowthMetrics,
} from "../src/lib/analytics/youtube-growth";

function argValue(flag: string): string | undefined {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function main() {
  const file = argValue("--file") || argValue("-f");
  if (!file) {
    console.error("Usage: npm run diagnose:youtube -- --file <metrics.json>");
    process.exit(2);
  }
  const abs = path.resolve(file);
  const raw = JSON.parse(fs.readFileSync(abs, "utf8")) as YouTubeGrowthMetrics[];
  const summary = summarizeGrowthDashboard(raw);
  const { recommendations, leaders } = diagnoseCatalog(raw);
  console.log(JSON.stringify({ summary, leaders, recommendations }, null, 2));
}

main();
