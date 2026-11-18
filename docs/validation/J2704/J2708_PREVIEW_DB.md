# J2708 — isolated Preview database not established, 13 November 2026

Cursor covering. Source of the earlier local pass remains `2f8835325b5c634f9b421456e6b6f12bf90fec33`. No application code changed. Production environment variables were not changed. No secret values are recorded here.

## Already in place

- Vercel project `history-of-science-content-ops` on the existing Hobby team.
- Neon is already installed on that team on billing plan `free_v3` (free, no card required on that plan).
- Preview environment variable list: empty (confirmed again after the attempt below).
- Production environment variable list: empty. That matches the public home failure: the runtime log has no `DATABASE_URL`.

## Attempt

A new Neon resource was requested on the existing free plan, for Preview only, region `lhr1`, Neon Auth off, with no environment pull. The command failed before a resource existed:

`Your Team exceeded our fair use limits and has been blocked. (402)`

The team record shows a soft block:

- reason `FAIR_USE_LIMITS_EXCEEDED`
- overage type `fluidCpuDuration`
- blocked at 2026-11-12 18:13 UTC
- unpause at 2026-12-12 18:13 UTC

After the failure, both Preview and Production environment lists were still empty. No new store for this job appeared.

## Existing Neon stores were not reused

These stores are on the same free Neon installation. None is a disposable database for this app.

- `channelscout-production`: another product, not connected to a project.
- `channelscout-preview`: connected to the channelscout project, Preview and Development.
- `orbit-content-ops`: connected to the orbit-content-ops project, Production and Preview.

Pointing this app at any of them would run History of Science migrations against another product's database. That is not an isolated disposable database.

## What has to happen next

Zero-cost path: when the fair-use pause lifts at 2026-12-12 18:13 UTC, create one new Neon resource on `free_v3`, connect it to Preview only, and set `DATABASE_URL` and `DIRECT_URL` to that database alone. Add new disposable operator and encryption secrets, `PUBLISHING_DRY_RUN=true`, and no live OAuth or publishing credentials. Then hand the Preview build and login checks back to J2704.

Leaving the Hobby plan early would be new spend. That was not done.

J2708 waits until 2026-12-12 18:30 UTC for the unpause. J2704 stays blocked on this setup. Production remains HELD.
