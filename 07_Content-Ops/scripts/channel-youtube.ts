/**
 * History of Science's half of the shared YouTube scripts (studio core, Ben 15 Oct 2026: "unify HOS and OWB but
 * keeping their own rules"). Core scripts (retitle-videos.ts, update-pinned-comment.ts, youtube-package-upload.ts)
 * import these hooks; each repo keeps its own copy of this file, so how a channel signs in, guards its desk and what
 * it does around an upload stays the channel's own.
 */
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

/** HOS has no upload flags of its own. */
export const UPLOAD_FLAGS = "";

type UploadHookInput = { resolved: ResolvedYouTubePackage; flag: (name: string) => boolean; repoRoot: string };

/** Checks 07_Content-Ops/.env before anything is sent (as the HOS upload always did). */
export async function beforeUpload(input: UploadHookInput): Promise<Record<string, unknown>> {
  void input;
  const { getEnv } = await import("../src/lib/env");
  getEnv();
  return {};
}

/** Nothing after the upload on HOS: no uploads registry and no Buffer mirror from this script. */
export async function afterUpload(
  input: UploadHookInput & { videoId: string; identity: Record<string, unknown> },
): Promise<Record<string, unknown>> {
  void input;
  return {};
}
