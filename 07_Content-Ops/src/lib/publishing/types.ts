export type PublishingPlatform =
  | "youtube_shorts"
  | "tiktok"
  | "instagram_reels"
  | "facebook_reels"
  | "x"
  | "threads";

export type ErrorCategory =
  | "authentication"
  | "permission"
  | "rate_limit"
  | "validation"
  | "media_processing"
  | "network"
  | "temporary_platform"
  | "permanent_platform"
  | "configuration"
  | "unknown";

export type PlatformCapabilities = {
  canConnect: boolean;
  canUploadVideo: boolean;
  canPublishDirectly: boolean;
  canUploadDraft: boolean;
  canScheduleNatively: boolean;
  canSetThumbnail: boolean;
  canSetPrivacy: boolean;
  canReadPublishStatus: boolean;
  canRetrievePostUrl: boolean;
  canDeletePost: boolean;
  requiresAppReview: boolean;
  requiresManualCompletion: boolean;
  limitations: string[];
};

export type ConnectionValidationResult = {
  ok: boolean;
  status: string;
  accountName?: string;
  accountUsername?: string;
  grantedScopes?: string[];
  capabilities: PlatformCapabilities;
  errors: string[];
  warnings: string[];
};

export type PostValidationResult = {
  ok: boolean;
  errors: string[];
  warnings: string[];
};

export type PublishResult = {
  success: boolean;
  published: boolean;
  /** True when the platform accepted a future publishAt (uploaded now, goes live later). */
  scheduledOnPlatform?: boolean;
  /** ISO timestamp the platform will make the video public, when scheduledOnPlatform. */
  scheduledFor?: string;
  platformPostId?: string;
  platformUrl?: string;
  externalUploadId?: string;
  message: string;
  method: "manual" | "api" | "scheduled_export" | "draft_upload" | "dry_run";
  errorCategory?: ErrorCategory;
  retryable?: boolean;
  httpStatus?: number;
  requestId?: string;
  responseSummary?: string;
  requiresManualCompletion?: boolean;
};

export type ExternalPublishStatus = {
  status:
    | "unknown"
    | "uploading"
    | "processing"
    | "published"
    | "scheduled"
    | "failed"
    | "draft"
    | "manual_action_required";
  platformPostId?: string;
  platformUrl?: string;
  detail: string;
};

export type RefreshConnectionResult = {
  ok: boolean;
  message: string;
  expiresAt?: Date;
};

export type RevokeConnectionResult = {
  ok: boolean;
  message: string;
};

export type PlatformConnectionRecord = {
  id: string;
  platform: string;
  accountName?: string | null;
  accountUsername?: string | null;
  accountType?: string | null;
  channelId?: string | null;
  pageId?: string | null;
  instagramBusinessAccountId?: string | null;
  externalUserId?: string | null;
  connectionStatus: string;
  grantedScopes?: string | null;
  accessTokenEncrypted?: string | null;
  refreshTokenEncrypted?: string | null;
  accessTokenExpiresAt?: Date | null;
  refreshTokenExpiresAt?: Date | null;
  metadataJson?: string | null;
};

export type PlatformPostRecord = {
  id: string;
  platform: string;
  title?: string | null;
  caption?: string | null;
  hashtags?: string | null;
  callToAction?: string | null;
  uploadStatus: string;
  privacyStatus?: string | null;
  madeForKids?: boolean | null;
  containsSyntheticMedia?: boolean | null;
  mediaFilePath?: string | null;
  mediaChecksum?: string | null;
  platformPostId?: string | null;
  platformUrl?: string | null;
  approvedForPublish?: boolean | null;
  scheduledAt?: Date | null;
  exportPath?: string | null;
  /** Optional custom thumbnail (jpg/png/gif under 2MB). */
  thumbnailPath?: string | null;
  /** When "longform", skip Shorts-oriented duration warnings. */
  contentFormat?: "shorts" | "longform" | null;
};

export type PublishingContext = {
  dryRun: boolean;
  workerId: string;
  jobId: string;
  attemptNumber: number;
  accessToken: string;
  refreshToken?: string;
};

export interface PublishingAdapter {
  platform: PublishingPlatform | "manual";
  id: string;
  label: string;

  getCapabilities(connection?: PlatformConnectionRecord | null): PlatformCapabilities;

  validateConnection(
    connection: PlatformConnectionRecord,
  ): Promise<ConnectionValidationResult>;

  validatePost(post: PlatformPostRecord): Promise<PostValidationResult>;

  publish(
    post: PlatformPostRecord,
    connection: PlatformConnectionRecord,
    context: PublishingContext,
  ): Promise<PublishResult>;

  getExternalStatus(
    externalPostId: string,
    connection: PlatformConnectionRecord,
  ): Promise<ExternalPublishStatus>;

  refreshConnection?(
    connection: PlatformConnectionRecord,
  ): Promise<RefreshConnectionResult>;

  revokeConnection?(
    connection: PlatformConnectionRecord,
  ): Promise<RevokeConnectionResult>;
}

/** Legacy v1 shape retained for existing settings UI / tests. */
export type LegacyPublishStatus = {
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

export type LegacyAdapterPost = {
  id: string;
  platform: string;
  title?: string | null;
  caption?: string | null;
  exportPath?: string | null;
  uploadStatus: string;
};

export type LegacyPublishResult = {
  success: boolean;
  platformPostId?: string;
  platformUrl?: string;
  message: string;
  method: "manual" | "api" | "scheduled_export" | "third_party";
};
