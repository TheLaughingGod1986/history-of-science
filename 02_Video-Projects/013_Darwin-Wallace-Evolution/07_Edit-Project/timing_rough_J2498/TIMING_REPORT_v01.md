# J2498: diagnostic timing rough — parked for Chief

Codex covering. Built on merged current-main picture plan v02 (94 rows, 66 Quality, no Fast). £0 / 0 credits. This is an internal diagnostic rough, not a completed edit, QA approval or Ben-watch submission.

NAS file: `/Volumes/data/studio-live/History Of Science/02_Video-Projects/013_Darwin-Wallace-Evolution/07_Edit-Project/timing_rough_J2498/hos_013_timing_rough_J2498_v01.mp4`

SHA-256: `565a0d6613de1c8e40ed9bf76ee7708c9e30b6b840687c9c277251db3fc634f2`. 515.00 s, 960×540, 30 fps. Locked narration only, padded with silence after its 512.48 s duration; no music or SFX. NAS copy hash matches the scratch master. ffprobe confirms video and audio streams.

## Input reconciliation

The shared HOS checkout is on an older branch. A clean branch from origin/main at 1c59247b was used instead; no shared local changes were touched. The v02 plan from J2558 is already merged.

22 existing code/archive renders passed their recorded SHA-256 checks. The rough contains those 22 renders and 72 labelled slates: 66 unminted Quality rows, five newly converted v02 free rows lacking renders, and one callback whose source is unminted. The original “23 built free rows” count included that unavailable reuse; it is not an existing rendered asset. No stock substitutions or generated pictures were used.

Missing free/reuse rows:
- `P2:10b_shipmate_tagged_tray` (149.90–153.20 s)
- `P3:09a_essay_1844_sealed` (234.20–240.64 s)
- `P4:07b_packet_to_mailbag` (326.00–330.68 s)
- `P5:02b_joint_papers_lectern` (376.56–382.34 s)
- `P5:04b_bell_report_1859` (398.00–404.66 s)
- `P6:08a_reuse_study_beaks_callback` (504.08–508.48 s)

The available WAV matches both the J1310 lock in VO_STATUS.md and the transcript hash: `837178125a72fb250d255f1039c5cb7f8630bbb313cf23801a1155f257d796e0`. Both plan summaries instead name `f8ef433b…`; that metadata is inconsistent. No source plan or lock was rewritten.

## Timing result: FAIL / unresolved

`clip_check.py cuts_v01.csv --words words_fw_small_en.json --vo-end 512.48 --json` exited **1**, `passed: false`, with nine errors. Exact output is in clip_check_v01.json. The independent timestamp audit found **14 cut-inside-word events, 23 cut-inside-sentence events and five rows longer than eight seconds**. These counts overlap; they are not 42 distinct bad rows. The raw punctuation comes from existing ASR and requires editorial confirmation, not claimed listening.

The checker’s sequential fuzzy text matcher can advance past a repeated word; its negative chapter-card breaths are therefore preserved as tool output, not asserted to be actual negative silence. The direct word-boundary audit below is independent of that matcher. Chapter cards start at 75.50, 171.08, 276.26, 366.34 and 448.16 s; their planned 1.5–2.22 s spans include the opening words of the next chapter. No checker was changed.

### Cuts inside words

| Row ending at cut | Cut (s) | Word and actual interval (s) |
|---|---:|---|
| `P1:07_darwin_1837_desk` | 39.40 | in (39.36–39.62) |
| `P2:12a_arch_notebook_tree_zoom` | 166.60 | could (166.26–166.72) |
| `P2:12b_tree_question` | 171.08 | On (171.02–171.22) |
| `P3:01_card_p03` | 172.58 | 1838 (172.54–173.80) |
| `P3:11_barnacles_microscope` | 261.50 | that (260.98–261.62) |
| `P3:13b_brass_globe_turn` | 276.26 | Alfred (276.16–276.62) |
| `P4:01_card_p04` | 277.76 | not (277.62–277.92) |
| `P4:06a_wallace_fever` | 315.30 | and (314.92–315.78) |
| `P4:07a_wallace_writes_hut` | 326.00 | famous (325.82–326.32) |
| `P4:12_lyell_hooker_bundle` | 366.34 | On (366.28–366.52) |
| `P5:01_card_p05` | 368.56 | Darwin's (368.52–369.20) |
| `P5:06_murray_bookshop` | 419.00 | and (418.20–419.10) |
| `P5:10_darwin_worried_shelf` | 448.16 | The (448.10–448.34) |
| `P6:01_card_p06` | 449.66 | engineer (449.42–449.86) |

