# J3137 — HOS 005 Shorts s06 / s07 / s08 music repair

Zero spend. No YouTube change. The scheduled films `Sq_lV89VMUs` and `fgsR8yAHr5s` were not touched.

The old shared bed `hos005-part05-temp_score_bed_v01.mp3` is left in place. Each candidate is a new file. The picture packet MD5 of each candidate matches its locked source, so the picture was stream-copied. s06 and s07 use the voice stems saved with those cuts. s08's voice was lifted again from the locked Part 05 take with the same word indices and the same 1.11 speed; its silence map matches the locked mix (first speech at 0.845521 s).

New beds, own synthesis, in this film's `05_Music`, each with a plan JSON. Checked against the 85-bed library (84 History of Science beds plus the Jupiter archive equivalent). Highest similarity was 0.289.

| Cut | Duration | Open gate | Music | Picture | Polish |
|---|---|---|---|---|---|
| `hos_005_s06_blood_pressure_cuff_v05.mp4` | 23.1 s | PASS | PASS | PASS, 1 warn | PASS, 1 warn |
| `hos_005_s07_heart_pulse_v05.mp4` | 25.1 s | PASS | PASS | PASS, 1 warn | PASS, 1 warn |
| `hos_005_s08_capillaries_v02.mp4` | 25.17 s | FAIL | PASS | PASS, 1 warn | PASS, 1 warn |

s08's open-gate fail is the locked picture: the first cut is still at 4.50 s, the same fail as `hos_005_s08_capillaries_v01.mp4`, and the opening-frame hash is unchanged (`17160faa2f0f1717`). Loudness on s08 was brought inside the gate window. The 8–10 s blur-pad warning is also on v01. The picture was not recut.

Masters and gate logs are in the film folder `10_Shorts/J3137/` on the shared working store. This note does not approve a swap.
