import { prisma } from "@/lib/storage/prisma";
import {
  appendAffiliateSectionToDescription,
  buildAffiliateDescriptionSection,
  DEFAULT_AFFILIATE_TEMPLATES,
  type AffiliateDescriptionLink,
  type DescriptionTemplateMap,
} from "./description";
import { getActiveDescriptionPlacements } from "./placements";
import { buildOrbitRedirectUrl } from "./urls";

export async function loadDescriptionTemplates(): Promise<DescriptionTemplateMap> {
  const rows = await prisma.affiliateDescriptionTemplate.findMany({
    where: { active: true },
  });
  const map: DescriptionTemplateMap = { ...DEFAULT_AFFILIATE_TEMPLATES };
  for (const row of rows) {
    map[row.key] = row.body;
  }
  return map;
}

export async function buildDescriptionLinksFromVideo(
  videoId: string,
): Promise<AffiliateDescriptionLink[]> {
  const placements = await getActiveDescriptionPlacements(videoId);
  return placements
    .filter((p) => p.status !== "REJECTED")
    .slice(0, 4)
    .map((p) => ({
      productName: p.affiliateProduct.name,
      productSlug: p.affiliateProduct.slug,
      category: p.affiliateProduct.category,
      programSlug: p.affiliateProduct.affiliateProgram.slug,
      url: buildOrbitRedirectUrl(p.affiliateProduct.slug),
    }));
}

/**
 * Extend a YouTube description with the video's approved/pending affiliate block.
 */
export async function generateYouTubeDescriptionWithAffiliates(args: {
  baseDescription: string;
  videoId: string;
  useRedirectUrls?: boolean;
}): Promise<string> {
  const [links, templates] = await Promise.all([
    buildDescriptionLinksFromVideo(args.videoId),
    loadDescriptionTemplates(),
  ]);
  return appendAffiliateSectionToDescription({
    description: args.baseDescription,
    links,
    templates,
    useRedirectUrls: args.useRedirectUrls !== false,
  });
}

export async function previewAffiliateDescriptionBlock(videoId: string): Promise<string> {
  const [links, templates] = await Promise.all([
    buildDescriptionLinksFromVideo(videoId),
    loadDescriptionTemplates(),
  ]);
  return buildAffiliateDescriptionSection({ links, templates });
}

export { appendAffiliateSectionToDescription, buildAffiliateDescriptionSection };
