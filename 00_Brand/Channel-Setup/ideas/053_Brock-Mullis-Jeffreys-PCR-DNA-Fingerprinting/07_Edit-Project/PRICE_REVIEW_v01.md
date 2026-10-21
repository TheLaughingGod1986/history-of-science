# 053 price review v01 (pre-VO plate boards)

Gemini, 18 Oct 2026, J0600. Boards only. **No mint. No spend. No merge.**
Prepared from `pcr_script_master_v01.md` (`91.1 PASS`) and `SOURCES_v01.md` so 053's full plate board rows, non-emissive Fast prompts, £0 code graphics, and Teach-on-Screen overlays are ready to re-time the moment long VO locks. Parked for Chief.

## Totals (base 25-row board before VO continuation splits)

| Part | Title | Rows | Quality | Fast | £0 code | £0 reuse | Flow try-1 | Flow expected | Vertex try-1 | Vertex expected |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Part 01 | Part 01 — How a 70 °C Yellowstone Hot Spring Turned One DNA Strand Into a Billion Copies | 9 | 5 | 2 | 2 | 0 | 520 | 1335 | £5.76 | £14.82 |
| Part 02 | Part 02 — 19 September 1966 & 1976: Thomas Brock's Boiling Yellowstone Spring (Thermus aquaticus) & the Heat-Proof Taq Enzyme | 4 | 1 | 2 | 1 | 0 | 120 | 299 | £2.40 | £5.73 |
| Part 03 | Part 03 — April 1983 – January 1988: Kary Mullis's Moonlight Drive (PCR) & Swapping in Yellowstone's Taq — Midpoint Twist | 4 | 1 | 2 | 1 | 0 | 120 | 299 | £2.40 | £5.73 |
| Part 04 | Part 04 — 9:05 a.m., 10 September 1984 & 1986: Alec Jeffreys's 'Eureka!' Darkroom X-Ray (DNA Fingerprinting) & the First Exoneration | 4 | 2 | 1 | 1 | 0 | 210 | 538 | £2.88 | £7.28 |
| Part 05 | Part 05 — Why the First DNA Crime Test Freed an Innocent Boy — & How Yogurt Bacteria Gave Us CRISPR Gene Scissors | 4 | 1 | 1 | 1 | 1 | 110 | 279 | £1.76 | £4.40 |
| **Film** | | **25** | **10** | **8** | **6** | **1** | **1080** | **2750** | **£15.20** | **£37.96** |

## Route breakdown

- **Quality (10 rows):** readable faces (Thomas D. Brock, Hudson Freeze, Alice Chien, Kary B. Mullis, Randall K. Saiki, Henry A. Erlich, Alec J. Jeffreys, Svante Pääbo, Francisco Mojica, Rodolphe Barrangou, Emmanuelle Charpentier, Jennifer Doudna), 19 September 1966 Yellowstone 70 °C Mushroom Spring sampling, 1976 Cincinnati Taq purification, April 1983 Highway 128 & 1985–1988 Cetus PCR automation, 10 September 1984 Leicester darkroom DNA fingerprint X-ray, and the 2 Explorer beats.
- **Fast (8 rows, non-emissive):** daylight prop and laboratory shots (Yellowstone microscope slide, ATCC vial, micropipette, PCR tubes & DNA helix model pan, 3-object callback bench, Brock's 1966 field notebook & geothermal thermometer, Cincinnati 1976 chromatography column & water bath, 3-temperature PCR water baths & stopwatch, DNA double-helix model with primer brackets, Leicester 1984 autoradiograph film & gel tray, Yellowstone slide & PCR rack on museum plinth). Zero candles, flames, sparks, or glowing elements on Fast.
- **£0 code graphics (6 rows):**
  1. `P1:04_pcr_30_cycle_exponential_2_to_30_1073741824_copies_and_thermal_cycle_chart` — 3-step PCR thermal cycling (95 °C unzip, 54 °C primer anneal, 72 °C Taq extension) multiplying 1 DNA strand by 2^30 = 1,073,741,824 copies (`SCALE: searching for one gene inside all three billion letters of human DNA without PCR is like hunting for a single needle in a haystack the size of a stadium — whereas thirty cycles of PCR turn that needle into a billion-needle mountain while leaving the hay behind`)
  2. `P1:06_ecoli_polymerase_vs_yellowstone_taq_95c_thermal_survival_chart` — E. coli DNA polymerase I (0% activity after 1 min at 95 °C) vs Yellowstone Thermus aquaticus Taq polymerase (75–80 °C optimum, surviving 30 cycles at 95 °C) (`SCALE: ninety-five degrees Celsius is five degrees below boiling water — hot enough to cook an egg white solid in seconds, yet Yellowstone's Taq enzyme copies DNA right through the heat without flinching`)
  3. `P2:02_brock_1969_thermus_aquaticus_70c_growth_and_chien_1976_taq_80c_optimum_chart` — Brock & Freeze's 1966/1969 Thermus aquaticus strain YT-1 growth curve (40–79 °C, optimum 70 °C) and Chien's 1976 Taq polymerase synthesis peak (75–80 °C) (`SCALE: seventy degrees Celsius is hot enough to scald human skin in one second — yet for Yellowstone's Thermus aquaticus, seventy degrees is a comfortable room temperature`)
  4. `P3:02_saiki_mullis_1985_manual_klenow_vs_1988_automated_closed_tube_taq_pcr_chart` — Saiki & Mullis's 1985 manual E. coli Klenow PCR (opening the tube after every 95 °C cycle) vs 1988 automated closed-tube Yellowstone Taq PCR (`SCALE: doubling one molecule thirty times in a row is like folding a sheet of paper thirty times — it grows from a single invisible strand into more than a billion copies inside a droplet smaller than a teardrop`)
  5. `P4:02_jeffreys_1985_minisatellite_vntr_barcode_inheritance_and_1986_exoneration_chart` — Alec Jeffreys's 10 September 1984 / 1985 minisatellite VNTR/STR barcode (<1 in 10^9–10^12 match odds) and 1986 exoneration of Richard Buckland (`SCALE: although ninety-nine point nine per cent of your DNA is identical to the person sitting next to you, counting the stutters at just a dozen repeating spots makes your genetic barcode rarer than one in a billion`)
  6. `P5:01_timeline_1966_1988_and_yellowstone_taq_pcr_to_dna_fingerprinting_chart` — completed 4-date timeline (19 Sep 1966 → 29 Jan 1988) + single-cell PCR and forensic exoneration diagram (`SCALE: a single free sample of pink bacteria lifted from a Yellowstone puddle in nineteen sixty-six now powers billions of diagnostic and forensic DNA tests around the globe every year`)
- **£0 verified reuse (1 row):** `P5:04_table_three_callback` uses the 2.40 s unused moving tail `[5.50s..7.90s]` of `P1:07_table_three_props_yellowstone_slide_jar_pcr_thermal_block_and_jeffreys_xray_film`.

## Mint order

006 > 007 > 008 > 009 > 010 > 011 > 012 > 013 > 014 > 015 > 016 > 017 > 018 > 019 > 020 > 021 > 022 > 023 > 024 > 025 > 026 > 027 > 028 > 029 > 030 > 031 > 032 > 033 > 034 > 035 > 036 > 037 > 038 > 039 > 040 > 041 > 042 > 043 > 044 > 045 > 046 > 047 > 048 > 049 > 050 > 051 > 052 > 053 > 054 > 055 > 056. `generation_authorized` is `false` on every row.
