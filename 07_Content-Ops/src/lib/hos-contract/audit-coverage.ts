/**
 * HOS channel-audit uploads coverage reconciliation (J3847, 27 Nov 2026).
 *
 * YouTube's `playlistItems.list` on an uploads playlist (`UU...`) can repeat items across
 * page boundaries and omit an equal number of real channel videos while still reporting
 * `pageInfo.totalResults` equal to the raw row count. Relying solely on `playlistItems.list`
 * therefore risks silently dropping still-public videos from audits and `LIVE_VIDEOS.json`.
 *
 * This module collects known HOS video IDs from repo records, identifies any omitted from
 * the uploads playlist enumeration so `channel-audit.ts` can check them directly via
 * `videos.list`, merges only confirmed HOS-channel responses, and emits an honest coverage
 * summary without fabricating causes or forcing listing totals.
 */
import fs from "fs";
import path from "path";
import { dedupeVideoIds, dedupeVideosById, HOS_CHANNEL_ID, type ApiVideo } from "./rules";

export const YOUTUBE_VIDEO_ID_RE = /^[A-Za-z0-9_-]{11}$/;

export function isValidVideoId(id: unknown): id is string {
  return typeof id === "string" && YOUTUBE_VIDEO_ID_RE.test(id);
}

/** Return distinct video IDs that appeared more than once, in first-duplicate order. */
export function findDuplicateVideoIds(ids: readonly string[]): string[] {
  const seen = new Set<string>();
  const dups = new Set<string>();
  const out: string[] = [];
  for (const id of ids) {
    if (seen.has(id)) {
      if (!dups.has(id)) {
        dups.add(id);
        out.push(id);
      }
    } else {
      seen.add(id);
    }
  }
  return out;
}

/** Extract valid 11-char video IDs from column 2 (`Id`) of `audits/SHORTS_LOG.md`. */
export function parseShortsLogIds(markdown: string): string[] {
  const ids: string[] = [];
  for (const line of markdown.split(/\r?\n/)) {
    if (!line.trim().startsWith("|")) continue;
    const cells = line.split("|").map((c) => c.trim());
    const id = /`([A-Za-z0-9_-]{11})`/.exec(cells[2] || "")?.[1];
    if (id && isValidVideoId(id)) ids.push(id);
  }
  return dedupeVideoIds(ids);
}

export type KnownVideoSources = {
  ids: string[];
  bySource: {
    liveVideosJson: string[];
    shortsLog: string[];
    shortsRelease: string[];
    packageManifests: string[];
  };
};

/**
 * Collect known HOS video IDs recorded in this repo so `channel-audit.ts` can directly check
 * any ID omitted by `playlistItems.list` before reporting coverage or writing `LIVE_VIDEOS.json`.
 */
