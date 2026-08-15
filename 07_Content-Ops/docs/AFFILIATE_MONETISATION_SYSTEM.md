# Affiliate Monetisation System

Long-term monetisation platform for **Orbit With Ben**, integrated into Content Ops (`07_Content-Ops/`). Relevance before revenue — never recommend a product solely because it pays commission.

## Philosophy

Every recommendation must pass: *Would we still recommend this if there were no commission?*  
Editorial / scientific interest is primary. Max **4** affiliate links per video. No spam.

## Architecture

```
src/lib/affiliate/
  types.ts              Shared constants & DTOs
  schemas.ts            Zod validation
  matching.ts           Deterministic relevance + interchangeable strategy
  description.ts        Pure YouTube affiliate block builder
  description-service.ts DB-backed templates + video placement merge
  urls.ts               Redirect base, UTM, programme tag injection
  tracking.ts           Click recording + destination resolve
  placements.ts         Video ↔ product placements / regenerate
  products.ts / programs.ts
  revenue.ts            Commission, EPC, affiliate RPM, Total Content RPM prep
  opportunity.ts        Affiliate Opportunity Score 0–100
  csv-import.ts         Amazon/Brilliant/generic report parsing
  conversions.ts        Preview + commit import (dedupe by content hash)
  health.ts             Throttled URL health-check abstraction
  analytics.ts          Dashboard, opportunities, video panel
  gear.ts               Phase 5 gear catalogue JSON shape
  social-copy-rules.ts  Hard constraints for affiliate-aware social copy
  social-copy.ts        Sanitize + one soft mention on platform captions
  social-context.ts     Resolve placement context for Shorts generation
  editorial-trust-gate.ts  Video Auditor trust gate (approve + description)
```

UI lives under `/affiliate/*` and on each long-form video detail page. Redirects: `/go/[slug]`.

## Editorial trust gate (Video Auditor)

Matching may still surface **up to 4 candidates** on the video Affiliate Monetisation card so an editor can see options. **Auto-insert, description generation, and APPROVED placements** must pass this gate. Relevance and trust beat the old “max 4 links in the description” default.

**Hard rule:** would we still name this product if there were no commission? If no, it does not go in.

### Placement checklist (before a link hits a description)

1. Named on screen or in the VO of **this** video — not “related,” not “viewers also bought.”
2. A curious viewer is better off after using it (see the sky, read the paper, understand the picture).
3. **One** primary affiliate link per long-form film. A second only if it is a free/cheap companion (e.g. paper + book). Never a stack. Hard cap: **2**.
4. Disclosure once, **first line** of the description, plain:  
   `Some links are affiliate. We only add ones we’d recommend with no commission.`  
   Do not duplicate if already present.
5. Tone stays documentary. “If you want to look at this yourself” is fine. “Buy now / limited / 50% off” is not.
6. Must not compete with the real CTA (film title + subscribe). Affiliate sits **below** that.

### Video types

| Type | Affiliate policy |
|------|------------------|
| All Shorts / companion Shorts | **Zero** links |
| Wonder films (picture is the point) | Zero unless a specific book/paper is named on screen |
| Explainer (JWST, Fermi, black hole) | At most one book, paper, or sky app that was used or named |
| How-to / “look tonight” | One relevant tool max, only if shown |

### Reject spam patterns

More than 1 link on a Short (should be 0) or more than 2 on a film · product never in the video (VPN, hosting, protein) · high-commission junk (crypto, supplements, mystery boxes, generic space merch) · same link on every video · stacked disclosures · salesy VO/end card · link that outranks the film title.

### Code

```ts
import {
  evaluateEditorialTrustGate,
  filterDescriptionLinksThroughTrustGate,
} from "@/lib/affiliate/editorial-trust-gate";

// Approve / auto-insert
evaluateEditorialTrustGate(video, product); // must .pass

// Description generation
filterDescriptionLinksThroughTrustGate({ video, candidates });
```

`setPlacementStatus(..., "APPROVED")` and description builders call this gate. Card candidates may remain `PENDING` when they fail.

## Social copy house rules (hard constraints)

Affiliate must not turn Orbit into a spam channel. These rules apply wherever Content Ops **generates or stores** social copy next to affiliate placements (`generatePlatformCopy`, clip platform-copy / distribution-pack / export). This is **not** a new social product — only guardrails.

### Every platform

- Max **one** soft mention per post. If the video is not actually about the thing, say nothing.
- Never stack brands. Never open on a product. Never “links in bio” as the hook.
- No raw affiliate / merchant URLs, no “use my code”, no percent-off, no haul energy.
- Point to the **YouTube description** or an Orbit **`/go/`** link only. That is the only place a tracked URL lives on social.
- Disclose once, quietly, where the platform requires it. Do not make the disclosure the joke.
- Sky / science first. The tool is an afterthought.

### Platform notes

| Platform | Rule |
|----------|------|
| YouTube Shorts / TikTok | Mention only in the last 1–2s **or** caption tail; no spoken list of links; no URL on screen; no TikTok Shop |
| Instagram Reels | Keep the mention out of the reel; one caption line (or a reply if asked); sticker/bio → YouTube or `/go/`, never a merchant |
| X / Threads | The post is the thought; one extra line or a reply — not a product thread; links only to `youtube.com` or `/go/` |

### Skip soft mentions when

- the short has no natural object, or
- that platform already soft-mentioned something this week, or
- you cannot name a specific film (no YouTube URL / title).

### Code entry points

```ts
import { applyAffiliateSocialConstraints, assertAffiliateSafeSocialCopy } from "@/lib/affiliate/social-copy";
import { resolveAffiliateSocialContextForVideo } from "@/lib/affiliate/social-context";

// generatePlatformCopy({ …, affiliate }) applies constraints automatically
```

