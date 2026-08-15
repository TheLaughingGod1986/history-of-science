/**
 * Social Media Manager copy patterns — fixtures + deterministic templates
 * for affiliate-aware live-channel snippets (Threads, Instagram, Facebook Page).
 *
 * House rules still apply: max one soft mention, never open on a product,
 * tracked URLs = youtube.com / youtu.be / Orbit /go/ only.
 */

export type SocialSnippetPostStyle = "thursday_film" | "how_to";

export type SocialSnippetTemplateVars = {
  /** Line 1 — the wonder. Never a product. */
  wonder: string;
  /** Optional middle line(s) — what Orbit shows / context. */
  body?: string | null;
  /** YouTube film URL or Orbit /go/{slug} — the only door. */
  doorUrl: string;
  /** Soft product label for how-to tone (never line 1). */
  productLabel?: string | null;
};

/** Exact Thursday-film Facebook Page example (JWST) from Social Media Manager. */
export const FIXTURE_FACEBOOK_PAGE_THURSDAY_FILM = {
  wonder: "JWST keeps finding galaxies that should not be there yet.",
  body: "Orbit walks through what the pictures actually show, and what they do not.",
  softLine:
    "Film is up. If you want the one explainer I used, it is under the film.",
  doorPlaceholder: "[YouTube film URL]",
  captionWithoutUrl: [
    "JWST keeps finding galaxies that should not be there yet.",
    "",
    "Orbit walks through what the pictures actually show, and what they do not.",
    "",
    "Film is up. If you want the one explainer I used, it is under the film.",
  ].join("\n"),
} as const;

/** Exact how-to / telescope Facebook Page example from Social Media Manager. */
export const FIXTURE_FACEBOOK_PAGE_HOWTO = {
  wonder: "I spent a night on this patch of sky. This is what it looked like.",
  softLineWithFilm:
    "If you want that kind of view, I left the one I use under the film. I get a small cut if you grab it.",
  softLineWithoutFilm:
    "If you want that kind of view, I left the one I use here. I get a small cut if you grab it.",
  ctaWithFilm: "Watch the film first.",
  doorPlaceholderFilm: "[YouTube film URL]",
  doorPlaceholderGo: "[https://orbit…/go/telescope]",
  captionWithFilmWithoutUrl: [
    "I spent a night on this patch of sky. This is what it looked like.",
    "",
    "If you want that kind of view, I left the one I use under the film. I get a small cut if you grab it.",
    "",
    "Watch the film first.",
  ].join("\n"),
} as const;

/**
 * Honest comment reply when someone asks “what telescope?” —
 * one reply, film description or /go/, disclose once, stop.
 */
export const FIXTURE_COMMENT_REPLY_TELESCOPE = {
  withFilm:
    "I left the one I use under the film (description). Some links are affiliate.",
  withoutFilm:
    "I left the one I use here: {{doorUrl}} — some links are affiliate.",
} as const;

/** Soft lines used by generators (never line 1). */
export const SOCIAL_SOFT_LINES = {
  thursdayFilmUnderFilm:
    "Film is up. If you want the one explainer I used, it is under the film.",
  thursdayFilmGoOnly:
    "Film context above. If you want the one explainer I used:",
  howtoUnderFilm:
    "If you want that kind of view, I left the one I use under the film. I get a small cut if you grab it.",
  howtoGoOnly:
    "If you want that kind of view, I left the one I use here. I get a small cut if you grab it.",
  howtoWatchFirst: "Watch the film first.",
  threadsExtraUnderFilm: "I left the one thing under the film.",
  threadsExtraGo: "If you want to look at this yourself:",
  reelsCaptionUnderFilm: "I left the one thing under the film.",
  reelsCaptionGo: "If you want to look at this yourself:",
  bodyFallback: (topic: string, title: string) =>
    `Orbit walks through what the pictures actually show for ${topic} — and what they do not. (“${title}”)`,
} as const;

/**
 * Phrases / patterns that must never appear on the Facebook Page feed
 * (reject in generator + tests). Extends general affiliate bans.
 */
export const FACEBOOK_PAGE_NEVER_PHRASES = [
  "shop now",
  "shop today",
  "buy now",
  "add to cart",
  "use my code",
  "use code",
  "promo code",
  "discount code",
  "% off",
  "percent off",
  "haul",
  "unboxing",
  "link in comments",
  "links in comments",
  "link in bio",
  "links in bio",
  "product carousel",
  "boosted catalog",
  "boost this as",
  "store tab",
  "product tag",
  "amazon associate",
  "swipe up to buy",
  "tiktok shop",
] as const;

/**
 * Render Facebook Page feed caption (3–5 short lines).
 * First line = wonder. Soft mention never in line 1. Last line = door URL.
 */
