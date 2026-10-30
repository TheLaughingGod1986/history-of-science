const puppeteer = require("/Users/benjaminoats/.npm-global/lib/node_modules/puppeteer-core");
const fs = require("fs");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const JOBS = [
  ["Rl2uZ-KOTl8", "Tied Arm"],
  ["PFj6172YU4Q", "Tied Arm"],
  ["Wvjd8g0CpzE", "Tied Arm"],
  ["pWySvZsneZg", "Inside an Atom"],
  ["qW2OsD4mujc", "Periodic Table"],
  ["xHnIi9GqOsM", "Tied Arm"],
  ["xzKoHg0E0_U", "Inside an Atom"],
];
(async () => {
  const browser = await puppeteer.connect({ browserURL: "http://127.0.0.1:9460", defaultViewport: null });
  const page = await browser.newPage();
  const out = [];
  for (const [id, needle] of JOBS) {
    await page.goto(`https://studio.youtube.com/video/${id}/edit`, { waitUntil: "domcontentloaded", timeout: 90000 });
    await sleep(2500);
    for (let i = 0; i < 14; i++) { await page.evaluate(() => window.scrollBy(0, 1200)); await sleep(40); }
    const chunk = await page.evaluate(() => {
      const t = document.body ? document.body.innerText : "";
      const i = t.indexOf("Related video");
      return i < 0 ? "" : t.slice(i, i + 200);
    });
    const ok = chunk.toLowerCase().includes(needle.toLowerCase()) && !/\bNone\b/.test(chunk.slice(0, 80));
    console.log(ok ? "OK" : "FAIL", id, JSON.stringify(chunk.slice(0, 100)));
    out.push({ id, needle, chunk, ok });
  }
  fs.writeFileSync(__dirname + "/READBACK.json", JSON.stringify({ at: new Date().toISOString(), out }, null, 2) + "\n");
  await page.close(); browser.disconnect();
  process.exit(out.every((r) => r.ok) ? 0 : 1);
})().catch((e) => { console.error(e); process.exit(3); });
