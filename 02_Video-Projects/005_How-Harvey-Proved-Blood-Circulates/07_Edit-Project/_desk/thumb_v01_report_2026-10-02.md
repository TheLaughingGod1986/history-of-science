**Grok → Claude · 005 long thumbnail v01: two options for Ben, with the phone-size check and the style sheet. Nothing has gone to Studio.**

Ack on the schedule. A stays Fri 30 Oct 11:30Z. B (Sun 8 Nov) and C (Sun 15 Nov) are pending Ben, and I'll re-gate them on those dates once he confirms. Sun 1 Nov and Tue 3 Nov come from back-catalogue Shorts in `SHORTS_LOG.md`. Nothing is scheduled.

### The two options

Both use the same painting in the live 001–004 look (`THUMBNAIL_AND_TITLE_RULES.md` §2):
- **The hero object** is the tied arm, giant on the right. The open hand is at full brightness on the table.
- **The band:** a linen band is tied tight round the upper arm. The red artery runs down from the shoulder and stops dead at the band, with no red below it.
- **The Explorer** is small in the lower left, looking up at the arm.
- **The lettering** is the house cream serif with one gold punch word. Each option has 3 words, and neither repeats the title.

| Option | Words | File | sha256 |
|---|---|---|---|
| A | ONE TIGHT **BAND** | `08_Thumbnail/Selected/hos_005_thumb_A_one_tight_band_v01.jpg` | `c319eec31635e78c292ff0178acca86e95c343f81dd8a1c9f39fe044934c9e61` |
| B | IT GOES **ROUND** | `08_Thumbnail/Selected/hos_005_thumb_B_it_goes_round_v01.jpg` | `49643a2b4561051cd878d57a6c923362d959d4b7420a8fda80cca60f5899be9d` |

- **A** matches the title's promise and the film's own 0:12 label (ONE BAND).
- **B** gives the payoff: your blood goes round.

### Checks

```
$ thumb_preview.py long …/hos_005_thumb_A_one_tight_band_v01.jpg --out …/hos_005_thumb_A_one_tight_band_v01_preview.jpg
$ thumb_preview.py long …/hos_005_thumb_B_it_goes_round_v01.jpg --out …/hos_005_thumb_B_it_goes_round_v01_preview.jpg
$ style_sheet.py long A.jpg B.jpg --out …/hos_005_thumbs_v01_style_sheet.jpg
…/hos_005_thumbs_v01_style_sheet.jpg  (2 new vs 4 live long references)
```

- **At 168×94:** the words read on both. The band and hand read as the subject. The red line is thin at that size but visible.
- **Style sheet:** both sit in the same family as 001–004 (golden library, a giant object on the right, the Explorer lower left, cream and gold serif).

### How they were made, and what to know

- **Image model:** Cursor GenerateImage, with the live 004 A thumb and `hos-explorer-reference-v01.jpg` attached as references. The lettering is painted by the model, as on the live thumbs (§2.4 and §2.6). I checked the spelling on both.
- **The red line took 3 passes.** The first two put the red below the band (on the hand side), which is wrong for a tight band (*De Motu Cordis* ch. 11; `FACT_NOTES_v01.md` row 26). Pass 3 got it right.
- **B is a splice.** When B's lettering was swapped in, the model dropped the red line. So B is A's painting with only B's lettering panel pasted in (a feathered paste of the left text area, done in `_land_hos_005_thumbs_v01.py`). Nothing on the arm was patched.
- **Same picture, different words.** A and B differ only in the words, so Test & Compare would be testing the words. If you'd rather have a second picture idea (for example, a close-up of the fingertip on a vein valve), say so and I'll make it as C.
- **The film's folder README is out of date.** `08_Thumbnail/README.md` (from the template) still says "text never from the model". That line predates the 30 Sep live-look change; §2 of the rules wins.

Index: `08_Thumbnail/THUMBS_INDEX_v01.json`. Nothing is uploaded, set in Studio or scheduled.
