# HOS Buffer backlog pack v01 (5 Oct 2026, HOS Showrunner)

Status: DRAFT for HOS UAT. Nothing here is scheduled. UAT PASS = CoS green (CoS 12:01/12:03). Scheduled through BUFFER_HOS_API_KEY only.

## Scope
- Public HOS Shorts on YouTube (yt-dlp of the channel Shorts tab, 5 Oct 12:10): 13. Three are 003 (already on TikTok/Reels 6–8 Oct), five are 001, five are 002.
- No public test Shorts. 001 s06 carbolic, the Semmelweis and Four Elements backcats and 000 Explorer test are not public, so they are out of scope.
- Platforms: TikTok, IG Reels, Facebook page (as a Reel, type `reel`, vertical video). One Short a day at 11:30 London (10:30Z).

## Schedule
- **003 S1–S3 Facebook:** Tue 6 – Thu 8 Oct, the same days as their TikTok/Reels posts. Video URL reuses the existing `social-media-hos003` prerelease (no new file on GitHub; it comes down Fri as agreed). If UAT passes after Tue 10:00, the 003 Facebook posts move to the end of the run instead.
- **Backlog:** Fri 9 – Sun 18 Oct, oldest film first: 001 s01–s05 (9–13 Oct), then 002 s01–s05 (14–18 Oct), each on TikTok + Reels + Facebook. 30 posts, plus 3 Facebook posts for 003 = 33.

## Blocker before 001/002 can schedule: on-screen "watch the full film →"
Every live 001 and 002 master ends with a small "watch the full film →" caption in the last few seconds (it points at the YouTube Related link). The 002 `punch_pill` masters also carry a "How Did We Discover the Periodic Table?" pill at the top, and the non-pill 002 `punch` masters still have the end caption. Under the CoS rule (no "watch on YouTube" end card), none of these masters can go out as they are. Frame evidence: `bl_sheet_s.png` and `cta_end_frames.png` beside this file.

Decision: ask HOS Picture / HOS Local for one clean social master per Short, `hos_00X_sNN_<name>_social_v01.mp4`, from the same edit with the end caption and the pill removed (re-render without the overlay, or end the cut on the last frame before the caption appears without clipping the final VO line). No other changes. UAT then fresh-checks each social master against the house rules and records its sha256 here. If a Short cannot get a clean social master by Thu 8 Oct, it is skipped and listed, and the rest move up a day.

