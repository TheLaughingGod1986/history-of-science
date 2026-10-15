/**
 * History of Science's half of the shared YouTube scripts (studio core, Ben 15 Oct 2026: "unify HOS and OWB but
 * keeping their own rules"). Core scripts (retitle-videos.ts, update-pinned-comment.ts) import these three hooks; each
 * repo keeps its own copy of this file, so how a channel signs in and guards its desk stays the channel's own.
 */
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
