async (page) => {
  const fs = require('fs');
  const path = require('path');
  const crypto = require('crypto');
  const { execSync } = require('child_process');

  const QA = '/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays/07_Edit-Project/_qa_part03_batch_a';
  const CLIP = '/Users/benjaminoats/YouTube/History Of Science/02_Video-Projects/003_Invisible-Bones-X-Rays/04_Generated-Clips/part03';
  const PLATE = JSON.parse(fs.readFileSync(path.join(QA, 'REMINT_CURRENT.json'), 'utf8')).plate;
  const DEST = path.join(CLIP, `${PLATE}_v02.mp4`);
  const prompts = JSON.parse(fs.readFileSync(path.join(QA, 'REMINT_PROMPTS_v02.json'), 'utf8')).plates;
  const PROMPT = prompts[PLATE];
  if (!PROMPT) return { stop: true, stage: 'no-prompt', PLATE };
  if (fs.existsSync(DEST)) return { stop: true, stage: 'dest-exists', DEST };

  // Reminting 07 → v02; do not mutate KEEP plates 01/03 or historical 07_v01.
  const KEEP_NAMES = ['01_chapter_bones_v01.mp4', '03_soft_fades_v01.mp4', '07_explorer_hand_beam_v01.mp4'];
  const OTHER_PASS = [
    '02_hand_enters_path_v03.mp4',
    '04_bones_hold_v03.mp4',
    '05_ring_darker_v05.mp4',
    '06_living_skeleton_read_v02.mp4',
    '08_medicine_question_v02.mp4',
    '09_wonder_v02.mp4',
    '10_caution_burn_v02.mp4',
    '11_hold_beam_v02.mp4',
  ];
  const keepBefore = {};
  for (const name of [...KEEP_NAMES, ...OTHER_PASS]) {
    const p = path.join(CLIP, name);
    keepBefore[name] = { size: fs.statSync(p).size, mtime: fs.statSync(p).mtimeMs };
  }

  const UNUSUAL = /unusual activity|suspicious activity|you're not signed in|session ended|try signing in|verify it.?s you|couldn.?t verify|too many (requests|attempts)/i;
  const UNPAID = /unpaid|payment (failed|error)|couldn.?t (charge|process)|billing|add a payment|update (your )?payment|purchase failed|transaction failed/i;

  const bodyText = async () => {
    try { return (await page.locator('body').innerText({ timeout: 5000 })).slice(0, 12000); }
    catch { return ''; }
  };
  const abortIf = async (stage) => {
    const t = await bodyText();
    if (UNUSUAL.test(t)) {
      const shot = path.join(QA, `unusual_${PLATE}_${stage}.png`);
      await page.screenshot({ path: shot, fullPage: false });
      return { stop: true, stage, dialog: t.slice(0, 800), shot };
    }
    return null;
  };
  const unpaid = async () => UNPAID.test(await bodyText());

  if (!page.url().includes('537a3344-5ba3-46c3-b727-4e166601d9d0')) {
    await page.goto('https://flow.google.com/project/537a3344-5ba3-46c3-b727-4e166601d9d0', { waitUntil: 'domcontentloaded', timeout: 120000 });
    await page.waitForTimeout(2000);
  }

  let stop = await abortIf('pre');
  if (stop) return stop;

  const settingsBtn = page.getByRole('button', { name: 'Settings trigger' });
  await settingsBtn.click({ timeout: 10000 });
  await page.waitForTimeout(800);
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button,[role="tab"]')) {
      const t = (b.innerText || '').trim().replace(/\n/g, ' ');
      if (/^Video$/i.test(t) || /^Videos?$/i.test(t)) { b.click(); return; }
    }
  });
  await page.waitForTimeout(400);
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText || '').trim().replace(/\n/g, ' ');
      if (/Veo|Banana|Nano|model/i.test(t) && t.length < 60) {
        const r = b.getBoundingClientRect();
        if (r.width > 40 && r.y > 80) { b.click(); break; }
      }
    }
  });
  await page.waitForTimeout(600);
  const clickedModel = await page.evaluate(() => {
    for (const el of document.querySelectorAll('button,[role="option"],[role="menuitem"],li')) {
      const t = (el.innerText || '').trim().replace(/\n/g, ' ');
      if (/veo/i.test(t) && /quality/i.test(t)) { el.click(); return t.slice(0, 80); }
    }
    return null;
  });
  await page.waitForTimeout(400);
  await page.evaluate(() => {
    for (const b of document.querySelectorAll('button')) {
      const t = (b.innerText || '').trim();
      if (t.includes('16:9')) b.click();
    }
    const x1 = [...document.querySelectorAll('button')].filter(b => (b.innerText || '').trim() === 'x1');
    if (x1.length) x1[x1.length - 1].click();
  });
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);

  stop = await abortIf('post-settings');
  if (stop) return stop;

  const fillPrompt = async () => {
    const editor = page.locator('[contenteditable="true"], textarea, [role="textbox"]').last();
    await editor.click({ timeout: 10000 });
    await page.keyboard.press('Meta+A');
    await page.keyboard.press('Backspace');
    await page.keyboard.insertText(PROMPT);
    await page.waitForTimeout(400);
  };

  const clickCreate = async () => {
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
    if (!send) return { ok: false, createState };
    await page.mouse.click(send.x, send.y);
    await page.waitForTimeout(1200);
    await page.evaluate(() => {
      for (const b of document.querySelectorAll('button')) {
        const t = (b.innerText || '').trim().replace(/\n/g, ' ');
        if (/^(Confirm|Continue|Generate|OK|Got it)$/i.test(t) || /confirm.*credit/i.test(t)) {
          b.click(); return t;
        }
      }
      return null;
    });
    return { ok: true, createState };
  };

  await fillPrompt();
  stop = await abortIf('pre-create');
  if (stop) return stop;
  let created = await clickCreate();
  if (!created.ok) {
    await page.screenshot({ path: path.join(QA, `create_disabled_${PLATE}.png`), fullPage: false });
    return { stop: true, stage: 'create-disabled', created };
  }

  let unpaidRetry = false;
  await page.waitForTimeout(2500);
  if (await unpaid()) {
    unpaidRetry = true;
    await page.reload({ waitUntil: 'domcontentloaded', timeout: 120000 });
    await page.waitForTimeout(2000);
    if (!page.url().includes('537a3344-5ba3-46c3-b727-4e166601d9d0')) {
      await page.goto('https://flow.google.com/project/537a3344-5ba3-46c3-b727-4e166601d9d0', { waitUntil: 'domcontentloaded', timeout: 120000 });
      await page.waitForTimeout(2000);
    }
    try {
      await page.getByRole('button', { name: 'Settings trigger' }).click({ timeout: 5000 });
      await page.waitForTimeout(500);
      await page.keyboard.press('Escape');
    } catch (e) {}
    await fillPrompt();
    created = await clickCreate();
    if (!created.ok) return { stop: true, stage: 'create-disabled-retry', created };
    await page.waitForTimeout(2500);
    if (await unpaid()) {
      return { stop: true, stage: 'unpaid-after-refresh', note: 'no charge-loop' };
    }
  }

  stop = await abortIf('post-create');
  if (stop) return stop;

  const t0 = Date.now();
  let mediaUrl = null;
  let lastStatus = '';
  while (Date.now() - t0 < 720000) {
    stop = await abortIf('wait');
    if (stop) return stop;
    if (await unpaid()) return { stop: true, stage: 'unpaid-during-wait', unpaidRetry };
    const body = (await bodyText()).toLowerCase();
    if (body.includes('generation quota') || body.includes('reached your generation quota')) {
      return { stop: true, stage: 'quota' };
    }

    const vids = await page.evaluate(() =>
      [...document.querySelectorAll('video')].map(v => v.currentSrc || v.src).filter(Boolean)
    );
    for (const u of vids) {
      if (u.startsWith('http') && u.includes('google')) { mediaUrl = u; break; }
    }
    if (mediaUrl) break;

    if (Date.now() - t0 > 50000) {
      const dl = page.getByRole('button', { name: 'Download batch' }).first();
      if (await dl.count()) {
        try {
          const [download] = await Promise.all([
            page.waitForEvent('download', { timeout: 20000 }),
            dl.click({ timeout: 5000 }),
          ]);
          const tmpZip = path.join(QA, `${PLATE}_v02_dl.zip`);
          await download.saveAs(tmpZip);
          const unzipDir = path.join(QA, `_unzip_remint_${PLATE}`);
          execSync(`rm -rf "${unzipDir}" && mkdir -p "${unzipDir}" && unzip -o "${tmpZip}" -d "${unzipDir}" >/dev/null`);
          const mp4 = execSync(`find "${unzipDir}" -type f -iname '*.mp4' | head -1`).toString().trim();
          if (mp4 && fs.statSync(mp4).size > 150000) {
            fs.mkdirSync(CLIP, { recursive: true });
            fs.copyFileSync(mp4, DEST);
            mediaUrl = 'download-batch:' + tmpZip;
            break;
          }
        } catch (e) {}
      }
    }

    let status = '...';
    for (const k of ['generating', 'thinking', 'queue', 'high demand', 'creating', 'working']) {
      if (body.includes(k)) { status = k; break; }
    }
    const line = `wait ${Math.floor((Date.now()-t0)/1000)}s ${status}`;
    if (line !== lastStatus) { lastStatus = line; console.log(line); }
    await page.waitForTimeout(4000);
  }

  if (!fs.existsSync(DEST)) {
    if (!mediaUrl) {
      await page.screenshot({ path: path.join(QA, `timeout_${PLATE}.png`), fullPage: false });
      return { stop: true, stage: 'timeout', lastStatus };
    }
    if (!String(mediaUrl).startsWith('download-batch:')) {
      const resp = await page.request.get(mediaUrl, { timeout: 120000 });
      const buf = Buffer.from(await resp.body());
      if (buf.length < 150000 || buf.slice(0, 64).indexOf('ftyp') < 0) {
        return { stop: true, stage: 'bad-download', bytes: buf.length, mediaUrl: String(mediaUrl).slice(0, 120) };
      }
      fs.mkdirSync(CLIP, { recursive: true });
      fs.writeFileSync(DEST, buf);
    }
  }

  for (const name of Object.keys(keepBefore)) {
    const p = path.join(CLIP, name);
    const st = fs.statSync(p);
    if (st.size !== keepBefore[name].size || st.mtimeMs !== keepBefore[name].mtime) {
      return { stop: true, stage: 'keep-mutated', name };
    }
  }

  const stripPy = path.join(QA, '_strip_one.py');
  fs.writeFileSync(
    stripPy,
    'from pathlib import Path\nimport sys\nsys.path.insert(0, "/Users/benjaminoats/YouTube/History Of Science/04_Audio/tools")\nimport orbit_gemini_veo as veo\nveo.strip_audio(Path(' + JSON.stringify(DEST) + '))\n'
  );
  try { execSync(`/Users/benjaminoats/YouTube/History\\ Of\\ Science/.venv-hos/bin/python "${stripPy}"`); } catch (e) {}

  const buf = fs.readFileSync(DEST);
  const sha = crypto.createHash('sha256').update(buf).digest('hex');
  let duration_s = 8.0;
  try {
    duration_s = parseFloat(execSync(`ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "${DEST}"`).toString().trim());
  } catch (e) {}
  try {
    execSync(`ffmpeg -y -ss 0.4 -i "${DEST}" -frames:v 1 -q:v 3 "${path.join(QA, PLATE + '_v02_start.jpg')}" 2>/dev/null`);
    execSync(`ffmpeg -y -ss ${Math.max(0.5, duration_s/2)} -i "${DEST}" -frames:v 1 -q:v 3 "${path.join(QA, PLATE + '_v02_mid.jpg')}" 2>/dev/null`);
    execSync(`ffmpeg -y -ss ${Math.max(0.5, duration_s-0.6)} -i "${DEST}" -frames:v 1 -q:v 3 "${path.join(QA, PLATE + '_v02_end.jpg')}" 2>/dev/null`);
  } catch (e) {}

  const report = {
    plate: PLATE,
    version: 'v02',
    path: DEST,
    bytes: buf.length,
    sha256: sha,
    duration_s,
    model: 'Veo 3.1 - Quality',
    clickedModel,
    unpaidRetry,
    project: page.url(),
    account: 'benoats@googlemail.com',
    mute_note: 'Mute: on-model Explorer (glasses, crown, teal trenchcoat) raises hand into safe beam then lowers; clean empty lab behind him — NO DNA helix / purple helix garnish.',
    mediaUrlHead: String(mediaUrl || '').slice(0, 160),
    ts: new Date().toISOString(),
  };
  fs.writeFileSync(path.join(QA, `${PLATE}_v02_mint.json`), JSON.stringify(report, null, 2));
  await page.screenshot({ path: path.join(QA, `${PLATE}_v02_landed.png`), fullPage: false });
  return report;
}
