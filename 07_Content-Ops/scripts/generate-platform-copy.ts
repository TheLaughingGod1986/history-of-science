#!/usr/bin/env tsx
import { generatePlatformCopy } from "../src/lib/platforms/generate-platform-copy";

const input = {
  shortTitle: process.argv[2] || "The Great Filter",
  hook: process.argv[3] || "The universe may be hiding something from us.",
  topic: process.argv[4] || "Alien Civilisations",
  youtubeUrl: process.argv[5] || "https://youtu.be/Mo93x0fxB1Q",
};

console.log(JSON.stringify(generatePlatformCopy(input), null, 2));
