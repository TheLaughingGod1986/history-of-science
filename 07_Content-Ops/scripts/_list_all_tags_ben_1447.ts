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
  const search = await fetch(
    "https://www.googleapis.com/youtube/v3/search?part=id&forMine=true&type=video&maxResults=50",
    { headers: { Authorization: `Bearer ${tok.access_token}` } },
  ).then((r) => r.json());
  const ids = (search.items || []).map((i: { id: { videoId: string } }) => i.id.videoId);
  // also include known privates that search may miss
  for (const extra of ["CUu8k38iAMc", "kzDiVk4603s", "clV6E10NLPw", "TbMMJSRKC3U", "29bpGAI0wb8", "GHZDsiH7L7A"]) {
    if (!ids.includes(extra)) ids.push(extra);
  }
  const out: { id: string; n: number; title: string; tags: string[]; ok: boolean }[] = [];
  for (let i = 0; i < ids.length; i += 50) {
    const chunk = ids.slice(i, i + 50);
    const got = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${chunk.join(",")}`,
      { headers: { Authorization: `Bearer ${tok.access_token}` } },
    ).then((r) => r.json());
    for (const it of got.items || []) {
      if (it.snippet.channelId !== "UCXp7HkBIl1LgaznXuZHJyRg") continue;
      const tags: string[] = it.snippet.tags || [];
      const n = tags.length;
      out.push({
        id: it.id,
        n,
        title: (it.snippet.title || "").slice(0, 55),
        tags,
        ok: n >= 5 && n <= 8,
      });
    }
  }
  out.sort((a, b) => Number(a.ok) - Number(b.ok) || a.n - b.n);
  for (const r of out) {
    console.log(`${r.ok ? "OK" : "OUT"} n=${r.n} ${r.id} ${r.title} | ${JSON.stringify(r.tags)}`);
  }
  console.log(JSON.stringify({ total: out.length, outside: out.filter((r) => !r.ok).map((r) => r.id) }));
  await prisma.$disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
