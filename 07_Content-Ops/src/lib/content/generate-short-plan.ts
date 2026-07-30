import { CONTENT_RULES, HookCategory } from "@/config/content-rules";
import { validateScriptPresent } from "@/lib/validation/schemas";
import { scoreClipQuality } from "@/lib/content/quality-score";
import { VIDEO_PLATFORMS, PlatformId } from "@/config/platforms";

export type ProposedClip = {
  clipNumber: number;
  workingTitle: string;
  hook: string;
  hookCategory: HookCategory;
  alternativeHooks: string[];
  sourceStartTime: string;
  sourceEndTime: string;
  targetDurationSeconds: number;
  transcript: string;
  whyItWorks: string;
  visualDirection: string;
  onScreenText: string;
  endingLine: string;
  callToAction: string;
  suitabilityScore: number;
  platformsRecommended: PlatformId[];
  qualityBreakdown: ReturnType<typeof scoreClipQuality>;
};

type MomentSeed = {
  workingTitle: string;
  hook: string;
  hookCategory: HookCategory;
  alternativeHooks: string[];
  sourceStartTime: string;
  sourceEndTime: string;
  transcript: string;
  whyItWorks: string;
  visualDirection: string;
  onScreenText: string;
  endingLine: string;
};

/**
 * Heuristic clip planner for v1 — rule-based moments from chapter/script cues.
 * Does not call paid APIs. Designed to be swapped for richer NLP later.
 */
export function generateShortPlan(input: {
  title: string;
  script: string;
  youtubeUrl?: string | null;
}): { clips: ProposedClip[]; errors: string[]; warnings: string[] } {
  const errors = validateScriptPresent(input.script);
  if (errors.length) return { clips: [], errors, warnings: [] };

  const seeds = pickMoments(input.title, input.script);
  const warnings: string[] = [];
  if (seeds.length < CONTENT_RULES.clipProposalCount.min) {
    warnings.push("Fewer than 4 strong moments found — review and add manually");
  }

  const cta = CONTENT_RULES.softCtas[0];
  const clips: ProposedClip[] = seeds.map((seed, index) => {
    const duration = estimateDuration(seed.sourceStartTime, seed.sourceEndTime);
    const quality = scoreClipQuality({
      hook: seed.hook,
      hookCategory: seed.hookCategory,
      transcript: seed.transcript,
      endingLine: seed.endingLine,
      callToAction: cta,
      visualDirection: seed.visualDirection,
      targetDurationSeconds: duration,
      whyItWorks: seed.whyItWorks,
    });
    return {
      clipNumber: index + 1,
      workingTitle: seed.workingTitle,
      hook: seed.hook,
      hookCategory: seed.hookCategory,
      alternativeHooks: seed.alternativeHooks,
      sourceStartTime: seed.sourceStartTime,
      sourceEndTime: seed.sourceEndTime,
      targetDurationSeconds: duration,
      transcript: seed.transcript,
      whyItWorks: seed.whyItWorks,
      visualDirection: seed.visualDirection,
      onScreenText: seed.onScreenText,
      endingLine: seed.endingLine,
      callToAction: cta,
      suitabilityScore: quality.total,
      platformsRecommended: [...VIDEO_PLATFORMS],
      qualityBreakdown: quality,
    };
  });

  return { clips, errors: [], warnings };
}

function estimateDuration(start: string, end: string): number {
  const toSec = (t: string) => {
    const p = t.split(":").map(Number);
    return p.length === 2 ? p[0] * 60 + p[1] : p[0] * 3600 + p[1] * 60 + p[2];
  };
  return Math.max(20, toSec(end) - toSec(start));
}

