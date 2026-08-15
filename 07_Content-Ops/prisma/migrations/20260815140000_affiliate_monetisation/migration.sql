-- Affiliate Monetisation System
-- Additive migration — preserves all existing data

-- CreateTable
CREATE TABLE "AffiliateProgram" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "description" TEXT,
    "website" TEXT,
    "network" TEXT,
    "defaultCommissionType" TEXT NOT NULL DEFAULT 'PERCENTAGE',
    "defaultCommissionValue" REAL,
    "cookieDurationDays" INTEGER,
    "status" TEXT NOT NULL DEFAULT 'ACTIVE',
    "affiliateIdEnvKey" TEXT,
    "categoriesJson" TEXT,
    "disclosureText" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "AffiliateProduct" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "affiliateProgramId" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "slug" TEXT NOT NULL,
    "description" TEXT,
    "destinationUrl" TEXT NOT NULL,
    "affiliateUrl" TEXT NOT NULL,
    "imageUrl" TEXT,
    "category" TEXT NOT NULL,
    "subcategory" TEXT,
    "price" REAL,
    "currency" TEXT NOT NULL DEFAULT 'GBP',
    "estimatedCommission" REAL,
    "commissionType" TEXT,
    "commissionValue" REAL,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "featured" BOOLEAN NOT NULL DEFAULT false,
    "priority" INTEGER NOT NULL DEFAULT 0,
    "evergreen" BOOLEAN NOT NULL DEFAULT false,
    "unsuitableForJson" TEXT,
    "notes" TEXT,
    "urlHealthStatus" TEXT NOT NULL DEFAULT 'UNKNOWN',
    "urlLastCheckedAt" DATETIME,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "AffiliateProduct_affiliateProgramId_fkey" FOREIGN KEY ("affiliateProgramId") REFERENCES "AffiliateProgram" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "AffiliateTag" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "slug" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "AffiliateProductTag" (
    "productId" TEXT NOT NULL,
    "tagId" TEXT NOT NULL,
    CONSTRAINT "AffiliateProductTag_productId_fkey" FOREIGN KEY ("productId") REFERENCES "AffiliateProduct" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "AffiliateProductTag_tagId_fkey" FOREIGN KEY ("tagId") REFERENCES "AffiliateTag" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY ("productId", "tagId")
);

-- CreateTable
CREATE TABLE "AffiliatePlacement" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "videoId" TEXT NOT NULL,
    "affiliateProductId" TEXT NOT NULL,
    "placementType" TEXT NOT NULL,
    "position" INTEGER NOT NULL DEFAULT 0,
    "relevanceScore" REAL,
    "manuallyApproved" BOOLEAN NOT NULL DEFAULT false,
    "generatedAutomatically" BOOLEAN NOT NULL DEFAULT false,
    "status" TEXT NOT NULL DEFAULT 'PENDING',
    "clicks" INTEGER NOT NULL DEFAULT 0,
    "conversions" INTEGER NOT NULL DEFAULT 0,
    "estimatedRevenue" REAL NOT NULL DEFAULT 0,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "AffiliatePlacement_videoId_fkey" FOREIGN KEY ("videoId") REFERENCES "LongFormVideo" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "AffiliatePlacement_affiliateProductId_fkey" FOREIGN KEY ("affiliateProductId") REFERENCES "AffiliateProduct" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "AffiliateClick" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "affiliateProductId" TEXT NOT NULL,
    "videoId" TEXT,
    "placementId" TEXT,
    "source" TEXT,
    "campaign" TEXT,
    "medium" TEXT,
    "content" TEXT,
    "destinationUrl" TEXT NOT NULL,
    "userAgent" TEXT,
    "referrer" TEXT,
    "timestamp" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "AffiliateClick_affiliateProductId_fkey" FOREIGN KEY ("affiliateProductId") REFERENCES "AffiliateProduct" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "AffiliateClick_videoId_fkey" FOREIGN KEY ("videoId") REFERENCES "LongFormVideo" ("id") ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT "AffiliateClick_placementId_fkey" FOREIGN KEY ("placementId") REFERENCES "AffiliatePlacement" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "AffiliateConversion" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "affiliateProgramId" TEXT NOT NULL,
    "affiliateProductId" TEXT,
    "videoId" TEXT,
    "orderReference" TEXT,
    "saleAmount" REAL NOT NULL DEFAULT 0,
    "commissionAmount" REAL NOT NULL DEFAULT 0,
    "currency" TEXT NOT NULL DEFAULT 'GBP',
    "conversionDate" DATETIME NOT NULL,
    "imported" BOOLEAN NOT NULL DEFAULT false,
    "importBatchId" TEXT,
    "source" TEXT,
    "notes" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "AffiliateConversion_affiliateProgramId_fkey" FOREIGN KEY ("affiliateProgramId") REFERENCES "AffiliateProgram" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "AffiliateConversion_affiliateProductId_fkey" FOREIGN KEY ("affiliateProductId") REFERENCES "AffiliateProduct" ("id") ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT "AffiliateConversion_videoId_fkey" FOREIGN KEY ("videoId") REFERENCES "LongFormVideo" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "AffiliateUrlHealthCheck" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "affiliateProductId" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "httpStatus" INTEGER,
    "finalUrl" TEXT,
    "checkedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "notes" TEXT,
    CONSTRAINT "AffiliateUrlHealthCheck_affiliateProductId_fkey" FOREIGN KEY ("affiliateProductId") REFERENCES "AffiliateProduct" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "AffiliateDescriptionTemplate" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "key" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "category" TEXT,
    "body" TEXT NOT NULL,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "AffiliateImportBatch" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "programmeSlug" TEXT,
    "filename" TEXT,
    "source" TEXT NOT NULL,
    "rowCount" INTEGER NOT NULL,
    "successCount" INTEGER NOT NULL,
    "errorCount" INTEGER NOT NULL,
    "skippedCount" INTEGER NOT NULL DEFAULT 0,
    "errorsJson" TEXT,
    "contentHash" TEXT,
    "importedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "notes" TEXT
);

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateProgram_slug_key" ON "AffiliateProgram"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateProduct_slug_key" ON "AffiliateProduct"("slug");

