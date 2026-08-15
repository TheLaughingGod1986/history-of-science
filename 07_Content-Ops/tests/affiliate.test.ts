import { describe, expect, it } from "vitest";
import {
  recommendProductsForVideo,
  scoreAffiliateRelevance,
  dedupeRecommendations,
  deterministicRelevanceStrategy,
  setRelevanceStrategy,
} from "../src/lib/affiliate/matching";
import {
  appendAffiliateSectionToDescription,
  buildAffiliateDescriptionSection,
  recommendationsToDescriptionLinks,
} from "../src/lib/affiliate/description";
import {
  affiliateRpm,
  estimateCommission,
  earningsPerClick,
  conversionRate,
  totalContentRpm,
} from "../src/lib/affiliate/revenue";
import { scoreAffiliateOpportunity } from "../src/lib/affiliate/opportunity";
import {
  buildOrbitRedirectUrl,
  buildTrackedAffiliateUrl,
  applyProgrammeAffiliateId,
} from "../src/lib/affiliate/urls";
import {
  previewAffiliateCsv,
  parseAffiliateCsv,
  rowsToConversions,
  AFFILIATE_CSV_DEFAULT_MAPPINGS,
} from "../src/lib/affiliate/csv-import";
import { shouldCheckUrl } from "../src/lib/affiliate/health";
import { mergeDescriptionWithAffiliateLinks } from "../src/lib/publishing/youtube-package";
import type { ProductMatchInput, VideoMatchInput } from "../src/lib/affiliate/types";
import {
  sanitizeAffiliateSocialText,
  containsRawMerchantUrl,
  containsBannedAffiliatePhrase,
  isAllowedSocialTrackedUrl,
  shouldIncludeAffiliateSoftMention,
  buildSoftAffiliateMentionLine,
} from "../src/lib/affiliate/social-copy-rules";
import {
  assertAffiliateSafeSocialCopy,
} from "../src/lib/affiliate/social-copy";
import { generatePlatformCopy } from "../src/lib/platforms/generate-platform-copy";

function product(partial: Partial<ProductMatchInput> & Pick<ProductMatchInput, "id" | "name" | "slug" | "category" | "tagSlugs">): ProductMatchInput {
  return {
    active: true,
    featured: false,
    priority: 0,
    evergreen: false,
    programStatus: "ACTIVE",
    ...partial,
  };
}

describe("affiliate matching", () => {
  const blackHoleVideo: VideoMatchInput = {
    title: "What Would Happen If You Fell Into a Black Hole?",
    topic: "Black Holes",
    primaryKeyword: "black hole",
    secondaryKeywords: ["event horizon", "spaghettification", "relativity"],
    summary: "A calm journey past the event horizon.",
    category: "Space Documentary",
  };

  const catalogue: ProductMatchInput[] = [
    product({
      id: "1",
      name: "Brilliant Physics",
      slug: "brilliant-physics",
      category: "Physics",
      tagSlugs: ["physics", "black-hole", "cosmology"],
      featured: true,
      priority: 8,
      estimatedCommission: 40,
      programSlug: "brilliant",
    }),
    product({
      id: "2",
      name: "Cosmology book",
      slug: "cosmology-book",
      category: "Astronomy books",
      tagSlugs: ["books", "cosmology", "black-hole"],
      estimatedCommission: 1,
    }),
    product({
      id: "3",
      name: "Beginner astronomy book",
      slug: "beginner-astronomy-book",
      category: "Astronomy books",
      tagSlugs: ["books", "beginner", "astronomy"],
      evergreen: true,
    }),
    product({
      id: "4",
      name: "Beginner telescope",
      slug: "beginner-telescope",
      category: "Beginner telescopes",
      tagSlugs: ["telescope", "beginner", "astronomy"],
      evergreen: true,
      featured: true,
    }),
    product({
      id: "5",
      name: "Random high-commission gadget",
      slug: "spam-gadget",
      category: "Kitchen",
      tagSlugs: ["unrelated"],
      estimatedCommission: 200,
      featured: true,
      priority: 99,
    }),
    product({
      id: "6",
      name: "Inactive leftover",
      slug: "inactive",
      category: "Physics",
      tagSlugs: ["physics", "black-hole"],
      active: false,
    }),
  ];

  it("scores black-hole episode toward Brilliant + books + telescope, not spam", () => {
    const set = recommendProductsForVideo(blackHoleVideo, catalogue);
    expect(set.all.length).toBeGreaterThan(0);
    expect(set.all.length).toBeLessThanOrEqual(4);
    const slugs = set.all.map((r) => r.product.slug);
    expect(slugs).toContain("brilliant-physics");
    expect(slugs).not.toContain("spam-gadget");
    expect(slugs).not.toContain("inactive");
    expect(set.primary?.product.slug).toBe("brilliant-physics");
  });

  it("excludes inactive products from relevance", () => {
    const inactive = catalogue.find((p) => p.slug === "inactive")!;
    const { score } = scoreAffiliateRelevance(blackHoleVideo, inactive);
    expect(score).toBe(0);
  });

  it("supports interchangeable relevance strategy", () => {
    setRelevanceStrategy({
      scoreAffiliateRelevance: () => ({ score: 99, reasons: ["llm stub"] }),
    });
    const { score, reasons } = scoreAffiliateRelevance(blackHoleVideo, catalogue[0]);
    expect(score).toBe(99);
    expect(reasons[0]).toBe("llm stub");
    setRelevanceStrategy(deterministicRelevanceStrategy);
  });
});

