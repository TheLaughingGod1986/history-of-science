import { prisma } from "@/lib/storage/prisma";
import {
  dedupeRecommendations,
  recommendProductsForVideo,
} from "./matching";
import { loadActiveProductsForMatching, toProductMatchInput } from "./products";
import type { PlacementType, VideoMatchInput } from "./types";
import { MAX_AFFILIATE_LINKS_PER_VIDEO } from "./types";
import { placementActionSchema } from "./schemas";

function videoToMatchInput(video: {
  id: string;
  title: string;
  workingTitle: string | null;
  slug: string;
  topic: string;
  category: string | null;
  summary: string | null;
  script: string | null;
  primaryKeyword: string | null;
  secondaryKeywords: string | null;
}): VideoMatchInput {
  return {
    id: video.id,
    title: video.title,
    workingTitle: video.workingTitle,
    slug: video.slug,
    topic: video.topic,
    category: video.category,
    summary: video.summary,
    script: video.script,
    primaryKeyword: video.primaryKeyword,
    secondaryKeywords: video.secondaryKeywords,
  };
}

export async function generateRecommendationsForVideo(videoId: string) {
  const video = await prisma.longFormVideo.findUnique({ where: { id: videoId } });
  if (!video) throw new Error("Video not found");
  const products = await loadActiveProductsForMatching();
  const set = recommendProductsForVideo(videoToMatchInput(video), products);
  return {
    video: videoToMatchInput(video),
    recommendations: dedupeRecommendations(set.all).slice(0, MAX_AFFILIATE_LINKS_PER_VIDEO),
    set,
  };
}

function placementTypeForRole(
  role: "primary" | "secondary" | "evergreen",
  index: number,
): PlacementType {
  if (role === "primary" || index === 0) return "DESCRIPTION_PRIMARY";
  return "DESCRIPTION_SECONDARY";
}

/**
 * Regenerate automatic placements for a video.
 * Does not remove manually approved placements unless replaceAll is true.
 */
export async function regeneratePlacementsForVideo(
  videoId: string,
  opts?: { replaceAll?: boolean; autoApprove?: boolean },
) {
  const { recommendations } = await generateRecommendationsForVideo(videoId);

  if (opts?.replaceAll) {
    await prisma.affiliatePlacement.deleteMany({
      where: { videoId, generatedAutomatically: true },
    });
  } else {
    await prisma.affiliatePlacement.deleteMany({
      where: {
        videoId,
        generatedAutomatically: true,
        manuallyApproved: false,
        status: { in: ["PENDING", "REJECTED"] },
      },
    });
  }

  const created = [];
  for (const [i, rec] of recommendations.entries()) {
    const placementType = placementTypeForRole(rec.role, i);
    const existing = await prisma.affiliatePlacement.findUnique({
      where: {
        videoId_affiliateProductId_placementType: {
          videoId,
          affiliateProductId: rec.product.id,
          placementType,
        },
      },
    });
    if (existing && existing.status === "REJECTED" && !opts?.replaceAll) {
      continue;
    }
    if (existing && existing.manuallyApproved && !opts?.replaceAll) {
      created.push(existing);
      continue;
    }

    const row = await prisma.affiliatePlacement.upsert({
      where: {
        videoId_affiliateProductId_placementType: {
          videoId,
          affiliateProductId: rec.product.id,
          placementType,
        },
      },
      create: {
        videoId,
        affiliateProductId: rec.product.id,
        placementType,
        position: i,
        relevanceScore: rec.relevanceScore,
        generatedAutomatically: true,
        manuallyApproved: Boolean(opts?.autoApprove),
        status: opts?.autoApprove ? "APPROVED" : "PENDING",
      },
      update: {
        position: i,
        relevanceScore: rec.relevanceScore,
        generatedAutomatically: true,
        status: opts?.autoApprove ? "APPROVED" : "PENDING",
      },
      include: {
        affiliateProduct: {
          include: { affiliateProgram: true, tags: { include: { tag: true } } },
        },
      },
    });
    created.push(row);
  }

  return { recommendations, placements: created };
}

export async function upsertPlacement(raw: unknown) {
  const input = placementActionSchema.parse(raw);
  return prisma.affiliatePlacement.upsert({
    where: {
      videoId_affiliateProductId_placementType: {
        videoId: input.videoId,
        affiliateProductId: input.affiliateProductId,
        placementType: input.placementType,
      },
    },
    create: {
      videoId: input.videoId,
      affiliateProductId: input.affiliateProductId,
      placementType: input.placementType,
      position: input.position ?? 0,
      relevanceScore: input.relevanceScore ?? null,
      manuallyApproved: input.manuallyApproved ?? true,
      generatedAutomatically: input.generatedAutomatically ?? false,
      status: input.status ?? "APPROVED",
    },
    update: {
      position: input.position,
      relevanceScore: input.relevanceScore,
      manuallyApproved: input.manuallyApproved,
      status: input.status,
    },
    include: {
      affiliateProduct: { include: { affiliateProgram: true } },
    },
  });
}

export async function setPlacementStatus(
  placementId: string,
  status: "APPROVED" | "REJECTED" | "ACTIVE" | "REMOVED" | "PENDING",
) {
  return prisma.affiliatePlacement.update({
    where: { id: placementId },
    data: {
      status,
      manuallyApproved: status === "APPROVED" || status === "ACTIVE",
    },
  });
}

export async function removePlacement(placementId: string) {
  return prisma.affiliatePlacement.update({
    where: { id: placementId },
    data: { status: "REMOVED" },
  });
}

export async function listPlacementsForVideo(videoId: string) {
  return prisma.affiliatePlacement.findMany({
    where: { videoId, status: { not: "REMOVED" } },
    include: {
      affiliateProduct: {
        include: { affiliateProgram: true, tags: { include: { tag: true } } },
      },
    },
    orderBy: [{ position: "asc" }, { createdAt: "asc" }],
  });
}

export async function getActiveDescriptionPlacements(videoId: string) {
  const placements = await listPlacementsForVideo(videoId);
  return placements.filter(
    (p) =>
      (p.status === "APPROVED" || p.status === "ACTIVE" || p.status === "PENDING") &&
      (p.placementType === "DESCRIPTION_PRIMARY" ||
        p.placementType === "DESCRIPTION_SECONDARY"),
  );
}

export { videoToMatchInput, toProductMatchInput };
