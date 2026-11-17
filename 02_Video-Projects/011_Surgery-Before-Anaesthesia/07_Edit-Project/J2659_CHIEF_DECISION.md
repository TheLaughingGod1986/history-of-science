# J2659 — Chief timing decision and J2563 assembly handoff

Codex covering, 12 Nov 2026. HOS Chief election checked: Codex; Grok and Claude down. Decision: KEEP the mechanical retime at PR #554, source commit 0b1d1c82. This approves timing data for an internal rough, not the picture/edit stage or UAT. No listening or motion review performed. GBP 0 / 0 credits. Generation remains unauthorized at plan and row level.

Reviewed all 92 audit boundaries against tracked Scribe words and all eleven long-sentence splits. The 37 moves remove 18 word crossings. Each long sentence has one split at the nearest suitable clause/list join; named people and tight noun phrases remain together. v02, narration, row identities and budgets are unchanged. All six applicable PR checks passed at 0b1d1c82.

The 139.52 s and / not cut is accepted for this mechanical rough: the tracked gap is 139.48–139.54. The next sentence ends at 147.50, so starting this row before 139.50 would exceed eight seconds. It keeps “not feel a thing” together. This is a constrained word boundary, not a claim of audible silence. The 125.76 / 133.30 / 139.52 / 147.50 propagation is accepted. So are the 202.74 / 210.70 / 218.70 / 226.68 propagation and the Snow archive interval 429.63–437.60 (7.97 s). The rendered review must still assess picture fit and the tight cuts.

```text
PASS: mechanical retime validation — 93 contiguous rows, 92 word-safe boundaries; 18 word crossings removed; all 11 long sentences split; maximum 8.00 s; v02 source, VO lock, row identities, budgets and generation locks preserved.
This is a data validation result, not film-stage approval or listening/motion QA.
```

## Inputs and source precedence

J2653 restored the narration to `/Volumes/data/studio-live/History Of Science/02_Video-Projects/011_Surgery-Before-Anaesthesia/02_Voiceover/hos_011_vo_v01.wav`. Rechecked in J2659: SHA-256 `d873f1d0c9158087fd61ce0b9f53de985055d778cd58b8df70c67c0701300ae2`, duration 532.720 s. No regeneration or narration changes.

Use PICTURE_PLAN_v03 for row timing, not old part boards. Its inherited archive fields are NOT download authority. Use ARCHIVE_SOURCES_BRIEF_v01.json from merged #553, overridden by Grok’s later source ruling [6810336587](https://github.com/TheLaughingGod1986/history-of-science/pull/180#issuecomment-6810336587). Carry those corrections into a versioned assembly source manifest before downloading; preserve v02/v03 timing provenance. Recheck each actual file and licence and record URL, credit and hash.

Mandatory source overrides from that ruling:

- P1:09b: Wellcome L0041135, Paré instruments; CC BY 4.0, not low-resolution Pare_instruments.jpg. UVA remains bibliographic only.
- P2:02a Davy: Wellcome V0006497, Walker 1830 after Jackson, CC BY 4.0; not the NPG file with copyright claims.
- P2:07a Long: Wellcome M0003193, CC BY 4.0; not Crawford_Long.jpg with the rights-managed provenance.
- P3:05b: Wellcome L0018234, Morton inhaler replica c.1945, CC BY 4.0, plus own-drawn airflow arrows. Never describe it as a nineteenth-century engraving or credit Wood Library-Museum.
- P3:09a: public-domain Google Art Project scan of Southworth & Hawes, 4147×3280; not the small Getty JPEG.
- P5:03a: Wellcome L0057829 photograph of a Squire-type copy; not an 1846 engraving.
- P5:07a: follow the JSON alternate (Snow inhaler L0058154), not the differing Markdown alternate.
- Carry every required Wellcome CC BY 4.0 credit both on screen and into description credits, including Liston operating M0005603, Lister spray M0003436, and Liston portrait L0012831. Add the portrait corner credit: “Portrait: C. Turner (1840), Wellcome / CC BY 4.0”. Use the exact remaining credit strings in Grok’s ruling and the approved source brief.
- Ether Monument DSC04197 CC0 and P2:05a own-drawn 1844 broadside remain approved. Savings proposals remain held; P3:10a is still a generation slate.

## J2563 resumed scope

1. Build the 26 available free rows (13 code graphics + 13 archive/own-drawn composites) using v03 timing and the source precedence above. No minting, stock substitutes, new spoken lines or permission changes.
2. Make the 535.30 s internal timing rough against the locked 532.720 s WAV, with labelled slates for all 66 unmade generation rows AND P5:16b. It is not a finished film or Ben’s watch copy.
3. P5:16b stays a dependency slate until P1:07b exists and its interval is verified. The inherited claim that 3.48–8.00 s is “unused” is not approved: P1:07b now occupies 6.61 s, so at native speed an eight-second clip cannot provide both that use and a disjoint 4.52 s tail. A start-at-zero use would overlap by 3.13 s. Record actual source duration/in/out and overlap; do not invent an unused tail, stretch, freeze or spend to solve it. Return the concrete reuse finding to Chief before replacing the slate.
4. Generate a word-accurate overlay cue schedule from stt_raw.json (WHO/WHEN/DATA/FACT and archive credits), with source word indices, absolute cue times, one-label-at-a-time checks, and no premature reveals. Timing-sensitive visual prose needs reconciliation to the retimed row, without changing narration. The 008–010 opening experiment is not approved for 011.
5. Verify hashes, durations, continuous row coverage, word boundaries, <=8 s rows and overlay timing. Deliver the built rows, manifest, cue schedule, verification output and rough to studio-live with a PR. Keep original media and plan versions. Request a reviewer with demonstrated moving-video input; audio assessment needs demonstrated audio input. No film-stage PASS or UAT until applicable gates and reviews pass.

The three input blockers are resolved for this bounded free build. J2563 may resume after this decision merges; the unavailable generated picture is represented by slates and remains unapproved. No further decision from Ben is needed for this internal work.
