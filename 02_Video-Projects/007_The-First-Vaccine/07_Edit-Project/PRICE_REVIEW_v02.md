# 007 price review v02

Cursor, 16 Oct 2026, J0322. Boards only. **No mint. No spend. No merge.**
Applies `CLAUDE_BOARDS_REVIEW_v01.md` (J0315, a4474f9). Parked for the Chief's price pass.

## Readings

- Flow: **23740** credits at 2026-10-15T21:42:22Z (the 009 v04 read). Not re-read. Nothing spent in this pass.
- Vertex promo: **£71.02**. Usable **£70.02** after the £1 margin. The route stays Flow-first.

## Rates

Same rates as HOS 009. Expected credits are `ceil(try-1 × takes per keep)`.

| Model | Try-1 | Takes per keep | Expected per row |
|---|---:|---:|---:|
| Quality | 100 | 2.59 (70/27) | 259 |
| Fast | 10 | 1.96 (94/48) | 20 |

Vertex, if it were the route: Quality £0.16/s, Fast £0.08/s, clip lengths 4/6/8 s. It does not fit.

## Totals

v01 was 96 rows, 25 Quality / 55 Fast / 16 reuse, priced as Vertex (£58.24 try-1, £139.01 expected).
v02 is Flow-first. Six Fast mints and one Quality mint come off. One £0 archive cutaway is added. The VO timing is unchanged: the cutaway takes 2.0 s from `01_sarah_nelmes`.

| | rows | Quality | Fast | code | archive | reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | 20 | 4 | 13 | 1 | 0 | 2 | 530 | 1296 | £11.84 | £26.22 |
| Part 02 | 22 | 6 | 15 | 0 | 0 | 1 | 750 | 1854 | £16.16 | £36.50 |
| Part 03 | 16 | 3 | 9 | 0 | 1 | 3 | 390 | 957 | £8.16 | £18.21 |
| Part 04 | 20 | 3 | 8 | 1 | 2 | 6 | 380 | 937 | £7.04 | £16.03 |
| Part 05 | 19 | 8 | 4 | 1 | 0 | 6 | 840 | 2152 | £11.84 | £29.28 |
| **Film** | **97** | **24** | **49** | **3** | **3** | **18** | **2890** | **7196** | **£55.04** | **£126.24** |

All on Flow: **7196** expected against 23740 left.
All on Vertex: DOES NOT FIT (£126.24 expected vs £70.02 usable).

## Mint order

006 needs 0 Flow. Then 007, then 008 (5605), then 009 tranche 1 (7354). Every mint job reads Flow live first and stops if the read after its spend would drop below 3000. No top-up.

| After | Flow left | Against the 3000 floor |
|---|---:|---|
| 007 (7196) | 16544 | above |
| 007 + 008 | 10939 | above |
| 007 + 008 + 009 tranche 1 | 3585 | fits |

## What changed

1. **P4 `08b_title_page`** is the real 1798 title page, Wellcome M0005386, Public Domain Mark. £0. A hand turns the page. No generated title.
2. **P4 `09_satire`** is Gillray's *The Cow-Pock* (12 June 1802), Library of Congress 94509853, public domain. £0. Not a pastiche.
3. **Two near-duplicate handwriting mints are cut.** `P3:09_casebook_open` reuses `P2:13_casebook`. `P4:01_page_turns` reuses `P3:05_quill_writes` (the 1 JULY 1796 overlay stays in the edit).
4. **Four handwriting plates stay Fast, reframed** so no glyph is in focus: `P2:12_hunter_letter` (page edge-on), `P2:13_casebook` (page block edge-on), `P3:05_quill_writes` (nib and shadow), `P4:06_line_underlined` (a line on a blank edge). The spoken overlays stay in the edit.
5. **Both parchment maps are £0 code graphics** (`P1:07_map_shadows`, `P4:11_news_spreads`). No place names in the render. Their old reuse rows stay reuse, still £0.
6. **`P5:10_history_book`** stays Fast. Spines face away.
7. **`P5:08_body_learns`** is a £0 code graphic (THE BODY LEARNS). That is the one Quality mint saved.
8. **`P3:01c_nelmes_plate`** is a £0 cutaway of the real 1798 plate of Sarah Nelmes' hand (Wellcome M0009446), 2.0 s taken from the generated study shot.
9. **`P4:12_explorer_press`** stays Quality. The book is seen from the back. The title lives on the real scan.
10. **Face lock.** `P2:08_jenner_window` is the master still, and its page is edge-on. Later readable Jenner faces start from the first KEEP of that plate.
11. **Kite hand-off kept** (`11b_storm_builds`, `12_kite_storm`). The flash never touches the kite.

`generation_authorized` is false on every row.

## For the Chief

No mint in this pass. Vertex does not fit. Flow fits in the order above: after 007, 008 and 009 tranche 1 the reading would show **3585** left.

Two things are not a price question:

- **Plate I shows cowpox pustules.** The film's forbidden list rejects sores. Claude asked for the real plate as a £0 cutaway. Dropping `01c_nelmes_plate` does not change the mint total; the 2.0 s goes back onto `01_sarah_nelmes`.
- **Archive stills and the motion lock.** The lock forbids a Ken Burns push. The boards ask for a hand turning the page instead. If that is not enough, the price pass can waive one slow push on the title page and the Gillray print.

The code graphics (`P1:07`, `P4:11`, `P5:08`) are a `chart` job after this pass. They are not minted.
