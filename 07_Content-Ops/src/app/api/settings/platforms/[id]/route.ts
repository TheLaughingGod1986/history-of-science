import { NextResponse } from "next/server";
import { prisma } from "@/lib/storage/prisma";

export async function PATCH(
  req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id } = await ctx.params;
  const body = await req.json();
  const updated = await prisma.platformSettings.update({
    where: { id },
    data: {
      enabled: body.enabled ?? undefined,
      accountDisplayName: body.accountDisplayName ?? undefined,
      profileUrl: body.profileUrl ?? undefined,
      defaultCallToAction: body.defaultCallToAction ?? undefined,
      defaultHashtags: body.defaultHashtags ?? undefined,
      publishingMethod: body.publishingMethod ?? undefined,
      defaultVisibility: body.defaultVisibility ?? undefined,
    },
  });
  return NextResponse.json(updated);
}
