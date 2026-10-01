/**
 * HOS release contract — the channel rules as code (30 Sep 2026).
 *
 * The docs in force (AGENTS.md → STUDIO_PLAYBOOK.md §9, THUMBNAIL_AND_TITLE_RULES.md,
 * HOS_STRATEGY.md) say what the rules are. This module makes the machine-checkable ones fail:
 *   - lintLongPackage / lintShortsRelease: before anything is uploaded (scripts/package-lint.ts)
 *   - auditVideo / auditChannel: what is actually on YouTube (scripts/channel-audit.ts)
 * Every rule here traces to a real slip on HOS 004 (Made for Kids, wrong times, duplicate
 * Short, mixed tags, competitor tags, Premiere). Change a rule here and in the doc together.
 */
import { formatInTimeZone } from "date-fns-tz";

export const HOS_CHANNEL_ID = "UCXp7HkBIl1LgaznXuZHJyRg";
export const HOS_HANDLE = "@HistoryOfScienceYT";
export const UK_TZ = "Europe/London";
export const CATEGORY_EDUCATION = "27";
export const LANGUAGE = "en-GB";
export const LONG_SLOT = { weekday: "Thu", time: "18:00" } as const;
export const SHORT_SLOT_TIME = "11:30";
export const TITLE_SOFT_MAX = 60;
export const TITLE_HARD_MAX = 70;
export const TAGS_MIN = 5;
export const TAGS_MAX = 8;
export const SHORT_MAX_SECONDS = 40;

/** Other channels and creators. Naming them in tags or titles is misleading metadata. */
export const BANNED_NAMES = [
  "crash course",
  "crashcourse",
  "vlogbrothers",
  "hank green",
  "john green",
  "ted-ed",
  "ted ed",
  "teded",
  "kurzgesagt",
  "veritasium",
  "vsauce",
  "scishow",
  "pbs",
  "pbs space time",
  "bbc",
  "national geographic",
  "khan academy",
  "mark rober",
  "startalk",
  "neil degrasse tyson",
  "bobbybroccoli",
  "animistry",
  "heyhistorically",
  "freesciencelessons",
  "cognito",
  "orbit with ben",
  "opptiai",
];

export type Severity = "error" | "warn";
export type Finding = { severity: Severity; rule: string; message: string };

const err = (rule: string, message: string): Finding => ({ severity: "error", rule, message });
const warn = (rule: string, message: string): Finding => ({ severity: "warn", rule, message });

