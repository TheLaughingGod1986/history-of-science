# 013 take-3 retake board v02: Darwin & Wallace

**Written 25 Nov 2026 (`J3757`). Spend: `£0` / `0` Flow credits. Nothing minted, no browser opened. `generation_authorized` is `false` on both rows. Parked for the Chief's price PASS and mint GO.**

Covers only the 2 rows the acting Chief ruled RETAKE again after take 2 (`J3747`): rows `49` and `63`. Both failed because the take-1 start still already held the fault, so each row gets a **fresh start still** (take 3, Flow Nano Banana 2, 0 credits) and a new video prompt.

Not read or changed: `REVIEW_STATE.json`, `archive_v01_pass1/`, `archive_v01_retake1/`, the 10 capability-held rows (`56-62, 64-66`, `J3178`), the 6 clean take-2 rows (`3, 10, 24, 28, 47, 54`), `J2529`.

Built by `_build_retake_board_v02.py`. Machine copy: `RETAKE_BOARD_v02.json`.

## 1. Price

Flow balance: **22,650 credits** (after J3747 (25 Nov 2026), from the job brief; this job did not open Flow). The mint job reads the live balance before any Create. Headroom floor: 3,000.

| Option | Models | Stills | First try | Expected (2.59x) | Balance after first try | Balance after expected | Clears floor |
|---|---|---:|---:|---:|---:|---:|---|
| **A: before 5 Dec** | 2 x Nano Banana 2 still + 2 x Veo 3.1 - Quality, 8 s | 0 | 200 | 518 | 22,450 | 22,132 | yes |
| **B1: after 5 Dec, Lite** | 2 x Nano Banana 2 still + 2 x Veo 3.1 - Lite | 0 | 10 | 26 | 22,640 | 22,624 | yes |
| **B2: after 5 Dec, Omni** | 2 x Nano Banana 2 still + 2 x Omni 1.2 Flash, 8 s | 0 | 48 | 124 | 22,602 | 22,526 | yes |

- **A: before 5 Dec:** Same model as the 48 KEEP plates and the 6 clean take-2 plates. No new-model style UAT. Must be minted before 5 Dec 2026.
- **B1: after 5 Dec, Lite:** Needs a first-use style UAT against the KEEP plates in parts 04 and 06. Retry rate for Lite is not measured; 2.59x is the Quality figure.
- **B2: after 5 Dec, Omni:** 720p. Needs a first-use style UAT. Retry rate not measured.

**Recommendation (worker advice, the Chief decides):** A. 200 credits is under 1% of the balance, it keeps one look per part and it needs no new-model UAT. It only exists until 5 Dec 2026. Worker advice; the Chief decides.

## 2. Mint order

- 1. Mint each take-3 still (0 credits) and check it against accept_before_video.
- 2. Only from an accepted still, mint the take-3 clip.
- 3. Take-3 clips go to the Chief's review; keep is not set by the mint job.

## 3. Prompt checks

- Real person names in the 4 take-3 prompts: **0** (checked by the builder).
- Forbidden terms (`same DNA`, `lab DNA`, Ken Burns, photoreal, retired Omni): **0**.
- Each prompt's sha256 is pinned in the builder; `--check` fails on an unpinned edit.
- The take-1 start stills are marked `reuse: false`.

## Row 49 · `P4:12_lyell_hooker_bundle` · take 3

Film window 360.98-366.34 s, uses 5.36 s of an 8 s clip.

- **Take-2 fault:** At 2.0-2.5 s the left gentleman hands the brown tied bundle to the top-hatted gentleman, who already carries a light ribbon-tied parcel under his left arm. At 3.0-5.5 s (inside the used 0.00-5.36 s) the light parcel merges into one shrinking brown bundle; at 6.0-7.0 s the light parcel is back and the brown bundle is gone (acting Chief, J3747).
- **Cause:** The take-1 start still already shows two bulky separate bundles (one under an arm, one thick stack on the step). With one carrier on the steps, the model dissolves one of them.
- **Fix:** Fresh start still with exactly one tied bundle, already in one gentleman's hands. No hand-off, nothing put down, nothing on the steps. The other gentleman walks beside him with empty hands.
- **Accept the still only if:** exactly one bundle, two gentlemen, nothing on the steps.

