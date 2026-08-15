import {
  MAX_AFFILIATE_LINKS_PER_VIDEO,
  RELEVANCE_WEIGHTS,
  type AffiliateRecommendationSet,
  type ProductMatchInput,
  type ScoredRecommendation,
  type VideoMatchInput,
} from "./types";

function parseKeywords(raw: string[] | string | null | undefined): string[] {
  if (!raw) return [];
  if (Array.isArray(raw)) return raw.map((k) => k.toLowerCase());
  try {
    const parsed = JSON.parse(raw) as unknown;
    if (Array.isArray(parsed)) return parsed.map((k) => String(k).toLowerCase());
  } catch {
    /* fall through */
  }
  return raw
    .split(/[,;|]/)
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
}

function normalize(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9\s-]/g, " ").replace(/\s+/g, " ").trim();
}

function tokenize(...parts: Array<string | null | undefined>): Set<string> {
  const tokens = new Set<string>();
  for (const part of parts) {
    if (!part) continue;
    for (const t of normalize(part).split(" ")) {
      if (t.length >= 3) tokens.add(t);
    }
  }
  return tokens;
}

/** Map common topic phrases → canonical tag slugs. */
const TOPIC_TAG_ALIASES: Record<string, string[]> = {
  "black hole": ["black-hole", "physics", "cosmology", "relativity"],
  "black holes": ["black-hole", "physics", "cosmology"],
  fermi: ["aliens", "seti", "astronomy"],
  alien: ["aliens", "seti"],
  aliens: ["aliens", "seti"],
  seti: ["seti", "aliens"],
  mars: ["mars", "nasa", "astronomy"],
  moon: ["moon", "nasa", "astronomy"],
  telescope: ["telescope", "astronomy", "beginner"],
  telescopes: ["telescope", "astronomy"],
  astronomy: ["astronomy"],
  cosmology: ["cosmology", "physics"],
  physics: ["physics"],
  relativity: ["relativity", "physics"],
  quantum: ["quantum", "physics"],
  exoplanet: ["exoplanets", "astronomy"],
  exoplanets: ["exoplanets", "astronomy"],
  spacex: ["spacex", "starship", "nasa"],
  starship: ["starship", "spacex"],
  nasa: ["nasa"],
  lego: ["lego", "kids"],
  ai: ["ai"],
  "artificial intelligence": ["ai"],
  mathematics: ["mathematics"],
  maths: ["mathematics"],
  math: ["mathematics"],
  engineering: ["engineering"],
  orbital: ["orbital-mechanics", "physics"],
  orbit: ["orbital-mechanics", "astronomy"],
  binoculars: ["binoculars", "astronomy", "beginner"],
  astrophotography: ["astrophotography", "telescope"],
  beginner: ["beginner", "astronomy"],
  kids: ["kids"],
  book: ["books"],
  books: ["books"],
  jupiter: ["astronomy", "planets"],
  saturn: ["astronomy"],
  jwst: ["astronomy", "nasa", "telescope"],
  "james webb": ["astronomy", "nasa", "telescope"],
};

function inferTagsFromText(text: string): Set<string> {
  const n = normalize(text);
  const tags = new Set<string>();
  for (const [phrase, mapped] of Object.entries(TOPIC_TAG_ALIASES)) {
    if (n.includes(phrase)) {
      for (const t of mapped) tags.add(t);
    }
  }
  return tags;
}

export type RelevanceStrategy = {
  scoreAffiliateRelevance(
    video: VideoMatchInput,
    product: ProductMatchInput,
  ): { score: number; reasons: string[] };
};

/**
 * Deterministic first-pass matcher.
 * Future LLM strategy can implement the same RelevanceStrategy interface.
 */
