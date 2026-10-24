# 009 price review v04

Cursor, 15 Oct 2026, J0335. Boards only. **No mint. No spend. No merge.**
v03 (PR #331, a27348b) stands on the six J0333 Fast mints, the parchment code graphics,
and the 24-row continuation count. This pass applies the Chief FIX on J0333
(desk #180, 15 Oct ~23:10 London). Parked for Chief.

## Readings

- Flow: **23740** credits at 2026-10-15T21:42:22Z (the v02 read, CDP :9222). Not re-read. Nothing spent.
- Vertex promo: **£71.02** at 2026-10-15T07:30:31Z. Usable **£70.02** after the £1 margin. The route stays Flow-first.

## Rates

Same rates as v01, v02 and v03. Expected credits are `ceil(try-1 × takes per keep)`.

| Model | Try-1 | Takes per keep | Expected per row |
|---|---:|---:|---:|
| Quality | 100 | 2.59 (70/27) | 259 |
| Fast | 10 | 1.96 (94/48) | 20 |

Vertex, if it were the route: Quality £0.16/s, Fast £0.08/s (USD 0.20 and 0.10 at 0.80 GBP), clip lengths 4/6/8 s, plus stills. It does not fit.

## Totals

v03 was 90 rows, 52 Quality / 25 Fast / 12 code / 0 edit-hold / 1 other reuse, Flow expected 13,968.
v04 turns six Quality continuations into Fast mints. Row count stays 90.

| | rows | Quality | Fast | code | edit-hold | other reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | 14 | 6 | 8 | 0 | 0 | 0 | 680 | 1714 | £11.04 | £26.51 |
| Part 02 | 18 | 16 | 0 | 2 | 0 | 0 | 1600 | 4144 | £16.32 | £43.45 |
| Part 03 | 15 | 6 | 5 | 4 | 0 | 0 | 650 | 1654 | £9.44 | £23.35 |
| Part 04 | 22 | 8 | 9 | 5 | 0 | 0 | 890 | 2252 | £14.56 | £35.64 |
| Part 05 | 21 | 10 | 9 | 1 | 0 | 1 | 1090 | 2770 | £16.32 | £40.25 |
| **Film** | **90** | **46** | **31** | **12** | **0** | **1** | **4910** | **12534** | **£67.68** | **£169.20** |

All on Flow, as one block: **12534** expected against 23740 left. That is 11206 before 007 and 008, so 009 does not mint as one block.
All on Vertex: DOES NOT FIT (£169.20 expected vs £70.02 usable).

## Mint order

006 needs 0 Flow. Then 007, then 008, then 009 in two tranches. Every mint job reads Flow live first and stops if the read after its spend would drop below 3,000. If 007 or 008 overrun, tranche 1 shrinks from the latest Quality parent still in it, other than the closer, and that row moves to tranche 2. Fast mints stay in tranche 1 until every other Quality parent has moved. No top-up.

On this reading the cap for tranche 1 is 23740 − 7550 − 5605 − 3000 = **7585**.

## 1. Parchment teach → £0 code graphics

Unchanged from v03. Twelve rows. Flow and Vertex are 0. They sit in neither tranche.

## 2. Six J0333 Fast mints

Unchanged. Each stays its own Fast mint in tranche 1, expected 20.

## 2b. Six Fast-parent continuations → own Fast mints

Each parent is already Fast. v03 still priced the continuation as a second Quality mint, which would jump look at the cut. v04 mints each beat on its own, Fast, with a new angle or move and the parent's look. Try-1 is 10, expected is 20, each. All six move into tranche 1.

| Row | Needed s | Parent | Shortfall s | Try-1 | Expected | Tranche |
|---|---:|---|---:|---:|---:|---:|
| P4:02_spray_paint_c1 | 6.96 | P4:02_spray_paint | 6.01 | 10 | 20 | 1 |
| P4:02_spray_paint_c2 | 6.95 | P4:02_spray_paint | 6.00 | 10 | 20 | 1 |
| P5:01_one_law_c1 | 4.45 | P5:01_one_law | 1.00 | 10 | 20 | 1 |
| P5:08_cup_and_planets_c1 | 6.56 | P5:08_cup_and_planets | 5.21 | 10 | 20 | 1 |
| P5:08_cup_and_planets_c2 | 6.55 | P5:08_cup_and_planets | 5.20 | 10 | 20 | 1 |
| P5:12_clay_handoff_c1 | 6.19 | P5:12_clay_handoff | 4.48 | 10 | 20 | 1 |

Distinct beats:

- P4:02_spray_paint_c1: From the side of the same pale plaster wall, the hand steps back. Daylight. The small dark spot of paint spreads into a wider, paler patch as the hand moves away. The hand and the wall only, no face.
- P4:02_spray_paint_c2: The camera drops to the height of the pale plaster wall and tracks along the edge of the wider pale patch. The same hand finishes and lowers. Daylight. The hand and the wall only, no face.
- P5:01_one_law_c1: The camera tilts across the same painted card, from the painted Sun out along one matte ink line to a planet, then on toward Jupiter and its moons. Matte ink only. Daylight on the card.
- P5:08_cup_and_planets_c1: A side angle on the same wooden table. The cup is already past the edge and falling, while the matte painted card of planets on ink curves stays on the wall behind. Daylight.
- P5:08_cup_and_planets_c2: From the floor, the camera rises off the fallen cup toward the same painted card. The painted Sun and the ink curves fill the frame. Daylight on the table and the card.
- P5:12_clay_handoff_c1: The camera tracks along the rock face in bright daytime. The same thin pale band of clay runs across the stone, and above the rock the small pale stone is already crossing the blue sky. No impact, no fire, no creatures hurt.

Six rows, Flow try-1 **60**, expected **120**.

## 3. Remaining Quality continuations

Eighteen of the v03 condition-3 rows stay second Quality mints. Their parents are still Quality, and the parent clip cannot cover them. They stay in tranche 2. The other six are the Fast-parent rows in section 2b.

## 4. Quality → Fast parents

Unchanged from v02: P1:10_farmhouse_dawn, P3:02_cannon_world, P4:02_spray_paint, P5:01_one_law, P5:08_cup_and_planets, P5:12_clay_handoff.

## Tranches

| | Rows | Quality | Fast | Flow try-1 | Flow expected |
|---|---:|---:|---:|---:|---:|
| Tranche 1, now-ish, after 007 and 008 | 57 | 26 | 31 | 2910 | 7354 |
| Tranche 2, after the ~12 Nov renewal | 20 | 20 | 0 | 2000 | 5180 |
| **009** | **77** | **46** | **31** | **4910** | **12534** |

After 007 (~7550), 008 (5605) and tranche 1 (7354) the reading would show **3231** left, against the 3,000 floor. Cap on this reading is 7585.

Tranche 1 is the parents and the Fast plates, including the six J0333 Fast mints, the six new Fast mints, and the closer:

- P5:10_explorer_bench ("It is falling towards you, right now.").

Deferred to tranche 2 instead, so the closer is not the row that waits:

- P2:10_how_high, P3:07_ball_to_moon.

Those two mint at the start of tranche 2, before any continuation. Tranche 2 is the 18 remaining second-Quality continuations plus these two parents. Confirm the renewal with a live read before it starts. 009 picture is due Sun 15 Nov.

## If tranche 2 slips past ~13 Nov

These 18 continuation beats would have to sit as an edit-hold of the parent. The parent clip cannot cover them, so the picture on that beat would be shorter than the VO. A picture hole is not allowed while the row is still a planned mint; this list is the hole if the renewal slips.

| Beat | Needed s | Parent | Shortfall s | Expected credits |
|---|---:|---|---:|---:|
| P1:05_heavens_map_c1 | 4.58 | P1:05_heavens_map | 1.26 | 259 |
| P1:07_night_field_c1 | 4.65 | P1:07_night_field | 1.40 | 259 |
| P2:01_cambridge_closes_c1 | 4.19 | P2:01_cambridge_closes | 0.48 | 259 |
| P2:03_christmas_birth_c1 | 5.02 | P2:03_christmas_birth | 2.14 | 259 |
| P2:05_working_alone_c1 | 5.16 | P2:05_working_alone | 2.42 | 259 |
| P2:08_the_apple_c1 | 4.99 | P2:08_the_apple | 2.08 | 259 |
| P2:11_explorer_apple_c1 | 4.94 | P2:11_explorer_apple | 1.98 | 259 |
| P3:01_really_falling_c1 | 5.26 | P3:01_really_falling | 2.62 | 259 |
| P3:05_shot_orbit_c1 | 6.42 | P3:05_shot_orbit | 4.94 | 259 |
| P3:05_shot_orbit_c2 | 6.42 | P3:05_shot_orbit | 4.94 | 259 |
| P4:05_minute_second_c1 | 6.76 | P4:05_minute_second | 5.61 | 259 |
| P4:05_minute_second_c2 | 6.75 | P4:05_minute_second | 5.60 | 259 |
| P4:08_halley_visit_c1 | 5.88 | P4:08_halley_visit | 3.86 | 259 |
| P4:08_halley_visit_c2 | 5.88 | P4:08_halley_visit | 3.86 | 259 |
| P5:04_comet_1758_c1 | 4.49 | P5:04_comet_1758 | 1.08 | 259 |
| P5:05_iss_orbit_c1 | 7.70 | P5:05_iss_orbit | 7.51 | 259 |
| P5:05_iss_orbit_c2 | 7.71 | P5:05_iss_orbit | 7.52 | 259 |
| P5:06_iss_apple_c1 | 4.59 | P5:06_iss_apple | 1.28 | 259 |

The two deferred Quality parents do not leave a hole. Their slip fallback is a £0 hold or extension of the neighbouring code graphic:

| Deferred parent | Needed s | Fallback |
|---|---:|---|
| P2:10_how_high | 2.58 | £0 hold or extension of P2:09_pull_heights |
| P3:07_ball_to_moon | 2.84 | £0 hold or extension of P3:06_orbit_teach and P3:08_km_a_second |

## For the Chief

No mint in this pass. PR #331 stays open. Vertex does not fit. Flow fits only as the split above.

Tranche 1 is 26 Quality + 31 Fast = 7,354, under the 7,585 cap, with 3,231 left after 007, 008 and tranche 1. Tranche 2 is 18 continuations + 2 deferred parents = 20 Quality = 5,180. The film is 46 Quality + 31 Fast = 12,534.

The closer is back in tranche 1. Chief can still name a different pair to wait. Fast mints stay in tranche 1.