describe("affiliate description generation", () => {
  const links = [
    {
      productName: "Beginner telescope",
      productSlug: "beginner-telescope",
      category: "Beginner telescopes",
      programSlug: "astronomy-retailer",
      url: "https://example.invalid/aff/beginner-telescope",
    },
    {
      productName: "Brilliant Physics",
      productSlug: "brilliant-physics",
      category: "Physics",
      programSlug: "brilliant",
      url: "https://example.invalid/aff/brilliant-physics",
    },
  ];

  it("builds go-deeper section with templates", () => {
    const section = buildAffiliateDescriptionSection({ links });
    expect(section).toContain("🚀 Go deeper");
    expect(section).toContain("beginner-telescope");
    expect(section).toContain("Brilliant");
  });

  it("appends disclosure once and prevents duplicate links", () => {
    const withDupes = [...links, links[0]];
    const desc = appendAffiliateSectionToDescription({
      description: "Hook paragraph about black holes.",
      links: withDupes,
    });
    expect(desc).toContain("affiliate links");
    expect(desc.match(/beginner-telescope/g)?.length).toBe(1);
    const again = appendAffiliateSectionToDescription({
      description: desc,
      links,
    });
    expect(again.toLowerCase().split("affiliate links").length - 1).toBe(1);
  });

  it("integrates with YouTube package description merge", () => {
    const merged = mergeDescriptionWithAffiliateLinks("Base description", links);
    expect(merged).toContain("Base description");
    expect(merged).toContain("Go deeper");
  });

  it("dedupes recommendation lists", () => {
    const recs = recommendationsToDescriptionLinks([
      {
        product: product({
          id: "1",
          name: "A",
          slug: "a",
          category: "Books",
          tagSlugs: [],
        }),
        relevanceScore: 50,
        reasons: [],
        role: "primary",
      },
      {
        product: product({
          id: "1",
          name: "A",
          slug: "a",
          category: "Books",
          tagSlugs: [],
        }),
        relevanceScore: 40,
        reasons: [],
        role: "secondary",
      },
    ]);
    expect(dedupeRecommendations([
      {
        product: product({ id: "1", name: "A", slug: "a", category: "Books", tagSlugs: [] }),
        relevanceScore: 50,
        reasons: [],
        role: "primary",
      },
      {
        product: product({ id: "1", name: "A", slug: "a", category: "Books", tagSlugs: [] }),
        relevanceScore: 40,
        reasons: [],
        role: "secondary",
      },
    ])).toHaveLength(1);
    expect(recs).toHaveLength(2); // conversion helper does not dedupe; append does
  });
});

describe("redirect URL generation", () => {
  it("builds tracked affiliate URLs with utm params", () => {
    const url = buildTrackedAffiliateUrl({
      affiliateUrl: "https://example.invalid/aff/item?existing=1",
      videoSlug: "black-hole-fall",
      productSlug: "brilliant-physics",
    });
    expect(url).toContain("utm_source=youtube");
    expect(url).toContain("utm_medium=affiliate");
    expect(url).toContain("utm_campaign=black-hole-fall");
    expect(url).toContain("utm_content=brilliant-physics");
    expect(url).toContain("existing=1");
  });

  it("builds orbit redirect paths", () => {
    process.env.AFFILIATE_REDIRECT_BASE_URL = "https://orbitwithben.com/go";
    expect(buildOrbitRedirectUrl("beginner-telescope")).toBe(
      "https://orbitwithben.com/go/beginner-telescope",
    );
    delete process.env.AFFILIATE_REDIRECT_BASE_URL;
  });

  it("applies amazon tag from env without hard-coding", () => {
    process.env.AMAZON_ASSOCIATE_TAG = "orbit-test-21";
    const url = applyProgrammeAffiliateId(
      "https://www.amazon.co.uk/dp/B00TEST?tag=old",
      "amazon-associates-uk",
    );
    expect(url).toContain("tag=orbit-test-21");
    delete process.env.AMAZON_ASSOCIATE_TAG;
  });
});

