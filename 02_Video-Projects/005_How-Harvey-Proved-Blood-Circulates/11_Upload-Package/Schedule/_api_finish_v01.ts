/**
 * HOS 005: Data API finish on the uploaded long (HOS connection only).
 *
 *   cd 07_Content-Ops && npx tsx --env-file=.env <this file> scopes
 *   … thumb <videoId> <jpg>        thumbnails.set (main thumbnail)
 *   … captions <videoId> <srt>     captions.insert, English (United Kingdom), published
 *   … list-captions <videoId>
 */
import fs from "fs";
import path from "path";
import { prisma } from "../../../../07_Content-Ops/src/lib/storage/prisma";
import { decryptSecret } from "../../../../07_Content-Ops/src/lib/security/token-crypto";
import { YouTubePublishingAdapter } from "../../../../07_Content-Ops/src/lib/publishing/adapters/youtube";

const HOS_ID = "UCXp7HkBIl1LgaznXuZHJyRg";

async function token(): Promise<string> {
  let conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn?.accessTokenEncrypted) throw new Error("no connected YouTube account");
  if (conn.accessTokenExpiresAt && conn.accessTokenExpiresAt.getTime() < Date.now() + 60_000) {
    const r = await new YouTubePublishingAdapter().refreshConnection!(conn);
    if (!r.ok) throw new Error(`refresh failed: ${r.message}`);
    conn = await prisma.platformConnection.findUnique({ where: { id: conn.id } });
  }
  return decryptSecret(conn!.accessTokenEncrypted!);
}

async function assertHos(t: string, videoId?: string) {
  const ch = await (
    await fetch("https://www.googleapis.com/youtube/v3/channels?part=id&mine=true", {
      headers: { Authorization: `Bearer ${t}` },
    })
  ).json();
  if (ch.items?.length !== 1 || ch.items[0].id !== HOS_ID) throw new Error("connection is not @HistoryOfScienceYT");
  if (videoId) {
    const v = await (
      await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${videoId}`, {
        headers: { Authorization: `Bearer ${t}` },
      })
    ).json();
    if (v.items?.[0]?.snippet?.channelId !== HOS_ID) throw new Error(`${videoId} is not on @HistoryOfScienceYT`);
  }
}

async function main() {
  const [cmd, videoId, file] = process.argv.slice(2);
  const t = await token();
  await assertHos(t, cmd === "scopes" ? undefined : videoId);
  const auth = { Authorization: `Bearer ${t}` };

  if (cmd === "scopes") {
    const info = await (await fetch(`https://oauth2.googleapis.com/tokeninfo?access_token=${t}`)).json();
    console.log(JSON.stringify({ scope: info.scope?.split(" ") }, null, 2));
  } else if (cmd === "thumb") {
    const res = await fetch(
      `https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${videoId}&uploadType=media`,
      { method: "POST", headers: { ...auth, "Content-Type": "image/jpeg" }, body: fs.readFileSync(file) },
    );
    console.log(res.status, JSON.stringify(await res.json(), null, 2));
  } else if (cmd === "captions") {
    const boundary = `hos005${Date.now()}`;
    const meta = JSON.stringify({
      snippet: { videoId, language: "en-GB", name: "", isDraft: false },
    });
    const body = Buffer.concat([
      Buffer.from(`--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${meta}\r\n`),
      Buffer.from(`--${boundary}\r\nContent-Type: application/octet-stream\r\n\r\n`),
      fs.readFileSync(file),
      Buffer.from(`\r\n--${boundary}--\r\n`),
    ]);
    const res = await fetch(
      "https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart&sync=false",
      { method: "POST", headers: { ...auth, "Content-Type": `multipart/related; boundary=${boundary}` }, body },
    );
    console.log(res.status, path.basename(file), JSON.stringify(await res.json(), null, 2));
  } else if (cmd === "list-captions") {
    const res = await fetch(
      `https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=${videoId}`,
      { headers: auth },
    );
    console.log(res.status, JSON.stringify(await res.json(), null, 2));
  } else {
    throw new Error(`unknown command ${cmd}`);
  }
}

main()
  .catch((e) => {
    console.error(e instanceof Error ? e.message : e);
    process.exitCode = 1;
  })
  .finally(() => prisma.$disconnect());
