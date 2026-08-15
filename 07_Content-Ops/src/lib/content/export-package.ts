import fs from "fs/promises";
import path from "path";
import { PlatformCopy } from "@/lib/platforms/generate-platform-copy";
import { CaptionExport } from "@/lib/content/captions";
import { PLATFORMS, PlatformId } from "@/config/platforms";

export type ExportPackageInput = {
  exportRoot: string;
  slug: string;
  clipId: string;
  clipNumber: number;
  clipSlug: string;
  sourceVideoTitle: string;
  sourceVideoPath?: string | null;
  sourceStartTime?: string | null;
  sourceEndTime?: string | null;
  platforms: PlatformCopy[];
  captions: CaptionExport;
  scheduledDates?: Partial<Record<PlatformId, string>>;
  publishingStatus?: Partial<Record<PlatformId, string>>;
  videoPlaceholderNote?: string;
};

export type ExportManifest = {
  sourceVideo: string;
  clipId: string;
  sourceTimestamps: { start?: string | null; end?: string | null };
  exportDate: string;
  platforms: PlatformId[];
  titles: Partial<Record<PlatformId, string>>;
  captions: Partial<Record<PlatformId, string>>;
  hashtags: Partial<Record<PlatformId, string[]>>;
  scheduledDates: Partial<Record<PlatformId, string>>;
  filePaths: Record<string, string>;
  publishingStatus: Partial<Record<PlatformId, string>>;
};

const CHECKLISTS: Record<PlatformId, string[]> = {
  youtube_shorts: [
    "Upload vertical MP4",
    "Confirm title",
    "Add description",
    "Add hashtags",
    "Link related long video",
    "Add pinned comment",
    "Confirm visibility",
    "Record published URL",
  ],
  tiktok: [
    "Upload clean video",
    "Confirm no third-party watermark",
    "Add caption",
    "Add hashtags",
    "Select cover frame",
    "Check audio",
    "Publish or schedule",
    "Record published URL",
  ],
  instagram_reels: [
    "Upload clean vertical MP4",
    "Set cover with cover text",
    "Paste caption + hashtags",
    "Add Story share caption if desired",
    "Publish or schedule",
    "Record published URL",
  ],
  instagram_feed: [
    "Paste feed caption (YouTube or /go/ only)",
    "No merchant stickers",
    "Publish or schedule",
    "Record published URL",
  ],
  facebook_reels: [
    "Upload clean vertical MP4",
    "Paste caption + discussion question",
    "Add 2–4 hashtags",
    "Publish or schedule",
    "Record published URL",
  ],
  facebook_page: [
    "Paste documentary Page feed post",
    "One YouTube or /go/ link at the end only",
    "No shop now / Amazon stickers",
    "Publish or schedule",
    "Record published URL",
  ],
  x: [
    "Attach clean clip or still",
    "Paste concise post",
    "Place link near end if used",
    "Publish",
    "Record published URL",
  ],
  threads: [
    "Paste conversational post",
    "Optional follow-up with YouTube link",
    "Publish",
    "Record published URL",
  ],
};

