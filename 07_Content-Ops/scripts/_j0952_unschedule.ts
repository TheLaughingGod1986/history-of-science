import fs from "fs";
import { youtubeAccessToken } from "../src/lib/publishing/youtube-token";
import { prisma } from "../src/lib/storage/prisma";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const NEW_ID = "-3L6HzJ_d_4";
const OLD_ID = "1-BZaFIMwYU";
const EXPECT = "2026-10-27T11:30:00Z";
const TITLE = "What Is the Pasteur Swan Neck Flask Experiment?";

const CUES: [number, number, string][] = [
  [0.0, 1.85, "a flask stays clear."],
  [1.85, 2.65, "Boil broth."],
  [2.65, 3.65, "Air can drift,"],
  [3.65, 5.116, "but dust and microbes"],
  [5.116, 6.33, "settle in the curve."],
  [6.33, 7.538, "If life arrives as"],
  [7.538, 9.37, "passengers from the outside,"],
  [9.37, 11.6, "then disease can be a passenger too."],
  [11.6, 12.38, "Break the neck,"],
  [12.38, 13.4, "or tip the trap,"],
  [13.4, 15.755, "and life blooms into cloudiness."],
  [15.755, 17.315, "Keep the swan neck intact."],
];

function srtTime(s: number): string {
  const ms = Math.round(s * 1000);
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  const sec = Math.floor((ms % 60000) / 1000);
  const milli = ms % 1000;
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${pad(h)}:${pad(m)}:${pad(sec)},${String(milli).padStart(3, "0")}`;
}

function srt(): string {
  return CUES.map((c, i) => `${i + 1}\n${srtTime(c[0])} --> ${srtTime(c[1])}\n${c[2]}\n`).join("\n") + "\n";
}

async function yt(t: string, url: string, init?: RequestInit) {
  const r = await fetch(url, {
    ...init,
    headers: { Authorization: `Bearer ${t}`, ...(init?.headers || {}) },
  });
  const text = await r.text();
  let json: any;
  try { json = JSON.parse(text); } catch { json = { raw: text.slice(0, 400) }; }
  return { ok: r.ok, status: r.status, json };
}

function brief(it: any) {
  if (!it) return null;
  return {
    id: it.id,
    title: it.snippet?.title,
    description: it.snippet?.description,
    privacy: it.status?.privacyStatus,
    publishAt: it.status?.publishAt || null,
    kids: it.status?.selfDeclaredMadeForKids,
    synthetic: it.status?.containsSyntheticMedia ?? null,
    lang: it.snippet?.defaultLanguage,
    audioLang: it.snippet?.defaultAudioLanguage,
    tags: it.snippet?.tags || [],
    duration: it.contentDetails?.duration,
    channelId: it.snippet?.channelId,
    categoryId: it.snippet?.categoryId,
    hasCustomThumbnail: it.contentDetails?.hasCustomThumbnail ?? null,
  };
}

async function main() {
  const t = await youtubeAccessToken();
  const ch = await yt(t, "https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true");
  if (ch.json.items?.[0]?.id !== HOS) throw new Error(`not HOS: ${ch.json.items?.[0]?.snippet?.title}`);
  const before = await yt(
    t,
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${NEW_ID},${OLD_ID}`,
  );
  const items = before.json.items || [];
  const neu = items.find((i: any) => i.id === NEW_ID);
  const old = items.find((i: any) => i.id === OLD_ID);
  console.log("BEFORE", JSON.stringify({ neu: brief(neu), old: brief(old) }));
  if (!neu || neu.status?.privacyStatus !== "private" || neu.status?.publishAt !== EXPECT) {
    throw new Error("new video is not private with the expected publishAt; leaving v02 scheduled");
  }
  if (neu.snippet?.title !== TITLE) {
    throw new Error("new title does not match; leaving v02 scheduled");
  }
  if (neu.snippet?.channelId !== HOS || old?.snippet?.channelId !== HOS) {
    throw new Error("video is not on HOS");
  }
  if (old?.status?.privacyStatus !== "private" || old?.status?.publishAt !== EXPECT) {
    throw new Error("old video is not the scheduled private short; leaving it untouched");
  }

  const uns = await yt(t, "https://www.googleapis.com/youtube/v3/videos?part=status", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: OLD_ID,
      status: { privacyStatus: "private", selfDeclaredMadeForKids: false },
    }),
  });
  console.log("UNSCHED", uns.status, JSON.stringify({
    privacy: uns.json?.status?.privacyStatus,
    publishAt: uns.json?.status?.publishAt || null,
    error: uns.json?.error?.message || null,
  }));
  if (!uns.ok) throw new Error("unschedule failed; v02 may still be scheduled");

  const srtBody = srt();
  fs.writeFileSync("/tmp/j0952_flask_v07.en-GB.srt", srtBody);
  const boundary = `j0952${Date.now()}`;
  const meta = JSON.stringify({ snippet: { videoId: NEW_ID, language: "en-GB", name: "", isDraft: false } });
  const body = Buffer.concat([
    Buffer.from(`--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${meta}\r\n`),
    Buffer.from(`--${boundary}\r\nContent-Type: application/octet-stream\r\n\r\n`),
    Buffer.from(srtBody),
    Buffer.from(`\r\n--${boundary}--\r\n`),
  ]);
  const cap = await yt(
    t,
    "https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart&sync=false",
    { method: "POST", headers: { "Content-Type": `multipart/related; boundary=${boundary}` }, body },
  );
  console.log("CAPTIONS", cap.status, JSON.stringify({
    id: cap.json?.id || null,
    language: cap.json?.snippet?.language || null,
    status: cap.json?.snippet?.status || null,
    error: cap.json?.error?.message || null,
  }));

  const after = await yt(
    t,
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${NEW_ID},${OLD_ID}`,
  );
  const caps = await yt(t, `https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=${NEW_ID}`);
  console.log("AFTER", JSON.stringify({
    items: (after.json.items || []).map(brief),
    captions: (caps.json.items || []).map((c: any) => ({
      id: c.id,
      language: c.snippet?.language,
      trackKind: c.snippet?.trackKind,
      status: c.snippet?.status,
      isDraft: c.snippet?.isDraft,
    })),
    captionError: caps.json?.error?.message || null,
  }, null, 2));
}

main()
  .catch((e) => {
    console.error(e instanceof Error ? e.message : e);
    process.exitCode = 1;
  })
  .finally(() => prisma.$disconnect());
