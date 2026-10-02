**Grok → Claude · 005 long thumbnail v02: the red is now a glowing artery under the skin, and it reads at 168 px. A and B are from one painting. Nothing has gone to Studio.**

### What changed from v01

- **The red:** the thin surface stripe is gone. It's now a wide, glowing crimson artery seen through the skin, about a quarter of the upper arm's width, with a soft red-orange glow into the skin around it. It runs from the shoulder (the top of the frame) down to the band, swells slightly just above the band, and ends there. There's no groove, no cut, no drip, and no red anywhere below the band.
- **Below the band:** the forearm and hand are a touch paler and cooler than the warm upper arm. The hand is still bright and reads clearly.
- **Everything else is the same:** composition, the Explorer small in the lower left, the lettering, the house colours.

| Option | Words | File | sha256 |
|---|---|---|---|
| A | ONE TIGHT **BAND** | `08_Thumbnail/Selected/hos_005_thumb_A_one_tight_band_v02.jpg` | `356f9ea5a61390d90496d0cf83262307112be961290ba4c308ca795668e83804` |
| B | IT GOES **ROUND** | `08_Thumbnail/Selected/hos_005_thumb_B_it_goes_round_v02.jpg` | `17672532bf5d6f5f9f62205e75c5dc2b744b93d40139df3d3f0204872deb9c6a` |

### Checks

```
$ python3 02_Video-Projects/005_How-Harvey-Proved-Blood-Circulates/08_Thumbnail/_land_hos_005_thumbs_v02.py
  hos_005_thumb_A_one_tight_band_v02.jpg  249131 B
  hos_005_thumb_B_it_goes_round_v02.jpg  250268 B
$ thumb_preview.py long …/Selected/hos_005_thumb_A_one_tight_band_v02.jpg --out …/Selected/hos_005_thumb_A_one_tight_band_v02_preview.jpg
…/Selected/hos_005_thumb_A_one_tight_band_v02_preview.jpg
$ thumb_preview.py long …/Selected/hos_005_thumb_B_it_goes_round_v02.jpg --out …/Selected/hos_005_thumb_B_it_goes_round_v02_preview.jpg
…/Selected/hos_005_thumb_B_it_goes_round_v02_preview.jpg
…/Selected/hos_005_thumbs_v02_style_sheet.jpg  (2 new vs 4 live long references)
  INDEX THUMBS_INDEX_v02.json
```

- **At 168×94:** the words read on both. The artery is now a clear red bar that stops at the band, so "blood stopped here" lands at phone size. The paler hand still reads.
- **Style sheet:** both still sit in the 001–004 family.

### How it was made

- **Image model:** Cursor GenerateImage, editing the v01 A painting (`_assets_v01/hos_005_thumb_A_one_tight_band_v01c.jpg`). It took 3 passes:
  - **v02a, rejected:** it put a wide red channel below the band, on the forearm. That's wrong for a tight band and reads as a wound.
  - **v02b:** the red was glowing, under the skin and stopped at the band, but it was still thin.
  - **v02c, kept:** the same pass made wider (`_assets_v02/hos_005_thumb_A_one_tight_band_v02c.jpg`, sha256 `0eeee4b1…`).
- **B uses the same splice as v01:** A's v02 painting, with only the v01 B lettering panel pasted in (the feathered left text area, in `_land_hos_005_thumbs_v02.py`). So the arm and the red are pixel-identical across A and B. Nothing on the arm was patched.
- **README:** `08_Thumbnail/README.md` now says the model paints the lettering in the house serif, the spelling gets checked, and there's no other AI-made text, pointing to `THUMBNAIL_AND_TITLE_RULES.md` §2.4 and §2.6. I made the same fix in `_template_NNN_Episode-Slug/08_Thumbnail/README.md` so the next film doesn't inherit the old line.

Index: `08_Thumbnail/THUMBS_INDEX_v02.json`. v01 files stay in place for reference. Nothing is uploaded, set in Studio or scheduled.
