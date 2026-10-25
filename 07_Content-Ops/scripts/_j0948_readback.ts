import { youtubeAccessToken } from "../src/lib/publishing/youtube-token";
import { prisma } from "../src/lib/storage/prisma";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const ID = "BW_CFAX-mxc,5n7xFQRBUvI";

async function main() {
  const t = await youtubeAccessToken();
  const ch = await fetch("https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true", {
    headers: { Authorization: `Bearer ${t}` },
  }).then((r) => r.json());
  const channelId = ch.items?.[0]?.id;
  const channelTitle = ch.items?.[0]?.snippet?.title;
  if (channelId !== HOS) {
    console.log(JSON.stringify({ channelOk: false, channelId, channelTitle }));
    return;
  }
  const v = await fetch(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${ID}`,
    { headers: { Authorization: `Bearer ${t}` } },
  ).then((r) => r.json());
  const items = (v.items || []).map((it: any) => ({
    id: it.id,
    title: it.snippet?.title,
    description: it.snippet?.description,
    tags: it.snippet?.tags,
    categoryId: it.snippet?.categoryId,
    defaultLanguage: it.snippet?.defaultLanguage,
    defaultAudioLanguage: it.snippet?.defaultAudioLanguage,
    privacy: it.status?.privacyStatus,
    publishAt: it.status?.publishAt || null,
    uploadStatus: it.status?.uploadStatus || null,
    kids: it.status?.selfDeclaredMadeForKids,
    synthetic: it.status?.containsSyntheticMedia,
    duration: it.contentDetails?.duration,
    channelId: it.snippet?.channelId,
    thumbs: {
      maxres: it.snippet?.thumbnails?.maxres?.url || null,
      standard: it.snippet?.thumbnails?.standard?.url || null,
      high: it.snippet?.thumbnails?.high?.url || null,
    },
  }));
  console.log(JSON.stringify({ channelOk: true, channelTitle, error: v.error?.message || null, items }, null, 2));
}

main()
  .catch((e) => {
    console.error(e instanceof Error ? e.message : e);
    process.exitCode = 1;
  })
  .finally(() => prisma.$disconnect());
