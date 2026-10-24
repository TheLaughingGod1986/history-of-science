# Production status — Dinosaurs (Alvarez and the clay line)

| Field | Value |
|---|---|
| Slug | `010_Alvarez-Clay-Line-Dinosaurs` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Dinosaurs** — Alvarez and the clay line (iridium / *Science* 1980 → Chicxulub after-act) |
| Stage | **Script PASS on main** (PR #208, review **92.1**). **FACT_NOTES + HARD_CHECKS + upload scaffold** this PR (write lane, desk #180 claim 5982333546). |
| Neighbour gate | **PASS** (4 Oct 2026): 10 education ≥1M; TED-Ed/TED yes. Evidence `11_Upload-Package/evidence_2026-10-04_neighbours.json` |
| Script review | `clay_script_master_v01.md` on main; **92.1 PASS** |
| FACT_NOTES | **this PR** — every new-claims row sourced; hard-checks 7/7 PASS |
| VO | **waits Claude** confirm on FACT_NOTES + HARD_CHECKS (Ben VO listen not required first once Claude PASSes) |
| Picture | **BOARDS v01, no mint** (J0314, 15 Oct). Flow-first price review in `07_Edit-Project/PRICE_REVIEW_v01.md`. Parked for Chief. |
| Runtime target | 7–9 min, 5 parts (house default) |
| Air (proposed) | Thu **3 Dec 2026** 18:00 UK (`2026-12-03T18:00:00.000Z`) — draft in PACKAGE_MANIFEST |
| Shorts | not outlined yet |

## 15 Oct 2026 — plate boards v01 (J0314)

The long VO is locked (Chief KEEP, desk #180 comment 6101773293). Plate boards are timed from that VO and priced Flow-first, the same table as 009 J0261. Flow expected **12,572** credits against **23,740** left (fits on its own). Vertex expected **£146.88** against **£70.02** usable (does not fit). 006–009 still share the Flow pot, so mint order is the Chief's call. Nothing in the boards is generation-authorised.

## STOP

- No Vertex/Veo/Flow minting on this film.
- No ElevenLabs VO until Claude confirms sourced FACT_NOTES + HARD_CHECKS.
- Do not merge or close desk PR #180 from this work.

## 24 Oct 2026 — J0909 (`J0899` Change 5): 2-way Title T&C launch plan, Shorts positive-question title + payoff-past-15s lock & `300× TOO MUCH` / `rumble_low` notes (Gemini covering)

- **Authority:** Chief PASS on `J0899` (`02_Video-Projects/_analytics/HOS_2026-10-24.md` §4 #5) and queue job `J0909`. `£0` spend, no live YouTube changes.
- **Applied to `11_Upload-Package/` and `10_Shorts/SHORTS_SCRIPTS_v02.md`:**
  1. **2-way Title Test & Compare on launch (`PACKAGE_MANIFEST.json` `titleAbc`, `LAUNCH_PLAN.md`, `PRE_BUILD_VIDIQ_AUDIT.md`):** Armed Variant A *What Killed the Dinosaurs Was Hidden in a Line of Clay* vs Variant B *How a 1-Centimetre Line of Clay Solved What Killed the Dinosaurs* (`64` chars, shares neighbour phrase `dinosaurs`).
  2. **Shorts positive-question titles + payoffs held past `15 s` (`10_Shorts/SHORTS_SCRIPTS_v02.md`, `LAUNCH_PLAN.md`, `PACKAGE_MANIFEST.json`):** Locked positive question titles on Short A (*What Killed the Dinosaurs?*, `24.16 s`) and Short C (*Are Birds Really Dinosaurs?*, `23.51 s`) with payoffs explicitly held past `15 s` (`15.0–23.8 s` on Short A and `15.1–23.2 s` on Short C, clear of the `9.0–14.0 s` promoted-long title banner).
  3. **Thumbnail cover text & Part 04 SFX note (`LAUNCH_PLAN.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, `PACKAGE_MANIFEST.json`):** Documented pairing **`300× TOO MUCH`** cover text with `sfx_kit.py` `rumble_low` on the Part 04 crater reveal.
- **Package lint (`npm run lint:package -- --film 010`):** `PASS  02_Video-Projects/010_Alvarez-Clay-Line-Dinosaurs/11_Upload-Package/PACKAGE_MANIFEST.json`.