export function normTitle(t: string): string {
  return t
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

export function ukSlot(iso: string | Date): { weekday: string; time: string; date: string } {
  const d = typeof iso === "string" ? new Date(iso) : iso;
  return {
    weekday: formatInTimeZone(d, UK_TZ, "EEE"),
    time: formatInTimeZone(d, UK_TZ, "HH:mm"),
    date: formatInTimeZone(d, UK_TZ, "yyyy-MM-dd"),
  };
}

export function checkTitle(
  title: string,
  opts: { liveTitles?: string[]; reservedTitles?: string[]; label?: string } = {},
): Finding[] {
  const f: Finding[] = [];
  const label = opts.label ? `${opts.label}: ` : "";
  if (!title.trim()) return [err("title.missing", `${label}title is empty`)];
  if (title.includes("#")) f.push(err("title.hashtag", `${label}"${title}" has a hashtag`));
  if (title.length > TITLE_HARD_MAX)
    f.push(err("title.length", `${label}"${title}" is ${title.length} chars (max ${TITLE_HARD_MAX})`));
  else if (title.length > TITLE_SOFT_MAX)
    f.push(warn("title.length", `${label}"${title}" is ${title.length} chars (aim ≤ ${TITLE_SOFT_MAX})`));
  const low = title.toLowerCase();
  for (const name of BANNED_NAMES) {
    if (new RegExp(`\\b${name.replace(/[-]/g, "[- ]?")}\\b`).test(low))
      f.push(err("title.other-channel", `${label}"${title}" names another channel (${name})`));
  }
  const n = normTitle(title);
  if ((opts.liveTitles || []).some((t) => normTitle(t) === n))
    f.push(err("title.duplicate-live", `${label}"${title}" is already the title of a live video`));
  if ((opts.reservedTitles || []).some((t) => normTitle(t) === n))
    f.push(
      err("title.duplicate-test", `${label}"${title}" is a title a long is testing (Test & Compare)`),
    );
  return f;
}

export function checkTags(tags: string[], label = ""): Finding[] {
  const f: Finding[] = [];
  const p = label ? `${label}: ` : "";
  if (tags.length < TAGS_MIN || tags.length > TAGS_MAX)
    f.push(warn("tags.count", `${p}${tags.length} tags (want ${TAGS_MIN}–${TAGS_MAX})`));
  for (const tag of tags) {
    const low = tag.toLowerCase().trim();
    if (low.includes("#")) f.push(err("tags.hashtag", `${p}tag "${tag}" has a #`));
    for (const name of BANNED_NAMES) {
      if (low === name || low.includes(name))
        f.push(err("tags.other-channel", `${p}tag "${tag}" names another channel (${name})`));
    }
  }
  return f;
}

export type LongPackageInput = {
  manifest: Record<string, unknown>;
  title: string;
  titleAbc: string[];
  tags: string[];
  description: string;
  liveTitles: string[];
  now?: Date;
  /** Films from 005 on must name their neighbours; older packages only warn. */
  requireNeighbours?: boolean;
};

/**
 * Neighbours (1 Oct 2026, from HOS 002: 108 of 126 views were "suggested", 55.6% of them from
 * TED-Ed's Mendeleev video). Ben evening same day: every future film needs a pool of big
 * education neighbours so YouTube can recommend it. A long names those videos
 * (`tools/neighbours.py`) and uses their subject words (never channel names): the title,
 * the description's opening and the tags each hold one of `neighbours.phrases`.
 */
export type Neighbours = {
  phrases?: string[];
  checked?: string;
  videos?: { id: string; channel: string; title: string; views?: number }[];
};

export const NEIGHBOUR_MIN_VIEWS = 1_000_000;
/** At least this many education neighbours must have NEIGHBOUR_MIN_VIEWS+ (Ben, 1 Oct 2026). */
export const NEIGHBOUR_MIN_COUNT = 3;
const TED_CHANNELS = new Set(["TED-Ed", "TED", "TEDx Talks"]);

export function checkNeighbours(input: {
  neighbours: unknown;
  title: string;
  titleAbc: string[];
  tags: string[];
  description: string;
  required: boolean;
}): Finding[] {
  const f: Finding[] = [];
  const n = input.neighbours as Neighbours | undefined;
  const missing = input.required ? err : warn;
  if (!n || typeof n !== "object") {
    f.push(missing("neighbours.missing", "no neighbours block: run tools/neighbours.py --manifest (STUDIO_PLAYBOOK.md §2)"));
    return f;
  }
  const phrases = (n.phrases || []).map((p) => p.toLowerCase().trim()).filter(Boolean);
  const videos = n.videos || [];
  if (!phrases.length) f.push(missing("neighbours.phrases", "neighbours.phrases is empty"));
  if (!videos.length) f.push(missing("neighbours.videos", "neighbours.videos is empty"));
  else {
    const big = videos.filter((v) => (v.views ?? 0) >= NEIGHBOUR_MIN_VIEWS);
    if (big.length < NEIGHBOUR_MIN_COUNT)
      f.push(
        missing(
          "neighbours.size",
          `need ${NEIGHBOUR_MIN_COUNT} education neighbours with ${NEIGHBOUR_MIN_VIEWS.toLocaleString("en-GB")}+ views; found ${big.length}`,
        ),
      );
    if (!videos.some((v) => TED_CHANNELS.has(v.channel)))
      f.push(warn("neighbours.ted", "no TED-Ed / TED neighbour; prefer a topic that has one"));
  }
  if (!phrases.length) return f;
  const has = (s: string) => phrases.some((p) => s.toLowerCase().includes(p));
  if (!has(input.title))
    f.push(missing("neighbours.title", `title "${input.title}" holds none of: ${phrases.join(", ")}`));
  for (const t of input.titleAbc)
    if (normTitle(t) !== normTitle(input.title) && !has(t))
      f.push(warn("neighbours.tc-title", `T&C title "${t}" holds none of: ${phrases.join(", ")}`));
  const opening = input.description.split(/\n/).filter((l) => l.trim()).slice(0, 2).join(" ");
  if (!has(opening))
    f.push(missing("neighbours.description", "description's first two lines hold no neighbour phrase"));
  if (!input.tags.some(has)) f.push(missing("neighbours.tags", "no tag holds a neighbour phrase"));
  return f;
}

/** Published packages are history: audit them with channel-audit, not here. */
export function isPublished(manifest: Record<string, unknown>, now = new Date()): boolean {
  const schedule = typeof manifest.schedule === "string" ? new Date(manifest.schedule) : null;
  const id = manifest.youtubeId as string | undefined;
  if (!id) return false;
  return !schedule || schedule.getTime() <= now.getTime();
}

export function lintLongPackage(input: LongPackageInput): Finding[] {
  const m = input.manifest;
  const f: Finding[] = [];
  if (m.channel != null && m.channel !== HOS_HANDLE)
    f.push(err("channel", `channel is ${String(m.channel)}, must be ${HOS_HANDLE}`));
  if (m.madeForKids !== false)
    f.push(err("audience", "madeForKids must be explicitly false (never Made for Kids)"));
  if (m.premiere && m.premiere !== false)
    f.push(err("premiere", "premiere must be false (normal publish, never a Premiere)"));
  if ((m.privacy ?? "private") !== "private")
    f.push(err("privacy", `privacy is ${String(m.privacy)}; upload private and schedule`));
  if (m.alteredContent !== true)
    f.push(err("ai-disclosure", "alteredContent must be true (AI visuals + AI voice)"));
  if ((m.language ?? LANGUAGE) !== LANGUAGE)
    f.push(err("language", `language must be ${LANGUAGE}`));
  if ((m.categoryId ?? CATEGORY_EDUCATION) !== CATEGORY_EDUCATION)
    f.push(err("category", `categoryId must be ${CATEGORY_EDUCATION} (Education)`));
  if (typeof m.schedule !== "string") {
    f.push(err("schedule.missing", "schedule (ISO, UTC) is required"));
  } else {
    const s = ukSlot(m.schedule);
    if (s.weekday !== LONG_SLOT.weekday || s.time !== LONG_SLOT.time)
      f.push(
        err(
          "schedule.slot",
          `schedule is ${s.weekday} ${s.date} ${s.time} UK; longs go out Thu 18:00 UK`,
        ),
      );
    if (input.now && new Date(m.schedule).getTime() < input.now.getTime() && !m.youtubeId)
      f.push(err("schedule.past", "schedule is in the past"));
  }
  const reserved = input.titleAbc.filter((t) => normTitle(t) !== normTitle(input.title));
  f.push(...checkTitle(input.title, { liveTitles: input.liveTitles, label: "title" }));
  for (const t of reserved) f.push(...checkTitle(t, { liveTitles: input.liveTitles, label: "T&C title" }));
  f.push(...checkTags(input.tags));
  if (/\/go\//.test(input.description) && !m.affiliate)
    f.push(err("description.go-link", "/go/ link in a description with no affiliate product"));
  if (!input.description.trim()) f.push(err("description.missing", "description is empty"));
  if (!m.captionsFile) f.push(warn("captions", "no captionsFile (captions from the script)"));
  f.push(
    ...checkNeighbours({
      neighbours: m.neighbours,
      title: input.title,
      titleAbc: input.titleAbc,
      tags: input.tags,
      description: input.description,
      required: input.requireNeighbours ?? false,
    }),
  );
  return f;
}

export type ShortRelease = {
  id?: string;
  title: string;
  airDate: string; // ISO with time, or YYYY-MM-DD (then 11:30 UK assumed)
  promotes: string; // film number, e.g. "004"
  promotesVideoId?: string | null;
  relatedVideoId?: string | null;
  tags?: string[];
  madeForKids?: boolean;
  alteredContent?: boolean;
  durationSeconds?: number;
  cover?: string;
};

export function lintShortsRelease(input: {
  shorts: ShortRelease[];
  liveTitles: string[];
  reservedTitles: string[];
  longPublicAt?: Record<string, string>; // film -> ISO of the long going public
  otherShortDays?: string[]; // UK dates already taken by other scheduled Shorts
}): Finding[] {
  const f: Finding[] = [];
  const days = new Map<string, string>();
  for (const d of input.otherShortDays || []) days.set(d, "another release");
  for (const s of input.shorts) {
    const label = s.title || s.id || "short";
    if (s.madeForKids !== false) f.push(err("audience", `${label}: madeForKids must be false`));
    if (s.alteredContent !== true) f.push(err("ai-disclosure", `${label}: alteredContent must be true`));
    f.push(...checkTitle(s.title, { liveTitles: input.liveTitles, reservedTitles: input.reservedTitles, label }));
    f.push(...checkTags(s.tags || [], label));
    if (s.durationSeconds != null && s.durationSeconds >= SHORT_MAX_SECONDS)
      f.push(err("short.length", `${label}: ${s.durationSeconds}s (a Short is under ${SHORT_MAX_SECONDS}s)`));
    const iso = /T/.test(s.airDate) ? s.airDate : null;
    const slot = iso ? ukSlot(iso) : { date: s.airDate, time: SHORT_SLOT_TIME, weekday: "" };
    if (slot.time !== SHORT_SLOT_TIME)
      f.push(err("schedule.slot", `${label}: ${slot.date} ${slot.time} UK; Shorts go out 11:30 UK`));
    if (days.has(slot.date))
      f.push(err("schedule.one-a-day", `${label}: ${slot.date} already has a Short (${days.get(slot.date)})`));
    days.set(slot.date, label);
    const publicAt = input.longPublicAt?.[s.promotes];
    if (publicAt && iso && new Date(iso).getTime() <= new Date(publicAt).getTime())
      f.push(err("schedule.before-long", `${label}: airs before its long (${s.promotes}) is public`));
    if (!s.relatedVideoId)
      f.push(
        warn(
          "related",
          `${label}: Related video not set yet (set it to the ${s.promotes} long once that long is public)`,
        ),
      );
  }
  return f;
}

/** YouTube Data API `videos` resource, the fields the audit reads. */
export type ApiVideo = {
  id: string;
  snippet?: {
    title?: string;
    tags?: string[];
    categoryId?: string;
    defaultLanguage?: string;
    defaultAudioLanguage?: string;
    liveBroadcastContent?: string;
    channelId?: string;
  };
  status?: {
    privacyStatus?: string;
    publishAt?: string;
    madeForKids?: boolean;
    selfDeclaredMadeForKids?: boolean;
    containsSyntheticMedia?: boolean;
    embeddable?: boolean;
    license?: string;
  };
  contentDetails?: { duration?: string };
};

export function isoDurationSeconds(d?: string): number | null {
  if (!d) return null;
  const m = /^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/.exec(d);
  if (!m) return null;
  return Number(m[1] || 0) * 3600 + Number(m[2] || 0) * 60 + Number(m[3] || 0);
}

export function isShort(v: ApiVideo): boolean {
  const s = isoDurationSeconds(v.contentDetails?.duration);
  return s != null && s <= 60;
}

export function auditVideo(v: ApiVideo): Finding[] {
  const f: Finding[] = [];
  const sn = v.snippet || {};
  const st = v.status || {};
  const kind = isShort(v) ? "Short" : "long";
  if (sn.channelId && sn.channelId !== HOS_CHANNEL_ID)
    f.push(err("channel", `on channel ${sn.channelId}, not HOS`));
  if (st.madeForKids || st.selfDeclaredMadeForKids)
    f.push(err("audience", "marked Made for Kids (no comments, notifications, end screens; cut reach)"));
  // videos.list does not return containsSyntheticMedia even when Studio shows Altered YES
  // and even after videos.update sets it. Fail only on an explicit No; otherwise confirm in Studio.
  if (st.containsSyntheticMedia === false)
    f.push(err("ai-disclosure", "altered/synthetic content is No"));
  else if (st.containsSyntheticMedia !== true)
    f.push(
      warn(
        "ai-disclosure",
        "Data API omits altered/synthetic — confirm Yes in Studio (Altered content)",
      ),
    );
  if (sn.categoryId && sn.categoryId !== CATEGORY_EDUCATION)
    f.push(err("category", `category ${sn.categoryId}, want ${CATEGORY_EDUCATION} (Education)`));
  if (sn.defaultLanguage !== LANGUAGE)
    f.push(err("language.title", `title/description language ${sn.defaultLanguage ?? "unset"}, want ${LANGUAGE}`));
  if (sn.defaultAudioLanguage !== LANGUAGE)
    f.push(err("language.audio", `video language ${sn.defaultAudioLanguage ?? "unset"}, want ${LANGUAGE}`));
  if (sn.liveBroadcastContent === "upcoming" || sn.liveBroadcastContent === "live")
    f.push(err("premiere", "set up as a Premiere/live; normal publish only"));
  if (st.embeddable === false) f.push(warn("embeddable", "embedding is off"));
  if (st.license && st.license !== "youtube") f.push(warn("license", `licence ${st.license}`));
  f.push(...checkTitle(sn.title || "", { label: kind }).filter((x) => x.rule !== "title.length"));
  f.push(...checkTags(sn.tags || [], kind));
  if (kind === "Short") {
    const secs = isoDurationSeconds(v.contentDetails?.duration);
    if (secs != null && secs >= SHORT_MAX_SECONDS)
      f.push(warn("short.length", `${secs}s long (Shorts should be under ${SHORT_MAX_SECONDS}s)`));
  }
  if (st.privacyStatus === "private" && st.publishAt) {
    const s = ukSlot(st.publishAt);
    if (kind === "long" && (s.weekday !== LONG_SLOT.weekday || s.time !== LONG_SLOT.time))
      f.push(err("schedule.slot", `scheduled ${s.weekday} ${s.date} ${s.time} UK; longs go out Thu 18:00 UK`));
    if (kind === "Short" && s.time !== SHORT_SLOT_TIME)
      f.push(err("schedule.slot", `scheduled ${s.date} ${s.time} UK; Shorts go out 11:30 UK`));
  }
  return f;
}

/** Cross-video checks: duplicate public titles, two Shorts on one day, Shorts before their long. */
export function auditChannel(videos: ApiVideo[]): Map<string, Finding[]> {
  const out = new Map<string, Finding[]>();
  const add = (id: string, x: Finding) => out.set(id, [...(out.get(id) || []), x]);
  const visible = videos.filter(
    (v) => v.status?.privacyStatus !== "private" || Boolean(v.status?.publishAt),
  );
  const byTitle = new Map<string, ApiVideo[]>();
  for (const v of visible) {
    const k = normTitle(v.snippet?.title || "");
    byTitle.set(k, [...(byTitle.get(k) || []), v]);
  }
  for (const group of byTitle.values()) {
    if (group.length > 1)
      for (const v of group)
        add(v.id, err("title.duplicate-live", `same title as ${group.filter((g) => g !== v).map((g) => g.id).join(", ")}`));
  }
  const shortDays = new Map<string, ApiVideo[]>();
  for (const v of visible.filter(isShort)) {
    const when = v.status?.publishAt;
    if (!when) continue;
    const d = ukSlot(when).date;
    shortDays.set(d, [...(shortDays.get(d) || []), v]);
  }
  for (const [d, group] of shortDays)
    if (group.length > 1)
      for (const v of group) add(v.id, err("schedule.one-a-day", `${group.length} Shorts scheduled on ${d}`));
  return out;
}

/** Things the Data API cannot read: a person or agent checks these in Studio every time. */
export const STUDIO_ONLY_CHECKS = [
  "AI disclosure = Yes (confirm by eye)",
  "Every video: Altered / synthetic content = Yes (Data API videos.list omits this field)",
  "Shorts: Related video points at the long it promotes (set at 18:05 on the long's day if needed)",
  "Longs: end screen (related long + Subscribe) and 2 cards, none in the first minute",
  "Longs: Test & Compare (title+thumbnail pairs, or thumbnails only) running after publish",
  "Longs: pinned comment posted as the channel",
  "Paid promotion = No; education fields (concept overview, secondary, GCSE subject)",
  "Automatic places off; comments on (Basic moderation); Studio time zone London",
];