## Masters and UAT records
| Film | Slot | YouTube | Live master (sha256) | Earlier UAT pass | Social master |
|---|---|---|---|---|---|
| 003 | S1 | `oowAOWTBoq0` | `hos_003_s1_cardboard_glow_v01.mp4` (`a06967893af11465bdd6571011e92ad140e559c2fb14cd4a27f6c9e30d72aded`) | HOS 003 Buffer pack v01 PASS, 5 Oct | same file, clean |
| 003 | S2 | `xvanpsLeADE` | `hos_003_s2_bones_no_knife_v01.mp4` (`3bb67af65c87c969fe35c5017ff1b3063d486277925fbb27b4fbf1a550707492`) | HOS 003 Buffer pack v01 PASS, 5 Oct | same file, clean |
| 003 | S3 | `zI_eD3vFWmE` | `hos_003_s3_bertha_ring_v01.mp4` (`911f546882c2164ca663bf1a01348c63b14b804b2357969dbc7fe288475a54c7`) | HOS 003 Buffer pack v01 PASS, 5 Oct | same file, clean |
| 001 | s01 | `H1y0DXFVmw8` | `hos_001_s01_shadow_punch_v02.mp4` (`055315a54a28f19e78c32a76b90567127ad22ccb30a686f9fe3b8e0df5437aaf`) | none on record, fresh check needed | TO MAKE (blocker above) |
| 001 | s02 | `iqToagXnjX0` | `hos_001_s02_pond_punch_v02.mp4` (`94256ce1418fb3453f01167322589249caf81d86af011fdd84323b2ac3072a90`) | none on record, fresh check needed | TO MAKE (blocker above) |
| 001 | s03 | `8_Edn_HCi1s` | `hos_001_s03_vector_punch_v02.mp4` (`ef304cd1eb19fba4393ab7ba7b93d01081ab8664e759642725d41f0b44b26ec2`) | none on record, fresh check needed | TO MAKE (blocker above) |
| 001 | s04 | `sILtQxgYQk8` | `hos_001_s04_flask_punch_v02.mp4` (`acf9f7e685eddbbc99e4452aa0ac8f2a0fb0e22fe0b91643e34fa914e7ad040b`) | none on record, fresh check needed | TO MAKE (blocker above) |
| 001 | s05 | `93fPUG-hW0A` | `hos_001_s05_soap_punch_v03.mp4` (`de928d5438038370f108176ddb66bc604323c407ae9f6c61f471f8a285805397`) | none on record, fresh check needed | TO MAKE (blocker above) |
| 002 | s01 | `uU12JA5rMWg` | `hos_002_s01_empty_chairs_punch_pill_v01.mp4` (`935d41c4e06f195e017d8d60a266df8001c0815a4d7a062519f5f1b4db39f880`) | none on record, fresh check needed | TO MAKE (blocker above) |
| 002 | s02 | `nFQRWmpulTQ` | `hos_002_s02_predict_metal_punch_pill_v01.mp4` (`daa91ad24072f1cb0dbde73002c5a28242cc77fdbf8b0b76466f594dc734311e`) | none on record, fresh check needed | TO MAKE (blocker above) |
| 002 | s03 | `CnHwX1L9XHg` | `hos_002_s03_gallium_punch_pill_v01.mp4` (`a87cabc53839ba7c9f95ba5defe15988e6836caf6d1f0c0e7fc09dc02c6cca72`) | none on record, fresh check needed | TO MAKE (blocker above) |
| 002 | s04 | `nba0-f7PPeU` | `hos_002_s04_tellurium_punch_pill_v01.mp4` (`865a2a25b1c20ced38cf8ae508ab6940598ee2de8def69760ef700e1f9230f2a`) | none on record, fresh check needed | TO MAKE (blocker above) |
| 002 | s05 | `LanTHJckYx8` | `hos_002_s05_other_table_punch_pill_v01.mp4` (`b24c1b358d222ec7f38130105537bcf36483ab0bbecb0fabc72ab079ba2ae3d9`) | none on record, fresh check needed | TO MAKE (blocker above) |

## Hosting (not GitHub, torn down daily)
Buffer pulls the video at publish time, so the link must live until 11:30 that day. Plan: each morning at about 09:45 London I upload only that day's master to uguu.se (it deletes itself about 3 hours later, so each link is gone by early afternoon), download it back on my own computer to confirm the sha256 matches the table, then create that day's three posts. Buffer accepted a uguu link earlier today and made its thumbnail. Buffer post ids get posted in HOS Desk each day. If an upload or sha check fails, that day is held and reported, never sent with a different file.

## Full-film pointer (Ben via CoS, 5 Oct 12:51)
- Facebook: `Full film: https://youtu.be/<long id>` (clickable).
- Instagram: `Full film on YouTube, link in bio.` (once the bio link is confirmed).
- TikTok: `Full film on YouTube: search History of Science` (no bio link until the account qualifies; 3 queued 003 TikToks already edited).
- Long ids: 001 `_C92tIJCk8A`, 002 `AL_-qlWko_g`, 003 `frP_YrNShsU`.
- Queued 003 posts (9) were edited in place to this rule; backlog posts use it from the start.

## Captions (each opens with the locked live YouTube title; no /go/, no Orbit)
### 2026-10-06 · 003 S1 · FB
```
How X-rays Were Discovered by Accident

In 1895 Wilhelm Röntgen covered his tube in black card, yet a screen nearby lit up. That glow was the first sign of X-rays.

Full film: https://youtu.be/frP_YrNShsU
```

### 2026-10-07 · 003 S2 · FB
```
How did Röntgen see bones without cutting

X-rays pass through skin and muscle but are stopped by bone, so for the first time a doctor could see a living skeleton without a single cut.

Full film: https://youtu.be/frP_YrNShsU
```

### 2026-10-08 · 003 S3 · FB
```
The first X-ray showed a wedding ring

The first famous X-ray photo was Bertha Röntgen's hand: the bones of her fingers and the dark band of her wedding ring.

Full film: https://youtu.be/frP_YrNShsU
```