export const deterministicRelevanceStrategy: RelevanceStrategy = {
  scoreAffiliateRelevance(video, product) {
    const reasons: string[] = [];
    let score = 0;

    if (!product.active) {
      return { score: 0, reasons: ["inactive product"] };
    }
    if (product.programStatus && product.programStatus !== "ACTIVE") {
      return { score: 0, reasons: ["programme inactive"] };
    }

    const episodeType = video.episodeType || video.category || "";
    if (
      product.unsuitableFor?.length &&
      episodeType &&
      product.unsuitableFor.some(
        (u) => normalize(u) === normalize(episodeType) || normalize(episodeType).includes(normalize(u)),
      )
    ) {
      return { score: 0, reasons: ["unsuitable for episode type"] };
    }

    const videoCorpus = [
      video.title,
      video.workingTitle,
      video.topic,
      video.category,
      video.summary,
      video.primaryKeyword,
      ...(video.chapterTitles || []),
      ...(video.tags || []),
      ...parseKeywords(video.secondaryKeywords),
      // Light script sample for keyword hits only (first 2k chars)
      (video.script || "").slice(0, 2000),
    ]
      .filter(Boolean)
      .join(" ");

    const videoTags = new Set<string>([
      ...inferTagsFromText(videoCorpus),
      ...(video.tags || []).map((t) => normalize(t).replace(/\s+/g, "-")),
    ]);
    const productTags = new Set(product.tagSlugs.map((t) => normalize(t).replace(/\s+/g, "-")));

    const topicNorm = normalize(video.topic);
    const primaryKw = normalize(video.primaryKeyword || "");

    // Exact primary topic / keyword ↔ product tags or category
    const primaryHits = [...productTags].filter(
      (t) =>
        topicNorm.includes(t.replace(/-/g, " ")) ||
        primaryKw.includes(t.replace(/-/g, " ")) ||
        videoTags.has(t),
    );
    if (primaryHits.length > 0) {
      const exact =
        primaryHits.some(
          (t) =>
            topicNorm === t.replace(/-/g, " ") ||
            topicNorm.includes(t.replace(/-/g, " ")) ||
            primaryKw.includes(t.replace(/-/g, " ")),
        ) || [...inferTagsFromText(video.topic)].some((t) => productTags.has(t));
      if (exact) {
        score += RELEVANCE_WEIGHTS.exactPrimaryTopic;
        reasons.push(`exact topic match (+${RELEVANCE_WEIGHTS.exactPrimaryTopic})`);
      } else {
        score += RELEVANCE_WEIGHTS.relatedTopic;
        reasons.push(`related topic (+${RELEVANCE_WEIGHTS.relatedTopic})`);
      }
    } else {
      // Related via shared inferred tags
      const overlap = [...productTags].filter((t) => videoTags.has(t));
      if (overlap.length > 0) {
        score += RELEVANCE_WEIGHTS.relatedTopic;
        reasons.push(`related tags: ${overlap.slice(0, 3).join(", ")} (+${RELEVANCE_WEIGHTS.relatedTopic})`);
      }
    }

    // Tag exact bonus
    const exactTagHits = [...productTags].filter((t) => videoTags.has(t));
    if (exactTagHits.length > 0) {
      const bonus = Math.min(
        RELEVANCE_WEIGHTS.tagExact * exactTagHits.length,
        RELEVANCE_WEIGHTS.tagExact * 2,
      );
      score += bonus;
      reasons.push(`tag overlap (+${bonus})`);
    }

    // Category alignment
    const catNorm = normalize(product.category);
    const videoCat = normalize(video.category || "");
    const videoTokens = tokenize(videoCorpus);
    if (
      (videoCat && (videoCat.includes(catNorm) || catNorm.includes(videoCat))) ||
      [...tokenize(product.category, product.subcategory, product.name)].some((t) =>
        videoTokens.has(t),
      )
    ) {
      score += RELEVANCE_WEIGHTS.category;
      reasons.push(`category (+${RELEVANCE_WEIGHTS.category})`);
    }

    // Keyword hits in title/description
    const productTokens = tokenize(product.name, product.description, product.category);
    let keywordHits = 0;
    for (const t of productTokens) {
      if (videoTokens.has(t)) keywordHits += 1;
    }
    if (keywordHits >= 2) {
      score += RELEVANCE_WEIGHTS.keywordHit;
      reasons.push(`keyword hits (+${RELEVANCE_WEIGHTS.keywordHit})`);
    }

    // Editorial gate: featured / evergreen / priority must not promote unrelated junk.
    // Require at least one content signal (topic, tag, category, or keyword hit).
    const hasEditorialSignal = reasons.some((r) =>
      /exact topic|related topic|related tags|tag overlap|category|keyword hits/.test(r),
    );
    if (!hasEditorialSignal) {
      return { score: 0, reasons: ["no editorial relevance — excluded"] };
    }

    if (product.evergreen) {
      score += RELEVANCE_WEIGHTS.evergreenGeneral;
      reasons.push(`evergreen (+${RELEVANCE_WEIGHTS.evergreenGeneral})`);
    }

    if (product.featured) {
      score += RELEVANCE_WEIGHTS.manuallyFeatured;
      reasons.push(`featured (+${RELEVANCE_WEIGHTS.manuallyFeatured})`);
    }

    if (product.priority > 0) {
      const boost = Math.min(product.priority * RELEVANCE_WEIGHTS.priorityBoost, 8);
      score += boost;
      reasons.push(`priority (+${boost})`);
    }

    return { score, reasons };
  },
};

