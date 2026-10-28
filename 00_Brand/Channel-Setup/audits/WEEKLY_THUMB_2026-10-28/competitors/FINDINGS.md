# Reference-channel comparison — J1107, 28 October 2026

Worker evidence, not a Chief approval. This completes manual observations for the **122 selected served thumbnails from the five reference channels**: 68 long thumbnails and 54 Short thumbnails. The six additional search-neighbour channels remain to be coded before the full competitor study is complete. No winning pattern or new HOS design is approved.

## Scope and reproducibility

`cohorts.json` retains all eligible rows, ranks, URLs, exact dates, views/day and fast/slow membership from the completed public yt-dlp collection at 18:31 UTC. Window starts 30 July 2026 at 18:31 UTC. Views/day = cumulative views divided by age in days, with a one-day denominator floor. Videos under a day old cannot be interpreted as mature performers. This is a cross-sectional screen, not first-day performance or CTR. Current thumbnails may differ from the thumbnails which earned historical views.

`thumbnail_manifest.json` verifies all 122 local image hashes. Media and review sheets remain in `/Users/benjaminoats/_desk/J1107/competitors/`, outside git. `long_visual_coding.json` and `short_visual_coding.json` record text, size/colour, subject/composition, curiosity mechanism, title shape/length/hook, luma and contrast. Those visual observations were made directly from the saved sheets; the accompanying scripts preserve their row mapping and calculations. Small Short subtitles sometimes remain explicitly unreadable. Logos are not treated as hook text. Numeric luma is a descriptive measurement, never an HOS grade rule.

| Channel | Longs in window | Shorts in window | Fast/slow overlap (long / Short) |
|---|---:|---:|---:|
| Veritasium (broad preliminary sample) | 6 | 14 | 6 / 6 |
| SciShow | 55 | 0 | 0 / 0 |
| Big Think | 17 | 42 | 3 / 0 |
| Real Engineering | 5 | 0 | 5 / 0 |
| Kings and Generals | 37 | 40 | 0 / 0 |

The latest fetched SciShow Short dates to 21 January 2026 and Real Engineering Short to 2 July: neither supplies a 90-day Short cohort. These are zero eligible records, not failed collection. The 125 excluded details are nonpublic records (124 subscriber-only and one requiring authentication), so they are deliberately outside the public study. `coverage.json` shows exact-date coverage before the cutoff for all ten tabs, including capped listings. This assumes the channel tabs are reverse chronological; it does not claim a platform-wide catalogue guarantee.

**Veritasium history filter:** the job asks for history pieces, not its full output. Two longs meet that focus from public descriptions/chapters: Fibre Optics and Enigma. The atomic-clock film is current experimental physics; spider silk is principally current tests; the other two are an announcement and an eclipse expedition. `veritasium_history_filter.json` records this conservative judgement. Both history films occur in both tails because n=2. They are design references, not a fast-versus-slow experiment. The 14 broad Shorts are coded for reuse, but history eligibility remains unresolved and no Veritasium Short pattern is asserted.

## Supported observations

- **SciShow does not establish that questions win.** Six of ten fast longs and six of ten slow longs have question-shaped titles under the recorded grammar. Median title lengths are 41.5 and 33.5 characters respectively: its faster group is not the shorter one. The fast group often visualises a concrete oddity or test (hot sphere, implant, gold, mothballs); the slow group also contains concrete objects. The useful design hypothesis is a readily understood physical puzzle, not a universal question or word-count rule.
- **Big Think's fixed interview layout appears in both tails.** Seated experts on white cutouts and large phrase text recur in fast and slow longs. Three videos overlap the tails. Fast/slow median title length is 79.5/82.5 characters and question count is 1/1. The data does not isolate layout or short titles as a cause.
- **Kings and Generals uses maps, named events and large lettering throughout.** Long fast/slow question counts are 4/2 and median title lengths 54/64.5, but topics, recency and established historical interest differ. Maps and big lettering also occur among the slow ten. Its Short red top-band house treatment occurs on both sides; that repeatable identity alone does not predict speed.
- **Real Engineering and the history-only Veritasium subset cannot support independent tails.** All five Real Engineering longs and both qualifying Veritasium history longs would be in both groups. Enigma's machine and fibre's physical demonstration offer readable mechanisms to study; they provide no controlled evidence for copying white type, black backgrounds or vague “How?” lettering into HOS.
- **Short images need a surface caveat.** Most Big Think and Veritasium served images show dialogue frames with small subtitles. These are neither verified chosen covers nor feed frame zero. Big Think has 5/6 question titles in fast/slow Shorts, versus 6/2 for Kings and Generals: the direction is not consistent. Do not attribute Shorts-feed views/day to these cached images.

No competitor impressions or CTR were collected. View velocity is affected by channel size, subject, age and distribution. Cross-channel ranking, pooled success rates and causal claims are inappropriate.

## HOS implications to test after the remaining study

1. Keep the warm painted world, cream/gold serif long lettering, small Explorer and a single large hero object. Competitor darkness/colour measurements do not override the HOS rules.
2. Test a specific visible physical puzzle rather than a title painted verbatim. A periodic-table B should actually communicate a missing/predicted element; the saved live thumbnail is dominated by glassware. Any new text must complement the title and stay clear of the hero.
3. Hold all running and prearmed tests. Do not invent three eligible longs: present evidence protects Germs, X-rays, Atom and three scheduled films. Periodic Table has a finished historical test; the compilation has no displayed test badge, which still requires a current configuration check before arming.

These are **untried hypotheses**. No pattern has a recorded win or loss. No new rule, retitle, thumbnail swap or test is authorised by this document.

## Next work, without repeating collection

Use `../recovered/neighbour_competitors.json`, `search_neighbours.json`, and `neighbour_thumbnail_manifest.json` from the first J1107 checkpoint to code the six search-neighbour cohorts. Their images and existing sheets are already under `_desk/J1107/competitors/` (channel names include RationalThinker118, HistoryoftheUniverse, pbsorigins, crashcourse, HumanProgressOrg, TEDEd). Then finish Short cover/opening verification, reconcile live test configuration/ledger, select eligible designs, run the independent packaging panel and prepare Chief-gated Studio jobs. The original job remains unfinished.
