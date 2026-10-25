/**
 * J0946: upload en-GB captions for the new 007 long and read the video back.
 * Refuses anything that is not the HOS channel, private, and publishAt 2026-11-12T18:00:00Z.
 */
import fs from "fs";
import path from "path";
import { youtubeAccessToken } from "../src/lib/publishing/youtube-token";
import { prisma } from "../src/lib/storage/prisma";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const EXPECT = "2026-11-12T18:00:00.000Z";
const TITLE = "Why Vaccines Are Named After a Cow";
const SRT = path.resolve(
  __dirname,
  "../../02_Video-Projects/007_The-First-Vaccine/11_Upload-Package/Captions/hos_007_master_v04.en.srt",
);
const OUT = path.resolve(
  __dirname,
  "../../02_Video-Projects/007_The-First-Vaccine/11_Upload-Package/API_READBACK_J0946.json",
);

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? undefined : process.argv[i + 1];
}

async function yt(t: string, url: string, init?: RequestInit) {
  const r = await fetch(url, {
    ...init,
    headers: { Authorization: `Bearer ${t}`, ...(init?.headers || {}) },
  });
  const text = await r.text();
  let json: any;
  try { json = JSON.parse(text); } catch { json = { raw: text.slice(0, 500) }; }
  return { ok: r.ok, status: r.status, json };
}

async function main() {
  const videoId = arg("video");
  if (!videoId) throw new Error("need --video");
  const t = await youtubeAccessToken();
  const ch = await yt(t, "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true");
  const channelId = ch.json.items?.[0]?.id;
  if (channelId !== HOS) throw new Error(`not HOS (${channelId})`);

  const before = await yt(
    t,
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${videoId}`,
  );
  const item = (before.json.items || [])[0];
  if (!item) throw new Error("video not found");
  if (item.snippet?.channelId !== HOS) throw new Error("video is not on HOS");
  if (item.status?.privacyStatus !== "private") throw new Error(`privacy is ${item.status?.privacyStatus}`);
  if (item.status?.publishAt !== EXPECT && item.status?.publishAt !== "2026-11-12T18:00:00Z") {
    throw new Error(`publishAt is ${item.status?.publishAt}`);
  }
  if (item.snippet?.title !== TITLE) throw new Error(`title is ${item.snippet?.title}`);

  if (process.argv.includes("--list-only")) {
    const capsOnly = await yt(t, `https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=${videoId}`);
    console.log(JSON.stringify({
      privacy: item.status?.privacyStatus,
      publishAt: item.status?.publishAt,
      uploadStatus: item.status?.uploadStatus,
      failure: item.status?.failureReason || null,
      duration: item.contentDetails?.duration,
      hasCustomThumbnail: item.contentDetails?.hasCustomThumbnail,
      captions: (capsOnly.json.items || []).map((c: any) => ({
        id: c.id, language: c.snippet?.language, status: c.snippet?.status, isDraft: c.snippet?.isDraft,
      })),
      capErr: capsOnly.json.error?.message || null,
    }, null, 2));
    return;
  }

  const srtBody = fs.readFileSync(SRT);
  const boundary = `j0946${Date.now()}`;
  const meta = JSON.stringify({
    snippet: { videoId, language: "en-GB", name: "English (United Kingdom)", isDraft: false },
  });
  const body = Buffer.concat([
    Buffer.from(`--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${meta}\r\n`),
    Buffer.from(`--${boundary}\r\nContent-Type: application/octet-stream\r\n\r\n`),
    srtBody,
    Buffer.from(`\r\n--${boundary}--\r\n`),
  ]);
  const cap = await yt(
    t,
    "https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart&sync=false",
    { method: "POST", headers: { "Content-Type": `multipart/related; boundary=${boundary}` }, body },
  );

  const after = await yt(
    t,
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${videoId}`,
  );
  const caps = await yt(t, `https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=${videoId}`);
  const v = (after.json.items || [])[0];
  const readback = {
    videoId,
    channelId: v?.snippet?.channelId,
    title: v?.snippet?.title,
    privacy: v?.status?.privacyStatus,
    publishAt: v?.status?.publishAt || null,
    madeForKids: v?.status?.selfDeclaredMadeForKids,
    containsSyntheticMedia: v?.status?.containsSyntheticMedia ?? null,
    language: v?.snippet?.defaultLanguage,
    audioLanguage: v?.snippet?.defaultAudioLanguage,
    categoryId: v?.snippet?.categoryId,
    tags: v?.snippet?.tags || [],
    duration: v?.contentDetails?.duration,
    hasCustomThumbnail: v?.contentDetails?.hasCustomThumbnail ?? null,
    thumbnails: v?.snippet?.thumbnails || null,
    description: v?.snippet?.description || "",
    captionUpload: {
      ok: cap.ok,
      status: cap.status,
      id: cap.json?.id || null,
      language: cap.json?.snippet?.language || null,
      trackStatus: cap.json?.snippet?.status || null,
      error: cap.json?.error?.message || null,
    },
    captions: (caps.json.items || []).map((c: any) => ({
      id: c.id,
      language: c.snippet?.language,
      trackKind: c.snippet?.trackKind,
      status: c.snippet?.status,
      isDraft: c.snippet?.isDraft,
      name: c.snippet?.name,
    })),
  };
  fs.writeFileSync(OUT, JSON.stringify(readback, null, 2) + "\n");
  console.log(JSON.stringify({
    videoId,
    privacy: readback.privacy,
    publishAt: readback.publishAt,
    title: readback.title,
    tags: readback.tags.length,
    duration: readback.duration,
    hasCustomThumbnail: readback.hasCustomThumbnail,
    descriptionHasChapters: /Chapters/.test(readback.description) && /1:41/.test(readback.description),
    captionUpload: readback.captionUpload,
    captions: readback.captions,
    wrote: OUT,
  }, null, 2));
  if (!cap.ok) process.exitCode = 1;
}

main()
  .catch((e) => {
    console.error(e instanceof Error ? e.message : e);
    process.exitCode = 1;
  })
  .finally(() => prisma.$disconnect());
