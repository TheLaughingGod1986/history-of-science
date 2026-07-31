import {
  ConnectionValidationResult,
  ExternalPublishStatus,
  PlatformCapabilities,
  PlatformConnectionRecord,
  PlatformPostRecord,
  PublishingAdapter,
  PublishingContext,
  PublishResult,
  RefreshConnectionResult,
  RevokeConnectionResult,
} from "@/lib/publishing/types";
import { decryptSecret } from "@/lib/security/token-crypto";
import { classifyHttpError, redactSummary } from "@/lib/publishing/errors";
import { probeVideo, validateForPlatform } from "@/lib/publishing/media/ffprobe";
import fs from "fs";
import { getEnv } from "@/lib/env";

const YT_UPLOAD = "https://www.googleapis.com/auth/youtube.upload";
const YT_READONLY = "https://www.googleapis.com/auth/youtube.readonly";

export function youtubeCapabilities(connected: boolean, scopes: string[] = []): PlatformCapabilities {
  const hasUpload = scopes.includes(YT_UPLOAD) || scopes.some((s) => s.includes("youtube.upload"));
  return {
    canConnect: true,
    canUploadVideo: connected && hasUpload,
    canPublishDirectly: connected && hasUpload,
    canUploadDraft: false,
    canScheduleNatively: connected && hasUpload,
    canSetThumbnail: connected && hasUpload,
    canSetPrivacy: true,
    canReadPublishStatus: connected,
    canRetrievePostUrl: true,
    canDeletePost: false,
    requiresAppReview: false,
    requiresManualCompletion: !connected || !hasUpload,
    limitations: [
      ...(connected ? [] : ["Connect Google OAuth before publishing"]),
      "Default test uploads use privacyStatus=private",
      "madeForKids must be set explicitly",
    ],
  };
}

export class YouTubePublishingAdapter implements PublishingAdapter {
  platform = "youtube_shorts" as const;
  id = "youtube";
  label = "YouTube";

  getCapabilities(connection?: PlatformConnectionRecord | null): PlatformCapabilities {
    const scopes = connection?.grantedScopes ? JSON.parse(connection.grantedScopes) : [];
    return youtubeCapabilities(Boolean(connection && connection.connectionStatus === "connected"), scopes);
  }

  async validateConnection(connection: PlatformConnectionRecord): Promise<ConnectionValidationResult> {
    const caps = this.getCapabilities(connection);
    if (!connection.accessTokenEncrypted) {
      return {
        ok: false,
        status: "expired",
        capabilities: caps,
        errors: ["No access token stored. Reconnect YouTube."],
        warnings: [],
      };
    }
    try {
      const token = decryptSecret(connection.accessTokenEncrypted);
      const res = await fetch(
        "https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
        { headers: { Authorization: `Bearer ${token}` } },
      );
      const body = await res.json();
      if (!res.ok) {
        return {
          ok: false,
          status: res.status === 401 ? "expired" : "requires_attention",
          capabilities: caps,
          errors: [redactSummary(body)],
          warnings: [],
        };
      }
      const channel = body.items?.[0];
      return {
        ok: true,
        status: "connected",
        accountName: channel?.snippet?.title,
        accountUsername: channel?.id,
        grantedScopes: connection.grantedScopes ? JSON.parse(connection.grantedScopes) : [],
        capabilities: this.getCapabilities({
          ...connection,
          grantedScopes: JSON.stringify([YT_UPLOAD, YT_READONLY]),
        }),
        errors: [],
        warnings: [],
      };
    } catch (err) {
      return {
        ok: false,
        status: "requires_attention",
        capabilities: caps,
        errors: [err instanceof Error ? err.message : "YouTube validation failed"],
        warnings: [],
      };
    }
  }

  async validatePost(post: PlatformPostRecord) {
    const errors: string[] = [];
    const warnings: string[] = [];
    if (!post.title && !post.caption) errors.push("Title or caption required");
    if (post.privacyStatus == null) errors.push("privacyStatus is required (default tests to private)");
    if (post.madeForKids == null) errors.push("madeForKids must be set explicitly");
    const file = post.mediaFilePath || post.exportPath;
    if (!file) errors.push("mediaFilePath / export video missing");
    else {
      const probe = await probeVideo(resolveVideoFile(file));
      const platformCheck = validateForPlatform("youtube_shorts", probe);
      errors.push(...platformCheck.errors);
      warnings.push(...platformCheck.warnings);
    }
    return { ok: errors.length === 0, errors, warnings };
  }

