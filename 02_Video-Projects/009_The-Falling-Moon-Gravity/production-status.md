# Production status — Gravity (the falling Moon)

| Field | Value |
|---|---|
| Slug | `009_The-Falling-Moon-Gravity` |
| Stage | **FACT_NOTES sourced + upload package scaffold** (4 Oct 2026) |
| Script | PR #208 v01 · review **91.3** (may still be off main) |
| FACT_NOTES | Sourced from script new-claims; **7/7 hard-checks PASS**; Claude UNSIGNED |
| Neighbour gate | **PASS — 5 education ≥1M; TED-Ed yes** |
| Upload package | Manifest / description / tags / PRE_BUILD (UNSIGNED) / checklist scaffolded |
| Picture | **BOARDS v04 KEEP** (Chief PASS J0335, 15 Oct). 90 rows. Flow tranche 1 7,354 then tranche 2 5,180. **NO MINT.** |
| VO | **LOCKED v01** (Chief KEEP, desk #180 comment 6101629662, 11 Oct). Retime 8:38.4 in `07_Edit-Project/VO_RETIME_v01.json`. |

## STOP

- No Vertex/Veo/Flow minting on this film.
- Do not merge or close desk PR #180 from this work.
- Does **not** close #180.

## 24 Oct 2026 — J0909 (`J0899` Change 4): Gravity-apparatus search terms in description lines 1–2 and tags + Shorts VO & `J0383` teach-graphic alternation notes (Gemini covering)

- **Authority:** Chief PASS on `J0899` (`02_Video-Projects/_analytics/HOS_2026-10-24.md` §4 #4) and queue job `J0909`. `£0` spend, no live YouTube changes.
- **Applied to `11_Upload-Package/` and `10_Shorts/SHORTS_SCRIPTS_v02.md`:**
  1. **Gravity-apparatus search terms in description lines 1–2 and tags (`Descriptions/moon_long_description_v01.txt`, `Tags/moon_long_tags_v01.txt`, `PACKAGE_MANIFEST.json`, `PRE_BUILD_VIDIQ_AUDIT.md`):** Wove `"theory of gravity"`, `"how Newton proved gravity"`, and `"Cavendish torsion balance"` (from breakout neighbour `eyZEqSPeMwg`, `1.14M` views in 6.8h on 23–24 Oct, zero channel names) into lines 1–2 of `moon_long_description_v01.txt` (retaining `Moon`, `Newton`, `gravity` in the first 100 chars) and into `moon_long_tags_v01.txt` (8 tags total). Added `eyZEqSPeMwg` to `PACKAGE_MANIFEST.json` `neighbours.videos`.
  2. **Search-titled `v02` Shorts VO & `J0383` teach-graphic alternation (`LAUNCH_PLAN.md`, `10_Shorts/SHORTS_SCRIPTS_v02.md`, `PACKAGE_MANIFEST.json`):** Documented positive-question Shorts VO titles (*What Would Happen If the Moon Stopped Moving?* / *Why Doesn't the Moon Crash Into the Earth?*, *How Did Newton Discover Gravity?*) and alternating every `J0383`-verified parchment teach graphic in `0:00–0:30` and `1:00–2:00` with a moving 3D plate.
- **Package lint (`npm run lint:package -- --film 009`):** `PASS  02_Video-Projects/009_The-Falling-Moon-Gravity/11_Upload-Package/PACKAGE_MANIFEST.json`.
