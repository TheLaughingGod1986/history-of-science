# History of Science — Facebook + Instagram setup

Mirror of YouTube brand for Meta discovery. Pillar stays YouTube.

Canonical handles: `../SOCIALS_LAUNCH.md` · `../SOCIAL_IDENTITY.json`

## Identity

| Field | Value |
|-------|-------|
| Display name | **History of Science** |
| Preferred IG | **@historyofscienceyt** |
| Blocked | `@historyofscience` (Wellesley Science Center) · `@thehistoryofscience` |
| Fallbacks | `@hoscienceyt` · `@historyofsciencefilms` |
| Facebook Page | **History of Science** (new Meta Business portfolio) |
| Bio | `instagram_bio.txt` |
| Website | https://www.youtube.com/@HistoryOfScience |
| Avatar | Explorer (`TikTok/avatar_800x800.png`) — not Orbit |

## Soft CTA rule

Captions: “Full film on YouTube.” — never hard sell, never watermarked re-uploads.

## Auto-post

When a YouTube Short goes live, mirror to IG Reels + Facebook Page Reels:

→ **[AUTO_POST.md](./AUTO_POST.md)**

## Content Ops

OAuth + Page/IG selection:

→ **[CONNECT_TO_CONTENT_OPS.md](./CONNECT_TO_CONTENT_OPS.md)**

## Layout

```
00_Brand/Channel-Setup/Meta/
  META_ACCOUNTS.json
  META_CREDENTIALS.example.json   # copy → META_CREDENTIALS.json
  META_POSTED.json                # ledger (created at runtime)
  AUTO_POST.md
  CONNECT_TO_CONTENT_OPS.md
  META_SETUP.md
  auto/
    live_shorts_to_meta.py
    hooks.py
    graph_publish.py              # Graph API + resumable upload
    studio_upload.py              # Business Suite CDP fallback
    …
```
