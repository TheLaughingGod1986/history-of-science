/**
 * Fix playlist PLEbpfUzWzcXU order toward 001→004.
 * Add missing 001; remove deleted private stub if present; leave Blood after 004.
 */
import fs from "fs";
import path from "path";
import { afterRun, beforeRun, youtubeAccessToken } from "./channel-youtube";

const PID = "PLEbpfUzWzcXU";
const WANT = ["_C92tIJCk8A", "AL_-qlWko_g", "frP_YrNShsU", "GHZDsiH7L7A"];
const OUT = path.resolve(
  __dirname,
  "../../02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule/evidence_2026-10-15_launch_day/API_PLAYLIST_ORDER.json",
);

async function yt(token: string, url: string, init?: RequestInit) {
  const res = await fetch(url, {
    ...init,
    headers: { Authorization: `Bearer ${token}`, ...(init?.headers || {}) },
  });
  const text = await res.text();
  let body: unknown = null;
  if (text) {
    try {
      body = JSON.parse(text);
    } catch {
      body = text;
    }
  }
  return { status: res.status, ok: res.ok || res.status === 204, body };
}

async function listItems(token: string) {
  const items: any[] = [];
  let page = "";
  do {
    const u =
      `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=50&playlistId=${PID}` +
      (page ? `&pageToken=${page}` : "");
    const j = await yt(token, u);
    items.push(...(j.body.items || []));
    page = j.body.nextPageToken || "";
  } while (page);
  return items;
}

async function main() {
  beforeRun("launch-day-playlist-order");
  const token = await youtubeAccessToken();
  const result: Record<string, unknown> = { at: new Date().toISOString() };

  let items = await listItems(token);
  result.before = items.map((it) => ({
    pos: it.snippet.position,
    id: it.contentDetails.videoId,
    title: it.snippet.title,
    playlistItemId: it.id,
  }));

  // Remove deleted video stubs
  const removed: string[] = [];
  for (const it of items) {
    if (/^Deleted video$/i.test(it.snippet.title || "")) {
      const del = await yt(
        token,
        `https://www.googleapis.com/youtube/v3/playlistItems?id=${it.id}`,
        { method: "DELETE" },
      );
      removed.push(it.id);
      result.deleteDeleted = { status: del.status, ok: del.status === 204 || del.ok };
    }
  }
  result.removedDeleted = removed;

  items = await listItems(token);
  const byVid = new Map(items.map((it) => [it.contentDetails.videoId, it]));

  // Add missing core longs
  const added: string[] = [];
  for (const vid of WANT) {
    if (!byVid.has(vid)) {
      const ins = await yt(token, "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          snippet: { playlistId: PID, resourceId: { kind: "youtube#video", videoId: vid } },
        }),
      });
      added.push(vid);
      result[`add_${vid}`] = { status: ins.status, ok: ins.ok, err: ins.ok ? undefined : ins.body };
    }
  }

  items = await listItems(token);
  const map = new Map(items.map((it) => [it.contentDetails.videoId, it]));

  // Reorder: place WANT at positions 0..3; leave others after
  const others = items
    .filter((it) => !WANT.includes(it.contentDetails.videoId))
    .map((it) => it.contentDetails.videoId);
  const finalOrder = [...WANT, ...others];
  const moves: unknown[] = [];
  for (let pos = 0; pos < finalOrder.length; pos++) {
    const vid = finalOrder[pos];
    const it = map.get(vid);
    if (!it) continue;
    if (it.snippet.position === pos) continue;
    const upd = await yt(token, "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: it.id,
        snippet: {
          playlistId: PID,
          position: pos,
          resourceId: { kind: "youtube#video", videoId: vid },
        },
      }),
    });
    moves.push({ vid, pos, status: upd.status, ok: upd.ok });
  }
  result.moves = moves;
  result.added = added;

  const after = await listItems(token);
  result.after = after.map((it) => ({
    pos: it.snippet.position,
    id: it.contentDetails.videoId,
    title: it.snippet.title,
  }));
  result.coreOrderOk = WANT.every((vid, i) => after[i]?.contentDetails?.videoId === vid);

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(result, null, 2) + "\n");
  console.log(JSON.stringify(result, null, 2));
  afterRun("launch-day-playlist-order");
}

main().catch((e) => {
  console.error(String(e));
  process.exit(1);
});