export function collectKnownHosVideoIds(repoRoot: string): KnownVideoSources {
  const liveVideosJson: string[] = [];
  const shortsLog: string[] = [];
  const shortsRelease: string[] = [];
  const packageManifests: string[] = [];

  const livePath = path.join(repoRoot, "00_Brand", "Channel-Setup", "audits", "LIVE_VIDEOS.json");
  if (fs.existsSync(livePath)) {
    try {
      const data = JSON.parse(fs.readFileSync(livePath, "utf8")) as { videos?: Array<{ id?: unknown }> };
      for (const v of data.videos || []) {
        if (isValidVideoId(v?.id)) liveVideosJson.push(v.id);
      }
    } catch {
      // Unreadable snapshot should not block live API auditing.
    }
  }

  const logPath = path.join(repoRoot, "00_Brand", "Channel-Setup", "audits", "SHORTS_LOG.md");
  if (fs.existsSync(logPath)) {
    try {
      shortsLog.push(...parseShortsLogIds(fs.readFileSync(logPath, "utf8")));
    } catch {
      // Unreadable log should not block live API auditing.
    }
  }

  const projectsDir = path.join(repoRoot, "02_Video-Projects");
  if (fs.existsSync(projectsDir)) {
    for (const entry of fs.readdirSync(projectsDir)) {
      const relPath = path.join(projectsDir, entry, "10_Shorts", "SHORTS_RELEASE.json");
      if (fs.existsSync(relPath)) {
        try {
          const data = JSON.parse(fs.readFileSync(relPath, "utf8")) as { shorts?: Array<{ id?: unknown }> };
          for (const s of data.shorts || []) {
            if (isValidVideoId(s?.id)) shortsRelease.push(s.id);
          }
        } catch {
          // Skip malformed release file during ID collection; package-lint catches schema errors.
        }
      }

      const manifestPath = path.join(projectsDir, entry, "11_Upload-Package", "PACKAGE_MANIFEST.json");
      if (fs.existsSync(manifestPath)) {
        try {
          const data = JSON.parse(fs.readFileSync(manifestPath, "utf8")) as { youtubeId?: unknown };
          if (isValidVideoId(data?.youtubeId)) packageManifests.push(data.youtubeId);
        } catch {
          // Skip malformed manifest during ID collection; package-lint catches schema errors.
        }
      }
    }
  }

  const bySource = {
    liveVideosJson: dedupeVideoIds(liveVideosJson),
    shortsLog: dedupeVideoIds(shortsLog),
    shortsRelease: dedupeVideoIds(shortsRelease),
    packageManifests: dedupeVideoIds(packageManifests),
  };

  return {
    ids: dedupeVideoIds([
      ...bySource.liveVideosJson,
      ...bySource.shortsLog,
      ...bySource.shortsRelease,
      ...bySource.packageManifests,
    ]),
    bySource,
  };
}

/** Return valid known IDs that were absent from the uploads playlist enumeration. */
export function planDirectLookupIds(playlistUniqueIds: readonly string[], knownIds: readonly string[]): string[] {
  const present = new Set(playlistUniqueIds);
  return dedupeVideoIds(knownIds.filter((id) => isValidVideoId(id) && !present.has(id)));
}

export type PlaylistEnumResult = {
  pages: number;
  rawIds: string[];
  totalResults: number | null;
};

export type RecoveredVideoSummary = {
  id: string;
  privacy: string;
  scheduled: boolean;
  title: string;
};

export type UploadsCoverageReport = {
  playlistPages: number;
  playlistRawCount: number;
  playlistUniqueCount: number;
  playlistDuplicateIds: string[];
  playlistTotalResults: number | null;
  channelVideoCount: number | null;
  knownSourceIdCount: number;
  omittedKnownIdsChecked: string[];
  recoveredViaDirectLookup: RecoveredVideoSummary[];
  notReturnedByDirectLookup: string[];
  auditedTotal: number;
  auditedPublicCount: number;
  incompletePlaylistDetected: boolean;
};

/**
 * Reconcile uploads-playlist `videos.list` rows with direct `videos.list` lookups for known
 * repo IDs that `playlistItems.list` omitted. Only confirmed `channelId` matches are merged;
 * unreturned IDs are reported explicitly rather than assumed private or deleted.
 */
