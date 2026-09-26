async (page) => {
  const PLATE = "05_ring_darker";
  const VERSION = "v04";
  const PROMPT = "Animistry premium 3D cartoon. ONE persistent 1895 W\u00fcrzburg physics lab only: dark wood benches, dark curtains, copper coils, ONE Crookes cathode-ray glass tube, ONE flat rectangular fluorescent cardboard sheet. Soft green-violet beam is a straight cone of light. Camera and objects move continuously through the final frame. Silent picture only. NO stock lifestyle. NO photoreal medical. NO Orbit robot. NO Ken Burns still. Desk and shelves hold ONLY the tube, coils, and flat cardboard \u2014 nothing else standing on the bench. No tall sculptures. No twisted ladders. No yellow or purple decorative towers. No molecular classroom models. Clean empty bench surfaces otherwise. Close-up: denser ring-shaped shadow sits darker on the hand bone silhouette in the beam. Mute must read denser darker ring on bones. Clean palm. Continuous. Silent. Wonder not horror.";
  await page.evaluate(() => {
    for (const el of document.querySelectorAll('.cdk-overlay-container, .mat-mdc-snack-bar-container, .mdc-snackbar')) {
      try { el.remove(); } catch (e) {}
    }
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText||'').trim();
      if (/^(I agree|Agree|Accept|OK|Got it|No thanks)$/i.test(t)) b.click();
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
    return el ? { len: el.innerText.length, head: el.innerText.slice(0,100) } : null;
  });
  if (!promptNow || promptNow.len < 80) return { ok:false, stage:'prompt-short', promptNow };
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