-- CreateIndex
CREATE INDEX "AffiliateProduct_affiliateProgramId_active_idx" ON "AffiliateProduct"("affiliateProgramId", "active");

-- CreateIndex
CREATE INDEX "AffiliateProduct_category_idx" ON "AffiliateProduct"("category");

-- CreateIndex
CREATE INDEX "AffiliateProduct_featured_priority_idx" ON "AffiliateProduct"("featured", "priority");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateTag_slug_key" ON "AffiliateTag"("slug");

-- CreateIndex
CREATE INDEX "AffiliateProductTag_tagId_idx" ON "AffiliateProductTag"("tagId");

-- CreateIndex
CREATE INDEX "AffiliatePlacement_videoId_status_idx" ON "AffiliatePlacement"("videoId", "status");

-- CreateIndex
CREATE INDEX "AffiliatePlacement_affiliateProductId_idx" ON "AffiliatePlacement"("affiliateProductId");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliatePlacement_videoId_affiliateProductId_placementType_key" ON "AffiliatePlacement"("videoId", "affiliateProductId", "placementType");

-- CreateIndex
CREATE INDEX "AffiliateClick_affiliateProductId_timestamp_idx" ON "AffiliateClick"("affiliateProductId", "timestamp");

-- CreateIndex
CREATE INDEX "AffiliateClick_videoId_timestamp_idx" ON "AffiliateClick"("videoId", "timestamp");

-- CreateIndex
CREATE INDEX "AffiliateClick_placementId_idx" ON "AffiliateClick"("placementId");

-- CreateIndex
CREATE INDEX "AffiliateConversion_affiliateProgramId_conversionDate_idx" ON "AffiliateConversion"("affiliateProgramId", "conversionDate");

-- CreateIndex
CREATE INDEX "AffiliateConversion_affiliateProductId_idx" ON "AffiliateConversion"("affiliateProductId");

-- CreateIndex
CREATE INDEX "AffiliateConversion_videoId_idx" ON "AffiliateConversion"("videoId");

-- CreateIndex
CREATE INDEX "AffiliateConversion_importBatchId_idx" ON "AffiliateConversion"("importBatchId");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateConversion_importBatchId_orderReference_key" ON "AffiliateConversion"("importBatchId", "orderReference");

-- CreateIndex
CREATE INDEX "AffiliateUrlHealthCheck_affiliateProductId_checkedAt_idx" ON "AffiliateUrlHealthCheck"("affiliateProductId", "checkedAt");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateDescriptionTemplate_key_key" ON "AffiliateDescriptionTemplate"("key");

-- CreateIndex
CREATE UNIQUE INDEX "AffiliateImportBatch_contentHash_key" ON "AffiliateImportBatch"("contentHash");
