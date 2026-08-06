-- AlterTable
ALTER TABLE "PerformanceMetric" ADD COLUMN "clickThroughRate" REAL;
ALTER TABLE "PerformanceMetric" ADD COLUMN "retention30s" REAL;
ALTER TABLE "PerformanceMetric" ADD COLUMN "retentionDropAtSeconds" REAL;
ALTER TABLE "PerformanceMetric" ADD COLUMN "retentionDropDepth" REAL;
ALTER TABLE "PerformanceMetric" ADD COLUMN "returningViewers" INTEGER;
ALTER TABLE "PerformanceMetric" ADD COLUMN "newViewers" INTEGER;
ALTER TABLE "PerformanceMetric" ADD COLUMN "browsePercent" REAL;
ALTER TABLE "PerformanceMetric" ADD COLUMN "suggestedPercent" REAL;
ALTER TABLE "PerformanceMetric" ADD COLUMN "searchPercent" REAL;
ALTER TABLE "PerformanceMetric" ADD COLUMN "endScreenCtr" REAL;
ALTER TABLE "PerformanceMetric" ADD COLUMN "cardsCtr" REAL;
ALTER TABLE "PerformanceMetric" ADD COLUMN "averageSessionSeconds" REAL;
