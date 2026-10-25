import fs from "fs";
import { youtubeAccessToken } from "../src/lib/publishing/youtube-token";
import { prisma } from "../src/lib/storage/prisma";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const NEW_ID = "BW_CFAX-mxc";
const OLD_ID = "5n7xFQRBUvI";
const EXPECT = "2026-10-31T11:30:00Z";

function srtTime(s: number): string {
  const ms = Math.round(s * 1000);
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  const sec = Math.floor((ms % 60000) / 1000);
  const milli = ms % 1000;
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${pad(h)}:${pad(m)}:${pad(sec)},${String(milli).padStart(3, "0")}`;
}

const CUES = [
  [0.03, 2.051, "The heart wasn't a pump at all."],
  [2.24, 5.641, "It was a warm stove, and its job was to heat the blood."],
  [5.75, 10.62, "Your food turns into a milky juice, and your liver turns that juice into blood."],
  [10.73, 16.45, "Your veins carry the blood out to every part of you, and your flesh soaks it up as nourishment."],
  [16.62, 20.62, "For 14 centuries, hardly anyone dared to argue with his books."],
] as const;

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
  };
}

async function main() {
  const t = await youtubeAccessToken();
  const ch = await yt(t, "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true");
  if (ch.json.items?.[0]?.id !== HOS) throw new Error("not HOS");
  const before = await yt(
    t,
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${NEW_ID},${OLD_ID}`,
  );
  const items = before.json.items || [];
  const neu = items.find((i: any) => i.id === NEW_ID);
  const old = items.find((i: any) => i.id === OLD_ID);
  console.log("BEFORE", JSON.stringify({ neu: brief(neu), old: brief(old) }));
  if (!neu || neu.status?.privacyStatus !== "private" || neu.status?.publishAt !== EXPECT) {
    throw new Error("new video is not private with the expected publishAt; leaving v01 scheduled");
  }
  if (neu.snippet?.title !== "Is the Heart a Pump?") {
    throw new Error("new title does not match; leaving v01 scheduled");
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
  if (!uns.ok) throw new Error("unschedule failed; v01 may still be scheduled");

  const srtBody = srt();
  const srtPath = "/tmp/j0948_galen_v04.en-GB.srt";
  fs.writeFileSync(srtPath, srtBody);
  const boundary = `j0948${Date.now()}`;
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