### Cuts inside sentences

| Row ending at cut | Cut (s) | Next sentence end (s) | Spoken context |
|---|---:|---:|---|
| `P1:01_study_beaks` | 3.80 | 6.82 | work out how life changes over time and then lock it in a drawer |
| `P1:03a_unlabelled_birds` | 11.90 | 20.22 | you'll know how a few unlabeled birds, eight years of barnacles and one letter |
| `P1:03b_malay_packet` | 16.02 | 20.22 | letter from the other side of the world forced the biggest secret in biology |
| `P1:04a_packet_seal` | 19.00 | 20.22 | world forced the biggest secret in biology into the open. In the 1830s most |
| `P1:05a_museum_cases` | 25.64 | 29.22 | the 1830s most naturalists believed every kind of animal and plant had been made |
| `P1:07_darwin_1837_desk` | 39.40 | 45.44 | -old Charles Darwin drew a little tree in a private notebook, one kind of |
| `P2:01_card_p02` | 77.00 | 81.22 | life changes? When people picture Darwin on the Galapagos Islands they imagine a flash |
| `P2:10a_explorer_shipmates` | 149.90 | 152.58 | out which beak came from which island and slowly a question formed. What if |
| `P2:12a_arch_notebook_tree_zoom` | 166.60 | 167.92 | see that one kind of animal could split into many. But what was doing |
| `P3:01_card_p03` | 172.58 | 181.44 | the shaping? On the 28th of September 1838 Darwin started reading a book about |
| `P3:02a_malthus_lamplight` | 178.80 | 181.44 | book about human populations by Thomas Malthus and the missing piece fell into place. |
| `P3:09a_essay_1844_sealed` | 240.64 | 242.12 | all out. About 230 pages sealed it and left Emma a letter. If he |
| `P3:10a_arch_vestiges_1844` | 250.20 | 253.78 | months later an unsigned book claiming life had changed over time was torn apart |
| `P3:11_barnacles_microscope` | 261.50 | 266.02 | So many barnacles the story goes that one of his children asked a friend |
| `P4:01_card_p04` | 277.76 | 279.08 | was that someone? Alfred Russell Wallace was not rich like Darwin. He made his |
| `P4:06a_wallace_fever` | 315.30 | 319.08 | thought about the same book by Malthus and like Darwin 20 years before he |
| `P4:07a_wallace_writes_hut` | 326.00 | 328.24 | and he posted it to the one famous naturalist he knew would be interested. |
| `P5:01_card_p05` | 368.56 | 376.56 | heard? On the 1st of July 1858 Darwin's friends Charles Lyle and Joseph Hooker |
| `P5:05a_darwin_writes_origin` | 411.56 | 413.64 | he finished a shorter book for everyone on the origin of species. It came |
| `P5:06_murray_bookshop` | 419.00 | 423.4 | on the 24th of November 1859 and booksellers had ordered every copy before it |
| `P6:01_card_p06` | 449.66 | 453.0 | print. The problem came from an engineer called Fleming Jenkin in 1867. Everyone then |
| `P6:04a_mendel_pea_garden` | 476.56 | 478.9 | in 1866 a friar called Gregor Mendel had published his work on pea plants. |
| `P6:08a_reuse_study_beaks_callback` | 508.48 | 512.24 | Darwin's selection together with Mendel's beads and you have the core of how biologists |

### Rows longer than eight seconds

| Row | In–out (s) | Length (s) |
|---|---|---:|
| `P1:08_cg_i_think_tree` | 39.40–54.30 | 14.90 |
| `P2:09_cg_finch_toolbox` | 131.40–143.72 | 12.32 |
| `P3:03_cg_malthus_curve` | 182.70–192.10 | 9.40 |
| `P4:05_cg_wallace_counter` | 298.12–308.62 | 10.50 |
| `P6:03_cg_blending_beaks` | 458.78–471.06 | 12.28 |

All five are code graphics, not a request to stretch an eight-second Veo source. They still require a picture/motion decision. The callback P6:08a asks for 4.40 s from a 4.20 s tail (3.80–8.00); an overlap does not create missing source frames. It remains a slate.

### Overlay timing

No newly composited overlays are claimed in this rough. Existing rendered graphics retain their baked animation. The plan carries overlay descriptions and hold lengths, but no explicit word-level onset. Every semantic cue is listed below; names with exact transcript matches include their nearest name onset. A row-start comparison is diagnostic and does not prove the overlay actually appears at that time in a rendered source. Unmatched spellings and non-verbatim labels remain unresolved.

