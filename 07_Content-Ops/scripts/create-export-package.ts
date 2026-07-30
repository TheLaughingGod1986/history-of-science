#!/usr/bin/env tsx
import path from "path";
import { createExportPackage, slugify } from "../src/lib/content/export-package";
import { exportCaptions } from "../src/lib/content/captions";
import { generatePlatformCopy } from "../src/lib/platforms/generate-platform-copy";

async function main() {
  const title = "The Great Filter";
  const copies = generatePlatformCopy({
    shortTitle: title,
    hook: "The universe may be hiding something from us.",
    topic: "Alien Civilisations",
    transcript:
      "Some thinkers call this kind of barrier a Great Filter — a stage so difficult that almost no civilisation crosses it.",
    youtubeUrl: "https://youtu.be/Mo93x0fxB1Q",
  });
  const captions = exportCaptions({
    transcript: copies[0].caption,
    startSeconds: 0,
    endSeconds: 40,
  });
  const result = await createExportPackage({
    exportRoot: path.join(process.cwd(), "content", "exports"),
    slug: "2026-08-will-we-ever-meet-aliens",
    clipId: "demo-clip",
    clipNumber: 1,
    clipSlug: slugify(title),
    sourceVideoTitle: "Will We Ever Meet Aliens?",
    sourceStartTime: "03:20",
    sourceEndTime: "04:00",
    platforms: copies,
    captions,
  });
  console.log(result.dir);
}

main();
