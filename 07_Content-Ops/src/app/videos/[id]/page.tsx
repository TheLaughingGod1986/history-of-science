import Link from "next/link";
import { notFound } from "next/navigation";
import { prisma } from "@/lib/storage/prisma";
import { formatLondon } from "@/lib/publishing/schedule";
import { PLATFORMS } from "@/config/platforms";
import { DistributionPackButton } from "@/components/DistributionPackButton";
import { ClipActions } from "@/components/ClipActions";

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

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <Link href="/videos" className="text-sm text-[#5A6E82] hover:text-[#F5E8D2]">
            ← Long-form library
          </Link>
          <h1 className="mt-3 font-[family-name:var(--font-orbit-display)] text-3xl text-[#F5E8D2]">
            {video.workingTitle || video.title}
          </h1>
          <p className="mt-2 text-[#F5E8D2]/55">{video.title}</p>
          <div className="mt-3 flex flex-wrap gap-3 text-xs uppercase tracking-[0.16em] text-[#FF7A24]">
            <span>{video.status}</span>
            <span>{video.topic}</span>
            {video.publicationDate ? <span>{formatLondon(video.publicationDate)}</span> : null}
          </div>
        </div>
        <DistributionPackButton videoId={video.id} />
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <div className="card-panel p-5 lg:col-span-2">
          <h2 className="font-[family-name:var(--font-orbit-display)] text-xl">Script</h2>
          <pre className="mt-4 max-h-80 overflow-auto whitespace-pre-wrap text-sm text-[#F5E8D2]/70">
            {(video.script || "").slice(0, 4000)}
            {(video.script || "").length > 4000 ? "\n…" : ""}
          </pre>
        </div>
        <div className="card-panel space-y-3 p-5 text-sm text-[#F5E8D2]/70">
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">YouTube</div>
            <div className="mt-1 break-all">{video.youtubeUrl || "—"}</div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">Project folder</div>
            <div className="mt-1">{video.projectFolder || "—"}</div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-[0.16em] text-[#5A6E82]">Primary keyword</div>
            <div className="mt-1">{video.primaryKeyword || "—"}</div>
          </div>
        </div>
      </div>

      <section className="space-y-4">
        <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl">Short clips</h2>
        {video.clips.map((clip) => {
          const platformsPosted = new Set(clip.posts.map((p) => p.platform));
          const missing = Object.keys(PLATFORMS).filter((p) => !platformsPosted.has(p));
          return (
            <div key={clip.id} className="card-panel p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <div className="text-xs uppercase tracking-[0.16em] text-[#FF7A24]">
                    Clip {clip.clipNumber} · {clip.status} · score {clip.qualityScore ?? "—"}
                  </div>
                  <h3 className="mt-2 text-xl text-[#F5E8D2]">{clip.workingTitle}</h3>
                  <p className="mt-1 text-sm text-[#F5E8D2]/65">{clip.hook}</p>
                  <p className="mt-2 text-xs text-[#5A6E82]">
                    {clip.sourceStartTime} → {clip.sourceEndTime} · {clip.targetDurationSeconds}s ·{" "}
                    {clip.hookCategory}
                  </p>
                </div>
                <ClipActions clipId={clip.id} status={clip.status} />
              </div>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <div className="rounded-xl bg-white/3 p-3 text-sm text-[#F5E8D2]/70">
                  <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Transcript</div>
                  <p className="mt-2">{clip.transcript}</p>
                </div>
                <div className="rounded-xl bg-white/3 p-3 text-sm text-[#F5E8D2]/70">
                  <div className="text-xs uppercase tracking-[0.14em] text-[#5A6E82]">Platform coverage</div>
                  <p className="mt-2">
                    Tracked: {Array.from(platformsPosted).join(", ") || "none"}
                  </p>
                  <p className="mt-1 text-[#FFC85A]/80">
                    Missing: {missing.join(", ") || "none"}
                  </p>
                  <Link
                    href={`/clips/${clip.id}`}
                    className="mt-3 inline-block text-[#FF7A24] hover:underline"
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
