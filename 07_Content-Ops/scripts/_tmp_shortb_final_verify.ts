import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
async function main() {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  const tr = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID || "",
      client_secret: env.GOOGLE_CLIENT_SECRET || "",
      refresh_token: decryptSecret(conn!.refreshTokenEncrypted!),
      grant_type: "refresh_token",
    }),
  });
  const j = await tr.json();
  const access = j.access_token as string;
  const r = await fetch(
    "https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails,fileDetails&id=mTY67qet7cM,KIWJRl0dzjw,wwcjcFfC-5M",
    { headers: { Authorization: "Bearer " + access } },
  );
  const data = await r.json();
  for (const it of data.items || []) {
    console.log(
      JSON.stringify({
        id: it.id,
        title: it.snippet.title,
        privacy: it.status.privacyStatus,
        publishAt: it.status.publishAt || null,
        kids: it.status.selfDeclaredMadeForKids,
        file: it.fileDetails?.fileName,
        dur: it.contentDetails?.duration,
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
