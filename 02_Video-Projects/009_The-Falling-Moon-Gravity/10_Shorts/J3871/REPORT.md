# J3871 — Newton apple Short repair; loop gate still blocked

Codex covering. Internal repair only; J3816 and draft HOS PR #811 remain held. No Short PASS, UAT handoff or publishing approval.

## Ancestry and exact deliverable

Branch codex/J3871 starts at 2922143e2bc116edd800c63e8bfb42c20abb3c82 (failed J3816 v02, draft PR #811). V04 supersedes that failed draft for further repair only; it does not supersede approved existing Shorts. V02 and failed evidence remain untouched. V03 receipts preserve the first SFX attempt, which was too quiet to register a hit; v04 repairs that.

V04: 17.100 s, 952×1692, 30 fps. SHA256 3e21b51f9314df661b1556fc94ac313a6a73830a66c04ddfb59d33a8e2731dac. Copy and separate VO/SFX stems checksum-verified at /Volumes/data/studio-live/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/10_Shorts/J3871/v04/. BUILD.json contains source hashes and exact timeline/source windows. No narration word or speed changed; VO stem hash remains 4eae192f1a4ab1c24fd76e131d73cd901e9ab44c7a906717e13acd7902f60ff4.

## Repair and checks

Opening now uses native apple footage source 0.9–1.7 s, then cuts at 0.8 s to existing Newton footage. No still push, synthetic motion or gate adjustment. Newton windows are contiguous 0–4.14 and 4.14–7.44 s; orchard windows 0–3.3 and 3.3–7.96 s. Last 0.9 s plays native apple source 0–0.9 s, ending at opening source time. House sfx_hos_tick_ink_v01.wav enters at 5.0 s on the Newton card, gain -9 dB. Caption, WHO and title rendering are retained from v02.

Exact v04 check receipts (full command/output and exits in v04/GATES.json and individual text files):

```text
open: PASS  hos_009_s03_apple_head_v04.mp4  dur=17.1s  audio=-17.5dB  motion=24.4  f0diff=1.91  cut1=0.77s  vo_onset=0.07s  tail_gap=1.33s  vo_src=/Volumes/MiniWork/scratch/J3871-build-v04/vo.wav  dhash=dbc97cf9ddde3615
picture: be/History Of Science/02_Video-Projects/009_The-Falling-Moon-Gravity/04_Generated-Clips/part02/raw/v01/08_the_apple_t1.mp4: reuse: same stretch as 0:00 (give it a new stretch, or a new render)
polish: apple_1     0.4s /Volumes/data/mac-mini-archi ok
music: WARN reused: couldn't read part01_zoo_of_stuff_v02.mp3 to compare (OSError); download it or pass --others
sfx: SFX level PASS: VO -19.8 LUFS, SFX -44.1 LUFS, 1 hits
vo: PASS  vo.wav  0:17.10  mean -23.1 dB  peak -4.1 dB  179 wpm
```

Opening f0diff=1.91 (was 1.14; requires 1.50), first cut=0.77 s; full bleed 0/18 padded at 1 Hz and 0/35 at 2 Hz. Polish has one low-detail warning; picture has five warnings for review. Music returned PASS with two pre-existing unreadable comparison-track warnings. SFX integrated -44.1 LUFS versus VO -19.8, one hit; word-check PASS was freshly rerun through the pinned Python environment. Repository check_all.sh: ALL CHECKS PASS (full receipt saved). These technical results do not establish audible quality or motion KEEP.

## Exact unresolved contract conflict

picture_qa.py reuse_checks uses SAME_STRETCH=10.0: its final apple row fails because abs(0 - 0.9) < 10, even though the natural pre-roll source interval [0,0.9) does not overlap opening [0.9,1.7). All other rows pass. The optional terminal_loop.validate rejects duration 17.1 before media eligibility: `Short duration must be 22–27 seconds` (source lines 71–73). HOS new Shorts require 16–19 seconds, with no overlap between bands. Its prescribed same-offset opening replay also differs from this natural pre-roll return. Extending to 22 s would violate current HOS length; no source renaming, fabricated offsets or waiver was used. No conforming exact-return solution is established from the approved existing sources under these unmodified checks. This is the separate gate-review case authorised by the brief, not authority to change tests.

Static source and v04 full-cut sheets inspected; no audible or moving-video perception available (heard=false, watched=false). WHO/title phone readability and continuity still need the capable J3872 review after all gates pass. Do not treat the sheet as motion approval. No money, credits, paid API, voice generation, YouTube, privacy, schedule or Buffer action.

Disk housekeeping: chief status showed ~13.6 GB free; required checksum-verifying nas_offload.py --apply ran in tmux J3871-offload and found no /private/tmp scratch old enough to move. Log: ~/_desk/logs/J3871-offload.log. No NAS file deleted.

Next: separate elected-Chief gate review J3874, then finish J3871 with exact-file rechecks, then J3872 actual audio/motion/phone review. J3871 is not done and J3816 remains held. Nothing to Ben at this stage.
