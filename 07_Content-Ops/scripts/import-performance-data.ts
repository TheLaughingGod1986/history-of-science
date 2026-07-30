#!/usr/bin/env tsx
/**
 * CLI helper: node scripts/import-performance-data.ts <platform> <file.csv>
 * Prefer the dashboard Analytics page for interactive mapping/preview.
 */
import fs from "fs";
import { DEFAULT_MAPPINGS, parseMetricsCsv, previewCsv } from "../src/lib/analytics/csv-import";

const platform = (process.argv[2] || "youtube") as keyof typeof DEFAULT_MAPPINGS;
const file = process.argv[3];
if (!file || !fs.existsSync(file)) {
  console.error("Usage: tsx scripts/import-performance-data.ts <platform> <file.csv>");
  process.exit(1);
}
const csv = fs.readFileSync(file, "utf8");
const mapping = DEFAULT_MAPPINGS[platform] || {};
console.log(JSON.stringify({ preview: previewCsv(csv, mapping), parsed: parseMetricsCsv(csv, mapping) }, null, 2));
