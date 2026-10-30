# J0329 — Franklin code graphics v01, Chief review requested

16 October 2026 · builder: codex · no creative PASS or final OK issued.

**FIX, 16 Oct ~02:06 London (Cursor covering).** P5:11 only. Label is now **SAFE PATH DOWN** (3 words). Re-rendered `code_graphic_008_p5_11_safe_path.mp4` (210 frames, 1920×1080, 30 fps, no audio). The other ten MP4s and five alpha MOVs are the 00:37 renders, hashes unchanged. Frame at 2.5 s shows the new label. NAS mirror was not retried.

Eleven silent 1920×1080, 30 fps MP4s follow the v03 board's `use_s` and film/part VO placements. Five additional ProRes 4444 MOVs contain straight alpha. Full-frame rows have a cream/gold/blue ink drawing on brown period paper, Didot italic labels, and drawn mechanisms. The builder uses the existing Pillow/ffmpeg house approach, with no API calls, generated imagery or paid dependencies. No VO or source board was changed.

## Files and reproduction

Local pack: `/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/code_graphics_v01/`.

NAS destination (copy pending; not yet verified): `/Volumes/data/mac-mini-archive/YouTube/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/code_graphics_v01/`.

The pack contains all clips, eleven sample stills, `CONTACT_SHEET.jpg`, `MANIFEST.json`, `TECHNICAL_CHECKS.json`, and `SHA256SUMS.txt`. Text-only copies of the manifest, checks and hashes accompany this note. Renders are excluded from git.

```sh
/Users/benjaminoats/_desk/venv-graphics/bin/python \
  02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/_build_code_graphics_v01.py \
  --out <new-empty-output-directory>
```

`--stills-only` makes the sample stills first. The renderer refuses to overwrite existing videos. It streams frames into ffmpeg, avoiding large image-sequence scratch folders. Duration rounds up by less than one 30 fps frame: assembly trims to the manifest's exact `use_s`. Manifest records locked VO hash, source-board hash, spoken lines, film start, part-relative start and original `tick_ink_s`. Ticks are cues for the separate SFX stem, not embedded audio; their eventual mix requires the house level check.

## Composite and review holds

The brief mentions two overlays; the authoritative plan has **five**. All five are delivered as alpha plus clearly provisional paper-backed MP4 previews:

| Row | Required moving picture |
|---|---|
| P2:15 likeness_fire | P2:12 notebook_list, unused moving tail |
| P3:04 letter_crosses | P3:07 slow_news |
| P4:06 same_thing | P2:08 jar_spark and P4:02 knuckle_spark, left/right |
| P5:08 looking_path | P1:16 question_sky |
| P5:10 metal_easy | P5:06 rod_fitting |

No local picture KEEP record exists for 008 yet. In particular P4:06 is only its divider and label: it is **not a completed spark comparison**. Paper MP4s must never be substituted into these moving-plate slots in the finished film. After mint/KEEP, position overlays against the actual subjects and verify unused windows and continuous movement.

Chief should review each graphic against its VO in motion, not only the contact sheet. Outstanding judgment points:

- The Atlantic contour is a schematic ink coastline, not a verified historical 1752 map. Its geographical fidelity needs review or a sourced geometry revision before acceptance.
- P5:11 label is SAFE PATH DOWN (3 words), set by Chief on 16 Oct and re-rendered. The old seven-word line is gone.
- Tick times and graphic events follow the boards; exact spoken-word alignment remains an assembly review against the locked audio. The builder does not replace the part VO or retime speech.
- Five rows still require moving plates; plate alignment, composite readability and final UAT cannot be judged from these standalone alpha files.

The mint gate remains unchanged: after 006 and 007, with a live Flow reading leaving at least 3,000 credits after 008's expected 5,605. No Flow, Vertex or ElevenLabs calls, no spend, no uploads, and no deletion.

## Validation evidence

Repository `check_all.sh` output:

```text
-- no media: PASS
-- status board in sync: PASS
-- ElevenLabs guard tests: PASS
-- vo_check word tests: PASS
-- contract tests: PASS
-- package-lint: PASS
ALL CHECKS PASS
```

