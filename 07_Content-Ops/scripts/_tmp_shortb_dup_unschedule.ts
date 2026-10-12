import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";

async function token(): Promise<string> {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn?.refreshTokenEncrypted) throw new Error("no HOS connection");
  const tr = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID || "",
      client_secret: env.GOOGLE_CLIENT_SECRET || "",
      refresh_token: decryptSecret(conn.refreshTokenEncrypted),
      grant_type: "refresh_token",
    }),
  });
  const j = await tr.json();
  if (!j.access_token) throw new Error("token fail " + JSON.stringify(j));
  return j.access_token as string;
}

async function yt(access: string, path: string, init?: RequestInit) {
  const r = await fetch(`https://www.googleapis.com/youtube/v3/${path}`, {
    ...init,
    headers: { Authorization: `Bearer ${access}`, ...(init?.headers || {}) },
  });
  const text = await r.text();
  let json: any;
  try { json = JSON.parse(text); } catch { json = { raw: text }; }
  return { ok: r.ok, status: r.status, json };
}

async function main() {
  const access = await token();
  const get = await yt(access, "videos?part=snippet,status&id=KIWJRl0dzjw,mTY67qet7cM");
  for (const it of get.json.items || []) {
    console.log("NOW", it.id, JSON.stringify({ title: it.snippet.title, privacy: it.status.privacyStatus, publishAt: it.status.publishAt || null, kids: it.status.selfDeclaredMadeForKids }));
  }
  const dup = (get.json.items || []).find((i: any) => i.id === "KIWJRl0dzjw");
  if (!dup) throw new Error("dup missing");

  // Ensure title has (duplicate)
  let title = dup.snippet.title || "";
  if (!/\(duplicate\)/i.test(title)) {
    title = title + " (duplicate)";
    const updT = await yt(access, "videos?part=snippet", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: "KIWJRl0dzjw",
        snippet: {
          title,
          categoryId: dup.snippet.categoryId,
          description: dup.snippet.description || "",
          tags: dup.snippet.tags,
          defaultLanguage: dup.snippet.defaultLanguage,
          defaultAudioLanguage: dup.snippet.defaultAudioLanguage,
        },
      }),
    });
    console.log("RETITLE2", updT.status, updT.json?.error ? JSON.stringify(updT.json.error) : title);
  }

  // Clear schedule: private without publishAt. YouTube API: omit publishAt and set private.
  // To remove publishAt must set privacyStatus private and not include publishAt — but PUT replaces status fields carefully.
  // Per YouTube API: setting privacyStatus to private without publishAt clears the schedule.
  const upd = await yt(access, "videos?part=status", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: "KIWJRl0dzjw",
      status: {
        privacyStatus: "private",
        selfDeclaredMadeForKids: false,
      },
    }),
  });
  console.log("UNSCHED", upd.status, upd.json?.error ? JSON.stringify(upd.json.error) : JSON.stringify({ privacy: upd.json?.status?.privacyStatus, publishAt: upd.json?.status?.publishAt || null }));

  const after = await yt(access, "videos?part=snippet,status&id=KIWJRl0dzjw,mTY67qet7cM");
  for (const it of after.json.items || []) {
    console.log("AFTER", it.id, it.snippet.title, it.status.privacyStatus, it.status.publishAt || "NO_SCHED", "kids="+it.status.selfDeclaredMadeForKids);
  }
  await prisma.$disconnect();
}
main().catch(async (e) => { console.error(e); await prisma.$disconnect(); process.exit(1); });
