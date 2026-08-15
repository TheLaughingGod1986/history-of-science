import { prisma } from "@/lib/storage/prisma";
import { startOfMonth, endOfMonth } from "date-fns";
import {
  affiliateRpm,
  earningsPerClick,
  conversionRate,
  roundMoney,
} from "./revenue";
import { scoreAffiliateOpportunity } from "./opportunity";
import { loadActiveProductsForMatching } from "./products";
import { videoToMatchInput } from "./placements";

export async function getAffiliateDashboardSummary() {
  const now = new Date();
  const monthStart = startOfMonth(now);
  const monthEnd = endOfMonth(now);

  const [
    activePrograms,
    activeProducts,
    videosWithLinks,
    clicksTotal,
    clicksMonth,
    conversionsAgg,
    conversionsMonth,
    topProduct,
    topVideoPlacement,
    brokenProducts,
    inactiveInDescriptions,
  ] = await Promise.all([
    prisma.affiliateProgram.count({ where: { status: "ACTIVE" } }),
    prisma.affiliateProduct.count({ where: { active: true } }),
    prisma.affiliatePlacement.groupBy({
      by: ["videoId"],
      where: { status: { in: ["APPROVED", "ACTIVE", "PENDING"] } },
    }),
    prisma.affiliateClick.count(),
    prisma.affiliateClick.count({
      where: { timestamp: { gte: monthStart, lte: monthEnd } },
    }),
    prisma.affiliateConversion.aggregate({
      _sum: { commissionAmount: true },
      _count: true,
    }),
    prisma.affiliateConversion.aggregate({
      where: { conversionDate: { gte: monthStart, lte: monthEnd } },
      _sum: { commissionAmount: true },
      _count: true,
    }),
    prisma.affiliateClick.groupBy({
      by: ["affiliateProductId"],
      _count: true,
      orderBy: { _count: { affiliateProductId: "desc" } },
      take: 1,
    }),
    prisma.affiliatePlacement.findMany({
      where: { status: { in: ["APPROVED", "ACTIVE"] } },
      orderBy: [{ estimatedRevenue: "desc" }, { clicks: "desc" }],
      take: 1,
      include: { video: true, affiliateProduct: true },
    }),
    prisma.affiliateProduct.count({ where: { urlHealthStatus: "BROKEN" } }),
    prisma.affiliatePlacement.count({
      where: {
        status: { in: ["APPROVED", "ACTIVE", "PENDING"] },
        affiliateProduct: { active: false },
      },
    }),
  ]);

  const revenueTotal = conversionsAgg._sum.commissionAmount ?? 0;
  const revenueMonth = conversionsMonth._sum.commissionAmount ?? 0;
  const conversionsTotal = conversionsAgg._count;

  let highestProductName: string | null = null;
  if (topProduct[0]) {
    const p = await prisma.affiliateProduct.findUnique({
      where: { id: topProduct[0].affiliateProductId },
    });
    highestProductName = p?.name ?? null;
  }

  const highClickZeroConv = await findHighClickZeroConversionProducts();
  const videosMissingLinks = await countHighViewVideosMissingLinks();

  return {
    activePrograms,
    activeProducts,
    videosWithLinks: videosWithLinks.length,
    clicksTotal,
    clicksMonth,
    conversionsEstimated: conversionsTotal,
    revenueTotal: roundMoney(revenueTotal),
    revenueMonth: roundMoney(revenueMonth),
    highestPerformingProduct: highestProductName,
    highestPerformingVideo: topVideoPlacement[0]?.video.title ?? null,
    warnings: {
      brokenUrls: brokenProducts,
      inactiveProductInDescriptions: inactiveInDescriptions,
      highClickZeroConversions: highClickZeroConv,
      videosMissingLinks,
      programmesNeedingReports: await countProgrammesNeedingReports(),
    },
  };
}

async function findHighClickZeroConversionProducts(): Promise<number> {
  const grouped = await prisma.affiliateClick.groupBy({
    by: ["affiliateProductId"],
    _count: true,
  });
  let count = 0;
  for (const g of grouped) {
    if (g._count < 5) continue;
    const conv = await prisma.affiliateConversion.count({
      where: { affiliateProductId: g.affiliateProductId },
    });
    if (conv === 0) count += 1;
  }
  return count;
}

async function countProgrammesNeedingReports(): Promise<number> {
  const programs = await prisma.affiliateProgram.findMany({
    where: { status: "ACTIVE" },
    include: { _count: { select: { conversions: true } } },
  });
  return programs.filter((p) => p._count.conversions === 0).length;
}

