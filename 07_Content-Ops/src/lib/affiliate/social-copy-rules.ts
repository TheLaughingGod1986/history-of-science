/**
 * Hard constraints for affiliate mentions in social copy.
 * Not a social product — guards so affiliate-aware captions never spam or leak merchant URLs.
 */

import type { PlatformId } from "@/config/platforms";

/** Platforms that may receive at most one soft affiliate afterthought. */
export const AFFILIATE_SOCIAL_PLATFORMS = [
  "youtube_shorts",
  "tiktok",
  "instagram_reels",
  "instagram_feed",
  "facebook_reels",
  "facebook_page",
  "x",
  "threads",
] as const satisfies readonly PlatformId[];

export type AffiliateSocialPlatform = (typeof AFFILIATE_SOCIAL_PLATFORMS)[number];

export const AFFILIATE_SOCIAL_HOUSE_RULES = {
  maxSoftMentionsPerPost: 1,
  /** Sky / science first — the tool is an afterthought. */
  scienceFirst: true,
  /** Never open the post on a product or brand. */
  neverOpenOnProduct: true,
  /** Never stack multiple brands in one post. */
  neverStackBrands: true,
  /** “Links in bio” must never be the hook. */
  neverLinksInBioAsHook: true,
  /** No raw merchant / affiliate programme URLs on social. */
  noRawAffiliateUrls: true,
  /** No coupon / haul language. */
  noPromoCodesOrHaul: true,
  /**
   * Only allowed tracked destinations on social:
   * YouTube description pointer, youtube.com / youtu.be, or Orbit /go/ links.
   */
  allowedLinkHosts: ["youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com", "historyofscience.com", "www.historyofscience.com"] as const,
  allowedGoPathPrefix: "/go/",
  /** Disclose once, quietly, only where the platform requires it — never as the joke. */
  quietDisclosureOnly: true,
} as const;

/** Phrases that must never appear in affiliate-aware social copy. */
export const AFFILIATE_SOCIAL_BANNED_PHRASES = [
  "use my code",
  "use code",
  "promo code",
  "discount code",
  "% off",
  "percent off",
  "%off",
  "haul",
  "unboxing haul",
  "unboxing",
  "link in bio",
  "links in bio",
  "linkinbio",
  "link in comments",
  "links in comments",
  "swipe up to buy",
  "shop now",
  "buy now",
  "add to cart",
  "tiktok shop",
  "amazon haul",
  "sponsored haul",
  "product carousel",
  "boosted catalog",
] as const;

/** Host patterns treated as raw merchant / affiliate destinations (never emit on social). */
export const RAW_MERCHANT_HOST_PATTERNS = [
  /amazon\.(co\.uk|com|de|fr|ca|in)/i,
  /amzn\.to/i,
  /brilliant\.org/i,
  /shareasale\.com/i,
  /pjatr\.com/i,
  /gopjn\.com/i,
  /anrdoezrs\.net/i,
  /dpbolvw\.net/i,
  /jdoqocy\.com/i,
  /tkqlhce\.com/i,
  /click\.linksynergy\.com/i,
  /firstlightoptics\.com/i,
  /highpointscientific\.com/i,
  /lego\.com/i,
] as const;

export type SoftMentionSkipReason =
  | "no_natural_object"
  | "platform_already_mentioned_this_week"
  | "no_specific_film"
  | "video_not_about_product"
  | "no_placement"
  | "inactive_or_rejected"
  | "ok";

export type AffiliateSocialMentionInput = {
  platform: PlatformId;
  /** Short / clip is actually about this object (telescope, book topic, etc.). */
  hasNaturalObject: boolean;
  /** Long-form film can be named (title or YouTube URL present). */
  canNameSpecificFilm: boolean;
  /** This platform already carried an affiliate soft-mention earlier this week. */
  platformMentionedThisWeek?: boolean;
  /** Product is editorially relevant to the episode (not commission-driven). */
  productRelevantToVideo: boolean;
  /** Approved / active placement exists for this video. */
  hasApprovedPlacement: boolean;
};

