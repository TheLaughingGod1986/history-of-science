import { describe, expect, it } from "vitest";
import {
  auditChannel,
  auditVideo,
  checkTags,
  checkNeighbours,
  checkTitle,
  lintLongPackage,
  lintShortsRelease,
  ukSlot,
  type ApiVideo,
} from "@/lib/hos-contract/rules";

const rules = (fs: { rule: string; severity: string }[], sev = "error") =>
  fs.filter((f) => f.severity === sev).map((f) => f.rule);

const goodManifest = {
  channel: "@HistoryOfScienceYT",
  madeForKids: false,
  alteredContent: true,
  premiere: false,
  privacy: "private",
  schedule: "2026-10-15T17:00:00.000Z", // Thu 18:00 BST
  captionsFile: "Captions/x.srt",
};

const longInput = (manifest: Record<string, unknown>, extra: Partial<Parameters<typeof lintLongPackage>[0]> = {}) => ({
  manifest,
  title: "What's Really Inside an Atom?",
  titleAbc: ["What's Really Inside an Atom?", "Why Is the Periodic Table in This Order?"],
  tags: ["atom", "periodic table", "rutherford", "moseley", "history of science"],
  description: "What's inside an atom? Mostly nothing.",
  liveTitles: ["How Did We Discover the Periodic Table?"],
  ...extra,
});

describe("UK slots", () => {
  it("reads BST and GMT correctly", () => {
    expect(ukSlot("2026-10-15T17:00:00Z")).toMatchObject({ weekday: "Thu", time: "18:00" });
    expect(ukSlot("2026-10-16T10:30:00Z").time).toBe("11:30");
    expect(ukSlot("2026-10-29T18:00:00Z")).toMatchObject({ weekday: "Thu", time: "18:00" }); // after clocks change
  });
});

describe("long package lint", () => {
  it("passes a correct package", () => {
    expect(rules(lintLongPackage(longInput(goodManifest)))).toEqual([]);
  });
  it("fails Made for Kids missing or true (HOS 004 went up as Made for Kids)", () => {
    const { madeForKids: _drop, ...noKidsFlag } = goodManifest;
    expect(rules(lintLongPackage(longInput(noKidsFlag)))).toContain("audience");
    expect(rules(lintLongPackage(longInput({ ...goodManifest, madeForKids: true })))).toContain("audience");
  });
  it("fails a Premiere and a missing AI disclosure", () => {
    const r = rules(lintLongPackage(longInput({ ...goodManifest, premiere: { type: "premiere" }, alteredContent: undefined })));
    expect(r).toEqual(expect.arrayContaining(["premiere", "ai-disclosure"]));
  });
  it("fails the wrong slot (HOS 004 Shorts went in at 00:15)", () => {
    expect(rules(lintLongPackage(longInput({ ...goodManifest, schedule: "2026-10-15T23:15:00Z" })))).toContain("schedule.slot");
    expect(rules(lintLongPackage(longInput({ ...goodManifest, schedule: "2026-10-16T17:00:00Z" })))).toContain("schedule.slot");
  });
  it("fails a /go/ link with no affiliate, and a T&C title that is already live", () => {
    const r = rules(
      lintLongPackage(
        longInput(goodManifest, {
          description: "Buy it https://x/go/book",
          titleAbc: ["What's Really Inside an Atom?", "How small can you cut gold?"],
          liveTitles: ["How Small Can You Cut Gold?"],
        }),
      ),
    );
    expect(r).toEqual(expect.arrayContaining(["description.go-link", "title.duplicate-live"]));
  });
});

describe("titles and tags", () => {
  it("rejects hashtags and other channels", () => {
    expect(rules(checkTitle("What's the smallest piece of gold? #shorts"))).toContain("title.hashtag");
    expect(rules(checkTags(["atoms", "crash course", "hank green", "periodic table", "gold"]))).toContain("tags.other-channel");
  });
  it("warns on tag count but passes subject-only tags", () => {
    expect(rules(checkTags(["a", "b"]), "warn")).toContain("tags.count");
    expect(rules(checkTags(["joseph lister", "carbolic spray", "germ theory", "surgery", "history of science"]))).toEqual([]);
  });
});

