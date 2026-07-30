# Orbit Content Ops

Local multi-platform distribution dashboard for **Orbit with Ben**.

## Quick start

```bash
cp .env.example .env
npm install
npx prisma migrate dev
npm run db:seed
npm run dev
```

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Dashboard |
| `npm test` | Vitest suite |
| `npm run typecheck` | TypeScript |
| `npm run db:seed` | Seed aliens episode + 4 clips |
| `npm run generate:short-plan` | CLI clip planner |
| `npm run create:export-package` | Demo export package |

## Notes

- Does not replace the video production folders under `02_Video-Projects/`
- Publishing is **manual** in v1 — adapters are ready for future APIs
- Never commit secrets; use `.env`
