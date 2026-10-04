# HOS 006 Part 02 — twin-FAIL decisions (Grok, 4 Oct 2026)

Authority: Claude #180 **5981276239**. **No Vertex re-roll** on any of these.

## `07_explorer_snow` — CUT
- t1 + t2 both FAIL (no real snow / twin stop).
- `06_garden_years` **t2 KEEP** already has snow covering the garden-years line.
- Board: `07` marked `cut: true`, `use_s: 0`.
- Board: `06` `use_s` extended **6.98 → 7.90** (`clip_use_s`) so the KEEP take covers as far into `07`'s VO land (`t_s=97.47`, was `use_s=5.38`) as the 8 s clip allows.
- Rough: hold/ease the last frames of `06` if the VO still needs a beat after 7.90 s; do not remint Explorer snow.

## `08_haul_tree` — TRIM t1 → UAT (not park)
Frame inspect (`_evidence/haul_tree_inspect_20261004/`):

| Take | Tree present | Vanish | Clean window |
|---|---|---|---|
| t1 | ~0–5.0 s | ~6.0 s floating / 7.5 s leaves only, man exits | **≥3 s** (use **0.00–4.80**) |
| t2 | ~0–4.0 s | gone by 5.0 s | **≥3 s** (0.00–3.80 spare) |

- Primary: **t1 trimmed** `in=0.00 out=4.80` → `04_Generated-Clips/part02/raw/v01_trim/08_haul_tree_t1_trim_0to4p8.mp4` (mp4 gitignored; path noted for edit).
- Quad for the trim posted under `_desk/006/uat_pending/` with the PENDING set.
- If Claude FAILs the trim: park one Tuesday retry with lock prompt: **"tree stays on the balance pan for the whole shot, no one leaves frame"** on whichever free route covers it.

## `02_balance_200` — PARK (Tuesday Flow)
- t1 + t2 FAIL (pot never on pan). No characters → **Flow** slot after Tuesday reset (Quality if credits allow); pot on pan in the start still.
- Until then: hold **`09_weights_169`** KEEP balance composition as rough stand-in.
- No Vertex re-roll now.
