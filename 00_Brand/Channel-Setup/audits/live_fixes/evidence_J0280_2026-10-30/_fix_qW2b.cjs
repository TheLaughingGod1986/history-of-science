const puppeteer = require("/Users/benjaminoats/.npm-global/lib/node_modules/puppeteer-core");
const fs = require("fs");
const path = require("path");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const VID = "qW2OsD4mujc";
const WANT = "How Did We Discover the Periodic Table?";

async function relatedChunk(page) {
  return page.evaluate(() => {
    const t = document.body ? document.body.innerText : "";
    const i = t.indexOf("Related video");
    return i < 0 ? "" : t.slice(i, i + 240);
  });
}

(async () => {
  const browser = await puppeteer.connect({ browserURL: "http://127.0.0.1:9460", defaultViewport: null });
  const page = await browser.newPage();
  await page.goto(`https://studio.youtube.com/video/${VID}/edit`, { waitUntil: "domcontentloaded", timeout: 90000 });
  await sleep(3000);
  for (let i = 0; i < 16; i++) { await page.evaluate(() => window.scrollBy(0, 1200)); await sleep(50); }
  const widget = await page.$("ytcp-shorts-content-links-picker");
  if (widget) await widget.click();
  await sleep(2500);

  // Search exact long title fragment
  await page.evaluate(() => {
    const dlg = document.querySelector("ytcp-video-pick-dialog");
    const walk = (r, d = 0) => {
      if (!r || d > 45) return null;
      for (const el of r.querySelectorAll ? r.querySelectorAll("input") : []) { el.focus(); return true; }
      for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) if (el.shadowRoot) { const h = walk(el.shadowRoot, d + 1); if (h) return h; }
      return null;
    };
    walk(dlg);
  });
  await page.keyboard.down("Meta"); await page.keyboard.press("a"); await page.keyboard.up("Meta");
  await page.keyboard.press("Backspace");
  await page.keyboard.type("How Did We Discover the Periodic", { delay: 20 });
  await sleep(3500);

  const dump = await page.evaluate(() => {
    const cards = [];
    const walk = (r, d = 0) => {
      if (!r || d > 50) return;
      for (const el of r.querySelectorAll ? r.querySelectorAll("div,span,a") : []) {
        const t = (el.innerText || "").replace(/\s+/g, " ").trim();
        if (!t || t.length < 10 || t.length > 200) continue;
        if (!/periodic|discover/i.test(t)) continue;
        const b = el.getBoundingClientRect();
        if (b.width > 60 && b.height >= 28 && b.height <= 120 && b.y > 60 && b.y < 900)
          cards.push({ t: t.slice(0, 160), x: b.x + b.width / 2, y: b.y + b.height / 2, h: Math.round(b.height) });
      }
      for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) if (el.shadowRoot) walk(el.shadowRoot, d + 1);
    };
    walk(document.querySelector("ytcp-video-pick-dialog") || document);
    const seen = new Set(); const out = [];
    for (const c of cards.sort((a,b)=>a.h-b.h)) { const k=c.t.slice(0,50); if(seen.has(k)) continue; seen.add(k); out.push(c); }
    return out.slice(0, 20);
  });
  console.log("candidates:");
  for (const c of dump) console.log("-", c.h, c.t);

  const hit = dump.find((c) => /how did we discover the periodic table/i.test(c.t))
    || dump.find((c) => /discover the periodic table/i.test(c.t));
  if (!hit) {
    console.log("NO LONG TITLE");
    await page.screenshot({ path: path.join(__dirname, "qW2b_fail.png"), fullPage: true });
    await page.keyboard.press("Escape");
    await page.close(); browser.disconnect(); process.exit(1);
  }
  console.log("picking", hit.t);
  await page.mouse.click(hit.x, hit.y);
  await sleep(900);
  const saved = await page.evaluate(() => {
    const walk = (r, d = 0) => {
      if (!r || d > 35) return null;
      for (const el of r.querySelectorAll ? r.querySelectorAll("button,ytcp-button,[role=button]") : []) {
        const t = (el.innerText || "").trim();
        if (/^Save$/i.test(t)) {
          const dis = el.disabled || el.getAttribute("aria-disabled") === "true";
          if (!dis) { el.click(); return "clicked"; }
          return "disabled";
        }
      }
      for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) if (el.shadowRoot) { const x = walk(el.shadowRoot, d + 1); if (x) return x; }
      return null;
    };
    return walk(document);
  });
  console.log("saved", saved);
  await sleep(2800);
  await page.goto(`https://studio.youtube.com/video/${VID}/edit`, { waitUntil: "domcontentloaded", timeout: 90000 });
  await sleep(3000);
  for (let i = 0; i < 14; i++) { await page.evaluate(() => window.scrollBy(0, 1200)); await sleep(50); }
  const chunk = await relatedChunk(page);
  console.log("after", JSON.stringify(chunk));
  const ok = /How Did We Discover the Periodic Table/i.test(chunk);
  fs.writeFileSync(path.join(__dirname, "qW2_RESULT.json"), JSON.stringify({ id: VID, want: WANT, hit, saved, chunk, ok }, null, 2) + "\n");
  await page.screenshot({ path: path.join(__dirname, "qW2_after.png"), fullPage: true });
  await page.close(); browser.disconnect();
  process.exit(ok ? 0 : 1);
})().catch((e) => { console.error(e); process.exit(3); });
