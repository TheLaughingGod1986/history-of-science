# Vertex £5 lag floor — mirrored into hos-006-trees

**Authority:** Claude #180 comments **5981064652** + **5981112327** + **5981276239** (Strategy A GO + credit-lag fix, 4 Oct 2026)

- `FLOOR_GBP = 5.0` in `_mint_vertex_v01.py` and `_vertex_credit_v01.py` (this Edit-Project).
- **Usable (lag-aware):** `last_console − (logged Vertex spend since that reading) − £5`.
  When consecutive console readings share the same Free Trial £, baseline = first of that plateau.
  **Never** the console figure alone. Rate: `GBP_PER_USD = 0.80` (`PICTURE_PLAN` planning).
- Current (after Part 02 resume, no further mint): console plateau £37.48 − $11.39×0.8 − £5 = **usable £23.37**.
- Hold previously LIFTED in hos-006-hold-lift `VERTEX_MINT_HOLD.md`; this tree now enforces the floor in code.
- Hard stop 10 Nov 23:59 UK; never onto paid card without Ben.
- Nothing more mints until UAT on PENDING takes is reviewed.