export async function createExportPackage(
  input: ExportPackageInput,
): Promise<{ dir: string; manifest: ExportManifest }> {
  const dir = path.join(
    input.exportRoot,
    input.slug,
    `clip-${String(input.clipNumber).padStart(2, "0")}-${input.clipSlug}`,
  );

  const videoDir = path.join(dir, "video");
  const captionsDir = path.join(dir, "captions");
  const thumbsDir = path.join(dir, "thumbnails");
  const metaDir = path.join(dir, "metadata");

  await fs.mkdir(videoDir, { recursive: true });
  await fs.mkdir(captionsDir, { recursive: true });
  await fs.mkdir(thumbsDir, { recursive: true });
  await fs.mkdir(metaDir, { recursive: true });

  const base = `orbit-${input.clipSlug}`;
  await fs.writeFile(path.join(captionsDir, `${base}.srt`), input.captions.srt);
  await fs.writeFile(path.join(captionsDir, `${base}.vtt`), input.captions.vtt);
  await fs.writeFile(path.join(captionsDir, "transcript.txt"), input.captions.plain);
  await fs.writeFile(
    path.join(captionsDir, "burned-in-script.txt"),
    `${input.captions.burnedInScript}\n\nPOSITIONING\n${input.captions.positioningNotes}\n`,
  );
  await fs.writeFile(
    path.join(captionsDir, "word-timings.json"),
    JSON.stringify(input.captions.wordTimings, null, 2),
  );

  await fs.writeFile(
    path.join(videoDir, "README.txt"),
    input.videoPlaceholderNote ||
      "Place the clean 1080x1920 MP4 here. Never reuse a watermarked download from TikTok/Instagram.\n",
  );
  await fs.writeFile(
    path.join(thumbsDir, "README.txt"),
    "Place youtube-short-cover.png and instagram-reel-cover.png here.\n",
  );

  const titles: ExportManifest["titles"] = {};
  const captions: ExportManifest["captions"] = {};
  const hashtags: ExportManifest["hashtags"] = {};
  const filePaths: Record<string, string> = {
    srt: path.join(captionsDir, `${base}.srt`),
    vtt: path.join(captionsDir, `${base}.vtt`),
    transcript: path.join(captionsDir, "transcript.txt"),
  };

  const checklistLines: string[] = ["# Upload checklist", ""];
  for (const copy of input.platforms) {
    const fname = `${copy.platform.replace(/_/g, "-")}.md`;
    const body = [
      `# ${PLATFORMS[copy.platform].label}`,
      "",
      copy.title ? `## Title\n${copy.title}\n` : "",
      `## Caption\n${copy.caption}\n`,
      `## Hashtags\n${copy.hashtags.map((h) => `#${h.replace(/^#/, "")}`).join(" ")}\n`,
      `## Call to action\n${copy.callToAction}\n`,
      copy.pinnedComment ? `## Pinned comment\n${copy.pinnedComment}\n` : "",
      copy.coverText ? `## Cover text\n${copy.coverText}\n` : "",
      copy.storyCaption ? `## Story caption\n${copy.storyCaption}\n` : "",
      copy.commentPrompt ? `## Comment prompt\n${copy.commentPrompt}\n` : "",
      copy.alternatives?.length
        ? `## Alternatives\n${copy.alternatives.map((a, i) => `${i + 1}. ${a}`).join("\n")}\n`
        : "",
      `## Notes\n${copy.notes.map((n) => `- ${n}`).join("\n")}\n`,
    ]
      .filter(Boolean)
      .join("\n");
    await fs.writeFile(path.join(metaDir, fname), body);
    titles[copy.platform] = copy.title || copy.caption.slice(0, 60);
    captions[copy.platform] = copy.caption;
    hashtags[copy.platform] = copy.hashtags;
    filePaths[`metadata_${copy.platform}`] = path.join(metaDir, fname);

    checklistLines.push(`## ${PLATFORMS[copy.platform].label}`);
    for (const item of CHECKLISTS[copy.platform]) {
      checklistLines.push(`[ ] ${item}`);
    }
    checklistLines.push("");
  }

  await fs.writeFile(path.join(dir, "upload-checklist.md"), checklistLines.join("\n"));

  const manifest: ExportManifest = {
    sourceVideo: input.sourceVideoTitle,
    clipId: input.clipId,
    sourceTimestamps: {
      start: input.sourceStartTime,
      end: input.sourceEndTime,
    },
    exportDate: new Date().toISOString(),
    platforms: input.platforms.map((p) => p.platform),
    titles,
    captions,
    hashtags,
    scheduledDates: input.scheduledDates || {},
    filePaths,
    publishingStatus: input.publishingStatus || {},
  };

  await fs.writeFile(path.join(dir, "manifest.json"), JSON.stringify(manifest, null, 2));
  return { dir, manifest };
}

export function slugify(input: string): string {
  return input
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 48);
}
