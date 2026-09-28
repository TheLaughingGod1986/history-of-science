# Part 04 rough v01 — VO-literal audit (Ben FAIL)

**Cut:** `hos_004_part04_rough_v01.mp4` · sha256 `49efa91a…f9fa`  
**Verdict:** FAIL — remint to `hos_004_part04_rough_v02.mp4`. Do not land PR as PASS. Do not start Part 05.

**House rule for v02:** every plate must literally show its VO line; same set stays continuous across a sequence; no decorative / random action.

**Stadium lock (VO says “football”):** UK **soccer** pitch — centre circle, penalty box, **rectangular soccer goal with net**. Same empty stadium, same goal, same markings, same dusk lighting on plates **16–18**. Forbidden: American football posts/yard lines, rugby H-posts, crowded stands, sport switching mid-sequence.

| id | VO line (board) | What v01 shows | Verdict | Fix |
|---|---|---|---|---|
| `01_manchester_1909` | Manchester, 1909. Rutherford has a new kind of bullet. | Bearded physicist at glowing gold-foil chamber in lab | **KEEP** | — |
| `02_alpha_bullets` | Alpha particles, tiny and fast, thrown out by radioactive rocks. | Many vacuum tubes glowing at once + particle stream | **FIX** | One clear action: rock samples emit tiny glowing alpha particles (no room-wide flare) |
| `03_fire_at_gold` | Geiger & Marsden fire them at gold beaten thinner than paper. | Two men fire glowing beam at thin gold foil | **KEEP** | — |
| `04_thin_gold_foil` | …gold beaten thinner than paper. Picture yourself in that room. | ECU paper-thin gold foil in frame | **KEEP** | — |
| `05_lights_off` | Picture yourself in that room. The lights are off, | Lab with **many flames / lamps flaring at once** | **FIX** | Lights extinguish → deep dark; one darken action only |
| `06_eyes_adjust_scope` | …eyes adjust. You look through a microscope at a small screen. | Microscope already blasting green particle screen | **FIX** | Dark room; lean into quiet eyepiece / dark screen (flashes belong on next plate) |
| `07_green_flash_count` | Tiny green flash, and you count it. | Grid of many green dots (not sparse flashes) | **FIX** | Sparse one-by-one green pin-flashes on dark screen |
| `08_pudding_punch` | If Thomson's pudding is right, every bullet should punch straight through. | Space battle: silver bullets + fire trails into pink sphere / Saturn | **FIX** | Soft plum-pudding atom sphere; glowing bullets punch **straight through** |
| `09_almost_all_pass` | Almost all of them do. | **Blue rockets / smoke trails over steampunk city** (Ben #2) | **FIX** | Same foil: dense stream passes straight through gold leaf |
| `10_one_bounces` | About one in 8,000 bounces back. | Chaotic bullets flying at camera in busy lab | **FIX** | Foil: almost all pass; **one** particle ricochets steeply back |
| `11_shell_tissue` | …fired a huge shell at a piece of tissue paper, | Steampunk projector at iridescent screen | **FIX** | Literal artillery **shell** racing toward a sheet of **tissue paper** (wonder, not gore) |
| `12_shell_comes_back` | …and it came back and hit you. | **Gold seashell in blue waves + clock machines in space** (Ben #4) | **FIX** | Same metaphor: shell **bounces back** toward camera from the tissue |
| `13_mass_packed` | Nearly all of an atom's mass is packed into a tiny, positive centre, | Busy atom + **DNA helix** + gauges | **FIX** | Cutaway: mass packs into tiny bright positive centre; **no DNA** |
| `14_nucleus_electrons` | …the nucleus. The electrons sit far outside it. | Clear nucleus + distant electrons | **KEEP** | — |
| `15_almost_empty` | Everything in between is almost empty. How empty? | Brass **orrery / planets** under glass dome in space | **FIX** | Atom cutaway: vast empty middle between pinprick centre and far electrons |
| `16_explorer_stadium_pea` | Football stadium, holding a pea. Nucleus = that pea. | Explorer + pea but **American football yard lines**, crowded stands (Ben #1) | **FIX** | Explorer on **empty UK soccer pitch**, rectangular soccer goal, pea = nucleus |
| `17_electrons_past_seats` | Electrons out past the back row of seats. | Different crowded futuristic stadium (soccer goal OK) | **FIX** | **Same** empty UK stadium; camera lifts past empty back-row seats |
| `18_nothing_at_all` | Everything else… is nothing at all. | Crowded steampunk stadium + clocks | **FIX** | **Same** empty UK stadium: vast empty pitch/stands — nothing |
| `19_nucleus_question` | What makes one nucleus different from another? | Jar of atoms with fake **CH / CO** lettering | **FIX** | Two bare nuclei, different soft charge colours; **no text** |
| `20_lawyer_amateur` | Dutch lawyer / amateur… bold guess | Study desk + board with **fake element tiles** | **FIX** | Lawyer-amateur at desk; **blank** table board + nucleus sketch; no fake letters |
| `21_place_equals_charge` | Place in the table might equal positive charge in its nucleus. | Machine + garbled embossed text | **FIX** | Blank place slot glow-linked to tiny positive nucleus charge; **no text** |
| `22_cannot_measure_yet` | Brilliant guess, but nobody could measure it. Yet. | Busy glowing apparatus (many actions) | **FIX** | Unused measuring instruments; glow dims — unanswered; one quiet settle |

**Summary:** KEEP **4** · FIX **18**

**Remint path:** Flow CDP first (gate). Credits ~162 → next Fast would breach ~150 buffer → **Gemini API same Veo 3.1** (`veo-3.1-lite-generate-preview` / `veo-3.1-generate-preview`). Log path + spend per plate in `PART04_MINT_LOG_v02.json`.


## v02 remint notes

- Reminted 18 FIX plates; KEEP 4 carried from v01.
- Path mix: mostly `gemini-api` Veo 3.1; Flow Fast for plates after Gemini `429 RESOURCE_EXHAUSTED`; Flow credits ended ~92 (I2V Quality blocked).
- Stadium lock (16–18): UK soccer pitch + rectangular goal + empty stands — Explorer pea beat reminted.
- City rockets (09) replaced with foil pass-through; seashell/clock space (12) replaced with artillery-shell metaphor.
- Soft residual risk for Ben UAT: `05_lights_off` can still drift toward a lit hall; `09` sometimes bleeds stadium bokeh behind the foil; `12` rebound vs punch-through can be soft. Further remints need Flow credits or Gemini quota reset.

