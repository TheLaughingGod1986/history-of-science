/** Honest labels from existing LongFormVideo fields only — no commerce, no invented privacy. */

export function resolveYoutubeId(video: {
  youtubeVideoId: string | null;
  youtubeUrl: string | null;
}): string | null {
  const stored = video.youtubeVideoId?.trim();
  if (stored) return stored;
  const url = video.youtubeUrl?.trim();
  if (!url) return null;
  try {
    const u = new URL(url);
    if (u.hostname.includes("youtu.be")) {
      const id = u.pathname.replace(/^\//, "").split("/")[0];
      return id || null;
    }
    const v = u.searchParams.get("v");
    if (v) return v;
  } catch {
    return null;
  }
  return null;
}

/**
 * One-line Auditor status. We have no privacy field on LongFormVideo —
 * never claim "private" or "live" without status=published.
 * Commerce is always absent on this page (Film-only).
 */
export function auditorFilmStatusLine(video: {
  status: string;
  youtubeVideoId: string | null;
  youtubeUrl: string | null;
}): string {
  if (video.status === "published") return "Long · Film-only · Published";
  if (video.status === "scheduled") return "Long · Film-only · Scheduled";
  // Has a YouTube id/URL or not — still not published in our records; do not invent privacy.
  return "Long · Film-only · Not published";
}