Start-still prompt (`b08b71a86a2e`):

```
Premium Animistry-class 3D cartoon. In London daylight, two Victorian gentlemen in dark frock coats and top hats stand side by side at the foot of wide pale stone steps, seen from the side. The nearer gentleman holds exactly one thick bundle of cream manuscript pages, tied once with a dark ribbon, in both hands against his chest. The other gentleman's hands are empty at his sides. There is exactly one bundle in the picture. Nothing else is carried, and nothing lies on the steps or the ground. Soft overcast daylight, matte painted stone. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. No Explorer. No Orbit.
```

Video prompt (`b80f34a68cad`):

```
Premium Animistry-class 3D cartoon. In London daylight, two Victorian gentlemen climb wide pale stone steps side by side at a calm walking pace. One gentleman carries exactly one ribbon-tied manuscript bundle in both hands against his chest for the whole clip. The other gentleman walks beside him with empty hands. The bundle is never handed over, never put down and never splits, and it keeps the same size, colour and shape. No second parcel appears at any time. The stone steps stay fixed. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```

## Row 63 · `P6:06a_origin_fifth_edition` · take 3

Film window 485.64-490.60 s, uses 4.96 s of an 8 s clip.

- **Take-2 fault:** Bright golden light comes out of the inside of the green book at 0.0-2.0 s (inside the used 0.00-4.96 s), against the no-glow rule. The front cover is jaggedly cracked across the middle (0.0-2.0 s) and morphs flat into green pages (2.5-3.5 s). The folded letter curls into the air and flips itself (4.0-4.5 s) (acting Chief, J3747).
- **Cause:** The take-1 start still itself has the cracked green cover and a warm yellow-orange light inside the open pages, so any clip started from it fails at 0.0 s.
- **Fix:** Mandatory fresh start still: the book closed, whole and flat, lit only by cool grey window light, so there is no open gutter for light to come from at frame 0. In the clip one hand lays the cover open; the letter and the spectacles do not move.
- **Accept the still only if:** book closed and whole, no crack, no warm or gold light, letter and spectacles flat on the desk.
- **Alternative:** If the Chief would sooner have no hand in frame: the same still with the book already open flat at its first pages, and a slow push-in with one page settling. Not written up here; it puts an open gutter in frame 0, which is where both earlier takes went gold.

Start-still prompt (`331f7c47ab5a`):

```
Premium Animistry-class 3D cartoon. Close on a mahogany desk beside a window, lit only by cool grey overcast window light from the left side. A green cloth-bound book lies closed and flat on the desk. Its cover is whole, smooth and undamaged, with no crack, tear or crease. Beside the book one folded handwritten letter lies flat on the desk, with ink scribble lines only. A pair of round wire spectacles rests on the desk next to the letter. Matte cream page edges, neutral grey-beige shadows. No warm, yellow, gold or orange light anywhere, and no light comes from inside the book. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. No Explorer. No Orbit.
```

Video prompt (`2ff63983f809`):

```
Premium Animistry-class 3D cartoon. Close in cool grey window light on a mahogany desk. One sleeved hand slowly lifts the front cover of the green cloth-bound book by its edge and lays it open flat on the desk. The cover stays whole, smooth and green, and it hinges at the spine like a real book. The pages inside are matte cream paper with ink scribble lines, lit only by the grey window from one side, and the gutter between the pages stays in soft neutral shadow. No warm, yellow or gold light at any time. The folded letter stays flat on the desk and the spectacles stay where they are for the whole clip. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```
