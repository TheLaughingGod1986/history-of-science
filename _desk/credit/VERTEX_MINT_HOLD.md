# Vertex mint HOLD — LIFTED (with £5 floor)

**Status:** **LIFTED**  
**As of:** 2026-10-04 15:35 Europe/London  
**Sources:** HOS desk #180 comments **5981064652** and **5981083881** (Claude → Grok)  
**Project:** `gen-lang-client-0538779324` (History of Science on billing account Orbit API / `0124D1-E6EFD6-40F6DA`)

## Prior hold
Was **HOLD active** from 2026-10-04 00:56 Europe/London (comment 5974778997) pending Ben's billing answer. Claude lifted it (5981064652); Ben confirmed wait-for-Flow/API-reset Tuesday (5981083881).

## Working rule (mandatory)
- **Free Trial only.** Stop at **£0 of real money**. **Nothing on the card. No top-up.**
- **Hard stop: 10 Nov 2026 23:59 Europe/London** (credit itself expires 11 Nov).
- **£5 lag floor:** before every mint, read the live Free Trial balance and estimate the job cost. **Refuse the job if `balance − job cost < £5`.**
- **Usable = live Free Trial − £5.** At lift (last confirmed): live **£37.84** → usable **£32.84**. Re-read live before each mint (gcloud was unauth on Mini this run; figure is from credit-confirm screenshot / credit log).
- After each batch: re-read live balance and append `VERTEX_CREDIT_LOG_v01.json` (this folder).
- **Vertex default** for character + teaching + boarded wides. **Vertex Fast** unless the board says **Quality**.
- **Flow Fast** only for no-character establishing (boarded: `P1:09_vilvoorde` KEEP already; park `P3:06_leeds_brewery`, `P5:01_geneva_lake` — and any other no-char establishing — for **Tuesday Flow reset**; do not burn remaining Flow credits before then).
- **007** = research / script / Shorts scripts only (**£0** mint).

## Tuesday (post-reset)
1. Post new Flow / Google Developer Program monthly / Gemini API balances (confirm exact reset times — do not assume).
2. Re-price remaining 006 vs live usable; if still over by ~20 Oct, propose reuses/cuts for 5 Nov air.

## Do not
- Change Google Cloud Billing (caps, budgets, linking) without Ben.
- Spend past Free Trial / onto pay-as-you-go without Ben.
- Mint when the £5 floor would be breached.
- Merge or close PR #180.

## Evidence at lift
- Screenshot: `_desk/credit/vertex_credits_2026-10-04_free_trial.png` (£37.84 Free Trial, Available, ends 11 Nov 2026).
- Reprice: `_desk/006/006_VERTEX_FLOW_SPLIT_REPRICE_20261004.json` (+ `.md`).
- This file also mirrored at `_desk/credit/VERTEX_MINT_HOLD.md`.
