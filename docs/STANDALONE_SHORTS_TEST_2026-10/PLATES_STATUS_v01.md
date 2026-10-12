# Standalone Shorts S1–S4: still plates v01 (J0203, Cursor, 12 Oct 2026)

Chief ruling (a), HOS #180 re 6131173528: purpose-built stills on Vertex `gemini-2.5-flash-image`, 9:16 (1080×1920), no Flow, no Veo. Assembly (J0171) moves them with a gentle push.

- **Script:** `_mint_plates_v01.py` (prompts inside, one row per plate). **Log:** `PLATES_MINT_LOG_v01.json` (full prompt, time and cost per still).
- **Media (gitignored, Mini only):** `plates_v01/s1…s4/*_v01.jpg`, contact sheets `plates_v01/s{1..4}_sheet_v01.jpg`.
- **Spend:** 20 stills × $0.039 = $0.78 ≈ £0.62. Vertex Free Trial read £1.46 before and after (console lags); conservative estimate after ≈ £0.63 (J0160 plateau £4.93 − £3.68 logged − £0.62). Floor £0.10 never approached. Logged in OWB `ai_spend.py` (pool vertex, film HOS:standalone).

| Short | Plates (5 each, in VO order) | Flag for Chief's KEEP |
|---|---|---|
| S1 Herschel infrared | beyond red · prism at window · thermometers in colours · past the red · invisible glow | 05 heat shimmer reads like smoke/flame |
| S2 Brand phosphorus | glowing flask · Hamburg lab · black sludge · no gold · first glow | Brand's face and age change between plates (02 bearded, 03 young clean-shaven) |
| S3 Snow / Broad Street | pump (hook) · Soho 1854 · Snow tracking · map with bars (no lettering) · handle off | 05 the pump still appears to carry a handle while Snow holds one |
| S4 Curie notebooks | lead box (hook) · shed lab 1898 · glowing vials · bare hands · Paris archive | none |

## Chief FAIL retakes v02 (J0171, Cursor, 12 Oct 2026 ~20:55 London)

Chief KEEP/FAIL: HOS #180 6131411243 (KEEP S1 01–04, S2 01–02, S3 01–04, S4 01–05; FAIL S1-05, S2-03/04/05, S3-05; hold J0171 until the FAILs land). One retake each: `_mint_plates_v01.py --retake` (S2 retakes take S2-02 as the face and apron lock). 5 × $0.039 ≈ £0.16; Vertex console £1.46 (lagging), conservative est after ≈ £0.47. Sheet: `plates_v01/retakes_sheet_v02.jpg` (S2-02 reference, then the five v02s).

| Plate | v02 | Cursor's check (Chief decides) |
|---|---|---|
| S1-05 invisible glow | `s1/05_invisible_glow_v02.jpg` | **Fails again:** model returned a letterboxed frame (black bands top and bottom, about half the frame near-black) and the heat still reads as wavy smoke lines. Suggest no third take: close S1 on plate 01 (the hook frame), which the loop rule asks for anyway. |
| S2-03 black sludge | `s2/03_black_sludge_v02.jpg` | Same man as S2-02 (beard, apron, no glasses). OK. |
| S2-04 no gold | `s2/04_no_gold_v02.jpg` | Same man; composition close to S2-02, but the empty crucible reads. OK. |
| S2-05 first glow | `s2/05_first_glow_v02.jpg` | Same man, face lit green by the dish. OK. |
| S3-05 handle off | `s3/05_handle_off_v02.jpg` | **Fails again:** the pump still has its curved handle fixed on, and Snow holds a second one. Options: one more take with a prompt showing the bare pump only, nobody holding anything (~£0.03), or close S3 on 04 (map) then 01 (pump, loop). |

Next (v01 note): Chief KEEP/FAIL per plate; a FAIL gets one re-take (~£0.03) or a public-domain fill. Then J0171 assembles S1–S4 (pause-trim VO ~0.4 s on S1/S4). S5–S8 need their VO, then a follow-on plates job, before J0171 covers them.

## Chief rulings applied + S1–S4 v01 assembled (J0171, Cursor, 12 Oct 2026 ~21:30 London)

Rulings HOS #180 6131594106: KEEP S2-03/04/05 v02; S1-05 dropped (S1 runs 01–04, loops to 01); S3-05 one last take.

- **S3-05 v03** (`s3/05_handle_off_v03.jpg`, `--retake-v03`): the bare pump alone on the cobbles, a bolt hole where the handle was, no person, nothing held. Cursor's check: no handle on the pump. Used as S3's "handle taken off" beat. ~£0.03 Vertex trial (console £1.46 lagging; est after ≈ £0.44).
- **Bed:** `music_v01/hos-standalone-shorts_score_bed_v01.mp3`, 45 s, ElevenLabs music_v2, brief in `music_v01/MUSIC_PROMPT_v01.md` (Pace 72–84, NOT list). ~620 credits est (6,557 before; cap 1,500). Same bed under all four.
- **SFX:** HOS house kit `sfx_kit_v01/` (own synthesis): soft whoosh on frame 0, ink tick on each plate change.
- **Assembler:** `_assemble_standalone_shorts_v01.py` → `shorts_v01/hos_sa_<id>_v01.mp4` (gitignored), index `SHORTS_INDEX_v01.json`, sheet `shorts_v01/contact_sheet_v01.jpg`.

