-- AlterTable
ALTER TABLE "PlatformPost" ADD COLUMN "approvedForPublish" BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE "PlatformPost" ADD COLUMN "privacyStatus" TEXT;
ALTER TABLE "PlatformPost" ADD COLUMN "madeForKids" BOOLEAN;
ALTER TABLE "PlatformPost" ADD COLUMN "containsSyntheticMedia" BOOLEAN;
ALTER TABLE "PlatformPost" ADD COLUMN "mediaChecksum" TEXT;
ALTER TABLE "PlatformPost" ADD COLUMN "mediaFilePath" TEXT;

-- CreateTable
CREATE TABLE "PlatformConnection" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "platform" TEXT NOT NULL,
    "accountId" TEXT,
    "accountName" TEXT,
    "accountUsername" TEXT,
    "accountType" TEXT,
    "profileUrl" TEXT,
    "avatarUrl" TEXT,
    "channelId" TEXT,
    "pageId" TEXT,
    "instagramBusinessAccountId" TEXT,
    "externalUserId" TEXT,
    "connectionStatus" TEXT NOT NULL DEFAULT 'pending',
    "grantedScopes" TEXT,
    "capabilitiesJson" TEXT,
    "accessTokenEncrypted" TEXT,
    "refreshTokenEncrypted" TEXT,
    "accessTokenExpiresAt" DATETIME,
    "refreshTokenExpiresAt" DATETIME,
    "lastValidatedAt" DATETIME,
    "lastRefreshAt" DATETIME,
    "lastSuccessfulPublishAt" DATETIME,
    "lastConnectionError" TEXT,
    "metadataJson" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    "disconnectedAt" DATETIME
);

-- CreateTable
CREATE TABLE "PublishingJob" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "platformPostId" TEXT NOT NULL,
    "platformConnectionId" TEXT,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "scheduledAt" DATETIME,
    "startedAt" DATETIME,
    "completedAt" DATETIME,
    "nextAttemptAt" DATETIME,
    "attemptCount" INTEGER NOT NULL DEFAULT 0,
    "maxAttempts" INTEGER NOT NULL DEFAULT 5,
    "lockedAt" DATETIME,
    "lockedBy" TEXT,
    "idempotencyKey" TEXT NOT NULL,
    "lastErrorCode" TEXT,
    "lastErrorMessage" TEXT,
    "lastErrorRetryable" BOOLEAN,
    "externalUploadId" TEXT,
    "externalPostId" TEXT,
    "externalPostUrl" TEXT,
    "requestSummary" TEXT,
    "responseSummary" TEXT,
    "dryRun" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "PublishingJob_platformPostId_fkey" FOREIGN KEY ("platformPostId") REFERENCES "PlatformPost" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "PublishingJob_platformConnectionId_fkey" FOREIGN KEY ("platformConnectionId") REFERENCES "PlatformConnection" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "PublishingAttempt" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "publishingJobId" TEXT NOT NULL,
    "attemptNumber" INTEGER NOT NULL,
    "startedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completedAt" DATETIME,
    "status" TEXT NOT NULL,
    "requestId" TEXT,
    "httpStatus" INTEGER,
    "externalErrorCode" TEXT,
    "errorCategory" TEXT,
    "errorMessage" TEXT,
    "retryable" BOOLEAN NOT NULL DEFAULT false,
    "responseSummary" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "PublishingAttempt_publishingJobId_fkey" FOREIGN KEY ("publishingJobId") REFERENCES "PublishingJob" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "OAuthState" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "platform" TEXT NOT NULL,
    "stateHash" TEXT NOT NULL,
    "codeVerifierEncrypted" TEXT,
    "redirectPath" TEXT,
    "expiresAt" DATETIME NOT NULL,
    "usedAt" DATETIME,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "WorkerHeartbeat" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "workerId" TEXT NOT NULL,
    "lastHeartbeatAt" DATETIME NOT NULL,
    "lastJobId" TEXT,
    "status" TEXT NOT NULL DEFAULT 'online',
    "metadataJson" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateIndex
CREATE INDEX "PlatformConnection_platform_connectionStatus_idx" ON "PlatformConnection"("platform", "connectionStatus");

-- CreateIndex
CREATE UNIQUE INDEX "PlatformConnection_platform_externalUserId_key" ON "PlatformConnection"("platform", "externalUserId");

-- CreateIndex
CREATE UNIQUE INDEX "PublishingJob_idempotencyKey_key" ON "PublishingJob"("idempotencyKey");

-- CreateIndex
CREATE INDEX "PublishingJob_status_nextAttemptAt_idx" ON "PublishingJob"("status", "nextAttemptAt");

-- CreateIndex
CREATE INDEX "PublishingJob_scheduledAt_idx" ON "PublishingJob"("scheduledAt");

-- CreateIndex
CREATE INDEX "PublishingJob_lockedAt_idx" ON "PublishingJob"("lockedAt");

-- CreateIndex
CREATE INDEX "PublishingAttempt_publishingJobId_attemptNumber_idx" ON "PublishingAttempt"("publishingJobId", "attemptNumber");

-- CreateIndex
CREATE UNIQUE INDEX "OAuthState_stateHash_key" ON "OAuthState"("stateHash");

-- CreateIndex
CREATE INDEX "OAuthState_expiresAt_idx" ON "OAuthState"("expiresAt");

-- CreateIndex
CREATE UNIQUE INDEX "WorkerHeartbeat_workerId_key" ON "WorkerHeartbeat"("workerId");
