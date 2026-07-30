-- CreateTable
CREATE TABLE "LongFormVideo" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "workingTitle" TEXT,
    "slug" TEXT NOT NULL,
    "topic" TEXT NOT NULL,
    "category" TEXT,
    "status" TEXT NOT NULL DEFAULT 'idea',
    "script" TEXT,
    "summary" TEXT,
    "youtubeUrl" TEXT,
    "youtubeVideoId" TEXT,
    "thumbnailPath" TEXT,
    "finalVideoPath" TEXT,
    "durationSeconds" INTEGER,
    "publicationDate" DATETIME,
    "primaryKeyword" TEXT,
    "secondaryKeywords" TEXT,
    "targetAudience" TEXT,
    "projectFolder" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "ShortClip" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "longFormVideoId" TEXT NOT NULL,
    "clipNumber" INTEGER NOT NULL,
    "workingTitle" TEXT NOT NULL,
    "hook" TEXT,
    "hookCategory" TEXT,
    "transcript" TEXT,
    "sourceStartTime" TEXT,
    "sourceEndTime" TEXT,
    "targetDurationSeconds" INTEGER,
    "visualDirection" TEXT,
    "onScreenText" TEXT,
    "endingLine" TEXT,
    "callToAction" TEXT,
    "whyItWorks" TEXT,
    "exportPath" TEXT,
    "thumbnailPath" TEXT,
    "fileChecksum" TEXT,
    "status" TEXT NOT NULL DEFAULT 'proposed',
    "qualityScore" INTEGER,
    "qualityBreakdown" TEXT,
    "sortOrder" INTEGER NOT NULL DEFAULT 0,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "ShortClip_longFormVideoId_fkey" FOREIGN KEY ("longFormVideoId") REFERENCES "LongFormVideo" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "PlatformPost" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "shortClipId" TEXT NOT NULL,
    "platform" TEXT NOT NULL,
    "title" TEXT,
    "caption" TEXT,
    "hashtags" TEXT,
    "callToAction" TEXT,
    "scheduledAt" DATETIME,
    "publishedAt" DATETIME,
    "platformPostId" TEXT,
    "platformUrl" TEXT,
    "uploadStatus" TEXT NOT NULL DEFAULT 'draft',
    "publishingMethod" TEXT NOT NULL DEFAULT 'manual',
    "notes" TEXT,
    "pinnedComment" TEXT,
    "coverText" TEXT,
    "storyCaption" TEXT,
    "commentPrompt" TEXT,
    "repostReason" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "PlatformPost_shortClipId_fkey" FOREIGN KEY ("shortClipId") REFERENCES "ShortClip" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "PerformanceMetric" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "platformPostId" TEXT NOT NULL,
    "recordedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "views" INTEGER,
    "impressions" INTEGER,
    "likes" INTEGER,
    "comments" INTEGER,
    "shares" INTEGER,
    "saves" INTEGER,
    "averageWatchTime" REAL,
    "averagePercentageViewed" REAL,
    "completionRate" REAL,
    "profileVisits" INTEGER,
    "linkClicks" INTEGER,
    "subscribersGained" INTEGER,
    "followersGained" INTEGER,
    "engagementRate" REAL,
    "importSource" TEXT,
    "importBatchId" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "PerformanceMetric_platformPostId_fkey" FOREIGN KEY ("platformPostId") REFERENCES "PlatformPost" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "ContentInsight" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "type" TEXT NOT NULL,
    "topic" TEXT,
    "platform" TEXT,
    "finding" TEXT NOT NULL,
    "evidence" TEXT,
    "confidence" REAL,
    "recommendedAction" TEXT,
    "sampleSize" INTEGER,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "PlatformSettings" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "platform" TEXT NOT NULL,
    "enabled" BOOLEAN NOT NULL DEFAULT true,
    "accountDisplayName" TEXT,
    "profileUrl" TEXT,
    "defaultHashtags" TEXT,
    "defaultCallToAction" TEXT,
    "publishingMethod" TEXT NOT NULL DEFAULT 'manual',
    "postingTimesJson" TEXT,
    "connectionStatus" TEXT NOT NULL DEFAULT 'manual_only',
    "tokenStatus" TEXT NOT NULL DEFAULT 'not_configured',
    "lastSuccessfulPublish" DATETIME,
    "defaultVisibility" TEXT NOT NULL DEFAULT 'public',
    "analyticsImportNotes" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "ContentTemplate" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "key" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "platform" TEXT,
    "body" TEXT NOT NULL,
    "updatedAt" DATETIME NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "AnalyticsImport" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "platform" TEXT NOT NULL,
    "filename" TEXT NOT NULL,
    "importedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "rowCount" INTEGER NOT NULL,
    "successCount" INTEGER NOT NULL,
    "errorCount" INTEGER NOT NULL,
    "errorsJson" TEXT,
    "notes" TEXT
);

-- CreateTable
CREATE TABLE "AppSetting" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "key" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "updatedAt" DATETIME NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "LongFormVideo_slug_key" ON "LongFormVideo"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "ShortClip_longFormVideoId_clipNumber_key" ON "ShortClip"("longFormVideoId", "clipNumber");

-- CreateIndex
CREATE INDEX "PlatformPost_platform_uploadStatus_idx" ON "PlatformPost"("platform", "uploadStatus");

-- CreateIndex
CREATE INDEX "PlatformPost_scheduledAt_idx" ON "PlatformPost"("scheduledAt");

-- CreateIndex
CREATE INDEX "PerformanceMetric_platformPostId_recordedAt_idx" ON "PerformanceMetric"("platformPostId", "recordedAt");

-- CreateIndex
CREATE INDEX "PerformanceMetric_importBatchId_idx" ON "PerformanceMetric"("importBatchId");

-- CreateIndex
CREATE UNIQUE INDEX "PlatformSettings_platform_key" ON "PlatformSettings"("platform");

-- CreateIndex
CREATE UNIQUE INDEX "ContentTemplate_key_key" ON "ContentTemplate"("key");

-- CreateIndex
CREATE UNIQUE INDEX "AppSetting_key_key" ON "AppSetting"("key");
