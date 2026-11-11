# HOS 008 contact spark — bloom revision (desk 6797257524)

Second size pass. The first pass (peak alpha 80, radius about 25 px) changed pixels under a zoom and did not read at 390 px. Geometry stays the measured pair, (933, 340.5) to (945, 333) at 1080. The core stays about 3.8 px FWHM. The bloom carries the phone read.

- f030: warm white, peak alpha 190, Gaussian radius 60 px at 1080, centred on the gap.
- f031: the same bloom at half strength, on the shorter half-strength streak.
- f029: a pre-glow at 25% of f030's bloom, no streak, so the flash is three frames.
- The streak's lower end stops at the skin edge. It does not continue onto the finger.

The glance test is `review_phone390_pair_bare.png`: the untouched f029 source beside f030, each exactly 390 px wide, with no enlargement. The 4× crop is separate, so a flare can be judged without using the zoom as the proof. Sheets are in `review_J2613_bloom/`. No spend, no take edited, nothing past f060. The first-pass sheets stay in `review_J2613_size/` as the failed comparison.

---

# HOS 008 contact spark — J2613 revision for review

Supersedes the point-shaped J2591 design below. Requested by owner-authored desk rulings 6793746982 (shape) and 6795970738 (take/timing). Existing PR #515 stays unmerged pending Grok’s review.

The renderer now draws a warm RGB 255/246/224 tapered streak spanning the measured endpoints, with a Gaussian cross-section (~2 px FWHM at 1080p), rounded ends and 8× pixel integration. Phase +0 has one faint bloom; +1 is shorter at half strength; optional +2/+3 are fading round points at the knuckle. Endpoint-distance and coordinate guards remain. Two-frame output is also supported for the later placement ruling.

## Take 4 review (not placement in the film)

`review_J2613/` contains full 1920×1080 PNGs for f029–f031, a full-size sheet, a 4× before/after crop, and a separately labelled four-phase design swatch. The take is native 1280×720; the 1080 delivery previews are a 1.5× Lanczos resize, not native captured 1080 detail. The artifact directory also contains native-720 previews and canonical 1080 RGBA overlays.

Gemini’s upper knuckle/rim pair is used: knuckle (622,227), rim (630,222) at 720p; exactly (933,340.5) and (945,333) at 1080p. Source hash is checked by the reproducible `review_take4.py` before extraction. Only f029, f030 and f031 are extracted. No source take or edit is modified.

**Timing proposed for Grok:** the later ruling requests 2–3 frames around f030, superseding the earlier four-frame duration. f029 is unchanged; f030 is the bright streak; f031 is the shorter half-strength streak. The optional +2/+3 tail is demonstrated on the separate design swatch only and is not placed on f032/f033. J2592 must use only the duration Grok approves. Cue the existing pen-tap at f030 once; no new audio or audio mix is made here.

**Source restriction:** only f000–f060 may ever be used from take 4. Nothing later may appear in any cut, thumbnail or Short. Placement belongs to J2592 after Grok’s PASS, followed by the existing review jobs. This delivery neither approves a stage nor changes the film.

Reproduce with the `owb-cg` Python environment:

```sh
python review_take4.py --take /path/to/02_salon_spark_j2241_t4.mp4 --out NEW_REVIEW_DIRECTORY
python -m unittest discover -s . -p test_render.py
```

Four tests cover duration/blank frames, warm colour, input guards, gap-spanning tapered profile, half-strength shortened second frame, knuckle-only tail, rotational symmetry and local support. The source hash and unchanged f029 checks pass. Stills inspected at full delivery size and 4×; no moving-video or audio perception claimed. See `review_J2613/REPO_CHECKS.txt` for this revision’s repository checks. The original picture/polish checks below apply only to the original still demo, not this revision or the finished film.

