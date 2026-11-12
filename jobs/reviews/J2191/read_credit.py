"""Read-only billing evidence; reuse the existing tab, never create or close one."""
import sys,json
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,'/Users/benjaminoats/YouTube/orbit-with-ben/scripts')
from cdp_tabs import reuse_page
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.connect_over_cdp('http://127.0.0.1:9222')
 page=reuse_page(b.contexts[0],'console.cloud.google.com')
 page.goto('https://console.cloud.google.com/billing/0124D1-E6EFD6-40F6DA/credits/all?project=gen-lang-client-0538779324',wait_until='domcontentloaded')
 page.get_by_text('Free Trial',exact=True).first.wait_for(timeout=30000)
 rows=page.locator('tr').all_inner_texts()
 rows=[r for r in rows if ('Developer Program' in r or 'Free Trial' in r)]
 out={'at':datetime.now(timezone.utc).isoformat(),'read_only':True,'credit_rows':rows}
 Path('jobs/reviews/J2191/LIVE_CREDITS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
