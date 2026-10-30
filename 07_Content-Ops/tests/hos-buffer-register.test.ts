import { describe, expect, it } from "vitest";
import crypto from "crypto";
import fs from "fs";
import os from "os";
import path from "path";
import {
  hosUploadsPath,
  registerHosShortForBuffer,
  resolveOwbRoot,
} from "../src/lib/publishing/hos-buffer-register";

function tmpOwb(): { root: string; uploads: string; cleanup: () => void } {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "j1202-owb-"));
  const social = path.join(root, "00_Brand/Channel-Setup/social/hos");
  fs.mkdirSync(social, { recursive: true });
  const uploads = path.join(social, "UPLOADS.json");
  fs.writeFileSync(uploads, JSON.stringify({ version: 1, videos: {} }, null, 2) + "\n");
  return { root, uploads, cleanup: () => fs.rmSync(root, { recursive: true, force: true }) };
}

describe("hos-buffer-register (J1202)", () => {
  it("resolves Orbit as the sibling orbit-with-ben checkout", () => {
    expect(resolveOwbRoot("/Users/benjaminoats/YouTube/History Of Science")).toBe(
      path.resolve("/Users/benjaminoats/YouTube/orbit-with-ben"),
    );
    expect(hosUploadsPath("/owb")).toBe(path.join("/owb", "00_Brand/Channel-Setup/social/hos/UPLOADS.json"));
  });

  it("registers a Short with sha256 into social/hos/UPLOADS.json and does not invent a Buffer post", () => {
    const owb = tmpOwb();
    const hosRoot = fs.mkdtempSync(path.join(os.tmpdir(), "j1202-hos-"));
    const media = path.join(hosRoot, "short.mp4");
    const body = Buffer.from("fake-hos-short-bytes");
    fs.writeFileSync(media, body);
    try {
      const out = registerHosShortForBuffer({
        hosRepoRoot: hosRoot,
        owbRoot: owb.root,
        videoId: "AbCdEfGhIjK",
        mediaPath: media,
        longId: "wwcjcFfC-5M",
        social: { hook: "Hook line.", question: "A question?" },
        now: new Date("2026-10-30T08:00:00Z"),
      });
      expect(out.entry.sha256).toBe(crypto.createHash("sha256").update(body).digest("hex"));
      expect(out.entry.long).toBe("wwcjcFfC-5M");
      expect(out.entry.file).toBe(media); // outside Orbit → absolute
      expect(out.entry.note).toMatch(/daily check --channel hos/);
      const reg = JSON.parse(fs.readFileSync(owb.uploads, "utf8"));
      expect(reg.videos.AbCdEfGhIjK.sha256).toBe(out.entry.sha256);
      expect(reg.videos.AbCdEfGhIjK.social.hook).toBe("Hook line.");
      // Register only: no BUFFER_POSTS write from this helper.
      expect(fs.existsSync(path.join(owb.root, "00_Brand/Channel-Setup/social/hos/BUFFER_POSTS.json"))).toBe(false);
    } finally {
      owb.cleanup();
      fs.rmSync(hosRoot, { recursive: true, force: true });
    }
  });

  it("refuses a Short with neither long nor standalone", () => {
    const owb = tmpOwb();
    const hosRoot = fs.mkdtempSync(path.join(os.tmpdir(), "j1202-hos-"));
    const media = path.join(hosRoot, "short.mp4");
    fs.writeFileSync(media, "x");
    try {
      expect(() =>
        registerHosShortForBuffer({
          hosRepoRoot: hosRoot,
          owbRoot: owb.root,
          videoId: "AbCdEfGhIjK",
          mediaPath: media,
        }),
      ).toThrow(/longId or standalone/);
    } finally {
      owb.cleanup();
      fs.rmSync(hosRoot, { recursive: true, force: true });
    }
  });
});
