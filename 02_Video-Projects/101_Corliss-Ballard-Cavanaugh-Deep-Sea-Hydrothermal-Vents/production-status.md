# Production status — 101 How Do Deep Sea Vents Feed Life Without Sunlight?

| Field | Value |
|---|---|
| Slug | `101_Corliss-Ballard-Cavanaugh-Deep-Sea-Hydrothermal-Vents` |
| Channel | `@HistoryOfScienceYT` only |
| Topic | **Rule-E Topic Review `GO` (`J2473`, 10 Nov 2026 · `95/100`)**: pre-cleared in `jobs/WIP.json` `next_hos` under Rule G (waits for an active HOS slot to free up). Packages: [`TOPIC_GO_NO_GO_SHEET.md`](11_Upload-Package/TOPIC_GO_NO_GO_SHEET.md) · [`TOPIC_OPPORTUNITY_SCORE.md`](11_Upload-Package/TOPIC_OPPORTUNITY_SCORE.md) · [`PRE_BUILD_VIDIQ_AUDIT.md`](11_Upload-Package/PRE_BUILD_VIDIQ_AUDIT.md) |
| Working Title (A1 — Collision-Free Primary) | *How Do Deep Sea Vents Feed Life Without Sunlight?* (`49 chars`, `0` exact collisions; replaces `J2411` working string *How Does Life Survive at the Bottom of the Ocean?* which has `1` exact match `U5pd5BfX-5s`) |
| Title B (T&C) | *Deep Sea Vents: The World That Lives Without Sun* (`48 chars`, `0` exact collisions) |
| Title D (Rule 26) | *Deep Sea Hydrothermal Vents (The 1977 Dive That Found Sunless Life)* (`67 chars`, `0` exact collisions; exact autocomplete phrase `"deep sea hydrothermal vents"` first) |
| Neighbour gate | **PASS** — `3` education videos `≥1M` views (`TED-Ed/TED: yes`, led by Kurzgesagt `25.80M` `PaErPyEnDvk` *What's Hiding at the Most Solitary Place on Earth? The Deep Sea*, TED `1.55M` `PbgB2TaYhio` Karen Lloyd, and TED-Ed `1.16M` `Uqly8ERIkHM` David Gallo *Deep ocean mysteries and wonders*) |
| Public search | Saved (`11_Upload-Package/evidence_2026-11-08_public_search.json`; `"hydrothermal vents"`, `"deep sea hydrothermal vents"`, `"deep sea vents"`, `"deep sea ecosystems"`, `"chemosynthesis"`, and `"life at the bottom of the ocean"` all autocomplete `yes`; ranking videos `PaErPyEnDvk` `25.80M` & `1LrcTa0dDmw` `6.81M`) |
| Script review | — / 90 (waits on Rule G active HOS WIP slot) |
| Episode gate | not run |
| VO | pending (Ben Orbit Narrator) |
| Picture | pending (Flow Veo 3.1, plate library) |
| Runtime target | 7–9 min, 5 parts |
| Air | Backlog (`next_hos`) — Thursday 18:00 UK, normal publish (no Premiere) |
| Shorts | 2 search-titled Shorts pre-designed (`S01`: *How Do Giant Worms Live Without Sunlight?*, `S02`: *Why Doesn't 400°C Deep-Sea Water Boil?* / *How Can Deep-Sea Vent Water Reach 400°C?*; expands to 4 Shorts on active build per `STUDIO_PLAYBOOK.md` §1) |

## Topic Gate Evidence (`neighbours.py` & `public_search.py` PASS)

```text
| # | Channel | Views | Title | Found by |
|---|---|---|---|---|
| 1 | TED ★ | 1,547,916 views | [This deep-sea mystery is changing our understanding of life | Karen Lloyd](https://youtu.be/PbgB2TaYhio) | deep sea ted |
| 2 | TED-Ed ★ | 1,156,252 views | [Deep ocean mysteries and wonders - David Gallo](https://youtu.be/Uqly8ERIkHM) | ted-ed deep sea |
| 3 | TED ★ | 541,608 views | [Deep sea diving ... in a wheelchair | Sue Austin](https://youtu.be/PCWIGN3181U) | deep sea ted |
| 4 | TED-Ed ★ | 356,401 views | [How Life Begins in the Deep Ocean](https://youtu.be/i_R7ouD8-Eo) | ted-ed deep sea |
| 5 | Kurzgesagt – In a Nutshell | 25,803,975 views | [What’s Hiding at the Most Solitary Place on Earth? The Deep Sea](https://youtu.be/PaErPyEnDvk) | ted-ed deep sea |
| 6 | TED ★ | 79,152 views | [Meet the Mysterious “Monsters” of the Deep Sea | Alan Jamieson | TED](https://youtu.be/Cz9w0sx-_rs) | deep sea ted |
| 7 | Natural History Museum | 66,623 views | [Life at hydrothermal vents | Natural History Museum](https://youtu.be/fOGEuhQPKvY) | hydrothermal vents |
| 8 | TED ★ | 45,217 views | [The Deep Sea's Medicinal Secrets | Sam Afoullouss | TED](https://youtu.be/zFJH9zUK2mo) | deep sea ted |
| 9 | National Geographic | 38,797 views | [Hydrothermal Ocean Vents Found in Surprisingly Shallow Water | National Geographic](https://youtu.be/c3-4JvGSsaA) | hydrothermal vents |
| 10 | Natural History Museum | 3,801 views | [Life from vents | Natural History Museum](https://youtu.be/SfyAgl9uhos) | hydrothermal vents ted |
| 11 | TEDx Talks ★ | 924 views | [From Deep Sea Vents to the Classroom | Dr. Jon Briggs | TEDxPCC](https://youtu.be/ovlIqBxS33k) | ted-ed hydrothermal vents |

Words the top neighbours share: deep sea, the deep, deep ocean, vents natural, natural history, history museum
TED-Ed/TED neighbour: yes
Big neighbours (≥ 1,000,000 views): 3 (need 3)
Neighbour gate (≥ 3 education videos with 1,000,000+ views): PASS
Raw pull: 02_Video-Projects/101_Corliss-Ballard-Cavanaugh-Deep-Sea-Hydrothermal-Vents/11_Upload-Package/evidence_2026-11-08_neighbours.json
```

```text
| Phrase | Autocomplete? | Top results (GB) |
|---|---|---|
| hydrothermal vents | yes | Natural World Facts 801,077 · Woods Hole Oceanographic Institution 174,200 · Natural History Museum 66,623 · Natural World Facts 6,810,086 · MBARI (Monterey Bay Aquarium Research Institute) 209,037 |
| deep sea ecosystems | yes | Kurzgesagt – In a Nutshell 25,803,975 · Natural World Facts 6,810,086 · Natural World Facts 11,757,942 · BBC Earth 4,236,097 · Auralis and Natural World Facts 522,856 |
| chemosynthesis | yes | Natural World Facts 801,077 · Science With Johnston 12,199 · Revision Monkey 47,459 · EVNautilus 226,114 · Microbiology Videos 319 |
| How Does Life Survive at the Bottom of the Ocean? | no | LivingZoo 146,057 · Kurzgesagt – In a Nutshell 25,803,975 · Natural World Facts 1,717,102 · Mr. Science 17,251,904 · The Infographics Show 1,241,493 |
| Deep Sea Vents: The World That Lives Without Sun | no | Natural World Facts 6,810,086 · Natural World Facts 801,054 · Woods Hole Oceanographic Institution 14,040 · Ocean Discover 1,064 · DENEVIO 79 |

Raw pull: 02_Video-Projects/101_Corliss-Ballard-Cavanaugh-Deep-Sea-Hydrothermal-Vents/11_Upload-Package/evidence_2026-11-08_public_search.json
```

## Parts

| Part | Plate board | Latest cut | Status |
|---|---|---|---|
| 01 | `07_Edit-Project/parts/part-01_plates_v01.json` | — | — |
| 02 | | | |
| 03 | | | |
| 04 | | | |
| 05 | | | |

Keep this file current on `main`. A STOP (quota, auth, missing VO) is a line here, not an open branch.