async function countHighViewVideosMissingLinks(): Promise<number> {
  const videos = await prisma.longFormVideo.findMany({
    where: { status: { in: ["published", "ready", "scheduled"] } },
    include: {
      affiliatePlacements: {
        where: { status: { in: ["APPROVED", "ACTIVE", "PENDING"] } },
      },
      clips: {
        include: {
          posts: {
            where: { platform: { in: ["youtube", "youtube_shorts"] } },
            include: { metrics: { orderBy: { recordedAt: "desc" }, take: 1 } },
          },
        },
      },
    },
  });

  let n = 0;
  for (const v of videos) {
    if (v.affiliatePlacements.length > 0) continue;
    const views = v.clips.reduce((sum, c) => {
      return (
        sum +
        c.posts.reduce((s, p) => s + (p.metrics[0]?.views ?? 0), 0)
      );
    }, 0);
    if (views >= 100 || v.status === "published") n += 1;
  }
  return n;
}

export async function listVideoOpportunities() {
  const products = await loadActiveProductsForMatching();
  const videos = await prisma.longFormVideo.findMany({
    include: {
      affiliatePlacements: {
        where: { status: { in: ["APPROVED", "ACTIVE", "PENDING"] } },
        include: { affiliateProduct: true },
      },
      affiliateClicks: true,
      affiliateConversions: true,
      clips: {
        include: {
          posts: {
            include: { metrics: { orderBy: { recordedAt: "desc" }, take: 1 } },
          },
        },
      },
    },
    orderBy: { updatedAt: "desc" },
  });

  return videos.map((video) => {
    const views = video.clips.reduce(
      (sum, c) =>
        sum + c.posts.reduce((s, p) => s + (p.metrics[0]?.views ?? 0), 0),
      0,
    );
    const clicks = video.affiliateClicks.length;
    const revenue = roundMoney(
      video.affiliateConversions.reduce((s, c) => s + c.commissionAmount, 0) +
        video.affiliatePlacements.reduce((s, p) => s + p.estimatedRevenue, 0),
    );
    const score = scoreAffiliateOpportunity(videoToMatchInput(video), products, {
      views,
    });
    const linksInserted = video.affiliatePlacements.length;
    const isOpportunity = views >= 100 && linksInserted === 0 && score.total >= 40;

    return {
      videoId: video.id,
      title: video.title,
      workingTitle: video.workingTitle,
      slug: video.slug,
      topic: video.topic,
      views,
      affiliateScore: score.total,
      scoreBreakdown: score,
      productsAvailable: products.filter((p) => p.active).length,
      linksInserted,
      clicks,
      estimatedRevenue: revenue,
      revenuePerThousandViews: affiliateRpm(revenue, views),
      monetisationOpportunity: isOpportunity,
    };
  }).sort((a, b) => {
    if (a.monetisationOpportunity !== b.monetisationOpportunity) {
      return a.monetisationOpportunity ? -1 : 1;
    }
    return b.affiliateScore - a.affiliateScore;
  });
}

export async function getHomeMonetisationCard() {
  const summary = await getAffiliateDashboardSummary();
  const opportunities = await listVideoOpportunities();
  const top = opportunities[0];
  const monthViews = opportunities.reduce((s, o) => s + o.views, 0);

  return {
    revenueMonth: summary.revenueMonth,
    clicksMonth: summary.clicksMonth,
    affiliateRpm: affiliateRpm(summary.revenueMonth, monthViews),
    videosMissingLinks: summary.warnings.videosMissingLinks,
    topAffiliateVideo: summary.highestPerformingVideo || top?.title || null,
    topOpportunitySlug: top?.slug ?? null,
  };
}

export async function getVideoAffiliatePanel(videoId: string) {
  const video = await prisma.longFormVideo.findUnique({
    where: { id: videoId },
    include: {
      affiliatePlacements: {
        where: { status: { not: "REMOVED" } },
        include: {
          affiliateProduct: {
            include: { affiliateProgram: true, tags: { include: { tag: true } } },
          },
        },
        orderBy: { position: "asc" },
      },
      affiliateClicks: true,
      affiliateConversions: true,
      clips: {
        include: {
          posts: {
            include: { metrics: { orderBy: { recordedAt: "desc" }, take: 1 } },
          },
        },
      },
    },
  });
  if (!video) return null;

  const products = await loadActiveProductsForMatching();
  const views = video.clips.reduce(
    (sum, c) => sum + c.posts.reduce((s, p) => s + (p.metrics[0]?.views ?? 0), 0),
    0,
  );
  const revenue = roundMoney(
    video.affiliateConversions.reduce((s, c) => s + c.commissionAmount, 0),
  );
  const opportunity = scoreAffiliateOpportunity(videoToMatchInput(video), products, {
    views,
  });

  return {
    video,
    placements: video.affiliatePlacements,
    clicks: video.affiliateClicks.length,
    conversions: video.affiliateConversions.length,
    revenue,
    affiliateRpm: affiliateRpm(revenue, views),
    epc: earningsPerClick(revenue, video.affiliateClicks.length),
    conversionRate: conversionRate(
      video.affiliateConversions.length,
      video.affiliateClicks.length,
    ),
    opportunity,
    matchProducts: products,
  };
}
