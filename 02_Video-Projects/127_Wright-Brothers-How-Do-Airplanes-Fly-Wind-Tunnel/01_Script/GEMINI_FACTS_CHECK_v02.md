# Independent Gemini Facts & Exact-Quote Verification — `HOS:127` (`v02`, `J3690`)

- **Job:** `J3690` (`kind: facts`, Gemini `facts` lane, agent id `gemini`)
- **Date:** `2026-11-25` (UTC)
- **Reviewed PR & commit:** HOS PR `#774` (`origin/macbook/J3688`, commit `45953e56d7a41bca78d1985f451663246d47c649`, stacked cleanly on `origin/gemini/J3621-hos127-facts-audit` `925c2a92`)
- **Prior audits & rulings read:** `J3264` (`11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md`, Rule-E GO `97.2/100`, 5 script guardrails), `J3504` (PR `#756`, `v01` draft), `J3621` (PR `#771`, `01_Script/GEMINI_FACTS_CHECK_v01.md`, 5 blocking `FLAG`s + `R04`/`R07`/`R10`/`R14`/`R16` polishes), `J3622` (Acting Chief FIX ruling), and `J3688` (PR `#774`, `v02` revision resolving `FIX-1` through `FIX-8`).
- **Scope & constraints:** Independent end-to-end verification of `01_Script/wright_brothers_wind_tunnel_script_master_v02.md`, `01_Script/SOURCES.md`, `01_Script/FACT_NOTES_v02.md` (`R01–R18`), `10_Shorts/SHORTS_SCRIPTS_v02.md` (`S01` & `S02`), `11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md`, `11_Upload-Package/LAUNCH_PLAN.md`, `11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md`, saved search/neighbour evidence JSONs, archive layout, and `_template` plate stub status. Every live MUST QUOTE URL (`20` cited URLs plus CrossRef API for Smeaton `1759` DOI = `21` endpoints) was independently fetched and checked verbatim on `2026-11-25` (no `v01` rows inherited blindly). **No spoken rewrites made; no script lock, PR merge, VO, or picture spend authorised (`£0.00`).** All audited `v02` files remain byte-for-byte identical to PR `#774` (`45953e56d7a41bca78d1985f451663246d47c649`).

---

## 1. Exact Input SHA-256 Hashes Verified (`45953e56d7a41bca78d1985f451663246d47c649`)

All four required `v02` hashes match the `J3690` brief byte-for-byte, and all supporting packaging/state files are recorded for provenance:

```text
1488f59692ec624c9225b0d509d8dc47c7a1ded8e5b276514783d2fd5eddfdd4  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/wright_brothers_wind_tunnel_script_master_v02.md
9f331ba20a6f221668c53084fd26dd3d71ff1d7b95e8b6cba606094233f1e8da  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/SOURCES.md
7ad7cb465190e3d3bd1f32f8ccaf65e55e569ed7eb23afb10683c80c935f71b6  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/FACT_NOTES_v02.md
59e3005dee9df893d7c3c81f5bab2e9a5ffa8563e4cb97b4f0ab68721b174ef6  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/10_Shorts/SHORTS_SCRIPTS_v02.md
32fb501ae6a28b6c9a9729cd0650793786d5f746c3669cf45d6643950bbecd69  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/11_Upload-Package/PACKAGE_FIRST_SCORING_v01.md
3c9738a278fe902c7ce1af02f4ab431a20308bb18376b42858ad0ff3e3d1b989  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md
5007dc56184f984cbe7dce9caba2d57d525e29f2904faef1fbd41f8d5788e62e  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/11_Upload-Package/LAUNCH_PLAN.md
13f43cb8b74cd4f5cffc9204f06a807ff6e987c9344c0c9c207c98936ff20f5f  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/status.json
42889ac6288f09d705fb5bf99b69cdc565e92f25d3fbbb65be1a3d5e6d4825a7  02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/production-status.md
```

---

## 2. Executive Verdict & Handoff Recommendation (`J3622`)

- **Blocking `FLAG`s remaining:** **`0`** (down from `6` audited items / `5` blocking `FLAG`s in `v01`).
- **Explicit tally across `21` audited items (`R01–R18` + `S01–S02` + `P01`):**
  - **`OK`: `17`** (`R02, R03, R06, R07, R08, R09, R10, R11, R12, R13, R15, R16, R17, R18, S01, S02, P01`)
  - **`PARTIAL`: `4`** (`R01, R04, R05, R14` — **non-blocking**: every historical/scientific fact is backed verbatim by primary NASA GRC, Smithsonian NASM, or CrossRef Royal Society DOI sources; `PARTIAL` reflects only honestly labelled secondary Wikipedia citations used strictly for biographical lifespans per `SOURCES.md` rules)
  - **`FLAG`: `0`**