These are automated repository results, not Chief's creative PASS. Status board regenerated and checked again after the review handoff update.

Native-resolution alpha verification is used: a first attempt downscaled alpha to 192×108 and failed an opacity threshold because it averaged thin ink strokes. The corrected check examines the actual full-resolution alpha, requiring both fully transparent pixels and opaque ink.

## NAS handoff — blocked on mkdir

The first mirror attempt stopped on the downscaled-alpha test before any copy. The corrected run passed all decode/alpha checks (`TECHNICAL_CHECKS.json`, 11 rows), then blocked inside macOS `mkdir` while creating the new NAS destination (process sample: stuck in `mkdir`, empty log). Cursor covering stopped that session at 01:24 London on 16 Oct after 45 minutes with no copy started (exit marker `143`). It was not a second render.

The share is mounted (`192.168.1.119:/volume1/data` on `/Volumes/data`). Existing paths stat normally, including `.../History Of Science/02_Video-Projects`. Creating `008_Lightning-Franklin` under that folder, and creating `mini-tmp-scratch/2026-10-16`, did not return within 20–25 seconds. No verified NAS mirror exists. Do not start another mkdir against this share until a create returns; a hung `mkdir` wedges later listings.

Local media is intact at `02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/code_graphics_v01/` in the History of Science checkout (untracked; mp4/mov are gitignored). A safety copy, not a NAS mirror, is at `~/_desk/j0329-code-graphics-v01/`.

Second probe, 16 Oct ~01:50 London (Cursor covering, no mkdir): `listdir` of `.../History Of Science/02_Video-Projects` did not return within 8 seconds. Local `shasum -a 256 -c SHA256SUMS.txt` is OK (11 mp4, 5 alpha mov, contact sheet, manifest, checks). PR #338 is MERGEABLE. No copy was started.

Parked for Chief: review the eleven graphics (holds in "Composite and review holds" above). The mint gate is unchanged. No files were deleted.

---

## 30 October 2026 — J1193 Multimodal Motion & VO Review (Gemini specialist, parked for Chief)

Read-only multimodal specialist review (`gemini`) of all 11 `J0329` code graphics in motion (`code_graphics_v01/*.mp4` and `.mov`), at phone scale (`360×202` and `168×94`), and in their `J1218` `rough_v02` composites (`special_assets/*.mp4` over the minted `J1191` Flow `KEEP` plates), checked word-for-word against the locked VO timestamps in `VO_RETIME_v01.json`. No re-render, no spend (`£0`), no files modified in `code_graphics_v01/`.

### 1. Ruling on the Atlantic contour (`P3:04_letter_crosses`) + sourced 1752 geometry fix

- **Does the schematic contour read as wrong to a viewer?** **YES — `FIX`.**
  1. **Unrecognisable zigzag silhouettes & wrong relative latitude/coastal placement:** The two 8-segment vertical polylines in `_build_code_graphics_v01.py` (`west=[(340,300)...(540,830)]`, `east=[(1480,310)...(1500,840)]`) read as two symmetrical vertical lightning zigzags or cliff faces rather than North America and Western Europe. Neither coastline has any recognisable geographic landmark (no Cape Cod, Long Island, Delaware/Chesapeake Bays, or Florida on the west; no Great Britain, Ireland, English Channel, Brittany, Bay of Biscay, or Iberia on the east). Furthermore, **Paris `(1360, 535)` is placed at the exact same vertical coordinate (`y=535`) as Philadelphia `(560, 535)` and directly on the Atlantic shoreline**, whereas Paris (`48.86°N, 2.35°E`) is `~8.9°` north of Philadelphia (`39.95°N, 75.16°W`) and inland up the Seine from Le Havre / the English Channel.
  2. **Collision over moving plate `P3:07_slow_news`:** When composited over `P3:07_slow_news` (the 3D sailing packet ship at sea), the vertical zigzags slice straight through the ship's hull and rigging (`x=340..600` and `x=1320..1500`).
  3. **Low-detail QA warning:** In standalone QA (`polish_gate_v01.txt`), `P3:04_letter_crosses` triggers `WARN low detail: edge density 0.0135 < film p5 0.0162`.
