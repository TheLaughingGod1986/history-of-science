# Thumbnail Brief v01 — HOS:011 *Anesthesia: The Day Surgery Stopped Hurting*

- **Stage:** **Approved & locked £0 pre-build brief** (`J3740`, Acting Chief `gemini`, 25 Nov 2026; drafted by `claudecode`, queued in `J3734`). **Not a rendered packaging PASS.** Nothing is generated from this brief until the film's picture locks; no image or Flow credit was spent writing or locking it.
- **Target air:** Thu 17 Dec 2026 18:00 London (Ben's watch Mon 14 Dec 2026).
- **Title pair on launch (2-way Title Test & Compare, `J0180`):** A *Anesthesia: The Day Surgery Stopped Hurting* · B *What Surgery Was Like Before Anesthesia*. No cover below uses a word from either title.
- **House rules:** painted 3D cartoon key art in the period palette (warm window and lamp light, no saturation push); serif lettering, cream with **one** gold hook word, in a clear top-left band and never over the hero object; the Explorer small at lower left (`CHARACTER_BIBLE.md`); cover text never repeats the title (`THUMBNAIL_AND_TITLE_RULES.md` §2.5); lettering composited in code and checked glyph by glyph (§2.6), never generated; name the thing, no vague teaser.
- **No gore:** no blade on skin, no blood, no wound. The watch, the globe, the chair and the faces carry it.

## Thumbnail concepts (Test & Compare A / B / C)

1. **Thumb A (primary — the stakes):**
   - **Cover text (2 words, top-left band):** `WIDE` *(cream serif)* / **`AWAKE`** *(gold serif)*
   - **Key art:** a steep wooden 1840s London operating theatre in tall window light. Centre-right, the empty wooden operating chair with leather straps hanging from its arms; behind it a surgeon in a dark frock coat holds an open brass pocket watch. Students crowd the gallery rail above. Explorer small at lower left, lantern raised, looking at the chair.
   - **Flow Nano Banana 2 prompt (0 cr):** *Premium painted 3D cartoon illustration, 16:9. A steep wooden 1840s operating theatre lit by tall windows, warm dusty light. Right of centre, an empty wooden operating chair with worn leather straps hanging from its arms. Behind it a stern surgeon in a dark frock coat holds an open brass pocket watch. Rows of students lean over a curved wooden gallery rail above. The top-left third of the frame is plain dark wood panelling in soft shadow, left empty. Period palette of walnut brown, brass and cream. No text, no letters, no numbers, no blood, no instruments on skin.*
2. **Thumb B (the object — Ether Day):**
   - **Cover text (2 words, top-left band):** **`ETHER`** *(gold serif)* / `1846` *(cream serif)*
   - **Key art:** close on the two-necked glass inhaler globe held up in a hand under the domed skylight of the Boston operating theatre, a soaked sponge inside it catching the light; the packed benches a soft blur behind. Explorer small at lower left with his notebook open.
   - **Flow Nano Banana 2 prompt (0 cr):** *Premium painted 3D cartoon illustration, 16:9. Close view of a hand in a dark sleeve holding up a round two-necked glass inhaler globe with a small sponge inside, glowing softly in daylight from a domed skylight above. Behind it, out of focus, steep benches packed with men in 1840s dark coats. The top-left third of the frame is plain shadowed plaster wall, left empty. Period palette of warm cream, brass and deep green. No text, no letters, no numbers, no blood.*
3. **Thumb C (third arm, §2.9 — the race):**
   - **Cover text (3 words, top-left band):** `TIMED BY` *(cream serif)* / **`WATCH`** *(gold serif)* *(Chief amendment in `J3740`: trimmed from 4 words / 2 gold words to 3 words with one gold punch word per §2.4/§2.5/§2.B and cleaner `168×94` phone legibility)*
   - **Key art:** a row of students' hands along the gallery rail, each holding an open pocket watch; the nearest watch large at centre-right, its second hand mid-sweep; far below and soft, the surgeon looks up at them. Explorer small at lower left, peering up at the watches.
   - **Flow Nano Banana 2 prompt (0 cr):** *Premium painted 3D cartoon illustration, 16:9. A curved wooden gallery rail in an 1840s operating theatre. A row of students' hands rest on the rail, each holding an open brass pocket watch; the nearest watch is large at centre-right with its second hand mid-sweep. Far below and softly out of focus, a surgeon in a dark frock coat looks up. The top-left third of the frame is plain dark timber in shadow, left empty. Warm window light, walnut, brass and cream palette. No text, no letters, no readable numerals, no blood.*

**Explorer:** composited from the approved Explorer plate at lower left after generation, not asked for in the prompt, so his look stays on the bible.

## Why these three

- **A** sells the fear the film resolves and pairs with either title without repeating it.
- **B** names the thing and the year for the search-led title A; it is the only arm with a number.
- **C** carries the same pocket-watch image as Short A, so the long and its Short recognise each other in the feed.

## Gate checklist (after picture lock)

- [ ] Generate the three key-art plates with Flow Nano Banana 2 (`0` cr); read the live Flow balance first and record it in `ai_spend.py`.
- [ ] Composite the cream and gold serif lettering in Python/Pillow; exact glyph check (§2.6); lettering clear of the hero object and the duration badge.
- [ ] `style_sheet.py long <thumb.jpg>` and `thumb_preview.py long <thumb.jpg>` (`168×94` phone read).
- [ ] `packaging_panel.py` critique, then the Chief's HOOK / BAND / PHONE call before Ben's watch.
- [ ] Each test goes in `THUMB_LEDGER.json` when it is armed.
