/**
 * Deterministic affiliate-aware social snippets for live Orbit channels:
 * Threads, Instagram (Reels + feed), Facebook Page.
 * Never emits raw merchant URLs. Approval required before publish.
 */

import { PLATFORMS, type PlatformId } from "@/config/platforms";
import {
  AFFILIATE_LIVE_SOCIAL_PLATFORMS,
  socialPlatformToClickSource,
  type AffiliateLiveSocialPlatform,
} from "./social-channels";
import {
  buildSocialGoUrl,
  buildSocialYouTubeUrl,
} from "./urls";
import {
  containsBannedAffiliatePhrase,
  containsRawMerchantUrl,
  shouldIncludeAffiliateSoftMention,
} from "./social-copy-rules";
import { assertAffiliateSafeSocialCopy } from "./social-copy";

export type AffiliateSocialSnippetInput = {
  videoSlug: string;
  videoTitle: string;
  topic: string;
  hook?: string | null;
  youtubeUrl?: string | null;
  productLabel: string;
  productSlug: string;
  hasNaturalObject: boolean;
  productRelevantToVideo: boolean;
  hasApprovedPlacement: boolean;
  /** Platforms already used this week for soft mentions. */
  platformsMentionedThisWeek?: PlatformId[];
  /**
   * Prefer pointing at YouTube (“under the film”) vs embedding /go/.
   * Default true for Shorts/Reels; Facebook Page may use /go/ at the end.
   */
  preferYouTubePointer?: boolean;
};

export type AffiliateSocialSnippet = {
  platform: AffiliateLiveSocialPlatform;
  label: string;
  caption: string;
  /** Tracked URL embedded in the caption, if any (YouTube or /go/ only). */
  trackedUrl: string | null;
  clickSource: ReturnType<typeof socialPlatformToClickSource>;
  includeAffiliateMention: boolean;
  skipReason?: string;
  /** Must stay false until editor approves — never auto-post. */
  approvedForPublish: false;
  notes: string[];
};

function truncate(s: string, max: number): string {
  if (s.length <= max) return s;
  return s.slice(0, max - 1).trimEnd() + "…";
}

function filmThought(input: AffiliateSocialSnippetInput): string {
  return (
    input.hook?.trim() ||
    `A calm look at ${input.topic} — from our film “${input.videoTitle}”.`
  );
}

/**
 * Generate copy-ready snippets for Threads, Instagram Reels, Instagram Feed, Facebook Page.
 * Distinct from facebook_reels. Respects house rules + editorial soft-mention gate.
 */
export function generateAffiliateSocialSnippets(
  input: AffiliateSocialSnippetInput,
): AffiliateSocialSnippet[] {
  return AFFILIATE_LIVE_SOCIAL_PLATFORMS.map((platform) =>
    buildSnippetForPlatform(platform, input),
  );
}

