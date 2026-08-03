# Facebook Page missing videos — 2026-08-03

## Diagnosis
The 3 live Orbit shorts were published to **Instagram only** (`asset_id=1251385088056874`).

The Facebook Page (`Orbit with Ben`, `page_id=61592833318203`) Reels tab was empty:
`You haven't created any reels yet.`

Suite composer destination shows **Connect a Facebook Page** — IG is not linked to the Page, so "Share to Facebook and Instagram" does not actually reach Facebook.

## Blockers found while trying to post to the Page
1. **IG ↔ Facebook Page not connected** in Meta Business Suite (Connect a Facebook Page link was disabled / pending Benkay Creative access for some settings).
2. Facebook **Create reel → Post button stays permanently disabled** (`aria-disabled=true`) even after upload + caption + AI label toggle + waiting 2+ minutes. Manual finish may be required in the FB UI.
3. Direct Suite URL for FB Page asset `1285932871266399` returns "content isn't available" in this CDP session.

## What users need on Facebook
Until reels are posted to the Page:
- Bio already: `Full films on YouTube`
- Page URL: https://www.facebook.com/profile.php?id=61592833318203

## Resolution (2026-08-03 ~11:55)
Posted all 3 shorts directly on the Facebook Page via CDP `:9222` (TikTok Chrome profile still had a live FB session; Meta profile cookies on `:9223` were wiped).

Verified on Page Reels + Videos:
- Where Is Everybody?
- Space Is Rude About Distance
- What If Aliens Are Watching Us?

Each caption includes `Full film on YouTube. https://youtu.be/Mo93x0fxB1Q`.

Artifacts: `audits/fb_page_retry_2026-08-03/V17_RESULT.json`, `v17_probe_0.png`, `v17_probe_1.png`, `_post_fb_page_reels_v17.py`.

## Still recommended
1. Re-login `~/.orbit-chrome-meta-dev` on `:9223` (start with `--remote-allow-origins=*`).
2. In Suite → Create reel → **Share to** → **Connect a Facebook Page** → **Orbit with Ben** (so IG shares also land on FB).
3. Exports: `02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports/aliens_short-0{1,2,3}_*_v02.mp4`
