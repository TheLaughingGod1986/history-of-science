import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const IDS = ["mTY67qet7cM", "KIWJRl0dzjw"];

async function main() {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn?.refreshTokenEncrypted) throw new Error("no token");
  const tok = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID!,
      client_secret: env.GOOGLE_CLIENT_SECRET!,
      refresh_token: decryptSecret(conn.refreshTokenEncrypted),
      grant_type: "refresh_token",
    }),
  }).then((r) => r.json());
  const ch = await fetch("https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true", {
    headers: { Authorization: `Bearer ${tok.access_token}` },
  }).then((r) => r.json());
  if (ch.items?.[0]?.id !== HOS) throw new Error("wrong channel");
  console.log("CHANNEL_OK", ch.items[0].snippet.title);

  for (const id of IDS) {
    const cur = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${id}`, {
      headers: { Authorization: `Bearer ${tok.access_token}` },
    }).then((r) => r.json());
    const sn = cur.items?.[0]?.snippet;
    const st = cur.items?.[0]?.status;
    if (!sn) { console.log("MISSING", id); continue; }
    const body = {
      id,
      snippet: {
        title: sn.title,
        description: sn.description,
        categoryId: sn.categoryId || "27",
        tags: sn.tags || [],
        defaultLanguage: "en-GB",
        defaultAudioLanguage: "en-GB",
      },
    };
    const upd = await fetch("https://www.googleapis.com/youtube/v3/videos?part=snippet", {
      method: "PUT",
      headers: { Authorization: `Bearer ${tok.access_token}`, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const uj = await upd.json();
    console.log(id, upd.status, {
      lang: uj.snippet?.defaultLanguage,
      audio: uj.snippet?.defaultAudioLanguage,
      privacy: st?.privacyStatus,
      publishAt: st?.publishAt || null,
    });
  }
  // re-check status not wiped
  const got = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${IDS.join(",")}`, {
    headers: { Authorization: `Bearer ${tok.access_token}` },
  }).then((r) => r.json());
  for (const it of got.items || []) {
    console.log("AFTER", JSON.stringify({
      id: it.id,
      lang: it.snippet.defaultLanguage,
      audio: it.snippet.defaultAudioLanguage,
      privacy: it.status.privacyStatus,
      publishAt: it.status.publishAt || null,
    }));
  }
  await prisma.$disconnect();
}
main().catch(async (e) => { console.error(e); await prisma.$disconnect(); process.exit(1); });
