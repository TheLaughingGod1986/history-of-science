import {
  ConnectionValidationResult,
  ExternalPublishStatus,
  PlatformCapabilities,
  PlatformConnectionRecord,
  PlatformPostRecord,
  PublishingAdapter,
  PublishingContext,
  PublishResult,
} from "@/lib/publishing/types";
import { decryptSecret } from "@/lib/security/token-crypto";
import { classifyHttpError, redactSummary } from "@/lib/publishing/errors";
import { getMediaStagingProvider } from "@/lib/publishing/media/staging";
import { probeVideo, validateForPlatform } from "@/lib/publishing/media/ffprobe";

function baseCaps(extra: Partial<PlatformCapabilities> = {}): PlatformCapabilities {
  return {
    canConnect: true,
    canUploadVideo: false,
    canPublishDirectly: false,
    canUploadDraft: false,
    canScheduleNatively: false,
    canSetThumbnail: false,
    canSetPrivacy: false,
    canReadPublishStatus: true,
    canRetrievePostUrl: true,
    canDeletePost: false,
    requiresAppReview: true,
    requiresManualCompletion: true,
    limitations: [],
    ...extra,
  };
}

export class InstagramPublishingAdapter implements PublishingAdapter {
  platform = "instagram_reels" as const;
  id = "instagram";
  label = "Instagram Reels";

  getCapabilities(connection?: PlatformConnectionRecord | null): PlatformCapabilities {
    const connected =
      connection?.connectionStatus === "connected" &&
      Boolean(connection.instagramBusinessAccountId);
    return baseCaps({
      canUploadVideo: connected,
      canPublishDirectly: connected,
      canSetThumbnail: connected,
      requiresManualCompletion: !connected,
      limitations: [
        "Requires Instagram professional account linked to a Facebook Page",
        "App Review usually required for content publishing permissions",
        "Needs public video URL or Meta resumable upload",
        ...(connected ? [] : ["Select an Instagram professional account after Meta OAuth"]),
      ],
    });
  }

  async validateConnection(connection: PlatformConnectionRecord): Promise<ConnectionValidationResult> {
    const caps = this.getCapabilities(connection);
    if (!connection.accessTokenEncrypted) {
      return { ok: false, status: "expired", capabilities: caps, errors: ["Missing Meta token"], warnings: [] };
    }
    if (!connection.instagramBusinessAccountId) {
      return {
        ok: false,
        status: "requires_attention",
        capabilities: caps,
        errors: [
          "Your Facebook account is connected, but no eligible Instagram professional account is selected.",
        ],
        warnings: [],
      };
    }
    return {
      ok: true,
      status: "connected",
      accountName: connection.accountName || undefined,
      accountUsername: connection.accountUsername || undefined,
      capabilities: this.getCapabilities(connection),
      errors: [],
      warnings: [],
    };
  }

  async validatePost(post: PlatformPostRecord) {
    const errors: string[] = [];
    const warnings: string[] = [];
    if (!post.caption && !post.title) errors.push("Caption required");
    const file = post.mediaFilePath || post.exportPath;
    if (!file) errors.push("Video file missing");
    else {
      const probe = await probeVideo(file);
      const check = validateForPlatform("instagram_reels", probe);
      errors.push(...check.errors);
      warnings.push(...check.warnings);
    }
    return { ok: errors.length === 0, errors, warnings };
  }

