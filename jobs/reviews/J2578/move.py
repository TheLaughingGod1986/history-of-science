"""J2578: move History of Science's own rules from AGENTS.md to studio/RULES.md. Every line goes whole to one file.

The pattern is orbit-with-ben's jobs/reviews/J2527/move.py. A record of how the move was made, kept so it can be read
and re-run. It reads AGENTS.md and studio/RULES.md at the commit named in BEFORE, WRITES both in the working tree,
and prints the check: no old line lost or changed, and every new line listed. Do not run it on main to "refresh" the
rules: both files have their own life after the move.

What decides where a line goes: it moves only if it is about this channel alone (its films, its Explorer, its picture
and voice routes, its titles, its accounts, its own docs). A line that holds both kinds stays in AGENTS.md, where a
studio rule can never be lost. A section that is copied whole into other files and is mostly the studio's stays whole."""
import subprocess, sys
from collections import Counter
from pathlib import Path

BEFORE = "aba45ecb5e9947e4a725cc9e96dff6fbdc835b37"   # main when the move was made; the record stays runnable after the merge
show = lambda path: subprocess.run(["git", "show", f"{BEFORE}:{path}"], capture_output=True, text=True, check=True).stdout
old = show("AGENTS.md").split("\n")
if old and old[-1] == "":
    old.pop()
stub = show("studio/RULES.md").split("\n")
if stub and stub[-1] == "":
    stub.pop()
L = lambda n: old[n - 1]                       # 1-indexed
S = lambda n: stub[n - 1]
def rng(a, b): return list(range(a, b + 1))

# --- anchors: fail loudly if main has moved under us
EXPECT = {1: "# AGENTS.md", 5: "Read this first", 7: "**The channel:**", 9: "**The job:**", 11: "**The week", 13: "**Not this repo:**",
          15: "## Docs in force", 27: "Also in force as references", 29: "## Where things live", 49: "## Commands",
          76: "## Definition of done", 92: "## Teach on screen", 147: "## Polish pass", 209: "## Reference lessons",
          278: "## Packaging", 287: "## The desk", 302: "## Who does what", 329: "## Status board", 339: "## Ben's check-in",
          362: "## Never", 364: "- **Channels:**", 365: "- **Uploads:**", 370: "- **Publishing:**", 371: "  - Premiere a long",
          372: "  - Leave any video or Short marked **Made for Kids**", 373: "  - Air more than one Short a day",
          376: "  - Put the Explorer at frame 0", 377: "  - Burn subscribe or like graphics", 378: "- **Titles:**",
          379: "- **Studio:**", 380: "- **Picture:**", 388: "  - Ken Burns", 389: "- **Voice:**", 390: "- **TikTok:**",
          391: "- **Social:**", 392: "- **Secrets:**", 393: "- **Network details:**", 395: "## Git",
          399: "## Missing footage fallback", 410: "## Studio core", 414: "## Changing the rules"}
for n, start in EXPECT.items():
    assert L(n).startswith(start), f"line {n} is not what the plan expects: {L(n)[:60]!r}"
assert len(old) == 416, len(old)
STUB_EXPECT = {1: "# History of Science: rules for the studio", 3: "The studio engine", 5: "- `channel.json`", 8: "- This file:",
               10: "Studio-wide rules always come first", 13: "The channel's own rules are in this repo's", 17: "To change how the studio"}
for n, start in STUB_EXPECT.items():
    assert S(n).startswith(start), f"studio/RULES.md line {n} is not what the plan expects: {S(n)[:60]!r}"
assert len(stub) == 18, len(stub)

DOCS = rng(15, 27)                               # Docs in force: every doc on the list is this channel's
SECTIONS = rng(76, 286)                          # Definition of done, Teach on screen, Polish pass, Reference lessons, Packaging
NEVER = [364, 371, 372, 376, 377, 378] + rng(380, 391)
channel = set([7, 8, 9, 10] + DOCS + [28] + SECTIONS + NEVER)

