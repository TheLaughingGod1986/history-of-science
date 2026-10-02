# Thumbnail and title rules

Set 25 Sep 2026. Adapted from Orbit With Ben's thumbnail and title audit (48 Shorts, 25 Sep 2026) and checked against HOS's own first eleven Shorts (`audits/HOS_STUDIO_AUDIT_2026-09-25/`).

Evidence: **[HOS]** means our own channel. **[Orbit]** means Orbit's 48 Shorts; that is a sister channel with the same voice and stack, so it is the best evidence we have until HOS has more uploads. Replace Orbit evidence with our own as it comes in.

## 1. Titles (Shorts and longs)

1. **A familiar noun in the first four words:** your hands, your bones, a table, the sky, a drop of water, you. [HOS: *Microbes in a drop of pond water* 110, *Germs don't cast a shadow* 78] [Orbit]
2. **One concrete promise, in one of these shapes:**

   | Shape | HOS example |
   |---|---|
   | A familiar thing turned strange | *Germs don't cast a shadow* |
   | The body or the everyday, seen for the first time | *The first photo of bones inside a living hand* |
   | A yes/no about something everyone believed | *Did doctors really refuse to wash their hands?* |
   | A prediction that came true | *He predicted a metal before it was found* (32, best of the periodic table Shorts) |
   | One real number or object | *The flask that has stayed sterile since the 1860s* |
   | An accident that changed everything | *The glowing screen that showed a skeleton* |

3. **Longs share the neighbours' words (1 Oct 2026).** The title, the description's first two lines and the tags each hold one of the film's neighbour phrases: the subject noun the big TED-Ed/education videos on the topic use (never their channel names) (*periodic table*, *atom*, *X-rays*, *germs*). That is how YouTube knows to suggest us beside them. [HOS 002: 108 of 126 views from "suggested", 55.6% of those from TED-Ed's *The genius of Mendeleev's periodic table*] `npm run lint:package` checks it against the manifest's `neighbours` block (`tools/neighbours.py`). Test & Compare variants should keep the phrase too; one picture-led variant without it is allowed.
4. **Longs: the phrase people search, as a question or a promise,** with the subject in the first five words. Prefer the thing over the method: *How X-rays Let Us See Inside the Body*, *Why Doctors Laughed at Handwashing*. **Don't use *How Did We Discover X?* every week.** It reads as a series label and competes with the largest education channels on the same phrase. [HOS: the three formula titles had 88 views between them by 25 Sep; 002 then took off through TED-Ed suggestions because *periodic table* is in its title, not because of the formula] [Orbit: series formulas and "Everything you need to know" lose]
5. **No abstract labels or riddles.** *What other table has empty chairs?* (4 views) and *Invisible life is still everywhere* (6) make the viewer decode the title. If it could be a caption under a still, rewrite it. [HOS] [Orbit]
6. **No hedged claims.** "We may have…", "It might…", "What if…". A yes/no question starting "Did…" or "Could…" is fine. [Orbit]
7. **No hashtags, no series suffix, and never the title of a live video.** [Orbit]
8. **Under about 60 characters,** so it isn't cut off on a phone. Length is not the lever; the shape is. [Orbit]
9. **Wonder, not fear.** Proof and discovery, not "deadly" or "horror".

## 2. Long thumbnails (16:9)

Changed 30 Sep 2026 to match the live look (001 flask, 002 gallium; `02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/08_Thumbnail/LIVE_THUMB_LOCK.md`). The 25 Sep version asked for a flat sans yellow/white style; three rounds of HOS 004 thumbs built to it looked like another channel, and Ben rejected them. The first set built to the live look (HOS 004 v04) he passed.

1. **Painted key art, not a film frame and not a graphic.** Premium 3D cartoon painting, full bleed, warm golden library or lab light, the same world as the film. Never flat shapes, split panels or a plain dark background.
2. **One giant hero object, about two thirds of the frame, on the right:** the flask, the gallium, the atom, the coin under the knife. It must read at a glance at phone size.
3. **The Explorer small in the lower left,** on model (teal coat, round gold glasses, satchel; attach `01_Character/05_Generation-References/hos-explorer-reference-v01.jpg`), looking at the object. A garnish, never the subject, never filling the right half.
4. **Painted lettering on the left:** cream words with **one gold punch word**, the same serif display lettering and small gold flourishes on every thumb. The same lettering every week is how a returning viewer spots us. 2–5 words, readable at **168×94** (check with `python3 00_Brand/Channel-Setup/tools/thumb_preview.py long <thumb.jpg> --out <sheet.jpg>`).
5. **Words:** the main thumb may carry the title painted in, as the live ones do. The other variants carry 2–3 hook words that add to the title (*CUT GOLD?*, *THE HIDDEN NUMBER*). Test & Compare decides which works; don't assume.
6. **Facts on the picture must be right.** No AI-made text anywhere except the painted lettering: blank tiles, plain coins, no fake element symbols. Any symbol or number (Te 52, I 53) is checked and, if the model gets it wrong, added by hand in the same lettering.
7. **Keep the subject and lettering out of the bottom-right corner** (the duration badge), and every object fully in frame.
8. **Make it** with an image model (Gemini / Flow image), attaching a live thumb as the style reference and the Explorer reference. Put each new thumb next to a live one on one sheet to check it's the same family.
9. **Test & Compare with 3 variants on every long.** Judge CTR only past about 500 impressions.

## 3. Shorts: frame 0 is the thumbnail

In the Shorts feed nobody sees the custom cover. They see frame 0.

1. **Frame 0 is the named thing, moving.** Never a blank card grid, an empty room or a dark card. [HOS: pond water 110 and shadow 78 open on the thing; empty chairs 4 opens on blank cards] [Orbit: world or object at frame 0 median 86.5 views; dark or text card 16.5]
2. **The Explorer is never at frame 0.** [Orbit: mascot-first opens got 0% feed traffic]
3. **A frame-0 caption: the promise in 2–4 words,** cap height about 8–10% of the frame, yellow on the hook word, vertically centred and clear of the bottom UI.
4. **A different opening frame from every Short in the last 14 days.** `gate_shorts_open.py` fails a repeat.

## 4. Shorts: custom cover (search, channel page, Related)

1. **Use the title's hook words,** not a new poetic line.
2. **2–4 words, big, like the live covers.** The stack spans about 85–90% of the frame width across the top third, as on *GALLIUM / in the / GAP* and *THE / CARBOLIC / SPRAY* in `style/shorts/` (2 Oct 2026: the live set is the approved look; 005 v01's centred 61% stacks read small next to it). Check with `thumb_preview.py short` and `style_sheet.py short`.
3. Use a different still from frame 0 when you can: the cover is a second chance.
4. **The Shorts lettering is not the long lettering** (30 Sep 2026, Ben). Covers use **chunky rounded bold display letters in gold/cream with a thick dark outline, one small teal middle word** (*GALLIUM / in the / GAP*, *TELLURIUM / before / IODINE*), on a painted 3D scene with the Explorer as a small reaction. Never the long thumbs' serif, and never a film-frame crop with a text box. The two styles share the painted world, the gold and the Explorer; each format stays in its own lettering.

## Two lettering styles, one channel

| Format | Lettering | Why |
|---|---|---|
| Long thumbnail (16:9) | Serif painted lettering: cream words, one gold punch word, small gold flourishes | Decides CTR on home and search; the distinctive "History of Science" look |
| Shorts cover (9:16) | Chunky rounded gold/cream, thick outline, one small teal word | Channel page and search only (the feed shows frame 0); punchier |

Before any new thumb or cover goes to Ben, put it on one sheet next to live ones **of the same format** and check that it's the same family: `python3 00_Brand/Channel-Setup/tools/style_sheet.py long|short <new.jpg> --out <sheet.jpg>` builds it from the reference set in `00_Brand/Channel-Setup/style/`. Approved new ones are added to that set.

## 5. Checklist before upload

- [ ] Title: familiar noun first, one of the shapes, no hedge, hashtag, formula or repeat.
- [ ] Thumb: 2–4 words that add to the title; `thumb_preview.py` sheet checked at the smallest tile.
- [ ] Longs: painted key art in the live look (one giant hero object, the Explorer small lower left, cream and gold painted lettering); facts on it checked; next to a live thumb on one sheet.
- [ ] Shorts: frame 0 passes `gate_shorts_open.py`; the frame-0 caption is the promise.
- [ ] Longs: Test & Compare with 3 variants.
- [ ] After 7 days: log impressions and CTR in `audits/SHORTS_LOG.md` (Shorts) or the film's `11_Upload-Package/` (longs).
