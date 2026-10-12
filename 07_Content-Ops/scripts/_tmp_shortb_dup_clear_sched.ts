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

async function main() {
  const access = await token();
  const auth = { Authorization: `Bearer ${access}`, "Content-Type": "application/json" };
  const attempts = [
    { privacyStatus: "private", selfDeclaredMadeForKids: false, publishAt: null as any },
    { privacyStatus: "private", selfDeclaredMadeForKids: false, publishAt: "" },
    { privacyStatus: "unlisted", selfDeclaredMadeForKids: false },
  ];
  for (const status of attempts) {
    const res = await fetch("https://www.googleapis.com/youtube/v3/videos?part=status", {
      method: "PUT",
      headers: auth,
      body: JSON.stringify({ id: "KIWJRl0dzjw", status }),
    });
    const text = await res.text();
    console.log("try", res.status, JSON.stringify(status), text.slice(0, 280).replace(/\n/g, " "));
    if (!res.ok) continue;
    const after = await (await fetch("https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id=KIWJRl0dzjw", { headers: { Authorization: `Bearer ${access}` } })).json();
    const it = after.items?.[0];
    console.log("after", it?.status?.privacyStatus, it?.status?.publishAt || "CLEARED", it?.snippet?.title);
    if (!it?.status?.publishAt) {
      if (it.status.privacyStatus !== "private") {
        const back = await fetch("https://www.googleapis.com/youtube/v3/videos?part=status", {
          method: "PUT",
          headers: auth,
          body: JSON.stringify({ id: "KIWJRl0dzjw", status: { privacyStatus: "private", selfDeclaredMadeForKids: false } }),
        });
        console.log("back", back.status, (await back.text()).slice(0, 200).replace(/\n/g, " "));
        const after2 = await (await fetch("https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id=KIWJRl0dzjw", { headers: { Authorization: `Bearer ${access}` } })).json();
        console.log("final", after2.items?.[0]?.status?.privacyStatus, after2.items?.[0]?.status?.publishAt || "CLEARED", after2.items?.[0]?.snippet?.title);
      }
      await prisma.$disconnect();
      return;
    }
  }
  console.log("FAIL still scheduled");
  await prisma.$disconnect();
  process.exit(2);
}
main().catch(async (e) => { console.error(e); await prisma.$disconnect(); process.exit(1); });
