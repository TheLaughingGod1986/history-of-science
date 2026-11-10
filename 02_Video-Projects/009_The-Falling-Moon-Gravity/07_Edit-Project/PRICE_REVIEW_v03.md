# 009 price review v03

Cursor, 15 Oct 2026, J0333. Boards only. **No mint. No spend. No merge.**
v02 (PR #331, 38bb802) stands on conditions 1, 3 and 4. This pass fixes condition 2
(Chief, desk #180 6202998478) and splits the mint into two tranches
(Chief, desk #180 6202968147). That split supersedes the whole-and-last line in 6202998478. Parked for Chief.

## Readings

- Flow: **23740** credits at 2026-10-15T21:42:22Z (the v02 read, CDP :9222). Not re-read. Nothing spent.
- Vertex promo: **£71.02** at 2026-10-15T07:30:31Z. Usable **£70.02** after the £1 margin. The route stays Flow-first.

## Rates

Same rates as v01 and v02. Expected credits are `ceil(try-1 × takes per keep)`.

| Model | Try-1 | Takes per keep | Expected per row |
|---|---:|---:|---:|
| Quality | 100 | 2.59 (70/27) | 259 |
| Fast | 10 | 1.96 (94/48) | 20 |

Vertex, if it were the route: Quality £0.16/s, Fast £0.08/s (USD 0.20 and 0.10 at 0.80 GBP), clip lengths 4/6/8 s, plus stills. It does not fit.

## Totals

v02 was 90 rows, 52 Quality / 19 Fast / 12 code / 6 edit-hold / 1 other reuse, Flow expected 13,848.
v03 adds six Fast mints and clears the six edit-holds. Row count stays 90.

| | rows | Quality | Fast | code | edit-hold | other reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | 14 | 6 | 8 | 0 | 0 | 0 | 680 | 1714 | £11.04 | £26.51 |
| Part 02 | 18 | 16 | 0 | 2 | 0 | 0 | 1600 | 4144 | £16.32 | £43.45 |
| Part 03 | 15 | 6 | 5 | 4 | 0 | 0 | 650 | 1654 | £9.44 | £23.35 |
| Part 04 | 22 | 10 | 7 | 5 | 0 | 0 | 1070 | 2730 | £15.84 | £39.76 |
| Part 05 | 21 | 14 | 5 | 1 | 0 | 1 | 1450 | 3726 | £18.72 | £47.98 |
| **Film** | **90** | **52** | **25** | **12** | **0** | **1** | **5450** | **13968** | **£71.36** | **£181.05** |

All on Flow, as one block: **13968** expected against 23740 left. That is 9772 before 007 and 008, so 009 does not mint as one block.
All on Vertex: DOES NOT FIT (£181.05 expected vs £70.02 usable).

## Mint order

006 needs 0 Flow. Then 007, then 008, then 009 in two tranches. Every mint job reads Flow live first and stops if the read after its spend would drop below 3,000. If 007 or 008 overrun, tranche 1 shrinks from the latest Quality parent still in it, and that row moves to tranche 2. The six Fast mints below stay in tranche 1 until every Quality parent has moved. No top-up.

On this reading the cap for tranche 1 is 23740 − 7550 − 5605 − 3000 = **7585**.

## 1. Parchment teach → £0 code graphics

Unchanged from v02. Twelve rows. Flow and Vertex are 0. They sit in neither tranche.

## 2. Six Fast continuations → own Fast mints

Each parent is an 8.00 s clip (7.90 s usable) and is short of the next beat, so an edit-hold would leave a picture hole. v03 mints each beat on its own, Fast, with a new angle or move and the parent's look. Try-1 is 10, expected is 20, each.

| Row | Needed s | Parent | Shortfall s | Try-1 | Expected | Tranche |
|---|---:|---|---:|---:|---:|---:|
| P1:03_table_three_c1 | 7.00 | P1:03_table_three | 6.10 | 10 | 20 | 1 |
| P1:03_table_three_c2 | 7.00 | P1:03_table_three | 6.10 | 10 | 20 | 1 |
| P3:09_can_he_calculate_c1 | 6.10 | P3:09_can_he_calculate | 4.30 | 10 | 20 | 1 |
| P4:06_pretty_nearly_c1 | 7.03 | P4:06_pretty_nearly | 6.16 | 10 | 20 | 1 |
| P4:10_write_it_down_c1 | 5.34 | P4:10_write_it_down | 2.78 | 10 | 20 | 1 |
| P5:03_halley_comet_path_c1 | 5.98 | P5:03_halley_comet_path | 4.06 | 10 | 20 | 1 |

Distinct beats:

- P1:03_table_three_c1: From table height the camera tracks along the wood. The green apple with a red flush is already set, a small brass cannon is turned so its mouth points along the table, and a sheet of unreadable scribbles is laid between them. Grey window light. The marks are scribbles, not numbers.
- P1:03_table_three_c2: The camera rises off the same wooden table toward the grey window. The green apple, the brass cannon and the sheet of scribbles stay in frame below, still in grey window light, with a plain pale wall beyond the window.
- P3:09_can_he_calculate_c1: A side angle on the same table. The pen lowers toward the paper and stops just above it, beside the apple. Seen from the side of the hand, no readable face, grey window light only.
- P4:06_pretty_nearly_c1: From the left side of the desk, a hand lifts one corner of the same page. Two short columns of unreadable marks still end level with each other. Window light, no digits.
- P4:10_write_it_down_c1: A side view of the same desk. Another closed stack of pages is set down beside the man, who is still seen from behind. Window light only. No readable face.
- P5:03_halley_comet_path_c1: The same painted-parchment card, camera tilting along the long ink ellipse. The small ink marker steps from the far side of the loop toward the near side. Matte ink only, no digits, no tail.

Six rows, Flow try-1 **60**, expected **120**.

## 3. Quality continuations stay second Quality mints

Unchanged from v02. The parent clip cannot cover any of them. The split note said 22; the v02 condition-3 table has **24** rows, and all 24 stay Quality mints here (including `02_spray_paint_c1` and `_c2`, whose parent is now Fast and still cannot cover them).

## 4. Quality → Fast

Unchanged from v02: P1:10_farmhouse_dawn, P3:02_cannon_world, P4:02_spray_paint, P5:01_one_law, P5:08_cup_and_planets, P5:12_clay_handoff.

## Tranches

| | Rows | Quality | Fast | Flow try-1 | Flow expected |
|---|---:|---:|---:|---:|---:|
| Tranche 1, now-ish, after 007 and 008 | 52 | 27 | 25 | 2950 | 7493 |
| Tranche 2, after the ~12 Nov renewal | 25 | 25 | 0 | 2500 | 6475 |
| **009** | **77** | **52** | **25** | **5450** | **13968** |

After 007 (~7550), 008 (5605) and tranche 1 (7493) the reading would show **3092** left, against the 3,000 floor.

Tranche 1 is the parents and the Fast plates, including the six new Fast mints, minus the Quality parents that did not fit:

P5:10_explorer_bench.

Those moved rows mint at the start of tranche 2, before any continuation of the same plate.

Tranche 2 is those moved rows plus the 24 second-Quality continuations. Confirm the renewal with a live read before it starts. 009 picture is due Sun 15 Nov.

## If tranche 2 slips past ~13 Nov

These continuation beats would have to sit as an edit-hold of the parent. The parent clip cannot cover them, so the picture on that beat would be shorter than the VO. A picture hole is not allowed while the row is still a planned mint; this list is the hole if the renewal slips.

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
| P4:02_spray_paint_c1 | 6.96 | P4:02_spray_paint | 6.01 | 259 |
| P4:02_spray_paint_c2 | 6.95 | P4:02_spray_paint | 6.00 | 259 |
| P4:05_minute_second_c1 | 6.76 | P4:05_minute_second | 5.61 | 259 |
| P4:05_minute_second_c2 | 6.75 | P4:05_minute_second | 5.60 | 259 |
| P4:08_halley_visit_c1 | 5.88 | P4:08_halley_visit | 3.86 | 259 |
| P4:08_halley_visit_c2 | 5.88 | P4:08_halley_visit | 3.86 | 259 |
| P5:01_one_law_c1 | 4.45 | P5:01_one_law | 1.00 | 259 |
| P5:04_comet_1758_c1 | 4.49 | P5:04_comet_1758 | 1.08 | 259 |
| P5:05_iss_orbit_c1 | 7.70 | P5:05_iss_orbit | 7.51 | 259 |
| P5:05_iss_orbit_c2 | 7.71 | P5:05_iss_orbit | 7.52 | 259 |
| P5:06_iss_apple_c1 | 4.59 | P5:06_iss_apple | 1.28 | 259 |
| P5:08_cup_and_planets_c1 | 6.56 | P5:08_cup_and_planets | 5.21 | 259 |
| P5:08_cup_and_planets_c2 | 6.55 | P5:08_cup_and_planets | 5.20 | 259 |
| P5:12_clay_handoff_c1 | 6.19 | P5:12_clay_handoff | 4.48 | 259 |

Quality parents moved into tranche 2 have no earlier clip to hold. Until tranche 2 mints them, that beat has no plate:

- P5:10_explorer_bench

## For the Chief

No mint in this pass. PR #331 stays open. Vertex does not fit. Flow fits only as the split above.

The one Quality parent that does not fit tranche 1 is the latest one, P5:10_explorer_bench (the closer: "It is falling towards you, right now."). It waits for tranche 2. Chief can name a different Quality parent to wait instead. The six Fast mints stay in tranche 1.

