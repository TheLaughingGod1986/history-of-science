import {
  DEFAULT_AMAZON_DISCLOSURE,
  type ScoredRecommendation,
} from "./types";
import { buildOrbitRedirectUrl } from "./urls";
import {
  EDITORIAL_TRUST_DISCLOSURE,
  descriptionViolatesEditorialTone,
  filterDescriptionLinksThroughTrustGate,
  hasEditorialTrustDisclosure,
  type EditorialTrustProductInput,
  type EditorialTrustVideoInput,
} from "./editorial-trust-gate";

export type DescriptionTemplateMap = Record<string, string>;

/** Documentary tone — never “buy now / limited / % off”. */
export const DEFAULT_AFFILIATE_TEMPLATES: DescriptionTemplateMap = {
  section_header: "If you want to look at this yourself",
  brilliant: "If you want to understand the physics behind this film:",
  telescope: "If you want to look at this yourself:",
  binoculars: "If you want to start under the night sky:",
  books: "If you want to go deeper into what this film named:",
  paper: "The paper named in this film:",
  lego: "If you want to build a piece of what we explored:",
  general: "If you want to look at this yourself:",
  disclosure: EDITORIAL_TRUST_DISCLOSURE,
  amazon_disclosure: DEFAULT_AMAZON_DISCLOSURE,
};

export type AffiliateDescriptionLink = {
  productName: string;
  productSlug: string;
  category: string;
  programSlug?: string;
  url: string;
  role?: ScoredRecommendation["role"] | "companion";
  templateKey?: string;
  trustProduct?: EditorialTrustProductInput;
};

