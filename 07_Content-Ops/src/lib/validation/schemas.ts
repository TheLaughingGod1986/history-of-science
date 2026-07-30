import { z } from "zod";
import { ALL_PLATFORM_IDS, PlatformId } from "@/config/platforms";
import { CONTENT_RULES } from "@/config/content-rules";

export const longFormStatusSchema = z.enum([
  "idea",
  "scripting",
  "production",
  "editing",
  "ready",
  "scheduled",
  "published",
  "archived",
]);

export const clipStatusSchema = z.enum([
  "proposed",
  "approved",
  "editing",
  "exported",
  "scheduled",
  "published",
  "rejected",
]);

export const uploadStatusSchema = z.enum([
  "draft",
  "ready",
  "scheduled",
  "published",
  "failed",
  "skipped",
]);

export const platformSchema = z.enum(
  ALL_PLATFORM_IDS as [PlatformId, ...PlatformId[]],
);

export const timestampSchema = z
  .string()
  .regex(/^(\d{1,2}:)?\d{1,2}:\d{2}(\.\d{1,3})?$/, "Invalid timestamp (mm:ss or hh:mm:ss)");

export function parseTimestampToSeconds(ts: string): number {
  const parts = ts.split(":").map(Number);
  if (parts.some((n) => Number.isNaN(n))) {
    throw new Error(`Invalid timestamp: ${ts}`);
  }
  if (parts.length === 2) return parts[0] * 60 + parts[1];
  if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2];
  throw new Error(`Invalid timestamp: ${ts}`);
}

export function validateClipTimestamps(
  start?: string | null,
  end?: string | null,
): { ok: boolean; errors: string[]; durationSeconds?: number } {
  const errors: string[] = [];
  if (!start || !end) {
    errors.push("Start and end timestamps are required");
    return { ok: false, errors };
  }
  try {
    const s = parseTimestampToSeconds(start);
    const e = parseTimestampToSeconds(end);
    if (e <= s) errors.push("End time must be after start time");
    const duration = e - s;
    if (duration < CONTENT_RULES.shortDuration.minSeconds) {
      errors.push(
        `Clip is ${duration}s — shorter than recommended minimum ${CONTENT_RULES.shortDuration.minSeconds}s`,
      );
    }
    if (duration > CONTENT_RULES.shortDuration.maxSeconds) {
      errors.push(
        `Clip is ${duration}s — longer than recommended maximum ${CONTENT_RULES.shortDuration.maxSeconds}s`,
      );
    }
    return { ok: errors.length === 0, errors, durationSeconds: duration };
  } catch (err) {
    errors.push(err instanceof Error ? err.message : "Invalid timestamps");
    return { ok: false, errors };
  }
}

export function validateScriptPresent(script?: string | null): string[] {
  if (!script || !script.trim()) return ["Script is empty — cannot propose clips"];
  if (script.trim().length < 200) return ["Script is too short to propose reliable clips"];
  return [];
}

export type ValidationResult = {
  ok: boolean;
  errors: string[];
  warnings: string[];
};

export function okResult(warnings: string[] = []): ValidationResult {
  return { ok: true, errors: [], warnings };
}

export function failResult(errors: string[], warnings: string[] = []): ValidationResult {
  return { ok: false, errors, warnings };
}
