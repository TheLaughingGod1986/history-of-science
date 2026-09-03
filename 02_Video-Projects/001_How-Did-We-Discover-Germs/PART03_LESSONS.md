# Part 03 lessons — A childbirth ward, 1840s

**Date:** 2026-09-02  
**Status:** **UAT v14 — official PASS revoked** on `hos_001_part03_rough_v14.mp4`  
**Copy:** `09_Final-Export/hos_001_part03_rough_v14.mp4` (also **HOS UAT**)  
**sha256:** `a007e1330e85556ab8912f5b5a57f6bb8a69f2ba4ebdce44cb20e4071d9a8428`  
**Dur:** 71.292s · bytes 36337418 · VO 70.480s (`part03_childbirth_ward_v01` — do not remint)

Parent v13 stays on disk (`c53e9a830ac146f5dbbb32a71c7dfee1b96479a76fdf65e68fc78965e5e15983`). PASS revoked. Do not overwrite.  
**Not LOCKED.** Stop for UAT. Do not ping Ben. Do not start Part 05.

**Ship gate (film-wide):** continuity is **all four parts of this film**, not 03 only. Every two-doctor plate = KEEP **0:48** `07_mocked_v12` (mustache younger, grey 1840s beard older, matching dark frocks, finished faces, 1840s wood ward). **Finish 03 v14 first.** Do not remint 01 / 02 / 04 unless CoS sends a UAT FAIL with stills. No top-hat twins. No new hallway pair. No hats.

## Ship gate — doctor continuity (Ben 2 Sep 2026)

Every two-doctor plate in **Parts 01–04** must be **THE SAME two men** as KEEP **0:48** `07_mocked_v12`.

- Younger: dark hair + **mustache** (Semmelweis). Older: grey **1840s** hair + beard.
- Matching dark frocks. Finished faces.
- **Same 1840s wood ward style as 0:48** — not a different hospital.
- Living. Flow **Veo 3.1 Fast** only.
- **Forbidden:** new pair · powdered wig · cheap leftover faces · clean-shaven younger · crossed-arms leftover pair · matching top-hat twins · grand hallway pair · flask ghost on the doctors.

Finish 03 v14 first. Remint a locked part (01 / 02 / 04) only when CoS sends a **UAT FAIL with stills**. Rule: `.cursor/rules/hos-part03-doctor-continuity.mdc`.

Superseded locks: v08 (`LOCKED_v08`) · v11 (PASS lifted for VECTOR era mix). Do not overwrite those files.

## Style parent

Match Part 01 **v21** bible + Part 02 **v12**. Animistry 3D cartoon · faceless germs · Explorer garnish once · continuous motion · no Ken Burns.

## What shipped in v14 (UAT — not locked)

| Plate | Call |
|---|---|
| 01–03, 05–06, 08, 10 | KEEP from the v11/v08 set. Explorer 06 HOLDS (profile walk, garnish). |
| 04_autopsy_to_ward | **v14 remint** Fast T2V — same 0:48 VECTOR pair walking the wood ward. Replaced HITCHHIKER top-hat twins in a grand hallway. |
| 07_mocked | **v12 KEEP** — locked VECTOR two-shot at 0:48. Younger dark-hair mustache at the stone basin; older grey 1840s hair + beard; finished faces; beds/nurses moving. |
| 09_they_still_sneer | **v14 remint** Fast T2V — same two faces as 0:48. Replaced v13 leftover-stout read. |
| 10_flask_in_the_room | KEEP (flask only, no doctors). **Hard-cut** after 09 at 64.30s — do not xfade a flask ghost onto the doctors. |

Engine: Flow **Veo 3.1 Fast**. I2V start-frame path is dead on this machine — Fast T2V only if a remint is ever asked. Create / Add to Prompt / `arrow_forward` dies → **STOP**.

## VECTOR doctor identity (film-wide lock)

- Younger / Semmelweis: dark swept hair, **mustache stays**, at stone basin, finished face.
- Older colleague: grey/white **1840s** hair + beard, dark frock, white cuffs. Same man as 0:49 — not a new professor.
- **Forbidden:** powdered wig, 1700s silhouette, mannequin heads, Explorer on doctor plates, clean-shaven younger on 09, crossed-arms leftover pair.

v11 FAIL at ~0:49: dark-hair mustache washer vs 18th-c powdered wig walking away.  
v12 FAIL at ~1:00: different pair, arms crossed, younger no mustache, older heavier new face (`09_they_still_sneer_v05`). Prompt still said CLEAN-SHAVEN. ~1:04 backs were that leftover pair into the flask xfade.

## Labels (HOLD — `_build_part03_rough_v02.py`)

- Chapter “A childbirth ward, 1840s” 1.50–5.00 left
- LIVING SEEDS 10.86–15.06
- HITCHHIKER 23.97–28.17
- SEMMELWEIS 26.54–28.15 hallway only (off before wash at 28.40)
- HANDWASHING 34.78–35.70
- THE VECTOR 44.82–49.02
- A FLASK 68.41–71.08

## What failed (do not repeat)

| Fail | Why |
|---|---|
| v11 VECTOR two-shot era mix | Powdered wig vs 1840s washer. Same plate, two centuries. |
| v12 later-doctor identity | 09 leftover pair at ~0:58–1:02: stout bearded bowtie + clean-shaven widow’s peak, arms crossed. Official UAT FAIL. Recut 09 to the 0:49 pair. |
| v13 flask ghost | 09→10 xfade stamped a swan-neck flask on the doctors at ~1:04. Hard-cut that join. Do not nest a flask on the pair. |
| v13 HITCHHIKER pair | Official UAT FAIL stills **~0:22–0:28**: matching top-hat twins, grand hallway (`04_autopsy_to_ward_v01`). Reminted in v14. Do not remint 04 again. |
| Empty-ward Ken Burns | Unique occupied still per plate. |
| Explorer presenting | Profile walk only. |
| I2V start-frame loop | Dead on this machine. Fast T2V if ever reminted. |
| Create / Add to Prompt credit-burn | One Create. If it dies, STOP. |

## Copy forward

1. One minute only. Fast T2V. If Create dies: **STOP**.
2. Explorer once, garnish — never presenting.
3. Unique motion per plate. Mute test: picture names the VO line.
4. Faceless germs only when the line needs them.
5. Two scientists on VECTOR = same 1840s wardrobe and hair era. Never a powdered wig.
6. **Ship gate (film-wide):** every two-doctor plate in Parts 01–04 = the same two men **and** the same 1840s wood ward as 0:48. Mustache stays. Older stays grey 1840s beard. No new pair. No wig. No top-hat twins. No cheap leftover faces. Do not write CLEAN-SHAVEN into 09. Finish 03 v14 first. Do not remint 01 / 02 / 04 unless CoS FAIL + stills.

## Next

**STOP for UAT on v14.** Not locked. Continuity = all four parts; finish 03 v14 first. Do not remint 01 / 02 / 04 unless CoS sends a UAT FAIL with stills. Part 04 stays official PASS on v19. 05 parked. Do not ping Ben.
