#!/usr/bin/env tsx
/**
 * HOS release contract — check every upload package BEFORE anything goes to YouTube.
 *
 *   npm run lint:package                      # every film's long package + Shorts release
 *   npm run lint:package -- --film 004        # one film
 *   npm run lint:package -- --json
 *
 * Reads, per film in 02_Video-Projects/NNN_*:
 *   11_Upload-Package/PACKAGE_MANIFEST.json   (the long)
 *   10_Shorts/SHORTS_RELEASE.json             (the week's Shorts; see the 004 one for the format)
 * Rules: src/lib/hos-contract/rules.ts (and STUDIO_PLAYBOOK.md §9). Exit 1 on any error.
 * A package whose long is already public is history and is skipped: audit it with
 * `npm run channel:audit` instead. An agent may not upload or schedule until this prints PASS.
 */
import fs from "fs";
import path from "path";
import { parseTagsFile, parseTitleAbcSheet } from "../src/lib/publishing/youtube-package";
import {
  isPublished,
  lintLongPackage,
  lintShortsRelease,
  type Finding,
  type ShortRelease,
} from "../src/lib/hos-contract/rules";

const REPO = path.resolve(__dirname, "..", "..");
const PROJECTS = path.join(REPO, "02_Video-Projects");
const SHORTS_LOG = path.join(REPO, "00_Brand", "Channel-Setup", "audits", "SHORTS_LOG.md");
const LIVE_VIDEOS = path.join(REPO, "00_Brand", "Channel-Setup", "audits", "LIVE_VIDEOS.json");

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? undefined : process.argv[i + 1];
}

