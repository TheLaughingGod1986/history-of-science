import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import fs from "fs";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const SHORT_B = "mTY67qet7cM";
const PUBLISH_AT = "2026-11-08T11:30:00.000Z";

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
  const ch = await yt(access, "channels?part=id,snippet&mine=true");
  const channel = ch.json.items?.[0];
  console.log("CHANNEL", channel?.id, channel?.snippet?.title, channel?.snippet?.customUrl);
  if (channel?.id !== HOS) throw new Error("WRONG CHANNEL " + channel?.id);

  const s = await yt(access, "search?part=snippet&forMine=true&type=video&maxResults=25&q=" + encodeURIComponent("One Tight Band"));
  console.log("SEARCH", JSON.stringify((s.json.items||[]).map((i:any)=>({id:i.id?.videoId,title:i.snippet?.title,pub:i.snippet?.publishedAt})),null,2));

  const ids = new Set<string>([SHORT_B, "wwcjcFfC-5M", "0IfXGSX7Ypw"]);
  for (const it of s.json.items||[]) if (it.id?.videoId) ids.add(it.id.videoId);

  const list = await yt(access, `videos?part=snippet,status,contentDetails&id=${[...ids].join(",")}`);
  for (const it of list.json.items||[]) {
    console.log("BEFORE", JSON.stringify({
      id: it.id,
      title: it.snippet?.title,
      privacy: it.status?.privacyStatus,
      publishAt: it.status?.publishAt||null,
      uploadStatus: it.status?.uploadStatus,
      madeForKids: it.status?.selfDeclaredMadeForKids,
      duration: it.contentDetails?.duration,
    }));
  }

  const upd = await yt(access, "videos?part=status", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: SHORT_B,
      status: {
        privacyStatus: "private",
        publishAt: PUBLISH_AT,
        selfDeclaredMadeForKids: false,
      },
    }),
  });
  console.log("UPDATE", upd.status, JSON.stringify(upd.json, null, 2).slice(0, 2500));

  const after = await yt(access, `videos?part=snippet,status&id=${SHORT_B}`);
  const a = after.json.items?.[0];
  console.log("AFTER", JSON.stringify({
    id: a?.id,
    title: a?.snippet?.title,
    privacy: a?.status?.privacyStatus,
    publishAt: a?.status?.publishAt||null,
    uploadStatus: a?.status?.uploadStatus,
    madeForKids: a?.status?.selfDeclaredMadeForKids,
  }, null, 2));

  const outPath = "/Users/benjaminoats/YouTube/hos-005-blood/02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/11_Upload-Package/Schedule/evidence_2026-10-03_short_b/SHORT_B_API_SCHEDULE.json";
  fs.mkdirSync(outPath.replace(/\/[^/]+$/, ""), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify({
    at: new Date().toISOString(),
    channel: { id: channel.id, title: channel.snippet.title },
    search: s.json.items,
    updateStatus: upd.status,
    update: upd.json,
    after: a,
  }, null, 2));
  console.log("WROTE", outPath);
  await prisma.$disconnect();
}
main().catch(async (e) => { console.error(e); await prisma.$disconnect(); process.exit(1); });