describe("commission and RPM", () => {
  it("estimates percentage and fixed commissions", () => {
    expect(
      estimateCommission({
        price: 100,
        commissionType: "PERCENTAGE",
        commissionValue: 10,
      }),
    ).toBe(10);
    expect(
      estimateCommission({
        price: 100,
        commissionType: "FIXED",
        commissionValue: 7.5,
      }),
    ).toBe(7.5);
  });

  it("computes affiliate RPM, EPC, conversion rate", () => {
    expect(affiliateRpm(50, 10_000)).toBe(5);
    expect(earningsPerClick(50, 100)).toBe(0.5);
    expect(conversionRate(5, 100)).toBe(5);
    expect(totalContentRpm({ views: 1000, adsenseRevenue: 4, affiliateRevenue: 2 })).toBe(6);
  });
});

describe("opportunity scoring", () => {
  it("scores beginner telescope intent very high", () => {
    const products = [
      product({
        id: "1",
        name: "Beginner telescope",
        slug: "beginner-telescope",
        category: "Beginner telescopes",
        tagSlugs: ["telescope", "beginner", "astronomy"],
        price: 179,
        evergreen: true,
        featured: true,
        programSlug: "astronomy-retailer",
      }),
      product({
        id: "2",
        name: "Binoculars",
        slug: "binoculars",
        category: "Binoculars",
        tagSlugs: ["binoculars", "astronomy"],
        price: 65,
        programSlug: "amazon-associates-uk",
      }),
    ];
    const score = scoreAffiliateOpportunity(
      {
        title: "Best Telescope for Beginners",
        topic: "Telescopes",
        primaryKeyword: "best telescope for beginners",
      },
      products,
      { views: 50_000 },
    );
    expect(score.total).toBeGreaterThanOrEqual(80);
  });

  it("scores speculative science lower than gear intent", () => {
    const products = [
      product({
        id: "1",
        name: "Beginner telescope",
        slug: "beginner-telescope",
        category: "Beginner telescopes",
        tagSlugs: ["telescope", "astronomy"],
        evergreen: true,
      }),
    ];
    const score = scoreAffiliateOpportunity(
      {
        title: "Could Humans Survive Inside Jupiter?",
        topic: "Planetary Science",
        primaryKeyword: "survive inside jupiter",
      },
      products,
    );
    expect(score.total).toBeLessThan(70);
  });
});

describe("affiliate CSV import", () => {
  const csv = `Date,Product Name,Clicks,Items Shipped,Revenue,Earnings,Order ID,Currency
2026-08-01,Beginner telescope,12,1,179.00,8.95,AMZ-001,GBP
2026-08-02,Astronomy binoculars,8,2,130.00,5.20,AMZ-002,GBP`;

  it("previews and parses amazon mapping", () => {
    const preview = previewAffiliateCsv(csv, AFFILIATE_CSV_DEFAULT_MAPPINGS.amazon!);
    expect(preview.missing).toHaveLength(0);
    expect(preview.rowCount).toBe(2);
    expect(preview.sampleRows[0].commission).toBe(8.95);

    const { rows, contentHash } = parseAffiliateCsv(
      csv,
      AFFILIATE_CSV_DEFAULT_MAPPINGS.amazon!,
    );
    expect(contentHash).toHaveLength(64);
    const { conversions, errors } = rowsToConversions(rows);
    expect(errors).toHaveLength(0);
    expect(conversions).toHaveLength(2);
    expect(conversions[0].orderReference).toBe("AMZ-001");
  });
});

describe("url health scheduling", () => {
  it("only rechecks after interval", () => {
    expect(shouldCheckUrl(null)).toBe(true);
    expect(shouldCheckUrl(new Date(), 1000, Date.now())).toBe(false);
    expect(shouldCheckUrl(new Date(Date.now() - 2000), 1000, Date.now())).toBe(true);
  });
});

