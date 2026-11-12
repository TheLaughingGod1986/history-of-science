# J2706 — Prisma 7 migration

12 November 2026, Codex. Separate follow-up to J2483 and the existing Chief ruling:
https://github.com/TheLaughingGod1986/orbit-with-ben/issues/478#issuecomment-6813294950

Official migration guide read before editing:
https://www.prisma.io/docs/guides/upgrade-prisma-orm/v7

## Changes

- Pin prisma, @prisma/client and @prisma/adapter-pg to 7.10.1. Next remains 16.4.6.
- Generate TypeScript into ignored src/generated/prisma with prisma-client. Explicit CommonJS output preserves existing tsx scripts using __dirname, avoiding a package-wide ESM conversion.
- The sole PrismaClient constructor is the cached storage singleton, now supplied with PrismaPg. Seed imports that singleton too. Runtime uses DATABASE_URL; adapter connection timeout is 5 seconds and idle timeout is 300 seconds. Driver pool defaults otherwise apply. TLS validation is not disabled.
- prisma.config.ts owns CLI connection selection (DIRECT_URL first, DATABASE_URL fallback), migrations path and seed command. Generator works with no credentials. Schema retains only the PostgreSQL provider; every model, relation, index and field is byte-for-byte unchanged. No migration SQL added or modified.
- with-direct-url retains aliases and the existing no-database migrate-deploy skip. It passes URLs in the child environment without writing them to .env. Four regression tests cover distinct URLs, alias fallback, no-URL migration skip and child exit propagation.

## Safe database verification

A new PostgreSQL 17 cluster was initialized exclusively for this job in SSD scratch, listening only on loopback on a dedicated port. Its empty job-specific database was created locally; no hosted credentials or shared .env files were copied. Before every verification batch a Python guard parsed BOTH DATABASE_URL and DIRECT_URL, requiring that exact loopback endpoint, dedicated port and disposable database name. Values are deliberately omitted here.

PASS: both database URLs target the disposable loopback cluster.

The existing migration was applied to this empty database, then the full build reran migrate deploy with no pending migrations. No seed or destructive reset was run. Existing database integration tests executed against that database with publishing dry-run enabled.

## Security audit

Before: 3 high, 0 critical/moderate/low (npm audit, full lockfile).
Dependency path: prisma 6.19.3 → @prisma/config 6.19.3 → deepmerge-ts 7.1.5.
Advisory: https://github.com/advisories/GHSA-ggr8-5vv4-36mx

After: 0 vulnerabilities at all severities.
Dependency path: prisma 7.10.1 → @prisma/config 7.10.1 → deepmerge-ts 8.0.2.
Runtime driver: @prisma/adapter-pg 7.10.1 → pg 8.23.1.
No npm audit fix --force was used.

## Validation

- Client generation (postinstall): PASS.
- Client generation without either database URL or env files: PASS.
- Existing migration deploy to the disposable database: PASS.
- Typecheck: PASS.
- ESLint: PASS.
- Full Vitest suite, including database-backed autopublish tests and new URL tests: PASS (20 files, 203 tests).
- Full npm run build, including generate + migrate deploy + Next build: PASS.
- check_all.sh: ALL CHECKS PASS.
- git diff --check: PASS.

No claim of audio or moving-video perception is involved in this tooling task.

## Rollback and release

This PR is for review only; no deployment or live migration is authorized by it. A later explicit elected-Chief decision is required before any deployment. Before release, review the hosted driver's TLS trust and pool capacity for that environment; the local test does not establish hosted connectivity.

Rollback before deployment: close the PR or revert the upgrade PR. After a separately authorized deployment: revert the upgrade PR, reinstall from the prior lockfile and regenerate Prisma 6 before redeploying under a new Chief decision. There is no application-schema or data rollback because this change introduces no schema/data migration. Regenerate the client whenever switching Prisma versions.

CI caught an app-level ignore file change governed by studio-core. The entry was moved into the channel root .gitignore; the shared file is restored exactly. `core_sync.py check`: PASS after correction.