- **Sourced 1752 North Atlantic geometry fix:**
  Project `lat 25°N–58°N`, `lon 82°W–8°E` into `1920×1080` (`x(lon) = round(260 + (lon + 82.0) / 90.0 * 1400)`, `y(lat) = round(860 - (lat - 25.0) / 33.0 * 600)`), sourced from **Jacques-Nicolas Bellin, *Carte réduite de l'Océan Occidental* (Paris: Dépôt des Cartes et Plans de la Marine, 1742 / 1752 ed.)**, with a faint 1752 chart graticule (`30°N, 40°N, 50°N` and `75°W, 45°W, 15°W, 0°`) and dark outer casing stroke:
  - `west_coast_1752` (Newfoundland / Nova Scotia → Cape Sable → Cape Cod → Long Island → Delaware Bay / Philadelphia → Chesapeake → Cape Hatteras → Charleston → Florida):
    `[(711, 460), (620, 495), (515, 524), (470, 535), (447, 555), (415, 566), (384, 576), (366, 588), (376, 610), (353, 642), (361, 675), (320, 700), (293, 718), (282, 765), (288, 845), (265, 855)]`
  - `east_coast_1752` (Low Countries → Calais → Le Havre / Seine mouth → Cotentin → Brest / Brittany → Bay of Biscay → Cape Finisterre → Lisbon → Cape St. Vincent → Gibraltar):
    `[(1613, 342), (1564, 387), (1537, 415), (1511, 411), (1466, 435), (1500, 468), (1517, 496), (1460, 515), (1391, 535), (1394, 611), (1396, 642), (1448, 660)]`
  - `britain_1752` (closed loop: Land's End → Dover → East Anglia → Scotland → West Highlands → Wales → Land's End):
    `[(1447, 404), (1556, 385), (1562, 356), (1518, 310), (1504, 269), (1450, 287), (1472, 340), (1458, 375), (1447, 404)]`
  - `ireland_1752` (closed loop):
    `[(1385, 345), (1425, 340), (1430, 388), (1375, 395), (1385, 345)]`
  - `seine_river_1752` (Le Havre mouth to inland Paris):
    `[(1537, 415), (1554, 420), (1572, 426)]`
  - **Philadelphia marker (`39.95°N, 75.16°W`):** `(366, 588)` · **Paris marker (`48.86°N, 2.35°E`, inland):** `(1572, 426)`
  - **`route_1752` (Westerlies packet arc from Delaware Bay to Le Havre, then up the Seine to Paris):**
    `[(366, 588), (580, 515), (860, 445), (1180, 410), (1440, 412), (1537, 415), (1572, 426)]`

### 2. Ruling on label legibility at phone size (`360×202` mobile player & `168×94` preview)

- **Full-frame period-paper cards (`P2:14`, `P3:03`, `P3:15`, `P4:08`, `P5:09`, `P5:11`, plus `P5:10` on paper):**
  - The `66 pt` Didot Italic cream labels (`CREAM=(244,228,195)` at `y=150`) have strong contrast (`~6.2:1`) against the dark vignette top (`RGB ~(94,69,45)`) of the procedural period paper and read clearly at `360×202`, **with two fixes required:**
    1. **Double-label collision in assembly (`P4:08_teach_charge` and `P5:11_safe_path`):** `parts/part-04_plates_v03.json` (`08_teach_charge`) and `parts/part-05_plates_v03.json` (`11_safe_path`) still carry `side_label` (`"NO BOLT, JUST CHARGE"` and the superseded 7-word `"A SAFE PATH TO THE GROUND"`), so `_assemble_rough_v02.py` stamps a bottom gold label (`y=940`) simultaneously with the baked-in top CG header (`y=150`), violating "one label at a time" and re-introducing the 7-word label on `P5:11`. Fix: suppress `draw_side_label` on `code_graphic` rows when the CG already carries a baked-in header, and clear `11_safe_path["side_label"]` in `part-05_plates_v03.json`.
    2. **`WET TWINE` italic kerning at phone size (`P3:15_wet_dry`):** In `66 pt` Didot Italic (`index=1`), the trailing overhang of `T` in `WET` nearly touches the top bar of `T` in `TWINE` (`WETTWINE` at `360×202`). Widen word spacing (`WET  TWINE · DRY  SILK`).
    3. **Word-count check (`P2:14`, `P2:15`, `P3:15`):** All 11 labels have `≤4` actual English words (`SAME COLOUR · CROOKED LINES` = 4w, `CRACK · FIRE · SHOCK` = 3w, `WET TWINE · DRY SILK` = 4w; `MANIFEST.json` reports `label_words: 5` only because `str.split()` counts the `·` separator token).
