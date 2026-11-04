const puppeteer = require("/Users/benjaminoats/.npm-global/lib/node_modules/puppeteer-core");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function openPicker(page) {
  for (let i = 0; i < 16; i++) {
    await page.evaluate(() => window.scrollBy(0, 1200));
    await sleep(50);
  }
  const widget = await page.$("ytcp-shorts-content-links-picker");
  if (widget) await widget.click();
  await sleep(2200);
}

async function clickTab(page, name) {
  const hit = await page.evaluate((name) => {
    const re = new RegExp("^" + name + "$", "i");
    const walk = (r, d = 0) => {
      if (!r || d > 45) return null;
      for (const el of r.querySelectorAll
        ? r.querySelectorAll("[role=tab],tp-yt-paper-tab,button,div,span")
        : []) {
        const t = (el.innerText || "").trim();
        if (re.test(t)) {
          const b = el.getBoundingClientRect();
          if (b.width > 30 && b.height > 14 && b.y > 40 && b.y < 500)
            return { x: b.x + b.width / 2, y: b.y + b.height / 2, t };
        }
      }
      for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) {
        if (el.shadowRoot) {
          const h = walk(el.shadowRoot, d + 1);
          if (h) return h;
        }
      }
      return null;
    };
    return walk(document.querySelector("ytcp-video-pick-dialog") || document);
  }, name);
  if (hit) {
    await page.mouse.click(hit.x, hit.y);
    await sleep(1500);
  }
  return hit;
}

async function fill(page, q) {
  await page.evaluate((q) => {
    const dlg = document.querySelector("ytcp-video-pick-dialog");
    const walk = (r, d = 0) => {
      if (!r || d > 45) return null;
      for (const el of r.querySelectorAll ? r.querySelectorAll("input") : []) {
        el.focus();
        el.value = "";
        el.dispatchEvent(new Event("input", { bubbles: true }));
        return true;
      }
      for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) {
        if (el.shadowRoot) {
          const h = walk(el.shadowRoot, d + 1);
          if (h) return h;
        }
      }
      return null;
    };
    walk(dlg);
  }, q);
  await page.keyboard.down("Meta");
  await page.keyboard.press("a");
  await page.keyboard.up("Meta");
  await page.keyboard.press("Backspace");
  await page.keyboard.type(q, { delay: 20 });
  await sleep(3500);
}

async function dump(page, label) {
  const after = await page.evaluate(() => {
    const d = document.querySelector("ytcp-video-pick-dialog");
    const cards = [];
    const walk = (r, dpth = 0) => {
      if (!r || dpth > 50) return;
      for (const el of r.querySelectorAll
        ? r.querySelectorAll(
            "ytcp-entity-card,ytcp-video-list-cell-video,[role=option],ytcp-video-row,a,div"
          )
        : []) {
        const t = (el.innerText || "").replace(/\s+/g, " ").trim();
        const b = el.getBoundingClientRect();
        if (b.width > 80 && b.height > 36 && b.y > 80 && b.y < 900 && t.length >= 8 && t.length < 280) {
          cards.push({ tag: el.tagName, t: t.slice(0, 140), h: Math.round(b.height), y: Math.round(b.y) });
        }
      }
      for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) {
        if (el.shadowRoot) walk(el.shadowRoot, dpth + 1);
      }
    };
    if (d) walk(d);
    const seen = new Set();
    const out = [];
    for (const c of cards.sort((a, b) => a.h - b.h)) {
      const k = c.t.slice(0, 40);
      if (seen.has(k)) continue;
      seen.add(k);
      out.push(c);
    }
    return { text: ((d && d.innerText) || "").slice(0, 500), cards: out.slice(0, 12) };
  });
  console.log("\n==", label, "==");
  console.log("text", JSON.stringify(after.text).slice(0, 300));
  for (const c of after.cards) console.log("-", c.tag, "h"+c.h, c.t);
}

(async () => {
  const browser = await puppeteer.connect({ browserURL: "http://127.0.0.1:9460", defaultViewport: null });
  const page = await browser.newPage();
  await page.goto("https://studio.youtube.com/video/Rl2uZ-KOTl8/edit", { waitUntil: "domcontentloaded", timeout: 90000 });
  await sleep(3000);
  await openPicker(page);
  await dump(page, "initial");

  // Try Your videos + title
  await clickTab(page, "Your videos");
  await fill(page, "Tied Arm");
  await dump(page, "Your videos / Tied Arm");

  await fill(page, "The Tied Arm That Proved Your Blood Circulates");
  await dump(page, "Your videos / full title");

  // Search YouTube + id
  const tab = await clickTab(page, "Search YouTube");
  console.log("Search YouTube tab", tab);
  await fill(page, "wwcjcFfC-5M");
  await dump(page, "Search YouTube / id");

  await fill(page, "Tied Arm That Proved");
  await dump(page, "Search YouTube / title");

  await page.screenshot({ path: "/Users/benjaminoats/YouTube/History Of Science/00_Brand/Channel-Setup/audits/live_fixes/evidence_J0280_2026-10-30/picker_probe2.png", fullPage: true });
  await page.keyboard.press("Escape");
  await page.close();
  browser.disconnect();
})().catch((e) => { console.error(e); process.exit(1); });