  async publish(
    post: PlatformPostRecord,
    connection: PlatformConnectionRecord,
    context: PublishingContext,
  ): Promise<PublishResult> {
    if (context.dryRun) {
      const errors: string[] = [];
      if (!post.title && !post.caption) errors.push("Title or caption required");
      if (post.privacyStatus == null) errors.push("privacyStatus is required");
      if (post.madeForKids == null) errors.push("madeForKids must be set explicitly");
      if (errors.length) {
        return {
          success: false,
          published: false,
          message: errors.join("; "),
          method: "dry_run",
          errorCategory: "validation",
          retryable: false,
        };
      }
      return {
        success: true,
        published: false,
        message: "Dry-run complete. YouTube upload request prepared but not sent.",
        method: "dry_run",
        responseSummary: redactSummary({
          title: post.title,
          privacyStatus: post.privacyStatus || "private",
          madeForKids: post.madeForKids,
          connectionId: connection.id,
        }),
      };
    }

    const validation = await this.validatePost(post);
    if (!validation.ok) {
      return {
        success: false,
        published: false,
        message: validation.errors.join("; "),
        method: "api",
        errorCategory: "validation",
        retryable: false,
      };
    }

    const filePath = resolveVideoFile(post.mediaFilePath || post.exportPath!);
    const title = (post.title || post.caption || "Orbit Short").slice(0, 100);
    const description = post.caption || "";
    const privacyStatus = post.privacyStatus || "private";
    const madeForKids = Boolean(post.madeForKids);

    try {
      const metaRes = await fetch(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${context.accessToken}`,
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": String(fs.statSync(filePath).size),
          },
          body: JSON.stringify({
            snippet: {
              title,
              description,
              categoryId: "28",
              tags: safeTags(post.hashtags),
            },
            status: {
              privacyStatus,
              selfDeclaredMadeForKids: madeForKids,
            },
          }),
        },
      );

      if (!metaRes.ok) {
        const text = await metaRes.text();
        const classified = classifyHttpError(metaRes.status, text);
        return {
          success: false,
          published: false,
          message: `YouTube session init failed (${metaRes.status})`,
          method: "api",
          errorCategory: classified.category,
          retryable: classified.retryable,
          httpStatus: metaRes.status,
          responseSummary: redactSummary(text),
        };
      }

      const uploadUrl = metaRes.headers.get("location");
      if (!uploadUrl) {
        return {
          success: false,
          published: false,
          message: "YouTube did not return a resumable upload URL",
          method: "api",
          errorCategory: "temporary_platform",
          retryable: true,
        };
      }

      const fileBuf = fs.readFileSync(filePath);
      const uploadRes = await fetch(uploadUrl, {
        method: "PUT",
        headers: {
          "Content-Type": "video/mp4",
          "Content-Length": String(fileBuf.length),
        },
        body: fileBuf,
      });
      const uploadBody = await uploadRes.json().catch(() => ({}));
      if (!uploadRes.ok || !uploadBody.id) {
        const classified = classifyHttpError(uploadRes.status, JSON.stringify(uploadBody));
        return {
          success: false,
          published: false,
          message: "YouTube upload failed",
          method: "api",
          errorCategory: classified.category,
          retryable: classified.retryable,
          httpStatus: uploadRes.status,
          responseSummary: redactSummary(uploadBody),
        };
      }

      const videoId = uploadBody.id as string;
      return {
        success: true,
        published: true,
        platformPostId: videoId,
        platformUrl: `https://youtu.be/${videoId}`,
        message: `Uploaded to YouTube as ${privacyStatus}`,
        method: "api",
        responseSummary: redactSummary({ id: videoId, privacyStatus }),
      };
    } catch (err) {
      return {
        success: false,
        published: false,
        message: err instanceof Error ? err.message : "YouTube network error",
        method: "api",
        errorCategory: "network",
        retryable: true,
      };
    }
  }