### 2026-10-09 · 001 s01 · TT
```
Germs don't cast a shadow
For centuries doctors blamed disease on bad air. The real enemy was alive, everywhere, and far too small to see.
Full film on YouTube: search History of Science
#germs #germtheory #historyofscience #science #sciencetok
```

### 2026-10-09 · 001 s01 · IG
```
Germs don't cast a shadow
For centuries doctors blamed disease on bad air. The real enemy was alive, everywhere, and far too small to see.
Full film on YouTube, link in bio.
#germs #germtheory #historyofscience #sciencehistory #science
```

### 2026-10-09 · 001 s01 · FB
```
Germs don't cast a shadow

For centuries doctors blamed disease on bad air. The real enemy was alive, everywhere, and far too small to see.

Full film: https://youtu.be/_C92tIJCk8A
```

### 2026-10-10 · 001 s02 · TT
```
Microbes in a drop of pond water
A drop of pond water looks empty. Under an early microscope it was crowded with tiny living things.
Full film on YouTube: search History of Science
#microbes #microscope #historyofscience #science #sciencetok
```

### 2026-10-10 · 001 s02 · IG
```
Microbes in a drop of pond water
A drop of pond water looks empty. Under an early microscope it was crowded with tiny living things.
Full film on YouTube, link in bio.
#microbes #microscope #historyofscience #sciencehistory #science
```

### 2026-10-10 · 001 s02 · FB
```
Microbes in a drop of pond water

A drop of pond water looks empty. Under an early microscope it was crowded with tiny living things.

Full film: https://youtu.be/_C92tIJCk8A
```

### 2026-10-11 · 001 s03 · TT
```
Germs hitch a ride on you
Germs do not fly across a ward on their own. They travel on hands, cloth and breath, and doctors were carrying them.
Full film on YouTube: search History of Science
#germs #medicalhistory #historyofscience #science #sciencetok
```

### 2026-10-11 · 001 s03 · IG
```
Germs hitch a ride on you
Germs do not fly across a ward on their own. They travel on hands, cloth and breath, and doctors were carrying them.
Full film on YouTube, link in bio.
#germs #medicalhistory #historyofscience #sciencehistory #science
```

### 2026-10-11 · 001 s03 · FB
```
Germs hitch a ride on you

Germs do not fly across a ward on their own. They travel on hands, cloth and breath, and doctors were carrying them.

Full film: https://youtu.be/_C92tIJCk8A
```

### 2026-10-12 · 001 s04 · TT
```
A flask that proved germs come from outside
Louis Pasteur boiled broth in a flask with a long swan neck. Dust and germs got stuck in the bend, and the broth stayed clear.
Full film on YouTube: search History of Science
#pasteur #germtheory #historyofscience #science #sciencetok
```

### 2026-10-12 · 001 s04 · IG
```
A flask that proved germs come from outside
Louis Pasteur boiled broth in a flask with a long swan neck. Dust and germs got stuck in the bend, and the broth stayed clear.
Full film on YouTube, link in bio.
#pasteur #germtheory #historyofscience #sciencehistory #science
```

### 2026-10-12 · 001 s04 · FB
```
A flask that proved germs come from outside

Louis Pasteur boiled broth in a flask with a long swan neck. Dust and germs got stuck in the bend, and the broth stayed clear.

Full film: https://youtu.be/_C92tIJCk8A
```

### 2026-10-13 · 001 s05 · TT
```
Invisible life is still everywhere
Every time you wash your hands with soap, you are using the discovery of germs. What else around us is still invisible?
Full film on YouTube: search History of Science
#germs #handwashing #historyofscience #science #sciencetok
```

### 2026-10-13 · 001 s05 · IG
```
Invisible life is still everywhere
Every time you wash your hands with soap, you are using the discovery of germs. What else around us is still invisible?
Full film on YouTube, link in bio.
#germs #handwashing #historyofscience #sciencehistory #science
```

### 2026-10-13 · 001 s05 · FB
```
Invisible life is still everywhere

Every time you wash your hands with soap, you are using the discovery of germs. What else around us is still invisible?

Full film: https://youtu.be/_C92tIJCk8A
```

