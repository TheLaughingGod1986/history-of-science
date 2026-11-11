# J2632 revised candidate — Chief review required

Codex covering. Implements desk 6806341672 on PR #543, superseding the old out 94 / 39-frame instruction. No KEEP, merge, splice, generation or spend.

- **179 unique decoded frames at 30 fps**, 1920×1080, silent; nominal 5.96 s, encoded 5.966667s. Exactly 21 new tangent-draw frames; old motion frame 0 becomes 21. Original 158 Moon positions and 70-degree path unchanged. Earth centre (560, 880), radius 150, orbit 720, Moon 57; clearance 513 px.
- Two off-centre open rings on this graphic only: 4 px stroke, 30 px outside diameter, 22 px inner hole, unchanged Moon wash. Other graphics retain their Moon. Coastlines and line weights unchanged.
- `CONTACT_SHEET.jpg`: 8 decoded frames plus 390 px-wide 1:1 frames 10, 137 (old 116), 178 (last). `PHONE_390.jpg` contains the three 390 px frames without enlargement. Both holes are visible in Codex's still inspection.
- `CUT_BOUNDARIES.jpg`: parent 99–104, excluded 112 and 125, graphic first/last and cannon first. Parent 104 is the required out; 108 is excluded from any future join. These are source samples, not an assembled crossfade.
- New SHA256: `cb8051bb9d6b46d014be46977522d089e19262fa7fd7fd90dfee3099fb13c2f7`. Superseded: `73e77846090c30cc3ae3b67c9df9a3f730dfecad42c1312691f511e13ec3889a`. Old media remains untouched. New media path and source hashes in `MANIFEST.json`.

## Timing conflict — not ready to splice

The literal 21-frame head at 30 fps lasts 0.700 s. Cutting parent 125 to 104 at 24 fps removes 0.875 s. **Difference 0.175 s**, larger than a frame. The brief's constraints cannot all hold together without an additional timing decision. No freeze, retime, extra head frames or hold has been introduced.

Mapping new frame 21 to 183.94 preserves the original Moon gap on the words and end 189.20; the new nominal start is 183.24. That alone does not reconcile the earlier parent out. The requested 0.20 s fade ending on parent 104 must also be checked against the final source-to-film mapping. Gemini independently rechecked the supplied alignment and geometry: **BLOCKED / CONTRADICTION FLAGGED (Do Not Pass Join)**. It confirms the 0.175 s mismatch, with further head coverage required if the graphic overlaps the parent for the crossfade. Its unedited response is adjacent. The old timing advisory does not approve this revised join.

Chief must reconcile the 24 fps parent and 30 fps graphic clocks, then decide KEEP. `splice_authorized` remains false and J2035 stays held. No question or approval is sent to Ben.

## Verification and limits

`J2632 geometry, stream, silence, 179 unique decoded frames and full decode checks passed; timing conflict FLAG; review pending.`

Still-image inspection plus encoded-frame/coordinate checks only; no claim of hearing narration or watching motion. Full repository validation is recorded in `CHECK_ALL.txt`. Board pins were refreshed using the required repin tool after merging main. No film stage was approved.
