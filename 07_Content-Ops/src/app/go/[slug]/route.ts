import { NextRequest, NextResponse } from "next/server";
import { recordAffiliateClickAndResolve } from "@/lib/affiliate/tracking";

export const dynamic = "force-dynamic";

/**
 * Tracked affiliate redirect: /go/{slug}?video=…&utm_*…
 * Records click then 302 to the programme affiliate URL.
 */
export async function GET(
  request: NextRequest,
  context: { params: Promise<{ slug: string }> },
) {
  const { slug } = await context.params;
  const sp = request.nextUrl.searchParams;

  try {
    const result = await recordAffiliateClickAndResolve({
      productSlug: slug,
      videoId: sp.get("video"),
      videoSlug: sp.get("v") || sp.get("utm_campaign"),
      placementId: sp.get("placement"),
      source: sp.get("utm_source") || "youtube",
      medium: sp.get("utm_medium") || "affiliate",
      campaign: sp.get("utm_campaign"),
      content: sp.get("utm_content") || slug,
      userAgent: request.headers.get("user-agent"),
      referrer: request.headers.get("referer"),
    });

    return NextResponse.redirect(result.destinationUrl, 302);
  } catch {
    return NextResponse.json(
      { error: "Affiliate link not found" },
      { status: 404 },
    );
  }
}
