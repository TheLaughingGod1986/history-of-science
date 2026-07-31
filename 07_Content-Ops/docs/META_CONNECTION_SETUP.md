# Meta Connection Setup (Instagram + Facebook Reels)

**Docs checked:** 2026-07-31 — Instagram Content Publishing + Facebook Page APIs.

## Developer portal

1. Create an app at [Meta for Developers](https://developers.facebook.com/)
2. Add **Facebook Login** (and Instagram Graph / Content Publishing products as required)
3. Valid OAuth redirect:
   `http://localhost:3000/api/oauth/meta/callback`
4. Request permissions (App Review for live users beyond app roles):
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts` (as required for Page Reels)
   - `instagram_basic`
   - `instagram_content_publish`
   - `business_management` (if needed for Page discovery)

## Account requirements

- A Facebook user who can **manage** at least one Page
- Instagram **professional** account linked to that Page
- Personal IG accounts cannot be API-published

## Environment

```env
META_APP_ID=
META_APP_SECRET=
META_REDIRECT_URI=http://localhost:3000/api/oauth/meta/callback
ORBIT_TOKEN_ENCRYPTION_KEY=
```

## Connect flow

1. Connect via `/settings/connections` → Meta OAuth
2. System lists manageable Pages (stored in connection `metadataJson`)
3. Select Page + linked Instagram professional account
4. Validate permissions

Missing Page → `requires_attention`  
Missing IG pro → Instagram capabilities stay manual

## Publishing

### Instagram Reels

Container → poll processing → `media_publish`. Public media URL or resumable upload required. Localhost files are **not** fetchable by Meta — configure staging or use resumable path.

### Facebook Page Reels

Publish only to the selected Page. Personal profiles are not used.

## Safe test

Prefer the safest visibility Meta allows for your app mode. Confirm before any public feed post. Record genuine media IDs only after API success.

## Manual fallback

Always available via export packages when App Review or staging is incomplete.
