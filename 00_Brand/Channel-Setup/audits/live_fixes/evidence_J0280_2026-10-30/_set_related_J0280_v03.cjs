#!/usr/bin/env node
/**
 * J0280 v03: set Studio Related on 7 HOS Shorts. Related only. CDP :9460.
 * Uses puppeteer-core + shadow-DOM picker (Playwright connect hangs).
 */
const fs = require("node:fs");
const path = require("node:path");
const puppeteer = require("/Users/benjaminoats/.npm-global/lib/node_modules/puppeteer-core");

const EV = __dirname;
const CDP = "http://127.0.0.1:9460";
const HOS = "UCXp7HkBIl1LgaznXuZHJyRg";
const ONLY = process.argv.includes("--only")
  ? process.argv[process.argv.indexOf("--only") + 1]
  : null;

const JOBS = [
  { n: 1, id: "Rl2uZ-KOTl8", related_id: "wwcjcFfC-5M", related_title: "The Tied Arm That Proved Your Blood Circulates" },
  { n: 2, id: "PFj6172YU4Q", related_id: "wwcjcFfC-5M", related_title: "The Tied Arm That Proved Your Blood Circulates" },
  { n: 3, id: "Wvjd8g0CpzE", related_id: "wwcjcFfC-5M", related_title: "The Tied Arm That Proved Your Blood Circulates" },
  { n: 4, id: "pWySvZsneZg", related_id: "GHZDsiH7L7A", related_title: "What's Really Inside an Atom?" },
  { n: 5, id: "qW2OsD4mujc", related_id: "AL_-qlWko_g", related_title: "How Did We Discover the Periodic Table?" },
  { n: 6, id: "xHnIi9GqOsM", related_id: "wwcjcFfC-5M", related_title: "The Tied Arm That Proved Your Blood Circulates" },
  { n: 7, id: "xzKoHg0E0_U", related_id: "GHZDsiH7L7A", related_title: "What's Really Inside an Atom?" },
].filter((j) => !ONLY || j.id === ONLY);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function relatedChunk(page) {
  return page.evaluate(() => {
    const t = document.body ? document.body.innerText : "";
    const i = t.indexOf("Related video");
    return i < 0 ? "" : t.slice(i, i + 240);
  });
}

function relatedOk(chunk, title, relatedId) {
  if (!chunk) return false;
  const head = chunk.slice(0, 160);
  if (/\bNone\b/.test(head)) return false;
  const words = (title.match(/[A-Za-z]{4,}/g) || []).slice(0, 5);
  const titleHit = words.some((w) => head.toLowerCase().includes(w.toLowerCase()));
  return titleHit || chunk.includes(relatedId) || chunk.includes(title.slice(0, 18));
}

async function openEdit(page, vid) {
  await page.goto(`https://studio.youtube.com/video/${vid}/edit`, {
    waitUntil: "domcontentloaded",
    timeout: 90000,
  });
  await sleep(3000);
  for (let i = 0; i < 16; i++) {
    await page.evaluate(() => window.scrollBy(0, 1200));
    await sleep(80);
  }
  // Scroll Related into view if present
  await page.evaluate(() => {
    const walk = (r, d = 0) => {
      if (!r || d > 40) return null;
      for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) {
        const t = (el.innerText || "").trim();
        if (/^Related video$/i.test(t) || /related video/i.test(el.getAttribute("aria-label") || "")) {
          el.scrollIntoView({ block: "center" });
          return true;
        }
        if (el.shadowRoot) {
          const x = walk(el.shadowRoot, d + 1);
          if (x) return x;
        }
      }
      return null;
    };
    walk(document);
  });
  await sleep(400);
}

