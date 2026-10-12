import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const IDS = [
  "Pp5LmjsduI4","JyRjM-9Yc8g","x_3L_IdYgEc","1lszTrYRp-8","mTY67qet7cM","KIWJRl0dzjw",
  "K0TQHg4XCHY","JI2ewIT1KSM","6btaax7wp2E","DdggTdAzk84","VZsUxmzGyyE",
];

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
  if (!tok.access_token) throw new Error(JSON.stringify(tok).slice(0,200));
  const ch = await fetch("https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true", {
    headers: { Authorization: `Bearer ${tok.access_token}` },
  }).then((r) => r.json());
  console.log("CHANNEL", ch.items?.[0]?.id, ch.items?.[0]?.snippet?.title);
  if (ch.items?.[0]?.id !== HOS) throw new Error("wrong channel");
  const got = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${IDS.join(",")}`,
    { headers: { Authorization: `Bearer ${tok.access_token}` } },
  ).then((r) => r.json());
  for (const it of got.items || []) {
    console.log(JSON.stringify({
      id: it.id,
      title: it.snippet.title,
      lang: it.snippet.defaultLanguage || null,
      audio: it.snippet.defaultAudioLanguage || null,
      privacy: it.status.privacyStatus,
      publishAt: it.status.publishAt || null,
      channelId: it.snippet.channelId,
    }));
  }
  await prisma.$disconnect();
}
main().catch(async (e) => { console.error(e); await prisma.$disconnect(); process.exit(1); });
