# Orbit Content Ops

Local multi-platform distribution + autopublish dashboard for **Orbit with Ben**.

## Quick start

```bash
cp .env.example .env
# set ORBIT_TOKEN_ENCRYPTION_KEY=$(openssl rand -base64 32)
npm install
npx prisma migrate dev
npm run db:seed
npm run dev:all
```

Open http://localhost:3000 — connect accounts at `/settings/connections`.

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Dashboard only |
| `npm run worker` | Publishing worker |
| `npm run dev:all` | Dashboard + worker |
| `npm test` | Vitest suite |
| `npm run typecheck` | TypeScript |
| `npm run connections:validate` | Re-validate OAuth connections |
| `npm run publishing:reconcile` | Reconcile ambiguous jobs |
| `npm run db:seed` | Seed aliens episode + 4 clips |

## Autopublish notes

- Official OAuth/APIs only; tokens encrypted at rest (AES-256-GCM)
- Posts are marked `published` only after a genuine platform ID/URL
- Local scheduling requires the worker process — not cloud-reliable
- Default `PUBLISHING_DRY_RUN=true` in `.env.example`
- Setup: `docs/ACCOUNT_CONNECTION_SETUP.md` and platform guides under `docs/`

## Scope

- Does not replace video production under `02_Video-Projects/`
- Never commit secrets; use `.env`
