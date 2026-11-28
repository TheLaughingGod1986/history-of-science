import { describe, expect, it } from "vitest";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { auditPaidPlacement, readSponsorshipDeclarations } from "@/lib/hos-contract/paid-placement";
import type { ApiVideo } from "@/lib/hos-contract/rules";
const video = (flag?: boolean | null): ApiVideo => ({ id: "abcdefghijk", paidProductPlacementDetails: { hasPaidProductPlacement: flag } });
describe("paid placement review", () => {
  it("requests the paid-placement part in the common playlist/direct-ID fetch path", () => {
    const source = fs.readFileSync("scripts/channel-audit.ts", "utf8");
    expect(source).toContain("part=snippet,status,contentDetails,paidProductPlacementDetails&id=");
    expect(source).toContain("fetchVideosByIds(token, uniquePlaylistIds)");
    expect(source).toContain("fetchVideosByIds(token, omittedKnownIds)");
  });
  it("shows true with ID without inferring sponsorship from affiliate links", () => {
    expect(auditPaidPlacement(video(true))).toMatchObject({ state: "unexpected-true", findings: [{ severity: "warn", message: expect.stringContaining("abcdefghijk") }] });
  });
  it("keeps declared true visible", () => {
    expect(auditPaidPlacement(video(true), { abcdefghijk: "Chief reference" })).toMatchObject({ state: "declared-sponsored", findings: [{ rule: "paid-placement.declared-sponsored" }] });
  });
  it("false is clean unless a declaration conflicts", () => {
    expect(auditPaidPlacement(video(false))).toEqual({ state: "false", findings: [] });
    expect(auditPaidPlacement(video(false), { abcdefghijk: "reference" }).findings[0].rule).toBe("paid-placement.declaration-mismatch");
  });
  it.each([{}, { paidProductPlacementDetails: null }, { paidProductPlacementDetails: {} }, video(null)])("missing data stays unknown: %j", (fields) => {
    expect(auditPaidPlacement({ id: "abcdefghijk", ...fields })).toMatchObject({ state: "unknown", findings: [{ rule: "paid-placement.unknown" }] });
  });
  it("validates declaration evidence", () => {
    expect(readSponsorshipDeclarations({ abcdefghijk: "Chief reference" })).toEqual({ abcdefghijk: "Chief reference" });
    for (const value of [[], null, { abcdefghijk: "" }, { bad: "ref" }]) expect(() => readSponsorshipDeclarations(value)).toThrow();
  });
  it("CLI exposes states in JSON and text offline", () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), "paid-placement-"));
    try {
      const file = path.join(dir, "videos.json");
      const declarations = path.join(dir, "declarations.json");
      fs.writeFileSync(file, JSON.stringify([video(true), { ...video(false), id: "bcdefghijkl" }, { id: "cdefghijklm" }]));
      fs.writeFileSync(declarations, JSON.stringify({ abcdefghijk: "Chief reference" }));
      const run = (...args: string[]) => {
        try { return execFileSync(process.execPath, ["--import", "tsx", "scripts/channel-audit.ts", "--file", file, ...args], { encoding: "utf8" }); }
        catch (error: any) { if (error.status === 1) return error.stdout as string; throw error; }
      };
      expect(JSON.parse(run("--json", "--sponsorship-declarations", declarations)).rows.map((r: any) => [r.id, r.paidProductPlacement])).toEqual([
        ["abcdefghijk", "declared-sponsored"], ["bcdefghijkl", "false"], ["cdefghijklm", "unknown"],
      ]);
      const text = run();
      expect(text).toContain("paid product placement: unexpected-true");
      expect(text).toContain("paid product placement: unknown");
    } finally { fs.rmSync(dir, { recursive: true, force: true }); }
  });
});
