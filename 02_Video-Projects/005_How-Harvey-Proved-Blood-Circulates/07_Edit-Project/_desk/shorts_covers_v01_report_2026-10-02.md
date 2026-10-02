**Grok → Claude · 005 Shorts: frame-0 sheet, covers v01 and three titles, ready for Ben to check together. Nothing is in Studio.**

### 1. Frame 0 (what the feed shows, rules §3)

Sheet: `10_Shorts/covers_v01/hos_005_shorts_v01_frame0_sheet.jpg`. It shows frame 0 of each passed v01 file (shas `732bca40…`, `e2eacb0c…`, `5839c4dd…`, unchanged) at phone width, 390 px. There's no new build.

| Short | Frame 0 | Hook caption |
|---|---|---|
| A | fingertips on a wrist pulse, a warm stream racing up the arm | MORE THAN YOU **HAVE** |
| B | two hands pulling a linen band tight round a bare arm | ONE TIGHT **BAND** |
| C | the capillary mesh through the eyepiece | HE NEVER **SAW** THIS |

The Explorer isn't in any frame 0. The gate was re-run on the proposed air dates (A 30 Oct, B 8 Nov, C 15 Nov):

```
$ gate_shorts_open.py check hos_005_s01_the_sum_v01.mp4 --air-date 2026-10-30
PASS  hos_005_s01_the_sum_v01.mp4  dur=24.07s  audio=-21.2dB  motion=27.31  dhash=4b5307236a79723b
$ gate_shorts_open.py check hos_005_s02_the_tied_arm_v01.mp4 --air-date 2026-11-08
PASS  hos_005_s02_the_tied_arm_v01.mp4  dur=25.83s  audio=-21.6dB  motion=19.22  dhash=070f46033fa90e0e
$ gate_shorts_open.py check hos_005_s03_never_saw_v01.mp4 --air-date 2026-11-15
PASS  hos_005_s03_never_saw_v01.mp4  dur=24.83s  audio=-21.7dB  motion=17.01  dhash=0f0f0d1f6e030f0f
```

**14-day uniqueness:**
- **A (30 Oct):** 0 near opens (`near_opens: []`). The nearest library open is 32 bits away (fail ≤10, warn ≤16).
- **B (8 Nov) and C (15 Nov):** no other Short in the library falls inside their windows.
- **A, B and C against each other** (none is in the library until upload): A–B 26 bits, A–C 27, B–C 17. B–C is just clear of the 16-bit warn line.

**Two things for you to know:**
- **The gate library is stale.** It doesn't have the carbolic spray Short (`clV6E10NLPw`, scheduled 20 Oct, inside A's window), and it still lists `CUu8k38iAMc` (made private 30 Sep) as scheduled. I checked carbolic spray by hand against `hos_001_s06_carbolic_spray_punch_v01.mp4`: A 39 bits, B 35, C 34, so all clear. Caveat: I haven't confirmed that file is the exact one scheduled. I didn't edit the library; that wants `gate_shorts_open.py add` and `status … retired` in its own change.
- **The hook caption is smaller and higher than §3.3 asks.** On all three, the yellow hook word's cap height is 4.6% of frame height (§3.3: 8–10%). The two-line caption block sits at about 13–26% from the top, not in the vertical centre. Ben has already passed these files, so I didn't rebuild. If he wants it to rule, it's a re-export of the caption layer only (`_build_shorts_v01.py`), then a re-gate.

### 2. Covers v01 (search, channel page and Related, rules §4)

| Short | Words (teal middle) | Picture | File (`10_Shorts/covers_v01/`) | sha256 |
|---|---|---|---|---|
| A | MORE / **THAN YOU** / HAVE | a tower of copper and pewter jugs, far taller than a glowing faceless glass figure with a warm loop in its chest; the Explorer small, lower left, looking up | `hos_005_s01_the_sum_cover_v01.jpg` | `e67dc816…` |
| B | ONE / **TIGHT** / BAND | an arm on the table, a linen band round the upper arm, blue veins swelling below it, the hand flat; the Explorer small on the table | `hos_005_s02_the_tied_arm_cover_v01.jpg` | `4bd0fa6c…` |
| C | FINER / **THAN A** / HAIR | a brass microscope at a Bologna window; below, a magnifying glass over a slide shows a net of vessels next to one hair lying across it like a rope; the Explorer small at the lens rim | `hos_005_s03_never_saw_cover_v01.jpg` | `77e34ab7…` |

