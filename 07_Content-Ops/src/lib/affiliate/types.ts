/**
 * Affiliate Monetisation System — shared types & constants.
 * Editorial trust first: relevance before revenue.
 */

export const AFFILIATE_PROGRAM_STATUSES = ["ACTIVE", "INACTIVE", "PENDING"] as const;
export type AffiliateProgramStatus = (typeof AFFILIATE_PROGRAM_STATUSES)[number];

export const COMMISSION_TYPES = ["PERCENTAGE", "FIXED"] as const;
export type CommissionType = (typeof COMMISSION_TYPES)[number];

export const URL_HEALTH_STATUSES = ["HEALTHY", "REDIRECTED", "BROKEN", "UNKNOWN"] as const;
export type UrlHealthStatus = (typeof URL_HEALTH_STATUSES)[number];

export const PLACEMENT_TYPES = [
  "DESCRIPTION_PRIMARY",
  "DESCRIPTION_SECONDARY",
  "PINNED_COMMENT",
  "WEBSITE_ARTICLE",
  "GEAR_PAGE",
  "SHORT_DESCRIPTION",
] as const;
export type PlacementType = (typeof PLACEMENT_TYPES)[number];

export const PLACEMENT_STATUSES = [
  "PENDING",
  "APPROVED",
  "REJECTED",
  "ACTIVE",
  "REMOVED",
] as const;
export type PlacementStatus = (typeof PLACEMENT_STATUSES)[number];

/** Max affiliate links per YouTube description — never spam. */
export const MAX_AFFILIATE_LINKS_PER_VIDEO = 4;

/** Scoring weights for deterministic relevance matching. */
export const RELEVANCE_WEIGHTS = {
  exactPrimaryTopic: 40,
  relatedTopic: 20,
  category: 15,
  evergreenGeneral: 5,
  manuallyFeatured: 10,
  priorityBoost: 2, // per priority point, capped
  tagExact: 12,
  keywordHit: 8,
} as const;

export const DEFAULT_DISCLOSURE =
  "Some links above are affiliate links. If you purchase through them, Orbit With Ben may receive a commission at no additional cost to you.";

export const DEFAULT_AMAZON_DISCLOSURE =
  "As an Amazon Associate I earn from qualifying purchases.";

/** Canonical semantic tags for product ↔ video matching. */
export const CANONICAL_AFFILIATE_TAGS = [
  "mars",
  "moon",
  "black-hole",
  "telescope",
  "astronomy",
  "astrophotography",
  "spacex",
  "starship",
  "nasa",
  "physics",
  "ai",
  "cosmology",
  "aliens",
  "seti",
  "exoplanets",
  "kids",
  "beginner",
  "books",
  "lego",
  "binoculars",
  "mathematics",
  "engineering",
  "relativity",
  "quantum",
  "orbital-mechanics",
] as const;

export type CanonicalAffiliateTag = (typeof CANONICAL_AFFILIATE_TAGS)[number];

export type VideoMatchInput = {
  id?: string;
  title: string;
  workingTitle?: string | null;
  slug?: string;
  topic: string;
  category?: string | null;
  summary?: string | null;
  script?: string | null;
  primaryKeyword?: string | null;
  secondaryKeywords?: string[] | string | null;
  chapterTitles?: string[];
  tags?: string[];
  episodeType?: string | null;
};

export type ProductMatchInput = {
  id: string;
  name: string;
  slug: string;
  description?: string | null;
  category: string;
  subcategory?: string | null;
  active: boolean;
  featured: boolean;
  priority: number;
  evergreen: boolean;
  estimatedCommission?: number | null;
  commissionType?: string | null;
  commissionValue?: number | null;
  price?: number | null;
  currency?: string;
  unsuitableFor?: string[];
  tagSlugs: string[];
  programSlug?: string;
  programStatus?: string;
};

export type ScoredRecommendation = {
  product: ProductMatchInput;
  relevanceScore: number;
  reasons: string[];
  role: "primary" | "secondary" | "evergreen";
};

export type AffiliateRecommendationSet = {
  primary: ScoredRecommendation | null;
  secondary: ScoredRecommendation[];
  evergreen: ScoredRecommendation | null;
  all: ScoredRecommendation[];
};

export type OpportunityScoreBreakdown = {
  commercialRelevance: number;
  searchIntent: number;
  topicRelevance: number;
  likelyPrice: number;
  partnerCoverage: number;
  viewPotential: number;
  evergreenPotential: number;
  total: number;
};
