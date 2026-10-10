# Shorts

Rules: `HOS_STRATEGY.md` → *Short hook* and *The first two seconds*; `STUDIO_PLAYBOOK.md` §3 and §7.

- 22–27 s. Two lines, then one hard fact. Line 1 (5–7 words) is the surprising truth about a familiar thing, said in the first second.
- Frame 0: the named thing, already moving, with a 2–4 word hook caption. Never the Explorer, a blank card or an empty room.
- The hook caption's cap height is 8–10% of the frame (rule 3.3; 154–192 px at 1920). Older HOS Shorts ran at about 3% (thumb audit 9 Oct, item 12). Build it with `render_hook` from `005_How-Harvey-Proved-Blood-Circulates/10_Shorts/_build_shorts_v02.py` (`HOOK_CAP = 0.09`, block centred, clear of the bottom UI), and record its `cap_pct` in each Short's build log.
- The promoted film's exact live title on screen at 9–14 s. The last 4 s loop to the opening picture. Captions throughout.
- Ship gate on every export: `python3 00_Brand/Channel-Setup/tools/gate_shorts_open.py check <mp4> --air-date YYYY-MM-DD`.
- Never before this film's long is public. One Short a day at most. Studio Related → this long. Zero `/go/`, no pinned comment.
- Log stayed-to-watch at 48 h in `00_Brand/Channel-Setup/audits/SHORTS_LOG.md`.
