# J2704 — HOS Next 16 validation, 12 November 2026

Codex covering. Source tested: `2f8835325b5c634f9b421456e6b6f12bf90fec33` (merged main, includes PR558 and PR568). No application code changed. Production deployment remains HELD.

## Results

- Full `npm run build`: exit 0, Next 16.4.6 compiled and generated routes. Prisma generation and the initial PostgreSQL migration both completed. See build.txt.
- `npm run typecheck`: exit 0. `npm run lint`: exit 0.
- `npm test`: 19 files / 199 tests PASS, exit 0.
- `bash 00_Brand/Channel-Setup/tools/check_all.sh`: exit 0, `ALL CHECKS PASS`.
- Local production server: home 200, login 200, OAuth start 307 to login, unauthenticated operator PATCH 401, authenticated PATCH 400 with expected missing-id validation. This request cannot mutate a product or publish. Authenticated login GET redirects 307 to home.
- Actual multipart password login returned 303 to home and issued a session cookie. Only new disposable credentials used; no credential values retained in evidence. A first URL-encoded form probe returned 200 without a cookie; correcting the probe to match the multipart server-action form succeeded.

## Database isolation

Fresh PostgreSQL 17 cluster created for this job, listening only at loopback on port 55474; new empty database `j2704_disposable`, no production data copied. Before build, DATABASE_URL and DIRECT_URL were asserted identical and pointed to that cluster. No live environment files were copied. Generated local operator/encryption secrets, PUBLISHING_DRY_RUN=true; no publishing worker or third-party credentials. Build migrations ran against this database only. Local cluster/server stopped after validation.

## Public baseline and root cause

Read-only probes on `https://history-of-science-content-ops.vercel.app` on 12 November 2026: login 200, home 500, unauthenticated OAuth start redirects to login (final page 200). Vercel runtime log at `2026-11-12T14:25:44.198Z`, production deployment `dpl_67ao5AXaWfQMehd3cyjGRNGWjdJF`, reports PrismaClientInitializationError: `Environment variable not found: DATABASE_URL` in schema.prisma:7 while calling longFormVideo.count(). This proves the current home failure is absent runtime database configuration; local home succeeds with a migrated disposable database. No production environment was changed. This is configuration repair, not an established Next 16 regression.

## Preview prerequisite — unresolved

Preview URL: none; no deployment attempted. Vercel connector environment metadata returned 403. Authorized CLI fallback (Vercel 65.14.0, explicit team and existing HOS project) succeeded and reported **No Environment Variables found** for Preview. No safe remotely reachable disposable PostgreSQL endpoint/configuration was established. A loopback database cannot serve Vercel; never substitute production URLs or expose local PostgreSQL publicly.

Required next work: identify or provision an approved zero-cost disposable hosted PostgreSQL database reachable from Vercel, verify both migration/runtime URLs belong solely to it, and configure a Preview deployment only with disposable operator/encryption secrets, dry run enabled, and no live OAuth/publishing credentials. Use explicit existing HOS project/team; do not change Production variables. Then run the same full build and auth/home checks on the Preview URL and submit evidence for elected-Chief review. Any new charge/account login requires its existing approval. This is actionable setup work, not an external timed wait, so no artificial recheck timer is set.

Production stays HELD until full build plus hosted Preview checks pass and elected Chief authorizes it. No YouTube, Buffer, live database, production deployment or spending side effect occurred.
