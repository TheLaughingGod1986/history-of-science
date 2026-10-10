import fs from "fs";
import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const OLD = "93fPUG-hW0A";
const PUBLISH_AT = "2026-10-13T10:30:00.000Z";
const DIR = "/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/001_How-Did-We-Discover-Germs/10_Shorts";
const VIDEO = `${DIR}/hos_001_s05_soap_punch_v04_audiofix.mp4`;
const COVER = `${DIR}/hos_001_s05_soap_cover_animistry_v02.jpg`;
const OUT = process.argv[2];
const REAL = process.argv.includes("--real");

async function token(): Promise<string> {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({ where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null }, orderBy: { updatedAt: "desc" } });
  if (!conn?.refreshTokenEncrypted) throw new Error("no HOS connection");
  const tr = await fetch("https://oauth2.googleapis.com/token", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams({ client_id: env.GOOGLE_CLIENT_ID || "", client_secret: env.GOOGLE_CLIENT_SECRET || "", refresh_token: decryptSecret(conn.refreshTokenEncrypted), grant_type: "refresh_token" }) });
  const j = await tr.json();
  if (!j.access_token) throw new Error("token refresh failed");
  return j.access_token;
}

async function main() {
  const t = await token();
  const auth = { Authorization: `Bearer ${t}` };
  const yt = async (p: string, init?: RequestInit) => {
    const r = await fetch(`https://www.googleapis.com/youtube/v3/${p}`, { ...init, headers: { ...auth, ...(init?.headers || {}) } });
    const txt = await r.text();
    let json: any; try { json = JSON.parse(txt); } catch { json = { raw: txt }; }
    return { status: r.status, json };
  };
  const log: any = { at: new Date().toISOString(), job: "J0120", real: REAL };

  const ch = (await yt("channels?part=id,snippet&mine=true")).json.items?.[0];
  log.channel = { id: ch?.id, title: ch?.snippet?.title };
  console.log("CHANNEL", ch?.id, ch?.snippet?.title);
  if (ch?.id !== HOS) throw new Error("WRONG CHANNEL");

  const old = (await yt(`videos?part=snippet,status,localizations&id=${OLD}`)).json.items?.[0];
  if (!old) throw new Error("old video not found");
  log.oldBefore = { privacy: old.status.privacyStatus, publishAt: old.status.publishAt || null };

  const s = (await yt(`search?part=snippet&forMine=true&type=video&maxResults=25&q=${encodeURIComponent(old.snippet.title)}`)).json;
  const dups = (s.items || []).filter((i: any) => i.id?.videoId !== OLD && i.snippet?.title === old.snippet.title);
  log.existingCopies = dups.map((i: any) => i.id.videoId);
  console.log("EXISTING COPIES", log.existingCopies);
  if (dups.length) throw new Error("a copy already exists; not uploading again");

  const sn = old.snippet;
  const body = {
    snippet: { title: sn.title, description: sn.description, tags: sn.tags, categoryId: sn.categoryId, defaultLanguage: sn.defaultLanguage, defaultAudioLanguage: sn.defaultAudioLanguage },
    status: { privacyStatus: "private", publishAt: PUBLISH_AT, selfDeclaredMadeForKids: false, license: old.status.license, embeddable: old.status.embeddable, publicStatsViewable: old.status.publicStatsViewable, ...(old.status.containsSyntheticMedia !== undefined ? { containsSyntheticMedia: old.status.containsSyntheticMedia } : {}) },
    localizations: old.localizations,
  };
  log.newMetadata = body;
  console.log("NEW METADATA", JSON.stringify(body, null, 2));
  if (!REAL) { fs.writeFileSync(OUT, JSON.stringify(log, null, 2)); console.log("DRY RUN ONLY"); await prisma.$disconnect(); return; }

  const size = fs.statSync(VIDEO).size;
  const init = await fetch("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status,localizations&notifySubscribers=false", {
    method: "POST", headers: { ...auth, "Content-Type": "application/json; charset=UTF-8", "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": String(size) }, body: JSON.stringify(body),
  });
  const loc = init.headers.get("location");
  if (!loc) throw new Error("upload init failed " + init.status + " " + (await init.text()).slice(0, 500));
  const up = await fetch(loc, { method: "PUT", headers: { "Content-Type": "video/mp4", "Content-Length": String(size) }, body: fs.readFileSync(VIDEO) });
  const upj = await up.json();
  if (!upj.id) throw new Error("upload failed " + up.status + " " + JSON.stringify(upj).slice(0, 500));
  log.newId = upj.id;
  console.log("NEW ID", upj.id);
  fs.writeFileSync(OUT, JSON.stringify(log, null, 2));

  const th = await fetch(`https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${upj.id}`, { method: "POST", headers: { ...auth, "Content-Type": "image/jpeg" }, body: fs.readFileSync(COVER) });
  log.thumbnail = { status: th.status, result: th.ok ? "set" : "refused", body: (await th.text()).slice(0, 300) };
  console.log("THUMBNAIL", log.thumbnail.status, log.thumbnail.result);

  const priv = await yt("videos?part=status", { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ id: OLD, status: { ...old.status, privacyStatus: "private", uploadStatus: undefined, madeForKids: undefined, publishAt: undefined } }) });
  log.oldPrivateUpdate = priv.status;
  console.log("OLD PRIVATE UPDATE", priv.status, priv.status === 200 ? "" : JSON.stringify(priv.json).slice(0, 300));

  const after = (await yt(`videos?part=snippet,status&id=${upj.id},${OLD}`)).json.items || [];
  log.after = after.map((v: any) => ({ id: v.id, title: v.snippet.title, channel: v.snippet.channelTitle, privacy: v.status.privacyStatus, publishAt: v.status.publishAt || null, uploadStatus: v.status.uploadStatus, madeForKids: v.status.selfDeclaredMadeForKids }));
  console.log("AFTER", JSON.stringify(log.after, null, 2));
  fs.writeFileSync(OUT, JSON.stringify(log, null, 2));
  await prisma.$disconnect();
}
main().catch(async (e) => { console.error("ERROR", String(e).slice(0, 600)); await prisma.$disconnect(); process.exit(1); });
