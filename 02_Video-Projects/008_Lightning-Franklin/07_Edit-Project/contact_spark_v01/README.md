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
