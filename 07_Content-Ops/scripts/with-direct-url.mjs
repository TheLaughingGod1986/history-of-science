#!/usr/bin/env node
/**
 * Ensure DIRECT_URL is set before Prisma CLI runs.
 *
 * Prisma schema keeps `directUrl = env("DIRECT_URL")` for Neon/pooler setups.
 * On Vercel, DATABASE_URL is often set alone; without this helper, `prisma generate`
 * and `prisma migrate deploy` fail with P1012 (DIRECT_URL not found).
 *
 * If DIRECT_URL is unset and DATABASE_URL is present, default DIRECT_URL=DATABASE_URL.
 * Does not invent a database URL when DATABASE_URL is also missing.
 *
 * Usage: node scripts/with-direct-url.mjs <command> [args...]
 */
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const binDir = path.join(root, "node_modules", ".bin");
const pathSep = path.delimiter;

if (!process.env.DIRECT_URL && process.env.DATABASE_URL) {
  process.env.DIRECT_URL = process.env.DATABASE_URL;
  console.log(
    "[with-direct-url] DIRECT_URL unset; defaulting to DATABASE_URL for Prisma",
  );
}

const [command, ...args] = process.argv.slice(2);
if (!command) {
  console.error("usage: node scripts/with-direct-url.mjs <command> [args...]");
  process.exit(1);
}

const env = {
  ...process.env,
  PATH: `${binDir}${pathSep}${process.env.PATH || ""}`,
};

const result = spawnSync(command, args, {
  stdio: "inherit",
  env,
  cwd: root,
  shell: false,
});

if (result.error) {
  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status === null ? 1 : result.status);
