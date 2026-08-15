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
```

UI lives under `/affiliate/*` and on each long-form video detail page. Redirects: `/go/[slug]`.

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
