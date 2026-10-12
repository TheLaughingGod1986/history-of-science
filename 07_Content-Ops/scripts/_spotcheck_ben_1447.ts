import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";

async function main() {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn?.refreshTokenEncrypted) throw new Error("no token");
  const refresh = decryptSecret(conn.refreshTokenEncrypted);
  const tok = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID!,
      client_secret: env.GOOGLE_CLIENT_SECRET!,
      refresh_token: refresh,
      grant_type: "refresh_token",
    }),
  }).then((r) => r.json());
  const ids = [
    "clV6E10NLPw",
    "_C92tIJCk8A",
    "29bpGAI0wb8",
    "CUu8k38iAMc",
    "GHZDsiH7L7A",
    "frP_YrNShsU",
    "AL_-qlWko_g",
    "TbMMJSRKC3U",
  ];
  const got = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${ids.join(",")}`,
    { headers: { Authorization: `Bearer ${tok.access_token}` } },
  ).then((r) => r.json());
  for (const it of got.items || []) {
    console.log(
      JSON.stringify({
        id: it.id,
        title: it.snippet.title.slice(0, 40),
        lang: it.snippet.defaultLanguage,
        audio: it.snippet.defaultAudioLanguage,
        cat: it.snippet.categoryId,
        tags: it.snippet.tags,
        privacy: it.status.privacyStatus,
        publishAt: it.status.publishAt || null,
      }),
    );
  }
  await prisma.$disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
