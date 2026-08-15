/**
 * Additive apply of LIVE_PRODUCT_URLS onto existing AffiliateProduct rows.
 * Does not reset the database. Never invents or commits affiliate tags.
 */

import { prisma } from "@/lib/storage/prisma";
import { upsertProductTags } from "./products";
import {
  LIVE_PRODUCT_URLS,
  type LiveProductUrlSpec,
} from "./live-product-urls";

export type ApplyLiveUrlsResult = {
  updated: string[];
  skipped: string[];
  missing: string[];
};

/**
 * Apply confirmed live destination URLs onto matching products.
 * Leaves affiliateUrl empty — tag stamped at /go from AMAZON_ASSOCIATE_TAG.
 */
export async function applyLiveProductUrls(opts?: {
  dryRun?: boolean;
}): Promise<ApplyLiveUrlsResult> {
  const updated: string[] = [];
  const skipped: string[] = [];
  const missing: string[] = [];

  for (const spec of LIVE_PRODUCT_URLS) {
    const product = await prisma.affiliateProduct.findUnique({
      where: { slug: spec.slug },
    });
    if (!product) {
      missing.push(spec.slug);
      continue;
    }

    const affiliateUrl = resolveStoredAffiliateUrl(spec);
    const programmeId = await resolveProgrammeId(spec, product.affiliateProgramId);

    const needsUpdate =
      product.destinationUrl !== spec.destinationUrl ||
      product.affiliateUrl !== affiliateUrl ||
      (spec.active !== undefined && product.active !== spec.active) ||
      (spec.name !== undefined && product.name !== spec.name) ||
      (spec.description !== undefined && product.description !== spec.description) ||
      programmeId !== null;

    if (!needsUpdate) {
      if (!opts?.dryRun && spec.tags?.length) {
        await upsertProductTags(product.id, spec.tags);
      }
      skipped.push(spec.slug);
      continue;
    }

    if (!opts?.dryRun) {
      await prisma.affiliateProduct.update({
        where: { id: product.id },
        data: {
          destinationUrl: spec.destinationUrl,
          affiliateUrl,
          notes: spec.notes,
          urlHealthStatus: "UNKNOWN",
          ...(spec.name ? { name: spec.name } : {}),
          ...(spec.description ? { description: spec.description } : {}),
          ...(spec.active !== undefined ? { active: spec.active } : {}),
          ...(programmeId ? { affiliateProgramId: programmeId } : {}),
        },
      });
      if (spec.tags?.length) {
        await upsertProductTags(product.id, spec.tags);
      }
    }
    updated.push(spec.slug);
  }

  return { updated, skipped, missing };
}

function resolveStoredAffiliateUrl(spec: LiveProductUrlSpec): string {
  if (spec.affiliateUrl === undefined || spec.affiliateUrl === "") {
    return "";
  }
  return spec.affiliateUrl;
}

async function resolveProgrammeId(
  spec: LiveProductUrlSpec,
  currentProgrammeId: string,
): Promise<string | null> {
  if (!spec.programmeSlug) return null;
  const programme = await prisma.affiliateProgram.findUnique({
    where: { slug: spec.programmeSlug },
    select: { id: true },
  });
  if (!programme || programme.id === currentProgrammeId) return null;
  return programme.id;
}
