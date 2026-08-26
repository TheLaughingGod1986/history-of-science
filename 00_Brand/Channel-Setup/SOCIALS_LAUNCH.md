# History of Science — YouTube + socials launch pack

Prepared: **26 Aug 2026**  
Canonical identity: `SOCIAL_IDENTITY.json` · vision: `CHANNEL_VISION.md`  
Google login: `benoats86@gmail.com`  
**Never** create, brand, or OAuth against Orbit With Ben (`UC_esArsDKd3GJvOkeO0DUog` / `@orbitwithben`).

Paste-ready copy lives next to this file (`channel_description.txt`, `instagram_bio.txt`, …).

---

## What this channel is

| | |
|---|---|
| Display name | **History of Science** |
| YouTube handle | **@HistoryOfScienceYT** |
| Feel | 3D cartoon · Animistry-class · 8–9 min longs |
| Tagline | How we discovered what we know. |
| Banner | DISCOVERY. WONDER. PROOF. |
| Mascot | **the Explorer** — side character only |
| Not | Orbit With Ben · orange robot · continuous mascot show |

---

## Handle check (26 Aug 2026)

| Platform | Wanted | Status | What to do |
|---|---|---|---|
| YouTube | `@HistoryOfScience` | Taken. Live handle is **`@HistoryOfScienceYT`** (`UCXp7HkBIl1LgaznXuZHJyRg`) | Done 26 Aug 2026 |
| Instagram | `@historyofscience` | **Taken** (Wellesley Science Center) | Created **`@historyofscienceyt`** (Creator, 26 Aug 2026) |
| Instagram | `@thehistoryofscience` | **Taken** | Skip |
| Threads | follows IG | `@historyofscienceyt` | Live https://www.threads.com/@historyofscienceyt |
| TikTok | `@historyofscience` | **Taken** — ภวัต วิชัยรัตน์ (empty-ish, not ours) | Create **`@historyofscienceyt`**. **Not** the banned `@orbitwithben` account. |
| Facebook Page | History of Science | Live `61593586420124` | https://www.facebook.com/profile.php?id=61593586420124 — Page↔IG link still to retry |
| X | optional | Skip at launch | Only after YouTube + Meta are live |

---

## Create order (Ben, logged in as `benoats86@gmail.com`)

Do these in this order. Fill IDs into `CHANNEL_META.json` / `SOCIAL_IDENTITY.json` as you go.

### 1. YouTube (pillar) — today

1. [youtube.com/channel_switcher](https://www.youtube.com/channel_switcher) → look for **History of Science**.
2. **If it is there:** switch into it. Studio → Customisation.
3. **If it is not there:** Create a channel → name `History of Science` → handle `@HistoryOfScience` (or nearest).
4. Apply (or run `python3 00_Brand/Channel-Setup/_brand_hos_youtube.py` after Google sign-in):
   - Avatar: `00_Brand/Channel-Setup/avatar_800x800.png`
   - Banner: `00_Brand/Channel-Setup/banner_2560x1440.png`
   - Name: `History of Science` (Title Case)
   - Handle: `@HistoryOfScience`
   - Description: `channel_description.txt`
   - Keywords: `channel_keywords.txt`
   - Country: United Kingdom · Language: English (UK)
   - Made for kids: **No**
5. Copy the `UC…` channel ID into `CHANNEL_META.json` (`channel_id` + `studio_url`).
6. Do **not** upload films yet. Do **not** connect VidIQ/OAuth until the ID is in that file.

### 2. Meta Business + Facebook Page

1. [business.facebook.com](https://business.facebook.com) → create portfolio **History of Science** (not Benkay, not Orbit).
2. Create Facebook **Page** named **History of Science**.
3. About: `facebook_about.txt`. Website: `https://www.youtube.com/@HistoryOfScience`.
4. Avatar = same 800×800 file. Cover = banner (crop).
5. Save Page ID into `Meta/META_ACCOUNTS.json`.

### 3. Instagram (Professional)

1. New IG account **`@historyofscienceyt`** (confirm available at create).
2. Switch to **Professional → Creator**.
3. Bio: `instagram_bio.txt`. Link: YouTube handle URL.
4. Avatar = same 800×800.
5. Link IG to the new Facebook Page (required for Reels publishing).

### 4. Threads

Created from the same Instagram. Display name **History of Science**. Bio: `threads_bio.txt`. Website: YouTube.

### 5. TikTok (account only — no posts yet)

1. Confirm whether `@historyofscience` is already on this Google/phone login.
2. Display name **History of Science**. Bio: `tiktok_bio.txt`.
3. Avatar = same 800×800. Website = YouTube.
4. **Do not post** until the first YouTube Short is public.  
   Orbit’s TikTok **upload ban does not apply** to this new account — still wait for YouTube-first.

### 6. After IDs exist

1. YouTube Data API OAuth for **this** Brand Account only (`07_Content-Ops`).
2. Deploy HOS Content Ops (do not reuse `orbit-content-ops.vercel.app`).
3. Connect Meta + Threads in Content Ops `/settings/connections`.
4. Optional X later.

---

## Soft CTA (locked)

Captions: **Full film on YouTube.**  
On-screen Shorts: **watch the full film →**  
One unique post per Short on IG, Facebook, and Threads. Zero `/go/` on Shorts.

---

## Assets

| File | Use |
|---|---|
| `avatar_800x800.png` | YouTube, IG, TikTok, Threads, FB |
| `banner_2560x1440.png` | YouTube banner (also FB cover crop) |
| `01_Character/01_Master-References/hos-explorer-character-sheet-v01.jpg` | Identity lock — not the avatar itself |

Avatar/banner are **v01 drafts** from the Explorer sheet. If the face feels off-model vs the sheet, regen before publishing the channel art.

---

## Done when

- [x] YouTube `channel_id` is `UCXp7HkBIl1LgaznXuZHJyRg` — **not** `UC_esArsDKd3GJvOkeO0DUog`
- [x] Avatar, banner, Title Case name, description live
- [x] IG `@historyofscienceyt` + FB Page + Threads exist
- [ ] Link IG ↔ Facebook Page (Meta temporary restriction 26 Aug 2026)
- [ ] TikTok skipped for now; planned `@historyofscienceyt`; no posts
- [x] `CHANNEL_META.json` + `SOCIAL_IDENTITY.json` + `META_ACCOUNTS.json` filled
- [ ] Content Ops OAuth points at **this** channel only
