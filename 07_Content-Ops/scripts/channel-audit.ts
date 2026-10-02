#!/usr/bin/env tsx
/**
 * HOS release contract — audit what is ACTUALLY on the channel (read-only).
 *
 *   npx tsx --env-file=.env scripts/channel-audit.ts                 # table, exit 1 on any error
 *   npx tsx --env-file=.env scripts/channel-audit.ts --json
 *   npx tsx --env-file=.env scripts/channel-audit.ts --write-live    # also refresh audits/LIVE_VIDEOS.json
 *   npx tsx scripts/channel-audit.ts --file <videos.json>            # offline: audit a saved API response
 *
 * Reads every upload on @HistoryOfScienceYT through the YouTube Data API (videos.list:
 * snippet, status, contentDetails) and checks each against src/lib/hos-contract/rules.ts:
 * Made for Kids, AI disclosure, Education category, en-GB languages, Premiere, tags, titles,
 * schedule slots, one Short a day, duplicate titles. It changes nothing.
 *
 * Run it after every Studio session and every Monday (with weekly_public_audit.py). Things the
 * API can't read (Related video, end screens, cards, T&C, pinned comment) are printed as a
 * checklist to confirm in Studio.
 */
import fs from "fs";
import path from "path";
import {
  auditChannel,
  auditVideo,
  HOS_CHANNEL_ID,
  isShort,
  STUDIO_ONLY_CHECKS,
  ukSlot,
  type ApiVideo,
  type Finding,
} from "../src/lib/hos-contract/rules";

const REPO = path.resolve(__dirname, "..", "..");
const LIVE_VIDEOS = path.join(REPO, "00_Brand", "Channel-Setup", "audits", "LIVE_VIDEOS.json");
const API = "https://www.googleapis.com/youtube/v3";

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? undefined : process.argv[i + 1];
}

async function accessToken(): Promise<string> {
  // Shared helper: retries an "expired" row that still has a refresh token, and explains invalid_grant.
  const { youtubeAccessToken } = await import("../src/lib/publishing/youtube-token");
  return youtubeAccessToken();
}

async function get(token: string, url: string) {
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  const body = await res.json();
  if (!res.ok) throw new Error(`${url.split("?")[0]} → ${res.status}: ${JSON.stringify(body).slice(0, 200)}`);
  return body;
}

async function fetchChannel(token: string): Promise<{ channel: Record<string, any>; videos: ApiVideo[] }> {
  const ch = await get(token, `${API}/channels?part=id,snippet,status,contentDetails&mine=true`);
  const channel = ch.items?.[0];
  if (!channel) throw new Error("No channel on this token");
  if (channel.id !== HOS_CHANNEL_ID)
    throw new Error(`Token is for channel ${channel.id}, not HOS (${HOS_CHANNEL_ID}). Stop: wrong account.`);
  const uploads = channel.contentDetails.relatedPlaylists.uploads as string;
  const ids: string[] = [];
  let page = "";
  do {
    const pl = await get(
      token,
      `${API}/playlistItems?part=contentDetails&maxResults=50&playlistId=${uploads}${page ? `&pageToken=${page}` : ""}`,
    );
    ids.push(...pl.items.map((i: any) => i.contentDetails.videoId));
    page = pl.nextPageToken || "";
  } while (page);
  const videos: ApiVideo[] = [];
  for (let i = 0; i < ids.length; i += 50) {
    const v = await get(
      token,
      `${API}/videos?part=snippet,status,contentDetails&id=${ids.slice(i, i + 50).join(",")}`,
    );
    videos.push(...v.items);
  }
  return { channel, videos };
}

