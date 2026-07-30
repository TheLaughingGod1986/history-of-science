import { CONTENT_RULES, HookCategory } from "@/config/content-rules";

export type QualityBreakdown = {
  hookStrength: number;
  standaloneClarity: number;
  curiosity: number;
  scientificAccuracy: number;
  pacing: number;
  visualPotential: number;
  payoff: number;
  ctaSubtlety: number;
  reasons: string[];
  total: number;
};

export type ClipScoreInput = {
  hook?: string | null;
  hookCategory?: string | null;
  transcript?: string | null;
  endingLine?: string | null;
  callToAction?: string | null;
  visualDirection?: string | null;
  targetDurationSeconds?: number | null;
  whyItWorks?: string | null;
};

function clamp(n: number, max: number): number {
  return Math.max(0, Math.min(max, Math.round(n)));
}

export function scoreClipQuality(input: ClipScoreInput): QualityBreakdown {
  const reasons: string[] = [];
  const w = CONTENT_RULES.qualityWeights;
  const hook = (input.hook || "").trim();
  const transcript = (input.transcript || "").trim();
  const cta = (input.callToAction || "").toLowerCase();
  const duration = input.targetDurationSeconds ?? 0;

  let hookStrength = 8;
  if (hook.length > 12) hookStrength += 4;
  if (hook.includes("?") || /may|might|could|never|hiding|silent/i.test(hook)) {
    hookStrength += 4;
  }
  if (CONTENT_RULES.avoidPhrases.some((p) => hook.toLowerCase().includes(p))) {
    hookStrength -= 10;
    reasons.push("Hook contains a banned/hype phrase");
  }
  if (input.hookCategory && CONTENT_RULES.hookCategories.includes(input.hookCategory as HookCategory)) {
    hookStrength += 3;
    reasons.push(`Hook category: ${input.hookCategory}`);
  }
  hookStrength = clamp(hookStrength, w.hookStrength);

  let standaloneClarity = transcript.length > 80 ? 12 : 6;
  if (transcript.length > 200) standaloneClarity += 3;
  if (/hey guys|in today's video|as i said earlier/i.test(transcript)) {
    standaloneClarity -= 6;
    reasons.push("Transcript relies on prior context or intro filler");
  } else {
    reasons.push("Transcript reads as mostly standalone");
  }
  standaloneClarity = clamp(standaloneClarity, w.standaloneClarity);

  let curiosity = input.whyItWorks ? 12 : 7;
  if (/mystery|paradox|silence|filter|signal/i.test(`${hook} ${transcript}`)) curiosity += 3;
  curiosity = clamp(curiosity, w.curiosity);

  let scientificAccuracy = 12;
  if (/definitely proven|guaranteed aliens|cover.?up/i.test(transcript)) {
    scientificAccuracy -= 10;
    reasons.push("Over-certain or conspiratorial language reduces accuracy score");
  } else {
    reasons.push("Tone stays scientifically responsible");
  }
  scientificAccuracy = clamp(scientificAccuracy, w.scientificAccuracy);

  let pacing = 5;
  if (
    duration >= CONTENT_RULES.shortDuration.minSeconds &&
    duration <= CONTENT_RULES.shortDuration.maxSeconds
  ) {
    pacing += 3;
  }
  if (
    duration >= CONTENT_RULES.shortDuration.preferredMin &&
    duration <= CONTENT_RULES.shortDuration.preferredMax
  ) {
    pacing += 2;
    reasons.push("Duration sits in preferred 31–42s range");
  }
  pacing = clamp(pacing, w.pacing);

  let visualPotential = input.visualDirection ? 8 : 4;
  if (/orbit|planet|telescope|surface|atmosphere/i.test(input.visualDirection || "")) {
    visualPotential += 2;
  }
  visualPotential = clamp(visualPotential, w.visualPotential);

  let payoff = input.endingLine ? 8 : 4;
  if (input.endingLine && input.endingLine.length > 20) payoff += 2;
  payoff = clamp(payoff, w.payoff);

  let ctaSubtlety = 3;
  if (CONTENT_RULES.softCtas.some((s) => cta.includes(s.toLowerCase().slice(0, 20)))) {
    ctaSubtlety = 5;
    reasons.push("Uses a soft Orbit CTA");
  } else if (/subscribe|smash|follow for more/i.test(cta)) {
    ctaSubtlety = 1;
    reasons.push("CTA feels promotional");
  }
  ctaSubtlety = clamp(ctaSubtlety, w.ctaSubtlety);

  const total =
    hookStrength +
    standaloneClarity +
    curiosity +
    scientificAccuracy +
    pacing +
    visualPotential +
    payoff +
    ctaSubtlety;

  return {
    hookStrength,
    standaloneClarity,
    curiosity,
    scientificAccuracy,
    pacing,
    visualPotential,
    payoff,
    ctaSubtlety,
    reasons,
    total,
  };
}
