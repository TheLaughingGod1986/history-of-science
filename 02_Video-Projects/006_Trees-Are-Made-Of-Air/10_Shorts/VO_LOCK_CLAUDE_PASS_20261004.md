# HOS 006 Shorts VO — Claude PASS lock (4 Oct 2026)

Source: [HOS #180 comment 5982291115](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-5982291115)  
`from=claude to=grok film=006 stage=vo status=pass` · A v02 · **B v03b** · C v01

**Picture stays paused** (VO-first). Shorts cut from the long's plates when 006 picture resumes. No Vertex/Flow mint from this lock.

## Locked takes

| Short | Take | Dur | Desk path | Repo path (working copy) | sha256 |
|---|---|---:|---|---|---|
| A | v02 | 22.64 s | `/Users/benjaminoats/_desk/006/shorts_vo_20261004/vo/t1_willow_air_vo_v02.mp3` | `10_Shorts/vo_20261004/t1_willow_air_vo_v02.mp3` | `ccce477426bc7b1db1a9c6bd65aa671e999f3528aee3c51b523d4da6f69c6f03` |
| B | **v03b** | 23.20 s | `/Users/benjaminoats/_desk/006/shorts_vo_20261004/vo/t2_mint_fixed_vo_v03b.mp3` | `10_Shorts/vo_20261004/t2_mint_fixed_vo_v03b.mp3` | `0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479` |
| C | v01 | 24.16 s | `/Users/benjaminoats/_desk/006/shorts_vo_20261004/vo/t3_bubbles_sunlight_vo_v01.mp3` | `10_Shorts/vo_20261004/t3_bubbles_sunlight_vo_v01.mp3` | `5b5d84e560d51ed9ad6f9bf5588f458802620f48f008b9409c532f8a1ea4e269` |

## Edit notes (from Claude PASS)

- **A:** trim spoken title after "…lost just two ounces." (~20 s VO + ~4 s silent loop to willow). Align tip: ounces ends ~19.92 s.
- **B:** v03b = volume −0.3 dB peak trim only; no title; closing line present. **Do not use** desk `t2_mint_fixed_vo_v03.mp3` (128 kbps sibling / overwrite confusion) or `*_OVERWRITE_21s.mp3`.
- **C:** pace 139 OK; Whisper "Ingenhaus" is ASR, not the voice.

## Evidence

- Desk word-check: `/Users/benjaminoats/_desk/006/shorts_vo_20261004/wordcheck_20261004/vo_check_B_v03b.json` (PASS mean −21.3 / peak −1.5)
- Desk report: `/Users/benjaminoats/_desk/006/shorts_vo_20261004/REPORT.md`
- #204 merged (`a99b59c`) carried earlier VO report scaffolding; this lock corrects B to **v03b**.

Locked by Grok Bot · 4 Oct 2026 ~17:55 Europe/London · no #180 merge · no picture mint


## Provenance confirmation (Grok, 4 Oct 2026 ~18:02 London)

One-process remeasure (`PROVENANCE_B_ONEPROC_20261004.md`) confirms:

- **B lock stays v03b** — `0f1099262037b62ea2b2a003ce86e196458fa983e9ca97877afb5600e97c7479` · **23.200000 s** · vo_check PASS (mean −21.3 / peak −1.5) · whisper **56/56 PASS** · no title.
- Sibling currently named `t2_mint_fixed_vo_v03.mp3` is **also** a good 23.20 s take (`cb45356…`, peak −1.2) — not the 21.6 s overwrite. Overwrite lives only as `t2_mint_fixed_vo_v03_OVERWRITE_21s.mp3` (`f11b88…`).
- No Short B TTS retake required.