function buildSnippetForPlatform(
  platform: AffiliateLiveSocialPlatform,
  input: AffiliateSocialSnippetInput,
): AffiliateSocialSnippet {
  const gate = shouldIncludeAffiliateSoftMention({
    platform,
    hasNaturalObject: input.hasNaturalObject,
    canNameSpecificFilm: Boolean(input.youtubeUrl || input.videoTitle),
    platformMentionedThisWeek: input.platformsMentionedThisWeek?.includes(platform),
    productRelevantToVideo: input.productRelevantToVideo,
    hasApprovedPlacement: input.hasApprovedPlacement,
  });

  const preferYt = input.preferYouTubePointer !== false;
  const clickSource = socialPlatformToClickSource(platform);
  const notes: string[] = [
    "Affiliate social: max one soft mention; never raw merchant URLs.",
    "Requires the same approval flow as description placements before publish.",
  ];

  const thought = filmThought(input);
  let caption = thought;
  let trackedUrl: string | null = null;
  let includeAffiliateMention = false;

  if (!gate.include) {
    // Still allow a non-affiliate YouTube pointer (utm_medium=social)
    if (input.youtubeUrl) {
      trackedUrl = buildSocialYouTubeUrl({
        youtubeUrl: input.youtubeUrl,
        platform,
        videoSlug: input.videoSlug,
        hasAffiliateMention: false,
      });
      caption = appendLink(platform, thought, trackedUrl, false, input);
    }
    notes.push(`Affiliate soft mention skipped (${gate.reason}).`);
  } else {
    includeAffiliateMention = true;
    if (preferYt && input.youtubeUrl) {
      trackedUrl = buildSocialYouTubeUrl({
        youtubeUrl: input.youtubeUrl,
        platform,
        videoSlug: input.videoSlug,
        productSlug: input.productSlug,
        hasAffiliateMention: true,
      });
      caption = appendAffiliateLine(platform, thought, trackedUrl, input, "youtube");
    } else {
      trackedUrl = buildSocialGoUrl({
        productSlug: input.productSlug,
        platform,
        videoSlug: input.videoSlug,
        hasAffiliateMention: true,
      });
      caption = appendAffiliateLine(platform, thought, trackedUrl, input, "go");
    }
    notes.push(platformNotes(platform));
  }

  const max = PLATFORMS[platform].maxCaptionLength || 2200;
  caption = truncate(caption, max);

  assertAffiliateSafeSocialCopy(caption);
  if (containsRawMerchantUrl(caption) || containsBannedAffiliatePhrase(caption)) {
    // Fail closed — science thought only
    caption = truncate(thought, max);
    trackedUrl = null;
    includeAffiliateMention = false;
    notes.push("Stripped unsafe URL/language — fell back to science-only caption.");
  }

  return {
    platform,
    label: PLATFORMS[platform].label,
    caption,
    trackedUrl,
    clickSource,
    includeAffiliateMention,
    skipReason: gate.include ? undefined : gate.reason,
    approvedForPublish: false,
    notes,
  };
}

function platformNotes(platform: AffiliateLiveSocialPlatform): string {
  switch (platform) {
    case "threads":
      return "Threads: the post is the thought; one soft line; links only to youtube.com or /go/.";
    case "instagram_reels":
      return "IG Reels: mention in caption only — not spoken link list; sticker/bio → YouTube or /go/.";
    case "instagram_feed":
      return "IG Feed: one caption soft mention; never merchant stickers.";
    case "facebook_page":
      return "Facebook Page: documentary feed post — one optional /go/ or YouTube link at the end. No shop now.";
    default:
      return "";
  }
}

function appendLink(
  platform: AffiliateLiveSocialPlatform,
  thought: string,
  url: string,
  affiliate: boolean,
  input: AffiliateSocialSnippetInput,
): string {
  if (platform === "facebook_page") {
    return `${thought}\n\nFull film:\n${url}`;
  }
  if (platform === "threads") {
    return truncate(`${thought}\n\n${url}`, PLATFORMS.threads.maxCaptionLength || 500);
  }
  if (platform === "instagram_reels" || platform === "instagram_feed") {
    return affiliate
      ? `${thought}\n\nI left the one thing under the film.\n${url}`
      : `${thought}\n\nFull film:\n${url}`;
  }
  return `${thought}\n\n${url}`;
}

function appendAffiliateLine(
  platform: AffiliateLiveSocialPlatform,
  thought: string,
  url: string,
  input: AffiliateSocialSnippetInput,
  mode: "youtube" | "go",
): string {
  const label = input.productLabel.toLowerCase();
  if (platform === "facebook_page") {
    // Documentary feed — link only at the end, no shop energy
    const soft =
      mode === "youtube"
        ? `If you want to look at this yourself, I left the ${label} under the film.`
        : `If you want to look at this yourself:`;
    return `${thought}\n\n${soft}\n${url}`;
  }
  if (platform === "threads") {
    const soft =
      mode === "youtube"
        ? `(I left the one thing under the film.)`
        : `(If you want to look at this yourself — ${url})`;
    const body =
      mode === "youtube" ? `${thought}\n\n${soft}\n${url}` : `${thought}\n\n${soft}`;
    return truncate(body, PLATFORMS.threads.maxCaptionLength || 500);
  }
  // Instagram Reels + feed
  const soft =
    mode === "youtube"
      ? `I left the one thing under the film.`
      : `If you want to look at this yourself:`;
  return `${thought}\n\n${soft}\n${url}`;
}

/** Platforms required by Ben’s live-channel brief (for UI). */
export function affiliateLiveSocialPlatformIds(): AffiliateLiveSocialPlatform[] {
  return [...AFFILIATE_LIVE_SOCIAL_PLATFORMS];
}
