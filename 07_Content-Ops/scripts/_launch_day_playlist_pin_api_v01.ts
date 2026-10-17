/**
 * Launch-day API helpers: confirm/add GHZDsiH7L7A to playlist PLEbpfUzWzcXU;
 * create pinned comment via update-pinned-comment path.
 * Uses HOS 07_Content-Ops .env only. Never prints secrets.
 */
import fs from "fs";
import path from "path";
import { afterRun, beforeRun, youtubeAccessToken } from "./channel-youtube";
import { buildPinnedCommentText, DEFAULT_MILESTONES } from "../src/lib/publishing/pinned-comment";

const PID = "PLEbpfUzWzcXU";
const VID = "GHZDsiH7L7A";
const EXPECT_NAME = "How Did We Discover";
const PIN_Q =
  "What's really inside an atom — and why is the periodic table in this order?";
const CONFIG = path.resolve(__dirname, "../../00_Brand/Channel-Setup/PINNED_COMMENTS.json");
const OUT = path.resolve(
  __dirname,
  "../../02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package/Schedule/evidence_2026-10-15_launch_day/API_PLAYLIST_PIN.json",
);

async function yt(token: string, url: string, init?: RequestInit) {
  const res = await fetch(url, {
    ...init,
    headers: { Authorization: `Bearer ${token}`, ...(init?.headers || {}) },
  });
  const body = await res.json();
  return { status: res.status, ok: res.ok, body };
}

async function main() {
  beforeRun("launch-day-playlist-pin-api");
  const token = await youtubeAccessToken();
  const result: Record<string, unknown> = { at: new Date().toISOString(), vid: VID, pid: PID };

  const pl = await yt(
    token,
    `https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&id=${PID}`,
  );
  const title = pl.body?.items?.[0]?.snippet?.title as string | undefined;
  const count = pl.body?.items?.[0]?.contentDetails?.itemCount as number | undefined;
  result.playlist = { status: pl.status, title, count, nameOk: !!(title && title.includes(EXPECT_NAME)) };

  const items: { pos: number; id: string; title: string }[] = [];
  let page = "";
  do {
    const u =
      `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=50&playlistId=${PID}` +
      (page ? `&pageToken=${page}` : "");
    const j = await yt(token, u);
    for (const it of j.body?.items || []) {
      items.push({
        pos: it.snippet.position,
        id: it.contentDetails.videoId,
        title: it.snippet.title,
      });
    }
    page = j.body?.nextPageToken || "";
  } while (page);
  result.items = items;
  const has = items.some((i) => i.id === VID);
  result.has004 = has;

  if (!has && result.playlist && (result.playlist as { nameOk?: boolean }).nameOk) {
    const ins = await yt(token, "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        snippet: {
          playlistId: PID,
          resourceId: { kind: "youtube#video", videoId: VID },
        },
      }),
    });
    result.insert = { status: ins.status, ok: ins.ok, id: ins.body?.id, err: ins.ok ? undefined : ins.body };
  }

  // Pin comment create (API cannot pin — Studio step after)
  const config = JSON.parse(fs.readFileSync(CONFIG, "utf8"));
  const existing = (config.comments || []).find((c: { videoId: string }) => c.videoId === VID);
  const channel = await yt(
    token,
    "https://www.googleapis.com/youtube/v3/channels?part=statistics&mine=true",
  );
  const subscribers = Number(channel.body?.items?.[0]?.statistics?.subscriberCount ?? 0);
  const text = buildPinnedCommentText({
    question: PIN_Q,
    subscribers,
    milestones: config.milestones ?? DEFAULT_MILESTONES,
    cadence: config.cadence,
  });
  result.pinText = text;
  result.pinTextMatchesExact =
    text === PIN_Q || text.startsWith(PIN_Q) || text.includes(PIN_Q);

  if (existing?.commentId) {
    result.pin = { already: true, commentId: existing.commentId };
  } else {
    // Prefer exact package text for first post (user asked exact from file)
    const postText = PIN_Q;
    const thread = await yt(token, "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        snippet: {
          videoId: VID,
          topLevelComment: { snippet: { textOriginal: postText } },
        },
      }),
    });
    const commentId = thread.body?.snippet?.topLevelComment?.id as string | undefined;
    result.pin = { status: thread.status, ok: thread.ok, commentId, err: thread.ok ? undefined : thread.body };
    if (thread.ok && commentId) {
      config.comments = (config.comments || []).filter((c: { videoId: string }) => c.videoId !== VID);
      config.comments.push({
        videoId: VID,
        commentId,
        question: PIN_Q,
        title: "What's Really Inside an Atom?",
      });
      fs.writeFileSync(CONFIG, JSON.stringify(config, null, 2) + "\n");
      result.pinConfigUpdated = true;
    }
  }

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(result, null, 2) + "\n");
  console.log(JSON.stringify(result, null, 2));
  afterRun("launch-day-playlist-pin-api");
}

main().catch((e) => {
  console.error(String(e));
  process.exit(1);
});
