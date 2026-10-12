import { prisma } from "../src/lib/storage/prisma";
import { getEnv } from "../src/lib/env";
import { decryptSecret } from "../src/lib/security/token-crypto";
import fs from "fs";

async function token(): Promise<string> {
  const env = getEnv();
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  if (!conn?.refreshTokenEncrypted) throw new Error("no HOS connection");
  const tr = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID || "",
      client_secret: env.GOOGLE_CLIENT_SECRET || "",
      refresh_token: decryptSecret(conn.refreshTokenEncrypted),
      grant_type: "refresh_token",
    }),
  });
  const j = await tr.json();
  if (!j.access_token) throw new Error("token fail " + JSON.stringify(j));
  return j.access_token as string;
}

async function yt(access: string, path: string, init?: RequestInit) {
  const r = await fetch(`https://www.googleapis.com/youtube/v3/${path}`, {
    ...init,
    headers: { Authorization: `Bearer ${access}`, ...(init?.headers || {}) },
  });
  const text = await r.text();
  let json: any;
  try { json = JSON.parse(text); } catch { json = { raw: text }; }
  return { ok: r.ok, status: r.status, json };
}

async function main() {
  const access = await token();
  const ids = ["mTY67qet7cM", "KIWJRl0dzjw"];
  const list = await yt(access, `videos?part=snippet,status,contentDetails,fileDetails&id=${ids.join(",")}`);
  for (const it of list.json.items || []) {
    console.log("BEFORE", JSON.stringify({
      id: it.id,
      title: it.snippet?.title,
      privacy: it.status?.privacyStatus,
      publishAt: it.status?.publishAt || null,
      madeForKids: it.status?.selfDeclaredMadeForKids,
      duration: it.contentDetails?.duration,
      fileName: it.fileDetails?.fileName,
      fileSize: it.fileDetails?.fileSize,
      publishedAt: it.snippet?.publishedAt,
    }));
  }

  const dup = (list.json.items || []).find((i: any) => i.id === "KIWJRl0dzjw");
  if (dup && !/\(duplicate\)/i.test(dup.snippet?.title || "")) {
    const newTitle = `${dup.snippet.title} (duplicate)`;
    const upd = await yt(access, "videos?part=snippet", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: "KIWJRl0dzjw",
        snippet: {
          title: newTitle,
          categoryId: dup.snippet.categoryId,
          description: dup.snippet.description || "",
          tags: dup.snippet.tags,
          defaultLanguage: dup.snippet.defaultLanguage,
          defaultAudioLanguage: dup.snippet.defaultAudioLanguage,
        },
      }),
    });
    console.log("RETITLE", upd.status, upd.json?.error ? JSON.stringify(upd.json.error) : "ok", "->", newTitle);
  } else {
    console.log("RETITLE skip", dup?.snippet?.title);
  }

  const after = await yt(access, `videos?part=snippet,status&id=${ids.join(",")}`);
  for (const it of after.json.items || []) {
    console.log("AFTER", it.id, it.status?.privacyStatus, it.status?.publishAt, "kids="+it.status?.selfDeclaredMadeForKids, it.snippet?.title);
  }
  fs.writeFileSync("/tmp/hos_shortb_verify_dup_out.json", JSON.stringify({ at: new Date().toISOString(), after: after.json }, null, 2));
  await prisma.$disconnect();
}
main().catch(async (e) => { console.error(e); await prisma.$disconnect(); process.exit(1); });
