/**
 * J2958: upload en-GB captions for the 007 eradication Short (s07 v06) and read the video back.
 * Refuses anything that is not the HOS channel, private, and publishAt 2026-11-29T11:30:00Z.
 * Adds no second track: if a standard en-GB track is already there it only reads back.
 */
import fs from "fs";
import path from "path";
import { youtubeAccessToken } from "../src/lib/publishing/youtube-token";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const VIDEO = "jkUZpyO71lU";
const EXPECT = "2026-11-29T11:30:00Z";
const TITLE = "How Was Smallpox Eradicated?";
const PKG = path.resolve(
  __dirname,
  "../../02_Video-Projects/007_The-First-Vaccine/10_Shorts/11_Upload-Package/s07_eradication_v06",
);
const SRT = path.join(PKG, "Captions/hos_007_eradication_v06.en-GB.srt");
const OUT = path.join(PKG, "API_READBACK_J2958.json");

async function yt(t: string, url: string, init?: RequestInit) {
  const r = await fetch(url, { ...init, headers: { Authorization: `Bearer ${t}`, ...(init?.headers || {}) } });
  const text = await r.text();
  let json: any;
  try { json = JSON.parse(text); } catch { json = { raw: text.slice(0, 500) }; }
  return { ok: r.ok, status: r.status, json };
}
const video = (t: string) =>
  yt(t, `https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id=${VIDEO}`);
const tracks = (t: string) => yt(t, `https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=${VIDEO}`);

async function main() {
  const t = await youtubeAccessToken();
  const ch = await yt(t, "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true");
  if (ch.json.items?.[0]?.id !== HOS) throw new Error(`not HOS (${ch.json.items?.[0]?.id})`);
  const item = ((await video(t)).json.items || [])[0];
  if (!item) throw new Error("video not found");
  const at = new Date(item.status?.publishAt || 0).toISOString().replace(".000Z", "Z");
  if (item.snippet?.channelId !== HOS || item.status?.privacyStatus !== "private" || at !== EXPECT || item.snippet?.title !== TITLE)
    throw new Error(`refusing: ${item.snippet?.channelId} ${item.status?.privacyStatus} ${at} ${item.snippet?.title}`);

  const before = ((await tracks(t)).json.items || []) as any[];
  let captionUpload: any = { skipped: "a standard en-GB track is already there" };
  if (!before.some((c) => c.snippet?.language === "en-GB" && c.snippet?.trackKind === "standard")) {
    const boundary = `j2958${Date.now()}`;
    const meta = JSON.stringify({ snippet: { videoId: VIDEO, language: "en-GB", name: "English (United Kingdom)", isDraft: false } });
    const body = Buffer.concat([
      Buffer.from(`--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${meta}\r\n`),
      Buffer.from(`--${boundary}\r\nContent-Type: application/octet-stream\r\n\r\n`),
      fs.readFileSync(SRT),
      Buffer.from(`\r\n--${boundary}--\r\n`),
    ]);
    const cap = await yt(t, "https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart&sync=false", {
      method: "POST", headers: { "Content-Type": `multipart/related; boundary=${boundary}` }, body,
    });
    captionUpload = { ok: cap.ok, status: cap.status, id: cap.json?.id || null, language: cap.json?.snippet?.language || null,
      trackStatus: cap.json?.snippet?.status || null, error: cap.json?.error?.message || null };
  }
  const v = ((await video(t)).json.items || [])[0];
  const caps = await tracks(t);
  const readback = {
    job: "J2958", at: new Date().toISOString(), videoId: VIDEO, channelId: v?.snippet?.channelId, title: v?.snippet?.title,
    privacy: v?.status?.privacyStatus, publishAt: v?.status?.publishAt || null, uploadStatus: v?.status?.uploadStatus,
    madeForKids: v?.status?.selfDeclaredMadeForKids, containsSyntheticMedia: v?.status?.containsSyntheticMedia ?? null,
    language: v?.snippet?.defaultLanguage, audioLanguage: v?.snippet?.defaultAudioLanguage, categoryId: v?.snippet?.categoryId,
    tags: v?.snippet?.tags || [], duration: v?.contentDetails?.duration, hasCustomThumbnail: v?.contentDetails?.hasCustomThumbnail ?? null,
    description: v?.snippet?.description || "", captionUpload,
    captions: (caps.json.items || []).map((c: any) => ({ id: c.id, language: c.snippet?.language, trackKind: c.snippet?.trackKind,
      status: c.snippet?.status, isDraft: c.snippet?.isDraft, name: c.snippet?.name })),
    captionError: caps.json.error?.message || null,
  };
  fs.writeFileSync(OUT, JSON.stringify(readback, null, 2) + "\n");
  const { description, tags, ...short } = readback;
  console.log(JSON.stringify({ ...short, tags: tags.length }, null, 1));
}
main().catch((e) => { console.error(String(e?.message || e).slice(0, 300)); process.exit(1); });