NEW = {
 "pointer": "**Then read `studio/RULES.md`.** It holds this channel's own rules: the docs in force, the contract each stage must pass, what its films teach, look and sound like, how they are packaged, and the lines it adds to the Never list below. Both files are in force. Where they disagree, this file wins.",
 "docs_h": "## Docs in force",
 "docs": "This file first. Then the channel's rules file, `studio/RULES.md`, and the docs it lists in its own order of precedence. Where one of the channel's docs and this file disagree, this file wins. Anything not listed there, and everything in `_archive/`, is history only.",
 "never": "The channel adds its own lines to this list in `studio/RULES.md` (\"Never (this channel's additions)\"). Those add to this list and remove nothing from it.",
 "changing": "The docs numbered 1–7 are listed in `studio/RULES.md`. The channel's own rules are changed the same way, in that file.",
}

# --- the studio file
out = []
for n in range(1, len(old) + 1):
    if n in channel:
        if n == 15:                               # where "Docs in force" stood
            out += [NEW["docs_h"], "", NEW["docs"], ""]
        continue
    out.append(L(n))
    if n == 5:
        out += ["", NEW["pointer"]]
    if n == 393:                                  # the last line of the Never list
        out += ["", NEW["never"]]
    if n == 416:
        out += ["", NEW["changing"]]
studio = "\n".join(out) + "\n"
while "\n\n\n" in studio:
    studio = studio.replace("\n\n\n", "\n\n")

# --- the channel file
RH = {
 "title": "# History of Science: this channel's rules",
 "intro": "Read `AGENTS.md` first. It holds the rules that are not this channel's alone: the desk, who does what, the status board, Ben's check-in, uploads, secrets, git. This file adds History of Science's own: the docs in force, the contract each stage must pass, what its films teach, look and sound like, how they are packaged, and the lines it adds to the Never list. Both are in force. Where they disagree, `AGENTS.md` wins.",
 "plug_h": "## How the studio plugs this channel in",
 "never_h": "## Never (this channel's additions)",
 "never_note": "These add to the Never list in `AGENTS.md`. They remove nothing from it.",
 "fill": "  - Ship a Short with a shot that does not fill the 9:16 frame: black bars, a flat band, or a blurred or mirrored copy above and below a picture band. `gate_shorts_open.py` fails it at the opening and over the whole Short (10 Nov 2026).",
}
STUB_KEPT = [3, 4] + rng(5, 8) + [9, 10, 11, 12, 17, 18]
STUB_DROPPED = [1, 13, 14, 15]                    # the old title, and the paragraph that said the rules were in AGENTS.md
ch = [RH["title"], "", RH["intro"], "", L(7), "", L(9), ""]
ch += [RH["plug_h"], ""] + [S(n) for n in STUB_KEPT] + [""]
ch += [L(n) for n in DOCS] + [""]
ch += [L(n) for n in SECTIONS]
ch += [RH["never_h"], "", RH["never_note"], "", L(364), L(370), L(371), L(372), L(376), L(377), RH["fill"], L(378)] + [L(n) for n in rng(380, 391)]
rules = "\n".join(ch) + "\n"
while "\n\n\n" in rules:
    rules = rules.replace("\n\n\n", "\n\n")

Path("AGENTS.md").write_text(studio)
Path("studio/RULES.md").write_text(rules)

# --- the check: nothing lost, nothing changed, every added line declared
strip = lambda text: Counter(l.strip() for l in text.split("\n") if l.strip())
before = strip("\n".join(old)) + strip("\n".join(stub))
after = strip(studio) + strip(rules)
dropped = Counter(S(n).strip() for n in STUB_DROPPED)
lost = before - after - dropped
added = after - before
declared = Counter([v.strip() for v in NEW.values()] + [v.strip() for v in RH.values()] + [L(370).strip()])   # new lines, and the header both files need
undeclared = added - declared
moved = [n for n in channel if L(n).strip()]
print(f"old AGENTS.md: {len(old)} lines; old studio/RULES.md: {len(stub)} lines ({sum(before.values())} with text in all)")
print(f"new AGENTS.md: {len(studio.splitlines())} lines; new studio/RULES.md: {len(rules.splitlines())} lines")
print(f"lines moved to the channel file: {len(moved)} with text")
print(f"lines of the old pointer file dropped on purpose: {sum(dropped.values())}"); [print("   DROPPED:", k[:110]) for k in dropped]
print("lost or changed:", sum(lost.values())); [print("   LOST:", k[:110]) for k in lost]
print("added and declared:", sum((added & declared).values()))
print("added and NOT declared:", sum(undeclared.values())); [print("   EXTRA:", k[:110]) for k in undeclared]
sys.exit(1 if lost or undeclared else 0)
