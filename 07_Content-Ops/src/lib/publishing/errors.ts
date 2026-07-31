import { ErrorCategory } from "@/lib/publishing/types";

export function classifyHttpError(httpStatus?: number, body?: string): {
  category: ErrorCategory;
  retryable: boolean;
} {
  const text = (body || "").toLowerCase();
  if (httpStatus === 401 || text.includes("invalid_grant") || text.includes("token")) {
    return { category: "authentication", retryable: false };
  }
  if (httpStatus === 403 || text.includes("permission") || text.includes("scope")) {
    return { category: "permission", retryable: false };
  }
  if (httpStatus === 429 || text.includes("rate limit")) {
    return { category: "rate_limit", retryable: true };
  }
  if (httpStatus && httpStatus >= 500) {
    return { category: "temporary_platform", retryable: true };
  }
  if (httpStatus === 400) {
    if (text.includes("processing") || text.includes("media")) {
      return { category: "media_processing", retryable: true };
    }
    return { category: "validation", retryable: false };
  }
  return { category: "unknown", retryable: false };
}

export function backoffMs(attemptNumber: number): number {
  const table = [0, 60_000, 5 * 60_000, 15 * 60_000, 60 * 60_000];
  const base = table[Math.min(attemptNumber, table.length - 1)] ?? 60 * 60_000;
  const jitter = Math.floor(Math.random() * 5_000);
  return base + jitter;
}

export function redactSummary(input: unknown): string {
  const raw = typeof input === "string" ? input : JSON.stringify(input);
  return raw
    .replace(/Bearer\s+[A-Za-z0-9._~+/=-]+/gi, "Bearer [REDACTED]")
    .replace(/"(access_token|refresh_token|client_secret|code)"\s*:\s*"[^"]*"/gi, '"$1":"[REDACTED]"')
    .slice(0, 2000);
}
