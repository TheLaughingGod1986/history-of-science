# J1300 — HOS 013 shaping re-hear (Codex, 31 Oct 2026)

Final take for the J1301 check: **v03**. This is a worker repair record, not a VO lock or final sign-off.

Source v02 SHA-256: `fa100bb9cf771fd5bc7889a2fb0c217f1577df9a1927302d448e7cd9469b47b6`.
The brief's ~164.58 s estimate is early. The sentence is at ~168.8–170.28 s. The initial 160–170 s trial clipped its end and is excluded; all evidence here uses a copied 165–177 s padded clip, and an additional 168.4–170.7 s sentence clip. Source files were never moved.

## Re-hear

faster-whisper, CPU, int8, word_timestamps=True, beam_size=5, English; no script prompt. Full transcripts and word records are in each model JSON. Absolute film seconds below.

| Model | Sentence | doing | disputed article | shaping |
|---|---|---|---|---|
| base.en | But what was doing was shaping. | doing 169.26–169.48, p=0.9916 | was 169.48–169.70, p=0.6482 | shaping. 169.70–170.02, p=0.9970 |
| small.en | But what was doing was shaping. | doing 169.32–169.58, p=0.9946 | was 169.58–169.76, p=0.6056 | shaping. 169.76–170.16, p=0.9951 |
| medium.en | But what was doing the shaping? | doing 169.36–169.60, p=0.9693 | the 169.60–169.80, p=0.9771 | shaping? 169.80–170.28, p=0.9959 |

The tighter sentence-only check repeats the split: base hears “doing was shaping” (was p=0.7341), medium hears “doing the shaping” (the p=0.9873). “Doing” is present throughout. This is evidence of an unclear article, not proof of an absent syllable. The brief's no-pickup condition (both medium and base hear the phrase) was not met. One authorized pickup resolves the persistent substitution; no spoken wording was changed.

## Energy envelope

`envelope_10ms.json` and `envelope.svg` show 10 ms RMS. The doing region has a peak at 169.43 s (−16.11 dBFS), then a continuous lower-energy shoulder over 169.60–169.72 s (about −29 to −26 dBFS), before the fricative and shaping vowel. There is energy in the disputed interval, but no clearly isolated extra syllable peak identifying “the”. An envelope cannot distinguish “the” from “was”; it does not independently prove omission. The model disagreement above drove the conservative pickup.

## Pickup and splice

Exactly “But what was doing the shaping?”; Ben Orbit Narrator, eleven_v3, speed 1.04, same settings as credit pickup. Dry run first. One take, 31 characters (below ~50 cap), no second attempt. Live balance 101,592 / 121,114 before the take; immediate API counter unchanged due to lag. Recorded the reading and 31-credit spend in ai_spend. No money, top-up or overage.

Tool output:

```text
PASS: hos_013_pickup_shaping_v01 1.6 s, LUFS -20.0, Scribe 100.0% (0 mismatch runs), 31 chars spent
```

Scribe exact transcript: “But what was doing the shaping?” (six of six words). This pickup-only tool result is not the final film VO gate.

v03 uses v02 head through 168.75 s and tail from 170.50 s. Pickup gain +1 dB matches original sentence −19.0 LUFS; pickup fades over 1.58–1.60 s after Scribe's final word endpoint, pads 0.19 s, and both joins crossfade 20 ms in silence. No tempo change. The complete cut recipe and hashes are in `hos_013_vo_v03_SPLICE.json`.

Final v03 SHA-256: `d56ba2a45a76125e29b0d620ab84772a9311399354c07d860ac168938ff05038`. Duration **512.48 s**. ebur128 **−19.5 LUFS**; mean **−23.0 dB**, peak **−3.6 dB**.

Audio lives in the HOS checkout's `02_Video-Projects/013_Darwin-Wallace-Evolution/02_Voiceover/`; metadata only in git. v01 and v02 untouched. J1301 owns the final vo_check and any lock after J1299; no final vo_check run here. No picture or upload.

## Local splice verification

On the final faded v03, base.en hears “But what was doing the shaping?”; the probability for “the” is 0.9727 (`v03_base.en.json`). Both untouched regions compare sample-for-sample equal with v02 (before 168.73 s and from 170.50 s). Duration is the same number of PCM frames. The largest sample jump at the four crossfade boundaries is one 16-bit PCM step, and at the pickup-to-padding boundary it is zero (`join_checks.json`). Original v01 and v02 hashes remain as recorded. This is a local repair check, not a final vo_check.
