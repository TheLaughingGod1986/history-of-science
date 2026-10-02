/**
 * One way for every script to get a YouTube access token from the stored Content Ops connection.
 *
 * 2 Oct 2026: the scripts each looked only for a connection marked "connected". One failed refresh
 * (a network blip, or the worker) flipped it to "expired" and every script then stopped with
 * "No connected YouTube account", although the refresh token was often still good. Now any
 * non-disconnected connection with a refresh token is tried, and a good refresh marks it connected
 * again. A dead refresh token (invalid_grant) gets a message that says what to do.
 */
import { prisma } from "../storage/prisma";
import { getEnv } from "../env";
import { decryptSecret, encryptSecret } from "../security/token-crypto";

export const RECONNECT_HELP =
  "Reconnect YouTube on Content Ops → Settings → Connections. If this happens about every 7 days, " +
  "the Google OAuth app is in Testing mode: publish it (Google Cloud Console → APIs & Services → " +
  "OAuth consent screen → Publish app) so refresh tokens stop expiring.";

/** What a failed token refresh means. `invalid_grant` = the refresh token itself is dead. */
export function classifyRefreshFailure(status: number, body: unknown): { dead: boolean; message: string } {
  const err = (body && typeof body === "object" && "error" in body ? String((body as any).error) : "") || "";
  if (err === "invalid_grant") {
    return { dead: true, message: `YouTube refresh token expired or revoked (invalid_grant). ${RECONNECT_HELP}` };
  }
  return { dead: false, message: `YouTube token refresh failed (${status}${err ? `: ${err}` : ""}); try again.` };
}

export async function youtubeAccessToken(): Promise<string> {
  const env = getEnv();
  const candidates = await prisma.platformConnection.findMany({
    where: { platform: "youtube_shorts", disconnectedAt: null },
    orderBy: { updatedAt: "desc" },
  });
  // Prefer a connected row, then any row that can still refresh.
  const conn =
    candidates.find((c) => c.connectionStatus === "connected") ??
    candidates.find((c) => Boolean(c.refreshTokenEncrypted));
  if (!conn) throw new Error(`No YouTube account stored. ${RECONNECT_HELP}`);

  if (!conn.refreshTokenEncrypted || !env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET) {
    if (!conn.accessTokenEncrypted) throw new Error(`No YouTube token. ${RECONNECT_HELP}`);
    return decryptSecret(conn.accessTokenEncrypted);
  }

  const res = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID,
      client_secret: env.GOOGLE_CLIENT_SECRET,
      refresh_token: decryptSecret(conn.refreshTokenEncrypted),
      grant_type: "refresh_token",
    }),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok || !body.access_token) {
    const failure = classifyRefreshFailure(res.status, body);
    if (failure.dead) {
      await prisma.platformConnection.update({
        where: { id: conn.id },
        data: { connectionStatus: "expired", lastConnectionError: failure.message },
      });
    }
    throw new Error(failure.message);
  }
  await prisma.platformConnection.update({
    where: { id: conn.id },
    data: {
      accessTokenEncrypted: encryptSecret(body.access_token),
      accessTokenExpiresAt: new Date(Date.now() + Number(body.expires_in || 3600) * 1000),
      lastRefreshAt: new Date(),
      connectionStatus: "connected",
      lastConnectionError: null,
    },
  });
  return body.access_token as string;
}
