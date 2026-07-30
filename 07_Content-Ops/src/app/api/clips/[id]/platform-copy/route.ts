import { NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";
import { generatePlatformCopy } from "@/lib/platforms/generate-platform-copy";

export async function POST(
  _req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id } = await ctx.params;
  const clip = await prisma.shortClip.findUnique({
    where: { id },
    include: { longFormVideo: true, posts: true },
  });
  if (!clip) return NextResponse.json({ error: "Clip not found" }, { status: 404 });
  if (clip.status === "proposed" || clip.status === "rejected") {
    return NextResponse.json(
      { error: "Approve the clip before generating final platform copy" },
      { status: 400 },
    );
  }

  const copies = generatePlatformCopy({
    shortTitle: clip.workingTitle,
    hook: clip.hook || clip.workingTitle,
    topic: clip.longFormVideo.topic,
    transcript: clip.transcript,
    youtubeUrl: clip.longFormVideo.youtubeUrl,
    longTitle: clip.longFormVideo.title,
    callToAction: clip.callToAction,
  });

  let count = 0;
  for (const copy of copies) {
    const existing = clip.posts.find((p) => p.platform === copy.platform);
    if (existing) {
      await prisma.platformPost.update({
        where: { id: existing.id },
        data: {
          title: copy.title,
          caption: copy.caption,
          hashtags: JSON.stringify(copy.hashtags),
          callToAction: copy.callToAction,
          pinnedComment: copy.pinnedComment,
          coverText: copy.coverText,
          storyCaption: copy.storyCaption,
          commentPrompt: copy.commentPrompt,
          uploadStatus: existing.uploadStatus === "draft" ? "ready" : existing.uploadStatus,
        },
      });
    } else {
      await prisma.platformPost.create({
        data: {
          shortClipId: clip.id,
          platform: copy.platform,
          title: copy.title,
          caption: copy.caption,
          hashtags: JSON.stringify(copy.hashtags),
          callToAction: copy.callToAction,
          pinnedComment: copy.pinnedComment,
          coverText: copy.coverText,
          storyCaption: copy.storyCaption,
          commentPrompt: copy.commentPrompt,
          uploadStatus: "ready",
          publishingMethod: "manual",
        },
      });
    }
    count += 1;
  }

  return NextResponse.json({ count });
}
