# J2174 — HOS 005 `s06_blood_pressure_cuff` Bounded Rule-8 Opening & Clinical-Source Repair Decision (5 November 2026)

- **Worker:** `gemini` (`gemini-4-argon-high`, fallback lane 3 of 4 under `J2174`, ref `J2168`)
- **Scope:** £0, max 20-minute bounded editorial, source, and EDL decision. Zero generation, zero new VO, zero spend, zero YouTube/Studio writes, zero Buffer writes, zero `awaits`.
- **Verdict:** **NO-GO for £0 unchanged-word assembly (`v02` not queued).** No contiguous or non-invented unchanged-word slice of `02_Voiceover/part05_the_vessels_he_never_saw_v01_raw.mp3` can satisfy `LEARNINGS.md` Rule 8 (and Rules 2, 3, 6, 7) plus the HOS `22.0–27.0 s` / `55–65` word contract without either (a) inventing unapproved out-of-order sentence splicing that leaves an unresolved pronoun at `0.0 s` and violates the `≥70%` payoff-start lock, or (b) recording a dedicated Short VO take and adding modern-cuff visual coverage. Conditional slot **10 November 11:30** and **10 December** (`s07_heart_pulse_v01` rejected in `J2168` for `BW_CFAX-mxc` pump/stove premise overlap; `s08_capillaries_v01` excluded for `Wvjd8g0CpzE` overlap; no extra `007` Short) remain **unfilled**.

---

## 1. Authoritative Clinical-Method Source Repair (`01_Script/FACT_NOTES_v01.md` Row 38)

`01_Script/FACT_NOTES_v01.md` row 38 previously cited only `"Any clinical-methods text."` It has been repaired in git with the primary American Heart Association (AHA) Scientific Statement on human blood pressure measurement, distinguishing **manual auscultatory sphygmomanometry** (which literally *listens* for acoustic Korotkoff sounds as blood flow resumes after brachial artery occlusion—matching the locked script line) from **automated oscillometric cuffs** (which sense arterial pressure oscillations in the cuff bladder and compute systolic/diastolic values algorithmically without listening for sound):

- **Citation:** Thomas G. Pickering, John E. Hall, Lawrence J. Appel, Bonita E. Falkner, John W. Graves, Martha N. Hill, Daniel W. Jones, Theodore Kurtz, Sheldon G. Sheps, and Edward J. Roccella, *"Recommendations for Blood Pressure Measurement in Humans: An AHA Scientific Statement from the Council on High Blood Pressure Research Professional and Public Education Subcommittee"*, *The Journal of Clinical Hypertension* 7(2):102–109 (2005), DOI `10.1111/j.1524-6175.2005.04377.x`, PMID `15722655`.
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8109470/
- **Exact quote — Manual Auscultatory Method (Korotkoff, 1905):**
  > *"The brachial artery is occluded by a cuff placed around the upper arm and inflated to above systolic pressure. As it is gradually deflated pulsatile blood flow is reestablished and accompanied by sounds that can be detected by a stethoscope held over the brachial artery just below the cuff. The onset of phase I of the Korotkoff sounds (tapping sounds corresponding to the appearance of a palpable pulse) corresponds to systolic pressure, but tends to underestimate the systolic pressure recorded by direct intra‐arterial measurement."*
- **Exact quote — Automated Oscillometric Technique:**
  > *"When the oscillations of pressure in a sphygmomanometer cuff are recorded during gradual deflation, the point of maximal oscillation corresponds to the mean intra‐arterial pressure. The oscillations begin above systolic BP and continue below diastolic BP, so that systolic and diastolic BPs can only be estimated indirectly according to some empirically derived algorithm. One advantage of the method is that no transducer needs to be placed over the brachial artery, so placement of the cuff is not critical."*
- **Editorial consequence for any future cuff Short:** The locked line (*"It squeezes until the blood stops getting in, then lets go, and listens for the moment it starts to flow again"*) describes **manual auscultatory measurement** (occluding the brachial artery above systolic pressure, then listening with a stethoscope over the antecubital fossa for Phase I Korotkoff sounds when intermittent flow returns), not an automated home oscillometric cuff that measures cuff-wall pressure oscillations around mean arterial pressure. Any visual or script repair must depict or specify manual stethoscope auscultation (or explicitly contrast manual auscultation with oscillometric sensing) so picture and mechanism match the clinical source.

---

## 2. Word-Level Proof: Why Approved Unchanged Words Cannot Form a Compliant Rule-8 Opening

