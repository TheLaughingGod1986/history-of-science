import { describe, expect, it } from "vitest";
import { lengthBonus, reviewScript } from "@/lib/analytics/script-reviewer";

// 1 Oct 2026: the reviewer was built for Orbit (space words) and capped every HOS discovery film
// below 90 (004 v02 88.9, 005 v01 84.4). These pin the fixes.
const HOS = `# A Title That Is Not Spoken (script master v01)

## PART 01: The Open (0:00–1:00)

Why did doctors believe blood was used up? Harvey measured it, tested it and proved them wrong.
But nobody believed him. Then he published the evidence. Now the experiment is famous.
`;

describe("script reviewer on HOS discovery scripts", () => {
  it("counts every science and escalation hit, not just the first", () => {
    const r = reviewScript(HOS);
    const one = reviewScript("Harvey measured it.");
    expect(r.scores.scientificAccuracy).toBeGreaterThan(one.scores.scientificAccuracy);
    expect(r.scores.escalation).toBeGreaterThan(reviewScript("But nobody believed him.").scores.escalation);
  });

  it("scores history-of-science method words, not only space words", () => {
    expect(reviewScript("He discovered it, proved it and published the evidence.").scores.scientificAccuracy).toBeGreaterThan(
      reviewScript("He found it and wrote it down.").scores.scientificAccuracy,
    );
  });

  it("keeps headings out of the word count and the cold open", () => {
    const r = reviewScript(HOS);
    expect(r.estimates.wordCount).toBe(reviewScript(HOS.replace(/^#.*$/gm, "")).estimates.wordCount);
    expect(r.coldOpenExcerpt.startsWith("Why did doctors")).toBe(true);
  });

  it("has no cliff at 8 minutes: a few words either side barely move the score", () => {
    expect(lengthBonus(8)).toBe(2);
    expect(lengthBonus(12)).toBe(2);
    expect(lengthBonus(6.9)).toBe(0);
    expect(lengthBonus(7.98)).toBeCloseTo(1.96, 2);
    const words = (n: number) => Array.from({ length: n }, () => "word").join(" ");
    const short = reviewScript(words(1197)).total;
    const long = reviewScript(words(1203)).total;
    expect(Math.abs(long - short)).toBeLessThan(0.5);
  });
});
