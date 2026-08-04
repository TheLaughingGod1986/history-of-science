# Retention & growth — locked going forward (Orbit with Ben)

**Locked:** 2026-08-05  
**Applies to:** every Short + every long from **V013 onward** (JWST ships under existing plan; don’t mid-rebuild)  
**Success:** more views **and** higher % watched — then subscribers.

Canonical detail: `docs/ORBIT_GROWTH_PLAYBOOK.md` · memory: `docs/RETENTION_LEARNINGS.md`  
Pre-build data: `PRE_BUILD_VIDIQ_AUDIT_TEMPLATE.md` · story/VO: `LONGFORM_STORY_AND_VO_PICTURE_GATE.md`

---

## P0 — Retention

1. **First 1.5s is the product (Shorts)** — speech + drama on frame 1; no logo/welcome/soft wind-up.  
2. **Long open ≤15–20s to first paradox** — no brand-first cold open.  
3. **Curiosity reset every 30–60s** — chapter card / new Q / number / turn.  
4. **VO–picture lock** — show or act the narration; no generic filler under specific VO.  
5. **One teach-point per chapter** — viewer leaves knowing something concrete.  
6. **Payoff before outro** — answer the open loop; soft CTA only at the end.

## P0 — Growth

7. **Shorts = discovery engine** — keep cluster cadence; package **22–30s** micro-stories (not 44s pads).  
8. **Pre-build vidIQ audit (blocking)** — keywords · title ≥90 · outliers → then script/VO/gen.  
9. **Thumb = title promise** — one idea, mobile-readable.  
10. **Related + pinned full-film** on every Short once the long is public.  
11. **Soft “follow for the next mystery”** at end only — never interrupt the hook.

## P1 — Habits

12. **Weekly scorecard** — Short stayed-to-watch / AVD / completion · long CTR / 30s / APV · subs.  
13. **Series rhythm** — next mysteries feel like “next lesson” (e.g. Moon → star-walk → Mars).  
14. **Reuse only branding + Orbit kit** — unique story plates per episode.  
15. **No niche pivot under ~1k views** — sample still directional.

## Do not

- Fearbait titles (even if vidIQ scores higher)  
- Stretch Shorts to 45–60s  
- Mid-flight rebuild of JWST for length  
- Meme/movie outlier chasing  
- Schedule thrash during experiment windows  

---

## Per-episode checklist (quick)

**Before gen**

- [ ] Pre-build vidIQ audit signed off  
- [ ] Title ≥90 · thumb matches promise  
- [ ] 4–6 chapters with teach-points  
- [ ] Retention plan (hook → turns → payoff)

**Shorts**

- [ ] 22–30s standalone micro-story  
- [ ] ≥5 hooks scored; punch-first open  
- [ ] Visual change ≤3s · Orbit in-story  
- [ ] Related + pin when long is public · soft end CTA

**After publish**

- [ ] Log metrics into `RETENTION_LEARNINGS.md` / `SHORTS_EXPERIMENTS.md`  
- [ ] Diagnose open vs topic before killing an idea  

---

## Agent reminder

If building or advising on Orbit content, follow this file + the longform VO–picture gate + pre-build vidIQ audit. Prefer these over ad-hoc process changes.

**Cursor hooks (project):**

- `sessionStart` → injects this checklist + sets `ORBIT_RETENTION_GATE` env  
- `preToolUse` (Shell) → reminds before Veo/Omni/VO gen-looking commands  

Config: `.cursor/hooks.json` · scripts: `.cursor/hooks/orbit-*.py`  
Primary enforcement remains `alwaysApply` rules in `.cursor/rules/`.

