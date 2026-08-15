import Link from "next/link";
import { formatInTimeZone } from "date-fns-tz";
import { prisma } from "@/lib/storage/prisma";
import { PUBLISHING_SCHEDULE } from "@/config/publishing-schedule";
import { AddThursdayFilmButton } from "@/components/AddThursdayFilmButton";

export const dynamic = "force-dynamic";

/** Map existing LongFormVideo fields to Video Creator language — no new model. */
function creatorFilmStatus(video: {
  status: string;
  youtubeUrl: string | null;
  youtubeVideoId: string | null;
  finalVideoPath: string | null;
}): string {
  if (video.status === "scheduled" || video.status === "published") return "scheduled";
  if (video.youtubeUrl || video.youtubeVideoId) return "listed";
  if (video.status === "ready" || video.status === "editing" || video.finalVideoPath) {
    return "cut";
  }
  return video.status;
}

function formatThursdayDate(date: Date): string {
  return formatInTimeZone(date, PUBLISHING_SCHEDULE.timezone, "EEE d MMM HH:mm");
}

export default async function VideosPage() {
  const videos = await prisma.longFormVideo.findMany({
    orderBy: { publicationDate: "desc" },
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="font-[family-name:var(--font-orbit-display)] text-3xl text-[#F5E8D2]">
            Thursday films
          </h1>
          <p className="mt-2 max-w-xl text-[#F5E8D2]/60">
            Next Thursday film, whether the cut is ready, the listing is written, and it is
            scheduled.
          </p>
        </div>
        {videos.length > 0 ? <AddThursdayFilmButton primary={false} /> : null}
      </div>

      {videos.length === 0 ? (
        <div className="card-panel space-y-5 p-6 sm:p-8">
          <div>
            <h2 className="font-[family-name:var(--font-orbit-display)] text-2xl text-[#F5E8D2]">
              No Thursday film here yet.
            </h2>
            <p className="mt-3 max-w-xl text-[#F5E8D2]/65">
              When the cut is ready to list, add it here. Then we make the Short and the YouTube
              listing.
            </p>
          </div>
          <AddThursdayFilmButton />
        </div>
      ) : (
        <ul className="divide-y divide-white/5 overflow-hidden rounded-2xl border border-white/8">
          {videos.map((video) => {
            const status = creatorFilmStatus(video);
            const title = video.workingTitle || video.title;
            return (
              <li key={video.id}>
                <Link
                  href={`/videos/${video.id}`}
                  className="flex min-h-14 items-center gap-3 px-4 py-3.5 transition hover:bg-white/5 sm:gap-4 sm:px-5"
                >
                  <div className="min-w-0 flex-1">
                    <div className="truncate text-base text-[#F5E8D2]">{title}</div>
                    <div className="mt-0.5 text-sm text-[#F5E8D2]/55 sm:hidden">
                      {video.publicationDate
                        ? formatThursdayDate(video.publicationDate)
                        : "No Thursday date"}
                      <span className="mx-1.5 text-[#5A6E82]">·</span>
                      <span className="text-[#FF7A24]">{status}</span>
                    </div>
                  </div>
                  <div className="hidden shrink-0 text-sm text-[#F5E8D2]/55 sm:block">
                    {video.publicationDate
                      ? formatThursdayDate(video.publicationDate)
                      : "No Thursday date"}
                  </div>
                  <div className="hidden shrink-0 text-xs uppercase tracking-[0.14em] text-[#FF7A24] sm:block">
                    {status}
                  </div>
                </Link>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
