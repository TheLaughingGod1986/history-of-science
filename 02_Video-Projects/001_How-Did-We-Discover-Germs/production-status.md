# Production status — 001 How Did We Discover Germs?

**Queue (27 Aug 2026):** This is the film to finish. Then one more HOS long. Then compare Veo vs Omni — do not rewrite Orbit Omni until that compare. `hos-finish-then-compare-omni.mdc`

| Step | Status |
|---|---|
| Topic score | DONE |
| Cluster plan | DONE |
| Pre-build VidIQ audit | SIGNED (live VidIQ re-score before upload) |
| Master script | `germs_script_master_v01.md` |
| Script / gate | **PASS 90.4** |
| Shorts cadence | Cluster 4–6 · **not daily** |
| Part 01 VO | DONE · Ben Orbit Narrator |
| Part 01 picture | **PASS — `hos_001_part01_rough_v08.mp4`** |
| Style / microbe / motion locks | **LOCKED** |
| Part 02 VO + stills | DONE |
| Part 02 picture | **10/10 Flow I2V** · ward beat **v04 remint** (locked cam) spliced into `hos_001_part02_rough_v04.mp4` (~76.4s). **STOP for Ben UAT** — watch **0:53–1:01**. Not agent PASS. |
| Parts 03–05 | Blocked until Ben passes Part 02 |
| Broadcast + Shorts | Later (Shorts only after long is public; zero `/go/` on Shorts) |

## Artifacts

- Part 01 locked: `/opt/cursor/artifacts/hos_001_part01_LOCKED_v08.mp4`
- Part 02 real plates: `04_Generated-Clips/part02/raw/v01_flow/` (**01–10**)
- Part 02 still-push (REJECT): `09_Final-Export/hos_001_part02_rough_v01_STILLPUSH_REJECT.mp4`
- Part 02 animated rough (baseline): `09_Final-Export/hos_001_part02_rough_v01.mp4`
- Part 02 **UAT cut:** `09_Final-Export/hos_001_part02_rough_v04.mp4` (ward 0:53–1:01 = `raw/v04_flow/08_ward_vs_lens_v04.mp4`)
- Do **not** splice `08_ward_vs_lens_v02` / `v03` again

## Quota (2026-08-28)

- **Gemini Veo API:** prepaid depleted (separate from Free Trial / GDP).
- **Flow Ultra:** plate **10** Lite I2V completed after Ben confirmed **52 credits**. Send-button bug (plus vs arrow) was why earlier retries sat at `gen=False` even with credits.

## Next

1. **Ben UAT** `hos_001_part02_rough_v04.mp4` (ward 0:53–1:01). Do not start Part 03 until pass.
2. After pass: write Part 03 script → VO → Lite plates one minute at a time.
3. Do not start HOS 002 or spend Omni on Neutron Star while this minute is open.