let activeStrategy: RelevanceStrategy = deterministicRelevanceStrategy;

export function setRelevanceStrategy(strategy: RelevanceStrategy): void {
  activeStrategy = strategy;
}

export function getRelevanceStrategy(): RelevanceStrategy {
  return activeStrategy;
}

export function scoreAffiliateRelevance(
  video: VideoMatchInput,
  product: ProductMatchInput,
): { score: number; reasons: string[] } {
  return activeStrategy.scoreAffiliateRelevance(video, product);
}

/**
 * Return strongest recommendations: 1 primary, up to 2 secondary, 1 evergreen.
 * Max 4 links. Irrelevant high-commission products must not win on commission alone.
 */
export function recommendProductsForVideo(
  video: VideoMatchInput,
  products: ProductMatchInput[],
  options?: { maxLinks?: number; minScore?: number },
): AffiliateRecommendationSet {
  const maxLinks = options?.maxLinks ?? MAX_AFFILIATE_LINKS_PER_VIDEO;
  const minScore = options?.minScore ?? 15;

  const scored: ScoredRecommendation[] = products
    .map((product) => {
      const { score, reasons } = scoreAffiliateRelevance(video, product);
      return {
        product,
        relevanceScore: score,
        reasons,
        role: "secondary" as const,
      };
    })
    .filter((s) => s.relevanceScore >= minScore)
    .sort((a, b) => {
      if (b.relevanceScore !== a.relevanceScore) return b.relevanceScore - a.relevanceScore;
      // Tie-break: prefer lower commission noise — editorial first, then featured
      if (a.product.featured !== b.product.featured) return a.product.featured ? -1 : 1;
      return a.product.name.localeCompare(b.product.name);
    });

  const used = new Set<string>();
  const pick = (
    list: ScoredRecommendation[],
    role: ScoredRecommendation["role"],
    predicate?: (s: ScoredRecommendation) => boolean,
  ): ScoredRecommendation | null => {
    for (const item of list) {
      if (used.has(item.product.id)) continue;
      if (predicate && !predicate(item)) continue;
      used.add(item.product.id);
      return { ...item, role };
    }
    return null;
  };

  const primary = pick(scored, "primary");
  const secondary: ScoredRecommendation[] = [];
  while (secondary.length < 2) {
    const next = pick(scored, "secondary");
    if (!next) break;
    secondary.push(next);
  }
  const evergreen =
    pick(scored, "evergreen", (s) => s.product.evergreen) ||
    pick(scored, "evergreen", (s) =>
      /astronomy|beginner|telescope|books/i.test(
        `${s.product.category} ${s.product.tagSlugs.join(" ")}`,
      ),
    );

  const all = [primary, ...secondary, evergreen].filter(
    (x): x is ScoredRecommendation => x != null,
  ).slice(0, maxLinks);

  return {
    primary: all.find((a) => a.role === "primary") || all[0] || null,
    secondary: all.filter((a) => a.role === "secondary").slice(0, 2),
    evergreen: all.find((a) => a.role === "evergreen") || null,
    all,
  };
}

/** Prevent duplicate product links in a description placement set. */
export function dedupeRecommendations(
  items: ScoredRecommendation[],
): ScoredRecommendation[] {
  const seen = new Set<string>();
  const out: ScoredRecommendation[] = [];
  for (const item of items) {
    if (seen.has(item.product.id) || seen.has(item.product.slug)) continue;
    seen.add(item.product.id);
    seen.add(item.product.slug);
    out.push(item);
  }
  return out;
}