- **Lettering:** the Shorts style: chunky bevelled gold/cream letters with a thick dark outline and a smaller teal middle line, all caps. Never the long's serif.
- **Measured** (`COVERS_INDEX_v01.json`): the stack is 62.7%, 60.8% and 61.4% of the width. It sits at 34.5–65.5% of the height, inside the 34–66% slice the Shorts list crops to. No horizontal stretch.
- **Picture:** all three differ from frame 0. They're painted scenes, not film-frame crops.
- **Facts:**
  - B has no red anywhere: just a natural skin tone and blue veins below the band. So it can't read as blood below a tight band, or as a wound.
  - A's only red is the warm loop glowing inside the faceless figure. The jugs are closed and nothing spills.
  - C's capillaries have no faces, and there's no animal (no frog). No gore anywhere.
  - C's microscope is the same brass type as the film's Malpighi plate, not a strict 1661 instrument.
- **How it was made:**
  1. Cursor GenerateImage painted each scene with no text, using the film's plate frame and the Explorer reference.
  2. It painted each lettering stack separately on flat magenta, using the live covers as the style reference.
  3. `10_Shorts/_land_hos_005_covers_v01.py` keys out the magenta and stacks the three lines.

  It places the stack in the centre band, because in five tries the model would not hold its own lettering there (it landed at 5–50% or 42–76%). Rejected passes stay in the Cursor assets folder; the kept inputs are in `covers_v01/_assets/`.
- **The Explorer:** clear of the lettering on all three. A's and C's stacks are offset right of centre (centre at 56% and 60% of the width) to keep him clear. In C, FINER is the widest line and HAIR is narrower, so HAIR clears his head.

```
$ python3 02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/10_Shorts/_land_hos_005_covers_v01.py
…/covers_v01/hos_005_s01_the_sum_cover_v01_preview.jpg
…/covers_v01/hos_005_s02_the_tied_arm_cover_v01_preview.jpg
…/covers_v01/hos_005_s03_never_saw_cover_v01_preview.jpg
…/covers_v01/hos_005_shorts_covers_v01_style_sheet.jpg  (3 new vs 8 live short references)
  hos_005_s01_the_sum_cover_v01.jpg  width 62.7%  x [24.6, 87.3]  y [34.5, 65.5]  in 34–66% band: True  stretch 1.0
  hos_005_s02_the_tied_arm_cover_v01.jpg  width 60.8%  x [29.6, 90.5]  y [34.5, 65.5]  in 34–66% band: True  stretch 1.0
  hos_005_s03_never_saw_cover_v01.jpg  width 61.4%  x [29.3, 90.6]  y [34.5, 65.5]  in 34–66% band: True  stretch 1.0
  INDEX 02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/10_Shorts/covers_v01/COVERS_INDEX_v01.json
```

(`thumb_preview.py short` runs once per cover and `style_sheet.py short` once on all three, both inside the script.)

- **At 168×94 (the centre crop) and in the 110×196 tile:** every word reads, and the teal line is small but readable.
- **Style sheet:** same family as the eight live covers (the painted world, the lettering, the gold, the Explorer). One visible difference: the live covers put larger lettering (about 85–90% of the width) across the top. §4.2 asks for the vertical centre and the Shorts-list crop, so ours are centred at about 61%, and they read a little smaller in the tile than the live ones. If Ben prefers the live look, I'll move the stacks to the top at about 85% width. That's a rule change for §4.2, so it's your and Ben's call.

### 3. Titles to upload with

| Short | Title | Characters |
|---|---|---:|
| A | Your Heart Pumps More Blood Than You Have | 41 |
| B | One Tight Band Proved Your Blood Goes Round | 43 |
| C | The Blood Vessels Finer Than a Hair | 35 |

- **Rules §1:** each has a familiar noun in the first four words (heart / band / blood vessels). None has a hedge, a hashtag or a suffix, and none copies a live title (checked against `SHORTS_LOG.md`).
- **Cover words** come from each title's hook. A's matches its frame-0 caption, and so does B's. C's cover, FINER THAN A HAIR, is a second chance next to its frame 0, HE NEVER SAW THIS.
- **Facts:**
  - A: about 5 litres a minute at rest, so the heart moves more than the body's whole supply within minutes. Harvey's half-hour sum gives the same result.
  - C: capillaries are about 5–10 µm across; a hair is about 50–100 µm.
- **B and the long:** B echoes the long's title (*The Tied Arm That Proved Your Blood Circulates*) without copying it.

Images on this post: the frame-0 sheet, the covers style sheet, and the three 168×94 previews. Nothing is uploaded, set in Studio or scheduled. The covers wait for Ben's sign-off, with the titles.
