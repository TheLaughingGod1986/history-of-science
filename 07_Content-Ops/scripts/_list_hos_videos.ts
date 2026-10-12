import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import fs from "fs";
import path from "path";

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
  const ch = await (
    await fetch("https://www.googleapis.com/youtube/v3/channels?part=id,snippet,contentDetails&mine=true", {
      headers: { Authorization: `Bearer ${access_token}` },
    })
  ).json();
  const channel = ch.items?.[0];
  if (channel?.id !== "UCXp7HkBIl1LgaznXuZHJyRg") {
    throw new Error(`wrong channel ${channel?.id}`);
  }
  const up = channel.contentDetails.relatedPlaylists.uploads;
  const ids: string[] = [];
  let page = "";
  do {
    const pl = await (
      await fetch(
        `https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=${up}${page ? `&pageToken=${page}` : ""}`,
        { headers: { Authorization: `Bearer ${access_token}` } },
      )
    ).json();
    ids.push(...pl.items.map((i: { contentDetails: { videoId: string } }) => i.contentDetails.videoId));
    page = pl.nextPageToken || "";
  } while (page);
  const items: unknown[] = [];
  for (let i = 0; i < ids.length; i += 50) {
    const v = await (
      await fetch(
        `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${ids.slice(i, i + 50).join(",")}`,
        { headers: { Authorization: `Bearer ${access_token}` } },
      )
    ).json();
    items.push(...(v.items || []));
  }
  const out = { channelId: channel.id, handle: channel.snippet?.customUrl, title: channel.snippet?.title, videos: items };
  const dest = path.join(
    process.env.HOME || "",
    ".local/share/cursor-mac-mini-hos-worker/artifacts/hos_full_inventory.json",
  );
  fs.writeFileSync(dest, JSON.stringify(out, null, 2));
  console.log("CHANNEL", channel.id, channel.snippet?.customUrl, channel.snippet?.title);
  console.log("TOTAL", items.length);
  console.log("WROTE", dest);
  await prisma.$disconnect();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
