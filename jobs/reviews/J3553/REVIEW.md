# Acting Chief Review & Ruling — `HOS:136` (`v01`, `J3553`)

- **Job:** `J3553` (`kind: review`, `HOS:136 script`, ref `J3507`)
- **Decision Maker:** `gemini` — **Elected Acting Chief** under Ben's 24 Nov 2026 Chief chain (`Claude → Codex → Gemini → Grok`; live `chief_relay.py status` at `2026-11-25T05:47Z`: `claude` down until `07:50Z`, `codex` down on usage limit until Nov 27, `gemini` UP as `Chief: Gemini`)
- **Date:** `2026-11-25` (UTC)
- **Film:** `HOS:136` — *Trinity Test Explained: Could It Ignite the Sky?* (Cluster 2 Film 2, target air Thu 17 Dec 2026 18:00 London; Ben's watch Mon 14 Dec; script lock due Fri 4 Dec)
- **Reviewed PRs & Commits:**
  - HOS PR `#746` (`macbook/J3502`, `b76eea6f`) — Rule-E Topic GO (`96.3/100`)
  - HOS PR `#753` (`gemini/J3507-hos136-script`, `ebb55eea`) — Package-first scoring, `v01` script, `SOURCES.md`, `FACT_NOTES_v01.md`, `SHORTS_SCRIPTS_v01.md`
  - HOS PR `#764` (`gemini/J3552-hos136-facts-audit`, `4afb106f`) — Independent Gemini `v01` facts audit (`01_Script/GEMINI_FACTS_CHECK_v01.md`: `13 OK / 2 PARTIAL / 8 FLAG`)
- **Verdict:** **FIX (NOT LOCKED)** — Do **NOT** lock `v01` and do **NOT** merge PR `#746`, `#753`, or `#764` as-is.
- **Spend & Publishing:** `£0.00` cash, `0` ElevenLabs / Flow / Vertex credits. No VO, no picture spend, no upload, no schedule change, no PR merged.

---

## 1. Exact Audited Input SHA-256 Hashes (`ebb55eea` / `4afb106f`)

```text
29be0f3a9b7eb6cf92de42a43b0200ac0d23d90ad5092c446f8bb7e3846d4cb9  01_Script/trinity_test_explained_script_master_v01.md
b1da1e1602a6883d1f022177a1134bcdf0b75acad784c220b1e4cbdd4c432edf  01_Script/SOURCES.md
fb50391b6c13df0b61e65038e54f91c253c71cd5976fd6d78b0028a8fb7309e1  01_Script/FACT_NOTES_v01.md
a8160c07a949625b9bc63fd2e0a2367ac10d70d870aa134d911bc026fe08b4d2  10_Shorts/SHORTS_SCRIPTS_v01.md
bcf98849bb6d4258070965a4add4e0b30580afd27e7cc9604d93a4ceea71ed96  11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md
```

---

## 2. Packaging Confirmation (Checklist Item 1 — Draft Concepts Only)

- **Long Titles Confirmed as Draft Lock Candidates (once `v02` clears):**
  - **Primary Arm A:** *Trinity Test Explained: Could It Ignite the Sky?* (`48c <= 50`, `96/100`, `0` collisions)
  - **T&C Arm B (plan title):** *Trinity Test Explained: The Calculation That Nearly Stopped the Bomb* (`68c <= 70`, `92/100`, `0` collisions)
  - **T&C Arm C:** *Trinity Test: The Calculation That Nearly Stopped It* (`52c`, `88/100`, `0` collisions)
  - Low-RPM trap `nuclear bomb` remains excluded across titles and metadata.
- **Shorts Titles Confirmed (Test B search-titled, Ben 7 Nov week compliant):**
  - **`S01`:** *Could the Trinity Test Have Ignited the Sky?* (`44c`, `0` collisions, Sat 19 Dec 11:30)
  - **`S02`:** *How Did Enrico Fermi Measure the Trinity Blast With Paper?* (`58c`, `0` collisions, Fri 18 Dec 11:30)
- **Thumbnail Concepts A & B Confirmed as Draft Concepts (NOT a rendered packaging PASS):**
  - **Thumb A:** `AIR ON FIRE?` (gold on `FIRE?`, `96/100`, §2.5 zero title-word repeat)
  - **Thumb B:** `MEASURED BY PAPER` (gold on `PAPER`, `93/100`, §2.5 zero title-word repeat)
  - **Build-time locks for Codex (`thumbnails` stage):** (1) §2.6 hand-verified equations — generate Thumb A's chalkboard blank/smudged with zero AI text and ink any `¹⁴N + ¹⁴N` symbol in code/edit clear of the left-edge `AIR ON FIRE?` serif band so the left third does not crowd at `168×94`; (2) confirm 2-way vs adding a 3rd variant per §2.9 at thumbnail build.

---

## 3. Formal Acting Chief FIX Ruling (Checklist Item 2 — 14 Blocking Fixes + 2 Polishes for `v02`)

Independently confirmed all 8 `J3552` blocking `FLAG`s (`PR #764`), both `R20` polishes, and all 6 editorial / Teach-on-Screen / opening-pacing / hygiene findings (`ADD-1`–`ADD-6`), including direct programmatic re-verification of Short word counts (`S01 = 55w / 21.4 s`, `S02 = 65w / 25.3 s` at `154 wpm`) and Part 01 opening timing (`L11+L15 = 40w / 15.6–16.0 s`, `L11–L19 = 76w / 29.6–30.4 s`, `L11–L27 = 122w / 47.5–48.8 s`):

### A. Blocking Facts & Source Fixes (`J3552`, `FLAG-1`–`FLAG-8` + `R20`)
1. **`FLAG-1`:** Remove bogus OSTI URL `4036390` (1964 R. M. Misra paper) and WAF-blocked `sgp.fas.org` from `SOURCES.md` & `FACT_NOTES` Row 7; cite the verified 22-page Wayback scan of declassified `LA-602` (`14 August 1946`, declassified `2-2-73`) + DOE OpenNet `trinity_safety.htm` + LANL/OSTI `1836991` (Katz 2021), and remove unbacked `OSTI/DOE` on `LA-602` from the draft description `Sources:` line.
2. **`FLAG-2`:** Remove unsourced `"a thousand times faster"` cooling ratio in Long Part 02 (`SCALE:` & spoken; contradicts `LA-602`'s worst-case `~1.6` minimum safety factor / `7.4` with inverse Compton in a 57 m sphere).
3. **`FLAG-3`:** Populate `FACT_NOTES` Row 3 with NASA Goddard Earth Fact Sheet verbatim quote (`78.08% Nitrogen (N2)`), Row 8 with verbatim `LA-602` PDF pp. 10 & 15–16 quotes, and Row 9 with CrossRef DOI `10.1080/00963402.1976.11455623` (Bethe June 1976) + opened, verifiable open-source verbatim quotes for Compton 1959 & Bethe 1976 (removing non-matching Wikipedia links).
4. **`FLAG-4`:** Fix Long Part 04 `VISUAL MUST: 5:03` — Bainbridge's countdown bunker was **`S-10000` (10,000 yards ≈ `5.7 miles / 9.1 km` south of Ground Zero)** per DOE OpenNet `trinity.htm`, NOT `"ten miles away"`. Keep `5:34` at Base Camp (`~10 miles`) clearly pre-shot.
5. **`FLAG-5`:** Fix Short `S02` `"for the silent shockwave to arrive"` → accurate phrasing (flash silent for ~40 s; blast wave arrived with a roar).
6. **`FLAG-6`:** Fix mathematically inverted light-speed analogy in Long Part 03 (`SCALE:` & spoken): light crosses a 100 m / 100 yd football field in `0.31–0.33 µs`, so `1 µs` is `~3× LONGER` (not shorter).
7. **`FLAG-7`:** Trim Shorts `S01` (`55w → 40–44w`) and `S02` (`65w → 40–44w`) in `10_Shorts/SHORTS_SCRIPTS_v02.md` to pass Ben's 19 Nov 2026 `16.0–19.0 s` house rule (verified programmatically), updating `status.json` and `production-status.md`.
8. **`FLAG-8`:** Replace spliced `FACT_NOTES` Row 10 Wikipedia `Edward_Teller` quote with verified DOE OpenNet `hans-bethe.html` verbatim quote.
9. **`R20` Polishes:** Unify Part 05 timeline span (`1942–1945` vs `1942–1946` / `August 1946 LA-602`) and tighten Chicago Pile-1 interval (`2 Dec 1942 → 16 Jul 1945` = `2 yr 7.5 mo` → `"Nearly three years"` / `"Two and a half years"`).

### B. Editorial, Teach-on-Screen, Opening-Pacing & Hygiene Fixes (`J3553`, `ADD-1`–`ADD-6`)
10. **`ADD-1` (`WHO:`):** Resolve **Cloyd Marvin** in Part 02 (add primary-verified `WHO:` + `FACT_NOTES` row, or refer cleanly to Konopinski and Teller's co-author/team if lifespan is not cleanly open-source verifiable); move **Arthur Compton's** `WHO:` card from Part 02 to his first spoken mention in Part 01.
11. **`ADD-2` (`WHEN:`):** Add `WHEN: 1959` (Part 02) and `WHEN: Los Alamos, 1943` (Part 03), and align `FACT_NOTES` markers.
12. **`ADD-3` (One card/label at a time):** Split stacked multi-card `[VISUAL MUST]` blocks in Parts 02–05 and interleave `[VISUAL MUST]` cues at their spoken beats (`studio/RULES.md` L70).
13. **`ADD-4` (Part 01 opening milestones):** Trim `L15` by 3–4 words (`<=0:15` proof/promise) and tighten `L19`'s 36-word agenda sentence by ~12–15 words into crisp stakes ending `<=0:24`, so early `DATA+SCALE` lands `0:25–0:35` and Berkeley July 1942 lands `<0:45`.
14. **`ADD-5` (`S02` overlay & §2.6):** Tighten `2.5 M SHIFT ≈ 10 KT` (6 tokens) to `<=4` words (e.g., `2.5m SHIFT ≈ 10 KT`) and mark `S02`'s `10,000 TONS TNT` cream pad as hand-verified edit ink.
15. **`ADD-6` (Single master filename & `LAUNCH_PLAN.md`):** Keep only `trinity_test_explained_script_master_v02.md` in `01_Script/` (removing `v01` so default `gate:episode` without `--script` scores `v02`, per `HOS:128` `J3630` `FIX-6`), and align `LAUNCH_PLAN.md` archive-credit note at upload lock.

---

## 4. Queued Follow-On Chain & Disposition (Checklist Item 3)

- **`J3675` (`kind: script`, due Mon 30 Nov 18:00):** Correct `HOS:136` script, `SOURCES.md`, `FACT_NOTES_v02.md`, and `SHORTS_SCRIPTS_v02.md` to `v02` off `origin/gemini/J3552-hos136-facts-audit` (`4afb106f`).
- **`J3676` (`kind: facts`, after `J3675`, due Wed 2 Dec 18:00):** Independent `v02` facts and exact-quote verification (`GEMINI_FACTS_CHECK_v02.md`).
- **`J3677` (`kind: review`, after `J3676`, due Fri 4 Dec 18:00):** Chief direct quote check and `v02` script lock decision (merges `v02` PR superseding `#746`/`#753`/`#764`, closes `J3553`, and queues `HOS:136` VO only under Rule G WIP rules).
- **`J3553` status:** Kept waiting on `J3677` (`jobs.py wait --type dependency`), mirroring `HOS:128` (`J3547` → `J3660`). Zero VO or picture spend until Chief `KEEP` lock.
