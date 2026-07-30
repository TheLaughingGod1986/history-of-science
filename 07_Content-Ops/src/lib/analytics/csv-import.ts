import Papa from "papaparse";
import { engagementRate } from "@/lib/analytics/insights";

export type CsvMetricRow = {
  platformPostId?: string;
  platformUrl?: string;
  platform?: string;
  views?: number;
  impressions?: number;
  likes?: number;
  comments?: number;
  shares?: number;
  saves?: number;
  averageWatchTime?: number;
  averagePercentageViewed?: number;
  completionRate?: number;
  profileVisits?: number;
  linkClicks?: number;
  subscribersGained?: number;
  followersGained?: number;
};

export type ColumnMapping = Record<keyof CsvMetricRow, string | undefined>;

export const DEFAULT_MAPPINGS: Record<string, Partial<ColumnMapping>> = {
  youtube: {
    platformUrl: "Video URL",
    views: "Views",
    likes: "Likes",
    comments: "Comments",
    shares: "Shares",
    averageWatchTime: "Average view duration",
    averagePercentageViewed: "Average percentage viewed",
    subscribersGained: "Subscribers gained",
  },
  tiktok: {
    platformUrl: "Video link",
    views: "Video views",
    likes: "Likes",
    comments: "Comments",
    shares: "Shares",
    saves: "Favourited",
    averageWatchTime: "Average watch time",
    completionRate: "Completion rate",
    profileVisits: "Profile views",
    followersGained: "Followers",
  },
  instagram: {
    platformUrl: "Permalink",
    views: "Plays",
    likes: "Likes",
    comments: "Comments",
    shares: "Shares",
    saves: "Saves",
    averageWatchTime: "Average watch time",
    completionRate: "Completion rate",
    profileVisits: "Profile visits",
    linkClicks: "Link clicks",
  },
  facebook: {
    platformUrl: "Post URL",
    views: "3-second video views",
    likes: "Reactions",
    comments: "Comments",
    shares: "Shares",
    averageWatchTime: "Average watch time",
  },
};

export type ImportPreview = {
  headers: string[];
  matched: Partial<ColumnMapping>;
  missing: string[];
  sampleRows: Record<string, string>[];
};

export function previewCsv(
  csvText: string,
  mapping: Partial<ColumnMapping>,
): ImportPreview {
  const parsed = Papa.parse<Record<string, string>>(csvText, {
    header: true,
    skipEmptyLines: true,
  });
  const headers = parsed.meta.fields || [];
  const missing: string[] = [];
  for (const [field, col] of Object.entries(mapping)) {
    if (col && !headers.includes(col)) missing.push(`${field} ← ${col}`);
  }
  return {
    headers,
    matched: mapping,
    missing,
    sampleRows: (parsed.data || []).slice(0, 5),
  };
}

export type ImportResult = {
  rows: CsvMetricRow[];
  errors: string[];
  duplicatesSkipped: number;
};

export function parseMetricsCsv(
  csvText: string,
  mapping: Partial<ColumnMapping>,
  options?: { seenKeys?: Set<string> },
): ImportResult {
  const parsed = Papa.parse<Record<string, string>>(csvText, {
    header: true,
    skipEmptyLines: true,
  });
  const errors: string[] = [];
  const rows: CsvMetricRow[] = [];
  const seen = options?.seenKeys ?? new Set<string>();
  let duplicatesSkipped = 0;

  if (parsed.errors?.length) {
    for (const e of parsed.errors.slice(0, 10)) {
      errors.push(`CSV parse: ${e.message} (row ${e.row})`);
    }
  }

  (parsed.data || []).forEach((raw, i) => {
    try {
      const row: CsvMetricRow = {};
      for (const [field, col] of Object.entries(mapping) as [keyof CsvMetricRow, string | undefined][]) {
        if (!col) continue;
        const val = raw[col];
        if (val == null || val === "") continue;
        if (
          [
            "views",
            "impressions",
            "likes",
            "comments",
            "shares",
            "saves",
            "profileVisits",
            "linkClicks",
            "subscribersGained",
            "followersGained",
          ].includes(field)
        ) {
          const n = Number(String(val).replace(/,/g, ""));
          if (Number.isNaN(n)) {
            errors.push(`Row ${i + 2}: invalid number for ${field}`);
            continue;
          }
          // @ts-expect-error dynamic assign
          row[field] = n;
        } else if (
          ["averageWatchTime", "averagePercentageViewed", "completionRate"].includes(field)
        ) {
          const n = Number(String(val).replace(/%/g, ""));
          if (Number.isNaN(n)) {
            errors.push(`Row ${i + 2}: invalid number for ${field}`);
            continue;
          }
          // @ts-expect-error dynamic assign
          row[field] = n;
        } else {
          // @ts-expect-error dynamic assign
          row[field] = String(val);
        }
      }

      const key = `${row.platformPostId || ""}|${row.platformUrl || ""}|${row.views ?? ""}|${row.likes ?? ""}`;
      if (seen.has(key)) {
        duplicatesSkipped += 1;
        return;
      }
      seen.add(key);

      if (!row.platformPostId && !row.platformUrl) {
        errors.push(`Row ${i + 2}: missing platformPostId and platformUrl`);
        return;
      }
      rows.push(row);
    } catch (err) {
      errors.push(`Row ${i + 2}: ${err instanceof Error ? err.message : "unknown error"}`);
    }
  });

  return { rows, errors, duplicatesSkipped };
}

export function withEngagement<T extends CsvMetricRow>(row: T): T & { engagementRate: number | null } {
  return { ...row, engagementRate: engagementRate(row) };
}