async function main() {
  let channel: Record<string, any> | null = null;
  let videos: ApiVideo[];
  const file = arg("file");
  if (file) {
    const data = JSON.parse(fs.readFileSync(path.resolve(file), "utf8"));
    videos = Array.isArray(data) ? data : data.items || data.videos || [];
    channel = data.channel || null;
  } else {
    const token = await accessToken();
    ({ channel, videos } = await fetchChannel(token));
  }

  const findings = new Map<string, Finding[]>();
  const channelFindings: Finding[] = [];
  if (channel?.status && (channel.status.madeForKids || channel.status.selfDeclaredMadeForKids))
    channelFindings.push({
      severity: "error",
      rule: "channel.audience",
      message: "the CHANNEL is set as Made for Kids: Settings → Channel → Advanced → No",
    });
  for (const v of videos) findings.set(v.id, auditVideo(v));
  // Declared Shorts (02_Video-Projects/*/10_Shorts/SHORTS_RELEASE.json): the live title must match.
  const projects = path.join(REPO, "02_Video-Projects");
  for (const d of fs.existsSync(projects) ? fs.readdirSync(projects) : []) {
    const rel = path.join(projects, d, "10_Shorts", "SHORTS_RELEASE.json");
    if (!fs.existsSync(rel)) continue;
    const shorts = (JSON.parse(fs.readFileSync(rel, "utf8")).shorts || []) as { id?: string; title: string }[];
    for (const s of shorts) {
      const v = videos.find((x) => x.id === s.id);
      if (v && (v.snippet?.title || "") !== s.title)
        findings.set(v.id, [
          ...(findings.get(v.id) || []),
          {
            severity: "error",
            rule: "title.not-as-released",
            message: `live title "${v.snippet?.title}" ≠ SHORTS_RELEASE title "${s.title}"`,
          },
        ]);
    }
  }
  for (const [id, extra] of auditChannel(videos)) findings.set(id, [...(findings.get(id) || []), ...extra]);

  const rows = videos.map((v) => {
    const f = findings.get(v.id) || [];
    const when = v.status?.publishAt ? `${ukSlot(v.status.publishAt).date} ${ukSlot(v.status.publishAt).time} UK` : "";
    return {
      id: v.id,
      kind: isShort(v) ? "Short" : "long",
      title: v.snippet?.title || "",
      privacy: v.status?.privacyStatus || "",
      scheduled: when,
      errors: f.filter((x) => x.severity === "error"),
      warns: f.filter((x) => x.severity === "warn"),
    };
  });

  if (process.argv.includes("--write-live")) {
    fs.writeFileSync(
      LIVE_VIDEOS,
      JSON.stringify(
        {
          source: "scripts/channel-audit.ts --write-live (YouTube Data API, owner view)",
          pulledAt: new Date().toISOString(),
          videos: rows
            .filter((r) => r.privacy !== "private" || r.scheduled)
            .map((r) => ({ id: r.id, kind: r.kind, title: r.title, privacy: r.privacy, scheduled: r.scheduled })),
        },
        null,
        2,
      ) + "\n",
    );
  }

  const bad = channelFindings.length + rows.reduce((n, r) => n + r.errors.length, 0);
  if (process.argv.includes("--json")) {
    console.log(JSON.stringify({ channelFindings, rows, studioOnly: STUDIO_ONLY_CHECKS }, null, 2));
  } else {
    for (const c of channelFindings) console.log(`FAIL  CHANNEL  [${c.rule}] ${c.message}`);
    for (const r of rows) {
      const verdict = r.errors.length ? "FAIL" : "PASS";
      console.log(`${verdict}  ${r.kind.padEnd(5)} ${r.id}  ${r.privacy}${r.scheduled ? ` ${r.scheduled}` : ""}  ${r.title}`);
      for (const x of r.errors) console.log(`   FAIL  [${x.rule}] ${x.message}`);
      for (const x of r.warns) console.log(`   warn  [${x.rule}] ${x.message}`);
    }
    console.log(`\n${videos.length} videos, ${bad} errors.`);
    console.log("Confirm in Studio (not readable through the API):");
    for (const c of STUDIO_ONLY_CHECKS) console.log(`  - ${c}`);
  }
  process.exit(bad ? 1 : 0);
}

main().catch((e) => {
  console.error(String(e?.message || e));
  process.exit(2);
});
