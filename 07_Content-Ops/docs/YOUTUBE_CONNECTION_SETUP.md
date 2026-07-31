# YouTube Connection Setup

**Docs checked:** 2026-07-31 — see [PLATFORM_API_REQUIREMENTS.md](./PLATFORM_API_REQUIREMENTS.md)

## Developer portal

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **YouTube Data API v3**
3. Configure OAuth consent screen (External or Internal)
4. Create **OAuth 2.0 Client ID** → Web application
5. Add authorised redirect URI:
   `http://localhost:3000/api/oauth/google/callback`

## Scopes (minimum)

- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.readonly`

## Environment

```env
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:3000/api/oauth/google/callback
ORBIT_TOKEN_ENCRYPTION_KEY=
APP_BASE_URL=http://localhost:3000
```

## Connect

1. Open `/settings/connections`
2. Click **Connect** on YouTube
3. Sign in with the Google account that owns the Orbit channel
4. Confirm the channel title, ID, and thumbnail appear

## Validate

Use **Validate** on the connection card. Expired tokens refresh via stored refresh token when available.

## Safe test upload

1. Set `PUBLISHING_DRY_RUN=false` only when ready
2. Ensure post has:
   - export MP4 path
   - `privacyStatus=private` (default for tests)
   - explicit `madeForKids` (do not infer from animation)
3. Enqueue the platform post
4. Run `npm run worker`
5. Confirm job shows genuine YouTube video ID + `https://www.youtube.com/watch?v=…`

**Do not claim autopublish operational until this private test succeeds.**

## Limitations

- Service accounts cannot upload to a normal channel
- Thumbnail upload needs the same OAuth user
- Shorts still use `videos.insert`; vertical validation is application-side

## Manual fallback

Export package → YouTube Studio → record URL/ID in Content Ops.