In the locked long script (`01_Script/blood_script_master_v02.md`, Part 05 line 157) and aligned raw VO (`02_Voiceover/part05_the_vessels_he_never_saw_v01_raw_align.json`, sha256 `8313148b80400f47134c8690104985b08643b5dfcbbbb7cff10545dcec9056a0`), the **entire blood-pressure cuff passage** is 3 sentences totalling **43 words** and **14.700 s** raw (`80.740–95.440 s`, word indices `178–220`; `14.513 s` with pauses capped at `0.45 s`):

| Word indices | Raw time (s) | Raw dur (s) | Words | Verbatim locked text |
|---|---|---|---|---|
| `178–192` | `80.740–85.200` | `4.460` | 15 | *"And the next time a nurse wraps a cuff round your arm, think of Harvey."* |
| `193–199` | `85.560–88.080` | `2.520` | 7 | *"A blood pressure cuff is his band."* |
| `200–220` | `88.267–95.440` | `7.173` | 21 | *"It squeezes until the blood stops getting in, then lets go, and listens for the moment it starts to flow again."* |

Testing every possible unchanged-word window proves why no £0 edit is lawful:

1. **Candidate A — Existing `v01` lift (`107–126` + `178–220`, 63 words, `23.667 s` VO):**
   - Opens on `107–126` (`0.000–8.304 s`, 20 words): *"Your blood leaves your heart, runs out through your arteries, crosses through the capillaries, and comes home through your veins."*
   - **Fails `LEARNINGS.md` Rule 2 & Rule 8:** Sentence 1 names neither the subject (*blood pressure cuff*) nor a cuff surprise; `"cuff"` is first spoken at word 28 (`~10.81 s`), and swapping `13_cuff_t1.mp4` onto `0.0–2.458 s` would violate `CHANNEL_AUTHORITY.md` (*"picture matches the words"*) while still failing the spoken sentence-1 gate.
2. **Candidate B — Start at the cuff paragraph (`178–220`, starting *"And the next time a nurse wraps a cuff round your arm, think of Harvey."*):**
   - **Fails `LEARNINGS.md` Rule 2 & Rule 8:** Sentence 1 begins with a conversational continuation conjunction (`"And the next time..."`), delays `"cuff"` until `2.044–2.300 s > 1.50 s`, and states no surprise claim in sentence 1 (`"think of Harvey"` ends at `4.460 s`).
   - **Fails HOS duration & word locks:** `178–220` alone is **43 words** and **14.513 s** VO (`15.513 s` with a `1.0 s` loop tail, outside `55–65` words and `22.0–27.0 s`).
   - **Fails if extended into `221–251`** (*"A sum, a band, and a row of little doors. Harvey proved that your heart is a pump and that your blood goes round, long before anyone saw the last link."*, +31 words / `11.840 s`): total word count becomes **74 words** (exceeding the `65`-word cap), the cuff measurement mechanism (`200–220`) finishes at `14.51 s` (`54% < 70%` of runtime, failing `LEARNINGS.md` Rule 6 payoff-start withholding), and the final `11.8 s` reverts to a generic summary of Harvey's 1628 film instead of centering the modern measurement mechanism.
3. **Candidate C — Start at Sentence B (`193–220`, starting *"A blood pressure cuff is his band."*):**
   - **Fails `LEARNINGS.md` Rule 2:** Without `178–192` before it, `"his band"` at `1.620–2.520 s` is an unresolved anaphoric pronoun (`"his"` has no antecedent at `0.0 s`, violating *"never a mid-chapter Long lift with pronoun/anaphoric/chronological setup"*).
   - **Fails HOS duration & word locks:** `193–220` alone is **28 words** and **9.880 s** VO.
   - **Barred from non-chronological sentence splicing:** Prepending `193–220` and then splicing earlier sentences (`107–126` or `178–192`) *after* `199` or `220` would invent an unapproved out-of-order sentence splice (prohibited by `J2174`: *"Prove a subject-plus-surprise opening from approved unchanged words, or state precise additional approved input/no-go; never invent splice/line approval"*), and still either places the payoff at `2.52–9.88 s` (`< 70%`, failing `LEARNINGS.md` Rule 6) or leaves `"his band"` pronoun-broken at `0.0 s`.

---

## 3. Exact Missing Approved Inputs Required Before Any Future `v02` Build

