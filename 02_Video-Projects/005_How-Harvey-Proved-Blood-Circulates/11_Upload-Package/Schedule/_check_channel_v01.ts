/**
 * HOS 005: confirm the uploader's YouTube connection is @HistoryOfScienceYT before upload,
 * and list the channel's playlists. With a video id, also read that video back. Read-only.
 *
 *   cd 07_Content-Ops && npx tsx --env-file=.env \
 *     ../02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/11_Upload-Package/Schedule/_check_channel_v01.ts
 */
import { prisma } from "../../../../07_Content-Ops/src/lib/storage/prisma";
import { decryptSecret } from "../../../../07_Content-Ops/src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../../../../07_Content-Ops/src/lib/publishing/adapters/youtube";

const HOS_ID = "UCXp7HkBIl1LgaznXuZHJyRg";

async function main() {
  let conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn?.accessTokenEncrypted) throw new Error("no connected YouTube account");
  const adapter = new YouTubePublishingAdapter();
  if (conn.accessTokenExpiresAt && conn.accessTokenExpiresAt.getTime() < Date.now() + 60_000) {
    const r = await adapter.refreshConnection!(conn);
    if (!r.ok) throw new Error(`refresh failed: ${r.message}`);
    conn = await prisma.platformConnection.findUnique({ where: { id: conn.id } });
  }
  const token = decryptSecret(conn!.accessTokenEncrypted!);
  const get = async (url: string) => {
    const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
    if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
    return res.json();
  };
  const ch = await get("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true");
  const items = (ch.items || []).map((c: any) => ({
    id: c.id,
    title: c.snippet?.title,
    handle: c.snippet?.customUrl,
  }));
  const pl = await get(
    "https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&mine=true&maxResults=50",
  );
  const playlists = (pl.items || []).map((p: any) => ({
    id: p.id,
    title: p.snippet?.title,
    count: p.contentDetails?.itemCount,
  }));
  const vid = process.argv[2];
  let video: unknown = null;
  if (vid) {
    const v = await get(
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails,processingDetails&id=${vid}`,
    );
    const it = v.items?.[0];
    video = it && {
      id: it.id,
      channelId: it.snippet.channelId,
      title: it.snippet.title,
      tags: it.snippet.tags,
      categoryId: it.snippet.categoryId,
      defaultLanguage: it.snippet.defaultLanguage,
      defaultAudioLanguage: it.snippet.defaultAudioLanguage,
      descriptionHead: it.snippet.description.split("\n").slice(0, 2),
      thumbnail: it.snippet.thumbnails?.maxres?.url || it.snippet.thumbnails?.high?.url,
      status: it.status,
      duration: it.contentDetails?.duration,
      caption: it.contentDetails?.caption,
      processing: it.processingDetails?.processingStatus,
    };
  }
  const ok = items.length === 1 && items[0].id === HOS_ID;
  console.log(JSON.stringify({ ok, channels: items, playlists, video }, null, 2));
  console.log(ok ? `PASS  channel ${HOS_ID}` : "FAIL  connection is not @HistoryOfScienceYT; do not upload");
  if (!ok) process.exitCode = 1;
}

main()
  .catch((e) => {
    console.error(e instanceof Error ? e.message : e);
    process.exitCode = 1;
  })
  .finally(() => prisma.$disconnect());
