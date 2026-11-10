# HOS 007 plate boards v01: Claude review (J0315, 15 Oct 2026)

Boards: `parts/part-0{1..5}_plates_v01.json`, `PICTURE_PLAN_v01.json` (written 7 Oct). 96 rows: 25 Quality, 55 Fast, 16 reuse; 78 Vertex, 2 Flow. **Verdict: FIX before any mint.** The script match, part timing and Explorer count (3 beats, on model) are fine. The plan needs re-pricing, and ten plates carry a real risk of fake lettering.

## 1. Re-price Flow-first (blocking)

- **Why:** v01 is priced on Vertex (£58.24 try-1, £139.01 expected) from a time when Flow had 52 credits. Usable Vertex is now about £70, so v01 cannot be minted as written.
- **Flow estimate:** using the HOS 009 J0261 rates (Quality 100 cr × 2.59 takes, Fast 10 cr × 1.96), the 80 mints come to about **7,550 credits** (Quality ≈ 6,475, Fast ≈ 1,080).
- **Budget:** 23,730 left minus HOS 009 (15,642 expected) minus 028 (279) leaves ≈ 7,800. 007 fits, just. The order call (007 before or after 009, per STATUS "after 006 and 007") is the Chief's. Flow refills on 12 Nov.
- **Ask:** v02 boards should carry the Flow-first price table in the same format as HOS 009, with Vertex as fallback only.

## 2. Plates that would generate fake lettering (blocking: the 004 lesson)

**Why this matters:** HOS 004's `03_weights_line` was prompted "no readable words" and still came out with Hp/Hg/Op glyphs, and it shipped (now blurred, J0320). "Soft unreadable handwriting" asks the model to draw letters, so the same failure is likely.

| Plate | Risk | Fix (all £0 or cheaper) |
|---|---|---|
| P4 `08b_title_page` (printed title page) | the model draws a fake title | **Real scan:** Jenner, *An Inquiry into the Causes and Effects of the Variolae Vaccinae* (1798) title page, public domain (Wellcome Collection / Internet Archive). Push in on the scan; title added in the edit if needed. |
| P4 `09_satire` (etching-style crowd with cow heads) | fake etching captions | **Real print:** James Gillray, *The Cow-Pock — or — the Wonderful Effects of the New Inoculation!* (1802), public domain. It's the real satire the line describes, and better than a pastiche. |
| P2 `12_hunter_letter`, P2 `13_casebook`, P3 `05_quill_writes`, P3 `09_casebook_open`, P4 `01_page_turns`, P4 `06_line_underlined` | close-ups of handwriting | Reframe so no glyph is ever in focus: page edge-on, quill tip and shadow only, shallow focus on the hand. Or use real Jenner manuscript scans (Wellcome) where the line is about his notes. Drop at least two of the six as near-duplicates (casebook appears six times); reuse the strongest. |
| P1 `07_map_shadows`, P4 `11_news_spreads` (parchment maps) | invented place names | **£0 code-graphic map** in the house teach style (inked map that draws itself; one label at a time added in the edit). |
| P5 `10_history_book` (book spines on a shelf) | fake spine titles | Spines turned away / out of focus, or cut: it is a 4.6 s transition. |

**Net effect:** about 6–8 fewer Fast mints, with real-source plates replacing generated ones where the film names a real document or print.

## 3. Smaller notes (not blocking)

- **Plate I of the 1798 *Inquiry*** (Sarah Nelmes' cowpox hand, hand-coloured, public domain) is the real image of the moment in P3 `01_sarah_nelmes`. Use it as a cutaway after the generated plate, as a £0 teach beat.
- **P5 `11b_storm_builds` / `12_kite_storm`** are the hand-off to 008 Franklin. Keep them only if the after-act stays on 008; the plates must not show lightning touching the kite (prompts already say so).
- **P5 `08_body_learns`** (abstract immune cutaway) is Quality. It is a mechanism beat, so the house rule says an inked diagram on period paper or a cream teach card, i.e. a £0 code graphic. That saves one Quality mint.
- **Faces:** Jenner appears in several Quality plates (`04_lancet_touch`, `02_variolation_calm`). Lock one reference still after the first keep and use it as the start frame for the rest, so his face doesn't drift.
- **Explorer:** 3 beats (`12_explorer_press`, `13_explorer_meadow`, plus Part 01). In the press beat he picks up the printed book, so the same lettering rule applies to its cover.

## Next

Cursor: boards v02 with §1 and §2 (and §3 where cheap), Flow-first table, then park for the Chief's price pass. No mint until that PASS.
