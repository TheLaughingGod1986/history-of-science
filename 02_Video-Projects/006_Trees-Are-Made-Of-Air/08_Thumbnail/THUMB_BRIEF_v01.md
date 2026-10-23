# HOS 006 Thumbnails — Step 1 Concepts & Flow Credit Price Pass (`J0858`)

- **Film:** `006_Trees-Are-Made-Of-Air` (*The Willow Tree That Was Made of Air* / *Where Does a Tree's Weight Come From?*)
- **Air date:** Proposed Thu 5 Nov 2026 18:00 UK (`18:00Z`), normal publish; thumbnail stage due **29 Oct 2026** (before Ben's final OK on **1 Nov 2026**).
- **Job:** OWB Queue `J0858` (Step 1 of 2, `gemini` covering, 23 Oct 2026).
- **Status:** **No mint. No spend (`0` Flow credits, `£0.00`).** Parked for Chief: `parked for Chief: 006 thumbnail price + concept pick`.

---

## 1. House HOS Thumbnail Lock & LEARNINGS Rule #1 Framing

1. **House HOS look (`THUMBNAIL_AND_TITLE_RULES.md` §2 & §2.B):**
   - **Art on Flow (`1280×720`, 16:9):** Premium 3D cartoon key art in warm golden Flemish study / sunlit laboratory light, matching live HOS `001` (Germs), `002` (Periodic Table), `004` (Atom), and `005` (Harvey). Attach live long thumb (`00_Brand/Channel-Setup/style/long/001_how_did_we_discover_germs.jpg`), 006 look ref (`04_sunny_window_v01.jpg`), and `01_Character/05_Generation-References/hos-explorer-reference-v01.jpg`.
   - **Hero object (right two-thirds, `x ≈ 520..1240`):** One giant, immediately readable object from the cold open / Part 02 experiment, whole and uncut, with **zero AI-made text or numbers** on the plate and the **bottom-right corner (`x > 1060, y > 580`) empty** for the YouTube duration badge.
   - **The Explorer (lower left, `x ≈ 80..340, y ≈ 340..720`):** On-model (teal coat, tan waistcoat, brown bow tie, round gold glasses, satchel), ~48–52% of frame height so his glasses and reaction read clearly at `168×94` phone size.
   - **Lettering from the cover builder (`£0 / 0 credits`, deterministic in code):** Upper-left clear band (`x ≈ 90..500, y ≈ 60..325`, above the Explorer's hair and completely left of the hero object). Rendered by the Python composer (`Georgia Bold` display serif, cream words + **one larger gold punch word**, dark ink outline, drop shadow, and top/bottom gold scroll flourishes; `Times New Roman Bold` lining figures if numerals are used).
2. **Positive-question framing (`05_Analytics/LEARNINGS.md` Rule #1 & `THUMBNAIL_AND_TITLE_RULES.md` §2.5 / §2.B.1):**
   - **Proven channel rule:** Positive questions naming the concrete subject outperform negative or abstract statements across 10+ OWB and HOS uploads (e.g., HOS `29bpGAI0wb8` *What happens if you keep cutting gold in half?* 1,218 views; `c2q7w0pgcn8` *Who Discovered Infrared Light?* 90.5% avg viewed; `T009` Germs B *INVISIBLE LIFE?*).
   - **Cover words never repeat the title (`THUMBNAIL_AND_TITLE_RULES.md` §2.5):** Each concept below uses a **2–4 word positive question** naming the concrete object/substance in the hook, with **one gold punch word** and **zero content-word overlap** with Manifest Title A (*"The Willow Tree That Was Made of Air"*) or Manifest Title B (*"Where Does a Tree's Weight Come From?"*).
   - **Long Title pairing (`PACKAGE_MANIFEST.json` `titleAbc`):**
     - **Title A (current manifest primary):** *The Willow Tree That Was Made of Air* (36 chars; shares neighbour phrase `tree`).
     - **Title B (current manifest T&C, positive question per LEARNINGS #1):** *Where Does a Tree's Weight Come From?* (37 chars; positive question naming `tree`).
     - **Optional Title C (positive question with hook twist):** *How Can a Tree Grow Out of Thin Air?* (36 chars; combines positive-question framing with the "thin air" hook).

---

## 2. Three Thumbnail Concepts (from 006's Hook)

| Concept | Hook Beat (Script) | Lettering (2–4 Words, Positive Question) | Gold Punch Word | Hero Object (Right 2/3) & Explorer (Lower Left) | Fact Lock (`FACT_NOTES_v01.md`) |
|---|---|---|---|---|---|
| **A (Primary candidate)** | `0:00` Answer Image & Part 05 `7:22`: A willow growing out of thin air & sunlight | **`WOOD / FROM / SKY?`** *(3 words; 0 overlap with Title A or B. Alt if paired with Title B only: **`GROWN / FROM / AIR?`**)* | **`SKY?`** *(or **`AIR?`**)* | **Right 2/3:** Giant living willow in a terracotta pot on a sunlit oak table by an arched window; luminous golden-teal ribbons of sky/air stream through the window into the green leaves and condense into glowing solid wood rings inside a clean cutaway of the thick trunk. **Lower left:** Explorer (~50% height) looking up in wonder at the glowing trunk cutaway. | Rows 1 & 48: *"The wood of a tree is built mostly out of thin air… About half of dry wood is carbon, and every bit of that carbon came out of the air."* |
| **B (Test & Compare candidate)** | `0:04` Cold-Open Balance & Part 02 `2:06–2:19`: Van Helmont's brass scales (169 lb tree vs unchanged soil) | **`DO PLANTS / EAT / SOIL?`** *(4 words; 0 overlap with Title A or B; matches GB YouTube autocomplete hit. Alt 3-word: **`FED BY / SOIL?`** or **`164 POUNDS / GAINED?`**)* | **`SOIL?`** *(or **`GAINED?`**)* | **Right 2/3:** Giant 17th-century polished brass balance scale on an oak lab table. Lower-right pan weighed down low by the massive uprooted willow tree (thick trunk, roots, green canopy); raised middle-right pan holds the clay pot of dried dark furnace soil — beam tilted sharply toward the tree. Blank pans/weights (no AI text). **Lower left:** Explorer (~50% height) leaning in beside the balance, staring at the tipped beam. | Rows 8–19: Aristotle taught roots eat soil like a mouth; van Helmont's willow gained 164 lb (5 lb → 169 lb) while 200 lb of dried furnace soil lost only ~2 oz. |
| **C (Alternate / 3-way T&C candidate)** | Part 01 `0:56` & Part 02 `1:32–2:35`: Van Helmont's 5-year sealed clay pot & pure water test | **`GROWN / ON / WATER?`** *(3 words; 0 overlap with Title A or B. Alt 3-word: **`ONLY / RAIN / WATER?`** or **`FIVE YEARS / SEALED?`**)* | **`WATER?`** *(or **`SEALED?`**)* | **Right 2/3:** Hero close-up of van Helmont's large earthen clay pot sealed with its perforated tin-plated iron lid (tiny holes keeping dust out while glistening silver water droplets pour from a tilted glass vessel through the lid), with a thick willow trunk bursting up through the lid's collar. **Lower left:** Explorer (~50% height) pointing at the perforated metal lid and water droplets. | Rows 13–14 & 19–21: Covered with a perforated tin-plated iron sheet (`"lest any dust from outside should get into the soil"`), given only rain/distilled water for 5 years (`"from water alone"`). |

### Pre-Gate Self-Check on All 3 Concepts (`THUMBNAIL_AND_TITLE_RULES.md` §2.B.3)

- **HOOK:** **PASS** on A (`WOOD FROM SKY?`), B (`DO PLANTS EAT SOIL?`), and C (`GROWN ON WATER?`). Each is a 3–4 word positive question (`LEARNINGS.md` Rule #1) that names the concrete physical thing (`WOOD / SKY`, `PLANTS / SOIL`, `WATER`), uses zero vague teasers, and repeats zero words from the video title.
- **BAND:** **PASS** by layout lock. All Flow prompts reserve dark, uncluttered upper-left wall/bookshelf shadow (`x=60..510, y=20..335`) for the cover builder's `Georgia Bold` stack + gold scroll flourishes, completely left of the hero object (`x >= 520`), above the Explorer's hair (`y >= 340`), and clear of the bottom-right duration badge (`x > 1060, y > 580`).
- **PHONE (`168×94`):** **PASS** by typography lock. Short 3–4 word stacks (11–16 characters total) with the gold punch word (`SKY?`, `SOIL?`, `WATER?`) sized to `~90–140 px` glyph height and the Explorer at `~50%` frame height (`~350–375 px`) guarantee 1-second legibility on `thumb_preview.py long`.

---

## 3. Flow Credit Price Table (`J0858`)

### Live Balance Reading (`2026-10-23T01:57Z`)

- **Flow (`benoats@googlemail.com`, CDP `:9222`):** **20,830 credits** (`ai_spend_daily.py --dry-run --pools flow`, `0` credits spent in Step 1).
- **Flow unit rates:**
  - **Flow Image (`Nano Banana 2`, 16:9 landscape still via `_flow_still_v01.py`):** **0 Flow credits / still** on Google AI Ultra (primary route per `AGENTS.md` §Who does what row `image`, verified at `0 cr` in `J0140` and `J0279`).
  - **Flow Fast / Paid Still Reserve (`Veo 3.1 Fast` 16:9 hero plate or paid still tier, if used to pull a hero still):** **10 Flow credits / take**.
  - **Cover builder lettering (`Georgia Bold` + gold flourishes) & gate sheets (`thumb_preview.py`, `style_sheet.py`):** **0 Flow credits / £0.00** (deterministic Python Pillow composer).

### Pricing Options for Step 2 Mint

| Option | Scope | Model / Route | Takes per Concept | Total Takes | Try-1 Flow Credits | Expected Flow Credits (with 2x retake allowance) | Cash Spend (£) | Balance After (from `20,830` cr) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **Option 1 (Recommended default)** | Mint picked **A/B pair** (or all **3 concepts**) in Flow Image mode | **Flow Image · `Nano Banana 2` (16:9)** + cover builder lettering | 1–2 | 2–6 stills | **0 cr** | **0 cr** | **£0.00** | **20,830 cr** |
| **Option 2 (Fast / paid-tier reserve — A/B pair)** | Mint picked **A/B pair** (`Concept A` + `Concept B`) at Fast rate | **Flow · `Veo 3.1 Fast` / 10-cr tier (16:9)** + cover builder lettering | 1 (Try-1) / 2 (Exp) | 2–4 takes | **20 cr** | **40 cr** | **£0.00** | **20,810 cr** *(Try-1)* / **20,790 cr** *(Exp)* |
| **Option 3 (Fast / paid-tier reserve — all 3 concepts)** | Mint all **3 concepts** (`A`, `B`, `C`) at Fast rate | **Flow · `Veo 3.1 Fast` / 10-cr tier (16:9)** + cover builder lettering | 1 (Try-1) / 2 (Exp) | 3–6 takes | **30 cr** | **60 cr** | **£0.00** | **20,800 cr** *(Try-1)* / **20,770 cr** *(Exp)* |

### Studio Pool Headroom Check (against the `3,000` Flow Credit Floor)

| Pool / Film | Try-1 Credits | Expected Credits | Balance After (Try-1) | Balance After (Expected) | Notes |
|---|---:|---:|---:|---:|---|
| **Live Flow balance (23 Oct 01:57Z)** | — | — | **20,830** | **20,830** | Read via `ai_spend_daily.py --dry-run` on CDP `:9222` |
| **HOS 006 Thumbnails (`J0858` Step 2)** | **0–30** | **0–60** | **20,800–20,830** | **20,770–20,830** | `0 cr` on Nano Banana 2; `20–60 cr` if Fast / 10-cr tier used |
| **HOS 008 (`PRICE_REVIEW_v03`)** | 2,360 | 5,605 | 18,440–18,470 | 15,165–15,225 | 15 Quality + 86 Fast (11 £0 code graphics done) |
| **HOS 009 Tranche 1 (`PRICE_REVIEW_v04`)** | 2,910 | 7,354 | **15,530–15,560** | **7,811–7,871** | 26 Quality + 31 Fast (12 £0 code graphics done) |
| **Headroom above `3,000` Flow floor** | — | — | **+12,530 to +12,560 cr** | **+4,811 to +4,871 cr** | **PASSES (`7,811 >= 3,000`, `£0` cash)** |

---

## 4. Decisions Requested from Chief (to Unblock Step 2)

1. **Concept pick:**
   - **Recommended A/B pair:** **Concept A (`WOOD FROM SKY?`)** as Primary A + **Concept B (`DO PLANTS EAT SOIL?`)** as Test & Compare B (or add **Concept C (`GROWN ON WATER?`)** for a 3-variant A/B/C set).
   - Confirm preferred lettering on Concept A (`WOOD FROM SKY?` vs `GROWN FROM AIR?`) and Concept B (`DO PLANTS EAT SOIL?` vs `FED BY SOIL?`).
2. **Flow price pass:**
   - Approve **Option 1 (`0 cr` Nano Banana 2 16:9 stills on Flow)** with **Option 2/3 (`20–60 cr` Flow Fast / paid-still reserve)** authorized as fallback if needed.
3. **Step 2 execution (`J0869`, 23 Oct 2026 — DONE at 0 Flow credits):**
   - Chief pick on `J0858` (OWB `#99` comment `6355648154`): **Concept A (`WOOD / FROM / SKY?`)** primary + **Concept B (`DO PLANTS / EAT / SOIL?`)** Test & Compare second; Concept C dropped; **Option 1 (`0` Flow credits, Nano Banana 2 16:9 stills + £0 cover-builder lettering)**.
   - Minted key-art plates on Flow (`CDP :9222`, `🍌 Nano Banana 2.1 crop_16_9 x1`, 3 style ref chips attached, `20,830 -> 20,830` credits, `0` Flow credits spent, `£0.00` cash):
     - `_assets_v01/hos_006_thumb_A_wood_from_sky_plate01.jpg` (`sha256: 7e7a9877b4234ba00489818f4cdfb8e4ae14edb3f91bc6b3e55769dff66785b8`)
     - `_assets_v01/hos_006_thumb_B_do_plants_eat_soil_plate01.jpg` (`sha256: 9ea89834cdbea312e848be8d9a65e1ac5a21cdc89816816cbfd96a6e9e1ece46`, blank pans/weights with zero written numbers)
   - Composed deterministic house `Georgia Bold` cream + gold punch lettering and gold scroll flourishes via `_compose_hos_006_thumbs_v01.py`, ran `thumb_preview.py long` and `style_sheet.py long`, and staged the A/B pair in `08_Thumbnail/Selected/`, `08_Thumbnail/THUMBS_INDEX_v01.json`, `11_Upload-Package/PACKAGE_MANIFEST.json`, and `HOS UAT/006_Trees-Are-Made-Of-Air/08_Thumbnail/` for Chief review before Ben's 1 Nov watch:
     - **Primary A (`WOOD / FROM / SKY?`):** `Selected/hos_006_thumb_A_wood_from_sky_v01.jpg` (`278,441` bytes, `sha256: 904d2f58be22be993fb36e9c86997d00e239649e9f4b576ccebe4703c83dd0f0`)
     - **Test & Compare B (`DO PLANTS / EAT / SOIL?`):** `Selected/hos_006_thumb_B_do_plants_eat_soil_v01.jpg` (`279,043` bytes, `sha256: ee5f2605520a0155f146d26700d41c99d47b45596457f84d9692415fe15360c4`)
     - **Previews & style sheets:** `Selected/hos_006_thumb_A_wood_from_sky_v01_preview.jpg`, `Selected/hos_006_thumb_B_do_plants_eat_soil_v01_preview.jpg`, `Selected/hos_006_thumb_A_wood_from_sky_v01_style_sheet.jpg`, `Selected/hos_006_thumb_B_do_plants_eat_soil_v01_style_sheet.jpg`, `Selected/hos_006_thumbs_AB_v01_style_sheet.jpg`, and `Selected/hos_006_thumbs_AB_v01_phone_168.jpg`.
