# Topic Opportunity Score — `HOS:110` (`110_Virtanen-Block-Imai-Why-Do-Onions-Make-You-Cry`)

> **RULE-E GO & VERIFICATION STATUS (`J2922` / `J2924`, `2026-11-16`):**
> - **Verdict:** **GO (`9.50 / 10` · `95 / 100` Opportunity Score)** — Pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (`active` has `4 / 4` HOS slots full: `008`, `009`, `010`, `013`).
> - **Guardrail:** All historical and scientific claims in `TOPIC.md` and `PRE_BUILD_VIDIQ_AUDIT.md` remain **UNVERIFIED** working notes until an active HOS WIP slot opens, verbatim primary-source quotes are recorded in `SOURCES.md`, and the `facts` lane (`gemini-agy`) verifies every claim.

---

## 1. Weighted Opportunity Rubric (`STUDIO_PLAYBOOK.md` §2)

| Dimension | Weight | Score (1–10) | Weighted | Evidence (`2026-11-16`) |
|---|---:|---:|---:|---|
| **1. Evergreen search intent** | 25% | **9.6** | **2.400** | `"why do onions make you cry"` (`autocomplete = yes`, `5` suggestions), `"why do we cry"` (`autocomplete = yes`, `10` suggestions incl. `"why do we cry when we cut onions"`), and `"how enzymes work"` (`autocomplete = yes`, `10` suggestions). **`15` strictly on-topic videos `≥ 1,000,000` views** (`9` in `neighbours.py` + `6` in `public_search.py`), led by `TED-Ed` `14.04M` (`Og5xAdC8EUI`), `Amoeba Sisters` `7.27M` (`qgVFkRn8f10`), `TED-Ed` `6.91M` (`keMF8YzQoRM` *Why do we cry? The three types of tears*), `AsapSCIENCE` `5.54M` (`QGdHJSIr1Z0`), `TED-Ed` `4.45M` (`Hja0SLs2kus` *The amazing ways plants defend themselves*), `TED-Ed` `4.17M` (`n6wpNhyreDE`), `Colossal Cranium` `3.49M` (`1OoWsiY6Lf8`), `AumSum's What-If` `2.92M` (`dVw3DrqihIg`), `TED-Ed` `2.47M` (`OttRV5ykP7A`), and `It's AumSum Time` `2.45M` (`9ZinH1jEhb4`). |
| **2. Competition gap** | 20% | **9.5** | **1.900** | Top direct search results on `"why do onions make you cry"` are `1–3 min` kids/cartoon summaries (`Colossal Cranium` `2:05`, `It's AumSum Time` `1:12`, `SciShow Kids` `3:33`, `Reactions` `2:19`) or studio talking-head explainers (`SciShow` `5:34` `107.9k` views). **Zero** videos on YouTube tell the 4-room historical discovery drama in painted 3D: Stoll & Seebeck's 1948 Basel garlic enzyme → Virtanen's 1961–1963 Helsinki onion `isoalliin` compartment puzzle → Brodnitz/Pascale (1971) & Eric Block's (1979–1992) cryogenic trap for `(Z)`-propanethial *S*-oxide → Shinsuke Imai's 2002 *Nature* vial experiment that uncovered the hidden second enzyme (`LFS`). |
| **3. Narrative & visual arc** | 20% | **9.5** | **1.900** | Immediate proof-first visual hook (`0:00–0:15`: intact onion with zero gas vs. steel knife rupturing cytoplasmic fuel and vacuolar enzyme vaults), followed by cryogenic glass traps, the garlic-vs-onion isomer paradox (`alliin` vs `isoalliin`), Imai's two test vials in Chiba (one clear, one steaming with golden tear-gas vapor when `LFS` is added), and tearless `LFS`-silenced onions. |
| **4. Brand & guardrail fit** | 20% | **10.0** | **2.000** | Classic History of Science everyday-mystery discovery story with a 40-year textbook assumption overturned by a clean 2002 two-vial experiment (`Nature` 419: 685). Zero fearbait, zero medical-advice risk, zero overlap with `000–109`, `111`, or `ideas/`. |
| **5. Series / cluster potential** | 15% | **8.7** | **1.305** | Anchors the **Everyday Plant Defense & Kitchen Biochemistry Cluster** alongside `051` (Scoville, Julius & Patapoutian — why chili peppers burn via `TRPV1`), `070` (Fischer, Buchner & Sumner — how enzymes were discovered), `105` (Darwin & Burdon-Sanderson — how the Venus flytrap counts to two), and `107` (Caventou, Pelletier & Willstätter — why autumn leaves change colour). |
| **Total** | **100%** | — | **`9.505 / 10` (`95 / 100`)** | **GO (`≥ 7.5` threshold exceeded by `+2.00` points)** |

**Rule:** Proceed (`GO`) if **Total ≥ 7.5** and **Brand fit ≥ 8**. Both pass (`9.50 / 10` total, `10.0 / 10` brand fit).

---

## 2. Education Neighbour Gate (`neighbours.py` + `public_search.py`, Retrieved `2026-11-16`)

Saved in [`evidence_2026-11-16_neighbours.json`](evidence_2026-11-16_neighbours.json) (`bigCount = 12`, `onTopicBigCount = 9`, `hasTed = true`, `gate = PASS`) and [`evidence_2026-11-16_public_search.json`](evidence_2026-11-16_public_search.json):

