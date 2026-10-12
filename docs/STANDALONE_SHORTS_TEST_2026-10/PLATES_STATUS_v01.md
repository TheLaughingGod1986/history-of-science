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
