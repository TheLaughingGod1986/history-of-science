#!/usr/bin/env python3
"""Read the Vertex Free Trial credit from Cloud Billing → Credits (Chrome CDP :9222 on the Mini).

  ~/.venvs/hos-vertex/bin/python 07_Edit-Project/_vertex_credit_v01.py <label>

Prints CREDIT free_trial_remaining_gbp=… usable_gbp=… and saves a screenshot to
07_Edit-Project/_evidence/vertex_credits_<label>.png (gitignored). Appends the reading to
07_Edit-Project/VERTEX_CREDIT_LOG_v01.json.

Lag-aware floor (Claude #180 5981276239, 4 Oct 2026):
  usable = last_console − (all logged Vertex spend since that reading) − FLOOR_GBP
never the console figure alone. When consecutive readings share the same Free Trial £
(console lag plateau), the baseline is the FIRST of those equal readings.

Exits 3 if usable_gbp < 0 (i.e. estimated remaining would breach the £5 lag floor).
Authority: Claude 5981064652 + 5981112327 + 5981276239.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

EDIT = Path(__file__).resolve().parent
EVID = EDIT / "_evidence"
LOG = EDIT / "VERTEX_CREDIT_LOG_v01.json"
URL = "https://console.cloud.google.com/billing/0124D1-E6EFD6-40F6DA/credits/all?project=gen-lang-client-0538779324"
FLOOR_GBP = 0.0  # Ben, 10 Oct 2026 22:50 (OWB #117 / HOS #275): spend the Free Trial to £0; never onto paid billing
GBP_PER_USD = 0.80  # PICTURE_PLAN_v01.json rates.gbp_per_usd_planning


def spend_usd_since(iso_at: str) -> float:
    """Sum take + still costs across PART0*_MINT_LOG_v01.json with timestamp > iso_at."""
    total = 0.0
    for f in sorted(EDIT.glob("PART0*_MINT_LOG_v01.json")):
        log = json.loads(f.read_text())
        for t in log.get("takes", []):
            ts = t.get("submitted_at") or t.get("at") or ""
            if ts > iso_at:
                total += float(t.get("cost_usd") or 0.0)
        for s in log.get("stills", []):
            ts = s.get("at") or ""
            if ts > iso_at:
                total += float(s.get("cost_usd") or 0.0)
    return total


def lag_plateau(readings: list[dict]) -> dict:
    """Last reading, walked back across equal Free Trial £ values (console lag plateau)."""
    if not readings:
        raise SystemExit("STOP: no credit readings")
    last = readings[-1]
    plateau = last
    for r in reversed(readings):
        if abs(float(r["free_trial_remaining_gbp"]) - float(last["free_trial_remaining_gbp"])) < 0.005:
            plateau = r
        else:
            break
    return plateau


def usable_from_log(extra_usd: float = 0.0) -> tuple[float, float, float, dict]:
    """Return (usable_gbp, est_remaining_gbp, spend_since_usd, plateau_reading)."""
    log = json.loads(LOG.read_text()) if LOG.exists() else {"readings": []}
    plateau = lag_plateau(log.get("readings", []))
    spend = spend_usd_since(plateau["at"]) + extra_usd
    est = float(plateau["free_trial_remaining_gbp"]) - spend * GBP_PER_USD
    usable = est - FLOOR_GBP
    return usable, est, spend, plateau


def main() -> int:
    label = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d_%H%M")
    EVID.mkdir(exist_ok=True)
    shot = EVID / f"vertex_credits_{label}.png"
    with sync_playwright() as p:
        br = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx = br.contexts[0]
        page = ctx.new_page()
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=60000)
            page.get_by_text("Free Trial").first.wait_for(timeout=60000)
            page.wait_for_timeout(2500)
            page.screenshot(path=str(shot))
            text = page.inner_text("body")
        finally:
            page.close()
    rows = [ln for ln in text.splitlines() if ln.strip()]
    remaining, status = None, None
    for i, ln in enumerate(rows):
        if ln.strip() == "Free Trial":
            window = " ".join(rows[i:i + 8])
            if "Available" in window:
                m = re.search(r"£([\d,]+\.\d\d)", window)
                if m:
                    remaining, status = float(m.group(1).replace(",", "")), "Available"
                    break
    if remaining is None:
        print(f"STOP: could not read the Free Trial row (screenshot {shot})")
        return 2
    rec = {"label": label, "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "free_trial_remaining_gbp": remaining, "status": status, "screenshot": shot.name,
           "floor_gbp": FLOOR_GBP, "gbp_per_usd": GBP_PER_USD}
    log = json.loads(LOG.read_text()) if LOG.exists() else {"source": URL, "readings": []}
    log["readings"].append(rec)
    # Lag-aware usable after appending this reading
    plateau = lag_plateau(log["readings"])
    spend = spend_usd_since(plateau["at"])
    est = float(plateau["free_trial_remaining_gbp"]) - spend * GBP_PER_USD
    usable = est - FLOOR_GBP
    rec["lag_plateau_label"] = plateau["label"]
    rec["lag_plateau_at"] = plateau["at"]
    rec["spend_usd_since_plateau"] = round(spend, 4)
    rec["est_remaining_gbp"] = round(est, 4)
    rec["usable_gbp"] = round(usable, 4)
    LOG.write_text(json.dumps(log, indent=2) + "\n")
    print(
        f"CREDIT free_trial_remaining_gbp={remaining:.2f} status={status} "
        f"plateau={plateau['label']}@{plateau['at']} spend_since_usd={spend:.4f} "
        f"est_remaining_gbp={est:.2f} floor={FLOOR_GBP:.0f} usable_gbp={usable:.2f} "
        f"rate={GBP_PER_USD} shot={shot}"
    )
    return 3 if usable < 0 else 0


if __name__ == "__main__":
    sys.exit(main())
