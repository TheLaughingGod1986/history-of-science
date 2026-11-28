import type { ApiVideo, Finding } from "./rules";

/** Explicit video ID -> review evidence. Affiliate links never establish sponsorship. */
export type SponsorshipDeclarations = Record<string, string>;
export function readSponsorshipDeclarations(value: unknown): SponsorshipDeclarations {
  if (!value || typeof value !== "object" || Array.isArray(value))
    throw new Error("Sponsorship declarations must map video IDs to evidence");
  for (const [id, evidence] of Object.entries(value))
    if (!/^[A-Za-z0-9_-]{11}$/.test(id) || typeof evidence !== "string" || !evidence.trim())
      throw new Error(`Invalid sponsorship declaration for ${id}`);
  return value as SponsorshipDeclarations;
}
export function auditPaidPlacement(v: ApiVideo, declarations: SponsorshipDeclarations = {}): {
  state: "unexpected-true" | "declared-sponsored" | "false" | "unknown";
  findings: Finding[];
} {
  const flag = v.paidProductPlacementDetails?.hasPaidProductPlacement;
  const evidence = Object.prototype.hasOwnProperty.call(declarations, v.id) ? declarations[v.id] : undefined;
  const finding = (rule: string, message: string): Finding[] => [{ severity: "warn", rule, message: `${v.id}: ${message}` }];
  if (flag === true) return evidence ? {
    state: "declared-sponsored",
    findings: finding("paid-placement.declared-sponsored", `paid placement true; declared sponsorship (${evidence}); confirm in Studio`),
  } : {
    state: "unexpected-true",
    findings: finding("paid-placement.unexpected", "paid placement true without explicit sponsorship declaration; review with Chief, never automatically clear"),
  };
  if (flag === false) return {
    state: "false",
    findings: evidence ? finding("paid-placement.declaration-mismatch", `API false despite declared sponsorship (${evidence}); review in Studio`) : [],
  };
  return {
    state: "unknown",
    findings: finding("paid-placement.unknown", `unavailable/missing paid placement; not evidence of false; confirm in Studio${evidence ? ` (declared sponsorship: ${evidence})` : ""}`),
  };
}