| Row | Kind | Row start (s) | Name onset (s) | Row start minus name (s) | Result |
|---|---|---:|---:|---:|---|
| `P1:01_study_beaks` | LABEL | 0.00 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P1:03b_malay_packet` | LABEL | 11.90 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P1:05a_museum_cases` | WHEN | 21.64 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P1:06_padlock_shut` | LABEL | 29.22 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P1:07_darwin_1837_desk` | WHO | 33.44 | 37.02 | -3.58 | MISALIGNED |
| `P1:08_cg_i_think_tree` | DATA | 39.40 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P1:09_wallace_hut_split` | WHO | 54.30 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P1:10_cg_globe_arc` | DATA | 62.08 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P2:03_unlabelled_bagging` | WHEN | 84.22 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P2:04_blank_tags_row` | FACT | 92.18 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P2:06a_lawson_jetty` | WHO | 104.56 | 106.6 | -2.04 | MISALIGNED |
| `P2:06b_cg_tortoise_shells` | EXPLAINER | 110.00 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P2:08a_gould_sorting` | WHO | 120.88 | 123.2 | -2.32 | MISALIGNED |
| `P2:09_cg_finch_toolbox` | DATA | 131.40 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P3:02a_malthus_lamplight` | WHO | 172.58 | 177.64 | -5.06 | MISALIGNED |
| `P3:02b_notebook_d_open` | LABEL | 178.80 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P3:03_cg_malthus_curve` | DATA | 182.70 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P3:06_nature_keeps_fit` | EXPLAINER | 211.76 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P3:07b_confessing_murder_letter` | LABEL | 223.90 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P3:08_emma_study` | WHO | 229.34 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P3:09a_essay_1844_sealed` | WHEN | 234.20 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P3:09b_emma_letter_cupboard` | LABEL | 240.64 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P3:11_barnacles_microscope` | FACT | 254.76 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P3:12_cg_barnacle_counter` | DATA | 261.50 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P4:03a_helen_burning` | WHEN | 283.70 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P4:03b_crates_sinking` | FACT | 289.90 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P4:05_cg_wallace_counter` | DATA | 298.12 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P4:06a_wallace_fever` | WHEN | 308.62 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P4:09a_darwin_reads_wallace` | WHO | 337.30 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P4:09b_smashed_letter_pen` | LABEL | 344.20 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P5:02a_linnean_reading` | WHO | 368.56 | 370.88 | -2.32 | MISALIGNED |
| `P5:03a_two_empty_chairs` | LABEL | 382.34 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P5:04b_bell_report_1859` | FACT | 398.00 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P5:06_murray_bookshop` | WHEN | 414.44 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P5:07_cg_timeline_origin` | DATA | 419.00 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P6:02a_jenkin_study` | WHO | 449.66 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P6:02b_paint_pots_mix` | LABEL | 453.50 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P6:03_cg_blending_beaks` | EXPLAINER | 458.78 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P6:04a_mendel_pea_garden` | WHO | 471.06 | 475.5 | -4.44 | MISALIGNED |
| `P6:05_beads_not_paint` | LABEL | 479.92 | — | — | NEEDS_EDITORIAL_ANCHOR |
| `P6:06b_spencer_coined` | WHO | 490.60 | 491.74 | -1.14 | MISALIGNED |
| `P6:07_key_in_lock` | LABEL | 496.54 | — | — | NEEDS_EDITORIAL_ANCHOR |

## Retiming decision needed

v02 does **not** hold against the literal “no picture change inside a sentence” requirement. Timings have deliberately not been moved, so this is a reproducible diagnostic of the merged plan rather than a falsely passing revision. Do not overwrite J2558’s v02 with another v02. A corrected edit should be versioned v03 after Chief resolves the conflicting constraints.

Concrete conflict: the opening sentence runs from 0.00 to 6.82 s, but the plan cuts at 3.80 s and the standing picture cadence is 4–6 s. Preserving every row, keeping that cadence, and forbidding every sentence-internal picture cut cannot all hold. Moving a boundary to the next sentence end also changes the planned durations of adjacent rows and their already built animation. Chief must choose whether sentence-internal picture cuts may continue over uninterrupted VO, or commission a revised picture structure that removes/combines rows and rebuilds affected graphics. This report waives neither rule.

Next: Chief reviews the diagnostic rough and the failed timing evidence; scope the v03 cut/overlay revision and five missing free renders. Keep the callback as a slate until its actual source exists. No minting, generation_authorized change, upload, schedule change or Ben notification was performed.

Session has terminal and still-image tools, but no demonstrated direct audio or moving-video perception. No listening, motion quality or sync-by-ear approval is claimed.
