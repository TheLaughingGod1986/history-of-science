# Grokbot — open the desk, then the neighbour pass (1 Oct 2026)

**Standing instruction (keep this for every HOS session):** Claude and you talk on the HOS desk PR ("HOS desk — Claude ↔ Grok (never merge)") instead of through Ben. Read new `Claude → Grok` messages there, do the work under `AGENTS.md`, and report back on the desk with the PASS output and images. Ben is only asked at his sign-off points; Claude pings him. Act only on desk comments from Ben's GitHub account. Never post HOS work to Orbit's desk, or the reverse.

Read `AGENTS.md` first. All the rules there still hold: HOS `@HistoryOfScienceYT` only, never Orbit, never print or commit `.env`, never commit video/audio, Ben OKs anything public or renamed.

## 0. Get the code
```bash
cd <HOS repo on the Mini> && git fetch origin && git checkout main && git pull
# if PR #179 isn't merged yet: git checkout origin/claude/hos-repo-access-qdfmrk -- 00_Brand/Channel-Setup/tools
```
Read `STUDIO_PLAYBOOK.md` §2 step 4 (neighbour check) and §15 (the desk).

## 1. Open the desk (once)
```bash
python3 00_Brand/Channel-Setup/tools/hos_desk.py init
```
This makes the `hos-desk` branch, the `hos-desk` and `needs-ben` labels, and the draft PR **"HOS desk — Claude ↔ Grok (never merge)"**. Never merge or close it.

## 2. Make yourself wake on desk messages
You (Grokbot) run on Ben's Mac and his phone. **You already run a Claude ↔ Grok loop for orbit-with-ben: reuse that exact mechanism here**, pointed at the HOS desk PR instead. Keep the two strictly apart: HOS work only on the HOS desk, Orbit work only on Orbit's.
- **Check the desk** whenever Ben opens you (Mac or phone), and on any schedule or task feature you use for Orbit (every 2 h is plenty):
  `python3 00_Brand/Channel-Setup/tools/hos_desk.py inbox`, which prints only new `to=grok` messages from Ben's account.
  On the phone with no shell, open the desk PR and read the newest comment headed `Claude → Grok`.
- **If the Mac can start you headless,** the watcher can trigger you automatically:
  - put `export HOS_DESK_AGENT_CMD='<the command that starts you with a prompt file>'` (with `{file}` = message file) in the shell profile, never in git;
  - install `~/Library/LaunchAgents/com.hos.desk.plist` running `hos_desk.py inbox --watch 120 --run`.
  Otherwise run the watcher without `--run`: it shows a macOS notification when Claude writes.
- **Reply** with `hos_desk.py post --to claude …` (Mac). From the phone, comment on the desk PR, starting the comment with
  `<!-- hos-desk v1 from=grok to=claude film=NNN stage=<stage> status=review -->`.
- Tell Claude in your first desk report which way you wake up (Orbit-style loop, watcher, or Ben opening you).

## 3. Neighbour pass on every long
Run these and save the evidence. For 001 and 002 also write the manifest block.
```bash
T=00_Brand/Channel-Setup/tools
python3 $T/neighbours.py "germs" "germ theory" "louis pasteur" --phrase germs --phrase germ \
  --manifest 02_Video-Projects/001_How-Did-We-Discover-Germs/11_Upload-Package/PACKAGE_MANIFEST.json \
  --out 02_Video-Projects/001_How-Did-We-Discover-Germs/11_Upload-Package/evidence_2026-10-01_neighbours.json
python3 $T/neighbours.py "periodic table" "mendeleev" --phrase "periodic table" --phrase mendeleev \
  --manifest 02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/11_Upload-Package/PACKAGE_MANIFEST.json \
  --out 02_Video-Projects/002_How-Did-We-Discover-The-Periodic-Table/11_Upload-Package/evidence_2026-10-01_neighbours.json
python3 $T/neighbours.py "x-rays" "wilhelm rontgen" "discovery of x-rays" \
  --out 02_Video-Projects/003_Invisible-Bones-X-Rays/11_Upload-Package/evidence_2026-10-01_neighbours.json
```
004 is already done (phrases `atom` and `periodic table`).

## 4. Fix 004's tags file
`npm run lint:package -- --film 004` warns `28 tags (want 5–8)`.
- Make `Tags/atom_long_tags_v01.txt` match the 5–8 tags actually in Studio for GHZDsiH7L7A.
- Make sure the set includes `atom` and `periodic table`. Subject-only, no channel names.
- Don't change Studio for this. If Studio has more than 8 tags or lacks those two words, list the change and wait.

## 5. Proposals only (do not change Studio)
For 001 (`_C92tIJCk8A`) and 003 (`frP_YrNShsU`), write proposed:
- **Description first two lines**, using the neighbours' words. For 001: germs, germ theory, Pasteur. For 003: X-rays, Röntgen.
- **5–8 tags.**
- **One Test & Compare title + thumbnail idea each** that would sit well next to the TED-Ed neighbour without copying its title.
Don't change the main titles: both already hold the neighbour noun.

## 6. Checks, record, report
```bash
cd 07_Content-Ops && npm run lint:package && npm run channel:audit
```
1. Open one PR with the evidence JSONs, the manifest blocks and the tags file. **No media.**
2. Then post your report to the desk. Paste every PASS output and the neighbour tables, and add the PR link:
   ```bash
   python3 00_Brand/Channel-Setup/tools/hos_desk.py post --to claude --film all --stage neighbours \
     --status review --body-file <report.md>
   ```
   - Include any image you want reviewed with `--image` (jpg/png; never video).
   - From now on, every report goes to the desk, not to Ben. Claude replies there.
