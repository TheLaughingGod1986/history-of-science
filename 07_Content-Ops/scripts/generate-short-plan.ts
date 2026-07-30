#!/usr/bin/env tsx
import fs from "fs";
import path from "path";
import { generateShortPlan } from "../src/lib/content/generate-short-plan";

const scriptPath =
  process.argv[2] ||
  path.resolve(
    __dirname,
    "../../02_Video-Projects/001_Will-We-Ever-Meet-Aliens/01_Script/aliens_script_master_v01.md",
  );
const title = process.argv[3] || "Will We Ever Meet Aliens?";

if (!fs.existsSync(scriptPath)) {
  console.error("Script not found:", scriptPath);
  process.exit(1);
}

const script = fs.readFileSync(scriptPath, "utf8");
const plan = generateShortPlan({ title, script });
if (plan.errors.length) {
  console.error(plan.errors.join("\n"));
  process.exit(1);
}
console.log(JSON.stringify(plan, null, 2));
