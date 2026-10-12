import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const IDS = ["mTY67qet7cM", "KIWJRl0dzjw", "wwcjcFfC-5M", "0IfXGSX7Ypw"];

async function main() {
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
  const { access_token } = await tr.json();
  const ch = await (await fetch("https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true", { headers: { Authorization: `Bearer ${access_token}` } })).json();
  if (ch.items?.[0]?.id !== HOS) throw new Error("wrong channel");
  console.log("CHANNEL_OK", ch.items[0].snippet.title);

  // Re-set schedule with fuller status (keep embeddable true like house)
  for (const id of ["mTY67qet7cM"]) {
    const cur = await (await fetch(`https://www.googleapis.com/youtube/v3/videos?part=status&id=${id}`, { headers: { Authorization: `Bearer ${access_token}` } })).json();
    console.log("CUR", JSON.stringify(cur.items?.[0]?.status, null, 2));
    const status = {
      ...(cur.items?.[0]?.status || {}),
      privacyStatus: "private",
      publishAt: "2026-11-08T11:30:00.000Z",
      selfDeclaredMadeForKids: false,
      embeddable: true,
      publicStatsViewable: true,
      license: "youtube",
    };
    // remove fields API rejects on update
    delete (status as any).uploadStatus;
    delete (status as any).rejectionReason;
    delete (status as any).publishAt; // set explicitly below
    const body = { id, status: { ...status, publishAt: "2026-11-08T11:30:00.000Z", privacyStatus: "private", selfDeclaredMadeForKids: false } };
    const upd = await fetch("https://www.googleapis.com/youtube/v3/videos?part=status", {
      method: "PUT",
      headers: { Authorization: `Bearer ${access_token}`, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const uj = await upd.json();
    console.log("UPD", upd.status, JSON.stringify(uj.status || uj, null, 2));
  }

  await new Promise((r) => setTimeout(r, 2000));
  const got = await (await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${IDS.join(",")}`, { headers: { Authorization: `Bearer ${access_token}` } })).json();
  for (const it of got.items || []) {
    console.log(JSON.stringify({
      id: it.id,
      title: it.snippet.title.slice(0, 50),
      privacy: it.status.privacyStatus,
      publishAt: it.status.publishAt || null,
      kids: it.status.selfDeclaredMadeForKids,
      upload: it.status.uploadStatus,
    }));
  }
  await prisma.$disconnect();
}
main().catch(async (e) => { console.error(e); await prisma.$disconnect(); process.exit(1); });
