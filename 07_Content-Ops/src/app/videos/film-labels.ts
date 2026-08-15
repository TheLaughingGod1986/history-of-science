/**
 * Honest labels from existing LongFormVideo fields only.
 *
 * Video Auditor (15 Aug 2026):
 * - /videos is a film list forever — never /go/, Amazon, or a shop module here,
 *   even after a book is marked named-in-film elsewhere.
 * - If a verified named-in-film mark exists later, the only extra line is
 *   `Named: {book title}` — no slug, no link.
 * - As of 15 Aug 2026 Auditor marked ZERO films named-in-film. LongFormVideo
 *   has no named-in-film field — do not invent Named rows from topic/quotes.
 * - Shorts never get a book line.
 */

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
 * One-line Auditor status. No privacy field on LongFormVideo —
 * never claim "private" or "live" without status=published.
 * Visible commerce on /videos: none (Film-only).
 */
export function auditorFilmStatusLine(video: {
  status: string;
  youtubeVideoId: string | null;
  youtubeUrl: string | null;
}): string {
  if (video.status === "published") return "Long · Film-only · Published";
  if (video.status === "scheduled") return "Long · Film-only · Scheduled";
  return "Long · Film-only · Not published";
}

/**
 * Optional Auditor line when a verified named-in-film book title exists.
 * Returns null until LongFormVideo gains a real named-in-film field that is set.
 * Never invent from topic, quotes (“Where is everybody?”), or affiliate maps.
 */
export function namedInFilmBookLine(video: { id: string }): string | null {
  void video;
  // No named-in-film column on LongFormVideo (Auditor 15 Aug 2026: zero films marked).
  return null;
}
