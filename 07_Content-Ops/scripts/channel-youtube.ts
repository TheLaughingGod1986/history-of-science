/**
 * History of Science's half of the shared YouTube scripts (studio core, Ben 15 Oct 2026: "unify HOS and OWB but
 * keeping their own rules"). Core scripts (retitle-videos.ts, update-pinned-comment.ts, youtube-package-upload.ts)
 * import these hooks; each repo keeps its own copy of this file, so how a channel signs in, guards its desk and what
 * it does around an upload stays the channel's own.
 */
import path from "path";
import type { ResolvedYouTubePackage } from "../src/lib/publishing/youtube-package";
import type { ChannelUpload } from "../src/lib/youtube/upload";

export function beforeRun(): void {
  // No desk lock on HOS: its desk guard is 00_Brand/Channel-Setup/tools/hos_desk.py.
}

export async function youtubeAccessToken(): Promise<string> {
  // Retries an "expired" row that still has a refresh token, and explains invalid_grant.
  const { youtubeAccessToken } = await import("../src/lib/publishing/youtube-token");
  return youtubeAccessToken();
}

export async function afterRun(): Promise<void> {
  const { prisma } = await import("../src/lib/storage/prisma");
  await prisma.$disconnect();
}

/** HOS release contract (hos-contract/rules.ts): Education, British English title and audio. */
export const UPLOAD: ChannelUpload = { categoryId: "27", defaultLanguage: "en-GB" };

/**
 * --no-buffer: skip Orbit social/hos registration (J1202).
 * --standalone: Short with no long (rare; HOS Shorts normally promote a long).
 */
export const UPLOAD_FLAGS = "[--no-buffer] [--standalone]";

type UploadHookInput = { resolved: ResolvedYouTubePackage; flag: (name: string) => boolean; repoRoot: string };

/** Checks 07_Content-Ops/.env before anything is sent (as the HOS upload always did). */
export async function beforeUpload(input: UploadHookInput): Promise<Record<string, unknown>> {
  void input;
  const { getEnv } = await import("../src/lib/env");
  getEnv();
  return {};
}

/**
 * After a live Short upload (J1202): register the master mp4 + long id into Orbit
 * `00_Brand/Channel-Setup/social/hos/UPLOADS.json` so `buffer-mirror.ts check --channel hos`
 * can schedule Buffer when the Short is Public/scheduled. Does not post to Buffer from this hook.
 * Longs: nothing (HOS never cross-posts longs).
 */
export async function afterUpload(
  input: UploadHookInput & { videoId: string; identity: Record<string, unknown> },
): Promise<{ buffer: Record<string, unknown> | null }> {
  const { resolved, flag, videoId, repoRoot } = input;
  if (resolved.format !== "shorts") return { buffer: null };
  if (flag("no-buffer")) return { buffer: { skipped: true, reason: "--no-buffer" } };

  try {
    const { registerHosShortForBuffer } = await import("../src/lib/publishing/hos-buffer-register");
    const longId = resolved.relatedVideoId ?? null;
    if (!longId && !flag("standalone")) {
      console.error(
        `HOS Buffer register skipped for ${videoId}: Short has no relatedVideoId. ` +
          `Re-run with --standalone, or: cd ../orbit-with-ben/07_Content-Ops && npx tsx scripts/buffer-mirror.ts register --channel hos --video ${videoId} --media <mp4> --long <longId>`,
      );
      return {
        buffer: {
          registered: false,
          errors: ["Short has no relatedVideoId; pass --standalone or set relatedVideoId in the package"],
        },
      };
    }
    const result = registerHosShortForBuffer({
      hosRepoRoot: repoRoot,
      videoId,
      mediaPath: resolved.videoPath,
      longId,
      standalone: flag("standalone") || undefined,
      social: resolved.social ?? null,
    });
    console.log(
      `HOS Buffer: registered ${videoId} in ${path.relative(repoRoot, result.uploadsFile) || result.uploadsFile} ` +
        `(sha256 ${result.entry.sha256.slice(0, 12)}…). Daily check --channel hos will mirror when Public/scheduled; nothing posted now.`,
    );
    return {
      buffer: {
        registered: true,
        uploadsFile: result.uploadsFile,
        sha256: result.entry.sha256,
        deferred: "registered for daily check --channel hos (no post from upload hook)",
      },
    };
  } catch (e) {
    const message = (e as Error).message;
    console.error(
      `HOS Buffer register incomplete for ${videoId}: ${message}. ` +
        `Fix, then: cd ../orbit-with-ben/07_Content-Ops && npx tsx scripts/buffer-mirror.ts register --channel hos --video ${videoId} --media <mp4> --long <longId>`,
    );
    return { buffer: { registered: false, errors: [message] } };
  }
}