| Short | Length | VO pause trim | gate_shorts_open |
|---|---|---|---|
| S1 Herschel | 22.43 s | 2.02 s (gaps capped at 0.4 s) | PASS, motion 11.9 |
| S2 Brand | 22.97 s | none | PASS, motion 13.4 |
| S3 Snow | 22.17 s | none | PASS, motion 17.7 |
| S4 Curie | 22.63 s | 1.84 s | PASS, motion 16.7 |

Open for Chief: the hook block sits high (S2's four lines start near the top edge; S3's touches the pump handle on frame 0); no long-title or end card (SCRIPTS_v02); no overlay used; `sfx_kit.py level` not run (stems not kept separately in v01); custom covers not built yet. S5–S8 wait on their VO and plates.

## S5–S8 still plates v01 (J0214, Cursor, 12 Oct 2026 ~23:30 London)

Same method as J0203 (Chief ruling (a)): `_mint_plates_v01.py` rows `s5`–`s8`, logged in `PLATES_MINT_LOG_v01.json` (`"job": "J0214"`). Beats from SCRIPTS_v01 as amended by SCRIPTS_v02. S5's VO kept "blamed on pigeons", so the caption is BLAMED THE **PIGEONS**. Face lock: each later plate with a person takes that person's first plate as Image 2 (`LOCKS`).

- **Spend:** 18 stills × $0.039 ≈ £0.56. Vertex Free Trial live reading £0.70 (22:23Z, `j0214_before`), nothing logged since; est after ≈ £0.14, above the £0.10 margin. 20 stills (£0.62) would have gone under it, so **S7 and S8 run 4 plates** and loop to 01. J0107 is done. Logged in OWB `ai_spend.py` (pool vertex, film HOS:standalone).
- **Media (gitignored, Mini only):** `plates_v01/s5…s8/*_v01.jpg`, sheets `plates_v01/s{5..8}_sheet_v01.jpg`.

| Short | Plates (VO order) | Cursor's flags (Chief decides KEEP/FAIL) |
|---|---|---|
| S5 Penzias pigeons | pigeons leave horn (hook) · receiver, needle · nests inside horn · still the noise · every direction | 04 copies 02's framing almost exactly (only a broom added), so it reads as a repeat; the assembler can push differently or drop 04. Same faces in 02/04. |
| S6 Fleming mould | mouldy dish on stacked dishes (hook) · back from holiday · fuzzy mould at window · clear ring · medicine vials (blank labels) | 04: the ring with no colonies around the mould is there but faint; the mould is olive, not blue-green. Fleming wears glasses in 03 only. |
| S7 Priestley mint | candle dying in jar in water (hook) · Priestley lowers jar · mint under rim · fresh candle bright | 03 copies 02's framing and the candle is **still lit** (the line says it burnt out). Never shows or says oxygen. |
| S8 Hales blood | tall tube on barn wall (hook) · Hales sketching a heart (no text) · calm mare, tube by her · column above Hales's head | none. No blood outside the tube, no procedure shown. |

Next: Chief KEEP/FAIL per plate; a FAIL gets one retake (~£0.03 each, est ≈ £0.14 left, so at most one or two before the £0.10 margin) or a reuse/drop. Then J0171 assembles S5–S8.

### Chief rulings (HOS #180, 22:33Z and 22:34Z) and the S7-03 retake check (Cursor, 12 Oct ~23:45 London)

- **KEEP:** S5 01, 02, 03, 05 · S6 01–05 · S7 01, 02, 04 · S8 01–04.
- **S5-04: DROP.** S5 runs 01 · 02 · 03 · 05, looping to 01. "Still the noise" sits on S5-02 with a different, tighter push on the needle dial.
- **S6-04:** KEEP, with a slow push-in centred on the mould so the clear band fills the frame.
- **S7-03: FAIL** (the candle is still lit). One retake was allowed only if the estimate stayed at or above £0.10. **Retake skipped, nothing spent.** The console read £0.67 at 22:43Z (`j0214_s7retake`), down only £0.03 since 22:23Z, while J0214 logged £0.56 at 22:29Z. The conservative estimate is ≈ £0.11, and a £0.031 take would leave ≈ £0.08, under the margin (billing account is a Paid account). The console also dropped £0.20 between 21:15Z and 22:23Z with only £0.03 logged, so the lag isn't reliable.
- **S7 in J0171:** use Chief's no-spend crop from the 22:33Z ruling. That's a 1.5× top-anchored push-in on S7-03 that keeps Priestley's head and the mint and finishes above the flame and the jar rim (the flame sits at ~73% of frame height, so the crop ends by ~67%). Log it as `crop_no_flame`. If the crop still shows the flame or looks soft at 1080×1920, drop 03 and run S7 01 → 02 → 04, looping to 01, per the 22:34Z ruling. A retake waits for a fresh balance that clears the margin.

### S7-03 retake v02 (J0215, Cursor, 13 Oct 00:06 London)

- **Credit:** pool read £76.06 at 23:06Z (Dev Program £75.39 + Free Trial £0.67), usable £75.06 after the £1 margin. Run capped at £0.10.
- **One take, £0.03:** `plates_v01/s7/03_mint_sprig_v02.jpg` (gitignored; Priestley face-locked to S7-02 v01). The prompt asked for a tight close-up on the hands at the jar rim and a burnt-out candle with no flame.
- **Cursor's flags (Chief decides KEEP/FAIL):** a **small flame is still visible** on the wick, below a smoke wisp. The mint floats inside the jar rather than being slipped under the rim. The framing is mid-shot, tighter than 02 but not the close-up asked for. The face, wig and coat match S7-02.
- **No second take** (the brief allows one). If it FAILs, the 22:33Z no-spend crop or the 01 → 02 → 04 drop still stands for J0171.