  async getExternalStatus(
    externalPostId: string,
    connection: PlatformConnectionRecord,
  ): Promise<ExternalPublishStatus> {
    if (!connection.accessTokenEncrypted) {
      return { status: "unknown", detail: "No token" };
    }
    try {
      const token = decryptSecret(connection.accessTokenEncrypted);
      const res = await fetch(
        `https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id=${encodeURIComponent(externalPostId)}`,
        { headers: { Authorization: `Bearer ${token}` } },
      );
      const body = await res.json();
      const item = body.items?.[0];
      if (!item) return { status: "failed", detail: "Video not found", platformPostId: externalPostId };
      return {
        status: "published",
        platformPostId: externalPostId,
        platformUrl: `https://youtu.be/${externalPostId}`,
        detail: `privacy=${item.status?.privacyStatus}`,
      };
    } catch (err) {
      return {
        status: "unknown",
        detail: err instanceof Error ? err.message : "status check failed",
        platformPostId: externalPostId,
      };
    }
  }

  async refreshConnection(connection: PlatformConnectionRecord): Promise<RefreshConnectionResult> {
    if (!connection.refreshTokenEncrypted) {
      return { ok: false, message: "No refresh token stored" };
    }
    const env = getEnv();
    if (!env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET) {
      return { ok: false, message: "Google OAuth client not configured" };
    }
    try {
      const refreshToken = decryptSecret(connection.refreshTokenEncrypted);
      const res = await fetch("https://oauth2.googleapis.com/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          client_id: env.GOOGLE_CLIENT_ID,
          client_secret: env.GOOGLE_CLIENT_SECRET,
          refresh_token: refreshToken,
          grant_type: "refresh_token",
        }),
      });
      const body = await res.json();
      if (!res.ok || !body.access_token) {
        return { ok: false, message: redactSummary(body) };
      }
      const { encryptSecret } = await import("@/lib/security/token-crypto");
      const { prisma } = await import("@/lib/storage/prisma");
      const expiresAt = new Date(Date.now() + Number(body.expires_in || 3600) * 1000);
      await prisma.platformConnection.update({
        where: { id: connection.id },
        data: {
          accessTokenEncrypted: encryptSecret(body.access_token),
          accessTokenExpiresAt: expiresAt,
          lastRefreshAt: new Date(),
          connectionStatus: "connected",
          lastConnectionError: null,
        },
      });
      return { ok: true, message: "Token refreshed", expiresAt };
    } catch (err) {
      return { ok: false, message: err instanceof Error ? err.message : "refresh failed" };
    }
  }

  async revokeConnection(connection: PlatformConnectionRecord): Promise<RevokeConnectionResult> {
    try {
      if (connection.accessTokenEncrypted) {
        const token = decryptSecret(connection.accessTokenEncrypted);
        await fetch(`https://oauth2.googleapis.com/revoke?token=${encodeURIComponent(token)}`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });
      }
      return { ok: true, message: "Revoke requested" };
    } catch {
      return { ok: true, message: "Local disconnect will proceed even if revoke call failed" };
    }
  }
}

function safeTags(hashtags?: string | null): string[] {
  if (!hashtags) return [];
  try {
    const parsed = JSON.parse(hashtags);
    if (Array.isArray(parsed)) return parsed.map(String).slice(0, 15);
  } catch {
    /* ignore */
  }
  return [];
}

function resolveVideoFile(fileOrDir: string): string {
  if (fs.existsSync(fileOrDir) && fs.statSync(fileOrDir).isFile()) return fileOrDir;
  // export package directory — look for mp4
  if (fs.existsSync(fileOrDir) && fs.statSync(fileOrDir).isDirectory()) {
    const videoDir = `${fileOrDir}/video`;
    if (fs.existsSync(videoDir)) {
      const mp4 = fs.readdirSync(videoDir).find((f) => f.endsWith(".mp4"));
      if (mp4) return `${videoDir}/${mp4}`;
    }
  }
  return fileOrDir;
}

export const YOUTUBE_SCOPES = [YT_UPLOAD, YT_READONLY];