function readJson(p: string): Record<string, unknown> {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function readIf(dir: string, rel: unknown): string {
  if (typeof rel !== "string" || !rel) return "";
  const p = path.resolve(dir, rel);
  return fs.existsSync(p) ? fs.readFileSync(p, "utf8").replace(/^﻿/, "").trim() : "";
}

type LiveRow = { id: string; title: string };

/** Titles already on the channel: LIVE_VIDEOS.json (written by channel:audit) + SHORTS_LOG.md. */
export function liveRows(): LiveRow[] {
  const rows: LiveRow[] = [];
  if (fs.existsSync(LIVE_VIDEOS)) {
    const data = JSON.parse(fs.readFileSync(LIVE_VIDEOS, "utf8")) as { videos?: LiveRow[] };
    rows.push(...(data.videos || []).map((v) => ({ id: v.id, title: v.title })));
  }
  if (fs.existsSync(SHORTS_LOG)) {
    for (const line of fs.readFileSync(SHORTS_LOG, "utf8").split("\n")) {
      const cells = line.split("|").map((c) => c.trim());
      const id = /`([A-Za-z0-9_-]{11})`/.exec(cells[2] || "")?.[1];
      if (id && cells[3] && !/private/i.test(line)) rows.push({ id, title: cells[3] });
    }
  }
  return rows;
}

type FilmPkg = {
  film: string;
  dir: string;
  manifestPath: string | null;
  manifest: Record<string, unknown> | null;
  releasePath: string | null;
};

function films(only?: string): FilmPkg[] {
  return fs
    .readdirSync(PROJECTS)
    .filter((d) => /^\d{3}_/.test(d) && (!only || d.startsWith(only)))
    .map((d) => {
      const dir = path.join(PROJECTS, d);
      const manifestPath = path.join(dir, "11_Upload-Package", "PACKAGE_MANIFEST.json");
      const releasePath = path.join(dir, "10_Shorts", "SHORTS_RELEASE.json");
      return {
        film: d.slice(0, 3),
        dir,
        manifestPath: fs.existsSync(manifestPath) ? manifestPath : null,
        manifest: fs.existsSync(manifestPath) ? readJson(manifestPath) : null,
        releasePath: fs.existsSync(releasePath) ? releasePath : null,
      };
    });
}

function longTitle(pkgDir: string, m: Record<string, unknown>): { title: string; abc: string[] } {
  let title = typeof m.title === "string" ? m.title : "";
  let abc = Array.isArray(m.titleAbc) ? (m.titleAbc as string[]) : [];
  if (!title || !abc.length) {
    const tdir = path.join(pkgDir, "Titles");
    const f = fs.existsSync(tdir) ? fs.readdirSync(tdir).find((n) => n.endsWith(".txt")) : null;
    if (f) {
      const parsed = parseTitleAbcSheet(fs.readFileSync(path.join(tdir, f), "utf8"));
      title = title || parsed.recommended || "";
      abc = abc.length ? abc : parsed.titles;
    }
  }
  return { title, abc: abc.length ? abc : title ? [title] : [] };
}

function main() {
  const now = new Date();
  const all = films();
  const selected = films(arg("film"));
  // A Short listed in a SHORTS_RELEASE.json is judged by its declared title (the contract);
  // channel:audit then fails any live title that doesn't match it yet.
  const declared = new Map<string, string>();
  for (const f of all) {
    if (!f.releasePath) continue;
    for (const s of (readJson(f.releasePath) as { shorts?: ShortRelease[] }).shorts || [])
      if (s.id) declared.set(s.id, s.title);
  }
  const live = liveRows().map((r) => ({ ...r, title: declared.get(r.id) ?? r.title }));
  const report: { target: string; status: "PASS" | "FAIL" | "SKIP"; findings: Finding[]; note?: string }[] = [];

  // Every title a long is testing, across all films: no Short may reuse one.
  const reserved: string[] = [];
  const longPublicAt: Record<string, string> = {};
  for (const f of all) {
    if (!f.manifest) continue;
    const pkgDir = path.dirname(f.manifestPath!);
    reserved.push(...longTitle(pkgDir, f.manifest).abc);
    if (typeof f.manifest.schedule === "string") longPublicAt[f.film] = f.manifest.schedule;
  }

  const releaseDays = new Map<string, string[]>();
  for (const f of all) {
    if (!f.releasePath) continue;
    const rel = readJson(f.releasePath) as { shorts?: ShortRelease[] };
    releaseDays.set(
      f.film,
      (rel.shorts || []).map((s) => s.airDate.slice(0, 10)),
    );
  }

  for (const f of selected) {
    if (f.manifest && f.manifestPath) {
      const pkgDir = path.dirname(f.manifestPath);
      const target = path.relative(REPO, f.manifestPath);
      if (isPublished(f.manifest, now)) {
        report.push({ target, status: "SKIP", findings: [], note: "long already public; use channel:audit" });
      } else {
        const { title, abc } = longTitle(pkgDir, f.manifest);
        let tags = Array.isArray(f.manifest.tags) ? (f.manifest.tags as string[]) : [];
        if (!tags.length) tags = parseTagsFile(readIf(pkgDir, f.manifest.tagsFile));
        const selfId = f.manifest.youtubeId as string | undefined;
        const findings = lintLongPackage({
          manifest: f.manifest,
          title,
          titleAbc: abc,
          tags,
          description: readIf(pkgDir, f.manifest.descriptionFile) || String(f.manifest.description || ""),
          liveTitles: live.filter((r) => r.id !== selfId).map((r) => r.title),
          now,
        });
        report.push({ target, status: findings.some((x) => x.severity === "error") ? "FAIL" : "PASS", findings });
      }
    }
    if (f.releasePath) {
      const target = path.relative(REPO, f.releasePath);
      const rel = readJson(f.releasePath) as { shorts?: ShortRelease[] };
      const upcoming = (rel.shorts || []).filter((s) => {
        const when = /T/.test(s.airDate) ? new Date(s.airDate) : new Date(`${s.airDate}T23:59:59Z`);
        return when.getTime() > now.getTime();
      });
      if (!upcoming.length) {
        report.push({ target, status: "SKIP", findings: [], note: "all Shorts already aired" });
        continue;
      }
      const ownIds = new Set(upcoming.map((s) => s.id).filter(Boolean));
      const otherDays = [...releaseDays.entries()].filter(([film]) => film !== f.film).flatMap(([, d]) => d);
      const findings = lintShortsRelease({
        shorts: upcoming,
        liveTitles: live.filter((r) => !ownIds.has(r.id)).map((r) => r.title),
        reservedTitles: reserved,
        longPublicAt,
        otherShortDays: otherDays,
      });
      report.push({ target, status: findings.some((x) => x.severity === "error") ? "FAIL" : "PASS", findings });
    }
  }

  if (process.argv.includes("--json")) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    for (const r of report) {
      console.log(`${r.status}  ${r.target}${r.note ? `  (${r.note})` : ""}`);
      for (const x of r.findings) console.log(`   ${x.severity === "error" ? "FAIL" : "warn"}  [${x.rule}] ${x.message}`);
    }
    if (!report.length) console.log("No packages found.");
  }
  process.exit(report.some((r) => r.status === "FAIL") ? 1 : 0);
}

main();
