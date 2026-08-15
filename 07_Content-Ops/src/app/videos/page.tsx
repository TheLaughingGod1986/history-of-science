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
        <p className="mt-2 max-w-2xl text-[#F5E8D2]/60">
          Finished long-form films live here. Open one to create a distribution pack — short
          clips and posts for each platform.
        </p>
      </div>

      {videos.length === 0 ? (
        <div className="card-panel space-y-5 p-6 sm:p-8">
          <div>
            <p className="text-xs uppercase tracking-[0.18em] text-[#FF7A24]">Getting started</p>
            <h2 className="mt-2 font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
              No long-form films yet
            </h2>
            <p className="mt-3 max-w-xl text-[#F5E8D2]/65">
              This list stays empty until a finished long-form film is added. After it appears,
              open it and create a distribution pack to propose short clips and platform posts.
            </p>
          </div>
          <ol className="space-y-3 text-sm text-[#F5E8D2]/70">
            <li className="flex gap-3">
              <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[#FF7A24]/20 text-xs text-[#FF7A24]">
                1
              </span>
              <span>Add a finished long-form film to the library.</span>
            </li>
            <li className="flex gap-3">
              <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[#FF7A24]/20 text-xs text-[#FF7A24]">
                2
              </span>
              <span>Open the film and create a distribution pack of short clips.</span>
            </li>
            <li className="flex gap-3">
              <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[#FF7A24]/20 text-xs text-[#FF7A24]">
                3
              </span>
              <span>Track clip and post progress in Pipeline.</span>
            </li>
          </ol>
          <div className="flex flex-wrap gap-3 pt-1">
            <Link
              href="/pipeline"
              className="inline-flex min-h-11 items-center justify-center rounded-full bg-[#FF7A24] px-5 py-2.5 text-sm font-medium text-[#0A0C12]"
            >
              Open Pipeline
            </Link>
            <Link
              href="/"
              className="inline-flex min-h-11 items-center justify-center rounded-full border border-white/10 px-5 py-2.5 text-sm text-[#F5E8D2]"
            >
              Back to Overview
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid gap-4">
          {videos.map((video) => (
            <Link
              key={video.id}
              href={`/videos/${video.id}`}
              className="card-panel block p-4 transition hover:border-[#FF7A24]/40 sm:p-5"
            >
              <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div className="min-w-0">
                  <div className="text-xs uppercase tracking-[0.18em] text-[#FF7A24]">
                    {video.status} · {video.topic}
                  </div>
                  <h2 className="mt-2 break-words font-[family-name:var(--font-orbit-display)] text-xl text-[#F5E8D2]">
                    {video.workingTitle || video.title}
                  </h2>
                  {video.workingTitle ? (
                    <p className="mt-1 break-words text-sm text-[#F5E8D2]/55">{video.title}</p>
                  ) : null}
                </div>
                <div className="flex shrink-0 flex-wrap gap-x-4 gap-y-1 text-sm text-[#F5E8D2]/55 sm:flex-col sm:items-end sm:text-right">
                  <div>
                    {video._count.clips} clip{video._count.clips === 1 ? "" : "s"}
                  </div>
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
      )}
    </div>
  );
}
