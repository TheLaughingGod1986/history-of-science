#!/usr/bin/env tsx
/**
 * Review a long-form (or Short) script against Growth System v2.
 *
 * Usage:
 *   npm run review:script -- --file ../02_Video-Projects/.../script.md
 *   npm run review:script -- --file script.md --json
 */
import fs from "fs";
import path from "path";
import {
  formatReviewMarkdown,
  reviewScript,
  PASS_THRESHOLD,
} from "../src/lib/analytics/script-reviewer";

function argValue(flag: string): string | undefined {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function main() {
  const file = argValue("--file") || argValue("-f");
  if (!file) {
    console.error("Usage: npm run review:script -- --file <script.md> [--json]");
    process.exit(2);
  }
  const abs = path.resolve(file);
  if (!fs.existsSync(abs)) {
    console.error(`File not found: ${abs}`);
    process.exit(2);
  }
  const text = fs.readFileSync(abs, "utf8");
  const result = reviewScript(text);
  const asJson = process.argv.includes("--json");

  if (asJson) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(formatReviewMarkdown(result, path.basename(abs)));
    console.log(`Pass threshold: ${PASS_THRESHOLD}`);
  }

  process.exit(result.passed ? 0 : 1);
}

main();
