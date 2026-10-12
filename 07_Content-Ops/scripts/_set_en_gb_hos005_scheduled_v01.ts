/**
 * Set defaultLanguage (+ keep/set defaultAudioLanguage) to en-GB on HOS 005
 * scheduled Nov Shorts + Short B. Does not touch privacy/publishAt.
 */
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const IDS = [
  "Pp5LmjsduI4", // 3 Nov
  "JyRjM-9Yc8g", // 1 Nov
  "x_3L_IdYgEc", // 15 Nov
  "1lszTrYRp-8", // 30 Oct
  "mTY67qet7cM", // Short B keeper
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
  if (!tok.access_token) throw new Error(JSON.stringify(tok).slice(0, 240));
  const auth = { Authorization: `Bearer ${tok.access_token}` };

  const ch = await fetch("https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true", {
    headers: auth,
  }).then((r) => r.json());
  if (ch.items?.[0]?.id !== HOS) throw new Error(`wrong channel ${ch.items?.[0]?.id}`);
  console.log("CHANNEL_OK", ch.items[0].snippet.title, ch.items[0].id);

  for (const id of IDS) {
    const cur = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${id}`, {
      headers: auth,
    }).then((r) => r.json());
    const sn = cur.items?.[0]?.snippet;
    const st = cur.items?.[0]?.status;
    if (!sn) {
      console.log(JSON.stringify({ id, error: "missing" }));
      continue;
    }
    if (sn.channelId !== HOS) {
      console.log(JSON.stringify({ id, error: "wrong_channel", channelId: sn.channelId }));
      continue;
    }
    const before = {
      lang: sn.defaultLanguage || null,
      audio: sn.defaultAudioLanguage || null,
      privacy: st?.privacyStatus,
      publishAt: st?.publishAt || null,
      title: sn.title,
    };
    if (before.lang === "en-GB" && before.audio === "en-GB") {
      console.log(JSON.stringify({ id, skipped: "already_en_GB", before }));
      continue;
    }
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
      headers: { ...auth, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const uj = await upd.json();
    if (!upd.ok) {
      console.log(JSON.stringify({ id, error: upd.status, body: uj }));
      continue;
    }
    // verify
    const got = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${id}`, {
      headers: auth,
    }).then((r) => r.json());
    const a = got.items?.[0];
    console.log(
      JSON.stringify({
        id,
        updated: true,
        before,
        after: {
          lang: a?.snippet?.defaultLanguage || null,
          audio: a?.snippet?.defaultAudioLanguage || null,
          privacy: a?.status?.privacyStatus,
          publishAt: a?.status?.publishAt || null,
          title: a?.snippet?.title,
        },
      }),
    );
  }
  await prisma.$disconnect();
}
main().catch(async (e) => {
  console.error(e);
  await prisma.$disconnect();
  process.exit(1);
});