- **Recommendation to elected Chief (`J3622`):** **`KEEP` candidate for `v02` script, sources/facts, Shorts, and packaging lock** (advisory only — worker does NOT lock, merge, or spend). All `8` `J3621`/`J3622` items (`FIX-1` through `FIX-8`) and all `J3264` guardrails are cleanly resolved, `77/77` cited verbatim quotes verified live on `2026-11-25`, and zero unverified new spoken claims were introduced between `v01` and `v02`.

### Non-Blocking Hygiene Notes (Logged Transparently for Chief Awareness)

1. **`10_Shorts/SHORTS_SCRIPTS_v02.md` (`S01` table rows 3–4 word-count labels — zero spoken change needed):** Combined `S01` spoken VO is exact (`43` word tokens / `44` spoken words splitting `oh-one`, `144.9–148.3 wpm` over `17.8 s`, cleanly inside `16.0–19.0 s`). In the 4-row timing table (lines 36–37), Row 3 (`"So inside their Dayton bicycle shop, they built a wooden wind tunnel,"`) has **`12` words** (labelled `13w` → `133.3 wpm` over `5.4 s`) and Row 4 (`"tested up to two hundred tiny steel wings, and proved why..."`) has **`11` words** (labelled `10w` → `165.0 wpm` over `4.0 s`). Shifting the edit cut by `0.4 s` (`5.0 s` / `4.4 s`, total `17.8 s` unchanged) gives `144.0` / `150.0 wpm` with zero spoken edits and keeps R7 (`9.0–14.0 s`) completely clear.
2. **`SOURCES.md` line 58 & `FACT_NOTES_v02.md` Row 13 parenthetical `389 ft` note (not spoken):** `en.wikipedia.org/wiki/Wright_brothers` prints `"50 to 400 ft (15 to 122 m)"` rather than `"389 ft"` verbatim (the exact `389 ft` figure is non-spoken parenthetical context only). All spoken/on-screen `R13` numbers (`700–1,000`, `622.5 ft`, `26 s`, typical `300 ft` 1901 glides, Wilbur's quote) are 100% verified verbatim on primary Smithsonian, NASA GRC, and NPS pages.
3. **Smeaton `1759` DOI (`https://doi.org/10.1098/rstl.1759.0019`):** Resolving `doi.org` redirects cleanly to Royal Society Publishing (`royalsocietypublishing.org/rstl/article/doi/10.1098/rstl.1759.0019/119734/...`), which returns WAF `HTTP 403` to automated clients; CrossRef primary metadata API (`https://api.crossref.org/works/10.1098/rstl.1759.0019`) returns `HTTP 200` confirming author `John Smeaton`, issued `1759`, *Philosophical Transactions of the Royal Society of London*, pp. `100-174`, and exact title verbatim.

---

## 3. Resolution Audit: `FIX-1` Through `FIX-8` (`J3621` + `J3622`)

| Fix | Target Scope | Verdict | Independent `2026-11-25` Verification |
|---|---|---|---|
| **FIX-1** | Part 04 L126 spoken & L119 `SCALE:`; `FACT_NOTES_v02.md` Row 13 | **RESOLVED (OK)** | Spoken L126 now reads `"more than double their typical three-hundred-foot glides of nineteen oh-one"` (`622.5 / 300 = 2.075×`); `SCALE:` L119 matches. NASA GRC `1901-wind-tunnel-tests/` (`HTTP 200`) verified verbatim: `"The aircraft were flown frequently up to 300 feet in a single glide."` Contradictory `"almost double"` error removed; `1.60×` vs `389 ft` 1901 record noted transparently. |
| **FIX-2** | Part 05 L160 Harrison `H4` handoff; `SOURCES.md` #9; `FACT_NOTES_v02.md` Row 18 | **RESOLVED (OK)** | Spoken L160 reads `"Yet a century and a half earlier — in the very same year Smeaton published his table — another workshop craftsman faced an even deadlier measurement mystery: building a brass watch that had to keep perfect time on a pitching wooden ship at sea."` (`1901–1905 − 1759 = 142–146 yr`, exact same year `1759`). RMG `ZAA0037` (`HTTP 200`) verified verbatim: `"Marine timekeeper, H4"`, `"This is Harrison's prize-winning longitude watch, completed in 1759"`, `"Work began on H4 in 1755"`, `"Brass"`. RMG *Longitude found* (`HTTP 200` via redirect to `/stories/time/harrisons-clocks-longitude-problem`) verified verbatim for `1761` Jamaica trial. |
| **FIX-3** | Part 01 L9, L21 & `[TEACH]` L40; Short `S01` Caption Line 1 | **RESOLVED (OK)** | Part 01 L9 reads `"an eighteenth-century flight formula"`. Part 01 L21 (`"Alongside flawed wing-lift curves, a major culprit was an air-pressure number published in seventeen fifty-nine by English engineer John Smeaton..."`) and `[TEACH]` L40 accurately attribute the `1/3` lift drop to Smeaton's `0.005` *together with* flawed wing-lift curves, verified verbatim on NASA GRC `1901-wind-tunnel-tests/`. `S01` Caption Line 1 (`Their 1901 glider lifted only a third of what tables promised.`, yellow keyword `only a third`) aligns cleanly with spoken VO; ambiguous `"50% wrong"` removed. |
| **FIX-4** | Short `S02` (`SHORTS_SCRIPTS_v02.md` L46, L52, L54, L60) | **RESOLVED (OK)** | `"spin backward"` replaced across Caption Line 1, spoken VO, loop check, and Row 1 with `"spin the wrong way"`, matching Part 04 adverse-yaw `"well digging"` physics verified verbatim on Smithsonian NASM `researching-wright-way`. Zero occurrences of `"spin backward"` remain. |
| **FIX-5** | `PRE_BUILD_VIDIQ_AUDIT.md`, `LAUNCH_PLAN.md`, `PACKAGE_FIRST_SCORING_v01.md`; `SOURCES.md` #8 & Row 4 DOI | **RESOLVED (OK)** | Programmatic sweep confirms Primary Arm A (`Wright Brothers First Flight: The 1901 Wind Tunnel`, `50c`, `0` collisions) synced across all three docs; `20-gauge steel` wing models synced (`0` `"brass"` wing/airfoil slips, `0` `"THE TABLES LIED"`, `0` stale `6-foot`/`16-inch`/`66%`/`cardboard`/`UNVERIFIED` leaks); verified `v02` description line 1 aligned; Smeaton `1759` Royal Society DOI (`https://doi.org/10.1098/rstl.1759.0019`) added to `SOURCES.md` #8, Description `Sources:` line, and `FACT_NOTES_v02.md` Row 4 (verified live via CrossRef API `HTTP 200`). |
| **FIX-6** | Spoken `1899–1905` timeline `SCALE` (Part 05 L158); Part 01 `1900` vs `1901` chronology (L15 & L39); all `WHEN:` stamps `≤4` words | **RESOLVED (OK)** | Part 05 L158 speaks `"In just six years, they had gone from a five-foot kite to a thirty-nine-minute airplane."` matching Part 01 L31 `DATA:`/`SCALE:`. Part 01 L15 shows `1900` canvas tent camp near Kitty Hawk (`WHEN: Kitty Hawk, 1900`) and L39 shows `1901` wooden camp shed & 1901 glider at Kill Devil Hills (`WHEN: Kill Devil Hills, 1901`). Programmatic audit confirms **all `14/14` `WHEN:` stamps are `1–4` words** (`0` violations). |
| **FIX-7** | `10_Shorts/SHORTS_SCRIPTS_v02.md` pacing, overlays, and R7 title/loop handling | **RESOLVED (OK)** *(1 minor table-label note)* | `S01` (`43` tokens / `44` spoken, `17.8 s`, `145–148 wpm` overall; single `3w` overlay `1/3 PREDICTED LIFT` at `4.6–8.0 s`) & `S02` (`44` tokens / `46` spoken, `18.0 s`, `147–153 wpm` overall, all rows `142–158 wpm`; single `4w` overlay `KILL DEVIL HILLS, 1902` at `4.2–7.8 s`) both fit `16.0–19.0 s` (`atempo ≤ 1.06`), overlays sit strictly outside `0–2 s` and `9.0–14.0 s`, R7 exact live long title runs `9.0–14.0 s` fading cleanly out `3.8–4.0 s` before `≤ 0.3 s` Frame-0 match-cut loop, and table rows match combined VO paragraphs verbatim (`True`). Minor non-blocking label note on `S01` rows 3–4 (`12w`/`11w` vs `13w`/`10w`) logged in §2. |
| **FIX-8** | `v01` archive, `_template` plate stub exclusion, and `R04`/`R10`/`R14`/`R16` polishes | **RESOLVED (OK)** | `wright_brothers_wind_tunnel_script_master_v01.md` confirmed removed from `01_Script/` and archived at `_archive/02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/wright_brothers_wind_tunnel_script_master_v01.md`; default `npm run gate:episode` (no `--script`) resolves `v02` directly (`9/9 OK`). Unfilled `_template` stub `07_Edit-Project/parts/part-01_plates_v01.json` explicitly excluded from completed plate boards in `production-status.md`. `R04` full quote & `1759` DOI, `R10` bank-card thickness (`0.794 mm` vs `0.76 mm`), `R14` `"Ten responded..."` quote & Part 05 L133 `"By early nineteen oh-three"`, and `R16` `14 Dec` quotes & `WHEN: 17 Dec 1903` (`3w`) all verified. |

---

## 4. Independent Live URL Fetch & Exact-Quote Verification Log (`2026-11-25`)

Every URL in `01_Script/SOURCES.md` and `01_Script/FACT_NOTES_v02.md` (`20` cited URLs + CrossRef API = `21` endpoints) was independently fetched live on `2026-11-25`, and **`77/77` cited verbatim quote substrings** were verified against the freshly downloaded pages:

| Endpoint Key | Live URL Fetched (`2026-11-25`) | HTTP Status | Verbatim Quote Check |
|---|---|---|---|
| `NASA_SMEATON` | `https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/smeaton-coefficient/` | `200` (`73,338 B`) | `4/4` exact (`R03`, `R04`) |
| `NASA_BERNOULLI` | `https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/bernoulli-and-newton/` | `200` (`75,041 B`) | `4/4` exact (`R11`; `"Bernoulli” and “Newton” are correct.` has inline HTML tag before `.`) |
| `NASA_1901_TESTS` | `https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/1901-wind-tunnel-tests/` | `200` (`72,182 B`) | `3/3` exact (`R02`, `R13`) |
| `NASA_AIRCRAFT` | `https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/wright-brothers-aircraft/` | `200` (`74,077 B`) | `1/1` exact (`R13`) |
| `NASA_TUNNEL` | `https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/wind-tunnel/` | `200` (`70,813 B`) | `4/4` exact (`R01`, `R09`) |
| `NASA_MODELS` | `https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/wind-tunnel-models/` | `200` (`80,532 B`) | `2/2` exact (`R10`) |
| `NASA_BALANCE` | `https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/lift-balance-design/` | `200` (`72,474 B`) | `1/1` exact (`R09`) |
| `NASA_CONTROL_1902` | `https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/aircraft-control-1902-glider/` | `200` (`71,874 B`) | `1/1` exact (`R12`) |
| `NASA_PROPELLERS` | `https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/propellers/` | `200` (`70,077 B`) | `3/3` exact (`R14`, `R15`) |
| `SI_RESEARCH` | `https://airandspace.si.edu/explore/stories/researching-wright-way` | `200` (`508,933 B`) | `20/20` exact (`R04, R05, R06, R08, R10, R11, R12, R14, R15, R17`) |
| `SI_FLYER` | `https://airandspace.si.edu/collection-objects/1903-wright-flyer/nasm_A19610048000` | `200` (`197,503 B`) | `5/5` exact (`R05`, `R13`, `R16`) |
| `SI_KITTY_HAWK` | `https://airandspace.si.edu/stories/editorial/wright-brothers-made-history-kitty-hawk` | `200` (`131,843 B`) | `6/6` exact (`R02`, `R07`, `R16`) |
| `NPS_FIRST_FLIGHT` | `https://www.nps.gov/wrbr/learn/historyculture/thefirstflight.htm` | `200` (`42,592 B`) | `8/8` exact (`R07`, `R13`, `R16`) |
| `DOI_SMEATON_1759` + `CROSSREF_SMEATON` | `https://doi.org/10.1098/rstl.1759.0019` → `https://api.crossref.org/works/10.1098/rstl.1759.0019` | `403` (Royal Soc. WAF) / **`200`** (CrossRef JSON, `2,903 B`) | Exact metadata: `John Smeaton`, `1759`, *Phil. Trans. R. Soc. London*, pp. `100-174` (`R04`, `R18`) |
| `RMG_H4` | `https://www.rmg.co.uk/collections/objects/rmgc-object-79142` | `200` (`98,039 B`) | `5/5` exact (`R18`: `ZAA0037`, `H4`, `1759`, `1755`, `Brass`) |
| `RMG_LONGITUDE` | `https://www.rmg.co.uk/stories/topics/harrisons-clocks-longitude-problem` (→ `/stories/time/harrisons-clocks-longitude-problem`) | `200` (`99,557 B`) | `1/1` exact (`R18`: `1761` Jamaica trial) |
| `WIKI_WRIGHT` *(secondary)* | `https://en.wikipedia.org/wiki/Wright_brothers` | `200` (`988,823 B`) | Lifespans exact (`R01`); `"50 to 400 ft (15 to 122 m)"` exact (`R13` hygiene note in §2) |
| `WIKI_LILIENTHAL` *(secondary)* | `https://en.wikipedia.org/wiki/Otto_Lilienthal` | `200` (`356,247 B`) | `2/2` exact (`R05`: `23 May 1848` – `10 August 1896`) |
| `WIKI_SMEATON` *(secondary)* | `https://en.wikipedia.org/wiki/John_Smeaton` | `200` (`252,628 B`) | `2/2` exact (`R04`: `8 June 1724` – `28 October 1792`) |
| `WIKI_TAYLOR` *(secondary)* | `https://en.wikipedia.org/wiki/Charlie_Taylor_(mechanic)` | `200` (`139,370 B`) | `2/2` exact (`R14`: `May 24, 1868` – `January 30, 1956`) |

---

## 5. Claim-by-Claim Independent Verification Table (`R01–R18`, `S01–S02`, `P01`)

| ID | Audited Claim (`v02` Script / Visual / Shorts / Packaging) | Verdict | Primary / Secondary Sources Verified Live (`2026-11-25`) | Independent Verification Notes |
|---|---|---|---|---|
| **R01** | `WHO: Wilbur Wright (1867–1912) — Dayton bicycle maker` & `WHO: Orville Wright (1871–1948) — Dayton bicycle maker`; Dayton bicycle shop | **PARTIAL** *(non-blocking: secondary lifespans)* | Primary: NASA GRC (`wind-tunnel/`) · Secondary: Wikipedia (`Wright_brothers`) | Dayton bicycle shop verified verbatim on NASA GRC; lifespans verified on Wikipedia and honestly labelled secondary; `WHO` roles (`3w`) accurate for 1901. |
| **R02** | Summer `1901` glider produced only `1/3` predicted lift (`FACT: One-third predicted lift`), caused by flawed wing-lift curves together with Smeaton's `0.005` (`FIX-3`) | **OK** | Primary: NASA GRC (`1901-wind-tunnel-tests/`), Smithsonian NASM (`wright-brothers-made-history-kitty-hawk`) | Verbatim confirmed; Part 01 L21 & `[TEACH]` L40 cleanly resolve `J3621` FLAG-3a (`0.0033 / 0.005 = 2/3` alongside flawed wing-lift curves). |
| **R03** | 1901 glider designed to lift `100 lb` airframe + `150 lb` pilot (`250 lb`) in `15 mph` wind at `5°`, yet barely lifted itself | **OK** | Primary: NASA GRC (`smeaton-coefficient/`) | 100% verbatim confirmed. |
| **R04** | `WHO: John Smeaton (1724–1792) — English civil engineer`; `0.005` published `1759` (`WHEN: 1759`) vs Wrights' `0.0033` (modern `0.00327`) — `>50% too high` (`+51.5%`, `142` yr before `1901`) (`FIX-3`, `FIX-5`, `FIX-8`) | **PARTIAL** *(non-blocking: secondary lifespan)* | Primary: NASA GRC (`smeaton-coefficient/`), Smithsonian NASM (`researching-wright-way`), CrossRef DOI `10.1098/rstl.1759.0019` · Secondary: Wikipedia (`John_Smeaton`) | Full Smithsonian quote restored (`"...0.0033 for Smeaton's coefficient."`), `1759` Royal Society DOI verified via CrossRef `HTTP 200`, math exact (`+51.5%` / `+52.9%`); lifespan honestly labelled secondary. |
| **R05** | `WHO: Otto Lilienthal (1848–1896) — German glider pioneer`; died in `1896` stall (`WHEN: Germany, 1896`); compiled published lift/drag table | **PARTIAL** *(non-blocking: secondary lifespan)* | Primary: Smithsonian NASM (`nasm_A19610048000`, `researching-wright-way`) · Secondary: Wikipedia (`Otto_Lilienthal`) | Verbatim confirmed; `WHO` role (`3w`) year-accurate; lifespan honestly labelled secondary. |
| **R06** | `30 May 1899` Wilbur wrote to Smithsonian (`WHEN: Dayton, May 1899`); summer `1899` `5-foot` (`1.5 m`) wing-warping biplane kite | **OK** | Primary: Smithsonian NASM (`researching-wright-way`) | 100% verbatim confirmed. |
| **R07** | U.S. Weather Bureau inquiry → Kitty Hawk & Kill Devil Hills, NC; `1900` canvas tent camp (`WHEN: Kitty Hawk, 1900`, L15) vs `1901` wooden camp shed & 1901 glider (`WHEN: Kill Devil Hills, 1901`, L39) (`FIX-6`) | **OK** | Primary: Smithsonian NASM (`wright-brothers-made-history-kitty-hawk`), NPS (`thefirstflight.htm`) | `J3621` R07 visual-chronology mismatch cleanly resolved; Kitty Hawk village vs Kill Devil Hills dunes distinguished accurately. |
| **R08** | Autumn `1901` (`WHEN: Dayton, autumn 1901`) horizontal third bicycle wheel test: wing needed `>3×` greater angle than Lilienthal predicted (`FACT: Over 3× expected angle`) | **OK** | Primary: Smithsonian NASM (`researching-wright-way`) | 100% verbatim confirmed. |
| **R09** | `Oct–Dec 1901` belt-driven open-return wooden wind tunnel; nearly a month perfecting flow-straighteners; lift & drag balances from bicycle spokes and hacksaw blades (`FACT: Hacksaw-blade lift balance`) | **OK** | Primary: NASA GRC (`wind-tunnel/`, `lift-balance-design/`) | 100% verbatim confirmed. |
| **R10** | `100–200` (up to `200`) miniature wings cut/hammered/filed/soldered from `20-gauge` steel (`1/32` in = `0.794 mm` ≈ ISO bank card `0.76 mm`), nearly `50` formally charted (NASA: `~30` detailed) (`FIX-5`, `FIX-8`) | **OK** | Primary: NASA GRC (`wind-tunnel-models/`), Smithsonian NASM (`researching-wright-way`) | Verbatim confirmed; Row 10 bank-card comment fixed (`~4%` difference) and packaging docs synced to `20-gauge steel`. |
| **R11** | Accurate lift physics (debunks equal-transit-time myth; faster upper flow / pressure difference + downward airflow deflection; long, narrow, gently curved wings beat thick 1901 airfoil) | **OK** | Primary: NASA GRC (`bernoulli-and-newton/`), Smithsonian NASM (`researching-wright-way`) | Verbatim confirmed; `J3264` Guardrail 2 PASS. |
| **R12** | `1902` glider adverse yaw / `"well digging"` turn reversals (`WHEN: Kill Devil Hills, 1902`); fixed double tail → movable single rear rudder linked to hip cradle + front elevator = world's first three-axis control | **OK** | Primary: Smithsonian NASM (`researching-wright-way`), NASA GRC (`aircraft-control-1902-glider/`) | 100% verbatim confirmed. |
| **R13** | Sept–Oct `1902` (`WHEN: Oct 1902`): `700–1,000` glides, best `622.5 ft` (`191.5 m`) in `26 s` — `"more than double their typical three-hundred-foot glides of nineteen oh-one"`; Wilbur quote (`FIX-1`) | **OK** | Primary: Smithsonian NASM (`nasm_A19610048000`), NASA GRC (`1901-wind-tunnel-tests/`, `wright-brothers-aircraft/`), NPS (`thefirstflight.htm`) | `J3621` FLAG-1 cleanly resolved (`622.5 / 300 = 2.075×`; `"almost double"` removed; `1.60×` vs `389 ft` record noted transparently; see §2 hygiene note 2). |
| **R14** | `"By early nineteen oh-three"`, `10` engine makers had replied, none met spec; `WHO: Charlie Taylor (1868–1956) — Wright shop machinist` built `12-hp` cast-aluminium engine in `6` weeks (`12 Feb 1903`, `2×` typical `6-hp` lawn-mower engine) (`FIX-8`) | **PARTIAL** *(non-blocking: secondary lifespan)* | Primary: Smithsonian NASM (`researching-wright-way`), NASA GRC (`propellers/`) · Secondary: Wikipedia (`Charlie_Taylor_(mechanic)`) | `"Ten responded..."` verbatim quote added to Row 14 and Part 05 L133 tightened; cast-aluminium first & NASA `6-hp` comparison verified verbatim; lifespan honestly labelled secondary. |
| **R15** | `8.5-foot` laminated-spruce rotary-wing counter-rotating propellers (`~350 rpm`), carved with hatchet & drawknife, driven by bicycle chains (one figure-eight) | **OK** | Primary: Smithsonian NASM (`researching-wright-way`), NASA GRC (`propellers/`) | 100% verbatim confirmed. |
| **R16** | `14 Dec 1903` coin toss, `60-foot` rail, `3.5 s` stall; `17 Dec 1903 10:35 a.m.` (`WHEN: 17 Dec 1903`), `27 mph` wind, Orville `12 s / 120 ft` (`2` rails), Wilbur 4th flight `59 s / 852 ft` (`7.1×`), gust rolled empty plane (`FIX-6`, `FIX-8`) | **OK** | Primary: Smithsonian NASM (`nasm_A19610048000`, `wright-brothers-made-history-kitty-hawk`), NPS (`thefirstflight.htm`) | `14 Dec` quotes appended to Row 16, `WHEN:` tightened to `17 Dec 1903` (`3w`), all figures & ratios exact. |
| **R17** | `1899–1905` animated timeline & `5 Oct 1905` Huffman Prairie flight (`30` circles, `39 min`, `24.5 mi`, `195×` `12 s`), with spoken 6-year timeline `SCALE` in Part 05 L158 (`FIX-6`) | **OK** | Primary: Smithsonian NASM (`researching-wright-way`) | Verbatim confirmed; spoken `SCALE` added cleanly; transparent `38m03s` diary note preserved (`190.25×` still `"nearly two hundred times longer"`). |
| **R18** | Final handoff (Part 05 L160): John Harrison's `1759` brass marine longitude watch `H4` — `"a century and a half earlier — in the very same year Smeaton published his table"` (`FIX-2`) | **OK** | Primary: Royal Museums Greenwich (`ZAA0037` `rmgc-object-79142`, *Longitude found*), CrossRef DOI `10.1098/rstl.1759.0019` | `J3621` FLAG-2 cleanly resolved (`1901–1905 − 1759 = 142–146 yr` = century and a half, exact year `1759`); brass watch & `1755–1759` / `1761` trial verified verbatim on RMG. |
| **S01** | Short A (`SHORTS_SCRIPTS_v02.md`): *Why Did the Wright Brothers Build a Wind Tunnel?* (`48c`, `0` collisions, `43w` tokens / `44` spoken ≈ `17.8 s`, Sat 2 Jan 2027); Caption Line 1 concrete fact (`FIX-3`, `FIX-7`) | **OK** *(1 minor table-label note in §2)* | Backed by R02, R09, R10 | `J3621` FLAG-3b & `J3622` FIX-7 resolved: Caption Line 1 matches spoken fact, single `3w` overlay `1/3 PREDICTED LIFT` (`4.6–8.0 s`) clear of `0–2 s` & `9.0–14.0 s`, R7 title `9.0–14.0 s` fades cleanly before `≤ 0.3 s` loop, paragraph = table rows (`True`). |
| **S02** | Short B (`SHORTS_SCRIPTS_v02.md`): *How Did the Wright Brothers Steer the First Plane?* (`50c`, `0` collisions, `44w` tokens / `46` spoken ≈ `18.0 s`, Fri 1 Jan 2027); `"spin the wrong way"` (`FIX-4`, `FIX-7`) | **OK** | Backed by R12 | `J3621` FLAG-4 & `J3622` FIX-7 resolved: adverse-yaw wording exact, all 4 rows `142–158 wpm`, single `4w` overlay `KILL DEVIL HILLS, 1902` (`4.2–7.8 s`) clear of `0–2 s` & `9.0–14.0 s`, R7 title `9.0–14.0 s` fades cleanly before `≤ 0.3 s` loop, paragraph = table rows (`True`). |
| **P01** | `PRE_BUILD_VIDIQ_AUDIT.md`, `LAUNCH_PLAN.md`, `PACKAGE_FIRST_SCORING_v01.md`, collision JSONs (`80` rows), `neighbours.json` (`gate=PASS`), `v01` archive & `_template` stub (`FIX-5`, `FIX-8`) | **OK** | Repo evidence JSONs + OWB `2026-11-20.md` + `SOURCES.md` #8 | `J3621` FLAG-5 & `FIX-8` cleanly resolved: Arm A (`50c`) primary across all docs, `0` collisions across all `6` titles (`80` rows), `20-gauge steel` models synced, `0` stale outline leaks, `v01` archived out of `01_Script/`, `_template` plate stub excluded. |

---

## 6. Programmatic Verification Summary (`2026-11-25`)

### 6.1 Spoken Diff (`v01` → `v02`)
Unified spoken-text diff against `_archive/02_Video-Projects/127_Wright-Brothers-How-Do-Airplanes-Fly-Wind-Tunnel/01_Script/wright_brothers_wind_tunnel_script_master_v01.md` confirmed exactly **6 targeted spoken edits** (`FIX-1`, `FIX-2`, `FIX-3`, `FIX-6`, `FIX-8`), with zero unverified new claims introduced:
1. Part 01 L9: `"a century-old flight formula"` → `"an eighteenth-century flight formula"` (`FIX-3`)
2. Part 01 L21: `"The culprit was an air-pressure number published in the seventeen hundreds..."` → `"Alongside flawed wing-lift curves, a major culprit was an air-pressure number published in seventeen fifty-nine..."` (`FIX-3`)
3. Part 04 L126: `"more than double their nineteen oh-one mark"` → `"more than double their typical three-hundred-foot glides of nineteen oh-one"` (`FIX-1`)
4. Part 05 L133: `"In nineteen oh-three, ten engine makers replied"` → `"By early nineteen oh-three, ten engine makers had replied"` (`FIX-8`)
5. Part 05 L158: appended `"In just six years, they had gone from a five-foot kite to a thirty-nine-minute airplane."` (`FIX-6`)
6. Part 05 L160: `"Yet two centuries earlier, another workshop craftsman..."` → `"Yet a century and a half earlier — in the very same year Smeaton published his table — another workshop craftsman..."` (`FIX-2`)

### 6.2 Long Part 01 First-Minute Milestones & Full Marker Audit (`v02`)
- **Part 01 spoken timing check (`@ 150 wpm` / `@ 154 wpm`):**
  - `L05` (`17w`, `0.0–6.8 s` / `0.0–6.6 s`): Title question (`≤ 0:08` **PASS**; answer image by `0:05`)
  - `L09` (`+17w = 34w`, `6.8–13.6 s` / `6.6–13.2 s`): Physical proof & promise (`≤ 0:15` **PASS**)
  - `L13` (`+24w = 58w`, `13.6–23.2 s` / `13.2–22.6 s`): Stakes (`≤ 0:25` **PASS**)
  - `L17` (`+18w = 76w`, `23.2–30.4 s` / `22.6–29.6 s`): First real fact (`< 0:45` **PASS**)
  - `L21` (`+36w = 112w`, `30.4–44.8 s` / `29.6–43.6 s`): Early `DATA+SCALE` Smeaton `0.005` vs `0.0033` lands inside `0:25–0:40` (**PASS**)
- **Marker counts verified programmatically:** `WHO: 5` (all roles `3w ≤ 4w`), `WHEN: 14` (all `1w–4w ≤ 4w`), `DATA: 7`, `SCALE: 7` (all 7 spoken & sourced), `FACT: 4` (all `3w–4w ≤ 4w`), `LABEL: 27` (all `2w–4w ≤ 4w`), `EXPLORER ACTS: 2` (`2:06` Part 02 & `7:22` Part 05, outside first minute), `TEACH: 5`, `CHAPTER CARD: 4`.

### 6.3 Shorts `S01` & `S02` Programmatic Pacing Check (`SHORTS_SCRIPTS_v02.md`)
- **`S01`:** `43` tokens / `44` spoken words (`17.8 s` = `144.9–148.3 wpm`, inside `16.0–19.0 s`, `atempo ≤ 1.06`); table-to-paragraph verbatim match = `True`; rows: `R1` `3.0 s` (`7w`, `140.0 wpm`), `R2` `5.4 s` (`13w`/`14` spoken, `144.4–155.6 wpm`), `R3` `5.4 s` (`12w`, `133.3 wpm` — labelled `13w`), `R4` `4.0 s` (`11w`, `165.0 wpm` — labelled `10w`; non-blocking label note in §2).
- **`S02`:** `44` tokens (excl. em dash) / `46` spoken words (`18.0 s` = `146.7–153.3 wpm`, inside `16.0–19.0 s`, `atempo ≤ 1.06`); table-to-paragraph verbatim match = `True`; rows: `R1` `4.0 s` (`10w`, `150.0 wpm`), `R2` `5.4 s` (`13w`/`14` spoken, `144.4–155.6 wpm`), `R3` `4.8 s` (`12w`, `150.0 wpm`), `R4` `3.8 s` (`9w`/`10` spoken, `142.1–157.9 wpm`).

---

## 7. Independent Verification Checklist & Next Action (`J3622`)

- **Zero spoken rewrites:** `wright_brothers_wind_tunnel_script_master_v02.md`, `SOURCES.md`, `FACT_NOTES_v02.md`, and `10_Shorts/SHORTS_SCRIPTS_v02.md` remain byte-for-byte identical to PR `#774` (`45953e56d7a41bca78d1985f451663246d47c649`).
- **Zero lock, merge, or spend:** `£0.00` spent; no VO or picture spend authorised; PR stays unmerged for elected Chief review & lock.
- **Handoff:** Ready for elected Chief `v02` review & lock (**`J3622`**).