- **Moving-plate alpha overlays (`P2:15_likeness_fire`, `P3:04_letter_crosses`, `P4:06_same_thing`, `P5:08_looking_path`, `P5:10_metal_easy`) — `FIX`:**
  - In `_build_code_graphics_v01.py` line 163, `d.text((W/2,150), label, ...)` draws un-stroked, un-shadowed cream text (`stroke_width=0`). Over bright upper areas of the moving Flow plates — `P2:12_notebook_list` (sunlit window/cuff at `y=150`, luma `210–240`), `P3:07_slow_news` (bright sunlit topsails at `y=150`, luma `205–235`), and `P1:16_question_sky` (bright cloud rim + drawn cloud overlap at `y=150–250`) — **the top label washes out and fails phone-size legibility (`360×202`)**.
  - **Fix:** Add a dark umber outline (`stroke_width=4, stroke_fill=(36, 22, 12, round(235*alpha))`) and/or a soft translucent brown parchment backing band behind `d.text(...)` and a dark casing understroke (`width+4` in `(36, 22, 12, 190)`) on all overlay ink paths.

### 3. Per-row KEEP / FIX table (tick/event timing vs locked VO words & motion)

All relative times (`+s`) are measured from each row's `part_start_s` in `VO_RETIME_v01.json`.

