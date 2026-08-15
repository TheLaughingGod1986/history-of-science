import Link from "next/link";
import { notFound } from "next/navigation";
import { prisma } from "@/lib/storage/prisma";
import { formatLondon } from "@/lib/publishing/schedule";
import { PLATFORMS } from "@/config/platforms";
import { DistributionPackButton } from "@/components/DistributionPackButton";
import { ClipActions } from "@/components/ClipActions";
import { VideoAffiliatePanel } from "@/components/affiliate/VideoAffiliatePanel";
import { getVideoAffiliatePanel } from "@/lib/affiliate/analytics";
import { generateRecommendationsForVideo } from "@/lib/affiliate/placements";
import { previewAffiliateDescriptionBlock } from "@/lib/affiliate/description-service";

export const dynamic = "force-dynamic";

export default async function VideoDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const video = await prisma.longFormVideo.findUnique({
    where: { id },
    include: {
      clips: {
        orderBy: { sortOrder: "asc" },
        include: { posts: true },
      },
    },
  });
  if (!video) notFound();

  const affiliatePanel = await getVideoAffiliatePanel(video.id);
  let descriptionPreview: string | null = null;
  try {
    if (affiliatePanel && affiliatePanel.placements.length > 0) {
      descriptionPreview = await previewAffiliateDescriptionBlock(video.id);
    } else {
      const recs = await generateRecommendationsForVideo(video.id);
      if (recs.recommendations.length) {
        descriptionPreview = `${recs.recommendations.length} recommendation(s) ready — regenerate placements to insert.`;
      }
    }
  } catch {
    descriptionPreview = null;
  }

  return (
    <div className="space-y-8 overflow-x-hidden">
      <div className="flex flex-col gap-4 sm:flex-row sm:flex-wrap sm:items-start sm:justify-between">
        <div className="min-w-0">
          <Link
            href="/videos"
            className="inline-flex min-h-11 items-center text-sm text-[#5A6E82] hover:text-[#F5E8D2]"
          >
            ← Long-form library
          </Link>
          <h1 className="mt-2 break-words font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2] sm:mt-3 sm:text-3xl">
            {video.workingTitle || video.title}
          </h1>
          {video.workingTitle ? (
            <p className="mt-2 break-words text-[#F5E8D2]/55">{video.title}</p>
          ) : null}
          <div className="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-xs uppercase tracking-[0.16em] text-[#FF7A24]">
            <span>{video.status}</span>
            <span className="break-words">{video.topic}</span>
            {video.publicationDate ? <span>{formatLondon(video.publicationDate)}</span> : null}
          </div>
        </div>
        <div className="w-full sm:w-auto sm:[&>div]:text-right [&_button]:min-h-11 [&_button]:w-full sm:[&_button]:w-auto">
          <DistributionPackButton videoId={video.id} />
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <div className="card-panel p-4 sm:p-5 lg:col-span-2">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Script</h2>
          <pre className="mt-4 max-h-80 overflow-auto whitespace-pre-wrap break-words text-sm text-[#F5E8D2]/70">
            {(video.script || "").slice(0, 4000)}
            {(video.script || "").length > 4000 ? "\n…" : ""}
          </pre>
        </div>
        <div className="card-panel space-y-3 p-4 text-sm text-[#F5E8D2]/70 sm:p-5">
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">YouTube</div>
            <div className="mt-1 break-all">{video.youtubeUrl || "—"}</div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">Project folder</div>
            <div className="mt-1 break-all">{video.projectFolder || "—"}</div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">Primary keyword</div>
            <div className="mt-1 break-words">{video.primaryKeyword || "—"}</div>
          </div>
        </div>
      </div>

      {affiliatePanel ? (
        <VideoAffiliatePanel
          videoId={video.id}
          opportunityScore={affiliatePanel.opportunity.total}
          placements={affiliatePanel.placements.map((p) => ({
            id: p.id,
            status: p.status,
            placementType: p.placementType,
            relevanceScore: p.relevanceScore,
            affiliateProduct: {
              id: p.affiliateProduct.id,
              name: p.affiliateProduct.name,
              slug: p.affiliateProduct.slug,
              category: p.affiliateProduct.category,
              estimatedCommission: p.affiliateProduct.estimatedCommission,
              affiliateProgram: { name: p.affiliateProduct.affiliateProgram.name },
            },
          }))}
        />
      ) : null}

      {descriptionPreview ? (
        <div className="card-panel p-5">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">
            Affiliate description preview
          </h2>
          <pre className="mt-3 whitespace-pre-wrap text-sm text-[#F5E8D2]/65">
            {descriptionPreview}
          </pre>
        </div>
      ) : null}

      <section className="space-y-4">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl">Short clips</h2>
        {video.clips.length === 0 ? (
          <div className="card-panel p-5 text-sm text-[#F5E8D2]/65">
            No short clips yet. Create a distribution pack to propose clips from this film.
          </div>
        ) : null}
        {video.clips.map((clip) => {
          const platformsPosted = new Set(clip.posts.map((p) => p.platform));
          const missing = Object.keys(PLATFORMS).filter((p) => !platformsPosted.has(p));
          return (
            <div key={clip.id} className="card-panel p-4 sm:p-5">
              <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-start sm:justify-between">
                <div className="min-w-0">
                  <div className="text-xs uppercase tracking-[0.16em] text-[#FF7A24]">
                    Clip {clip.clipNumber} · {clip.status} · score {clip.qualityScore ?? "—"}
                  </div>
                  <h3 className="mt-2 break-words text-xl text-[#F5E8D2]">{clip.workingTitle}</h3>
                  <p className="mt-1 break-words text-sm text-[#F5E8D2]/65">{clip.hook}</p>
                  <p className="mt-2 text-xs text-[#5A6E82]">
                    {clip.sourceStartTime} → {clip.sourceEndTime} · {clip.targetDurationSeconds}s ·{" "}
                    {clip.hookCategory}
                  </p>
                </div>
                <div className="[&_button]:inline-flex [&_button]:min-h-11 [&_button]:items-center [&_button]:px-4 [&_button]:py-2 [&_button]:text-sm">
                  <ClipActions clipId={clip.id} status={clip.status} />
                </div>
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <div className="rounded-xl bg-white/3 p-3 text-sm text-[#F5E8D2]/70">
                  <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Transcript</div>
                  <p className="mt-2 break-words">{clip.transcript}</p>
                </div>
                <div className="rounded-xl bg-white/3 p-3 text-sm text-[#F5E8D2]/70">
                  <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">
                    Platform coverage
                  </div>
                  <p className="mt-2 break-words">
                    Tracked: {Array.from(platformsPosted).join(", ") || "none"}
                  </p>
                  <p className="mt-1 break-words text-[#FFC85A]/80">
                    Missing: {missing.join(", ") || "none"}
                  </p>
                  <Link
                    href={`/clips/${clip.id}`}
                    className="mt-3 inline-flex min-h-11 items-center text-[#FF7A24] hover:underline"
                  >
                    Open clip workspace →
                  </Link>
                </div>
              </div>
            </div>
          );
        })}
      </section>
    </div>
  );
}
