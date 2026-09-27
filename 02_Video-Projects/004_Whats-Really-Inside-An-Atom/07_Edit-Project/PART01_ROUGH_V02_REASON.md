# Part 01 rough v02 — why

v01 assembly error: `_assemble_part01_rough_v01.py` used hardcoded `CLIP_USE=7.9` per plate × 17 with 0.35s xfade → **128.7s** picture. VO v04 is **69.81s**; audio stream ended at VO while video kept playing (no black pad — full Veo clips). v02 cuts each plate to `part-01_plates_v02.json` `t_s` windows (hard concat, no freeze-pad) so A/V both ≈70s. v01 kept.

- v01: `hos_004_part01_rough_v01.mp4` 128.7s (kept)
- v02: `hos_004_part01_rough_v02.mp4` 69.813s  v=69.800s a=69.813s
- sha256: `b74ab21d3820ebcad62a2872c56f00fd37d0e2024474ee15b19c381f934d8050`
- iCloud: `/Users/benjaminoats/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/004_Whats-Really-Inside-An-Atom/09_Final-Export/hos_004_part01_rough_v02.mp4`
- cold-open cuts >6s: 0 (none)