function pickTemplateKey(link: AffiliateDescriptionLink): string {
  if (link.templateKey) return link.templateKey;
  const cat = link.category.toLowerCase();
  if (/paper|journal|arxiv|jades|study/i.test(cat) || /paper/i.test(link.productName)) {
    return "paper";
  }
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
  if (hasEditorialTrustDisclosure(description)) return true;
  const lower = description.toLowerCase();
  return (
    lower.includes("some links are affiliate") ||
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

function stripLeadingDisclosure(description: string): string {
  const lines = description.split("\n");
  if (lines[0] && /^some links are affiliate/i.test(lines[0].trim())) {
    return lines.slice(1).join("\n").replace(/^\n+/, "").trim();
  }
  return description.trim();
}

/**
 * Build the affiliate block for a YouTube description.
 * Documentary tone only. Orbit redirect URLs by default.
 */
export function buildAffiliateDescriptionSection(args: {
  links: AffiliateDescriptionLink[];
  templates?: DescriptionTemplateMap;
  useRedirectUrls?: boolean;
}): string {
  if (!args.links.length) return "";
  const templates = { ...DEFAULT_AFFILIATE_TEMPLATES, ...args.templates };
  const useRedirect = args.useRedirectUrls !== false;

  const lines: string[] = [
    templates.section_header || "If you want to look at this yourself",
    "",
  ];

  for (const link of args.links) {
    const key = pickTemplateKey(link);
    const intro =
      templates[key] || templates.general || "If you want to look at this yourself:";
    if (descriptionViolatesEditorialTone(intro).length) continue;
    const url = useRedirect ? buildOrbitRedirectUrl(link.productSlug) : link.url;
    lines.push(intro);
    lines.push(link.productName);
    lines.push(url);
    lines.push("");
  }

  return lines.join("\n").trimEnd();
}

export type AppendAffiliateOptions = {
  description: string;
  links: AffiliateDescriptionLink[];
  templates?: DescriptionTemplateMap;
  useRedirectUrls?: boolean;
  includeAmazonDisclosure?: boolean;
  /** When set, links must pass the Video Auditor trust gate before insert. */
  trustVideo?: EditorialTrustVideoInput;
};

/**
 * Place affiliate content **below** the real CTA (film body / subscribe).
 * Disclosure once as the **first line** of the description when affiliate links exist.
 * Trust gate filters links when `trustVideo` is provided (fail closed without product metadata).
 */
export function appendAffiliateSectionToDescription(args: AppendAffiliateOptions): string {
  let links = args.links;

  if (args.trustVideo) {
    const withTrust = links.filter((l) => l.trustProduct);
    if (!withTrust.length) {
      return args.description.trimEnd();
    }
    const { accepted } = filterDescriptionLinksThroughTrustGate({
      video: args.trustVideo,
      candidates: withTrust.map((l) => ({
        product: l.trustProduct!,
        role:
          l.role === "companion"
            ? "companion"
            : l.role === "primary"
              ? "primary"
              : "secondary",
      })),
    });
    const ok = new Set(accepted.map((a) => a.product.id));
    links = withTrust.filter((l) => ok.has(l.trustProduct!.id));
  }

  const seen = new Set<string>();
  const uniqueLinks = links
    .filter((l) => {
      if (seen.has(l.productSlug)) return false;
      seen.add(l.productSlug);
      return true;
    })
    .slice(0, 2);

  if (!uniqueLinks.length) return args.description.trimEnd();

  const section = buildAffiliateDescriptionSection({
    links: uniqueLinks,
    templates: args.templates,
    useRedirectUrls: args.useRedirectUrls,
  });
  if (!section || descriptionViolatesEditorialTone(section).length) {
    return args.description.trimEnd();
  }

  const templates = { ...DEFAULT_AFFILIATE_TEMPLATES, ...args.templates };
  const disclosure = templates.disclosure || EDITORIAL_TRUST_DISCLOSURE;

  // Keep film CTA body above affiliate; disclosure is always the first line when links exist
  let body = stripLeadingDisclosure(args.description.trimEnd());

  // Avoid duplicating the same affiliate block if generator is called twice
  for (const link of uniqueLinks) {
    if (body.includes(link.productSlug) || body.includes(buildOrbitRedirectUrl(link.productSlug))) {
      // Already present — ensure disclosure is first line, do not stack another block
      if (!hasEditorialTrustDisclosure(args.description) && !descriptionAlreadyHasDisclosure(body)) {
        return `${disclosure}\n\n${body}`.trim();
      }
      if (hasEditorialTrustDisclosure(args.description) || /^some links are affiliate/i.test(args.description.trim())) {
        return args.description.trimEnd();
      }
      return `${disclosure}\n\n${body}`.trim();
    }
  }

  const hadDisclosure = descriptionAlreadyHasDisclosure(args.description);
  let result = `${body}\n\n${section}`.trim();

  if (!hadDisclosure || !hasEditorialTrustDisclosure(args.description)) {
    result = `${disclosure}\n\n${result}`;
    if (
      args.includeAmazonDisclosure !== false &&
      needsAmazonDisclosure(uniqueLinks) &&
      !result.includes(templates.amazon_disclosure || DEFAULT_AMAZON_DISCLOSURE)
    ) {
      result = `${result}\n${templates.amazon_disclosure || DEFAULT_AMAZON_DISCLOSURE}`;
    }
  } else {
    result = `${disclosure}\n\n${body}\n\n${section}`.trim();
  }

  return result.trim();
}

export function recommendationsToDescriptionLinks(
  recommendations: ScoredRecommendation[],
  opts?: {
    affiliateUrlBySlug?: Record<string, string>;
    programSlugByProductId?: Record<string, string>;
  },
): AffiliateDescriptionLink[] {
  return recommendations.map((r) => ({
    productName: r.product.name,
    productSlug: r.product.slug,
    category: r.product.category,
    programSlug: opts?.programSlugByProductId?.[r.product.id] || r.product.programSlug,
    url:
      opts?.affiliateUrlBySlug?.[r.product.slug] ||
      `https://example.invalid/go/${r.product.slug}`,
    role: r.role,
    trustProduct: r.product,
  }));
}
