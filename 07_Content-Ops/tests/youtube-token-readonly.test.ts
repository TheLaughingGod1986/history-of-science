import { beforeEach, describe, expect, it, vi } from "vitest";
const mocks = vi.hoisted(() => ({ findMany: vi.fn(), update: vi.fn(), fetch: vi.fn() }));
vi.mock("../src/lib/storage/prisma", () => ({ prisma: { platformConnection: mocks } }));
vi.mock("../src/lib/env", () => ({ getEnv: () => ({ GOOGLE_CLIENT_ID: "fixture", GOOGLE_CLIENT_SECRET: "fixture" }) }));
vi.mock("../src/lib/security/token-crypto", () => ({ decryptSecret: () => "fixture", encryptSecret: () => "encrypted-fixture" }));
import { youtubeAccessToken } from "../src/lib/publishing/youtube-token";
beforeEach(() => {
  vi.clearAllMocks();
  vi.stubGlobal("fetch", mocks.fetch);
  mocks.findMany.mockResolvedValue([{ id: "fixture", connectionStatus: "connected", refreshTokenEncrypted: "fixture" }]);
});
describe("read-only YouTube authentication", () => {
  it("refreshes in memory without saving credentials", async () => {
    mocks.fetch.mockResolvedValue({ ok: true, json: async () => ({ access_token: "refreshed", expires_in: 3600 }) });
    expect(await youtubeAccessToken({ readOnly: true })).toBe("refreshed");
    expect(mocks.update).not.toHaveBeenCalled();
  });
  it("does not mark a dead token expired in read-only mode", async () => {
    mocks.fetch.mockResolvedValue({ ok: false, status: 400, json: async () => ({ error: "invalid_grant" }) });
    await expect(youtubeAccessToken({ readOnly: true })).rejects.toThrow("invalid_grant");
    expect(mocks.update).not.toHaveBeenCalled();
  });
  it("preserves credential persistence for ordinary publishing callers", async () => {
    mocks.fetch.mockResolvedValue({ ok: true, json: async () => ({ access_token: "refreshed", expires_in: 3600 }) });
    await youtubeAccessToken();
    expect(mocks.update).toHaveBeenCalledOnce();
  });
});
