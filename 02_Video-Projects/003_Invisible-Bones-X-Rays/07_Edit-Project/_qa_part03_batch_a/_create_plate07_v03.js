async (page) => {
  const PROMPT = "Animistry premium 3D cartoon. 1895 W\u00fcrzburg physics lab only: dark wood benches, dark curtains, copper coils, ONE Crookes cathode-ray glass tube, soft green-violet beam as a straight cone of light. Explorer teal trenchcoat boy on-model: messy wavy brown hair, round thin gold wire-rim glasses, small gold crown in hair, teal-blue long overcoat, gold atom pin, tan waistcoat, white shirt, dark brown floppy bow, rolled brown trousers, cream socks, brown boots, satchel with compass. He raises his own hand toward the safe stylised beam, eyes wide, then lowers it. Finished hair. Continuous motion through final frame. Silent-readable. BEHIND Explorer: only plain dark curtain, window panes, or soft empty lab shadow \u2014 clean negative space. Desk and shelves hold ONLY the tube and coils \u2014 nothing else standing tall behind or beside him. No tall white sculptures. No twisted ladders. No molecular classroom models. No decorative towers. HARD REJECT: Orbit robot, twins, unfinished mid-crown hair, academic blazer, photoreal medical, Ken Burns only.";
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
  return { ok: true, typedLen, confirm, beforeDl, afterDl: await page.getByRole('button', { name: 'Download batch' }).count(), bodyHead: after.slice(0, 400) };
}