| # | Channel | Views (`2026-11-16`) | Video ID & URL | Title | Source File |
|---:|---|---:|---|---|---|
| 1 | **TED-Ed ★** | `14,043,201` | [`Og5xAdC8EUI`](https://youtu.be/Og5xAdC8EUI) | *How your digestive system works - Emma Bryce* | `neighbours.json` (Tier 1) |
| 2 | **Amoeba Sisters** | `7,269,331` | [`qgVFkRn8f10`](https://youtu.be/qgVFkRn8f10) | *Enzymes (Updated)* | `neighbours.json` (Tier 2) + `public_search.json` |
| 3 | **TED-Ed ★** | `6,914,192` | [`keMF8YzQoRM`](https://youtu.be/keMF8YzQoRM) | *Why do we cry? The three types of tears - Alex Gendler* | `neighbours.json` (Tier 1) + `public_search.json` |
| 4 | **AsapSCIENCE** | `5,544,058` | [`QGdHJSIr1Z0`](https://youtu.be/QGdHJSIr1Z0) | *Why Do We Cry?* | `public_search.json` |
| 5 | **TED-Ed ★** | `4,447,334` | [`Hja0SLs2kus`](https://youtu.be/Hja0SLs2kus) | *The amazing ways plants defend themselves - Valentin Hammoudi* | `neighbours.json` (Tier 1) |
| 6 | **TED-Ed ★** | `4,171,001` | [`n6wpNhyreDE`](https://youtu.be/n6wpNhyreDE) | *How to make the perfect cookies (according to science) - Stephanie Warren* | `neighbours.json` (Tier 1) |
| 7 | **Colossal Cranium** | `3,486,968` | [`1OoWsiY6Lf8`](https://youtu.be/1OoWsiY6Lf8) | *Why Do Onions Make Us Cry? \| COLOSSAL QUESTIONS \| Learn #withme* | `public_search.json` |
| 8 | **AumSum's What-If** | `2,917,778` | [`dVw3DrqihIg`](https://youtu.be/dVw3DrqihIg) | *Why do Onions make us Cry?* | `public_search.json` |
| 9 | **TED-Ed ★** | `2,468,735` | [`OttRV5ykP7A`](https://youtu.be/OttRV5ykP7A) | *How to speed up chemical reactions (and get a date) - Aaron Sams* | `neighbours.json` (Tier 1) |
| 10 | **It's AumSum Time** | `2,452,719` | [`9ZinH1jEhb4`](https://youtu.be/9ZinH1jEhb4) | *Human Tears - Why do onions make you cry?* | `public_search.json` |
| 11 | **TED-Ed ★** | `2,362,239` | [`ee7muQ_qKU0`](https://youtu.be/ee7muQ_qKU0) | *The wild world of carnivorous plants - Kenny Coogan* | `neighbours.json` (Tier 1) |
| 12 | **RCSBProteinDataBank** | `1,634,395` | [`yk14dOOvwMk`](https://youtu.be/yk14dOOvwMk) | *How Enzymes Work (from PDB-101)* | `public_search.json` |
| 13 | **Amoeba Sisters** | `1,379,665` | [`6EDBlowVST0`](https://youtu.be/6EDBlowVST0) | *Enzyme Examples, Cofactors/Coenzymes, Inhibitors, and Feedback Inhibition* | `public_search.json` |
| 14 | **FuseSchool** | `1,151,481` | [`rlH1ym916Fo`](https://youtu.be/rlH1ym916Fo) | *Enzymes \| Cells \| Biology \| FuseSchool* | `neighbours.json` (Tier 2) |
| 15 | **TED-Ed ★** | `1,073,460` | [`8m6RtOpqvtU`](https://youtu.be/8m6RtOpqvtU) | *What triggers a chemical reaction? - Kareem Jarrah* | `neighbours.json` (Tier 1) |

---

## 3. Cluster Sketch (3 Adjacent Episodes)

1. **`HOS:110` (This Episode):** *Why Do Onions Make You Cry? (The 2002 Enzyme Twist)* — Virtanen's two-compartment `isoalliin`/`alliinase` binary bomb, Brodnitz/Pascale & Block's `(Z)`-propanethial *S*-oxide structure, and Shinsuke Imai's 2002 *Nature* discovery of lachrymatory-factor synthase (`LFS`).
2. **`HOS:051` (`051_Scoville-Julius-Patapoutian-Capsaicin-Pain-Receptors`, in `ideas/`):** *Why Do Chili Peppers Burn Your Mouth?* — Wilbur Scoville's 1912 organoleptic dilution test and David Julius's 1997 cloning of the `TRPV1` heat-and-capsaicin ion channel.
3. **`HOS:070` (`070_Buchner-Sumner-Northrop-Enzymes`, in `ideas/`):** *How Do Enzymes Work?* — Eduard Buchner's 1897 cell-free yeast fermentation press and James Batcheller Sumner's 1926 crystallization of jack-bean urease proving enzymes are proteins.
4. **`HOS:105` (`105_Ellis-Darwin-Burdon-Sanderson-Venus-Flytrap`, on PR `#581`):** *How Does a Venus Flytrap Know When to Snap Shut?* — Charles Darwin's 1875 trigger-hair tests, John Burdon-Sanderson's 1873 plant action potentials, and the two-touch calcium clock.
