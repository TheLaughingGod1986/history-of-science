# P05 The Guests Arrive — BED-ONLY remaster → `hos_002_part05_rough_v02`

**GREEN 12 Sep 2026 (CoS):** bed dies last ~20s. loop130 = **135.000s**, cut = **147.310s**. Ben KEEP + music fix — Mini go. **RUN THIS FIRST** if Mini can only do one bed remaster at a time; then P04 v26.  
**Parent KEEP/LOCK picture:** `hos_002_part05_rough_v01.mp4` sha `8dcb06b596318a7283210928fbb0e78f6f89c7db5d200b8edeefbaa9b5522ec4`.  
**Scope:** **audio bed only** through end card. **No picture remint.** Explorer soft only.  
**Sibling GREEN:** `PART04_BED_ONLY_REMASTER_V26.md` (after this).  
**Do not touch** P01–P03. Scores → CoS. Ben ping only if watch needed after PASS.

---

## Do

1. Keep all video / labels / VO from v01 (fork `_assemble_part05_rough_v01.py` → v02 bed-only, or bed-swap remux).  
2. Extend workshop bed to cover **full 147.310s** (+ soft fade last ~1–2s):
   - Rebuild from `05_Music/hos_002_part01_curious_workshop_v02_norm.wav` → e.g. `…_loop150_norm.wav` ≥148s (or ffmpeg loop to vo_dur).  
   - Same `BED_VOL` as v01 (0.38). Curious/warm — not death-ward.  
3. Export `09_Final-Export/hos_002_part05_rough_v02.mp4` + sha + duration + bytes.  
4. iCloud `HOS UAT/hos_002_part05_rough_v02.mp4` + `WATCH_part05_v02.txt`.  
5. UAT audio gate: bed open through last ~20s / end card; VO clear; picture = v01.

---

## Do not

- Remint plates / Flow / paint / Explorer  
- HOLD or cancel this brief  
- Start Part 06  

---

## Paths

- Parent LOCK: `hos_002_part05_rough_v01.mp4`  
- Assemble ref: `_assemble_part05_rough_v01.py`  
- This brief: `PART05_BED_ONLY_REMASTER_V02.md`
