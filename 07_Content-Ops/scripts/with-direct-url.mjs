#!/usr/bin/env node
/**
 * Ensure DIRECT_URL is set before Prisma CLI runs.
 *
 * Prisma schema keeps `directUrl = env("DIRECT_URL")` for Neon/pooler setups.
 * On Vercel, DATABASE_URL is often set alone. Without this helper,
 * `prisma migrate deploy` fails with P1012 (DIRECT_URL not found).
 *
 * Also handles the case where Prisma loads DATABASE_URL from a dotenv file
 * that Node does not auto-load: we read .env*, default DIRECT_URL, write it
 * back into `.env`, then spawn Prisma with an updated env.
 *
 * Usage: node scripts/with-direct-url.mjs <command> [args...]
 */
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const binDir = path.join(root, "node_modules", ".bin");
const pathSep = path.delimiter;
const envFiles = [".env", ".env.production", ".env.local", "prisma/.env"];

/** Non-empty string, or undefined. */
function nonEmpty(value) {
  if (typeof value !== "string") return undefined;
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

function readFileSafe(filePath) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return "";
  }
}

function parseEnvValue(content, key) {
  const re = new RegExp(
    `^\\s*${key}\\s*=\\s*(?:["']([^"']*)["']|([^#\\r\\n]*))`,
    "m",
  );
  const match = content.match(re);
  if (!match) return undefined;
  return nonEmpty(match[1] ?? match[2] ?? "");
}

function readFromEnvFiles(key) {
  for (const relative of envFiles) {
    const value = parseEnvValue(readFileSafe(path.join(root, relative)), key);
    if (value) return value;
  }
  return undefined;
}

function ensureDirectUrlInDotEnv(directUrl) {
  const envPath = path.join(root, ".env");
  const existing = readFileSafe(envPath);
  if (parseEnvValue(existing, "DIRECT_URL")) return;

  const prefix =
    existing.length === 0 || existing.endsWith("\n") ? "" : "\n";
  fs.appendFileSync(
    envPath,
    `${prefix}DIRECT_URL=${JSON.stringify(directUrl)}\n`,
  );
  console.log(
    "[with-direct-url] Wrote DIRECT_URL to .env for Prisma dotenv loading",
  );
}

function resolveDatabaseUrl() {
  return (
    nonEmpty(process.env.DATABASE_URL) ||
    nonEmpty(process.env.POSTGRES_PRISMA_URL) ||
    nonEmpty(process.env.POSTGRES_URL) ||
    nonEmpty(process.env.PRISMA_DATABASE_URL) ||
    readFromEnvFiles("DATABASE_URL") ||
    readFromEnvFiles("POSTGRES_PRISMA_URL") ||
    readFromEnvFiles("POSTGRES_URL")
  );
}

function resolveDirectUrl() {
  return (
    nonEmpty(process.env.DIRECT_URL) ||
    nonEmpty(process.env.POSTGRES_URL_NON_POOLING) ||
    nonEmpty(process.env.DATABASE_URL_UNPOOLED) ||
    readFromEnvFiles("DIRECT_URL") ||
    readFromEnvFiles("POSTGRES_URL_NON_POOLING")
  );
}

const urlKeys = Object.keys(process.env)
  .filter((key) => /DATABASE|DIRECT|POSTGRES|PRISMA.*URL/i.test(key))
  .sort();

console.log(
  `[with-direct-url] probe hasDATABASE_URL=${typeof process.env.DATABASE_URL === "string"} len=${process.env.DATABASE_URL?.length ?? "n/a"} hasDIRECT_URL=${typeof process.env.DIRECT_URL === "string"} len=${process.env.DIRECT_URL?.length ?? "n/a"} urlKeys=${urlKeys.join(",") || "(none)"}`,
);

const databaseUrl = resolveDatabaseUrl();
let directUrl = resolveDirectUrl();

if (!directUrl && databaseUrl) {
  directUrl = databaseUrl;
  console.log(
    "[with-direct-url] DIRECT_URL unset; defaulting to DATABASE_URL for Prisma",
  );
} else if (!databaseUrl) {
  console.log(
    "[with-direct-url] No non-empty DATABASE_URL (or alias) in process.env/.env* — Prisma may fail",
  );
} else {
  console.log("[with-direct-url] DIRECT_URL already present");
}

if (databaseUrl) process.env.DATABASE_URL = databaseUrl;
if (directUrl) {
  process.env.DIRECT_URL = directUrl;
  ensureDirectUrlInDotEnv(directUrl);
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

const prismaBin = path.join(binDir, "prisma");
const executable =
  command === "prisma" && fs.existsSync(prismaBin) ? prismaBin : command;

const result = spawnSync(executable, args, {
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
