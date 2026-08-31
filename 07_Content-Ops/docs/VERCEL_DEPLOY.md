# Deploy Content Ops on Vercel (Postgres)

Public host for `/go/{slug}` and click persistence. Locked production origin:

**`https://history-of-science-content-ops.vercel.app`**

Do **not** use `orbit-content-ops.vercel.app` (Orbit With Ben). SQLite file DB is **not** the production path.

Live infra status / blockers: `00_Brand/Channel-Setup/HOS_CLOUD_INFRASTRUCTURE.md`.

## Vercel project (created 28 Aug 2026)

| Field | Value |
|---|---|
| Project | `history-of-science-content-ops` |
| Project id | `prj_GQglbnYlh6fZicGZGl8AhLHSWz3j` |
| Team | `ben's projects` |
| Git | `TheLaughingGod1986/history-of-science` · branch `main` |
| Root Directory | `07_Content-Ops` |

If recreating from scratch:

1. Import this monorepo into Vercel (or reuse the project above).
2. Set **Root Directory** to `07_Content-Ops` (Project Settings → General).
3. Framework Preset: Next.js (auto-detected).
4. Build Command (default from `package.json`):  
   `prisma generate && prisma migrate deploy && next build`  
   Do **not** use `prisma migrate dev` in CI/build — it hangs waiting for input.
5. Install Command: `npm install` (runs `postinstall` → `prisma generate`).

No repo-root `vercel.json` is required; keep other folders out of this project’s root.

## Environment variables

Set these on the Vercel project for **Production** and **Preview**:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Pooled Postgres URL for the app (Neon pooler, Supabase pooler, Vercel Postgres, etc.) |
| `DIRECT_URL` | Direct (non-pooled) URL for `prisma migrate deploy`. If your host has no pooler, set `DIRECT_URL` to the **same value** as `DATABASE_URL`. |
| `APP_BASE_URL` | `https://history-of-science-content-ops.vercel.app` |
| `CONTENT_OPS_OPERATOR_PASSWORD` | Operator login for mutating dashboard actions |
| `AMAZON_ASSOCIATE_TAG` | Set in the Vercel dashboard only (Production + Preview), e.g. the live Associates tag. Never commit the value. `/go` stamps `tag=` from this env at redirect time. |
| `AFFILIATE_REDIRECT_BASE_URL` | Optional. Defaults to `${APP_BASE_URL}/go`. |
| `ORBIT_TOKEN_ENCRYPTION_KEY` | Required in production for OAuth token encryption (see `.env.example`). |

Copy the rest of OAuth / publishing keys from `.env.example` as needed.

## After first deploy

Migrations run automatically during the Vercel build (`prisma migrate deploy`). Then seed and apply live Amazon destination URLs against the **hosted** DB (use your project’s env, not a fictional host):

```bash
cd 07_Content-Ops
# Point at the same DATABASE_URL / DIRECT_URL as the Vercel project
export DATABASE_URL="…"
export DIRECT_URL="…"   # or same as DATABASE_URL
npm run db:seed
npm run affiliate:apply-urls
```

Confirm `/go/{product-slug}` on `APP_BASE_URL` redirects and that `AffiliateClick` rows appear in Postgres.

## Local development

Local still uses **Postgres** (local Docker Postgres, Neon, etc.):

```bash
cd 07_Content-Ops
cp .env.example .env
# Set DATABASE_URL + DIRECT_URL (DIRECT_URL may equal DATABASE_URL for non-pooled local Postgres)
npm install
npx prisma migrate deploy   # or: npm run db:migrate
npm run db:seed
npm run dev
```

`npm run db:migrate` remains `prisma migrate dev` for local schema work. Production / Vercel always uses `prisma migrate deploy`.

## Notes

- Prisma provider is `postgresql` with `url = env("DATABASE_URL")` and `directUrl = env("DIRECT_URL")`.
- The Prisma client is cached on `globalThis` for Vercel serverless.
- Affiliate Amazon `tag=` is stamped only from `AMAZON_ASSOCIATE_TAG` at redirect time — never hard-coded in source or seed.
