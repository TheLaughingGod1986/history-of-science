# Part 04 v08 — Explorer garnish remint

**Status:** LANDED for CoS / UAT (do not ping Ben).

## Scope
- Reminted ONLY `06_explorer_leaves_gap`
- KEEP parent `hos_002_part04_rough_v07.mp4` sha `a74fa8ecd7f74785b3c4887e574d009676844189a0dc67620e659ae96e09efe2`
- KEEP 02b / 05 / 09 / 09b and all other plates; P01–P03 untouched

## Flow
- Account: `benoats@googlemail.com` on `/u/1/` (ULTRA)
- Model: Veo 3.1 Fast T2V (I2V media-library attach flaked on Mini; garnish locked in prompt + visual QA)
- Flow project: `https://flow.google.com/u/1/project/3c1c247d-6d70-4c9e-8af3-4ee78a04ae1f`
- Raw clip: `04_Generated-Clips/part04/raw/v08_fast/06_explorer_leaves_gap_v08.mp4`
  - bytes=1968748 · dur=8.00s · sha256=`efb69579fa84b18fa3f124167bf6bd8124fc79cf641096368d7c872c04048897`
  - unique vs v07 plate sha `ad93141401965cacac4dc2b430510166b669b23636e74ed6e98f855e5604fa29`

## Assembled cut
- Path: `09_Final-Export/hos_002_part04_rough_v08.mp4`
- iCloud HOS UAT: `~/Library/Mobile Documents/com~apple~CloudDocs/HOS UAT/hos_002_part04_rough_v08.mp4`
- bytes=87885278 · duration=127.760s
- sha256=`8cafb379af976897d6cee46484439b1ecbda56f8a42760327a96d1744d614a83`
- Explorer picture window: 45.30–53.20s

## Visual QA
- v07 @ ~48s: waist-up face-hero (REJECT) — `_qa_part04_v08_plate/v07_cut_explorer_t48_BAD.jpg`
- v08 @ ~48s: back/profile toy-scale teal garnish + glowing vacant seat; indoor bookcase; no window/sky/roofs — `_qa_part04_v08_plate/v08_cut_explorer_t48.jpg`
- Proof window clip: `_qa_part04_v08_plate/v08_explorer_window_proof.mp4` (45.3–53.3s)
- Cluster teal measure on raw stills: h_frac ≈ 0.09–0.18 (garnish). Loose auto gate false-positived on book spines; visual pass used.

## UAT notes
- Teal trenchcoat DNA present; this take adds a teal hat (not on sheet) — CoS may request hat-free remint.
- Empty-seat glow + cream card beat readable.
- No navy sky boxes / roofs / exterior window in the Explorer window.

## Scripts
- `_mint_part04_flow_v08.py`
- `_assemble_part04_rough_v08.py`
