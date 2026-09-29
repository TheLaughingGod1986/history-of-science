/**
 * HOS 004 package dry-run (music PASS on full_v02). No upload. No secrets printed.
 * Run from 07_Content-Ops: npx tsx scripts/hos-004-package-dry-run-v02.ts
 */
import fs from "fs";
import path from "path";
import { createHash } from "crypto";
import {
  buildStudioFinishChecklist,
  loadYouTubePackage,
} from "../src/lib/publishing/youtube-package";

const REPO = path.resolve(__dirname, "../..");
const PKG = path.join(
  REPO,
  "02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package",
);
const VIDEO = path.join(
  REPO,
  "02_Video-Projects/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_v02.mp4",
);
const HOS_ENV = path.join(REPO, "07_Content-Ops/.env");
const OWB_ENV = "/Users/benjaminoats/YouTube/orbit-with-ben/07_Content-Ops/.env";
const OUT = path.join(PKG, "Schedule", "PACKAGE_DRY_RUN_MUSIC_PASS_2026-09-29.json");
const EXPECTED_SHA =
  "ed870939f476d326197cdaf1403ce7064850d4286ff63aa81bc5a7584761e98e";

function sha256File(p: string): string {
  const h = createHash("sha256");
  h.update(fs.readFileSync(p));
  return h.digest("hex");
}

function main() {
  const hosEnvPresent = fs.existsSync(HOS_ENV);
  const videoSha = sha256File(VIDEO);
  if (videoSha !== EXPECTED_SHA) {
    throw new Error(`full_v02 sha mismatch: got ${videoSha}`);
  }

  const resolved = loadYouTubePackage({
    packageDir: PKG,
    videoPath: VIDEO,
  });

  const studioFinish = buildStudioFinishChecklist({
    videoId: null,
    format: resolved.format,
    titleAbc: resolved.titleAbc,
    thumbnailAbc: resolved.thumbnailAbc,
    pinnedComment: resolved.pinnedComment,
    relatedVideoId: resolved.relatedVideoId,
    firstCommentPosted: false,
    thumbnailSet: Boolean(resolved.thumbnailPath),
    playlistAdded: false,
    playlistId: resolved.playlistId,
  });

  const desc = resolved.description || "";
  const scheduleISO = resolved.scheduledAt?.toISOString() ?? null;

  const result = {
    status: "MUSIC_PASS_DRY_RUN",
    upload: false,
    premiere: false,
    dryRun: true,
    channel: "@HistoryOfScienceYT",
    commandAttempted:
      "cd 07_Content-Ops && npm run youtube:package -- --package ../02_Video-Projects/004_Whats-Really-Inside-An-Atom/11_Upload-Package --video ../02_Video-Projects/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_full_v02.mp4 --dry-run",
    envPathExpected: HOS_ENV,
    envPathForbidden: OWB_ENV,
    hosEnvPresent,
    owbEnvNotUsed: true,
    npmApiPath: hosEnvPresent
      ? "available_if_npm_succeeds"
      : "blocked — HOS 07_Content-Ops/.env absent (DATABASE_URL). Resolved locally via loadYouTubePackage. Secrets not printed. Do not substitute Orbit .env.",
    npmAttemptLog:
      "artifacts/hos_004_npm_package_dryrun_attempt.log — Invalid environment configuration: DATABASE_URL undefined",
    musicPass: {
      cut: "hos_004_full_v02.mp4",
      sha256: videoSha,
      ben: "music is a pass, lets go.",
      passedAt: "2026-09-29",
    },
    unusedMix: {
      cut: "hos_004_full_v03.mp4",
      sha256: "503e228745d4cf87fe6f504522cbad99f6af0f9c8b038c1ed8c52da493428157",
      status: "parked unused — do not upload",
    },
    scheduledAt: scheduleISO,
    scheduleISO,
    scheduleUK: "Thu 15 Oct 2026 18:00 Europe/London",
    privacy: resolved.privacy,
    madeForKids: resolved.madeForKids,
    title: resolved.title,
    titleAbc: resolved.titleAbc,
    thumbnailPath: resolved.thumbnailPath,
    thumbnailAbc: resolved.thumbnailAbc.map((t) => path.basename(t)),
    captionsFile: "Captions/hos_004_full_v02.en.srt",
    captionsPresent: fs.existsSync(path.join(PKG, "Captions", "hos_004_full_v02.en.srt")),
    relatedVideoId: resolved.relatedVideoId,
    endScreen: {
      relatedVideoId: "AL_-qlWko_g",
      relatedTitle: "How Did We Discover the Periodic Table?",
      subscribe: true,
      note: "Studio end screen only — 002 long + Subscribe. No Premiere.",
    },
    pinnedComment: resolved.pinnedComment,
    descriptionFirst100: desc.slice(0, 100),
    descriptionKeywordGate: {
      "inside an atom": /inside an atom/i.test(desc),
      "periodic table": /periodic table/i.test(desc),
      order: /order/i.test(desc),
    },
    description: desc,
    tagsCount: resolved.tags.length,
    tags: resolved.tags,
    videoPath: path.basename(VIDEO),
    videoSha256: videoSha,
    videoBytes: fs.statSync(VIDEO).size,
    testAndCompare: [
      { slot: 1, title: "What's Really Inside an Atom?", thumb: "A atom v04" },
      {
        slot: 2,
        title: "Why Is the Periodic Table in This Order?",
        thumb: "C hidden number v06",
      },
      { slot: 3, title: "How Small Can You Cut Gold?", thumb: "B cut gold v04" },
    ],
    studioFinish,
    stop: "No upload until Ben says yes to this dry-run.",
  };

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(result, null, 2) + "\n");
  console.log(
    JSON.stringify(
      {
        wrote: OUT,
        upload: false,
        premiere: false,
        hosEnvPresent,
        title: result.title,
        schedule: result.scheduledAt,
        privacy: result.privacy,
        tAndC: result.testAndCompare,
        captionsPresent: result.captionsPresent,
        pinnedComment: result.pinnedComment,
        endScreen: result.endScreen,
        npmApiPath: result.npmApiPath,
        studioFinishSummary: studioFinish.summary,
      },
      null,
      2,
    ),
  );
}

main();
