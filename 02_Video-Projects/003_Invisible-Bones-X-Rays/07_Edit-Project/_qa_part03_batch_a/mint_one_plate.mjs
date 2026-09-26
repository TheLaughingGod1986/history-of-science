async (page) => {
  const fs = require('fs');
  const path = require('path');
  const crypto = require('crypto');

  const DEST = '/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays/04_Generated-Clips/part03/01_chapter_bones_v01.mp4';
  const QA = '/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project/_qa_part03_batch_a';
  const MODEL = 'Veo 3.1 - Quality';
  const PROMPT = [
    'Animistry premium 3D cartoon. ONE persistent 1895 Würzburg physics lab DNA:',
    'dark wood benches, dark curtains, coils, one Crookes/cathode-ray glass tube,',
    'fluorescent cardboard screen, ominous soft green-violet glow.',
    'Chapter/beam/cardboard establish Bones Without a Knife — soft green-violet beam cone',
    'toward cardboard; continuous camera motion; silent-readable chapter energy.',
    'Continuous motion through the final frame. Silent. No Explorer.',
    'SCENERY ONLY — no characters, no robots, no mascots, no Orbit, no text wall.',
    'Silent picture only. HARD REJECT: gore, Orbit, Ken Burns only, photoreal medical.',
  ].join(' ');

  const UNUSUAL = /unusual activity|suspicious activity|you're not signed in|session ended|try signing in|verify it.?s you|couldn.?t verify|too many (requests|attempts)/i;

  const bodyText = async () => {
    try { return (await page.locator('body').innerText({ timeout: 5000 })).slice(0, 12000); }
    catch { return ''; }
  };

  const abortIfUnusual = async (stage) => {
    const t = await bodyText();
    if (UNUSUAL.test(t)) {
      const shot = path.join(QA, `unusual_${stage}.png`);
      await page.screenshot({ path: shot, fullPage: false });
      return { stop: true, stage, dialog: t.slice(0, 800), shot };
    }
    return null;
  };

  // Rename project title
  try {
    const titleBox = page.getByRole('textbox', { name: 'Editable text' });
    if (await titleBox.count()) {
      await titleBox.click({ timeout: 3000 });
      await page.keyboard.press('Meta+A');
      await page.keyboard.insertText('HOS 003 Part 03 Batch A');
      await page.keyboard.press('Enter');
      await page.waitForTimeout(800);
    }
  } catch (e) {}

  let stop = await abortIfUnusual('pre');
  if (stop) return stop;

  // Open settings
  const settingsBtn = page.getByRole('button', { name: 'Settings trigger' });
  await settingsBtn.click({ timeout: 10000 });
  await page.waitForTimeout(900);

  // Prefer Video tab / mode if present
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button,[role="tab"]')) {
      const t = (b.innerText || '').trim().replace(/\n/g, ' ');
      if (/^Video$/i.test(t) || /^Videos?$/i.test(t)) { b.click(); return; }
    }
  });
  await page.waitForTimeout(500);

  // Open model dropdown and pick Veo 3.1 Quality
  const modelPick = await page.evaluate((want) => {
    const texts = [];
    for (const el of document.querySelectorAll('button,[role="option"],[role="menuitem"],li,div')) {
      const t = (el.innerText || '').trim().replace(/\n/g, ' ');
      if (!t || t.length > 80) continue;
      if (/Veo|Quality|Fast|Lite|Banana|Omni/i.test(t)) texts.push(t.slice(0, 80));
    }
    // Click anything that looks like the model selector first
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText || '').trim().replace(/\n/g, ' ');
      if (/Veo|Banana|Nano|model/i.test(t) && t.length < 60) {
        const r = b.getBoundingClientRect();
        if (r.width > 40 && r.y > 80) { b.click(); break; }
      }
    }
    return texts.slice(0, 40);
  }, MODEL);
  await page.waitForTimeout(700);

  const clicked = await page.evaluate((want) => {
    const norm = (s) => s.toLowerCase().replace(/\s+/g, ' ');
    const w = norm(want);
    let best = null;
    for (const el of document.querySelectorAll('button,[role="option"],[role="menuitem"],li,div[role="button"]')) {
      const t = (el.innerText || '').trim().replace(/\n/g, ' ');
      const n = norm(t);
      if (!n.includes('veo')) continue;
      if (n.includes('quality') || n === w || n.includes(w)) {
        const r = el.getBoundingClientRect();
        if (r.width > 20 && r.height > 10) { best = { t: t.slice(0, 60), x: r.x + r.width/2, y: r.y + r.height/2 }; break; }
      }
    }
    if (best) {
      // click nearest element by text again
      for (const el of document.querySelectorAll('button,[role="option"],[role="menuitem"],li')) {
        const t = (el.innerText || '').trim().replace(/\n/g, ' ');
        if (t.slice(0, 60) === best.t || (t.toLowerCase().includes('veo') && t.toLowerCase().includes('quality'))) {
          el.click();
          return t.slice(0, 80);
        }
      }
    }
    return null;
  }, MODEL);
  await page.waitForTimeout(600);

  // Aspect 16:9 and x1
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText || '').trim();
      if (t.includes('16:9')) b.click();
    }
    const x1 = [...document.querySelectorAll('button')].filter(b => (b.innerText || '').trim() === 'x1');
    if (x1.length) x1[x1.length - 1].click();
  });
  await page.waitForTimeout(400);

  // Close settings overlay
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);

  stop = await abortIfUnusual('post-settings');
  if (stop) return stop;

  // Collect media ids before
  const beforeIds = await page.evaluate(() => {
    const ids = new Set();
    for (const a of document.querySelectorAll('a[href],img[src],video[src],source[src]')) {
      const s = a.href || a.src || '';
      const m = s.match(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i);
      if (m) ids.add(m[0]);
    }
    return [...ids];
  });

  // Focus prompt editor and type
  const editor = page.locator('[contenteditable="true"], textarea, [role="textbox"]').last();
  await editor.click({ timeout: 10000 });
  await page.keyboard.press('Meta+A');
  await page.keyboard.press('Backspace');
  await page.keyboard.insertText(PROMPT);
  await page.waitForTimeout(400);

  stop = await abortIfUnusual('pre-create');
  if (stop) return stop;

  // Click Start generation / arrow_forward — ONE Create only
  const createState = await page.evaluate(() => {
    const hits = [];
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText || '').trim().replace(/\n/g, ' ');
      const isArrow = /arrow_forward/i.test(t);
      const isCreate = /^Create$/i.test(t) || /Start generation/i.test(b.getAttribute('aria-label') || '');
      if (!isArrow && !isCreate) continue;
      const disabled = b.disabled || b.getAttribute('aria-disabled') === 'true';
      const r = b.getBoundingClientRect();
      hits.push({ disabled, t: t.slice(0,40), aria: (b.getAttribute('aria-label')||'').slice(0,40), x: r.x+r.width/2, y: r.y+r.height/2, arrow: isArrow });
    }
    return hits;
  });

  const send = createState.find(h => h.arrow && !h.disabled) || createState.find(h => !h.disabled);
  if (!send) {
    await page.screenshot({ path: path.join(QA, 'create_disabled.png'), fullPage: false });
    return { stop: true, stage: 'create-disabled', createState, modelCandidates: modelPick, clickedModel: clicked };
  }

  await page.mouse.click(send.x, send.y);
  await page.waitForTimeout(1200);

  // Confirm spend if dialog
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText || '').trim().replace(/\n/g, ' ');
      if (/^(Confirm|Continue|Generate|OK|Got it)$/i.test(t) || /confirm.*credit/i.test(t)) {
        b.click(); return t;
      }
    }
    return null;
  });

  stop = await abortIfUnusual('post-create');
  if (stop) return stop;

  // Wait for video (up to ~12 min)
  const t0 = Date.now();
  let mediaUrl = null;
  let lastStatus = '';
  while (Date.now() - t0 < 720000) {
    stop = await abortIfUnusual('wait');
    if (stop) return stop;
    const body = (await bodyText()).toLowerCase();
    if (body.includes('generation quota') || body.includes('reached your generation quota')) {
      return { stop: true, stage: 'quota', dialog: body.slice(0, 400) };
    }
    if (/\bfailed\b/.test(body) && /generat|create|video/.test(body)) {
      return { stop: true, stage: 'failed', dialog: body.slice(0, 600) };
    }

    // Try harvest video srcs
    const found = await page.evaluate((before) => {
      const beforeSet = new Set(before);
      const vids = [...document.querySelectorAll('video')].map(v => v.currentSrc || v.src).filter(Boolean);
      for (const u of vids) {
        if (u.startsWith('http') && u.includes('google')) return { url: u, kind: 'video' };
      }
      // media links
      for (const a of document.querySelectorAll('a[href*="http"]')) {
        const u = a.href;
        if (/\.mp4|videoplayback|usercontent|lh3\.google/i.test(u)) return { url: u, kind: 'a' };
      }
      return null;
    }, beforeIds);

    if (found && found.url) {
      mediaUrl = found.url;
      break;
    }

    let status = '…';
    for (const k of ['generating', 'thinking', 'queue', 'high demand', 'creating', 'working']) {
      if (body.includes(k)) { status = k; break; }
    }
    const line = `wait ${Math.floor((Date.now()-t0)/1000)}s ${status}`;
    if (line !== lastStatus) { lastStatus = line; console.log(line); }

    await page.waitForTimeout(4000);
  }

  if (!mediaUrl) {
    await page.screenshot({ path: path.join(QA, 'timeout_01.png'), fullPage: false });
    return { stop: true, stage: 'timeout', lastStatus };
  }

  // Download via page request
  const resp = await page.request.get(mediaUrl, { timeout: 120000 });
  const buf = Buffer.from(await resp.body());
  if (buf.length < 150000 || buf.slice(0, 64).indexOf('ftyp') < 0) {
    return { stop: true, stage: 'bad-download', bytes: buf.length, mediaUrl: mediaUrl.slice(0, 120) };
  }
  fs.mkdirSync(path.dirname(DEST), { recursive: true });
  fs.writeFileSync(DEST, buf);
  const sha = crypto.createHash('sha256').update(buf).digest('hex');
  const report = {
    plate: '01_chapter_bones',
    path: DEST,
    bytes: buf.length,
    sha256: sha,
    model: MODEL,
    clickedModel: clicked,
    modelCandidates: modelPick,
    project: page.url(),
    account: 'benoats@googlemail.com',
    mediaUrlHead: mediaUrl.slice(0, 160),
    ts: new Date().toISOString(),
  };
  fs.writeFileSync(path.join(QA, '01_chapter_bones_mint.json'), JSON.stringify(report, null, 2));
  await page.screenshot({ path: path.join(QA, '01_chapter_bones_landed.png'), fullPage: false });
  return report;
}