| Row | Film / Part (`use_s`) | Verdict | Locked VO word timings (`rel_s` from `part_start_s`) | Current graphic events & `tick_ink_s` | Required FIX / Ruling |
|---|---|---|---|---|---|
| `P2:14_likeness_pairs` | `171.85s` / P2 `64.54–69.62s` (`5.08s`) | **FIX** | `"They (+0.00s) both (+0.18s) gave (+0.42s) light (+0.68s) of (+1.02s) the (+1.26s) same (+1.38s) colour (+1.60s). They (+2.50s) both (+2.70s) moved (+2.90s) in (+3.40s) crooked (+3.62s) lines (+3.86s)."` | Divider `0–0.4s`; label `0.5–4.5s`; left crooked spark `0.60–1.15s` (tick `0.6s`, **3.0s before** `"crooked"`); right crooked bolt `2.20–2.75s` (tick `2.2s`, **0.87s before** `"crooked"`). Static `0.00 MAD` holds at `1.15–2.20s` and `2.75–5.08s` (`J1218` WARN). | Stage beat 1 (`0.4–1.8s`, tick `0.68s`) as matched blue-white glow rings on jar & cloud for `"same colour (+1.60s)"`; stage beat 2 (`2.90–4.25s`, tick `3.55s`) drawing both crooked traces on `"moved (+2.90s) in crooked (+3.62s) lines (+3.86s)"`, with travelling charge dots through `5.08s`. |
| `P2:15_likeness_fire` | `176.93s` / P2 `69.62–74.90s` (`5.28s`) | **FIX** | `"They (+0.00s) both (+0.12s) made (+0.36s) a (+0.58s) crack (+0.76s), set (+1.52s) things (+1.82s) on (+2.08s) fire (+2.26s), and (+2.96s) could (+3.14s) kill (+3.28s) animals (+3.56s)."` | Box `0.35–0.70s`; left flame `0.70–1.10s` (tick `0.7s` on `"crack"`); right roof flame `2.30–2.70s` (tick `2.3s` on `"fire"`). **No 3rd beat or tick for `"kill animals"` (`SHOCK`)**; box obscures 3D notebook/hand; un-stroked label washes out over bright window. | Add dark stroke to `CRACK · FIRE · SHOCK`; replace full-frame wireframe box over the notebook with 3 compact margin callout icons timed to `"crack"` (`0.76s`), `"fire"` (`2.26s`), and `"kill animals"` (`3.28s`, shock arc). Set `tick_ink_s: [0.76, 2.26, 3.28]`. |
| `P3:03_rod_cloud` | `213.81s` / P3 `13.36–19.86s` (`6.50s`) | **FIX** | `"If (+0.00s) lightning (+0.40s) really (+0.68s) was (+1.02s) electricity (+1.38s), the (+2.60s) rod (+2.78s) should (+2.98s) pull (+3.22s) sparks (+3.50s) out (+3.98s) of (+4.26s) a (+4.38s) passing (+4.48s) storm (+4.84s) cloud (+5.26s)."` | Tower/rod ink `0.0–1.2s` (tick `0.5s`); dotted charge stream starts at `1.50s` (tick `1.5s`, **1.28s before** `"the rod"` at `+2.78s` and **1.72s before** `"pull sparks"` at `+3.22s`); label fades out at `4.5s` before `"storm cloud (+5.26s)"`; `4.5–6.0s` near-static (`0.044 MAD`). | Ink tower + cloud on `"If lightning really was electricity"` (`0.0–1.8s`, tick `0.40s`); ink pointed iron rod upward at `2.50–3.10s` on `"the rod (+2.78s)"` (tick `2.78s`); start charge stream at `3.20–6.50s` on `"pull (+3.22s) sparks (+3.50s)"` (tick `3.50s`); shift label window to `1.2–5.2s`. |
| `P3:04_letter_crosses` | `220.31s` / P3 `19.86–23.62s` (`3.76s`) | **FIX** | `"He (+0.00s) published (+0.24s) the (+0.58s) idea (+0.80s), and (+1.16s) it (+1.68s) crossed (+1.80s) the (+2.08s) ocean (+2.38s)."` | Schematic zigzags ink `0.30–0.65s` (tick `0.3s`); dotted route starts at `0.60s` (**1.20s before** `"crossed"` at `+1.80s`) and lands Paris ring at `3.10s` (tick `3.1s`, **0.72s after** `"ocean"` ends); un-stroked label washes out over ship sails; `WARN low detail`. | Apply sourced 1752 Bellin coastline + Britain/Ireland + graticule coordinates (§1 above); add dark stroke to `PHILADELPHIA TO PARIS`; ink coastlines + Philadelphia ring `0.25–0.85s` (`tick 0.30s`), draw track across Atlantic `1.50–2.70s` on `"it (+1.68s) crossed (+1.80s) the (+2.08s) ocean (+2.38s)"` (`tick_ink_s: [0.3, 2.65]`). |
| `P3:15_wet_dry` | `279.29s` / P3 `78.84–84.14s` (`5.30s`) | **FIX** | `"Wet (+0.00s) twine (+0.10s) would (+0.70s) carry (+0.88s) electricity (+1.18s), but (+1.80s) dry (+2.62s) silk (+2.96s) would (+3.48s) not (+3.76s)."` | Twine/key/silk ink `0.0–0.8s` (tick `0.5s`); dots run `1.0–5.3s` down to `y=755` past the key (`y=625`); insulator bar inks `2.8–3.1s` (tick `2.8s` on `"dry silk"`). Rain streaks freeze after `0.75s`, causing `MAD 0.023–0.032` (`J1218` WARN); `WETTWINE` kerning tight. | Keep `tick_ink_s: [0.5, 2.8]`; animate diagonal rain streaks continuously across `0.0–5.3s`; halt charge dots at the key/knot (`y=625`) from `2.8s` onward with a blocked glow pulse at the `y=780` dry-silk barrier on `"would (+3.48s) not (+3.76s)"`; widen space in `WET  TWINE · DRY  SILK`. |
| `P4:06_same_thing` | `362.69s` / P4 `25.18–32.48s` (`7.30s`) | **FIX** | `"Lightning (+0.00s) and (+0.96s) the (+1.66s) spark (+1.76s) in (+2.20s) the (+2.46s) jar (+2.60s) were (+3.02s) the (+3.50s) same (+3.66s) thing (+3.96s). Electricity (+5.14s)."` | Divider `0.2–0.7s` (tick `0.3s`); left spark `0.5–1.2s`; right spark `0.8–1.5s`; label `ELECTRICITY` inks in at `1.20s` (**3.94s before** `"Electricity"` at `+5.14s`) and **fades out at `5.00s` (0.14s BEFORE `"Electricity"` is spoken!)**; standalone MP4 freezes `1.5–7.3s` (`0.000 MAD`). | Time `ELECTRICITY` label (with dark stroke `stroke_width=4`) to fade in at `4.80s` and hold through `7.10s` (`2.3s` hold ≤4s lock) so it lands squarely on `"Electricity (+5.14s)"`; set `tick_ink_s: [0.25, 1.76, 5.0]`; suppress duplicate `side_label` if using CG header. |
| `P4:08_teach_charge` | `373.07s` / P4 `35.56–42.66s` (`7.10s`) | **FIX** | `"The (+0.00s) kite (+0.12s) was (+0.46s) never (+0.76s) struck (+1.20s) by (+1.58s) lightning (+1.90s). If (+2.86s) it (+3.06s) had (+3.16s) been (+3.38s), Franklin (+3.78s) would (+4.42s) almost (+4.72s) certainly (+5.02s) have (+5.54s) died (+5.78s)."` | Cloud/kite/shed ink `0.0–1.2s`; label `0.6–4.4s` (tick `0.6s` on `"never"`, tick `1.8s` on `"lightning"`); tiny string dots `1.2–7.1s` (`MAD 0.036`, `5.9s` near-hold with no beat on sentence 2). `rough_v02` draws duplicate bottom `side_label` `NO BOLT, JUST CHARGE` over the key. | Suppress `side_label` on `08_teach_charge` in assembly; add dashed ghost-bolt cancellation (`×`) at `1.2–2.0s` on `"never struck by lightning"`, continuous diagonal rain streaks across `0.0–7.1s`, and a second visual pulse on the shed/key at `3.3–4.5s` (`"If it had been, Franklin..."`). Keep `tick_ink_s: [0.6, 1.8]`. |
| `P5:08_looking_path` | `474.31s` / P5 `40.30–43.46s` (`3.16s`) | **FIX** | `"It's (+0.00s) looking (+0.28s) for (+0.48s) the (+0.74s) easiest (+0.88s) path (+1.28s) to (+1.68s) the (+1.94s) ground (+2.04s)."` | Stepped leaders draw `0.2–2.6s` (ticks `0.3s` on `"looking"`, `1.4s` on `"path"` — good VO sync). **Bugs:** (1) leader branch 1 last vertex `(900,300)` shoots upward from `(1000,660)` to the tower peak; (2) alpha `.mov` bakes 2D wireframe `roof()` + `tower()` over 3D roofs of `P1:16_question_sky`; (3) un-stroked label. | Fix branch 1 final vertex so all leaders step strictly downward (`y` increasing) to the highest gable; omit `cloud()`, `roof()`, and `tower()` from the alpha `.mov` layer (keep in paper preview only); add dark stroke (`stroke_width=4`) to `EASIEST PATH DOWN`. Keep `tick_ink_s: [0.3, 1.4]`. |
| `P5:09_wood_vs_metal` | `477.47s` / P5 `43.46–50.32s` (`6.86s`) | **FIX** | `"A (+0.00s) wooden (+0.10s) roof (+0.28s) or (+0.72s) a (+1.00s) stone (+1.16s) steeple (+1.50s) is (+2.18s) a (+2.54s) terrible (+2.70s) path (+3.08s), so (+3.58s) it (+4.10s) bursts (+4.24s) into (+4.54s) flame (+4.86s) or (+5.22s) cracks (+5.48s) apart (+5.78s)."` | Roof + tower ink `0.0–1.2s` (tick `0.5s`); blue bolt hits roof `1.2–1.8s` (tick `1.8s`) with **no flame ever drawn** on `"bursts into flame (+4.24s..+4.86s)"`; radial cracks on tower grow `1.8–6.8s` (**3.68s before** `"cracks apart"` at `+5.48s`), giving `MAD 0.008–0.039` (`J1218` WARN). | Stage 4 beats to VO: (1) timber roof `0.0–0.9s` (`tick 0.28s` `"wooden roof"`); (2) stone steeple `0.9–1.9s` (`tick 1.16s` `"stone steeple"`); (3) choked current paths `2.2–3.8s` (`"terrible path"`); (4) roof flame tongues `4.2–5.1s` (`tick 4.24s` `"bursts into flame"`) + masonry fracture lines `5.2–6.5s` (`"cracks apart"`). |
| `P5:10_metal_easy` | `484.33s` / P5 `50.32–53.30s` (`2.98s`) | **FIX** | `"But (+0.00s) a (+0.32s) metal (+0.46s) rod (+0.82s) is (+1.18s) an (+1.66s) easy (+1.78s) path (+2.10s)."` | Rod inks `0.25–1.60s` (`tick 0.25s`), smooth current line + charge dots glide down `0.30–2.90s` (VO timing good). **Bug:** alpha `.mov` bakes 2D wireframe `roof()`, `tower()`, and cross-hatched wall (`x=520..1040`), blocking `P5:06_rod_fitting` and forcing `rough_v02` into 3 back-to-back full-frame paper cards (`P5:09–P5:11`). | Omit `roof()`, `tower()`, and the left wall column from the alpha `.mov` layer (keep in paper preview only) and add dark stroke (`stroke_width=4`) to `METAL CONDUCTS`, so `P5:10` composites cleanly over moving plate `P5:06_rod_fitting` between full-frame cards `P5:09` and `P5:11`. Keep `tick_ink_s: [0.25]`. |
| `P5:11_safe_path` | `487.31s` / P5 `53.30–60.28s` (`6.98s`) | **KEEP (CG) / FIX (board)** | `"So (+0.00s) the (+0.26s) lightning (+0.40s) takes (+0.72s) the (+1.04s) rod (+1.32s), round (+1.64s) the (+2.26s) outside (+2.42s) of (+2.80s) the (+2.96s) building (+3.06s), and (+3.42s) goes (+3.98s) harmlessly (+4.20s) into (+4.84s) the (+5.30s) earth (+5.50s)."` | Steeple + exterior rod ink `0.0–1.3s` (lands on `"rod"` at `+1.32s`); label `SAFE PATH DOWN` (3 words) `0.6–4.4s` (tick `0.6s`); current line + dots trace exterior rod (`1.5s`, tick 2, `"round the outside"`) to earth stake (`3.5–6.98s`, tick 3 at `3.5s`, `"and goes harmlessly into the earth"`). | **Standalone CG (`code_graphic_008_p5_11_safe_path.mp4`) is `KEEP`.** **Board/assembly fix (`J1218`):** clear `"side_label": "A SAFE PATH TO THE GROUND"` (7 words) in `parts/part-05_plates_v03.json` row `11_safe_path` so the assembler does not stamp a second 7-word label at `y=940`. |

### Summary for Chief
- **Standalone CGs:** `1 KEEP` (`P5:11_safe_path`) · `10 FIX` (`P2:14`, `P2:15`, `P3:03`, `P3:04`, `P3:15`, `P4:06`, `P4:08`, `P5:08`, `P5:09`, `P5:10`).
- **Assembly / board (`J1218` `rough_v02`):** Suppress `draw_side_label` on `code_graphic` rows with baked-in headers (`P4:08`, `P5:11`), update `part-05_plates_v03.json` `11_safe_path["side_label"]`, and use the cleaned `P5:10_metal_easy.mov` alpha over `P5:06_rod_fitting` so `P5:09–P5:11` never run two full-frame teach graphics back to back.

