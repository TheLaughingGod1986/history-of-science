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

## Next manual steps (recommended)
1. In Meta Business Suite (IG home) → Create reel → **Share to** → **Connect a Facebook Page** → select **Orbit with Ben**.
2. Or on the Facebook Page → **Create reel** → upload the 3 short MP4s → when **Post** turns blue, publish with caption `… Full film on YouTube. https://youtu.be/Mo93x0fxB1Q`.
3. Exports: `02_Video-Projects/001_Will-We-Ever-Meet-Aliens/10_Shorts/06_Final-Exports/aliens_short-0{1,2,3}_*_v02.mp4`
