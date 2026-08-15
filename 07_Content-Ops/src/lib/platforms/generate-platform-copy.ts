import { CHANNEL_NAME, PlatformId, PLATFORMS } from "@/config/platforms";
import { CONTENT_RULES } from "@/config/content-rules";
import {
  applyAffiliateSocialConstraints,
  type AffiliateSocialContext,
} from "@/lib/affiliate/social-copy";

export type ClipCopyInput = {
  shortTitle: string;
  hook: string;
  topic: string;
  transcript?: string | null;
  youtubeUrl?: string | null;
  longTitle?: string | null;
  callToAction?: string | null;
  hashtags?: string[];
  /**
   * Optional affiliate context. When present, social copy is hard-constrained:
   * no raw merchant URLs, max one soft mention, science first.
   */
  affiliate?: AffiliateSocialContext | null;
};

export type PlatformCopy = {
  platform: PlatformId;
  title?: string;
  caption: string;
  hashtags: string[];
  callToAction: string;
  pinnedComment?: string;
  coverText?: string;
  storyCaption?: string;
  commentPrompt?: string;
  alternatives?: string[];
  notes: string[];
};

function truncate(s: string, max: number): string {
  if (s.length <= max) return s;
  return s.slice(0, max - 1).trimEnd() + "…";
}

function defaultHashtags(topic: string): string[] {
  const base = ["OrbitWithBen", "Space", "Astronomy"];
  if (/alien|fermi/i.test(topic)) return ["FermiParadox", "AreWeAlone", ...base];
  return [topic.replace(/\s+/g, ""), ...base].slice(0, 5);
}

export function renderTemplate(
  template: string,
  vars: Record<string, string | undefined | null>,
): string {
  return template.replace(/\{\{(\w+)\}\}/g, (_, key: string) => vars[key] ?? "");
}

function buildBasePlatformCopy(input: ClipCopyInput): PlatformCopy[] {
  const cta = input.callToAction || CONTENT_RULES.softCtas[0];
  const tags = input.hashtags?.length ? input.hashtags : defaultHashtags(input.topic);
  const url = input.youtubeUrl || "";
  const long = input.longTitle || input.topic;

  return [
    {
      platform: "youtube_shorts",
      title: truncate(input.hook || input.shortTitle, PLATFORMS.youtube_shorts.maxTitleLength!),
      caption: [
        input.hook,
        "",
        url ? `Full film:\n${url}` : `Full story on ${CHANNEL_NAME}.`,
        "",
        tags.map((t) => `#${t.replace(/^#/, "")}`).join(" "),
      ].join("\n"),
      hashtags: tags.slice(0, 5),
      callToAction: cta,
      pinnedComment: url
        ? `Full documentary: ${url}`
        : `The full explanation is on the channel — ${CHANNEL_NAME}.`,
      notes: ["Keep title under ~60 characters", "Link related long-form video", "Soft CTA only"],
    },
    {
      platform: "tiktok",
      caption: `${input.hook}\n\n${cta}\n\n${tags
        .slice(0, 5)
        .map((t) => `#${t.replace(/^#/, "")}`)
        .join(" ")}`,
      hashtags: tags.slice(0, 5),
      callToAction: cta,
      commentPrompt: "Which explanation for the silence do you find most convincing?",
      notes: [
        "Natural, curious tone",
        "No third-party watermark",
        "Optional reply-video idea: deepen one comment question",
      ],
    },
    {
      platform: "instagram_reels",
      caption: `${input.hook}\n\n${cta}\n\nSave this if you love big questions.\n\n${tags
        .slice(0, 5)
        .map((t) => `#${t.replace(/^#/, "")}`)
        .join(" ")}`,
      hashtags: tags.slice(0, 5),
      callToAction: cta,
      coverText: truncate(input.shortTitle, 42),
      storyCaption: `${input.hook} — full film on YouTube.`,
      notes: ["Cover text ≤ 5–7 words", "Include save/share prompt"],
    },
    {
      platform: "facebook_reels",
      caption: `${input.hook}\n\n${input.transcript?.slice(0, 220) || long}\n\nWhat do you think — are we early, or just looking in the wrong way?\n\n${tags
        .slice(0, 4)
        .map((t) => `#${t.replace(/^#/, "")}`)
        .join(" ")}`,
      hashtags: tags.slice(0, 4),
      callToAction: cta,
      notes: ["Slightly more explanatory than TikTok", "Invite discussion"],
    },
    {
      platform: "instagram_feed",
      caption: `${input.hook}\n\n${cta}\n\nFull film on YouTube${url ? `:\n${url}` : "."}\n\n${tags
        .slice(0, 4)
        .map((t) => `#${t.replace(/^#/, "")}`)
        .join(" ")}`,
      hashtags: tags.slice(0, 4),
      callToAction: cta,
      notes: ["Instagram feed caption — distinct from Reels", "No merchant stickers"],
    },
    {
      platform: "facebook_page",
      caption: `${input.hook}\n\n${(input.transcript || long).slice(0, 320)}\n\n${
        url ? `Full documentary:\n${url}` : `Full story on ${CHANNEL_NAME}.`
      }`,
      hashtags: tags.slice(0, 2),
      callToAction: cta,
      notes: [
        "Facebook Page feed — distinct from facebook_reels",
        "Documentary tone; one YouTube or /go/ link at the end; never shop now",
      ],
    },
    {
      platform: "x",
      caption: truncate(
        url ? `${input.hook} ${url}` : `${input.hook}`,
        PLATFORMS.x.maxCaptionLength!,
      ),
      hashtags: tags.slice(0, 2),
      callToAction: cta,
      alternatives: [
        truncate(`${input.hook.replace(/\.$/, "")}?`, 280),
        truncate(
          `${input.hook}\n\n1/ A quick thought from our latest Orbit film.\n2/ ${cta}${url ? `\n3/ ${url}` : ""}`,
          900,
        ),
      ],
      notes: ["Prefer insight over title+link paste", "Link near end when used"],
    },
    {
      platform: "threads",
      caption: `${input.hook}\n\n${(input.transcript || "").slice(0, 280)}\n\n${cta}`,
      hashtags: tags.slice(0, 2),
      callToAction: cta,
      alternatives: [
        `Honest question: ${input.hook}`,
        `Mini explainer:\n${(input.transcript || input.hook).slice(0, 320)}`,
      ],
      notes: ["Conversational", "Optional follow-up comment with YouTube link"],
    },
  ];
}

/**
 * Generate platform social copy. When `affiliate` context is provided,
 * house rules are applied (sanitize merchant URLs; at most one soft mention).
 */
export function generatePlatformCopy(input: ClipCopyInput): PlatformCopy[] {
  const base = buildBasePlatformCopy(input);
  if (!input.affiliate) return base;
  return applyAffiliateSocialConstraints(base, input.affiliate).copies;
}

export type { AffiliateSocialContext };