  async publish(
    post: PlatformPostRecord,
    connection: PlatformConnectionRecord,
    context: PublishingContext,
  ): Promise<PublishResult> {
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
    if (!connection.instagramBusinessAccountId) {
      return {
        success: false,
        published: false,
        message: "No Instagram professional account selected",
        method: "api",
        errorCategory: "configuration",
        retryable: false,
      };
    }
    if (context.dryRun) {
      return {
        success: true,
        published: false,
        message: "Dry-run: Instagram Reel container/publish not sent",
        method: "dry_run",
      };
    }

    const staging = getMediaStagingProvider();
    const staged = await staging.stageMedia(post.mediaFilePath || post.exportPath!);
    if (!staged.publicUrl && staged.mode === "local_direct_upload") {
      return {
        success: false,
        published: false,
        message:
          "Instagram requires a publicly retrievable video URL or resumable upload. Configure MEDIA_STAGING_MODE=existing_public_url and MEDIA_PUBLIC_BASE_URL, or use resumable Meta upload in a later iteration.",
        method: "api",
        errorCategory: "configuration",
        retryable: false,
        requiresManualCompletion: true,
      };
    }

    const igId = connection.instagramBusinessAccountId;
    const createUrl = new URL(`https://graph.facebook.com/v21.0/${igId}/media`);
    createUrl.searchParams.set("media_type", "REELS");
    createUrl.searchParams.set("caption", post.caption || post.title || "");
    createUrl.searchParams.set("video_url", staged.publicUrl!);
    createUrl.searchParams.set("access_token", context.accessToken);

    const createRes = await fetch(createUrl, { method: "POST" });
    const createBody = await createRes.json();
    if (!createRes.ok || !createBody.id) {
      const c = classifyHttpError(createRes.status, JSON.stringify(createBody));
      return {
        success: false,
        published: false,
        message: "Instagram container creation failed",
        method: "api",
        errorCategory: c.category,
        retryable: c.retryable,
        httpStatus: createRes.status,
        responseSummary: redactSummary(createBody),
      };
    }

    const containerId = createBody.id as string;
    const ready = await pollIgContainer(containerId, context.accessToken);
    if (!ready.ok) {
      return {
        success: false,
        published: false,
        message: ready.message,
        method: "api",
        errorCategory: "media_processing",
        retryable: true,
        externalUploadId: containerId,
      };
    }

    const publishUrl = new URL(`https://graph.facebook.com/v21.0/${igId}/media_publish`);
    publishUrl.searchParams.set("creation_id", containerId);
    publishUrl.searchParams.set("access_token", context.accessToken);
    const pubRes = await fetch(publishUrl, { method: "POST" });
    const pubBody = await pubRes.json();
    if (!pubRes.ok || !pubBody.id) {
      const c = classifyHttpError(pubRes.status, JSON.stringify(pubBody));
      return {
        success: false,
        published: false,
        message: "Instagram publish failed",
        method: "api",
        errorCategory: c.category,
        retryable: c.retryable,
        httpStatus: pubRes.status,
        responseSummary: redactSummary(pubBody),
        externalUploadId: containerId,
      };
    }

    const mediaId = String(pubBody.id);
    let permalink: string | undefined;
    try {
      const per = await fetch(
        `https://graph.facebook.com/v21.0/${mediaId}?fields=permalink&access_token=${encodeURIComponent(context.accessToken)}`,
      );
      const perBody = await per.json();
      permalink = perBody.permalink;
    } catch {
      /* optional */
    }

    return {
      success: true,
      published: true,
      platformPostId: mediaId,
      platformUrl: permalink,
      externalUploadId: containerId,
      message: "Instagram Reel published",
      method: "api",
      responseSummary: redactSummary({ id: mediaId }),
    };
  }

  async getExternalStatus(
    externalPostId: string,
    connection: PlatformConnectionRecord,
  ): Promise<ExternalPublishStatus> {
    if (!connection.accessTokenEncrypted) return { status: "unknown", detail: "No token" };
    const token = decryptSecret(connection.accessTokenEncrypted);
    const res = await fetch(
      `https://graph.facebook.com/v21.0/${externalPostId}?fields=id,permalink&access_token=${encodeURIComponent(token)}`,
    );
    const body = await res.json();
    if (!res.ok) return { status: "failed", detail: redactSummary(body), platformPostId: externalPostId };
    return {
      status: "published",
      platformPostId: externalPostId,
      platformUrl: body.permalink,
      detail: "Found",
    };
  }
}

export class FacebookPublishingAdapter implements PublishingAdapter {
  platform = "facebook_reels" as const;
  id = "facebook";
  label = "Facebook Reels";

  getCapabilities(connection?: PlatformConnectionRecord | null): PlatformCapabilities {
    const connected = connection?.connectionStatus === "connected" && Boolean(connection.pageId);
    return baseCaps({
      canUploadVideo: connected,
      canPublishDirectly: connected,
      requiresManualCompletion: !connected,
      limitations: [
        "Publishes to a Facebook Page only",
        ...(connected ? [] : ["Select a manageable Facebook Page after Meta OAuth"]),
      ],
    });
  }