function pickMoments(title: string, script: string): MomentSeed[] {
  const isAliens =
    /alien|fermi|drake|seti|great filter|zoo hypothesis/i.test(`${title} ${script}`);

  if (isAliens) {
    return [
      {
        workingTitle: "The Great Filter",
        hook: "The universe may be hiding something from us.",
        hookCategory: "mystery",
        alternativeHooks: [
          "What if life almost never makes it past a hidden barrier?",
          "There may be a reason the sky stays silent.",
          "One idea could explain why we see no one else.",
        ],
        sourceStartTime: "03:20",
        sourceEndTime: "04:00",
        transcript: extractAround(script, "filter", [
          "Some thinkers call this kind of barrier a Great Filter — a stage so difficult that almost no civilisation crosses it. We do not know if that filter is behind us… or still ahead.",
        ]),
        whyItWorks:
          "Mystery + existential stakes in one idea; standalone without needing the whole Fermi lunch scene.",
        visualDirection:
          "Dark cosmic timeline graphic; Orbit thoughtful PiP; vibrant nebula bed once, then still board pan.",
        onScreenText: "The Great Filter?",
        endingLine: "We do not know if that filter is behind us — or still ahead.",
      },
      {
        workingTitle: "Why the Universe Seems Silent",
        hook: "If the universe should be full of life… why is it so quiet?",
        hookCategory: "direct_question",
        alternativeHooks: [
          "Where is everybody?",
          "A crowded galaxy can still sound empty.",
          "Silence might not mean what we think.",
        ],
        sourceStartTime: "01:40",
        sourceEndTime: "02:25",
        transcript: extractAround(script, "fermi", [
          "If alien civilisations are common… where are they? No radio greetings. No obvious megastructures. Just silence — or at least, silence as far as we can tell.",
        ]),
        whyItWorks: "Classic Fermi hook; strong first sentence; high curiosity retention.",
        visualDirection: "Quiet starfield with Orbit reacting; telescope arrays; no empty distant-galaxy plate.",
        onScreenText: "Where is everybody?",
        endingLine: "That silence has inspired dozens of explanations — most of them incomplete.",
      },
      {
        workingTitle: "How Far an Alien Signal Could Travel",
        hook: "This is why we may never reach another star.",
        hookCategory: "scale_comparison",
        alternativeHooks: [
          "Space is not just big. It is awkwardly big.",
          "Even a quick hello could take generations.",
          "Our nearest neighbour is still impossibly far.",
        ],
        sourceStartTime: "00:50",
        sourceEndTime: "01:35",
        transcript: extractAround(script, "light-year", [
          "Our nearest star system, Alpha Centauri, is about four light-years away. Light itself takes four years to cross that gap. Our fastest spacecraft would need tens of thousands of years.",
        ]),
        whyItWorks: "Scale comparison lands immediately; educational payoff without clickbait.",
        visualDirection: "Distance scale animation Earth → Alpha Centauri; Orbit explaining.",
        onScreenText: "4 light-years",
        endingLine: "And that is the close one.",
      },
      {
        workingTitle: "What First Contact Might Actually Look Like",
        hook: "First contact may not look how you imagine.",
        hookCategory: "scientific_reveal",
        alternativeHooks: [
          "The first alien clue might already be in an archive.",
          "It may arrive as data — not a landing.",
          "A strange chemical imbalance could be the hello.",
        ],
        sourceStartTime: "06:10",
        sourceEndTime: "06:55",
        transcript: extractAround(script, "contact", [
          "Meeting may not mean a handshake. It might mean a radio whisper, a chemical imbalance in an atmosphere, or a pattern we finally learn how to read.",
        ]),
        whyItWorks: "Reframes expectations; soft CTA to full documentary feels natural.",
        visualDirection: "Biosignature spectrum graphic; archive UI motif; Orbit curious.",
        onScreenText: "Not a landing",
        endingLine: "The first hello may already be waiting in the data.",
      },
    ];
  }

  // Generic fallback: chapter-ish paragraphs
  const paragraphs = script
    .split(/\n\n+/)
    .map((p) => p.trim())
    .filter((p) => p.length > 120 && !p.startsWith("#") && !p.startsWith("|"));

  return paragraphs.slice(0, 4).map((p, i) => {
    const first = p.split(/[.!?]/)[0]?.trim() || `Moment ${i + 1}`;
    return {
      workingTitle: first.slice(0, 48),
      hook: first.slice(0, 80),
      hookCategory: "scientific_reveal" as HookCategory,
      alternativeHooks: [first.slice(0, 60)],
      sourceStartTime: formatTime(i * 90 + 30),
      sourceEndTime: formatTime(i * 90 + 70),
      transcript: p.slice(0, 500),
      whyItWorks: "Selected as a dense standalone paragraph with a clear opening line.",
      visualDirection: "Vibrant scenic board matching the beat; Orbit guide PiP optional.",
      onScreenText: first.slice(0, 28),
      endingLine: "The full story is on Orbit with Ben.",
    };
  });
}

function extractAround(script: string, keyword: string, fallback: string[]): string {
  const idx = script.toLowerCase().indexOf(keyword.toLowerCase());
  if (idx < 0) return fallback[0];
  const start = Math.max(0, idx - 120);
  const end = Math.min(script.length, idx + 280);
  const slice = script.slice(start, end).replace(/\s+/g, " ").trim();
  return slice.length > 80 ? slice : fallback[0];
}

function formatTime(totalSeconds: number): string {
  const m = Math.floor(totalSeconds / 60);
  const s = totalSeconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}
