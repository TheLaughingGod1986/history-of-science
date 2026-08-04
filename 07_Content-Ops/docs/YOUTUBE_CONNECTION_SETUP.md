# YouTube Connection Setup

**Docs checked:** 2026-08-05 — see [PLATFORM_API_REQUIREMENTS.md](./PLATFORM_API_REQUIREMENTS.md)

## Default upload path

**YouTube Data API v3 is the default** for Orbit uploads and native schedules (`privacyStatus=private` + `publishAt`).

YouTube Studio CDP / Playwright is **fallback only** when OAuth is unavailable or the API rejects a one-off edge case.

```bash
# Dry-run (no network upload)
npm run youtube:upload -- --file /path/to.mp4 --title "Test" --dry-run

# Private test upload now
npm run youtube:upload -- --file /path/to.mp4 --title "Test" --privacy private --made-for-kids false

# Upload now, go live later (native schedule)
npm run youtube:upload -- --file /path/to.mp4 --title "Episode" \
  --format longform --schedule 2026-08-10T18:00:00Z \
  --thumbnail /path/to.jpg --made-for-kids false
```

Or enqueue a Content Ops `PlatformPost` and run `npm run worker` — YouTube jobs with a future `scheduledAt` are claimed **immediately** and uploaded with `publishAt`.

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
3. Enqueue the platform post (or use `npm run youtube:upload`)
4. Run `npm run worker` if using the queue
5. Confirm job shows genuine YouTube video ID + `https://youtu.be/…`
6. For scheduled posts: `uploadStatus=scheduled` and Studio shows the future publish time

**Do not claim autopublish operational until a private test succeeds.**

## Native schedule behaviour

| Step | Behaviour |
|------|-----------|
| Enqueue with future `scheduledAt` | Job `nextAttemptAt = now` (do not wait until air time) |
| Worker claim | Allowed before `scheduledAt` for YouTube |
| API payload | `status.privacyStatus=private` (or unlisted) + `status.publishAt` ISO |
| After upload | Job → `awaiting_platform_processing`; post → `uploadStatus=scheduled` |
| After go-live | Reconcile via `videos.list` → `uploadStatus=published` |

`publishAt` must be roughly **≥15 minutes** ahead; closer times upload immediately without native schedule.

## Limitations

- Service accounts cannot upload to a normal channel
- Thumbnail upload needs the same OAuth user (`thumbnails.set`)
- Shorts and long-form both use `videos.insert`; format is application-side (`--format longform` skips Shorts duration warnings)
- Local worker must be online **at upload time**, not at air time (YouTube holds the schedule)

## Manual fallback

Export package → YouTube Studio → record URL/ID in Content Ops. Prefer fixing OAuth / API errors over CDP automation.
