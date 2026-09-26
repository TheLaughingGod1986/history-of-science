async (page) => {
  const PLATE = "05_ring_darker";
  const VERSION = "v03";
  const PROMPT = "Animistry premium 3D cartoon. ONE persistent 1895 W\u00fcrzburg physics lab: dark wood benches, dark curtains, coils, one Crookes/cathode-ray glass tube, fluorescent cardboard screen when needed, ominous soft green-violet glow. Camera/object motion continuous through final frame. Silent picture only. NO stock lifestyle. NO photoreal medical. NO Orbit robot. NO Ken Burns only. A denser ring-shaped shadow sits darker on the hand/bone silhouette in the beam; mute must read denser/darker ring. Continuous. Silent. Clean palm/desk. HARD REJECT: Bertha nameplate text wall. HARD NEGATIVE: NO DNA helix, NO double helix, NO yellow DNA spiral, NO purple DNA spiral, NO science-lab DNA model garnish, NO Periodic-table DNA desk prop, NO molecular helix decoration anywhere in frame. Clean W\u00fcrzburg physics lab only. The fluorescent screen is a FLAT rectangular cardboard sheet only \u2014 never a spiral, never a twisted ladder, never a double-helix structure inside glass. Beam is a soft straight green-violet cone or ray only. Absolutely no molecular models, no helix props, no yellow/purple/green spiral structures anywhere. DESK IS EMPTY OF MODELS: never place any tall standing spiral, twisted ladder, molecular sculpture, yellow-purple twisted tower, or DNA-like prop on the bench, shelf, or background. Only allowed props: Crookes/cathode tube, coils, flat rectangular fluorescent cardboard sheet, dark wood benches, curtains. If a prop looks like a helix, delete it from the scene.";
  await page.evaluate(() => {
    for (const el of document.querySelectorAll('.cdk-overlay-container, .mat-mdc-snack-bar-container, .mdc-snackbar')) {
      try { el.remove(); } catch (e) {}
    }
  });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(300);
  const pm = page.locator('.ProseMirror[contenteditable="true"]').first();
  await pm.click();
  await page.waitForTimeout(200);
  await page.keyboard.press('Meta+A');
  await page.keyboard.press('Backspace');
  await page.keyboard.insertText(PROMPT);
  await page.waitForTimeout(900);
  const promptNow = await page.evaluate(() => {
    const el = document.querySelector('.ProseMirror[contenteditable="true"]');
    return el ? { len: el.innerText.length, head: el.innerText.slice(0,100), hasDNA: /NO DNA helix/i.test(el.innerText) } : null;
  });
  if (!promptNow || promptNow.len < 80 || !promptNow.hasDNA) return { ok:false, stage:'prompt-short', promptNow };
  const createState = await page.evaluate(() => {
    const hits = [];
    for (const b of document.querySelectorAll('button')) {
      const aria = b.getAttribute('aria-label') || '';
      const t = (b.innerText || '').trim();
      if (!/arrow_forward|Start generation|^Create$/i.test(t + ' ' + aria)) continue;
      const disabled = b.disabled || b.getAttribute('aria-disabled') === 'true';
      const r = b.getBoundingClientRect();
      hits.push({ disabled, x: r.x+r.width/2, y: r.y+r.height/2 });
    }
    return hits;
  });
  const send = createState.find(h => !h.disabled);
  if (!send) return { ok:false, stage:'create-disabled', createState, promptNow };
  await page.mouse.click(send.x, send.y);
  await page.waitForTimeout(1500);
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText || '').trim().replace(/\n/g, ' ');
      if (/^(Confirm|Continue|Generate|OK|Got it)$/i.test(t) || /confirm.*credit/i.test(t)) { b.click(); return t; }
    }
    return null;
  });
  await page.waitForTimeout(3000);
  const body = (await page.locator('body').innerText({ timeout: 5000 }).catch(()=>'' ));
  const unpaid = /unpaid|payment (failed|error)|billing|purchase failed/i.test(body);
  if (unpaid) {
    await page.reload({ waitUntil: 'domcontentloaded', timeout: 120000 });
    await page.waitForTimeout(2000);
    return { ok:false, stage:'unpaid-need-retry', unpaid:true };
  }
  const pcts = [...body.matchAll(/(\d{1,3})\s*%/g)].map(m => m[1]);
  return { ok:true, plate:PLATE, version:VERSION, promptNow, unpaid:false, pcts:pcts.slice(0,5), bodyHead: body.replace(/\n/g,' | ').slice(0,400) };
}
