import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";

const db = vi.hoisted(() => ({
  films: vi.fn(),
  heartbeat: vi.fn(),
  connections: vi.fn(),
}));
vi.mock("@/lib/storage/prisma", () => ({
  prisma: {
    longFormVideo: { findMany: db.films },
    workerHeartbeat: { findFirst: db.heartbeat },
    platformConnection: { findMany: db.connections },
  },
}));
vi.mock("@/lib/security/operator-auth", () => ({ isOperatorAuthenticated: async () => false }));
vi.mock("next/headers", () => ({ headers: async () => new Headers({ host: "example.com" }) }));
vi.mock("@/lib/env", () => ({
  isDryRun: () => true,
  hasGoogleOAuth: () => false,
  hasMetaOAuth: () => false,
  hasTikTokOAuth: () => false,
  hasXOAuth: () => false,
  hasThreadsOAuth: () => false,
}));
vi.mock("@/lib/publishing/adapters", () => ({
  getPublishingAdapter: () => ({
    getCapabilities: () => ({ canPublishDirectly: false, canUploadDraft: false, limitations: [] }),
  }),
}));
vi.mock("@/components/ConnectionActions", () => ({ ConnectionActions: () => null }));

import VideosPage from "../src/app/videos/page";
import ConnectionsPage from "../src/app/settings/connections/page";

const now = new Date("2026-11-12T18:00:00Z");
function film(id: string, date: string | null, youtubeVideoId: string | null = null) {
  return {
    id, title: `Film ${id}`, workingTitle: null, slug: id, status: "scheduled",
    summary: null, youtubeUrl: null, youtubeVideoId, thumbnailPath: null,
    finalVideoPath: null, projectFolder: null,
    publicationDate: date ? new Date(date) : null, _count: { clips: 0 },
  };
}

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(now);
  db.connections.mockResolvedValue([]);
});
afterEach(() => { vi.useRealTimers(); vi.clearAllMocks(); });

describe("request-time page state", () => {
  it.each([
    [29_999, "online"], [30_000, "offline"], [30_001, "offline"],
  ])("keeps the heartbeat boundary at %i ms", async (age, status) => {
    db.heartbeat.mockResolvedValue({ lastHeartbeatAt: new Date(now.getTime() - age) });
    const html = renderToStaticMarkup(await ConnectionsPage({ searchParams: Promise.resolve({}) }));
    expect(html).toContain(`Worker: ${status}`);
  });

  it("shows a missing worker as offline", async () => {
    db.heartbeat.mockResolvedValue(null);
    const html = renderToStaticMarkup(await ConnectionsPage({ searchParams: Promise.resolve({}) }));
    expect(html).toContain("Worker: offline");
  });

  it("selects a film at the current time as upcoming and excludes private cuts", async () => {
    db.films.mockResolvedValue([
      film("private", now.toISOString(), "dbBojuwg4r8"),
      film("later", "2026-11-19T18:00:00Z"),
      film("current", now.toISOString()),
    ]);
    const html = renderToStaticMarkup(await VideosPage());
    expect(html).toContain("Next Thursday");
    expect(html.match(/<h2[^>]*>(.*?)<\/h2>/)?.[1]).toBe("Film current");
  });

  it("falls back to the most recent dated film when none is upcoming", async () => {
    db.films.mockResolvedValue([
      film("old", "2026-10-01T18:00:00Z"), film("undated", null),
      film("recent", "2026-11-05T18:00:00Z"),
    ]);
    const html = renderToStaticMarkup(await VideosPage());
    expect(html).not.toContain("Next Thursday</span>");
    expect(html.match(/<h2[^>]*>(.*?)<\/h2>/)?.[1]).toBe("Film recent");
  });
});
