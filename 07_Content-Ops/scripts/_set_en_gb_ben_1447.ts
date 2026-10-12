/**
 * Set defaultLanguage + defaultAudioLanguage to en-GB on every listed video.
 * Keeps title, description, tags, category. Does not touch status/visibility.
 */
import fs from "fs";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret, encryptSecret } from "../src/lib/security/token-crypto";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const IDS: string[] = JSON.parse(
  fs.readFileSync(
    "/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/hos_full_inventory.json",
    "utf8",
  ),
).videos.map((v: { id: string }) => v.id);

async function accessToken(): Promise<string> {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn?.refreshTokenEncrypted) throw new Error("no token");
  const refreshToken = decryptSecret(conn.refreshTokenEncrypted);
  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID!,
      client_secret: env.GOOGLE_CLIENT_SECRET!,
      refresh_token: refreshToken,
      grant_type: "refresh_token",
    }),
  });
  const body = await res.json();
  if (!res.ok || !body.access_token) throw new Error(JSON.stringify(body).slice(0, 240));
  await prisma.platformConnection.update({
    where: { id: conn.id },
    data: {
      accessTokenEncrypted: encryptSecret(body.access_token),
      accessTokenExpiresAt: new Date(Date.now() + Number(body.expires_in || 3600) * 1000),
      lastRefreshAt: new Date(),
    },
  });
  return body.access_token as string;
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

async function main() {
  const token = await accessToken();
  const ch = await yt(token, "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true");
  if (ch.items?.[0]?.id !== HOS) throw new Error(`wrong channel ${ch.items?.[0]?.id}`);
  const results: unknown[] = [];
  for (const id of IDS) {
    const got = await yt(token, `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${id}`);
    const item = got.items?.[0];
    if (!item) {
      results.push({ id, error: "not_found" });
      continue;
    }
    if (item.snippet.channelId !== HOS) {
      results.push({ id, error: "wrong_channel" });
      continue;
    }
    const before = {
      lang: item.snippet.defaultLanguage,
      audio: item.snippet.defaultAudioLanguage,
      privacy: item.status.privacyStatus,
      publishAt: item.status.publishAt || null,
      title: item.snippet.title,
    };
    if (before.lang === "en-GB" && before.audio === "en-GB") {
      results.push({ id, skipped: "already_en_GB", before });
      console.log(JSON.stringify({ id, skipped: "already_en_GB" }));
      continue;
    }
    const snippet = {
      title: item.snippet.title,
      description: item.snippet.description,
      tags: item.snippet.tags,
      categoryId: item.snippet.categoryId,
      defaultLanguage: "en-GB",
      defaultAudioLanguage: "en-GB",
    };
    await yt(token, "https://www.googleapis.com/youtube/v3/videos?part=snippet", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, snippet }),
    });
    const after = await yt(token, `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${id}`);
    const a = after.items?.[0];
    const row = {
      id,
      updated: true,
      before,
      after: {
        lang: a?.snippet?.defaultLanguage,
        audio: a?.snippet?.defaultAudioLanguage,
        privacy: a?.status?.privacyStatus,
        publishAt: a?.status?.publishAt || null,
        tags: a?.snippet?.tags,
      },
    };
    results.push(row);
    console.log(JSON.stringify({ id, lang: row.after.lang, audio: row.after.audio, privacy: row.after.privacy }));
  }
  const out =
    "/Users/benjaminoats/.local/share/cursor-mac-mini-hos-worker/artifacts/BEN_1447_whole_channel/EN_GB_RESULT.json";
  fs.writeFileSync(out, JSON.stringify({ at: new Date().toISOString(), results }, null, 2) + "\n");
  console.log(JSON.stringify({ wrote: out, n: results.length }));
  await prisma.$disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
