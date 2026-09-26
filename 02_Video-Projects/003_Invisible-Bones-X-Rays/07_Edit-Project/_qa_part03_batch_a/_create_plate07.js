async (page) => {
  const PROMPT = "W\u00fcrzburg 1895 physics lab only \u2014 dark wood benches, dark curtains, coils, one Crookes tube, soft green-violet beam glow. Clean empty negative space behind Explorer: plain curtain / dark wood wall / soft lab shadow \u2014 NEVER a DNA helix, double helix, Periodic DNA desk prop, or purple/yellow helix soft garnish behind him. Explorer teal trenchcoat boy (on-model: messy wavy brown hair, round thin gold wire-rim glasses, teal-blue long overcoat, gold atom pin, tan waistcoat, white shirt, dark brown floppy bow, rolled brown trousers, cream socks, brown boots, satchel+compass) holds his own hand toward a safe stylised beam, eyes wide, then lowers it. Finished hair. Continuous motion. Silent-readable. HARD REJECT: Orbit robot, twins, unfinished mid-crown hair, academic blazer. HARD FAIL FOREVER \u2014 no DNA helix, no double helix, no Periodic-table DNA desk prop, NO helix garnish / DNA soft background behind Explorer (soft-garnish does not stand). Animistry premium 3D cartoon. Soft green-violet beam is a straight cone of light only \u2014 never a spiral. DESK / BACKGROUND EMPTY OF MODELS: never place any tall standing spiral, twisted ladder, molecular sculpture, yellow-purple twisted tower, DNA-like prop, or glowing purple/yellow helix garnish behind Explorer, on the bench, shelf, or background. Only allowed environment: Crookes/cathode tube, coils, dark wood benches, curtains, soft lab shadow. If a prop looks like a helix, delete it from the scene. No readable text wall.";
  const UNUSUAL = /unusual activity|suspicious activity|you're not signed in|session ended|try signing in|verify it.?s you|couldn.?t verify|too many (requests|attempts)/i;
  const UNPAID = /unpaid|payment (failed|error)|couldn.?t (charge|process)|billing|add a payment|update (your )?payment|purchase failed|transaction failed/i;
  const bodyText = async () => {
    try { return (await page.locator('body').innerText({ timeout: 5000 })).slice(0, 12000); }
    catch { return ''; }
  };
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  const t0body = await bodyText();
  if (UNUSUAL.test(t0body)) return { stop: true, stage: 'pre-unusual', snip: t0body.slice(0, 400) };
  const beforeDl = await page.getByRole('button', { name: 'Download batch' }).count();
  // click visible contenteditable (not hidden recaptcha)
  const target = await page.evaluate(() => {
    for (const el of document.querySelectorAll('[contenteditable="true"]')) {
      const r = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      if (r.width > 20 && r.height > 10 && style.visibility !== 'hidden' && style.display !== 'none') {
        return { x: r.x + r.width/2, y: r.y + r.height/2 };
      }
    }
    return null;
  });
  if (!target) return { stop: true, stage: 'no-editor' };
  await page.mouse.click(target.x, target.y);
  await page.waitForTimeout(200);
  await page.keyboard.press('Meta+A');
  await page.keyboard.press('Backspace');
  await page.keyboard.insertText(PROMPT);
  await page.waitForTimeout(600);
  const typedLen = await page.evaluate(() => {
    for (const el of document.querySelectorAll('[contenteditable="true"]')) {
      const r = el.getBoundingClientRect();
      if (r.width > 20 && r.height > 10) return (el.innerText || '').length;
    }
    return 0;
  });
  const createState = await page.evaluate(() => {
    const hits = [];
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText || '').trim().replace(/\n/g, ' ');
      const aria = b.getAttribute('aria-label') || '';
      const isArrow = /arrow_forward/i.test(t) || /arrow_forward/i.test(aria);
      const isCreate = /^Create$/i.test(t) || /Start generation/i.test(aria);
      if (!isArrow && !isCreate) continue;
      const disabled = b.disabled || b.getAttribute('aria-disabled') === 'true';
      const r = b.getBoundingClientRect();
      hits.push({ disabled, t: t.slice(0,40), aria: aria.slice(0,40), x: r.x+r.width/2, y: r.y+r.height/2, arrow: isArrow });
    }
    return hits;
  });
  const send = createState.find(h => h.arrow && !h.disabled) || createState.find(h => !h.disabled);
  if (!send) return { stop: true, stage: 'create-disabled', createState, typedLen };
  await page.mouse.click(send.x, send.y);
  await page.waitForTimeout(1200);
  const confirm = await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText || '').trim().replace(/\n/g, ' ');
      if (/^(Confirm|Continue|Generate|OK|Got it)$/i.test(t) || /confirm.*credit/i.test(t)) {
        b.click(); return t;
      }
    }
    return null;
  });
  await page.waitForTimeout(3000);
  const after = await bodyText();
  if (UNPAID.test(after)) return { stop: true, stage: 'unpaid', snip: after.slice(0, 400) };
  if (UNUSUAL.test(after)) return { stop: true, stage: 'unusual-post', snip: after.slice(0, 400) };
  const afterDl = await page.getByRole('button', { name: 'Download batch' }).count();
  const generating = /generat|thinking|queue|creating|working|high demand/i.test(after);
  return {
    ok: true,
    typedLen,
    confirm,
    createState,
    beforeDl,
    afterDl,
    generating,
    bodyHead: after.slice(0, 600),
  };
}