export function reconcileChannelUploads(input: {
  channelId?: string;
  channelVideoCount: number | null;
  playlist: PlaylistEnumResult;
  playlistVideos: readonly ApiVideo[];
  knownIds: readonly string[];
  directLookupVideos: readonly ApiVideo[];
}): { videos: ApiVideo[]; coverage: UploadsCoverageReport } {
  const channelId = input.channelId ?? HOS_CHANNEL_ID;
  const playlistUniqueIds = dedupeVideoIds(input.playlist.rawIds);
  const playlistDuplicateIds = findDuplicateVideoIds(input.playlist.rawIds);
  const omittedKnownIdsChecked = planDirectLookupIds(playlistUniqueIds, input.knownIds);
  const omittedSet = new Set(omittedKnownIdsChecked);

  const confirmedRecovered = dedupeVideosById(input.directLookupVideos).filter(
    (v) => omittedSet.has(v.id) && v.snippet?.channelId === channelId,
  );
  const recoveredSet = new Set(confirmedRecovered.map((v) => v.id));

  const recoveredViaDirectLookup: RecoveredVideoSummary[] = confirmedRecovered.map((v) => ({
    id: v.id,
    privacy: v.status?.privacyStatus || "",
    scheduled: Boolean(v.status?.publishAt),
    title: v.snippet?.title || "",
  }));

  const notReturnedByDirectLookup = omittedKnownIdsChecked.filter((id) => !recoveredSet.has(id));
  const videos = dedupeVideosById([...input.playlistVideos, ...confirmedRecovered]);
  const auditedPublicCount = videos.filter((v) => v.status?.privacyStatus === "public").length;

  const incompletePlaylistDetected =
    playlistDuplicateIds.length > 0 ||
    (input.playlist.totalResults != null && playlistUniqueIds.length < input.playlist.totalResults) ||
    recoveredViaDirectLookup.length > 0 ||
    (input.channelVideoCount != null && auditedPublicCount < input.channelVideoCount);

  return {
    videos,
    coverage: {
      playlistPages: input.playlist.pages,
      playlistRawCount: input.playlist.rawIds.length,
      playlistUniqueCount: playlistUniqueIds.length,
      playlistDuplicateIds,
      playlistTotalResults: input.playlist.totalResults,
      channelVideoCount: input.channelVideoCount,
      knownSourceIdCount: dedupeVideoIds(input.knownIds.filter(isValidVideoId)).length,
      omittedKnownIdsChecked,
      recoveredViaDirectLookup,
      notReturnedByDirectLookup,
      auditedTotal: videos.length,
      auditedPublicCount,
      incompletePlaylistDetected,
    },
  };
}

export function formatCoverageWarnings(coverage: UploadsCoverageReport): string[] {
  const lines: string[] = [];
  if (coverage.playlistDuplicateIds.length > 0) {
    const totalNote = coverage.playlistTotalResults != null ? ` (totalResults=${coverage.playlistTotalResults})` : "";
    lines.push(
      `Coverage notice: playlistItems.list returned ${coverage.playlistRawCount} raw rows across ${coverage.playlistPages} page(s)${totalNote} with ${coverage.playlistDuplicateIds.length} duplicate ID(s) (${coverage.playlistDuplicateIds.join(", ")}) -> ${coverage.playlistUniqueCount} unique playlist IDs.`,
    );
  } else if (coverage.playlistTotalResults != null && coverage.playlistUniqueCount < coverage.playlistTotalResults) {
    lines.push(
      `Coverage notice: playlistItems.list returned ${coverage.playlistUniqueCount} unique ID(s) vs pageInfo.totalResults=${coverage.playlistTotalResults}.`,
    );
  }

  if (coverage.recoveredViaDirectLookup.length > 0) {
    const summary = coverage.recoveredViaDirectLookup
      .map((r) => `${r.id} (${r.privacy || "unknown"}${r.scheduled ? ", scheduled" : ""})`)
      .join(", ");
    lines.push(
      `Direct videos.list recovery: ${coverage.recoveredViaDirectLookup.length} known HOS ID(s) omitted from playlistItems.list confirmed on channel via direct lookup: ${summary}.`,
    );
  }

  if (coverage.notReturnedByDirectLookup.length > 0) {
    lines.push(
      `Direct videos.list unresolved: ${coverage.notReturnedByDirectLookup.length} known repo ID(s) not returned on HOS by direct lookup (${coverage.notReturnedByDirectLookup.join(", ")}) — verify directly in Studio before inferring visibility.`,
    );
  }

  if (coverage.channelVideoCount != null && coverage.auditedPublicCount < coverage.channelVideoCount) {
    lines.push(
      `Coverage warning: audited public count (${coverage.auditedPublicCount}) is below channel statistics.videoCount (${coverage.channelVideoCount}); uploads playlist may still omit an unrecorded public video.`,
    );
  }

  if (lines.length > 0) {
    const statNote =
      coverage.channelVideoCount != null ? `; channel statistics.videoCount=${coverage.channelVideoCount}` : "";
    lines.push(
      `Coverage totals: ${coverage.auditedTotal} audited HOS video(s) (${coverage.auditedPublicCount} public${statNote}).`,
    );
  }

  return lines;
}
