import {
  DEFAULT_AMAZON_DISCLOSURE,
  DEFAULT_DISCLOSURE,
  type ScoredRecommendation,
} from "./types";
import { buildOrbitRedirectUrl } from "./urls";

export type DescriptionTemplateMap = Record<string, string>;

export const DEFAULT_AFFILIATE_TEMPLATES: DescriptionTemplateMap = {
  section_header: "🚀 Go deeper",
  brilliant:
    "🧠 Want to understand the physics behind this episode? Explore Brilliant:",
  telescope:
    "🔭 Want to explore the night sky yourself? Here’s the telescope setup I recommend:",
  binoculars: "🔭 Ready to start stargazing? These binoculars are a great first step:",
  books: "📚 Go deeper into today’s topic:",
  lego: "🚀 Build your own piece of space exploration:",
  general: "✨ Recommended for this episode:",
  disclosure: DEFAULT_DISCLOSURE,
  amazon_disclosure: DEFAULT_AMAZON_DISCLOSURE,
};

export type AffiliateDescriptionLink = {
  productName: string;
  productSlug: string;
  category: string;
  programSlug?: string;
  url: string;
  role?: ScoredRecommendation["role"];
  templateKey?: string;
};

function pickTemplateKey(link: AffiliateDescriptionLink): string {
  if (link.templateKey) return link.templateKey;
  const cat = link.category.toLowerCase();
  if (link.programSlug === "brilliant" || /physics|mathematics|brilliant/i.test(cat)) {
    return "brilliant";
  }
  if (/telescope/i.test(cat)) return "telescope";
  if (/binocular/i.test(cat)) return "binoculars";
  if (/book/i.test(cat)) return "books";
  if (/lego/i.test(cat)) return "lego";
  return "general";
}

function descriptionAlreadyHasDisclosure(description: string): boolean {
  const lower = description.toLowerCase();
  return (
    lower.includes("affiliate link") ||
    lower.includes("amazon associate") ||
    lower.includes("may receive a commission") ||
    lower.includes("earns from qualifying purchases")
  );
}

function needsAmazonDisclosure(links: AffiliateDescriptionLink[]): boolean {
  return links.some(
    (l) =>
      l.programSlug === "amazon-associates-uk" ||
      /amazon\.(co\.uk|com)/i.test(l.url),
  );
}

/**
 * Build the affiliate block for a YouTube description.
 * Uses Orbit redirect URLs by default (not raw affiliate URLs).
 */
export function buildAffiliateDescriptionSection(args: {
  links: AffiliateDescriptionLink[];
  templates?: DescriptionTemplateMap;
  useRedirectUrls?: boolean;
}): string {
  if (!args.links.length) return "";
  const templates = { ...DEFAULT_AFFILIATE_TEMPLATES, ...args.templates };
  const useRedirect = args.useRedirectUrls !== false;

  const lines: string[] = [templates.section_header || "🚀 Go deeper", ""];

  for (const link of args.links) {
    const key = pickTemplateKey(link);
    const intro = templates[key] || templates.general || "✨ Recommended:";
    const url = useRedirect ? buildOrbitRedirectUrl(link.productSlug) : link.url;
    lines.push(`${intro}`);
    lines.push(`${link.productName}`);
    lines.push(url);
    lines.push("");
  }

  return lines.join("\n").trimEnd();
}

/**
 * Append affiliate section + disclosure to an existing description.
 * Does not duplicate disclosure if one is already present.
 * Dedupes by product slug so the same link never appears twice.
 */
export function appendAffiliateSectionToDescription(args: {
  description: string;
  links: AffiliateDescriptionLink[];
  templates?: DescriptionTemplateMap;
  useRedirectUrls?: boolean;
  includeAmazonDisclosure?: boolean;
}): string {
  const seen = new Set<string>();
  const uniqueLinks = args.links.filter((l) => {
    if (seen.has(l.productSlug)) return false;
    seen.add(l.productSlug);
    return true;
  });

  if (!uniqueLinks.length) return args.description.trimEnd();

  const section = buildAffiliateDescriptionSection({
    links: uniqueLinks,
    templates: args.templates,
    useRedirectUrls: args.useRedirectUrls,
  });

  let result = args.description.trimEnd();
  if (section) {
    result = `${result}\n\n${section}`;
  }

  const templates = { ...DEFAULT_AFFILIATE_TEMPLATES, ...args.templates };
  if (!descriptionAlreadyHasDisclosure(result)) {
    result = `${result}\n\n${templates.disclosure || DEFAULT_DISCLOSURE}`;
    const includeAmazon =
      args.includeAmazonDisclosure !== false && needsAmazonDisclosure(uniqueLinks);
    if (includeAmazon) {
      result = `${result}\n${templates.amazon_disclosure || DEFAULT_AMAZON_DISCLOSURE}`;
    }
  }

  return result;
}

export function recommendationsToDescriptionLinks(
  recommendations: ScoredRecommendation[],
  opts?: { affiliateUrlBySlug?: Record<string, string>; programSlugByProductId?: Record<string, string> },
): AffiliateDescriptionLink[] {
  return recommendations.map((r) => ({
    productName: r.product.name,
    productSlug: r.product.slug,
    category: r.product.category,
    programSlug: opts?.programSlugByProductId?.[r.product.id] || r.product.programSlug,
    url: opts?.affiliateUrlBySlug?.[r.product.slug] || `https://example.invalid/go/${r.product.slug}`,
    role: r.role,
  }));
}
