import { ValidationResult, okResult, failResult } from "@/lib/validation/schemas";

export type PublishResult = {
  success: boolean;
  platformPostId?: string;
  platformUrl?: string;
  message: string;
  method: "manual" | "api" | "scheduled_export" | "third_party";
};

export type PublishStatus = {
  status: "draft" | "ready" | "scheduled" | "published" | "failed" | "skipped" | "unknown";
  detail: string;
  connection:
    | "manual_upload_required"
    | "api_available"
    | "api_unavailable"
    | "authentication_expired"
    | "publish_successful"
    | "publishing_failed";
};

export type AdapterPost = {
  id: string;
  platform: string;
  title?: string | null;
  caption?: string | null;
  exportPath?: string | null;
  uploadStatus: string;
};

export interface PublishingAdapter {
  id: string;
  label: string;
  validate(post: AdapterPost): Promise<ValidationResult>;
  publish(post: AdapterPost): Promise<PublishResult>;
  getStatus(postId: string): Promise<PublishStatus>;
}

function envPresent(...keys: string[]): boolean {
  return keys.every((k) => Boolean(process.env[k] && process.env[k]!.trim()));
}

export class ManualPublishingAdapter implements PublishingAdapter {
  id: string;
  label: string;

  constructor(id: string, label: string) {
    this.id = id;
    this.label = label;
  }

  async validate(post: AdapterPost): Promise<ValidationResult> {
    const errors: string[] = [];
    const warnings: string[] = [];
    if (!post.caption && !post.title) errors.push("Title or caption required");
    if (!post.exportPath) warnings.push("No export path set — upload the clean source file manually");
    warnings.push("Manual upload required — API publishing is not enabled for this adapter");
    return errors.length ? failResult(errors, warnings) : okResult(warnings);
  }

  async publish(post: AdapterPost): Promise<PublishResult> {
    const validation = await this.validate(post);
    if (!validation.ok) {
      return {
        success: false,
        message: validation.errors.join("; "),
        method: "manual",
      };
    }
    return {
      success: false,
      message:
        "Manual upload required. Export the package, upload in the platform UI, then record the published URL in Content Ops.",
      method: "manual",
    };
  }

  async getStatus(): Promise<PublishStatus> {
    return {
      status: "unknown",
      detail: "No live API status — track URLs manually after upload.",
      connection: "manual_upload_required",
    };
  }
}

/** Placeholder YouTube adapter — activates only when credentials exist; still does not fake publish. */
export class YouTubeAdapter extends ManualPublishingAdapter {
  constructor() {
    super("youtube", "YouTube");
  }

  async getStatus(): Promise<PublishStatus> {
    if (envPresent("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET")) {
      return {
        status: "unknown",
        detail: "Credentials detected in env, but automated publish is not wired in v1.",
        connection: "api_available",
      };
    }
    return {
      status: "unknown",
      detail: "YouTube API credentials not configured.",
      connection: "manual_upload_required",
    };
  }
}

export class TikTokAdapter extends ManualPublishingAdapter {
  constructor() {
    super("tiktok", "TikTok");
  }

  async getStatus(): Promise<PublishStatus> {
    if (envPresent("TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET")) {
      return {
        status: "unknown",
        detail: "Credentials present, but TikTok publishing remains manual in v1.",
        connection: "api_unavailable",
      };
    }
    return super.getStatus();
  }
}

export class MetaAdapter extends ManualPublishingAdapter {
  constructor() {
    super("meta", "Meta (Instagram/Facebook)");
  }

  async getStatus(): Promise<PublishStatus> {
    if (envPresent("META_ACCESS_TOKEN")) {
      return {
        status: "unknown",
        detail: "Meta token present in env; unrestricted Reels publishing is not assumed. Manual workflow active.",
        connection: "api_unavailable",
      };
    }
    return super.getStatus();
  }
}

export class XAdapter extends ManualPublishingAdapter {
  constructor() {
    super("x", "X");
  }

  async getStatus(): Promise<PublishStatus> {
    if (envPresent("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")) {
      return {
        status: "unknown",
        detail: "X credentials present; API publish not enabled in v1.",
        connection: "api_available",
      };
    }
    return super.getStatus();
  }
}

export function getAdapterForPlatform(platform: string): PublishingAdapter {
  switch (platform) {
    case "youtube_shorts":
      return new YouTubeAdapter();
    case "tiktok":
      return new TikTokAdapter();
    case "instagram_reels":
    case "facebook_reels":
      return new MetaAdapter();
    case "x":
      return new XAdapter();
    case "threads":
      return new ManualPublishingAdapter("threads", "Threads");
    default:
      return new ManualPublishingAdapter(platform, platform);
  }
}
