import Link from "next/link";
import { prisma } from "@/lib/storage/prisma";
import { formatLondon } from "@/lib/publishing/schedule";

export const dynamic = "force-dynamic";

export default async function VideosPage() {
  const videos = await prisma.longFormVideo.findMany({
    orderBy: { publicationDate: "desc" },
    include: { _count: { select: { clips: true } } },
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-[family-name:var(--font-orbit-display)] text-3xl text-[#F5E8D2]">
          Long-form library
        </h1>
        <p className="mt-2 text-[#F5E8D2]/60">
          Register completed pillars, then create a distribution pack.
        </p>
      </div>

      <div className="grid gap-4">
        {videos.map((video) => (
          <Link
            key={video.id}
            href={`/videos/${video.id}`}
            className="card-panel block p-5 transition hover:border-[#FF7A24]/40"
          >
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <div className="text-xs uppercase tracking-[0.18em] text-[#FF7A24]">
                  {video.status} · {video.topic}
                </div>
                <h2 className="mt-2 font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
                  {video.workingTitle || video.title}
                </h2>
                <p className="mt-1 text-sm text-[#F5E8D2]/55">{video.title}</p>
              </div>
              <div className="text-right text-sm text-[#F5E8D2]/55">
                <div>{video._count.clips} clips</div>
                <div>
                  {video.publicationDate
                    ? formatLondon(video.publicationDate)
                    : "Unscheduled"}
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
