import { describe, expect, it } from "vitest";
import fs from "fs";
import os from "os";
import path from "path";
import { countExplorerBeats, gateEpisode } from "../src/lib/analytics/episode-gate";
import { reviewScript } from "../src/lib/analytics/script-reviewer";

const HOS_SCRIPT = `
What if you could see a living skeleton, without cutting anyone open?

[CHAPTER CARD: Part 01 — The Dark Lab]
[VISUAL MUST: a glowing tube in a dark 1895 lab]
[TEACH: cathode rays make the glass glow]

Würzburg, 1895. But something glows across the room.

[CHAPTER CARD: Part 02 — The Cardboard]
[VISUAL MUST: a screen glowing through black card]
[EXPLORER ACTS: once — peeks at the tube, steps back when it flares]
[TEACH: the rays pass through card]

[CHAPTER CARD: Part 03 — Bones]
[VISUAL MUST: a hand's bones on the screen]
[EXPLORER ACTS: none]
[TEACH: dense bone stops the rays]
`;

describe("Explorer beats", () => {
  it("counts [EXPLORER ACTS] and skips markers that say he is absent", () => {
    expect(countExplorerBeats(HOS_SCRIPT)).toBe(1);
    expect(countExplorerBeats("[EXPLORER ACTS: Explorer is not in this act]")).toBe(0);
    expect(countExplorerBeats("[ORBIT ACTS: Explorer lifts a heavy ore]")).toBe(1);
  });

  it("passes the gate's beat check on an HOS script with no [ORBIT ACTS]", () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), "hos-gate-"));
    fs.mkdirSync(path.join(dir, "01_Script"));
    fs.writeFileSync(path.join(dir, "01_Script", "x_script_master_v01.md"), HOS_SCRIPT);
    const beat = gateEpisode({ projectDir: dir }).checks.find((c) => c.id === "explorer_acts");
    expect(beat?.ok).toBe(true);
    expect(beat?.severity).toBe("info");
  });

  it("warns above three Explorer beats", () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), "hos-gate-"));
    fs.mkdirSync(path.join(dir, "01_Script"));
    const busy = Array.from({ length: 4 }, (_, i) => `[EXPLORER ACTS: beat ${i + 1}]`).join("\n");
    fs.writeFileSync(path.join(dir, "01_Script", "x_script_master_v01.md"), `${HOS_SCRIPT}\n${busy}`);
    const beat = gateEpisode({ projectDir: dir }).checks.find((c) => c.id === "explorer_acts");
    expect(beat?.ok).toBe(true);
    expect(beat?.severity).toBe("warn");
  });

  it("credits [EXPLORER ACTS] like the old [ORBIT ACTS] marker", () => {
    const legacy = HOS_SCRIPT.replace(/EXPLORER ACTS/g, "ORBIT ACTS");
    const noBeats = HOS_SCRIPT.replace(/\[EXPLORER ACTS:[^\]]*\]/g, "");
    expect(reviewScript(HOS_SCRIPT).scores.visualOpportunities).toBe(reviewScript(legacy).scores.visualOpportunities);
    expect(reviewScript(HOS_SCRIPT).total).toBeGreaterThan(reviewScript(noBeats).total);
    expect(reviewScript(HOS_SCRIPT).estimates.wordCount).toBe(reviewScript(noBeats).estimates.wordCount);
    const findings = reviewScript(HOS_SCRIPT).findings.map((f) => f.message).join("\n");
    expect(findings).not.toMatch(/No character beats/);
  });
});
