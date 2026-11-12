# J2652 continuation: cue schedule repaired; picture timing remains FIX

12 November 2026, Codex. This is a continuation of Grok's ruling 6808560760,
not a replacement ruling or a gate exception. No film stage is approved.

`PICTURE_PLAN_v03b.json` is a **cue-scope revision**, not a new approved cut
list. It inherits the v03 pictures, marks timing FIX and render_authorized=false.
v02, v03, the previous rough, and the J1310 audio remain unchanged.

## What this run finished

- Repaired the seven cue collisions: 43 cues now occupy nonoverlapping display
  intervals. All eleven names retain their original word onset and a 3–4 s hold.
- Removed the optional “THE MISSING PIECE” label that collided with Malthus.
  Merged the duplicate barnacle labels into one fact/data graphic, keeping its
  counter, scale, and both source-row references.
- Shortened overlapping optional holds. Two labels begin slightly later **within
  their anchored spoken word**: JULY 1844 at 234.60 s (word anchor 234.36,
  word end 235.38), and ORIGINALITY SMASHED at 345.88 s (anchor 345.40,
  word end 346.20). The original transcript onset remains a separate field;
  neither delay is presented as a changed transcript timestamp. Name onsets
  were not moved. The compositor must use display_start_s/display_end_s.
- Added 177 candidate interword boundary windows backed by the locked script's
  punctuation or transcript/measured pauses. The nine rejected current cuts and
  nearest supported alternatives are in acceptance_audit_v03b.json. These are
  candidate windows, not an approved retimed sequence or a proof of global
  sentence preference.

## The disputed Linnean cut: measurable pause, not an invented clause

The transcript reports no gaps in the 368.52–376.56 s sentence segment. Looking
only at its word times would suggest an unbridgeable 8.04 s span. The actual
locked WAV supplies additional evidence: ffmpeg silencedetect at **−45 dB,
minimum 120 ms** measures a **391.292 ms** low-energy interval from
371.794750 to 372.186042 s. The existing word boundary at **371.82 s** is inside
that interval. It can therefore be considered as a pause-supported candidate,
without calling “Hooker / had” a clause or cutting inside a transcript word.

The full intervals are in measured_pauses_v03b.json. Seven interword boundaries
have this additional measured support. No listening, breath identification by
ear, or motion perception is claimed. A measured interval never authorizes
cutting inside a transcript word; the legal intersection is the recorded
interword boundary. The source WAV SHA-256 was independently read back as
837178125a72fb250d255f1039c5cb7f8630bbb313cf23801a1155f257d796e0.

Measurement command (read-only):

```text
ffmpeg -hide_banner -i <locked hos_013_vo_v03a.wav> -af silencedetect=noise=-45dB:d=0.12 -f null -
```

Script-boundary evidence records the word index, punctuation and nearby script
text. Most entries come from matching runs of at least three normalized words
against darwin_script_master_v02.md, excluding directions; the date boundaries
59, 88, 137, 415, 865, 986 and 1123 were checked directly because the transcript
uses numerals while the script spells dates out. This mapping does not rewrite
spoken words or silently infer subject/predicate breaks.

## Seven checks requested by the ruling

| Check | Result | Scope |
|---|---|---|
| No in-word cuts | PASS, inherited timing | v03b retains v03's zero-crossing cut list. No new rough is claimed. |
| Qualifying gaps, sentence preference, 7 s ceiling | FAIL | Nine inherited cuts remain unsupported by this stricter audit. The ceiling passes, but candidate alternatives still need a globally feasible allocation. |
| Graphics/overlays at most 8 s | PASS, plan only | Inherited picture beats at most 7 s; revised cues at most 4 s. Revised art remains unbuilt. |
| Locked WAV/hash | PASS | Full WAV hash verified; no audio changes. |
| Callback at most 4.20 s, no loop/stretch | PASS, inherited scope only | Existing 4.18 s callback scope is untouched; no new callback media acceptance. |
| Word-level onset audit | PASS, schedule only | 43 cues, zero collisions, exact anchors preserved; names held 3–4 s. The two in-word display delays above are explicit. |
| Three proposed code replacements | PASS, not adopted | All three Quality sources retained; no claimed savings or 390 px acceptance for unbuilt replacements. |

**Overall FIX.** The existing phone/contact sheets remain attached through
ROUGH_MANIFEST_v03.json; they show the old diagnostic, not this cue revision.
No new master, phone sheet, final-picture PASS or Ben UAT is claimed.

## Exact next step

1. Use qualified_boundaries_v03b.json to replace the nine rejected cuts, allowing
   redundant views to be removed. Preserve sentence preference and the 7 s cap.
   The four source overallocations in REVIEW_v03.md still require correcting.
   A bounded solver experiment with 1.5 s chapter cards and an 8 s cumulative
   source cap reached P5:02a_linnean_reading before finding no legal path in
   the original per-row search windows. It produced no plan. Do not claim
   that merely splitting this source makes enough footage: revise its shot
   allocation and semantic coverage.
2. Resolve chapter treatment with the locked VO. Five old card holds remain
   0.28–0.56 s and are unreadable. A title needs a readable duration, the
   required preceding breath, and no collision with the mandatory name cue.
3. Apply the repaired cue scheduler to the revised picture rows; recompute host
   rows. Do not pass display delays off as word times or drop the merged DATA.
4. Only after those constraints pass, build the five missing free sources and
   revised graphics at zero credits; rebuild under a **new** rough filename,
   inspect phone/contact sheets, and record all seven checks again.

J2652 stays at step 2 of 3 and is released at this verified checkpoint. The
remaining work is editorial/source allocation and rendering, not a missing
Ben approval or a media-input-only hold. No spend, generation or YouTube change.

## Validation output

```text
CUE SCHEDULE PASS: 43 cues, zero collisions; names remain at their word onset for 3–4 s.
TIMING FIX: 9 unsupported existing cuts; 0 spans exceed 7 s without a verified boundary.
Ran 4 tests ... OK
ALL CHECKS PASS
```

The last line is the repository check_all.sh result, not film acceptance.
The four regression tests cover exact named-person onsets, 3–4 s holds, no
collisions, delays contained within their spoken word, retained barnacle data,
input immutability, and rejection of an impossible pair of name cards.
