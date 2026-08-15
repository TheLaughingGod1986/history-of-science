/**
 * Honest labels from existing LongFormVideo fields only.
 *
 * Video Auditor:
 * - /videos is a film list forever — never /go/, Amazon, or a shop module here.
 * - Named-in-film (if marked): only `Named: {book title}` — no slug, no link.
 * - Shorts never get a book line.
 * - last-star v09 (`dbBojuwg4r8`) is private — never treat as live/next Thursday.
 */

/** Auditor-confirmed named-in-film long (last-star only). Book title text — no /go/. */
const NAMED_IN_FILM_BY_YOUTUBE_ID: Record<string, string> = {
  "z-fUtdjWn5o": "The End of Everything",
};

/** Private cut — must not win “next Thursday” / “this film”. */
const PRIVATE_NOT_NEXT_YOUTUBE_IDS = new Set(["dbBojuwg4r8"]);

const LAST_STAR_V10_MARK = "last-star_v10";

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
 * Visible commerce on /videos: none (Film-only), aside from optional Named title text.
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

function looksLikeLastStarV10(video: {
  workingTitle?: string | null;
  title?: string | null;
  slug?: string | null;
  projectFolder?: string | null;
  finalVideoPath?: string | null;
}): boolean {
  const hay = [
    video.workingTitle,
    video.title,
    video.slug,
    video.projectFolder,
    video.finalVideoPath,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
  return hay.includes(LAST_STAR_V10_MARK);
}

/**
 * Auditor named-in-film mark for last-star only (`z-fUtdjWn5o` / last-star_v10).
 * Returns `Named: The End of Everything` or null. Never a slug or link.
 */
export function namedInFilmBookLine(video: {
  youtubeVideoId: string | null;
  youtubeUrl: string | null;
  workingTitle?: string | null;
  title?: string | null;
  slug?: string | null;
  projectFolder?: string | null;
  finalVideoPath?: string | null;
}): string | null {
  const ytId = resolveYoutubeId(video);
  if (ytId && NAMED_IN_FILM_BY_YOUTUBE_ID[ytId]) {
    return `Named: ${NAMED_IN_FILM_BY_YOUTUBE_ID[ytId]}`;
  }
  // Fallback only when YouTube id is missing on the record.
  if (!ytId && looksLikeLastStarV10(video)) {
    return "Named: The End of Everything";
  }
  return null;
}

/** True when this cut must not be the next/this Thursday hero (e.g. private last-star v09). */
export function excludeFromNextThursdayHero(video: {
  youtubeVideoId: string | null;
  youtubeUrl: string | null;
}): boolean {
  const ytId = resolveYoutubeId(video);
  return Boolean(ytId && PRIVATE_NOT_NEXT_YOUTUBE_IDS.has(ytId));
}