### 2026-10-14 · 002 s01 · TT
```
The periodic table's empty chairs
In 1869 Dmitri Mendeleev left gaps in his table on purpose, saving seats for elements nobody had found yet.
Full film on YouTube: search History of Science
#periodictable #mendeleev #historyofscience #science #sciencetok
```

### 2026-10-14 · 002 s01 · IG
```
The periodic table's empty chairs
In 1869 Dmitri Mendeleev left gaps in his table on purpose, saving seats for elements nobody had found yet.
Full film on YouTube, link in bio.
#periodictable #mendeleev #historyofscience #sciencehistory #science
```

### 2026-10-14 · 002 s01 · FB
```
The periodic table's empty chairs

In 1869 Dmitri Mendeleev left gaps in his table on purpose, saving seats for elements nobody had found yet.

Full film: https://youtu.be/AL_-qlWko_g
```

### 2026-10-15 · 002 s02 · TT
```
He predicted a metal before it was found
Mendeleev described a missing metal, which he called eka-aluminium, years before anyone had held it.
Full film on YouTube: search History of Science
#periodictable #chemistry #historyofscience #science #sciencetok
```

### 2026-10-15 · 002 s02 · IG
```
He predicted a metal before it was found
Mendeleev described a missing metal, which he called eka-aluminium, years before anyone had held it.
Full film on YouTube, link in bio.
#periodictable #chemistry #historyofscience #sciencehistory #science
```

### 2026-10-15 · 002 s02 · FB
```
He predicted a metal before it was found

Mendeleev described a missing metal, which he called eka-aluminium, years before anyone had held it.

Full film: https://youtu.be/AL_-qlWko_g
```

### 2026-10-16 · 002 s03 · TT
```
Gallium sat where the table said
In 1875 a new metal, gallium, was discovered. It fitted the empty seat Mendeleev had left for it.
Full film on YouTube: search History of Science
#periodictable #gallium #historyofscience #science #sciencetok
```

### 2026-10-16 · 002 s03 · IG
```
Gallium sat where the table said
In 1875 a new metal, gallium, was discovered. It fitted the empty seat Mendeleev had left for it.
Full film on YouTube, link in bio.
#periodictable #gallium #historyofscience #sciencehistory #science
```

### 2026-10-16 · 002 s03 · FB
```
Gallium sat where the table said

In 1875 a new metal, gallium, was discovered. It fitted the empty seat Mendeleev had left for it.

Full film: https://youtu.be/AL_-qlWko_g
```

### 2026-10-17 · 002 s04 · TT
```
Why tellurium sat before iodine
By weight, tellurium should come after iodine. Mendeleev put it first anyway, because of how the two elements behave.
Full film on YouTube: search History of Science
#periodictable #chemistry #historyofscience #science #sciencetok
```

### 2026-10-17 · 002 s04 · IG
```
Why tellurium sat before iodine
By weight, tellurium should come after iodine. Mendeleev put it first anyway, because of how the two elements behave.
Full film on YouTube, link in bio.
#periodictable #chemistry #historyofscience #sciencehistory #science
```

### 2026-10-17 · 002 s04 · FB
```
Why tellurium sat before iodine

By weight, tellurium should come after iodine. Mendeleev put it first anyway, because of how the two elements behave.

Full film: https://youtu.be/AL_-qlWko_g
```

### 2026-10-18 · 002 s05 · TT
```
What other table has empty chairs?
Mendeleev's table kept seats for elements no one had seen. Good science still leaves room for what we have not found.
Full film on YouTube: search History of Science
#periodictable #mendeleev #historyofscience #science #sciencetok
```

### 2026-10-18 · 002 s05 · IG
```
What other table has empty chairs?
Mendeleev's table kept seats for elements no one had seen. Good science still leaves room for what we have not found.
Full film on YouTube, link in bio.
#periodictable #mendeleev #historyofscience #sciencehistory #science
```

### 2026-10-18 · 002 s05 · FB
```
What other table has empty chairs?

Mendeleev's table kept seats for elements no one had seen. Good science still leaves room for what we have not found.

Full film: https://youtu.be/AL_-qlWko_g
```
