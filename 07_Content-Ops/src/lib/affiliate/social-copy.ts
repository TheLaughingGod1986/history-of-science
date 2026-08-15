/**
 * Apply affiliate house rules to existing platform social copy.
 * Does not invent a new social product — only soft-constrains captions
 * when placements exist beside Shorts / social generation.
 */

import type { PlatformCopy } from "@/lib/platforms/generate-platform-copy";
import type { PlatformId } from "@/config/platforms";
import { buildOrbitRedirectUrl } from "./urls";
import {
  buildSoftAffiliateMentionLine,
  containsBannedAffiliatePhrase,
  containsRawMerchantUrl,
  opensOnProductOrBrand,
  sanitizeAffiliateSocialText,
  shouldIncludeAffiliateSoftMention,
  softMentionStyleForPlatform,
  type SoftMentionSkipReason,
} from "./social-copy-rules";

export type AffiliateSocialContext = {
  /** Human label for the single allowed soft mention (e.g. "beginner telescope"). */
  productLabel: string;
  productSlug: string;
  brandNames?: string[];
  /** Programme / product is actually what the short is about. */
  hasNaturalObject: boolean;
  productRelevantToVideo: boolean;
  hasApprovedPlacement: boolean;
  youtubeUrl?: string | null;
  longTitle?: string | null;
  /** Platforms that already soft-mentioned affiliate this calendar week. */
  platformsMentionedThisWeek?: PlatformId[];
  /** When true, append quiet disclosure on platforms that expect it (IG/TikTok captions). */
  includeQuietDisclosure?: boolean;
  /** Prefer /go/ over “YouTube description” pointer when both exist. Default: prefer YT description. */
  preferGoLink?: boolean;
};

export type AffiliateSocialApplicationResult = {
  copies: PlatformCopy[];
  mentionsByPlatform: Partial<
    Record<PlatformId, { included: boolean; reason: SoftMentionSkipReason }>
  >;
  sanitizationViolations: string[];
};

function canNameFilm(ctx: AffiliateSocialContext): boolean {
  return Boolean(
    (ctx.youtubeUrl && ctx.youtubeUrl.trim()) || (ctx.longTitle && ctx.longTitle.trim()),
  );
}

function appendCaptionTail(caption: string, line: string, maxLen?: number): string {
  const merged = `${caption.trimEnd()}\n\n${line}`.trim();
  if (maxLen && merged.length > maxLen) {
    return caption.trimEnd();
  }
  return merged;
}

/**
 * Sanitize all copy fields, then optionally append one soft affiliate afterthought
 * (never as the hook, never raw merchant URLs, never stacked brands).
 */
