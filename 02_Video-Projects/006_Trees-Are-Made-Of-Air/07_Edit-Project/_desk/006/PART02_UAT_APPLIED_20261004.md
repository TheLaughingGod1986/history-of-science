# HOS 006 Part 02 — UAT applied (4 Oct 2026)

Authority: Claude → Grok **#180 comment 5981378493**. Credit accepted: £28.37 real / £23.37 usable. **No new mints.**

## Claude dispositions → edit application

| Plate | Claude | Applied |
|---|---|---|
| 08_haul_tree | KEEP t1 trim 0–4.80s; drop t2 | `use_s` 5.88→**4.8**; source `raw/v01_trim/08_haul_tree_t1_trim_0to4p8.mp4`; t2 spare unused |
| 12_pointer_short | KEEP full t1 | full `12_pointer_short_t1.mp4`, board `use_s` 6.78 |
| 14_why_grown | FAIL — cover w/ 17 opening | `cut: true` + cover `17_mostly_wrong` in=0 out=4.4; 14 clip not used |
| 15_desk_candle | KEEP | full t1, `use_s` 5.46 |
| 16_water_drawing | KEEP | full t1, `use_s` 5.14 |
| 17_mostly_wrong | KEEP (leaf spin) | still itself after 14 cover pull; `use_s` 5.32 |
| 18_charcoal_hearth | KEEP | full t1, `use_s` 6.78 |
| 19_ash_mound | KEEP trim 0→~66% | `uat_trim` 0–4.0s; assemble uses board `use_s` 3.54 from that window |
| 20_shimmer_coals | KEEP | full window for self; tail also covers 21 |
| 21_gas_window | FAIL — cover w/ 20 tail + hold | `cut: true` + cover from `20_shimmer_coals` + freeze pad to `use_s` 6.64 |
| 22_shimmer_willow | KEEP last third | `uat_trim` in≈5.333 out=8.0 (~2.67s); freeze-pad to `use_s` 5.96 |

## Prior twin-FAIL (already on board; unchanged)

| Plate | Disposition |
|---|---|
| 07_explorer_snow | CUT (`use_s` 0); 06 t2 covers |
| 02_balance_200 | PARK stand-in = 09_weights_169 until Tuesday Flow |
| 11_furnace_again | REUSE 2.00–5.54s of 01_furnace_soil |

Earlier KEEP spine still KEEP: 01, 03, 04, 05, 06t2, 09, 10, 13.

## Rough outputs

- Local: `07_Edit-Project/_precheck/hos_006_part02_rough_v02.mp4`
- Assemble dir: `07_Edit-Project/_precheck/part02_full_assemble/` (+ `ROUGH_META.json`)
- iCloud UAT: `HOS UAT/006_Trees-Are-Made-Of-Air/hos_006_part02_rough_v02.mp4` + `stills/`
- Board: `07_Edit-Project/parts/part-02_plates_v01.json` (`status: UAT_APPLIED_PART02_ROUGH_V02`)
- VO mux: `02_Voiceover/part02_five_years_and_two_ounces_v02.mp3` (~117s)
- Method: ffmpeg trim (+ tpad freeze where needed) → flat concat of board `use_s` segments (xfade 0.35 noted on board; rough uses hard cuts like prior KEEP spine for speed)

## Cut-checker

Advisory freezedetect + chapter stills → `PART02_CUTCHECK_RESULT_20261004.md`. Queue/status marked DONE for full rough.

## Explicitly not done

- No Vertex / Flow mint
- No spend
- #180 not merged / not closed
- No Ben ping; parent posts from=grok reply

## Evidence / local-only paths (gitignored mp4/png)

- Rough local: `07_Edit-Project/_precheck/hos_006_part02_rough_v02.mp4` (**gitignored** via `_precheck/`)
- Assemble: `07_Edit-Project/_precheck/part02_full_assemble/` (**gitignored**; meta copied to `_desk/006/ROUGH_META_part02_v02.json`)
- iCloud: `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/006_Trees-Are-Made-Of-Air/hos_006_part02_rough_v02.mp4`
- Finder screenshot (full PNG gitignored): `_desk/006/_evidence/hos_006_part02_rough_v02_icloud_finder_20261004.png`
- Finder screenshot (JPG in git): `_desk/006/_evidence/hos_006_part02_rough_v02_icloud_finder_20261004.jpg`
