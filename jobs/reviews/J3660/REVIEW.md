# HOS 128 — `v03` Fix Verification & Acting Chief `KEEP` / Script Lock Ruling (`J3660`)

- **Job:** `J3660` (`kind: review`)
- **Acting Chief:** `gemini` (elected Acting Chief under `Claude -> Codex -> Gemini -> Grok` per Ben's 24 Nov 2026 order; verified via live `chief_relay.py status` = `Chief: Gemini` at session start `04:20Z` and immediately prior to every protected call at `04:23Z` and `04:25Z`)
- **Date:** `2026-11-25` (UTC)
- **Audited PR:** HOS PR `#762` (`gemini/J3659-hos128-v03`, head `9bc20d9c82913eea885b63960d2254e698cad8d3`, `MERGEABLE` / `CLEAN`, 7/7 GitHub CI checks green)
- **Ruling:** **`KEEP` & SCRIPT LOCKED**
- **Protected Actions Executed by Elected Acting Chief (`gemini`):**
  - Merged HOS PR `#762` into `main` as **`84af0f7d05701a5147d7ad7fb30403a0152e80ff`** (automatically superseding/merging PRs `#758`, `#760`, `#751`, and `#725`).
  - Updated `status.json` and `production-status.md` (`script`: `done`, `facts`: `done`, `shorts_scripts`: `done`, `vo` & `shorts_vo`: `todo` referencing queued VO jobs).
  - Queued HOS 128 long VO (**`J3670`**) and Shorts `S01`/`S02` VO (**`J3671`**) under normal ElevenLabs credit rules (Mac mini `el_client.py`/`vo_take.py`, floor `0`, check live balance first, never buy/top up, `vo_check_py312.sh` required).
  - Updated and closed original **`J3547`** as `done` (lock achieved).
  - **Spend / Scheduling:** **£0.00 / 0 credits spent**; nothing uploaded, scheduled, or altered on YouTube.
  - **Target & contingency preserved:** **Thu 10 Dec 2026, 18:00 London** target (normal publish, no Premiere; Shorts Fri 11 Dec / Sat 12 Dec 11:30 London) and **Mon 7 Dec → Thu 17 Dec** slip contingency.
  - **Packaging caveat preserved:** Draft thumbnail concepts (`WASTED AS HEAT`, `HIGH VOLTAGE`, optional `22 MILES AWAY`) remain **unrendered drafts (NOT rendered packaging PASS)**; picture and thumbnail generation continue to wait for Chief VO PASS.

---

## 1. Exact Locked `v03` SHA-256 Hashes (Independently Verified on `9bc20d9c` / Merged `84af0f7d`)

All 8 hashes independently recomputed on a clean detached worktree at `9bc20d9c82913eea885b63960d2254e698cad8d3` — **8/8 EXACT MATCH**:

```text
c389c3cfbf758f5f261103bc6aa174cdb85dcc6f48c7e546f50ae63c98d3bb8b  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/01_Script/edison_tesla_ac_dc_script_master_v03.md
4104ad2d77769bab6b1bd0cef35e760a1ecccd7430b0ccf50fea8b402fe08474  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/01_Script/FACT_NOTES_v03.md
be44dd42e2bdfefb5e3c1b82866ca3fdb6790331e05fe24bc9059672495a9379  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/01_Script/SOURCES.md
1132ad9f8b44d4e545f699bf702b83894370effb34afe37ce12b25a2080694e7  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/10_Shorts/SHORTS_SCRIPTS_v03.md
c1dad1fed48f2705aa898a021e331e1ceccc1f2b60ee2b099e7acf910dd0d816  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/11_Upload-Package/PACKAGE_FIRST_SCORING_v03.md
d368e59111adfcfdb22253ac7aa8b9a4b345367f62033fbdc2b3ccd8c277bfbc  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/11_Upload-Package/evidence_2026-11-25_public_search_arm_b.json
92de6faed0b0300d2f1b4f88df316c3af9277e38e05723efc55f7839fd7ce502  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md
4bcab7b579cf8ccb9f6502853148c6ebb6c82ef6cce2193bd58a4db8a3fe7797  02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/11_Upload-Package/LAUNCH_PLAN.md
```

---

## 2. Independent Verification Matrix — All 6 `J3630` Blocking Fixes + 3 Minor Polishes

| Item | Requirement (`J3630` / PR `#761`) | Independent `v03` Audit Result | Status |
|---|---|---|---|
| **`FIX-1`** | Edison age at Holborn Viaduct (12 Jan 1882, born 11 Feb 1847 → 34, not 35) | Long Part 01 L21 reads `"Eight months earlier, thirty-four-year-old Edison had proved the concept under London's Holborn Viaduct."` Aligned across `FACT_NOTES_v03.md` Row 3, `SOURCES.md`, and `PRE_BUILD_VIDIQ_AUDIT.md`. | **PASS** |
| **`FIX-2`** | Galileo Ferraris date & verb (presented 18 March 1888 in Turin; published April 1888) | Long Part 03 L87 reads `"On the eighteenth of March, eighteen eighty-eight, Italian physics professor Galileo Ferraris presented the same rotating-field discovery in Turin — yet never patented his work."` L90 reads `"Ferraris's Turin lecture paper"` and `WHEN: Turin, 18 March 1888`. Aligned across `FACT_NOTES_v03.md` Row 11, `SOURCES.md`, and `PRE_BUILD_VIDIQ_AUDIT.md`. | **PASS** |
| **`FIX-3`** | `FACT_NOTES` Row 8 William Stanley Jr. birthdate verbatim | Corrected to exact live ETHW verbatim `"William Stanley was born in Brooklyn, New York, 22 November 1858"`. | **PASS** |
| **`FIX-4`** | `FACT_NOTES` Row 10 + Row 2 `[...]` ellipsis + 6 primary institutional upgrades + Niagara ruling | Row 10 replaced with verbatim USPTO `US381968A` + Sylvanus P. Thompson (`"no commutator or connection of any kind with the armature was required"`). Row 2 includes `[...]` ellipsis and boiler/steam-engine quote. All 6 verified primary institutional upgrades folded (`Rutgers` Edison death `18 Oct 1931` & `1888` Brown experiments, `ETHW` Westinghouse death `1914/03/12`, `Library of Congress` Kemmler `6 Aug 1890`, `UK SI 2002/2665 Reg. 27` `50 Hz / 230 V`, `US DOE Electricity 101` `110-120V / 60 Hz`). Acting Chief `J3630` Niagara ruling (NPS NRIS `75001212` `22 miles` / `15 Nov 1896` with ETHW `20 miles` / US DOE `Nov. 16` variance) logged. | **PASS** |
| **`FIX-5`** | Candidate Arm B `public_search.py` collision check & honest draft status | `evidence_2026-11-25_public_search_arm_b.json` saved (`0` exact collisions across 8 GB YouTube results, `2026-11-25`). Reflected in `PACKAGE_FIRST_SCORING_v03.md`, `PRE_BUILD_VIDIQ_AUDIT.md`, and `LAUNCH_PLAN.md`. Thumbnails explicitly preserved as unrendered drafts (not rendered packaging PASS). | **PASS** |
| **`FIX-6`** | Single `master` filename (`STUDIO_PLAYBOOK.md` §3 L85) | `01_Script/` contains solely `edison_tesla_ac_dc_script_master_v03.md` matching `*master*.md`; superseded `v01`/`v02` renamed to `_draft.md`. Default `gate:episode` (WITHOUT `--script`) selects `edison_tesla_ac_dc_script_master_v03.md` and PASSes. | **PASS** |
| **Polish (a)** | Part 01 L19 Pearl Street visual note accuracy | Reads `"six giant iron dynamos driven by coal-fired steam engines"`. | **PASS** |
| **Polish (b)** | Part 06 L161 `DATA` #6 card aligned strictly to spoken numbers | Unspoken `120 V` / `230 V` removed from card; aligned strictly to spoken `50 or 60 cycles per second`. | **PASS** |
| **Polish (c)** | Short `S02` overlay window `TESLA PATENT · 1888` | Shifted `6.0-8.6 s` → `6.4-8.6 s` in `SHORTS_SCRIPTS_v03.md`, aligned to 6.4 s spoken line and strictly clear of `9.0-14.0 s` title row. | **PASS** |
| **Zero unverified claims** | Exact `v02` → `v03` spoken diff check | Only spoken changes are the J3629/J3630-verified `FIX-1` (`thirty-four-year-old`) and `FIX-2` (`eighteenth of March ... presented`). Zero new unverified claims in long or Shorts. | **PASS** |

---

## 3. Fresh Independent Gate Outputs (`9bc20d9c`, `2026-11-25`)

- **Teach / Polish / Craft markers on `edison_tesla_ac_dc_script_master_v03.md`:** `DATA: 6` · `SCALE: 6` · `WHO: 7` · `WHEN: 14` · `FACT: 4` · `VISUAL MUST: 41` · `TEACH: 6` · `CHAPTER CARD: 5` · `EXPLORER ACTS: 2` (outside first minute).
- **`npm run review:script -- --file ../02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC/01_Script/edison_tesla_ac_dc_script_master_v03.md`:** **PASS · 91.9 / 100** (`Words: 1314 · Est. min: 8.8 · Chapters: 5 · Structure gates 8/8`).
- **Default `npm run gate:episode -- --project ../02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC` (WITHOUT `--script`):** **PASS — VO / Gemini Veo allowed**, selecting `01_Script/edison_tesla_ac_dc_script_master_v03.md` (`9/9 OK`).
- **`bash 00_Brand/Channel-Setup/tools/check_all.sh 02_Video-Projects/128_Edison-Tesla-Westinghouse-Why-Do-We-Use-AC-Instead-Of-DC`:** **ALL CHECKS PASS** (`12/12 PASS`).

---

## 4. Next Production Steps (Queued)

1. **`J3670`** — HOS 128 long VO (6 parts from locked `edison_tesla_ac_dc_script_master_v03.md`, `c389c3cf...`, Mac mini `el_client.py`/`vo_take.py`, `vo_check_py312.sh`).
2. **`J3671`** — HOS 128 Shorts `S01` & `S02` VO (from locked `SHORTS_SCRIPTS_v03.md`, `1132ad9f...`, 16–19 s band, Mac mini `el_client.py`/`vo_take.py`, `vo_check_py312.sh`).
3. Picture generation (`Flow Veo 3.1`) and rendered thumbnail design/panel remain **strictly blocked until Chief VO PASS**.
