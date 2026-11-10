# 011 Surgery Before Anaesthesia: Claude's quote check before lock (J0224, 14 Oct 2026)

I checked every MUST QUOTE row in `SOURCES_v01.md` against the primary texts themselves, not against Gemini's quotes. The texts were the archive.org full text of Davy 1800, Long 1849 (*Southern Med. & Surg. J.* vol. 5), Rice 1859, Gordon 1897, Simpson 1847 and *The Lancet* Jan–Jun 1847, plus Europe PMC for the Wells letter, the Russell Museum Ether Dome page and Google Patents. The script is `surgery_script_master_v02.md`. `review:script` gives PASS 91.1 (v01 was also 91.1) at 1,259 words.

| Row | Claim (spoken) | Result | Source checked |
|---|---|---|---|
| 1 | Davy 1800: "used with advantage during surgical operations…" | ✓ verbatim (long-s OCR: "ufed with advantage during furgical operations in which no great efFufion of blood takes place") | Davy, *Researches* (1800), archive.org `researcheschemic00davy` |
| 3 | Long, Venable, ether on a towel, March 1842 | ✓ "The ether was given to Mr. Venable on a towel; and when fully under its influence I extirpated the tumour." The OCR reads the day as "20ih March, 1842"; the usual record is 30 March. The VO says only "March", so it's safe. Check the page image before any card shows the day | Long 1849, pp. 706–708, archive.org `southmed1849medi` |
| 4 / 25 | Long published 1849 | ✓ "I know that my interests have suffered from not making an earlier publication" | same |
| 5 / 26 | Wells saw Colton's show, Dec 1844; tooth out the next day | ✓ "On the evening of December 10, 1844, there was an exhibition of the effects of the so-called 'Laughing Gas'… lecture given by a Dr. Colton". (The Riggs deposition item on archive.org gives 404 now, so I couldn't recheck that one.) | Yale J Biol Med (PMC2606479), Europe PMC full text |
| 6 | Boston 1845: "the patient cried out" | ✗ **Not supported.** Wells: "he testified that he experienced some pain, but not as usually attends the operation… several expressed their opinion that it was a humbug affair". **VO v02: "the patient said it hurt"**, and the visual "cries out" becomes "winces". "Humbug" ✓ | PMC2606479 p. 426–427; Rice 1859 |
| 7 | 16 Oct 1846, Abbott, Warren | ✓ "The demonstration took place in the Ether Dome on October 16, 1846. The patient – a young printer named Gilbert Abbott…". The Bigelow link (PMC7897152) is the *Buffalo Medical Journal* reprint of Bigelow's paper, not BMSJ. It's scan-only, so its wording isn't text-checked | russellmuseum.org/ether-dome |
| 8 | "Gentlemen, this is no humbug." (hedged) | ✓ Rice 1859: "Dr. Warren turned to the audience and said slowly and emphatically 'Gentlemen! this is no humbug.'" Keep the hedge | Rice 1859, archive.org `trialsofpublicbe00rice` |
| 10 | Holmes letter, 21 Nov 1846, "anaesthesia" | ✓ "My Dear Sir:— Everybody wants to have a hand in a great discovery… The state should, I think, be called 'Anaesthesia.'" This is in Rice's footnote, pp. 137–138. The Wood Library page refused my fetch | Rice 1859 |
| 11 | Patent 4,848, 12 Nov 1846, Jackson and Morton | ✓ US4848A, "C. T. Jackson and Wm. T. G. Morton, of Boston", priority date 1846-11-12 (the scan's OCR is garbled) | Google Patents US4848A |
| 14 | Liston, ether, London, 21 Dec 1846 | ✓ claim. ✗ **Gemini's quote isn't in the *Lancet*** (no "Frederick Churchill… a butler… quite unconscious of pain"). The real text, now in SOURCES: Liston's note "Clifford-street, Dec. 21, 1846… I tried the ether inhalation to-day in a case of amputation of the thigh… with the most perfect and satisfactory results" | *The Lancet* 1847 vol. 1, archive.org `sim_the-lancet_january-2-june-26-1847_1_1218-1243` |
| 15 | "This Yankee dodge…" (hedged) | PARTIAL stands. There's no 1846–47 print, and *The Lancet* Jan–Jun 1847 has no "Yankee" or "mesmerism hollow". Keep "is said to have" | same |
| 17 | Simpson, chloroform, Nov 1847 | ✓ title page: "Communicated to the Medico-Chirurgical Society of Edinburgh, at their meeting on 10th November 1847" | Simpson 1847, archive.org `b31927336_0001` |
| 18 | Snow, Queen Victoria, Prince Leopold, 1853 | ✓ for 1853 and Leopold (the VO says the year only). The MSU casebook page needs JavaScript and showed no text, so the casebook wording quoted in the row isn't checked. Re-read it before any card quotes it | MSU John Snow Archive; DSB via secondary |
| 23 | Davy's wisdom tooth | ✓ "in cutting one of the unlucky teeth called dentes sapientiae… swallowed up in pleasure" | Davy 1800, p. 465 |
| 28 | Letheon, from Lethe | ✓ claim. ✗ **Gemini's p. 81 quote isn't in Rice.** The real text (pp. 137–138) is now in SOURCES | Rice 1859 |
| 33 | Liston's patient asked when it would begin | **FLAG.** It isn't in *The Lancet* 1847, and both URLs are home pages. It's a later anecdote, so **VO v02 hedges it: "When he woke, he is said to have asked when it would begin. It was already over."** | *The Lancet* 1847 vol. 1 |
| 34 | Simpson, Keith and Duncan, 4 Nov 1847; "slid quietly to the floor" | ✓ the date and the party (Miller, via Gordon 1897, p. 105–107: "Late one evening, it was the 4th of November, 1847"). ✗ **"quietly" is wrong:** "a moment more and then all was quiet — and then crash!… he was prostrate on the floor… Dr. Duncan beneath a chair". **VO v02: "moments later all three were out cold on the floor"**, and the visual now shows them toppling from their chairs | Gordon 1897, archive.org `sirjamesyoungsim00gord` |
| 35 | 1 in 100,000; stadium of 90,000 | ✓ the figure, with its scope: RCoA patient information (2019), as cited in NAP7, gives "1 in 100,000 risk of death as a direct result of anaesthesia in a healthy adult having a general anaesthetic for routine surgery". rcoa.ac.uk refused my fetch, so Gemini's own wording is unchecked. ✗ **The v01 maths was wrong:** 90,000 × 1/100,000 = 0.9 expected deaths, so "every one of them would wake up again" is false more often than not (P(at least one) ≈ 59%). **VO v02: "for a healthy adult… On average, fewer than one of them would die because of the anaesthetic."** | NAP7 report (rcoa.ac.uk/media/38866) |
| 36 | Wembley 90,000 | ✓ 90,000 (Populous, the stadium's architects). Gemini's wembleystadium.com URL gives 404, so its quote is unchecked | populous.com/project/wembley-stadium |

## Not MUST QUOTE, but noted

- Row 13 (FACT card: the Ether Monument names no claimant): the quote is credited to the Smithsonian, but the URL is boston.gov. Get the real Smithsonian SIRIS page before the card is made.
- Row 21: the Science Museum quote links only to the site's home page. The line isn't a number, so the VO stands.

## Lock

Script **v02 is locked for Chief** (J0224). Rows 8 and 15 keep their hedges, and row 33 gains one. No spend. VO can be cast from v02 after Chief's PASS.
