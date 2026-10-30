const puppeteer = require("/Users/benjaminoats/.npm-global/lib/node_modules/puppeteer-core");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const browser = await puppeteer.connect({
    browserURL: "http://127.0.0.1:9460",
    defaultViewport: null,
  });
  const page = await browser.newPage();
  await page.goto("https://studio.youtube.com/video/Rl2uZ-KOTl8/edit", {
    waitUntil: "domcontentloaded",
    timeout: 90000,
  });
  await sleep(3000);
  for (let i = 0; i < 16; i++) {
    await page.evaluate(() => window.scrollBy(0, 1200));
    await sleep(60);
  }
  const widget = await page.$("ytcp-shorts-content-links-picker");
  console.log("widget", !!widget);
  if (widget) {
    await widget.click();
    await sleep(2500);
  }
  console.log(
    "dialog",
    await page.evaluate(() => !!document.querySelector("ytcp-video-pick-dialog"))
  );

  const filled = await page.evaluate((q) => {
    const dlg = document.querySelector("ytcp-video-pick-dialog");
    const walk = (r, d = 0) => {
      if (!r || d > 45) return null;
      for (const el of r.querySelectorAll ? r.querySelectorAll("input") : []) {
        el.focus();
        el.value = "";
        el.dispatchEvent(new Event("input", { bubbles: true }));
        el.value = q;
        el.dispatchEvent(new Event("input", { bubbles: true }));
        return el.id || "input";
      }
      for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) {
        if (el.shadowRoot) {
          const h = walk(el.shadowRoot, d + 1);
          if (h) return h;
        }
      }
      return null;
    };
    return walk(dlg);
  }, "wwcjcFfC-5M");
  console.log("filled", filled);
  await page.keyboard.down("Meta");
  await page.keyboard.press("a");
  await page.keyboard.up("Meta");
  await page.keyboard.press("Backspace");
  await page.keyboard.type("wwcjcFfC-5M", { delay: 25 });
  await sleep(4000);
  await page.screenshot({
    path:
      "/Users/benjaminoats/YouTube/History Of Science/00_Brand/Channel-Setup/audits/live_fixes/evidence_J0280_2026-10-30/picker_probe.png",
    fullPage: true,
  });

  const after = await page.evaluate(() => {
    const d = document.querySelector("ytcp-video-pick-dialog");
    const cards = [];
    const walk = (r, dpth = 0) => {
      if (!r || dpth > 50) return;
      for (const el of r.querySelectorAll
        ? r.querySelectorAll(
            "ytcp-entity-card,ytcp-video-list-cell-video,[role=option],ytcp-video-row,a,div,span,img"
          )
        : []) {
        const t = (el.innerText || "").replace(/\s+/g, " ").trim();
        const b = el.getBoundingClientRect();
        if (b.width > 80 && b.height > 36 && b.y > 80 && b.y < 900 && t.length >= 8 && t.length < 280) {
          cards.push({
            tag: el.tagName,
            t: t.slice(0, 140),
            w: Math.round(b.width),
            h: Math.round(b.height),
            y: Math.round(b.y),
          });
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
    return { text: ((d && d.innerText) || "").slice(0, 1200), cards: out.slice(0, 25) };
  });
  console.log("after text", JSON.stringify(after.text).slice(0, 600));
  console.log("cards", after.cards.length);
  for (const c of after.cards.slice(0, 20)) {
    console.log("-", c.tag, c.w + "x" + c.h, "y" + c.y, c.t);
  }
  await page.keyboard.press("Escape");
  await page.close();
  browser.disconnect();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