Durable artifacts: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/contact_spark_J2613_v02/`. Hashes are in the review manifest. £0 spent.

---

## Historical J2591 delivery (superseded design; retained evidence)

# HOS 008 salon contact spark — J2591

Built under the desk ruling 6793185344, confirmed by 6793202900. Worker delivery for review, not a picture-stage approval. No generation credit or money spent; no video take changed.

Artifacts: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/07_Edit-Project/contact_spark_J2591_v01/`. `MANIFEST.json` records paths, hashes, dimensions, colour, frame count and the existing SFX cue. The four PNGs are canonical straight-alpha RGBA; `spark_rgba.mov` is lossless qtrle/ARGB. All four decoded frames match the PNGs exactly.

## Placement inputs for J2592

Use the KEEP third take's native dimensions and frame rate. Extract its contact still, measure the visible rod-tip and knuckle gap edges in that same pixel coordinate system, then run this renderer. Coordinates are x,y from top left; contact-frame is zero-based and refers to the destination take. It is metadata and the sound cue, not embedded transparent preroll. Overlay PNG/MOV frames 0–3 go on destination frames N–N+3, once only. Do not loop or extend the last frame. For three frames pass `--frames 3`. A new output directory is required.

```sh
python render.py --still CONTACT_STILL.png --contact-frame N \
  --rod X1 Y1 --knuckle X2 Y2 --frames 4 --fps 24 \
  --sfx '/Volumes/data/studio-live/History Of Science/02_Video-Projects/008_Lightning-Franklin/06_Sound-Effects/kit_v01/sfx_hos_tick_ink_v01.wav' \
  --out NEW_OUTPUT_DIRECTORY
```

Dependencies: Python, Pillow, NumPy, ffmpeg. Mini environment: `/Users/benjaminoats/_desk/venvs/owb-cg/bin/python`.

The point is centred between the two inputs. Maximum core radius is 2.8 px at 1080p; a faint bloom appears on the first frame only, radius at most 6 px. Both supports are clipped to a circle whose diameter cannot exceed the gap. Colour is RGB 255/246/224. No line, branches, blue/purple, hair lighting or face lighting is drawn. The 1080p gap guard is 2–24 px (scaled with height); a distant hand is rejected. At contact use the visible edges, not coincident coordinates. Re-measure if a crop or scale is applied. Check all four frames after placement; this static coordinate renderer does not track moving points.

The existing film pen-tap (`sfx_hos_tick_ink_v01.wav`) is paired on the first bright frame. The two-second still demo includes it at 0.5 s. Its level is not a final VO mix: J2592/assembly must retain the film's SFX level rules and avoid doubling an existing cue. No new sound was generated.

## Preview limits and checks

The original start frame has no rod-to-knuckle contact. The demo uses rod `(643,190)` and illustrative second endpoint `(633,190)` near the tip, at native 1376×768. The second point is **not a measured knuckle**. This is a size/colour test only; do not reuse these placement coordinates on a take. `preview_00.png` is the full-size composite; `review_sheet.jpg` shows the four local crops enlarged. `still_demo_with_existing_tick.mp4` animates the flick over that same still, not over a video take. The source SHA-256 matches the J2241 brief.

Verification output:

```text
Ran 3 tests ... OK
4 decoded RGBA frames; lossless_rgba_roundtrip: true
picture QA PASS: 0 of 1 cuts fail, 0 to look at
polish gate PASS: 0 of 1 rows failed, 0 to look at
ALL CHECKS PASS
```

The tests cover transparent frames outside the three/four-frame interval, warm colour, gap containment, invalid inputs and single-frame bloom. Picture/polish checks apply to the still demonstration only, not the final take or film. Text/WHO/DATA counts and full-film motion/SFX mixing are not assessed by this isolated overlay check. Stills were visually inspected; no claim of hearing audio or perceiving moving video is made.

Next: Claude reviews size and colour; J2592 places a fresh render on the KEEP third take, records its actual frame/points/hashes and sends the composite for frame review. The existing J2592 handoff owns that work. No production stage has been marked approved.