export function renderFacebookPageTemplate(args: {
  style: SocialSnippetPostStyle;
  wonder: string;
  body?: string | null;
  doorUrl: string;
  /** When false and how-to: door is /go/ only (no “Watch the film first”). */
  hasFilmThisWeek: boolean;
  includeSoftMention: boolean;
}): string {
  const wonder = args.wonder.trim();
  const body = args.body?.trim() || null;
  const door = args.doorUrl.trim();
  const lines: string[] = [wonder];

  if (args.style === "thursday_film") {
    if (body) {
      lines.push("", body);
    }
    if (args.includeSoftMention) {
      lines.push(
        "",
        args.hasFilmThisWeek
          ? SOCIAL_SOFT_LINES.thursdayFilmUnderFilm
          : SOCIAL_SOFT_LINES.thursdayFilmGoOnly,
      );
    } else if (args.hasFilmThisWeek) {
      lines.push("", "Film is up.");
    }
    lines.push(door);
  } else {
    // how_to
    if (args.includeSoftMention) {
      lines.push(
        "",
        args.hasFilmThisWeek
          ? SOCIAL_SOFT_LINES.howtoUnderFilm
          : SOCIAL_SOFT_LINES.howtoGoOnly,
      );
      if (args.hasFilmThisWeek) {
        lines.push("", SOCIAL_SOFT_LINES.howtoWatchFirst);
      }
    } else if (args.hasFilmThisWeek) {
      lines.push("", SOCIAL_SOFT_LINES.howtoWatchFirst);
    }
    lines.push(door);
  }

  return lines.join("\n").trim();
}

/**
 * Instagram feed uses the same documentary caption shape as Facebook Page.
 */
export function renderInstagramFeedTemplate(args: {
  style: SocialSnippetPostStyle;
  wonder: string;
  body?: string | null;
  doorUrl: string;
  hasFilmThisWeek: boolean;
  includeSoftMention: boolean;
}): string {
  return renderFacebookPageTemplate(args);
}

/**
 * Threads: thought first, one extra line, one link (YouTube or /go/).
 * Never a product thread. Soft mention never line 1. /go/ never line 1.
 */
export function renderThreadsTemplate(args: {
  wonder: string;
  doorUrl: string;
  includeSoftMention: boolean;
  doorIsGo: boolean;
}): string {
  const wonder = args.wonder.trim();
  const door = args.doorUrl.trim();
  if (!args.includeSoftMention) {
    return `${wonder}\n\n${door}`;
  }
  if (args.doorIsGo) {
    return `${wonder}\n\n${SOCIAL_SOFT_LINES.threadsExtraGo}\n${door}`;
  }
  return `${wonder}\n\n${SOCIAL_SOFT_LINES.threadsExtraUnderFilm}\n${door}`;
}

/**
 * IG Reels: science thought + soft mention in caption only.
 * Door URL at end (YouTube or /go/). Never /go/ on line 1.
 */
export function renderInstagramReelsTemplate(args: {
  wonder: string;
  doorUrl: string;
  includeSoftMention: boolean;
  doorIsGo: boolean;
}): string {
  const wonder = args.wonder.trim();
  const door = args.doorUrl.trim();
  if (!args.includeSoftMention) {
    return `${wonder}\n\nFull film:\n${door}`;
  }
  if (args.doorIsGo) {
    return `${wonder}\n\n${SOCIAL_SOFT_LINES.reelsCaptionGo}\n${door}`;
  }
  return `${wonder}\n\n${SOCIAL_SOFT_LINES.reelsCaptionUnderFilm}\n${door}`;
}

/** Build comment-reply fixture text (disclose once, stop). */
export function renderTelescopeCommentReply(args: {
  doorUrl?: string | null;
  hasFilm: boolean;
}): string {
  if (args.hasFilm) return FIXTURE_COMMENT_REPLY_TELESCOPE.withFilm;
  const url = args.doorUrl?.trim() || "https://orbitwithben.com/go/telescope";
  return FIXTURE_COMMENT_REPLY_TELESCOPE.withoutFilm.replace("{{doorUrl}}", url);
}

/**
 * Count non-empty lines (Facebook Page target: 3–5 short lines + door).
 * Door URL counts as the last line.
 */
export function countCaptionLines(caption: string): number {
  return caption
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean).length;
}

export function firstNonEmptyLine(caption: string): string {
  return (
    caption
      .split("\n")
      .map((l) => l.trim())
      .find((l) => l.length > 0) || ""
  );
}

export function lastNonEmptyLine(caption: string): string {
  const lines = caption
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean);
  return lines[lines.length - 1] || "";
}
