# HOS cloud infrastructure (28 Aug 2026)

**Goal:** live Content Ops for History of Science at  
`https://history-of-science-content-ops.vercel.app`  
(locked `/go/{slug}` host — never `orbit-content-ops.vercel.app`).

## Done this run

| Piece | Status |
|---|---|
| Vercel project `history-of-science-content-ops` | **Created** · id `prj_GQglbnYlh6fZicGZGl8AhLHSWz3j` |
| Team | `ben's projects` (`team_UPErYpfb3ww71LYTIWUoKvcH`) |
| Git link | `TheLaughingGod1986/history-of-science` (GitHub) · production branch `main` |
| Root Directory | `07_Content-Ops` |
| Domains / live deploy | **None yet** — no successful production build |
| Separate from Orbit | Yes — Orbit stays on project `orbit-content-ops` → `orbit-with-ben` |

Dashboard: https://vercel.com/bens-projects-11c93b15/history-of-science-content-ops

## Blocked — Postgres

First production deploy needs `DATABASE_URL` + `DIRECT_URL`.

Attempted paths (28 Aug 2026 cloud agent):

| Path | Result |
|---|---|
| **New Supabase project** (`eu-west-2`) | **Blocked** — free-project admin limit (2 active). Active: OpptiAI · Family Discovery. Do **not** pause those without Ben. |
| **Render Postgres** | MCP unauthorized / no workspace confirmed |
| **Neon via Vercel CLI** | No Vercel CLI credentials in this cloud VM |

### Unblock (pick one)

1. **Neon (preferred for Vercel):** create a free Neon DB → copy pooled + direct URLs into Vercel project env (Production + Preview).
2. **Supabase:** free a slot (pause/delete an unused free project **you** choose, or upgrade) → create `history-of-science-content-ops` → set pooled + direct URLs on Vercel.
3. **Vercel Marketplace Postgres / Neon:** add from the project Storage / Integrations tab → same env wiring.

## Env to set before first deploy

Set on Vercel **Production** and **Preview** (never commit values):

| Variable | Notes |
|---|---|
| `DATABASE_URL` | Pooled Postgres |
| `DIRECT_URL` | Direct URL for `prisma migrate deploy` (same as pooled if no pooler) |
| `APP_BASE_URL` | `https://history-of-science-content-ops.vercel.app` |
| `ORBIT_TOKEN_ENCRYPTION_KEY` | `openssl rand -base64 32` |
| `CONTENT_OPS_OPERATOR_PASSWORD` | `openssl rand -base64 24` |
| `PUBLISHING_DRY_RUN` | `true` until OAuth is ready |
| `AMAZON_ASSOCIATE_TAG` | Dashboard only, when Associates is live |
| `BRILLIANT_AFFILIATE_ID` | Optional until Brilliant is live |

OAuth keys (YouTube / Meta / Threads) can wait until channel accounts exist.

## After env is set

1. Redeploy from Vercel (or push to `main`) — build runs `prisma generate && prisma migrate deploy && next build`.
2. Against the **hosted** DB:

```bash
cd 07_Content-Ops
export DATABASE_URL="…"
export DIRECT_URL="…"
npm run db:seed
npm run affiliate:apply-urls
npm run affiliate:verify -- --probe
```

3. Smoke: `https://history-of-science-content-ops.vercel.app/go/<product-slug>` → 302 + `AffiliateClick` row.
4. Sign in at `/login` with `CONTENT_OPS_OPERATOR_PASSWORD`.

## Explicitly not this run

- Do **not** point HOS at `orbit-content-ops.vercel.app`
- Do **not** use `historyofscience.com` / `oppti.dev` until DNS points here
- Do **not** spend Flow/Omni credits or remint HOS Part 02 here
- TikTok remains paused

Canonical deploy runbook: `07_Content-Ops/docs/VERCEL_DEPLOY.md`  
Affiliate go-live: `07_Content-Ops/docs/AFFILIATE_GO_LIVE.md`
