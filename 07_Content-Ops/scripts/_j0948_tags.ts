import { youtubeAccessToken } from "../src/lib/publishing/youtube-token";
import { prisma } from "../src/lib/storage/prisma";

const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const NEW_ID = "BW_CFAX-mxc";
const TAGS = [
  "blood circulation",
  "galen",
  "history of medicine",
  "history of science",
  "is the heart a pump",
  "what did galen believe about the heart",
  "william harvey",
];

async function yt(t: string, url: string, init?: RequestInit) {
  const r = await fetch(url, {
    ...init,
    headers: { Authorization: `Bearer ${t}`, ...(init?.headers || {}) },
  });
  const text = await r.text();
  let json: any;
  try { json = JSON.parse(text); } catch { json = { raw: text.slice(0, 400) }; }
  return { ok: r.ok, status: r.status, json };
}

async function main() {
  const t = await youtubeAccessToken();
  const ch = await yt(t, "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true");
  if (ch.json.items?.[0]?.id !== HOS) throw new Error("not HOS");
  const put = await yt(t, "https://www.googleapis.com/youtube/v3/videos?part=snippet", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id: NEW_ID,
      snippet: {
        title: "Is the Heart a Pump?",
        description: "Galen taught that the heart's job was to heat the blood, not to pump it.\n\nFull film:\nThe Tied Arm That Proved Your Blood Circulates\nhttps://youtu.be/wwcjcFfC-5M\n\n#HistoryOfScience #Harvey #Galen #BloodCirculation #Shorts",
        categoryId: "27",
        defaultLanguage: "en-GB",
        defaultAudioLanguage: "en-GB",
        tags: TAGS,
      },
    }),
  });
  console.log("TAGS", put.status, JSON.stringify({
    tags: put.json?.snippet?.tags || [],
    title: put.json?.snippet?.title || null,
    lang: put.json?.snippet?.defaultLanguage || null,
    error: put.json?.error?.message || null,
  }));
  if (!put.ok) throw new Error("tag update failed");
  const after = await yt(
    t,
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=${NEW_ID}`,
  );
  const it = (after.json.items || [])[0];
  const caps = await yt(t, `https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=${NEW_ID}`);
  console.log("READ", JSON.stringify({
    privacy: it?.status?.privacyStatus,
    publishAt: it?.status?.publishAt || null,
    tags: it?.snippet?.tags || [],
    title: it?.snippet?.title,
    lang: it?.snippet?.defaultLanguage,
    captions: (caps.json.items || []).map((c: any) => ({
      language: c.snippet?.language,
      status: c.snippet?.status,
      trackKind: c.snippet?.trackKind,
      isDraft: c.snippet?.isDraft,
    })),
    captionError: caps.json?.error?.message || null,
  }, null, 2));
}

main()
  .catch((e) => {
    console.error(e instanceof Error ? e.message : e);
    process.exitCode = 1;
  })
  .finally(() => prisma.$disconnect());