describe("affiliate social copy house rules", () => {
  it("strips raw merchant URLs and haul language", () => {
    const dirty =
      "Check this telescope https://www.amazon.co.uk/dp/B00TEST use my code ORBIT20 for 20% off haul";
    const { text, violations } = sanitizeAffiliateSocialText(dirty);
    expect(containsRawMerchantUrl(text)).toBe(false);
    expect(containsBannedAffiliatePhrase(text)).toBe(false);
    expect(violations.length).toBeGreaterThan(0);
    expect(text).not.toMatch(/amazon/i);
    expect(text).not.toMatch(/use my code/i);
  });

  it("allows only YouTube or /go/ tracked URLs", () => {
    expect(isAllowedSocialTrackedUrl("https://youtu.be/abc")).toBe(true);
    expect(isAllowedSocialTrackedUrl("https://orbitwithben.com/go/beginner-telescope")).toBe(
      true,
    );
    expect(isAllowedSocialTrackedUrl("/go/beginner-telescope")).toBe(true);
    expect(isAllowedSocialTrackedUrl("https://www.amazon.co.uk/dp/x")).toBe(false);
    expect(isAllowedSocialTrackedUrl("https://brilliant.org/course/physics")).toBe(false);
  });

  it("skips soft mention without natural object, film, or when platform already used", () => {
    expect(
      shouldIncludeAffiliateSoftMention({
        platform: "tiktok",
        hasNaturalObject: false,
        canNameSpecificFilm: true,
        productRelevantToVideo: true,
        hasApprovedPlacement: true,
      }).reason,
    ).toBe("no_natural_object");

    expect(
      shouldIncludeAffiliateSoftMention({
        platform: "tiktok",
        hasNaturalObject: true,
        canNameSpecificFilm: false,
        productRelevantToVideo: true,
        hasApprovedPlacement: true,
      }).reason,
    ).toBe("no_specific_film");

    expect(
      shouldIncludeAffiliateSoftMention({
        platform: "instagram_reels",
        hasNaturalObject: true,
        canNameSpecificFilm: true,
        productRelevantToVideo: true,
        hasApprovedPlacement: true,
        platformMentionedThisWeek: true,
      }).reason,
    ).toBe("platform_already_mentioned_this_week");
  });

  it("never emits raw merchant URLs when applying constraints", () => {
    const copies = generatePlatformCopy({
      shortTitle: "Event horizon",
      hook: "What happens at the event horizon?",
      topic: "Black Holes",
      youtubeUrl: "https://youtu.be/Mo93x0fxB1Q",
      longTitle: "What Would Happen If You Fell Into a Black Hole?",
      affiliate: {
        productLabel: "Brilliant Physics",
        productSlug: "brilliant-physics",
        hasNaturalObject: true,
        productRelevantToVideo: true,
        hasApprovedPlacement: true,
        youtubeUrl: "https://youtu.be/Mo93x0fxB1Q",
        longTitle: "What Would Happen If You Fell Into a Black Hole?",
      },
    });

    for (const copy of copies) {
      expect(containsRawMerchantUrl(copy.caption)).toBe(false);
      expect(containsBannedAffiliatePhrase(copy.caption)).toBe(false);
      expect(copy.caption.toLowerCase()).not.toContain("amazon.");
      expect(copy.caption.toLowerCase()).not.toContain("brilliant.org");
      // Soft mention is a caption tail afterthought — never the opening line
      const first = copy.caption.split("\n").find((l) => l.trim()) || "";
      expect(first.toLowerCase().startsWith("brilliant")).toBe(false);
    }

    const tiktok = copies.find((c) => c.platform === "tiktok")!;
    expect(tiktok.caption).toContain("YouTube description");
  });

  it("assertAffiliateSafeSocialCopy rejects merchant leaks", () => {
    expect(() =>
      assertAffiliateSafeSocialCopy("Buy here https://www.amazon.co.uk/dp/x"),
    ).toThrow(/house rules/);
    expect(() =>
      assertAffiliateSafeSocialCopy("Thought about silence.\n\nFull film: https://youtu.be/abc"),
    ).not.toThrow();
  });

  it("soft mention line never includes merchant hosts", () => {
    const line = buildSoftAffiliateMentionLine({
      platform: "x",
      productLabel: "Beginner telescope",
      goUrl: "https://orbitwithben.com/go/beginner-telescope",
    });
    expect(line).toBeTruthy();
    expect(line!).toContain("/go/");
    expect(containsRawMerchantUrl(line!)).toBe(false);
  });
});
