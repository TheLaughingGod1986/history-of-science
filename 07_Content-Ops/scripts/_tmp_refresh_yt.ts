import { prisma } from "../src/lib/storage/prisma";
import { YouTubePublishingAdapter } from "../src/lib/publishing/adapters/youtube";
async function main() {
  const conn = await prisma.platformConnection.findFirst({
    where: { platform: "youtube_shorts", connectionStatus: "connected", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  console.log(JSON.stringify({ id: conn?.id, account: conn?.accountName, status: conn?.connectionStatus, exp: conn?.accessTokenExpiresAt, hasRefresh: !!conn?.refreshTokenEncrypted }, null, 2));
  if (!conn) return;
  const adapter = new YouTubePublishingAdapter();
  if (adapter.refreshConnection) {
    const r = await adapter.refreshConnection(conn);
    console.log("refresh", JSON.stringify(r));
  }
}
main().then(()=>process.exit(0)).catch(e=>{console.error(e); process.exit(1);});
