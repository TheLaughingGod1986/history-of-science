# Standalone Shorts VO, weeks 1–2 (J0170, 12 Oct 2026)

One take each with `vo_take.py --text` (Ben Orbit Narrator, eleven_v3, speed 1.04), cleared by Chief's lock of the 8 scripts on J0169 (HOS PR #291). Gemini facts pass J0177: OK 27, FLAG 0 (`../SOURCES_v01.md`, "Gemini findings"). Spoken text is word for word the Chief-locked `SCRIPTS_v02.md` (HOS #180 6127927589): S1 and S4 are the v01 takes (their lines didn't change; Chief KEEP, HOS #180 6129698941), and S2 and S3 were retaken from v02 as `_vo_v02` (Chief, J0170 reopen, 12 Oct 18:10Z). Audio is on the Mini only, in this folder (`*.wav` / `*.mp3` are git-ignored).

| Short | Stem | Length | vo_check | Scribe | Mismatches | Chars |
|---|---|---|---|---|---|---|
| S1 Herschel, infrared | `hos_sa_s1_herschel_infrared_vo_v01` | 23.92 s | PASS | 98.0% | "colour" written as "color" | 288 |
| S2 Brand, phosphorus | **`hos_sa_s2_brand_phosphorus_vo_v02`** | 22.40 s | PASS | 100% | none | 268 |
| S3 Snow, the pump | **`hos_sa_s3_snow_pump_vo_v02`** | 21.60 s | PASS | 100% | none | 269 |
| S4 Curie, notebooks | `hos_sa_s4_curie_notebooks_vo_v01` | 23.92 s | PASS | 96.2% | "sixteen hundred" written as "1,600" | 306 |

1,132 characters spent; the account read 11,414 before the first take and 11,392 after the last (its counter lags). Logged in the OWB `ai_spend` ledger as `HOS:SA`.

**Length.** The test's target is 18–22 s. S1 and S4 run about 2 s over because of pauses: pauses over 0.35 s total 4.5 s (S1), 4.4 s (S2), 4.3 s (S3) and 3.1 s (S4), most of them 0.6–0.9 s. Trimming each pause to about 0.4 s at assembly (J0171), as on the 022 Shorts' `_pause_trim`, gives about 22.2 s, 20.2 s, 20.1 s and 22.8 s. Nothing is near the 40 s gate. Chief rules whether S1 and S4 at about 22–23 s stand for the test; no retake proposed.

**v02 retakes (J0170 reopen, 12 Oct 2026).** S2 and S3 v01 were recorded from `SCRIPTS_v01.md`, but the lock is v02, which softened unsourced lines (S2: "He boiled it down to a black sludge." / "a white substance"; S3: "many still blamed bad air" / "John Snow tracked where the dead had lived."). One take each with `vo_take.py --text --order 6127927589`: 537 characters, account at 9,230 after. Use the `_vo_v02` stems for S2 and S3 at assembly (J0171); the S2/S3 `_vo_v01` takes are superseded and must not be cut in. Pause trim to about 0.4 s gives about 21.0 s (S2) and 18.8 s (S3). S1/S4 length call stands (pause trim, no line cut).
