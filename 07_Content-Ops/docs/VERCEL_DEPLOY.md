# Deploy Content Ops on Vercel (Postgres)

Public host for `/go/{slug}` and click persistence. Use the Vercel `*.vercel.app` URL (or a custom domain you control later). SQLite file DB is **not** the production path.

## Vercel project setup

1. Import this monorepo into Vercel.
2. Set **Root Directory** to `07_Content-Ops` (Project Settings → General).
3. Framework Preset: Next.js (auto-detected).
4. Build Command (default from `package.json`):  
   `node scripts/with-direct-url.mjs prisma generate && node scripts/with-direct-url.mjs prisma migrate deploy && next build`  
   Do **not** use `prisma migrate dev` in CI/build — it hangs waiting for input.
5. Install Command: `npm install` (runs `postinstall` → `with-direct-url` → `prisma generate`).
6. **Ignored Build Step** (`vercel.json` → `ignoreCommand`):  
   `bash scripts/vercel-ignore-build.sh`  
   - **Skip** (exit 0) when `07_Content-Ops` has **no** diff vs the previous commit — docs-only / non-app merges must not take production down.  
   - **Proceed** (exit 1) when this package changed.  
   Root Directory is `07_Content-Ops`; the script diffs that path from the git toplevel (monorepo root), not only the Root Directory cwd.

No repo-root `vercel.json` is required; keep other folders out of this project’s root.

## Environment variables

Set these on the Vercel project for **Production** and **Preview**:

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Pooled Postgres URL for the app (Neon pooler, Supabase pooler, Vercel Postgres, etc.). Set for **Production and Preview**. Required for migrations and `/go/` click persistence. If unset at build time, `prisma migrate deploy` is skipped so the Next build can still go Ready (Prisma only reports a missing `DIRECT_URL` even when `DATABASE_URL` is also absent — Validation Error Count: 1 is ambiguous). |
| `DIRECT_URL` | Direct (non-pooled) URL for `prisma migrate deploy`. **Optional on Vercel:** if unset, `scripts/with-direct-url.mjs` defaults it to `DATABASE_URL` for both `postinstall` and `build`. Set an explicit direct (non-pooler) URL when using Neon/Supabase pooler. |
| `APP_BASE_URL` | Public origin of this deploy, e.g. `https://YOUR-PROJECT.vercel.app` |
| `AMAZON_ASSOCIATE_TAG` | Set in the Vercel dashboard only (Production + Preview), e.g. the live Associates tag. Never commit the value. `/go` stamps `tag=` from this env at redirect time. |
| `AFFILIATE_REDIRECT_BASE_URL` | Optional. Defaults to `${APP_BASE_URL}/go`. |
| `ORBIT_TOKEN_ENCRYPTION_KEY` | Required in production for OAuth token encryption (see `.env.example`). |

Copy the rest of OAuth / publishing keys from `.env.example` as needed.

**Do not** put secrets in git. Prefer setting `DATABASE_URL` on Vercel (Production **and** Preview); add a separate `DIRECT_URL` only when the pooled URL must not be used for migrations. `with-direct-url.mjs` never skips `migrate deploy` when a real `DATABASE_URL` is present; it only skips when no DB URL exists at build time.

## After first deploy

Migrations run automatically during the Vercel build (`prisma migrate deploy` via `with-direct-url` — never skipped when a real `DATABASE_URL` is present). Then seed and apply live Amazon destination URLs against the **hosted** DB (use your project’s env, not a fictional host):

```bash
cd 07_Content-Ops
# Point at the same DATABASE_URL / DIRECT_URL as the Vercel project
export DATABASE_URL="…"
export DIRECT_URL="…"   # optional; defaults to DATABASE_URL in npm scripts via with-direct-url
npm run db:seed
npm run affiliate:apply-urls
```

Confirm `/go/{product-slug}` on `APP_BASE_URL` redirects and that `AffiliateClick` rows appear in Postgres.

## Local development

Local still uses **Postgres** (local Docker Postgres, Neon, etc.):

```bash
cd 07_Content-Ops
cp .env.example .env
# Set DATABASE_URL. DIRECT_URL may equal DATABASE_URL for non-pooled local Postgres
# (npm postinstall/build will default DIRECT_URL from DATABASE_URL if unset).
npm install
npx prisma migrate deploy   # or: npm run db:migrate
npm run db:seed
npm run dev
```

`npm run db:migrate` remains `prisma migrate dev` for local schema work. Production / Vercel always uses `prisma migrate deploy`.

## Notes

- Prisma provider is `postgresql` with `url = env("DATABASE_URL")` and `directUrl = env("DIRECT_URL")` (kept for Neon/pooler). Build/postinstall wrap Prisma with `scripts/with-direct-url.mjs` so a missing `DIRECT_URL` does not fail the deploy when `DATABASE_URL` is set.
- Docs-only merges outside `07_Content-Ops` are skipped by `ignoreCommand` so they cannot redline production.
- The Prisma client is cached on `globalThis` for Vercel serverless.
- Affiliate Amazon `tag=` is stamped only from `AMAZON_ASSOCIATE_TAG` at redirect time — never hard-coded in source or seed.
