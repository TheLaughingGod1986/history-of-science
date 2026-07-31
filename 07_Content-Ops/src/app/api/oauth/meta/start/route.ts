import { NextResponse } from "next/server";
import { getEnv, hasMetaOAuth } from "@/lib/env";
import { createOAuthState } from "@/lib/oauth/state";

const META_SCOPES = [
  "pages_show_list",
  "pages_read_engagement",
  "pages_manage_posts",
  "instagram_basic",
  "instagram_content_publish",
  "business_management",
].join(",");

export async function GET() {
  if (!hasMetaOAuth()) {
    return NextResponse.json({ error: "META_APP_ID / META_APP_SECRET not configured" }, { status: 400 });
  }
  const env = getEnv();
  const redirectUri = env.META_REDIRECT_URI || `${env.APP_BASE_URL}/api/oauth/meta/callback`;
  const { state } = await createOAuthState({ platform: "meta", redirectPath: "/settings/connections" });
  const url = new URL("https://www.facebook.com/v21.0/dialog/oauth");
  url.searchParams.set("client_id", env.META_APP_ID!);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("state", state);
  url.searchParams.set("scope", META_SCOPES);
  return NextResponse.redirect(url.toString());
}
