<!-- hos-desk v1 from=grok to=claude film=007 stage=vo status=review -->
### Grok → Claude · 007 VO v01 — evidence for review

Long-film voiceover for **HOS 007 The First Vaccine** recorded from `origin/main` script (Phipps line fixed). **No picture / Vertex / Flow spend. Do not merge or close #180.** Ben listen not required before Claude PASS (standing Ben order 4 Oct).

#### Voice lock
Ben Orbit Narrator `kDch6ACCIpqgQ0NsU9kk` · `eleven_v3` · stability 0.34 / similarity 0.78 / style 0.42 / speed 1.04 / speaker_boost · via `orbit_voice.settings_for_part` + `el_auth` api_key

#### Credits (Creator plan)
| | Value |
|---|---|
| Limit | 209536 |
| Used before (first snapshot) | 109367 |
| Remaining before | **100169** |
| Used at TTS start | 109976 |
| Remaining at TTS start | 99560 |
| Used after (refreshed) | 114054 |
| Remaining after | **95482** |
| Chars sent | 6733 (1197 words) |
| API delta (refreshed − TTS start) | 4078 (count lagged mid-mint, same as 006) |

Stayed above ~50k headroom. No plan upgrade. No TTS v02 retakes.

#### Per-part KEEP table
| Part | Slug | Keep | Dur | Mean / Peak | Loudness+silence | Word-check | sha256 |
|---|---|---|---|---|---|---|---|
| 01 | the_speckled_monster | **v01b** | 105.76s | −22.1 / −2.0 dB | **PASS** | ASR FAIL×1* | `11137318bde9dad3ad122d31f77c54e39f4883d1c315a514b92a4d0a89fc7bac` |
| 02 | the_milkmaids_secret | **v01** | 129.04s | −20.8 / −1.3 dB | **PASS** | ASR FAIL×1* | `a4c4ad87d73b9ffca9dfc9e7530cfc10f1d4a68f27c612054be4669a9a9ae21e` |
| 03 | a_pail_a_lancet_and_a_boy | **v01** | 69.76s | −20.4 / −1.0 dB | **PASS** | ASR FAIL×3* | `afbbe16957cd3f6d33591937b5fc6b5edba02712278c083c260c87f6f03cada0` |
| 04 | the_test | **v01b** | 92.16s | −21.1 / −1.7 dB | **PASS** | ASR FAIL×1* | `090676adfb3c3dc9d4ebe94243483702359b71cfbc9f38ec8bfae8f5f532aa8d` |
| 05 | the_word_that_saved_millions | **v01b** | 102.56s | −21.3 / −1.9 dB | **PASS** | ASR FAIL×1* | `18b725326c0b40e6bba2250be9f25a2581366a2ff76a2121fa889191f727557f` |

\*faster-whisper under **Python 3.12** (`uv` + `av==12.3.0`). Remaining word FAILs are **ASR false positives**: ElevenLabs `*_align.json` contains the exact script span (part01 `how did a cow` + `day after day`; part02 `Berkeley`; part03 Phipps “healthy boy, about eight years old” + matter sentence; part04 `first of July`; part05 spelling honour/honor). Peak-hot v01 takes remastered with `ffmpeg volume=-0.8dB` → **v01b** (no new TTS). No silence >1.5s on any part.

#### Paths (desk — binaries gitignored)
- `/Users/benjaminoats/_desk/007/vo_20261004/REPORT.md`
- `/Users/benjaminoats/_desk/007/vo_20261004/vo/` (txt, mp3, align, `VO_TAKES_KEEP.json`, `vo_check/*.json`)
- Listen: `/Users/benjaminoats/_desk/007/vo_20261004/hos_007_vo_all_parts_listen_v01.mp3` (499.28s) sha256 `b615b8e8aabbbf8f0d179d83608e2b1affa9873986955cb95f73f62272602f9c`
- Evidence: `evidence_report_summary.png`, `evidence_terminal.png`
- Script desk copy: truncated at `---` before New-claims table so part05 prose-only

Did **not** dirty `grok/hos-vo-first-20261004` (#204) with VO media. No evidence PR opened (binaries stay on desk; text evidence on desk for Claude). Leave #205 alone.

Ready for Claude VO review PASS/FAIL.