If Chief later elects to scope a paid/new-input build for `s06_blood_pressure_cuff_v02` (instead of leaving the slot unfilled), the exact missing inputs and recipe locks are:

1. **Missing Input 1 — Approved standalone Short script (`58–62` words) and new ElevenLabs VO take (`04_Audio/tools/vo_take.py`, Ben Orbit Narrator):**
   - **Title:** `How Does a Blood Pressure Cuff Work?` (positive question, verified signed-out GB YouTube autocomplete hit).
   - **Sentence 1 (`0.00–2.80 s`, `≤0.15 s` VO onset, subject + surprise by `1.50 s`, no anaphoric pronoun):** Must name the blood pressure cuff and state the surprise claim directly (e.g., *"A blood pressure cuff works by stopping the blood in your arm completely."*).
   - **Bridge across the `4–5 s` seam (`LEARNINGS.md` Rule 7, `<0.25 s` breath, no meta-promise):** Connect directly to William Harvey's 1628 arterial-inflow / venous-occlusion proof without retelling the full Part 04 hand-swelling sequence used by `PFj6172YU4Q`.
   - **Payoff withheld to `≥70%` of runtime (`LEARNINGS.md` Rule 6, starting at `~16.5–18.5 s` of a `23.5–25.0 s` cut):** Explain the manual auscultatory measurement step sourced in `FACT_NOTES_v01.md`—inflating above systolic pressure to occlude the brachial artery, then deflating while listening with a stethoscope for the first Korotkoff tapping sounds as pulsatile blood flow returns—and close with a loop-ready line into sentence 1.
2. **Missing Input 2 — Distinct modern-measurement visual coverage (`04_Generated-Clips/` or house-style code graphic):**
   - Current Part 05 holds only two 8.0 s modern-cuff plates (`13_cuff_t1.mp4` and `14_cuff_release_t1..t4.mp4`). Under `LEARNINGS.md` Rule 3 (`change something every 2.5–4 s`, max hold `≤3.8 s`) and `picture_qa.py` (no non-adjacent plate reuse within `10 s`), filling a `23–25 s` cuff Short without reusing Part 04 ligature plates from `PFj6172YU4Q` requires **2–3 additional shots** (either house-style inked anatomical/pressure-gauge diagrams on period paper built at £0 by `--kind chart`, or Chief-scoped Flow Veo 3.1 plates of brachial-artery occlusion and stethoscope auscultation).
3. **Mandatory Recipe & Gate Locks for Any Future `v02` Assembly:**
   - **Frame 0 (`0.0–2.8 s`, first cut `≤3.0 s`):** Moving `13_cuff_t1.mp4` (`in_s=1.00, crop_x=420`, `frame0_diff_0_1_5s ≥ 1.50`, `frame0_black ≤ 0.30`), concrete 2–3 word hook caption `STOPS YOUR **BLOOD**` or `SQUEEZES IT **SHUT**` (yellow hook word, never abstract `HIS BAND TODAY`).
   - **9–14 s parent-title banner (`LEARNINGS.md` Rule 6):** Exact live long title `The Tied Arm That Proved Your Blood Circulates` at `9.0–14.0 s` over top shaded band; spoken payoff must NOT start inside `9.0–14.0 s`.
   - **Single educational overlay (`AGENTS.md` *Teach on screen*):** At most **one** overlay in the Short (e.g., `WILLIAM HARVEY · London, 1628` or `NIKOLAI KOROTKOFF · 1905` in lower third of the 16:9 centre band `[656, 1264]`, `3.0–3.5 s` hold, fading `0.35 s`, clear of `0.0–2.0 s`, `9.0–14.0 s`, and the final `2.0 s`), with one ink-tick SFX (`sfx_hos_tick_ink_v01.wav`).
   - **Loop tail (`LEARNINGS.md` Rule 3):** `1.00 s` (`≤1.50 s`) return to opening plate `13_cuff_t1.mp4` (`in_s = F0_IN - 1.00`), **`no_cta: true` (no `"watch the full film →"` text or end-card in the last `2.0 s`)**.
   - **Audio & QA gates:** Dedicated synthesized/approved bed (`music_gate.py` PASS) + house SFX stem (`sfx_kit.py level` PASS), AAC mastered to `-14.0 ± 0.5 LUFS` and true peak `≤ -1.6 dBTP`, passing `gate_shorts_open.py check`, `vo_check.py`, `polish_gate.py`, and `picture_qa.py`, with hash-verified copies to NAS and iCloud UAT before any `awaits` card is set.