export function applyAffiliateSocialConstraints(
  copies: PlatformCopy[],
  ctx: AffiliateSocialContext | null | undefined,
): AffiliateSocialApplicationResult {
  const sanitizationViolations: string[] = [];
  const brandNames = [
    ...(ctx?.brandNames || []),
    ctx?.productLabel,
    "Amazon",
    "Brilliant",
    "LEGO",
  ].filter((x): x is string => Boolean(x));

  const cleaned = copies.map((copy) => {
    const next: PlatformCopy = { ...copy, notes: [...copy.notes] };

    const applyField = (value: string | undefined, field: string): string | undefined => {
      if (typeof value !== "string" || !value) return value;
      const { text, violations } = sanitizeAffiliateSocialText(value);
      sanitizationViolations.push(
        ...violations.map((v) => `${copy.platform}.${field}:${v}`),
      );
      return text;
    };

    next.caption = applyField(next.caption, "caption") || "";
    next.title = applyField(next.title, "title");
    next.callToAction = applyField(next.callToAction, "callToAction") || next.callToAction;
    next.pinnedComment = applyField(next.pinnedComment, "pinnedComment");
    next.coverText = applyField(next.coverText, "coverText");
    next.storyCaption = applyField(next.storyCaption, "storyCaption");
    next.commentPrompt = applyField(next.commentPrompt, "commentPrompt");

    if (next.alternatives?.length) {
      next.alternatives = next.alternatives.map((alt) => {
        const { text, violations } = sanitizeAffiliateSocialText(alt);
        sanitizationViolations.push(
          ...violations.map((v) => `${copy.platform}.alternatives:${v}`),
        );
        return text;
      });
    }

    if (opensOnProductOrBrand(next.caption, brandNames)) {
      sanitizationViolations.push(`${copy.platform}.caption:opened_on_product`);
      const lines = next.caption.split("\n");
      next.caption = lines.slice(1).join("\n").trim() || next.caption;
    }

    next.notes = [
      ...next.notes,
      "Affiliate social: max one soft mention; sky/science first; YouTube or /go/ only — never raw merchant URLs.",
    ];
    return next;
  });

  const mentionsByPlatform: AffiliateSocialApplicationResult["mentionsByPlatform"] = {};

  if (!ctx) {
    return { copies: cleaned, mentionsByPlatform, sanitizationViolations };
  }

  const goUrl = buildOrbitRedirectUrl(ctx.productSlug);
  const preferGo = Boolean(ctx.preferGoLink);

  const withMentions = cleaned.map((copy) => {
    const gate = shouldIncludeAffiliateSoftMention({
      platform: copy.platform,
      hasNaturalObject: ctx.hasNaturalObject,
      canNameSpecificFilm: canNameFilm(ctx),
      platformMentionedThisWeek: ctx.platformsMentionedThisWeek?.includes(copy.platform),
      productRelevantToVideo: ctx.productRelevantToVideo,
      hasApprovedPlacement: ctx.hasApprovedPlacement,
    });
    mentionsByPlatform[copy.platform] = {
      included: gate.include,
      reason: gate.reason,
    };
    if (!gate.include) {
      copy.notes.push(`Affiliate soft mention skipped (${gate.reason}).`);
      return copy;
    }

    if (softMentionStyleForPlatform(copy.platform) !== "caption_tail") {
      return copy;
    }

    const needsDisclosure =
      ctx.includeQuietDisclosure === true &&
      (copy.platform === "instagram_reels" || copy.platform === "tiktok");

    let resolvedLine = buildSoftAffiliateMentionLine({
      platform: copy.platform,
      productLabel: ctx.productLabel,
      goUrl: preferGo ? goUrl : null,
      youtubeUrl: preferGo ? null : ctx.youtubeUrl,
      includeQuietDisclosure: needsDisclosure,
    });

    if (!resolvedLine) {
      resolvedLine = buildSoftAffiliateMentionLine({
        platform: copy.platform,
        productLabel: ctx.productLabel,
        goUrl,
        youtubeUrl: null,
        includeQuietDisclosure: needsDisclosure,
      });
    }

    if (!resolvedLine) {
      mentionsByPlatform[copy.platform] = {
        included: false,
        reason: "no_specific_film",
      };
      copy.notes.push("Affiliate soft mention skipped (no allowed destination).");
      return copy;
    }

    if (copy.platform === "tiktok" || copy.platform === "youtube_shorts") {
      if (copy.coverText && /https?:\/\//i.test(copy.coverText)) {
        copy.coverText = sanitizeAffiliateSocialText(copy.coverText).text;
      }
      copy.notes.push(
        "Shorts/TikTok: affiliate only in caption tail — no spoken link list, no URL on screen, no TikTok Shop.",
      );
    }

    if (copy.platform === "instagram_reels") {
      copy.notes.push(
        "IG Reels: mention stays in caption (or reply if asked); sticker/bio → YouTube or /go/, never a merchant.",
      );
    }

    if (copy.platform === "x" || copy.platform === "threads") {
      copy.notes.push(
        "X/Threads: post is the thought; one soft line only — links solely to youtube.com or /go/.",
      );
    }

    copy.caption = appendCaptionTail(copy.caption, resolvedLine);
    copy.notes.push("Affiliate soft mention: one afterthought line (science first).");
    return copy;
  });

  return {
    copies: withMentions,
    mentionsByPlatform,
    sanitizationViolations,
  };
}

/**
 * Assert text is safe to store beside an affiliate placement.
 * Throws if residual merchant URLs or banned promo language remain.
 */
export function assertAffiliateSafeSocialCopy(text: string): void {
  if (containsRawMerchantUrl(text) || containsBannedAffiliatePhrase(text)) {
    throw new Error(
      "Affiliate social copy violates house rules: raw merchant URL or promo/haul language is not allowed on social",
    );
  }
}

/** True when text is already safe (no merchant URLs / haul language). */
export function isAffiliateSafeSocialCopy(text: string): boolean {
  return !containsRawMerchantUrl(text) && !containsBannedAffiliatePhrase(text);
}