describe("Shorts release lint", () => {
  const base = {
    liveTitles: ["The first X-ray showed a wedding ring"],
    reservedTitles: ["How Small Can You Cut Gold?"],
    longPublicAt: { "004": "2026-10-15T17:00:00Z" },
  };
  const s = (over: Record<string, unknown>) => ({
    title: "The spray that stopped surgery killing patients",
    airDate: "2026-10-20T10:30:00Z",
    promotes: "001",
    relatedVideoId: "_C92tIJCk8A",
    tags: ["joseph lister", "carbolic spray", "germ theory", "surgery", "history of science"],
    madeForKids: false,
    alteredContent: true,
    ...over,
  });
  it("passes a clean week", () => {
    expect(rules(lintShortsRelease({ ...base, shorts: [s({})] }))).toEqual([]);
  });
  it("catches a duplicate live Short and a long's test title", () => {
    const r = rules(
      lintShortsRelease({
        ...base,
        shorts: [s({ title: "The first X-ray showed a wedding ring" }), s({ title: "How small can you cut gold?", airDate: "2026-10-16T10:30:00Z" })],
      }),
    );
    expect(r).toEqual(expect.arrayContaining(["title.duplicate-live", "title.duplicate-test"]));
  });
  it("catches midnight scheduling, two in a day, and airing before the long", () => {
    const r = rules(
      lintShortsRelease({
        ...base,
        shorts: [
          s({ airDate: "2026-10-15T23:00:00Z", promotes: "004" }),
          s({ airDate: "2026-10-18T10:30:00Z", title: "A" + "b".repeat(10) }),
          s({ airDate: "2026-10-18T10:30:00Z", title: "C" + "d".repeat(10) }),
        ],
      }),
    );
    expect(r).toEqual(expect.arrayContaining(["schedule.slot", "schedule.one-a-day"]));
    const early = rules(lintShortsRelease({ ...base, shorts: [s({ airDate: "2026-10-15T10:30:00Z", promotes: "004" })] }));
    expect(early).toContain("schedule.before-long");
  });
});

describe("channel audit", () => {
  const good: ApiVideo = {
    id: "GHZDsiH7L7A",
    snippet: {
      title: "What's Really Inside an Atom?",
      tags: ["atom", "periodic table", "rutherford", "moseley", "history of science"],
      categoryId: "27",
      defaultLanguage: "en-GB",
      defaultAudioLanguage: "en-GB",
      liveBroadcastContent: "none",
      channelId: "UCXp7HkBIl1LgaznXuZHJyRg",
    },
    status: {
      privacyStatus: "private",
      publishAt: "2026-10-15T17:00:00Z",
      madeForKids: false,
      selfDeclaredMadeForKids: false,
      containsSyntheticMedia: true,
      embeddable: true,
      license: "youtube",
    },
    contentDetails: { duration: "PT8M45S" },
  };
  it("passes a correct video", () => {
    expect(rules(auditVideo(good))).toEqual([]);
  });
  it("flags Made for Kids, no AI label, Science category, unset language, Premiere", () => {
    // Data API omits containsSyntheticMedia even when Studio shows Yes — warn only, confirm by eye.
    const { containsSyntheticMedia: _drop, ...statusNoAiLabel } = good.status!;
    const findings = auditVideo({
      ...good,
      snippet: { ...good.snippet, categoryId: "28", defaultLanguage: undefined, liveBroadcastContent: "upcoming" },
      status: { ...statusNoAiLabel, madeForKids: true },
    });
    const errors = rules(findings);
    expect(errors).toEqual(
      expect.arrayContaining(["audience", "category", "language.title", "premiere"]),
    );
    expect(errors).not.toContain("ai-disclosure");
    expect(findings.filter((f) => f.rule === "ai-disclosure")[0]?.severity).toBe("warn");
  });
  it("errors when altered/synthetic is explicitly No", () => {
    expect(
      rules(
        auditVideo({
          ...good,
          status: { ...good.status, containsSyntheticMedia: false },
        }),
      ),
    ).toContain("ai-disclosure");
  });
  it("warns (not errors) when Data API omits containsSyntheticMedia", () => {
    const { containsSyntheticMedia: _drop, ...status } = good.status!;
    const findings = auditVideo({ ...good, status });
    expect(findings.filter((f) => f.severity === "error").map((f) => f.rule)).not.toContain("ai-disclosure");
    expect(findings.filter((f) => f.rule === "ai-disclosure")[0]?.severity).toBe("warn");
  });
  it("flags a Short scheduled at midnight, and two Shorts on one day, and duplicate titles", () => {
    const short = (id: string, when: string, title: string): ApiVideo => ({
      ...good,
      id,
      snippet: { ...good.snippet, title },
      status: { ...good.status, publishAt: when },
      contentDetails: { duration: "PT25S" },
    });
    expect(rules(auditVideo(short("a", "2026-10-15T23:15:00Z", "x".repeat(12))))).toContain("schedule.slot");
    const cross = auditChannel([
      short("a", "2026-10-18T10:30:00Z", "One title here"),
      short("b", "2026-10-18T10:30:00Z", "Another title"),
      { ...short("c", "2026-10-20T10:30:00Z", "One title here") },
    ]);
    expect(rules(cross.get("a") || [])).toEqual(expect.arrayContaining(["schedule.one-a-day", "title.duplicate-live"]));
    expect(rules(cross.get("c") || [])).toContain("title.duplicate-live");
  });
});

