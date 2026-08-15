import { getEnv } from "@/lib/env";

/**
 * Resolve affiliate IDs from env / admin config.
 * Never hard-code real affiliate IDs in source or seed.
 */
export function getAmazonAssociateTag(): string | null {
  return process.env.AMAZON_ASSOCIATE_TAG?.trim() || null;
}

export function getBrilliantAffiliateId(): string | null {
  return process.env.BRILLIANT_AFFILIATE_ID?.trim() || null;
}

export function getAffiliateRedirectBaseUrl(): string {
  const fromEnv = process.env.AFFILIATE_REDIRECT_BASE_URL?.trim();
  if (fromEnv) return fromEnv.replace(/\/$/, "");
  try {
    const env = getEnv();
    return `${env.APP_BASE_URL.replace(/\/$/, "")}/go`;
  } catch {
    return "http://localhost:3000/go";
  }
}

/** Production gear redirect: https://orbitwithben.com/go/{slug} */
export function buildOrbitRedirectUrl(productSlug: string): string {
  return `${getAffiliateRedirectBaseUrl()}/${encodeURIComponent(productSlug)}`;
}

/**
 * Build destination URL with UTM params while preserving existing programme tracking.
 */
export function buildTrackedAffiliateUrl(args: {
  affiliateUrl: string;
  videoSlug?: string | null;
  productSlug: string;
  utmSource?: string;
  utmMedium?: string;
  utmCampaign?: string;
  utmContent?: string;
}): string {
  let url: URL;
  try {
    url = new URL(args.affiliateUrl);
  } catch {
    return args.affiliateUrl;
  }

  const source = args.utmSource ?? "youtube";
  const medium = args.utmMedium ?? "affiliate";
  const campaign = args.utmCampaign ?? args.videoSlug ?? "orbit";
  const content = args.utmContent ?? args.productSlug;

  if (!url.searchParams.has("utm_source")) url.searchParams.set("utm_source", source);
  if (!url.searchParams.has("utm_medium")) url.searchParams.set("utm_medium", medium);
  if (!url.searchParams.has("utm_campaign")) url.searchParams.set("utm_campaign", campaign);
  if (!url.searchParams.has("utm_content")) url.searchParams.set("utm_content", content);

  return url.toString();
}

/**
 * Apply programme affiliate tag to a destination URL when the env ID is present.
 * Returns placeholder-aware URLs unchanged when no ID is configured.
 */
export function applyProgrammeAffiliateId(
  affiliateUrl: string,
  programmeSlug: string,
): string {
  try {
    const url = new URL(affiliateUrl);
    if (programmeSlug === "amazon-associates-uk") {
      const tag = getAmazonAssociateTag();
      if (tag) url.searchParams.set("tag", tag);
    }
    if (programmeSlug === "brilliant") {
      const id = getBrilliantAffiliateId();
      if (id && !url.searchParams.has("ref")) {
        url.searchParams.set("ref", id);
      }
    }
    return url.toString();
  } catch {
    return affiliateUrl;
  }
}