`assertAffiliateSafeSocialCopy` rejects captions that still contain merchant URLs or banned promo language before posts are written.

## Data model

| Model | Role |
|-------|------|
| `AffiliateProgram` | Amazon UK, Brilliant, Astronomy Retailer, LEGO, … |
| `AffiliateProduct` | Offers / kits / courses / category landings |
| `AffiliateTag` + `AffiliateProductTag` | Semantic matching tags |
| `AffiliatePlacement` | Video ↔ product link with type, score, approval |
| `AffiliateClick` | Redirect tracking (no fingerprinting / PII) |
| `AffiliateConversion` | Manual / CSV revenue attribution |
| `AffiliateUrlHealthCheck` | HEALTHY / REDIRECTED / BROKEN / UNKNOWN |
| `AffiliateDescriptionTemplate` | Editable YouTube snippet copy |
| `AffiliateImportBatch` | CSV import audit + duplicate hash |

`LongFormVideo` gains relations for placements, clicks, and conversions. Existing video metadata (`topic`, keywords, script, category) is reused for matching — not duplicated.

Migration: `20260815140000_affiliate_monetisation`

## Programme setup

1. Apply migration: `npx prisma migrate deploy`
2. Seed (dev): `npm run db:seed`
3. Set env IDs (never commit real values):

```bash
AMAZON_ASSOCIATE_TAG=your-uk-tag
BRILLIANT_AFFILIATE_ID=your-brilliant-id
AFFILIATE_REDIRECT_BASE_URL=https://orbitwithben.com/go   # optional; defaults to ${APP_BASE_URL}/go
```

Seed URLs are `example.invalid` placeholders. Replace product destination/affiliate URLs in `/affiliate/products` after accounts are approved.

| Programme | Slug | Notes |
|-----------|------|-------|
| Amazon Associates UK | `amazon-associates-uk` | Tag from `AMAZON_ASSOCIATE_TAG` at redirect time |
| Brilliant | `brilliant` | `BRILLIANT_AFFILIATE_ID` |
| Astronomy Retailer | `astronomy-retailer` | Generic specialist slot (FLO / HPS later) |
| LEGO | `lego` | Seeded **INACTIVE** until access is ready |

## Adding products

1. Open `/affiliate/products?new=1`
2. Choose programme, set destination + affiliate URLs, category, tags, commission estimates
3. Mark **featured** / **evergreen** carefully — featured boosts score; evergreen fills the Orbit recommendation slot
4. Or POST `/api/affiliate/products`

## Matching & recommendations

Deterministic first (`scoreAffiliateRelevance`). Future LLM strategy can implement the same `RelevanceStrategy` interface via `setRelevanceStrategy()`.

Scoring highlights: exact topic +40, related +20, category +15, evergreen +5, featured +10. Inactive programmes/products excluded. Max 4 links: 1 primary · ≤2 secondary · 1 evergreen.

On a video page: **Regenerate recommendations** → Approve / Reject / Remove.

## YouTube descriptions

```ts
import { generateYouTubeDescriptionWithAffiliates } from "@/lib/affiliate/description-service";
import { mergeDescriptionWithAffiliateLinks } from "@/lib/publishing/youtube-package";
```

- Editable templates in `AffiliateDescriptionTemplate` (seeded defaults)
- Disclosure appended unless the description already contains one
- Amazon-specific disclosure configurable (`amazon_disclosure` template)
- Links use Orbit redirects (`/go/{slug}`), not raw affiliate URLs

## Link tracking

`GET /go/{slug}?utm_campaign={video-slug}&video={id}`

1. Resolve product  
2. Record click (video, placement, UTM, timestamp, destination)  
3. Apply programme tag from env  
4. 302 to affiliate URL with UTM preserved  

Recommended UTM: `utm_source=youtube` · `utm_medium=affiliate` · `utm_campaign={video-slug}` · `utm_content={product-slug}`

## Reporting

- `/affiliate` — summary + warnings  
- `/affiliate/opportunities` — opportunity score, views, links, RPM  
- Homepage **Monetisation** card — month revenue, clicks, affiliate RPM, missing links  
- Metrics: clicks, CTR, conversions, EPC, revenue / 1k views, affiliate RPM (alongside YouTube RPM when ads data exists). `totalContentRpm()` ready for AdSense + Affiliate + Sponsorship.

## CSV imports

`/affiliate/import` or `POST /api/affiliate/import`

1. Preview (`dryRun`)  
2. Commit with `programmeSlug`  
3. Duplicate `contentHash` rejected  

Sample: `content/samples/csv/affiliate_amazon_sample.csv`

## URL health

`POST /api/affiliate/health` with `{ due: true, limit: 10 }` — throttled; does not hammer every URL. Prefer weekly manual/scheduled runs.

## Gear / public site (Phase 5 prep)

`GET /api/affiliate/gear` returns SEO-ready category + product JSON (`goUrl`, tags, programme). Ready for orbitwithben.com/gear — no full public marketing site in this app.

## Commands

```bash
cd 07_Content-Ops
npx prisma migrate deploy
npx prisma generate
npm run db:seed          # optional full reseed including affiliate catalogue
npm test                 # includes tests/affiliate.test.ts
npm run dev
```

Open http://localhost:3000/affiliate

## Manual account setup still required

- Amazon Associates UK approval + real tag in `AMAZON_ASSOCIATE_TAG`
- Brilliant affiliate approval + `BRILLIANT_AFFILIATE_ID`
- Specialist retailer programme contracts / tracking links
- LEGO Affiliate access (programme seeded inactive)
- Replace all `example.invalid` product URLs
- Production `AFFILIATE_REDIRECT_BASE_URL=https://orbitwithben.com/go` + DNS/hosting for redirects (or proxy to Content Ops)
