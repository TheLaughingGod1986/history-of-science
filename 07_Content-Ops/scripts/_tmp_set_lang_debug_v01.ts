import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const id = "Pp5LmjsduI4";

async function main() {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  const tok = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID!,
      client_secret: env.GOOGLE_CLIENT_SECRET!,
      refresh_token: decryptSecret(conn!.refreshTokenEncrypted!),
      grant_type: "refresh_token",
    }),
  }).then((r) => r.json());
  const auth = { Authorization: `Bearer ${tok.access_token}` };
  const info = await fetch(`https://oauth2.googleapis.com/tokeninfo?access_token=${tok.access_token}`).then(r=>r.json());
  console.log("SCOPES", info.scope);

  const cur = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,status,localizations&id=${id}`, { headers: auth }).then(r=>r.json());
  console.log("BEFORE", JSON.stringify(cur.items?.[0]?.snippet, null, 2).slice(0,800));
  console.log("LOCS", JSON.stringify(cur.items?.[0]?.localizations));

  const sn = cur.items[0].snippet;
  // Attempt 1: full snippet write with defaultLanguage
  const body = {
    id,
    snippet: {
      title: sn.title,
      description: sn.description ?? "",
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
  console.log("PUT", upd.status, JSON.stringify({ lang: uj.snippet?.defaultLanguage, audio: uj.snippet?.defaultAudioLanguage, err: uj.error }, null, 2));

  const after = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${id}`, { headers: auth }).then(r=>r.json());
  console.log("AFTER", JSON.stringify({
    lang: after.items?.[0]?.snippet?.defaultLanguage,
    audio: after.items?.[0]?.snippet?.defaultAudioLanguage,
    keys: Object.keys(after.items?.[0]?.snippet||{}),
  }));

  // Compare with working Short B
  const b = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet&id=mTY67qet7cM`, { headers: auth }).then(r=>r.json());
  console.log("SHORT_B", JSON.stringify({
    lang: b.items?.[0]?.snippet?.defaultLanguage,
    audio: b.items?.[0]?.snippet?.defaultAudioLanguage,
    keys: Object.keys(b.items?.[0]?.snippet||{}),
  }));
  await prisma.$disconnect();
}
main().catch(async e=>{console.error(e); await prisma.$disconnect(); process.exit(1);});