/**
 * Gate: skip affiliate mentions when the short has no natural object,
 * when that platform already mentioned something this week,
 * or when you cannot name a specific film.
 */
export function shouldIncludeAffiliateSoftMention(
  input: AffiliateSocialMentionInput,
): { include: boolean; reason: SoftMentionSkipReason } {
  if (!input.hasApprovedPlacement) {
    return { include: false, reason: "no_placement" };
  }
  if (!input.productRelevantToVideo) {
    return { include: false, reason: "video_not_about_product" };
  }
  if (!input.hasNaturalObject) {
    return { include: false, reason: "no_natural_object" };
  }
  if (!input.canNameSpecificFilm) {
    return { include: false, reason: "no_specific_film" };
  }
  if (input.platformMentionedThisWeek) {
    return { include: false, reason: "platform_already_mentioned_this_week" };
  }
  return { include: true, reason: "ok" };
}

export function isAllowedSocialTrackedUrl(url: string): boolean {
  const trimmed = url.trim();
  if (!trimmed) return false;

  // Relative Orbit redirect
  if (trimmed.startsWith("/go/") || trimmed.startsWith("go/")) return true;

  try {
    const parsed = new URL(trimmed);
    const host = parsed.hostname.toLowerCase();
    if (
      (host === "historyofscience.com" || host === "www.historyofscience.com") &&
      parsed.pathname.startsWith("/go/")
    ) {
      return true;
    }
    if (
      host === "youtube.com" ||
      host === "www.youtube.com" ||
      host === "m.youtube.com" ||
      host === "youtu.be"
    ) {
      return true;
    }
    // Dev localhost /go/
    if (
      (host === "localhost" || host === "127.0.0.1") &&
      parsed.pathname.startsWith("/go/")
    ) {
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

export function containsRawMerchantUrl(text: string): boolean {
  const urlMatches = text.match(/https?:\/\/[^\s)]+/gi) || [];
  for (const raw of urlMatches) {
    if (isAllowedSocialTrackedUrl(raw)) continue;
    try {
      const host = new URL(raw).hostname;
      if (RAW_MERCHANT_HOST_PATTERNS.some((re) => re.test(host))) return true;
      // Any non-allowed absolute URL is treated as merchant leak for affiliate-aware copy
      return true;
    } catch {
      return true;
    }
  }
  // Bare amazon / brilliant without scheme
  if (/\b(amazon\.(co\.uk|com)|amzn\.to|brilliant\.org)\b/i.test(text)) return true;
  return false;
}

export function containsBannedAffiliatePhrase(text: string): boolean {
  const lower = text.toLowerCase();
  return AFFILIATE_SOCIAL_BANNED_PHRASES.some((p) => lower.includes(p));
}

/**
 * Strip / rewrite violations so stored social copy never keeps raw merchant URLs
 * or haul/code language. Returns cleaned text + list of fixes applied.
 */
export function sanitizeAffiliateSocialText(text: string): {
  text: string;
  violations: string[];
} {
  const violations: string[] = [];
  let out = text;

  const urls = out.match(/https?:\/\/[^\s)]+/gi) || [];
  for (const url of urls) {
    if (!isAllowedSocialTrackedUrl(url)) {
      violations.push(`removed_non_orbit_url:${url}`);
      out = out.replace(url, "").replace(/[ \t]+\n/g, "\n");
    }
  }

  for (const phrase of AFFILIATE_SOCIAL_BANNED_PHRASES) {
    const re = new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
    if (re.test(out)) {
      violations.push(`removed_banned_phrase:${phrase}`);
      out = out.replace(re, "");
    }
  }

  // Collapse leftover blank lines / spaces
  out = out
    .replace(/[ \t]{2,}/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();

  return { text: out, violations };
}

/** Quiet disclosure lines — never the joke, never the hook. */
export const QUIET_AFFILIATE_DISCLOSURE =
  "Some links may be affiliate links.";

export type SoftMentionStyle = "caption_tail" | "reply_only" | "none";

export function softMentionStyleForPlatform(platform: PlatformId): SoftMentionStyle {
  switch (platform) {
    case "youtube_shorts":
    case "tiktok":
      return "caption_tail";
    case "instagram_reels":
    case "instagram_feed":
      return "caption_tail";
    case "facebook_reels":
    case "facebook_page":
      return "caption_tail";
    case "x":
    case "threads":
      return "caption_tail";
    default:
      return "none";
  }
}

/**
 * Build at most one soft afterthought line.
 * Points only to YouTube description or an Orbit /go/ link — never a merchant URL.
 */
export function buildSoftAffiliateMentionLine(args: {
  platform: PlatformId;
  productLabel: string;
  /** Orbit /go/{slug} or full https://historyofscience.com/go/{slug} */
  goUrl?: string | null;
  /** Prefer pointing at the YouTube description when a film URL exists. */
  youtubeUrl?: string | null;
  includeQuietDisclosure?: boolean;
}): string | null {
  const style = softMentionStyleForPlatform(args.platform);
  if (style === "none") return null;

  const label = args.productLabel.trim();
  if (!label) return null;

  // Prefer YouTube description pointer; otherwise a single /go/ link
  let destinationNote: string;
  if (args.youtubeUrl && isAllowedSocialTrackedUrl(args.youtubeUrl)) {
    destinationNote = "details in the YouTube description";
  } else if (args.goUrl && isAllowedSocialTrackedUrl(args.goUrl)) {
    destinationNote = args.goUrl;
  } else if (args.youtubeUrl) {
    destinationNote = "details in the YouTube description";
  } else {
    return null;
  }

  // Platform-specific soft tone — science first, tool as afterthought
  let line: string;
  if (args.platform === "instagram_reels" || args.platform === "instagram_feed") {
    line = `I left the one thing under the film${args.youtubeUrl ? "" : args.goUrl ? `: ${args.goUrl}` : ""}.`;
    if (args.youtubeUrl && isAllowedSocialTrackedUrl(args.youtubeUrl)) {
      line = `I left the one thing under the film.`;
    } else if (args.goUrl && isAllowedSocialTrackedUrl(args.goUrl)) {
      line = `If you want to look at this yourself:\n${args.goUrl}`;
    }
  } else if (args.platform === "facebook_page") {
    line =
      args.goUrl && isAllowedSocialTrackedUrl(args.goUrl)
        ? `If you want to look at this yourself:\n${args.goUrl}`
        : `If you want to look at this yourself — details under the film.`;
  } else if (args.platform === "x" || args.platform === "threads") {
    line = `(For this film’s tools — ${destinationNote}.)`;
  } else if (args.platform === "tiktok" || args.platform === "youtube_shorts") {
    line = `Curious about the ${label.toLowerCase()} angle? ${destinationNote}.`;
  } else {
    line = `More on the ${label.toLowerCase()} for this film: ${destinationNote}.`;
  }

  if (args.includeQuietDisclosure) {
    line = `${line} ${QUIET_AFFILIATE_DISCLOSURE}`;
  }

  // Hard check before return
  if (containsRawMerchantUrl(line) || containsBannedAffiliatePhrase(line)) {
    return null;
  }
  return line;
}

/** True if the first non-empty line looks like a product/brand open. */
export function opensOnProductOrBrand(text: string, productOrBrandNames: string[]): boolean {
  const first = text
    .split(/\n/)
    .map((l) => l.trim())
    .find((l) => l.length > 0);
  if (!first) return false;
  const lower = first.toLowerCase();
  if (/^link(s)? in bio/i.test(first)) return true;
  if (/^(shop|buy|check out|use my code|sponsored)/i.test(first)) return true;
  return productOrBrandNames.some((n) => n && lower.startsWith(n.toLowerCase()));
}
