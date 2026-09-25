# Cutscene rules — History of Science YouTube (hard production rules)

## Never reuse a cutscene in one video
- Every B-roll / card / fill plate filename appears **at most once** in a single episode edit.
- No clip may play twice, even in different sections.

## Never loop cutscenes
- Cutscenes play **once** at native duration only.
- Do **not** use `stream_loop`, ping-pong, or freeze-extend to stretch a scenery clip.
- **Seedance / animated board beds:** play once. If the scene is longer than the clip, continue with that panel’s unique still board (smooth pan) — never restart the same motion.
- If picture time is short, add **new unique** plates/cards — never loop existing ones.
- Exception: Orbit character PiP may loop (character bed only).

# Text plates (title cards, brand stings)
- Never apply zoompan / Ken Burns / sin-wobble to any on-screen text.
- Encode text plates as locked stills (`-tune stillimage`, all-intra).
- In assembly, do not rescale/crop text plates — geometric filters make glyphs vibrate.

## Branding
- After cold-open / cold open VO start: short **Orbit brand intro** (~1s).
- End with **like & subscribe outro** (buttons + arrows pointing to like/subscribe) and matching VO CTA.

## Builder
- Use `_build_broadcast_noloop_v02.py` (asserts uniqueness; no cutscene loops).