async function openPicker(page) {
  const info = { open: false };
  // Prefer Shorts related widget
  const widget = await page.$("ytcp-shorts-content-links-picker");
  if (widget) {
    await widget.evaluate((el) => el.scrollIntoView({ block: "center" }));
    await widget.click({ delay: 30 }).catch(() => {});
    info.via = "shorts-content-links-picker";
    info.open = true;
  }
  if (!info.open) {
    // Click None / Add related / Related video in shadow DOM by coordinates
    const hit = await page.evaluate(() => {
      const walk = (r, d = 0) => {
        if (!r || d > 50) return null;
        for (const el of r.querySelectorAll
          ? r.querySelectorAll(
              "ytcp-button,button,[role=button],div,span,ytcp-icon-button,ytcp-shorts-content-links-picker"
            )
          : []) {
          const t = (el.innerText || "").trim();
          const a = el.getAttribute("aria-label") || "";
          if (
            /related video/i.test(a) ||
            t === "None" ||
            t === "Add" ||
            t === "Add video" ||
            /Add (a )?related video/i.test(t) ||
            /^Related video$/i.test(t) ||
            /Select video/i.test(t)
          ) {
            const b = el.getBoundingClientRect();
            if (b.width > 18 && b.height > 14 && b.y > 120) {
              return { x: b.x + b.width / 2, y: b.y + b.height / 2, t: (t || a).slice(0, 60) };
            }
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
      return walk(document);
    });
    if (hit) {
      await page.mouse.click(hit.x, hit.y);
      info.via = `mouse:${hit.t}`;
      info.open = true;
    }
  }
  await sleep(2000);
  info.dialog = await page.evaluate(() => !!document.querySelector("ytcp-video-pick-dialog"));
  return info;
}

async function fillSearch(page, query) {
  // JS fill through shadow roots inside dialog
  const ok = await page.evaluate((q) => {
    const dlg = document.querySelector("ytcp-video-pick-dialog");
    const root = dlg || document;
    const walk = (r, d = 0) => {
      if (!r || d > 45) return null;
      for (const el of r.querySelectorAll ? r.querySelectorAll("input") : []) {
        const meta = `${el.getAttribute("aria-label") || ""}${el.id || ""}${el.placeholder || ""}`;
        if (/search/i.test(meta) || el.id === "search-yours" || el.type === "text" || el.type === "search") {
          el.focus();
          el.value = "";
          el.dispatchEvent(new Event("input", { bubbles: true }));
          el.value = q;
          el.dispatchEvent(new Event("input", { bubbles: true }));
          el.dispatchEvent(new Event("change", { bubbles: true }));
          return el.id || el.placeholder || meta.slice(0, 40) || "input";
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
    return walk(root) || "no_input";
  }, query);
  await sleep(500);
  // Also type via keyboard if we focused an input
  if (ok !== "no_input") {
    await page.keyboard.down("Meta");
    await page.keyboard.press("a");
    await page.keyboard.up("Meta");
    await page.keyboard.press("Backspace");
    await page.keyboard.type(query, { delay: 25 });
  }
  await sleep(2800);
  return ok;
}

async function clickYourVideosTab(page) {
  const hit = await page.evaluate(() => {
    const walk = (r, d = 0) => {
      if (!r || d > 45) return null;
      for (const el of r.querySelectorAll
        ? r.querySelectorAll("[role=tab],tp-yt-paper-tab,button,div")
        : []) {
        const t = (el.innerText || "").trim();
        if (/^(Your videos|Search YouTube)$/i.test(t)) {
          const b = el.getBoundingClientRect();
          if (b.width > 40 && b.height > 16 && b.y > 40 && b.y < 500) {
            return { x: b.x + b.width / 2, y: b.y + b.height / 2, t };
          }
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
    const dlg = document.querySelector("ytcp-video-pick-dialog") || document;
    return walk(dlg);
  });
  if (hit) {
    await page.mouse.click(hit.x, hit.y);
    await sleep(1200);
    return hit.t;
  }
  return null;
}

async function pickCard(page, relatedId, relatedTitle) {
  // First find a visible matching row, prefer the smallest height (the list row).
  const hit = await page.evaluate(
    ({ relatedTitle }) => {
      const needle = relatedTitle.toLowerCase();
      const keyWords = relatedTitle
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, " ")
        .split(/\s+/)
        .filter((w) => w.length >= 4)
        .slice(0, 4);
      const matches = [];
      const walk = (r, d = 0) => {
        if (!r || d > 50) return;
        for (const el of r.querySelectorAll
          ? r.querySelectorAll(
              "ytcp-entity-card,ytcp-video-list-cell-video,[role=option],ytcp-video-row,a,div,span"
            )
          : []) {
          const t = (el.innerText || "").replace(/\s+/g, " ").trim();
          if (!t || t.length < 8 || t.length > 220) continue;
          const tl = t.toLowerCase();
          const ok =
            tl.includes(needle.slice(0, 24)) ||
            keyWords.every((w) => tl.includes(w));
          if (!ok) continue;
          const b = el.getBoundingClientRect();
          if (b.width > 60 && b.height >= 28 && b.height <= 120 && b.y > 60 && b.y < 900) {
            matches.push({
              t: t.slice(0, 140),
              x: b.x + b.width / 2,
              y: b.y + b.height / 2,
              h: b.height,
              w: b.width,
            });
          }
        }
        for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) {
          if (el.shadowRoot) walk(el.shadowRoot, d + 1);
        }
      };
      const dlg = document.querySelector("ytcp-video-pick-dialog") || document;
      walk(dlg);
      matches.sort((a, b) => a.h - b.h || a.y - b.y);
      return matches[0] || null;
    },
    { relatedTitle }
  );
  if (!hit) return null;
  await page.mouse.click(hit.x, hit.y);
  await sleep(600);
  return hit.t;
}

async function clickSave(page) {
  return page.evaluate(() => {
    const walk = (r, d = 0) => {
      if (!r || d > 35) return null;
      for (const el of r.querySelectorAll ? r.querySelectorAll("button,ytcp-button,[role=button]") : []) {
        const t = (el.innerText || el.getAttribute("aria-label") || "").trim();
        if (/^Save$/i.test(t)) {
          const dis =
            el.disabled ||
            el.getAttribute("aria-disabled") === "true" ||
            el.classList.contains("disabled");
          if (!dis) {
            el.click();
            return "clicked";
          }
          return "disabled";
        }
      }
      for (const el of r.querySelectorAll ? r.querySelectorAll("*") : []) {
        if (el.shadowRoot) {
          const x = walk(el.shadowRoot, d + 1);
          if (x) return x;
        }
      }
      return null;
    };
    return walk(document);
  });
}

async function setRelated(page, relatedId, relatedTitle) {
  const before = await relatedChunk(page);
  if (relatedOk(before, relatedTitle, relatedId)) {
    return { action: "already_set", before };
  }
  const picker = await openPicker(page);
  if (!picker.open && !picker.dialog) {
    return { action: "picker_closed", before, picker };
  }
  await clickYourVideosTab(page);
  // Prefer the initial Your-videos grid (IDs return "No matching results").
  let search = "grid_first";
  let hit = await pickCard(page, relatedId, relatedTitle);
  if (!hit) {
    // Title search only — never search by video id in this picker.
    const q = relatedTitle.split(" ").slice(0, 5).join(" ");
    search = await fillSearch(page, q);
    hit = await pickCard(page, relatedId, relatedTitle);
  }
  if (!hit) {
    await page.keyboard.press("Escape").catch(() => {});
    return { action: "no_card", before, picker, search };
  }
  await sleep(900);
  const saved = await clickSave(page);
  await sleep(2800);
  return {
    action: saved === "clicked" ? "set_saved" : `picked:${saved}`,
    before,
    picker,
    search,
    hit,
  };
}

async function main() {
  fs.mkdirSync(EV, { recursive: true });
  const started = new Date().toISOString();
  const results = [];
  console.log(`J0280 v03 start ${started} only=${ONLY || "all"}`);

  const browser = await puppeteer.connect({ browserURL: CDP, defaultViewport: null });
  const page = await browser.newPage();
  await page.goto(`https://studio.youtube.com/channel/${HOS}`, {
    waitUntil: "domcontentloaded",
    timeout: 60000,
  });
  await sleep(2000);
  if (!page.url().includes(HOS)) {
    console.log("STOPPED WRONG_CHANNEL", page.url());
    await page.close();
    browser.disconnect();
    process.exit(2);
  }
  console.log("channel ok", page.url());

  for (const job of JOBS) {
    const row = {
      n: job.n,
      id: job.id,
      related_id: job.related_id,
      related_title: job.related_title,
      at: new Date().toISOString(),
    };
    console.log(`\n=== [${job.n}] ${job.id} -> ${job.related_id} ===`);
    try {
      await openEdit(page, job.id);
      const beforeChunk = await relatedChunk(page);
      row.before = { chunk: beforeChunk };
      await page.screenshot({
        path: path.join(EV, `${job.id}_v03_before.png`),
        fullPage: true,
      });
      if (relatedOk(beforeChunk, job.related_title, job.related_id)) {
        row.action = "already_set";
        row.after = row.before;
        row.ok = true;
        results.push(row);
        console.log("already_set", beforeChunk.slice(0, 80));
        continue;
      }
      const set = await setRelated(page, job.related_id, job.related_title);
      row.action = set.action;
      row.picker = set.picker || null;
      row.search = set.search || null;
      row.hit = set.hit || null;
      await page.screenshot({
        path: path.join(EV, `${job.id}_v03_mid.png`),
        fullPage: true,
      });
      await openEdit(page, job.id);
      const afterChunk = await relatedChunk(page);
      row.after = { chunk: afterChunk };
      await page.screenshot({
        path: path.join(EV, `${job.id}_v03_after.png`),
        fullPage: true,
      });
      row.ok = relatedOk(afterChunk, job.related_title, job.related_id);
      console.log(
        `action=${row.action} search=${row.search} ok=${row.ok} chunk=${JSON.stringify(
          afterChunk.slice(0, 120)
        )}`
      );
    } catch (e) {
      row.ok = false;
      row.error = `${e.name || "Error"}:${e.message}`;
      console.log("ERR", row.error);
    }
    results.push(row);
    fs.writeFileSync(
      path.join(EV, "RESULT.json"),
      JSON.stringify(
        { job: "J0280", version: "v03", started, updated: new Date().toISOString(), results },
        null,
        2
      ) + "\n"
    );
  }

  await page.close();
  browser.disconnect();
  const ended = new Date().toISOString();
  const passed = results.filter((r) => r.ok).length;
  const out = {
    job: "J0280",
    version: "v03",
    started,
    ended,
    passed,
    total: JOBS.length,
    results,
  };
  fs.writeFileSync(path.join(EV, "RESULT.json"), JSON.stringify(out, null, 2) + "\n");
  console.log(`\nDONE passed=${passed}/${JOBS.length} ended=${ended}`);
  process.exit(passed === JOBS.length ? 0 : 1);
}

main().catch((e) => {
  console.error("FATAL", e);
  process.exit(3);
});
