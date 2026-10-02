import { describe, expect, it } from "vitest";
import { classifyRefreshFailure, RECONNECT_HELP } from "../src/lib/publishing/youtube-token";

describe("YouTube token refresh failures", () => {
  it("treats invalid_grant as a dead refresh token and says how to fix it", () => {
    const r = classifyRefreshFailure(400, { error: "invalid_grant", error_description: "Token has been expired or revoked." });
    expect(r.dead).toBe(true);
    expect(r.message).toContain("invalid_grant");
    expect(r.message).toContain(RECONNECT_HELP);
    expect(r.message).toContain("Testing mode");
  });

  it("treats other failures as retryable, not dead", () => {
    expect(classifyRefreshFailure(503, { error: "backendError" }).dead).toBe(false);
    expect(classifyRefreshFailure(500, null).dead).toBe(false);
  });
});
