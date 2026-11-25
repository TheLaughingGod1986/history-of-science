# 013 retake prompt and price board v01: Darwin & Wallace

**Written 25 Nov 2026 (`J3738`). Spend: `£0` / `0` Flow credits. Nothing minted. `generation_authorized` is `false` on every row. Parked for the Chief's price PASS and mint GO.**

Covers only the 8 pass-1 rows the Chief ruled RETAKE in `J2529` (rows `3, 10, 24, 28, 47, 49, 54, 63`). The 10 capability-held rows (`56-62, 64-66`) stay with `J3178`; this board does not read or change their marks.

Built by `_build_retake_board_v01.py` from the v02 plate boards and the J2529 receipts. Machine copy: `RETAKE_BOARD_v01.json`.

## 1. Price

Flow balance: **23,450 credits** (daily reading 2026-11-24T08:30:22Z, from the spend ledger; this job did not open Flow). The mint job reads the live balance before any Create. Headroom floor: 3,000.

| Option | Models | First try | Expected (2.59x) | Balance after first try | Balance after expected | Clears floor |
|---|---|---:|---:|---:|---:|---|
| **A: before 5 Dec** | 8 x Veo 3.1 - Quality, 8 s | 800 | 2,072 | 22,650 | 21,378 | yes |
| **B: after 5 Dec, mixed** | 6 x Veo 3.1 - Lite + 2 x Omni 1.2 Flash (rows 10, 24), 8 s | 78 | 202 | 23,372 | 23,248 | yes |
| **C: after 5 Dec, all Omni** | 8 x Omni 1.2 Flash, 8 s | 192 | 497 | 23,258 | 22,953 | yes |

- **A: before 5 Dec:** Same model as the 48 KEEP plates and the same start stills. Must be minted before 5 Dec 2026.
- **B: after 5 Dec, mixed:** Needs a first-use style UAT for each new model against the KEEP plates in the same part. Omni is 720p. Retry rate for these models is not measured; 2.59x is the Quality figure.
- **C: after 5 Dec, all Omni:** One new model instead of two. 720p. First-use style UAT still needed.

**Recommendation (worker advice, the Chief decides):** A. 800 credits is 3.4% of the balance, it keeps one look per part, and it needs no new-model UAT. It only exists until 5 Dec 2026. Worker advice; the Chief decides.

**Hold gap:** the recorded retake hold is 700 credits for 7 rows. Row 63 joined the list without raising it. Option A needs 800, so the Chief raises the hold by 100.

**Rows 24, 47 and 49:** the Chief's rulings said "same locked prompt". Each row below carries both the locked prompt and the retake prompt (locked prompt plus one fix sentence), so the Chief can pick either at the price PASS.

## 2. Prompt checks

- Real person names in any prompt: **0** (checked by the builder on all 16 prompts).
- Forbidden terms (`same DNA`, `lab DNA`, Ken Burns, photoreal, retired Omni): **0**.
- Every retake prompt keeps its locked v02 prompt whole, word for word, and adds one sentence.
- Every take-1 prompt hash in the J2529 receipts matches the locked v02 prompt.
- Start still: the same pinned still as take 1 (path and sha256 in the JSON).

## 3. Rows

| # | Row | Film window | Use | Before 5 Dec | After 5 Dec (option B) |
|---:|---|---|---:|---|---|
| 3 | `P1:03a_unlabelled_birds` | 7.90-11.90 s | 4.00 s | Veo 3.1 - Quality, 100 | Veo 3.1 - Lite 4 s, 5 |
| 10 | `P1:07_darwin_1837_desk` | 33.44-39.40 s | 5.96 s | Veo 3.1 - Quality, 100 | Omni 1.2 Flash 8 s, 24 |
| 24 | `P3:02a_malthus_lamplight` | 172.58-178.80 s | 6.22 s | Veo 3.1 - Quality, 100 | Omni 1.2 Flash 8 s, 24 |
| 28 | `P3:05a_chicks_deep_beaks` | 201.96-206.50 s | 4.54 s | Veo 3.1 - Quality, 100 | Veo 3.1 - Lite 6 s, 5 |
| 47 | `P4:10_fairness_25_june` | 349.50-355.58 s | 6.08 s | Veo 3.1 - Quality, 100 | Veo 3.1 - Lite 8 s, 5 |
| 49 | `P4:12_lyell_hooker_bundle` | 360.98-366.34 s | 5.36 s | Veo 3.1 - Quality, 100 | Veo 3.1 - Lite 6 s, 5 |
| 54 | `P5:05a_darwin_writes_origin` | 404.66-411.56 s | 6.90 s | Veo 3.1 - Quality, 100 | Veo 3.1 - Lite 8 s, 5 |
| 63 | `P6:06a_origin_fifth_edition` | 485.64-490.60 s | 4.96 s | Veo 3.1 - Quality, 100 | Veo 3.1 - Lite 6 s, 5 |

### Row 3 · `P1:03a_unlabelled_birds` · take 2

- **Defect (Chief):** At about 2.9-3.1 s a fist separates from the sleeve and a second hand fragment shows top right (desk comment 6815859027, in force by 6815870258).
- **Fix sentence:** Exactly two hands are in frame, and each hand stays whole and joined to its sleeved forearm for the whole clip. Exactly three finch skins.

Retake prompt:

```
Premium Animistry-class 3D cartoon. On a wooden study table in grey window light, a naturalist's hands set down three small dark finch skins with blank unlettered paper tags tied to their legs. Exactly two hands are in frame, and each hand stays whole and joined to its sleeved forearm for the whole clip. Exactly three finch skins. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```

### Row 10 · `P1:07_darwin_1837_desk` · take 2

- **Defect (Chief):** Steel dip pen until about 3.5 s; by about 4.0 s it is a modern pen with barrel and clip (desk comment 6815859027, in force by 6815870258).
- **Fix sentence:** The pen is a plain wooden holder with a steel nib for the whole clip, with no clip, cap or button. He dips it and draws, and the pen stays the same object.
- **Fragile light:** warm lamplight. No unverified `Veo 3.1 - Lite` after 5 Dec.

Retake prompt:

```
Premium Animistry-class 3D cartoon. Summer 1837: a 28-year-old English naturalist, clean-shaven with dark sideburns and a dark frock coat, dips a steel pen in an inkwell at his study desk by warm lamplight. The pen is a plain wooden holder with a steel nib for the whole clip, with no clip, cap or button. He dips it and draws, and the pen stays the same object. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```

### Row 24 · `P3:02a_malthus_lamplight` · take 2

- **Defect (Chief):** Flame climbs clear of the top of the chimney glass at 4.5-5.0 s (desk comment 6822411223).
- **Fix sentence:** The lamp flame stays small and steady inside its glass chimney for the whole clip and never rises above the glass.
- **Fragile light:** warm oil lamp light. No unverified `Veo 3.1 - Lite` after 5 Dec.

Retake prompt:

```
Premium Animistry-class 3D cartoon. London study, 28 September 1838: a young English naturalist reads an open octavo book by warm oil lamp light. The lamp flame stays small and steady inside its glass chimney for the whole clip and never rises above the glass. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```

### Row 28 · `P3:05a_chicks_deep_beaks` · take 2

- **Defect (Chief):** Parent finch beak shifts dark grey (0.0-2.0 s) to bright orange (3.0-4.5 s) with a head and body morph (desk comment 6829662956).
- **Fix sentence:** The parent finch's beak stays dark grey-black and the same size and shape for the whole clip, and its head and body keep one form.

Retake prompt:

```
Premium Animistry-class 3D cartoon. In a Galápagos cactus nest, a deep-beaked parent finch feeds chicks whose beaks are stout and deep like the parent's. The parent finch's beak stays dark grey-black and the same size and shape for the whole clip, and its head and body keep one form. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```

### Row 47 · `P4:10_fairness_25_june` · take 2

- **Defect (Chief):** Tied bundle rises off the book at about 2.5 s without a hand and vanishes by about 3.0 s (desk comments 6830884885 / 6830918005).
- **Fix sentence:** The manuscript and the packet stay resting on the desk for the whole clip. Nothing lifts unless a hand is holding it, and nothing disappears.

Retake prompt:

```
Premium Animistry-class 3D cartoon. In grey window light at Down House, hands place the thick 1844 manuscript beside the thin foreign paper packet and fold a second letter. The manuscript and the packet stay resting on the desk for the whole clip. Nothing lifts unless a hand is holding it, and nothing disappears. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```

### Row 49 · `P4:12_lyell_hooker_bundle` · take 2

- **Defect (Chief):** Carried parcel under the arm smears at 0.85 s and dissolves by 1.00 s (desk comments 6830884885 / 6830918005).
- **Fix sentence:** The tied bundle stays one solid parcel under the carrying gentleman's arm for the whole clip and keeps its shape. The stone steps stay fixed.

Retake prompt:

```
Premium Animistry-class 3D cartoon. In London daylight, two Victorian gentlemen tie two manuscript bundles together with ribbon and carry them up stone steps. The tied bundle stays one solid parcel under the carrying gentleman's arm for the whole clip and keeps its shape. The stone steps stay fixed. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```

### Row 54 · `P5:05a_darwin_writes_origin` · take 2

- **Defect (Chief):** Sheet under the hand turns from a white written page at 2.80 s to a blank tan curl at 2.90 s (desk comments 6831422974 / 6831444565).
- **Fix sentence:** The page under his hand stays the same flat cream sheet, covered in ink scribble lines, for the whole clip. It never turns blank and never curls.

Retake prompt:

```
Premium Animistry-class 3D cartoon. Down House study, 1858–1859: an English naturalist of about fifty, clean-shaven with long greying side whiskers, writes page after page at his mahogany desk as light shifts across the window, stacking a thick manuscript. The page under his hand stays the same flat cream sheet, covered in ink scribble lines, for the whole clip. It never turns blank and never curls. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```

### Row 63 · `P6:06a_origin_fifth_edition` · take 2

- **Defect (Chief):** Warm gold light in the gutter of the open book from about 2.0 s to 4.5 s, forbidden by the prompt (desk comments 7020824090 / 7023130641).
- **Fix sentence:** The open pages stay matte cream paper lit only by the grey window from one side, and the gutter between the pages stays in soft neutral shadow.

Retake prompt:

```
Premium Animistry-class 3D cartoon. Close in grey window light on a mahogany desk as a green cloth-bound book opens beside a folded handwritten letter. The open pages stay matte cream paper lit only by the grey window from one side, and the gutter between the pages stays in soft neutral shadow. Daylight, window light or matte painted ink only. No candle, flame, glow, spark, fireball or lightning. No readable words or numbers anywhere. Silent. Continuous motion through the final frame. No Explorer. No Orbit.
```