  async validateConnection(connection: PlatformConnectionRecord): Promise<ConnectionValidationResult> {
    const caps = this.getCapabilities(connection);
    if (!connection.pageId) {
      return {
        ok: false,
        status: "requires_attention",
        capabilities: caps,
        errors: ["Your Facebook account is connected, but no manageable Page was found/selected."],
        warnings: [],
      };
    }
    return {
      ok: true,
      status: "connected",
      accountName: connection.accountName || undefined,
      capabilities: caps,
      errors: [],
      warnings: [],
    };
  }

  async validatePost(post: PlatformPostRecord) {
    const errors: string[] = [];
    const warnings: string[] = [];
    if (!post.caption && !post.title) errors.push("Description/caption required");
    const file = post.mediaFilePath || post.exportPath;
    if (!file) errors.push("Video file missing");
    else {
      const probe = await probeVideo(file);
      const check = validateForPlatform("facebook_reels", probe);
      errors.push(...check.errors);
      warnings.push(...check.warnings);
    }
    return { ok: errors.length === 0, errors, warnings };
  }

  async publish(
    post: PlatformPostRecord,
    connection: PlatformConnectionRecord,
    context: PublishingContext,
  ): Promise<PublishResult> {
    if (!connection.pageId) {
      return {
        success: false,
        published: false,
        message: "No Facebook Page selected",
        method: "api",
        errorCategory: "configuration",
        retryable: false,
      };
    }
    if (context.dryRun) {
      return {
        success: true,
        published: false,
        message: "Dry-run: Facebook Reel not sent",
        method: "dry_run",
      };
    }

    const staging = getMediaStagingProvider();
    const staged = await staging.stageMedia(post.mediaFilePath || post.exportPath!);
    if (!staged.publicUrl) {
      return {
        success: false,
        published: false,
        message:
          "Facebook Reel publishing from this local setup requires a publicly retrievable media URL. Configure MEDIA_PUBLIC_BASE_URL or use the manual upload package.",
        method: "api",
        errorCategory: "configuration",
        retryable: false,
        requiresManualCompletion: true,
      };
    }

    // Page video upload via graph — simplified officially-supported path using file_url where available
    const url = new URL(`https://graph.facebook.com/v21.0/${connection.pageId}/videos`);
    url.searchParams.set("file_url", staged.publicUrl);
    url.searchParams.set("description", post.caption || post.title || "");
    url.searchParams.set("published", "true");
    url.searchParams.set("access_token", context.accessToken);
    const res = await fetch(url, { method: "POST" });
    const body = await res.json();
    if (!res.ok || !body.id) {
      const c = classifyHttpError(res.status, JSON.stringify(body));
      return {
        success: false,
        published: false,
        message: "Facebook video publish failed",
        method: "api",
        errorCategory: c.category,
        retryable: c.retryable,
        httpStatus: res.status,
        responseSummary: redactSummary(body),
        requiresManualCompletion: true,
      };
    }
    const id = String(body.id);
    return {
      success: true,
      published: true,
      platformPostId: id,
      platformUrl: `https://www.facebook.com/reel/${id}`,
      message: "Facebook video/Reel publish recorded",
      method: "api",
      responseSummary: redactSummary({ id }),
    };
  }

  async getExternalStatus(externalPostId: string): Promise<ExternalPublishStatus> {
    return {
      status: "published",
      platformPostId: externalPostId,
      platformUrl: `https://www.facebook.com/reel/${externalPostId}`,
      detail: "Assumed published when ID known; reconcile if needed",
    };
  }
}

async function pollIgContainer(
  containerId: string,
  token: string,
  maxAttempts = 30,
): Promise<{ ok: boolean; message: string }> {
  for (let i = 0; i < maxAttempts; i++) {
    const res = await fetch(
      `https://graph.facebook.com/v21.0/${containerId}?fields=status_code&access_token=${encodeURIComponent(token)}`,
    );
    const body = await res.json();
    const code = body.status_code;
    if (code === "FINISHED") return { ok: true, message: "ready" };
    if (code === "ERROR") return { ok: false, message: redactSummary(body) };
    await new Promise((r) => setTimeout(r, 2000));
  }
  return { ok: false, message: "Instagram container processing timed out" };
}
