/**
 * Canonical public destination URLs for Orbit affiliate products.
 *
 * Affiliate programme tags/IDs are NEVER stored here — applied at /go redirect
 * from AMAZON_ASSOCIATE_TAG / BRILLIANT_AFFILIATE_ID.
 *
 * Only confirmed amazon.co.uk product pages (or explicit inactive stubs).
 * Do not invent ASINs — leave TODO notes in seed for unconfirmed Amazon products.
 */

export type LiveProductUrlSpec = {
  slug: string;
  /** Optional display name update when applying live URLs. */
  name?: string;
  description?: string;
  destinationUrl: string;
  /**
   * Optional pre-built affiliate URL. Prefer omit/empty — /go builds from
   * destinationUrl + AMAZON_ASSOCIATE_TAG (or Brilliant env) at redirect time.
   */
  affiliateUrl?: string;
  /** Reassign product to this programme when applying (e.g. telescope → Amazon UK). */
  programmeSlug?: string;
  tags?: string[];
  /** When false, product stays inactive (e.g. LEGO until programme access). */
  active?: boolean;
  notes: string;
};

/**
 * Confirmed Amazon Associates UK product pages (verified listings).
 * Other catalogue slugs keep seed placeholders / TODOs until an ASIN is confirmed.
 */
export const LIVE_PRODUCT_URLS: LiveProductUrlSpec[] = [
  {
    slug: "beginner-astronomy-book",
    name: "Turn Left at Orion",
    description:
      "Consolmagno & Davis — hundreds of night-sky objects for a home telescope. Orbit’s beginner desk book.",
    destinationUrl:
      "https://www.amazon.co.uk/Turn-Left-Orion-Hundreds-Telescope/dp/1108457568",
    programmeSlug: "amazon-associates-uk",
    tags: ["books", "astronomy", "beginner", "telescope"],
    notes:
      "Verified amazon.co.uk ASIN 1108457568 (Consolmagno / Davis, 5th ed.). Tag from AMAZON_ASSOCIATE_TAG at /go — never commit the tag.",
  },
  {
    slug: "beginner-telescope",
    name: "Celestron FirstScope (Cometron 76)",
    description:
      "Celestron FirstScope tabletop Dobsonian — a practical first telescope for clear nights.",
    // Verified live amazon.co.uk product page (Cometron FirstScope 76, ASIN B00DV6SBRO).
    // Classic 21024 FirstScope (B001UQ6E4Y) returned bot/503 during verification — use Cometron listing.
    // AstroMaster 70AZ: no verified amazon.co.uk ASIN at wire-up time — do not invent one.
    destinationUrl:
      "https://www.amazon.co.uk/Celestron-21023-Cometron-FirstScope-Telescope/dp/B00DV6SBRO",
    programmeSlug: "amazon-associates-uk",
    tags: ["telescope", "beginner", "astronomy"],
    notes:
      "Verified amazon.co.uk ASIN B00DV6SBRO (Celestron Cometron FirstScope 76). Tag from AMAZON_ASSOCIATE_TAG at /go.",
  },
  {
    slug: "space-lego",
    destinationUrl: "https://example.invalid/dest/space-lego",
    programmeSlug: "amazon-associates-uk",
    tags: ["lego", "kids", "nasa", "spacecraft"],
    active: false,
    notes:
      "LEGO stays inactive — do not put on social or descriptions until LEGO Affiliate access. Programme slug `lego` is INACTIVE.",
  },
];

export function liveUrlForSlug(slug: string): LiveProductUrlSpec | undefined {
  return LIVE_PRODUCT_URLS.find((u) => u.slug === slug);
}

export function isPlaceholderAffiliateUrl(url: string): boolean {
  return !url?.trim() || /example\.invalid/i.test(url) || /PLACEHOLDER/i.test(url);
}

/** True when destination is a real amazon.co.uk product page (not a placeholder). */
export function isAmazonUkDestinationUrl(url: string): boolean {
  try {
    const u = new URL(url);
    return (
      (u.hostname === "www.amazon.co.uk" || u.hostname === "amazon.co.uk") &&
      !isPlaceholderAffiliateUrl(url)
    );
  } catch {
    return false;
  }
}