describe("neighbours (HOS 002: 55.6% of suggested views from TED-Ed's Mendeleev video; ≥3 at 1M+)", () => {
  const neighbours = {
    phrases: ["atom"],
    videos: [
      { id: "yQP4UJhNn0I", channel: "TED-Ed", title: "Just How Small is an Atom?", views: 7_960_719 },
      { id: "a1", channel: "Kurzgesagt – In a Nutshell", title: "The Atom", views: 3_100_000 },
      { id: "a2", channel: "Veritasium", title: "What's Inside an Atom?", views: 2_400_000 },
    ],
  };
  const base = {
    neighbours,
    title: "What's Really Inside an Atom?",
    titleAbc: ["What's Really Inside an Atom?", "How Small Can You Cut Gold?"],
    tags: ["atom", "rutherford"],
    description: "What's inside an atom? Mostly nothing.\n\nChapters",
    required: true,
  };
  it("passes a long that shares the neighbour's words, and warns on a T&C title that drops them", () => {
    const f = checkNeighbours(base);
    expect(rules(f)).toEqual([]);
    expect(rules(f, "warn")).toEqual(["neighbours.tc-title"]);
  });
  it("fails a new film with no neighbours block; an older film only warns", () => {
    expect(rules(checkNeighbours({ ...base, neighbours: undefined }))).toEqual(["neighbours.missing"]);
    expect(rules(checkNeighbours({ ...base, neighbours: undefined, required: false }), "warn")).toEqual(["neighbours.missing"]);
  });
  it("fails when fewer than 3 neighbours have 1M+ views", () => {
    const r = checkNeighbours({
      ...base,
      neighbours: {
        phrases: ["atom"],
        videos: [
          { id: "yQP4UJhNn0I", channel: "TED-Ed", title: "Just How Small is an Atom?", views: 7_960_719 },
          { id: "a1", channel: "SciShow", title: "Atoms", views: 500_000 },
        ],
      },
    });
    expect(rules(r)).toContain("neighbours.size");
  });
  it("fails a title, description or tags without the phrase, and a small or non-TED neighbour pool", () => {
    const r = checkNeighbours({
      ...base,
      title: "How Small Can You Cut Gold?",
      description: "Cut gold in half.",
      tags: ["gold"],
      neighbours: { phrases: ["atom"], videos: [{ id: "x", channel: "SciShow", title: "Atoms", views: 5000 }] },
    });
    expect(rules(r)).toEqual(
      expect.arrayContaining(["neighbours.title", "neighbours.description", "neighbours.tags", "neighbours.size"]),
    );
    expect(rules(r, "warn")).toContain("neighbours.ted");
  });
});
