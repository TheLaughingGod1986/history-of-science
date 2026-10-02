#!/usr/bin/env tsx
/**
 * Replace tags only on listed YouTube ids.
 * Reads the live snippet first and sends it back with new tags, so
 * title, description, category and languages stay as they are. Does not
 * send status, so privacy and publishAt stay untouched.
 *
 * Input: { "retag": [{ id, tags }] }
 *
 *   npx tsx --env-file=.env scripts/retag-videos.ts --file <fixes.json> --dry-run
 *   npx tsx --env-file=.env scripts/retag-videos.ts --file <fixes.json>
 */
import fs from "fs";
import path from "path";

type RetagRow = {
  id: string;
  tags: string[];
};

const WRITABLE_SNIPPET_KEYS = [
  "title",
  "description",
  "categoryId",
  "defaultLanguage",
  "defaultAudioLanguage",
] as const;

function arg(name: string): string | undefined {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

async function accessToken(): Promise<string> {
  // Shared helper: retries an "expired" row that still has a refresh token, and explains invalid_grant.
  const { youtubeAccessToken } = await import("../src/lib/publishing/youtube-token");
  return youtubeAccessToken();
}

async function yt(token: string, url: string, init?: RequestInit) {
  const res = await fetch(url, {
    ...init,
    headers: { Authorization: `Bearer ${token}`, ...(init?.headers || {}) },
  });
  const body = await res.json();
  if (!res.ok) throw new Error(`${url} ${res.status} ${JSON.stringify(body).slice(0, 400)}`);
  return body;
}

function sameTags(a: string[] | undefined, b: string[]): boolean {
  const aa = (a || []).map((t) => t.toLowerCase()).sort();
  const bb = b.map((t) => t.toLowerCase()).sort();
  return aa.length === bb.length && aa.every((t, i) => t === bb[i]);
}

async function main() {
  const file = arg("file");
  if (!file) {
    console.error("Usage: retag-videos.ts --file <json> [--dry-run]");
    process.exit(1);
  }
  const dry = process.argv.includes("--dry-run");
  const pack = JSON.parse(fs.readFileSync(path.resolve(file), "utf8"));
  const rows: RetagRow[] = pack.retag;
  const token = await accessToken();
  const results: unknown[] = [];

  // Confirm channel is HOS before any write
  const ch = await yt(token, "https://www.googleapis.com/youtube/v3/channels?part=snippet,id&mine=true");
  const channelId = ch.items?.[0]?.id;
  const handle = ch.items?.[0]?.snippet?.customUrl;
  if (channelId !== "UCXp7HkBIl1LgaznXuZHJyRg") {
    throw new Error(`Refuse: token channel is ${channelId} (${handle}), not HOS`);
  }

  for (const row of rows) {
    const got = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(row.id)}`,
    );
    const item = got.items?.[0];
    if (!item) {
      results.push({ id: row.id, error: "not_found" });
      continue;
    }
    if (item.snippet?.channelId && item.snippet.channelId !== "UCXp7HkBIl1LgaznXuZHJyRg") {
      results.push({ id: row.id, error: "wrong_channel", channelId: item.snippet.channelId });
      continue;
    }
    const beforeTags: string[] = item.snippet?.tags || [];
    const before = {
      title: item.snippet?.title,
      tags: beforeTags,
      privacy: item.status?.privacyStatus,
      publishAt: item.status?.publishAt || null,
    };
    if (sameTags(beforeTags, row.tags)) {
      results.push({ id: row.id, skipped: "already_tagged", before });
      console.log(JSON.stringify({ id: row.id, skipped: "already_tagged" }));
      continue;
    }
    const snippet: Record<string, unknown> = { tags: row.tags };
    for (const key of WRITABLE_SNIPPET_KEYS) {
      if (item.snippet?.[key] !== undefined) snippet[key] = item.snippet[key];
    }
    if (dry) {
      results.push({ id: row.id, dryRun: true, before, nextTags: row.tags });
      console.log(JSON.stringify({ id: row.id, from: beforeTags, to: row.tags, dryRun: true }));
      continue;
    }
    await yt(token, "https://www.googleapis.com/youtube/v3/videos?part=snippet", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: row.id, snippet }),
    });
    const after = await yt(
      token,
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${encodeURIComponent(row.id)}`,
    );
    const a = after.items?.[0];
    results.push({
      id: row.id,
      updated: true,
      before,
      after: {
        title: a?.snippet?.title,
        tags: a?.snippet?.tags || [],
        privacy: a?.status?.privacyStatus,
        publishAt: a?.status?.publishAt || null,
      },
    });
    console.log(JSON.stringify({ id: row.id, tags: a?.snippet?.tags || [], publishAt: a?.status?.publishAt || null }));
  }

  const out = path.resolve(file.replace(/\.json$/, "") + "_RESULT.json");
  fs.writeFileSync(
    out,
    JSON.stringify({ dry, channelId, handle, finishedAt: new Date().toISOString(), results }, null, 2) + "\n",
  );
  console.log(JSON.stringify({ wrote: out, n: results.length, dry }, null, 2));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
