# Analytics import

## Sample templates

```
07_Content-Ops/content/samples/csv/
  youtube_analytics_sample.csv
  tiktok_analytics_sample.csv
  instagram_insights_sample.csv
  facebook_insights_sample.csv
```

## Flow

1. Export analytics from the platform UI
2. Paste into Content Ops → Analytics
3. Preview column mapping
4. Import valid rows
5. Duplicate metric keys are skipped
6. Import batch metadata is stored on `AnalyticsImport`

## Mapping layer

Defaults live in `src/lib/analytics/csv-import.ts` (`DEFAULT_MAPPINGS`).

Missing fields are listed in the preview. Blank numeric cells are allowed — metrics stay `null`.

## Matching posts

Rows match existing `PlatformPost` records by `platformUrl` or `platformPostId`.  
If neither matches, the row errors clearly so you can paste the published URL onto the post first.
