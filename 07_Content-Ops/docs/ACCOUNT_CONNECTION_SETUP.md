# Account Connection Setup

Shared steps for all History of Science Content Ops platforms.

## Prerequisites

1. Node.js 20+
2. Content Ops installed (`npm install` in `07_Content-Ops/`)
3. Encryption key generated (see [TOKEN_SECURITY.md](./TOKEN_SECURITY.md))
4. Developer accounts for each platform you intend to connect

## Base environment

```bash
cp .env.example .env
# set ORBIT_TOKEN_ENCRYPTION_KEY, APP_BASE_URL, and platform OAuth vars
npm run db:migrate
npm run db:seed
npm run dev:all
```

Open http://localhost:3000/settings/connections

## Callback URLs

Register these exact redirect URIs in each developer portal:

```text
http://localhost:3000/api/oauth/google/callback
http://localhost:3000/api/oauth/meta/callback
http://localhost:3000/api/oauth/tiktok/callback
http://localhost:3000/api/oauth/x/callback
```

For production, replace the host with your deployed `APP_BASE_URL`.

## Connection card actions

| Action | Effect |
|--------|--------|
| Connect / Reconnect | Starts server-side OAuth |
| Validate | Live API check of token + account |
| Disconnect | Revokes where supported, clears encrypted tokens, keeps history |
| Select Page / IG | Meta only — choose Page and linked Instagram pro account |

## Publishing modes

Default: `approve_each_post` (stored in `AppSetting` key `publishing_mode`).

A post is only eligible for API publish when:

- clip approved
- platform copy approved (`approvedForPublish`)
- export file exists
- connection valid
- required declarations set (e.g. YouTube `madeForKids`)
- duplicate checks pass
- dry-run is off (or job marked dry-run intentionally)

## Manual fallback

Every platform retains export packages + checklist. API unavailability never pretends to publish.

## Per-platform guides

- [YOUTUBE_CONNECTION_SETUP.md](./YOUTUBE_CONNECTION_SETUP.md)
- [META_CONNECTION_SETUP.md](./META_CONNECTION_SETUP.md)
- [TIKTOK_CONNECTION_SETUP.md](./TIKTOK_CONNECTION_SETUP.md)
- [X_CONNECTION_SETUP.md](./X_CONNECTION_SETUP.md)
- [THREADS_PUBLISHING_ASSESSMENT.md](./THREADS_PUBLISHING_ASSESSMENT.md)
